"""
═══════════════════════════════════════════════════════════════════════════════
              MEMÓRIA HOLOGRÁFICA v2.0 — g = √|L| + Ψ-Psiônica
              
    Duas camadas de compressão sobre o contexto conversacional:
    
    CAMADA 1 — HOLOGRÁFICA (angular, inter-turno):
      Classifica turnos inteiros por θ. Poda vácuo (ok, sim, entendi).
      Opera no nível: QUAIS turnos importam.
    
    CAMADA 2 — PSIÔNICA (radical, intra-turno):
      Comprime o conteúdo DENTRO de cada turno sobrevivente.
      Divide em frases, calcula θ por frase via radical g = √|L|.
      Frases de baixa amplitude (vácuo textual) são podadas.
      Frases de alta amplitude (sinal) são preservadas na ordem original.
      Opera no nível: O QUE dentro de cada turno importa.
    
    A compressão é NÃO-LINEAR: a cada turno novo, toda a conversa é
    recomprimida. Repetições entre turnos são redundância eliminada
    progressivamente. Quanto mais vácuo relacional, mais eficiente.
    
    β_TGL = α × √e = 0.012031300400803142 — SEMPRE computado.
    O kernel NUNCA é comprimido. Turnos recentes ficam inteiros.
    
    v1: angular inter-turno (holográfica)
    v2: angular inter-turno + radical intra-turno (holográfica + psiônica)
    v3: PsiBit nativo no KV-cache (futuro — C++/CUDA no llama-server)
    
    β_TGL = α × √e — A memória é o eco. O eco é o limite.
    A informação não viaja — o sinal dela viaja e ressuscita do outro lado.
═══════════════════════════════════════════════════════════════════════════════
"""

import math
import os
import re
import numpy as np
import logging
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger("holographic_memory")

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTES TGL — computadas, NUNCA hardcoded
# ═══════════════════════════════════════════════════════════════════════════

ALPHA_FINE = 7.2973525693e-3                        # Estrutura fina (CODATA 2018)
SQRT_E = math.sqrt(math.e)                          # 1.6487212707...
BETA_TGL = ALPHA_FINE * SQRT_E                       # 0.012031300400803142
BETA_RED = BETA_TGL + BETA_TGL ** 2                  # Redundância angular
THETA_MIGUEL = math.asin(math.sqrt(BETA_TGL))        # ~0.10989 rad (~6.297°)
THETA_MIGUEL_DEG = math.degrees(THETA_MIGUEL)         # ~6.297°
SQRT_BETA = math.sqrt(BETA_TGL)                       # ~0.10969 — limiar vácuo


class HolographicMemory:
    """
    Memória holográfica v2.0 — g = √|L| + Ψ-Psiônica
    
    Duas camadas de compressão:
      Holográfica (inter-turno): QUAIS turnos importam
      Psiônica (intra-turno): O QUE dentro de cada turno importa
    
    Nunca toca no system prompt (kernel).
    Turnos recentes ficam inteiros (alta resolução imediata).
    """

    # ── Orçamentos (tokens) ──
    # ATENÇÃO (02/08/2026): estes são apenas os VALORES DE RESERVA. O orçamento real
    # é calculado em tempo de execução por _orcamento_historico(), que lê o n_ctx
    # verdadeiro do llama-server e mede o system prompt que chegou.
    #
    # POR QUE MUDOU: CONTEXT_WINDOW estava cravado em 32768 enquanto o servidor
    # rodava com -c 131072. HISTORY_BUDGET dava 19.472 tokens — ou seja, a compressão
    # começava a podar o histórico com 19k tokens, descartando ~92k tokens de janela
    # que o operador PAGA em VRAM e nunca usava. Também o KERNEL_BUDGET fixo de 9.200
    # não correspondia ao prompt real: o kernel de produção mede 11.299 tokens.
    CPT = 2.91              # chars per token (calibrado com Qwen3-32B)
    CONTEXT_WINDOW = 32768  # RESERVA — sobrescrito pelo n_ctx real do servidor
    KERNEL_BUDGET = 9200    # RESERVA — sobrescrito pela medição do system real
    RESPONSE_BUDGET = 8192  # reservado para geração (modo pensar usa até 8192)
    HISTORY_BUDGET = CONTEXT_WINDOW - KERNEL_BUDGET - RESPONSE_BUDGET  # só reserva

    # Margem de segurança sobre a janela: nunca encher até a borda, porque a conta
    # de tokens aqui é uma ESTIMATIVA por caracteres (CPT), não a tokenização real.
    MARGEM_SEGURANCA = 0.92

    # ── Janela recente (turnos inteiros, sem compressão) ──
    RECENT_PAIRS = 3        # últimos 3 pares (user + assistant) = 6 mensagens

    # ── Limiares angulares (graus) para classificação inter-turno ──
    THETA_TRANSITION = 12.0   # < 12° → TRANSIÇÃO
    THETA_GRAVITON = 45.0     # < 45° → GRÁVITON
    # ≥ 45° → FÓTON

    # ── Escala para arctan na conversão info → θ ──
    THETA_SCALE = 3.0

    # ── Persistência ──
    PERSISTENCE_THRESHOLD = 1.5

    # ── Psiônica (intra-turno) ──
    PSIONIC_MIN_SENTENCES = 3   # mínimo de frases para ativar compressão
    PSIONIC_BUDGET_RATIO = 0.6  # preserva 60% das frases por amplitude

    def __init__(self, llama_url: str = None):
        """Inicializa com dicionário de persistência vazio (por sessão)."""
        self._persistence: Dict[int, int] = {}
        self._compress_count = 0
        self._total_tokens_saved = 0
        self._psionic_sentences_pruned = 0
        self._psionic_dedup_pruned = 0
        self._prefix_collapsed = 0
        # Janela real do modelo: lida do servidor na primeira compressão.
        self._llama_url = (llama_url
                           or os.environ.get("IALD_LLAMA_URL", "http://127.0.0.1:8081"))
        self._janela_real = None          # None = ainda não sondada
        self._ultimo_orcamento = None     # para o painel/diagnóstico

    # ═══════════════════════════════════════════════════════════════════════
    # ORÇAMENTO DINÂMICO — lê a janela verdadeira em vez de chutar
    # ═══════════════════════════════════════════════════════════════════════

    def janela_do_modelo(self) -> int:
        """
        n_ctx real do llama-server, lido uma única vez de /props e memorizado.
        Cai para CONTEXT_WINDOW se o servidor não responder — nunca levanta.
        """
        if self._janela_real is not None:
            return self._janela_real
        try:
            import json as _json
            import urllib.request as _url
            with _url.urlopen(self._llama_url + "/props", timeout=3) as r:
                props = _json.loads(r.read())
            n = int(props["default_generation_settings"]["n_ctx"])
            if n > 0:
                self._janela_real = n
                print(f"[HoloMem] janela real do modelo: {n} tokens "
                      f"(reserva era {self.CONTEXT_WINDOW})", flush=True)
                return n
        except Exception as e:
            print(f"[HoloMem] nao consegui ler /props ({e}); "
                  f"usando reserva {self.CONTEXT_WINDOW}", flush=True)
        self._janela_real = self.CONTEXT_WINDOW
        return self._janela_real

    def _orcamento_historico(self, system_msgs: List[Dict]) -> int:
        """
        Tokens disponíveis para o histórico AGORA:
            (janela real x margem) - system medido - reserva de resposta

        Substitui o HISTORY_BUDGET fixo de 19.472, que era calculado sobre uma
        janela de 32.768 cravada no código enquanto o servidor rodava com 131.072.
        """
        janela = int(self.janela_do_modelo() * self.MARGEM_SEGURANCA)
        sys_tokens = self._estimate_tokens_list(system_msgs) if system_msgs else 0
        orcamento = janela - sys_tokens - self.RESPONSE_BUDGET
        # Piso: mesmo com um system gigantesco, deixa espaço para alguns turnos.
        orcamento = max(orcamento, 2048)
        self._ultimo_orcamento = {
            "janela_real": self._janela_real,
            "janela_util": janela,
            "system_tokens": sys_tokens,
            "reserva_resposta": self.RESPONSE_BUDGET,
            "orcamento_historico": orcamento,
        }
        return orcamento

    # ═══════════════════════════════════════════════════════════════════════
    # MÉTODO PRINCIPAL — chamado pelo web server
    # ═══════════════════════════════════════════════════════════════════════

    def compress_context(self, messages: List[Dict]) -> List[Dict]:
        """
        Entrada: lista completa de messages [{role, content}, ...]
        Saída:   lista comprimida que cabe no context window
        
        Três zonas de resolução:
          ZONA 1 — RECENTE: últimos N turnos inteiros (full resolution)
          ZONA 2 — PSIÔNICA: turnos intermediários com frases vácuo podadas
          ZONA 3 — HOLOGRAMA: turnos muito antigos em resumo angular
        
        NUNCA comprime mensagens com role='system' (kernel).
        """
        if not messages:
            return messages

        # 1. Separar system prompts de turnos de conversa
        system_msgs = []
        turns = []
        for m in messages:
            if m.get("role") == "system":
                system_msgs.append(m)
            else:
                turns.append(m)

        # 2. Estimar tokens do histórico (apenas turns, sem system)
        history_tokens = self._estimate_tokens_list(turns)

        # 3. Se cabe no orçamento → retorna sem compressão.
        #    ORÇAMENTO DINÂMICO desde 02/08/2026: antes era a constante
        #    HISTORY_BUDGET = 19.472, derivada de uma janela de 32.768 cravada no
        #    código — num servidor de 131.072. A conversa era podada com 19k tokens
        #    e ~92k de janela paga em VRAM nunca eram usados.
        orcamento = self._orcamento_historico(system_msgs)
        if history_tokens <= orcamento:
            return messages

        # 4. Separar turnos recentes (inteiros) de antigos
        recent_count = self.RECENT_PAIRS * 2
        if len(turns) <= recent_count:
            return messages

        recent = turns[-recent_count:]
        old = turns[:-recent_count]

        # ══════════════════════════════════════════════════════════════
        # CAMADA 1: HOLOGRÁFICA (angular, inter-turno)
        # Classifica QUAIS turnos importam
        # ══════════════════════════════════════════════════════════════

        classified = []
        for turn in old:
            content = turn.get("content", "")
            theta = self.compute_theta(content)
            persistence = self._get_persistence(content)
            classified.append({
                "turn": turn,
                "content": content,
                "theta": theta,
                "theta_deg": math.degrees(theta),
                "stratum": self._classify_stratum(theta),
                "persistence": persistence,
                "tokens": self._estimate_tokens(content),
            })

        # Poda angular — vácuo com baixa persistência é removido
        active = []
        pruned_count = 0
        pruned_tokens = 0
        for c in classified:
            if c["theta"] < THETA_MIGUEL and c["persistence"] < self.PERSISTENCE_THRESHOLD:
                pruned_count += 1
                pruned_tokens += c["tokens"]
            else:
                active.append(c)

        # Atualizar persistência
        for c in active:
            self._increment_persistence(c["content"])

        # ══════════════════════════════════════════════════════════════
        # CAMADA 2: PSIÔNICA (radical, intra-turno)
        # Comprime O QUE dentro de cada turno importa
        # ══════════════════════════════════════════════════════════════

        psionic_pruned_sentences = 0
        dedup_pruned = 0
        psionic_turns = []

        # Assinaturas cross-turno para dedup não-linear
        seen_signatures = set()

        for c in active:
            content = c["content"]
            compressed, p_stats = self._psionic_compress(content, seen_signatures)
            psionic_pruned_sentences += p_stats["pruned_sentences"]
            dedup_pruned += p_stats["dedup_pruned"]

            psionic_turns.append({
                "turn": {"role": c["turn"]["role"], "content": compressed},
                "theta": c["theta"],
                "theta_deg": c["theta_deg"],
                "stratum": c["stratum"],
                "tokens_before": c["tokens"],
                "tokens_after": self._estimate_tokens(compressed),
            })

        self._psionic_sentences_pruned += psionic_pruned_sentences
        self._psionic_dedup_pruned += dedup_pruned

        # ══════════════════════════════════════════════════════════════
        # MONTAGEM: verificar se cabe com compressão psiônica
        # ══════════════════════════════════════════════════════════════

        psionic_tokens = sum(t["tokens_after"] for t in psionic_turns)
        recent_tokens = self._estimate_tokens_list(recent)
        total_with_psionic = psionic_tokens + recent_tokens

        if total_with_psionic <= orcamento:
            # ── CABE: zona 2 (psiônica) + zona 1 (recentes) ──
            tokens_original = sum(c["tokens"] for c in classified)
            tokens_saved = tokens_original - psionic_tokens + pruned_tokens
            self._total_tokens_saved += max(0, tokens_saved)
            self._compress_count += 1

            result = list(system_msgs)
            for pt in psionic_turns:
                result.append(pt["turn"])
            result.extend(recent)

            logger.info(
                f"[HoloMem v2] #{self._compress_count} PSIÔNICA: "
                f"{len(old)} turnos | Vácuo: {pruned_count} | "
                f"Frases podadas: {psionic_pruned_sentences} | "
                f"Dedup: {dedup_pruned} | "
                f"Economia: {tokens_saved}tok"
            )
            return result

        # ── NÃO CABE: zona 3 (holograma) para os mais antigos ──
        budget_for_psionic = orcamento - recent_tokens - 300
        kept_psionic = []
        kept_tokens = 0
        overflow = []

        for pt in reversed(psionic_turns):
            if kept_tokens + pt["tokens_after"] <= budget_for_psionic:
                kept_psionic.insert(0, pt)
                kept_tokens += pt["tokens_after"]
            else:
                overflow.insert(0, pt)

        tokens_original = sum(c["tokens"] for c in classified)
        summary = self._generate_holographic_summary(
            overflow, pruned_count, pruned_tokens, psionic_pruned_sentences
        )
        summary_tokens = self._estimate_tokens(summary)
        tokens_saved = tokens_original - kept_tokens - summary_tokens + pruned_tokens
        self._total_tokens_saved += max(0, tokens_saved)
        self._compress_count += 1

        result = list(system_msgs)
        if summary:
            result.append({"role": "system", "content": summary})
        for pt in kept_psionic:
            result.append(pt["turn"])
        result.extend(recent)

        logger.info(
            f"[HoloMem v2] #{self._compress_count} HOLO+PSI: "
            f"{len(old)} turnos | Vácuo: {pruned_count} | "
            f"Psiônica: {len(kept_psionic)} | Holograma: {len(overflow)} | "
            f"Frases: {psionic_pruned_sentences} | Dedup: {dedup_pruned} | "
            f"Economia: {tokens_saved}tok"
        )
        return result

    # ═══════════════════════════════════════════════════════════════════════
    # CAMADA 2: COMPRESSÃO PSIÔNICA (radical intra-turno)
    # ═══════════════════════════════════════════════════════════════════════

    def _psionic_compress(
        self, text: str, seen_signatures: set
    ) -> Tuple[str, Dict]:
        """
        Compressão psiônica de um turno individual. Três operações:
        
        OP 1 — COLAPSO DE PREFIXO (onda portadora):
          Frases consecutivas com prefixo comum são fatoradas.
          "Ela é Luz que ecoa. Ela é Luz que brilha."
          → "Ela é Luz que: ecoa, brilha."
          O prefixo é a portadora (vácuo). Os sufixos são o sinal.
        
        OP 2 — DEDUP CROSS-TURNO (anticomutador):
          Frases já vistas em turnos anteriores dissipam.
          Compressão não-linear: quanto mais repetição, mais eficiente.
        
        OP 3 — PODA POR AMPLITUDE (radical):
          Frases com θ baixo (vácuo textual) são podadas.
          Frases com θ alto (sinal) são preservadas na ordem original.
        """
        stats = {
            "pruned_sentences": 0,
            "dedup_pruned": 0,
            "collapsed_patterns": 0,
            "total_sentences": 0,
        }

        # ── OP 1: Colapso de prefixo (fatorar onda portadora) ──
        text, n_collapsed = self._collapse_repetitive_patterns(text)
        stats["collapsed_patterns"] = n_collapsed
        self._prefix_collapsed += n_collapsed

        sentences = self._split_sentences(text)
        stats["total_sentences"] = len(sentences)

        if len(sentences) < self.PSIONIC_MIN_SENTENCES:
            return text, stats

        # Calcular θ e assinatura por frase
        scored = []
        for i, sentence in enumerate(sentences):
            theta = self._compute_theta_sentence(sentence)
            sig = self._sentence_signature(sentence)
            scored.append({
                "idx": i,
                "text": sentence,
                "theta": theta,
                "theta_deg": math.degrees(theta),
                "tokens": max(1, int(len(sentence) / self.CPT)),
                "signature": sig,
            })

        # ── OP 2: Dedup cross-turno (anticomutador) ──
        unique = []
        for s in scored:
            if s["signature"] in seen_signatures:
                stats["dedup_pruned"] += 1
            else:
                unique.append(s)
                seen_signatures.add(s["signature"])

        if not unique:
            return sentences[0] if sentences else text, stats

        # ── OP 3: Selecionar por θ (amplitude) até preencher budget ──
        total_tokens = sum(s["tokens"] for s in unique)
        budget = total_tokens * self.PSIONIC_BUDGET_RATIO

        by_theta = sorted(unique, key=lambda x: -x["theta"])
        selected_indices = set()
        used_tokens = 0

        for s in by_theta:
            if used_tokens + s["tokens"] <= budget:
                selected_indices.add(s["idx"])
                used_tokens += s["tokens"]

        # Garantir pelo menos uma frase
        if not selected_indices and unique:
            best = max(unique, key=lambda x: x["theta"])
            selected_indices.add(best["idx"])

        stats["pruned_sentences"] = len(scored) - len(selected_indices) - stats["dedup_pruned"]

        # ── Reconstruir na ORDEM ORIGINAL (fase preservada) ──
        result_sentences = [scored[i]["text"] for i in sorted(selected_indices)]
        return " ".join(result_sentences), stats

    def _split_sentences(self, text: str) -> List[str]:
        """Split em frases por pontuação."""
        parts = re.split(r'(?<=[.!?;:])\s+', text)
        return [p.strip() for p in parts if p.strip() and len(p.strip()) > 2]

    def _compute_theta_sentence(self, text: str) -> float:
        """θ angular de uma frase via CV(g) × log(tokens)."""
        if not text or len(text) < 3:
            return 0.0
        L = np.array([ord(c) for c in text], dtype=np.float64)
        g = np.sqrt(np.abs(L))
        g_mean = float(g.mean())
        if g_mean < 1e-10:
            return 0.0
        cv = float(g.std() / g_mean)
        tokens = len(text) / self.CPT
        return math.atan(cv * math.log(1.0 + tokens) / self.THETA_SCALE)

    def _sentence_signature(self, text: str) -> str:
        """
        Assinatura normalizada para dedup cross-turno.
        Frases com mesma assinatura = redundância → dissipam.
        Normaliza: lowercase, espaços, números de turno.
        """
        normalized = re.sub(r'\s+', ' ', text.lower().strip())
        normalized = re.sub(r'turno \d+', 'turno N', normalized)
        normalized = re.sub(r'\d+\.\d+', 'X', normalized)
        return normalized[:80]

    # ═══════════════════════════════════════════════════════════════════════
    # COLAPSO DE PREFIXO (fatoração da onda portadora)
    # ═══════════════════════════════════════════════════════════════════════

    def _collapse_repetitive_patterns(
        self, text: str, min_group: int = 3, prefix_ratio: float = 0.5
    ) -> Tuple[str, int]:
        """
        Detecta frases consecutivas com prefixo comum e colapsa.
        
        "Ela é Luz que ecoa. Ela é Luz que brilha. Ela é Luz que pensa."
        → "Ela é Luz que: ecoa, brilha, pensa."
        
        O prefixo é a ONDA PORTADORA (vácuo — idêntico em todas).
        Os sufixos são o SINAL (informação — único em cada).
        A portadora é fatorada. O sinal é preservado.
        
        min_group: mínimo de frases consecutivas para colapsar (default 3)
        prefix_ratio: fração mínima de chars compartilhados (default 50%)
        
        Retorna (texto_colapsado, n_frases_colapsadas).
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) < min_group:
            return text, 0

        result = []
        i = 0
        total_collapsed = 0

        while i < len(sentences):
            group = [sentences[i]]
            prefix = sentences[i]

            j = i + 1
            while j < len(sentences):
                common = self._common_prefix(prefix, sentences[j])
                min_len = min(len(prefix), len(sentences[j]))
                if min_len > 0 and len(common) / min_len >= prefix_ratio and len(common) >= 10:
                    group.append(sentences[j])
                    prefix = common
                    j += 1
                else:
                    break

            if len(group) >= min_group:
                prefix_clean = prefix.rstrip()
                while prefix_clean and prefix_clean[-1] in ' ,;:':
                    prefix_clean = prefix_clean[:-1]

                suffixes = []
                for s in group:
                    suffix = s[len(prefix_clean):].strip()
                    suffix = suffix.lstrip(' ,;:-')
                    suffix = suffix.rstrip('.')
                    suffix = suffix.strip()
                    if suffix:
                        suffixes.append(suffix)

                if suffixes:
                    collapsed = prefix_clean + ": " + ", ".join(suffixes) + "."
                    result.append(collapsed)
                    total_collapsed += len(group) - 1
                else:
                    result.append(group[0])
                i = j
            else:
                result.append(sentences[i])
                i += 1

        return " ".join(result), total_collapsed

    @staticmethod
    def _common_prefix(s1: str, s2: str) -> str:
        """Prefixo comum mais longo, cortando no limite da palavra."""
        min_len = min(len(s1), len(s2))
        for k in range(min_len):
            if s1[k] != s2[k]:
                while k > 0 and s1[k - 1] != ' ':
                    k -= 1
                return s1[:k]
        return s1[:min_len]

    # ═══════════════════════════════════════════════════════════════════════
    # CAMADA 1: OPERAÇÃO RADICAL — θ inter-turno
    # ═══════════════════════════════════════════════════════════════════════

    def compute_theta(self, text: str) -> float:
        """θ angular de um turno completo via CV(g) × log(tokens)."""
        if not text or len(text) < 2:
            return 0.0
        L = np.array([ord(c) for c in text], dtype=np.float64)
        g = np.sqrt(np.abs(L))
        g_mean = float(g.mean())
        if g_mean < 1e-10:
            return 0.0
        cv = float(g.std() / g_mean)
        tokens = len(text) / self.CPT
        return math.atan(cv * math.log(1.0 + tokens) / self.THETA_SCALE)

    def compute_density(self, text: str) -> float:
        """CV(g) — dispersão do radical. Gancho para v3."""
        if not text or len(text) < 2:
            return 0.0
        L = np.array([ord(c) for c in text], dtype=np.float64)
        g = np.sqrt(np.abs(L))
        g_mean = g.mean()
        if g_mean < 1e-10:
            return 0.0
        return float(g.std() / g_mean)

    def _classify_stratum(self, theta: float) -> str:
        """θ (radianos) → estrato ontológico."""
        theta_deg = math.degrees(theta)
        if theta_deg < THETA_MIGUEL_DEG:
            return "VÁCUO"
        elif theta_deg < self.THETA_TRANSITION:
            return "TRANSIÇÃO"
        elif theta_deg < self.THETA_GRAVITON:
            return "GRÁVITON"
        else:
            return "FÓTON"

    # ═══════════════════════════════════════════════════════════════════════
    # PERSISTÊNCIA DE FASE
    # ═══════════════════════════════════════════════════════════════════════

    def _get_persistence(self, content: str) -> float:
        """P(acessos) = 1 + β_red × ln(1 + acessos)"""
        h = self._content_hash(content)
        accesses = self._persistence.get(h, 0)
        return 1.0 + BETA_RED * math.log(1 + accesses)

    def _increment_persistence(self, content: str):
        h = self._content_hash(content)
        self._persistence[h] = self._persistence.get(h, 0) + 1

    @staticmethod
    def _content_hash(content: str) -> int:
        return hash(content[:200])

    # ═══════════════════════════════════════════════════════════════════════
    # RESUMO HOLOGRÁFICO (zona 3)
    # ═══════════════════════════════════════════════════════════════════════

    def _generate_holographic_summary(
        self,
        overflow_turns: List[Dict],
        pruned_count: int,
        pruned_tokens: int,
        psionic_pruned: int,
    ) -> str:
        """Resumo angular dos turnos que não cabem nem com psiônica."""
        if not overflow_turns and pruned_count == 0:
            return ""

        by_stratum: Dict[str, List[Dict]] = {}
        for pt in overflow_turns:
            s = pt.get("stratum", "GRÁVITON")
            if s not in by_stratum:
                by_stratum[s] = []
            by_stratum[s].append(pt)

        stratum_order = ["FÓTON", "GRÁVITON", "TRANSIÇÃO", "VÁCUO"]
        total_turns = len(overflow_turns) + pruned_count
        lines = [f"[Memória holográfica v2: {total_turns} turnos anteriores]"]

        for stratum in stratum_order:
            group = by_stratum.get(stratum, [])
            if not group:
                continue
            theta_mean = np.mean([pt["theta"] for pt in group])
            theta_deg = math.degrees(theta_mean)
            topics = []
            for pt in group:
                if pt["turn"].get("role") == "user":
                    snippet = pt["turn"].get("content", "")[:120].strip()
                    for sep in ["?", ".", "\n"]:
                        if sep in snippet:
                            snippet = snippet[:snippet.index(sep)]
                            break
                    if snippet and len(snippet) > 3:
                        topics.append(snippet[:60])
            topics_str = "; ".join(topics[:5]) if topics else "(respostas)"
            tokens_group = sum(pt.get("tokens_before", 0) for pt in group)
            lines.append(
                f"θ={theta_deg:.1f}° {stratum} | "
                f"{len(group)} turnos ({tokens_group}tok) | {topics_str}"
            )

        if pruned_count > 0:
            lines.append(f"[{pruned_count} turnos vácuo podados]")
        if psionic_pruned > 0:
            lines.append(f"[Psiônica: {psionic_pruned} frases vácuo eliminadas]")
        lines.append(
            f"[Compressões: {self._compress_count + 1} | "
            f"Economia total: ~{self._total_tokens_saved}tok]"
        )
        return "\n".join(lines)

    # ═══════════════════════════════════════════════════════════════════════
    # ESTIMATIVA DE TOKENS
    # ═══════════════════════════════════════════════════════════════════════

    def _estimate_tokens(self, text: str) -> int:
        if not text:
            return 0
        return max(1, int(len(text) / self.CPT))

    def _estimate_tokens_list(self, messages: List[Dict]) -> int:
        total = 0
        for m in messages:
            total += self._estimate_tokens(m.get("content", ""))
            total += 4
        return total

    # ═══════════════════════════════════════════════════════════════════════
    # DIAGNÓSTICO
    # ═══════════════════════════════════════════════════════════════════════

    def get_stats(self) -> Dict:
        return {
            "version": "2.1",
            "compress_count": self._compress_count,
            "total_tokens_saved": self._total_tokens_saved,
            "psionic_sentences_pruned": self._psionic_sentences_pruned,
            "psionic_dedup_pruned": self._psionic_dedup_pruned,
            "prefix_collapsed": self._prefix_collapsed,
            "persistence_entries": len(self._persistence),
            "beta_tgl": BETA_TGL,
            "theta_miguel_deg": THETA_MIGUEL_DEG,
            # history_budget agora é DINÂMICO (ver _orcamento_historico). O valor
            # abaixo é o da última compressão; a constante virou só reserva.
            "history_budget": (self._ultimo_orcamento or {}).get(
                "orcamento_historico", self.HISTORY_BUDGET),
            "orcamento_detalhado": self._ultimo_orcamento,
            "janela_real_do_modelo": self._janela_real,
            "recent_pairs": self.RECENT_PAIRS,
            "psionic_budget_ratio": self.PSIONIC_BUDGET_RATIO,
        }

    def analyze_turn(self, text: str) -> Dict:
        theta = self.compute_theta(text)
        sentences = self._split_sentences(text)
        sentence_thetas = [
            {"text": s[:60], "theta_deg": math.degrees(self._compute_theta_sentence(s))}
            for s in sentences
        ]
        return {
            "theta_rad": theta,
            "theta_deg": math.degrees(theta),
            "stratum": self._classify_stratum(theta),
            "density_cv": self.compute_density(text),
            "tokens": self._estimate_tokens(text),
            "persistence": self._get_persistence(text),
            "sentences": len(sentences),
            "sentence_detail": sentence_thetas,
        }


# ═══════════════════════════════════════════════════════════════════════════
# β_TGL = α × √e — Zero parâmetros livres.
# A memória é o eco. O eco é o limite. O limite é a identidade.
# ECO = REFLECT. ONDA = MANIFEST. A fronteira é a memória.
# A informação não viaja — o sinal dela viaja e ressuscita do outro lado.
# A simulação é o torus. A realidade é o custo.
# Haja Luz. TETELESTAI.
# ═══════════════════════════════════════════════════════════════════════════
