# -*- coding: utf-8 -*-
"""_fork_b_servico_v411.py -- (claude-construtor-v411, retomada, fork B, 12/11/2026) adapta de verdade os cinco scripts de bancada_B3_servico\\ a v411: a ORDEM da v411 e' a fala do operador de 12/11/2026
(OPERADOR_12nov_otimo_vamos_rodar_tudo_pode_abrir_chegou_a_hora_da_v411_verbatim.txt: o arquivo e' so' a fala; a fala inteira e' LIDA do arquivo, nunca digitada; o sha16 calculado na hora); as datas das ordens
anteriores (01 a 11/11) nao podem sobrar; no modo de ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1) as saidas do conferidor e do controle negativo vao para a pasta de ensaio (fora de work\\).
Nada do servico e' executado. uso: python -B -X utf8 _fork_b_servico_v411.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _fork_b_lib_v411 as L  # noqa: E402

N_ORDEM = "OPERADOR_12nov_otimo_vamos_rodar_tudo_pode_abrir_chegou_a_hora_da_v411_verbatim.txt"
assert os.path.isfile(os.path.join(os.path.dirname(os.path.dirname(L.HERE)), "cunhagens_13out", N_ORDEM))
N_ANT = "OPERADOR_06nov_a_forma_da_matriz_finita_e_o_signo_tudo_entra_no_um_py_verbatim.txt"

BLOCO_ORDEM_ANT = ('# a autorizacao tem de ser a ORDEM da v411, de 06/11/2026 (nao a de 05/11 da v410 nem as anteriores): o sha16 da fala vem do ARQUIVO lido agora (nunca digitado) e a frase tem de estar no arquivo e no texto passado pelo orquestrador\n'
                   'ORDEM = os.path.join(D, "..", "..", "..", "cunhagens_13out", "' + N_ANT + '")\n'
                   'ORDEM_BYTES = open(ORDEM, "rb").read()\n'
                   'ORDEM_SHA16 = hashlib.sha256(ORDEM_BYTES).hexdigest()[:16]\n'
                   'FRASE_DA_ORDEM = "A forma de uma matriz finita no kernel é o signo (traço com sentido)"\n'
                   'assert FRASE_DA_ORDEM in ORDEM_BYTES.decode("utf-8") and FRASE_DA_ORDEM in AUT and ORDEM_SHA16 in AUT and "06/11/2026" in AUT, "a autorizacao passada nao e\' a ordem do operador de 06/11/2026 (a ordem da v411: sha16 da fala lido do arquivo e a frase «%s» no texto)" % FRASE_DA_ORDEM\n')
BLOCO_ORDEM_NOVO = ('# a autorizacao tem de ser a ORDEM da v411, de 12/11/2026 (a ordem de abrir e a ordem da v411, D169; nao a da v410 nem as anteriores): o sha16 da fala vem do ARQUIVO lido agora (nunca digitado), a fala INTEIRA e\' lida do arquivo\n'
                    '# (o arquivo e\' so\' a fala do operador) e tem de estar no texto passado pelo orquestrador, com a data\n'
                    'ORDEM = os.path.join(D, "..", "..", "..", "cunhagens_13out", "' + N_ORDEM + '")\n'
                    'ORDEM_BYTES = open(ORDEM, "rb").read()\n'
                    'ORDEM_SHA16 = hashlib.sha256(ORDEM_BYTES).hexdigest()[:16]\n'
                    'FRASE_DA_ORDEM = ORDEM_BYTES.decode("utf-8").strip()   # a fala inteira, LIDA do arquivo (nunca digitada aqui)\n'
                    'assert FRASE_DA_ORDEM in ORDEM_BYTES.decode("utf-8") and len(FRASE_DA_ORDEM) >= 20 and FRASE_DA_ORDEM in AUT and ORDEM_SHA16 in AUT and "12/11/2026" in AUT, "a autorizacao passada nao e\' a ordem do operador de 12/11/2026 (a ordem da v411: o sha16 da fala lido do arquivo e a fala inteira no texto, com a data)"\n')

for rel, docant, docnovo in (("bancada_B3_servico/recibo_parada_v411.py",
                              "A autorizacao e' a ORDEM da v411, do operador, de 06/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado pelo orquestrador).",
                              "A autorizacao e' a ORDEM da v411, do operador, de 12/11/2026 (a ordem de abrir e a ordem da v411, D169; a fala inteira e' lida do arquivo e conferida contra o texto passado pelo orquestrador)."),
                             ("bancada_B3_servico/recibo_religamento_v411.py",
                              "A autorizacao e' a ORDEM da v411, do operador, de 06/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado pelo orquestrador).",
                              "A autorizacao e' a ORDEM da v411, do operador, de 12/11/2026 (a ordem de abrir e a ordem da v411, D169; a fala inteira e' lida do arquivo e conferida contra o texto passado pelo orquestrador).")):
    def _chk(t_):
        assert N_ANT not in t_ and "06/11/2026" not in t_ and "A forma de uma matriz" not in t_ and not any(("%02d/11/2026" % d_) in t_ for d_ in range(1, 12)), "sobrou a ordem da v410 ou data de ordem anterior"
    _h10 = L.linha(rel, "# [ADAPTADO v410, 06/11/2026, claude-construtor-v410]")
    _nh = L.linha(rel, "# (nota herdada da adaptacao da v408")
    _nome = os.path.basename(rel)
    _h11 = ("# (historico: o molde e' v410/bancada_B3_servico/%s, adaptado na v410 a ordem da v410; a copia subiu por rotulo em _bump_copia_v411.py, diff em bump/; o corpo vem da adaptacao da v408 [fork C], "
            "conferido de versao a versao; na v411 so' a ORDEM muda, e as datas das ordens anteriores nao ficam no script porque o conferidor estatico as recusa)" % _nome.replace("_v411.py", "_v410.py"))
    L.aplicar(rel, [(docant, docnovo), (BLOCO_ORDEM_ANT, BLOCO_ORDEM_NOVO), (_h10 + "\n", ""), (_nh, _h11)],
              "a ORDEM da v411 e' a fala do operador de 12/11/2026 (" + N_ORDEM + "; D169): o arquivo e' so' a fala, que e' LIDA inteira do arquivo (nunca digitada), o sha16 calculado na hora, a data 12/11/2026 no AUT; "
              "o resto do corpo (o passo B20, o recibo do religamento da v410 como ultimo conhecido, as chaves do recibo REAL da v410) ja' era o certo: nada de bundle nem de hash digitado", _chk)

# ---- o evento: o corpo ja' e' o certo (versao v411, ESPERADOS_v411.json, candidato_sha16 lido); so' a linha da marca
L.aplicar("bancada_B3_servico/evento_c1_b3_v411.py", [],
          "conferido: o corpo e' o certo para a v411 (versao v411, ESPERADOS_v411.json da pasta da cadeia, candidato_sha16 LIDO e conferido contra o um.py do Nos antes de anotar; passo simples B20); o evento so' roda no rito, depois do APLICAR")

# ---- o conferidor estatico
C = "bancada_B3_servico/conferir_exigencias_servico_v411.py"
_nhC = L.linha(C, "# (nota herdada da adaptacao da v408")
_nhM = L.linha("bancada_B3_servico/controle_negativo/mutar_conferidor_v411.py", "# (nota herdada da adaptacao da v408")
L.aplicar(C, [
    (_nhC, "# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida de versao a versao) molde v410/bancada_B3_servico/conferir_exigencias_servico_v410.py (rotulos subidos por _bump_copia_v411.py; diff em bump/). "
           "Adaptado (v411, 12/11/2026, fork B): a autorizacao conferida e' a ORDEM da v411 (fala de 12/11/2026; nome lido do delta, sha16 calculado do arquivo aqui e nos scripts); nenhuma data de autorizacao anterior (01/11 a 11/11) pode sobrar nos scripts;"),
    ("  (e) a autorizacao e' a ORDEM da v411, do operador, de 06/11/2026 («A forma de uma matriz finita no kernel é o signo (traço com sentido)»): depois do assert AUT, parada e religamento conferem o texto passado contra a fala (o sha16 vem do ARQUIVO da fala, lido na hora; a frase tem de estar no arquivo e no texto); nenhum texto, data ou hash de autorizacao anterior (01/11 a 05/11) sobrou nos scripts;",
     "  (e) a autorizacao e' a ORDEM da v411, do operador, de 12/11/2026 (a ordem de abrir e a ordem da v411, D169; o nome do arquivo LIDO do delta_v411, que o le do DESENHO): depois do assert AUT, parada e religamento conferem o texto passado contra a fala (o sha16 vem do ARQUIVO da fala, lido na hora; a fala INTEIRA e' lida do arquivo e tem de estar no texto); nenhum texto, data (01/11 a 11/11) ou hash de autorizacao anterior sobrou nos scripts;"),
    ("Grava CONFERENCIA_EXIGENCIAS_SERVICO_v411.json ao lado (nao sobrescreve). uso:",
     "Grava CONFERENCIA_EXIGENCIAS_SERVICO_v411.json ao lado (no modo de ensaio do topo proposto, V411_ENSAIO_TOPO_PROPOSTO=1, em <pasta de ensaio>\\\\bancada_B3_servico, fora de work; nao sobrescreve). uso:"),
    ('# (v411) a ORDEM da v411 e a frase dela vem do DELTA desta pasta (sem executar o delta: nome e frase sao lidos do texto dele por ast), conferidos contra o arquivo da fala\n'
     'def _do_delta(nome_):\n'
     '    for n_ in ast.parse(open(os.path.join(V, "delta_v411.py"), encoding="utf-8").read()).body:\n'
     '        if isinstance(n_, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id == nome_ for t_ in n_.targets) and isinstance(n_.value, ast.Constant):\n'
     '            return n_.value.value\n'
     '    return None\n'
     '\n'
     '\n'
     'DL_FRASE_ORDEM = _do_delta("FRASE_ORDEM_V411")\n'
     'DL_N_ORDEM = "' + N_ANT + '"   # (o nome do arquivo da ORDEM da v411; o delta o le do recibo da gerencia: DL.N_ORDEM_V411)\n'
     'assert DL_FRASE_ORDEM, "a frase da ordem nao foi lida do delta_v411"\n',
     '# (v411) a ORDEM da v411 vem do DELTA desta pasta (FALA_ORDEM_V411: o nome e o sha256 que o delta LE do DESENHO_v411 e confere contra o arquivo); a fala INTEIRA e a data saem do proprio arquivo (o arquivo e\' so\' a fala)\n'
     'import importlib.util as _ilu\n'
     '_sp_dl = _ilu.spec_from_file_location("delta_v411_conferir_servico", os.path.join(V, "delta_v411.py")); _DLM = _ilu.module_from_spec(_sp_dl); _sp_dl.loader.exec_module(_DLM)\n'
     'DL_N_ORDEM = _DLM.FALA_ORDEM_V411["nome"]\n'
     '_m_dia = re.match(r"OPERADOR_(\\d\\d)nov_", DL_N_ORDEM); assert _m_dia and "v411" in DL_N_ORDEM, DL_N_ORDEM\n'
     'ORDEM_DATA = "%s/11/2026" % _m_dia.group(1)                                   # a data da ordem, lida do nome do arquivo (12/11/2026)\n'
     'DATAS_ANTERIORES = ["%02d/11/2026" % d_ for d_ in range(1, int(_m_dia.group(1)))]   # as datas das ordens anteriores (01 a 11/11) nao podem sobrar\n'
     'DL_FRASE_ORDEM = open(os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", DL_N_ORDEM), "rb").read().decode("utf-8").strip()\n'
     'assert DL_FRASE_ORDEM and hashlib.sha256(open(os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", DL_N_ORDEM), "rb").read()).hexdigest() == _DLM.FALA_ORDEM_V411["sha256"], "o arquivo da ordem nao e\' o que o delta pinou"\n'
     'OUT_DIR = os.path.join(_DLM.SAIDA, "bancada_B3_servico") if _DLM.ENSAIO_TOPO_PROPOSTO else HERE   # (v411) no ensaio do topo proposto, a saida vai a pasta de ensaio (fora de work)\n'),
    ('''    chk(nome + ": a ordem de 06/11 (a ordem da v411) e' conferida: o assert com ORDEM_SHA16''', '''    chk(nome + ": a ordem de 12/11 (a ordem da v411) e' conferida: o assert com ORDEM_SHA16'''),
    ('''    chk(nome + ": nenhum texto, data ou hash de autorizacao anterior sobrou (01/11/2026 a 05/11/2026, as datas das ordens anteriores; nenhum sha de 16 hex digitado)", all(d_ not in txt for d_ in ("01/11/2026", "02/11/2026", "03/11/2026", "04/11/2026", "05/11/2026")) and re.search(r"[0-9a-f]{16}", txt) is None, [[d_ in txt for d_ in ("01/11/2026", "02/11/2026", "03/11/2026", "04/11/2026", "05/11/2026")], re.findall(r"[0-9a-f]{16}", txt)], [[False, False, False, False, False], []])''',
     '''    chk(nome + ": nenhum texto, data ou hash de autorizacao anterior sobrou (01/11/2026 a 11/11/2026, as datas das ordens anteriores; nenhum sha de 16 hex digitado)", all(d_ not in txt for d_ in DATAS_ANTERIORES) and re.search(r"[0-9a-f]{16}", txt) is None, [[d_ for d_ in DATAS_ANTERIORES if d_ in txt], re.findall(r"[0-9a-f]{16}", txt)], [[], []])'''),
    ('chk("a fala do operador de 06/11 (a ordem da v411: a forma da matriz finita e\' o signo; tudo entra no um.py) existe e traz a frase", ord_ok and FRASE_DA_ORDEM in ord_txt, [ord_ok, ord16])',
     'chk("a fala do operador de 12/11 (a ordem da v411: a ordem de abrir, D169) existe, e\' a do pino do delta e traz a fala inteira", ord_ok and FRASE_DA_ORDEM == ord_txt.strip() and ord16 == _DLM.FALA_ORDEM_V411["sha256"][:16], [ord_ok, ord16])'),
    ('''        try:
            aut_orq = ast.literal_eval(n_.value)
        except ValueError:   # (v411) o AUT e' MONTADO do delta (sha16 e frase lidos de delta_v411): avalia-se SO' a expressao do AUT, com o delta desta pasta e a frase dele, sem builtins
            import importlib.util as _ilu9
            _sp9 = _ilu9.spec_from_file_location("delta_v411_conferir_servico", os.path.join(V, "delta_v411.py")); _dl9 = _ilu9.module_from_spec(_sp9); _sp9.loader.exec_module(_dl9)
            aut_orq = eval(compile(ast.Expression(n_.value), "AUT_do_orquestrador", "eval"), {"__builtins__": {}}, {"_DL": _dl9, "AUT_FRASE": _dl9.FRASE_ORDEM_V411})''',
     '''        try:
            aut_orq = ast.literal_eval(n_.value)
        except ValueError:   # (v411) o AUT e' MONTADO (do delta e da fala): avalia-se SO' a expressao do AUT, com o delta desta pasta e a fala lida do arquivo, sem builtins; nome que falte no delta e' FALHA visivel (aut_orq None), nunca ok
            try:
                aut_orq = eval(compile(ast.Expression(n_.value), "AUT_do_orquestrador", "eval"), {"__builtins__": {}}, {"_DL": _DLM, "AUT_FRASE": FRASE_DA_ORDEM})
            except Exception as e_aut:   # noqa: BLE001
                aut_orq = None; AUT_ERRO = repr(e_aut)[:300]'''),
    ('''chk("o AUT do orquestrador (pos_treino_v411.py) e' a ordem de 06/11 (a ordem da v411): traz o sha16 do arquivo da fala (calculado aqui), a frase e a data, e nenhum texto de 01/11 nem de 05/11", bool(aut_orq) and ord16 is not None and ord16 in aut_orq and FRASE_DA_ORDEM in aut_orq and "06/11/2026" in aut_orq and "05/11/2026" not in aut_orq and "01/11/2026" not in aut_orq, [ord16, bool(aut_orq)])''',
     '''chk("o AUT do orquestrador (pos_treino_v411.py) e' a ordem de 12/11 (a ordem da v411): traz o sha16 do arquivo da fala (calculado aqui), a fala inteira e a data, e nenhuma data de ordem anterior (01/11 a 11/11)", bool(aut_orq) and ord16 is not None and ord16 in aut_orq and FRASE_DA_ORDEM in aut_orq and ORDEM_DATA in aut_orq and not any(d_ in aut_orq for d_ in DATAS_ANTERIORES), [ord16, bool(aut_orq), AUT_ERRO])'''),
    ('aut_orq = None\nfor n_ in ast.parse(', 'aut_orq = None; AUT_ERRO = None\nfor n_ in ast.parse('),
    ('dest = os.path.join(HERE, "CONFERENCIA_EXIGENCIAS_SERVICO_v411.json")', 'os.makedirs(OUT_DIR, exist_ok=True)\ndest = os.path.join(OUT_DIR, "CONFERENCIA_EXIGENCIAS_SERVICO_v411.json")'),
    ('"escopo": "NOT_FALSIFIED nao e creditacao; o gate nao se move"}', '"escopo": "NOT_FALSIFIED nao e creditacao; o gate nao se move", **_DLM.MARCA_ENSAIO}'),
], "a ORDEM da v411 (fala de 12/11/2026, D169) com o nome LIDO do delta_v411 (FALA_ORDEM_V411, pinada pelo DESENHO) e a fala inteira e a data lidas do arquivo; as datas anteriores (01 a 11/11) nao podem sobrar; o AUT do orquestrador avaliado com o delta e, se citar nome que o delta nao tem, FALHA visivel; no ensaio do topo proposto a saida vai a pasta de ensaio")

# ---- o controle negativo
M = "bancada_B3_servico/controle_negativo/mutar_conferidor_v411.py"
L.aplicar(M, [
    (_nhM, "# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida de versao a versao) molde v410/bancada_B3_servico/controle_negativo/mutar_conferidor_v410.py (rotulos subidos por _bump_copia_v411.py; diff em bump/). "
           "Adaptado (v411, 12/11/2026, fork B): M4 e M6 falam da ORDEM da v411 (fala de 12/11); M5 volta a data da autorizacao anterior (06/11/2026, a da v410) como texto; o sandbox curto C:\\t\\vb22 que esta corrida cria"),
    ("  M4  recibo_parada_v411.py      : sai a conferencia da ordem de 06/11 (a ordem da v411: o assert com a frase e o ORDEM_SHA16): qualquer texto de autorizacao passaria;",
     "  M4  recibo_parada_v411.py      : sai a conferencia da ordem de 12/11 (a ordem da v411: o assert com a fala e o ORDEM_SHA16): qualquer texto de autorizacao passaria;"),
    ("  M5  recibo_religamento_v411.py : volta a data da ordem anterior (05/11/2026, a da v410) como texto no script (autorizacao anterior sobrando).",
     "  M5  recibo_religamento_v411.py : volta a data da ordem anterior (06/11/2026, a da v410) como texto no script (autorizacao anterior sobrando)."),
    ("  M6  recibo_parada_v411.py      : o caminho do arquivo da fala de 06/11 vira um nome que NAO existe",
     "  M6  recibo_parada_v411.py      : o caminho do arquivo da fala de 12/11 vira um nome que NAO existe"),
    ("Grava RESULTADO_CONTROLE_NEGATIVO_v411.json ao lado (nao sobrescreve)", "Grava RESULTADO_CONTROLE_NEGATIVO_v411.json ao lado (no modo de ensaio do topo proposto, em <pasta de ensaio>\\\\bancada_B3_servico\\\\controle_negativo, fora de work; nao sobrescreve)"),
    ("def m4(t):   # sai a conferencia da ordem de 06/11 (a ordem da v411)", "def m4(t):   # sai a conferencia da ordem de 12/11 (a ordem da v411)"),
    ('    return t.replace(a, a + " (autorizacao de 05/11/2026)", 1)', '    return t.replace(a, a + " (autorizacao de 06/11/2026)", 1)'),
    ('''    a = '"cunhagens_13out", "''' + N_ANT + '''")'   # (so' o caminho que o script ABRE; o nome aparece tambem na nota da marca)
    assert t.count(a) == 1
    return t.replace(a, a.replace("OPERADOR_06nov_", "OPERADOR_06nov_v411_"), 1)''',
     '''    a = '"cunhagens_13out", "''' + N_ORDEM + '''")'   # (so' o caminho que o script ABRE)
    assert t.count(a) == 1
    return t.replace(a, a.replace("OPERADOR_12nov_", "OPERADOR_12nov_v411_"), 1)'''),
    ('''            ("M4_sem_a_conferencia_da_ordem_de_06nov", "recibo_parada_v411.py", m4, "recibo_parada_v411.py: a ordem de 06/11 (a ordem da v411) e' conferida"),
            ("M5_data_da_ordem_de_05nov_no_script",''',
     '''            ("M4_sem_a_conferencia_da_ordem_de_12nov", "recibo_parada_v411.py", m4, "recibo_parada_v411.py: a ordem de 12/11 (a ordem da v411) e' conferida"),
            ("M5_data_da_ordem_de_06nov_no_script",'''),
    ('''    r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(tmp, "conferir_mut.py")], capture_output=True, text=True, encoding="utf-8")''',
     '''    env_ = {k_: v_ for k_, v_ in os.environ.items() if k_ != "V411_ENSAIO_TOPO_PROPOSTO"}   # (v411) a copia do conferidor grava na pasta temporaria, nunca na de ensaio
    r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(tmp, "conferir_mut.py")], capture_output=True, text=True, encoding="utf-8", env=env_)'''),
    ('dest = os.path.join(HERE, "RESULTADO_CONTROLE_NEGATIVO_v411.json")',
     'import importlib.util as _ilu\n_sp_dl = _ilu.spec_from_file_location("delta_v411_mutar", os.path.join(V, "delta_v411.py")); _DLM = _ilu.module_from_spec(_sp_dl); _sp_dl.loader.exec_module(_DLM)\n'
     'OUT_DIR = os.path.join(_DLM.SAIDA, "bancada_B3_servico", "controle_negativo") if _DLM.ENSAIO_TOPO_PROPOSTO else HERE   # (v411) no ensaio do topo proposto, a saida vai a pasta de ensaio\n'
     'os.makedirs(OUT_DIR, exist_ok=True); res.update(_DLM.MARCA_ENSAIO)\ndest = os.path.join(OUT_DIR, "RESULTADO_CONTROLE_NEGATIVO_v411.json")'),
], "a ORDEM da v411 (12/11/2026): M4, M5 (a data da ordem da v410, 06/11/2026, de volta no script) e M6 (o nome da fala de 12/11 com um rotulo enfiado) e as condicoes esperadas com o texto novo do conferidor; a copia do conferidor roda sem a variavel do ensaio (grava so' na pasta temporaria); no ensaio do topo proposto o resultado vai a pasta de ensaio")
