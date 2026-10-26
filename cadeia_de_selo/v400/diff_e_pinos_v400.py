# -*- coding: utf-8 -*-
"""diff_e_pinos_v400.py -- (1) DIFF_KERNEL_v400.txt: o kernel embutido do candidato contra o da v399 selada (VAZIO: nenhum arquivo novo, removido ou mudado) e, do ponto de vista da Bancada de producao (que AINDA pina a v398), contra o da v398
(a pedra Testemunho + a raiz + o Audit: o que o recibo do kernel do B(n) lista); (2) PINOS_BN_v400.json: os sha256 que o elo B(n) pede (esboco R3.5, gerador e driver da bateria, base R2, CRITERIOS, recibo do kernel, recibo pre_selo [o da cadeia v399,
reconferido pelo esboco], selo e manifesto do kernel da v398, que a Bancada pina), LIDOS dos arquivos por script (path e sha256 recalculados aqui; nada digitado). O B(n) da v400 e' um PASSO SIMPLES v398 -> v400: nao ha pino de cadeia de selos.
Molde: diff_e_pinos_v399.py. Uso: python -I -B -X utf8 diff_e_pinos_v400.py   (roda DEPOIS de gerar_esperados_v400.py: o pino do ESPERADOS e' o do arquivo final)"""
import ast, difflib, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v400 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
BASE = os.path.join(HERE, DL.BASE_DIR)
E0, _, _, h0 = carregar(os.path.join(BASE, "um.py")); E1, _, _, h1 = carregar(os.path.join(HERE, DL.CANDIDATO)); E8, _, _, h8 = carregar(os.path.join(DL.V399_BASE98, "um.py"))


def diff(Ea, Eb, ha, hb, va, vb):
    novos = sorted(set(Eb) - set(Ea)); removidos = sorted(set(Ea) - set(Eb)); mudados = sorted(k for k in set(Ea) & set(Eb) if Ea[k] != Eb[k])
    out = ["DIFF DO KERNEL EMBUTIDO %s (%s) -> %s (%s)" % (va, ha, vb, hb), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, sha(Eb[k].encode())[:16], len(Eb[k].encode())) for k in novos]
    out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
    for k in mudados:
        a, b = Ea[k].splitlines(), Eb[k].splitlines(); d = list(difflib.unified_diff(a, b, va + "/" + k, vb + "/" + k, lineterm="", n=0))
        out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, sha(Ea[k].encode())[:16], sha(Eb[k].encode())[:16], sum(1 for l in d if l.startswith("+") and not l.startswith("+++")), sum(1 for l in d if l.startswith("-") and not l.startswith("---"))))
        out += ["      " + l[:200] for l in d[:40]]
    return novos, removidos, mudados, out


n9, r9, m9, out9 = diff(E0, E1, h0, h1, "v399", "v400")
n8, r8, m8, out8 = diff(E8, E1, h8, h1, "v398", "v400")
open(os.path.join(HERE, "DIFF_KERNEL_v400.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out9) + "\n\n" + "=" * 100 + "\nO MESMO DIFF DO PONTO DE VISTA DA BANCADA (que AINDA pina a v398): o que o recibo do kernel do B(n) lista\n" + "=" * 100 + "\n\n" + "\n".join(out8) + "\n")
print("v399 -> v400: novos", len(n9), "removidos", len(r9), "mudados", len(m9), "| v398 -> v400: novos", n8, "removidos", len(r8), "mudados", m8)
assert not n9 and not r9 and not m9 and DL.STONE_RELS == [], ("a v400 NAO acrescenta modulo nem muda arquivo do kernel: o diff v399 -> v400 tem de ser VAZIO", n9, r9, m9)
assert n8 == sorted(DL.STONE_RELS_DESDE_B8) and not r8 and sorted(m8) == ["TGL/Audit.lean", "TGLExt.lean"], ("o diff v398 -> v400 nao e' so' a pedra Testemunho + raiz + Audit", n8, r8, m8)
V = os.path.join(HERE, "vinculo")
f = lambda p, **kw: dict({"path": p, "sha256": sha(open(p, "rb").read()), "bytes": os.path.getsize(p)}, **kw) if os.path.exists(p) else {"path": p, "sha256": None, "estado": "NAO_PREPARADO"}
pr = json.load(open(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v400.json"), encoding="utf-8"))
assert sha(open(pr["path"], "rb").read()) == pr["sha256"], "o recibo pre-selo mudou desde o pino"
rp = {"path": pr["path"], "sha256": pr["sha256"], "versao_nos": pr["versao_nos"], "veredito": pr["veredito"], "utilizavel_como_recibo_pre_selo_do_B_n": pr["utilizavel_como_recibo_pre_selo_do_B_n"], "pino_do_pino": f(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v400.json")),
      "um_py_sha16_do_nos": pr["um_py_sha16_do_nos"], "bancada_pina": pr["bancada_pina"], "sem_salto": True, "origem": "recibo da CADEIA v399 (gerado e pinado antes da instalacao da v399), reconferido pelo esboco R3.5 na v400"}
P9 = json.load(open(os.path.join(DL.V399, "PINOS_BN_v399.json"), encoding="utf-8"))   # a fusao R3.4/R3.5: o esboco, o gerador e o driver da bateria, a base R2 (so' leitura; o sha e' RECALCULADO do arquivo)


def da_v399(k):
    d = P9[k]; assert os.path.exists(d["path"]) and sha(open(d["path"], "rb").read()) == d["sha256"], ("o pino herdado da v399 diverge do arquivo", k)
    return f(d["path"], origem="PINOS_BN_v399.json[%s] (recalculado do arquivo)" % k)


kr = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v400.json"), encoding="utf-8"))
B98 = os.path.join(HERE, DL.BASE98_DIR)
pn = {"criterios": f(os.path.join(V, "CRITERIOS_v400.json")), "kernel_recibo": f(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v400.json"), contrato=kr["contrato"], n_pedras=len(kr["pedras"]), modulos_de_auditoria=kr.get("modulos_de_auditoria", [])),
      "candidato": f(os.path.join(HERE, DL.CANDIDATO)), "esperados": f(os.path.join(HERE, "ESPERADOS_v400.json")), "pins_do_candidato": f(os.path.join(HERE, "v400_pins.py")),
      "esboco_R3_5": da_v399("esboco_R3_5"), "gerador_bateria": da_v399("gerador_bateria"), "driver_t12_t14": da_v399("driver_t12_t14"), "bateria_base_R2": da_v399("bateria_base_R2"),
      "bateria_do_pre_selo": f(pr["bateria"]["path"], versao="v398", nota="a bateria do ensaio pre_selo (a da v398); a do POS_SELO da v400 e' GERADA pelo chain depois do selo"),
      "recibo_pre_selo": rp,
      "selo_anterior_v398": f(os.path.join(B98, "um_absoluto_selo.json"), nota="o selo da v398 (custodia; a Bancada de producao AINDA o pina): --selo-anterior"),
      "kernel_manifesto_anterior_v398": f(os.path.join(B98, "tgl_kernel_proof_manifest.json"), nota="o manifesto do kernel da v398 (custodia): --kernel-manifesto-anterior"),
      "nota": "[REAL] lido dos arquivos por script (diff_e_pinos_v400.py): path e sha256 RECALCULADOS; PASSO SIMPLES v398 -> v400 (a Bancada de producao pina a v398; a v399 foi recusada pelo esboco e nunca e' sincronizada): sem pino de cadeia de selos nem 3o argumento do b3_recibo; "
              "o recibo pre_selo e' o da cadeia v399 (sobre o um.py v398), reconferido; o recibo do kernel lista o diff v398 -> v400 (a pedra Testemunho); o esboco R3.5 e a bateria/driver sao os da cadeia anterior (R3_5), reaproveitados; "
              "os vereditos esperados do passo simples (REPINADA_B9__...) estao no ESTADO_V400.md [lidos do codigo do esboco, nao rodados]."}
bad = [k for k, v in pn.items() if isinstance(v, dict) and "path" in v and v.get("sha256") is None]
assert not bad, ("pino sem arquivo", bad)
json.dump(pn, open(os.path.join(HERE, "PINOS_BN_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: (v["sha256"] or "NAO_PREPARADO")[:16] for k, v in pn.items() if isinstance(v, dict) and "sha256" in v})
