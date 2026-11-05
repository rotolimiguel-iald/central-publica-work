# -*- coding: utf-8 -*-
"""_adapt_harness_textos_v408.py -- (claude-construtor-v408-r2, a servico da gerencia c1, 04/11/2026, noite) adapta harness_textos_ensaio_v408.py (subida mecanica de rotulo da v407 FINAL)
ao conteudo da v408. PARTE 1 (`parte1`): os CONTROLES NEGATIVOS DA LEITURA, retargetados ao desenho da v408 e as mensagens da leitura_v408.py (fork A + r2):
  o registro NOVO com funcao tetelestai_terminal_v408 (ausente, nao selado, checagem, valores, beta, veredito, as respostas do operador [a das classes do dicionario, D51 revista],
  o insumo purgado [E23], as inscricoes [a correcao das classes], o nome provisorio, as chaves antigas, a ancora principal, as ressalvas, o podado, o gate, o runtime, a guarda; a bandeira ext_tt408_*;
  a conferencia, o selo primario, o stdout [v408]); o psion_canto_v407 e o fechamento_v406 HERDADOS (as mesmas recusas, com as mensagens de herdado; as ancoras e os bundles de cada um);
  cunhagens_v408 / kh_n1_cobertura_v408 (novos) e cunhagens_v407 / kh_n1_cobertura_v407 (herdados). PARTE 2 (`parte2`): os textos, os paragrafos e o cabecalho (depois de textos_v408.py).
Substituicao por SPAN entre ancoras unicas (as linhas inteiras), com contagem conferida; backup de bytes antes; ast.parse no fim. Nenhum controle e' retirado sem outro no lugar.
Uso: python -I -B -X utf8 _adapt_harness_textos_v408.py parte1|parte2"""
import datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(HERE, "harness_textos_ensaio_v408.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

NOVO_A = r'''    FE_ = DLX.FECHO_REGISTRO; FP_ = "psion_canto_v407"; FH_ = "fechamento_v406"; FJ_ = rdj(os.path.join(PKG, "kernel", "FLAGS_v408.json")); ANC_ = list(DLX.ANCORAS); FLAGS_ = [f_[0] for f_ in FJ_["flags"]]
    RESUMO_MSG = "o selo primario (um_absoluto_selo.json) nao traz os resumos"
    VER_HERD = ": o veredito do rito difere do esperado"   # a mensagem da leitura para os registros HERDADOS (REG_V407D, REG_V406D): o esperado e' o da v407 selada, ou o do ensaio a seco se na troca dita

    def _kf(c):
        return c["kernel_formalization"]

    def _fora_do_trio(c, termo):
        _kf(c)["axiom_report"][termo] = ["propext", "sorryAx"]

    def _std_selados(t_, trecho):
        return "\n".join(re.sub(r"\(selados \d+\)", "(selados 0)", l) if trecho in l else l for l in t_.splitlines()) + "\n"

    for a_n_ in (DLX.ANCORA_PRINCIPAL, DLX.ANCORA_TEMPO, DLX.ANCORA_PIGUALNP, ANC_[-1]):    # a ancora principal (tetelestai), a do tempo, a do «P = nP» e a ultima (as classes do dicionario): fora do trio, a bandeira falsa e o sha256 da fonte no hash formal adulterado
        curto_ = a_n_.split(".")[-1]; fl_a_ = FJ_["ancoras"][a_n_]["flag"]; rel_a_ = DLX.ANCORAS[a_n_]["rel"]
        NEG.extend([variante("ancora %s fora do trio" % curto_, f_core=lambda c, t=a_n_: _fora_do_trio(c, t), espera="a ancora "), variante("ancora %s: a bandeira falsa" % curto_, f_core=lambda c, f=fl_a_: _kf(c).__setitem__(f, False), espera="a ancora "),
                    variante("ancora %s: sha256 da fonte do modulo no hash formal adulterado" % curto_, f_core=lambda c, r=rel_a_: _kf(c)["formal_files_sha256"].__setitem__(r, "0" * 64), espera="a ancora ")])
    _EST7 = ESP["estrelas_v407"]; _a7 = list(_EST7)[0]; _b7 = list(ESP["bundle_v407_sha256"])[0]   # o psion_canto_v407 HERDADO: as 76 ancoras e os 9 modulos da v407
    _EST6 = ESP["estrelas_v406"]; _a6 = list(_EST6)[0]; _b6 = list(ESP["bundle_v406_sha256"])[0]; _ft6 = ESP["flags_true_v407"][len(ESP["flags_true_v407"]) // 2]   # o fechamento_v406 HERDADO: as oito ancoras e os 301 modulos da v406
    _N8, _N7, _N6 = len(ANC_), len(_EST7), len(_EST6)
    _CH_CLASSES = DLX.VERBATIM_CHAVE_PREFIXO_V408 + DLX._sha16_arq(DLX.N_CLASSES_PNP)   # a chave da correcao do operador sobre as classes (D51 revista), lida do arquivo

    def _bundle_anterior_no_disco(nome, rel_, msg_):
        """controle sobre o ARQUIVO de um modulo do bundle de uma versao ANTERIOR no kernel do Nos emulado (ausente ou com um byte a mais): a leitura tem de recusar; o arquivo e' restaurado byte a byte"""
        def _f(f_muda):
            pth = os.path.join(NOSE, "tgl_kernel", *rel_.split("/")); raw_ = open(pth, "rb").read()
            try:
                f_muda(pth, raw_)
                _, PV = L.ler()
            finally:
                if os.path.exists(pth + ".fora"):
                    os.remove(pth + ".fora")
                open(pth, "wb").write(raw_)
            return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": any(msg_ in x for x in PV), "problemas": [x[:140] for x in PV][:3]}
        return _f
    HERD_ = FH_ + " (HERDADO, recriado) nao selou inteiro"; HERDP_ = FP_ + " (HERDADO, recriado) nao selou inteiro"
    NEG.extend([
        # ---- tetelestai_terminal_v408 (o registro NOVO com funcao)
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
        variante("%s: a resposta das classes do dicionario (D51 revista) ausente" % FE_, f_core=lambda c: c[FE_]["values"]["respostas"].pop("p_igual_np_trata_das_classes_do_dicionario"), espera=FE_ + " nao selou inteiro"),
        variante("%s: a integra do acervo dita pinada (E23)" % FE_, f_core=lambda c: c[FE_]["insumo_purgado"].update(integra_pinada=True), espera=FE_ + " nao selou inteiro"),
        variante("%s: o insumo purgado com outro sha256" % FE_, f_core=lambda c: c[FE_]["values"]["insumo_purgado"].update(sha256="0" * 64), espera=FE_ + " nao selou inteiro"),
        variante("%s: uma inscricao de 04/11 nao conferida" % FE_, f_core=lambda c: c[FE_]["inscriptions"].update({sorted(c[FE_]["inscriptions"])[0]: False}), espera=FE_ + " nao selou inteiro"),
        variante("%s: a correcao das classes (D51 revista) fora das inscricoes" % FE_, f_core=lambda c: c[FE_]["inscriptions"].pop(_CH_CLASSES), espera=FE_ + " nao selou inteiro"),
        variante("%s: um nome provisorio de volta" % FE_, f_core=lambda c: c[FE_].update(nome_provisorio="Dicionario"), espera=FE_ + " nao selou inteiro"),
        variante("%s: uma chave antiga dita mudada" % FE_, f_core=lambda c: c[FE_].update(chaves_antigas_que_mudam=["rede_fock_v394.whole_certificate_inhabited"]), espera=FE_ + " nao selou inteiro"),
        variante("%s: a ancora principal dita outra" % FE_, f_core=lambda c: c[FE_].update(ancora_principal="TGLExt.TetelestaiTerminal.outra"), espera=FE_ + " nao selou inteiro"),
        variante("%s: as ressalvas adulteradas" % FE_, f_core=lambda c: c[FE_]["ressalvas"].pop(), espera=FE_ + " nao selou inteiro"),
        variante("%s: o podado vazio (a regra provar ou podar sem o que foi podado)" % FE_, f_core=lambda c: c[FE_].update(podado=[]), espera=FE_ + " nao selou inteiro"),
        variante("%s: o registro move o gate" % FE_, f_core=lambda c: c[FE_].update(does_not_gate_core=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: o calculo do runtime nao rodou" % FE_, f_core=lambda c: c[FE_].update(runtime_executed=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: a guarda das frases achou violacao no registro" % FE_, f_core=lambda c: c[FE_].update(guarda_violacoes=[["F34", "x"]]), espera=FE_ + " nao selou inteiro"),
        variante("uma bandeira do bundle (ext_tt408_*) falsa no kernel do rito", f_core=lambda c: _kf(c).__setitem__(FLAGS_[len(FLAGS_) // 2], False), espera="as bandeiras do fecho"),
        variante("a conferencia traz outro veredito de %s" % FE_, f_conf=lambda cj: cj.update({"veredito_tetelestai_terminal": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FE_),
        variante("selo primario: sem o resumo de %s" % FE_, f_selo=lambda s: s.pop(FE_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s difere do core" % FE_, f_selo=lambda s: s[FE_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v408", f_selo=lambda s: s.pop("registros_v408", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v408 do selo difere do core", f_selo=lambda s: s["registros_v408"][DLX.CUNHAGENS_REGISTRO].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % FE_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if ESP["vereditos_novos_v408"][FE_] not in l) + "\n", espera="o bloco " + FE_ + " do stdout"),
        variante("linha [v408] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v408] o registro do terminal e os registros por spec da v408" not in l) + "\n", espera="linha [v408]"),
        variante("linha [v408] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v408] o registro do terminal e os registros por spec da v408"), espera="a linha [v408] do stdout"),
        variante("linha do bloco TETELESTAI E' O TERMINAL: uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N8, _N8), "ancoras ok = %d/%d" % (_N8 - 1, _N8)), espera=FE_ + " nao selou inteiro"),
        variante("AVISO da v408 (o terminal nao rodou) no stdout", f_std=lambda t_: t_ + "   [v408] AVISO: o registro do terminal ou os registros por spec da v408 nao rodaram: ValueError('x')\n", espera="AVISO da v408"),
        variante("full_static_witness_exists dito True (deve ficar False por teorema)", f_core=lambda c: c["qg_closure"]["gate"].update(full_static_witness_exists=True), espera="full_static_witness_exists e trivial_inhabitant_exists devem seguir False"),
        variante("trivial_inhabitant_exists dito True (deve ficar False por teorema)", f_core=lambda c: c["witness_rigidity"].update(trivial_inhabitant_exists=True), espera="full_static_witness_exists e trivial_inhabitant_exists devem seguir False"),
        # ---- a CHAVE DO LEMA no registro da testemunha (v407, herdada): segue lida True do kernel, com o dict elo_v407
        variante("testemunha_estatica_v396: a chave do lema de volta a literal False", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"].update(linked_to_the_corner_by_a_lemma=False), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: o dict elo_v407 ausente", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"].pop("elo_v407"), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: o elo dito de VETORES (Omega identificado com o vetor de Bell)", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"]["elo_v407"].update(identifies_omega_with_bell_vector=True), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: o par na face de Fock dito provado", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"]["elo_v407"].update(pair_on_the_fock_face="PROVED"), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: a ponte Bell-TT dita termo", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"]["elo_v407"].update(bell_to_tt_bridge="A_TERM"), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("psibit_v395: o status antigo (CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE)", f_core=lambda c: c["psibit_v395"]["conditional_psion_face"].update(status="CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"), espera="psibit_v395: a face do psion nao le o habitante"),
        variante("a conferencia diz chave_do_lema != True", f_conf=lambda cj: cj.update({"chave_do_lema": False}), espera="chave_do_lema != True"),
        # ---- psion_canto_v407 (HERDADO da v407, recriado pelo rito da v408; a escada do contrato subida pela C12)
        variante("%s (herdado) ausente do core" % FP_, f_core=lambda c: c.pop(FP_, None), espera="registro obrigatorio ausente do core: " + FP_),
        variante("%s (herdado): o registro nao selou" % FP_, f_core=lambda c: c[FP_].update(all_verified=False), espera=FP_ + " nao selou"),
        variante("%s (herdado): uma checagem do calculo falhou" % FP_, f_core=lambda c: c[FP_]["mechanics"]["checks"][2].update(ok=False), espera=HERDP_),
        variante("%s (herdado): o numero de checagens != o do delta da v407" % FP_, f_core=lambda c: c[FP_]["mechanics"]["checks"].pop(), espera=HERDP_),
        variante("%s (herdado): o numero de modulos ok adulterado" % FP_, f_core=lambda c: c[FP_]["values"].update(n_modulos_ok=DLX.D7.N_BUNDLE - 1), espera=HERDP_),
        variante("%s (herdado): o numero de bandeiras True adulterado" % FP_, f_core=lambda c: c[FP_]["values"].update(n_flags_true=c[FP_]["values"]["n_flags"] - 1), espera=HERDP_),
        variante("%s (herdado): a escada do registro != a do ensaio" % FP_, f_core=lambda c: c[FP_]["values"].update(escada=[1, 1, 1]), espera=HERDP_),
        variante("%s (herdado): beta != alfa x raiz de e do core" % FP_, f_core=lambda c: c[FP_]["values"].update(beta=0.0121), espera=HERDP_),
        variante("%s (herdado): beta_ok falso" % FP_, f_core=lambda c: c[FP_].update(beta_ok=False), espera=HERDP_),
        variante("%s (herdado): veredito diferente do esperado" % FP_, f_core=lambda c: c[FP_].update(verdict="OUTRO_VEREDITO"), espera=FP_ + VER_HERD),
        variante("%s (herdado): o elo das duas faces dito NAO lido do kernel" % FP_, f_core=lambda c: c[FP_].update(link_read_from_the_kernel=False), espera=HERDP_),
        variante("%s (herdado): a chave do lema lida False no registro" % FP_, f_core=lambda c: c[FP_]["keys"].update({"testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma": False}), espera=HERDP_),
        variante("%s (herdado): o teste (d) deixou de ser so' citado" % FP_, f_core=lambda c: c[FP_]["teste_d"].update(so_citado=False), espera=HERDP_),
        variante("%s (herdado): as ressalvas adulteradas" % FP_, f_core=lambda c: c[FP_]["ressalvas"].pop(), espera=HERDP_),
        variante("%s (herdado): o registro move o gate" % FP_, f_core=lambda c: c[FP_].update(does_not_gate_core=False), espera=HERDP_),
        variante("%s (herdado): o calculo do runtime nao rodou" % FP_, f_core=lambda c: c[FP_].update(runtime_executed=False), espera=HERDP_),
        variante("%s (herdado): a guarda das frases achou violacao no registro" % FP_, f_core=lambda c: c[FP_].update(guarda_violacoes=[["F17", "x"]]), espera=HERDP_),
        variante("ancora %s da v407 (psion_canto_v407) fora do trio" % _a7.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _a7), espera="as ancoras do psion_canto_v407 (herdadas)"),
        variante("ancora %s da v407 (psion_canto_v407): a bandeira falsa" % _a7.split(".")[-1], f_core=lambda c: _kf(c).__setitem__(_EST7[_a7]["bandeira"], False), espera="as ancoras do psion_canto_v407 (herdadas)"),
        variante("o bundle da v407: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b7, "0" * 64), espera="o bundle da v407"),
        variante("a conferencia traz outro veredito de %s (herdado)" % FP_, f_conf=lambda cj: cj.update({"veredito_psion_herdado": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FP_),
        variante("selo primario: sem o resumo de %s (herdado)" % FP_, f_selo=lambda s: s.pop(FP_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s (herdado) difere do core" % FP_, f_selo=lambda s: s[FP_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v407", f_selo=lambda s: s.pop("registros_v407", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v407 do selo difere do core", f_selo=lambda s: s["registros_v407"]["cunhagens_v407"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("linha `>>> veredito <<<` de %s (herdado) ausente do stdout" % FP_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if L._ev(ESP, FP_) not in l) + "\n", espera="o bloco " + FP_ + " do stdout"),
        variante("linha [v407] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v407] o registro do psion e do canto e os registros por spec da v407" not in l) + "\n", espera="linha [v407]"),
        variante("linha [v407] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v407] o registro do psion e do canto e os registros por spec da v407"), espera="a linha [v407] do stdout"),
        variante("linha do bloco O PSION, O CANTO E O PAR (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N7, _N7), "ancoras ok = %d/%d" % (_N7 - 1, _N7)), espera=HERDP_),
        variante("linha do bloco O PSION, O CANTO E O PAR (herdado): chave do lema dita False", f_std=lambda t_: t_.replace("chave do lema (lida do kernel) = True", "chave do lema (lida do kernel) = False"), espera=HERDP_),
        variante("AVISO da v407 herdada (o psion e o canto nao rodou) no stdout", f_std=lambda t_: t_ + "   [v407] AVISO: o registro do psion e do canto ou os registros por spec da v407 nao rodaram: ValueError('x')\n", espera="AVISO da v408"),
        # ---- fechamento_v406 (HERDADO da v406, recriado pelo rito da v408, c8 versionada pela E20)
        variante("%s (herdado) ausente do core" % FH_, f_core=lambda c: c.pop(FH_, None), espera="registro obrigatorio ausente do core: " + FH_),
        variante("%s (herdado): o registro nao selou" % FH_, f_core=lambda c: c[FH_].update(all_verified=False), espera=FH_ + " nao selou"),
        variante("%s (herdado): uma checagem do calculo falhou" % FH_, f_core=lambda c: c[FH_]["mechanics"]["checks"][2].update(ok=False), espera=HERD_),
        variante("%s (herdado): a c8 versionada falhou" % FH_, f_core=lambda c: c[FH_]["mechanics"]["checks"][7].update(ok=False), espera=HERD_),
        variante("%s (herdado): o numero de checagens != o do delta da v406" % FH_, f_core=lambda c: c[FH_]["mechanics"]["checks"].pop(), espera=HERD_),
        variante("%s (herdado): o numero de modulos ok adulterado" % FH_, f_core=lambda c: c[FH_]["values"].update(n_modulos_ok=DLX.D6.N_BUNDLE - 1), espera=HERD_),
        variante("%s (herdado): o numero de bandeiras True adulterado" % FH_, f_core=lambda c: c[FH_]["values"].update(n_flags_true=c[FH_]["values"]["n_flags"] - 1), espera=HERD_),
        variante("%s (herdado): a escada do registro != a do ensaio" % FH_, f_core=lambda c: c[FH_]["values"].update(escada=[1, 1, 1]), espera=HERD_),
        variante("%s (herdado): beta != alfa x raiz de e do core" % FH_, f_core=lambda c: c[FH_]["values"].update(beta=0.0121), espera=HERD_),
        variante("%s (herdado): beta_ok falso" % FH_, f_core=lambda c: c[FH_].update(beta_ok=False), espera=HERD_),
        variante("%s (herdado): veredito diferente do esperado" % FH_, f_core=lambda c: c[FH_].update(verdict="OUTRO_VEREDITO"), espera=FH_ + VER_HERD),
        variante("%s (herdado): o certificado dito nao habitado" % FH_, f_core=lambda c: c[FH_].update(certificate_inhabited=False), espera=HERD_),
        variante("%s (herdado): uma chave de testemunha lida False no registro" % FH_, f_core=lambda c: c[FH_]["four_keys"].update({"rede_fock_v394.whole_certificate_inhabited": False}), espera=HERD_),
        variante("%s (herdado): a chave do lema lida False no registro" % FH_, f_core=lambda c: c[FH_]["four_keys"].update({"testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma": False}), espera=HERD_),
        variante("%s (herdado): as ressalvas adulteradas" % FH_, f_core=lambda c: c[FH_]["ressalvas"].pop(), espera=HERD_),
        variante("%s (herdado): o nome provisorio da candidata trocado" % FH_, f_core=lambda c: c[FH_].update(nome_provisorio_da_candidata="CanonicalFullTGLWitness"), espera=HERD_),
        variante("%s (herdado): o registro move o gate" % FH_, f_core=lambda c: c[FH_].update(does_not_gate_core=False), espera=HERD_),
        variante("%s (herdado): o calculo do runtime nao rodou" % FH_, f_core=lambda c: c[FH_].update(runtime_executed=False), espera=HERD_),
        variante("%s (herdado): a guarda das frases achou violacao no registro" % FH_, f_core=lambda c: c[FH_].update(guarda_violacoes=[["F17", "x"]]), espera=HERD_),
        variante("ancora %s da v406 (fechamento_v406) fora do trio" % _a6.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _a6), espera="as oito ancoras do fechamento_v406 (herdadas)"),
        variante("ancora %s da v406 (fechamento_v406): a bandeira falsa" % _a6.split(".")[-1], f_core=lambda c: _kf(c).__setitem__(_EST6[_a6]["bandeira"], False), espera="as oito ancoras do fechamento_v406 (herdadas)"),
        variante("uma bandeira True da v407 deixou de ser True", f_core=lambda c: _kf(c).__setitem__(_ft6, False), espera="alguma bandeira True da v407 deixou de ser True"),
        variante("o bundle da v406: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b6, "0" * 64), espera="o bundle da v406"),
        variante("selo primario: sem o resumo de %s (herdado)" % FH_, f_selo=lambda s: s.pop(FH_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s (herdado) difere do core" % FH_, f_selo=lambda s: s[FH_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v406", f_selo=lambda s: s.pop("registros_v406", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v406 do selo difere do core", f_selo=lambda s: s["registros_v406"]["cunhagens_v406"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("a conferencia traz outro veredito de %s (herdado)" % FH_, f_conf=lambda cj: cj.update({"veredito_fechamento_herdado": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FH_),
        variante("linha `>>> veredito <<<` de %s (herdado) ausente do stdout" % FH_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if L._ev(ESP, FH_) not in l) + "\n", espera="o bloco " + FH_ + " do stdout"),
        variante("linha [v406] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v406] o fechamento e os registros por spec da v406" not in l) + "\n", espera="linha [v406]"),
        variante("linha [v406] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v406] o fechamento e os registros por spec da v406"), espera="a linha [v406] do stdout"),
        variante("linha do bloco O FECHAMENTO (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N6, _N6), "ancoras ok = %d/%d" % (_N6 - 1, _N6)), espera=HERD_),
        variante("AVISO da v406 herdada (o fechamento nao rodou) no stdout", f_std=lambda t_: t_ + "   [v406] AVISO: o fechamento ou os registros por spec da v406 nao rodaram: ValueError('x')\n", espera="AVISO da v408"),
    ])
    _B8 = list(ESP["bundle_sha256"])
    NEG.append(_pedra_no_disco("o arquivo do modulo %s (a ancora principal) ausente do kernel do Nos" % _B8[0].split("/")[-1][:-5], lambda p, r: os.replace(p, p + ".fora"), 0))
    NEG.append(_pedra_no_disco("o arquivo de um modulo do bundle da v408 com um byte a mais no kernel do Nos", lambda p, r: open(p, "wb").write(r + b"\n"), len(_B8) // 2))
    NEG.append(_pedra_no_disco("o arquivo do modulo %s ausente do kernel do Nos" % _B8[1].split("/")[-1][:-5], lambda p, r: os.replace(p, p + ".fora"), 1))
    NEG.append(_pedra_no_disco("o arquivo do ultimo modulo do bundle (%s) ausente do kernel do Nos" % _B8[-1].split("/")[-1][:-5], lambda p, r: os.replace(p, p + ".fora"), len(_B8) - 1))
    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v407 ausente do kernel do Nos", _b7, "o bundle da v407")(lambda p, r: os.replace(p, p + ".fora")))
    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v407 com um byte a mais no kernel do Nos", _b7, "o bundle da v407")(lambda p, r: open(p, "wb").write(r + b"\n")))
    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v406 ausente do kernel do Nos", _b6, "o bundle da v406")(lambda p, r: os.replace(p, p + ".fora")))
'''

NOVO_B = r'''    CG8 = DLX.CUNHAGENS_REGISTRO; KH8 = DLX.KH_REGISTRO; CG_ = "cunhagens_v407"; KH7 = "kh_n1_cobertura_v407"
    PCG8 = "cunhagens_v408: as inscricoes embutidas nao sao as de CANDIDATO_v408.json"; PCG7 = "cunhagens_v407 (HERDADA, recriada pelo rito) nao confere"; PKH7 = "kh_n1_cobertura_v407 (HERDADO, recriado pelo rito) nao confere"
    CG6 = "cunhagens_v406"; KH6 = "kh_n1_cobertura_v406"; PCG6 = "cunhagens_v406 (HERDADA, recriada pelo rito) nao confere"; PKH6 = "kh_n1_cobertura_v406 (HERDADO, recriado pelo rito) nao confere"
    NEG.extend([
        # ---- cunhagens_v408 e kh_n1_cobertura_v408 (os dois registros NOVOS por spec)
        variante("%s nao selou" % CG8, f_core=lambda c: c[CG8].update(all_verified=False), espera=CG8 + " nao selou"),
        variante("%s nao selou" % KH8, f_core=lambda c: c[KH8].update(all_verified=False), espera=KH8 + " nao selou"),
        variante("%s ausente do core" % CG8, f_core=lambda c: c.pop(CG8, None), espera="registro obrigatorio ausente do core: " + CG8),
        variante("%s ausente do core" % KH8, f_core=lambda c: c.pop(KH8, None), espera="registro obrigatorio ausente do core: " + KH8),
        variante("%s: veredito diferente do ensaio a seco" % CG8, f_core=lambda c: c[CG8].update(verdict="OUTRO_VEREDITO"), espera=CG8 + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: veredito diferente do ensaio a seco" % KH8, f_core=lambda c: c[KH8].update(verdict="OUTRO_VEREDITO"), espera=KH8 + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: uma inscricao deixou de estar embutida" % CG8, f_core=lambda c: list(c[CG8]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG8),
        variante("%s: sha256 de uma inscricao adulterado" % CG8, f_core=lambda c: list(c[CG8]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG8),
        variante("%s: uma inscricao a menos" % CG8, f_core=lambda c: c[CG8]["verbatim"].pop(sorted(c[CG8]["verbatim"])[0]), espera=PCG8),
        variante("%s: a correcao das classes (D51 revista) fora das inscricoes" % CG8, f_core=lambda c: c[CG8]["verbatim"].pop(_CH_CLASSES), espera=PCG8),
        variante("%s: uma inscricao rotulada como da gerencia" % CG8, f_core=lambda c: c[CG8]["extras"]["autores"].update({sorted(c[CG8]["extras"]["autores"])[0]: "gerencia"}), espera="cunhagens_v408: as inscricoes de 04/11 tem de ser TODAS falas do operador"),
        variante("%s: falta uma errata" % CG8, f_core=lambda c: c[CG8]["erratas"].pop(), espera="cunhagens_v408: as erratas E21 a E23"),
        variante("%s: erratas ausentes" % CG8, f_core=lambda c: c[CG8].update(erratas=[]), espera="cunhagens_v408: as erratas E21 a E23"),
        variante("%s: a E21 adulterada" % CG8, f_core=lambda c: c[CG8]["erratas"][0].update(agora="mantida"), espera="cunhagens_v408: as erratas E21 a E23"),
        variante("%s: uma errata sem a assinatura da gerencia c1" % CG8, f_core=lambda c: c[CG8]["erratas"][1].update(assinatura="operador"), espera="cunhagens_v408: as erratas E21 a E23"),
        variante("%s: a decisao D49 ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D49"), espera="cunhagens_v408: as decisoes D48 a D54"),
        variante("%s: a decisao D51 (revista) ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D51"), espera="cunhagens_v408: as decisoes D48 a D54"),
        variante("%s: a decisao D51 de volta a redacao podada" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].update(D51="a igualdade das classes P e NP segue podada"), espera="cunhagens_v408: as decisoes D48 a D54"),
        variante("%s: a leitura de 04/11 dita REAL inteira" % CG8, f_core=lambda c: c[CG8]["extras"]["leituras"].update(estatuto="[REAL]"), espera="cunhagens_v408: a leitura [INPUT] de 04/11"),
        variante("%s: a leitura ausente" % CG8, f_core=lambda c: c[CG8]["extras"].pop("leituras"), espera="cunhagens_v408: a leitura [INPUT] de 04/11"),
        variante("%s: uma ressalva a menos" % CG8, f_core=lambda c: c[CG8]["extras"]["ressalvas"].pop(), espera="cunhagens_v408: a leitura [INPUT] de 04/11"),
        variante("%s: a frase proibida nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["agora tudo derivado"]), espera="a MOLDURA falhou"),
        variante("%s: a TGL dada como prova de P = NP de Turing nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["a TGL prova P = NP de Turing"]), espera="a MOLDURA falhou"),
        variante("%s: a negativa de que «P = nP» trate das classes nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o P = nP nao trata das classes"]), espera="a MOLDURA falhou"),
        variante("%s: uma checagem do registro falhou" % KH8, f_core=lambda c: c[KH8]["checks"][0].update(ok=False), espera="kh_n1_cobertura_v408 nao selou como o ensaio a seco"),
        # ---- cunhagens_v407 e kh_n1_cobertura_v407 (HERDADOS, recriados; a E21 ao lado; pisos)
        variante("%s (herdada) nao selou" % CG_, f_core=lambda c: c[CG_].update(all_verified=False), espera=CG_ + " nao selou"),
        variante("%s (herdado) nao selou" % KH7, f_core=lambda c: c[KH7].update(all_verified=False), espera=KH7 + " nao selou"),
        variante("%s (herdada) ausente do core" % CG_, f_core=lambda c: c.pop(CG_, None), espera="registro obrigatorio ausente do core: " + CG_),
        variante("%s (herdado) ausente do core" % KH7, f_core=lambda c: c.pop(KH7, None), espera="registro obrigatorio ausente do core: " + KH7),
        variante("%s (herdada): veredito diferente do esperado" % CG_, f_core=lambda c: c[CG_].update(verdict="OUTRO_VEREDITO"), espera=CG_ + VER_HERD),
        variante("%s (herdado): veredito diferente do esperado" % KH7, f_core=lambda c: c[KH7].update(verdict="OUTRO_VEREDITO"), espera=KH7 + VER_HERD),
        variante("%s (herdada): uma inscricao deixou de estar embutida" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG7),
        variante("%s (herdada): sha256 de uma inscricao adulterado" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG7),
        variante("%s (herdada): uma inscricao a menos" % CG_, f_core=lambda c: c[CG_]["verbatim"].pop(sorted(c[CG_]["verbatim"])[0]), espera=PCG7),
        variante("%s (herdada): a errata ao lado (E21) ausente" % CG_, f_core=lambda c: c[CG_]["erratas"].pop(), espera=PCG7),
        variante("%s (herdada): a E18 adulterada" % CG_, f_core=lambda c: c[CG_]["erratas"][0].update(agora="mantida"), espera=PCG7),
        variante("%s (herdado): uma checagem do registro falhou" % KH7, f_core=lambda c: c[KH7]["checks"][0].update(ok=False), espera=PKH7),
        variante("%s (herdado): a errata ao lado dos pisos ausente" % KH7, f_core=lambda c: c[KH7]["erratas"].pop(), espera=PKH7),
        variante("%s: a frase proibida «unico autovetor» nos limites do registro do terminal" % FE_, f_core=lambda c: c[FE_].update(limites=c[FE_]["limites"] + ["o unico autovetor da luz"]), espera="a MOLDURA falhou"),
'''


def _span(t, ini, fim, novo, rotulo):
    assert t.count(ini) == 1 and t.count(fim) == 1, ("ancora do span nao e' unica", rotulo, t.count(ini), t.count(fim))
    a = t.index(ini); b = t.index(fim)
    assert a < b, ("ancoras do span fora de ordem", rotulo)
    return t[:a] + novo + t[b:]


def parte1():
    b = open(ALVO, "rb").read(); t = b.decode("utf-8")
    assert "\r\n" not in t
    t = _span(t, '    FE_ = "psion_canto_v407"; FH_ = "fechamento_v406"; FJ_ = rdj(', "    # a errata de F2b (registro com FUNCAO, sem pedra): cada elo recusa visivelmente\n", NOVO_A, "fecho")
    t = _span(t, '    CG_ = "cunhagens_v407"; PCG = "cunhagens_v407: as inscricoes embutidas nao sao as de CANDIDATO_v408.json"\n', "        # ---- cunhagens_v406 e kh_n1_cobertura_v406 (HERDADOS", NOVO_B, "cunhagens")
    for proibido in ('FE_ = "psion_canto_v407"', "_bundle407_no_disco", "ext_psi407_*", 'PCG = "cunhagens_v407'):
        assert proibido not in t, ("sobrou texto da subida mecanica", proibido)
    compile(t, ALVO, "exec")
    bak = ALVO + ".bak_" + TS + "_parte1"
    open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    tmp = ALVO + ".tmp"; open(tmp, "wb").write(t.encode("utf-8")); assert os.path.getsize(tmp) > len(b) - 5000
    os.replace(tmp, ALVO)
    print("ok parte1: harness_textos_ensaio_v408.py %d -> %d B; sha16 %s; backup %s" % (len(b), os.path.getsize(ALVO), hashlib.sha256(open(ALVO, "rb").read()).hexdigest()[:16], os.path.basename(bak)))


CAB_NOVO = ("# [ADAPTADO v408, 04/11/2026, claude-construtor-v408-r2, a servico da gerencia c1] sobre a subida mecanica de rotulo da v407 FINAL (bump/pos_rito__harness_textos_ensaio_v408.py.diff fica como registro) por _adapt_harness_textos_v408.py (parte1: os controles negativos da leitura;\n"
            "# parte2: os textos, o paragrafo novo, as superficies e este cabecalho): o conteudo e' o da v408 (TETELESTAI E' O TERMINAL: bundle de 4 modulos, o registro com funcao tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados, nenhuma chave antiga muda); a gerencia revisa antes do rito.\n")
P2 = [
    ('"""harness_textos_ensaio_v408.py -- o HARNESS DO POS-RITO da v408 em modo ENSAIO (derivado do harness_textos_ensaio_v407.py, que rodou na v407, e adaptado em 03/11/2026 ao psion, ao canto e ao par: o bundle de 9 modulos, o registro psion_canto_v407, o fechamento_v406 HERDADO, a chave do lema lida do kernel)',
     '"""harness_textos_ensaio_v408.py -- o HARNESS DO POS-RITO da v408 em modo ENSAIO (derivado do harness_textos_ensaio_v407.py, que rodou na v407, e adaptado em 04/11/2026 a Tetelestai e o terminal: o bundle de 4 modulos, o registro tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS, nenhuma chave antiga muda)', 1),
    ("_REGS_NOVOS = ['psion_canto_v407', 'cunhagens_v407', 'kh_n1_cobertura_v407']", "_REGS_NOVOS = ['tetelestai_terminal_v408', 'cunhagens_v408', 'kh_n1_cobertura_v408']", 1),
    ('"<!-- INICIO_PARAGRAFO_O_PSION_v408 -->", "<!-- FIM_PARAGRAFO_O_PSION_v408 -->"', '"<!-- INICIO_PARAGRAFO_TETELESTAI_v408 -->", "<!-- FIM_PARAGRAFO_TETELESTAI_v408 -->"', 1),
    ('all(x in _ERR for x in ("E18", "NÃO foram editados", "fica como registro"))', 'all(x in _ERR for x in ("E21", "NÃO foram editados", "fica como registro", "D51 revista"))', 1),
    ('("o sha16 da ordem", T._sha_por(DL.N_ORDEM_B89)), ("o sha16 das decisoes", T._sha_por(DL.N_RATIFICA)), ("o sha16 do par", T._sha_por(DL.N_PAR))]',
     '("o sha16 da ordem", T._sha_por(DL.N_ORDEM_V408)), ("o sha16 dos nomes", T._sha_por(DL.N_NOMES)), ("o sha16 da correcao das classes", T._sha_por(DL.N_CLASSES_PNP))]', 1),
    ('    _NEGS.append(_muts("o nome da pedra PsionCanto trocado", lambda p: p.replace("`" + DL.TESTEMUNHA["name"] + "`", "`" + DL.TESTEMUNHA["name"][:-1] + "2`"), "ausente do paragrafo"))\n'
     '    _NEGS.append(_muts("o nome da pedra Par trocado", lambda p: p.replace("`Par`", "`Pax`"), "ausente do paragrafo"))\n',
     '    for _pn in [p_["name"] for p_ in DL.PEDRAS_V408]:   # cada um dos quatro nomes do operador trocado\n'
     '        _NEGS.append(_muts("o nome da pedra %s trocado" % _pn, lambda p, n_=_pn: p.replace("`" + n_ + "`", "`" + n_[:-1] + "Z`"), "ausente do paragrafo"))\n', 1),
    ('    _FRASES = (DL.FRASE_DA_MOLDURA_V408_PT, "validade no kernel nao e creditacao", "o gate nao se move", "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "K(O)", "II_inf", "ENNReal", "quem prova é o kernel", "isto não é teste", "lema", "FACE DE FOCK", "NAO e\' termo", "ESTRUTURA")',
     '    _FRASES = (DL.FRASE_DA_MOLDURA_V408_PT, DL.FRASE_D51_PT, "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "quem prova é o kernel", "isto não é teste", "face de Fock", "classes de computação do dicionário do operador", "máquinas de Turing", "não uma recusa")', 1),
    ('    _NEGS += [_muts("a creditacao dita pela validade", lambda p: p.replace("validade no kernel nao e creditacao", "validade no kernel e creditacao"), "frase de limite ausente"),\n'
     '              _muts("o gate dito movido", lambda p: p.replace("o gate nao se move", "o gate se move"), "frase de limite ausente"),\n'
     '              _muts("a ponte Bell-TT dita termo", lambda p: p.replace("NAO e\' termo", "e\' termo"), "frase de limite ausente"),\n'
     '              _muts("o elo dito de vetores (sem ESTRUTURA)", lambda p: p.replace("ESTRUTURA", "VETORES"), "frase de limite ausente"),\n',
     '    _NEGS += [_muts("a creditacao dita pela validade", lambda p: p.replace("validade no kernel não é creditação", "validade no kernel é creditação"), "frase de limite ausente"),\n'
     '              _muts("o gate dito movido", lambda p: p.replace("o gate não se move", "o gate se move"), "frase de limite ausente"),\n'
     '              _muts("a traducao a Turing dita no kernel", lambda p: p.replace("não está no kernel", "está no kernel"), "frase de limite ausente"),\n'
     '              _muts("o [OPEN] da traducao dito recusa", lambda p: p.replace("não uma recusa", "uma recusa"), "frase de limite ausente"),\n'
     '              _muts("frase proibida: a TGL prova P = NP de Turing", lambda p: p + "\\n> - E a TGL prova P = NP de Turing.\\n", "guarda das frases"),\n'
     '              _muts("frase proibida: relacao sem peso afirmada", lambda p: p + "\\n> - Agora há relação sem peso.\\n", "guarda das frases"),\n'
     '              _muts("frase proibida: a negativa de que P = nP trate das classes", lambda p: p + "\\n> - O P = nP não trata das classes.\\n", "guarda das frases"),\n', 1),
    ('              _muts("citacao do operador que nao e\' verbatim", lambda p: p.replace("também já pode ser derivado»", "também já foi derivado»", 1), "NAO e\' verbatim"),\n',
     '              _muts("citacao do operador que nao e\' verbatim", lambda p: p.replace("trata das classes de computação sim»", "trata das classes de computação talvez»", 1), "NAO e\' verbatim"),\n', 1),
    ('              _muts("o estatuto KNOWN removido", lambda p: p.replace("KNOWN", "XX"), "estatuto ausente"),\n'
     '              _muts("o estatuto ONTO removido", lambda p: p.replace("ONTO", "XX"), "estatuto ausente"),\n', '', 1),
    ('    for ini_ in ("> - **O que entrou**", "> - **O lema das duas faces**", "> - **A ordem do operador**", "> - **O par**", "> - **O que não muda**", "> - **O teste (d)**", "> - **As ressalvas, ditas**", "> - **O que o registro NÃO diz**", "> - **Limites:**", "> - **Origem."):',
     '    for ini_ in ("> - **O que entrou**", "> - **O terminal é a leitura**", "> - **O tempo é a moeda de β**", "> - **O ponto de contradição e as classes do dicionário**", "> - **A correção do operador sobre as classes**", "> - **O que não muda**", "> - **As ressalvas, ditas**", "> - **O que o registro NÃO diz**", "> - **Limites:**", "> - **Origem."):', 1),
    ('           "cita_verbatim_passa": (T._cita(DL.FRASE_LEMA_PSION) == "«" + DL.FRASE_LEMA_PSION + "»"),\n'
     '           "cita_com_aspas_do_operador_passa": (T._cita(DL.FRASE_PROSSIGAMOS) == "«" + DL.FRASE_PROSSIGAMOS + "»"),\n',
     '           "cita_verbatim_passa": (T._cita(DL.FRASE_TERMINAL) == "«" + DL.FRASE_TERMINAL + "»"),\n'
     '           "cita_com_aspas_do_operador_passa": (T._cita(DL.FRASE_INCLINACAO) == "«" + DL.FRASE_INCLINACAO + "»"),\n'
     '           "cita_do_paragrafo_do_operador_num_arquivo_de_autor_misto_passa": (T._cita(DL.FRASE_FACE_FOCK) == "«" + DL.FRASE_FACE_FOCK + "»"),\n'
     '           "cita_do_texto_da_outra_instancia_levanta": _levanta(lambda: T._cita("Operador. A chave girou.")),\n', 1),
    ('    print("  paragrafo novo (o psion, o canto e o par): positivo ok;', '    print("  paragrafo novo (Tetelestai e\' o terminal): positivo ok;', 1),
    ('# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (O psion, o canto e o par): verificacao propria, controles negativos, a citacao verbatim, a NOTA ao lado dos paragrafos anteriores (E18)',
     '# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (Tetelestai e\' o terminal): verificacao propria, controles negativos, a citacao verbatim, a NOTA ao lado dos paragrafos anteriores (E21 e a D51 revista)', 1),
    ('    _RN = ["psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407"]', '    _RN = ["tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408"]', 1),
    ("(o registro NOVO com funcao psion_canto_v407: as 76 ancoras, os 9 modulos, as 98 bandeiras, a escada, a chave do lema de volta a False, o dict elo_v407, as quatro chaves da v407, o que fica False por teorema, o teste (d) so' citado; o fechamento_v406 HERDADO e recriado com as oito ancoras, os 301 modulos e as 1794 bandeiras da v407; cunhagens_v407 com as erratas E18 a E20, as decisoes D41 a D47, a leitura de 03/11, as ressalvas e as falas; kh_n1_cobertura_v407; cunhagens_v406 e kh_n1_cobertura_v406 HERDADOS e versionados (E20);",
     "(o registro NOVO com funcao tetelestai_terminal_v408: as ancoras das quatro pedras, os 4 modulos, as bandeiras, a escada, as respostas do operador [a das classes do dicionario, D51 revista], o insumo purgado, as inscricoes, o nome provisorio, as chaves antigas, o que fica False por teorema; o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados, com as ancoras e os bundles deles; cunhagens_v408 com as 15 falas, as erratas E21 a E23 e a dos pisos, as decisoes D48 a D54, a leitura de 04/11 e as ressalvas; kh_n1_cobertura_v408; cunhagens_v407, kh_n1_cobertura_v407, cunhagens_v406 e kh_n1_cobertura_v406 HERDADOS;", 1),
    ("os dois paragrafos do README/site (o do quadro e o da v408: o psion, o canto e o par)", "os dois paragrafos do README/site (o do quadro e o da v408: Tetelestai e' o terminal)", 1),
]


def parte2():
    b = open(ALVO, "rb").read(); t = b.decode("utf-8")
    L = t.split("\n")
    assert L[1].startswith("# [A ADAPTAR v408]") and L[2].startswith("# [ADAPTADO v408, 03/11/2026]"), [l[:40] for l in L[:3]]
    t = "\n".join([L[0]] + CAB_NOVO.rstrip("\n").split("\n") + L[3:])
    for i, (a, z, n) in enumerate(P2):
        c = t.count(a)
        assert c == n, ("parte2: o trecho %d aparece %d vez(es), esperado %d" % (i, c, n), a[:120])
        t = t.replace(a, z)
    for proibido in ("[A ADAPTAR v408]", "N_ORDEM_B89", "FRASE_LEMA_PSION", "INICIO_PARAGRAFO_O_PSION"):
        assert proibido not in t, ("sobrou texto da subida mecanica", proibido)
    compile(t, ALVO, "exec")
    bak = ALVO + ".bak_" + TS + "_parte2"
    open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    tmp = ALVO + ".tmp"; open(tmp, "wb").write(t.encode("utf-8")); assert os.path.getsize(tmp) > len(b) - 5000
    os.replace(tmp, ALVO)
    print("ok parte2: harness_textos_ensaio_v408.py %d -> %d B; sha16 %s; backup %s" % (len(b), os.path.getsize(ALVO), hashlib.sha256(open(ALVO, "rb").read()).hexdigest()[:16], os.path.basename(bak)))


if __name__ == "__main__":
    {"parte1": parte1, "parte2": parte2}[sys.argv[1]]()
