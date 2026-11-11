# -*- coding: utf-8 -*-
# [ADAPTADO v410, 09/11/2026, claude-sonnet (fork C do pos-rito)] para o DESENHO_v410 e os AO LADO de 09/11: as 15 anotacoes (a do atrator, secao 6, e a do H0DN, D72), a regra D59 com o Kimi so' no contexto do H0DN (M.d59_viola), os controles negativos do H0DN e as funcoes puras h0dn_do_core/h0dn_textos rodadas com um registro SINTETICO.
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B] as 16 anotacoes (a da pedra AEscala, R_AESCALA, e a do H0DN com o recibo documental HMS/13, D80); os seq da candidata (1926) e da errata textual (1927) da rota da AEscala LIDOS do livro; as funcoes puras escala_do_core/escala_textos e hms13_do_core/hms13_textos rodadas com registros SINTETICOS, com controles negativos (a escala sem nomes ratificados, numeros diferentes do delta, a frase canonica do Clay trocada, o recibo com vetor observado lido ou entrega aberta em rito, o ESPERADOS sem os registros); a obrigacao D80 (a frase do HMS/13 onde o recibo for dito) e a forma canonica do Clay onde for dito resolvido, com controles negativos de texto.
"""teste_mapa_sem_candidato_v410.py -- (claude-construtor-v410, fork A, 06/11/2026; adaptado em 09/11/2026) o teste POSSIVEL SEM CANDIDATO do registrar_mapa_v410.py (so' leitura do livro do mapa):
(1) todas as rotas anotadas e citadas em refs existem no livro (inclusive a do atrator, seq 1920, e a da ORDEM ao Kimi do H0DN, seq 1921) e a nova (umpy.v410.selada_iald2_06nov) nao existe; (2) o seq que a E29 corrige e' lido do livro (a rota kernel.iald2_06nov traz «matricial» como leitura do operador);
(3) os titulos das anotacoes (com um pino sintetico) passam na guarda P18, na guarda das frases v410 (inclusive a F41b: Fock e v41x no mesmo trecho, e a F54: o titulo que traz H0DN traz «pré-registrado; nenhum dado observado lido»), na D59 (o Kimi so' no contexto do H0DN) e na D65;
(4) as funcoes puras h0dn_do_core e h0dn_textos rodam sobre um registro h0dn_bg1_v410 SINTETICO (numeros de brinquedo, que nao vao a texto publicado): o texto passa nas guardas, nao traz a cabeca do ramo de 5 sigma por extenso, nem o agregado publico, nem token proibido; e os CONTROLES NEGATIVOS TEM de reprovar
(vetor observado lido, registro ausente, checagem que falha, pino que nao bate, ramo nao visto, ESPERADOS sem o h0dn; titulo com H0DN sem a obrigacao, token de veredito proibido, «5σ atingido», «não falsificado» como cabeca de 5 sigma). montar() inteira roda no harness com o Nos emulado (precisa do core).
rc 0 = passou."""
import copy, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import delta_v410 as _DL0  # noqa: E402
if "delta_v409" not in sys.modules:   # (a ponte do ensaio: o quadro_v397.py da pasta da v410 ainda importa delta_v409 -- achado devolvido ao pai; aqui so' para o teste, como o ensaio e o conferidor fazem)
    sys.modules["delta_v409"] = _DL0
import registrar_mapa_v410 as M  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402
import delta_v410 as DL  # noqa: E402
from guarda_p18_v410 import violacoes  # noqa: E402
ids = M.ids_do_livro(); ok = True
falt = [r for r in M.ANOTADAS + M.REFS if r not in ids]
print("rotas anotadas+refs: %d; ausentes do livro: %s; a nova ja' existe: %s" % (len(M.ANOTADAS + M.REFS), falt, M.NOVA in ids))
ok = ok and not falt and M.NOVA not in ids
ok = ok and M.R_ATRATOR in M.ANOTADAS and M.R_H0DN in M.ANOTADAS and M.R_H0DN_COV in M.REFS and len(set(M.ANOTADAS)) == len(M.ANOTADAS)
sq = M.seq_do_alvo(M.livro(), M.R_IALD2, "ROTA", contem=("matricial", "leituras do operador"))
print("seq que a E29 corrige (kernel.iald2_06nov):", sq)
src = open(os.path.join(HERE, "registrar_mapa_v410.py"), encoding="utf-8").read()
tit = re.findall(r'anot\(R_[A-Z0-9]+, "(v410 SELADA %s:[^"]*)"', src)
S = "0123456789abcdef"; ruins = []
for t_ in tit:
    x_ = t_.replace("%s", S, 1).replace("%s", "IALD2")
    v_ = [list(a) for a in GF.violacoes(json.dumps({"titulo": x_}, ensure_ascii=False))] + list(violacoes(x_))
    if v_ or M.d59_viola(x_) or any(f.lower() in x_.lower() for f in DL.FORA_D65):
        ruins.append((x_[:120], v_[:2]))
print("titulos das anotacoes: %d; reprovados: %s" % (len(tit), ruins))
ok = ok and len(tit) == len(M.ANOTADAS) and not ruins
h_tit = [t_ for t_ in tit if re.search(r"\bH0DN\b", t_)]
h_ok = bool(h_tit) and all(DL.FRASE_H0DN_OBRIGATORIA_PT in t_ for t_ in h_tit)
print("titulos que trazem H0DN: %d; todos com a obrigacao no proprio titulo: %s" % (len(h_tit), h_ok)); ok = ok and h_ok
neg = GF.violacoes(json.dumps({"titulo": "v410 SELADA %s: o par na face de Fock ligado na v410" % S}, ensure_ascii=False))
print("controle negativo (Fock e v410 no mesmo trecho) reprovou:", bool(neg)); ok = ok and bool(neg)

# ---- (4) o H0DN: as funcoes puras sobre um registro SINTETICO (numeros de brinquedo; nada disto vai a texto publicado)
SHA = lambda c: c * 64
NP = DL.N_PINOS_FREEZE_R2 + 2
hd = {"all_verified": True, "verdict": DL.VEREDITO_H0DN_OK, "veredito_h0dn_source_sha256": SHA("a"), "does_not_gate_core": True, "runtime_executed": True, "beta_ok": True, "observed_vector_read": False,
      "mechanics": {"passed": True, "n_checks": DL.N_CHECKS_H0DN, "checks": [{"id": "c%d" % (i_ + 1), "ok": True} for i_ in range(DL.N_CHECKS_H0DN)]},
      "values": {"observed_vector_read": False, "n_pinos": NP, "pinos": {"p%d" % i_: {"sha256_ok": True, "bytes_ok": True} for i_ in range(NP)}, "ramos_vistos": [1, 2, 3, 4, 5, 6], "veredito_h0dn_source_sha256": SHA("a"),
                 "gate_verdict": "GATE_SINTETICO", "K": 1.5, "log10K": 0.17, "cauda_nula_analitica": 2.9e-07,
                 "D_esperado": [{"modelo": "published_baseline", "D": 6.5, "poder_analitico": 0.9}, {"modelo": "free_cepheid_host_differential_bias", "D": 5.5, "poder_analitico": 0.6}]},
      "modelos": ["published_baseline", "free_cepheid_host_differential_bias"], "insumos_pinados": {"i%d" % i_: {} for i_ in range(6)}, "ordem_kimi": {"sha256": SHA("b")}, "leitura_dossie": {"sha256": SHA("c")}, "o_que_falta": ["y_obs"]}
ESP = {"registros_funcao_v410": {"h0dn": {"nome": DL.H0DN_REGISTRO, "verdict": DL.VEREDITO_H0DN_OK, "n_checks": DL.N_CHECKS_H0DN, "values": {"veredito_h0dn_source_sha256": SHA("a")}}},
       "vereditos_novos_v410": {DL.H0DN_REGISTRO: DL.VEREDITO_H0DN_OK}, "qg_closure_gate_verdict_v409": "GATE_SINTETICO"}
F = M.h0dn_do_core(DL, hd, ESP)
e30 = "%s | lacuna de fidelidade: a D72 escrevia a palavra do livro de cobrancas na cabeca do ramo | estatuto: [REAL] | assinatura: %s" % (DL.ERRATA_E30, DL.ASSINA)
TH = M.h0dn_textos(DL, F, e30)
t_h_titulo = h_tit[0].replace("%s", S, 1)
reg_h = {"tipo": "ANOTACAO", "rota_id": M.R_H0DN, "estatuto": TH["estatuto"], "titulo": t_h_titulo, "resultado": TH["resultado"], "proximo_passo": TH["proximo"], "defeito": TH["defeito"], "refs": [M.NOVA, M.R_H0DN_COV]}
txt_h = json.dumps(reg_h, ensure_ascii=False)
v_h = [list(a) for a in GF.violacoes(txt_h)] + list(violacoes(txt_h))
print("registro do H0DN (sintetico): %d B; violacoes P18/frases: %s; D59: %s" % (len(txt_h.encode("utf-8")), v_h[:3], M.d59_viola(txt_h)))
ok = ok and not v_h and not M.d59_viola(txt_h) and len(txt_h) < 6 * 6000
chk = {"obrigacao no texto": DL.FRASE_H0DN_OBRIGATORIA_PT in txt_h, "sem token proibido do H0DN": not any(t_ in txt_h for t_ in DL.TOKENS_PROIBIDOS_H0DN), "sem o agregado publico": not any(a_ in txt_h for a_ in DL.H0DN_AGREGADO_NAO_ENTRA),
       "sem a cabeca do ramo de 5 sigma por extenso": ("BETA_TGL" not in txt_h and DL.VEREDITOS_H0DN["leitura"] % 6 not in txt_h), "a leitura em palavras (D76)": DL.FRASE_PROVADO_PT in txt_h and "outcome" in txt_h,
       "campos <= 6000": all(len(v_) <= 6000 for v_ in TH.values() if isinstance(v_, str))}
for k_, v_ in chk.items():
    print("  %-46s %s" % (k_, v_)); ok = ok and bool(v_)
# controles negativos de h0dn_do_core: cada um TEM de levantar AssertionError
def muda(f_hd=None, f_esp=None):
    h_ = copy.deepcopy(hd); e_ = copy.deepcopy(ESP)
    if f_hd:
        f_hd(h_)
    if f_esp:
        f_esp(e_)
    return h_, e_
def levanta(h_, e_):
    try:
        M.h0dn_do_core(DL, h_, e_)
    except AssertionError:
        return True
    return False
negs = {"vetor observado lido": muda(lambda h: h.update(observed_vector_read=True)), "vetor observado lido (values)": muda(lambda h: h["values"].update(observed_vector_read=True)), "registro ausente": ({}, ESP), "nao selou": muda(lambda h: h.update(all_verified=False)),
        "checagem falha": muda(lambda h: h["mechanics"]["checks"][-1].update(ok=False)), "pino nao bate": muda(lambda h: h["values"]["pinos"]["p0"].update(sha256_ok=False)), "ramo nao visto": muda(lambda h: h["values"].update(ramos_vistos=[1, 2, 3])),
        "veredito diferente": muda(lambda h: h.update(verdict="OUTRO")), "ESPERADOS sem o h0dn": muda(None, lambda e: e["registros_funcao_v410"].pop("h0dn")), "sha256 do texto-fonte != ESPERADOS": muda(None, lambda e: e["registros_funcao_v410"]["h0dn"]["values"].update(veredito_h0dn_source_sha256=SHA("f"))),
        "gate diferente da v409": muda(lambda h: h["values"].update(gate_verdict="OUTRO"))}
for k_, (h_, e_) in negs.items():
    r_ = levanta(h_, e_); print("  controle negativo h0dn_do_core %-36s reprovou: %s" % (k_, r_)); ok = ok and r_
# controles negativos das guardas de texto (o texto do H0DN): cada um TEM de reprovar
tit_sem = t_h_titulo.replace(DL.FRASE_H0DN_OBRIGATORIA_PT, "")
negt = {"titulo com H0DN sem a obrigacao": json.dumps({"titulo": tit_sem}, ensure_ascii=False), "H0DN sem a obrigacao no registro": json.dumps({"titulo": "v410 SELADA %s: o teste H0DN × BG1 entrou no um.py" % S}, ensure_ascii=False),
        "token de veredito proibido": txt_h + " " + DL.TOKENS_PROIBIDOS_H0DN[0], "token de veredito proibido (2)": txt_h + " " + DL.TOKENS_PROIBIDOS_H0DN[-1], "5σ atingido": txt_h + " Aqui 5σ atingido no H0DN.", "o teste deu": txt_h + " Neste ponto o teste deu 5 sigma.",
        "H0DN detectado": txt_h + " O H0DN detectou o desvio.", "nao falsificado como cabeca de 5 sigma": txt_h + " O resultado acima de 5σ é não falsificado."}
for k_, t_ in negt.items():
    r_ = bool(GF.violacoes(t_)) or bool(violacoes(t_)); print("  controle negativo de texto %-40s reprovou: %s" % (k_, r_)); ok = ok and r_
# D59: o Milenio e o Navier sempre; o Kimi so' no contexto do H0DN
d59 = {"Kimi fora do H0DN reprova": M.d59_viola("a ordem ao Kimi para outra coisa"), "Kimi no contexto do H0DN passa": not M.d59_viola("a ORDEM ao Kimi do H0DN: montar y_obs"), "Navier reprova": M.d59_viola("Navier-Stokes e o H0DN"), "Milenio reprova": M.d59_viola("problema do Milênio")}
for k_, v_ in d59.items():
    print("  D59 %-34s %s" % (k_, v_)); ok = ok and bool(v_)
# ---- (5) parte 2: a rota da AEscala (seq LIDOS do livro) e as funcoes puras da escala e do recibo HMS/13 sobre registros SINTETICOS
regs_ = M.livro()
sq_ae = M.seq_do_alvo(regs_, M.R_AESCALA, "ROTA"); sq_er = sorted(r_["seq"] for r_ in regs_ if r_.get("rota_id") == M.R_AESCALA and r_.get("tipo") == "ERRATA")
print("rota da AEscala (%s): a candidata e' o seq %s; erratas ao lado: %s" % (M.R_AESCALA, sq_ae, sq_er)); ok = ok and M.R_AESCALA in M.ANOTADAS and bool(sq_ae) and bool(sq_er)
ea = {"all_verified": True, "does_not_gate_core": True, "runtime_executed": True, "beta_ok": True, "nomes_ratificados": True, "nomes_novos_da_pedra": list(DL.NOMES_NOVOS_AESCALA), "campos_novos_da_estrutura": list(DL.CAMPOS_NOVOS_AESCALA), "estatuto_dos_nomes_ratificados_d101": DL.ESTATUTO_NOMES_NOVOS_AESCALA, "ratificacao_pendente": dict(DL.RATIFICACAO_PENDENTE_AESCALA), "ponte": dict(DL.PONTE_AESCALA), "chaves_antigas_que_mudam": [], "verdict": DL.VEREDITO_AESCALA_OK, "frase_canonica_pt": DL.FRASE_CLAY_CANONICA_PT, "frase_d83_pt": DL.FRASE_D83_OBRIGATORIA_PT, "ratificacao": {"sha256": DL.RATIFICACAO_D87_SHA256},
      "mechanics": {"passed": True, "n_checks": DL.N_CHECKS_AESCALA, "checks": [{"id": "c%d" % (i_ + 1), "ok": True} for i_ in range(DL.N_CHECKS_AESCALA)]},
      "values": {"n_ancoras_ok": len(DL.ANCORAS_AESCALA), "n_ancoras": len(DL.ANCORAS_AESCALA), "n_flags_true": 3, "n_flags": 3, "n_falas_ok": 8, "n_falas": 8, "n_nomes": len(DL.NOMES_AESCALA), "numeros": dict(DL.NUMEROS_AESCALA), "n_nomes_novos": len(DL.NOMES_NOVOS_AESCALA), "nomes_novos_declarados": len(DL.NOMES_NOVOS_AESCALA), "nomes_novos": {n_: True for n_ in DL.NOMES_NOVOS_AESCALA}, "campos_novos_na_estrutura": {c_: True for c_ in DL.CAMPOS_NOVOS_AESCALA}, "nomes_novos_ok": True, "ponte": {"ok": True}, "gate_verdict": "GATE_SINTETICO"}}   # (contagens SINTETICAS; os numeros, os nomes novos, a ponte e as frases sao os do delta)
hm = {"all_verified": True, "does_not_gate_core": True, "runtime_executed": True, "beta_ok": True, "observed_vector_read": False, "le_em_rito": False, "verdict": DL.VEREDITO_HMS13_OK, "estatuto": "x " + DL.FRASE_HMS13_OBRIGATORIA_PT, "scope": "y " + DL.FRASE_HMS13_OBRIGATORIA_PT,
      "mechanics": {"passed": True, "n_checks": DL.N_CHECKS_HMS13, "checks": [{"id": "c%d" % (i_ + 1), "ok": True} for i_ in range(DL.N_CHECKS_HMS13)]},
      "values": {"observed_vector_read": False, "le_em_rito": False, "campos": dict(DL.HMS13_CAMPOS), "n_fontes_primarias": DL.HMS13_CAMPOS["fontes_primarias"], "n_calibradores": DL.HMS13_CAMPOS["calibradores"], "n_embutidos": len(DL.HMS13_EMBUTIDOS), "sob_pasta_vedada": [], "com_nome_vedado": [], "gate_verdict": "GATE_SINTETICO", "ratificacao_sha256": SHA("d")},
      "o_que_falta": ["a covariancia fisica conjunta (G3/G4) [OPEN]"]}
ESP2 = copy.deepcopy(ESP); ESP2["registros_funcao_v410"].update({"a_escala": {"verdict": DL.VEREDITO_AESCALA_OK}, "hms13": {"verdict": DL.VEREDITO_HMS13_OK}}); ESP2["vereditos_novos_v410"].update({DL.AESCALA_REGISTRO: DL.VEREDITO_AESCALA_OK, DL.HMS13_REGISTRO: DL.VEREDITO_HMS13_OK})
FA = M.escala_do_core(DL, ea, ESP2); FH = M.hms13_do_core(DL, hm, hd, ESP2)
AE = M.escala_textos(DL, FA, (sq_ae, ", ".join(str(x_) for x_ in sq_er))); HM = M.hms13_textos(DL, FH)
reg_a = {"tipo": "ANOTACAO", "rota_id": M.R_AESCALA, "estatuto": AE["estatuto"], "titulo": "v410 SELADA %s: a pedra AEscala foi instalada, ratificada e selada" % S, "resultado": AE["resultado"], "proximo_passo": AE["proximo"], "defeito": AE["defeito"], "refs": [M.NOVA, M.R_IALD2]}
reg_h2 = dict(reg_h, resultado=TH["resultado"] + " || " + HM["resultado"], proximo_passo=TH["proximo"] + "; " + HM["proximo"], defeito=TH["defeito"] + "; " + HM["defeito"], estatuto=TH["estatuto"] + "; " + HM["estatuto"])
for rot_, r_ in (("AEscala", reg_a), ("H0DN + HMS/13", reg_h2)):
    t_ = json.dumps(r_, ensure_ascii=False); v_ = [list(a) for a in GF.violacoes(t_)] + list(violacoes(t_))
    print("registro %-14s (sintetico): %d B; violacoes P18/frases: %s; D59: %s; campos <= 6000: %s" % (rot_, len(t_.encode("utf-8")), v_[:3], M.d59_viola(t_), all(len(x_) <= 6000 for x_ in r_.values() if isinstance(x_, str))))
    ok = ok and not v_ and not M.d59_viola(t_) and all(len(x_) <= 6000 for x_ in r_.values() if isinstance(x_, str))
t_a = json.dumps(reg_a, ensure_ascii=False); t_h2 = json.dumps(reg_h2, ensure_ascii=False)
chk2 = {"a escala: a forma canonica do Clay (D84) e a da D83": DL.FRASE_CLAY_CANONICA_PT in t_a and DL.FRASE_D83_OBRIGATORIA_PT in t_a, "a escala: P = nP na forma da D81": DL.FRASE_D81_PT in t_a, "a escala: os numeros do delta": all(DL.NUMEROS_AESCALA[k_] in t_a for k_ in ("nome_pesa_um", "meio", "tres_faces", "um_terco_caiu", "nome_normalizado")),
        "a escala: os nomes ratificados (D87)": DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT in t_a, "a escala: os seq da candidata e da errata lidos do livro": str(sq_ae) in t_a and all(str(x_) in t_a for x_ in sq_er), "HMS/13: a frase obrigatoria (D80) e a do H0DN (D72) no mesmo registro": DL.FRASE_HMS13_OBRIGATORIA_PT in t_h2 and DL.FRASE_H0DN_OBRIGATORIA_PT in t_h2,
        "HMS/13: aditivo e posterior ao FREEZE_R2, sem abertura": "ADITIVO e POSTERIOR ao FREEZE_R2" in t_h2 and "NAO a autoriza" in t_h2, "HMS/13: sem o agregado publico nem token proibido": not any(a_ in t_h2 for a_ in DL.H0DN_AGREGADO_NAO_ENTRA) and not any(t_ in t_h2 for t_ in DL.TOKENS_PROIBIDOS_H0DN)}
for k_, v_ in chk2.items():
    print("  %-70s %s" % (k_, v_)); ok = ok and bool(v_)
def lev2(fn_, a_, b_):
    try:
        fn_(DL, a_, b_) if fn_ is M.escala_do_core else fn_(DL, a_, hd, b_)
    except AssertionError:
        return True
    return False
def mud(base_, f_=None, e_=None, esp_=ESP2):
    x_ = copy.deepcopy(base_); y_ = copy.deepcopy(esp_)
    if f_:
        f_(x_)
    if e_:
        e_(y_)
    return x_, y_
negs2 = {"escala: nomes nao ratificados": (M.escala_do_core,) + mud(ea, lambda x: x.update(nomes_ratificados=False)), "escala: numero diferente do delta": (M.escala_do_core,) + mud(ea, lambda x: x["values"]["numeros"].update(tres_faces="2")),
         "escala: a frase canonica do Clay trocada": (M.escala_do_core,) + mud(ea, lambda x: x.update(frase_canonica_pt="O Clay esta resolvido.")), "escala: nao selou": (M.escala_do_core,) + mud(ea, lambda x: x.update(all_verified=False)),
         "escala: checagem falha": (M.escala_do_core,) + mud(ea, lambda x: x["mechanics"]["checks"][-1].update(ok=False)), "escala: ratificacao diferente (D87)": (M.escala_do_core,) + mud(ea, lambda x: x["ratificacao"].update(sha256=SHA("0"))),
         "escala: nome novo dito ratificado": (M.escala_do_core,) + mud(ea, lambda x: x.update(estatuto_dos_nomes_ratificados_d101="RATIFICADOS pelo operador")), "escala: nomes novos diferentes do delta": (M.escala_do_core,) + mud(ea, lambda x: x.update(nomes_novos_da_pedra=list(x["nomes_novos_da_pedra"])[:-1])),
         "escala: ponte da escala diferente do delta": (M.escala_do_core,) + mud(ea, lambda x: x["ponte"]["casos"][1].__setitem__(2, "1/9")), "escala: a ponte nao recalculada": (M.escala_do_core,) + mud(ea, lambda x: x["values"]["ponte"].update(ok=False)),
         "escala: ESPERADOS sem a_escala": (M.escala_do_core,) + mud(ea, None, lambda e: e["registros_funcao_v410"].pop("a_escala")), "escala: o gate diferente da v409": (M.escala_do_core,) + mud(ea, lambda x: x["values"].update(gate_verdict="OUTRO")),
         "hms13: vetor observado lido": (M.hms13_do_core,) + mud(hm, lambda x: x.update(observed_vector_read=True)), "hms13: entrega aberta em rito": (M.hms13_do_core,) + mud(hm, lambda x: x.update(le_em_rito=True)),
         "hms13: caminho sob a pasta vedada": (M.hms13_do_core,) + mud(hm, lambda x: x["values"].update(sob_pasta_vedada=["x"])), "hms13: os dez campos diferentes do delta": (M.hms13_do_core,) + mud(hm, lambda x: x["values"]["campos"].update(opening_allowed=True)),
         "hms13: sem a frase obrigatoria no estatuto": (M.hms13_do_core,) + mud(hm, lambda x: x.update(estatuto="x")), "hms13: nao selou": (M.hms13_do_core,) + mud(hm, lambda x: x.update(all_verified=False)),
         "hms13: ESPERADOS sem o hms13": (M.hms13_do_core,) + mud(hm, None, lambda e: e["registros_funcao_v410"].pop("hms13")), "hms13: o gate diferente da v409": (M.hms13_do_core,) + mud(hm, lambda x: x["values"].update(gate_verdict="OUTRO"))}
for k_, (fn_, a_, b_) in negs2.items():
    r_ = lev2(fn_, a_, b_); print("  controle negativo %-44s reprovou: %s" % (k_, r_)); ok = ok and r_
negt2 = {"o recibo HMS/13 sem a frase obrigatoria": t_h2.replace(DL.FRASE_HMS13_OBRIGATORIA_PT, "XXXX"), "o Clay dito resolvido a seco": json.dumps({"titulo": "v410 SELADA %s: o Clay foi resolvido" % S}, ensure_ascii=False), "a covariancia fisica dita fechada": t_h2 + " A covariancia fisica esta fechada.",
         "a abertura dita permitida": t_h2 + " A abertura esta permitida.", "a forma HMS completa dita admitida": t_h2 + " A forma HMS completa é admitida.", "P = nP dito nao provado": t_a + " P = nP de Turing nao foi provado.", "a face caida dita ilegivel": t_a + " A face caida nao se le."}
for k_, t_ in negt2.items():
    if k_ == "o recibo HMS/13 sem a frase obrigatoria":
        r_ = bool(re.search(r"HMS\s*/\s*13", t_)) and DL.FRASE_HMS13_OBRIGATORIA_PT not in t_   # (a obrigacao local do montar(): hm_sem)
    elif k_ == "o Clay dito resolvido a seco":
        r_ = bool(GF.violacoes(t_))
    else:
        r_ = bool(GF.violacoes(t_)) or bool(violacoes(t_))
    print("  controle negativo de texto %-44s reprovou: %s" % (k_, r_)); ok = ok and r_
print("RESULTADO:", "PASSOU" if ok else "REPROVOU"); sys.exit(0 if ok else 1)
