# -*- coding: utf-8 -*-
"""diff_e_pinos_v394.py -- (1) DIFF_KERNEL_v394.txt: arquivos novos, removidos e mudados do kernel embutido do candidato contra o da v393 (com o diff da raiz e a contagem do Audit); (2) PINOS_BN_v394.json: os sha256
que o elo B(n) pede (esboco, bateria, CRITERIOS, recibo do kernel, recibo pre-selo), LIDOS dos arquivos. O recibo pre-selo e' o do ENSAIO de 19/10 contra a v393 instalada: PINADO, mas marcado
`utilizavel_como_recibo_pre_selo_do_B_n = false` (a bateria R2 falhou em T12/T13 e o esboco R3.3 exige JA_SINCRONIZADA + BATERIA_PASSA; ver ESTADO_V394 §6). Uso: python -I -B -X utf8 diff_e_pinos_v394.py"""
import ast, difflib, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta19_v394 as DL  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
sha = lambda b: hashlib.sha256(b).hexdigest()
if sha(open(os.path.join(NOS, "um.py"), "rb").read())[:16] != "18be2ddb06c60f90":   # o Nos ja nao e' a v393 (rito em curso): a v393 selada vem da copia base_v393
    NOS = os.path.join(HERE, "base_v393")
E0, _, _, h0 = carregar(os.path.join(NOS, "um.py")); E1, _, _, h1 = carregar(os.path.join(HERE, DL.CANDIDATO))
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v393 (%s) -> v394 (%s)" % (h0, h1), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, sha(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a, b = E0[k].splitlines(), E1[k].splitlines(); d = list(difflib.unified_diff(a, b, "v393/" + k, "v394/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, sha(E0[k].encode())[:16], sha(E1[k].encode())[:16], sum(1 for l in d if l.startswith("+") and not l.startswith("+++")), sum(1 for l in d if l.startswith("-") and not l.startswith("---"))))
    out += ["      " + l[:200] for l in d[:40]]
open(os.path.join(HERE, "DIFF_KERNEL_v394.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out[:3]), "...", "novos", len(novos), "removidos", len(removidos), "mudados", mudados)
V = os.path.join(HERE, "vinculo")
f = lambda p: {"path": p, "sha256": sha(open(p, "rb").read())} if os.path.exists(p) else {"path": p, "sha256": None, "estado": "NAO_PREPARADO"}
pr = json.load(open(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v394.json"), encoding="utf-8"))
rp = {"path": pr["path"], "sha256": sha(open(pr["path"], "rb").read()), "versao_nos": pr["versao_nos"], "veredito": pr["veredito"], "utilizavel_como_recibo_pre_selo_do_B_n": pr["utilizavel_como_recibo_pre_selo_do_B_n"],
      "pino_do_pino": f(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v394.json")), "motivos": pr.get("motivos_de_nao_ser_utilizavel")}
assert rp["sha256"] == pr["sha256"], "o recibo pre-selo mudou desde o pino"
pn = {"criterios": f(os.path.join(V, "CRITERIOS_v394.json")), "kernel_recibo": f(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v394.json")),
      "candidato": f(os.path.join(HERE, DL.CANDIDATO)), "esperados": f(os.path.join(HERE, "ESPERADOS_v394.json")), "pins_do_candidato": f(os.path.join(HERE, "v394_pins.py")),
      "esboco_R3_3": f(os.path.join(os.path.dirname(HERE), "v392", "vinculo", "sincronizar_bancada.py")), "bateria": f(os.path.join(os.path.dirname(HERE), "v392", "vinculo", "BATERIA_VINCULO.json")),
      "recibo_pre_selo": rp,
      "nota": "[REAL] lido dos arquivos por script; esboco e bateria sao os da v392 (R3.3 / R2); o recibo pre-selo e' o ENSAIO de 19/10 contra a v393 instalada (Bancada pinando a v392): BATERIA_FALHOU (T12/T13 pinam o um.py v391) e versao_alvo != a pinada; "
              "NAO e' utilizavel pelo B(n): ver ESTADO_V394 §6 (decisao do operador/gerencia: esboco R3.4 ou bateria R3). O pos-selo (aplicar) tambem esbarra nas 3 pedras sem declaracao (NetworkProofAuditR3/R7/R8)."}
json.dump(pn, open(os.path.join(HERE, "PINOS_BN_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: (v["sha256"] or "NAO_PREPARADO")[:16] for k, v in pn.items() if isinstance(v, dict)})
