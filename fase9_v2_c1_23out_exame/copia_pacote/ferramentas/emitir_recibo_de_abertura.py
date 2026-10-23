# -*- coding: utf-8 -*-
"""emitir_recibo_de_abertura.py -- ATO PROPRIO (F3.3: a palavra «abrir» so depois de congelar e auditar). NAO foi executado nesta preparacao.
Grava freeze/RECIBO_DE_ABERTURA.json referido ao sha256 do RECIBO_DE_CONGELAMENTO existente. Recusa sobrescrever.
Uso: python -P -E -X utf8 ferramentas/emitir_recibo_de_abertura.py --root <pacote> --quem "<quem ordena abrir>" --texto "<o ato, verbatim>" --escrever"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "runner"))
import f9v2_freeze as FRZ  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--quem", required=True)
    ap.add_argument("--texto", required=True)
    ap.add_argument("--escrever", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    fpath = os.path.join(root, *FRZ.FREEZE_REL.split("/"))
    if not os.path.isfile(fpath):
        sys.exit("RECUSA: nao ha RECIBO_DE_CONGELAMENTO")
    rec = FRZ.make_open_receipt(open(fpath, "rb").read(), {"quem": a.quem, "texto": a.texto})
    b = json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    dest = os.path.join(root, *FRZ.OPEN_REL.split("/"))
    if not a.escrever:
        print(b.decode("utf-8"))
        print("ENSAIO: nada foi gravado", file=sys.stderr)
        return 0
    if os.path.exists(dest):
        sys.exit("RECUSA: ja existe " + dest)
    open(dest + ".tmp", "wb").write(b)
    assert os.path.getsize(dest + ".tmp") == len(b)
    os.replace(dest + ".tmp", dest)
    print("RECIBO_DE_ABERTURA gravado:", dest, FRZ.sha256_bytes(b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
