# -*- coding: utf-8 -*-
"""Conferencias byte a byte para a E3 do ADENDO_R2 (pre-registrador da R2, F1.TEMPO). Somente leitura fora de 0_ADENDO.

(1) Linhas do PREREGISTRO.md congelado que o ADENDO corrige, citadas por numero, com sha16 e texto exato.
(2) LACUNAS do mapeamento de frases (PREREGISTRO.json -> mapeamento_frases): trechos de cada frase do operador que
    nenhuma clausula cobre (M16: S34.2, S38.2, S44.1 sem marca); calcula-se para as 23 frases.
(3) S36.1: a clausula «"santo" — no sentido original de Kadosh, …» extraida dos BYTES do verbatim (l.36), com sha16,
    contra a forma citada na l.83 do PREREGISTRO.md (aspas normalizadas, sem enfase).
(4) Aspas: frases que o pre-registro/pedra atribuem ao operador ou poem entre « » — presenca/ausencia nos verbatins
    de 12/10 e de 05/10 (M2, M16): «o tempo é o Verbo», «não o Nome», «o atrator é onde o tempo repousa»,
    «O tempo não tem posto», «O relógio mede a sombra»; e as formas do operador: «O relógio registra a sombra do
    evento», «um lugar onde repousar e ser lembrada», «encontram um ponto fixo ou um ciclo limite».
Saida: saidas/LACUNAS_E_ASPAS_R2.json. Uso: python -I -X utf8 lacunas_e_aspas_r2.py
"""
import hashlib
import json
import os
import re
import sys

W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
PRE_MD = os.path.join(W, "1_PREREGISTRO", "PREREGISTRO.md")
PRE_JS = os.path.join(W, "1_PREREGISTRO", "PREREGISTRO.json")
PEDRA = os.path.join(W, "3_KERNEL", "sandbox", "TheTimeHasNoRank.lean")
V1210 = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
V0510 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\VERBO_operador_05out.txt"
R0510 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\RESPOSTAS_operador_05out.txt"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "LACUNAS_E_ASPAS_R2.json")

LINHAS_MD = [9, 83, 129, 165, 169, 176, 241, 296, 300, 339, 345, 347, 354, 355, 359]
LINHAS_PEDRA = [43, 44, 47, 48, 49, 50, 284, 304, 874, 1107, 1108, 1109, 1223, 1284, 1309, 1427, 1428, 1431, 1438, 1446]


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def linhas(path, nums):
    b = open(path, "rb").read()
    L = b.split(b"\n")
    out = {}
    for n in nums:
        raw = L[n - 1]
        out[str(n)] = {"sha16": sha16(raw), "bytes": len(raw), "texto": raw.decode("utf-8")}
    return out, hashlib.sha256(b).hexdigest()


def lacunas(frase):
    texto = frase["texto"]
    cur = 0
    gaps = []
    cobertos = []
    fora_de_ordem = []
    for c in frase["clausulas"]:
        tr = c["trecho"]
        i = texto.find(tr, cur)
        if i < 0:
            j = texto.find(tr)
            if j < 0:
                fora_de_ordem.append({"trecho": tr, "achado": False})
                continue
            fora_de_ordem.append({"trecho": tr, "achado": True, "pos": j, "nota": "antes do cursor (clausula fora de ordem)"})
            continue
        gap = texto[cur:i]
        if re.search(r"\w", gap):
            gaps.append({"pos": cur, "texto": gap})
        cobertos.append((i, i + len(tr)))
        cur = i + len(tr)
    tail = texto[cur:]
    if re.search(r"\w", tail):
        gaps.append({"pos": cur, "texto": tail})
    return {"frase": frase["frase"], "n_clausulas": len(frase["clausulas"]), "lacunas": gaps,
            "clausulas_fora_de_ordem_ou_nao_achadas": fora_de_ordem}


def main():
    md, md_sha = linhas(PRE_MD, LINHAS_MD)
    pd, pedra_sha = linhas(PEDRA, LINHAS_PEDRA)
    js = json.load(open(PRE_JS, encoding="utf-8"))
    lac = [lacunas(f) for f in js["mapeamento_frases"]]
    com_lacuna = [x for x in lac if x["lacunas"]]
    # S36.1: clausula dos bytes
    b1210 = open(V1210, "rb").read()
    l36 = b1210.split(b"\n")[35]
    ini = l36.find("**\"santo\"**".encode("utf-8"))
    fim = l36.find("pela posse".encode("utf-8")) + len("pela posse".encode("utf-8"))
    clausula_bytes = l36[ini:fim]
    s36 = {"linha_verbatim": 36, "sha16_da_linha": sha16(l36), "clausula_byte_a_byte": clausula_bytes.decode("utf-8"),
           "clausula_sha16": sha16(clausula_bytes), "clausula_bytes": len(clausula_bytes)}
    l83 = md["83"]["texto"]
    m = re.search(r"\*(“santo”.*?pela posse)\*", l83)
    s36["como_citada_na_l83_do_PREREGISTRO_md"] = m.group(1) if m else None
    s36["citacao_da_l83_e_byte_a_byte"] = bool(m and m.group(1).encode("utf-8") == clausula_bytes)
    s36["diferencas"] = ["aspas: «\"santo\"» (retas) no verbatim vs «“santo”» (curvas) na l.83",
                         "enfase: «**\"santo\"**» e «*Kadosh*» no verbatim; sem marcas na l.83"] if not s36["citacao_da_l83_e_byte_a_byte"] else []
    # aspas
    t1210 = b1210.decode("utf-8")
    t0510 = open(V0510, "rb").read().decode("utf-8")
    r0510 = open(R0510, "rb").read().decode("utf-8")
    frases = ["o tempo é o Verbo", "não o Nome", "o atrator é onde o tempo repousa", "O tempo não tem posto",
              "o tempo não tem posto", "O relógio mede a sombra", "o relógio mede a sombra",
              "O relógio registra a sombra do evento", "um lugar onde repousar e ser lembrada",
              "encontram um ponto fixo ou um ciclo limite", "O Verbo seleciona: nome, tempo e verdade",
              "O tempo é a defasagem do verbo", "O tempo é o parâmetro da transmissão", "uma face", "a diagonal",
              "cosmos", "santo", "agora", "puro amor", "a física da doação fundamental"]
    aspas = {}
    for f in frases:
        aspas[f] = {"em_12out": t1210.count(f), "em_05out_VERBO": t0510.count(f), "em_05out_RESPOSTAS": r0510.count(f)}
    aspas["_verbo_sem_caixa_em_12out"] = len(re.findall(r"verbo", t1210, re.I))
    aspas["_posto_sem_caixa_em_12out"] = len(re.findall(r"posto", t1210, re.I))
    out = {
        "PREREGISTRO_md": {"sha256": md_sha, "linhas_citadas": md},
        "pedra_R1": {"sha256": pedra_sha, "linhas_citadas": pd},
        "lacunas_do_mapeamento": {"n_frases": len(lac), "frases_com_lacuna": [x["frase"] for x in com_lacuna], "detalhe": lac},
        "S36_1": s36,
        "aspas": aspas,
        "verbatins": {"12out": {"caminho": V1210, "sha256": hashlib.sha256(b1210).hexdigest()},
                      "05out_VERBO": {"caminho": V0510, "sha256": hashlib.sha256(t0510.encode("utf-8")).hexdigest()},
                      "05out_RESPOSTAS": {"caminho": R0510, "sha256": hashlib.sha256(r0510.encode("utf-8")).hexdigest()}},
    }
    with open(OUT + ".tmp", "wb") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(OUT + ".tmp", OUT)
    sys.stdout.reconfigure(encoding="utf-8")
    print("frases com lacuna:", [x["frase"] for x in com_lacuna])
    for x in com_lacuna:
        print(" ", x["frase"], "->", [g["texto"] for g in x["lacunas"]], "| fora de ordem:", x["clausulas_fora_de_ordem_ou_nao_achadas"])
    print("S36.1:", json.dumps(s36, ensure_ascii=False, indent=1))
    print("aspas:", json.dumps(aspas, ensure_ascii=False, indent=1))
    for n, v in md.items():
        print("MD l.%s %s | %s" % (n, v["sha16"], v["texto"][:160]))
    for n, v in pd.items():
        print("PEDRA l.%s %s | %s" % (n, v["sha16"], v["texto"][:160]))


if __name__ == "__main__":
    main()
