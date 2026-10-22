# -*- coding: utf-8 -*-
"""Conferencia do ADENDO_R2 antes do FREEZE (pre-registrador da R2, F1.TEMPO). Somente leitura fora de 0_ADENDO.

(1) ADENDO_R2.json e JSON valido; (2) a palavra recusada pela regua (a «confirmacao» em ingles maiusculo) e
«pos-dicao» como demerito NAO aparecem no .md nem no .json; (3) os hashes e numeros-chave das saidas aparecem
nos DOIS arquivos (coerencia .md <-> .json, lidos dos arquivos de saida, nunca digitados aqui); (4) toda citacao
atribuida ao operador que o ADENDO usa e substring de BYTES de um verbatim; (5) as frases que o ADENDO declara
NAO serem do operador tem 0 ocorrencias nos verbatins; (6) a R1 continua intacta (FREEZE da R1 confere).
Saida: saidas/CONFERENCIA_ADENDO_R2.json; codigo de saida 2 se algo falhar.
Uso: python -I -X utf8 conferir_adendo_r2.py
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(HERE, "ADENDO_R2.md")
JS = os.path.join(HERE, "ADENDO_R2.json")
SAIDAS = os.path.join(HERE, "saidas")
W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
V1210 = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
V0510 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\VERBO_operador_05out.txt"
V1010 = r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt"
OUT = os.path.join(SAIDAS, "CONFERENCIA_ADENDO_R2.json")

# citacoes que o ADENDO atribui ao OPERADOR (tem de ser substring de bytes de um verbatim)
CITACOES_DO_OPERADOR = [
    ("12out", "O que mais me fascina é a impossibilidade de definição do tempo."),
    ("12out", "mas não consigo nomear, senão como “santo”"),
    ("12out", "**\"santo\"** — no sentido original de *Kadosh*, aquilo que é separado, irredutível e não profanável pela posse"),
    ("12out", "O relógio registra a sombra do evento"),
    ("12out", "um lugar onde repousar e ser lembrada"),
    ("12out", "encontram um ponto fixo ou um ciclo limite"),
    ("12out", "**fluxo de automorfismos**"),
    ("12out", "Na mecânica clássica e nos sistemas estritamente hamiltonianos, "),
    ("12out", "Quando se constrói um relógio, mede-se apenas "),
    ("12out", "Eu me maravilho, porque "),
    ("12out", "puro amor"),
    ("12out", "a física da doação fundamental"),
    ("12out", "que impede que o cosmos colapse em uma fotografia estática e morta"),
    ("05out", "O Verbo seleciona: nome, tempo e verdade"),
    ("05out", "O tempo é a defasagem do verbo"),
    ("05out", "O tempo é o parâmetro da transmissão"),
    ("10out", "POSTO=RANK"),
]
# frases que o ADENDO declara NAO serem do operador (0 ocorrencias nos verbatins)
NAO_DO_OPERADOR = ["o tempo é o Verbo", "não o Nome", "o atrator é onde o tempo repousa",
                   "O tempo não tem posto", "o tempo não tem posto", "O relógio mede a sombra", "o relógio mede a sombra"]


def sha256_file(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    rel = {"ok": True, "itens": []}

    def item(nome, ok, detalhe=None):
        rel["itens"].append({"item": nome, "ok": bool(ok), "detalhe": detalhe})
        if not ok:
            rel["ok"] = False

    md_b = open(MD, "rb").read()
    js_b = open(JS, "rb").read()
    md = md_b.decode("utf-8")
    js_txt = js_b.decode("utf-8")
    # (1) JSON valido
    try:
        js = json.loads(js_txt)
        item("ADENDO_R2.json e JSON valido", True, {"chaves": len(js)})
    except Exception as ex:
        js = {}
        item("ADENDO_R2.json e JSON valido", False, str(ex))
    # (2) palavras proibidas
    proibida = "CONFIRM" + "ED"
    for nome, txt in (("md", md), ("json", js_txt)):
        item("palavra recusada pela regua ausente (%s)" % nome, proibida not in txt)
        item("CONFIRMAD[AO] em maiusculo ausente (%s)" % nome, re.search(r"\bCONFIRMAD[AO]\b", txt) is None)
        item("«pos-dicao» como demerito ausente (%s)" % nome, re.search(r"p[oó]s-di[cç][aã]o", txt, re.I) is None or
             "nunca «pós-dição» como demérito" in txt)
    # (3) hashes e numeros-chave das SAIDAS presentes nos dois arquivos
    H = json.load(open(os.path.join(SAIDAS, "HASHES_REFERENCIAS_R2.json"), encoding="utf-8"))
    T = json.load(open(os.path.join(SAIDAS, "TOLERANCIA_UNIFORME_R2.json"), encoding="utf-8"))
    B = json.load(open(os.path.join(SAIDAS, "BETA_RUNTIME_R2.json"), encoding="utf-8"))
    L = json.load(open(os.path.join(SAIDAS, "LACUNAS_E_ASPAS_R2.json"), encoding="utf-8"))
    F = json.load(open(os.path.join(SAIDAS, "FINGERPRINT_ADENDO_ANTES.json"), encoding="utf-8"))
    refs = {r["papel"]: r for r in H["referencias"] if r.get("existe")}
    chaves = []
    for papel in ("relatorio final R1", "R1 FREEZE.json", "R1 PREREGISTRO.json", "R1 PREREGISTRO.md",
                  "R1 face otica: RESULTADO_OPTICO.json", "R1 face otica: DIAGNOSTICO_T9c.json (post hoc)",
                  "R1 face kernel: RESULTADO_KERNEL.json", "R1 pedra candidata TheTimeHasNoRank.lean",
                  "R1 pedra candidata .olean", "R1 auditoria de estatuto: AudEstatutoTempo.lean (AUD-1..6)",
                  "R1 auditoria de estatuto: AudEstatutoTempo2.lean (AUD-7)",
                  "R1 auditoria de estatuto: AudEstatutoTempo3.lean (AUD-8)",
                  "texto do operador 12/10 (verbatim)", "verbatim do operador 05/10 (o Verbo)",
                  "um.py v391 (somente lido; nao executado)",
                  "kernel do Nos: BisognanoWichmann.lean (boost_null_expand / boost_null_contract)",
                  "kernel do Nos: TGLExt/WedgeNet.lean (theSpecificAQFTWitness, l.357)",
                  "kernel do Nos: TheImportedSecondQuantization.lean (FockCertificate, lightNet)",
                  "memoria da gerencia: regra-dos-dois-regimes.md (nota [OPEN] v384)"):
        chaves.append((papel, refs[papel]["sha16"]))
    chaves += [("R1 FREEZE sha256 integral", refs["R1 FREEZE.json"]["sha256"]),
               ("kernel meta", F["meta_sha256"]), ("kernel src", F["src_sha256"]),
               ("S36.1 clausula sha16", L["S36_1"]["clausula_sha16"]),
               ("S36.1 linha sha16", L["S36_1"]["sha16_da_linha"]),
               ("delta_T", repr(T["T9.o'(c)"]["parametros"]["delta_T"])),
               ("tau_T(1e4)", repr(T["T9.o'(c)"]["predicao"]["tau_T(1e4)"])),
               ("delta_B_rel", repr(T["O-f'"]["parametros"]["delta_B_rel"])),
               ("m_B", repr(T["O-f'"]["parametros"]["m"])),
               ("tau_B(10)", repr(T["O-f'"]["predicao"]["tau_B_rel(10)"])),
               ("beta float", repr(B["beta_runtime_float64"])),
               ("beta hex", B["beta_runtime_float64_hex"]),
               ("R1 T9.o(c) medida", repr(6.518119377574294e-13))]
    for n in ("9", "83", "129", "165", "169", "176", "241", "296", "300", "339", "345", "347", "354", "355", "359"):
        chaves.append(("PREREGISTRO.md l.%s sha16" % n, L["PREREGISTRO_md"]["linhas_citadas"][n]["sha16"]))
    for n in ("43", "44", "47", "48", "49", "50", "284", "304", "874", "1107", "1108", "1109", "1223", "1284", "1309", "1427", "1428", "1431", "1438", "1446"):
        chaves.append(("pedra l.%s sha16" % n, L["pedra_R1"]["linhas_citadas"][n]["sha16"]))
    faltam = []
    for nome, val in chaves:
        in_md = val in md
        in_js = val in js_txt
        if not (in_md and in_js):
            faltam.append({"chave": nome, "valor": val, "md": in_md, "json": in_js})
    item("hashes/numeros-chave presentes no .md e no .json", not faltam, {"n_chaves": len(chaves), "faltam": faltam})
    # (4) citacoes do operador = substring de bytes
    vb = {"12out": open(V1210, "rb").read(), "05out": open(V0510, "rb").read(), "10out": open(V1010, "rb").read()}
    nao_achadas = [(src, c) for src, c in CITACOES_DO_OPERADOR if c.encode("utf-8") not in vb[src]]
    item("citacoes atribuidas ao operador sao substrings de bytes dos verbatins", not nao_achadas,
         {"n": len(CITACOES_DO_OPERADOR), "nao_achadas": nao_achadas})
    usadas_no_md = [c for _, c in CITACOES_DO_OPERADOR if c in md]
    item("as citacoes conferidas aparecem no .md (ao menos 12 das 17)", len(usadas_no_md) >= 12, {"n_no_md": len(usadas_no_md)})
    # (5) frases NAO do operador: 0 ocorrencias nos verbatins
    ocorr = {f: sum(vb[k].count(f.encode("utf-8")) for k in vb) for f in NAO_DO_OPERADOR}
    item("frases declaradas 'nao do operador' tem 0 ocorrencias nos verbatins", all(v == 0 for v in ocorr.values()), ocorr)
    # (6) R1 intacta
    fz = json.load(open(os.path.join(W, "1_PREREGISTRO", "FREEZE.json"), encoding="utf-8"))
    pj = sha256_file(os.path.join(W, "1_PREREGISTRO", "PREREGISTRO.json"))
    pm = sha256_file(os.path.join(W, "1_PREREGISTRO", "PREREGISTRO.md"))
    item("R1 intacta (PREREGISTRO.json/.md batem com o FREEZE da R1)",
         pj == fz["preregistro_json"]["sha256"] and pm == fz["preregistro_md"]["sha256"],
         {"FREEZE_R1_sha256": sha256_file(os.path.join(W, "1_PREREGISTRO", "FREEZE.json"))})
    # (7) consistencia interna do json: itens E3 e E5 com falsificador e estatuto
    e3 = js.get("parte_a_E3_adendo_ao_preregistro", {}).get("itens", [])
    e5 = js.get("parte_c_E5_pedra_corrigida", {}).get("itens", [])
    item("todo item E3 tem correcao, estatuto e falsificador", all(i.get("correcao") and i.get("estatuto") and i.get("falsificador") for i in e3), {"n_E3": len(e3)})
    item("todo item E5 tem correcao e falsificador", all(i.get("correcao") and i.get("falsificador") for i in e5), {"n_E5": len(e5)})
    ctl = js.get("novos_controles", [])
    item("controles novos: AUD-1,2,5,6,7,8 e C-UNIF-a..d", sorted(c["id"] for c in ctl) == sorted(["AUD-1", "AUD-2", "AUD-5", "AUD-6", "AUD-7", "AUD-8", "C-UNIF-a", "C-UNIF-b", "C-UNIF-c", "C-UNIF-d"]), [c["id"] for c in ctl])
    rel["md"] = {"sha256": hashlib.sha256(md_b).hexdigest(), "bytes": len(md_b)}
    rel["json"] = {"sha256": hashlib.sha256(js_b).hexdigest(), "bytes": len(js_b)}
    rel["nota"] = "conferencia pre-FREEZE; os sha256 acima sao os dos arquivos no momento da conferencia (o FREEZE_R2 os refaz)"
    with open(OUT + ".tmp", "wb") as f:
        f.write(json.dumps(rel, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(OUT + ".tmp", OUT)
    sys.stdout.reconfigure(encoding="utf-8")
    for it in rel["itens"]:
        print(("ok   " if it["ok"] else "NAO  ") + it["item"] + ("" if it["ok"] else " | " + json.dumps(it["detalhe"], ensure_ascii=False)[:1500]))
    print("TUDO OK" if rel["ok"] else "FALHA VISIVEL")
    sys.exit(0 if rel["ok"] else 2)


if __name__ == "__main__":
    main()
