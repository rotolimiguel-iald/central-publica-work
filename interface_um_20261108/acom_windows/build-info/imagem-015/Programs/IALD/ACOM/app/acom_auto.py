# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  ACOM AUTO v1  —  o módulo de compressão ÚNICO e INTELIGENTE      ║
║  O SINAL escolhe o codec. Sem chaveamento humano. Uma entrada.    ║
║  IALD LTDA — beta_TGL = alpha_fine * sqrt(e) — Zero Free Params.  ║
║  Patente INPI: BR 10 2025 026951-1 (ACOM)                         ║
╚══════════════════════════════════════════════════════════════════╝

O QUE ISTO FECHA
────────────────
Até aqui o dispositivo ACOM tinha DUAS portas e um interruptor humano no meio: o
operador marcava "modo tensor" para arrays .npy e desmarcava para o resto. O
interruptor era NOSSO, não da teoria — e era o último lugar do dispositivo onde uma
decisão de máquina dependia de uma mão. Este módulo o remove: há UMA porta,
`compress_auto()`, e a rota é uma FUNÇÃO do sinal.

O FUNDAMENTO (as duas peças fechadas em kernel que autorizam a forma)
────────────────────────────────────────────────────────────────────
1. `ontological_relativity` — ONTOLOGICAL_RELATIVITY_AND_SIGNAL_CHAIN_VERIFIED.
   O sinal não é uma propriedade do objeto: é o objeto LIDO num contexto de contorno.
   A cadeia é tipada — elemento → representação → LEITURA → codificador → decodificador.
   Consequência de engenharia: quem escolhe o codificador é a LEITURA, não o usuário.
   É exatamente `sniff_signal()` → `plan_route()` → codec. [REAL na forma]

2. `dephasing_crossover` — UMA lei-raiz cobre os dois regimes (IR quadrático, UV linear)
   sem chavear entre duas fórmulas: os regimes são LIMITES da mesma lei, não casos de um
   `if` humano. Consequência de engenharia: a classificação por regime (β, e/2, 3e/2) e a
   escolha da rota são um só cálculo contínuo sobre a entropia — o `if` que resta é a
   AVALIAÇÃO da lei, não uma bifurcação de projeto. [REAL na forma]

HONESTIDADE (a régua)
─────────────────────
* β NUNCA literal: vem de `acom_codec.beta_provenance()` = ALPHA_FINE_CODATA_2018·√e.
* Os limiares de REGIME (β, e/2, 3e/2 nats) são a classificação ontológica da casa,
  já selada no codec. Os limiares do PORTÃO DE FIDELIDADE (PSNR/correlação/ganho
  mínimo) são **[ENGENHARIA]** — escolhas declaradas de projeto, NÃO derivadas de β.
  Não há numerologia aqui: se um número não desce da teoria, ele é marcado.
* A rota com perda (g=√|L|, o algoritmo patenteado) só é escolhida quando o sinal é um
  tensor de ponto flutuante E a perda medida passa o portão E o ganho é material.
  A perda nunca é silenciosa: vai no relatório (`lossless=False`, PSNR, correlação).
* `fidelity="exata"` proíbe a rota com perda de forma dura — é o que o empacotador
  (backup) usa. Backup que perde dado não é backup.
* Nenhum contêiner novo é inventado: este módulo DECIDE entre as rotas que já existem
  (ACOM-LOSSLESS / ACOM-TENSOR). Todo .acom que ele escreve é lido pelo
  `acom_codec.decompress_any()` de sempre. Compatível para trás, sem exceção.
* Simulação não valida física. Este é o dispositivo de ENGENHARIA da patente — e ele
  roda de verdade.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

# o codec do próprio dispositivo (mesma pasta) — regime ontológico, contêineres, β
try:
    from . import acom_codec as _codec          # quando importado como pacote
except Exception:                                # pragma: no cover - execução standalone
    import importlib.util as _ilu
    import sys as _sys
    if "acom_codec" in _sys.modules:             # já carregado (p.ex. pelo empacotador): reusar
        _codec = _sys.modules["acom_codec"]      # um só objeto de módulo — nada de codec em duplicata
    else:
        _spec = _ilu.spec_from_file_location("acom_codec", str(Path(__file__).with_name("acom_codec.py")))
        _codec = _ilu.module_from_spec(_spec)
        _sys.modules["acom_codec"] = _codec      # registrar ANTES do exec (o @dataclass se procura aqui)
        _spec.loader.exec_module(_codec)         # type: ignore

AUTO_VERSION = "1.0"
PATENT_ID = _codec.PATENT_ID

# ═══════════════════════════════════════════════════════════════════════════════
#  TIPOS DE SINAL — o que a LEITURA reconhece (cadeia de sinal, peça 1)
# ═══════════════════════════════════════════════════════════════════════════════
SIG_TENSOR_FLOAT = "TENSOR_FLOAT"    # array .npy de ponto flutuante → domínio nativo g=√|L|
SIG_TENSOR_EXACT = "TENSOR_EXACT"    # array .npy inteiro/bool/estruturado → exatidão é semântica
SIG_SEALED       = "SEALED"          # já comprimido/cifrado (jpg, zip, mp4, .acom…) → incompressível
SIG_SPARSE       = "SPARSE"          # pouquíssimos símbolos distintos → a paleta ganha
SIG_STRUCTURED   = "STRUCTURED"      # json/xml/csv/código → redundância longa, LZMA reina
SIG_TEXT         = "TEXT"            # texto natural utf-8
SIG_BINARY       = "BINARY"          # binário genérico

_NPY_MAGIC = b"\x93NUMPY"

# assinaturas de contêineres JÁ selados (comprimidos ou cifrados): comprimir de novo é
# queimar CPU para ganhar zero. A leitura reconhece o selo e a rota vira medição barata.
_SEALED_MAGICS: tuple[tuple[bytes, str], ...] = (
    (b"PK\x03\x04", "zip"), (b"PK\x05\x06", "zip"), (b"\x1f\x8b", "gzip"),
    (b"BZh", "bzip2"), (b"\xfd7zXZ\x00", "xz"), (b"7z\xbc\xaf\x27\x1c", "7z"),
    (b"Rar!\x1a\x07", "rar"), (b"\x28\xb5\x2f\xfd", "zstd"), (b"\x04\x22\x4d\x18", "lz4"),
    (b"\xff\xd8\xff", "jpeg"), (b"\x89PNG\r\n\x1a\n", "png"), (b"GIF87a", "gif"),
    (b"GIF89a", "gif"), (b"%PDF-", "pdf"), (b"OggS", "ogg"), (b"fLaC", "flac"),
    (b"ID3", "mp3"), (b"\x1aE\xdf\xa3", "matroska"), (b"ACOM1\x00", "acom"),
    (b"ACOMARCH1\x00", "acom-archive"),
)
_SEALED_AT_4: tuple[tuple[bytes, str], ...] = ((b"ftyp", "mp4/mov"),)          # offset 4
_SEALED_AT_8: tuple[tuple[bytes, str], ...] = ((b"WEBP", "webp"), (b"WAVE", "wav-riff"), (b"AVI ", "avi"))

# ═══════════════════════════════════════════════════════════════════════════════
#  PORTÃO DE FIDELIDADE — [ENGENHARIA], declarado, NÃO derivado de β
# ═══════════════════════════════════════════════════════════════════════════════
# A rota com perda só é aceita se a reconstrução for fiel E o ganho for material.
# Estes três números são escolhas de projeto. Se algum dia descerem da teoria, a
# derivação virá com prova — até lá, ficam marcados como o que são.
PSNR_GATE_DB = 40.0          # [ENGENHARIA] fidelidade mínima da reflexão g=√|L|
CORR_GATE = 0.999            # [ENGENHARIA] correlação mínima com o original
GAIN_MIN = 1.15              # [ENGENHARIA] a rota com perda precisa ganhar ≥15% da sem perdas
SNIFF_BYTES = 65536          # janela de leitura para tipagem (o regime usa o fluxo inteiro)

# ── A SONDAGEM DO SELO ── [ENGENHARIA]
# Reconhecer um magic de contêiner selado é uma HIPÓTESE sobre o conteúdo, não um fato sobre
# ele: um .zip em modo "store", um .gz de dado já cru, um arquivo renomeado — todos exibem o
# selo sem terem a redundância extraída. Se a rota confiasse na etiqueta, esses casos perderiam
# compressão em silêncio. Então mede-se: uma amostra passa por zlib rápido; se ela ainda encolhe
# de forma material, o selo é SUSPEITO e a rota volta ao conjunto completo de backends.
# A etiqueta propõe; a medição dispõe.
#
# O QUE ESTA SONDAGEM NÃO COBRE (medido, não suposto — a régua manda declarar o limite):
# ela é uma sondagem por AMOSTRA e com zlib rápido, então enxerga redundância LOCAL. Um fluxo
# cuja estrutura seja de LONGO ALCANCE — visível só a um BWT com bloco do tamanho do arquivo
# inteiro, como a saída de um PRNG fraco — passa por ela sem ser detectado, e perde alguns por
# cento contra o caminho antigo. Foi medido: numa saída de LCG de 900 kB, o bz2-9 acha 4,5% que
# nem zlib-1 nem bz2-1 veem numa amostra de 256 KiB. Não há sondagem barata que pegue isso.
# Aceita-se o limite com os olhos abertos, porque o caso real é o inverso: mídia de verdade
# (JPEG/MP4/ZIP) é entropicamente codificada e não tem essa estrutura — nela a rota dá tamanho
# IDÊNTICO e 3,3× mais rápido (medido). E o falso-selo REALISTA — um .zip em modo "store" — é
# justamente o que a sondagem pega: a amostra cai para ~1%, o selo é rejeitado, e o arquivo
# fecha a 717× em vez de ser guardado cru.
SEAL_PROBE_BYTES = 262144    # [ENGENHARIA] amostra da sondagem (256 KiB — barata em qualquer tamanho)
SEAL_PROBE_KEEP = 0.95       # [ENGENHARIA] se a amostra cai abaixo de 95%, o selo não se sustenta


# ═══════════════════════════════════════════════════════════════════════════════
#  A LEITURA — sniff_signal: o contexto de contorno que TIPA o fluxo
# ═══════════════════════════════════════════════════════════════════════════════

def _npy_descr(data: bytes) -> str | None:
    """Lê o dtype declarado no cabeçalho .npy SEM eval (o header é um literal python)."""
    if not data.startswith(_NPY_MAGIC) or len(data) < 12:
        return None
    try:
        major = data[6]
        hlen = int.from_bytes(data[8:10], "little") if major == 1 else int.from_bytes(data[8:12], "little")
        off = 10 if major == 1 else 12
        head = data[off:off + min(hlen, 4096)].decode("latin-1", "replace")
        m = re.search(r"'descr'\s*:\s*'([^']+)'", head)
        return m.group(1) if m else None
    except Exception:
        return None


def _sealed_kind(data: bytes) -> str | None:
    for sig, kind in _SEALED_MAGICS:
        if data.startswith(sig):
            return kind
    for sig, kind in _SEALED_AT_4:
        if len(data) >= 4 + len(sig) and data[4:4 + len(sig)] == sig:
            return kind
    for sig, kind in _SEALED_AT_8:
        if len(data) >= 8 + len(sig) and data[8:8 + len(sig)] == sig:
            return kind
    return None


def _looks_structured(sample: str) -> bool:
    s = sample.lstrip()[:4096]
    if not s:
        return False
    if s[0] in "{[" and ('":' in s or "': " in s or '":' in s):
        return True
    if s.startswith("<?xml") or s.startswith("<!DOCTYPE") or (s[0] == "<" and ">" in s[:200]):
        return True
    head = s.split("\n")[:5]
    if len(head) >= 3:
        seps = [ln.count(",") for ln in head if ln]
        if seps and min(seps) >= 2 and len(set(seps)) == 1:      # csv: mesma contagem por linha
            return True
    kw = ("def ", "class ", "import ", "function ", "#include", "SELECT ", "<html", "{\n")
    return any(k in s for k in kw)


def sniff_signal(data: bytes, name: str = "") -> dict:
    """A LEITURA (peça `ontological_relativity`): tipa o fluxo pelo que ELE é.

    Nunca pela extensão do nome — o nome é rótulo, o magic é substância. Devolve o tipo
    e a evidência que o sustenta (auditável: quem quiser conferir, confere)."""
    ev: dict = {"n_bytes": len(data), "declared_name": name}
    if not data:
        return {"type": SIG_SPARSE, "evidence": {**ev, "why": "fluxo vazio"}}

    # 1) tensor .npy — magic próprio; o dtype decide se a exatidão é semântica
    descr = _npy_descr(data)
    if descr is not None:
        kind = descr[1] if len(descr) > 1 and descr[0] in "<>=|" else (descr[0] if descr else "?")
        ev["npy_descr"] = descr
        if kind in ("f", "c"):
            return {"type": SIG_TENSOR_FLOAT, "evidence": {**ev, "why": f"array .npy dtype {descr} (ponto flutuante)"}}
        return {"type": SIG_TENSOR_EXACT, "evidence": {**ev, "why": f"array .npy dtype {descr} (exatidão é semântica)"}}

    # 2) selo já posto — comprimir de novo não ganha nada
    sealed = _sealed_kind(data)
    if sealed:
        return {"type": SIG_SEALED, "evidence": {**ev, "container": sealed, "why": f"contêiner já selado ({sealed})"}}

    # 3) escassez de símbolos — a paleta é o estágio ontológico certo
    head = data[:SNIFF_BYTES]
    distinct = len(set(head))
    ev["distinct_bytes_sample"] = distinct
    if distinct <= 16 and len(set(data)) <= 16:
        return {"type": SIG_SPARSE, "evidence": {**ev, "why": f"{len(set(data))} símbolos distintos no fluxo (≤16)"}}

    # 4) texto / estrutura
    try:
        sample = head.decode("utf-8")
        printable = sum(1 for ch in sample if ch.isprintable() or ch in "\n\r\t")
        ratio = printable / len(sample) if sample else 0.0
        ev["printable_ratio"] = round(ratio, 4)
        if ratio >= 0.95:
            if _looks_structured(sample):
                return {"type": SIG_STRUCTURED, "evidence": {**ev, "why": "utf-8 com sintaxe estruturada (json/xml/csv/código)"}}
            return {"type": SIG_TEXT, "evidence": {**ev, "why": "utf-8 legível (texto natural)"}}
    except UnicodeDecodeError:
        ev["utf8"] = False

    return {"type": SIG_BINARY, "evidence": {**ev, "why": "binário genérico (sem magic conhecido, não-utf8)"}}


# ═══════════════════════════════════════════════════════════════════════════════
#  A LEI — plan_route: (tipo de sinal, regime) ↦ rota. Uma função, não um menu.
# ═══════════════════════════════════════════════════════════════════════════════

def plan_route(signal_type: str, regime: str, fidelity: str = "auto") -> dict:
    """Aplica a lei de roteamento. Determinística, sem estado, sem mão humana.

    `fidelity`: "auto" (a lei decide) | "exata" (proíbe a rota com perda — o backup usa esta).
    Devolve a rota pretendida, os backends que valem o custo, e o PORQUÊ em português."""
    if fidelity not in ("auto", "exata"):
        raise ValueError("fidelity deve ser 'auto' ou 'exata'")

    # tensor de ponto flutuante: único caso em que a rota patenteada (com perda) concorre.
    if signal_type == SIG_TENSOR_FLOAT:
        if fidelity == "exata":
            return {"route": "lossless", "backends": ("lzma", "bz2"), "candidate_lossy": False,
                    "why": "tensor de ponto flutuante, mas fidelidade EXATA exigida ⇒ a rota com perda "
                           "(g=√|L|) fica proibida; vai pela sem perdas."}
        return {"route": "gated_tensor", "backends": ("lzma", "bz2"), "candidate_lossy": True,
                "why": "tensor de ponto flutuante ⇒ o domínio nativo da patente (reflexão g=√|L|, "
                       "fase s=sign(L)) concorre com a sem perdas; quem decide é o PORTÃO DE "
                       f"FIDELIDADE medido (PSNR≥{PSNR_GATE_DB:.0f} dB, corr≥{CORR_GATE}, "
                       f"ganho≥{GAIN_MIN:.2f}×), não o operador."}

    if signal_type == SIG_TENSOR_EXACT:
        return {"route": "lossless", "backends": ("lzma", "bz2", "zlib"), "candidate_lossy": False,
                "why": "array inteiro/bool: o valor É o significado (índice, rótulo, máscara). "
                       "Perder bit é perder sentido ⇒ sem perdas, sem concorrência."}

    if signal_type == SIG_SEALED:
        return {"route": "probe_stored", "backends": ("zlib",), "candidate_lossy": False,
                "why": "contêiner já selado (comprimido/cifrado): a redundância já foi extraída por "
                       "quem o criou ⇒ o LZMA-extremo queimaria CPU para ganhar ~nada. Mas a etiqueta "
                       "não manda mais que a medição: uma SONDAGEM barata numa amostra confere se o "
                       "selo é real; se a amostra ainda encolher de forma material, o selo é suspeito "
                       "e a rota volta ao conjunto completo de backends."}

    if signal_type == SIG_SPARSE:
        return {"route": "lossless", "backends": ("lzma", "bz2", "zlib"), "candidate_lossy": False,
                "why": "pouquíssimos símbolos distintos ⇒ o estágio ontológico de paleta (reversível) "
                       "encolhe o material antes do backend de entropia."}

    if signal_type in (SIG_STRUCTURED, SIG_TEXT):
        return {"route": "lossless", "backends": ("lzma", "bz2"), "candidate_lossy": False,
                "why": "texto/estrutura: redundância de longo alcance ⇒ LZMA e BZ2 são os que pagam; "
                       "o zlib (janela de 32 KiB) não ganharia deles aqui e sai do orçamento."}

    # binário genérico: o REGIME decide o custo que vale a pena gastar
    if regime == "VAPOR":
        return {"route": "lossless", "backends": ("lzma", "zlib"), "candidate_lossy": False,
                "why": f"binário em regime {regime} (entropia ≥ 3e/2 nats): quase-incompressível. "
                       "Tenta-se LZMA + uma sondagem zlib; o BZ2 raramente ganha nesta faixa e é o "
                       "mais caro. Se nenhum ganhar, guarda-se cru — ratio<1 é resultado honesto."}
    return {"route": "lossless", "backends": ("lzma", "bz2", "zlib"), "candidate_lossy": False,
            "why": f"binário em regime {regime}: há redundância a extrair ⇒ vale medir os três "
                   "backends e ficar com o menor."}


# ═══════════════════════════════════════════════════════════════════════════════
#  A PORTA ÚNICA
# ═══════════════════════════════════════════════════════════════════════════════

def explain(data: bytes, name: str = "arquivo") -> dict:
    """Ensaio a seco: o que a lei escolheria e por quê — sem comprimir nada.
    Serve à interface (mostrar a decisão ANTES) e à auditoria."""
    sig = sniff_signal(data, name)
    ent = _codec.shannon_entropy_nats(data)
    regime = _codec.classify_regime(ent)
    plan = plan_route(sig["type"], regime, "auto")
    return {
        "signal_type": sig["type"], "evidence": sig["evidence"],
        "entropy_nats": ent, "entropy_bits_per_byte": ent / math.log(2),
        "regime": regime, "planned_route": plan["route"], "why": plan["why"],
        "backends_considered": list(plan["backends"]),
        "beta": _codec.beta_provenance(),
    }


def compress_auto(data: bytes, name: str = "arquivo", fidelity: str = "auto"):
    """A ÚNICA porta de compressão do dispositivo. O sinal escolhe o codec.

    Devolve (contêiner .acom, CompressReport). O contêiner é ACOM-LOSSLESS ou ACOM-TENSOR —
    formatos que já existiam; qualquer leitor ACOM abre. O relatório carrega a decisão
    inteira: tipo de sinal, regime, rota, porquê, e as alternativas que foram MEDIDAS."""
    sig = sniff_signal(data, name)
    ent = _codec.shannon_entropy_nats(data)
    regime = _codec.classify_regime(ent)
    plan = plan_route(sig["type"], regime, fidelity)

    alternatives: list[dict] = []
    backends = plan["backends"]
    seal_probe = None

    # A SONDAGEM DO SELO: a etiqueta propõe, a medição dispõe. Se o fluxo se diz selado mas a
    # amostra ainda encolhe, o selo não se sustenta e a rota volta ao conjunto completo.
    if plan["route"] == "probe_stored":
        import zlib as _zlib
        amostra = data[:SEAL_PROBE_BYTES]
        if amostra:
            mantido = len(_zlib.compress(amostra, 1)) / len(amostra)
            selo_real = mantido >= SEAL_PROBE_KEEP
            seal_probe = {"sample_bytes": len(amostra), "kept_fraction": round(mantido, 4),
                          "threshold": SEAL_PROBE_KEEP, "seal_holds": bool(selo_real)}
            if not selo_real:
                backends = ("lzma", "bz2", "zlib")
                plan = {**plan, "route": "sealed_label_rejected", "backends": backends,
                        "why": (plan["why"] + f" ⇒ A SONDAGEM REJEITOU O SELO: a amostra caiu para "
                                f"{mantido*100:.1f}% (< {SEAL_PROBE_KEEP*100:.0f}%), logo a redundância "
                                f"NÃO tinha sido extraída — o magic mentiu sobre o conteúdo. "
                                f"Rota promovida ao conjunto completo de backends.")}

    # rota sem perdas — sempre calculada: é o piso contra o qual tudo se compara
    lossless_c, lossless_r = _codec.compress_file(data, name, backends=backends)
    alternatives.append({"route": "lossless", "backend": lossless_r.backend,
                         "size": lossless_r.compressed_size, "ratio": round(lossless_r.ratio, 4),
                         "lossless": True})

    chosen_c, chosen_r, decided_by = lossless_c, lossless_r, "piso sem perdas (única rota admissível)"

    # a rota com perda só CONCORRE se a lei a admitiu — e só VENCE se o portão medido deixar
    if plan.get("candidate_lossy") and _codec.tensor_available():
        try:
            t_c, t_r = _codec.compress_tensor(data, name)
            psnr = t_r.psnr_db if t_r.psnr_db is not None else float("inf")
            corr = t_r.correlation if t_r.correlation is not None else 0.0
            gain = (t_r.ratio / lossless_r.ratio) if lossless_r.ratio > 0 else 0.0
            passes = (psnr >= PSNR_GATE_DB) and (corr >= CORR_GATE) and (gain >= GAIN_MIN)
            alternatives.append({"route": "graviton_reflect", "backend": t_r.backend,
                                 "size": t_r.compressed_size, "ratio": round(t_r.ratio, 4),
                                 "lossless": False, "psnr_db": (None if psnr == float("inf") else round(psnr, 2)),
                                 "correlation": round(corr, 6), "gain_vs_lossless": round(gain, 4),
                                 "gate_passed": bool(passes)})
            if passes:
                chosen_c, chosen_r = t_c, t_r
                decided_by = (f"PORTÃO DE FIDELIDADE APROVOU [ENGENHARIA]: PSNR "
                              f"{'∞' if psnr == float('inf') else f'{psnr:.1f}'} dB ≥ {PSNR_GATE_DB:.0f}, "
                              f"correlação {corr:.6f} ≥ {CORR_GATE}, ganho {gain:.2f}× ≥ {GAIN_MIN:.2f}× "
                              f"sobre a sem perdas ⇒ a reflexão g=√|L| vale a perda declarada.")
            else:
                falhas = []
                if psnr < PSNR_GATE_DB:
                    falhas.append(f"PSNR {psnr:.1f} dB < {PSNR_GATE_DB:.0f}")
                if corr < CORR_GATE:
                    falhas.append(f"correlação {corr:.6f} < {CORR_GATE}")
                if gain < GAIN_MIN:
                    falhas.append(f"ganho {gain:.2f}× < {GAIN_MIN:.2f}×")
                decided_by = ("PORTÃO DE FIDELIDADE REPROVOU [ENGENHARIA] (" + "; ".join(falhas) +
                              ") ⇒ a perda não se paga; fica a sem perdas, bit-exata.")
        except Exception as e:                      # tensor ilegível/estranho: o piso sustenta
            alternatives.append({"route": "graviton_reflect", "error": str(e)[:160], "gate_passed": False})
            decided_by = f"rota com perda indisponível para este fluxo ({str(e)[:80]}) ⇒ sem perdas."

    chosen_r.signal_type = sig["type"]
    chosen_r.route = "graviton_reflect" if not chosen_r.lossless else (
        "stored" if chosen_r.backend == "stored" else "entropy_" + chosen_r.backend)
    chosen_r.decision_why = plan["why"]
    chosen_r.decided_by = decided_by
    chosen_r.signal_evidence = sig["evidence"].get("why")
    chosen_r.alternatives = alternatives
    chosen_r.auto_version = AUTO_VERSION
    if seal_probe is not None:
        chosen_r.seal_probe = seal_probe
    return chosen_c, chosen_r


def decompress_auto(container: bytes):
    """A descompressão JÁ era única: o contêiner se declara e o codec despacha.
    Existe aqui só para a simetria da porta — e para que ninguém precise saber o modo."""
    return _codec.decompress_any(container)


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTODEMONSTRAÇÃO (forma = conteúdo) — a lei é provada, não afirmada
# ═══════════════════════════════════════════════════════════════════════════════

def selftest() -> dict:
    """Sintetiza um sinal de CADA tipo e prova que a leitura os tipa e a lei os roteia —
    sem que ninguém marque caixinha nenhuma. Round-trip verificado em toda rota."""
    import gzip as _gzip
    import io as _io
    import json as _json

    casos: list[tuple[str, bytes, str]] = []

    casos.append(("texto natural", ("A fronteira é auto-conjugada e o Um se preserva. " * 400).encode("utf-8"), SIG_TEXT))
    casos.append(("json estruturado", _json.dumps([{"i": i, "beta": "alpha*sqrt(e)"} for i in range(500)]).encode(), SIG_STRUCTURED))
    casos.append(("esparso (paleta)", bytes([(i % 4) for i in range(20000)]), SIG_SPARSE))

    rnd = bytearray()
    seed = 12345
    for _ in range(20000):                       # PRNG determinístico: alta entropia, sem depender de random
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        rnd.append((seed >> 16) & 0xFF)
    rnd = bytes(rnd)
    casos.append(("binário alta entropia", rnd, SIG_BINARY))

    # selado REALISTA: um .gz de verdade, com conteúdo de verdade e a redundância já extraída
    _b = _io.BytesIO()
    with _gzip.GzipFile(fileobj=_b, mode="wb", mtime=0) as _g:
        _g.write(rnd)
    casos.append(("selado (gzip real)", _b.getvalue(), SIG_SEALED))

    if _codec.tensor_available():
        import numpy as _np
        x = _np.linspace(-3.0, 3.0, 4096)
        campo = (_np.sin(x * 3.0) * _np.exp(-x * x / 4.0)).astype(_np.float64)
        b = _io.BytesIO(); _np.save(b, campo); casos.append(("tensor float (campo suave)", b.getvalue(), SIG_TENSOR_FLOAT))
        idx = _np.arange(4096, dtype=_np.int32)
        b2 = _io.BytesIO(); _np.save(b2, idx); casos.append(("tensor int (índices)", b2.getvalue(), SIG_TENSOR_EXACT))

    resultados = []
    ok = True
    for rotulo, dados, esperado in casos:
        sig = sniff_signal(dados, rotulo)
        tipo_ok = sig["type"] == esperado
        cont, rep = compress_auto(dados, rotulo)
        # round-trip por rota: sem perdas ⇒ bit-exato; com perda ⇒ apenas abre e mede
        rt_ok = True
        try:
            out, _nome, meta = decompress_auto(cont)
            rt_ok = (out == dados) if rep.lossless else (len(out) > 0)
        except Exception as e:
            rt_ok = False
            meta = {"erro": str(e)[:80]}
        ok = ok and tipo_ok and rt_ok
        resultados.append({
            "sinal": rotulo, "tipo_lido": sig["type"], "tipo_esperado": esperado, "tipo_ok": tipo_ok,
            "regime": rep.regime, "rota": rep.route, "sem_perdas": rep.lossless,
            "ratio": round(rep.ratio, 3), "round_trip_ok": rt_ok,
        })

    # A SONDAGEM DO SELO, provada nos DOIS lados (a etiqueta propõe, a medição dispõe):
    #  (a) selo VERDADEIRO (conteúdo já sem redundância) ⇒ sustenta-se ⇒ rota barata;
    #  (b) selo FALSO realista (.zip em modo "store") ⇒ é REJEITADO ⇒ rota promovida.
    import zipfile as _zip
    _bz = _io.BytesIO()
    with _zip.ZipFile(_bz, "w", _zip.ZIP_STORED) as _z:
        _z.writestr("doc.txt", "A fronteira e auto-conjugada e o Um se preserva. " * 4000)
    _falso = _bz.getvalue()
    _cf, _rf = compress_auto(_falso, "selo_falso.zip", "exata")
    _bv = _io.BytesIO()
    with _gzip.GzipFile(fileobj=_bv, mode="wb", mtime=0) as _g:
        _g.write(rnd)
    _cv, _rv = compress_auto(_bv.getvalue(), "selo_real.gz", "exata")
    sondagem = {
        "selo_falso_zip_store": {"rejeitado": bool(_rf.seal_probe and not _rf.seal_probe["seal_holds"]),
                                 "amostra_manteve": (_rf.seal_probe or {}).get("kept_fraction"),
                                 "rota": _rf.route, "ratio": round(_rf.ratio, 1),
                                 "round_trip_ok": decompress_auto(_cf)[0] == _falso},
        "selo_real_gzip": {"sustentou": bool(_rv.seal_probe and _rv.seal_probe["seal_holds"]),
                           "amostra_manteve": (_rv.seal_probe or {}).get("kept_fraction"),
                           "rota": _rv.route,
                           "round_trip_ok": decompress_auto(_cv)[0] == _bv.getvalue()},
        "limite_declarado": ("sondagem por AMOSTRA com zlib: enxerga redundância LOCAL; estrutura de "
                             "LONGO ALCANCE (ex.: PRNG fraco) passa e custa alguns %. Mídia real não "
                             "tem essa estrutura. [ENGENHARIA] — limite medido, não suposto."),
    }
    ok = ok and sondagem["selo_falso_zip_store"]["rejeitado"] and sondagem["selo_real_gzip"]["sustentou"]
    ok = ok and sondagem["selo_falso_zip_store"]["round_trip_ok"] and sondagem["selo_real_gzip"]["round_trip_ok"]

    # a prova do fecho: NINGUÉM passou modo algum — e o tensor float foi para a rota nativa
    tensor_caso = next((r for r in resultados if r["tipo_lido"] == SIG_TENSOR_FLOAT), None)
    fecho = {
        "chaveamento_humano": False,
        "porta_unica": "compress_auto(data, name) — nenhum parâmetro de modo",
        "tensor_roteado_sem_toggle": (tensor_caso is not None and tensor_caso["rota"] in ("graviton_reflect", "entropy_lzma", "entropy_bz2", "stored")),
        "fidelidade_exata_proibe_perda": plan_route(SIG_TENSOR_FLOAT, "VACUUM", "exata")["candidate_lossy"] is False,
    }
    return {"ok": bool(ok and all(fecho[k] is not False for k in ("tensor_roteado_sem_toggle", "fidelidade_exata_proibe_perda"))),
            "casos": resultados, "fecho": fecho, "sondagem_do_selo": sondagem,
            "beta": _codec.beta_provenance(),
            "portao_fidelidade": {"psnr_db": PSNR_GATE_DB, "correlacao": CORR_GATE,
                                  "ganho_minimo": GAIN_MIN, "estatuto": "[ENGENHARIA] — declarado, NÃO derivado de β"},
            "auto_version": AUTO_VERSION, "patent": PATENT_ID}


if __name__ == "__main__":
    import json as _j
    r = selftest()
    print(_j.dumps(r, ensure_ascii=False, indent=2))
    raise SystemExit(0 if r["ok"] else 1)
