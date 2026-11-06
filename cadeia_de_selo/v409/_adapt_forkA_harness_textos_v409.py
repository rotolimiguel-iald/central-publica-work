# -*- coding: utf-8 -*-
"""_adapt_forkA_harness_textos_v409.py -- (claude-construtor-v409, fork A, 05/11/2026) adapta harness_textos_ensaio_v409.py (subida mecanica da v408) a v409, A TRADUCAO AS CLASSES DE TURING:
os controles negativos da leitura passam a mirar o registro NOVO traducao_turing_v409 (acervo repinado D57d, instancia de brinquedo, alcance D56, respostas de 05/11), ganham o bloco do tetelestai_terminal_v408 HERDADO,
o psion_canto_v407 HERDADO passa a ler as ancoras e o bundle da v407, cunhagens_v409/kh_n1_cobertura_v409 (E24 a E26, D55 a D60, a leitura de 05/11) e os HERDADOS cunhagens_v408 (E26 ao lado) e cunhagens_v407 (D57d ao lado);
os controles do paragrafo novo, a nota (E26), os marcadores e o veredito. Trocas com contagem exata (_adapt_util_v409.Arq: CRLF preservado, backup de BYTES)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("pos_rito/harness_textos_ensaio_v409.py")
ls = a.t.split("\n")
assert ls[1].startswith("# [A ADAPTAR v409]") and ls[2].startswith("# [ADAPTADO v409, 04/11/2026, claude-construtor-v409-r2") and ls[3].startswith("# parte2:")
ls[1] = ("# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 (fork A), a servico da gerencia c1] sobre a subida mecanica de rotulo da v408 FINAL (bump/pos_rito__harness_textos_ensaio_v409.py.diff fica como registro), por _adapt_forkA_harness_textos_v409.py: "
         "o conteudo e' o da v409 (A TRADUCAO AS CLASSES DE TURING: UM modulo novo, TraducaoTuring; o registro com funcao traducao_turing_v409; o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados; cunhagens_v409 e kh_n1_cobertura_v409; "
         "cunhagens_v408 com a E26 ao lado e cunhagens_v407 com a errata da D57(d) ao lado; o paragrafo novo, a nota E26 e o handoff).")
del ls[2:4]
a.t = "\n".join(ls)
# o docstring (so' o que descrevia o conteudo da v408)
a.troca_re(r"^\"\"\"harness_textos_ensaio_v409\.py -- o HARNESS DO POS-RITO da v409 em modo ENSAIO \(derivado do harness_textos_ensaio_v408\.py, que rodou na v408, e adaptado em 04/11/2026 a Tetelestai e o terminal: [^\n]*$",
           "\"\"\"harness_textos_ensaio_v409.py -- o HARNESS DO POS-RITO da v409 em modo ENSAIO (derivado do harness_textos_ensaio_v408.py, que rodou na v408, e adaptado em 05/11/2026 a traducao as classes de Turing: UM modulo novo, o registro traducao_turing_v409 e os herdados da v408, da v407 e da v406).")
a.troca_re(r"^  leitura        a leitura_v409\.ler\(\) REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS \(v409: o registro NOVO com funcao tetelestai_terminal_v408 [^\n]*$",
           "  leitura        a leitura_v409.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (v409: o registro NOVO com funcao traducao_turing_v409 [ausente, nao selado, checagem, valor, beta, veredito, as respostas do operador de 05/11, o pino do acervo da v407 (D57d), a instancia de brinquedo, o alcance (D56), as inscricoes,")
a.troca_re(r"^                 bandeira do bundle falsa, modulo adulterado ou ausente do kernel, as ressalvas, o podado\]; os registros HERDADOS psion_canto_v407 e fechamento_v406 [^\n]*$",
           "                 bandeira do bundle falsa, modulo adulterado ou ausente do kernel, as ressalvas]; os registros HERDADOS tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 [as mesmas recusas, mais as ancoras e os bundles de cada um]; cunhagens_v409 [falas de 05/11, D59, E24 a E26, D55 a D60, a leitura]; os HERDADOS cunhagens_v408 (E26 ao lado), cunhagens_v407 (D57d ao lado), kh_n1_cobertura_v408 e kh_n1_cobertura_v407;")
a.troca_re(r"^                 citacao nao verbatim, o 4,44 intruso, alegacao de seguranca criptografica, «consciencia» como termo, a direcao invertida, cada bullet removido\); a NOTA ao lado dos paragrafos anteriores \(E21 e a D51 revista\) [^\n]*$",
           "                 citacao nao verbatim, o 4,44 intruso, alegacao de seguranca criptografica, «consciencia» como termo, a direcao invertida, cada bullet removido); a NOTA ao lado do paragrafo da v408 (E26) e o handoff DIZ que os paragrafos anteriores seguem como estao;")
a.troca("e o PARAGRAFO NOVO (textos_v409.paragrafo_v409: Tetelestai e' o terminal) passa", "e o PARAGRAFO NOVO (textos_v409.paragrafo_v409: a traducao as classes de Turing) passa")

# ---------------------------------------------------------------- a preparacao dos controles da leitura
a.troca('FE_ = DLX.FECHO_REGISTRO; FP_ = "psion_canto_v407"; FH_ = "fechamento_v406";', 'FE_ = DLX.FECHO_REGISTRO; FT_ = DLX.D8.FECHO_REGISTRO; FP_ = "psion_canto_v407"; FH_ = "fechamento_v406";')
a.troca('    for a_n_ in (DLX.ANCORA_PRINCIPAL, DLX.ANCORA_TEMPO, DLX.ANCORA_PIGUALNP, ANC_[-1]):    # a ancora principal (tetelestai), a do tempo, a do «P = nP» e a ultima (as classes do dicionario): fora do trio, a bandeira falsa e o sha256 da fonte no hash formal adulterado',
        '    for a_n_ in list(dict.fromkeys((DLX.ANCORA_PRINCIPAL, DLX.ANCORAS_DE_SECAO[0], ANC_[-1]))):    # a ancora principal (p_igual_np_no_modo_selecao), a primeira de secao e a ultima: fora do trio, a bandeira falsa e o sha256 da fonte no hash formal adulterado')
a.troca('    _EST7 = ESP["estrelas_v408"]; _a7 = list(_EST7)[0]; _b7 = list(ESP["bundle_v408_sha256"])[0]   # o psion_canto_v407 HERDADO: as 76 ancoras e os 9 modulos da v408',
        '    _EST8 = ESP["estrelas_v408"]; _a8 = list(_EST8)[0]; _b8 = list(ESP["bundle_v408_sha256"])[0]   # o tetelestai_terminal_v408 HERDADO: as 48 ancoras e os 4 modulos da v408\n'
        '    _EST7 = ESP["estrelas_v407"]; _a7 = list(_EST7)[0]; _b7 = list(ESP["bundle_v407_sha256"])[0]   # o psion_canto_v407 HERDADO: as 76 ancoras e os 9 modulos da v407')
a.troca("    _N8, _N7, _N6 = len(ANC_), len(_EST7), len(_EST6)", "    _N9, _N8, _N7, _N6 = len(ANC_), len(_EST8), len(_EST7), len(_EST6)")
a.troca("    _CH_CLASSES = DLX.VERBATIM_CHAVE_PREFIXO_V409 + DLX._sha16_arq(DLX.N_CLASSES_PNP)   # a chave da correcao do operador sobre as classes (D51 revista), lida do arquivo",
        "    _CH_TRAD = DLX.VERBATIM_CHAVE_PREFIXO_V409 + DLX._sha16_arq(DLX.N_ORDEM_TRADUCAO)   # a chave da ordem do operador da traducao (05/11), lida do arquivo\n"
        "    _CH_Z = DLX.VERBATIM_CHAVE_PREFIXO_V409 + DLX._sha16_arq(DLX.N_Z)   # a chave de uma das duas falas da D59 (o sha16 do arquivo INTEIRO; o texto embutido e' o trecho)")
a.troca('    HERD_ = FH_ + " (HERDADO, recriado) nao selou inteiro"; HERDP_ = FP_ + " (HERDADO, recriado) nao selou inteiro"',
        '    HERD_ = FH_ + " (HERDADO, recriado) nao selou inteiro"; HERDP_ = FP_ + " (HERDADO, recriado) nao selou inteiro"; HERDT_ = FT_ + " (HERDADO, recriado) nao selou inteiro"')

# ---------------------------------------------------------------- o registro NOVO com funcao: traducao_turing_v409
a.troca("        # ---- tetelestai_terminal_v408 (o registro NOVO com funcao)", "        # ---- traducao_turing_v409 (o registro NOVO com funcao)")
VELHO_FE = (
    '        variante("%s: a resposta das classes do dicionario (D51 revista) ausente" % FE_, f_core=lambda c: c[FE_]["values"]["respostas"].pop("p_igual_np_trata_das_classes_do_dicionario"), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: a integra do acervo dita pinada (E23)" % FE_, f_core=lambda c: c[FE_]["insumo_purgado"].update(integra_pinada=True), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: o insumo purgado com outro sha256" % FE_, f_core=lambda c: c[FE_]["values"]["insumo_purgado"].update(sha256="0" * 64), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: uma inscricao de 04/11 nao conferida" % FE_, f_core=lambda c: c[FE_]["inscriptions"].update({sorted(c[FE_]["inscriptions"])[0]: False}), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: a correcao das classes (D51 revista) fora das inscricoes" % FE_, f_core=lambda c: c[FE_]["inscriptions"].pop(_CH_CLASSES), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: um nome provisorio de volta" % FE_, f_core=lambda c: c[FE_].update(nome_provisorio="Dicionario"), espera=FE_ + " nao selou inteiro"),\n')
NOVO_FE = (
    '        variante("%s: a resposta do modo selecao ausente" % FE_, f_core=lambda c: c[FE_]["values"]["respostas"].pop("o_np_e_o_modo_selecao"), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: a integra do acervo da v407 dita pinada (D57d)" % FE_, f_core=lambda c: c[FE_]["acervo_v407_repinado"].update(integra_pinada=True), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: o pino do acervo da v407 com outro sha256" % FE_, f_core=lambda c: c[FE_]["acervo_v407_repinado"].update(sha256="0" * 64), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: a instancia NAO com solucao" % FE_, f_core=lambda c: c[FE_]["values"]["instancia_nao"].update(solucoes=1), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: a instancia SIM sem solucao" % FE_, f_core=lambda c: c[FE_]["values"]["instancia_sim"].update(solucoes=0), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: o alcance sem o relativo ao leitor" % FE_, f_core=lambda c: c[FE_]["alcance"].update(frase="P = nP vale para as maquinas de Turing"), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: uma inscricao de 05/11 nao conferida" % FE_, f_core=lambda c: c[FE_]["inscriptions"].update({sorted(c[FE_]["inscriptions"])[0]: False}), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: a ordem da traducao fora das inscricoes" % FE_, f_core=lambda c: c[FE_]["inscriptions"].pop(_CH_TRAD), espera=FE_ + " nao selou inteiro"),\n'
    '        variante("%s: as ancoras de secao adulteradas" % FE_, f_core=lambda c: c[FE_]["ancoras_de_secao"].pop(), espera=FE_ + " nao selou inteiro"),\n')
a.troca(VELHO_FE, NOVO_FE)
a.troca('        variante("%s: a ancora principal dita outra" % FE_, f_core=lambda c: c[FE_].update(ancora_principal="TGLExt.TetelestaiTerminal.outra"), espera=FE_ + " nao selou inteiro"),',
        '        variante("%s: a ancora principal dita outra" % FE_, f_core=lambda c: c[FE_].update(ancora_principal="TGLExt.TraducaoTuring.outra"), espera=FE_ + " nao selou inteiro"),')
a.troca('        variante("%s: o podado vazio (a regra provar ou podar sem o que foi podado)" % FE_, f_core=lambda c: c[FE_].update(podado=[]), espera=FE_ + " nao selou inteiro"),\n', "")
a.troca('c[FE_].update(guarda_violacoes=[["F34", "x"]])', 'c[FE_].update(guarda_violacoes=[["F37", "x"]])')
a.troca('variante("uma bandeira do bundle (ext_tt408_*) falsa no kernel do rito"', 'variante("uma bandeira do bundle (ext_tu409_*) falsa no kernel do rito"')
a.troca('cj.update({"veredito_tetelestai_terminal": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FE_)', 'cj.update({"veredito_traducao_turing": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FE_)')
a.troca('        variante("selo primario: sem registros_v408", f_selo=lambda s: s.pop("registros_v408", None), espera=RESUMO_MSG),\n'
        '        variante("selo primario: registros_v408 do selo difere do core", f_selo=lambda s: s["registros_v408"][DLX.CUNHAGENS_REGISTRO].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),',
        '        variante("selo primario: sem registros_v409", f_selo=lambda s: s.pop("registros_v409", None), espera=RESUMO_MSG),\n'
        '        variante("selo primario: registros_v409 do selo difere do core", f_selo=lambda s: s["registros_v409"][DLX.CUNHAGENS_REGISTRO].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),')
a.troca('        variante("linha [v408] ausente do stdout", f_std=lambda t_: "\\n".join(l for l in t_.splitlines() if "[v408] o registro do terminal e os registros por spec da v409" not in l) + "\\n", espera="linha [v408]"),\n'
        '        variante("linha [v408] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v408] o registro do terminal e os registros por spec da v409"), espera="a linha [v408] do stdout"),\n'
        '        variante("linha do bloco TETELESTAI E\' O TERMINAL: uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N8, _N8), "ancoras ok = %d/%d" % (_N8 - 1, _N8)), espera=FE_ + " nao selou inteiro"),\n'
        '        variante("AVISO da v409 (o terminal nao rodou) no stdout", f_std=lambda t_: t_ + "   [v408] AVISO: o registro do terminal ou os registros por spec da v409 nao rodaram: ValueError(\'x\')\\n", espera="AVISO da v409"),\n',
        '        variante("linha [v409] ausente do stdout", f_std=lambda t_: "\\n".join(l for l in t_.splitlines() if "[v409] o registro da traducao e os registros por spec da v409" not in l) + "\\n", espera="linha [v409]"),\n'
        '        variante("linha [v409] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v409] o registro da traducao e os registros por spec da v409"), espera="a linha [v409] do stdout"),\n'
        '        variante("linha do bloco A TRADUCAO AS CLASSES DE TURING: uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N9, _N9), "ancoras ok = %d/%d" % (_N9 - 1, _N9)), espera=FE_ + " nao selou inteiro"),\n'
        '        variante("AVISO da v409 (a traducao nao rodou) no stdout", f_std=lambda t_: t_ + "   [v409] AVISO: o registro da traducao ou os registros por spec da v409 nao rodaram: ValueError(\'x\')\\n", espera="AVISO da v409"),\n')

# ---------------------------------------------------------------- o tetelestai_terminal_v408 HERDADO (bloco novo, antes do psion)
a.troca("        # ---- psion_canto_v407 (HERDADO da v408, recriado pelo rito da v409; a escada do contrato subida pela C12)\n",
        "        # ---- tetelestai_terminal_v408 (HERDADO da v408, recriado pelo rito da v409; a escada do contrato subida pela C12; a E26 vai ao lado do spec cunhagens_v408)\n"
        '        variante("%s (herdado) ausente do core" % FT_, f_core=lambda c: c.pop(FT_, None), espera="registro obrigatorio ausente do core: " + FT_),\n'
        '        variante("%s (herdado): o registro nao selou" % FT_, f_core=lambda c: c[FT_].update(all_verified=False), espera=FT_ + " nao selou"),\n'
        '        variante("%s (herdado): uma checagem do calculo falhou" % FT_, f_core=lambda c: c[FT_]["mechanics"]["checks"][2].update(ok=False), espera=HERDT_),\n'
        '        variante("%s (herdado): o numero de checagens != o do delta da v408" % FT_, f_core=lambda c: c[FT_]["mechanics"]["checks"].pop(), espera=HERDT_),\n'
        '        variante("%s (herdado): o numero de modulos ok adulterado" % FT_, f_core=lambda c: c[FT_]["values"].update(n_modulos_ok=DLX.D8.N_BUNDLE - 1), espera=HERDT_),\n'
        '        variante("%s (herdado): a escada do registro != a do ensaio" % FT_, f_core=lambda c: c[FT_]["values"].update(escada=[1, 1, 1]), espera=HERDT_),\n'
        '        variante("%s (herdado): beta != alfa x raiz de e do core" % FT_, f_core=lambda c: c[FT_]["values"].update(beta=0.0121), espera=HERDT_),\n'
        '        variante("%s (herdado): veredito diferente do esperado" % FT_, f_core=lambda c: c[FT_].update(verdict="OUTRO_VEREDITO"), espera=FT_ + VER_HERD),\n'
        '        variante("%s (herdado): as ressalvas adulteradas" % FT_, f_core=lambda c: c[FT_]["ressalvas"].pop(), espera=HERDT_),\n'
        '        variante("%s (herdado): o registro move o gate" % FT_, f_core=lambda c: c[FT_].update(does_not_gate_core=False), espera=HERDT_),\n'
        '        variante("%s (herdado): o calculo do runtime nao rodou" % FT_, f_core=lambda c: c[FT_].update(runtime_executed=False), espera=HERDT_),\n'
        '        variante("ancora %s da v408 (tetelestai_terminal_v408) fora do trio" % _a8.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _a8), espera="as ancoras do tetelestai_terminal_v408 (herdadas)"),\n'
        '        variante("ancora %s da v408 (tetelestai_terminal_v408): a bandeira falsa" % _a8.split(".")[-1], f_core=lambda c: _kf(c).__setitem__(_EST8[_a8]["bandeira"], False), espera="as ancoras do tetelestai_terminal_v408 (herdadas)"),\n'
        '        variante("o bundle da v408: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b8, "0" * 64), espera="o bundle da v408"),\n'
        '        variante("a conferencia traz outro veredito de %s (herdado)" % FT_, f_conf=lambda cj: cj.update({"veredito_tetelestai_terminal": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FT_),\n'
        '        variante("selo primario: sem o resumo de %s (herdado)" % FT_, f_selo=lambda s: s.pop(FT_, None), espera=RESUMO_MSG),\n'
        '        variante("selo primario: o resumo de %s (herdado) difere do core" % FT_, f_selo=lambda s: s[FT_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),\n'
        '        variante("selo primario: sem registros_v408", f_selo=lambda s: s.pop("registros_v408", None), espera=RESUMO_MSG),\n'
        '        variante("selo primario: registros_v408 do selo difere do core", f_selo=lambda s: s["registros_v408"]["cunhagens_v408"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),\n'
        '        variante("linha `>>> veredito <<<` de %s (herdado) ausente do stdout" % FT_, f_std=lambda t_: "\\n".join(l for l in t_.splitlines() if L._ev(ESP, FT_) not in l) + "\\n", espera="o bloco " + FT_ + " do stdout"),\n'
        '        variante("linha [v408] ausente do stdout", f_std=lambda t_: "\\n".join(l for l in t_.splitlines() if "[v408] o registro do terminal e os registros por spec da v408" not in l) + "\\n", espera="linha [v408]"),\n'
        '        variante("linha [v408] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v408] o registro do terminal e os registros por spec da v408"), espera="a linha [v408] do stdout"),\n'
        '        variante("linha do bloco TETELESTAI E\' O TERMINAL (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N8, _N8), "ancoras ok = %d/%d" % (_N8 - 1, _N8)), espera=HERDT_),\n'
        '        variante("AVISO da v408 herdada (o terminal nao rodou) no stdout", f_std=lambda t_: t_ + "   [v408] AVISO: o registro do terminal ou os registros por spec da v408 nao rodaram: ValueError(\'x\')\\n", espera="AVISO da v409"),\n'
        "        # ---- psion_canto_v407 (HERDADO da v407, recriado pelo rito da v409; a escada do contrato subida pela C12)\n")

# ---------------------------------------------------------------- o psion_canto_v407 HERDADO: as ancoras e o bundle da v407
a.troca('variante("ancora %s da v408 (psion_canto_v407) fora do trio" % _a7.split(".")[-1]', 'variante("ancora %s da v407 (psion_canto_v407) fora do trio" % _a7.split(".")[-1]')
a.troca('variante("ancora %s da v408 (psion_canto_v407): a bandeira falsa" % _a7.split(".")[-1]', 'variante("ancora %s da v407 (psion_canto_v407): a bandeira falsa" % _a7.split(".")[-1]')
a.troca('        variante("o bundle da v408: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b7, "0" * 64), espera="o bundle da v408"),',
        '        variante("o bundle da v407: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b7, "0" * 64), espera="o bundle da v407"),')
a.troca('"[v407] o registro do psion e do canto e os registros por spec da v408"', '"[v407] o registro do psion e do canto e os registros por spec da v407"', n=2)
a.troca('"   [v407] AVISO: o registro do psion e do canto ou os registros por spec da v408 nao rodaram: ValueError(\'x\')\\n"', '"   [v407] AVISO: o registro do psion e do canto ou os registros por spec da v407 nao rodaram: ValueError(\'x\')\\n"')
a.troca('variante("AVISO da v408 herdada (o psion e o canto nao rodou) no stdout"', 'variante("AVISO da v407 herdada (o psion e o canto nao rodou) no stdout"')

# ---------------------------------------------------------------- os arquivos do bundle no disco: a v409 tem UM modulo; a v408 e a v407 ficam como registro
a.troca('    NEG.append(_pedra_no_disco("o arquivo do modulo %s ausente do kernel do Nos" % _B8[1].split("/")[-1][:-5], lambda p, r: os.replace(p, p + ".fora"), 1))\n'
        '    NEG.append(_pedra_no_disco("o arquivo do ultimo modulo do bundle (%s) ausente do kernel do Nos" % _B8[-1].split("/")[-1][:-5], lambda p, r: os.replace(p, p + ".fora"), len(_B8) - 1))\n', "")
a.troca('    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v408 ausente do kernel do Nos", _b7, "o bundle da v408")(lambda p, r: os.replace(p, p + ".fora")))\n'
        '    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v408 com um byte a mais no kernel do Nos", _b7, "o bundle da v408")(lambda p, r: open(p, "wb").write(r + b"\\n")))\n',
        '    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v408 ausente do kernel do Nos", _b8, "o bundle da v408")(lambda p, r: os.replace(p, p + ".fora")))\n'
        '    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v408 com um byte a mais no kernel do Nos", _b8, "o bundle da v408")(lambda p, r: open(p, "wb").write(r + b"\\n")))\n'
        '    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v407 ausente do kernel do Nos", _b7, "o bundle da v407")(lambda p, r: os.replace(p, p + ".fora")))\n')

# ---------------------------------------------------------------- cunhagens_v409 / kh_n1_cobertura_v409 (NOVOS) e os herdados cunhagens_v408 (E26) e cunhagens_v407 (D57d)
a.troca('    CG8 = DLX.CUNHAGENS_REGISTRO; KH8 = DLX.KH_REGISTRO; CG_ = "cunhagens_v407"; KH7 = "kh_n1_cobertura_v407"\n'
        '    PCG8 = "cunhagens_v408: as inscricoes embutidas nao sao as de CANDIDATO_v409.json"; PCG7 = "cunhagens_v407 (HERDADA, recriada pelo rito) nao confere"; PKH7 = "kh_n1_cobertura_v407 (HERDADO, recriado pelo rito) nao confere"',
        '    CG8 = DLX.CUNHAGENS_REGISTRO; KH8 = DLX.KH_REGISTRO; CG_ = "cunhagens_v407"; KH7 = "kh_n1_cobertura_v407"; CGH8 = "cunhagens_v408"; KHH8 = "kh_n1_cobertura_v408"   # (CG8/KH8 sao os NOVOS da v409: o rotulo ficou da subida)\n'
        '    PCG8 = "cunhagens_v409: as inscricoes embutidas nao sao as de CANDIDATO_v409.json"; PCG7 = "cunhagens_v407 (HERDADA, recriada pelo rito) nao confere"; PKH7 = "kh_n1_cobertura_v407 (HERDADO, recriado pelo rito) nao confere"\n'
        '    PCGH8 = "cunhagens_v408 (HERDADA, recriada pelo rito) nao confere"; PKHH8 = "kh_n1_cobertura_v408 (HERDADO, recriado pelo rito) nao confere"')
a.troca("        # ---- cunhagens_v408 e kh_n1_cobertura_v408 (os dois registros NOVOS por spec)", "        # ---- cunhagens_v409 e kh_n1_cobertura_v409 (os dois registros NOVOS por spec)")
a.troca('        variante("%s: a correcao das classes (D51 revista) fora das inscricoes" % CG8, f_core=lambda c: c[CG8]["verbatim"].pop(_CH_CLASSES), espera=PCG8),\n',
        '        variante("%s: a ordem da traducao fora das inscricoes" % CG8, f_core=lambda c: c[CG8]["verbatim"].pop(_CH_TRAD), espera=PCG8),\n'
        '        variante("%s: uma fala da D59 com o sha256 do arquivo INTEIRO no lugar do trecho" % CG8, f_core=lambda c: c[CG8]["verbatim"][_CH_Z].update(sha256=_CH_Z[len(DLX.VERBATIM_CHAVE_PREFIXO_V409):] + "0" * 48), espera=PCG8),\n')
a.troca('espera="cunhagens_v408: as inscricoes de 04/11 tem de ser TODAS falas do operador"),', 'espera="cunhagens_v409: as inscricoes de 05/11 tem de ser TODAS falas do operador"),')
a.troca('espera="cunhagens_v408: as erratas E21 a E23"),', 'espera="cunhagens_v409: as erratas E24 a E26"),', n=4)
a.troca('        variante("%s: a E21 adulterada" % CG8, f_core=lambda c: c[CG8]["erratas"][0].update(agora="mantida"), espera="cunhagens_v409: as erratas E24 a E26"),',
        '        variante("%s: a E24 adulterada" % CG8, f_core=lambda c: c[CG8]["erratas"][0].update(agora="mantida"), espera="cunhagens_v409: as erratas E24 a E26"),')
a.troca('        variante("%s: a decisao D49 ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D49"), espera="cunhagens_v408: as decisoes D48 a D54"),\n'
        '        variante("%s: a decisao D51 (revista) ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D51"), espera="cunhagens_v408: as decisoes D48 a D54"),\n'
        '        variante("%s: a decisao D51 de volta a redacao podada" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].update(D51="a igualdade das classes P e NP segue podada"), espera="cunhagens_v408: as decisoes D48 a D54"),\n'
        '        variante("%s: a leitura de 04/11 dita REAL inteira" % CG8, f_core=lambda c: c[CG8]["extras"]["leituras"].update(estatuto="[REAL]"), espera="cunhagens_v408: a leitura [INPUT] de 04/11"),\n'
        '        variante("%s: a leitura ausente" % CG8, f_core=lambda c: c[CG8]["extras"].pop("leituras"), espera="cunhagens_v408: a leitura [INPUT] de 04/11"),\n'
        '        variante("%s: uma ressalva a menos" % CG8, f_core=lambda c: c[CG8]["extras"]["ressalvas"].pop(), espera="cunhagens_v408: a leitura [INPUT] de 04/11"),\n',
        '        variante("%s: a decisao D55 ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D55"), espera="cunhagens_v409: as decisoes D55 a D60"),\n'
        '        variante("%s: a decisao D56 (o alcance) adulterada" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].update(D56="P = nP vale para as maquinas de Turing"), espera="cunhagens_v409: as decisoes D55 a D60"),\n'
        '        variante("%s: a decisao D59 ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D59"), espera="cunhagens_v409: as decisoes D55 a D60"),\n'
        '        variante("%s: a leitura de 05/11 dita REAL inteira" % CG8, f_core=lambda c: c[CG8]["extras"]["leituras"].update(estatuto="[REAL]"), espera="cunhagens_v409: a leitura [INPUT] de 05/11"),\n'
        '        variante("%s: a leitura ausente" % CG8, f_core=lambda c: c[CG8]["extras"].pop("leituras"), espera="cunhagens_v409: a leitura [INPUT] de 05/11"),\n'
        '        variante("%s: uma ressalva a menos" % CG8, f_core=lambda c: c[CG8]["extras"]["ressalvas"].pop(), espera="cunhagens_v409: a leitura [INPUT] de 05/11"),\n')
a.troca('        variante("%s: a negativa de que «P = nP» trate das classes nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o P = nP nao trata das classes"]), espera="a MOLDURA falhou"),\n',
        '        variante("%s: a negativa de que «P = nP» trate das classes nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o P = nP nao trata das classes"]), espera="a MOLDURA falhou"),\n'
        '        variante("%s: a traducao a Turing dita [OPEN] (a D51 da v408) nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + [DLX.FRASE_D51_PT]), espera="a MOLDURA falhou"),\n'
        '        variante("%s: o problema do Clay dado por resolvido nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o problema do Clay esta resolvido"]), espera="a MOLDURA falhou"),\n')
a.troca('espera="kh_n1_cobertura_v408 nao selou como o ensaio a seco"),', 'espera="kh_n1_cobertura_v409 nao selou como o ensaio a seco"),')
a.troca("        # ---- cunhagens_v407 e kh_n1_cobertura_v407 (HERDADOS, recriados; a E21 ao lado; pisos)\n",
        "        # ---- cunhagens_v408 e kh_n1_cobertura_v408 (HERDADOS, recriados; a E26 ao lado; pisos)\n"
        '        variante("%s (herdada) nao selou" % CGH8, f_core=lambda c: c[CGH8].update(all_verified=False), espera=CGH8 + " nao selou"),\n'
        '        variante("%s (herdado) nao selou" % KHH8, f_core=lambda c: c[KHH8].update(all_verified=False), espera=KHH8 + " nao selou"),\n'
        '        variante("%s (herdada) ausente do core" % CGH8, f_core=lambda c: c.pop(CGH8, None), espera="registro obrigatorio ausente do core: " + CGH8),\n'
        '        variante("%s (herdada): veredito diferente do esperado" % CGH8, f_core=lambda c: c[CGH8].update(verdict="OUTRO_VEREDITO"), espera=CGH8 + VER_HERD),\n'
        '        variante("%s (herdada): uma inscricao deixou de estar embutida" % CGH8, f_core=lambda c: list(c[CGH8]["verbatim"].values())[0].update(embedded_ok=False), espera=PCGH8),\n'
        '        variante("%s (herdada): uma inscricao a menos" % CGH8, f_core=lambda c: c[CGH8]["verbatim"].pop(sorted(c[CGH8]["verbatim"])[0]), espera=PCGH8),\n'
        '        variante("%s (herdada): a errata E26 ao lado ausente" % CGH8, f_core=lambda c: c[CGH8]["erratas"].pop(), espera=PCGH8),\n'
        '        variante("%s (herdada): a E21 adulterada" % CGH8, f_core=lambda c: c[CGH8]["erratas"][0].update(agora="mantida"), espera=PCGH8),\n'
        '        variante("%s (herdado): uma checagem do registro falhou" % KHH8, f_core=lambda c: c[KHH8]["checks"][0].update(ok=False), espera=PKHH8),\n'
        '        variante("%s (herdado): a errata ao lado dos pisos ausente" % KHH8, f_core=lambda c: c[KHH8]["erratas"].pop(), espera=PKHH8),\n'
        "        # ---- cunhagens_v407 e kh_n1_cobertura_v407 (HERDADOS, recriados; a errata da D57(d) ao lado)\n")
a.troca('        variante("%s (herdada): a errata ao lado (E21) ausente" % CG_, f_core=lambda c: c[CG_]["erratas"].pop(), espera=PCG7),',
        '        variante("%s (herdada): a errata ao lado (D57d) ausente" % CG_, f_core=lambda c: c[CG_]["erratas"].pop(), espera=PCG7),')
a.troca('        variante("%s (herdado): a errata ao lado dos pisos ausente" % KH7, f_core=lambda c: c[KH7]["erratas"].pop(), espera=PKH7),\n', "")   # (v409: kh_n1_cobertura_v407 fica IGUAL ao da v408 selada; a errata dos pisos dele e' da v408)
a.troca('variante("%s: a frase proibida «unico autovetor» nos limites do registro do terminal" % FE_', 'variante("%s: a frase proibida «unico autovetor» nos limites do registro da traducao" % FE_')

# ---------------------------------------------------------------- os textos: os registros novos, os marcadores do handoff
a.troca("_REGS_NOVOS = ['tetelestai_terminal_v408', 'cunhagens_v408', 'kh_n1_cobertura_v408']", "_REGS_NOVOS = ['traducao_turing_v409', 'cunhagens_v409', 'kh_n1_cobertura_v409']")
a.troca('"<!-- INICIO_PARAGRAFO_TETELESTAI_v409 -->", "<!-- FIM_PARAGRAFO_TETELESTAI_v409 -->"', 'T.MARC_V409_INI, T.MARC_V409_FIM')
a.troca('    _RN = ["tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408"]', '    _RN = ["traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409"]')

# ---------------------------------------------------------------- o paragrafo novo e a nota E26
a.troca("# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (Tetelestai e' o terminal): verificacao propria, controles negativos, a citacao verbatim, a NOTA ao lado dos paragrafos anteriores (E21 e a D51 revista)",
        "# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (a traducao as classes de Turing): verificacao propria, controles negativos, a citacao verbatim, a NOTA ao lado do paragrafo da v408 (E26)")
a.troca('all(x in _ERR for x in ("E21", "NÃO foram editados", "fica como registro", "D51 revista"))', 'all(x in _ERR for x in ("E26", "NÃO foram editados", "fica como registro", "relativo ao leitor", "máquina sem leitor"))')
a.troca('("o sha16 da ordem", T._sha_por(DL.N_ORDEM_V409)), ("o sha16 dos nomes", T._sha_por(DL.N_NOMES)), ("o sha16 da correcao das classes", T._sha_por(DL.N_CLASSES_PNP))]',
        '("o sha16 da ordem", T._sha_por(DL.N_ORDEM_V409)), ("o sha16 da ordem da traducao", T._sha_por(DL.N_ORDEM_TRADUCAO))]')
a.troca("    for _pn in [p_[\"name\"] for p_ in DL.PEDRAS_V409]:   # cada um dos quatro nomes do operador trocado", "    for _pn in [p_[\"name\"] for p_ in DL.PEDRAS_V409]:   # o nome do modulo (da gerencia, ratificado pelo operador) trocado")
a.troca('    _FRASES = (DL.FRASE_DA_MOLDURA_V409_PT, DL.FRASE_D51_PT, "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "quem prova é o kernel", "isto não é teste", "face de Fock", "classes de computação do dicionário do operador", "máquinas de Turing", "não recusa")',
        '    _FRASES = (DL.FRASE_DA_MOLDURA_V409_PT, DL.FRASE_D56_PT, DL.FRASE_QUALIFICADOR_PT, "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "quem prova é o kernel", "isto não é teste", "face de Fock", "Baker", "máquina sem leitor")')
a.troca('              _muts("a traducao a Turing dita no kernel", lambda p: p.replace("é [OPEN], não recusa", "está no kernel"), "frase de limite ausente"),   # (r2, 05/11: a frase (9) da R3 diz «é [OPEN], não recusa»)\n'
        '              _muts("o [OPEN] da traducao dito recusa", lambda p: p.replace("não recusa", "recusa"), "frase de limite ausente"),\n',
        '              _muts("o alcance sem o relativo ao leitor", lambda p: p.replace("relativo ao leitor", "XXXX"), "frase de limite ausente"),\n'
        '              _muts("a maquina sem leitor dita dentro", lambda p: p.replace("a máquina sem leitor fica fora", "a máquina sem leitor fica dentro"), "frase de limite ausente"),\n'
        '              _muts("frase proibida: o problema do Clay resolvido", lambda p: p + "\\n> - O problema do Clay está resolvido.\\n", "guarda das frases"),\n'
        '              _muts("frase proibida: a traducao a Turing dita [OPEN] (a D51 da v408)", lambda p: p + "\\n> - " + DL.FRASE_D51_PT + ".\\n", "guarda das frases"),\n'
        '              _muts("D59: o que fica fora entra no paragrafo", lambda p: p + "\\n> - O teorema do milênio no json do Kimi.\\n", "D59"),\n')
a.troca('              _muts("citacao do operador que nao e\' verbatim", lambda p: p.replace("trata das classes de computação sim»", "trata das classes de computação talvez»", 1), "NAO e\' verbatim"),\n'
        '              _muts("o estatuto DECLARADO removido", lambda p: p.replace("DECLARADO", "XX"), "estatuto ausente"),',
        '              _muts("citacao do operador que nao e\' verbatim", lambda p: p.replace("ele trava no Nome»", "ele trava no Verbo»", 1), "NAO e\' verbatim"),\n'
        '              _muts("o estatuto KNOWN removido", lambda p: p.replace("KNOWN", "XX"), "estatuto ausente"),')
a.troca('    for ini_ in ("> - **O que entrou**", "> - **O terminal é a leitura**", "> - **O tempo é a moeda de β**", "> - **O ponto de contradição e as classes do dicionário**", "> - **A correção do operador sobre as classes**", "> - **O que não muda**", "> - **As ressalvas, ditas**", "> - **O que o registro NÃO diz**", "> - **Limites:**", "> - **Origem.")',
        '    for ini_ in ("> - **O que entrou**", "> - **A ordem**", "> - **O alcance**", "> - **O dicionário de Turing**", "> - **A trava no Nome**", "> - **A fita, o leitor, a fita sem escala e a identidade performada**", "> - **O que não muda**", "> - **As ressalvas, ditas**", "> - **O que o registro NÃO diz**", "> - **Limites:**", "> - **Origem.")')
a.troca('           "cita_verbatim_passa": (T._cita(DL.FRASE_TERMINAL) == "«" + DL.FRASE_TERMINAL + "»"),\n'
        '           "cita_com_aspas_do_operador_passa": (T._cita(DL.FRASE_INCLINACAO) == "«" + DL.FRASE_INCLINACAO + "»"),\n'
        '           "cita_do_paragrafo_do_operador_num_arquivo_de_autor_misto_passa": (T._cita(DL.FRASE_FACE_FOCK) == "«" + DL.FRASE_FACE_FOCK + "»"),',
        '           "cita_verbatim_passa": (T._cita(DL.FRASE_TRAVA) == "«" + DL.FRASE_TRAVA + "»"),\n'
        '           "cita_da_resposta_do_operador_passa": (T._cita(DL.FRASE_CLAY) == "«" + DL.FRASE_CLAY + "»"),\n'
        '           "cita_do_trecho_que_a_D59_deixa_entrar_passa": (T._cita(DL.FRASE_Z) == "«" + DL.FRASE_Z + "»"),')
a.troca("    print(\"  paragrafo novo (Tetelestai e' o terminal): positivo ok;", "    print(\"  paragrafo novo (a traducao as classes de Turing): positivo ok;")

# ---------------------------------------------------------------- o veredito do harness
a.troca_re(r'^R\["veredito"\] = \("TUDO PASSOU: o conferidor da v409 \(16 itens C1-C16 e o round trip\) bate no Nos emulado, a leitura le sem problema e reprova os controles negativos \(o registro NOVO com funcao tetelestai_terminal_v408: [^\n]*$',
           'R["veredito"] = ("TUDO PASSOU: o conferidor da v409 (16 itens C1-C16 e o round trip) bate no Nos emulado, a leitura le sem problema e reprova os controles negativos (o registro NOVO com funcao traducao_turing_v409: as ancoras da pedra, o modulo, as bandeiras, a escada, as respostas do operador de 05/11, '
           'o pino do acervo da v407 (D57d), a instancia de brinquedo, o alcance (D56), as inscricoes, as chaves antigas, o que fica False por teorema; o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados, com as ancoras e os bundles deles; '
           'cunhagens_v409 com as 10 falas de 05/11 (de duas, so\' o trecho da D59), as erratas E24 a E26 e a dos pisos, as decisoes D55 a D60, a leitura de 05/11 e as ressalvas; kh_n1_cobertura_v409; cunhagens_v408 (E26 ao lado), kh_n1_cobertura_v408, cunhagens_v407 (D57d ao lado), '
           'kh_n1_cobertura_v407, cunhagens_v406 e kh_n1_cobertura_v406 HERDADOS; os registros recriados, as pedras seladas no kernel e o gate sem se mover; as linhas [v409] a [v397] e a do sidecar do stdout), os textos renderizam e a guarda P18 e a guarda das frases estao limpas, a custodia G1 le o bloco da linhagem e o handoff, '
           'os dois paragrafos do README/site (o do quadro, intocado, e o novo da v409) e a nota E26 passam nas verificacoes, as superficies rodam em copias, o b3_recibo e o mapa montam sem registrar")')
a.grava()
