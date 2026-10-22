# -*- coding: utf-8 -*-
"""Aplica a regra do ACERVO DO ESCRITÓRIO (guarda_publica.toca_escritorio) aos preparos já construídos e à pasta central/ do site:
lista os arquivos de texto que trazem caminho para dentro do acervo, audiência realizada ou número de processo CNJ e grava a lista
(varredura_escritorio_<preparo>.txt, local). Com --tirar, remove-os do preparo (excluir_do_preparo.py). Nunca imprime o trecho achado.
Uso: aplicar_regra_escritorio.py [--tirar]"""
import json, os, subprocess, sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
import guarda_publica as GP  # noqa: E402

TIRAR = "--tirar" in sys.argv
ALVOS = [Path(r"C:\IALD\Central_publica\central-publica"), Path(r"C:\IALD\Central_publica\central-publica-work"),
         Path(r"C:\IALD\Central_publica\central-publica-bancada"), Path(r"C:\IALD\Site\tgl\v3.0\central")]
TXT = {".py", ".md", ".json", ".jsonl", ".txt", ".tex", ".csv", ".tsv", ".yaml", ".yml", ".html", ".js", ".ts", ".tsx", ".log", ".out",
       ".xml", ".lean", ".ipynb", ".toml", ".ini", ".cfg", ".sh", ".ps1", ".bat", ".bin", ".diff", ".patch", ".dat", ".svg", ".css", ".sql"}
for D in ALVOS:
    achados = []
    for dp, dns, fns in os.walk(D):
        dns[:] = [d for d in dns if d != ".git"]
        for f in fns:
            p = Path(dp) / f
            if p.suffix.lower() not in TXT and p.suffix:
                continue
            try:
                t = open("\\\\?\\" + str(p), "rb").read().decode("utf-8", "replace")
            except OSError:
                continue
            if GP.toca_escritorio(t) or GP.toca_escritorio(p.relative_to(D).as_posix()):
                achados.append(p.relative_to(D).as_posix())
    lista = W / ("varredura_escritorio_%s.txt" % D.name)
    lista.write_text("\n".join(achados) + ("\n" if achados else ""), encoding="utf-8")
    por_topo = Counter("/".join(a.split("/")[:2]) for a in achados)
    print("%s: %d arquivos tocam o acervo do Escritório | %s" % (D.name, len(achados), por_topo.most_common(8)), flush=True)
    if TIRAR and achados and (D / "INDICE_PUBLICO.json").is_file():
        r = subprocess.run([sys.executable, "-X", "utf8", str(W / "excluir_do_preparo.py"), str(D),
                            "toca o acervo do Escritório (PJ separada: caminhos internos, audiências, processos)", str(lista)],
                           capture_output=True, text=True, encoding="utf-8")
        print("   ", (r.stdout or r.stderr).strip()[-400:], flush=True)
