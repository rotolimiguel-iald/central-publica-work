# -*- coding: utf-8 -*-
"""CONFERÊNCIA do um.acom público (22/10/2026, custódia v396): abre o contêiner com a chave PÚBLICA da casa (o mesmo módulo da Central) e
conta, por membro, identificador de terceiro (lista privada) e dado pessoal sem máscara (os padrões da máscara única). Só contagens e nomes
de membro; nunca o valor achado. Uso: <python do backend> conferir_um_acom_publico.py <um.acom>   (exit 1 se achar algo)"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\IALD\Central de Patentes\backend")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import um_acom as UM          # noqa: E402
from mascara_pii import PII, TERCEIROS, MASK  # noqa: E402

r = UM.open_container(Path(sys.argv[1]).read_bytes(), UM.ONCOLOGIA_KEY)
fs = r["_files"]
terc, pii = [], {}
for nome, b in fs.items():
    t = b.decode("utf-8", "replace") if isinstance(b, (bytes, bytearray)) else str(b)
    if TERCEIROS is not None and TERCEIROS.search(t):
        terc.append(nome)
    for k, rx in PII:
        if any(m.group(0) != MASK for m in rx.finditer(t)):
            pii.setdefault(k, []).append(nome)
print("membros: %d | com identificador de terceiro: %d %s | com padrão de dado pessoal: %s" % (
    len(fs), len(terc), terc[:5], {k: len(v) for k, v in pii.items()}))
for k, v in pii.items():
    print("  %s: %s" % (k, v[:6]))
sys.exit(1 if terc or pii else 0)
