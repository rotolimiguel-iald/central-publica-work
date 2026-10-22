# Auditor c1: conserta os campos de caminho dos dois registros (o heredoc anterior gerou \v e \a por barra invertida em string normal).
import json, os
A = os.path.dirname(os.path.abspath(__file__))
V392 = os.path.join(os.path.dirname(A), "v392")
AUD = os.path.join(A, "AUDITORIA_CADEIA_V392_C1.md")
AF1 = os.path.join("C:" + os.sep, "t", "af1")
for nome, onde in (("registro_rota_F0.5.json", V392), ("registro_mapa_F0.5.json", AUD)):
    p = os.path.join(A, nome)
    d = json.load(open(p, encoding="utf-8"))
    d["onde"] = onde
    if "metodo" in d:
        d["metodo"] = d["metodo"].replace("C:\t\u0007f1", AF1)
    s = json.dumps(d, ensure_ascii=False, indent=1)
    assert "\u000b" not in s and "\u0007" not in s and "\\u000b" not in s and "\\u0007" not in s, nome
    open(p + ".tmp", "w", encoding="utf-8").write(s); os.replace(p + ".tmp", p)
    print(nome, d["onde"], AF1 in d.get("metodo", "") or "-")
