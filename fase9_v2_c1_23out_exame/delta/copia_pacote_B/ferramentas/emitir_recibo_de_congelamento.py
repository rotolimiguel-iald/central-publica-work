# -*- coding: utf-8 -*-
"""emitir_recibo_de_congelamento.py -- ATO DA GERENCIA (NAO foi executado nesta preparacao).
Calcula os pinos do pacote REAL (spec, funcao, registro D-H, modulos do runner, fontes, recibo de calibracao, arquivos da Bancada) e grava
freeze/RECIBO_DE_CONGELAMENTO.json. Recusa sobrescrever. Sem --escrever, so mostra o recibo (ensaio).
Uso (so depois da auditoria c1 do runner e da conferencia do PEDIDO_DE_CONGELAMENTO.json):
  python -B -P -E -X utf8 ferramentas/emitir_recibo_de_congelamento.py --root <pacote> --emitido-por "gerencia c1 ..." --auditoria-ref "<relatorio da auditoria c1>" --confirmo-auditoria --escrever"""
import argparse
import json
import os
import sys

sys.dont_write_bytecode = True   # B6: nunca gravar .pyc em runner/

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "runner"))
import f9v2_background as BG  # noqa: E402
import f9v2_freeze as FRZ  # noqa: E402
import f9v2_verdict as VER  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--emitido-por", required=True)
    ap.add_argument("--auditoria-ref", required=True)
    ap.add_argument("--confirmo-auditoria", action="store_true", help="a gerencia confirma que a auditoria c1 do runner passou")
    ap.add_argument("--escrever", action="store_true")
    a = ap.parse_args()
    if not a.confirmo_auditoria:
        sys.exit("RECUSA: sem --confirmo-auditoria (auditoria c1 do runner) nao ha recibo")
    root = os.path.abspath(a.root)
    rec = FRZ.make_freeze_receipt(root, "REAL", a.emitido_por, a.auditoria_ref, VER.TOKEN_BASE, bancada_pins=BG.bancada_pins())
    b = json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    dest = os.path.join(root, *FRZ.FREEZE_REL.split("/"))
    if not a.escrever:
        print(b.decode("utf-8"))
        print("ENSAIO: nada foi gravado", file=sys.stderr)
        return 0
    if os.path.exists(dest):
        sys.exit("RECUSA: ja existe " + dest)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest + ".tmp", "wb").write(b)
    assert os.path.getsize(dest + ".tmp") == len(b)
    os.replace(dest + ".tmp", dest)
    print("RECIBO_DE_CONGELAMENTO gravado:", dest, FRZ.sha256_bytes(b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
