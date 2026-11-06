# -*- coding: utf-8 -*-
"""_adapt_forkB_v409.py -- (claude-construtor-v409, fork B, 05/11/2026) adapta a v409 os scripts da bateria pre-selo do B(n), do servico da Bancada (B3), as guardas estaticas,
o instalar/reverter/rito e o conferidor deles, o carimbador, o conferidor dos logs do kernel, a arvore/sandbox pos-selo, a purga, o pino da memoria, as regras, a guarda da ordem de chamada,
a simulacao da arvore do Nos e os encadeadores (regerar, refazer_candidato, fim_de_cadeia). Molde: os mesmos da v408 e os _adapt_*_v408.py de la'.
O que muda na v409: o registro com funcao NOVO e' traducao_turing_v409 (17 checagens; miolo _v409_formal + _v398_beta; mecanica v409_traducao_mechanics), o da v408 (tetelestai_terminal_v408) passa a HERDADO;
o bundle e' de UM modulo (TraducaoTuring); a ORDEM do operador e' a de 05/11/2026 (OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt; a frase e' verbatim e o sha16 e' LIDO do arquivo pelos scripts);
o controle «selo anterior errado» da bateria usa o selo da v407 (v408\\base_v407); as decisoes novas sao D55-D60 e as erratas E24-E26 (lidas do delta). Numeros e hashes sao LIDOS dos arquivos (delta_v409, POS_BUILD_v409.json, a fala).
Trocas de contagem EXATA (_adapt_util_v409.Arq: backup de bytes, CRLF preservado, a marca [A ADAPTAR v409] trocada pela [ADAPTADO v409 ...]). Escrito pela ferramenta Write."""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from _adapt_util_v409 import Arq as _ArqReal  # noqa: E402


class _Pula:
    """arquivo ja' adaptado (sem a marca): nada a fazer (o adaptador e' reexecutavel)."""
    def __init__(self, p):
        self.p = p; self.t = ""
    def troca(self, *a, **k):
        return self
    def marca(self, *a, **k):
        return self
    def grava(self):
        print("ja adaptado (pulado):", os.path.basename(self.p)); return False


def Arq(rel):
    p_ = os.path.join(HERE, *rel.replace("\\", "/").split("/"))
    if not re.search(r"(?m)^# \[A ADAPTAR v409\]", open(p_, encoding="utf-8").read()):
        return _Pula(p_)
    return _ArqReal(rel)
import delta_v409 as DL  # noqa: E402

VELHA = "[ADAPTADO v409, 04/11/2026, claude-construtor-v409 (fork C)]"
HERDADA = "(nota herdada da adaptacao da v408 [fork C, 04/11/2026], com os rotulos subidos; reconferida em 05/11/2026 pelo fork B do claude-construtor-v409)"
ORDEM_NOME = DL.N_ORDEM_V409
FRASE = DL.FRASE_ORDEM_V409
ORDEM_P = os.path.join(DL._CUN13, ORDEM_NOME)
assert FRASE in open(ORDEM_P, encoding="utf-8").read(), "a frase da ordem nao e' verbatim no arquivo da fala"
DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D8.DECISOES), key=lambda k_: int(k_[1:]))
ERR_NOVAS = [e_.split(" --")[0] for e_ in DL.ERRATAS_V409]
assert DEC_NOVAS == ["D55", "D56", "D57", "D58", "D59", "D60"] and ERR_NOVAS == ["E24", "E25", "E26"], (DEC_NOVAS, ERR_NOVAS)
PB = json.load(open(os.path.join(HERE, "kernel", "POS_BUILD_v409.json"), encoding="utf-8"))
T_BUILD, T_AUDIT, T_SOMA, T_MAX = PB["duracao_build_s"], PB["duracao_audit_s"], PB["build_modulos_s_soma"], PB["build_modulos_s_max"]
CARIMBO_V408 = hashlib.sha256(open(os.path.join(DL.V408, "carimbar_stdout_v408.py"), "rb").read()).hexdigest()[:16]
PEDRAS_V408 = [r_.split("/")[-1][:-len(".lean")] for r_ in json.load(open(os.path.join(DL.V408, "kernel_modulos_novos_v408.json"), encoding="utf-8"))["novos"]]
assert PEDRAS_V408 == ["TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP"], PEDRAS_V408
N_BUNDLE, N_ANC, N_FALAS = DL.N_BUNDLE, len(DL.ANCORAS), DL.N_FALAS_V409


def herdada(a):
    if isinstance(a, _Pula):
        return
    n = a.t.count(VELHA)
    if n:
        a.troca(VELHA, HERDADA, n)


def linha(a, prefixo, nova):
    if isinstance(a, _Pula):
        return
    ls = a.t.split("\n")
    idx = [i for i, l in enumerate(ls) if l.startswith(prefixo)]
    assert len(idx) == 1, ("linha nao unica", os.path.basename(a.p), prefixo[:80], len(idx))
    ls[idx[0]] = nova
    a.t = "\n".join(ls)


feitos = []

# ============================== bateria_pre_selo ==============================
a = Arq("bateria_pre_selo/conferir_recibo_pre_selo_v409.py")
a.troca("Adaptado: o controle negativo «selo anterior errado» usa o selo da versao ANTES da anterior: na v409 e' a v406, guardada em v408\\base_v406\n# (a subida mecanica deixara `base_v405`, que a v408 nao guarda mais com esse papel); o controle chama-se selo_anterior_e_o_da_v406_nao_o_pinado.",
        "Adaptado (v409): o controle negativo «selo anterior errado» usa o selo da versao ANTES da anterior: na v409 e' a v407, guardada em v408\\base_v407\n# (a subida mecanica deixara `base_v406`, que a v408 nao guarda); o controle chama-se selo_anterior_e_o_da_v407_nao_o_pinado.")
herdada(a)
a.troca('SELO_V406 = os.path.join(V14, "base_v406", "um_absoluto_selo.json")      # o selo da versao ANTES da anterior (a v406, guardada em v408\\base_v406): o controle negativo "selo anterior errado"',
        'SELO_V407 = os.path.join(V14, "base_v407", "um_absoluto_selo.json")      # o selo da versao ANTES da anterior (a v407, guardada em v408\\base_v407): o controle negativo "selo anterior errado"')
a.troca('KM_V406 = os.path.join(V14, "base_v406", "tgl_kernel_proof_manifest.json")', 'KM_V407 = os.path.join(V14, "base_v407", "tgl_kernel_proof_manifest.json")')
a.troca('assert os.path.isfile(SELO_V406) and os.path.isfile(KM_V406), "a base v406 (o selo da versao antes da anterior) nao esta em v408\\\\base_v406"',
        'assert os.path.isfile(SELO_V407) and os.path.isfile(KM_V407), "a base v407 (o selo da versao antes da anterior) nao esta em v408\\\\base_v407"')
a.troca("ok, rec_t, _ = conferir(RP, RSHA, SELO_V406, KM_V406)", "ok, rec_t, _ = conferir(RP, RSHA, SELO_V407, KM_V407)")
a.troca('controle("selo_anterior_e_o_da_v406_nao_o_pinado"', 'controle("selo_anterior_e_o_da_v407_nao_o_pinado"')
a.marca("controle «selo anterior errado» com a v407 (v408\\base_v407); o resto e' lido do recibo, dos pinos da v408 e da producao")
a.grava(); feitos.append(a.p)

a = Arq("bateria_pre_selo/derivar_pre_selo_v409.py")
herdada(a)
a.troca("um mapa herdado deixaria `base_v405` onde a v409 precisa de `base_v406`\n(o controle negativo \"selo anterior errado\" usa o selo da versao ANTES da anterior: para a v409, a v406, guardada em v408\\\\base_v406).",
        "um mapa herdado deixaria `base_v406` onde a v409 precisa de `base_v407`\n(o controle negativo \"selo anterior errado\" usa o selo da versao ANTES da anterior: para a v409, a v407, guardada em v408\\\\base_v407).")
a.marca("o derivador segue RECUSANDO de proposito (os cinco scripts da v409 nasceram da subida e foram adaptados); so' a base do controle mudou no texto")
a.grava(); feitos.append(a.p)

for rel, oque in (("bateria_pre_selo/gerar_pino_recibo_pre_selo_v409.py", "le tudo do recibo do ensaio, do stdout, dos pinos e das fotografias; nada de bundle; os nomes e rotulos v409/v408 conferidos"),
                  ("bateria_pre_selo/limpar_sandbox_vb21.py", "apaga so' C:\\t\\vb21 depois de provar que nao ha juncao nem link; nao depende de versao"),
                  ("bateria_pre_selo/snap_producao_v409.py", "so' le a Bancada de producao e o Nos e fotografa; nao depende de versao"),
                  ("bateria_pre_selo/rodar_ensaio_1_pre_selo_v409.sh", "o ensaio pre_selo contra o Nos v408 (canonico hoje), com o esboco e a bateria pinados na v408 (lidos dos pinos); --versao v408"),
                  ("bateria_pre_selo/rodar_bn_pre_selo_v409.sh", "a ordem dos passos da v408; passos 8 e 9 chamam diff_e_pinos_v409 e p00_precondicoes_v409")):
    a = Arq(rel); herdada(a)
    if rel.endswith("rodar_bn_pre_selo_v409.sh") and not isinstance(a, _Pula):   # a mensagem da guarda citava a marca literal (a guarda em si casa por regex no comeco da linha e fica)
        a.troca('echo "algum script ainda traz a marca [A ADAPTAR v409] -- NAO RODO"', 'echo "algum script ainda traz a marca de adaptacao pendente (A ADAPTAR v409, no comeco da 2a linha) -- NAO RODO"')
    a.marca(oque); a.grava(); feitos.append(a.p)

# ============================== bancada_B3_servico ==============================
for rel, saida in (("bancada_B3_servico/recibo_parada_v409.py", "RECIBO_PARADA_v409.json"), ("bancada_B3_servico/recibo_religamento_v409.py", "RECIBO_RELIGAMENTO_v409.json")):
    a = Arq(rel)
    a.troca("Adaptado: a autorizacao e' a ORDEM da v409 (fala do operador de 04/11/2026, OPERADOR_04nov_ordem_v408_..., sha16 LIDO do",
            "Adaptado (v409): a autorizacao e' a ORDEM da v409 (fala do operador de 05/11/2026, %s, sha16 LIDO do" % ORDEM_NOME)
    herdada(a)
    a.troca("A autorizacao e' a ORDEM da v409, do operador, de 04/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado", "A autorizacao e' a ORDEM da v409, do operador, de 05/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado")
    a.troca("# a autorizacao tem de ser a ORDEM da v409, de 04/11/2026 (nao a de 03/11 da v408 nem a de 02/11 da v406)", "# a autorizacao tem de ser a ORDEM da v409, de 05/11/2026 (nao a de 04/11 da v408 nem as anteriores)")
    a.troca('ORDEM = os.path.join(D, "..", "..", "..", "cunhagens_13out", "OPERADOR_04nov_ordem_v409_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt")',
            'ORDEM = os.path.join(D, "..", "..", "..", "cunhagens_13out", "%s")' % ORDEM_NOME)
    a.troca('FRASE_DA_ORDEM = "liste as pedras que eu preciso nominar e em seguida produza a v409, rode e quando estiver completa, dê a ordem de handoff para a sessão irmã realizar a custódia completa e atualizar tudo"',
            'FRASE_DA_ORDEM = "%s"' % FRASE)
    a.troca('and "04/11/2026" in AUT, "a autorizacao passada nao e\' a ordem do operador de 04/11/2026 (a ordem da v409:', 'and "05/11/2026" in AUT, "a autorizacao passada nao e\' a ordem do operador de 05/11/2026 (a ordem da v409:')
    a.marca("a ORDEM da v409 e' a fala de 05/11/2026 (%s; frase verbatim conferida no arquivo e no AUT; sha16 lido do arquivo); grava so' %s" % (ORDEM_NOME, saida))
    a.grava(); feitos.append(a.p)

a = Arq("bancada_B3_servico/evento_c1_b3_v409.py"); herdada(a)
a.marca("evento do B(n) da v409 (B18, passo simples v408 -> v409); candidato_sha16 LIDO de ESPERADOS_v409.json e conferido contra o um.py do Nos antes de anotar"); a.grava(); feitos.append(a.p)

a = Arq("bancada_B3_servico/conferir_exigencias_servico_v409.py")
herdada(a)
a.troca("Adaptado: a autorizacao conferida e' a ORDEM da v409 (fala de 04/11/2026;", "Adaptado (v409): a autorizacao conferida e' a ORDEM da v409 (fala de 05/11/2026;")
a.troca("  (e) a autorizacao e' a ORDEM da v409, do operador, de 04/11/2026 («liste as pedras que eu preciso nominar e em seguida produza a v409, rode e quando estiver completa, dê a ordem de handoff para a sessão irmã realizar a custódia completa e atualizar tudo»)",
        "  (e) a autorizacao e' a ORDEM da v409, do operador, de 05/11/2026 («%s»)" % FRASE)
a.troca('ORDEM_ARQ = os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", "OPERADOR_04nov_ordem_v409_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt")',
        'ORDEM_ARQ = os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", "%s")' % ORDEM_NOME)
a.troca('FRASE_DA_ORDEM = "liste as pedras que eu preciso nominar e em seguida produza a v409, rode e quando estiver completa, dê a ordem de handoff para a sessão irmã realizar a custódia completa e atualizar tudo"', 'FRASE_DA_ORDEM = "%s"' % FRASE)
a.troca('chk(nome + ": a ordem de 04/11 (a ordem da v409) e\' conferida: o assert com ORDEM_SHA16 (lido do ARQUIVO da fala) vem DEPOIS do assert AUT", i_ordem is not None and i_assert is not None and i_ordem > i_assert and "cunhagens_13out" in txt and "OPERADOR_04nov_ordem_v408_liste_as_pedras" in txt',
        'chk(nome + ": a ordem de 05/11 (a ordem da v409) e\' conferida: o assert com ORDEM_SHA16 (lido do ARQUIVO da fala) vem DEPOIS do assert AUT", i_ordem is not None and i_assert is not None and i_ordem > i_assert and "cunhagens_13out" in txt and "%s" in txt' % ORDEM_NOME[:-len("_verbatim.txt")])
a.troca('chk(nome + ": nenhum texto, data ou hash de autorizacao anterior sobrou (01/11/2026, 02/11/2026, 03/11/2026; nenhum sha de 16 hex digitado)", "01/11/2026" not in txt and "02/11/2026" not in txt and "03/11/2026" not in txt and re.search(r"[0-9a-f]{16}", txt) is None, ["01/11/2026" in txt, "02/11/2026" in txt, "03/11/2026" in txt, re.findall(r"[0-9a-f]{16}", txt)], [False, False, False, []])',
        'chk(nome + ": nenhum texto, data ou hash de autorizacao anterior sobrou (01/11/2026 a 04/11/2026; nenhum sha de 16 hex digitado)", all(d_ not in txt for d_ in ("01/11/2026", "02/11/2026", "03/11/2026", "04/11/2026")) and re.search(r"[0-9a-f]{16}", txt) is None, [[d_ in txt for d_ in ("01/11/2026", "02/11/2026", "03/11/2026", "04/11/2026")], re.findall(r"[0-9a-f]{16}", txt)], [[False, False, False, False], []])')
a.troca("# ---- a ordem do operador de 04/11 (a ordem da v409) e o AUT do orquestrador", "# ---- a ordem do operador de 05/11 (a ordem da v409) e o AUT do orquestrador")
a.troca('chk("a fala do operador de 04/11 (a ordem da v409: liste as pedras, produza, rode, handoff para a custodia completa, atualize tudo) existe e traz a frase"', 'chk("a fala do operador de 05/11 (a ordem da v409: prossigamos para a proxima versao do um.py; a ratificacao dos nomes) existe e traz a frase"')
a.troca('chk("o AUT do orquestrador (pos_treino_v409.py) e\' a ordem de 04/11 (a ordem da v409): traz o sha16 do arquivo da fala (calculado aqui), a frase e a data, e nenhum texto de 01/11", bool(aut_orq) and ord16 is not None and ord16 in aut_orq and FRASE_DA_ORDEM in aut_orq and "04/11/2026" in aut_orq and "01/11/2026" not in aut_orq',
        'chk("o AUT do orquestrador (pos_treino_v409.py) e\' a ordem de 05/11 (a ordem da v409): traz o sha16 do arquivo da fala (calculado aqui), a frase e a data, e nenhum texto de 01/11", bool(aut_orq) and ord16 is not None and ord16 in aut_orq and FRASE_DA_ORDEM in aut_orq and "05/11/2026" in aut_orq and "01/11/2026" not in aut_orq')
a.marca("confere a ORDEM da v409 (05/11/2026, %s), as datas anteriores (01 a 04/11) ausentes e o AUT do orquestrador com o sha16 lido, a frase e a data" % ORDEM_NOME)
a.grava(); feitos.append(a.p)

a = Arq("bancada_B3_servico/controle_negativo/mutar_conferidor_v409.py")
a.troca("Adaptado: M4 e M6 falam da ORDEM da v409 (fala de 04/11); M5 volta uma data de autorizacao anterior (01/", "Adaptado (v409): M4 e M6 falam da ORDEM da v409 (fala de 05/11); M5 volta a data da autorizacao anterior (04/")
herdada(a)
a.troca("  M4  recibo_parada_v409.py      : sai a conferencia da ordem de 04/11 (a ordem da v409: o assert com a frase e o ORDEM_SHA16): qualquer texto de autorizacao passaria;",
        "  M4  recibo_parada_v409.py      : sai a conferencia da ordem de 05/11 (a ordem da v409: o assert com a frase e o ORDEM_SHA16): qualquer texto de autorizacao passaria;")
a.troca("  M5  recibo_religamento_v409.py : volta uma data de ordem anterior (01/11/2026) como texto no script (autorizacao anterior sobrando).",
        "  M5  recibo_religamento_v409.py : volta a data da ordem anterior (04/11/2026, a da v408) como texto no script (autorizacao anterior sobrando).")
a.troca("  M6  recibo_parada_v409.py      : o caminho do arquivo da fala de 04/11 vira um nome que NAO existe (ordem_v409 no lugar de ordem_v408: o tipo de defeito que uma subida mecanica de rotulo introduz).",
        "  M6  recibo_parada_v409.py      : o caminho do arquivo da fala de 05/11 vira um nome que NAO existe (v410 no lugar de v409: o tipo de defeito que uma subida mecanica de rotulo introduz).")
a.troca("def m4(t):   # sai a conferencia da ordem de 04/11 (a ordem da v409)", "def m4(t):   # sai a conferencia da ordem de 05/11 (a ordem da v409)")
a.troca('    return t.replace(a, a + " (autorizacao de 01/11/2026)", 1)', '    return t.replace(a, a + " (autorizacao de 04/11/2026)", 1)')
a.troca('def m6(t):   # o nome do arquivo da fala vira um inexistente (ordem_v409), o tipo de defeito que uma subida mecanica de rotulo introduz\n    a = "OPERADOR_04nov_ordem_v408_liste_as_pedras_produza_rode"\n    assert t.count(a) == 1\n    return t.replace(a, "OPERADOR_04nov_ordem_v409_liste_as_pedras_produza_rode", 1)',
        'def m6(t):   # o nome do arquivo da fala vira um inexistente (v410 no lugar de v409), o tipo de defeito que uma subida mecanica de rotulo introduz\n    a = "%s"\n    assert t.count(a) == 1\n    return t.replace(a, "%s", 1)' % (ORDEM_NOME, ORDEM_NOME.replace("_v409_", "_v410_")))
a.troca('("M4_sem_a_conferencia_da_ordem_de_04nov", "recibo_parada_v409.py", m4, "recibo_parada_v409.py: a ordem de 04/11 (a ordem da v409) e\' conferida")',
        '("M4_sem_a_conferencia_da_ordem_de_05nov", "recibo_parada_v409.py", m4, "recibo_parada_v409.py: a ordem de 05/11 (a ordem da v409) e\' conferida")')
a.troca('("M5_data_da_ordem_de_01nov_no_script", "recibo_religamento_v409.py", m5,', '("M5_data_da_ordem_de_04nov_no_script", "recibo_religamento_v409.py", m5,')
a.marca("controle negativo do conferidor do servico: M4 a M6 sobre a ORDEM da v409 (05/11/2026); M5 com a data da ordem da v408 (04/11/2026)")
a.grava(); feitos.append(a.p)

# ============================== guardas estaticas, carimbador, logs, arvore, purga, memoria, regras ==============================
a = Arq("guardas_estaticas_bancada_v409.py")
a.troca("[ADAPTADO v409, 04/11/2026, claude-construtor-v409-r2, a servico da gerencia c1] sobre a subida mecanica de rotulo da v408 FINAL", "(nota herdada da v408 [claude-construtor-v408-r2, 04/11/2026], rotulos subidos) sobre a subida mecanica de rotulo da v408 FINAL")
a.troca("nada depende do bundle, que na v409 e' de 4 modulos de TGLExt/)", "nada depende do bundle, que na v409 e' de %d modulo de TGLExt/)" % N_BUNDLE)
a.troca("(so' o rotulo muda: a v409 e' um BUNDLE de 4 modulos de kernel em TGLExt/ e os UNICOS pontos", "(so' o rotulo muda: a v409 e' um BUNDLE de %d modulo de kernel em TGLExt/ e os UNICOS pontos" % N_BUNDLE)
a.marca("o corpo da v408 serve sem mudanca de logica (so' as linhas unicas de ALPHA_FINE_CODATA_2018 e UM_VERSION sao lidas); o pino do esboco vem do CANDIDATO_v409.json")
a.grava(); feitos.append(a.p)

a = Arq("carimbar_stdout_v409.py")
a.troca("[copia na cadeia v409, 04/11/2026, claude-construtor-v409: o corpo e' o do carimbador da v408 (sha16 f0763c383795f3af); so' o rotulo da versao sobe no texto]",
        "[copia na cadeia v409, 05/11/2026, claude-construtor-v409: o corpo e' o do carimbador da v408 (sha16 do arquivo da v408, lido pelo adaptador: %s); so' o rotulo da versao sobe no texto]" % CARIMBO_V408)
a.marca("o carimbador do stdout do rito: corpo da v408, rotulo v409")
a.grava(); feitos.append(a.p)

a = Arq("copiar_logs_do_kernel_v409.py")
a.troca("(adaptado em 04/11/2026 a v409; desde a v408 ele nao grava nada: so' compara)", "(adaptado em 05/11/2026 a v409; desde a v408 ele nao grava nada: so' compara)")
a.troca("`lake build` a frio dos 4 modulos novos do bundle (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP)", "`lake build` a frio do modulo novo do bundle (TraducaoTuring)")
a.marca("conferidor idempotente dos logs do kernel da v409 (le KH_N1_v409.json e LOGS_COPIADOS_v409.json); nada de bundle no corpo")
a.grava(); feitos.append(a.p)

a = Arq("refazer_arvore_v409_pos_selo.py")
a.troca("o TGL/Audit.lean, os 4 modulos novos em TGLExt/ (R[\"pedras\"]", "o TGL/Audit.lean, o modulo novo em TGLExt/ (R[\"pedras\"]")
a.troca("a conferencia equivalente (as mesmas contagens e os mesmos sha contra a arvore ja' existente) foi feita so' por leitura em 04/11/2026 (pos_build_kernel_v409.py e p00).", "a conferencia equivalente (as mesmas contagens e os mesmos sha contra a arvore ja' existente) foi feita so' por leitura em 05/11/2026 (pos_build_kernel_v409.py e p00).")
a.troca("adaptado a v409 em 04/11/2026 (claude-construtor-v409)", "adaptado a v409 em 05/11/2026 (claude-construtor-v409)")
a.marca("pos-selo: refaz C:/t/k409c/arvore a partir do Nos v409 e confere contra KERNEL_RECIBO_v409.json (o corpo le tudo do recibo; NAO executado na preparacao)")
a.grava(); feitos.append(a.p)

a = Arq("refazer_sandbox_v409_pos_selo.sh")
a.troca("(raiz, Audit, os 4 modulos novos em TGLExt/ e as contagens de .lean)", "(raiz, Audit, o modulo novo em TGLExt/ e as contagens de .lean)")
a.marca("pos-selo: chama refazer_arvore_v409_pos_selo.py (NAO executado na preparacao)")
a.grava(); feitos.append(a.p)

a = Arq("purga_v409.py")
a.troca("por isso a validacao de preparacao (04/11/2026) foi so' de sintaxe", "por isso a validacao de preparacao (05/11/2026) foi so' de sintaxe")
a.marca("so' leitura; conta os padroes da fala de 25/10 e da fala excluida na pasta v409 e em C:\\t\\k409c (o corpo nao depende de versao); corre por fora (~20 min)")
a.grava(); feitos.append(a.p)

a = Arq("pino_memoria_py_v409.py")
a.troca('"""pino_memoria_py_v409.py (adaptado em 04/11/2026: o corpo nao depende do bundle; conferido por leitura, em 04/11/2026, que o memoria.py de hoje tem o sha16 declarado, o mesmo da v408; NAO executado na preparacao: e\' ato da gerencia)',
        '"""pino_memoria_py_v409.py (adaptado em 05/11/2026: o corpo nao depende do bundle; o sha16 declarado e\' o mesmo da v408, [DECLARADO], e so\' vale se o lido for igual; NAO executado na preparacao: e\' ato da gerencia antes do p00)')
a.marca("pina o memoria.py da fila (ato da gerencia antes do p00; nao executado pelo construtor)")
a.grava(); feitos.append(a.p)

a = Arq("regras_v409.py")
a.troca("# regras_v409.py -- ESCRITO em 04/11/2026 pela preparacao da cadeia v409", "# regras_v409.py -- ESCRITO em 05/11/2026 pela preparacao da cadeia v409")
a.marca("regras de permissao da cadeia v409 (RECUSA sem V409_REGRAS_AUTORIZADAS=sim; ato da gerencia; nao executado)")
a.grava(); feitos.append(a.p)

# ============================== guarda da ordem de chamada ==============================
a = Arq("guarda_ordem_de_chamada_v409.py")
a.troca("ADAPTADA a v409 (03/11/2026): a funcao NOVA e' UMA, `psion_canto_v407`", "(na v408 a funcao NOVA era o `tetelestai_terminal_v408`; na v407, o `psion_canto_v407`.) ADAPTADA a v409 (05/11/2026): a funcao NOVA e' UMA, `traducao_turing_v409` (le do core `kernel_formalization`, `external_ladder`, `qg_closure` e `beta`; chamada no main LOGO DEPOIS do bloco do `tetelestai_terminal_v408` e dos specs da v408; miolo `_v409_formal`, `_v398_beta`; mecanica `v409_traducao_mechanics`); a da v407 era o `psion_canto_v407`")
a.troca('FUNCOES_HERDADAS_V409 = FUNCOES_HERDADAS_V408 + ("fechamento_v406", "psion_canto_v407")   # (v409: os registros da v406 e da v408 sao herdados, intactos: nenhuma chave antiga muda)',
        'FUNCOES_HERDADAS_V409 = FUNCOES_HERDADAS_V408 + ("fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408")   # (v409: os registros da v406, da v407 e da v408 sao herdados, intactos: nenhuma chave antiga muda)')
a.troca('FUNCOES_NOVAS_V409 = ("tetelestai_terminal_v408",)                 # a v409 e\' um BUNDLE de quatro modulos de kernel: o UNICO registro com funcao novo e\' o do terminal',
        'FUNCOES_NOVAS_V409 = ("traducao_turing_v409",)                     # a v409 e\' um BUNDLE de um modulo de kernel: o UNICO registro com funcao novo e\' o da traducao')
a.troca('MECANICA_DE["tetelestai_terminal_v408"] = "v408_terminal_mechanics"\n', 'MECANICA_DE["tetelestai_terminal_v408"] = "v408_terminal_mechanics"\nMECANICA_DE["traducao_turing_v409"] = "v409_traducao_mechanics"\n')
a.troca('             "tetelestai_terminal_v408": ("_v408_formal", "_v398_beta")}   # o miolo comum do terminal (nao le chave de testemunha: nenhuma chave antiga muda)',
        '             "tetelestai_terminal_v408": ("_v408_formal", "_v398_beta"),   # o miolo comum do terminal (nao le chave de testemunha: nenhuma chave antiga muda)\n'
        '             "traducao_turing_v409": ("_v409_formal", "_v398_beta")}   # o miolo comum da traducao (nao le chave de testemunha: nenhuma chave antiga muda)')
a.troca('INSUMOS_EXIGIDOS = {"tetelestai_terminal_v408": ("psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),',
        'INSUMOS_EXIGIDOS = {"traducao_turing_v409": ("tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),\n'
        '                    "tetelestai_terminal_v408": ("psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),')
a.troca("    (8) [v408] o tetelestai_terminal_v408 chamado ANTES do psion_canto_v407 reprova, e o motivo e' o insumo exigido ausente; (9) [v408] o tetelestai_terminal_v408 sem a chamada no main reprova. Rodado sobre o texto: nada executa.\"\"\"",
        "    (8) [v408] o tetelestai_terminal_v408 chamado ANTES do psion_canto_v407 reprova, e o motivo e' o insumo exigido ausente; (9) [v408] o tetelestai_terminal_v408 sem a chamada no main reprova;\n"
        "    (10) [v409] o traducao_turing_v409 chamado ANTES do tetelestai_terminal_v408 reprova, e o motivo e' o insumo exigido ausente; (11) [v409] o traducao_turing_v409 sem a chamada no main reprova. Rodado sobre o texto: nada executa.\"\"\"")
a.troca('    r8 = ordem_de_chamada(_sem_chamada(src, "tetelestai_terminal_v408", "_r408"), ("tetelestai_terminal_v408",))\n',
        '    r8 = ordem_de_chamada(_sem_chamada(src, "tetelestai_terminal_v408", "_r408"), ("tetelestai_terminal_v408",))\n'
        '    # (10) o traducao_turing_v409 e o tetelestai_terminal_v408 trocam de lugar: a traducao passa a ser chamada ANTES do terminal\n'
        '    r9 = ordem_de_chamada(_troca_blocos(src, "tetelestai_terminal_v408", "traducao_turing_v409"), ("traducao_turing_v409",))\n'
        '    f9_ = r9["funcoes"].get("traducao_turing_v409") or {}\n'
        '    # (11) a chamada do traducao_turing_v409 sai do main\n'
        '    r10 = ordem_de_chamada(_sem_chamada(src, "traducao_turing_v409", "_r409"), ("traducao_turing_v409",))\n')
a.troca('"tetelestai_sem_chamada_no_main_reprova": bool(not r8["ok"] and "erro" in (r8["funcoes"].get("tetelestai_terminal_v408") or {}))}',
        '"tetelestai_sem_chamada_no_main_reprova": bool(not r8["ok"] and "erro" in (r8["funcoes"].get("tetelestai_terminal_v408") or {})),\n'
        '         "traducao_antes_do_terminal_reprova": bool(not r9["ok"] and "tetelestai_terminal_v408" in (f9_.get("insumos_exigidos_ausentes") or [])), "traducao_sem_chamada_no_main_reprova": bool(not r10["ok"] and "erro" in (r10["funcoes"].get("traducao_turing_v409") or {}))}')
a.marca("a funcao NOVA e' traducao_turing_v409 (depois do tetelestai_terminal_v408 e dos specs da v408); o terminal passa a herdado; controles negativos (10) e (11)")
a.grava(); feitos.append(a.p)

# ============================== simulacao da arvore do Nos ==============================
a = Arq("simular_arvore_do_nos_v409.py")
linha(a, "# ADAPTADO a v409 (04/11/2026, claude-construtor-v409): molde v408/simular_arvore_do_nos_v408.py;",
      "# (v409, 05/11/2026, claude-construtor-v409, fork B) molde v408/simular_arvore_do_nos_v408.py; bundle de %d modulo em TGLExt/ (TraducaoTuring), registro traducao_turing_v409 + specs cunhagens_v409/kh_n1_cobertura_v409 chamados NA ORDEM DO MAIN depois dos da v408 (tetelestai_terminal_v408 e os specs da v408, herdados); a chave do lema (v407) segue conferida como herdada; nenhuma chave antiga muda." % N_BUNDLE)
a.troca("v394, v395, v397, v401, v408 e v409 sobre esse kf (mais os quatro registros com funcao da v403, os tres da v404, os oito da v405, o `fechamento_v406` herdado e o `psion_canto_v407` da v409, que le a chave do lema e as quatro da v408).",
        "v394 a v409 sobre esse kf (mais os quatro registros com funcao da v403, os tres da v404, os oito da v405, o `fechamento_v406`, o `psion_canto_v407` e o `tetelestai_terminal_v408` herdados e o `traducao_turing_v409` novo).")
a.troca("ADAPTADO a v409 (03/11/2026): a arvore do Nos depois do rito", "ADAPTADO (v407 a v409): a arvore do Nos depois do rito")
a.troca("e o pino exato esta no spec `kh_n1_cobertura_v407`.", "e o pino exato esta no spec `kh_n1_cobertura_v409`.")
a.troca("um.tetelestai_terminal_v408(core); um._v408_rodar_specs(core)   # (v409:", "um.tetelestai_terminal_v408(core); um._v408_rodar_specs(core); um.traducao_turing_v409(core); um._v409_rodar_specs(core)   # (v409: a traducao_turing_v409 vem logo depois dos specs da v408, como no main;")
a.troca('for k in ("tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408",', 'for k in ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408",')
a.marca("simula a arvore do Nos depois do rito e roda os registros da v394 a v409 (traducao_turing_v409 e os specs da v409 depois dos da v408)")
a.grava(); feitos.append(a.p)

# ============================== instalar / reverter / rito e o conferidor deles ==============================
a = Arq("instalar_v409.py")
a.troca("(ato da gerencia c1; adaptado em 04/11/2026 por claude-construtor-v409 para o BUNDLE PEQUENO de quatro modulos em TGLExt/ [TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP], NAO executado na preparacao)",
        "(ato da gerencia c1; adaptado em 05/11/2026 por claude-construtor-v409 para o BUNDLE PEQUENO de um modulo em TGLExt/ [TraducaoTuring], NAO executado na preparacao)")
a.troca("a v409 so' ACRESCENTA quatro imports na raiz e nao muda o Audit;", "a v409 so' ACRESCENTA um import na raiz (o import da TraducaoTuring) e nao muda o Audit;")
a.troca("(a v409 traz 4 modulos novos de kernel em TGLExt/ [TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, com os nomes dados pelo operador em 04/11/2026; nenhum da bancada do ChatGPT];",
        "(a v409 traz %d modulo novo de kernel em TGLExt/ [TraducaoTuring, com o nome dado pela gerencia e ratificado pelo operador em 05/11/2026; nenhum da bancada do ChatGPT];" % N_BUNDLE)
a.troca("e os 9 modulos da v408: PsionCanto, Par, APonteDoAtrito, OUmInscrito, KEhATangente, AChaveDaGuarda, OGuarda, LeituraPreservada, OIgual)",
        "os 9 modulos da v407: PsionCanto, Par, APonteDoAtrito, OUmInscrito, KEhATangente, AChaveDaGuarda, OGuarda, LeituraPreservada, OIgual, e os 4 modulos da v408: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP)")
a.troca('                      "PsionCanto", "Par", "APonteDoAtrito", "OUmInscrito", "KEhATangente", "AChaveDaGuarda", "OGuarda", "LeituraPreservada", "OIgual")   # (os 9 da v408, lidos pelo adaptador da lista de modulos novos pinada na cadeia v408)',
        '                      "PsionCanto", "Par", "APonteDoAtrito", "OUmInscrito", "KEhATangente", "AChaveDaGuarda", "OGuarda", "LeituraPreservada", "OIgual",   # (os 9 da v407)\n'
        '                      "TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP")   # (os 4 da v408: os nomes da lista de modulos novos pinada na cadeia v408, kernel_modulos_novos_v408.json, conferidos pelo adaptador)')
a.troca('"as pedras anteriores (v394 a v408, as oito da v405, os 9 modulos da v408 e o bundle do fecho da v406 inclusive) nao estao no kernel do Nos -- nao instalo"',
        '"as pedras anteriores (v394 a v408, as oito da v405, os 9 modulos da v407, os 4 da v408 e o bundle do fecho da v406 inclusive) nao estao no kernel do Nos -- nao instalo"')
a.troca('("a lista dos modulos novos nao e\' a do ESPERADOS (o bundle de quatro modulos em TGLExt/)", _N)', '("a lista dos modulos novos nao e\' a do ESPERADOS (o bundle de um modulo em TGLExt/)", _N)')
a.marca("instala o candidato v409 (ato da gerencia): a raiz ganha UM import; as pedras anteriores incluem os 9 da v407 e os 4 da v408; a lista dos modulos novos lida de kernel_modulos_novos_v409.json")
a.grava(); feitos.append(a.p)

a = Arq("reverter_v409.py")
a.troca("adaptado em 04/11/2026 por claude-construtor-v409 para o BUNDLE PEQUENO de quatro modulos em TGLExt/, NAO executado na preparacao)", "adaptado em 05/11/2026 por claude-construtor-v409 para o BUNDLE PEQUENO de um modulo em TGLExt/, NAO executado na preparacao)")
a.troca("e poe os 4 modulos novos de kernel da v409 (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, em TGLExt/: a lista que o instalador gravou;", "e poe o modulo novo de kernel da v409 (TraducaoTuring, em TGLExt/: a lista que o instalador gravou;")
a.marca("reverte a instalacao da v409 (ato da gerencia, so' se o rito falhar): o modulo da lista do instalador vai a quarentena; o um.py volta a v408 (sha16 lido de ESPERADOS_v408.json)")
a.grava(); feitos.append(a.p)

a = Arq("rito_v409.sh")
linha(a, "# O RITO v409 (ato da gerencia c1, adaptado em 04/11/2026 por claude-construtor-v409; Tetelestai e' o terminal):",
      "# O RITO v409 (ato da gerencia c1, adaptado em 05/11/2026 por claude-construtor-v409; a traducao as classes de Turing): roda o um.py v409 instalado no Nos -- %d modulo(s) novo(s) de kernel em TGLExt/ (o BUNDLE PEQUENO: TraducaoTuring, com o nome dado pela gerencia e ratificado pelo operador em 05/11/2026; "
      "a lista e' lida de kernel_modulos_novos_v409.json e conferida contra ESPERADOS.bundle_sha256) materializado a partir do corpo embutido, kernel e Audit" % N_BUNDLE)
linha(a, "# construidos pelo proprio um.py (a raiz TGLExt.lean ganha quatro imports; o Audit nao muda), o registro com FUNCAO tetelestai_terminal_v408",
      "# construidos pelo proprio um.py (a raiz TGLExt.lean ganha um import; o Audit nao muda), o registro com FUNCAO traducao_turing_v409 (chamado no main logo depois do bloco do tetelestai_terminal_v408 e dos registros por spec da v408; le as %d ancoras do axiom_report do rito, a fonte embutida por sha256, "
      "as %d falas de 05/11 por sha256 [de duas, so' o trecho que a D59 deixa entrar] e a escada; faz as 17 checagens com a instancia de brinquedo fixa; NENHUMA chave antiga muda: a chave do lema (v407) segue LIDA do kernel; os vereditos de testemunha_estatica_v396, psibit_v395, rede_fock_v394, fechamento_v406, "
      "psion_canto_v407 e tetelestai_terminal_v408 nao mudam de prefixo; o gate e a funcao do neutrino nao mudam; o numero da massa nao muda), os registros por spec novos do core v409 (cunhagens_v409, com as %d falas de 05/11, os nomes da gerencia ratificados pelo operador, as decisoes %s a %s e as erratas %s a %s; kh_n1_cobertura_v409; "
      "os da v408, cunhagens_v408 e kh_n1_cobertura_v408, e os da v407, cunhagens_v407 e kh_n1_cobertura_v407, seguem, com a escada subida, os pisos da cobertura da v408, a errata E26 ao lado e o pino do acervo da v407 na copia purgada) e os demais registros, sem mudanca de veredito."
      % (N_ANC, N_FALAS, N_FALAS, DEC_NOVAS[0], DEC_NOVAS[-1], ERR_NOVAS[0], ERR_NOVAS[-1]))
linha(a, "# O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (a mesma da v408;",
      "# O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (a mesma da v408; o motor continuo no pilar NAO entra na v409: as decisoes D38/D45 das cadeias anteriores seguem, nenhuma decisao da v409 [%s a %s] as muda); TGL_RITE_CHECKPOINT DESLIGADO; nenhum dado novo e' aberto (o teste (d) do ramo B segue so' por citacao do pre-registro V1.1, D44 herdada). "
      "Molde: o rito da v408 (herdeiro do rito_v399.sh com as afericoes dele), trocados os nomes, o pacote (a propria pasta da cadeia v409) e a" % (DEC_NOVAS[0], DEC_NOVAS[-1]))
linha(a, "# TEMPO ESPERADO (v409, parametro lido de kernel/construir_marcas.txt e kernel/POS_BUILD_v409.json,",
      "# TEMPO ESPERADO (v409, parametro lido de kernel/construir_marcas.txt e kernel/POS_BUILD_v409.json, MEDIDO em 05/11/2026 no sandbox k409c): o `lake build` do modulo novo a frio (a v408 selada ja' esta' compilada em .lake/build; muda a raiz TGLExt; o Audit nao muda) = %d s e 1 Audit = %d s "
      "(a soma dos tempos por modulo e' %s s, o maximo de um modulo %s s); o rito faz 3 passagens de build + Audit no Nos, cuja arvore compilada e' a da v408: a PRIMEIRA compila o modulo a frio (a ordem de grandeza e' a medida do sandbox, %d s + %d s) e as outras duas passagens so' reconferem (build ja' pronto + Audit de %d s) "
      "[estimativa da gerencia, nao medida: o tempo total do rito sai das marcas rito_horarios_v409.txt]. O timeout do lake build DENTRO do um.py (candidato) tem de caber nisso: conferir no candidato antes de rodar." % (T_BUILD, T_AUDIT, T_SOMA, T_MAX, T_BUILD, T_AUDIT, T_AUDIT))
a.marca("o rito da v409 (ato da gerencia): textos do bundle de um modulo, do registro traducao_turing_v409 e do tempo medido; o corpo e' o do rito da v408")
a.grava(); feitos.append(a.p)

a = Arq("conferir_instalar_rito_v409.py")
a.troca("(derivados dos da v408, adaptados em 04/11/2026 ao BUNDLE PEQUENO de quatro modulos em TGLExt/, com as licoes da v408)", "(derivados dos da v408, adaptados em 05/11/2026 ao BUNDLE PEQUENO de um modulo em TGLExt/, com as licoes da v408)")
a.troca("a raiz e o Audit da v408 conferidos antes de instalar, os quatro modulos em TGLExt/, nao em TGLExt/F1Fecho394/...; as pedras anteriores incluem os 9 modulos da v408)", "a raiz e o Audit da v408 conferidos antes de instalar, o modulo em TGLExt/, nao em TGLExt/F1Fecho394/...; as pedras anteriores incluem os 9 modulos da v407 e os 4 da v408)")
a.troca('_DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D7.DECISOES), key=lambda k_: int(k_[1:]))   # as decisoes que a v409 acrescenta (D48..D54), lidas de DL (a diferenca contra o delta da v408, nao contra o da v406)\nassert _DEC_NOVAS and _DEC_NOVAS[0] == "D48" and _DEC_NOVAS[-1] == "D54", _DEC_NOVAS',
        '_DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D8.DECISOES), key=lambda k_: int(k_[1:]))   # as decisoes que a v409 acrescenta (D55..D60), lidas de DL (a diferenca contra o delta da v408)\nassert _DEC_NOVAS and _DEC_NOVAS[0] == "D55" and _DEC_NOVAS[-1] == "D60", _DEC_NOVAS')
a.troca('_ERR_NOVAS = [e_.split(" --")[0] for e_ in DL.ERRATAS_V409]   # as erratas da v409 (E21..E23), lidas de DL\nassert _ERR_NOVAS == ["E21", "E22", "E23"], _ERR_NOVAS',
        '_ERR_NOVAS = [e_.split(" --")[0] for e_ in DL.ERRATAS_V409]   # as erratas da v409 (E24..E26), lidas de DL\nassert _ERR_NOVAS == ["E24", "E25", "E26"], _ERR_NOVAS')
a.troca('"TetelestaiTerminal", "PIgualNP", "PsionCanto", "OIgual", "quatro imports", "os 9 modulos da v408", "bundle do fecho da v406"],',
        '"TetelestaiTerminal", "PIgualNP", "PsionCanto", "OIgual", "um import na raiz", "os 9 modulos da v407", "os 4 modulos da v408", "TraducaoTuring", "bundle do fecho da v406"],')
a.troca('"PsionCanto, Par e as sete pedras de 02/11, todos de nome ratificado", "bundle do fecho da v408", "03/11/2026"])',
        '"PsionCanto, Par e as sete pedras de 02/11, todos de nome ratificado", "bundle do fecho da v408", "03/11/2026", "quatro imports", "os 9 modulos da v408", "04/11/2026", "o bundle de quatro modulos", "BUNDLE PEQUENO de quatro modulos"])')
a.troca('"tentativa_v408_rito_falhou_", "modulos_novos_v408", "rodada_v408_stdout", "pedras_sha256", "quarentena_pedras_", \'x_.startswith("TGLExt/F1Fecho394/")\', "== 301", "o bundle de 301", "301 modulos novos", "[A ADAPTAR v409]", "nove modulos", "PsionCanto, Par e as sete pedras de 02/11", "03/11/2026"])',
        '"tentativa_v408_rito_falhou_", "modulos_novos_v408", "rodada_v408_stdout", "pedras_sha256", "quarentena_pedras_", \'x_.startswith("TGLExt/F1Fecho394/")\', "== 301", "o bundle de 301", "301 modulos novos", "[A ADAPTAR v409]", "nove modulos", "PsionCanto, Par e as sete pedras de 02/11", "03/11/2026", "04/11/2026", "quatro modulos", "TetelestaiTerminal, TempoIgualMoeda"])')
a.troca('"%d modulos novos de kernel em TGLExt/" % DL.N_BUNDLE, "le as %d ancoras do axiom_report" % len(DL.ANCORAS),', '"%d modulo(s) novo(s) de kernel em TGLExt/" % DL.N_BUNDLE, "le as %d ancoras do axiom_report" % len(DL.ANCORAS),')
a.troca('"tetelestai_terminal_v408", "TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "E21", "D38/D45", "NENHUMA chave antiga muda", "%d falas de 04/11" % DL.N_FALAS_V409,',
        '"traducao_turing_v409", "TraducaoTuring", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "E26", "D38/D45", "NENHUMA chave antiga muda", "%d falas de 05/11" % DL.N_FALAS_V409, "17 checagens",')
a.troca('"9 modulos novos de kernel em TGLExt/", "nove imports", "76 ancoras", "PsionCanto e Par, da gerencia c1", "the_psion_is_the_corner_on_both_faces", "D41 a D47", "E18 a E20", "o psion, o canto e o par", "carimbar_stdout_v408.py", "03/11/2026"])',
        '"9 modulos novos de kernel em TGLExt/", "nove imports", "76 ancoras", "PsionCanto e Par, da gerencia c1", "the_psion_is_the_corner_on_both_faces", "D41 a D47", "E18 a E20", "o psion, o canto e o par", "carimbar_stdout_v408.py", "03/11/2026",\n'
        '                              "4 modulos novos de kernel", "quatro imports", "48 ancoras", "D48 a D54", "E21 a E23", "Tetelestai e\' o terminal)", "falas de 04/11", "com o PIgualNP R3"])')
a.troca('("lista_que_nao_e_lista", {"novos": "TGLExt/TetelestaiTerminal.lean"})', '("lista_que_nao_e_lista", {"novos": "TGLExt/TraducaoTuring.lean"})')
a.troca('"[A ADAPTAR v409]"', '"[A ADAPTAR " + "v409]"', 3)   # (a marca ausente montada por concatenacao: o literal inteiro so' existe na 2a linha dos arquivos ainda nao adaptados)
a.marca("confere instalar/reverter/rito da v409 sem executar: marcas do bundle de um modulo, do registro traducao_turing_v409, D55-D60/E24-E26 lidas do delta, o tempo medido; o trecho da lista extraido por AST")
a.grava(); feitos.append(a.p)

# ============================== encadeadores ==============================
a = Arq("regerar_v409.sh")
a.troca("# regerar_v409.sh -- refaz, NA ORDEM, tudo o que depende do BUNDLE PEQUENO de 4 modulos (adaptado em 04/11/2026 da v408: la' eram os 9 modulos do psion e do canto; aqui o kernel novo sao 4 modulos em TGLExt/: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, com os nomes dados pelo operador em 04/11, normalizados por preparar_bundle_v409_04nov.py):",
        "# regerar_v409.sh -- refaz, NA ORDEM, tudo o que depende do BUNDLE PEQUENO de um modulo (adaptado em 05/11/2026 da v408: la' eram os 4 modulos do terminal; aqui o kernel novo e' UM modulo em TGLExt/: TraducaoTuring, com o nome dado pela gerencia e ratificado pelo operador em 05/11, normalizado por preparar_bundle_v409_05nov.py):")
a.troca("O sandbox C:\\t\\k409c\\final nasce de `sh ./copiar_k409c.sh` (robocopy do kernel do Nos v408 selado, so' leitura; sem /PURGE) e recebe o bundle UMA VEZ por `preparar_bundle_v409_04nov.py`",
        "O sandbox C:\\t\\k409c\\final nasce de `sh ./copiar_k409c.sh` (robocopy de C:\\t\\k408c\\final, o kernel da v408 ja' compilado, so' leitura; sem /PURGE) e recebe o bundle UMA VEZ por `preparar_bundle_v409_05nov.py`")
a.troca("# O build leva ~6 min e o Audit ~4 min no sandbox (medido em 04/11/2026: kernel/construir_marcas.txt, 331 s e 251 s: incremental sobre a v408 compilada, so' os 4 modulos a frio).",
        "# O build leva ~%d min e o Audit ~%d min no sandbox (medido em 05/11/2026: kernel/construir_marcas.txt, %d s e %d s: incremental sobre a v408 compilada, so' o modulo novo a frio)." % (round(T_BUILD / 60), round(T_AUDIT / 60), T_BUILD, T_AUDIT))
a.marca("regera, na ordem, o que depende do bundle de um modulo (guarda do sandbox, build, pos_build, insumos, refazer_candidato); o sandbox nasce de copiar_k409c.sh + preparar_bundle_v409_05nov.py")
a.grava(); feitos.append(a.p)

a = Arq("refazer_candidato_v409.sh")
a.troca("ou o kernel (copiar_k409c.sh + preparar_bundle_v409_04nov.py + construir_kernel_v409.sh", "ou o kernel (copiar_k409c.sh + preparar_bundle_v409_05nov.py + construir_kernel_v409.sh")
a.troca("# [v409, adaptado em 04/11/2026, claude-construtor-v409] o candidato e' o do BUNDLE PEQUENO de 4 modulos em TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP; registro com funcao tetelestai_terminal_v408 + specs cunhagens_v408/kh_n1_cobertura_v408); os 9 modulos do psion (v408) e os 301 do fecho (v406) ficam no kernel como registro;",
        "# [v409, adaptado em 05/11/2026, claude-construtor-v409] o candidato e' o do BUNDLE PEQUENO de um modulo em TGLExt/ (TraducaoTuring; registro com funcao traducao_turing_v409 + specs cunhagens_v409/kh_n1_cobertura_v409); os 4 modulos do terminal (v408), os 9 do psion (v407) e os 301 do fecho (v406) ficam no kernel como registro;")
a.marca("refaz, na ordem, tudo o que depende do texto do candidato v409 (gerador, comparacao, ensaio, ESPERADOS, conferidor, citacoes, pinos, instalar/rito, p00)")
a.grava(); feitos.append(a.p)

a = Arq("fim_de_cadeia_v409.sh")
a.troca("# fim_de_cadeia_v409.sh -- (adaptado em 04/11/2026, claude-construtor-v409;", "# fim_de_cadeia_v409.sh -- (adaptado em 05/11/2026, claude-construtor-v409;")
a.marca("o que vem depois do refazer_candidato: B(n) pre-selo, servico estatico, derivacao do pos-rito, harnesses e previa do X (o corpo nao depende do numero de modulos)")
a.grava(); feitos.append(a.p)

print("\nADAPTADOS:", len(feitos))
for p in feitos:
    print("  ", os.path.relpath(p, HERE))
