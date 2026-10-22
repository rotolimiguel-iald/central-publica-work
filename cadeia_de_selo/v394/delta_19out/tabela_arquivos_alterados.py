# -*- coding: utf-8 -*-
"""tabela_arquivos_alterados.py -- DELTA 19/10: lista, por script, os arquivos da raiz de cadeia_de_selo\\v394 (e vinculo\\) ALTERADOS pelo delta (sha16 ANTES, lido do backup de bytes mais antigo feito a partir de 13:00 de 19/10; sha16 DEPOIS, lido do arquivo)
e os arquivos NOVOS (sem backup anterior). Gera os diffs unificados dos textos em delta_19out\\diffs\\ e escreve ARQUIVOS_ALTERADOS_DELTA_19OUT.json/.md. Nada digitado. So' escreve em delta_19out.
uso: python -I -B -X utf8 tabela_arquivos_alterados.py"""
import difflib, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
RXB = re.compile(r"^(?P<base>.+)\.bak_(?P<ts>\d{8}_\d{6})_c1(?:blk|d19|d19b|d19c)?$")
DIFFD = os.path.join(HERE, "diffs"); os.makedirs(DIFFD, exist_ok=True)
CORTE = "20261019_130000"
pastas = [(V, ""), (os.path.join(V, "vinculo"), "vinculo/"), (os.path.join(V, "kernel"), "kernel/"), (os.path.join(V, "pos_rito"), "pos_rito/")]
CRIADOS_PELO_DELTA = ("delta19_v394.py", "um_v394_candidato_d19.py")   # nascem no delta: o backup deles e' um estado INTERMEDIARIO do proprio delta, nao um «antes»
alt, novos = [], []
vistos = set()
for pasta, pref in pastas:
    nomes = os.listdir(pasta)
    baks = {}
    for n in nomes:
        m = RXB.match(n)
        if m and m.group("ts") >= CORTE:
            baks.setdefault(m.group("base"), []).append((m.group("ts"), n))
    for base, lst in sorted(baks.items()):
        lst.sort(); antigo = os.path.join(pasta, lst[0][1]); atual = os.path.join(pasta, base)
        if not os.path.isfile(atual) or (pref + base) in CRIADOS_PELO_DELTA:
            continue
        ba, bb = open(antigo, "rb").read(), open(atual, "rb").read()
        vistos.add(pref + base)
        e = {"arquivo": pref + base, "sha16_antes": sha16(ba), "sha16_depois": sha16(bb), "bytes_antes": len(ba), "bytes_depois": len(bb), "backup": lst[0][1], "mudou": ba != bb}
        if e["mudou"]:
            alt.append(e)
            if base.endswith((".py", ".sh", ".txt", ".pysnip", ".md")) or base.endswith(".json") and len(ba) + len(bb) < 400000:
                try:
                    ta, tb = ba.decode("utf-8").splitlines(), bb.decode("utf-8").splitlines()
                    d = list(difflib.unified_diff(ta, tb, "ANTES/" + base, "DEPOIS/" + base, lineterm="", n=2))
                    open(os.path.join(DIFFD, base.replace("/", "_") + ".diff"), "w", encoding="utf-8", newline="\n").write("\n".join(d) + "\n")
                    e["diff"] = "diffs/" + base + ".diff"; e["linhas_diff"] = len(d)
                except UnicodeDecodeError:
                    pass
# novos: arquivos da raiz de V sem backup de hoje e criados a partir do corte (mtime)
import time
corte_t = time.mktime(time.strptime(CORTE, "%Y%m%d_%H%M%S"))
COPIAS_DO_EXAME = ("simular_arvore_do_nos.py", "exame_pontos_v394.py")   # copias de BYTES dos scripts do exame (cp -p preserva o mtime antigo)
for n in sorted(os.listdir(V)):
    p = os.path.join(V, n)
    if os.path.isfile(p) and n not in vistos and not RXB.match(n) and (os.path.getmtime(p) >= corte_t or n in COPIAS_DO_EXAME or n in CRIADOS_PELO_DELTA):
        novos.append({"arquivo": n, "sha16": sha16(open(p, "rb").read()), "bytes": os.path.getsize(p)})
pastas_novas = [n for n in sorted(os.listdir(V)) if os.path.isdir(os.path.join(V, n)) and os.path.getmtime(os.path.join(V, n)) >= corte_t]
R = {"alterados": alt, "novos_na_raiz": novos, "pastas_tocadas_ou_novas": pastas_novas, "n_alterados": len(alt), "n_novos": len(novos)}
json.dump(R, open(os.path.join(HERE, "ARQUIVOS_ALTERADOS_DELTA_19OUT.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L = ["| arquivo | sha16 antes | sha16 depois | bytes antes -> depois |", "|---|---|---|---|"]
for e in alt:
    L.append("| `%s` | `%s` | `%s` | %d -> %d |" % (e["arquivo"], e["sha16_antes"], e["sha16_depois"], e["bytes_antes"], e["bytes_depois"]))
L += ["", "NOVOS na raiz:", "", "| arquivo | sha16 | bytes |", "|---|---|---|"] + ["| `%s` | `%s` | %d |" % (e["arquivo"], e["sha16"], e["bytes"]) for e in novos]
L += ["", "Pastas novas ou tocadas (por mtime): " + ", ".join("`%s`" % p for p in pastas_novas) + ". `pos_rito` aparece porque OUTRO agente escreveu nela (antes das 13:00) e porque, na rodada final, a gerencia AUTORIZOU a aplicacao da proposta em `pos_rito\\textos_v394.py` (a unica escrita minha ali, com backup de bytes `.bak_<STAMP>_c1d19c`)."]
open(os.path.join(HERE, "ARQUIVOS_ALTERADOS_DELTA_19OUT.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("\n".join(L))
