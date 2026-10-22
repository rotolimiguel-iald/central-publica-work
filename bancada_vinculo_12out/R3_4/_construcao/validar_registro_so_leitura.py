# -*- coding: utf-8 -*-
"""validar_registro_so_leitura.py (R3.4, 19/10/2026) -- valida registro_mapa_F0.6_R3_4.json com o _valida do rotas.py do mapa, SO LEITURA: le o livro, nao grava nada, nao chama registrar().
uso: python -I -B -X utf8 validar_registro_so_leitura.py <registro.json>"""
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("rotas_ro", "C:/IALD/MAPA_DE_ROTAS/rotas.py")
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
regs = R._parse(R._ler_bytes(R.LIVRO))
ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}
seqs = {r["seq"] for r in regs}
reg = json.loads(Path(sys.argv[1]).read_bytes())
try:
    r = R._valida(reg, ids, seqs)
    print(json.dumps(dict(valido=True, tipo=r["tipo"], rota_id=r["rota_id"], status=r.get("status"), estatuto=r.get("estatuto"), n_artefatos=len(r.get("artefatos", [])),
                          campos=sorted(r), n_registros_no_livro=len(regs), campos_texto_maiores=sorted(((len(v), k) for k, v in r.items() if isinstance(v, str)), reverse=True)[:3]), ensure_ascii=False))
except Exception as exc:
    print(json.dumps(dict(valido=False, erro=str(exc)), ensure_ascii=False))
    sys.exit(2)
