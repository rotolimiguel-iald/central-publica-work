# -*- coding: utf-8 -*-
"""Os dois construtores passam a gravar, FORA do preparo publicado, a lista completa do que excluíram e por quê
(work/central_publica_22out/varredura_exclusoes_<preparo>.json — o prefixo «varredura_» o mantém fora do repositório público do work),
para auditar as exclusões sem reconstruir (22/10/2026). Backup de BYTES; troca conferida por contagem; idempotente."""
import os, re, time
from pathlib import Path

W = Path(__file__).resolve().parent
TS = time.strftime("%Y%m%d_%H%M%S")


def patch(nome, var, fim_ancora, fim_extra):
    p = W / nome
    raw = p.read_bytes()
    s = raw.decode("utf-8")
    if "LOCAL_EXCL" in s:
        print("já aplicado:", nome); return
    n0 = len(re.findall(r'fora\["[^"]+"\] \+= 1;', s))
    s = re.sub(r'fora\[("[^"]+")\] \+= 1;', lambda m: "fora_(%s, %s);" % (m.group(1), var), s)
    s = s.replace("fora[m] += 1; fora_lista.setdefault(m, []).append(t); continue",
                  "fora_(m, t); fora_lista.setdefault(m, []).append(t); continue")
    helper = ("LOCAL_EXCL = {}\n\n\ndef fora_(m, x):\n    fora[m] += 1\n    LOCAL_EXCL.setdefault(m, []).append(x)\n\n\n")
    assert s.count(fim_ancora) == 1, (nome, "âncora")
    s = s.replace(fim_ancora, helper + fim_ancora, 1)
    s = s.rstrip("\n") + "\n" + fim_extra
    compile(s, nome, "exec")
    p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    t = p.with_name(p.name + ".tmp_excl")
    t.write_bytes(s.encode("utf-8"))
    os.replace(t, p)
    print("ok", nome, "| trocas:", n0)


patch("construir_nucleo_publico.py", "t", "def motivo(t):",
      '(W / ("varredura_exclusoes_%s.json" % DST.name)).write_text(json.dumps(LOCAL_EXCL, ensure_ascii=False, indent=0), encoding="utf-8")\n')
patch("construir_regiao_publica.py", "rel", "def lp(x):",
      '(W / ("varredura_exclusoes_%s.json" % DST.name)).write_text(json.dumps(LOCAL_EXCL, ensure_ascii=False, indent=0), encoding="utf-8")\n')
