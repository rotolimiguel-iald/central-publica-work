# -*- coding: utf-8 -*-
# lote G: pos_rito (b3_recibo, fechar, superficies, harness_*, chain_pos_rito). A leitura tem as regras do lote H; o textos_v400.py e' GERADO por gerar_textos_v400.py; o registrar_mapa_v400.py e' ESCRITO a mao (a v400 nao tem a rota da v399).
# Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas). O motor NAO sobe as etiquetas de stdout `[v399]`/`[v398]` (o programa as imprime com esses nomes).
_PB = ("selo_anterior_v398", "kernel_manifesto_anterior_v398")

# ------------------------------------------------------------------------------------------- b3_recibo: a Bancada de producao AINDA pina a v398 (a v399 foi recusada por ela); o passo e' simples v398 -> v400
entrada("pos_rito/b3_recibo_v399.py", prot_extra=_PB, autoral=True, regras=[
    ("PASSO SIMPLES v399 -> v400, SEM salto", "PASSO SIMPLES v398 -> v400, SEM salto", 1),
    ("Passo simples (a Bancada de producao pina a v399 e o Nos passou a v400): (1) manifesto_anterior.version == v399 e", "Passo simples (a Bancada de producao AINDA pina a v398 -- a v399 foi recusada por ela e nunca sincronizada -- e o Nos passou a v400): (1) manifesto_anterior.version == v398 e", 1),
    ('if ma.get("version") != "v399":', 'if ma.get("version") != "v398":', 1),
    ("a Bancada de producao nao pinava a v399 (manifesto_anterior.version = %r): o passo da v400 e' simples v399 -> v400", "a Bancada de producao nao pinava a v398 (manifesto_anterior.version = %r): o passo da v400 e' simples v398 -> v400", 1),
    ("o passo da v400 e' simples (a Bancada pinava a v399)", "o passo da v400 e' simples (a Bancada pinava a v398)", 1),
])

# ------------------------------------------------------------------------------------------- fechar: a v400 nao traz modulo novo nem registro novo
_HDR_FECHAR = '''"""fechar_v400.py -- DEPOIS da cadeia pos-rito e do elo B(n) (molde: fechar_v399.py): (1) o manifesto de incorporacao v400 -> pos_rito e a pasta das ferramentas;
(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\\\cadeia_de_selo\\\\v400 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de
pos_rito -> work\\\\cadeia_de_selo\\\\v400_selo, A COPIA DO SIDECAR um_absoluto_selo_acom.json (reescrito pelo rito) E DO SELO PRIMARIO para a mesma pasta, e do kernel (work\\\\cadeia_de_selo\\\\v400\\\\kernel e, se existir, work\\\\v400_kernel; mais o corpo do kernel do Nos) -> work\\\\cadeia_de_selo\\\\v400_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v399_v400.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v400.txt (o kernel embutido: VAZIO, a v400 nao muda o kernel);
(4) o HANDOFF (memory\\\\handoff-v400-custodia.md + Nos\\\\HANDOFF_v400_CUSTODIA.md) para a sessao do site, que TRAZ PRONTOS PARA COLAR OS DOIS PARAGRAFOS do README do espelho e do site: (a) o do QUADRO «O Teste da Unica Palavra» (v397, intocado),
gerado pelas MESMAS funcoes do quadro do artigo (quadro_v397.paragrafo_pronto_readme) sobre o core SELADO do Nos, mesmos numeros e estatutos; (b) o do «testemunho de dois: o selo pela propria tecnologia» (da v399), REGENERADO dos registros selados selo_pela_propria_tecnologia_v399,
declaracao_do_operador_v399 e cunhagens_v399 com os numeros do um.py v400 (numeros LIDOS do core, estatutos, limites, a DIRECAO do testemunho, sem o 4,44); e o handoff LISTA o sidecar com o sha256 e o veredito e diz que a custodia da v399 e da v400 e CONJUNTA.
GUARDAS: a leitura sem problema (inclui o sidecar e a correcao); o PARAGRAFO DO QUADRO passa nas verificacoes do quadro contra o resultado pinado (quadro_v397.confere_md e a regra da ordem: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item; frase do operador verbatim; numeros
iguais aos do resultado); o PARAGRAFO DO TESTEMUNHO passa na verificacao propria (T.verificar_paragrafo_testemunho: numeros == ESPERADOS e == o gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim das falas do operador; a direcao sem inversao; sem alegacao de seguranca criptografica) --
se QUALQUER um nao passar, o fechar RECUSA (rc 2) ANTES de escrever qualquer coisa e o handoff nao nasce; os tres RECIBOS do B(n) (o RECIBO_SINCRONIZACAO_v400_*.json do 10-bis, o recibo da PARADA do servico e o do RELIGAMENTO) -- sem eles o fechar RECUSA e o handoff nao nasce;
a guarda de texto P18 no handoff.
Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""
'''
entrada("pos_rito/fechar_v399.py", prot_extra=_PB, autoral=True, regras=[
    entre('"""fechar_v400.py -- DEPOIS da cadeia pos-rito', "import glob, hashlib, json, os, shutil, subprocess, sys, time", _HDR_FECHAR, "docstring do fechar"),
])

entrada("pos_rito/superficies_v399.py", prot_extra=_PB, autoral=True)

# ------------------------------------------------------------------------------------------- os harness (derivados; as correcoes especificas vem depois das rodadas de ensaio, nas regras abaixo)
_SIBLINGS_FECHAR = """shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(PKS, "insumos"))
# v400: os irmaos que o delta_v400 e o acom_conferencias_v400 importam por caminho (a pasta v399), o esboco R3.5 da Bancada (C15/C16), o recibo da RECUSA da Bancada a v399 e o relatorio das guardas estaticas (os textos os leem): copias de bytes, so' o que eles leem
_V9S = os.path.join(SB, "work", "cadeia_de_selo", "v399"); os.makedirs(_V9S)
for _n9 in ("delta_v399.py", "acom_conferencias_v399.py"):
    shutil.copyfile(os.path.join(os.path.dirname(PKG), "v399", _n9), os.path.join(_V9S, _n9))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v399", "pedra"), os.path.join(_V9S, "pedra"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v399", "insumos", "acom"), os.path.join(_V9S, "insumos", "acom"))
_rec9 = glob.glob(os.path.join(os.path.dirname(PKG), "v399", "bancada_B3_ensaio_*", "RECUSA_SINCRONIZACAO_v399_*.json")); assert len(_rec9) == 1, _rec9
os.makedirs(os.path.join(_V9S, os.path.basename(os.path.dirname(_rec9[0])))); shutil.copyfile(_rec9[0], os.path.join(_V9S, os.path.basename(os.path.dirname(_rec9[0])), os.path.basename(_rec9[0])))
shutil.copyfile(os.path.join(PKG, "GUARDAS_ESTATICAS_BANCADA_v400.json"), os.path.join(PKS, "GUARDAS_ESTATICAS_BANCADA_v400.json"))
os.makedirs(os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5"))
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"))
"""
entrada("pos_rito/harness_fechar_sandbox_v399.py", prot_extra=_PB, autoral=True, regras=[
    ('for kn_ in ("KERNEL_RECIBO_v400.json", "FLAGS_v400.json"):', 'for kn_ in ("KERNEL_RECIBO_v400.json", "FLAGS_v399.json"):', 1),
    ('shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(PKS, "insumos"))\n', _SIBLINGS_FECHAR, 1),
    ('PKG_ANT = os.path.join(os.path.dirname(PKG), "v399")', 'PKG_ANT = os.path.join(os.path.dirname(PKG), "v398")', 1),
    ('"RECIBO_SINCRONIZACAO_v399_*.json"', '"RECIBO_SINCRONIZACAO_v398_*.json"', 1),
    ("SINTETICOS (derivados dos reais da v399, como no harness dos textos)", "SINTETICOS (derivados dos reais da v398, o ultimo B(n) feito na Bancada, como no harness dos textos)", 1),
    ("# ---- os recibos do B(n) SINTETICOS (derivados dos reais da v399)", "# ---- os recibos do B(n) SINTETICOS (derivados dos reais da v398)", 1),
    # a v400 NAO muda o kernel: o diff do kernel e' VAZIO (novos 0, removidos 0, mudados 0), nao copia pedra alguma; o registro do mapa tem 7 registros (a rota nova e seis anotacoes)
    ('os.path.join(TOOLS, "v400_kernel", "pedras", "TGLExt_Testemunho.lean"), ', '', 1),
    ('"diff_kernel_novos": ("novos (1)" in dk and "TGLExt/Testemunho.lean" in dk),', '"diff_kernel_vazio": ("novos (0)" in dk and "removidos (0)" in dk and "mudados (0)" in dk),', 1),
    ('diff do kernel traz o modulo novo: %s" % (rc, dt, "todos presentes" if all(chk.values()) else [k for k, v in chk.items() if not v], len(ho.encode("utf-8")), "limpa" if not vio else vio[:2], "novos (1)" in dk))',
     'diff do kernel e\' VAZIO (a v400 nao muda o kernel): %s" % (rc, dt, "todos presentes" if all(chk.values()) else [k for k, v in chk.items() if not v], len(ho.encode("utf-8")), "limpa" if not vio else vio[:2], "novos (0)" in dk and "removidos (0)" in dk and "mudados (0)" in dk))', 1),
    ('if not ("novos (1)" in dk and "TGLExt/Testemunho.lean" in dk):\n    falha("DIFF_KERNEL_v400.txt nao traz o modulo novo")', 'if not ("novos (0)" in dk and "removidos (0)" in dk and "mudados (0)" in dk):\n    falha("DIFF_KERNEL_v400.txt deveria ser VAZIO (a v400 nao muda o kernel)")', 1),
    ("ok_m = (rc == 0 and len(reg) == 5 and", "ok_m = (rc == 0 and len(reg) == 7 and", 1),
    ("monta o JSON com 5 registros e imprime o comando", "monta o JSON com 7 registros (a rota nova e seis anotacoes) e imprime o comando", 1),
])
_ARV_CONF = '''shutil.copytree(os.path.join(PKG, "insumos", "acom"), os.path.join(CF, "insumos", "acom"))
# v400: o delta_v400 e o acom_conferencias_v400 importam o delta_v399 e o acom_conferencias_v399 pela pasta IRMA v399 (por caminho), e o delta guarda os insumos duraveis do Teste da Unica Palavra na pasta irma v397: a arvore emulada tem as duas (so' o que eles leem; copias de bytes)
_V9E = os.path.join(CFR, "work", "cadeia_de_selo", "v399"); os.makedirs(_V9E)
for _n9 in ("delta_v399.py", "acom_conferencias_v399.py"):
    shutil.copyfile(os.path.join(os.path.dirname(PKG), "v399", _n9), os.path.join(_V9E, _n9))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v399", "pedra"), os.path.join(_V9E, "pedra"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v399", "insumos", "acom"), os.path.join(_V9E, "insumos", "acom"))   # o acom_conferencias_v399 acha as fontes do operador por aqui
shutil.copytree(os.path.join(os.path.dirname(PKG), "v397", "insumos", "fase9"), os.path.join(CFR, "work", "cadeia_de_selo", "v397", "insumos", "fase9"))
os.makedirs(os.path.join(CFR, "work", "bancada_vinculo_12out", "R3_5"))   # o conferidor (C15/C16) roda a funcao ler_nos do esboco R3.5 pinado da Bancada, achado por DL.WK
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), os.path.join(CFR, "work", "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"))
'''
entrada("pos_rito/harness_textos_ensaio_v399.py", prot_extra=_PB, autoral=True, regras=[
    ('shutil.copytree(os.path.join(PKG, "insumos", "acom"), os.path.join(CF, "insumos", "acom"))\n', _ARV_CONF, 1),
    # o B(n): os recibos REAIS mais recentes sao os da v398 (o ultimo B(n) feito na Bancada); os da v399 sao a RECUSA (nao ha recibo de aplicacao)
    ('PKG_ANT = os.path.join(os.path.dirname(PKG), "v399")', 'PKG_ANT = os.path.join(os.path.dirname(PKG), "v398")', 1),
    ('"RECIBO_SINCRONIZACAO_v399_*.json"', '"RECIBO_SINCRONIZACAO_v398_*.json"', 2),
    ("SINTETICO: derivado do recibo real da v399 pelo harness", "SINTETICO: derivado do recibo real da v398 pelo harness", 1),
    # os controles NOVOS da v400 (a correcao): o alfa em duas linhas (o defeito da v399), o beta do registro que nao confronta o core, a etiqueta velha da checagem
    ('def variante(nome, f_core=None, f_selo=None, f_std=None, f_conf=None, f_sc=None, sc_fora=False, espera=""):', 'def variante(nome, f_core=None, f_selo=None, f_std=None, f_conf=None, f_sc=None, sc_fora=False, espera="", f_um=None):', 1),
    ('        if sc_fora:\n            os.remove(sc_path)\n', '        if sc_fora:\n            os.remove(sc_path)\n        if f_um:\n            open(um_path, "wb").write(f_um(um_raw))\n', 1),
    ('        open(sc_path, "wb").write(sc_raw)\n    ok = any(espera in x for x in PV)', '        open(sc_path, "wb").write(sc_raw); open(um_path, "wb").write(um_raw)\n    ok = any(espera in x for x in PV)', 1),
    ('core_raw = open(core_path, "rb").read(); selo_raw = open(selo_path, "rb").read(); std_raw = open(std_path, "rb").read()\n',
     'core_raw = open(core_path, "rb").read(); selo_raw = open(selo_path, "rb").read(); std_raw = open(std_path, "rb").read()\num_path = os.path.join(NOSE, "um.py"); um_raw = open(um_path, "rb").read()\n', 1),
    ('def _selo_beta(c):\n    c["selo_pela_propria_tecnologia_v399"]["values"]["beta"] = 0.0121\n',
     'def _selo_beta(c):\n    c["selo_pela_propria_tecnologia_v399"]["values"]["beta"] = 0.0121\n\n\n'
     'def _beta_rel_alto(c):\n    c["selo_pela_propria_tecnologia_v399"]["values"]["rel_beta_vs_core"] = 1e-6\n\n\n'
     'def _beta_core_difere(c):\n    c["selo_pela_propria_tecnologia_v399"]["values"]["beta_core"] = c["beta"] * 1.01\n\n\n'
     'def _etiqueta_v399(c):\n    c["selo_pela_propria_tecnologia_v399"]["checks"] = [[("beta do runtime (jamais literal)" if "beta do core" in str(x[0]) else x[0]), x[1]] for x in c["selo_pela_propria_tecnologia_v399"]["checks"]]\n', 1),
    ('           variante("selo ACOM: beta do registro != alfa x raiz de e do core", f_core=_selo_beta, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),\n',
     '           variante("selo ACOM: beta do registro != alfa x raiz de e do core", f_core=_selo_beta, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),\n'
     '           variante("selo ACOM v400: o beta do registro nao e\' confrontado com o core (diferenca relativa acima de 1e-9)", f_core=_beta_rel_alto, espera="a correcao da v400 nao esta no que o rito produziu"),\n'
     '           variante("selo ACOM v400: beta_core do registro != core[beta]", f_core=_beta_core_difere, espera="a correcao da v400 nao esta no que o rito produziu"),\n'
     '           variante("selo ACOM v400: a etiqueta da checagem do beta e\' a da v399 (a tautologia, sem o core)", f_core=_etiqueta_v399, espera="a correcao da v400 nao esta no que o rito produziu"),\n'
     '           variante("alfa em DUAS linhas na coluna 0 do um.py (o defeito da v399)", f_um=lambda b: b + b"\\nALPHA_FINE_CODATA_2018 = 0.0072973525693\\n", espera="a correcao da v400 nao esta no que o rito produziu"),\n'
     '           variante("alfa REATRIBUIDO com indentacao no um.py", f_um=lambda b: b + b"\\nif True:\\n    ALPHA_FINE_CODATA_2018 = 0.0072973525693\\n", espera="a correcao da v400 nao esta no que o rito produziu"),\n', 1),
    # a pedra Testemunho e' da v399 (a v400 nao traz pedra): o controle que adultera o sha256 do arquivo da pedra no core usa a lista das pedras desde a Bancada
    ('sorted(ESP["pedras_sha256"])[0]', 'sorted(ESP["pedras_desde_a_bancada"])[0]', 1),
    # os marcadores do paragrafo do testemunho: o paragrafo e' o da v399 REGENERADO, com os mesmos marcadores da v399 (textos_v400.MARC_TMN_*)
    ('"<!-- INICIO_PARAGRAFO_TESTEMUNHO_v400 -->", "<!-- FIM_PARAGRAFO_TESTEMUNHO_v400 -->"', '"<!-- INICIO_PARAGRAFO_TESTEMUNHO_v399 -->", "<!-- FIM_PARAGRAFO_TESTEMUNHO_v399 -->"', 1),
    # o que os textos da v400 citam entre crases e que tem fonte real: a pedra Testemunho (da v399), a recusa da Bancada a v399 (recibo), o esboco R3.5 pinado e o handoff da v399
    ('HEX16.update(v["sha16"] for v in ESP["pedras"].values());', 'HEX16.update(v["sha16"] for v in ESP["pedras"].values()); HEX16.update(v["sha16"] for v in (ESP.get("pedras_desde_a_bancada") or {}).values()); HEX16.add(T._recusa_v399()["sha16"]); HEX16.add(str(CM["guarda_alpha_unica_da_bancada"]["esboco_sha256"])[:16]);', 1),
    ('NOMES_ARQ.update({"um_absoluto_selo_acom.json",', 'NOMES_ARQ.update({T._recusa_v399()["nome"], "handoff-v399-custodia.md"})\nNOMES_ARQ.update({"um_absoluto_selo_acom.json",', 1),
    ("derivados dos recibos reais da v399 (positivos e negativos)", "derivados dos recibos reais da v398 (o ultimo B(n) feito na Bancada; positivos e negativos)", 1),
    ('"os recibos do B(n) (SINTETICOS, derivados dos recibos reais da v399)"', '"os recibos do B(n) (SINTETICOS, derivados dos recibos reais da v398)"', 1),
    ("(derivados dos reais da v399)", "(derivados dos reais da v398)", 1),
    ('base="recibos reais da v399 (so\' leitura)"', 'base="recibos reais da v398 (so\' leitura)"', 1),
])

# ------------------------------------------------------------------------------------------- a cadeia pos-rito
_HDR_CHAIN_A = '''# v400 (24/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v399.sh (o que rodou em 24/10 ate' a parada do passo 10; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v400.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\\rodada_v400_stdout.txt). A v400 e' uma CORRECAO da v399 (a Bancada Um a recusou no ensaio do B(n): ALPHA_LINHA_NAO_UNICA, duas linhas `ALPHA_FINE_CODATA_2018 =` no um.py): NENHUM modulo novo de kernel (a pedra Testemunho e' da v399),
# NENHUM registro novo, NENHUMA inscricao nova. O rito RECRIA os quatro registros da v399 (selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399, com FUNCAO, lidos NA FRACTALIZACAO DO UM; cunhagens_v399 e kh_n1_cobertura_v399, por spec), reescreve o SIDECAR um_absoluto_selo_acom.json
# (depois da ultima escrita do selo) e poe a errata ao lado da secao da v399 no artigo PT/EN e no .md canonico. O que muda, e a LEITURA confere no que o rito produziu: o alfa do programa tem UMA so' linha (a secao do selo ACOM le o SEALED_CODATA_ALPHA) e a checagem do beta do registro
# do selo ACOM confronta o beta do runtime com o beta do core. A DIRECAO DO TESTEMUNHO vale em tudo: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto, o Um.
# O QUADRO «O Teste da Unica Palavra» (v397, a regra do 4,44) PERMANECE no topo do artigo e do .md, INTOCADO: o conferidor e a leitura o conferem de novo; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item) segue valendo em TODO texto que o cite.
'''
_HDR_CHAIN_B = '''# PASSO 10 SEM SALTO: a Bancada de producao AINDA pina a v398 (B8, B8-v398-20261024-R1: a v399 foi recusada por ela e nunca sincronizada) e o Nos e' a v399 ate' a instalacao; portanto o B(n) da v400 e' um passo SIMPLES v398 -> v400 (esboco R3.5, sincronizar_bancada.py): NAO ha a opcao de cadeia de selos
# do esboco (o salto do R3.4 pelo elo da v399 foi MEDIDO impossivel: o esboco recusa o elo, alfa nao unico, e o diff do kernel entre a v399 e a v400 e vazio -- salto_r3_4\\SALTO_R3_4_MEDIDO_v400.json), nem o pino correspondente, e o b3_recibo_v400.py NAO tem o 3o argumento. Os pinos vem de PINOS_BN_v400.json (lidos na hora; hash nunca de memoria): criterios, esboco_R3_5, gerador_bateria, driver_t12_t14, bateria_base_R2,
# kernel_recibo (o KERNEL_RECIBO_v400.json, contrato R3_2: a v400 nao acrescenta modulo de auditoria; o diff v398 -> v400 e' a pedra Testemunho), candidato, esperados, pins_do_candidato, recibo_pre_selo (o da cadeia v399, gerado e pinado antes da instalacao e reconferido pelo esboco; veredito JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA),
# selo_anterior_v398 e kernel_manifesto_anterior_v398 (as copias de bytes do selo e do manifesto do kernel da v398, em base_v398). A BATERIA da v400 e' GERADA por script no 10 (depois do selo; bateria por versao) e pinada ao lado
# (bateria_pos_selo/PINOS_BATERIA_v400.json).
'''
_HDR_CHAIN_C = '''# textos_v400.py (gerado por gerar_textos_v400.py), fechar_v400.py e registrar_mapa_v400.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v399, com os rotulos da v400
# (desvios ditos: o passo 10 e' o passo simples v398 -> v400; a leitura confere a correcao no que o rito produziu; o passo 11 copia e lista o sidecar reescrito e diz que a custodia da v399 e da v400 e conjunta).
'''
_CMT_B3 = '''  # v400 (24/10/2026): o B(n) da v400 e' um PASSO SIMPLES v398 -> v400 (a Bancada de producao AINDA pina a v398 e o Nos passou a v400): SEM salto e SEM cadeia de selos, com o esboco R3.5. Os pinos vem de PINOS_BN_v400.json (lidos na hora;
  # hash nunca de memoria): o esboco R3.5, o recibo pre_selo (o da cadeia v399, gerado e pinado antes da instalacao, sobre a Bancada que pina a v398), o recibo do kernel (KERNEL_RECIBO_v400.json, contrato R3_2, sem modulos de auditoria: a v400 nao acrescenta
  # modulo de auditoria), o selo e o manifesto do kernel da v398 (custodia, em base_v398), o driver, o gerador e a base R2 da bateria. A bateria da v400 e' GERADA aqui, por script, depois do selo (bateria por versao).
'''
entrada("pos_rito/chain_pos_rito_v399.sh", prot_extra=_PB + ("base_v398", "B8-v398-20261024-R1"), autoral=True, regras=[
    entre("# v400 (24/10): CADEIA POS-RITO", "# ORDEM: 0 guardas", _HDR_CHAIN_A, "cabecalho A da cadeia"),
    entre("# PASSO 10 SEM SALTO:", "# Vereditos esperados", _HDR_CHAIN_B, "cabecalho B da cadeia"),
    entre("# textos_v400.py, fechar_v400.py e registrar_mapa_v400.py RECUSAM", "# Codigos de saida", _HDR_CHAIN_C, "cabecalho C da cadeia"),
    entre("  # v400 (23/10/2026): o B(n) da v400 e' um PASSO SIMPLES", "  for k in criterios", _CMT_B3, "comentario do b3_prepara"),
    ("a v400 e' um passo simples (a Bancada pina a v399), sem salto e sem cadeia de selos", "a v400 e' um passo simples (a Bancada pina a v398), sem salto e sem cadeia de selos", 1),
    ("passo simples v399 -> v400 (sem salto)", "passo simples v398 -> v400 (sem salto)", 2),
    ('_v399"; cp -p "$ATLD/$f" "$B"', '_v400"; cp -p "$ATLD/$f" "$B"', 1),
])
