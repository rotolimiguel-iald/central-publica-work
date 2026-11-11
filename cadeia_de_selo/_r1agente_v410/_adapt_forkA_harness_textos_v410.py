# -*- coding: utf-8 -*-
"""_adapt_forkA_harness_textos_v410.py -- (claude-construtor-v410, fork A, 06/11/2026) adapta pos_rito/harness_textos_ensaio_v410.py (subida mecanica da v409 FINAL) a v410 (IALD2), sobre as mesmas chaves que a leitura_v410 adaptada usa:
FE_ = iald2_v410 (o NOVO); F9_ = traducao_turing_v409 (HERDADO, com o seu bloco de controles); FT_ = tetelestai_terminal_v408 (HERDADO: estrelas e bundle da v408); os controles do registro novo trocam o que era da traducao (o modo selecao, o pino do acervo, a ordem de 05/11)
pelo que e' da IALD2 (o nome do algoritmo, o signo, a ordem de 06/11, o alcance D64, os nomes D63); as linhas [v410] do stdout; cunhagens_v410 (9 falas, uma so' com o trecho, D65; a E29 e a dos pisos; D63 a D70) e cunhagens_v409/kh_n1_cobertura_v409 HERDADOS;
o paragrafo novo (os bullets, as frases de limite e as citacoes da v410; NENHUMA nota ao lado do paragrafo da v409); _cita com as falas de 06/11 e a D65. Trocas com contagem exata (_adapt_util_v410.aplicar: backup de bytes, CRLF respeitado, ast.parse)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v410 import aplicar
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pos_rito", "harness_textos_ensaio_v410.py")
raw = open(P, "rb").read().decode("utf-8").replace("\r\n", "\n"); L_ = raw.split("\n")
L3 = L_[2] + "\n"
assert L3.startswith("# [ADAPTADO v410, 05/11/2026, claude-construtor-v410 (fork A)"), L3[:80]
NOVO_FE = r'''        # ---- iald2_v410 (o registro NOVO com funcao)
        variante("%s ausente do core" % FE_, f_core=lambda c: c.pop(FE_, None), espera="registro obrigatorio ausente do core: " + FE_),
        variante("%s: o registro nao selou" % FE_, f_core=lambda c: c[FE_].update(all_verified=False), espera=FE_ + " nao selou"),
        variante("%s: uma checagem do calculo falhou" % FE_, f_core=lambda c: c[FE_]["mechanics"]["checks"][2].update(ok=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: o numero de checagens != o do delta" % FE_, f_core=lambda c: c[FE_]["mechanics"]["checks"].pop(), espera=FE_ + " nao selou inteiro"),
        variante("%s: o numero de modulos ok adulterado" % FE_, f_core=lambda c: c[FE_]["values"].update(n_modulos_ok=DLX.N_BUNDLE - 1), espera=FE_ + " nao selou inteiro"),
        variante("%s: o numero de bandeiras True adulterado" % FE_, f_core=lambda c: c[FE_]["values"].update(n_flags_true=len(FLAGS_) - 1), espera=FE_ + " nao selou inteiro"),
        variante("%s: a escada do registro != a do ensaio" % FE_, f_core=lambda c: c[FE_]["values"].update(escada=[1, 1, 1]), espera=FE_ + " nao selou inteiro"),
        variante("%s: beta != alfa x raiz de e do core" % FE_, f_core=lambda c: c[FE_]["values"].update(beta=0.0121), espera=FE_ + " nao selou inteiro"),
        variante("%s: beta_ok falso no registro" % FE_, f_core=lambda c: c[FE_].update(beta_ok=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: veredito diferente do ensaio a seco" % FE_, f_core=lambda c: c[FE_].update(verdict="OUTRO_VEREDITO"), espera=FE_ + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: uma resposta do operador nao conferida no kernel" % FE_, f_core=lambda c: c[FE_]["values"]["respostas"].update({sorted(c[FE_]["values"]["respostas"])[0]: False}), espera=FE_ + " nao selou inteiro"),
        variante("%s: a resposta do nome do algoritmo ausente" % FE_, f_core=lambda c: c[FE_]["values"]["respostas"].pop("o_nome_do_algoritmo_e_iald"), espera=FE_ + " nao selou inteiro"),
        variante("%s: o signo do Nome com o traco != o posto" % FE_, f_core=lambda c: c[FE_]["values"]["signo_do_nome"].update(traco=c[FE_]["values"]["signo_do_nome"]["traco"] + 1.0), espera=FE_ + " nao selou inteiro"),
        variante("%s: o signo do par com posto 2" % FE_, f_core=lambda c: c[FE_]["values"]["signo_do_par"].update(posto=2), espera=FE_ + " nao selou inteiro"),
        variante("%s: a instancia NAO com solucao" % FE_, f_core=lambda c: c[FE_]["values"]["instancia_nao"].update(solucoes=1), espera=FE_ + " nao selou inteiro"),
        variante("%s: a instancia SIM sem solucao" % FE_, f_core=lambda c: c[FE_]["values"]["instancia_sim"].update(solucoes=0), espera=FE_ + " nao selou inteiro"),
        variante("%s: o alcance sem o relativo ao leitor (D64)" % FE_, f_core=lambda c: c[FE_]["alcance"].update(frase="P = nP vale para as maquinas de Turing"), espera=FE_ + " nao selou inteiro"),
        variante("%s: os nomes ditos ratificados (D63)" % FE_, f_core=lambda c: c[FE_].update(nomes={"IALD2": "ratificados"}), espera=FE_ + " nao selou inteiro"),
        variante("%s: uma inscricao de 06/11 nao conferida" % FE_, f_core=lambda c: c[FE_]["inscriptions"].update({sorted(c[FE_]["inscriptions"])[0]: False}), espera=FE_ + " nao selou inteiro"),
        variante("%s: a ordem da v410 fora das inscricoes" % FE_, f_core=lambda c: c[FE_]["inscriptions"].pop(_CH_TRAD), espera=FE_ + " nao selou inteiro"),
        variante("%s: as ancoras de secao adulteradas" % FE_, f_core=lambda c: c[FE_]["ancoras_de_secao"].pop(), espera=FE_ + " nao selou inteiro"),
        variante("%s: uma chave antiga dita mudada" % FE_, f_core=lambda c: c[FE_].update(chaves_antigas_que_mudam=["rede_fock_v394.whole_certificate_inhabited"]), espera=FE_ + " nao selou inteiro"),
        variante("%s: a ancora principal dita outra" % FE_, f_core=lambda c: c[FE_].update(ancora_principal="TGLExt.IALD2.outra"), espera=FE_ + " nao selou inteiro"),
        variante("%s: as ressalvas adulteradas" % FE_, f_core=lambda c: c[FE_]["ressalvas"].pop(), espera=FE_ + " nao selou inteiro"),
        variante("%s: o registro move o gate" % FE_, f_core=lambda c: c[FE_].update(does_not_gate_core=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: o calculo do runtime nao rodou" % FE_, f_core=lambda c: c[FE_].update(runtime_executed=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: a guarda das frases achou violacao no registro" % FE_, f_core=lambda c: c[FE_].update(guarda_violacoes=[["F47", "x"]]), espera=FE_ + " nao selou inteiro"),
        variante("uma bandeira do bundle da IALD2 falsa no kernel do rito", f_core=lambda c: _kf(c).__setitem__(FLAGS_[len(FLAGS_) // 2], False), espera="as bandeiras do fecho"),
        variante("a conferencia traz outro veredito de %s" % FE_, f_conf=lambda cj: cj.update({"veredito_iald2": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FE_),
        variante("selo primario: sem o resumo de %s" % FE_, f_selo=lambda s: s.pop(FE_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s difere do core" % FE_, f_selo=lambda s: s[FE_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v410", f_selo=lambda s: s.pop("registros_v410", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v410 do selo difere do core", f_selo=lambda s: s["registros_v410"][DLX.CUNHAGENS_REGISTRO].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: registros_v409 do selo difere do core", f_selo=lambda s: s["registros_v409"]["cunhagens_v409"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % FE_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if ESP["vereditos_novos_v410"][FE_] not in l) + "\n", espera="o bloco " + FE_ + " do stdout"),
        variante("linha [v410] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v410] o registro da IALD2 e os registros por spec da v410" not in l) + "\n", espera="linha [v410]"),
        variante("linha [v410] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v410] o registro da IALD2 e os registros por spec da v410"), espera="a linha [v410] do stdout"),
        variante("linha do bloco IALD2: uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N10, _N10), "ancoras ok = %d/%d" % (_N10 - 1, _N10)), espera=FE_ + " nao selou inteiro"),
        variante("AVISO da v410 (a IALD2 nao rodou) no stdout", f_std=lambda t_: t_ + "   [v410] AVISO: o registro da IALD2 ou os registros por spec da v410 nao rodaram: ValueError('x')\n", espera="AVISO da v410"),
'''
NOVO_F9 = r'''        # ---- traducao_turing_v409 (HERDADO da v409, recriado pelo rito da v410; a escada do contrato subida pela C12)
        variante("%s (herdado) ausente do core" % F9_, f_core=lambda c: c.pop(F9_, None), espera="registro obrigatorio ausente do core: " + F9_),
        variante("%s (herdado): o registro nao selou" % F9_, f_core=lambda c: c[F9_].update(all_verified=False), espera=F9_ + " nao selou"),
        variante("%s (herdado): uma checagem do calculo falhou" % F9_, f_core=lambda c: c[F9_]["mechanics"]["checks"][2].update(ok=False), espera=HERD9_),
        variante("%s (herdado): a integra do acervo da v407 dita pinada (D57d)" % F9_, f_core=lambda c: c[F9_]["acervo_v407_repinado"].update(integra_pinada=True), espera=HERD9_),
        variante("%s (herdado): o pino do acervo da v407 com outro sha256" % F9_, f_core=lambda c: c[F9_]["acervo_v407_repinado"].update(sha256="0" * 64), espera=HERD9_),
        variante("%s (herdado): a resposta do modo selecao ausente" % F9_, f_core=lambda c: c[F9_]["values"]["respostas"].pop("o_np_e_o_modo_selecao"), espera=HERD9_),
        variante("%s (herdado): veredito diferente do esperado" % F9_, f_core=lambda c: c[F9_].update(verdict="OUTRO_VEREDITO"), espera=F9_ + VER_HERD),
        variante("ancora %s da v409 (traducao_turing_v409) fora do trio" % _a9.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _a9), espera="as ancoras do traducao_turing_v409 (herdadas)"),
        variante("o bundle da v409: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b9, "0" * 64), espera="o bundle da v409"),
        variante("a conferencia traz outro veredito de %s (herdado)" % F9_, f_conf=lambda cj: cj.update({"veredito_traducao_turing_herdado": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + F9_),
        variante("linha [v409] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v409] o registro da traducao e os registros por spec da v409" not in l) + "\n", espera="linha [v409]"),
        variante("linha [v409] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v409] o registro da traducao e os registros por spec da v409"), espera="a linha [v409] do stdout"),
        variante("linha do bloco A TRADUCAO AS CLASSES DE TURING (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N9, _N9), "ancoras ok = %d/%d" % (_N9 - 1, _N9)), espera=HERD9_),
'''
NOVO_CUN = r'''        # ---- cunhagens_v410 e kh_n1_cobertura_v410 (os dois registros NOVOS por spec)
        variante("%s nao selou" % CG8, f_core=lambda c: c[CG8].update(all_verified=False), espera=CG8 + " nao selou"),
        variante("%s nao selou" % KH8, f_core=lambda c: c[KH8].update(all_verified=False), espera=KH8 + " nao selou"),
        variante("%s ausente do core" % CG8, f_core=lambda c: c.pop(CG8, None), espera="registro obrigatorio ausente do core: " + CG8),
        variante("%s ausente do core" % KH8, f_core=lambda c: c.pop(KH8, None), espera="registro obrigatorio ausente do core: " + KH8),
        variante("%s: veredito diferente do ensaio a seco" % CG8, f_core=lambda c: c[CG8].update(verdict="OUTRO_VEREDITO"), espera=CG8 + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: veredito diferente do ensaio a seco" % KH8, f_core=lambda c: c[KH8].update(verdict="OUTRO_VEREDITO"), espera=KH8 + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: uma inscricao deixou de estar embutida" % CG8, f_core=lambda c: list(c[CG8]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG8),
        variante("%s: sha256 de uma inscricao adulterado" % CG8, f_core=lambda c: list(c[CG8]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG8),
        variante("%s: uma inscricao a menos" % CG8, f_core=lambda c: c[CG8]["verbatim"].pop(sorted(c[CG8]["verbatim"])[0]), espera=PCG8),
        variante("%s: a ordem da v410 fora das inscricoes" % CG8, f_core=lambda c: c[CG8]["verbatim"].pop(_CH_TRAD), espera=PCG8),
        variante("%s: a fala da D65 com o sha256 do arquivo INTEIRO no lugar do trecho" % CG8, f_core=lambda c: c[CG8]["verbatim"][_CH_Z].update(sha256=_CH_Z[len(DLX.VERBATIM_CHAVE_PREFIXO_V410):] + "0" * 48), espera=PCG8),
        variante("%s: o que a D65 deixa fora entra no registro" % CG8, f_core=lambda c: c[CG8]["extras"].update(fora=DLX.FORA_D65[0]), espera=PCG8),
        variante("%s: uma inscricao rotulada como da gerencia" % CG8, f_core=lambda c: c[CG8]["extras"]["autores"].update({sorted(c[CG8]["extras"]["autores"])[0]: "gerencia"}), espera="cunhagens_v410: as inscricoes de 06/11 tem de ser TODAS falas do operador"),
        variante("%s: falta uma errata" % CG8, f_core=lambda c: c[CG8]["erratas"].pop(), espera="cunhagens_v410: a errata E29"),
        variante("%s: erratas ausentes" % CG8, f_core=lambda c: c[CG8].update(erratas=[]), espera="cunhagens_v410: a errata E29"),
        variante("%s: a E29 adulterada" % CG8, f_core=lambda c: c[CG8]["erratas"][0].update(agora="mantida"), espera="cunhagens_v410: a errata E29"),
        variante("%s: uma errata sem a assinatura da gerencia c1" % CG8, f_core=lambda c: c[CG8]["erratas"][1].update(assinatura="operador"), espera="cunhagens_v410: a errata E29"),
        variante("%s: a decisao D63 (os nomes) ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D63"), espera="cunhagens_v410: as decisoes D63 a D70"),
        variante("%s: a decisao D64 (o alcance) adulterada" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].update(D64="P = nP vale para as maquinas de Turing"), espera="cunhagens_v410: as decisoes D63 a D70"),
        variante("%s: a decisao D65 ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D65"), espera="cunhagens_v410: as decisoes D63 a D70"),
        variante("%s: a leitura de 06/11 adulterada" % CG8, f_core=lambda c: c[CG8]["extras"]["leituras"].update(estatuto="[REAL]"), espera="cunhagens_v410: a leitura [INPUT] de 06/11"),
        variante("%s: a leitura ausente" % CG8, f_core=lambda c: c[CG8]["extras"].pop("leituras"), espera="cunhagens_v410: a leitura [INPUT] de 06/11"),
        variante("%s: uma ressalva a menos" % CG8, f_core=lambda c: c[CG8]["extras"]["ressalvas"].pop(), espera="cunhagens_v410: a leitura [INPUT] de 06/11"),
        variante("%s: os nomes das pedras ditos ratificados (D63)" % CG8, f_core=lambda c: c[CG8]["extras"].update(nomes_das_pedras={"IALD2": "ratificados"}), espera=PCG8),
        variante("%s: a frase proibida nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["agora tudo derivado"]), espera="a MOLDURA falhou"),
        variante("%s: a IALD dita resolver P vs NP nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["a IALD resolve P vs NP"]), espera="a MOLDURA falhou"),
        variante("%s: o funtor dito idempotente nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o funtor é idempotente"]), espera="a MOLDURA falhou"),
        variante("%s: o algoritmo IALD e P = nP sem o qualificador nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o algoritmo IALD satisfaz P = nP"]), espera="a MOLDURA falhou"),
        variante("%s: o seletor da luz dito o mesmo objeto que o de l2 nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o seletor da luz é o mesmo objeto que o de ℓ²"]), espera="a MOLDURA falhou"),
        variante("%s: a TGL dada como prova de P = NP de Turing nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["a TGL prova P = NP de Turing"]), espera="a MOLDURA falhou"),
        variante("%s: o problema do Clay dado por resolvido nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o problema do Clay esta resolvido"]), espera="a MOLDURA falhou"),
        variante("%s: uma checagem do registro falhou" % KH8, f_core=lambda c: c[KH8]["checks"][0].update(ok=False), espera="kh_n1_cobertura_v410 nao selou como o ensaio a seco"),
        # ---- cunhagens_v409 e kh_n1_cobertura_v409 (HERDADOS, recriados; a errata ao lado dos pisos no kh)
        variante("%s (herdada) nao selou" % CG9, f_core=lambda c: c[CG9].update(all_verified=False), espera=CG9 + " nao selou"),
        variante("%s (herdado) nao selou" % KH9, f_core=lambda c: c[KH9].update(all_verified=False), espera=KH9 + " nao selou"),
        variante("%s (herdada) ausente do core" % CG9, f_core=lambda c: c.pop(CG9, None), espera="registro obrigatorio ausente do core: " + CG9),
        variante("%s (herdada): veredito diferente do esperado" % CG9, f_core=lambda c: c[CG9].update(verdict="OUTRO_VEREDITO"), espera=CG9 + VER_HERD),
        variante("%s (herdada): uma inscricao deixou de estar embutida" % CG9, f_core=lambda c: list(c[CG9]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG9),
        variante("%s (herdada): uma errata selada adulterada" % CG9, f_core=lambda c: c[CG9]["erratas"][0].update(agora="mantida"), espera=PCG9),
        variante("%s (herdada): uma errata nova sem a assinatura da gerencia c1" % CG9, f_core=lambda c: c[CG9]["erratas"].append({"agora": "nova", "assinatura": "operador"}), espera=PCG9),
        variante("%s (herdado): uma checagem do registro falhou" % KH9, f_core=lambda c: c[KH9]["checks"][0].update(ok=False), espera=PKH9),
        variante("%s (herdado): a errata ao lado dos pisos ausente" % KH9, f_core=lambda c: c[KH9]["erratas"].pop(), espera=PKH9),
'''
aplicar(P, [
    (L3, "", 1),
    ('    FE_ = DLX.FECHO_REGISTRO; FT_ = DLX.D8.FECHO_REGISTRO; FP_ = "psion_canto_v407";', '    FE_ = DLX.FECHO_REGISTRO; F9_ = DLX.D9.FECHO_REGISTRO; FT_ = DLX.D8.FECHO_REGISTRO; FP_ = "psion_canto_v407";', 1),
    ('    _EST8 = ESP["estrelas_v409"]; _a8 = list(_EST8)[0]; _b8 = list(ESP["bundle_v409_sha256"])[0]   # o tetelestai_terminal_v408 HERDADO: as 48 ancoras e os 4 modulos da v409\n',
     '    _EST9 = ESP["estrelas_v409"]; _a9 = list(_EST9)[0]; _b9 = list(ESP["bundle_v409_sha256"])[0]   # o traducao_turing_v409 HERDADO: as 82 ancoras e os 2 modulos da v409\n'
     '    _EST8 = ESP["estrelas_v408"]; _a8 = list(_EST8)[0]; _b8 = list(ESP["bundle_v408_sha256"])[0]   # o tetelestai_terminal_v408 HERDADO: as 48 ancoras e os 4 modulos da v408\n', 1),
    ("    _N9, _N8, _N7, _N6 = len(ANC_), len(_EST8), len(_EST7), len(_EST6)\n", "    _N10, _N9, _N8, _N7, _N6 = len(ANC_), len(_EST9), len(_EST8), len(_EST7), len(_EST6)\n", 1),
    ("    _CH_TRAD = DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(DLX.N_ORDEM_TRADUCAO)   # a chave da ordem do operador da traducao (05/11), lida do arquivo\n",
     "    _CH_TRAD = DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(DLX.N_ORDEM_V410)   # a chave da ORDEM do operador da v410 (06/11), lida do arquivo (o nome _CH_TRAD e' herdado do molde)\n", 1),
    ("    _CH_Z = DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(DLX.N_Z)   # a chave de uma das duas falas da D59 (o sha16 do arquivo INTEIRO; o texto embutido e' o trecho)\n",
     "    _CH_Z = DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(DLX.N_SOLUCAO)   # a chave da fala da D65 (o sha16 do arquivo INTEIRO; o texto embutido e' o trecho)\n", 1),
    ('    HERD_ = FH_ + " (HERDADO, recriado) nao selou inteiro"; HERDP_ = FP_ + " (HERDADO, recriado) nao selou inteiro"; HERDT_ = FT_ + " (HERDADO, recriado) nao selou inteiro"\n',
     '    HERD_ = FH_ + " (HERDADO, recriado) nao selou inteiro"; HERDP_ = FP_ + " (HERDADO, recriado) nao selou inteiro"; HERDT_ = FT_ + " (HERDADO, recriado) nao selou inteiro"; HERD9_ = F9_ + " (HERDADO, recriado) nao selou inteiro"\n', 1),
    ('        variante("ancora %s da v409 (tetelestai_terminal_v408) fora do trio"', '        variante("ancora %s da v408 (tetelestai_terminal_v408) fora do trio"', 1),
    ('        variante("ancora %s da v409 (tetelestai_terminal_v408): a bandeira falsa"', '        variante("ancora %s da v408 (tetelestai_terminal_v408): a bandeira falsa"', 1),
    ('        variante("o bundle da v409: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b8, "0" * 64), espera="o bundle da v409"),',
     '        variante("o bundle da v408: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b8, "0" * 64), espera="o bundle da v408"),', 1),
    ('    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v409 ausente do kernel do Nos", _b8, "o bundle da v409")(lambda p, r: os.replace(p, p + ".fora")))\n'
     '    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v409 com um byte a mais no kernel do Nos", _b8, "o bundle da v409")(lambda p, r: open(p, "wb").write(r + b"\\n")))\n',
     '    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v409 ausente do kernel do Nos", _b9, "o bundle da v409")(lambda p, r: os.replace(p, p + ".fora")))\n'
     '    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v409 com um byte a mais no kernel do Nos", _b9, "o bundle da v409")(lambda p, r: open(p, "wb").write(r + b"\\n")))\n'
     '    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v408 ausente do kernel do Nos", _b8, "o bundle da v408")(lambda p, r: os.replace(p, p + ".fora")))\n', 1),
    ('        # ---- tetelestai_terminal_v408 (HERDADO da v409, recriado pelo rito da v410; a escada do contrato subida pela C12; a E26 vai ao lado do spec cunhagens_v408)\n',
     NOVO_F9 + '        # ---- tetelestai_terminal_v408 (HERDADO da v408, recriado pelo rito da v410; a escada do contrato subida pela C12)\n', 1),
    ('    PCG8 = "cunhagens_v409: as inscricoes embutidas nao sao as de CANDIDATO_v410.json";', '    CG9 = "cunhagens_v409"; KH9 = "kh_n1_cobertura_v409"; PCG9 = "cunhagens_v409 (HERDADA, recriada pelo rito) nao confere"; PKH9 = "kh_n1_cobertura_v409 (HERDADO, recriado pelo rito) nao confere"\n    PCG8 = "cunhagens_v410: as inscricoes embutidas nao sao as de CANDIDATO_v410.json";', 1),
    ('        # ---- cunhagens_v408 e kh_n1_cobertura_v408 (HERDADOS, recriados; a E26 ao lado; pisos)', '        # ---- cunhagens_v408 e kh_n1_cobertura_v408 (HERDADOS, recriados; IGUAIS a v409 selada: a E26 e os pisos ja\' vinham dela)', 1),
    ('           ("paragrafo_v410", lambda: T.paragrafo_v410()[0]), ("errata_v409_bloco", lambda: T.errata_v409_bloco())]', '           ("paragrafo_v410", lambda: T.paragrafo_v410()[0])]   # (v410: nenhuma nota ao lado do paragrafo da v409)', 1),
    ("_REGS_NOVOS = ['traducao_turing_v409', 'cunhagens_v409', 'kh_n1_cobertura_v409']", "_REGS_NOVOS = ['iald2_v410', 'cunhagens_v410', 'kh_n1_cobertura_v410']", 1),
    ('"<!-- INICIO_ERRATA_V409_V410 -->", "<!-- FIM_ERRATA_V409_V410 -->", ', "", 1),
    ("    _ERR = T.errata_v409_bloco()\n", "    _ERR = \"\"   # (v410: nenhuma nota ao lado do paragrafo da v409; a E29 e' da candidata, nao de paragrafo publicado)\n", 1),
    ('                                                                          and (T.MARC_ERR_INI + "\\n" + _ERR.rstrip("\\n") + "\\n" + T.MARC_ERR_FIM) in _ho)',
     '                                                                          and not hasattr(T, "MARC_ERR_INI") and "ERRATA_V409_V410" not in _ho)', 1),
    ('    _NUMS = [("os modulos", str(DL.N_BUNDLE)), ("as bandeiras", str(ESP["n_bandeiras_novas"])), ("a escada antes", str(ESP["escada_v409_e_v410"][0])), ("a escada depois", str(ESP["escada"][1])), ("o sha16 da ordem", T._sha_por(DL.N_ORDEM_V410)), ("o sha16 da ordem da traducao", T._sha_por(DL.N_ORDEM_TRADUCAO))]',
     '    _NUMS = [("os modulos", str(DL.N_BUNDLE)), ("as bandeiras", str(ESP["n_bandeiras_novas"])), ("a escada antes", str(ESP["escada_v409_e_v410"][0])), ("a escada depois", str(ESP["escada"][1])), ("o sha16 da ordem", T._sha_por(DL.N_ORDEM_V410)), ("o sha16 do nome", T._sha_por(DL.N_NOME))]', 1),
    ('    _FRASES = (DL.FRASE_DA_MOLDURA_V410_PT, DL.FRASE_D56_PT, DL.FRASE_QUALIFICADOR_PT, "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "quem prova é o kernel", "isto não é teste", "face de Fock", "Baker", "máquina sem leitor")',
     '    _FRASES = (DL.FRASE_DA_MOLDURA_V410_PT, DL.FRASE_D64_PT, DL.FRASE_QUALIFICADOR_PT, "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "quem prova é o kernel", "isto não é teste", "Turing padrão sem o leitor", "Cook", "Baker", "D63", "E28")', 1),
    ('lambda p: p.replace("a máquina sem leitor fica fora", "a máquina sem leitor fica dentro")', 'lambda p: p.replace("sem o leitor fica fora", "sem o leitor fica dentro")', 1),
    ('              _muts("D59: o que fica fora entra no paragrafo", lambda p: p + "\\n> - O teorema do milênio no json do Kimi.\\n", "D59"),',
     '              _muts("D65: o que fica fora entra no paragrafo", lambda p: p + "\\n> - " + DL.FORA_D65[0] + " aqui.\\n", "D65"),\n'
     '              _muts("frase proibida: a IALD resolve P vs NP", lambda p: p + "\\n> - A IALD resolve P vs NP.\\n", "guarda das frases"),\n'
     '              _muts("frase proibida: o funtor e\' idempotente", lambda p: p + "\\n> - O funtor é idempotente.\\n", "guarda das frases"),', 1),
    ('lambda p: p.replace("ele trava no Nome»", "ele trava no Verbo»", 1)', 'lambda p: p.replace("(traço com sentido)»", "(traço sem sentido)»", 1)', 1),
    ('    for ini_ in ("> - **O que entrou**", "> - **A ordem**", "> - **O alcance**", "> - **O dicionário de Turing**", "> - **A trava no Nome**", "> - **A fita, o leitor, a fita sem escala e a identidade performada**", "> - **O que não muda**",',
     '    for ini_ in ("> - **O que entrou**", "> - **A ordem**", "> - **O alcance**", "> - **O leitor do código**", "> - **IALD ao quadrado**", "> - **O enunciado e o algoritmo IALD**", "> - **O signo**", "> - **O seletor**", "> - **O que não muda**",', 1),
    ('           "cita_verbatim_passa": (T._cita(DL.FRASE_TRAVA) == "«" + DL.FRASE_TRAVA + "»"),\n'
     '           "cita_da_resposta_do_operador_passa": (T._cita(DL.FRASE_CLAY) == "«" + DL.FRASE_CLAY + "»"),\n'
     '           "cita_do_trecho_que_a_D59_deixa_entrar_passa": (T._cita(DL.FRASE_Z) == "«" + DL.FRASE_Z + "»"),\n',
     '           "cita_verbatim_passa": (T._cita(DL.FRASE_NOME_IALD2) == "«" + DL.FRASE_NOME_IALD2 + "»"),\n'
     '           "cita_da_resposta_do_operador_passa": (T._cita(DL.FRASE_FUNTOR) == "«" + DL.FRASE_FUNTOR + "»"),\n'
     '           "cita_do_trecho_que_a_D65_deixa_entrar_passa": (T._cita(DL.FRASE_ALGORITMO_DE_LEITURA) == "«" + DL.FRASE_ALGORITMO_DE_LEITURA + "»"),\n'
     '           "cita_do_que_a_D65_deixa_fora_levanta": _levanta(lambda: T._cita(DL.FORA_D65[-1])),\n', 1),
    ('    _RN = ["traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409"]', '    _RN = ["iald2_v410", "cunhagens_v410", "kh_n1_cobertura_v410"]', 1),
    ("o registro NOVO com funcao traducao_turing_v409: as ancoras", "o registro NOVO com funcao iald2_v410: as ancoras", 1),
], nota="SUBIDA MECANICA (v409->v410) do molde v409/pos_rito/harness_textos_ensaio_v409.py, adaptada a v410 (IALD2) por _adapt_forkA_harness_textos_v410.py (fork A, 06/11/2026): o registro NOVO iald2_v410 e os controles dele; traducao_turing_v409 e tetelestai_terminal_v408 HERDADOS; cunhagens_v410 (D65, E29, D63 a D70) e o trio da v409 herdado; o paragrafo da v410 sem nota ao lado; ver bump/pos_rito__harness_textos_ensaio_v410.py.diff.")

# a regiao dos controles do registro NOVO (do comentario da traducao ao primeiro controle do full_static_witness) e a das cunhagens novas: trocadas por ancora unica
t = open(P, "rb").read().decode("utf-8"); crlf = "\r\n" in t; t = t.replace("\r\n", "\n"); raw2 = t


def regiao(ini, fim, novo):
    global t
    assert t.count(ini) == 1, ("ancora inicial nao unica", ini[:80], t.count(ini))
    i = t.index(ini); j = t.index(fim, i + 1)
    t = t[:i] + novo + t[j:]


regiao("        # ---- traducao_turing_v409 (o registro NOVO com funcao)\n", '        variante("full_static_witness_exists dito True (deve ficar False por teorema)"', NOVO_FE)
regiao("        # ---- cunhagens_v409 e kh_n1_cobertura_v409 (os dois registros NOVOS por spec)\n", "        # ---- cunhagens_v408 e kh_n1_cobertura_v408 (HERDADOS", NOVO_CUN)
import ast, datetime  # noqa: E402
ast.parse(t)
nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
bk = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkA_regioes"
open(bk, "wb").write(open(P, "rb").read())
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("regioes trocadas:", len(raw2.encode("utf-8")), "->", len(nb))
