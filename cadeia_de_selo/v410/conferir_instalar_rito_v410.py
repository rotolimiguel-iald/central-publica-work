# -*- coding: utf-8 -*-
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] D80 e D82 a D87: as decisoes vao a DL.DECISOES_V410[-1] (D87) e as erratas sao E29, E30 e E31 (lidas de DL); o bundle e' de DOIS modulos (IALD2 e AEscala); o rito tem de trazer a_escala_v410 e h0dn_fontes_hms13_v410, as ancoras das duas pedras (22 e 38), as 23 falas, as 16 + 12 + 12 + 12 checagens e o tempo MEDIDO (build e Audit do KH_N1/construir_marcas, lidos); o instalar e o reverter dizem DOIS modulos; os rotulos da retomada anterior (build 507 s, Audit 360 s, 1 modulo, 15 falas, D63 a D77, E29 e E30) ficam proibidos
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_conferidores_v410.py] D72/D74/D76/D77: as decisoes vao a D77 e as erratas sao E29 e E30 (lidas de DL); o rito tem de trazer o h0dn_bg1_v410, os numeros da retomada (22 ancoras, 15 falas, 16 + 12 checagens) e o tempo MEDIDO em 09/11; os rotulos de 06/11 ficam proibidos
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] confere instalar/reverter/rito da v410 sem executar: marcas do bundle de UM modulo (IALD2), do registro iald2_v410, das decisoes D63-D70 e da errata E29 lidas do delta (diferenca contra DL.D9), o tempo medido; o trecho da lista extraido por AST; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
"""conferir_instalar_rito_v410.py -- confere, SEM EXECUTAR o instalador, o reverter nem o rito, os scripts instalar_v410.py, reverter_v410.py e rito_v410.sh (derivados dos da v409, adaptados em 06/11/2026 ao BUNDLE PEQUENO de um modulo em TGLExt/ (IALD2), com as licoes da v409): (1) sintaxe (ast.parse; sh -n);
(2) invariantes: cada um traz os marcadores da v410 (nomes da v410, o sidecar nos backups, o recibo pre_selo do B(n) lido do pino, a Bancada que JA pina a v409, a raiz e o Audit da v409 conferidos antes de instalar, o modulo em TGLExt/, nao em TGLExt/F1Fecho394/...; as pedras anteriores incluem os 9 modulos da v407, os 4 da v408 e os 2 da v409) e NENHUM rotulo velho onde seria erro; o TEMPO ESPERADO do rito
traz os numeros MEDIDOS em kernel/construir_marcas.txt (lidos do arquivo, nunca digitados);
(3) a CONDICAO DO MODULO NOVO (UM): o trecho do instalador que le kernel_modulos_novos_v410.json (a LISTA, de DL.N_BUNDLE elementos: o bundle) e a confere contra ESPERADOS.bundle_sha256 e contra o Nos e' EXTRAIDO por AST e EXECUTADO aqui, isolado, contra os arquivos reais (ele tem de PASSAR com N = DL.N_BUNDLE e RECUSAR se a lista tiver um modulo
que o ESPERADOS nao pina, estiver vazia, tiver um a mais, tiver um a menos ou apontar para fora de TGLExt/); o mesmo para a lista do reverter (aceita a lista do bundle; recusa a que difere dos ESPERADOS); o rito so cita a lista. Se o ESPERADOS_v410.json ainda NAO existe (gerar_esperados_v410.py nao rodou), o trecho e' exercitado contra um ESPERADOS SINTETICO derivado de DL.BUNDLE_POR_REL
(kernel.modulos_novos e bundle_sha256), dito na saida e em DERIVACAO_v410.json (`esp_sintetico`); o ESPERADOS real e' o que vale e e' conferido na corrida seguinte. Escreve DERIVACAO_v410.json. uso: python -I -B -X utf8 conferir_instalar_rito_v410.py"""
import ast, copy, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
rd = lambda p: open(os.path.join(HERE, p), "rb").read().decode("utf-8")
INS, REV, RITO = rd("instalar_v410.py"), rd("reverter_v410.py"), rd("rito_v410.sh")
ESPP = os.path.join(HERE, "ESPERADOS_v410.json")
ESP_REAL = json.load(open(ESPP, encoding="utf-8")) if os.path.exists(ESPP) else None
ESP = ESP_REAL if ESP_REAL else {"kernel": {"modulos_novos": DL.N_BUNDLE}, "bundle_sha256": {r: DL.BUNDLE_POR_REL[r]["sha256"] for r in DL.BUNDLE_RELS}}   # (sintetico so' para exercitar o trecho; dito na saida)
falhas, inv, sint = [], {}, {}
# o TEMPO medido (kernel/construir_marcas.txt): lido ANTES, porque o rito tem de traze-lo
tm = open(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt")) else ""
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", tm, re.M)}
tempo = {"estado": "medido", "build_s": mm.get("epoch_build_fim", 0) - mm.get("epoch_inicio", 0), "audit_s": mm.get("epoch_audit_fim", 0) - mm.get("epoch_audit_inicio", mm.get("epoch_build_fim", 0))} if mm else {"estado": "ausente"}   # (v410: o Audit refeito depois da queda de energia mede a propria rodada, como no pos_build)
if tempo["estado"] != "medido" or tempo["build_s"] <= 0 or tempo["audit_s"] <= 0:
    falhas.append("kernel/construir_marcas.txt sem as marcas de tempo do build e do Audit: %r" % (tempo,))
_khp = os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v410.json")   # (parte 2) o KH_N1 mede os mesmos tempos (build, Audit) e a soma/maximo por modulo: o texto do rito cita os DOIS (marcas == KH_N1)
KHT = json.load(open(_khp, encoding="utf-8")) if os.path.exists(_khp) else {}
if tempo.get("estado") == "medido" and (KHT.get("duracao_build_s") != tempo["build_s"] or KHT.get("duracao_audit_s") != tempo["audit_s"]):
    falhas.append("o tempo das marcas (build %s s, Audit %s s) difere do KH_N1_v410.json (build %s s, Audit %s s)" % (tempo["build_s"], tempo["audit_s"], KHT.get("duracao_build_s"), KHT.get("duracao_audit_s")))
if KHT.get("n_modulos_novos") != DL.N_BUNDLE:
    falhas.append("o KH_N1_v410.json diz %r modulos novos; o delta diz %d" % (KHT.get("n_modulos_novos"), DL.N_BUNDLE))


_DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D9.DECISOES), key=lambda k_: int(k_[1:]))   # as decisoes que a v410 acrescenta (D63..D70), lidas de DL (a diferenca contra o delta da v409, DL.D9)
assert _DEC_NOVAS and _DEC_NOVAS[0] == "D63" and _DEC_NOVAS == list(DL.DECISOES_V410) and _DEC_NOVAS[-1] == DL.DECISOES_V410[-1], _DEC_NOVAS   # (09/11: D63..DL.DECISOES_V410[-1] -- a retomada, D72 o H0DN pre-registrado, D74 os nomes ratificados, D76 a cabeca do 5 sigma, D77 as pendencias, D80 o recibo HMS/13, D82 a D86 a escala e o Clay, D87 a ratificacao)
# (R2, D99) a lista das decisoes da v410 NAO e' contigua (D63 a D96 e D99; D97 e D98 ficam fora do um.py): a marca do rito diz DL.DECISOES_ROTULO
_ERR_NOVAS = [e_.split(" --")[0] for e_ in DL.ERRATAS_V410]   # a errata da v410 (E29, em nome proprio da gerencia c1), lida de DL
assert _ERR_NOVAS and _ERR_NOVAS[0] == "E29" and _ERR_NOVAS == ["E%d" % i_ for i_ in range(29, 29 + len(_ERR_NOVAS))], _ERR_NOVAS   # (R1: a lista vai ate' onde o delta for; E29..E32 hoje; 09/11: a E30, em nome proprio da gerencia c1: a cabeca do ramo de 5 sigma e' a leitura, nunca a palavra do livro de cobrancas; a E31: as correcoes do operador sobre a D81 e a D83)


def exige(arq, txt, marcas, ausentes=()):
    r = []
    for m in marcas:
        ok = m in txt
        r.append({"marca": m[:90], "ok": ok})
        if not ok:
            falhas.append("%s: falta a marca %r" % (arq, m[:90]))
    for m in ausentes:
        ok = m not in txt
        r.append({"ausente": m[:90], "ok": ok})
        if not ok:
            falhas.append("%s: traz o rotulo velho %r" % (arq, m[:90]))
    inv[arq] = r


exige("instalar_v410.py", INS, ["PINO_RECIBO_PRE_SELO_v410.json", "utilizavel_como_recibo_pre_selo_do_B_n", "kernel_modulos_novos_v410.json", "NOVOS_V410", "modulos_novos_v410", 'ESP["kernel"]["modulos_novos"]', 'CM["kernel"]["modulos_novos"]', "um_absoluto_selo_acom.json", "pilar_anterior_v409_",
                              "APLICADO_AO_CANONICO_%s.json", "ESPERADOS_v410.json", "CANDIDATO_v410.json", "um_v410_candidato.py", "canonical_contracts.json", 'PINO["versao_nos"] == "v409"', "base_v409", '"Testemunho"', "base_v409_sha16", 'ESP["bundle_sha256"]', "PonteDaMassa", "PontoZeroDoPsion", "CanonicalFullTGLWitnessR1",
                              'x_.startswith("TGLExt/") and x_.count("/") == 1', "raiz_v409_sha16", "audit_v409_sha16", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "ProjecaoTransversalDaMeiaNat", "Jo8v32", "tgl_kernel_proof_manifest.json", '"version") == "v409"',
                              "TetelestaiTerminal", "PIgualNP", "PsionCanto", "OIgual", "ACRESCENTA imports na raiz (um por modulo do bundle", "os 9 modulos da v407", "os 4 modulos da v408", "os 2 modulos da v409", '"TraducaoTuring", "ParNaFaceDeFock")', "[IALD2, com o NOME do modulo dado pelo operador em 06/11/2026", "bundle do fecho da v406", "a v410 traz dois modulos novos de kernel em TGLExt/", "e AEscala, com o nome do modulo", "(D87)", "IALD2 e AEscala"],   # (v410: os 4 da v408 e os 2 da v409 entre as pedras anteriores; o modulo novo, IALD2)
      ["PINO_RECIBO_PRE_SELO_v409", "kernel_modulos_novos_v409", "NOVOS_V409", "um_v409_candidato", 'ESP["pedras_sha256"]', 'PINO["versao_nos"] == "v405"', 'PINO["versao_nos"] == "v399"', 'PINO["versao_nos"] == "v398"', "base_v398", "Testemunho [nome provisorio]", "[nomes provisorios; o primeiro e' o do Codex, ORDEM 025]",
       'x_.startswith("TGLExt/F1Fecho394/")', "== 301", "o bundle de 301", "301 modulos novos", "pilar_anterior_v405", "[A ADAPTAR " + "v410]", "nove imports", "nove modulos", "PsionCanto, Par e as sete pedras de 02/11, todos de nome ratificado", "bundle do fecho da v409", "03/11/2026", "quatro imports", "os 9 modulos da v409", "04/11/2026", "o bundle de quatro modulos", "BUNDLE PEQUENO de quatro modulos",
       "os 4 modulos da v409", "os 4 da v409", "[TraducaoTuring]", "(o import da TraducaoTuring)", "05/11/2026",
       "a raiz ganha UM import", "BUNDLE PEQUENO de um modulo", "bundle de um modulo", "traz 1 modulo novo", "(o import da IALD2)", "[DECLARADO] ate a ratificacao (D63)", "o modulo novo da v410"])   # (parte 2: o bundle e' de DOIS modulos; os rotulos de um modulo ficam proibidos)   # (v410: a subida mecanica escrevera «os 4 da v409»; o modulo da v409 e a data da v409 como a desta versao)
exige("reverter_v410.py", REV, ["APLICADO_AO_CANONICO_*.json", "backup ausente ou alterado", "quarentena_bundle_", "tentativa_v410_rito_falhou_", "RECIBO_REVERSAO_", "rodada_v410_stdout.txt", "ESPERADOS_v410.json", "um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json", "modulos_novos_v410", "ESPERADOS_v409.json", "bundle_sha256",
                                'esp["kernel"]["modulos_novos"]', 'x_.startswith("TGLExt/") and x_.count("/") == 1', "(IALD2 e AEscala, em TGLExt/:"],
      ["tentativa_v409_rito_falhou_", "modulos_novos_v409", "rodada_v409_stdout", "pedras_sha256", "quarentena_pedras_", 'x_.startswith("TGLExt/F1Fecho394/")', "== 301", "o bundle de 301", "301 modulos novos", "[A ADAPTAR " + "v410]", "nove modulos", "PsionCanto, Par e as sete pedras de 02/11", "03/11/2026", "04/11/2026", "quatro modulos", "TetelestaiTerminal, TempoIgualMoeda",
       "(TraducaoTuring, em TGLExt/:", "05/11/2026", "(IALD2, em TGLExt/:", "bundle de um modulo", "BUNDLE PEQUENO de um modulo", "o modulo novo de kernel da v410", "o modulo da lista do instalador"])   # (parte 2: dois modulos)
exige("rito_v410.sh", RITO, ["echo 1 | python um.py", "trap 'religar; rm -f", "TEMPO ESPERADO (v410", "kernel_modulos_novos_v410.json", "rodada_v410_stdout.txt", ".rito_v410.pid", "ESPERADOS_v410.json", ".servidor_parado_pelo_rito", "cadeia_de_selo/v409\" \"/c/IALD/Central de Patentes/work/cadeia_de_selo/v410",
                             "%d modulo(s) novo(s) de kernel em TGLExt/" % DL.N_BUNDLE, "le as %d ancoras do axiom_report" % len(DL.ANCORAS), "le as %d ancoras do axiom_report do rito" % len(DL.ANCORAS_AESCALA), "as decisoes %s e as erratas %s e %s vao nos registros" % (DL.DECISOES_ROTULO, ", ".join(_ERR_NOVAS[:-1]), _ERR_NOVAS[-1]), "IALD2", "AEscala", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410", "%d checagens do H0DN" % DL.N_CHECKS_H0DN, "%d checagens da AEscala" % DL.N_CHECKS_AESCALA, "%d checagens do recibo HMS/13" % DL.N_CHECKS_HMS13, DL.FRASE_H0DN_OBRIGATORIA_PT, DL.FRASE_HMS13_OBRIGATORIA_PT, "a_escala_v410 (D86/D87", "h0dn_fontes_hms13_v410 (D80", "o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1", "le as %d ancoras do axiom_report do rito" % len(DL.ANCORAS),   # (os numeros do texto do rito sao os de DL: modulos do bundle, ancoras, decisoes e errata novas)
                             "iald2_v410", "cunhagens_v410", "kh_n1_cobertura_v410", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "D38/D45", "NENHUMA chave antiga muda",
                             "%d falas de 06, 07, 08, 09 e 10/11" % DL.N_FALAS_V410, "%d checagens com as instancias de brinquedo fixas" % DL.N_CHECKS_FECHO, "carimbar_stdout_v410.py",
                             "= %d s e 1 Audit = %d s" % (tempo.get("build_s", -1), tempo.get("audit_s", -1)), "a soma dos tempos por modulo e' %s s, o maximo de um modulo %s s" % (KHT.get("build_modulos_s_soma"), KHT.get("build_modulos_s_max"))],   # (o tempo do rito e' o MEDIDO em construir_marcas.txt, lido acima)
      ["rodada_v409_stdout", ".rito_v409.pid", "rito_v409", "TGLExt/Testemunho, nome PROVISORIO", "do Codex, ORDEM 025", "OS OITO registros com FUNCAO", "8 modulos novos de kernel", "301 modulos novos", "TGLExt/F1Fecho394", "CanonicalFullTGLWitnessR1", "dois imports", "k409c", "1736 s", "2016 s", "15986 s", "[A ADAPTAR " + "v410]",
                              "9 modulos novos de kernel em TGLExt/", "nove imports", "76 ancoras", "PsionCanto e Par, da gerencia c1", "the_psion_is_the_corner_on_both_faces", "D41 a D47", "E18 a E20", "o psion, o canto e o par", "carimbar_stdout_v409.py", "03/11/2026",
                              "4 modulos novos de kernel", "quatro imports", "48 ancoras", "D48 a D54", "E21 a E23", "Tetelestai e' o terminal)", "falas de 04/11", "com o PIgualNP R3",
                              "82 ancoras", "D55 a D62", "E24 a E28", "falas de 05/11", "a traducao as classes de Turing)", "05/11/2026", "o registro com FUNCAO traducao_turing_v409", "19 ancoras", "9 falas de 06/11", "15 checagens", "D63 a D70", "e a errata E29 vao", "MEDIDO em 06/11/2026", "[DECLARADO] ate a ratificacao (D63);", "= 507 s", "360 s", "1 modulo(s) novo(s)", "as 15 falas", "D63 a D77", "E29 e E30 vao", "build 507 s"])   # (09/11: os rotulos de 06/11 e os da retomada anterior, anteriores a parte 2, ficam proibidos no rito)   # (v410: o registro novo e' o iald2_v410; o da v409 e' herdado)
# sintaxe
for f in ("instalar_v410.py", "reverter_v410.py"):
    try:
        ast.parse(rd(f)); sint[f] = "ok"
    except SyntaxError as e:
        sint[f] = "ERRO: %s" % e; falhas.append("%s: %s" % (f, e))
r = subprocess.run(["sh", "-n", os.path.join(HERE, "rito_v410.sh")], capture_output=True, text=True)
sint["rito_v410.sh"] = "ok" if r.returncode == 0 else "rc=%d %s" % (r.returncode, r.stderr[:200])
if r.returncode:
    falhas.append("rito_v410.sh: sh -n rc=%d" % r.returncode)
if r.returncode == 0:
    sint["rito_v410.sh"] = "ok (sh -n rc=0)"
# (3) o trecho do instalador sobre a LISTA dos modulos novos, extraido por AST e executado isolado contra os arquivos reais
NJ = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v410.json"), encoding="utf-8"))
tree = ast.parse(INS)
stmts = list(tree.body)
i0 = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_nj")
i1 = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assert) and "algum dos modulos novos" in ast.get_source_segment(INS, n))
trecho = ast.Module(body=stmts[i0:i1 + 1], type_ignores=[])
cod = compile(ast.fix_missing_locations(trecho), "<instalar:lista_dos_modulos_novos>", "exec")


def roda_trecho(esp):
    ns = {"os": os, "json": json, "hashlib": hashlib, "HERE": HERE, "NOS": DL.NOS, "ESP": esp}
    exec(cod, ns)
    return ns["_N"], ns["NOVOS_V410"]


n_passa = lista = None
try:
    n_passa, lista = roda_trecho(ESP)
except AssertionError as e:
    falhas.append("instalar: o trecho da lista de modulos novos RECUSOU com N=%d: %s" % (DL.N_BUNDLE, e))
inv["trecho_da_lista_do_instalador"] = {"passa_com_N_igual_ao_bundle": n_passa == DL.N_BUNDLE, "n_da_lista": len(lista) if lista else None, "n_do_bundle": DL.N_BUNDLE, "esp_sintetico": ESP_REAL is None}
if n_passa != DL.N_BUNDLE:
    falhas.append("instalar: o trecho da lista nao passou com N = %d (%r)" % (DL.N_BUNDLE, n_passa))
if lista is not None and sorted(lista) != sorted(DL.BUNDLE_RELS):
    falhas.append("instalar: a lista aceita pelo trecho nao e' a de DL.BUNDLE_RELS")
# controle negativo: a lista traz um modulo que o ESPERADOS NAO pina => o trecho tem de RECUSAR (fail-closed)
_MODS = list(NJ["novos"])
for nome_ctrl, nj_ruim in (("lista_sem_um_modulo", {"novos": _MODS[:-1]}), ("modulo_que_o_ESPERADOS_nao_pina", {"novos": ["TGLExt/ModuloQueOESPERADOSNaoPina.lean"]}), ("lista_vazia", {"novos": []}), ("lista_com_dois", {"novos": _MODS + ["TGLExt/Outro.lean"]}),
                           ("modulo_no_diretorio_errado", {"novos": ["TGLExt/F1Fecho394/" + _MODS[0].split("/")[-1]] + _MODS[1:]}), ("lista_que_nao_e_lista", {"novos": "TGLExt/TraducaoTuring.lean"}), ("modulo_que_ja_esta_no_Nos", {"novos": _MODS[:-1] + ["TGLExt/Caminho.lean"]})):   # (o ultimo: a lista E o ESPERADOS pinam um modulo que o Nos JA tem -- so' a ultima asserta do trecho o pega)
    esp_c = ESP if nome_ctrl != "modulo_que_ja_esta_no_Nos" else {"kernel": {"modulos_novos": len(nj_ruim["novos"])}, "bundle_sha256": {r_: "x" * 64 for r_ in nj_ruim["novos"]}}
    ns = {"os": os, "json": type("J", (), {"load": staticmethod(lambda fh, _x=nj_ruim: copy.deepcopy(_x))}), "hashlib": hashlib, "HERE": HERE, "NOS": DL.NOS, "ESP": esp_c}
    recusou = False
    try:
        exec(cod, ns)
    except AssertionError:
        recusou = True
    inv["controle_negativo_" + nome_ctrl] = {"recusou": recusou}
    if not recusou:
        falhas.append("instalar: o trecho da lista ACEITOU %s" % nome_ctrl)
# a raiz e o Audit do Nos tem de ser os da v409 selada: a asserta do instalador e' EXTRAIDA e executada isolada contra os arquivos reais (passa) e contra um hash trocado (recusa)
CMJ = json.load(open(os.path.join(HERE, "CANDIDATO_v410.json"), encoding="utf-8"))
i_kn = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_kn")
cod_kn = compile(ast.fix_missing_locations(ast.Module(body=stmts[i_kn:i_kn + 2], type_ignores=[])), "<instalar:raiz_e_audit_do_Nos>", "exec")
h16_ = lambda b: hashlib.sha256(b).hexdigest()[:16]


def roda_kn(cm):
    exec(cod_kn, {"os": os, "NOS": DL.NOS, "CM": cm, "h16": h16_})


kn_passa = True
try:
    roda_kn(CMJ)
except AssertionError:
    kn_passa = False
_ruim = copy.deepcopy(CMJ); _ruim["kernel"]["raiz_v409_sha16"] = "0" * 16
kn_recusa = False
try:
    roda_kn(_ruim)
except AssertionError:
    kn_recusa = True
inv["raiz_e_audit_do_Nos_sao_os_da_v409"] = {"passa_com_os_hashes_do_candidato": kn_passa, "recusa_com_hash_trocado": kn_recusa}
if not (kn_passa and kn_recusa):
    falhas.append("instalar: a asserta da raiz/Audit do Nos nao passa com os hashes reais ou nao recusa o trocado")
# o reverter: a asserta da lista aceita a lista do bundle (a dos ESPERADOS) e recusa a que difere
rev_idx = re.findall(r"_lista\[0\]|NOVOS_V410\[0\]|nov\[0\]", REV) + re.findall(r"NOVOS_V410\[0\]|_NJ\[\"novos\"\]\[0\]", INS)
inv["nenhum_indice_[0]_sobre_a_lista_de_modulos"] = {"ocorrencias": rev_idx}
if rev_idx:
    falhas.append("indexa a lista de modulos novos por [0]: %s" % rev_idx)
tr = ast.parse(REV)
linha_rev = next(n for n in tr.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_lista")
asr_rev = next(n for n in tr.body if isinstance(n, ast.Assert) and "_lista" in ast.get_source_segment(REV, n) and "bundle_sha256" in ast.get_source_segment(REV, n))
mod_aplic = ast.parse("_aplic = AP.get('modulos_novos_v410') or {}").body[0]


def roda_rev(lista_ap, pedras):
    ns_rev = {"AP": {"modulos_novos_v410": {"lista": list(lista_ap)}}, "esp": {"bundle_sha256": dict(pedras), "kernel": {"modulos_novos": len(pedras)}}}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[mod_aplic, linha_rev, asr_rev], type_ignores=[])), "<reverter:lista>", "exec"), ns_rev)


ped = {p: "x" * 64 for p in NJ["novos"]}   # (so' as chaves contam: a asserta compara conjuntos de nomes)
asr_ok = True
try:
    roda_rev(NJ["novos"], ped)
except AssertionError:
    asr_ok = False
asr_neg = False
try:
    roda_rev(["TGLExt/Outro.lean"], ped)
except AssertionError:
    asr_neg = True
asr_neg_dir = False
try:
    roda_rev(["TGLExt/F1Fecho394/" + _MODS[0].split("/")[-1]] + _MODS[1:], {("TGLExt/F1Fecho394/" + _MODS[0].split("/")[-1]) if i == 0 else m_: "x" * 64 for i, m_ in enumerate(_MODS)})
except AssertionError:
    asr_neg_dir = True
inv["reverter_aceita_a_lista_do_bundle_e_recusa_a_que_difere"] = {"aceita": asr_ok, "recusa_a_que_difere": asr_neg, "recusa_modulo_fora_de_TGLExt": asr_neg_dir, "n": len(NJ["novos"])}
if not (asr_ok and asr_neg and asr_neg_dir):
    falhas.append("reverter: a asserta da lista nao aceita a lista do bundle ou nao recusa a que difere / a de modulo fora de TGLExt/")
dv = {"contrato": "DERIVACAO_v410", "executado": False, "arquivos": {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest() for f in ("instalar_v410.py", "reverter_v410.py", "rito_v410.sh")}, "invariantes": inv, "sintaxe": sint, "falhas": falhas,
      "n_modulos_novos_da_lista": len(NJ["novos"]), "tempo_build": tempo, "esp_sintetico": ESP_REAL is None,
      "nota": "[REAL] conferido por script SEM executar o instalador, o reverter nem o rito; o trecho da lista foi EXTRAIDO por AST e executado isolado" + ("; ESPERADOS_v410.json AINDA NAO EXISTIA: o trecho foi exercitado contra um ESPERADOS SINTETICO (derivado de DL.BUNDLE_POR_REL); refazer depois do gerar_esperados" if ESP_REAL is None else "")}
json.dump(dv, open(os.path.join(HERE, "DERIVACAO_v410.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("falhas:", falhas or "nenhuma", "| invariantes:", sum(len(x) if isinstance(x, list) else 1 for x in inv.values()), "| sintaxe:", sint, "| N modulos novos:", len(NJ["novos"]), "| ESPERADOS", "real" if ESP_REAL else "SINTETICO (ainda nao existe)")
sys.exit(1 if falhas else 0)
