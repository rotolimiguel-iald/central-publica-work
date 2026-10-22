# -*- coding: utf-8 -*-
"""Conferencia (somente leitura) do FREEZE do pre-registro F1.FREQUENCIA (trilha POSTO) e dos pinos.
Calcula sha256 dos BYTES por script; nada e escrito fora de 3_KERNEL\rodada2 (copia do script da rodada 1, so com a pasta de saida trocada). Sai com codigo 2 na primeira divergencia."""
import hashlib, json, os, sys

PRE = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out\1_PREREGISTRO"
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # rodada2 (saida na raiz da rodada)

# valores da ordem (copiados do texto da tarefa; conferidos contra os bytes)
ORDEM = {
    "PREREGISTRO.json": (46753, "0c20d7c196a4c7efa75b6eae86fe233c5b12735f1e958f396b3b33a8634df813"),
    "PREREGISTRO.md": (27071, "3c80ea21057c337153f5cf135b3f99677f6b85916677924b47d811bef71ae066"),
}
NOS = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s"
PINOS_ORDEM = [
    (NOS + "\\um.py", 33910631, "8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6"),
    (NOS + "\\um_absoluto.json", 5003275, "a74241ff380b1b0e3d44a8f2c39e7ad4d462624b145353f3e4d82f3131036e98"),
    (NOS + "\\um_absoluto_selo.json", 113926, "95061f18c7102248ebd00c9414f1ef0dadcf08cefc1bec00bf046d778b38070a"),
]
TEXTOS = {
    "V1": (r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_10out_posto_rank_texto_verbatim.txt", "8d252f24e2806ff3"),
    "V2": (r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt", "2c8b7b712aa9ad7f"),
    "V3": (r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt", "5b9afcc691a0e1e4"),
    "V4": (r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt", "b365591ceb346cdf"),
}


def sha_arquivo(p):
    h = hashlib.sha256()
    n = 0
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
            n += len(b)
    return n, h.hexdigest()


out = {"freeze": {}, "freeze_demais": {}, "pinos": [], "pinos_preregistro": [], "verbatins": {}, "divergencias": []}
fz_b = open(os.path.join(PRE, "FREEZE.json"), "rb").read()
out["FREEZE.json"] = {"bytes": len(fz_b), "sha256": hashlib.sha256(fz_b).hexdigest()}
FZ = json.loads(fz_b.decode("utf-8"))

for nome, (nb, h) in ORDEM.items():
    n, hh = sha_arquivo(os.path.join(PRE, nome))
    fzv = FZ[nome]
    ok = (n == nb == fzv["bytes"]) and (hh == h == fzv["sha256"])
    out["freeze"][nome] = {"bytes": n, "sha256": hh, "ordem": [nb, h], "freeze": [fzv["bytes"], fzv["sha256"]], "confere": ok}
    if not ok:
        out["divergencias"].append(nome)

for rel, (nb, h) in FZ["demais_arquivos_da_pasta"].items():
    p = os.path.join(PRE, *rel.split("/"))
    n, hh = sha_arquivo(p)
    ok = (n == nb) and (hh == h)
    out["freeze_demais"][rel] = {"bytes": n, "sha256": hh, "confere": ok}
    if not ok:
        out["divergencias"].append(rel)

for p, nb, h in PINOS_ORDEM:
    n, hh = sha_arquivo(p)
    ok = (n == nb) and (hh == h)
    out["pinos"].append({"arquivo": p, "bytes": n, "sha256": hh, "confere_com_a_ordem": ok})
    if not ok:
        out["divergencias"].append(p)

# pinos do proprio pre-registro (sha256 completo ou sha16)
PR = json.loads(open(os.path.join(PRE, "PREREGISTRO.json"), "rb").read().decode("utf-8"))
for p, nb, h in PR["pinos"]:
    try:
        n, hh = sha_arquivo(p)
    except OSError as e:
        out["pinos_preregistro"].append({"arquivo": p, "erro": str(e)})
        out["divergencias"].append(p)
        continue
    ok = (n == nb) and hh.startswith(h)
    out["pinos_preregistro"].append({"arquivo": p, "bytes": n, "sha256": hh, "pre": [nb, h], "confere": ok})
    if not ok:
        out["divergencias"].append("pino_pre:" + p)

for c, (p, s16) in TEXTOS.items():
    n, hh = sha_arquivo(p)
    ok = hh[:16] == s16 and hh == PR["a_verbatins"][c]["sha256"] and n == PR["a_verbatins"][c]["bytes"]
    out["verbatins"][c] = {"arquivo": p, "bytes": n, "sha256": hh, "sha16_ordem": s16, "confere": ok}
    if not ok:
        out["divergencias"].append(c)

out["veredito"] = "FREEZE_E_PINOS_CONFEREM" if not out["divergencias"] else "DIVERGENCIA"
dst = os.path.join(AQUI, "CONFERENCIA_FREEZE.json")
tmp = dst + ".tmp"
with open(tmp, "wb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8") + b"\n")
os.replace(tmp, dst)
print(json.dumps({k: out[k] for k in ("FREEZE.json", "freeze", "pinos", "verbatins", "divergencias", "veredito")}, ensure_ascii=False, indent=1))
print("pinos do pre-registro conferidos:", sum(1 for x in out["pinos_preregistro"] if x.get("confere")), "/", len(out["pinos_preregistro"]))
print("demais arquivos do FREEZE conferidos:", sum(1 for x in out["freeze_demais"].values() if x["confere"]), "/", len(out["freeze_demais"]))
sys.exit(0 if not out["divergencias"] else 2)
