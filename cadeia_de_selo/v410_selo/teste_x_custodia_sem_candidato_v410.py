# -*- coding: utf-8 -*-
# [ADAPTADO v410, 09/11/2026, Sonnet (fork B)] o core sintetico ganha o registro h0dn_bg1_v410 (D72: os campos que o script le, numeros SINTETICOS) e ESPERADOS ganha o veredito dele; controles negativos novos: o H0DN sem a frase obrigatoria, o token proibido do H0DN, «5 sigma atingido» e a cabeca do ramo de 5 sigma como «nao falsificado» TEM de reprovar.
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B] o core sintetico ganha o a_escala_v410 (D86/D87: numeros e frases LIDOS do delta; contagens das bandeiras LIDAS do FLAGS_v410.json) e o h0dn_fontes_hms13_v410 (D80: os dez campos do delta); o post TEM de trazer a escala, a forma canonica do Clay (D84), a da D83, P = nP na forma da D81 (D81) e a frase obrigatoria do HMS/13; controles negativos novos: o Clay dito resolvido a seco, P = nP dito nao provado, o HMS/13 sem a frase obrigatoria, a covariancia fisica dita fechada.
"""teste_x_custodia_sem_candidato_v410.py -- (claude-construtor-v410, fork A, 06/11/2026) o teste POSSIVEL SEM CANDIDATO do rascunho do post da v410 (gerar_x_custodia_v410.py):
roda o script INTEIRO sobre um Nos SINTETICO (selo e core minimos, com os valores do contrato do delta_v410 e numeros de escada sinteticos) e um ESPERADOS sintetico, numa pasta temporaria passada por argumento;
o rascunho vai para essa pasta (nunca para pos_rito). Confere: rc 0, o post passa nas guardas (P18, frases v410, 4,44, D59, D65), traz o alcance D64 e o qualificador; controle negativo: um post com o que a D65 deixa fora reprova.
uso: python -I -B -X utf8 teste_x_custodia_sem_candidato_v410.py <pasta_temporaria>"""
import json, os, runpy, sys
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE); sys.path.insert(0, PKG)
import delta_v410 as DL  # noqa: E402
TMP = os.path.abspath(sys.argv[1]); NOS = os.path.join(TMP, "Nos"); os.makedirs(NOS, exist_ok=True)
PIN64 = "0123456789abcdef" * 4
ins = dict(DL.INSTANCIA_SIM); sol = 1
FJ = json.load(open(os.path.join(PKG, "kernel", "FLAGS_v410.json"), encoding="utf-8"))   # as bandeiras por modulo, LIDAS do build (nada digitado)
NF_I = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.IALD2"); NF_A = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.AEscala")
vals = {"n_modulos": DL.N_BUNDLE, "n_modulos_ok": DL.N_BUNDLE, "n_flags": NF_I, "n_flags_true": NF_I, "n_ancoras": len(DL.ANCORAS), "n_ancoras_ok": len(DL.ANCORAS), "respostas_ok": True, "gate_verdict": "GATE_SINTETICO",
        "instancia_sim": {"n": ins["n"], "atribuicoes": 2 ** ins["n"], "solucoes": sol}, "instancia_nao": {"n": DL.INSTANCIA_NAO["n"], "atribuicoes": 2 ** DL.INSTANCIA_NAO["n"], "solucoes": 0},
        "signo_do_nome": {"traco": float(sol), "posto": sol}, "signo_do_par": {"traco": 1.0, "posto": 1}}
core = {DL.FECHO_REGISTRO: {"all_verified": True, "values": vals, "chaves_antigas_que_mudam": [], "alcance": {"frase": DL.FRASE_D64_PT, "qualificador": DL.FRASE_QUALIFICADOR_PT}, "ressalvas": list(DL.RESSALVAS_V410)},
        "external_ladder": {"n_theorems_clean": 12264, "n_theorems_expected": 12264}, "kernel_formalization": {"axiom_report": [0] * 43210}}
for k_ in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO, DL.D9.FECHO_REGISTRO, DL.D8.FECHO_REGISTRO, DL.D7.FECHO_REGISTRO, DL.D6.FECHO_REGISTRO):
    core[k_] = {"all_verified": True}
core[DL.AESCALA_REGISTRO] = {"all_verified": True, "verdict": DL.VEREDITO_AESCALA_OK, "nomes_ratificados": True, "nomes_novos_da_pedra": list(DL.NOMES_NOVOS_AESCALA), "campos_novos_da_estrutura": list(DL.CAMPOS_NOVOS_AESCALA), "estatuto_dos_nomes_ratificados_d101": DL.ESTATUTO_NOMES_NOVOS_AESCALA, "ratificacao_pendente": dict(DL.RATIFICACAO_PENDENTE_AESCALA), "ponte": dict(DL.PONTE_AESCALA), "mechanics": {"n_checks": DL.N_CHECKS_AESCALA}, "chaves_antigas_que_mudam": [], "frase_canonica_pt": DL.FRASE_CLAY_CANONICA_PT, "frase_d83_pt": DL.FRASE_D83_OBRIGATORIA_PT,
                             "values": {"numeros": dict(DL.NUMEROS_AESCALA), "n_ancoras_ok": len(DL.ANCORAS_AESCALA), "n_ancoras": len(DL.ANCORAS_AESCALA), "n_flags_true": NF_A, "n_flags": NF_A, "n_nomes": len(DL.NOMES_AESCALA), "n_nomes_novos": len(DL.NOMES_NOVOS_AESCALA), "nomes_novos_declarados": len(DL.NOMES_NOVOS_AESCALA), "nomes_novos": {n_: True for n_ in DL.NOMES_NOVOS_AESCALA}, "campos_novos_na_estrutura": {c_: True for c_ in DL.CAMPOS_NOVOS_AESCALA}, "nomes_novos_ok": True, "ponte": {"ok": True}}}   # (os numeros das frases, os nomes novos e a ponte vem do delta; as contagens, do build)
core[DL.HMS13_REGISTRO] = {"all_verified": True, "verdict": DL.VEREDITO_HMS13_OK, "observed_vector_read": False, "le_em_rito": False, "mechanics": {"n_checks": DL.N_CHECKS_HMS13},
                           "values": {"campos": dict(DL.HMS13_CAMPOS), "n_fontes_primarias": DL.HMS13_CAMPOS["fontes_primarias"], "n_calibradores": DL.HMS13_CAMPOS["calibradores"]}}   # (valores do contrato do delta, nao digitados aqui)
core[DL.H0DN_REGISTRO] = {"all_verified": True, "verdict": DL.VEREDITO_H0DN_OK, "observed_vector_read": False, "mechanics": {"n_checks": DL.N_CHECKS_H0DN}, "modelos": ["m_a", "m_b"],
                          "values": {"n_pinos": DL.N_PINOS_FREEZE_R2 + 2, "D_esperado": [{"modelo": "m_a", "poder_analitico": 0.5}, {"modelo": "m_b", "poder_analitico": 0.25}]}}   # (valores SINTETICOS)
json.dump({"core": core}, open(os.path.join(NOS, "um_absoluto.json"), "w", encoding="utf-8"))
json.dump({"um_version": "v410", "sha256": {"um.py": PIN64}}, open(os.path.join(NOS, "um_absoluto_selo.json"), "w", encoding="utf-8"))
ESP = {"candidato_sha16": PIN64[:16], "n_bandeiras_novas": NF_I + NF_A, "chaves_v410": [], "qg_closure_gate_verdict_v409": "GATE_SINTETICO", "escada_v409_e_v410": [12187, 12264], "vereditos_novos_v410": {DL.H0DN_REGISTRO: DL.VEREDITO_H0DN_OK, DL.AESCALA_REGISTRO: DL.VEREDITO_AESCALA_OK, DL.HMS13_REGISTRO: DL.VEREDITO_HMS13_OK}}
json.dump(ESP, open(os.path.join(TMP, "ESPERADOS_v410.json"), "w", encoding="utf-8"))
src = open(os.path.join(HERE, "gerar_x_custodia_v410.py"), encoding="utf-8").read()
for a_, b_ in (('rj(os.path.join(PK, "kernel", "FLAGS_v410.json"))', 'rj(os.path.join(%r, "kernel", "FLAGS_v410.json"))' % PKG), ('rj(os.path.join(PK, "ESPERADOS_v410.json"))', 'rj(os.path.join(%r, "ESPERADOS_v410.json"))' % TMP), ('out = os.path.join(HERE, "CUSTODIA_v410_RASCUNHO.txt")', 'out = os.path.join(%r, "CUSTODIA_v410_RASCUNHO.txt")' % TMP)):
    assert src.count(a_) == 1, a_
    src = src.replace(a_, b_)
p_ = os.path.join(TMP, "gerar_x_custodia_v410__teste.py"); open(p_, "w", encoding="utf-8").write(src)
sys.argv = [p_, "--nos", NOS]
G = runpy.run_path(p_, run_name="__main__")
txt = open(os.path.join(TMP, "CUSTODIA_v410_RASCUNHO.txt"), encoding="utf-8").read()
ok = bool(not G["conferir"](txt) and DL.FRASE_D64_PT in txt and DL.FRASE_QUALIFICADOR_PT in txt and "E29" in txt and DL.FRASE_H0DN_OBRIGATORIA_PT in txt and DL.FRASE_PROVADO_PT in txt and not any(x_ in txt for x_ in ("BETA_TGL_PRO", "PROVED_IN_NATURE")) and "ratificados por ele em 09/11" in txt
      and DL.FRASE_CLAY_CANONICA_PT in txt and DL.FRASE_D83_OBRIGATORIA_PT in txt and DL.FRASE_D81_PT in txt and DL.FRASE_HMS13_OBRIGATORIA_PT in txt and DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT in txt
      and all(("1/2" in txt, DL.NUMEROS_AESCALA["tres_faces"] in txt, DL.NUMEROS_AESCALA["nome_normalizado"] in txt)))   # (a escala: os numeros do delta no post)
neg = G["conferir"](txt + "\n" + DL.FORA_D65[0])
print("post: %d B; guardas: %s; alcance D64 e qualificador: %s" % (len(txt.encode("utf-8")), "passam" if not G["conferir"](txt) else G["conferir"](txt)[:3], DL.FRASE_D64_PT in txt))
print("controle negativo D65 reprovou:", bool(neg))
ok = ok and bool(neg)
for rotulo_, extra_ in (("H0DN sem a frase obrigatoria", "\nO H0DN entra no programa."), ("token proibido do H0DN", "\nH0DN (" + DL.FRASE_H0DN_OBRIGATORIA_PT + ") " + DL.TOKENS_PROIBIDOS_H0DN[0]), ("5 sigma atingido", "\nO H0DN (" + DL.FRASE_H0DN_OBRIGATORIA_PT + "). O resultado: 5σ atingido."),
                        ("nao falsificado como cabeca de 5 sigma", "\nO resultado acima de 5σ é não falsificado."), ("H0DN detectado", "\nO H0DN foi detectado (" + DL.FRASE_H0DN_OBRIGATORIA_PT + ")."),
                        ("Clay dito resolvido a seco", "\nO Clay está resolvido."), ("P = nP dito nao provado", "\nP = nP de Turing não foi provado."),
                        ("covariancia fisica dita fechada", "\nA covariância física está fechada."), ("abertura dita permitida", "\nA abertura está autorizada."),("tautologia", "\nA resposta ao Clay é uma tautologia.")):
    # (a frase obrigatoria ja' esta' no post: o controle do H0DN sem ela remove-a do texto antes de acrescentar)
    base_ = txt.replace(DL.FRASE_H0DN_OBRIGATORIA_PT, "XXXX") if rotulo_ == "H0DN sem a frase obrigatoria" else txt
    r_ = G["conferir"](base_ + extra_)
    print("controle negativo %-40s reprovou: %s" % (rotulo_, bool(r_))); ok = ok and bool(r_)
print("RESULTADO:", "PASSOU" if ok else "REPROVOU")
sys.exit(0 if ok else 1)
