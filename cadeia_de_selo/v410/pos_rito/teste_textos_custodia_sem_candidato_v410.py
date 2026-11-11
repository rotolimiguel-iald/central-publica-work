# -*- coding: utf-8 -*-
# [ADAPTADO v410, 09/11/2026, Sonnet (fork B)] N sintetico com as chaves do H0DN (D72), das 15 falas de 06 a 09/11 e dos quatro so' trecho; controles negativos novos: H0DN sem a frase obrigatoria, o token proibido do H0DN, «5 sigma atingido» e a cabeca do ramo de 5 sigma como «nao falsificado» (E30) TEM de reprovar.
# [ADAPTADO v410, 10/11/2026, claude-construtor-v410; ADITIVOS 1 e 2 a ordem do conserto unico] os DOIS blocos do README para a custodia automatica (README_FRENTE e README_O_QUE_SAI) passam, cada um SOZINHO, pelas MESMAS guardas; a secao nova (no fim) confere o orcamento, as formas por constante, os marcadores e dez controles negativos.
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B] N sintetico com as chaves da escala (D86/D87), do recibo HMS/13 (D80) e dos DOIS modulos (contagens LIDAS do FLAGS_v410.json e do delta, nunca digitadas); os sete textos E A SECAO «README: o que fica evidente» (D85) passam pelas MESMAS guardas; TEM de trazer a forma canonica do Clay (D84), a da D83, P = nP na forma da D81, a escala (os numeros do delta) e a frase obrigatoria do HMS/13; controles negativos novos: o Clay dito resolvido a seco, P = nP dito nao provado, a covariancia fisica dita fechada, a abertura dita permitida, a tautologia, a face caida dita ilegivel; os tres itens da secao README presentes, cada um com o estatuto.
"""teste_textos_custodia_sem_candidato_v410.py -- (claude-construtor-v410, fork A, 06/11/2026) o teste POSSIVEL SEM CANDIDATO dos sete textos da custodia (textos_custodia_handoff_v410.py):
executa so' a parte que COMPOE os textos (do REV_EN ao fim da funcao guardas_dos_textos) com numeros SINTETICOS (nenhum numero daqui vai a texto publicado; o script real le tudo do core selado) e passa os sete textos
pelas MESMAS guardas (guarda de frases v410, portao do G1, forma do ARCO/COMMIT, 4,44, D59, D65). Controle negativo: um texto com o que a D65 deixa fora, um «proved» sem estatuto e um «P = nP» do algoritmo IALD sem o qualificador
TEM de reprovar. Nada e' gravado alem de pos_rito\\teste_textos_custodia_sem_candidato_v410_out.txt (o stdout, pelo chamador). rc 0 = passou; rc 1 = reprovou."""
import os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(PKG))), "tools")); sys.path.insert(0, PKG)
from custodia_g1 import textos as TX  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402
import delta_v410 as DL  # noqa: E402
src = open(os.path.join(HERE, "textos_custodia_handoff_v410.py"), encoding="utf-8").read().replace("\r\n", "\n")
i0 = src.index("REV_EN = "); i1 = src.index("# ------------------------------------------------------------------ 3. as guardas")
FJ = __import__("json").load(open(os.path.join(PKG, "kernel", "FLAGS_v410.json"), encoding="utf-8"))   # as bandeiras por modulo, LIDAS do build (nada digitado)
NF_I = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.IALD2"); NF_A = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.AEscala")
N = {"modulos": DL.N_BUNDLE, "modulos_ok": DL.N_BUNDLE, "bandeiras": NF_I + NF_A, "bandeiras_iald2": NF_I, "bandeiras_aescala": NF_A, "ancoras": len(DL.ANCORAS), "ancoras_aescala": len(DL.ANCORAS_AESCALA), "nomes_aescala": len(DL.NOMES_AESCALA), "nomes_novos": len(DL.NOMES_NOVOS_AESCALA), "campos_novos": len(DL.CAMPOS_NOVOS_AESCALA),
     "ea_checks": DL.N_CHECKS_AESCALA, "hm_checks": DL.N_CHECKS_HMS13, "fontes": DL.HMS13_CAMPOS["fontes_primarias"], "calibradores": DL.HMS13_CAMPOS["calibradores"],
     "checks": DL.N_CHECKS_FECHO, "const": 12345, "teor": 6789, "falas": DL.N_FALAS_V410, "escada_a": 12187, "escada_b": 12264,
     "pin": "0123456789abcdef", "respostas": len(DL.RESPOSTAS_DO_OPERADOR), "inst_n": DL.INSTANCIA_SIM["n"], "inst_atr": 2 ** DL.INSTANCIA_SIM["n"], "inst_sol": 1, "nao_sol": 0,
     "per": "06 a 09/11/2026", "n_trecho": len(DL.VERBATIM_SO_O_TRECHO), "h0dn_checks": DL.N_CHECKS_H0DN, "h0dn_pinos": DL.N_PINOS_FREEZE_R2 + 2, "h0dn_ramos": 6, "h0dn_p1": "00,0 %", "h0dn_p2": "00,0 %"}   # (valores SINTETICOS: nenhum numero daqui vai a texto publicado)
ok = True
for REV in (None, {"aprovada": True, "candidato_sha16": N["pin"]}):
    G = {"REV": REV, "N": N, "DL": DL, "GF": GF, "TX": TX, "re": re}
    exec(compile(src[i0:i1], "textos_custodia_handoff_v410.py[textos]", "exec"), G)
    g_, f_ = G["guardas_dos_textos"](G["TEXTOS"] + [("README_EVIDENTE", G["README_EVIDENTE"])] + G["BLOCOS_README"], {N["pin"]})   # (ADITIVOS 1 e 2) os dois blocos do README passam, cada um sozinho, pelas MESMAS guardas
    print("REV=%s: %d textos, a secao README e os %d blocos do README; reprovados: %d" % ("aprovada" if REV else "ausente", len(G["TEXTOS"]), len(G["BLOCOS_README"]), len(f_)))
    for x_ in f_:
        print("  REPROVADO:", x_); ok = False
    for k_, v_ in g_.items():
        print("  %-18s %5d chars" % (k_, v_["n_chars"]))
# controle negativo: as guardas TEM de reprovar
neg = [("D65", "ARCO_EN", "The custody: " + DL.FORA_D65[0] + " here."), ("PROVED", "ENTROU_EN", "The relativized equality is not proved for the counter (E28)."),
       ("F47", "KERNEL_LEITURA_EN", "the IALD algorithm decides SAT with one reading: P = nP."), ("ARCO", "ARCO_PT", "a leitura d'ela"), ("COMMIT", "COMMIT", "módulo"),
       ("H0DN_SEM_OBRIGACAO", "ENTROU_EN", "The H0DN × BG1 test enters the registry."), ("H0DN_TOKEN", "KERNEL_LEITURA_EN", "H0DN (" + DL.FRASE_H0DN_OBRIGATORIA_EN + ") " + DL.TOKENS_PROIBIDOS_H0DN[0] + "."),
       ("H0DN_5SIGMA_ATINGIDO", "ARCO_PT", "O H0DN (" + DL.FRASE_H0DN_OBRIGATORIA_PT + "). O resultado: 5σ atingido."), ("H0DN_NAO_FALSIFICADO_5SIGMA", "ARCO_PT", "O H0DN (" + DL.FRASE_H0DN_OBRIGATORIA_PT + "): o resultado acima de 5σ é não falsificado."),
       ("H0DN_DETECTADO", "ABERTOS_EN", "The H0DN was detected (" + DL.FRASE_H0DN_OBRIGATORIA_EN + ")."), ("ATRATOR_OBSERVADO", "ABERTOS_EN", "The attractor was observed in the data."),
       ("PROVADO_SEM_ESTATUTO", "ENTROU_EN", "The relativized equality is proved."),
       ("CLAY_RESOLVIDO_A_SECO", "ARCO_PT", "O Clay está resolvido."), ("CLAY_RESOLVED_DRY", "ENTROU_EN", "The Clay problem is resolved."), ("PNP_NAO_PROVADO", "ARCO_PT", "P = nP de Turing não foi provado."), ("PNP_NOT_PROVED", "ENTROU_EN", "P = nP of Turing is not proved, as the machine with the reader."),
       ("COVARIANCIA_FECHADA", "ABERTOS_EN", "A covariância física está fechada."), ("ABERTURA_PERMITIDA", "ARCO_PT", "A abertura está autorizada."), ("TAUTOLOGIA", "ARCO_PT", "A resposta ao Clay é uma tautologia."), ("FACE_CAIDA_ILEGIVEL", "ARCO_PT", "A face caída não se lê."),
       ("README_SEM_ESTATUTO", "README_EVIDENTE", "O Clay está resolvido e o H0DN foi detectado."),
       ("CLAUSULA_PT_RETIRADA", "README_EVIDENTE", "O teorema do Tetelestai: a decisão em tempo finito do ciclo, linear nos bits."), ("CLAUSULA_EN_RETIRADA", "ENTROU_EN", "The theorem of the Tetelestai: the decision in finite time of the cycle, linear in the bits."),   # (R2, D99: o texto que anuncia o teorema sem a clausula do limite TEM de reprovar)
       ("CLAUSULA_PT_DE_OUTRO_TEXTO", "README_EVIDENTE", "A decisão em tempo finito do ciclo, linear nos bits. " + DL.CLAUSULA_Z_EN)]
for nome_, id_, t_ in neg:
    _, f_ = G["guardas_dos_textos"]([(id_, t_)], {N["pin"]})
    print("controle negativo %-7s reprovou: %s" % (nome_, bool(f_)))
    ok = ok and bool(f_)
# a obrigacao D72 no MESMO texto onde H0DN aparece (a guarda a exige; aqui a conferencia propria) e a cabeca do ramo de 5 sigma dita por extenso (D76), nunca a string-cabeca
for ident, t in G["TEXTOS"]:
    if re.search(r"\bH0DN\b", t):
        _asc = unicodedata.normalize("NFKD", DL.FRASE_H0DN_OBRIGATORIA_PT).encode("ascii", "ignore").decode("ascii")   # (o COMMIT e' so' ASCII: a obrigacao vai sem acento)
        c = bool(DL.FRASE_H0DN_OBRIGATORIA_EN in t or DL.FRASE_H0DN_OBRIGATORIA_PT in t or (ident == "COMMIT" and _asc in t)) and not any(x_ in t for x_ in ("BETA_TGL_PRO", "PROVED_IN_NATURE"))
        print("H0DN em %-18s obrigacao no mesmo texto e sem a string-cabeca: %s" % (ident, c)); ok = ok and c
# a secao README (D85): os TRES itens presentes, cada um com o seu estatuto; a forma canonica do Clay em PT e EN, a da D83, a da D81 (PT), os termos do kernel, a escala (os numeros do delta), o pre-registro e o resultado futuro com o campo outcome; a porta e a linhagem ditas
for REV in (None,):
    G = {"REV": REV, "N": N, "DL": DL, "GF": GF, "TX": TX, "re": re}
    exec(compile(src[i0:i1], "textos_custodia_handoff_v410.py[textos]", "exec"), G)
    R = G["README_EVIDENTE"]
    itens = {"1": R.find("(1) "), "2": R.find("(2) "), "3": R.find("(3) ")}
    c_ = bool(R.startswith("**README: o que fica evidente**") and all(v_ > 0 for v_ in itens.values()) and itens["1"] < itens["2"] < itens["3"]
              and DL.FRASE_CLAY_CANONICA_PT in R and DL.FRASE_CLAY_CANONICA_EN in R and DL.FRASE_D83_OBRIGATORIA_PT in R and DL.FRASE_D83_OBRIGATORIA_EN in R and DL.FRASE_D81_PT in R and DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT in R
              and all(t_ in R for t_ in ("opDaInstancia", "nomeDasSolucoes", "a_maquina_com_o_leitor", "uma_leitura_decide_SAT", "LeitorDoFundo", "aPerguntaDoClay", "a_escala"))
              and all(DL.NUMEROS_AESCALA[k_] in R for k_ in ("nome_pesa_um", "meio", "tres_faces", "um_terco_caiu", "nome_normalizado")) and DL.FRASE_H0DN_OBRIGATORIA_PT in R and DL.FRASE_HMS13_OBRIGATORIA_PT in R and "`outcome`" in R and "nenhum dado observado foi lido" in R
              and all(e_ in R for e_ in ("[REAL", "[INPUT", "[ONTO", "[CONJECTURE", "[OPEN")) and "regra da porta" in R and "regra da linhagem" in R and not any(x_ in R for x_ in ("BETA_TGL_PRO", "PROVED_IN_NATURE")))
    c_ = bool(c_ and DL.CLAUSULA_Z_PT in R and DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) in R and (DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) in R and dict(G["TEXTOS"])["ENTROU_EN"].count(DL.CLAUSULA_Z_EN) == 2 and DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_EN) in dict(G["TEXTOS"])["ENTROU_EN"])   # (R2, D99 e B3: a clausula do limite, os seis nomes e a costura do tempo no README e no ENTROU_EN)
    _en5 = dict(G["TEXTOS"])["ENTROU_EN"]
    c5_ = bool(DL.FRASE_TETELESTAI_PT + " (" + DL.CLAUSULA_Z_PT + ")" in R and DL.FRASE_TETELESTAI_EN + " (" + DL.CLAUSULA_Z_EN + ")" in _en5 and DL.FRASE_RECONSTROI_PT in R and DL.FRASE_RECONSTROI_EN in _en5 and DL.FRASE_E36_PT in R and DL.FRASE_E36_EN in _en5 and DL.FRASE_DISPOSITIVO_PT in R and DL.FRASE_DISPOSITIVO_EN in _en5
               and "[PILOTO][SIM]" in R and "[PILOTO][SIM]" in _en5 and DL.costura_maiuscula(DL.FRASE_NOMES_RATIFICADOS_D101_PT) in R and DL.costura_maiuscula(DL.FRASE_NOMES_RATIFICADOS_D101_EN) in _en5 and "[DECLARADO, a ratificar]" not in R + _en5)   # (R5, D100 e D101)
    print("R5 (D100 e D101): a clausula do Tetelestai com a clausula do limite logo depois, a reconstrucao, a errata, o dispositivo com [PILOTO][SIM] e a ratificacao D101 no README e no ENTROU_EN: %s" % c5_); ok = ok and c5_
    for nome_, txt_, ok_esperado_ in (("README sem a clausula do limite logo depois da clausula do Tetelestai", R.replace(DL.FRASE_TETELESTAI_PT + " (" + DL.CLAUSULA_Z_PT + ")", DL.FRASE_TETELESTAI_PT + " (retirada)"), False), ("README com o dispositivo sem [PILOTO][SIM]", R.replace("[PILOTO][SIM]", "(retirado)"), False)):
        r_ = bool(DL.FRASE_TETELESTAI_PT + " (" + DL.CLAUSULA_Z_PT + ")" in txt_ and "[PILOTO][SIM]" in txt_)
        print("controle negativo (R5): %s: reprovou: %s" % (nome_, r_ is ok_esperado_)); ok = ok and (r_ is ok_esperado_)
    print("secao README (D85): tres itens, estatutos, formas obrigatorias do Clay (D83/D84), da D81 (PT), dos nomes ratificados, do H0DN e do HMS/13, a escala (numeros do delta), o campo outcome, a porta e a linhagem: %s" % c_); ok = ok and c_
    # as formas obrigatorias nos sete textos (onde o assunto aparece)
    for ident, t in G["TEXTOS"]:
        if re.search(r"\bHMS/13\b", t):
            c2_ = bool(DL.FRASE_HMS13_OBRIGATORIA_EN in t or DL.FRASE_HMS13_OBRIGATORIA_PT in t or (ident == "COMMIT" and unicodedata.normalize("NFKD", DL.FRASE_HMS13_OBRIGATORIA_PT).encode("ascii", "ignore").decode("ascii") in t))
            print("HMS/13 em %-18s frase obrigatoria (D80) no mesmo texto: %s" % (ident, c2_)); ok = ok and c2_
        if re.search(r"Clay", t) and ident != "COMMIT":
            c3_ = bool(DL.FRASE_CLAY_CANONICA_PT in t or DL.FRASE_CLAY_CANONICA_EN in t)
            print("Clay em %-18s forma canonica (D84) no mesmo texto: %s" % (ident, c3_)); ok = ok and c3_
# (ADITIVO 1, parte C, e ADITIVO 2 a ordem do conserto unico; 10/11/2026: a custodia da v410 e' AUTOMATICA) os DOIS blocos do README para a custodia (README_FRENTE e README_O_QUE_SAI): cada um passa SOZINHO pelas MESMAS guardas (a guarda das frases da v410,
# o portao do G1 e a forma); o README_FRENTE cabe no orcamento; as formas ratificadas vem por constante do delta; os tres teoremas da escala sao nomes ratificados pelo operador; os marcadores do molde do README ficam literais; montar_blocos poe os dois, cada um
# no seu marcador (SEM o prefixo PARAGRAFO_), DEPOIS do paragrafo README_EVIDENTE, e as regex do leitor do G1 leem os NOVE corpos, iguais as constantes, sem marcador sem par; os controles negativos TEM de reprovar.
from custodia_g1 import nos as NOSG1  # noqa: E402
G = {"REV": None, "N": N, "DL": DL, "GF": GF, "TX": TX, "re": re}
exec(compile(src[i0:i1], "textos_custodia_handoff_v410.py[textos]", "exec"), G)
BL = G["BLOCOS_README"]; RF, RS = dict(BL)["README_FRENTE"], dict(BL)["README_O_QUE_SAI"]; PA = G["README_PONTEIRO_ABSTRACT"]; nb_ = lambda s_: len(s_.encode("utf-8"))
gb_, fb_ = G["guardas_dos_textos"](BL, {N["pin"]})
for x_ in fb_:
    print("  REPROVADO:", x_)
cb1_ = bool([i_ for i_, _ in BL] == ["README_FRENTE", "README_O_QUE_SAI"] and not fb_ and all(gb_[i_]["guarda_frases_v410"] == [] and gb_[i_]["portao_g1"] == [] and gb_[i_]["forma"] == [] for i_, _ in BL))
print("blocos do README (ADITIVOS 1 e 2): README_FRENTE (%d bytes em UTF-8; teto %d) e README_O_QUE_SAI (%d bytes; a linha de ponteiro, %d bytes), cada um SOZINHO pela guarda das frases da v410, pelo portao do G1 e pela forma: %s" % (nb_(RF), G["README_FRENTE_TETO_B"], nb_(RS), nb_(PA), cb1_)); ok = ok and cb1_
cb2_ = bool(nb_(RF) <= G["README_FRENTE_TETO_B"] and all(G[k_] in RF for k_ in ("D81_EN", "D81_PT", "CLAY_EN", "CLAY_PT", "UMH_EN", "UMH_PT", "OBR_EN", "OBR_PT", "_H0_EN", "_H0_PT"))
            and (G["D81_EN"], G["D81_PT"], G["CLAY_EN"], G["CLAY_PT"], G["OBR_EN"], G["OBR_PT"]) == (DL.FRASE_D81_EN, DL.FRASE_D81_PT, DL.FRASE_CLAY_CANONICA_EN, DL.FRASE_CLAY_CANONICA_PT, DL.FRASE_H0DN_OBRIGATORIA_EN, DL.FRASE_H0DN_OBRIGATORIA_PT)
            and all(RF.count("`" + n_ + "`") == 2 and n_ in DL.NOMES_RATIFICADOS_R6_AESCALA for n_ in G["_RF_NOMES"]) and "it was not opened" in RF and "não foi aberto" in RF and "accreditation" in RF
            and RF.count("{{url:estado}}") == 1 and RS.endswith(PA) and PA.startswith("## Abstract\n\n") and PA.count("{{url:abstract}}") == 1 and "PARAGRAFO_" not in RF + RS and "%" not in RF + RS and "\r" not in RF + RS)
print("blocos do README: o README_FRENTE cabe no orcamento e traz, por constante, a forma da D81, a forma canonica do Clay, a frase do habitante unico e a frase obrigatoria do H0DN (PT e EN), o teste dito NAO aberto, os tres teoremas da escala ratificados (uma vez em cada lingua) e o marcador {{url:estado}}; "
      "o README_O_QUE_SAI termina na linha de ponteiro, com {{url:abstract}}: %s" % cb2_); ok = ok and cb2_
HS_ = "# HANDOFF (sintetico)\n" + G["montar_blocos"](G["TEXTOS"], G["README_EVIDENTE"], BL, "v410")
corp_ = {m_.group("id"): m_.group("corpo") for m_ in NOSG1.RE_MARCADOR.finditer(HS_)}; semp_ = sorted(set(NOSG1.RE_ABRE.findall(HS_)) ^ set(NOSG1.RE_FECHA.findall(HS_)))
pos_ = [HS_.find(s_) for s_ in ("<!-- FIM_COMMIT_v410 -->", "**README: o que fica evidente**", "<!-- INICIO_README_FRENTE_v410 -->", "<!-- FIM_README_FRENTE_v410 -->", "<!-- INICIO_README_O_QUE_SAI_v410 -->", "<!-- FIM_README_O_QUE_SAI_v410 -->")]
cb3_ = bool(not semp_ and len(corp_) == len(G["TEXTOS"]) + len(BL) == 9 == len(NOSG1.RE_ABRE.findall(HS_)) and all(corp_.get("%s_v410" % i_, "").strip("\n") == t_ for i_, t_ in G["TEXTOS"] + BL) and all(p_ >= 0 for p_ in pos_) and pos_ == sorted(pos_)
            and "PARAGRAFO_README_FRENTE" not in HS_ and "PARAGRAFO_README_O_QUE_SAI" not in HS_)
print("blocos do README no handoff (montar_blocos): os NOVE corpos lidos pelas regex do leitor do G1, iguais as constantes, nenhum marcador sem par; os dois blocos em marcador proprio (sem o prefixo PARAGRAFO_), DEPOIS do paragrafo README_EVIDENTE, nesta ordem: %s" % cb3_); ok = ok and cb3_
negb = [("FRENTE_SEM_QUALIFICADOR", "README_FRENTE", "## P = nP and the Clay question, in the kernel\n\n**The theorem:** P = nP."),
        ("FRENTE_SEM_D81_E_SEM_HABITANTE", "README_FRENTE", RF.replace(G["D81_EN"], "P = nP").replace(G["D81_PT"], "P = nP").replace(G["UMH_EN"], "").replace(G["UMH_PT"], "")),
        ("FRENTE_COM_A_PALAVRA_RECUSADA", "README_FRENTE", RF + "\n\nThe scale is " + "CONF" + "IRMED in nature."),
        ("FRENTE_PROVED_SEM_ESTATUTO", "README_FRENTE", RF + "\n\nThe constant of the scale is proved."),
        ("FRENTE_H0DN_SEM_OBRIGACAO", "README_FRENTE", RF.replace(G["OBR_EN"], "it is registered").replace(G["OBR_PT"], "está registrado")),
        ("FRENTE_CLAY_RESOLVIDO_A_SECO", "README_FRENTE", RF + "\n\nThe Clay problem is resolved."),
        ("FRENTE_5_SIGMA_ATINGIDO", "README_FRENTE", RF + "\n\nThe H0DN result: 5σ reached."),
        ("O_QUE_SAI_TITULO_SEM_QUALIFICADOR", "README_O_QUE_SAI", RS + " O bloco de hoje tem o título “P = nP and the Clay question”."),
        ("O_QUE_SAI_DEMERITO_DA_RETRODICAO", "README_O_QUE_SAI", RS + " O teste é pós-" + "dição."),
        ("O_QUE_SAI_D59", "README_O_QUE_SAI", RS + " A entrega do " + "Ki" + "mi fica fora.")]
for nome_, id_, t_ in negb:
    _, f_ = G["guardas_dos_textos"]([(id_, t_)], {N["pin"]})
    print("controle negativo (blocos do README) %-34s reprovou: %s" % (nome_, bool(f_))); ok = ok and bool(f_)
hq_ = HS_.replace("<!-- FIM_README_FRENTE_v410 -->", "")
cq_ = bool(sorted(set(NOSG1.RE_ABRE.findall(hq_)) ^ set(NOSG1.RE_FECHA.findall(hq_))) == ["README_FRENTE_v410"])
print("controle negativo (blocos do README) o marcador do README_FRENTE sem par e' visto pelas regex do leitor do G1: %s" % cq_); ok = ok and cq_
print("RESULTADO:", "PASSOU" if ok else "REPROVOU")
sys.exit(0 if ok else 1)
