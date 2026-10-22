# -*- coding: utf-8 -*-
"""diff_e_pinos_v395.py -- (1) DIFF_KERNEL_v395.txt: arquivos novos, removidos e mudados do kernel embutido do candidato contra o da v394 (com o diff da raiz e a contagem do Audit); (2) PINOS_BN_v395.json: os sha256 que o elo B(n)
pede (esboco R3.5, gerador e driver da bateria, base R2, CRITERIOS, recibo do kernel, recibo pre_selo, selo e manifesto do kernel da v394 SELADA), LIDOS dos arquivos por script (o path e o sha256 de cada um sao recalculados aqui;
nada digitado). O recibo pre_selo e' o que o ensaio do B(n) gerou ANTES da instalacao (PINO_RECIBO_PRE_SELO_v395.json). Nao ha salto de versoes (a Bancada pina a v394 e o Nos e' a v394): nao ha pino de cadeia de selos.
Molde: diff_e_pinos_v394.py. Uso: python -I -B -X utf8 diff_e_pinos_v395.py   (roda DEPOIS de gerar_esperados_v395.py: o pino do ESPERADOS e' o do arquivo final)"""
import ast, difflib, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v395 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
BASE = os.path.join(HERE, DL.BASE_DIR)
E0, _, _, h0 = carregar(os.path.join(BASE, "um.py")); E1, _, _, h1 = carregar(os.path.join(HERE, DL.CANDIDATO))
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v394 (%s) -> v395 (%s)" % (h0, h1), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, sha(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a, b = E0[k].splitlines(), E1[k].splitlines(); d = list(difflib.unified_diff(a, b, "v394/" + k, "v395/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, sha(E0[k].encode())[:16], sha(E1[k].encode())[:16], sum(1 for l in d if l.startswith("+") and not l.startswith("+++")), sum(1 for l in d if l.startswith("-") and not l.startswith("---"))))
    out += ["      " + l[:200] for l in d[:40]]
open(os.path.join(HERE, "DIFF_KERNEL_v395.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out[:3]), "...", "novos", len(novos), "removidos", len(removidos), "mudados", mudados)
assert novos == [DL.STONE_REL] and not removidos and sorted(mudados) == ["TGL/Audit.lean", "TGLExt.lean"], ("o diff do kernel nao e' so' a pedra + raiz + Audit", novos, removidos, mudados)
V = os.path.join(HERE, "vinculo")
f = lambda p, **kw: dict({"path": p, "sha256": sha(open(p, "rb").read()), "bytes": os.path.getsize(p)}, **kw) if os.path.exists(p) else {"path": p, "sha256": None, "estado": "NAO_PREPARADO"}
pr = json.load(open(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v395.json"), encoding="utf-8"))
assert sha(open(pr["path"], "rb").read()) == pr["sha256"], "o recibo pre-selo mudou desde o pino"
rp = {"path": pr["path"], "sha256": pr["sha256"], "versao_nos": pr["versao_nos"], "veredito": pr["veredito"], "utilizavel_como_recibo_pre_selo_do_B_n": pr["utilizavel_como_recibo_pre_selo_do_B_n"], "pino_do_pino": f(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v395.json")),
      "um_py_sha16_do_nos": pr["um_py_sha16_do_nos"], "bancada_pina": pr["bancada_pina"], "sem_salto": True}
P4 = json.load(open(os.path.join(DL.V394, "PINOS_BN_v394.json"), encoding="utf-8"))   # a fusao R3.4/R3.5: o esboco, o gerador e o driver da bateria, a base R2 (so' leitura; o sha e' RECALCULADO do arquivo)
def do_v394(k):
    d = P4[k]; assert os.path.exists(d["path"]) and sha(open(d["path"], "rb").read()) == d["sha256"], ("o pino herdado da v394 diverge do arquivo", k)
    return f(d["path"], origem="PINOS_BN_v394.json[%s] (recalculado do arquivo)" % k)
kr = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v395.json"), encoding="utf-8"))
pn = {"criterios": f(os.path.join(V, "CRITERIOS_v395.json")), "kernel_recibo": f(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v395.json"), contrato=kr["contrato"], n_pedras=len(kr["pedras"]), modulos_de_auditoria=kr.get("modulos_de_auditoria", [])),
      "candidato": f(os.path.join(HERE, DL.CANDIDATO)), "esperados": f(os.path.join(HERE, "ESPERADOS_v395.json")), "pins_do_candidato": f(os.path.join(HERE, "v395_pins.py")),
      "esboco_R3_5": do_v394("esboco_R3_5"), "gerador_bateria": do_v394("gerador_bateria"), "driver_t12_t14": do_v394("driver_t12_t14"), "bateria_base_R2": do_v394("bateria_base_R2"),
      "bateria_do_pre_selo": f(pr["bateria"]["path"], versao="v394", nota="a bateria do ensaio pre_selo (a da v394 gerada e pinada na cadeia anterior); a do POS_SELO da v395 e' GERADA pelo chain depois do selo"),
      "recibo_pre_selo": rp,
      "selo_anterior_v394": f(os.path.join(BASE, "um_absoluto_selo.json"), nota="o selo da v394 (custodia, o FIM da cadeia anterior): --selo-anterior"),
      "kernel_manifesto_anterior_v394": f(os.path.join(BASE, "tgl_kernel_proof_manifest.json"), nota="o manifesto do kernel da v394 (custodia): --kernel-manifesto-anterior"),
      "nota": "[REAL] lido dos arquivos por script (diff_e_pinos_v395.py): path e sha256 RECALCULADOS; sem salto de versoes (a Bancada de producao pina a v394 = o Nos de antes da instalacao), logo sem pino de cadeia de selos nem 3o argumento do b3_recibo; "
              "o esboco R3.5 e a bateria/driver sao os da cadeia anterior (R3_5), reaproveitados; os vereditos esperados do passo simples (REPINADA_B5__...) estao no ESTADO_V395.md [lidos do codigo do esboco pelo exame do pre_selo, nao rodados]."}
bad = [k for k, v in pn.items() if isinstance(v, dict) and "path" in v and v.get("sha256") is None]
assert not bad, ("pino sem arquivo", bad)
json.dump(pn, open(os.path.join(HERE, "PINOS_BN_v395.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: (v["sha256"] or "NAO_PREPARADO")[:16] for k, v in pn.items() if isinstance(v, dict) and "sha256" in v})
