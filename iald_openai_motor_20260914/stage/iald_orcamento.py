"""Persistent preflight reservations for every external inference call.

Reserve an upper bound before sending. Settle against provider usage, or keep
the bound when a stream is interrupted. SQLite serializes concurrent processes.
"""
from datetime import datetime, timezone
from contextlib import contextmanager
import json
import math
from pathlib import Path
import sqlite3
import uuid

from iald_memoria_canonica import payload_tokens


class BudgetError(ValueError):
    pass


class SpendingGuard:
    def __init__(self, path, legacy_path=None, clock=None):
        self.path = str(path)
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        with self._connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS calls (id TEXT PRIMARY KEY, user TEXT NOT NULL, day TEXT NOT NULL, model TEXT NOT NULL, cap REAL NOT NULL, actual REAL, status TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS metadata (name TEXT PRIMARY KEY, value TEXT NOT NULL)")
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

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        try:
            db.execute("PRAGMA synchronous=FULL")
            with db:
                yield db
        finally:
            db.close()

    def reserve(self, user, model, cap, user_limit, global_limit, quota_key=None, group=None, group_limit=None):
        values = (cap, user_limit, global_limit) + ((group_limit,) if group_limit is not None else ())
        if any(not math.isfinite(v) or v < 0 for v in values):
            raise BudgetError("Limites de uso inválidos; envio bloqueado.")
        day = self.clock().date().isoformat()
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT 1 FROM metadata WHERE name='blocked'").fetchone():
                raise BudgetError("Motor bloqueado para conferência de cobrança.")
            quota_key = quota_key or user
            db.execute('UPDATE calls SET quota_key=?, group_name=? WHERE user=? AND quota_key IS NULL',
                       (quota_key, group, user))
            rows = db.execute("SELECT user, COALESCE(actual, cap), quota_key, group_name FROM calls WHERE day=? OR status='reserved'", (day,)).fetchall()
            own = sum(amount for who, amount, key, _ in rows if who == user or key == quota_key)
            total = sum(amount for _, amount, _, _ in rows)
            grouped = sum(amount for _, amount, _, value in rows if value == group)
            if (own + cap > user_limit + 1e-10 or total + cap > global_limit + 1e-10
                    or (group_limit is not None and grouped + cap > group_limit + 1e-10)):
                raise BudgetError("O saldo diário disponível não cobre com segurança outra chamada ao modelo. Tente após a renovação ou peça ao operador para ajustar a cota.")
            key = uuid.uuid4().hex
            db.execute("INSERT INTO calls (id,user,day,model,cap,actual,status,quota_key,group_name) VALUES (?, ?, ?, ?, ?, NULL, 'reserved', ?, ?)", (key, user, day, model, cap, quota_key, group))
            return key

    def settle(self, key, amount=None):
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT cap, status FROM calls WHERE id=?", (key,)).fetchone()
            if row is None:
                raise BudgetError("Reserva de uso não localizada.")
            if row[1] != "reserved":
                return
            if amount is None:
                amount, status = row[0], "estimated_upper_bound"
            else:
                amount, status = float(amount), "settled"
                if not math.isfinite(amount) or amount < 0:
                    raise BudgetError("Uso inválido informado pelo provedor.")
            # A provider charge exceeding our bound must remain visible, never be capped.
            db.execute("UPDATE calls SET actual=?, status=? WHERE id=?", (amount, status, key))
            if amount > row[0] + 1e-8:
                db.execute("INSERT OR REPLACE INTO metadata VALUES ('blocked', 'provider_exceeded_reservation')")

    def check(self):
        with self._connect() as db:
            if db.execute("SELECT 1 FROM metadata WHERE name='blocked'").fetchone():
                raise BudgetError("A cobrança ultrapassou a reserva prevista; motor bloqueado para conferência.")

    def summary(self):
        with self._connect() as db:
            rows = db.execute("SELECT day, status, COUNT(*), SUM(COALESCE(actual, cap)) FROM calls GROUP BY day, status ORDER BY day DESC LIMIT 50").fetchall()
            return [{"day_utc": day, "status": status, "calls": count, "usd": amount}
                    for day, status, count, amount in rows]


class ReservedAccount:
    def __init__(self, guard, legacy_account, cfg, user, admin, model, quota_key=None, group=None, group_limit=None):
        self.guard, self.legacy, self.cfg = guard, legacy_account, cfg
        self.user, self.admin, self.model = user, admin, model
        self.key = None
        self.closed = False
        self.quota_key, self.group, self.group_limit = quota_key, group, group_limit

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
        self.guard.check()
        output = int(payload["max_completion_tokens"])
        if payload_tokens(payload) + output > self.cfg.janela:
            raise BudgetError("A memória, a conversa e a resposta excedem a janela configurada; nada foi enviado.")
        price_in, price_cache, price_out = self._rates(self.cfg.janela)
        if any(not math.isfinite(p) or p < 0 for p in (price_in, price_cache, price_out)):
            raise BudgetError("Preço inválido; envio bloqueado.")
        # Reserve the whole configured window, irrespective of cache expectations.
        cap = (self.cfg.janela * max(price_in, price_cache) + output * price_out) / 1_000_000
        self.key = self.guard.reserve(self.user, self.model, cap,
                                     self.cfg.cota_operador_usd if self.admin else self.cfg.cota_usuario_usd,
                                     self.cfg.cota_global_usd, quota_key=self.quota_key,
                                     group=self.group, group_limit=self.group_limit)
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
        self.legacy.texto(text)

    def _finish_pending(self):
        if self.key:
            self.guard.settle(self.key)
            self.key = None

    def fechar(self):
        if self.closed:
            return
        self._finish_pending()
        self.closed = True
        self.legacy.fechar()
