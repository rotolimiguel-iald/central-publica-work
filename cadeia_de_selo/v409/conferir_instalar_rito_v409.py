# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] confere instalar/reverter/rito da v409 sem executar: marcas do bundle de dois modulos, do registro traducao_turing_v409, D55-D62/E24-E28 e a E21 lidas do delta, o tempo medido; o trecho da lista extraido por AST
"""conferir_instalar_rito_v409.py -- confere, SEM EXECUTAR o instalador, o reverter nem o rito, os scripts instalar_v409.py, reverter_v409.py e rito_v409.sh (derivados dos da v408, adaptados em 05/11/2026 ao BUNDLE PEQUENO de um modulo em TGLExt/, com as licoes da v408): (1) sintaxe (ast.parse; sh -n);
(2) invariantes: cada um traz os marcadores da v409 (nomes da v409, o sidecar nos backups, o recibo pre_selo do B(n) lido do pino, a Bancada que JA pina a v408, a raiz e o Audit da v408 conferidos antes de instalar, o modulo em TGLExt/, nao em TGLExt/F1Fecho394/...; as pedras anteriores incluem os 9 modulos da v407 e os 4 da v408) e NENHUM rotulo velho onde seria erro; o TEMPO ESPERADO do rito
traz os numeros MEDIDOS em kernel/construir_marcas.txt (lidos do arquivo, nunca digitados);
(3) a CONDICAO DO MODULO NOVO (UM): o trecho do instalador que le kernel_modulos_novos_v409.json (a LISTA, de DL.N_BUNDLE elementos: o bundle) e a confere contra ESPERADOS.bundle_sha256 e contra o Nos e' EXTRAIDO por AST e EXECUTADO aqui, isolado, contra os arquivos reais (ele tem de PASSAR com N = DL.N_BUNDLE e RECUSAR se a lista tiver um modulo
que o ESPERADOS nao pina, estiver vazia, tiver um a mais, tiver um a menos ou apontar para fora de TGLExt/); o mesmo para a lista do reverter (aceita a lista do bundle; recusa a que difere dos ESPERADOS); o rito so cita a lista. Se o ESPERADOS_v409.json ainda NAO existe (gerar_esperados_v409.py nao rodou), o trecho e' exercitado contra um ESPERADOS SINTETICO derivado de DL.BUNDLE_POR_REL
(kernel.modulos_novos e bundle_sha256), dito na saida e em DERIVACAO_v409.json (`esp_sintetico`); o ESPERADOS real e' o que vale e e' conferido na corrida seguinte. Escreve DERIVACAO_v409.json. uso: python -I -B -X utf8 conferir_instalar_rito_v409.py"""
import ast, copy, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v409 as DL  # noqa: E402
rd = lambda p: open(os.path.join(HERE, p), "rb").read().decode("utf-8")
INS, REV, RITO = rd("instalar_v409.py"), rd("reverter_v409.py"), rd("rito_v409.sh")
ESPP = os.path.join(HERE, "ESPERADOS_v409.json")
ESP_REAL = json.load(open(ESPP, encoding="utf-8")) if os.path.exists(ESPP) else None
ESP = ESP_REAL if ESP_REAL else {"kernel": {"modulos_novos": DL.N_BUNDLE}, "bundle_sha256": {r: DL.BUNDLE_POR_REL[r]["sha256"] for r in DL.BUNDLE_RELS}}   # (sintetico so' para exercitar o trecho; dito na saida)
falhas, inv, sint = [], {}, {}
# o TEMPO medido (kernel/construir_marcas.txt): lido ANTES, porque o rito tem de traze-lo
tm = open(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt")) else ""
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", tm, re.M)}
tempo = {"estado": "medido", "build_s": mm.get("epoch_build_fim", 0) - mm.get("epoch_inicio", 0), "audit_s": mm.get("epoch_audit_fim", 0) - mm.get("epoch_audit_inicio", mm.get("epoch_build_fim", 0))} if mm else {"estado": "ausente"}   # (v409: o Audit refeito depois da queda de energia mede a propria rodada, como no pos_build)
if tempo["estado"] != "medido" or tempo["build_s"] <= 0 or tempo["audit_s"] <= 0:
    falhas.append("kernel/construir_marcas.txt sem as marcas de tempo do build e do Audit: %r" % (tempo,))


_DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D8.DECISOES), key=lambda k_: int(k_[1:]))   # as decisoes que a v409 acrescenta (D55..D62), lidas de DL (a diferenca contra o delta da v408)
assert _DEC_NOVAS and _DEC_NOVAS[0] == "D55" and _DEC_NOVAS[-1] == "D62", _DEC_NOVAS
_ERR_NOVAS = [e_.split(" --")[0] for e_ in DL.ERRATAS_V409]   # as erratas da v409 (E24..E28 e a E21 ao lado), lidas de DL
assert _ERR_NOVAS == ["E24", "E25", "E26", "E27", "E28", "E21"], _ERR_NOVAS
_ERR_SEQ = [e_ for e_ in _ERR_NOVAS if e_ != "E21"]   # a sequencia nova (E24 a E28); a E21 vai AO LADO da errata selada da v408


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


exige("instalar_v409.py", INS, ["PINO_RECIBO_PRE_SELO_v409.json", "utilizavel_como_recibo_pre_selo_do_B_n", "kernel_modulos_novos_v409.json", "NOVOS_V409", "modulos_novos_v409", 'ESP["kernel"]["modulos_novos"]', 'CM["kernel"]["modulos_novos"]', "um_absoluto_selo_acom.json", "pilar_anterior_v408_",
                              "APLICADO_AO_CANONICO_%s.json", "ESPERADOS_v409.json", "CANDIDATO_v409.json", "um_v409_candidato.py", "canonical_contracts.json", 'PINO["versao_nos"] == "v408"', "base_v408", '"Testemunho"', "base_v408_sha16", 'ESP["bundle_sha256"]', "PonteDaMassa", "PontoZeroDoPsion", "CanonicalFullTGLWitnessR1",
                              'x_.startswith("TGLExt/") and x_.count("/") == 1', "raiz_v408_sha16", "audit_v408_sha16", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "ProjecaoTransversalDaMeiaNat", "Jo8v32", "tgl_kernel_proof_manifest.json", '"version") == "v408"',
                              "TetelestaiTerminal", "PIgualNP", "PsionCanto", "OIgual", "um import na raiz", "os 9 modulos da v407", "os 4 modulos da v408", "TraducaoTuring", "bundle do fecho da v406"],
      ["PINO_RECIBO_PRE_SELO_v408", "kernel_modulos_novos_v408", "NOVOS_V408", "um_v408_candidato", 'ESP["pedras_sha256"]', 'PINO["versao_nos"] == "v405"', 'PINO["versao_nos"] == "v399"', 'PINO["versao_nos"] == "v398"', "base_v398", "Testemunho [nome provisorio]", "[nomes provisorios; o primeiro e' o do Codex, ORDEM 025]",
       'x_.startswith("TGLExt/F1Fecho394/")', "== 301", "o bundle de 301", "301 modulos novos", "pilar_anterior_v405", "[A ADAPTAR " + "v409]", "nove imports", "nove modulos", "PsionCanto, Par e as sete pedras de 02/11, todos de nome ratificado", "bundle do fecho da v408", "03/11/2026", "quatro imports", "os 9 modulos da v408", "04/11/2026", "o bundle de quatro modulos", "BUNDLE PEQUENO de quatro modulos"])
exige("reverter_v409.py", REV, ["APLICADO_AO_CANONICO_*.json", "backup ausente ou alterado", "quarentena_bundle_", "tentativa_v409_rito_falhou_", "RECIBO_REVERSAO_", "rodada_v409_stdout.txt", "ESPERADOS_v409.json", "um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json", "modulos_novos_v409", "ESPERADOS_v408.json", "bundle_sha256",
                                'esp["kernel"]["modulos_novos"]', 'x_.startswith("TGLExt/") and x_.count("/") == 1'],
      ["tentativa_v408_rito_falhou_", "modulos_novos_v408", "rodada_v408_stdout", "pedras_sha256", "quarentena_pedras_", 'x_.startswith("TGLExt/F1Fecho394/")', "== 301", "o bundle de 301", "301 modulos novos", "[A ADAPTAR " + "v409]", "nove modulos", "PsionCanto, Par e as sete pedras de 02/11", "03/11/2026", "04/11/2026", "quatro modulos", "TetelestaiTerminal, TempoIgualMoeda"])
exige("rito_v409.sh", RITO, ["echo 1 | python um.py", "trap 'religar; rm -f", "TEMPO ESPERADO (v409", "kernel_modulos_novos_v409.json", "rodada_v409_stdout.txt", ".rito_v409.pid", "ESPERADOS_v409.json", ".servidor_parado_pelo_rito", "cadeia_de_selo/v408\" \"/c/IALD/Central de Patentes/work/cadeia_de_selo/v409",
                             "%d modulo(s) novo(s) de kernel em TGLExt/" % DL.N_BUNDLE, "le as %d ancoras do axiom_report" % len(DL.ANCORAS), "%s a %s e as erratas %s a %s e a E21 ao lado" % (_DEC_NOVAS[0], _DEC_NOVAS[-1], _ERR_SEQ[0], _ERR_SEQ[-1]), "ParNaFaceDeFock",   # (os numeros do texto do rito sao os de DL: modulos do bundle, ancoras, decisoes e erratas novas)
                             "traducao_turing_v409", "TraducaoTuring", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "E26", "D38/D45", "NENHUMA chave antiga muda", "%d falas de 05/11" % DL.N_FALAS_V409, "%d checagens" % DL.N_CHECKS_FECHO, "carimbar_stdout_v409.py",
                             "= %d s e 1 Audit = %d s" % (tempo.get("build_s", -1), tempo.get("audit_s", -1))],   # (o tempo do rito e' o MEDIDO em construir_marcas.txt, lido acima)
      ["rodada_v408_stdout", ".rito_v408.pid", "rito_v408", "TGLExt/Testemunho, nome PROVISORIO", "do Codex, ORDEM 025", "OS OITO registros com FUNCAO", "8 modulos novos de kernel", "301 modulos novos", "TGLExt/F1Fecho394", "CanonicalFullTGLWitnessR1", "dois imports", "k408c", "1736 s", "2016 s", "15986 s", "[A ADAPTAR " + "v409]",
                              "9 modulos novos de kernel em TGLExt/", "nove imports", "76 ancoras", "PsionCanto e Par, da gerencia c1", "the_psion_is_the_corner_on_both_faces", "D41 a D47", "E18 a E20", "o psion, o canto e o par", "carimbar_stdout_v408.py", "03/11/2026",
                              "4 modulos novos de kernel", "quatro imports", "48 ancoras", "D48 a D54", "E21 a E23", "Tetelestai e' o terminal)", "falas de 04/11", "com o PIgualNP R3"])
# sintaxe
for f in ("instalar_v409.py", "reverter_v409.py"):
    try:
        ast.parse(rd(f)); sint[f] = "ok"
    except SyntaxError as e:
        sint[f] = "ERRO: %s" % e; falhas.append("%s: %s" % (f, e))
r = subprocess.run(["sh", "-n", os.path.join(HERE, "rito_v409.sh")], capture_output=True, text=True)
sint["rito_v409.sh"] = "ok" if r.returncode == 0 else "rc=%d %s" % (r.returncode, r.stderr[:200])
if r.returncode:
    falhas.append("rito_v409.sh: sh -n rc=%d" % r.returncode)
if r.returncode == 0:
    sint["rito_v409.sh"] = "ok (sh -n rc=0)"
# (3) o trecho do instalador sobre a LISTA dos modulos novos, extraido por AST e executado isolado contra os arquivos reais
NJ = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v409.json"), encoding="utf-8"))
tree = ast.parse(INS)
stmts = list(tree.body)
i0 = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_nj")
i1 = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assert) and "algum dos modulos novos" in ast.get_source_segment(INS, n))
trecho = ast.Module(body=stmts[i0:i1 + 1], type_ignores=[])
cod = compile(ast.fix_missing_locations(trecho), "<instalar:lista_dos_modulos_novos>", "exec")


def roda_trecho(esp):
    ns = {"os": os, "json": json, "hashlib": hashlib, "HERE": HERE, "NOS": DL.NOS, "ESP": esp}
    exec(cod, ns)
    return ns["_N"], ns["NOVOS_V409"]


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
# a raiz e o Audit do Nos tem de ser os da v408 selada: a asserta do instalador e' EXTRAIDA e executada isolada contra os arquivos reais (passa) e contra um hash trocado (recusa)
CMJ = json.load(open(os.path.join(HERE, "CANDIDATO_v409.json"), encoding="utf-8"))
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
_ruim = copy.deepcopy(CMJ); _ruim["kernel"]["raiz_v408_sha16"] = "0" * 16
kn_recusa = False
try:
    roda_kn(_ruim)
except AssertionError:
    kn_recusa = True
inv["raiz_e_audit_do_Nos_sao_os_da_v408"] = {"passa_com_os_hashes_do_candidato": kn_passa, "recusa_com_hash_trocado": kn_recusa}
if not (kn_passa and kn_recusa):
    falhas.append("instalar: a asserta da raiz/Audit do Nos nao passa com os hashes reais ou nao recusa o trocado")
# o reverter: a asserta da lista aceita a lista do bundle (a dos ESPERADOS) e recusa a que difere
rev_idx = re.findall(r"_lista\[0\]|NOVOS_V409\[0\]|nov\[0\]", REV) + re.findall(r"NOVOS_V409\[0\]|_NJ\[\"novos\"\]\[0\]", INS)
inv["nenhum_indice_[0]_sobre_a_lista_de_modulos"] = {"ocorrencias": rev_idx}
if rev_idx:
    falhas.append("indexa a lista de modulos novos por [0]: %s" % rev_idx)
tr = ast.parse(REV)
linha_rev = next(n for n in tr.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_lista")
asr_rev = next(n for n in tr.body if isinstance(n, ast.Assert) and "_lista" in ast.get_source_segment(REV, n) and "bundle_sha256" in ast.get_source_segment(REV, n))
mod_aplic = ast.parse("_aplic = AP.get('modulos_novos_v409') or {}").body[0]


def roda_rev(lista_ap, pedras):
    ns_rev = {"AP": {"modulos_novos_v409": {"lista": list(lista_ap)}}, "esp": {"bundle_sha256": dict(pedras), "kernel": {"modulos_novos": len(pedras)}}}
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
dv = {"contrato": "DERIVACAO_v409", "executado": False, "arquivos": {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest() for f in ("instalar_v409.py", "reverter_v409.py", "rito_v409.sh")}, "invariantes": inv, "sintaxe": sint, "falhas": falhas,
      "n_modulos_novos_da_lista": len(NJ["novos"]), "tempo_build": tempo, "esp_sintetico": ESP_REAL is None,
      "nota": "[REAL] conferido por script SEM executar o instalador, o reverter nem o rito; o trecho da lista foi EXTRAIDO por AST e executado isolado" + ("; ESPERADOS_v409.json AINDA NAO EXISTIA: o trecho foi exercitado contra um ESPERADOS SINTETICO (derivado de DL.BUNDLE_POR_REL); refazer depois do gerar_esperados" if ESP_REAL is None else "")}
json.dump(dv, open(os.path.join(HERE, "DERIVACAO_v409.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("falhas:", falhas or "nenhuma", "| invariantes:", sum(len(x) if isinstance(x, list) else 1 for x in inv.values()), "| sintaxe:", sint, "| N modulos novos:", len(NJ["novos"]), "| ESPERADOS", "real" if ESP_REAL else "SINTETICO (ainda nao existe)")
sys.exit(1 if falhas else 0)
