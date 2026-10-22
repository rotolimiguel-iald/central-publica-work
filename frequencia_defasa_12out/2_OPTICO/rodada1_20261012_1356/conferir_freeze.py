# -*- coding: utf-8 -*-
"""CONSTRUTOR OTICO, F1.FREQUENCIA (trilha POSTO), gerencia c1.
Conferencia de integridade ANTES de qualquer ensaio (somente leitura fora de 2_OPTICO).
(1) sha256 de PREREGISTRO.json / PREREGISTRO.md contra o FREEZE.json e contra os valores dados na ordem;
(2) sha256 de cada arquivo listado em FREEZE.demais_arquivos_da_pasta; nenhum arquivo novo em 1_PREREGISTRO;
(3) pinos do pre-registro (um.py, core, selo: sha256 integral; demais: sha16) e pinos do kernel (sha16);
(4) verbatins V1..V4 (sha256 e bytes) e o trecho V2 l.1-33.
Grava SO em 2_OPTICO (CONFERENCIA_FREEZE.json). Sai com codigo 2 na primeira divergencia, imprimindo-a."""
import hashlib, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PRE = os.path.join(os.path.dirname(AQUI), "1_PREREGISTRO")
KERNEL = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel"
# valores dados na ordem (texto da tarefa) -- conferidos contra o FREEZE e contra os bytes
ORDEM_JSON_SHA = "0c20d7c196a4c7efa75b6eae86fe233c5b12735f1e958f396b3b33a8634df813"
ORDEM_MD_SHA = "3c80ea21057c337153f5cf135b3f99677f6b85916677924b47d811bef71ae066"
ORDEM_CONGELADO = "2026-10-12T16:22:52.525493+00:00"
ORDEM_PINOS_INTEGRAIS = {
    "um.py": (33910631, "8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6"),
    "um_absoluto.json": (5003275, "a74241ff380b1b0e3d44a8f2c39e7ad4d462624b145353f3e4d82f3131036e98"),
    "um_absoluto_selo.json": (113926, "95061f18c7102248ebd00c9414f1ef0dadcf08cefc1bec00bf046d778b38070a"),
}
divergencias = []
ok = []


def sha_arquivo(p):
    h = hashlib.sha256()
    n = 0
    with open(p, "rb") as fh:
        while True:
            b = fh.read(1 << 20)
            if not b:
                break
            h.update(b)
            n += len(b)
    return n, h.hexdigest()


def diverge(m):
    divergencias.append(m)
    print("DIVERGENCIA:", m)


F = json.load(open(os.path.join(PRE, "FREEZE.json"), encoding="utf-8"))
nF, hF = sha_arquivo(os.path.join(PRE, "FREEZE.json"))
if F.get("congelado_utc") != ORDEM_CONGELADO:
    diverge("FREEZE.congelado_utc %r != ordem %r" % (F.get("congelado_utc"), ORDEM_CONGELADO))
for nome, ordem_sha in (("PREREGISTRO.json", ORDEM_JSON_SHA), ("PREREGISTRO.md", ORDEM_MD_SHA)):
    n, h = sha_arquivo(os.path.join(PRE, nome))
    if h != F[nome]["sha256"] or n != F[nome]["bytes"]:
        diverge("%s: disco (%d, %s) != FREEZE (%d, %s)" % (nome, n, h, F[nome]["bytes"], F[nome]["sha256"]))
    if h != ordem_sha:
        diverge("%s: disco %s != ordem %s" % (nome, h, ordem_sha))
    ok.append("%s %d B sha256 %s = FREEZE = ordem" % (nome, n, h))

# demais arquivos da pasta
vistos = set()
for dp, dns, fns in os.walk(PRE):
    dns.sort()
    for fn in sorted(fns):
        rel = os.path.relpath(os.path.join(dp, fn), PRE).replace("\\", "/")
        vistos.add(rel)
esperados = set(F["demais_arquivos_da_pasta"]) | {"FREEZE.json", "PREREGISTRO.json", "PREREGISTRO.md"}
for extra in sorted(vistos - esperados):
    diverge("arquivo novo em 1_PREREGISTRO depois do FREEZE: " + extra)
for falta in sorted(esperados - vistos):
    diverge("arquivo do FREEZE ausente em 1_PREREGISTRO: " + falta)
for rel, (nb, hs) in sorted(F["demais_arquivos_da_pasta"].items()):
    p = os.path.join(PRE, rel.replace("/", os.sep))
    if not os.path.exists(p):
        continue
    n, h = sha_arquivo(p)
    if (n, h) != (nb, hs):
        diverge("%s: disco (%d, %s) != FREEZE (%d, %s)" % (rel, n, h, nb, hs))
ok.append("%d demais arquivos do FREEZE conferem; nenhum arquivo novo em 1_PREREGISTRO" % len(F["demais_arquivos_da_pasta"]))

D = json.load(open(os.path.join(PRE, "PREREGISTRO.json"), encoding="utf-8"))
# pinos
pinos_out = []
for caminho, nb, hs in D["pinos"]:
    n, h = sha_arquivo(caminho)
    base = os.path.basename(caminho)
    if len(hs) == 64:
        if (n, h) != (nb, hs):
            diverge("pino %s: disco (%d, %s) != pre-registro (%d, %s)" % (caminho, n, h, nb, hs))
        if base in ORDEM_PINOS_INTEGRAIS and ORDEM_PINOS_INTEGRAIS[base] != (n, h):
            diverge("pino %s difere da ordem" % base)
    else:
        if n != nb or h[:16] != hs:
            diverge("pino %s: disco (%d, %s) != pre-registro (%d, %s)" % (caminho, n, h[:16], nb, hs))
    pinos_out.append([caminho, n, h])
ok.append("%d pinos do pre-registro conferem (um.py, core e selo por sha256 integral = ordem)" % len(D["pinos"]))
kpin = []
for s in D["pinos_kernel_sha16"]:
    rel, h16 = s.rsplit(" ", 1)
    n, h = sha_arquivo(os.path.join(KERNEL, rel.replace("/", os.sep)))
    if h[:16] != h16:
        diverge("pino de kernel %s: disco %s != pre-registro %s" % (rel, h[:16], h16))
    kpin.append([rel, n, h])
ok.append("%d pinos de kernel (sha16) conferem" % len(kpin))

# verbatins
base_t = "C:\\IALD\\Central de Patentes\\work\\"
TEXTOS = {
    "V1": base_t + "cunhagens_12out\\OPERADOR_10out_posto_rank_texto_verbatim.txt",
    "V2": base_t + "cunhagens_12out\\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
    "V3": base_t + "cunhagens_10out\\OPERADOR_10out_posto_rank_verbatim.txt",
    "V4": base_t + "cunhagens_10out\\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt",
}
SHA16_ORDEM = {"V1": "8d252f24e2806ff3", "V2": "2c8b7b712aa9ad7f", "V3": "5b9afcc691a0e1e4", "V4": "b365591ceb346cdf"}
verb = {}
for c, p in TEXTOS.items():
    n, h = sha_arquivo(p)
    v = D["a_verbatins"][c]
    if h != v["sha256"] or n != v["bytes"] or h[:16] != SHA16_ORDEM[c]:
        diverge("verbatim %s: disco (%d, %s) != pre-registro (%d, %s) / ordem %s" % (c, n, h, v["bytes"], v["sha256"], SHA16_ORDEM[c]))
    verb[c] = [os.path.basename(p), n, h]
b2 = open(TEXTOS["V2"], "rb").read().split(b"\n")
tr = b"\n".join(b2[:33])
if hashlib.sha256(tr).hexdigest() != D["a_verbatins"]["V2"]["trilha"]["sha256"] or not b2[33].startswith("O que mais me fascina".encode("utf-8")):
    diverge("trecho V2 l.1-33")
ok.append("V1..V4 conferem (sha256, bytes, sha16 da ordem); trecho V2 l.1-33 sha256 %s" % hashlib.sha256(tr).hexdigest())

out = {
    "documento": "CONFERENCIA DO FREEZE pelo construtor otico (antes de qualquer ensaio)",
    "FREEZE.json": [nF, hF],
    "PREREGISTRO.json": F["PREREGISTRO.json"],
    "PREREGISTRO.md": F["PREREGISTRO.md"],
    "pinos": pinos_out,
    "pinos_kernel": kpin,
    "verbatins": verb,
    "ok": ok,
    "divergencias": divergencias,
    "veredito": "CONFERE" if not divergencias else "DIVERGE",
}
b = (json.dumps(out, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
alvo = os.path.join(AQUI, "CONFERENCIA_FREEZE%s.json" % (("_" + sys.argv[1]) if len(sys.argv) > 1 else ""))
tmp = alvo + ".tmp"
open(tmp, "wb").write(b)
if open(tmp, "rb").read() != b:
    raise SystemExit("FALHA VISIVEL: temporario nao confere")
os.replace(tmp, alvo)
for linha in ok:
    print("OK", linha)
print("VEREDITO_CONFERENCIA", out["veredito"], "FREEZE.json", nF, hF)
sys.exit(0 if not divergencias else 2)
