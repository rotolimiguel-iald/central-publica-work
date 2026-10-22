# -*- coding: utf-8 -*-
"""Monta 3_KERNEL\\rodada2\\RESULTADO_KERNEL.json (RODADA 2 do construtor do kernel, F1.FREQUENCIA, trilha POSTO).
Le SO artefatos ja gravados (rodada 1 em 3_KERNEL, so leitura; rodada 2 em 3_KERNEL\\rodada2) e falha visivelmente se
algum numero nao fecha: cada declaracao citada por parte tem de existir na pedra r2 e ter axiomas no trio; a pedra, o
.olean e os recibos sao conferidos por sha256 dos bytes. Nao escreve fora de 3_KERNEL\\rodada2."""
import datetime, hashlib, json, os, sys

R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.dirname(R2)
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def J(*p):
    return json.loads(open(os.path.join(*p), "rb").read().decode("utf-8"))


def sha_arq(p):
    b = open(p, "rb").read()
    return len(b), hashlib.sha256(b).hexdigest()


falhas = []
R1 = J(K, "RESULTADO_KERNEL.json")
FZ = J(R2, "CONFERENCIA_FREEZE.json")
INT = J(R2, "INTEGRIDADE_RODADA1.json")
BETA = J(R2, "BETA_RUNTIME.json")
MON = J(R2, "MONTAGEM_PEDRA_R2_t03.json")
AUD = J(R2, "AUDITORIA_KERNEL.json")
DEC = J(R2, "DECLARACOES.json")
VAR = J(R2, "VARREDURA_FONTE.json")
CIT = J(R2, "CITACOES_R2.json")
CK = J(R2, "CONSULTAS_KERNEL.json")
FPA = J(R2, "IMPRESSAO_DIGITAL_KERNEL_ANTES.json")
FPD = J(R2, "IMPRESSAO_DIGITAL_KERNEL_DEPOIS.json")
FPF = J(R2, "IMPRESSAO_DIGITAL_KERNEL_FINAL_POS_LIMPEZA.json")
REC = {t: J(R2, "logs", t + "_RECIBO.json") for t in
       ("repro_r1_pedra", "r2_tentativa01", "r2_tentativa02", "r2_tentativa03", "auditoria_r2", "auditoria_r2_t03",
        "r2_repro_determinismo", "sonda_colA", "sonda_colA_t2", "sonda_colB", "sonda_colB_t2", "sonda_colC")}

PEDRA = os.path.join(R2, "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
OLEAN = os.path.join(R2, "olean", "TheUnitIsTheRank.olean")
pb, ph = sha_arq(PEDRA)
obb, oh = sha_arq(OLEAN)
# a pedra compilada, auditada, varrida e citada e a mesma
for nome, h in (("montagem", MON["r2"]["sha256"]), ("compilacao", REC["r2_tentativa03"]["source_sha256"]),
                ("auditoria", AUD["pedra_sha256_auditada"]), ("varredura", VAR["pedra_sha256"]),
                ("citacoes", CIT["pedra_sha256"]), ("declaracoes", DEC["pedra_sha256"]),
                ("determinismo", REC["r2_repro_determinismo"]["source_sha256"])):
    if h != ph:
        falhas.append("pedra diverge em " + nome)
if REC["r2_tentativa03"]["olean_sha256"] != oh or REC["r2_repro_determinismo"]["olean_sha256"] != oh:
    falhas.append("olean diverge do compilado")
if REC["repro_r1_pedra"]["olean_sha256"] != R1["compilacao"]["olean"]["sha256"]:
    falhas.append("reproducao da rodada 1 diverge")
for t in ("r2_tentativa03", "auditoria_r2_t03", "r2_repro_determinismo", "repro_r1_pedra"):
    r = REC[t]
    if r["exit_code"] != 0 or r["n_erros"] or r["ocorrencias_sorryAx"] or r["declaration_uses_sorry"]:
        falhas.append("recibo com falha: " + t)
fp_igual = (FPA["sha256_metadados"] == FPD["sha256_metadados"] == FPF["sha256_metadados"]
            and FPA["sha256_conteudo_lean"] == FPD["sha256_conteudo_lean"] == FPF["sha256_conteudo_lean"]
            and FPA["n_arquivos"] == FPD["n_arquivos"] == FPF["n_arquivos"])
if not fp_igual:
    falhas.append("impressao digital do tgl_kernel mudou")
fp_r1 = R1["tgl_kernel_impressao_digital"]["antes"]
fp_igual_r1 = [FPA["sha256_metadados"], FPA["sha256_conteudo_lean"], FPA["n_arquivos"]] == fp_r1

ax = {d["nome"]: d["axiomas"] for d in AUD["por_declaracao"]}
nomes_r2 = {d["nome_completo"] for d in DEC["declaracoes"]}
hyp = AUD["hipoteses_por_teorema"]
NS = "TGLExt.TheUnitIsTheRank."

COMPL = {
    "B2.a": ["anticomm_complement_zero_iff", "probe_complement_anticomm_both_sides"],
    "B3.a": ["leak_of_complement", "one_sub_rhoOut_eq_Qtheta_neg", "Qtheta_eq_one_sub_rhoOut_iff",
             "probe_two_readings_of_Q"],
    "B9.b": ["dephasingActs_iff_forward", "dephase_fixed_iff_neg", "probe_forward_both_sides",
             "probe_fixed_neg_both_sides"],
    "B9.a": ["dephasingActs_iff_forward"],
    "B8.b": ["dephasingActs_iff_forward"],
}
por_parte = []
for p in R1["por_parte"]:
    q = dict(p)
    axs = []
    for d in p["declaracoes"]:
        if d not in nomes_r2:
            falhas.append("declaracao da parte %s ausente na r2: %s" % (p["id"], d))
            continue
        a = ax.get(d)
        if a is None or not set(a) <= TRIO:
            falhas.append("axiomas fora do trio: " + d)
        axs.append(",".join(sorted(a or [])))
    q["axiomas"] = sorted(set(axs))
    q["hipoteses_sem_peso"] = sorted({h for d in p["declaracoes"] for h in hyp.get(d, {}).get("hipoteses_nao_usadas", [])})
    if p["id"] in COMPL:
        cs = [NS + c for c in COMPL[p["id"]]]
        for c in cs:
            if c not in nomes_r2 or not set(ax.get(c) or ["?"]) <= TRIO:
                falhas.append("complemento ausente/fora do trio: " + c)
        q["complementos_rodada2_fora_do_preregistro"] = cs
    q["rodada"] = "enunciado e prova identicos aos da rodada 1 (codigo sem comentarios identico); docstring com notas ao lado"
    if p["id"] == "B3.d":
        import re as _re, math as _m
        v4 = open(r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt", "rb").read().decode("utf-8").split(chr(10))
        mnum = _re.search(r"\\approx\s*([0-9]+\.[0-9]+)", v4[15])
        PRE = J(os.path.dirname(K), "1_PREREGISTRO", "PREREGISTRO.json")
        mtol = _re.search(r"<=\s*([0-9.eE+-]+)", PRE["protocolo_otico"]["CONF_OPERADOR"])
        bval = float(BETA["beta_repr"])
        q["runtime_informativo_rodada2"] = {
            "estatuto": "[REAL runtime, informativo] a parte e decidida pela face O (regra f: onde ha uma face so, ela decide); beta nunca entra no kernel como numero",
            "numero_do_operador_lido_dos_bytes_V4_l16": mnum.group(1) if mnum else None,
            "beta_runtime": BETA["beta_repr"],
            "abs_beta_menos_numero": abs(bval - float(mnum.group(1))) if mnum else None,
            "tolerancia_CONF_OPERADOR_lida_do_preregistro": mtol.group(1) if mtol else None,
            "dentro": (abs(bval - float(mnum.group(1))) <= float(mtol.group(1))) if (mnum and mtol) else None}
        if not (mnum and mtol):
            falhas.append("B3.d: numero ou tolerancia ilegivel")
    por_parte.append(q)

controles = []
for c in R1["controles"]:
    for d in c["declaracoes"]:
        if d not in nomes_r2 or not set(ax.get(d) or ["?"]) <= TRIO:
            falhas.append("controle ausente/fora do trio: " + d)
    controles.append(c)

sondas = dict(R1["sondas_de_vacuidade"])
sondas["os_dois_lados_de_cada_iff"] = dict(sondas["os_dois_lados_de_cada_iff"])
sondas["os_dois_lados_de_cada_iff"].update({
    "dephase_fixed_iff_neg (rodada 2)": "probe_fixed_neg_both_sides (rho*, t = +-1: os dois lados verdadeiros; F_{pi/4}(1), t = +-1: os dois falsos)",
    "dephasingActs_iff_forward (rodada 2)": "probe_forward_both_sides (th = pi/4 atua num t > 0; th = 0 nenhum t > 0)",
    "anticomm_complement_zero_iff (rodada 2)": "probe_complement_anticomm_both_sides (th = 0 nulo; th = pi/4 nao nulo)",
    "Qtheta_eq_one_sub_rhoOut_iff (rodada 2)": "probe_two_readings_of_Q (th = 0 coincidem; th_M com c : TGLCoupling diferem)",
})
for s in ("probe_fixed_neg_both_sides", "probe_forward_both_sides", "probe_complement_anticomm_both_sides",
          "probe_two_readings_of_Q"):
    if NS + s not in nomes_r2:
        falhas.append("sonda ausente: " + s)

res_count = {}
for q in por_parte:
    res_count.setdefault(q["resultado_K"], []).append(q["id"])

novas = [NS + n for n in MON["declaracoes_acrescentadas"]]
achados_r2 = [
    "R2-1 [REAL no sandbox; fora do pre-registro] «D atua» no semigrupo PARA A FRENTE: dephase_fixed_iff_neg (D_t x = x <=> D_{-t} x = x, quaisquer taxas, qualquer matriz) e dephasingActs_iff_forward (exists t em R <=> exists t > 0, quaisquer taxas). A definicao pre-registrada (exists t, sem sinal) e equivalente a pedir t > 0: B9 nunca precisa do inverso de D_t, que esta fora do semigrupo. Responde a sonda SondaTempoPositivo do auditor de reproducao da rodada 1 (la provada so com taxas positivas).",
    "R2-2 [REAL no sandbox; fora do pre-registro] as duas leituras de Q-chapeu (anexo A8 do otico da rodada 1): 1 - F_th(1) = Q_{-th} (one_sub_rhoOut_eq_Qtheta_neg); coincidem com Q_th = S(th)^H Q0 S(th) <=> sin 2th = 0 (Qtheta_eq_one_sub_rhoOut_iff; em th_M diferem: probe_two_readings_of_Q); dao o MESMO vazamento Tr(rho* .) = sin^2 th (leak_of_complement) e o MESMO «{., rho*} = 0 <=> sin th = 0» (anticomm_complement_zero_iff). B2 e B3 nao dependem da escolha; qual delas e o Q-chapeu de V4 l.16 e decisao do texto da v392.",
    "R2-3 [REAL - conferido nos bytes] citacoes: na rodada 1 as duas citacoes de V4 no cabecalho estavam em «» como parafrase (LaTeX renderizado; a segunda comecava dentro de «pequeno»); na r2 estao os bytes de V4 l.13 e l.16, a formula de V2 l.16 em LaTeX, a forma ASCII do um.py (l.6526 «Tudo = D_beta(F(1)) = VERDADE»; l.6502; l.6515 «limite inalcancavel») — 15 citacoes conferidas byte a byte na linha (CITACOES_R2.json); 3 citacoes de V1 herdadas da rodada 1 so conferem normalizando a quebra de linha do comentario (conteudo literal).",
    "R2-4 [REAL — consulta ao kernel] HOMONIMO de B9.c: nenhum enunciado do kernel do Nos liga axiomFlow (o fluxo do lock) a Smat/rhoOut/dephase/diagExpect (CONSULTAS_KERNEL.json: 1209 .lean varridos; os dois so coexistem em TheVerbSelectsTheAction.lean, sem enunciado-ponte). B9.c segue CITADO_REAL como termo existente, mas nao apoia a leitura B9.b.",
    "R2-5 [REAL — consulta ao kernel] as pedras da F1.ATRATOR (TheSingularityReadsTheAttractor*) NAO estao no kernel do Nos; a pedra desta unidade tambem nao (CONSULTAS_KERNEL.json). I/2 como estado fixo do canal entra por citacao a F1.ATRATOR (P3.b).",
    "R2-6 [REAL no sandbox; instalacao] a constante auxiliar TGLExt.rhoOut.eq_1, gerada neste modulo por `simp [rhoOut]` (ja na rodada 1), NAO colide com outro modulo que tambem a realize: sondas ColA/ColB/ColC (EXIT 0; os dois modulos a listam; importa-los juntos funciona).",
    "R2-7 [REAL — medido aqui] determinismo: a pedra da rodada 1, recompilada num sandbox novo, da o MESMO .olean (42b22d4f...); a pedra r2 recompilada da o MESMO .olean (d0830b4b... nas duas compilacoes).",
    "R2-8 [REAL — medido aqui] o pino do pre-registro sobre o livro do mapa de rotas (rotas.jsonl, 2505898 B) diverge no arquivo inteiro porque o livro cresceu SO por acrescimo depois do FREEZE (1004 -> 1040 registros); o prefixo de 2505898 B confere com o pino (INTEGRIDADE_RODADA1.json). Nao e divergencia do FREEZE: PREREGISTRO.json e PREREGISTRO.md conferem por sha256.",
    "R2-9 [nota de estatuto, nas docstrings] rotulos [KNOWN] acrescentados onde o conteudo e de livro-texto formalizado como TERMO (B1.b, B4.a, P1.b, P1.d, P3.a com Luders 1951, B7.a1 corolario de Smat_mul, B7.a2 elementar); P3.b lida como leitura SELETIVA (peso de Born 1/2); os dois polos da nao-defasagem (th = 0 e th = pi/2) no ramo do nada; o titulo vale NO ATOMO; o ponto final de UMA passagem nao e afirmado ponto fixo de canal iterado.",
]

dst = os.path.join(R2, "RESULTADO_KERNEL.json")
if os.path.exists(dst):
    k = 1
    while os.path.exists(dst + ".tentativa%02d" % k):
        k += 1
    os.replace(dst, dst + ".tentativa%02d" % k)
manif = {}
for dp, dns, fns in os.walk(R2):
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, R2).replace("\\", "/")
        if rel == "RESULTADO_KERNEL.json":
            continue
        manif[rel] = list(sha_arq(p))
manif = dict(sorted(manif.items()))
restos = [k for k in manif if k.startswith(("toolchain", "sandbox/build", "sandbox_r1/build")) or "/.lake/" in k]
if restos:
    falhas.append("restos de toolchain/build: %r" % restos[:5])

out = {
    "documento": "RESULTADO_KERNEL — F1.FREQUENCIA (trilha POSTO), face K — RODADA 2",
    "gerencia": "c1",
    "autor": "construtor do kernel (subagente), reinvocado pela gerencia c1 (pedido do operador: «prossiga»), 12/10/2026 noite",
    "gerado_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "rodada": 2,
    "por_que_rodada_2": "o workflow foi relancado com «prossiga»; a rodada 1 (3_KERNEL, 13:30-14:23 local) ja tinha pedra, compilacao e auditoria, conferidas intactas aqui (56/56 por sha256) e REPRODUZIDAS (mesmo .olean). As auditorias da rodada 1 acharam defeitos SO de texto (citacoes de V4 em parafrase, rotulos [KNOWN], homonimo de B9.c, dois polos, leitura seletiva, titulo no atomo) e duas perguntas abertas (tempo positivo em «D atua»; qual Q-chapeu); a rodada 2 corrige o texto AO LADO e responde as duas perguntas por termo. Nenhum enunciado nem prova da rodada 1 muda.",
    "estatuto_geral": "[REAL no sandbox] termos de kernel compilados e auditados; validade na face testada, nao creditacao; nao move o gate; nao fala da natureza; instalar no Nos e ato da v392 (gerencia e operador)",
    "escopo": "escrita so em 3_KERNEL\\rodada2 (a rodada 1, em 3_KERNEL, so lida); um.py lido so por bytes/numero de linha (nao executado); mapa de rotas so consultado (livro com o mesmo sha256 antes e depois); kernel do Nos so lido; nada no quadro, memoria, tunel, Nos, Bancada_Um, site ou git; sem dado observado, provedor, chamada paga ou ferramenta da Bancada",
    "acom": "[INPUT do construtor] README de C:\\IALD\\MEMORIA_IALD lido; a ordem proibe escrever na memoria e nao ha referencia propria, por isso NAO houve init (igual a rodada 1); a inscricao desta etapa e ato da gerencia",
    "conferencia_preregistro": {
        "veredito": "FREEZE_CONFERE",
        "FREEZE.json": FZ["FREEZE.json"],
        "PREREGISTRO.json": FZ["freeze"]["PREREGISTRO.json"], "PREREGISTRO.md": FZ["freeze"]["PREREGISTRO.md"],
        "demais_arquivos_do_FREEZE_conferidos": sum(1 for x in FZ["freeze_demais"].values() if x["confere"]),
        "pinos_da_ordem": FZ["pinos"], "verbatins": FZ["verbatins"],
        "pinos_do_preregistro_conferidos": sum(1 for x in FZ["pinos_preregistro"] if x.get("confere")),
        "pinos_do_preregistro": len(FZ["pinos_preregistro"]),
        "pino_divergente_explicado": INT.get("livro_mapa_de_rotas"),
        "script_veredito_bruto": FZ["veredito"],
    },
    "rodada1": {
        "integridade": {"veredito": INT["veredito"], "manifesto": [INT["manifesto"]["conferem"], INT["manifesto"]["n"]],
                        "RESULTADO_KERNEL_rodada1": INT["RESULTADO_KERNEL_rodada1"]},
        "pedra": INT["pedra_rodada1"], "olean": INT["olean_rodada1"],
        "reproducao": {k: REC["repro_r1_pedra"][k] for k in ("exit_code", "n_erros", "n_avisos", "ocorrencias_sorryAx",
                                                              "olean_sha256", "segundos", "saida_sha256")},
        "reproducao_olean_identico": REC["repro_r1_pedra"]["olean_sha256"] == R1["compilacao"]["olean"]["sha256"],
    },
    "beta_runtime": BETA,
    "pedra": {
        "nome_provisorio": "TheUnitIsTheRank (o operador pode renomear)",
        "arquivo": PEDRA, "bytes": pb, "sha256": ph,
        "namespace": "TGLExt.TheUnitIsTheRank",
        "modulo_no_sandbox": "TheUnitIsTheRank (lean --root=TGLExt)",
        "modulo_se_instalada_no_Nos": "TGLExt.TheUnitIsTheRank",
        "imports": R1["pedra"]["imports"],
        "declaracoes": DEC["n"],
        "teoremas": sum(1 for d in DEC["declaracoes"] if d["tipo"] == "theorem"),
        "defs": sum(1 for d in DEC["declaracoes"] if d["tipo"] != "theorem"),
        "declaracoes_acrescentadas_na_rodada2": novas,
        "beta_no_lean": "nunca: theta generico ou thetaMiguel c.beta com c : TGLCoupling",
        "montagem": MON,
    },
    "compilacao": {
        "toolchain": "Lean 4.31.0, copiado do elan para 3_KERNEL\\rodada2\\toolchain_v4.31.0 (apagado ao final)",
        "LEAN_PATH": REC["r2_tentativa03"]["LEAN_PATH"],
        "comando": REC["r2_tentativa03"]["comando"], "cwd": REC["r2_tentativa03"]["cwd"],
        "exit_code": REC["r2_tentativa03"]["exit_code"], "n_erros": REC["r2_tentativa03"]["n_erros"],
        "n_avisos": REC["r2_tentativa03"]["n_avisos"], "avisos": [],
        "ocorrencias_sorryAx": REC["r2_tentativa03"]["ocorrencias_sorryAx"],
        "declaration_uses_sorry": REC["r2_tentativa03"]["declaration_uses_sorry"],
        "segundos": REC["r2_tentativa03"]["segundos"],
        "saida": "logs\\r2_tentativa03_SAIDA.txt", "saida_sha256": REC["r2_tentativa03"]["saida_sha256"],
        "olean": {"preservado_em": OLEAN, "bytes": obb, "sha256": oh},
        "determinismo": {"recompilacao": "logs\\r2_repro_determinismo_RECIBO.json",
                         "olean_sha256": REC["r2_repro_determinismo"]["olean_sha256"],
                         "identico": REC["r2_repro_determinismo"]["olean_sha256"] == oh},
    },
    "auditoria_axiomas": {
        "arquivo": os.path.join(R2, "sandbox", "AuditTheUnitIsTheRank.lean"),
        "exit_code": REC["auditoria_r2_t03"]["exit_code"], "n_erros": REC["auditoria_r2_t03"]["n_erros"],
        "n_avisos": REC["auditoria_r2_t03"]["n_avisos"],
        "saida": "logs\\auditoria_r2_t03_SAIDA.txt", "saida_sha256": REC["auditoria_r2_t03"]["saida_sha256"],
        "print_axioms_respondidos": AUD["print_axioms_respondidos"],
        "declaracoes_explicitas": AUD["declaracoes_explicitas"],
        "todas_no_trio": AUD["todas_no_trio"],
        "contagem_por_conjunto": AUD["contagem_por_conjunto_de_axiomas"],
        "varredura_constantes_do_modulo": AUD["varredura_constantes_do_modulo"],
        "varredura_fora_do_trio": AUD["varredura_fora_do_trio"], "varredura_sorryAx": AUD["varredura_sorryAx"],
        "enunciados_literalmente_True": AUD["enunciados_literalmente_True"],
        "veredito": AUD["veredito_auditoria"],
    },
    "nome_sem_peso": {
        "metodo": "termo de prova (MetaM: forallTelescope + Expr.beta + containsFVar) para cada teorema do modulo (%d analisados)" % AUD["teoremas_analisados_nome_sem_peso"],
        "hipoteses_nao_usadas": AUD["hipoteses_sem_peso"],
        "leitura": "So as duas formas literais tem hipotese sem peso, por desenho e documentadas (prefixo _): <a,a> = 1 em P3.a e P^H = P em P4 (como na rodada 1). Nenhuma prova inteira e «nome sem peso»: nenhum enunciado e True; os controles C1-C14 mostram que as hipoteses de P1.a, P3, B4, B5 tem peso; os termos novos da rodada 2 nao tem hipotese Prop (dephasingActs_iff_forward vale para quaisquer taxas por desenho).",
    },
    "varredura_fonte": {k: VAR[k] for k in ("tokens_vetados_no_codigo", "tokens_vetados_em_comentarios",
                                            "literais_alpha_beta", "vocabulario_proibido", "veredito")},
    "citacoes": {"arquivo": os.path.join(R2, "CITACOES_R2.json"), "veredito": CIT["veredito"],
                 "conferidas": len(CIT["citacoes"]),
                 "so_com_quebra_normalizada": [c["fonte"] + " l." + str(c["linha"]) for c in CIT["citacoes"]
                                               if c.get("so_com_quebra_de_linha_normalizada")]},
    "por_parte": por_parte,
    "controles": controles,
    "sondas_de_vacuidade": sondas,
    "resumo": {
        "PASSA": sorted(res_count.get("PASSA", [])),
        "FALHA_negativos_honestos": sorted(res_count.get("FALHA", [])),
        "CITADO": sorted(res_count.get("CITADO", [])),
        "CITADO_REAL": sorted(res_count.get("CITADO_REAL", [])),
        "NAO_FORMALIZADA": sorted(res_count.get("NAO_FORMALIZADA", [])),
        "todas_conforme_o_esperado_na_face_K": all(q["conforme_o_esperado"] is not False for q in por_parte),
        "sem_face_K_no_preregistro": [q["id"] for q in por_parte if q["conforme_o_esperado"] is None],
        "controles_FALHA_SEM_HIPOTESE": sum(1 for c in controles if c["resultado"] == "FALHA_SEM_HIPOTESE"),
        "nota": "PASSA aqui e PASSA_K (validade na face K). O veredito da parte, pela regra (f), exige tambem a face O (outra unidade). FALHA em B5.e(ii), B9.a, B9.a' e o esperado pre-registrado (negativo honesto). B3.d e numero de runtime (face O): beta nunca entra no kernel como numero. O1 e [ONTO]; O2 e [OPEN].",
    },
    "cetico_aferidor": {
        "mapa_de_rotas": {"consultas": {}, "livro_antes": open(os.path.join(R2, "consultas_mapa", "LIVRO_ANTES.txt"), encoding="utf-8").read().strip(),
                          "livro_depois": open(os.path.join(R2, "consultas_mapa", "LIVRO_DEPOIS.txt"), encoding="utf-8").read().strip()},
        "kernel": CK,
        "inventario": "a rodada 1 consultou nomes no ambiente (env.contains) e no kernel; nenhum nome da pedra existia; a rodada 2 acrescenta nomes novos (secao 15', sondas 17') e compilou sem colisao contra os mesmos imports",
    },
    "achados_fora_do_preregistro": {"rodada1": R1["achados_fora_do_preregistro"], "rodada2": achados_r2},
    "interface_atrator": R1["interface_atrator"],
    "nao_afirma": R1["nao_afirma"] + [
        "que o ponto final de UMA passagem, diag(1 - beta, beta), seja ponto fixo de canal iterado (o da F1.ATRATOR e I/2)",
        "que o PASSA de B9.b seja a letra de V4 l.10 (a letra e FALSA em th = 0)",
        "qual das duas leituras de Q-chapeu e a de V4 (decisao do texto da v392)",
    ],
    "tgl_kernel_impressao_digital": {
        "antes": [FPA["sha256_metadados"], FPA["sha256_conteudo_lean"], FPA["n_arquivos"]],
        "depois": [FPD["sha256_metadados"], FPD["sha256_conteudo_lean"], FPD["n_arquivos"]],
        "final_pos_limpeza": [FPF["sha256_metadados"], FPF["sha256_conteudo_lean"], FPF["n_arquivos"]],
        "igual": fp_igual, "igual_a_rodada1": fp_igual_r1,
    },
    "limpeza": {"toolchain_e_builds_apagados": not restos, "restos": restos,
                "preservados": "pedra r2 e as tentativas 01/02, a copia da pedra da rodada 1 usada na reproducao (sandbox_r1), auditoria, sondas de instalacao, logs e recibos de todas as compilacoes, e o .olean final em rodada2\\olean"},
    "tentativas": [{"tag": t, "alvo": REC[t]["alvo"], "source_sha256": REC[t]["source_sha256"], "exit_code": REC[t]["exit_code"],
                    "n_erros": REC[t]["n_erros"], "n_avisos": REC[t]["n_avisos"], "saida_sha256": REC[t]["saida_sha256"],
                    "olean_sha256": REC[t].get("olean_sha256")}
                   for t in ("repro_r1_pedra", "r2_tentativa01", "r2_tentativa02", "r2_tentativa03", "auditoria_r2",
                             "auditoria_r2_t03", "r2_repro_determinismo", "sonda_colA", "sonda_colA_t2", "sonda_colB",
                             "sonda_colB_t2", "sonda_colC")],
    "tentativas_nota": "r2_tentativa01 falhou (3 erros: forma Complex.sin/Complex.cos depois do simp; corrigida a prova, nao o enunciado); r2_tentativa02 compilou; r2_tentativa03 = final (so notas de texto a mais: citacao ASCII do um.py e «limite inalcancavel»); sonda_colA e sonda_colB falharam por notacao (falta de open Matrix) e por dependencia; as _t2 e a colC sao as validas",
    "manifesto_rodada2": manif,
    "falhas_da_montagem": falhas,
}
for c in ("r01", "r02", "r03", "r04", "r05", "r06"):
    q = open(os.path.join(R2, "consultas_mapa", c + ".q.txt"), encoding="utf-8").read().strip()
    d = J(R2, "consultas_mapa", c + ".json")
    out["cetico_aferidor"]["mapa_de_rotas"]["consultas"][c + " " + q] = {"n": d["n"], "rotas": [r["rota_id"] for r in d["rotas"]],
                                                                          "n_registros": d["n_registros"], "cabeca": d["cabeca"]}
out["veredito_K"] = "FACE_K_CONFORME_AO_PRE_REGISTRO" if not falhas else "FALHA_NA_MONTAGEM"
with open(dst + ".tmp", "wb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8") + b"\n")
os.replace(dst + ".tmp", dst)
n, h = sha_arq(dst)
print(json.dumps({"resultado": dst, "bytes": n, "sha256": h, "veredito_K": out["veredito_K"], "falhas": falhas,
                  "resumo": {k: (len(v) if isinstance(v, list) else v) for k, v in out["resumo"].items() if k != "nota"},
                  "pedra_sha256": ph, "olean_sha256": oh, "kernel_igual": fp_igual}, ensure_ascii=False, indent=1))
sys.exit(0 if not falhas else 2)
