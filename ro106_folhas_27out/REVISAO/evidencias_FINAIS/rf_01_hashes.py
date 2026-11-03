# -*- coding: utf-8 -*-
# Revisor sonnet-ro106-revisor-final, 02/11/2026. Somente leitura. Hashes sha256 (sha16 = 16 primeiros hex) lidos por script.
import hashlib, json, sys, pathlib

K = pathlib.Path("C:/IALD/Central de Patentes/work/ro106_folhas_27out")
OUT = K / "REVISAO" / "evidencias_FINAIS" / "rf_01_hashes.json"

# sha16 esperados (fonte: ESTADO.json e REVISAO_RO106_050576_R3.md / 050579_R2.md; "aceitas" nao mudam)
ESPERADO = {
    "CARTA_REGRA_26_4_050576.md": "dbe1caff15ed32e4",
    "CARTA_REGRA_26_4_050576.pdf": "a72a89c3571cb828",
    "CARTA_REGRA_26_4_050579.md": "29029f0a6e2b0c4c",
    "CARTA_REGRA_26_4_050579.pdf": "2378f978494f2fdf",
    "FOLHAS_SUBSTITUTIVAS_050576.pdf": "884d978a39b20d1a",
    "FOLHAS_SUBSTITUTIVAS_050579.pdf": "4faa43ca81442fc5",
    "CONFERENCIA_050576.json": "d171e2bc9be9668e",
    "CONFERENCIA_050579.json": "529ca8412ad6baa1",
}
ARQ = list(ESPERADO) + [
    "CARTA_REGRA_26_4_050576_FINAL.md",
    "CARTA_REGRA_26_4_050576_FINAL.pdf",
    "CARTA_REGRA_26_4_050579_FINAL.md",
    "CARTA_REGRA_26_4_050579_FINAL.pdf",
    "fontes/carta_final.py",
    "fontes/carta.py",
    "REVISAO/REVISAO_RO106_050576_R3.md",
    "REVISAO/REVISAO_RO106_050579_R2.md",
    "entrada/aprendizado/04_DESENHOS_como_depositado.pdf",
    "entrada/mqc/04_DESENHOS_CINZA_como_depositado.pdf",
]
res = {}
for a in ARQ:
    p = K / a
    b = p.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    esp = ESPERADO.get(a)
    res[a] = {"bytes": len(b), "sha256": h, "sha16": h[:16],
              "esperado_sha16": esp,
              "confere": (None if esp is None else h[:16] == esp)}
    print(f"{a:62s} {len(b):8d} {h[:16]} " + ("" if esp is None else ("OK" if h[:16] == esp else "DIVERGE esperado " + esp)))
OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
