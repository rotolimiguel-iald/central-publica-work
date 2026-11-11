# -*- coding: utf-8 -*-
import json
from pathlib import Path

d = json.loads(Path(r"C:\IALD\Artigo\the_boundary\PRIMORDIAL.json").read_text(encoding="utf-8-sig"))
print("chaves:", list(d.keys())[:15])


def achar(o, ch, caminho=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ch:
                print(caminho + "/" + k, "=", str(v)[:80])
            achar(v, ch, caminho + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o[:50]):
            achar(v, ch, caminho + "[%d]" % i)


achar(d, {"kernel.declaracoes", "kernel.arquivos_formais", "escada.texto", "declaracoes", "arquivos_formais", "escada", "pin16", "selo.versao"})
vals = d.get("valores") or d.get("campos") or {}
for k in ("kernel.declaracoes", "kernel.arquivos_formais", "escada.texto", "escada.limpos", "selo.versao", "selo.pin16", "zenodo.doi", "zenodo.versao"):
    if k in vals:
        print(k, "=>", vals[k] if not isinstance(vals[k], dict) else vals[k].get("valor"))
