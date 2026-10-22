# -*- coding: utf-8 -*-
"""SÓ LEITURA, saída local (sem nomes de pessoas: só caminho do arquivo e contagem): o que, nos três preparos públicos, toca o acervo do
ESCRITÓRIO (PJ separada; regra das casas) — caminhos C:\\Escritorio, audiências, processos judiciais, varas, PJe, OAB, clientes — e
inventários de disco que listem pastas fora da IALD. Grava a lista em varredura_escritorio.json."""
import json, os, re, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(r"C:\IALD\Central_publica")
PAD = {"caminho_escritorio": re.compile(r"(?i)[A-Z]:[\\/]+Escrit[oó]rio|\\\\Escrit[oó]rio\\\\|/Escrit[oó]rio/"),
       "audiencia": re.compile(r"(?i)audi[eê]ncias?\s+realizad|audi[eê]ncia\s+(de\s+)?(instru|concilia|una)"),
       "processo_judicial": re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b"),
       "vara_tribunal": re.compile(r"(?i)\b(\d+ª?\s*vara\s+(c[ií]vel|criminal|do trabalho|federal|de fam)|TJGO|TRT\s?18|juizado especial)\b"),
       "pje": re.compile(r"(?i)\bPJe\b|pjedocs|projudi"),
       "escritorio_nome": re.compile(r"(?i)miguel advogados|rmiguel\.adv"),
       "cliente_parte": re.compile(r"(?i)\b(reclamante|reclamad[oa]|requerente|requerid[oa]|exequente|executad[oa]|r[ée]u|autor[a]?)\s*:")}
TXT = {".py", ".md", ".json", ".jsonl", ".txt", ".tex", ".csv", ".yaml", ".yml", ".html", ".js", ".ts", ".log", ".out", ".xml", ".lean"}
res = {}
for preparo in ("central-publica", "central-publica-work", "central-publica-bancada"):
    base = RAIZ / preparo
    cont = Counter(); arqs = defaultdict(list)
    for dp, dns, fns in os.walk(base):
        dns[:] = [d for d in dns if d != ".git"]
        for f in fns:
            p = Path(dp) / f
            rel = p.relative_to(base).as_posix()
            nomes = [k for k, rx in PAD.items() if k in ("caminho_escritorio", "audiencia", "escritorio_nome") and rx.search(rel)]
            if p.suffix.lower() in TXT:
                try:
                    t = open("\\\\?\\" + str(p), "rb").read().decode("utf-8", "replace")
                except OSError:
                    continue
                for k, rx in PAD.items():
                    n = len(rx.findall(t))
                    if n:
                        cont[k] += n
                        arqs[k].append((rel, n))
            for k in nomes:
                arqs["nome_do_arquivo:" + k].append((rel, 1))
    res[preparo] = {k: sorted(v, key=lambda x: -x[1]) for k, v in arqs.items()}
    print("==", preparo, dict(cont))
    for k, v in res[preparo].items():
        print("   %-28s %5d arquivos | ex.: %s" % (k, len(v), [x[0][-90:] for x in sorted(v, key=lambda x: -x[1])[:3]]))
Path(__file__).with_name("varredura_escritorio.json").write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding="utf-8")
