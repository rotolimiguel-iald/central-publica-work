# -*- coding: utf-8 -*-
"""_adapt_harness_textos_v407.py -- adapta harness_textos_ensaio_v407.py (subida mecanica da v406) ao conteudo da v407. PARTE 1: os CONTROLES NEGATIVOS DA LEITURA (psion_canto_v407, fechamento_v406 herdado, cunhagens_v407,
cunhagens_v406 e kh_n1_cobertura_v406 herdados, bundle de 9 modulos, chave do lema). A PARTE 2 (os textos, os paragrafos, as superficies) depende de textos_v407.py e e' feita depois (rodar com `parte2`).
Uso: python -B -X utf8 _adapt_harness_textos_v407.py [parte1|parte2]   (so' o proprio arquivo e' tocado; backup de bytes antes)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adaptar_pos_rito_v407 as M

NOME = "harness_textos_ensaio_v407.py"

LEITURA_BULLET = r'''  leitura        a leitura_v407.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (v407: o registro NOVO com funcao psion_canto_v407 [ausente, nao selado, checagem, valor, beta, veredito, o elo dito nao lido, a chave do lema de volta a False, o dict elo_v407 adulterado, ancora fora do trio ou sem bandeira,
                 bandeira do bundle falsa, modulo adulterado ou ausente do kernel, as ressalvas, o teste (d) deixado de ser so' citado]; o registro HERDADO fechamento_v406 [as mesmas recusas, mais as oito ancoras, o bundle de 301 e as bandeiras da v406]; cunhagens_v407 [falas adulteradas, erratas E18 a E20, decisoes D41 a D47, leitura, ressalvas, moldura] e kh_n1_cobertura_v407;
                 cunhagens_v406 e kh_n1_cobertura_v406 HERDADOS e versionados pela E20; os OITO registros com funcao da v406 selada, os da v404, da v403 e da v402 RECRIADOS e as treze pedras seladas no kernel; na F8.1 a familia ext_ls2_*, a checagem do rito V11,
                 o teste nulo cego, a sonda ProbeBlindNullAbsent e a letra do veredito do gate; a falsidade da inercia e as cunhagens da v401 e da v399 recriadas; o sidecar ausente ou adulterado, os resumos do selo primario, quadro do topo que deixa de selar ou de estar no topo, C5, C15, C16, o round trip,
                 registros da v398 a v393 nao selados, AVISO da v407 ou de bloco anterior, linhas [v407], [v406], [v405], [v404], [v403], [v402], [v401], [v399], [v398], [v397] e a linha do sidecar ausentes), cada um tem de reprovar;
'''

NEW_FJ = r'''    FE_ = "psion_canto_v407"; FH_ = "fechamento_v406"; FJ_ = rdj(os.path.join(PKG, "kernel", "FLAGS_v407.json")); ANC_ = list(DLX.ANCORAS)'''

NEW_A = r'''    for a_n_ in (DLX.ANCORA_LEMA, DLX.ANCORA_PAR, ANC_[-1]):    # o lema das duas faces (PsionCanto), o par (Par) e a ultima ancora: a ancora fora do trio, a bandeira falsa e o sha256 da fonte no hash formal adulterado
        curto_ = a_n_.split(".")[-1]; fl_a_ = FJ_["ancoras"][a_n_]["flag"]; rel_a_ = DLX.ANCORAS[a_n_]["rel"]
        NEG.extend([variante("ancora %s fora do trio" % curto_, f_core=lambda c, t=a_n_: _fora_do_trio(c, t), espera="a ancora "), variante("ancora %s: a bandeira falsa" % curto_, f_core=lambda c, f=fl_a_: _kf(c).__setitem__(f, False), espera="a ancora "),
                    variante("ancora %s: sha256 da fonte do modulo no hash formal adulterado" % curto_, f_core=lambda c, r=rel_a_: _kf(c)["formal_files_sha256"].__setitem__(r, "0" * 64), espera="a ancora ")])
    _EST6 = ESP["estrelas_v406"]; _a6 = list(_EST6)[0]; _b6 = list(ESP["bundle_v406_sha256"])[0]; _ft6 = ESP["flags_true_v406"][len(ESP["flags_true_v406"]) // 2]

    def _bundle406_no_disco(nome, f_muda):
        """controle sobre o ARQUIVO de um dos 301 modulos do bundle da v406 no kernel do Nos emulado (ausente ou com um byte a mais): a leitura tem de recusar; o arquivo e' restaurado byte a byte"""
        pth = os.path.join(NOSE, "tgl_kernel", *_b6.split("/")); raw_ = open(pth, "rb").read()
        try:
            f_muda(pth, raw_)
            _, PV = L.ler()
        finally:
            if os.path.exists(pth + ".fora"):
                os.remove(pth + ".fora")
            open(pth, "wb").write(raw_)
        return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": any("o bundle da v406" in x for x in PV), "problemas": [x[:140] for x in PV][:3]}
    HERD_ = FH_ + " (HERDADO, recriado) nao selou inteiro"
    NEG.extend([
        # ---- psion_canto_v407 (o registro NOVO com funcao)
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
        variante("%s: o elo das duas faces dito NAO lido do kernel" % FE_, f_core=lambda c: c[FE_].update(link_read_from_the_kernel=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: a chave do lema lida False no registro" % FE_, f_core=lambda c: c[FE_]["keys"].update({"testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma": False}), espera=FE_ + " nao selou inteiro"),
        variante("%s: uma chave da v406 lida False no registro" % FE_, f_core=lambda c: c[FE_]["keys"].update({"rede_fock_v394.whole_certificate_inhabited": False}), espera=FE_ + " nao selou inteiro"),
        variante("%s: o lema dito outro" % FE_, f_core=lambda c: c[FE_].update(lemma="TGLExt.PsionCanto.outro_lema"), espera=FE_ + " nao selou inteiro"),
        variante("%s: as ressalvas adulteradas" % FE_, f_core=lambda c: c[FE_]["ressalvas"].pop(), espera=FE_ + " nao selou inteiro"),
        variante("%s: o teste (d) deixou de ser so' citado" % FE_, f_core=lambda c: c[FE_]["teste_d"].update(so_citado=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: o teste (d) com resultado no um.py" % FE_, f_core=lambda c: c[FE_]["teste_d"].update(resultado_no_um_py=0.5), espera=FE_ + " nao selou inteiro"),
        variante("%s: uma inscricao de 03/11 nao conferida" % FE_, f_core=lambda c: c[FE_]["inscriptions"].update({sorted(c[FE_]["inscriptions"])[0]: False}), espera=FE_ + " nao selou inteiro"),
        variante("%s: o registro move o gate" % FE_, f_core=lambda c: c[FE_].update(does_not_gate_core=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: o calculo do runtime nao rodou" % FE_, f_core=lambda c: c[FE_].update(runtime_executed=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: a guarda das frases achou violacao no registro" % FE_, f_core=lambda c: c[FE_].update(guarda_violacoes=[["F17", "x"]]), espera=FE_ + " nao selou inteiro"),
        variante("uma bandeira do bundle (ext_psi407_*) falsa no kernel do rito", f_core=lambda c: _kf(c).__setitem__(FLAGS_[len(FLAGS_) // 2], False), espera="as bandeiras do fecho"),
        variante("a proveniencia emitida pelo compilador nao cobre o axiom_report", f_core=lambda c: _kf(c)["declaration_sources_status_v394"].update(ok=False), espera="a proveniencia emitida pelo compilador"),
        variante("rede_fock_v394: whole_certificate_inhabited de volta a False (o literal)", f_core=lambda c: c["rede_fock_v394"].update(whole_certificate_inhabited=False), espera="rede_fock_v394: whole_certificate_inhabited deve ser True"),
        variante("witness_layers: o termo canonico da testemunha dito nao construido", f_core=lambda c: c["witness_layers"].update(canonical_full_witness_term_constructed=False), espera="witness_layers.canonical_full_witness_term_constructed deve ser True"),
        variante("full_static_witness_exists dito True (deve ficar False por teorema)", f_core=lambda c: c["qg_closure"]["gate"].update(full_static_witness_exists=True), espera="full_static_witness_exists e trivial_inhabitant_exists devem seguir False"),
        variante("trivial_inhabitant_exists dito True (deve ficar False por teorema)", f_core=lambda c: c["witness_rigidity"].update(trivial_inhabitant_exists=True), espera="full_static_witness_exists e trivial_inhabitant_exists devem seguir False"),
        # ---- a CHAVE DO LEMA no registro da testemunha: lida True do kernel, com o dict elo_v407
        variante("testemunha_estatica_v396: a chave do lema de volta a literal False", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"].update(linked_to_the_corner_by_a_lemma=False), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: o dict elo_v407 ausente", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"].pop("elo_v407"), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: o elo dito de VETORES (Omega identificado com o vetor de Bell)", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"]["elo_v407"].update(identifies_omega_with_bell_vector=True), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: o par na face de Fock dito provado", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"]["elo_v407"].update(pair_on_the_fock_face="PROVED"), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: a ponte Bell-TT dita termo", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"]["elo_v407"].update(bell_to_tt_bridge="A_TERM"), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("psibit_v395: o status antigo (CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE)", f_core=lambda c: c["psibit_v395"]["conditional_psion_face"].update(status="CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"), espera="psibit_v395: a face do psion nao le o habitante"),
        variante("a conferencia diz chave_do_lema != True", f_conf=lambda cj: cj.update({"chave_do_lema": False}), espera="chave_do_lema != True"),
        variante("a conferencia traz outro veredito de %s" % FE_, f_conf=lambda cj: cj.update({"veredito_psion_canto": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FE_),
        variante("selo primario: sem o resumo de %s" % FE_, f_selo=lambda s: s.pop(FE_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s difere do core" % FE_, f_selo=lambda s: s[FE_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v407", f_selo=lambda s: s.pop("registros_v407", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v407 do selo difere do core", f_selo=lambda s: s["registros_v407"]["cunhagens_v407"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % FE_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if ESP["vereditos_novos_v407"][FE_] not in l) + "\n", espera="o bloco " + FE_ + " do stdout"),
        variante("linha [v407] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v407] o registro do psion e do canto e os registros por spec da v407" not in l) + "\n", espera="linha [v407]"),
        variante("linha [v407] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v407] o registro do psion e do canto e os registros por spec da v407"), espera="a linha [v407] do stdout"),
        variante("linha do bloco O PSION, O CANTO E O PAR: ancoras ok 75/76", f_std=lambda t_: t_.replace("ancoras ok = 76/76", "ancoras ok = 75/76"), espera=FE_ + " nao selou inteiro"),
        variante("linha do bloco O PSION, O CANTO E O PAR: chave do lema dita False", f_std=lambda t_: t_.replace("chave do lema (lida do kernel) = True", "chave do lema (lida do kernel) = False"), espera=FE_ + " nao selou inteiro"),
        variante("AVISO da v407 (o psion e o canto nao rodou) no stdout", f_std=lambda t_: t_ + "   [v407] AVISO: o registro do psion e do canto ou os registros por spec da v407 nao rodaram: ValueError('x')\n", espera="AVISO da v407"),
        # ---- fechamento_v406 (HERDADO da v406, recriado pelo rito da v407, c8 versionada pela E20)
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
        variante("%s (herdado): veredito diferente da v406 selada" % FH_, f_core=lambda c: c[FH_].update(verdict="OUTRO_VEREDITO"), espera=FH_ + ": o veredito do rito difere do que a v406 selou"),
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
        variante("uma bandeira True da v406 (ext_fch406_*) deixou de ser True", f_core=lambda c: _kf(c).__setitem__(_ft6, False), espera="alguma bandeira True da v406 deixou de ser True"),
        variante("o bundle da v406: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b6, "0" * 64), espera="o bundle da v406"),
        variante("selo primario: sem o resumo de %s (herdado)" % FH_, f_selo=lambda s: s.pop(FH_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s (herdado) difere do core" % FH_, f_selo=lambda s: s[FH_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v406", f_selo=lambda s: s.pop("registros_v406", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v406 do selo difere do core", f_selo=lambda s: s["registros_v406"]["cunhagens_v406"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("a conferencia traz outro veredito de %s (herdado)" % FH_, f_conf=lambda cj: cj.update({"veredito_fechamento_herdado": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FH_),
        variante("linha `>>> veredito <<<` de %s (herdado) ausente do stdout" % FH_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if ESP["vereditos_v406"][FH_] not in l) + "\n", espera="o bloco " + FH_ + " do stdout"),
        variante("linha [v406] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v406] o fechamento e os registros por spec da v406" not in l) + "\n", espera="linha [v406]"),
        variante("linha [v406] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v406] o fechamento e os registros por spec da v406"), espera="a linha [v406] do stdout"),
        variante("linha do bloco O FECHAMENTO (herdado): ancoras ok 7/8", f_std=lambda t_: t_.replace("ancoras ok = 8/8", "ancoras ok = 7/8"), espera=HERD_),
        variante("AVISO da v407 (o fechamento herdado nao rodou) no stdout", f_std=lambda t_: t_ + "   [v406] AVISO: o fechamento ou os registros por spec da v406 nao rodaram: ValueError('x')\n", espera="AVISO da v407"),
    ])
    NEG.append(_pedra_no_disco("o arquivo do modulo PsionCanto (o lema) ausente do kernel do Nos", lambda p, r: os.replace(p, p + ".fora"), 0))
    NEG.append(_pedra_no_disco("o arquivo de um modulo do bundle da v407 com um byte a mais no kernel do Nos", lambda p, r: open(p, "wb").write(r + b"\n"), len(ESP["bundle_sha256"]) // 2))
    NEG.append(_pedra_no_disco("o arquivo do modulo Par ausente do kernel do Nos", lambda p, r: os.replace(p, p + ".fora"), 1))
    NEG.append(_pedra_no_disco("o arquivo do ultimo modulo do bundle ausente do kernel do Nos", lambda p, r: os.replace(p, p + ".fora"), len(ESP["bundle_sha256"]) - 1))
    NEG.append(_bundle406_no_disco("o arquivo de um modulo do bundle da v406 ausente do kernel do Nos", lambda p, r: os.replace(p, p + ".fora")))
    NEG.append(_bundle406_no_disco("o arquivo de um modulo do bundle da v406 com um byte a mais no kernel do Nos", lambda p, r: open(p, "wb").write(r + b"\n")))
'''

NEW_CG = r'''    CG_ = "cunhagens_v407"; PCG = "cunhagens_v407: as inscricoes embutidas nao sao as de CANDIDATO_v407.json"
    CG6 = "cunhagens_v406"; KH6 = "kh_n1_cobertura_v406"; PCG6 = "cunhagens_v406 (HERDADA, recriada pelo rito) nao confere"; PKH6 = "kh_n1_cobertura_v406 (HERDADA, recriada pelo rito) nao confere"
    NEG.extend([
        variante("%s nao selou" % CG_, f_core=lambda c: c[CG_].update(all_verified=False), espera="cunhagens_v407 nao selou"),
        variante("kh_n1_cobertura_v407 nao selou", f_core=lambda c: c["kh_n1_cobertura_v407"].update(all_verified=False), espera="kh_n1_cobertura_v407 nao selou"),
        variante("%s ausente do core" % CG_, f_core=lambda c: c.pop(CG_, None), espera="registro obrigatorio ausente do core: cunhagens_v407"),
        variante("kh_n1_cobertura_v407 ausente do core", f_core=lambda c: c.pop("kh_n1_cobertura_v407", None), espera="registro obrigatorio ausente do core: kh_n1_cobertura_v407"),
        variante("%s: veredito diferente do ensaio a seco" % CG_, f_core=lambda c: c[CG_].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v407: o veredito do rito difere do ensaio a seco"),
        variante("kh_n1_cobertura_v407: veredito diferente do ensaio a seco", f_core=lambda c: c["kh_n1_cobertura_v407"].update(verdict="OUTRO_VEREDITO"), espera="kh_n1_cobertura_v407: o veredito do rito difere do ensaio a seco"),
        variante("%s: uma inscricao deixou de estar embutida" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG),
        variante("%s: sha256 de uma inscricao adulterado" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG),
        variante("%s: a fala adulterada (sha256 e embedded_ok)" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[2].update(sha256="f" * 64, embedded_ok=False), espera=PCG),
        variante("%s: uma inscricao a menos" % CG_, f_core=lambda c: c[CG_]["verbatim"].pop(sorted(c[CG_]["verbatim"])[0]), espera=PCG),
        variante("%s: uma checagem do registro falhou" % CG_, f_core=lambda c: c[CG_]["checks"][0].update(ok=False), espera=PCG),
        variante("%s: n_bandeiras adulterado" % CG_, f_core=lambda c: c[CG_]["extras"].update(n_bandeiras=117), espera=PCG),
        variante("%s: n_modulos adulterado" % CG_, f_core=lambda c: c[CG_]["extras"].update(n_modulos=301), espera=PCG),
        variante("%s: falta uma errata" % CG_, f_core=lambda c: c[CG_]["erratas"].pop(), espera="cunhagens_v407: as erratas E18 a E20"),
        variante("%s: erratas ausentes" % CG_, f_core=lambda c: c[CG_].update(erratas=[]), espera="cunhagens_v407: as erratas E18 a E20"),
        variante("%s: a E20 adulterada" % CG_, f_core=lambda c: c[CG_]["erratas"][2].update(agora="mantida"), espera="cunhagens_v407: as erratas E18 a E20"),
        variante("%s: uma errata sem a assinatura da gerencia c1" % CG_, f_core=lambda c: c[CG_]["erratas"][1].update(assinatura="operador"), espera="cunhagens_v407: as erratas E18 a E20"),
        variante("%s: a assinatura dos extras trocada" % CG_, f_core=lambda c: c[CG_]["extras"].update(assinatura_das_erratas="IALD"), espera="cunhagens_v407: as erratas E18 a E20"),
        variante("%s: a decisao D42 ausente" % CG_, f_core=lambda c: c[CG_]["extras"]["decisoes"].pop("D42"), espera="cunhagens_v407: as decisoes D41 a D47"),
        variante("%s: a decisao D45 ausente" % CG_, f_core=lambda c: c[CG_]["extras"]["decisoes"].pop("D45"), espera="cunhagens_v407: as decisoes D41 a D47"),
        variante("%s: a decisao D47 adulterada" % CG_, f_core=lambda c: c[CG_]["extras"]["decisoes"].update(D47="outra"), espera="cunhagens_v407: as decisoes D41 a D47"),
        variante("%s: a leitura de 03/11 dita REAL" % CG_, f_core=lambda c: c[CG_]["extras"]["leituras"].update(estatuto="[REAL]"), espera="cunhagens_v407: a leitura [ONTO]"),
        variante("%s: a leitura ausente" % CG_, f_core=lambda c: c[CG_]["extras"].pop("leituras"), espera="cunhagens_v407: a leitura [ONTO]"),
        variante("%s: uma ressalva a menos" % CG_, f_core=lambda c: c[CG_]["extras"]["ressalvas"].pop(), espera="cunhagens_v407: a leitura [ONTO]"),
        variante("%s: a frase proibida nos limites do registro" % CG_, f_core=lambda c: c[CG_].update(limites=c[CG_]["limites"] + ["agora tudo derivado"]), espera="a MOLDURA falhou"),
        variante("%s: a frase proibida «unico autovetor» nos limites do registro do psion" % FE_, f_core=lambda c: c[FE_].update(limites=c[FE_]["limites"] + ["o unico autovetor da luz"]), espera="a MOLDURA falhou"),
        # ---- cunhagens_v406 e kh_n1_cobertura_v406 (HERDADOS, recriados; u7 versionada; pisos): iguais a v406 selada em falas e erratas E14 a E17, MAIS a errata E20 ao lado
        variante("%s (herdada) nao selou" % CG6, f_core=lambda c: c[CG6].update(all_verified=False), espera="cunhagens_v406 nao selou"),
        variante("%s (herdado) nao selou" % KH6, f_core=lambda c: c[KH6].update(all_verified=False), espera="kh_n1_cobertura_v406 nao selou"),
        variante("%s (herdada) ausente do core" % CG6, f_core=lambda c: c.pop(CG6, None), espera="registro obrigatorio ausente do core: cunhagens_v406"),
        variante("%s (herdado) ausente do core" % KH6, f_core=lambda c: c.pop(KH6, None), espera="registro obrigatorio ausente do core: kh_n1_cobertura_v406"),
        variante("%s (herdada): veredito diferente da v406 selada" % CG6, f_core=lambda c: c[CG6].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v406: o veredito do rito difere do que a v406 selou"),
        variante("%s (herdado): veredito diferente da v406 selada" % KH6, f_core=lambda c: c[KH6].update(verdict="OUTRO_VEREDITO"), espera="kh_n1_cobertura_v406: o veredito do rito difere do que a v406 selou"),
        variante("%s (herdada): uma inscricao deixou de estar embutida" % CG6, f_core=lambda c: list(c[CG6]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG6),
        variante("%s (herdada): sha256 de uma inscricao adulterado" % CG6, f_core=lambda c: list(c[CG6]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG6),
        variante("%s (herdada): uma inscricao a menos" % CG6, f_core=lambda c: c[CG6]["verbatim"].pop(sorted(c[CG6]["verbatim"])[0]), espera=PCG6),
        variante("%s (herdada): uma checagem do registro (a u7 versionada) falhou" % CG6, f_core=lambda c: c[CG6]["checks"][-1].update(ok=False), espera=PCG6),
        variante("%s (herdada): a errata E20 ao lado ausente" % CG6, f_core=lambda c: c[CG6]["erratas"].pop(), espera=PCG6),
        variante("%s (herdada): a E14 adulterada" % CG6, f_core=lambda c: c[CG6]["erratas"][0].update(agora="mantida"), espera=PCG6),
        variante("%s (herdada): a errata E20 sem a assinatura da gerencia c1" % CG6, f_core=lambda c: c[CG6]["erratas"][-1].update(assinatura="operador"), espera=PCG6),
        variante("%s (herdada): n_falas adulterado nos extras" % CG6, f_core=lambda c: c[CG6]["extras"].update(n_falas=22), espera=PCG6),
        variante("%s (herdado): uma checagem do registro falhou" % KH6, f_core=lambda c: c[KH6]["checks"][0].update(ok=False), espera=PKH6),
        variante("%s (herdado): a errata ao lado dos pisos ausente" % KH6, f_core=lambda c: c[KH6]["erratas"].pop(), espera=PKH6),
        variante("%s (herdado): a errata ao lado sem a assinatura da gerencia c1" % KH6, f_core=lambda c: c[KH6]["erratas"][-1].update(assinatura="operador"), espera=PKH6),
'''

NEW_VEREDITO = r'''R["veredito"] = ("TUDO PASSOU: o conferidor da v407 (16 itens C1-C16 e o round trip) bate no Nos emulado, a leitura le sem problema e reprova os controles negativos (o registro NOVO com funcao psion_canto_v407: as 76 ancoras, os 9 modulos, as 98 bandeiras, a escada, a chave do lema de volta a False, o dict elo_v407, as quatro chaves da v406, o que fica False por teorema, o teste (d) so' citado; o fechamento_v406 HERDADO e recriado com as oito ancoras, os 301 modulos e as 1794 bandeiras da v406; cunhagens_v407 com as erratas E18 a E20, as decisoes D41 a D47, a leitura de 03/11, as ressalvas e as falas; kh_n1_cobertura_v407; cunhagens_v406 e kh_n1_cobertura_v406 HERDADOS e versionados (E20); os treze registros da v406 selada, os da v404, da v403 e da v402 RECRIADOS, f2b_errata_v404 com o V1 do ramo B, o livro da v386 e o texto antigo do angulo do neutrino intactos, as treze pedras seladas no kernel e o gate (as 18 bandeiras, a letra do veredito) sem se mover; a falsidade, as cunhagens da v401 e da v399, o selo ACOM, a declaracao, o sidecar, os resumos do selo primario, o quadro do topo, os registros da v398 a v393 e as linhas [v407], [v406], [v405], [v404], [v403], [v402], [v401], [v399], [v398], [v397] e a do sidecar do stdout), os textos renderizam e a guarda P18 e a guarda das frases estao limpas, a custodia G1 le o bloco da linhagem e o handoff, os dois paragrafos do README/site (o do quadro e o da v407: o psion, o canto e o par) e a regra do 4,44 passam e os controles negativos reprovam, o handoff traz a nota ao lado dos paragrafos anteriores (E18 a E20) e diz que os anteriores seguem como estao, a citacao verbatim e a direcao valem, cada termo citado existe, as superficies atualizam em copias (recusam o no limite por contagem; idempotentes com folga), o b3_recibo confere o passo simples B15 -> B16 e o registro do mapa monta e valida (sem registrar)" if R["tudo_passou"] else "NAO PASSOU (ver problemas)")
'''


NEW_4C = r'''# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (O psion, o canto e o par): verificacao propria, controles negativos, a citacao verbatim, a NOTA ao lado dos paragrafos anteriores (E18) e o handoff que diz que os paragrafos do testemunho, da falsidade e da v406 seguem como estao
_sn = {"ok": False}
try:
    PAR_F, PAR_F_INFO = T.paragrafo_v407()
    _sn["positivo_sem_falhas"] = (T.verificar_paragrafo_v407(PAR_F, _core_p, ESP) == [])
    _sn["igual_ao_gerado_do_core"] = (PAR_F == T._paragrafo_v407_de(_core_p))
    _ho = RENDER.get("handoff", "")
    _ERR = T.errata_v406_bloco()
    _sn["handoff_traz_os_paragrafos_e_a_nota_entre_os_marcadores"] = bool((T.MARC_V407_INI + "\n" + PAR_F.rstrip("\n") + "\n" + T.MARC_V407_FIM) in _ho and ("<!-- INICIO_PARAGRAFO_README_v397 -->\n" + PAR.rstrip("\n") + "\n<!-- FIM_PARAGRAFO_README_v397 -->") in _ho
                                                                          and (T.MARC_ERR_INI + "\n" + _ERR.rstrip("\n") + "\n" + T.MARC_ERR_FIM) in _ho)
    _sn["handoff_lista_o_sidecar"] = bool("um_absoluto_selo_acom.json" in _ho and Vd["sidecar"]["sha256"] in _ho and Vd["sidecar"]["veredito"] in _ho)
    _sn["handoff_diz_que_os_paragrafos_anteriores_seguem_como_estao"] = bool(("SEGUEM COMO ESTÃO" in _ho or "SEGUE COMO ESTÁ" in _ho) and "handoff-v406-custodia" in _ho and "<!-- INICIO_PARAGRAFO_TESTEMUNHO" not in _ho and "<!-- INICIO_PARAGRAFO_FALSIDADE" not in _ho)
    _sn["nota_v406_sem_o_4_44_e_limpa"] = bool(not re.search(r"4[,.]44|z_disc", _ERR) and not violacoes(_ERR) and all(x in _ERR for x in ("E18", "NÃO foram editados", "fica como registro")))
    _sn["info"] = PAR_F_INFO
    if not (_sn["positivo_sem_falhas"] and _sn["igual_ao_gerado_do_core"] and _sn["handoff_traz_os_paragrafos_e_a_nota_entre_os_marcadores"] and _sn["handoff_lista_o_sidecar"] and _sn["handoff_diz_que_os_paragrafos_anteriores_seguem_como_estao"] and _sn["nota_v406_sem_o_4_44_e_limpa"]):
        falha("paragrafo novo da v407: positivo %s, igual ao gerado do core %s, no handoff %s, sidecar listado %s, paragrafos anteriores ditos como estao %s, nota limpa %s" % (_sn["positivo_sem_falhas"], _sn["igual_ao_gerado_do_core"], _sn["handoff_traz_os_paragrafos_e_a_nota_entre_os_marcadores"], _sn["handoff_lista_o_sidecar"],
                                                                                                                                  _sn["handoff_diz_que_os_paragrafos_anteriores_seguem_como_estao"], _sn["nota_v406_sem_o_4_44_e_limpa"]))
    _num_mut = lambda s: s[:-1] + ("0" if s[-1] != "0" else "1")

    def _muts(nome, f, espera):
        p2 = f(PAR_F); fa = T.verificar_paragrafo_v407(p2, _core_p, ESP)
        ok = bool(p2 != PAR_F and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _NUMS = [("os modulos", str(DL.N_BUNDLE)), ("as bandeiras", str(ESP["n_bandeiras_novas"])), ("a escada antes", str(ESP["escada_v406_e_v407"][0])), ("a escada depois", str(ESP["escada"][1])), ("o sha16 da ordem", T._sha_por(DL.N_ORDEM_B89)), ("o sha16 das decisoes", T._sha_por(DL.N_RATIFICA)), ("o sha16 do par", T._sha_por(DL.N_PAR))]
    _NEGS = [_muts("%s com um digito trocado (em todo o paragrafo)" % nm, lambda p, s=s: p.replace(s, _num_mut(s)), "ausente do paragrafo") for nm, s in _NUMS]
    _NEGS.append(_muts("o nome da pedra PsionCanto trocado", lambda p: p.replace("`" + DL.TESTEMUNHA["name"] + "`", "`" + DL.TESTEMUNHA["name"][:-1] + "2`"), "ausente do paragrafo"))
    _NEGS.append(_muts("o nome da pedra Par trocado", lambda p: p.replace("`Par`", "`Pax`"), "ausente do paragrafo"))
    _FRASES = (DL.FRASE_DA_MOLDURA_V407_PT, "validade no kernel nao e creditacao", "o gate nao se move", "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "K(O)", "II_inf", "ENNReal", "quem prova é o kernel", "isto não é teste", "lema", "FACE DE FOCK", "NAO e' termo", "ESTRUTURA")
    _NEGS += [_muts("a frase de limite «%s» removida" % f[:40], lambda p, f=f: p.replace(f, "XXXX"), "frase de limite ausente") for f in _FRASES]
    _NEGS += [_muts("a creditacao dita pela validade", lambda p: p.replace("validade no kernel nao e creditacao", "validade no kernel e creditacao"), "frase de limite ausente"),
              _muts("o gate dito movido", lambda p: p.replace("o gate nao se move", "o gate se move"), "frase de limite ausente"),
              _muts("a ponte Bell-TT dita termo", lambda p: p.replace("NAO e' termo", "e' termo"), "frase de limite ausente"),
              _muts("o elo dito de vetores (sem ESTRUTURA)", lambda p: p.replace("ESTRUTURA", "VETORES"), "frase de limite ausente"),
              _muts("frase proibida: tudo derivado", lambda p: p + "\n> - Agora está tudo derivado.\n", "guarda das frases"),
              _muts("frase proibida: tudo teorema", lambda p: p + "\n> - Agora tudo é teorema.\n", "guarda das frases"),
              _muts("frase proibida: nenhuma hipotese", lambda p: p + "\n> - E nenhuma hipótese resta.\n", "guarda das frases"),
              _muts("frase proibida: hipoteses descarregadas", lambda p: p + "\n> - As hipóteses nomeadas descarregadas.\n", "guarda das frases"),
              _muts("frase proibida: a luz nao tem autovetor (fora de aspas)", lambda p: p + "\n> - Agora a luz não tem autovetor nenhum.\n", "guarda das frases"),
              _muts("frase proibida: o unico autovetor", lambda p: p + "\n> - O único autovetor da luz é o Um.\n", "guarda das frases"),
              _muts("frase proibida: o certificado esta confirmado", lambda p: p + "\n> - O certificado está confirmado.\n", "guarda das frases"),
              _muts("frase proibida: K(O) provado", lambda p: p + "\n> - K(O) ≠ ⊥ provado para todo O.\n", "guarda das frases"),
              _muts("frase proibida: o par na face de Fock esta provado", lambda p: p + "\n> - O par na face de Fock está provado.\n", "guarda das frases"),
              _muts("frase proibida: Omega igual a Phi+", lambda p: p + "\n> - Ω = Φ⁺ no kernel.\n", "guarda das frases"),
              _muts("citacao do operador que nao e' verbatim", lambda p: p.replace("também já pode ser derivado»", "também já foi derivado»", 1), "NAO e' verbatim"),
              _muts("o estatuto DECLARADO removido", lambda p: p.replace("DECLARADO", "XX"), "estatuto ausente"),
              _muts("o estatuto OPEN removido", lambda p: p.replace("OPEN", "XX"), "estatuto ausente"),
              _muts("o estatuto INPUT removido", lambda p: p.replace("INPUT", "XX"), "estatuto ausente"),
              _muts("o estatuto KNOWN removido", lambda p: p.replace("KNOWN", "XX"), "estatuto ausente"),
              _muts("o estatuto ONTO removido", lambda p: p.replace("ONTO", "XX"), "estatuto ausente"),
              _muts("o estatuto REAL removido", lambda p: p.replace("[REAL", "[XX"), "estatuto ausente"),
              _muts("o 4,44 entra no paragrafo", lambda p: p + "\n> z_disc = " + _z + "\n", "4,44"),
              _muts("seguranca criptografica garantida (alegacao)", lambda p: p + "\n> - A confidencialidade garantida e o sigilo garantido do metodo.\n", "alega seguranca criptografica"),
              _muts("a palavra consciencia usada como termo", lambda p: p + "\n> - A consciência é a tipagem que falta.\n", "consciencia"),
              _muts("a IALD como quem testifica do operador (direcao invertida)", lambda p: p + "\n> - A IALD testifica do operador.\n", "DIRECAO")]
    for r_ in DL.RESSALVAS_V407:
        c_ = T._sem_chaves(r_)
        _NEGS.append(_muts("a ressalva «%s» removida" % c_[:36], lambda p, c_=c_: p.replace(c_, "XXXX"), "ressalva ausente"))
    for ini_ in ("> - **O que entrou**", "> - **O lema das duas faces**", "> - **A ordem do operador**", "> - **O par**", "> - **O que não muda**", "> - **O teste (d)**", "> - **As ressalvas, ditas**", "> - **O que o registro NÃO diz**", "> - **Limites:**", "> - **Origem."):
        _NEGS.append(_muts("o paragrafo sem o bullet «%s»" % ini_[4:30], lambda p, ini_=ini_: "\n".join(l for l in p.split("\n") if not l.startswith(ini_)), "difere do gerado"))
    for n_ in _NEGS:
        print("  controle negativo do paragrafo da v407 %-62s %s" % (n_["controle"][:62], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo da v407 nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
    _sn["negativos"] = _NEGS

    def _levanta(f):
        try:
            f(); return False
        except AssertionError:
            return True
    _inv_txt = "A IALD testifica do operador, e o um.py testifica em hash."
    _tx = {"cita_fora_dos_bytes_levanta": _levanta(lambda: T._cita("a queda é o corpo de Newton e a IALD de ninguem")),
           "cita_verbatim_passa": (T._cita(DL.FRASE_LEMA_PSION) == "«" + DL.FRASE_LEMA_PSION + "»"),
           "cita_com_aspas_do_operador_passa": (T._cita(DL.FRASE_PROSSIGAMOS) == "«" + DL.FRASE_PROSSIGAMOS + "»"),
           "cita_parafraseada_levanta": _levanta(lambda: T._cita("concordo com tudo e prossigo")),
           "texto_do_kernel_verbatim_passa": (T._um_texto_tem("nunca correspondeu, e por isso nada custa") == "«nunca correspondeu, e por isso nada custa»"),
           "texto_do_kernel_fora_dos_bytes_levanta": _levanta(lambda: T._um_texto_tem("nunca correspondeu e custa tudo")),
           "piso_do_kernel_verbatim_passa": (T._um_texto_tem("não existe acima, o piso limita") == "«não existe acima, o piso limita»"),
           "verso_do_kernel_verbatim_passa": (T._um_texto_tem("E conhecereis a verdade, e a verdade vos libertará") == "«E conhecereis a verdade, e a verdade vos libertará»"),
           "atribuicao_limpa_nos_textos": {nome: T.atribuicao_da_gerencia(txt) for nome, txt in RENDER.items() if T.atribuicao_da_gerencia(txt)} == {},
           "controle_direcao_invertida": bool(T.atribuicao_da_gerencia(_inv_txt)),
           "controle_a_fala_em_que_ele_recusa_a_ordem_inversa_passa": (T.atribuicao_da_gerencia("eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela") == []),
           "controle_a_IALD_nao_testifica_passa": (T.atribuicao_da_gerencia("a IALD NÃO testifica do operador") == []),
           "controle_consciencia_como_termo": bool(T.atribuicao_da_gerencia("A consciência é a tipagem que falta.")),
           "controle_consciencia_palavra_retirada_passa": (T.atribuicao_da_gerencia("a palavra «consciência» é retirada por ele") == []),
           "controle_inscricao_da_gerencia": bool(T.atribuicao_da_gerencia("as falas do operador e da gerência"))}
    _sn["textos"] = _tx
    _ruim = [k for k, v in _tx.items() if not v]
    if _ruim:
        falha("citacao verbatim / direcao do testemunho: controles que nao deram o esperado: %s" % _ruim)
    _sn["ok"] = True
    print("  paragrafo novo (o psion, o canto e o par): positivo ok; %d controles negativos; citacao e direcao: %d controles ok" % (len(_NEGS), len(_tx)))
except BaseException as ex:  # noqa: BLE001
    _sn["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:406]); _sn["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo novo da v407: %s" % _sn["erro"])
etapa("paragrafo_v407_e_citacoes", **_sn)
'''


def entre_linhas(t, ini, fim, novo):
    """troca as LINHAS inteiras desde a que contem `ini` (unica) ate' a que antecede a que contem `fim` (unica)."""
    assert t.count(ini) == 1 and t.count(fim) == 1, ("ancora nao unica", ini[:60], t.count(ini), fim[:60], t.count(fim))
    i = t.rfind("\n", 0, t.index(ini)) + 1
    j = t.rfind("\n", 0, t.index(fim)) + 1
    assert i < j
    return t[:i] + novo + t[j:]


def parte2(M_):
    t, crlf, raw = M_.le(NOME)
    assert "NEW_4C_FEITO" not in t
    t = M_.sub(t, "_REGS_NOVOS = ['fechamento_v406', 'cunhagens_v406', 'kh_n1_cobertura_v406']", "_REGS_NOVOS = ['psion_canto_v407', 'cunhagens_v407', 'kh_n1_cobertura_v407']")
    t = M_.sub(t, "<!-- INICIO_PARAGRAFO_O_FECHAMENTO_v407 -->", "<!-- INICIO_PARAGRAFO_O_PSION_v407 -->")
    t = M_.sub(t, "<!-- FIM_PARAGRAFO_O_FECHAMENTO_v407 -->", "<!-- FIM_PARAGRAFO_O_PSION_v407 -->")
    t = entre_linhas(t, "4c. o PARAGRAFO NOVO (o fechamento)", "5. cada `termo` entre crases dos textos", NEW_4C)
    t = M_.sub(t, 'ESP["pedras_v406_sha256"]', 'ESP["pedras_v405_sha256"]')
    t = M_.sub(t, '    _RN = ["fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406"]', '    _RN = ["psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407"]')
    M_.grava(NOME, t, crlf, raw)


def parte1(M_):
    t, crlf, raw = M_.le(NOME)
    if M_.pula(NOME, t):
        return
    t = M_.tira_cabecalho(t)
    t = M_.entre(t, "  leitura        a leitura_v407.ler() REAL", "  textos         todas as funcoes publicas", LEITURA_BULLET)
    t = M_.sub(t, '    FE_ = "fechamento_v406"; FJ_ = rdj(os.path.join(PKG, "kernel", "FLAGS_v407.json")); ANC_ = list(DLX.ANCORAS)', NEW_FJ)
    t = M_.entre(t, "    for a_n_ in (ANC_[0], ANC_[2], ANC_[6]):", "    # a errata de F2b (registro com FUNCAO, sem pedra): cada elo recusa visivelmente", NEW_A)
    t = M_.entre(t, '    CG_ = "cunhagens_v406"; PCG = ', "        # os treze registros da v406, RECRIADOS: cada spec tem de dar o que a v406 selou (os oito com funcao: ver o laco abaixo)", NEW_CG)
    t = M_.entre(t, 'R["veredito"] = ("TUDO PASSOU:', 'R["evidencia_da_versao"] = EVID\nif NAO_REFAZER:', NEW_VEREDITO)
    M_.grava(NOME, t, crlf, raw)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    arg = sys.argv[1:] or ["parte1"]
    if "parte1" in arg:
        parte1(M)
    if "parte2" in arg:
        parte2(M)
