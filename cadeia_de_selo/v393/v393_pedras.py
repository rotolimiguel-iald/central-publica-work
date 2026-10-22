# -*- coding: utf-8 -*-
"""v393_pedras.py -- a LISTA das pedras da v393 (3 pedras da REGRA, entregues pelo Codex em 14/10/2026) com a ORIGEM de cada uma (copia em pedras/*.orig.lean, sha conferido contra o
encaminhamento AO_CLAUDE_INTEGRAR_REGRA_V393.md §5) e a regra de derivacao para o kernel embutido. Nenhum sha e' digitado como pino: os pinos sao LIDOS dos arquivos por script e so'
CRUZADOS com os 3 sha de entrega do encaminhamento (lidos do proprio .md por regex). Ordem = ordem de instalacao (dependencia): o contrato primeiro.
Derivacao (ajuste de modulo/import, sem tocar nos enunciados nem nas provas):
  (1) `import RuleTruthContract` -> `import TGLExt.RuleTruthContract` (o contrato vive agora em TGLExt/, nao na raiz do sandbox do Codex);
  (2) o bloco final `open Lean in run_cmd do ... LOCAL_DECL ...` (auditoria LOCAL do sandbox do Codex; imprime milhares de linhas LOCAL_DECL no lake build e nao faz parte do kernel) e' REMOVIDO;
      a auditoria de axiomas do kernel passa a ser a do TGL/Audit.lean (#print axioms por declaracao + o run_cmd de cobertura total KH-N1).
Gerencia c1, 14/10/2026 (preparacao da cadeia v393). Nada aqui move o gate."""
import hashlib, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
WK = os.path.dirname(os.path.dirname(HERE))                       # ...\work
PD = os.path.join(HERE, "pedras")
ENC = os.path.join(HERE, "insumos", "AO_CLAUDE_INTEGRAR_REGRA_V393.md")
sha256 = lambda b: hashlib.sha256(b).hexdigest()

RUN_CMD_INICIO = b"\nopen Lean in\nrun_cmd do\n"

STONES = [
    dict(mod="RuleTruthContract", sigla="rtc", src=os.path.join(PD, "RuleTruthContract.orig.lean"), derive="strip_run_cmd", entrega_nome="RuleTruthContract.lean"),
    dict(mod="TheRuleAndTheFigureOfTruth", sigla="rft", src=os.path.join(PD, "TheRuleAndTheFigureOfTruth.orig.lean"), derive="import_contrato", entrega_nome="TheRuleAndTheFigureOfTruth.lean"),
    dict(mod="TheRuleInTheContinuousMotor", sigla="rcm", src=os.path.join(PD, "TheRuleInTheContinuousMotor.orig.lean"), derive="import_contrato_e_strip", entrega_nome="TheRuleInTheContinuousMotor.lean"),
]


def bytes_da_pedra(s):
    b = open(s["src"], "rb").read()
    nl = b"\r\n" if b"\r\n" in b else b"\n"
    if s["derive"] in ("import_contrato", "import_contrato_e_strip"):
        velho, novo = b"import RuleTruthContract" + nl, b"import TGLExt.RuleTruthContract" + nl
        assert b.count(velho) == 1, "import do contrato nao achado"
        b = b.replace(velho, novo)
    if s["derive"] in ("strip_run_cmd", "import_contrato_e_strip"):
        ini = nl + b"open Lean in" + nl + b"run_cmd do" + nl
        assert b.count(ini) == 1, "bloco run_cmd local nao achado exatamente 1x"
        i = b.index(ini)
        corpo = i + len(ini)
        m = re.search(re.escape(nl + b"#print axioms") + b"|\\Z", b[corpo:])
        j = corpo + m.start()
        resto = b[j:].lstrip(b"\r\n")
        b = (b[:i] + nl + resto) if resto.strip() else (b[:i].rstrip(b"\r\n") + nl)
    return b


def entrega_sha(s):
    """sha256 declarado pelo encaminhamento do Codex para o arquivo ORIGINAL (§5 do .md), lido por regex do proprio texto."""
    t = open(ENC, encoding="utf-8").read()
    m = re.search(r"formal\\" + re.escape(s["entrega_nome"]) + r"`\s*[—-]\s*SHA256\s*`([0-9a-f]{64})`", t)
    assert m, ("sha de entrega nao achado no encaminhamento", s["entrega_nome"])
    return m.group(1)


def gerar_pinos():
    out = []
    for s in STONES:
        orig = open(s["src"], "rb").read(); b = bytes_da_pedra(s)
        out.append({"mod": s["mod"], "modulo": "TGLExt." + s["mod"], "arquivo": "TGLExt/%s.lean" % s["mod"], "sigla": s["sigla"], "src": s["src"], "derivada": s["derive"],
                    "sha256": sha256(b), "bytes": len(b), "sha256_original": sha256(orig), "bytes_original": len(orig), "sha256_da_entrega": entrega_sha(s),
                    "confere_com_a_entrega": sha256(orig) == entrega_sha(s)})
    return out


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for p in gerar_pinos():
        print(p["mod"], "orig", p["sha256_original"][:16], "->", p["sha256"][:16], p["bytes"], "entrega_ok=%s" % p["confere_com_a_entrega"], "derivada=%s" % p["derivada"])
        b = bytes_da_pedra([s for s in STONES if s["mod"] == p["mod"]][0]); print("   cauda:", repr(b[-160:]))
