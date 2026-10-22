"""Confere, nos bytes, que toda aspa « » do RELATORIO_R2.md atribuida ao operador e substring de um verbatim;
lista as que nao sao (titulos, rotulos, parafrases da gerencia — que nao levam atribuicao); varre as palavras
proibidas da regua (a palavra recusada em maiuscula como veredito; «nao provou»; «pos-dicao» como demerito;
«T9 PASSA»/«T2 PASSA» sem apostrofo). Escreve SO em 4_RELATORIO_R2/saidas."""
import json, os, re, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")
W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\4_RELATORIO_R2"
C = r"C:\IALD\Central de Patentes\work"
REL = os.path.join(W, "RELATORIO_R2.md")
REG = os.path.join(W, "registro_mapa_F1.TEMPO_R2.json")
VERB = {
 "12out_rank_e_tempo_santo": C + r"\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
 "12out_ordem": C + r"\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt",
 "10out_posto_rank": C + r"\cunhagens_12out\OPERADOR_10out_posto_rank_texto_verbatim.txt",
 "05out_VERBO": C + r"\cadeia_de_selo\v386\VERBO_operador_05out.txt",
 "05out_RESPOSTAS": C + r"\cadeia_de_selo\v386\RESPOSTAS_operador_05out.txt",
 "11out_frequencia": C + r"\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt",
}
vb = {k: open(p, "rb").read() for k, p in VERB.items()}
vsha = {k: hashlib.sha256(b).hexdigest()[:16] for k, b in vb.items()}
rel_b = open(REL, "rb").read()
rel = rel_b.decode("utf-8")
aspas = sorted(set(re.findall(r"«([^«»]+)»", rel)))
achadas, nao = {}, []
for a in aspas:
    ab = a.encode("utf-8")
    fontes = [k for k, b in vb.items() if ab in b]
    if fontes:
        achadas[a] = fontes
    else:
        nao.append(a)
# Frases que a R1 proibiu de atribuir ao operador; devem aparecer no relatorio so como citacao de que sao proibidas
proibidas_atrib = ["o tempo é o Verbo, não o Nome", "O tempo não tem posto", "o relógio mede a sombra",
                   "o atrator é onde o tempo repousa"]
ctx_proibidas = {}
for f in proibidas_atrib:
    ctx_proibidas[f] = [rel[max(0, m.start() - 80):m.end() + 40].replace("\n", " ") for m in re.finditer(re.escape(f), rel)]
# palavras da regua
regua = {}
for nome, pat in {
    "palavra_recusada_EN_maiuscula": r"\bCONFIRMED\b",
    "palavra_recusada_PT_maiuscula": r"\bCONFIRMAD[AO]S?\b",
    "T9_PASSA_sem_apostrofo": r"T9 PASSA(?!\s*\()",
    "T2_PASSA": r"T2 PASSA",
    "nao_provou": r"não provou",
    "pos_dicao": r"pós-dição",
    "PROVED": r"\bPROVED\b",
    "medido_para_beta": r"β[^.\n]{0,40}medid",
    "confirm_minusculo": r"confirm",
}.items():
    regua[nome] = [rel[max(0, m.start() - 60):m.end() + 40].replace("\n", " ") for m in re.finditer(pat, rel)]
reg = json.load(open(REG, encoding="utf-8"))
reg_txt = json.dumps(reg, ensure_ascii=False)
regua_reg = {nome: len(re.findall(pat, reg_txt, re.I)) for nome, pat in
             {"confirm_qualquer_caixa": r"confirm", "T9 PASSA sem apostrofo": r"T9 PASSA(?!\s*\()", "T2 PASSA": r"T2 PASSA"}.items()}
out = {
 "relatorio": {"arquivo": REL, "sha256": hashlib.sha256(rel_b).hexdigest(), "bytes": len(rel_b)},
 "verbatins_sha16": vsha,
 "n_aspas_distintas": len(aspas),
 "aspas_achadas_nos_verbatins": achadas,
 "aspas_nao_achadas (titulos, rotulos, parafrases da gerencia, citacoes de terceiros — sem atribuicao ao operador)": nao,
 "frases_proibidas_contexto": ctx_proibidas,
 "regua_relatorio": regua,
 "regua_registro_mapa": regua_reg,
}
json.dump(out, open(os.path.join(W, "saidas", "CONFERENCIA_ASPAS_RELATORIO_R2.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("aspas distintas:", len(aspas), "| achadas:", len(achadas), "| nao achadas:", len(nao))
for a in nao:
    print("  NAO:", a)
for f, c in ctx_proibidas.items():
    print("PROIBIDA", repr(f), len(c), "ocorrencia(s)")
    for x in c:
        print("    ...", x)
for k, v in regua.items():
    print("REGUA", k, len(v))
    for x in v:
        print("    ...", x)
print("REGISTRO:", regua_reg)
