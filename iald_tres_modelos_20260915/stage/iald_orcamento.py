"""Persistent preflight reservations for every external inference call.

Reserve an upper bound before sending. Settle against provider usage, or keep
the bound when a stream is interrupted. SQLite serializes concurrent processes.

REVISÃO (14/09/2026, noite — sessão Claude da Central; revisões ordem-régua 4 e 5 e
segurança MÉDIO 2, reproduzidas em scratchpad\\revisor_ordem\\simula_reserva.py):
  1. A reserva é pelo tamanho ESTIMADO do payload real (mensagens + ferramentas: o maior
     entre o contador de tokens e a conta por caracteres com CPT 2,91), com margem de 15%,
     mais a saída máxima. Antes reservava a janela inteira: ~US$ 0,0096 por chamada no
     gpt-5.6-luna contra US$ 0,02 por dia do plano gratuito (2 a 4 chamadas por dia).
  2. Reserva ainda 'reserved' de DIA ANTERIOR (o processo morreu no meio do stream) é
     liquidada pelo teto AO INICIAR, e a checagem soma só o dia corrente. Antes, duas
     reservas órfãs de 14/09 ainda recusavam a mesma conta em 20/09 (reproduzido).
  3. Chamada interrompida sem `usage` é liquidada pela ESTIMATIVA (entrada estimada +
     saída vista), nunca acima da reserva — não mais pela reserva cheia.
  4. Cobrança do provedor ACIMA da reserva continua fail-closed, sem travar todos para
     sempre: a conta (usuário ou chave da cota) que passou fica pausada até a renovação
     do dia (UTC); as demais seguem com a reserva multiplicada pela maior razão
     cobrado/reservado do dia; a partir da 3ª ocorrência no mesmo dia o motor para para
     TODOS até a renovação. A marca antiga `blocked` (permanente) de um banco anterior é
     convertida numa pausa global do dia em que o código novo a encontra.
  5. BudgetError carrega `bloqueado_por` e os textos ao público não mandam pedir nada ao
     operador (contrato do aviso "limite").
"""
from datetime import datetime, timezone
from contextlib import contextmanager
import json
import math
from pathlib import Path
import sqlite3
import uuid

from iald_memoria_canonica import payload_tokens
from iald_motores import CPT


# Margem sobre a entrada estimada (ordem de 14/09/2026, noite: "com margem de 15%").
RESERVATION_MARGIN = 1.15
# A partir desta quantidade de cobranças acima da reserva no MESMO dia, o motor para para todos.
EXCEEDED_GLOBAL_LIMIT = 3
# Teto do multiplicador de segurança (uma razão absurda não vira reserva infinita).
MAX_SAFETY_FACTOR = 50.0

MSG_LIMITES_INVALIDOS = "Limites de uso inválidos; envio bloqueado."
MSG_CONTA_DIA = ("O saldo diário desta conta não cobre com segurança outra resposta agora. "
                 "O limite renova à meia-noite UTC (21h em Brasília).")
MSG_GLOBAL = ("A IALD atingiu o limite diário de uso do serviço externo. O limite renova "
              "à meia-noite UTC (21h em Brasília).")
MSG_GRUPO_GRATUITO = ("A IALD atingiu o limite diário do uso gratuito de todas as contas. O "
                      "limite renova à meia-noite UTC (21h em Brasília).")
MSG_CONFERENCIA_CONTA = ("O custo de uma resposta desta conta passou do previsto e o uso ficou "
                         "pausado para conferência até a renovação diária (meia-noite UTC, 21h em Brasília).")
MSG_CONFERENCIA_GLOBAL = ("O serviço externo está pausado para conferência de cobrança até a "
                          "renovação diária (meia-noite UTC, 21h em Brasília).")
MSG_JANELA = "A memória, a conversa e a resposta excedem a janela configurada; nada foi enviado."


class BudgetError(ValueError):
    """Recusa do controle de gasto. `bloqueado_por` diz qual trava recusou (contrato do aviso
    "limite": usd_dia, global, global_gratuito, conferencia, razao, janela)."""

    def __init__(self, message="", bloqueado_por="razao"):
        super().__init__(message)
        self.bloqueado_por = bloqueado_por


class WindowError(BudgetError):
    """O pedido não cabe na janela configurada: não é cota, é pedido grande demais."""

    def __init__(self, message=MSG_JANELA):
        super().__init__(message, "janela")


def _without_images(payload):
    """(payload com as imagens trocadas por marcador, quantidade de imagens)."""
    messages, images = [], 0
    for message in payload.get("messages", []) or []:
        content = message.get("content") if isinstance(message, dict) else None
        if isinstance(content, list):
            parts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    images += 1
                    parts.append({"type": "text", "text": "[image input accounted separately]"})
                else:
                    parts.append(part)
            message = {**message, "content": parts}
        messages.append(message)
    return {**payload, "messages": messages}, images


def input_estimates(payload):
    """(tokens pelo contador, entrada estimada para a reserva).

    A entrada estimada é o MAIOR entre o contador (tiktoken + folga fixa + teto por imagem,
    ver payload_tokens) e a conta por caracteres do mesmo JSON (mensagens + ferramentas) com
    a calibração da casa (CPT). Levanta como payload_tokens (formato multimodal desconhecido).
    """
    counted = payload_tokens(payload)
    stripped, images = _without_images(payload)
    image_tokens = max(0, counted - payload_tokens(stripped)) if images else 0
    messages = stripped.get("messages", []) or []
    chars = len(json.dumps({"messages": messages, "tools": payload.get("tools", [])}, ensure_ascii=False))
    by_chars = math.ceil(chars / CPT) + 512 + 16 * len(messages) + image_tokens
    return counted, max(counted, by_chars)


def _today(clock):
    return clock().date().isoformat()


class SpendingGuard:
    def __init__(self, path, legacy_path=None, clock=None):
        self.path = str(path)
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        with self._connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS calls (id TEXT PRIMARY KEY, user TEXT NOT NULL, day TEXT NOT NULL, model TEXT NOT NULL, cap REAL NOT NULL, actual REAL, status TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS metadata (name TEXT PRIMARY KEY, value TEXT NOT NULL)")
            # 14/09/2026 (noite): cobranças acima da reserva, com o dia em que valem (item 4).
            db.execute("CREATE TABLE IF NOT EXISTS exceeded (id TEXT PRIMARY KEY, day TEXT NOT NULL, user TEXT, quota_key TEXT, cap REAL, actual REAL, at TEXT NOT NULL, scope TEXT NOT NULL)")
            columns = {row[1] for row in db.execute('PRAGMA table_info(calls)')}
            for column in ('quota_key', 'group_name'):
                if column not in columns:
                    db.execute('ALTER TABLE calls ADD COLUMN ' + column + ' TEXT')
            db.execute("BEGIN IMMEDIATE")
            if not db.execute("SELECT 1 FROM metadata WHERE name='legacy_imported'").fetchone():
                if legacy_path and Path(legacy_path).exists():
                    legacy = json.loads(Path(legacy_path).read_bytes())
                    if not isinstance(legacy.get("dias"), dict):
                        raise BudgetError("Razão anterior inválido; migração recusada.")
                    for day, record in legacy["dias"].items():
                        for user, usage in record.get("usuarios", {}).items():
                            amount = float(usage.get("usd", 0))
                            if not math.isfinite(amount) or amount < 0:
                                raise BudgetError("Gasto anterior inválido.")
                            db.execute("INSERT INTO calls (id,user,day,model,cap,actual,status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                       (uuid.uuid4().hex, user, day, "legacy", amount, amount, "settled"))
                db.execute("INSERT INTO metadata VALUES ('legacy_imported', '1')")
            today = _today(self.clock)
            # Item 2: reserva órfã de dia anterior — liquidada pelo teto (o gasto do dia dela
            # fica do lado caro); do dia corrente NÃO se toca: pode ser de outro processo vivo.
            db.execute("UPDATE calls SET actual=cap, status='estimated_upper_bound' WHERE status='reserved' AND day<?",
                       (today,))
            # Item 4: a marca permanente antiga vira pausa global do dia em que é encontrada.
            # A marca fica no banco (um processo com o código antigo continua parado); só não
            # é mais relida por este código depois de convertida.
            if (db.execute("SELECT 1 FROM metadata WHERE name='blocked'").fetchone()
                    and not db.execute("SELECT 1 FROM metadata WHERE name='blocked_migrated'").fetchone()):
                db.execute("INSERT INTO exceeded (id, day, user, quota_key, cap, actual, at, scope) VALUES (?, ?, NULL, NULL, NULL, NULL, ?, 'global')",
                           (uuid.uuid4().hex, today, self.clock().isoformat(timespec="seconds")))
                db.execute("INSERT INTO metadata VALUES ('blocked_migrated', ?)", (today,))

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        try:
            db.execute("PRAGMA synchronous=FULL")
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def _pauses(db, day, user=None, quota_key=None):
        """(pausa global?, pausa desta conta?, fator de segurança do dia)."""
        rows = db.execute("SELECT user, quota_key, cap, actual, scope FROM exceeded WHERE day=?", (day,)).fetchall()
        conta = [r for r in rows if r[4] == 'conta']
        global_pause = any(r[4] == 'global' for r in rows) or len(conta) >= EXCEEDED_GLOBAL_LIMIT
        own = any((user is not None and r[0] == user) or (quota_key is not None and r[1] == quota_key)
                  for r in conta)
        ratios = [r[3] / r[2] for r in conta if r[2] and r[3] is not None and r[2] > 0]
        factor = min(max(ratios + [1.0]), MAX_SAFETY_FACTOR)
        return global_pause, own, factor

    def reserve(self, user, model, cap, user_limit, global_limit, quota_key=None, group=None, group_limit=None):
        values = (cap, user_limit, global_limit) + ((group_limit,) if group_limit is not None else ())
        if any(not math.isfinite(v) or v < 0 for v in values):
            raise BudgetError(MSG_LIMITES_INVALIDOS, "razao")
        day = _today(self.clock)
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            quota_key = quota_key or user
            global_pause, own_pause, factor = self._pauses(db, day, user, quota_key)
            if global_pause:
                raise BudgetError(MSG_CONFERENCIA_GLOBAL, "conferencia")
            if own_pause:
                raise BudgetError(MSG_CONFERENCIA_CONTA, "conferencia")
            cap = cap * factor
            db.execute('UPDATE calls SET quota_key=?, group_name=? WHERE user=? AND quota_key IS NULL',
                       (quota_key, group, user))
            # Item 2: só o dia corrente (as órfãs de dias anteriores já foram liquidadas ao iniciar).
            rows = db.execute("SELECT user, COALESCE(actual, cap), quota_key, group_name FROM calls WHERE day=?", (day,)).fetchall()
            own = sum(amount for who, amount, key, _ in rows if who == user or key == quota_key)
            total = sum(amount for _, amount, _, _ in rows)
            grouped = sum(amount for _, amount, _, value in rows if value == group)
            if total + cap > global_limit + 1e-10:
                raise BudgetError(MSG_GLOBAL, "global")
            if group_limit is not None and grouped + cap > group_limit + 1e-10:
                raise BudgetError(MSG_GRUPO_GRATUITO if group == "gratuito" else MSG_GLOBAL,
                                  "global_gratuito" if group == "gratuito" else "global")
            if own + cap > user_limit + 1e-10:
                raise BudgetError(MSG_CONTA_DIA, "usd_dia")
            key = uuid.uuid4().hex
            db.execute("INSERT INTO calls (id,user,day,model,cap,actual,status,quota_key,group_name) VALUES (?, ?, ?, ?, ?, NULL, 'reserved', ?, ?)", (key, user, day, model, cap, quota_key, group))
            return key

    def settle(self, key, amount=None, estimate=None):
        """Liquida uma reserva. amount = o que o provedor informou (exato); sem amount, a
        `estimate` (chamada interrompida: entrada estimada + saída vista) limitada à reserva;
        sem os dois, a reserva inteira."""
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT cap, status, user, quota_key FROM calls WHERE id=?", (key,)).fetchone()
            if row is None:
                raise BudgetError("Reserva de uso não localizada.")
            if row[1] != "reserved":
                return
            if amount is None:
                if estimate is None:
                    amount, status = row[0], "estimated_upper_bound"
                else:
                    estimate = float(estimate)
                    if not math.isfinite(estimate) or estimate < 0:
                        amount, status = row[0], "estimated_upper_bound"
                    else:
                        amount, status = min(estimate, row[0]), "estimated_partial"
            else:
                amount, status = float(amount), "settled"
                if not math.isfinite(amount) or amount < 0:
                    raise BudgetError("Uso inválido informado pelo provedor.")
            # A provider charge exceeding our bound must remain visible, never be capped.
            db.execute("UPDATE calls SET actual=?, status=? WHERE id=?", (amount, status, key))
            if status == "settled" and amount > row[0] + 1e-8:
                db.execute("INSERT INTO exceeded (id, day, user, quota_key, cap, actual, at, scope) VALUES (?, ?, ?, ?, ?, ?, ?, 'conta')",
                           (uuid.uuid4().hex, _today(self.clock), row[2], row[3], row[0], amount,
                            self.clock().isoformat(timespec="seconds")))

    def check(self, user=None, quota_key=None):
        """Recusa se o motor está pausado hoje para todos (ou para esta conta, se informada)."""
        with self._connect() as db:
            global_pause, own_pause, _ = self._pauses(db, _today(self.clock), user, quota_key or user)
        if global_pause:
            raise BudgetError(MSG_CONFERENCIA_GLOBAL, "conferencia")
        if own_pause:
            raise BudgetError(MSG_CONFERENCIA_CONTA, "conferencia")

    def used_today(self):
        """Same amount as the reservation guard: settled costs plus active holds."""
        with self._connect() as db:
            amount = db.execute(
                "SELECT COALESCE(SUM(COALESCE(actual, cap)), 0) FROM calls WHERE day=?",
                (_today(self.clock),)).fetchone()[0]
        if not math.isfinite(amount) or amount < 0:
            raise BudgetError(MSG_LIMITES_INVALIDOS, "razao")
        return float(amount)

    def by_model_today(self):
        """Daily inference costs and reservations by actual recorded model."""
        with self._connect() as db:
            rows = db.execute(
                "SELECT model, COUNT(*), SUM(COALESCE(actual,cap)) FROM calls "
                "WHERE day=? GROUP BY model ORDER BY model", (_today(self.clock),)).fetchall()
        return [{"model": model, "calls": count, "usd": round(amount, 8)}
                for model, count, amount in rows]

    def summary(self):
        with self._connect() as db:
            rows = db.execute("SELECT day, status, COUNT(*), SUM(COALESCE(actual, cap)) FROM calls GROUP BY day, status ORDER BY day DESC LIMIT 50").fetchall()
            return [{"day_utc": day, "status": status, "calls": count, "usd": amount}
                    for day, status, count, amount in rows]

    def exceeded_summary(self, limit=50):
        """Cobranças acima da reserva (e pausas globais convertidas), para o painel."""
        with self._connect() as db:
            rows = db.execute("SELECT day, scope, user, cap, actual, at FROM exceeded ORDER BY at DESC LIMIT ?", (int(limit),)).fetchall()
        return [{"day_utc": day, "scope": scope, "user": user, "cap": cap, "actual": actual, "at": at}
                for day, scope, user, cap, actual, at in rows]


class ReservedAccount:
    def __init__(self, guard, legacy_account, cfg, user, admin, model, quota_key=None, group=None, group_limit=None):
        self.guard, self.legacy, self.cfg = guard, legacy_account, cfg
        self.user, self.admin, self.model = user, admin, model
        self.key = None
        self.closed = False
        self.quota_key, self.group, self.group_limit = quota_key, group, group_limit
        self._estimated_input = None
        self._estimated_rates = None
        self._output_chars = 0

    def _rates(self, input_tokens):
        rates = self.cfg.precos(self.model)
        input_rate = max(rates[0], rates[3]) if len(rates) == 4 else rates[0]
        if self.model == 'gpt-5.6-luna':
            # Official model page, 2026-09-14: long-context multipliers and
            # cache writes. Conservatively treat every uncached token as a
            # cache write until usage supplies an unambiguous split.
            long = input_tokens > 272000
            return (max(input_rate, rates[0] * 1.25) * (2 if long else 1),
                    rates[1] * (2 if long else 1), rates[2] * (1.5 if long else 1))
        return (input_rate, rates[1], rates[2])

    def iniciar_chamada(self, payload):
        self._finish_pending()
        self.guard.check(self.user, self.quota_key)
        output = int(payload["max_completion_tokens"])
        counted, estimate = input_estimates(payload)
        if counted + output > self.cfg.janela:
            raise WindowError()
        # Item 1: a entrada estimada do payload REAL com margem, não a janela configurada.
        reserved_input = math.ceil(estimate * RESERVATION_MARGIN)
        price_in, price_cache, price_out = self._rates(reserved_input)
        if any(not math.isfinite(p) or p < 0 for p in (price_in, price_cache, price_out)):
            raise BudgetError("Preço inválido; envio bloqueado.", "razao")
        cap = (reserved_input * max(price_in, price_cache) + output * price_out) / 1_000_000
        user_limit = self.cfg.cota_operador_usd if self.admin else self.cfg.cota_usuario_usd
        if self.admin and getattr(self.cfg, "somente_limite_global", False):
            # Personal usage is a subset of global usage; keep the same atomic guard.
            user_limit = self.cfg.cota_global_usd
        self.key = self.guard.reserve(self.user, self.model, cap,
                                     user_limit,
                                     self.cfg.cota_global_usd, quota_key=self.quota_key,
                                     group=self.group, group_limit=self.group_limit)
        self._estimated_input = estimate
        self._estimated_rates = (price_in, price_out)
        self._output_chars = 0
        self.legacy.iniciar_chamada(payload)

    def descartar_ultima_chamada(self):
        if self.key:
            self.guard.settle(self.key, 0)
            self.key = None
        self.legacy.descartar_ultima_chamada()

    def uso(self, usage):
        if self.key is None:
            return
        try:
            prompt = int(usage["prompt_tokens"])
            output = int(usage["completion_tokens"])
            cached = int(usage.get("prompt_tokens_details", {}).get("cached_tokens", 0))
            if min(prompt, output, cached) < 0 or cached > prompt:
                raise ValueError
        except (KeyError, TypeError, ValueError):
            raise BudgetError("O provedor retornou um registro de uso inválido; a reserva será mantida.")
        price_in, price_cache, price_out = self._rates(prompt)
        amount = ((prompt - cached) * price_in + cached * price_cache + output * price_out) / 1_000_000
        self.guard.settle(self.key, amount)
        self.key = None
        self.legacy.uso(usage)

    def texto(self, text):
        self._output_chars += len(text or "")
        self.legacy.texto(text)

    def _finish_pending(self):
        if self.key:
            # Item 3: sem `usage`, a estimativa (entrada estimada + saída vista, pela CPT da
            # casa). O raciocínio que o modelo não mostrou fica fora dela [DERIVED]; a
            # liquidação nunca passa da reserva e nunca marca "cobrança acima da reserva".
            estimate = None
            if self._estimated_input is not None and self._estimated_rates is not None:
                price_in, price_out = self._estimated_rates
                output_tokens = math.ceil(self._output_chars / CPT)
                estimate = (self._estimated_input * price_in + output_tokens * price_out) / 1_000_000
            self.guard.settle(self.key, estimate=estimate)
            self.key = None

    def fechar(self):
        if self.closed:
            return
        self._finish_pending()
        self.closed = True
        self.legacy.fechar()
