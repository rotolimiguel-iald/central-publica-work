# -*- coding: utf-8 -*-
# regras (lote F) de derivar_encanamento_v400.py: instalar, reverter e rito. Escrito pela ferramenta Write. (O p00_precondicoes e o refazer_candidato sao ESCRITOS A MAO para a v400: nao derivados.)
# O que a v400 muda aqui: (1) o canonico de partida e' a v399 SELADA e a Bancada AINDA pina a v398, entao o recibo pre_selo (o da cadeia v399) e' do um.py v398, nao do que esta no Nos; (2) a lista dos modulos novos e' VAZIA;
# (3) o sidecar um_absoluto_selo_acom.json (arquivo que a v399 criou e o rito reescreve) entra nos backups e na reversao; (4) a pedra Testemunho, da v399, ja esta no kernel do Nos.

entrada("instalar_v399.py", autoral=True, regras=[
    sub_n(r"(?m)^  \* o recibo pre_selo do B\(n\) \(PINO_RECIBO_PRE_SELO_v400\.json\)[^\n]*\n",
          "  * o recibo pre_selo do B(n) (PINO_RECIBO_PRE_SELO_v400.json: o da CADEIA v399, gerado e pinado ANTES da instalacao da v399, em ensaio, sobre o um.py v398 que a Bancada de producao AINDA pina) tem de existir, estar pinado (sha256 do arquivo == o do pino) e ser UTILIZAVEL; a Bancada de producao tem de seguir pinando a v398 (o sha256 do manifesto dela == o do pino);\n", 1, "docstring do recibo"),
    sub_n(r"(?m)^  \* nenhum processo um\.py ou trabalhador do pilar rodando[^\n]*\n",
          "  * nenhum processo um.py ou trabalhador do pilar rodando (a v400 NAO traz modulo novo de kernel: a lista kernel_modulos_novos_v400.json e' VAZIA, lida do arquivo; o kernel do Nos e' o da v399, com a pedra Testemunho; o proprio rito materializa o corpo embutido, identico);\n", 1, "docstring dos modulos"),
    ('PINO["versao_nos"] == "v399" and PINO["um_py_sha16_do_nos"] == h16(raw0), "o recibo pre_selo nao e\' utilizavel ou nao e\' do um.py que esta no Nos -- nao instalo"',
     'PINO["versao_nos"] == "v398" and PINO["um_py_sha16_do_nos"] == json.load(open(os.path.join(HERE, "base_v398", "um_absoluto_selo.json"), encoding="utf-8"))["sha256"]["um.py"][:16], "o recibo pre_selo nao e\' utilizavel ou nao e\' do um.py v398 que a Bancada pina -- nao instalo"\n'
     '_bmp = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "canonical_contracts.json"); _bmb = open(_bmp, "rb").read(); _bm = json.loads(_bmb.decode("utf-8"))\n'
     'assert hashlib.sha256(_bmb).hexdigest() == PINO["valido_enquanto"]["bancada_pina"]["manifesto_sha256"] and _bm["canonical"].get("version") == "v398", "a Bancada de producao nao pina mais o que o recibo pre_selo diz (re-pino antes do B(n)): o recibo ficou obsoleto -- nao instalo"', 1),
    ('"Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas")', '"Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho")', 1),
    ("(b) o modulo novo da v400 (Testemunho) NAO esta la ainda.", "(b) a v400 NAO traz modulo novo (a lista e' vazia): a pedra Testemunho, da v399, JA esta no kernel do Nos.", 1),
    ('"um_absoluto_pilar_quantico.json",\n            os.path.join("tgl_kernel", "TGLExt.lean")', '"um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json",\n            os.path.join("tgl_kernel", "TGLExt.lean")', 1),
    ("  * BACKUP DE BYTES de um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean;", "  * BACKUP DE BYTES de um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, o SIDECAR um_absoluto_selo_acom.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean;", 1),
])

entrada("reverter_v399.py", autoral=True, regras=[
    ('"um_absoluto_pilar_quantico.json",\n                                os.path.join("tgl_kernel", "TGLExt.lean")', '"um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json",\n                                os.path.join("tgl_kernel", "TGLExt.lean")', 1),
    ("restaura os 8 backups de BYTES (um.py, core, selo, .md, manifesto, pilar, TGLExt.lean, TGL/Audit.lean)", "restaura os 9 backups de BYTES (um.py, core, selo, .md, manifesto, pilar, o sidecar um_absoluto_selo_acom.json, TGLExt.lean, TGL/Audit.lean)", 1),
])

_HDR_RITO = '''# O RITO v400 (ato da gerencia c1, 24/10/2026): roda o um.py v400 instalado no Nos -- a CORRECAO da v399 (a secao do selo ACOM deixa de redeclarar alfa e le o SEALED_CODATA_ALPHA; a checagem do beta do registro confronta com o beta do core): NENHUM modulo novo de kernel
# (a lista kernel_modulos_novos_v400.json e' VAZIA; o kernel e o Audit sao os da v399, byte a byte; o proprio um.py materializa o corpo embutido, identico, e os constroi), os registros da v399 (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, cunhagens_v399 e kh_n1_cobertura_v399)
# RECRIADOS no mesmo ponto do main (o selo e a declaracao logo depois da afinacao das cordas), o SIDECAR um_absoluto_selo_acom.json (escrito depois da ultima escrita do selo) e a errata ao lado no artigo PT/EN e no .md canonico. O QUADRO do Teste da Unica Palavra segue no topo.
# O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (a mesma da v399); TGL_RITE_CHECKPOINT DESLIGADO. Molde: o script do rito da v399 herdado com as afericoes dele, trocados os nomes, o pacote (a propria pasta da cadeia v400) e a
# guarda do marcador anterior: echo 1 | python um.py no Nos, stdout canonico em rodada_v400_stdout.txt, trailer RITO_RC=<rc>, horarios no pacote. RODADA COMPLETA.
'''
_TEMPO = ("# TEMPO ESPERADO (v400): o kernel e' o da v399 (nenhum modulo novo). No sandbox k400c, `lake build` com a raiz e o Audit RECOMPILADOS = 697 s e 1 Audit = 376 s (kernel/construir_marcas.txt, MEDIDO em 24/10); no Nos o kernel JA esta compilado (rito da v399), logo as 3 passagens de build + Audit do rito\n"
          "# sao incrementais: a ordem de grandeza e' a do rito real da v399 (14:07:28 -> 16:16:02, 2 h 08 min, rc 0; v399/rito_horarios_v399.txt), fora a GPU. O timeout do lake build DENTRO do um.py (candidato) tem de caber nisso: conferir no candidato.\n")

entrada("rito_v399.sh", autoral=True, regras=[
    entre("# O RITO v400 (ato da gerencia c1, 24/10/2026)", "# O SERVIDOR DO MODELO NATIVO", _HDR_RITO, "cabecalho do rito"),
    sub_n(r"(?m)^# TEMPO ESPERADO \(v400[^\n]*\n", _TEMPO, 1, "tempo esperado"),
])
