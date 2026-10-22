# -*- coding: utf-8 -*-
"""corrige os dois campos do registro_mapa_F0.6_R3_2.json em que as barras invertidas foram perdidas na geracao (onde, dados[1])."""
import json
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "registro_mapa_F0.6_R3_2.json"
r = json.loads(P.read_bytes())
r["onde"] = str(P.parent)
r["dados"][1] = "sandbox " + str(Path("C:/t/vb7")) + " (raiz curta; 5 juncoes desfeitas com os.rmdir no link; apagado)"
for k, v in r.items():
    for s in (v if isinstance(v, list) else [v]):
        assert not (isinstance(s, str) and any(c in s for c in "\b\t\x07\x0c")), (k, s)
P.write_bytes(json.dumps(r, ensure_ascii=False, indent=1).encode("utf-8"))
print(r["onde"], "|", r["dados"][1])
