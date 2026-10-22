"""Auditoria (lente ESTATUTO E REGRA) da F1.TEMPO: confere por script
(1) o texto do operador e a segunda parte; (2) a segmentacao das 23 frases e os sha256;
(3) a cobertura de cada frase pelas clausulas mapeadas (trechos) e as marcas;
(4) os excertos do canone (arquivo, sha256 do arquivo, presenca byte a byte, sha16 do excerto).
Somente leitura das fontes; escreve so o JSON de saida (argv[1]).
Uso: python -I -X utf8 conferir_verbatins.py <saida.json>"""
import hashlib, json, re, sys, unicodedata

PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.json"
TXT = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"


def sha(b):
    return hashlib.sha256(b).hexdigest()


out = {"fontes": {}, "frases": [], "excertos": [], "marcas": {}, "problemas": []}
pre_b = open(PRE, "rb").read()
out["fontes"]["PREREGISTRO.json"] = {"sha256": sha(pre_b), "bytes": len(pre_b)}
pre = json.loads(pre_b.decode("utf-8"))
tb = open(TXT, "rb").read()
out["fontes"]["texto"] = {"sha256": sha(tb), "bytes": len(tb), "crlf": tb.count(b"\r\n")}
seg = pre["texto_do_operador"]["segunda_parte"]
off, nb = seg["byte_offset"], seg["bytes"]
part2 = tb[off:off + nb]
out["fontes"]["segunda_parte"] = {"offset": off, "bytes": len(part2), "sha256": sha(part2),
                                  "confere": sha(part2) == seg["sha256"],
                                  "vai_ate_o_fim": off + nb == len(tb),
                                  "comeca_em": part2[:40].decode("utf-8", "replace")}
# a segunda parte deve comecar exatamente em «O que mais me fascina»
txt = tb.decode("utf-8")
i0 = txt.find("O que mais me fascina")
out["fontes"]["inicio_char"] = i0
out["fontes"]["inicio_byte_calc"] = len(txt[:i0].encode("utf-8"))

# (2) segmentacao independente: paragrafos = linhas nao vazias da segunda parte;
#     frases separadas em ". " seguido de maiuscula (regra declarada no pre-registro)
p2 = part2.decode("utf-8")
paras = [ln for ln in p2.split("\n") if ln.strip()]
mine = []
for para in paras:
    parts = re.split(r"(?<=\.)\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])", para)
    mine.extend(parts)
out["segmentacao_independente_n"] = len(mine)
mapped = pre["mapeamento_frases"]
out["mapeadas_n"] = len(mapped)
mine_set = {sha(s.encode("utf-8")): s for s in mine}
for fr in mapped:
    t = fr["texto"]
    tbytes = t.encode("utf-8")
    rec = {"frase": fr["frase"], "sha16": fr["sha256"][:16],
           "sha_confere": sha(tbytes) == fr["sha256"],
           "no_arquivo_byte_a_byte": tbytes in tb,
           "na_segmentacao_independente": sha(tbytes) in mine_set}
    # (3) cobertura por trechos das clausulas
    covered = [False] * len(t)
    marcas = []
    trechos_nao_achados = []
    for cl in fr.get("clausulas", []):
        tr = cl.get("trecho", "")
        m = cl.get("marca", "")
        marcas.append(m)
        out["marcas"][m] = out["marcas"].get(m, 0) + 1
        # trecho pode conter «[...]» de elisao: casa cada pedaco
        pieces = [p.strip() for p in re.split(r"\[\s*(?:\.\.\.|…)\s*\]", tr) if p.strip()]
        if tr.startswith("(") and tr.endswith(")"):
            continue  # clausula meta (ex.: «(face finita)»), nao e trecho do texto
        for p in pieces:
            p2_ = p.replace("“", "“").replace("”", "”")
            k = t.find(p2_)
            if k < 0:
                # tolera aspas/asteriscos de enfase
                alt = p2_.replace("**", "").replace("*", "")
                k = t.replace("**", "").find(alt)
                if k < 0:
                    trechos_nao_achados.append(p)
                    continue
                continue
            for j in range(k, k + len(p2_)):
                covered[j] = True
        if not m.strip():
            out["problemas"].append(f"{fr['frase']}: clausula sem marca: {tr[:60]}")
    # trechos nao cobertos (ignora pontuacao/espacos/conectivos curtos)
    gaps = []
    cur = ""
    for ch, c in zip(t, covered):
        if not c:
            cur += ch
        else:
            if cur:
                gaps.append(cur)
            cur = ""
    if cur:
        gaps.append(cur)
    gaps_sig = [g.strip() for g in gaps if len(re.sub(r"[\W_]+", "", g)) >= 4]
    rec["marcas"] = marcas
    rec["trechos_nao_achados"] = trechos_nao_achados
    rec["lacunas_nao_mapeadas"] = gaps_sig
    out["frases"].append(rec)
# (4) excertos do canone
for v in pre["verbatins_citados"]:
    try:
        fb = open(v["arquivo"], "rb").read()
        fsha = sha(fb)
    except Exception as e:  # falha visivel
        out["excertos"].append({"fonte": v["id"], "erro": repr(e)})
        continue
    for ex in v.get("excertos", []):
        eb = ex["texto"].encode("utf-8")
        out["excertos"].append({
            "fonte": v["id"], "excerto": ex["id"], "arquivo_sha_confere": fsha == v["sha256"],
            "arquivo_bytes": len(fb), "presente_byte_a_byte": eb in fb,
            "sha16_excerto_confere": sha(eb)[:16] == ex.get("sha16", ex.get("sha256", ""))[:16],
            "estatuto": v.get("estatuto", ""), "texto": ex["texto"][:140]})
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ("fontes", "segmentacao_independente_n", "mapeadas_n", "marcas")},
                 ensure_ascii=False, indent=1))
print("problemas:", out["problemas"])
for r in out["frases"]:
    flag = (not r["sha_confere"]) or (not r["no_arquivo_byte_a_byte"]) or (not r["na_segmentacao_independente"])
    print(r["frase"], "OK" if not flag else "DIVERGE", "| nao_achados:", r["trechos_nao_achados"],
          "| lacunas:", r["lacunas_nao_mapeadas"])
bad = [e for e in out["excertos"] if not (e.get("arquivo_sha_confere") and e.get("presente_byte_a_byte")
                                          and e.get("sha16_excerto_confere"))]
print("excertos:", len(out["excertos"]), "divergentes:", json.dumps(bad, ensure_ascii=False)[:2000])
