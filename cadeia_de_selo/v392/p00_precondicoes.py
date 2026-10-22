# -*- coding: utf-8 -*-
"""p00_precondicoes.py -- confere, SO LENDO, as pre-condicoes de bytes da v392 (o que o plano chama de P-pre-condicoes que um script consegue medir).
Nada e escrito fora de PRECONDICOES_v392.json (nesta pasta). Os pinos sao LIDOS do selo/core/arquivos, nunca digitados. Fail-closed: rc 1 se algo falha.
uso: python -I -B -X utf8 p00_precondicoes.py"""
import hashlib, json, os, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v392_pedras as P  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); NK = os.path.join(NOS, "tgl_kernel")
KS = os.path.join("C:" + os.sep, "t", "k392", "kernel")
sha = lambda b: hashlib.sha256(b).hexdigest()
res = []; ok_all = True


def chk(nome, cond, det=None):
    global ok_all
    res.append({"checagem": nome, "ok": bool(cond), "detalhe": det}); ok_all = ok_all and bool(cond)
    print(("OK   " if cond else "FALHA"), nome, "" if det is None else "-> " + str(det)[:220])


raw = open(os.path.join(NOS, "um.py"), "rb").read(); selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
chk("um.py do Nos == o que o selo pina (v391)", sha(raw) == selo["sha256"]["um.py"] and selo.get("um_version") == "v391", sha(raw)[:16])
el = core["external_ladder"]; axr = core["kernel_formalization"]["axiom_report"]
chk("escada v391 6163/6163 e axiom_report lido do core", el["n_theorems_clean"] == el["n_theorems_expected"] == 6163, [el["n_theorems_clean"], el["n_theorems_expected"], len(axr)])
chk("nenhum registro v392 no core ainda", not any("v392" in k for k in core), [k for k in core if "v392" in k])
raiz, aud = open(os.path.join(NK, "TGLExt.lean"), "rb").read(), open(os.path.join(NK, "TGL", "Audit.lean"), "rb").read()
chk("raiz e Audit do Nos == os do sandbox C:\\t\\k392 (ponto de partida)", raiz == open(os.path.join(KS, "TGLExt.lean"), "rb").read() and aud == open(os.path.join(KS, "TGL", "Audit.lean"), "rb").read(),
    [sha(raiz)[:16], sha(aud)[:16]])
fl = json.load(open(os.path.join(NK, "tgl_kernel_proof_manifest.json"), encoding="utf-8")) if os.path.exists(os.path.join(NK, "tgl_kernel_proof_manifest.json")) else None
pins = P.gerar_pinos()
chk("13 pedras: sha dos bytes == sha de entrega (inventario F_KERNEL / recibos de 13/10)", all(p["confere_com_a_entrega"] for p in pins) and len(pins) == 13, [(p["mod"], p["sha256"][:8]) for p in pins if not p["confere_com_a_entrega"]])
chk("nenhuma das 13 pedras ja esta no kernel do Nos", not any(os.path.exists(os.path.join(NK, "TGLExt", p["mod"] + ".lean")) for p in pins))
chk("nenhuma das 13 pedras ja esta no sandbox", not any(os.path.exists(os.path.join(KS, "TGLExt", p["mod"] + ".lean")) for p in pins) or os.environ.get("V392_JA_PREPARADO") == "1")
# os imports de cada pedra existem no kernel do Nos ou entre as pedras
mods_nos = {f[:-5] for f in os.listdir(os.path.join(NK, "TGLExt")) if f.endswith(".lean")}
mods_nos |= {os.path.relpath(os.path.join(r, f), os.path.join(NK, "TGLExt"))[:-5].replace(os.sep, ".") for r, _, fs in os.walk(os.path.join(NK, "TGLExt")) for f in fs if f.endswith(".lean")}
novos = {p["mod"] for p in pins}; faltam = []
for p in pins:
    for m in re.finditer(rb"^import\s+TGLExt\.([\w.]+)", P.bytes_da_pedra([s for s in P.STONES if s["mod"] == p["mod"]][0]), re.M):
        nm = m.group(1).decode()
        if nm not in mods_nos and nm not in novos:
            faltam.append((p["mod"], nm))
chk("todo import TGLExt.X de cada pedra existe no kernel do Nos ou entre as 13", not faltam, faltam)
# a ordem de instalacao respeita as dependencias entre as pedras
ordem = [p["mod"] for p in pins]; viol = []
for p in pins:
    for m in re.finditer(rb"^import\s+TGLExt\.([\w.]+)", P.bytes_da_pedra([s for s in P.STONES if s["mod"] == p["mod"]][0]), re.M):
        nm = m.group(1).decode()
        if nm in novos and ordem.index(nm) > ordem.index(p["mod"]):
            viol.append((p["mod"], nm))
chk("a ordem de instalacao respeita as dependencias entre as pedras", not viol, viol)
# ancoras do candidato no um.py v391 (cada uma UMA vez)
T = raw.decode("utf-8")
ancoras = {"UM_VERSION": r'^UM_VERSION = "v391"', "flag_ancora": '    "ext_cpl_half_nat_fixed_point_kernel_proved": "TGLExt.TheCouplingRunsBoundedBelow.half_nat_fixed_point",',
           "ladder_ancora": '        "ext_cpl_half_nat_fixed_point_kernel_proved",', "ledger_v390": '    ("v390", "Fundacao", "TGLExt/Fundacao.lean", None, None),',
           "sorry_l192945": '''sorry = "declaration uses 'sorry'" in out''', "tokens_fn": "def _lean_source_forbidden_tokens():", "embedded": "_EMBEDDED_KERNEL_FILES = {"}
for k, a in ancoras.items():
    n = len(re.findall(a, T, re.M)) if k == "UM_VERSION" else T.count(a)
    chk("ancora do um.py %s ocorre exatamente 1 vez" % k, n == 1, n)
chk("pdflatex disponivel", shutil.which("pdflatex") is not None, shutil.which("pdflatex"))
chk("lake e lean (elan) disponiveis", shutil.which("lake") is not None and shutil.which("lean") is not None, shutil.which("lake"))
chk("pasta do vinculo R3_3 (esboco, bateria) existe", os.path.exists(os.path.join(P.WK, "bancada_vinculo_12out", "R3_3", "sincronizar_bancada.py")) and os.path.exists(os.path.join(P.WK, "bancada_vinculo_12out", "BATERIA_VINCULO.json")))
chk("Bancada Um de producao existe (so leitura)", os.path.isdir(os.path.join("C:" + os.sep, "IALD", "Bancada_Um")))
chk("o quadro da PORTA: o Nos nao tem processo um.py (nao medido por nome; ver instalar_v392)", True, "a instalacao tem o vigia proprio")
out = {"quando": __import__("datetime").datetime.now().isoformat(timespec="seconds"), "ok": ok_all, "um_py_sha16": sha(raw)[:16], "selo_sha256_do_um_py": selo["sha256"]["um.py"][:16],
       "pedras": [{k: v for k, v in p.items() if k not in ("src",)} for p in pins], "checagens": res}
open(os.path.join(HERE, "PRECONDICOES_v392.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print("\nPRECONDICOES:", "TODAS PASSARAM" if ok_all else "FALHOU"); sys.exit(0 if ok_all else 1)
