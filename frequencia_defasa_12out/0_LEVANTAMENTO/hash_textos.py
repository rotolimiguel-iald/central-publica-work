# -*- coding: utf-8 -*-
# Confere por script (sha256 dos bytes) os textos do operador citados na unidade F1.FREQUENCIA.
import hashlib, json, sys, os
AQUI = os.path.dirname(os.path.abspath(__file__))
B = "C:\\IALD\\Central de Patentes\\work\\"
ESPERADO = {
    "V1": (B + "cunhagens_12out\\OPERADOR_10out_posto_rank_texto_verbatim.txt", "8d252f24e2806ff3", 2937),
    "V2": (B + "cunhagens_12out\\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt", "2c8b7b712aa9ad7f", None),
    "V3": (B + "cunhagens_10out\\OPERADOR_10out_posto_rank_verbatim.txt", "5b9afcc691a0e1e4", None),
    "V4": (B + "cunhagens_10out\\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt", "b365591ceb346cdf", None),
}
out = {}
ok = True
for k, (p, sha16, nb) in ESPERADO.items():
    with open(p, "rb") as fh:
        b = fh.read()
    h = hashlib.sha256(b).hexdigest()
    c1 = h[:16] == sha16
    c2 = (nb is None) or (len(b) == nb)
    ok = ok and c1 and c2
    out[k] = {"path": p, "bytes": len(b), "sha256": h, "sha16": h[:16], "sha16_esperado": sha16,
              "confere_sha16": c1, "confere_bytes": c2,
              "crlf": b.count(b"\r\n"), "bom": b.startswith(b"\xef\xbb\xbf")}
out["_todos_conferem"] = ok
with open(os.path.join(AQUI, "HASHES_TEXTOS_OPERADOR.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
if not ok:
    sys.exit(2)
