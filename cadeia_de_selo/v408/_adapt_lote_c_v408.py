# -*- coding: utf-8 -*-
"""_adapt_lote_c_v408.py -- adapta a v408 (04/11/2026, claude-construtor-v408 [fork C], a servico da gerencia c1) os arquivos do lote C que a subida mecanica de rotulo (v407->v408) deixou com a marca `# [A ADAPTAR v408]`
e com NOTAS FALSAS «[ADAPTADO v408, 03/11/2026]» (eram as notas da v407, subidas de rotulo): bancada_B3_servico/* (5), bateria_pre_selo/* (7), copiar_logs_do_kernel_v408.py, pino_memoria_py_v408.py, purga_v408.py,
refazer_arvore_v408_pos_selo.py, refazer_sandbox_v408_pos_selo.sh, regras_v408.py e fechar_preparacao_v408.py.
O que muda de CONTEUDO: a autorizacao da parada/religamento da Bancada passa a ser a ORDEM da v408 (fala do operador de 04/11/2026, arquivo OPERADOR_04nov_ordem_v408_..., sha16 LIDO do arquivo pelos scripts; a frase conferida no arquivo e no texto
passado pelo orquestrador); o conferidor estatico e o controle negativo acompanham (M4/M5/M6); o controle negativo do recibo pre-selo usa o selo da versao ANTES da anterior, a v406 (v407\\base_v406); os textos dizem 4 modulos; datas 04/11/2026;
o fechar_preparacao diz a v408 (Tetelestai e' o terminal), D54 e o agente desta preparacao. Nada e' executado aqui. Trocas de contagem EXATA; backup de bytes; CRLF preservado; a marca e as notas falsas saem. Escrito pela ferramenta Write."""
import ast, datetime, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
ORDEM_NOME = "OPERADOR_04nov_ordem_v408_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt"
ORDEM_VELHA = "OPERADOR_02nov_quando_terminar_compile_v407_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt"
FRASE_V408 = "liste as pedras que eu preciso nominar e em seguida produza a v408, rode e quando estiver completa, dê a ordem de handoff para a sessão irmã realizar a custódia completa e atualizar tudo"
FRASE_VELHA = "compile a nova versão do um.py, rode, publique e atualize tudo por favor"
_ordem_p = os.path.join(os.path.dirname(os.path.dirname(HERE)), "cunhagens_13out", ORDEM_NOME)
assert os.path.isfile(_ordem_p) and FRASE_V408 in open(_ordem_p, encoding="utf-8").read(), "a fala da ordem da v408 nao esta em work\\cunhagens_13out ou nao traz a frase"
assert os.path.isdir(os.path.join(os.path.dirname(HERE), "v407", "base_v406")), "v407\\base_v406 (o selo da versao antes da anterior) nao existe"
MARCA_RX = re.compile(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n")
NOTA = "# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork C)] "


class Arq:
    def __init__(self, rel):
        self.p = os.path.join(HERE, *rel.split("/")); self.rel = rel
        self.raw = open(self.p, "rb").read()
        self.t = self.raw.decode("utf-8"); self.crlf = "\r\n" in self.t
        if self.crlf:
            self.t = self.t.replace("\r\n", "\n")
        self.done = MARCA_RX.search(self.t) is None   # ja adaptado numa corrida anterior desta mesma ferramenta (a marca saiu): nao se toca de novo
        if self.done:
            print("ja adaptado (sem a marca), pulo:", rel); return
        open(self.p + ".bak_" + TS + "_adapt", "wb").write(self.raw)

    def sub(self, old, new, n=1):
        if self.done:
            return
        assert self.t.count(old) == n, (self.rel, old[:100], self.t.count(old), n); self.t = self.t.replace(old, new)

    def linha(self, prefixo, nova):
        """troca a UNICA linha que comeca por `prefixo` pela linha `nova` (nova == None apaga a linha)"""
        if self.done:
            return
        rx = re.compile("(?m)^" + re.escape(prefixo) + "[^\n]*\n"); m = rx.findall(self.t); assert len(m) == 1, (self.rel, prefixo[:70], len(m))
        self.t = rx.sub(lambda m_: (nova + "\n") if nova is not None else "", self.t, count=1)

    def tira_marca(self):
        if self.done:
            return
        assert len(MARCA_RX.findall(self.t)) == 1, (self.rel, "marca"); self.t = MARCA_RX.sub("", self.t, count=1)

    def grava(self):
        if self.done:
            return
        # a marca so' conta no inicio de linha: rodar_bn_pre_selo_v408.sh a procura de proposito, num grep entre aspas
        assert MARCA_RX.search(self.t) is None and "[ADAPTADO v408, 03/11/2026" not in self.t and "claude-prep-v408" not in self.t, (self.rel, "sobrou marca, nota falsa ou agente velho")
        t = self.t.replace("\n", "\r\n") if self.crlf else self.t
        if self.rel.endswith(".py"):
            ast.parse(t)
        open(self.p, "wb").write(t.encode("utf-8"))
        if self.rel.endswith(".sh"):
            r = subprocess.run(["sh", "-n", self.p], capture_output=True, text=True); assert r.returncode == 0, (self.rel, r.stderr[:300])
        print("ok", self.rel, len(self.raw), "->", len(t.encode("utf-8")))


def ordem(a, docstring_velha, docstring_nova):
    """as trocas comuns da autorizacao nos recibos da Bancada: a ORDEM da v408 (arquivo, frase, data)"""
    a.sub(docstring_velha, docstring_nova)
    a.sub("# a autorizacao tem de ser a de 02/11/2026 (nao a de 01/11 da v405): o sha16 da fala vem do ARQUIVO lido agora (nunca digitado) e a frase tem de estar no arquivo e no texto passado pelo orquestrador",
          "# a autorizacao tem de ser a ORDEM da v408, de 04/11/2026 (nao a de 03/11 da v407 nem a de 02/11 da v406): o sha16 da fala vem do ARQUIVO lido agora (nunca digitado) e a frase tem de estar no arquivo e no texto passado pelo orquestrador")
    a.sub('"%s")' % ORDEM_VELHA, '"%s")' % ORDEM_NOME)
    a.sub('FRASE_DA_ORDEM = "%s"' % FRASE_VELHA, 'FRASE_DA_ORDEM = "%s"' % FRASE_V408)
    a.sub('and "02/11/2026" in AUT, "a autorizacao passada nao e\' a ordem do operador de 02/11/2026 (sha16 da fala lido do arquivo e a frase «%s» no texto)" % FRASE_DA_ORDEM',
          'and "04/11/2026" in AUT, "a autorizacao passada nao e\' a ordem do operador de 04/11/2026 (a ordem da v408: sha16 da fala lido do arquivo e a frase «%s» no texto)" % FRASE_DA_ORDEM')


# ======================================================================= bancada_B3_servico
a = Arq("bancada_B3_servico/evento_c1_b3_v408.py"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bancada_B3_servico/evento_c1_b3_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/); conferido em 04/11/2026: versao v408, ESPERADOS_v408.json (candidato_sha16 LIDO, conferido contra o um.py do Nos antes de anotar), unidade F0.6, B17 sobre a producao que pina B16-v407-20261104-R1 (delta_v408.BANCADA_PINA_HOJE); nada de bundle, de contagem de modulos nem de hash digitado")
a.grava()
a = Arq("bancada_B3_servico/recibo_parada_v408.py"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bancada_B3_servico/recibo_parada_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/). Adaptado: a autorizacao e' a ORDEM da v408 (fala do operador de 04/11/2026, OPERADOR_04nov_ordem_v408_..., sha16 LIDO do arquivo; a frase conferida no arquivo e no texto passado pelo orquestrador);")
a.linha("# (2) o insumo RELIGAMENTO_PREVIO_02nov.json era da v407", "# o ultimo religamento conhecido segue sendo o do B(n) da v407 (RECIBO_RELIGAMENTO_v407.json: PID, no_ar_desde), e o recibo diz se o PID lido da porta e' o mesmo; as chaves do recibo sao as do recibo REAL da v407; nada de bundle nem de hash digitado.")
ordem(a, "A autorizacao e' a ordem do operador de 02/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado pelo orquestrador).\nO ultimo religamento conhecido",
      "A autorizacao e' a ORDEM da v408, do operador, de 04/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado pelo orquestrador).\nO ultimo religamento conhecido")
a.grava()
a = Arq("bancada_B3_servico/recibo_religamento_v408.py"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bancada_B3_servico/recibo_religamento_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/). Adaptado: a autorizacao e' a ORDEM da v408 (fala do operador de 04/11/2026, OPERADOR_04nov_ordem_v408_..., sha16 LIDO do arquivo; a frase conferida no arquivo e no texto passado pelo orquestrador).")
a.linha("# O resto (geracao B<n> lida do recibo do B(n)", "# O resto (geracao B<n> lida do recibo do B(n), deployment B<n>-v408-<data>-R1, versao servida v408, manifesto e um.py conferidos) e' generico e nao tem bundle, contagem de modulos nem hash digitado.")
ordem(a, 'A autorizacao e\' a ordem do operador de 02/11/2026 (a fala e\' lida do arquivo e conferida contra o texto passado pelo orquestrador)."""',
      'A autorizacao e\' a ORDEM da v408, do operador, de 04/11/2026 (a fala e\' lida do arquivo e conferida contra o texto passado pelo orquestrador)."""')
a.grava()
a = Arq("bancada_B3_servico/conferir_exigencias_servico_v408.py"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bancada_B3_servico/conferir_exigencias_servico_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/). Adaptado: a autorizacao conferida e' a ORDEM da v408 (fala de 04/11/2026; sha16 calculado do arquivo aqui e nos scripts); nenhuma data de autorizacao anterior (01/11, 02/11, 03/11) pode sobrar nos scripts;")
a.linha("# RELIGAMENTO_PREVIO_02nov.json (era da v407)", "# o insumo da parada segue sendo o RECIBO_RELIGAMENTO_v407.json (pid e no_ar_desde); o evento aborta no assert do candidato enquanto o Nos for a v407.")
a.sub("  (e) a autorizacao e' a ordem do operador de 02/11/2026 (o arquivo da fala tem v407 no nome: a ordem foi dada na v407 e vale para «a nova versao»): depois do assert AUT, parada e religamento conferem o texto passado contra a fala (o sha16 vem do ARQUIVO da fala, lido na hora; a frase tem de estar no arquivo e no texto); nenhum texto, data ou hash de autorizacao da v405 (01/11) sobrou nos scripts;",
      "  (e) a autorizacao e' a ORDEM da v408, do operador, de 04/11/2026 («%s»): depois do assert AUT, parada e religamento conferem o texto passado contra a fala (o sha16 vem do ARQUIVO da fala, lido na hora; a frase tem de estar no arquivo e no texto); nenhum texto, data ou hash de autorizacao anterior (01/11, 02/11, 03/11) sobrou nos scripts;" % FRASE_V408)
a.sub('ORDEM_ARQ = os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", "%s")' % ORDEM_VELHA, 'ORDEM_ARQ = os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", "%s")' % ORDEM_NOME)
a.sub('FRASE_DA_ORDEM = "%s"' % FRASE_VELHA, 'FRASE_DA_ORDEM = "%s"' % FRASE_V408)
a.sub('chk(nome + ": a ordem de 02/11 e\' conferida: o assert com ORDEM_SHA16 (lido do ARQUIVO da fala) vem DEPOIS do assert AUT", i_ordem is not None and i_assert is not None and i_ordem > i_assert and "cunhagens_13out" in txt and "OPERADOR_02nov_quando_terminar_compile_v406" in txt and "hashlib.sha256(ORDEM_BYTES)" in txt, [i_assert, i_ordem])',
      'chk(nome + ": a ordem de 04/11 (a ordem da v408) e\' conferida: o assert com ORDEM_SHA16 (lido do ARQUIVO da fala) vem DEPOIS do assert AUT", i_ordem is not None and i_assert is not None and i_ordem > i_assert and "cunhagens_13out" in txt and "OPERADOR_04nov_ordem_v408_liste_as_pedras" in txt and "hashlib.sha256(ORDEM_BYTES)" in txt, [i_assert, i_ordem])')
a.sub('chk(nome + ": nenhum texto, data ou hash de autorizacao da v405 sobrou (01/11/2026, nenhum sha de 16 hex digitado)", "01/11/2026" not in txt and re.search(r"[0-9a-f]{16}", txt) is None, ["01/11/2026" in txt, re.findall(r"[0-9a-f]{16}", txt)], [False, []])',
      'chk(nome + ": nenhum texto, data ou hash de autorizacao anterior sobrou (01/11/2026, 02/11/2026, 03/11/2026; nenhum sha de 16 hex digitado)", "01/11/2026" not in txt and "02/11/2026" not in txt and "03/11/2026" not in txt and re.search(r"[0-9a-f]{16}", txt) is None, ["01/11/2026" in txt, "02/11/2026" in txt, "03/11/2026" in txt, re.findall(r"[0-9a-f]{16}", txt)], [False, False, False, []])')
a.sub("# ---- a ordem do operador de 02/11 e o AUT do orquestrador", "# ---- a ordem do operador de 04/11 (a ordem da v408) e o AUT do orquestrador")
a.sub('chk("a fala do operador de 02/11 (compile, rode, publique) existe e traz a frase", ord_ok and FRASE_DA_ORDEM in ord_txt, [ord_ok, ord16])', 'chk("a fala do operador de 04/11 (a ordem da v408: liste as pedras, produza, rode, handoff para a custodia completa, atualize tudo) existe e traz a frase", ord_ok and FRASE_DA_ORDEM in ord_txt, [ord_ok, ord16])')
a.sub('chk("o AUT do orquestrador (pos_treino_v408.py) e\' a ordem de 02/11: traz o sha16 do arquivo da fala (calculado aqui), a frase e a data, e nenhum texto de 01/11", bool(aut_orq) and ord16 is not None and ord16 in aut_orq and FRASE_DA_ORDEM in aut_orq and "02/11/2026" in aut_orq and "01/11/2026" not in aut_orq, [ord16, bool(aut_orq)])',
      'chk("o AUT do orquestrador (pos_treino_v408.py) e\' a ordem de 04/11 (a ordem da v408): traz o sha16 do arquivo da fala (calculado aqui), a frase e a data, e nenhum texto de 01/11", bool(aut_orq) and ord16 is not None and ord16 in aut_orq and FRASE_DA_ORDEM in aut_orq and "04/11/2026" in aut_orq and "01/11/2026" not in aut_orq, [ord16, bool(aut_orq)])')
a.grava()
a = Arq("bancada_B3_servico/controle_negativo/mutar_conferidor_v408.py"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bancada_B3_servico/controle_negativo/mutar_conferidor_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/). Adaptado: M4 e M6 falam da ORDEM da v408 (fala de 04/11); M5 volta uma data de autorizacao anterior (01/11/2026) como texto; o sandbox curto C:\\t\\vb21 que esta corrida cria")
a.sub("Adaptado em 02/11/2026 da v407: cada mutacao agora roda SOZINHA", "Adaptado em 04/11/2026 da v407 (que o herdou da v406): cada mutacao roda SOZINHA")
a.sub("  M4  recibo_parada_v408.py      : sai a conferencia da ordem de 02/11 (o assert com a frase e o ORDEM_SHA16): qualquer texto de autorizacao passaria;", "  M4  recibo_parada_v408.py      : sai a conferencia da ordem de 04/11 (a ordem da v408: o assert com a frase e o ORDEM_SHA16): qualquer texto de autorizacao passaria;")
a.sub("  M5  recibo_religamento_v408.py : volta a data da ordem anterior (01/11/2026) como texto no script (autorizacao da v405 sobrando).", "  M5  recibo_religamento_v408.py : volta uma data de ordem anterior (01/11/2026) como texto no script (autorizacao anterior sobrando).")
a.sub("  M6  recibo_parada_v408.py      : o caminho do arquivo da fala de 02/11 volta a ser um nome que NAO existe (o defeito que a subida mecanica de rotulo introduziu: compile_v408 em vez de compile_v406).", "  M6  recibo_parada_v408.py      : o caminho do arquivo da fala de 04/11 vira um nome que NAO existe (ordem_v409 no lugar de ordem_v408: o tipo de defeito que uma subida mecanica de rotulo introduz).")
a.sub("def m4(t):   # sai a conferencia da ordem de 02/11", "def m4(t):   # sai a conferencia da ordem de 04/11 (a ordem da v408)")
a.sub("def m6(t):   # o nome do arquivo da fala volta a ser o inexistente (com v408), como a subida mecanica de rotulo o deixou\n    a = \"OPERADOR_02nov_quando_terminar_compile_v406_rode\"\n    assert t.count(a) == 1\n    return t.replace(a, \"OPERADOR_02nov_quando_terminar_compile_v408_rode\", 1)",
      "def m6(t):   # o nome do arquivo da fala vira um inexistente (ordem_v409), o tipo de defeito que uma subida mecanica de rotulo introduz\n    a = \"OPERADOR_04nov_ordem_v408_liste_as_pedras_produza_rode\"\n    assert t.count(a) == 1\n    return t.replace(a, \"OPERADOR_04nov_ordem_v409_liste_as_pedras_produza_rode\", 1)")
a.sub('("M4_sem_a_conferencia_da_ordem_de_02nov", "recibo_parada_v408.py", m4, "recibo_parada_v408.py: a ordem de 02/11 e\' conferida")', '("M4_sem_a_conferencia_da_ordem_de_04nov", "recibo_parada_v408.py", m4, "recibo_parada_v408.py: a ordem de 04/11 (a ordem da v408) e\' conferida")')
a.sub('("M5_data_da_ordem_de_01nov_no_script", "recibo_religamento_v408.py", m5, "recibo_religamento_v408.py: nenhum texto, data ou hash de autorizacao da v405")', '("M5_data_da_ordem_de_01nov_no_script", "recibo_religamento_v408.py", m5, "recibo_religamento_v408.py: nenhum texto, data ou hash de autorizacao anterior")')
a.grava()
# ======================================================================= bateria_pre_selo
a = Arq("bateria_pre_selo/conferir_recibo_pre_selo_v408.py"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bateria_pre_selo/conferir_recibo_pre_selo_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/). Adaptado: o controle negativo «selo anterior errado» usa o selo da versao ANTES da anterior: na v408 e' a v406, guardada em v407\\base_v406")
a.linha("# (que em v407\\ NAO existe: o que a v407 guarda e' base_v405)", "# (a subida mecanica deixara `base_v405`, que a v407 nao guarda mais com esse papel); o controle chama-se selo_anterior_e_o_da_v406_nao_o_pinado. O resto nao depende de bundle nem de contagem de modulos (tudo e' LIDO do recibo, dos pinos e da producao).")
a.sub('SELO_V405 = os.path.join(V14, "base_v405", "um_absoluto_selo.json")      # o selo da versao ANTES da anterior (a v405, guardada em v407\\base_v405): o controle negativo "selo anterior errado"\nKM_V405 = os.path.join(V14, "base_v405", "tgl_kernel_proof_manifest.json")\nassert os.path.isfile(SELO_V405) and os.path.isfile(KM_V405), "a base v405 (o selo da versao antes da anterior) nao esta em v407\\\\base_v405"',
      'SELO_V406 = os.path.join(V14, "base_v406", "um_absoluto_selo.json")      # o selo da versao ANTES da anterior (a v406, guardada em v407\\base_v406): o controle negativo "selo anterior errado"\nKM_V406 = os.path.join(V14, "base_v406", "tgl_kernel_proof_manifest.json")\nassert os.path.isfile(SELO_V406) and os.path.isfile(KM_V406), "a base v406 (o selo da versao antes da anterior) nao esta em v407\\\\base_v406"')
a.sub('ok, rec_t, _ = conferir(RP, RSHA, SELO_V405, KM_V405)\ncontrole("selo_anterior_e_o_da_v405_nao_o_pinado", "SELO_ANTERIOR_NAO_E_O_PINADO", ok, rec_t)', 'ok, rec_t, _ = conferir(RP, RSHA, SELO_V406, KM_V406)\ncontrole("selo_anterior_e_o_da_v406_nao_o_pinado", "SELO_ANTERIOR_NAO_E_O_PINADO", ok, rec_t)')
assert "V405" not in a.t
a.grava()
a = Arq("bateria_pre_selo/derivar_pre_selo_v408.py"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "ESTE DERIVADOR NAO SE APLICA A v408 e RECUSA (fail-closed) de proposito; conferido em 04/11/2026: os cinco scripts de servico da v408 ja existem e foram adaptados a mao; ver abaixo.")
a.sub("(405 -> 407, 407 -> 408, B14 -> B16, B16 -> B17; diffs em bump/) e foram ADAPTADOS A MAO (marca `# [ADAPTADO v408, 03/11/2026]` na 2a linha de cada um). Rodar o derivador da v407 so' trocando os rotulos nao reproduz isso, e MEDIDO:",
      "(o mapa de versoes e de geracoes B(n) de _bump_copia_v408.py; diffs em bump/) e foram ADAPTADOS A MAO em 04/11/2026 (nota `# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork C)]` na 2a linha de cada um). Rodar o derivador da v407 so' trocando os rotulos nao reproduz isso, e MEDIDO na v407:")
a.sub("o mapa deixaria `base_v404` onde a v408 precisa de `base_v405`\n(o controle negativo \"selo anterior errado\" usa o selo da versao ANTES da anterior: para a v408, a v405, guardada em v407\\\\base_v405).",
      "um mapa herdado deixaria `base_v405` onde a v408 precisa de `base_v406`\n(o controle negativo \"selo anterior errado\" usa o selo da versao ANTES da anterior: para a v408, a v406, guardada em v407\\\\base_v406).")
a.grava()
a = Arq("bateria_pre_selo/gerar_pino_recibo_pre_selo_v408.py"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bateria_pre_selo/gerar_pino_recibo_pre_selo_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/); conferido em 04/11/2026: a lista `esta_tarefa_escreveu_so_em` diz o que o rodar_bn_pre_selo_v408.sh escreve de fato;")
a.grava()
a = Arq("bateria_pre_selo/limpar_sandbox_vb21.py"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bateria_pre_selo/limpar_sandbox_vb21.py (rotulos subidos por _bump_copia_v408.py; diff em bump/); conferido em 04/11/2026: o corpo nao depende de modulos nem de versao: apaga so' C:\\t\\vb21, depois de provar que nao ha juncao nem link")
a.grava()
a = Arq("bateria_pre_selo/rodar_bn_pre_selo_v408.sh"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bateria_pre_selo/rodar_bn_pre_selo_v407.sh (rotulos subidos por _bump_copia_v408.py; diff em bump/); conferido em 04/11/2026: (1) os cinco scripts da v408 JA existem (nasceram da subida mecanica e foram adaptados a mao); o derivador da v407 nao se aplica")
a.grava()
a = Arq("bateria_pre_selo/rodar_ensaio_1_pre_selo_v408.sh"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bateria_pre_selo/rodar_ensaio_1_pre_selo_v407.sh (rotulos subidos por _bump_copia_v408.py; diff em bump/); conferido linha a linha em 04/11/2026: o passo e' simples v407 -> v408, o esboco e a bateria sao os pinados na v407 (path e sha256 lidos dos pinos), nada de bundle nem de contagem de modulos aqui")
a.grava()
a = Arq("bateria_pre_selo/snap_producao_v408.py"); a.tira_marca()
a.linha("# [ADAPTADO v408, 03/11/2026]", NOTA + "molde v407/bateria_pre_selo/snap_producao_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/); conferido em 04/11/2026: o corpo nao tem nada especifico de modulos nem de versao: so' le a Bancada de producao e o Nos e fotografa")
a.grava()
# ======================================================================= raiz
a = Arq("copiar_logs_do_kernel_v408.py"); a.tira_marca()
a.sub("(adaptado em 02/11/2026; na v407 ele copiava e gravava o LOGS_COPIADOS; agora nao grava nada)", "(adaptado em 04/11/2026 a v408; desde a v407 ele nao grava nada: so' compara)")
a.sub("`lake build` a frio dos 301 modulos novos do bundle", "`lake build` a frio dos 4 modulos novos do bundle (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP)")
a.grava()
a = Arq("pino_memoria_py_v408.py"); a.tira_marca()
a.sub("(adaptado em 03/11/2026: o corpo nao depende do bundle; conferido por leitura que o memoria.py de hoje tem o sha16 declarado, o mesmo da v407)", "(adaptado em 04/11/2026: o corpo nao depende do bundle; conferido por leitura, em 04/11/2026, que o memoria.py de hoje tem o sha16 declarado, o mesmo da v407; NAO executado na preparacao: e' ato da gerencia)")
a.grava()
a = Arq("purga_v408.py"); a.tira_marca()
a.sub("por isso a validacao de preparacao (03/11/2026) foi so' de sintaxe (ast.parse) e dos padroes/raizes lidos do proprio arquivo, sem varrer.", "por isso a validacao de preparacao (04/11/2026) foi so' de sintaxe (ast.parse) e dos padroes/raizes lidos do proprio arquivo, sem varrer (a varredura corre por fora, como diz o fim_de_cadeia_v408.sh).")
a.grava()
a = Arq("refazer_arvore_v408_pos_selo.py"); a.tira_marca()
a.sub("os 9 modulos novos em TGLExt/ (R[\"pedras\"]: path e sha256, um por um, na arvore refeita E no Nos)", "os 4 modulos novos em TGLExt/ (R[\"pedras\"]: path e sha256, um por um, na arvore refeita E no Nos)")
a.sub("foi feita so' por leitura em 03/11/2026.", "foi feita so' por leitura em 04/11/2026 (pos_build_kernel_v408.py e p00).")
a.sub("adaptado a v408 em 03/11/2026. Molde direto: refazer_arvore_v407_pos_selo.py.", "adaptado a v408 em 04/11/2026 (claude-construtor-v408). Molde direto: refazer_arvore_v407_pos_selo.py.")
a.grava()
a = Arq("refazer_sandbox_v408_pos_selo.sh"); a.tira_marca()
a.sub("(raiz, Audit, os 9 modulos novos em TGLExt/ e as contagens de .lean)", "(raiz, Audit, os 4 modulos novos em TGLExt/ e as contagens de .lean)")
a.grava()
a = Arq("regras_v408.py"); a.tira_marca()
a.sub("# regras_v408.py -- ESCRITO em 03/11/2026 pela preparacao da cadeia v408 (claude-prep-v408) e NAO EXECUTADO", "# regras_v408.py -- ESCRITO em 04/11/2026 pela preparacao da cadeia v408 (claude-construtor-v408) e NAO EXECUTADO")
a.grava()
# ======================================================================= fechar_preparacao
a = Arq("fechar_preparacao_v408.py"); a.tira_marca()
a.sub("(o rota_id e' LIDO de registro_mapa_prep_v408_ABERTA.json: kernel.v408_preparacao_03nov)", "(o rota_id e' LIDO de registro_mapa_prep_v408_ABERTA.json, que a gerencia abre)")
a.sub("Molde: fechar_preparacao_v407.py, adaptado em 03/11/2026 a v408 (o psion, o canto e o par: bundle de 9 modulos em TGLExt/, registro psion_canto_v407, a chave linked_to_the_corner_by_a_lemma lida do kernel).",
      "Molde: fechar_preparacao_v407.py, adaptado em 04/11/2026 a v408 (Tetelestai e' o terminal: bundle de 4 modulos em TGLExt/, registro tetelestai_terminal_v408; nenhuma chave antiga muda).")
a.sub('"titulo": "v408 preparada (o psion, o canto e o par, 03/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,', '"titulo": "v408 preparada (Tetelestai e\' o terminal, 04/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,')
a.sub('"proximo_passo": "revisao de terceiro (o Sonnet, D37 herdada); depois o orquestrador instala, roda o rito e a cadeia; a rota da versao selada sera a da v408",', '"proximo_passo": "revisao de terceiro (o Sonnet, D54: ate\' tres rodadas; quem constroi nao aprova); depois o orquestrador instala, roda o rito e a cadeia; a rota da versao selada sera a da v408",')
a.sub('"--quem", "claude-prep-v408"], capture_output=True, text=True, encoding="utf-8")\nprint("mapa:"', '"--quem", "claude-construtor-v408"], capture_output=True, text=True, encoding="utf-8")\nprint("mapa:"')
a.sub('txt = ("v408 (o psion, o canto e o par) preparada em 03/11/2026 por claude-prep-v408 para a gerencia c1 (nada instalado; o rito nao rodou). " + res + ".\\n\\n"', 'txt = ("v408 (Tetelestai e\' o terminal) preparada em 04/11/2026 por claude-construtor-v408 para a gerencia c1 (nada instalado; o rito nao rodou). " + res + ".\\n\\n"')
_m0 = a.t.index('       "A moldura vale em todo texto: o psion e o canto sao a mesma construcao nas duas faces'); _m1 = a.t.index('       "Avisos para a gerencia:\\n"')
a.t = a.t[:_m0] + ('       "A moldura vale em todo texto: o terminal e\' a leitura, nao o fim do decaimento; nao ha\' relacao sem peso (o 1 sozinho e\' excluido por teorema); o tempo e\' a moeda de beta; o zero inscrito e\' o Um e o Um nao e\' o zero absoluto; «P = nP» so\' no sentido do operador; validade no kernel nao e\' creditacao e o gate nao se move. "\n'
                   '       "As ressalvas vao ditas: o par na face de Fock segue [OPEN] como ligacao (E21); a palavra impedancia fica podada como termo (D50); a igualdade das classes P e NP segue podada (D51); o lock e o Hamiltoniano modular sao objetos distintos; o insumo do acervo entra pela copia purgada (E23); nenhum teste com a natureza entra; a regra do 4,44 vale em qualquer texto que o cite. Os nomes das quatro pedras sao do operador (04/11/2026).\\n\\n"\n') + a.t[_m1:]
a.sub('"--quem", "claude-prep-v408", "--tipo", "project", "--estatuto", "REAL", "--alvo", "novo:v408-preparada-03nov", "--casa", "Central de Patentes", "--slug", "v408-preparada-03nov",', '"--quem", "claude-construtor-v408", "--tipo", "project", "--estatuto", "REAL", "--alvo", "novo:v408-preparada-04nov", "--casa", "Central de Patentes", "--slug", "v408-preparada-04nov",')
a.sub('"actor": {"id": "claude-prep-v408", "kind": "agent"}', '"actor": {"id": "claude-construtor-v408", "kind": "agent"}')
assert "03/11/2026" not in a.t and "psion" not in a.t
a.grava()
print("lote C adaptado")
