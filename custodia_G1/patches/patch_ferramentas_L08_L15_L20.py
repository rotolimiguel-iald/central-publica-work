# -*- coding: utf-8 -*-
"""Três remendos CONTADOS em ferramentas existentes (NÃO APLICADOS; escritos em 24/10/2026 por G1). Cada troca exige `count == 1`, faz backup de BYTES
(`<arquivo>.bak_G1_<TS>`), respeita CRLF/LF e passa por `py_compile` no temporário. Sem --aplicar só CONFERE as âncoras.

  L08  the_boundary\\tools\\verificar_portas.py: não tem código de saída (a falha só aparece em «ERROS … N» e «VEREDITO: FALHOU»). Acrescenta
       `sys.exit(1 if erros else 0)` depois do veredito. (G1 já lê a saída; o código de saída serve a quem chama de fora.)
  L15  Central de Patentes\\tools\\estado_do_organismo.py l.107: `(v3\\d\\d) SELADA` quebra na v400 -> `(v\\d{3,}) SELADA`.
  L20  o mesmo arquivo l.119-120: o medidor procura o backup `um_v{N-1}_*` e dá DEFASADO falso numa custódia CONJUNTA (v393+v394). Passa a aceitar
       qualquer `um_v{K}_*` com K < N (o maior), que é o que o passo zero de G1 produz.
ATENÇÃO: o verificar_portas.py é arquivo do ESPELHO (tracked): remendá-lo suja a árvore e exige commit próprio; o estado_do_organismo.py é da Central.
Uso:  python patch_ferramentas_L08_L15_L20.py [--aplicar]"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

VP = Path(r"C:\IALD\Artigo\the_boundary\tools\verificar_portas.py")
EO = Path(r"C:\IALD\Central de Patentes\tools\estado_do_organismo.py")
TS = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")

TROCAS = {
    VP: [('print("VEREDITO: %s" % ("TODAS AS PORTAS RESOLVEM" if not erros else "FALHOU"))\n',
          'print("VEREDITO: %s" % ("TODAS AS PORTAS RESOLVEM" if not erros else "FALHOU"))\nimport sys as _sys\n_sys.exit(1 if erros else 0)   # L08: código de saída (G1, 24/10/2026)\n')],
    EO: [('vs = re.findall(r"^## [^\\n]*\\*\\*(v3\\d\\d) SELADA", diario, re.M)\n', 'vs = re.findall(r"^## [^\\n]*\\*\\*(v\\d{3,}) SELADA", diario, re.M)   # L15: v\\d{3,} (G1, 24/10/2026)\n'),
         ('    bks = sorted(BK.glob("um_v%d_*" % (N - 1)))\n',
          '    bks = sorted((b for b in BK.glob("um_v*_*") if re.fullmatch(r"um_v(\\d{3,})_[0-9a-f]{16}", b.name) and int(b.name.split("_")[1][1:]) < N), key=lambda b: int(b.name.split("_")[1][1:]))[-1:]   # L20: P pode não ser N-1 (G1)\n')],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    ok = True
    novos = {}
    for p, pares in TROCAS.items():
        raw = p.read_bytes()
        s = raw.decode("utf-8")
        crlf = b"\r\n" in raw
        for velho, novo in pares:
            if crlf:
                velho, novo = velho.replace("\n", "\r\n"), novo.replace("\n", "\r\n")
            n = s.count(velho)
            print("%-28s âncora ×%d: %r" % (p.name, n, velho[:70]))
            if n != 1:
                ok = False
            else:
                s = s.replace(velho, novo)
        novos[p] = (raw, s.encode("utf-8"))
    if not ok:
        print("RECUSADO: alguma âncora não casou exatamente uma vez (o arquivo mudou?)")
        return 20
    if not a.aplicar:
        print("(conferência apenas: nada foi gravado)")
        return 0
    for p, (raw, dados) in novos.items():
        tmp = p.with_name(p.name + ".tmp_G1")
        tmp.write_bytes(dados)
        r = subprocess.run([sys.executable, "-m", "py_compile", str(tmp)], capture_output=True, text=True)
        if r.returncode != 0:
            tmp.unlink()
            print("SINTAXE INVÁLIDA em", p.name, r.stderr[-300:])
            return 20
        p.with_name("%s.bak_G1_%s" % (p.name, TS)).write_bytes(raw)
        os.replace(tmp, p)
        print("aplicado:", p.name, len(raw), "->", len(dados))
    return 0


if __name__ == "__main__":
    sys.exit(main())
