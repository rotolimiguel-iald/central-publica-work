"""Valida (SOMENTE LEITURA) o registro_mapa_rito9_poder_realista.json com o validador do proprio rotas.py.

NAO grava nada no mapa: chama apenas rotas._parse/_ler_bytes (leitura do livro) e rotas._valida (funcao pura).
Uso: python validar_registro_mapa.py <registro.json>
"""
import json
import sys

sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS")
import rotas  # noqa: E402

reg = json.load(open(sys.argv[1], encoding="utf-8"))
regs = rotas._parse(rotas._ler_bytes(rotas.LIVRO))
ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}
seqs = {r["seq"] for r in regs}
r = rotas._valida(reg, ids, seqs)
print("VALIDO. campos:", sorted(r.keys()))
print("artefatos (sha256 calculado pela ferramenta):")
for a in r["artefatos"]:
    print("  ", a["caminho"] if isinstance(a, dict) else a, (a.get("sha256", "")[:16] if isinstance(a, dict) else ""))
print("livro intacto: n_registros =", len(regs))
