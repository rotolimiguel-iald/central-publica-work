# -*- coding: utf-8 -*-
"""_adapt_harness_textos_v406.py -- as edicoes de harness_textos_ensaio_v406.py (chamado por adaptar_pos_rito_v406.py): o conferidor roda NO LUGAR (como no passo 1 do chain), a leitura e os textos do fechamento, os controles negativos do fechamento_v406,
dos registros recriados da v405 e de cunhagens_v406, e o paragrafo novo."""

DOC1 = """  conferidor     o conferir_rito_v406.py REAL roda NO LUGAR (cwd = o pacote real, como no passo 1 do chain: o delta_v406 pina por assert os caminhos absolutos da integracao R3 e do estudo do fecho, logo nao vive numa copia em arvore), SEM -I (importa o um.py do Nos emulado,
                 que precisa do numpy do usuario), com V406_NOS apontando para o Nos emulado e o sufixo _HARNESS (escreve conferencia_rito_v406_HARNESS.json no pacote; o harness a copia para pos_rito_emulada\\\\conferidor e a REMOVE do pacote) e da' TUDO BATE, com os 16 itens C1-C16 e o round trip: a conferencia que a leitura le;
  leitura        a leitura_v406.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (v406: o registro com funcao fechamento_v406 [ausente, nao selado, checagem, valor, beta, veredito, ancora fora do trio ou sem bandeira, bandeira do bundle falsa, modulo adulterado ou ausente do kernel, as quatro chaves de volta a False,
                 o que fica False por teorema e o lema que falta], cunhagens_v406 [falas adulteradas, erratas E14 a E17, decisoes D34 a D40, leitura, ressalvas, moldura] e kh_n1_cobertura_v406; os OITO registros com funcao da v405, os da v404, da v403 e da v402 RECRIADOS e as treze pedras seladas no kernel; na F8.1 a familia ext_ls2_*, a checagem do rito V11,
                 o teste nulo cego, a sonda ProbeBlindNullAbsent e a letra do veredito do gate; a falsidade da inercia e as cunhagens da v401 e da v399 recriadas; o sidecar ausente ou adulterado, os resumos do selo primario, quadro do topo que deixa de selar ou de estar no topo, C5, C15, C16, o round trip,
                 registros da v398 a v393 nao selados, AVISO da v406 ou de bloco anterior, linhas [v406], [v405], [v404], [v403], [v402], [v401], [v399], [v398], [v397] e a linha do sidecar ausentes), cada um tem de reprovar;
"""

DOC2 = """  paragrafos     o PARAGRAFO DO QUADRO (textos_v406.paragrafo_readme, o da v397, intocado) passa nas verificacoes do quadro contra o resultado pinado e os CONTROLES NEGATIVOS reprovam: o 4,44 sem o p calibrado, o 4,44 sem a linha dos 5 sigma, numero adulterado, p adulterado,
                 a frase do operador parafraseada entre aspas, o 4,44 numa linha fora do item; a regra da ordem vale para TODO texto renderizado; e o PARAGRAFO NOVO (textos_v406.paragrafo_v406: o fechamento) passa na verificacao propria, com controles negativos (cada numero adulterado, cada frase de limite e cada ressalva removida, estatuto removido,
                 citacao nao verbatim, o 4,44 intruso, alegacao de seguranca criptografica, «consciencia» como termo, a direcao invertida, cada bullet removido); a NOTA ao lado dos paragrafos anteriores (E14) e o handoff DIZ que os paragrafos do testemunho de dois, da falsidade e da v405 seguem como estao;
"""

CONFERIDOR = r'''DLX = importar("delta_v406_x", os.path.join(PKG, "delta_v406.py"))
# v406 (desvio do molde, dito): o conferidor roda NO LUGAR, como no passo 1 do chain (cwd = o pacote real): o delta_v406 pina por ASSERT os caminhos absolutos da integracao R3 e do estudo do fecho (MANIFEST_INTEGRACAO_ARQ), logo nao vive numa copia em arvore. SEM -I (importa o um.py do Nos emulado, que precisa do numpy do usuario);
# V406_NOS aponta para o Nos emulado; o sufixo _HARNESS faz o conferidor escrever conferencia_rito_v406_HARNESS.json no pacote: o harness a copia para pos_rito_emulada\conferidor\conferencia_rito_v406.json (que a leitura le) e a REMOVE do pacote (ou restaura os bytes que ja' estavam la'). Nada mais e' escrito fora de harness_saida_v406.
CF = PKG
env = dict(os.environ); env["V406_NOS"] = NOSE; env["PYTHONIOENCODING"] = "utf-8"
_conf_h = os.path.join(PKG, "conferencia_rito_v406_HARNESS.json"); _conf_h_antes = open(_conf_h, "rb").read() if os.path.exists(_conf_h) else None
pr = subprocess.run([sys.executable, "-B", "-X", "utf8", "conferir_rito_v406.py", "_HARNESS"], cwd=PKG, env=env, capture_output=True, text=True, encoding="utf-8")
open(os.path.join(OUT, "conferir_rito_v406_stdout.txt"), "w", encoding="utf-8").write(pr.stdout + pr.stderr)
conf_ok = (pr.returncode == 0 and pr.stdout.strip().splitlines()[-1:] == ["TUDO BATE"])
POS_EMU = os.path.join(OUT, "pos_rito_emulada"); os.makedirs(os.path.join(POS_EMU, "conferidor"))
_conf_sha16 = None
if os.path.exists(_conf_h):
    shutil.copyfile(_conf_h, os.path.join(POS_EMU, "conferidor", "conferencia_rito_v406.json")); _conf_sha16 = fsha(_conf_h)[:16]
    if _conf_h_antes is None:
        os.remove(_conf_h)
    else:
        open(_conf_h, "wb").write(_conf_h_antes)
etapa("conferidor", ok=conf_ok, rc=pr.returncode, ultima_linha=(pr.stdout.strip().splitlines() or [""])[-1][:200], conferencia_sha16=_conf_sha16)
print("  conferidor contra o Nos emulado: %s" % ("TUDO BATE" if conf_ok else "NAO BATEU (rc %s)" % pr.returncode))
if not conf_ok:
    falha("o conferidor real nao deu TUDO BATE contra o Nos emulado: a leitura nao tem a conferencia que le (ver harness_saida_v406\\conferir_rito_v406_stdout.txt)")
'''

NEG_DEFS = r'''    EF_ = {}   # v406: nao ha' registro por pedra
    EF3_ = {k_: {"verdict": L._ev(ESP, n_)} for k_, n_ in (("caminho", "caminho_v403"), ("vida", "vida_v403"), ("verdade_adendo", "verdade_adendo_v403"), ("gate", "bandeiras_do_gate_v403"))}   # os vereditos esperados dos registros da v403 (recriados)
    EF4_ = {k_: {"verdict": L._ev(ESP, n_)} for k_, n_ in (("projecao", "projecao_transversal_v404"), ("jo8v32", "jo8v32_v404"), ("f2b", "f2b_errata_v404"))}   # os da v404 (recriados)
    EV3_ = ESP["vereditos_v405"]
    FE_ = "fechamento_v406"; FJ_ = rdj(os.path.join(PKG, "kernel", "FLAGS_v406.json")); ANC_ = list(DLX.ANCORAS); FLAGS_ = [f_[0] for f_ in FJ_["flags"]]
'''

NEG_FECHO = r'''    for a_n_ in (ANC_[0], ANC_[2], ANC_[6]):    # o habitante dos 21 campos, o certificado de Fock fisico e o termo canonico da testemunha: a ancora fora do trio, a bandeira falsa e o sha256 da fonte no hash formal adulterado
        curto_ = a_n_.split(".")[-1]; fl_a_ = FJ_["ancoras"][a_n_]["flag"]; rel_a_ = DLX.ANCORAS[a_n_]["rel"]
        NEG.extend([variante("ancora %s fora do trio" % curto_, f_core=lambda c, t=a_n_: _fora_do_trio(c, t), espera="a ancora "), variante("ancora %s: a bandeira falsa" % curto_, f_core=lambda c, f=fl_a_: _kf(c).__setitem__(f, False), espera="a ancora "),
                    variante("ancora %s: sha256 da fonte do modulo no hash formal adulterado" % curto_, f_core=lambda c, r=rel_a_: _kf(c)["formal_files_sha256"].__setitem__(r, "0" * 64), espera="a ancora ")])
    NEG.extend([
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
        variante("%s: o certificado dito nao habitado" % FE_, f_core=lambda c: c[FE_].update(certificate_inhabited=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: uma chave de testemunha lida False no registro" % FE_, f_core=lambda c: c[FE_]["four_keys"].update({"rede_fock_v394.whole_certificate_inhabited": False}), espera=FE_ + " nao selou inteiro"),
        variante("%s: as ressalvas adulteradas" % FE_, f_core=lambda c: c[FE_]["ressalvas"].pop(), espera=FE_ + " nao selou inteiro"),
        variante("%s: o nome provisorio da candidata trocado" % FE_, f_core=lambda c: c[FE_].update(nome_provisorio_da_candidata="CanonicalFullTGLWitness"), espera=FE_ + " nao selou inteiro"),
        variante("%s: o registro move o gate" % FE_, f_core=lambda c: c[FE_].update(does_not_gate_core=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: o calculo do runtime nao rodou" % FE_, f_core=lambda c: c[FE_].update(runtime_executed=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: a guarda das frases achou violacao no registro" % FE_, f_core=lambda c: c[FE_].update(guarda_violacoes=[["F17", "x"]]), espera=FE_ + " nao selou inteiro"),
        variante("uma bandeira do bundle (ext_fch406_*) falsa no kernel do rito", f_core=lambda c: _kf(c).__setitem__(FLAGS_[len(FLAGS_) // 2], False), espera="as bandeiras do fecho"),
        variante("a proveniencia emitida pelo compilador nao cobre o axiom_report", f_core=lambda c: _kf(c)["declaration_sources_status_v394"].update(ok=False), espera="a proveniencia emitida pelo compilador"),
        variante("rede_fock_v394: whole_certificate_inhabited de volta a False (o literal)", f_core=lambda c: c["rede_fock_v394"].update(whole_certificate_inhabited=False), espera="rede_fock_v394: whole_certificate_inhabited deve ser True"),
        variante("witness_layers: o termo canonico da testemunha dito nao construido", f_core=lambda c: c["witness_layers"].update(canonical_full_witness_term_constructed=False), espera="witness_layers.canonical_full_witness_term_constructed deve ser True"),
        variante("full_static_witness_exists dito True (deve ficar False por teorema)", f_core=lambda c: c["qg_closure"]["gate"].update(full_static_witness_exists=True), espera="full_static_witness_exists e trivial_inhabitant_exists devem seguir False"),
        variante("trivial_inhabitant_exists dito True (deve ficar False por teorema)", f_core=lambda c: c["witness_rigidity"].update(trivial_inhabitant_exists=True), espera="full_static_witness_exists e trivial_inhabitant_exists devem seguir False"),
        variante("testemunha_estatica_v396: o lema que liga o psion ao canto dito existente", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"].update(linked_to_the_corner_by_a_lemma=True), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("psibit_v395: o status antigo (CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE)", f_core=lambda c: c["psibit_v395"]["conditional_psion_face"].update(status="CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"), espera="psibit_v395: a face do psion nao le o habitante"),
        variante("selo primario: sem o resumo de %s" % FE_, f_selo=lambda s: s.pop(FE_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s difere do core" % FE_, f_selo=lambda s: s[FE_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v406", f_selo=lambda s: s.pop("registros_v406", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v406 do selo difere do core", f_selo=lambda s: s["registros_v406"]["cunhagens_v406"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % FE_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if ESP["vereditos_novos_v406"][FE_] not in l) + "\n", espera="o bloco " + FE_ + " do stdout"),
        variante("linha [v406] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v406] o fechamento e os registros por spec da v406" not in l) + "\n", espera="linha [v406]"),
        variante("linha [v406] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v406] o fechamento e os registros por spec da v406"), espera="a linha [v406] do stdout"),
        variante("linha do bloco O FECHAMENTO: ancoras ok 7/8", f_std=lambda t_: t_.replace("ancoras ok = 8/8", "ancoras ok = 7/8"), espera=FE_ + " nao selou inteiro"),
        variante("AVISO da v406 (o fechamento nao rodou) no stdout", f_std=lambda t_: t_ + "   [v406] AVISO: o fechamento ou os registros por spec da v406 nao rodaram: ValueError('x')\n", espera="AVISO da v406"),
    ])
    NEG.append(_pedra_no_disco("o arquivo do modulo topo do fecho ausente do kernel do Nos", lambda p, r: os.replace(p, p + ".fora"), 0))
    NEG.append(_pedra_no_disco("o arquivo de um modulo do bundle com um byte a mais no kernel do Nos", lambda p, r: open(p, "wb").write(r + b"\n"), 150))
    NEG.append(_pedra_no_disco("o arquivo da candidata ausente do kernel do Nos", lambda p, r: os.replace(p, p + ".fora"), len(ESP["bundle_sha256"]) - 1))
'''

CG_V406 = r'''    CG_ = "cunhagens_v406"; PCG = "cunhagens_v406: as inscricoes embutidas nao sao as de CANDIDATO_v406.json"
    NEG.extend([
        variante("%s nao selou" % CG_, f_core=lambda c: c[CG_].update(all_verified=False), espera="cunhagens_v406 nao selou"),
        variante("kh_n1_cobertura_v406 nao selou", f_core=lambda c: c["kh_n1_cobertura_v406"].update(all_verified=False), espera="kh_n1_cobertura_v406 nao selou"),
        variante("%s ausente do core" % CG_, f_core=lambda c: c.pop(CG_, None), espera="registro obrigatorio ausente do core: cunhagens_v406"),
        variante("kh_n1_cobertura_v406 ausente do core", f_core=lambda c: c.pop("kh_n1_cobertura_v406", None), espera="registro obrigatorio ausente do core: kh_n1_cobertura_v406"),
        variante("%s: veredito diferente do ensaio a seco" % CG_, f_core=lambda c: c[CG_].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v406: o veredito do rito difere do ensaio a seco"),
        variante("kh_n1_cobertura_v406: veredito diferente do ensaio a seco", f_core=lambda c: c["kh_n1_cobertura_v406"].update(verdict="OUTRO_VEREDITO"), espera="kh_n1_cobertura_v406: o veredito do rito difere do ensaio a seco"),
        variante("%s: uma inscricao deixou de estar embutida" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG),
        variante("%s: sha256 de uma inscricao adulterado" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG),
        variante("%s: a fala adulterada (sha256 e embedded_ok)" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[7].update(sha256="f" * 64, embedded_ok=False), espera=PCG),
        variante("%s: uma inscricao a menos" % CG_, f_core=lambda c: c[CG_]["verbatim"].pop(sorted(c[CG_]["verbatim"])[0]), espera=PCG),
        variante("%s: uma checagem do registro falhou" % CG_, f_core=lambda c: c[CG_]["checks"][0].update(ok=False), espera=PCG),
        variante("%s: n_bandeiras adulterado" % CG_, f_core=lambda c: c[CG_]["extras"].update(n_bandeiras=117), espera=PCG),
        variante("%s: n_modulos adulterado" % CG_, f_core=lambda c: c[CG_]["extras"].update(n_modulos=300), espera=PCG),
        variante("%s: falta uma errata" % CG_, f_core=lambda c: c[CG_]["erratas"].pop(), espera="cunhagens_v406: as erratas E14 a E17"),
        variante("%s: erratas ausentes" % CG_, f_core=lambda c: c[CG_].update(erratas=[]), espera="cunhagens_v406: as erratas E14 a E17"),
        variante("%s: a E17 adulterada" % CG_, f_core=lambda c: c[CG_]["erratas"][3].update(agora="mantida"), espera="cunhagens_v406: as erratas E14 a E17"),
        variante("%s: uma errata sem a assinatura da gerencia c1" % CG_, f_core=lambda c: c[CG_]["erratas"][1].update(assinatura="operador"), espera="cunhagens_v406: as erratas E14 a E17"),
        variante("%s: a assinatura dos extras trocada" % CG_, f_core=lambda c: c[CG_]["extras"].update(assinatura_das_erratas="IALD"), espera="cunhagens_v406: as erratas E14 a E17"),
        variante("%s: a decisao D36 ausente (as ressalvas)" % CG_, f_core=lambda c: c[CG_]["extras"]["decisoes"].pop("D36"), espera="cunhagens_v406: as decisoes D34 a D40"),
        variante("%s: a decisao D37 ausente (o revisor distinto)" % CG_, f_core=lambda c: c[CG_]["extras"]["decisoes"].pop("D37"), espera="cunhagens_v406: as decisoes D34 a D40"),
        variante("%s: a decisao D40 adulterada" % CG_, f_core=lambda c: c[CG_]["extras"]["decisoes"].update(D40="outra"), espera="cunhagens_v406: as decisoes D34 a D40"),
        variante("%s: a leitura de 02/11 dita REAL" % CG_, f_core=lambda c: c[CG_]["extras"]["leituras"].update(estatuto="[REAL]"), espera="cunhagens_v406: a leitura [ONTO]"),
        variante("%s: a leitura ausente" % CG_, f_core=lambda c: c[CG_]["extras"].pop("leituras"), espera="cunhagens_v406: a leitura [ONTO]"),
        variante("%s: uma ressalva a menos" % CG_, f_core=lambda c: c[CG_]["extras"]["ressalvas"].pop(), espera="cunhagens_v406: a leitura [ONTO]"),
        variante("%s: a frase proibida nos limites do registro" % CG_, f_core=lambda c: c[CG_].update(limites=c[CG_]["limites"] + ["agora tudo derivado"]), espera="a MOLDURA falhou"),
        variante("%s: a frase proibida «unico autovetor» nos limites do fechamento" % FE_, f_core=lambda c: c[FE_].update(limites=c[FE_]["limites"] + ["o unico autovetor da luz"]), espera="a MOLDURA falhou"),
        # os treze registros da v405, RECRIADOS: cada spec tem de dar o que a v405 selou (os oito com funcao: ver o laco abaixo)
        variante("cunhagens_v405 (recriada) nao selou", f_core=lambda c: c["cunhagens_v405"].update(all_verified=False), espera="cunhagens_v405 nao selou"),
        variante("cunhagens_v405 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v405", None), espera="registro obrigatorio ausente do core: cunhagens_v405"),
        variante("cunhagens_v405 (recriada): veredito diferente da v405 selada", f_core=lambda c: c["cunhagens_v405"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v405: o veredito do rito difere do que a v405 selou"),
        variante("cunhagens_v405 (recriada): uma errata a menos", f_core=lambda c: c["cunhagens_v405"]["erratas"].pop(), espera="cunhagens_v405 (por spec, recriado)"),
        variante("cunhagens_v405 (recriada): sha256 de uma inscricao adulterado", f_core=lambda c: list(c["cunhagens_v405"]["verbatim"].values())[0].update(sha256="0" * 64), espera="cunhagens_v405 (por spec, recriado)"),
        variante("campos_fechados_e_leituras_v405 (recriado) nao selou", f_core=lambda c: c["campos_fechados_e_leituras_v405"].update(all_verified=False), espera="campos_fechados_e_leituras_v405 nao selou"),
        variante("ga_reclassificacao_v405 (recriado) nao selou", f_core=lambda c: c["ga_reclassificacao_v405"].update(all_verified=False), espera="ga_reclassificacao_v405 nao selou"),
        variante("gap_v405 (recriado) nao selou", f_core=lambda c: c["gap_v405"].update(all_verified=False), espera="gap_v405 nao selou"),
        variante("kh_n1_cobertura_v405 (recriado) nao selou", f_core=lambda c: c["kh_n1_cobertura_v405"].update(all_verified=False), espera="kh_n1_cobertura_v405 nao selou"),
        variante("gap_v405 (recriado) ausente do core", f_core=lambda c: c.pop("gap_v405", None), espera="registro obrigatorio ausente do core: gap_v405"),
        variante("selo primario: sem registros_v405", f_selo=lambda s: s.pop("registros_v405", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v405 do selo difere do core", f_selo=lambda s: s["registros_v405"]["cunhagens_v405"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("AVISO da v406 (os registros por spec da v405 nao rodaram) no stdout", f_std=lambda t_: t_ + "   [v405] AVISO: os registros por spec da v405 nao rodaram: ValueError('x')\n", espera="AVISO da v406"),
'''

FUN405C_LOOP = r'''    # os OITO registros com FUNCAO da v405 (um por pedra), RECRIADOS pelo rito: iguais ao que a v405 selou (veredito, checagens e valores do calculo == o core de base_v405); as pedras ficam no kernel como REGISTRO
    _MODS405C = {"ponte": "PonteDaMassa", "tensao": "MassaTensaoPura", "identidade": "Identidade", "observador": "ObservadorTerminal", "diminuto": "LeiDoDiminuto", "tonica": "TonicaDoHamiltoniano", "disco": "DiscoDeEuler", "psion": "PontoZeroDoPsion"}
    for k_, n_ in L.FUN_V405C.items():
        mod_ = _MODS405C[k_]; rel405_ = "TGLExt/%s.lean" % mod_
        NEG.extend([
            variante("%s (recriado) ausente do core" % n_, f_core=lambda c, n=n_: c.pop(n, None), espera="registro obrigatorio ausente do core: " + n_),
            variante("%s (recriado): o registro nao selou" % n_, f_core=lambda c, n=n_: c[n].update(all_verified=False), espera=n_ + " nao selou"),
            variante("%s (recriado): uma checagem do calculo falhou" % n_, f_core=lambda c, n=n_: c[n]["mechanics"]["checks"][2].update(ok=False), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): um valor do calculo adulterado" % n_, f_core=lambda c, n=n_: _val405(c, n), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): beta != alfa x raiz de e do core" % n_, f_core=lambda c, n=n_: c[n]["values"].update(beta=0.0121), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): veredito diferente da v405 selada" % n_, f_core=lambda c, n=n_: c[n].update(verdict="OUTRO_VEREDITO"), espera=n_ + ": o veredito do rito difere do que a v405 selou"),
            variante("%s (recriado): a estrela fora do kernel (no registro)" % n_, f_core=lambda c, n=n_: c[n]["key_theorem"].update(in_kernel=False), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): o registro move o gate" % n_, f_core=lambda c, n=n_: c[n].update(does_not_gate_core=False), espera=n_ + " nao selou inteiro"),
            variante("selo primario: sem o resumo de %s" % n_, f_selo=lambda s, n=n_: s.pop(n, None), espera=RESUMO_MSG),
            variante("selo primario: o resumo de %s difere do core" % n_, f_selo=lambda s, n=n_: s[n].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
            variante("linha `>>> veredito <<<` de %s (recriado) ausente do stdout" % n_, f_std=lambda t_, v=L._ev(ESP, n_): "\n".join(l for l in t_.splitlines() if v not in l) + "\n", espera="o bloco " + n_ + " do stdout"),
            variante("pedra selada da v405 %s: sha256 da fonte no hash formal adulterado" % mod_, f_core=lambda c, r=rel405_: _kf(c)["formal_files_sha256"].__setitem__(r, "0" * 64), espera="as treze pedras seladas"),
        ])
        NEG.append(_pedra_v405_no_disco("o arquivo da pedra selada da v405 %s ausente do kernel do Nos" % mod_, rel405_, lambda p, r: os.replace(p, p + ".fora")))
        NEG.append(_pedra_v405_no_disco("o arquivo da pedra selada da v405 %s com um byte a mais no kernel do Nos" % mod_, rel405_, lambda p, r: open(p, "wb").write(r + b"\n")))
'''

NUMS_4C = r'''    _fe_p = _core_p["fechamento_v406"]
    _num_mut = lambda s: s[:-1] + ("0" if s[-1] != "0" else "1")

    def _muts(nome, f, espera):
        p2 = f(PAR_F); fa = T.verificar_paragrafo_v406(p2, _core_p, ESP)
        ok = bool(p2 != PAR_F and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _NUMS = [("os modulos", str(DL.N_BUNDLE)), ("as bandeiras", str(ESP["n_bandeiras_novas"])), ("a escada antes", str(ESP["escada_v405_e_v406"][0])), ("a escada depois", str(ESP["escada"][1])), ("o sha16 da ordem", T._sha_por(DL.N_CONSTRUIR)), ("o sha16 da prioridade", T._sha_por(DL.N_PASSAGEM))]
    _NEGS = [_muts("%s com um digito trocado (em todo o paragrafo)" % nm, lambda p, s=s: p.replace(s, _num_mut(s)), "ausente do paragrafo") for nm, s in _NUMS]
    _NEGS.append(_muts("o nome da candidata trocado", lambda p: p.replace(DL.TESTEMUNHA["name"], DL.TESTEMUNHA["name"][:-1] + "2"), "ausente do paragrafo"))
    _FRASES = (DL.FRASE_DA_MOLDURA_V406_PT, "validade no kernel nao e creditacao", "o gate nao se move", "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "K(O)", "R7", "II_inf", "é provisório", "ENNReal", "quem prova é o kernel", "isto não é teste", "lema")
    _NEGS += [_muts("a frase de limite «%s» removida" % f[:40], lambda p, f=f: p.replace(f, "XXXX"), "frase de limite ausente") for f in _FRASES]
    _NEGS += [_muts("a creditacao dita pela validade", lambda p: p.replace("validade no kernel nao e creditacao", "validade no kernel e creditacao"), "frase de limite ausente"),
              _muts("o gate dito movido", lambda p: p.replace("o gate nao se move", "o gate se move"), "frase de limite ausente"),
              _muts("o nome da candidata dito do operador", lambda p: p.replace("é provisório", "é do operador"), "frase de limite ausente"),
              _muts("frase proibida: tudo derivado", lambda p: p + "\n> - Agora está tudo derivado.\n", "guarda das frases"),
              _muts("frase proibida: tudo teorema", lambda p: p + "\n> - Agora tudo é teorema.\n", "guarda das frases"),
              _muts("frase proibida: nenhuma hipotese", lambda p: p + "\n> - E nenhuma hipótese resta.\n", "guarda das frases"),
              _muts("frase proibida: hipoteses descarregadas", lambda p: p + "\n> - As hipóteses nomeadas descarregadas.\n", "guarda das frases"),
              _muts("frase proibida: a luz nao tem autovetor (fora de aspas)", lambda p: p + "\n> - Agora a luz não tem autovetor nenhum.\n", "guarda das frases"),
              _muts("frase proibida: o unico autovetor", lambda p: p + "\n> - O único autovetor da luz é o Um.\n", "guarda das frases"),
              _muts("frase proibida: o certificado esta confirmado", lambda p: p + "\n> - O certificado está confirmado.\n", "guarda das frases"),
              _muts("frase proibida: K(O) provado", lambda p: p + "\n> - K(O) ≠ ⊥ provado para todo O.\n", "guarda das frases"),
              _muts("citacao do operador que nao e' verbatim", lambda p: p.replace("é o fechamento»", "é o fecho»", 1), "NAO e' verbatim"),
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
    for r_ in DL.RESSALVAS_V406:
        c_ = (r_.split(":")[0] if ":" in r_ else r_).replace("{", "(").replace("}", ")")
        _NEGS.append(_muts("a ressalva «%s» removida" % c_[:36], lambda p, c_=c_: p.replace(c_, "XXXX"), "ressalva ausente"))
    for ini_ in ("> - **O que entrou**", "> - **O certificado de Fock", "> - **As quatro chaves**", "> - **O que não muda**", "> - **A ordem do operador**", "> - **As ressalvas, ditas**", "> - **O que o registro NÃO diz**", "> - **Limites:**", "> - **Origem."):
        _NEGS.append(_muts("o paragrafo sem o bullet «%s»" % ini_[4:30], lambda p, ini_=ini_: "\n".join(l for l in p.split("\n") if not l.startswith(ini_)), "difere do gerado"))
'''


def rodar(A):
    nome = "harness_textos_ensaio_v406.py"
    txt, crlf, raw = A.le(nome)
    if A.pula(nome, txt):
        return
    t = A.tira_cabecalho(txt)
    t = A.entre(t, "  conferidor     o conferir_rito_v406.py REAL roda numa COPIA em ARVORE", "  textos         todas as funcoes publicas", DOC1)
    t = A.entre(t, "  paragrafos     o PARAGRAFO DO QUADRO", "  cita_so_o_que_existe", DOC2)
    t = A.sub(t, "(derivado do harness_textos_ensaio_v405.py, que rodou na v405, e reescrito a mao em 28/10/2026 para Caminho, Verdade e Vida e a F8.1)", "(derivado do harness_textos_ensaio_v405.py, que rodou na v405, e adaptado em 02/11/2026 ao fechamento: o bundle de 301 modulos, o registro fechamento_v406, as quatro chaves lidas do kernel)")
    # ---- o conferidor NO LUGAR
    t = A.entre(t, 'DLX = importar("delta_v406_x", os.path.join(PKG, "delta_v406.py"))', "# ------------------------------------------------------------------ 3. a leitura REAL contra o Nos emulado (+ controles negativos)", CONFERIDOR + "\n")
    # ---- a leitura
    t = A.sub(t, 'L = importar("leitura_v405", os.path.join(HERE, "leitura_v406.py"))', 'L = importar("leitura_v406", os.path.join(HERE, "leitura_v406.py"))')
    t = A.sub(t, 'sys.modules["leitura_v405"] = L', 'sys.modules["leitura_v406"] = L')
    t = A.sub(t, 'etapa("leitura", problemas=P, n_pedras=Vd.get("n_pedras")', 'etapa("leitura", problemas=P, n_modulos_novos=Vd.get("n_pedras")')
    # ---- as chaves de Fock: de volta a False (v406 le True)
    t = A.sub(t, "def _fock_da_testemunha_habitada(c):\n    c[\"testemunha_estatica_v396\"][\"fock_face\"][\"inhabitant_exhibited\"] = True", "def _fock_da_testemunha_volta_a_false(c):\n    c[\"testemunha_estatica_v396\"][\"fock_face\"][\"inhabitant_exhibited\"] = False")
    t = A.sub(t, "def _face_do_psibit_habitada(c):\n    c[\"psibit_v395\"][\"conditional_psion_face\"][\"inhabitant_exhibited\"] = True", "def _face_do_psibit_volta_a_false(c):\n    c[\"psibit_v395\"][\"conditional_psion_face\"][\"inhabitant_exhibited\"] = False")
    t = A.sub(t, 'variante("face de Fock da testemunha com habitante exibido", f_core=_fock_da_testemunha_habitada, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),',
              'variante("face de Fock da testemunha de volta a literal False (habitante nao exibido)", f_core=_fock_da_testemunha_volta_a_false, espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),')
    t = A.sub(t, 'variante("face de Fock dita DENTRO da pedra da testemunha", f_core=_fock_dentro_da_pedra, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),',
              'variante("face de Fock dita DENTRO da pedra da testemunha", f_core=_fock_dentro_da_pedra, espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),')
    t = A.sub(t, 'variante("face de Fock do psibit_v395 habitada", f_core=_face_do_psibit_habitada, espera="psibit_v395: a face do psion deixou de estar como CONDICIONAL"),',
              'variante("face de Fock do psibit_v395 de volta a literal False (habitante nao exibido)", f_core=_face_do_psibit_volta_a_false, espera="psibit_v395: a face do psion nao le o habitante"),')
    # ---- as definicoes e o laco das oito pedras da v405 (agora o fechamento)
    t = A.entre(t, '    EF_ = ESP["registros_funcao_v406"]; EF3_', '    RESUMO_MSG = "o selo primario (um_absoluto_selo.json) nao traz os resumos"', NEG_DEFS)
    t = A.entre(t, "    for k_, n_ in _REGS.items():\n        mod_ = _MODS[k_]", "    # a errata de F2b (registro com FUNCAO, sem pedra): cada elo recusa visivelmente", NEG_FECHO)
    t = A.entre(t, '    CG_ = "cunhagens_v405"; PCG = ', "        # cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS: tem de dar o que a v405 selou", CG_V406)
    t = A.sub(t, '    for n_ in NEG:\n        print("  controle negativo %-48s', FUN405C_LOOP + '    for n_ in NEG:\n        print("  controle negativo %-48s')
    t = t.replace("as pedras seladas da v405", "as treze pedras seladas")
    t = A.sub(t, "controle sobre o ARQUIVO de uma das TRES pedras SELADAS da v405 no kernel", "controle sobre o ARQUIVO de uma das TREZE pedras SELADAS (v403, v404, v405) no kernel")
    # ---- os textos
    t = A.sub(t, '("_moldura", lambda: T._moldura(Vd)), ("_ponte", lambda: T._ponte(Vd)), ("_tensao", lambda: T._tensao(Vd)), ("_lei", lambda: T._lei(Vd)), ("_zero", lambda: T._zero(Vd)), ("_disco", lambda: T._disco(Vd)), ("_obs", lambda: T._obs(Vd)), ("_ident", lambda: T._ident(Vd)), ("_ga", lambda: T._ga(Vd)), ("_massa", lambda: T._massa(Vd)),',
              '("_moldura", lambda: T._moldura(Vd)), ("_escopo", lambda: T._escopo(Vd)), ("_ancoras", lambda: T._ancoras(Vd)), ("_chaves", lambda: T._chaves(Vd)), ("_diznao", lambda: T._diznao(Vd)), ("_ressalvas", lambda: T._ressalvas(Vd)), ("_leituras", lambda: T._leituras(Vd)), ("_blocos_fecho", lambda: T._blocos_fecho(Vd)),')
    t = A.sub(t, "_REGS_NOVOS = ['ponte_da_massa_v405', 'massa_tensao_pura_v405', 'identidade_v405', 'observador_terminal_v405', 'lei_do_diminuto_v405', 'tonica_do_hamiltoniano_v405', 'disco_de_euler_v405', 'ponto_zero_do_psion_v405', 'cunhagens_v405', 'campos_fechados_e_leituras_v405', 'ga_reclassificacao_v405', 'gap_v405', 'kh_n1_cobertura_v405']",
              "_REGS_NOVOS = ['fechamento_v406', 'cunhagens_v406', 'kh_n1_cobertura_v406']")
    t = A.sub(t, "<!-- INICIO_PARAGRAFO_MASSA_DERIVADA_E_IDENTIDADE_v406 -->", "<!-- INICIO_PARAGRAFO_O_FECHAMENTO_v406 -->")
    t = A.sub(t, "<!-- FIM_PARAGRAFO_MASSA_DERIVADA_E_IDENTIDADE_v406 -->", "<!-- FIM_PARAGRAFO_O_FECHAMENTO_v406 -->")
    t = A.sub(t, "_bd.modulos_novos == 8", "_bd.modulos_novos == DL.N_BUNDLE")
    # ---- o paragrafo novo (4c)
    t = A.sub(t, "# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (a massa derivada e a identidade definida): verificacao propria, controles negativos, a citacao verbatim, a NOTA ao lado do paragrafo da v405 e o handoff que diz que os paragrafos do testemunho, da falsidade e da v405 seguem como estao",
              "# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (o fechamento): verificacao propria, controles negativos, a citacao verbatim, a NOTA ao lado dos paragrafos anteriores e o handoff que diz que os paragrafos do testemunho, da falsidade e da v405 seguem como estao")
    t = A.entre(t, '    _pv = _core_p["ponte_da_massa_v405"]["values"]', "    for n_ in _NEGS:\n        print(\"  controle negativo do paragrafo da v406", NUMS_4C)
    t = A.sub(t, 'all(x in _ERR for x in ("POSTO", "REGISTRO", "`ProjecaoTransversalDaMeiaNat`", "`Jo8v32`", "fica como registro"))', 'all(x in _ERR for x in ("E14", "NÃO foram editados", "fica como registro"))')
    t = A.sub(t, "paragrafo novo (a massa derivada e a identidade definida): positivo ok;", "paragrafo novo (o fechamento): positivo ok;")
    # ---- os hashes lidos
    t = A.sub(t, 'HEX16.update(v["sha16"] for v in ESP["pedras"].values());', 'HEX16.update(v["sha16"] for v in (ESP.get("pedras") or {}).values()); HEX16.add(DL.TESTEMUNHA["sha16_da_ordem"]); HEX16.update(b_["sha256"][:16] for b_ in DL.BUNDLE_POR_REL.values());')
    t = A.sub(t, '"cita_verbatim_passa": (T._cita("é isso , perfeito, concordo com tudo") == "«é isso , perfeito, concordo com tudo»"),'+chr(10)+'           "cita_com_aspas_do_operador_passa": T._cita("o meu um absoluto é o um de 1 eV").startswith("«o meu um"),',
              '"cita_verbatim_passa": (T._cita(DL.FRASE_CONSTRUIR) == "«" + DL.FRASE_CONSTRUIR + "»"),'+chr(10)+'           "cita_com_aspas_do_operador_passa": T._cita(DL.FRASE_PASSAGEM).startswith("«a construção"),')
    t = A.sub(t, '_RN = ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404"]', '_RN = ["fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406"]')
    A.grava(nome, t, crlf, raw)
