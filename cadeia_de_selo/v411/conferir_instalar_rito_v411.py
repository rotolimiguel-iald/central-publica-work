# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] ESCRITO a partir do molde v410/conferir_instalar_rito_v410.py para uma versao SEM modulo novo: as marcas da v411 (a lista VAZIA de modulos novos, a raiz e o Audit que NAO mudam, os 2 modulos da v410 como pedras anteriores, o registro h0dn_bg1_v411, a recusa do modo de ensaio), o tempo MEDIDO do k411c, e os trechos do instalador e do reverter EXTRAIDOS por AST e exercitados (a lista vazia passa; um modulo a mais recusa)
"""conferir_instalar_rito_v411.py -- confere, SEM EXECUTAR o instalador, o reverter nem o rito, os scripts instalar_v411.py, reverter_v411.py e rito_v411.sh (derivados dos da v410; para a versao sem modulo novo, do molde v400): (1) sintaxe
(ast.parse; sh -n); (2) invariantes: cada um traz as marcas da v411 (o pacote, o ESPERADOS e o CANDIDATO da v411, o recibo pre_selo do B(n) lido do pino, a Bancada que JA pina a v410, a raiz e o Audit da v410 conferidos e que NAO mudam,
a lista VAZIA de modulos novos, os 2 modulos da v410 -- IALD2 e AEscala -- entre as pedras anteriores, a recusa do modo de ensaio do topo proposto) e NAO traz os rotulos velhos; o rito traz os numeros MEDIDOS em kernel/construir_marcas.txt
(lidos do arquivo, nunca digitados); (3) a CONDICAO DO MODULO NOVO (NENHUM): o trecho do instalador que monta a lista (de ESPERADOS.bundle_sha256) e a confere contra kernel.modulos_novos do ESPERADOS e do CANDIDATO e' EXTRAIDO por AST e EXECUTADO aqui,
isolado: tem de PASSAR com a lista VAZIA e RECUSAR se o ESPERADOS pinar um modulo, disser um modulo, o CANDIDATO disser um modulo ou houver bandeira nova; o mesmo para a asserta da raiz e do Audit (passa com os hashes do ESPERADOS contra o Nos
real; recusa com um hash trocado) e para a lista do reverter (aceita a lista vazia; recusa um modulo). Se o ESPERADOS_v411.json ainda NAO existe, os trechos sao exercitados contra um ESPERADOS SINTETICO (dito na saida). Escreve
DERIVACAO_v411.json em DL.saida (no ensaio do topo proposto, fora de work\\). uso: python -I -B -X utf8 conferir_instalar_rito_v411.py"""
import ast, copy, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
rd = lambda p: open(os.path.join(HERE, p), "rb").read().decode("utf-8")
INS, REV, RITO = rd("instalar_v411.py"), rd("reverter_v411.py"), rd("rito_v411.sh")
ESPP = DL.saida("ESPERADOS_v411.json")
ESP_REAL = json.load(open(ESPP, encoding="utf-8")) if os.path.exists(ESPP) else None
_F = json.load(open(DL.FORMAL_MAP_ARQ, encoding="utf-8"))
ESP = ESP_REAL if ESP_REAL else {"kernel": {"modulos_novos": 0, "raiz_sha16": _F["TGLExt.lean"][:16], "audit_sha16": _F["TGL/Audit.lean"][:16]}, "bundle_sha256": {}, "n_bandeiras_novas": 0}   # (sintetico so' para exercitar os trechos; dito na saida)
CMJ = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8"))
falhas, inv, sint = [], {}, {}
# o TEMPO medido (kernel/construir_marcas.txt): lido ANTES, porque o rito tem de traze-lo
tm = open(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt")) else ""
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", tm, re.M)}
tempo = {"estado": "medido", "build_s": mm.get("epoch_build_fim", 0) - mm.get("epoch_inicio", 0), "audit_s": mm.get("epoch_audit_fim", 0) - mm.get("epoch_audit_inicio", mm.get("epoch_build_fim", 0))} if mm else {"estado": "ausente"}
if tempo["estado"] != "medido" or tempo["build_s"] <= 0 or tempo["audit_s"] <= 0:
    falhas.append("kernel/construir_marcas.txt sem as marcas de tempo do build e do Audit: %r" % (tempo,))
KHT = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, DL.KH_N1_INSUMO), encoding="utf-8"))
if tempo.get("estado") == "medido" and (KHT.get("duracao_build_s") != tempo["build_s"] or KHT.get("duracao_audit_s") != tempo["audit_s"]):
    falhas.append("o tempo das marcas (build %s s, Audit %s s) difere do KH_N1_v411.json (build %s s, Audit %s s)" % (tempo["build_s"], tempo["audit_s"], KHT.get("duracao_build_s"), KHT.get("duracao_audit_s")))
if KHT.get("n_modulos_novos") != 0:
    falhas.append("o KH_N1_v411.json diz %r modulos novos; a v411 nao tem modulo novo" % (KHT.get("n_modulos_novos"),))
_DEC = sorted(DL.DECISOES_V411, key=lambda k_: int(k_[1:])); _ERR = list(DL.ERRATAS_IDS_V411)
assert _DEC[0] == "D159" and _DEC[-1] == "D181" and _ERR == ["E41", "E42", "E43", "E44"], (_DEC, _ERR)   # (ordem da gerencia c1 de 12/11: a faixa vai de D159 a D181 (a D181 e' a da conversa interna, noite); as erratas E41 a E44; antes, D173 e E43)


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


_MARCA_ADAPTAR = "[A ADAPTAR " + "v411]"
exige("instalar_v411.py", INS, ["PINO_RECIBO_PRE_SELO_v411.json", "utilizavel_como_recibo_pre_selo_do_B_n", "NOVOS_V411", "modulos_novos_v411", 'ESP["kernel"]["modulos_novos"]', 'CM["kernel"]["modulos_novos"]', 'ESP["n_bandeiras_novas"]', "um_absoluto_selo_acom.json", "pilar_anterior_v410_",
                                "APLICADO_AO_CANONICO_%s.json", "ESPERADOS_v411.json", "CANDIDATO_v411.json", "um_v411_candidato.py", "canonical_contracts.json", 'PINO["versao_nos"] == "v410"', "base_v410_sha16", 'ESP["bundle_sha256"]', 'ESP["bundle_v410_sha256"]', '"IALD2", "AEscala")',
                                "PonteDaMassa", "PontoZeroDoPsion", "CanonicalFullTGLWitnessR1", "TetelestaiTerminal", "PIgualNP", "PsionCanto", "OIgual", '"TraducaoTuring", "ParNaFaceDeFock"', "tgl_kernel_proof_manifest.json", '"version") == "v410"',
                                '_kn["raiz_sha16"]', '_kn["audit_sha16"]', "V411_ENSAIO_TOPO_PROPOSTO", "TOPO_RATIFICADO_v411.json", "a v411 NAO traz modulo novo"],
      ["PINO_RECIBO_PRE_SELO_v410", "kernel_modulos_novos_v41", "NOVOS_V410", "um_v410_candidato", 'PINO["versao_nos"] == "v409"', "base_v409", "pilar_anterior_v409", _MARCA_ADAPTAR, "ACRESCENTA imports na raiz", "raiz_v409_sha16", "audit_v409_sha16", "ESPERADOS_v410.json", "CANDIDATO_v410.json"])
exige("reverter_v411.py", REV, ["APLICADO_AO_CANONICO_*.json", "backup ausente ou alterado", "quarentena_bundle_", "tentativa_v411_rito_falhou_", "RECIBO_REVERSAO_", "rodada_v411_stdout.txt", "ESPERADOS_v411.json", "um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json",
                                "modulos_novos_v411", '"v410", "ESPERADOS_v410.json"', 'esp["kernel"]["modulos_novos"] == 0', "V411_ENSAIO_TOPO_PROPOSTO"],
      ["tentativa_v410_rito_falhou_", "modulos_novos_v410", "rodada_v410_stdout", _MARCA_ADAPTAR, "(IALD2 e AEscala, em TGLExt/:", "ESPERADOS_v409.json"])
exige("rito_v411.sh", RITO, ["echo 1 | python um.py", "trap 'religar; rm -f", "TEMPO ESPERADO (v411", "rodada_v411_stdout.txt", ".rito_v411.pid", "ESPERADOS_v411.json", ".servidor_parado_pelo_rito", 'cadeia_de_selo/v410" "/c/IALD/Central de Patentes/work/cadeia_de_selo/v411',
                             "NENHUM modulo novo de kernel", "h0dn_bg1_v411", "cunhagens_v411", "kh_n1_cobertura_v411", "D38/D45", "NENHUMA chave antiga muda", "%d falas de 11 e 12/11" % DL.N_FALAS_V411, "%d checagens" % DL.N_CHECKS_FECHO,
                             "as decisoes %s a %s e as erratas %s e %s vao nos registros" % (_DEC[0], _DEC[-1], ", ".join(_ERR[:-1]), _ERR[-1]), "carimbar_stdout_v411.py", "o executor da abertura do H0DN NUNCA roda",
                             "= %d s e 1 Audit = %d s" % (tempo.get("build_s", -1), tempo.get("audit_s", -1)), "a soma dos tempos por modulo e' %s s, o maximo de um modulo %s s" % (KHT.get("build_modulos_s_soma"), KHT.get("build_modulos_s_max"))],
      ["rodada_v410_stdout", ".rito_v410.pid", "rito_v410", "k410c", _MARCA_ADAPTAR, "carimbar_stdout_v410.py", "611 s", "2 modulo(s) novo(s)", "(o BUNDLE PEQUENO", "iald2_v410 (chamado"])
for f in ("instalar_v411.py", "reverter_v411.py"):
    try:
        ast.parse(rd(f)); sint[f] = "ok"
    except SyntaxError as e:
        sint[f] = "ERRO: %s" % e; falhas.append("%s: %s" % (f, e))
r = subprocess.run(["sh", "-n", os.path.join(HERE, "rito_v411.sh")], capture_output=True, text=True)
sint["rito_v411.sh"] = "ok (sh -n rc=0)" if r.returncode == 0 else "rc=%d %s" % (r.returncode, r.stderr[:200])
if r.returncode:
    falhas.append("rito_v411.sh: sh -n rc=%d" % r.returncode)
# (3) o trecho do instalador sobre a LISTA (VAZIA) dos modulos novos, extraido por AST e executado isolado
tree = ast.parse(INS); stmts = list(tree.body)
i0 = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assign) and any(isinstance(t_, ast.Tuple) and any(isinstance(e_, ast.Name) and e_.id == "NOVOS_V411" for e_ in t_.elts) or (isinstance(t_, ast.Name) and t_.id == "NOVOS_V411") for t_ in n.targets))
i1 = next(i for i, n in enumerate(stmts) if i > i0 and isinstance(n, ast.Assert) and "nao tem modulo novo" in ast.get_source_segment(INS, n))
cod = compile(ast.fix_missing_locations(ast.Module(body=stmts[i0:i1 + 1], type_ignores=[])), "<instalar:lista_dos_modulos_novos>", "exec")


def roda_trecho(esp, cm):
    ns = {"os": os, "json": json, "hashlib": hashlib, "HERE": HERE, "NOS": DL.NOS, "ESP": esp, "CM": cm}
    exec(cod, ns)
    return ns["_N"], ns["NOVOS_V411"]


n_passa = lista = None
try:
    n_passa, lista = roda_trecho(ESP, CMJ)
except AssertionError as e:
    falhas.append("instalar: o trecho da lista de modulos novos RECUSOU a lista VAZIA: %s" % e)
inv["trecho_da_lista_do_instalador"] = {"passa_com_a_lista_vazia": n_passa == 0 and lista == [], "esp_sintetico": ESP_REAL is None}
if not (n_passa == 0 and lista == []):
    falhas.append("instalar: o trecho da lista nao passou com a lista VAZIA (%r, %r)" % (n_passa, lista))
for nome_ctrl, esp_c, cm_c in (("o_ESPERADOS_pina_um_modulo", dict(ESP, bundle_sha256={"TGLExt/ModuloNovo.lean": "x" * 64}, kernel=dict(ESP["kernel"], modulos_novos=1)), CMJ),
                               ("o_ESPERADOS_diz_um_modulo_sem_pinar", dict(ESP, kernel=dict(ESP["kernel"], modulos_novos=1)), CMJ),
                               ("o_CANDIDATO_diz_um_modulo", ESP, dict(CMJ, kernel=dict(CMJ["kernel"], modulos_novos=1))),
                               ("uma_bandeira_nova", dict(ESP, n_bandeiras_novas=1), CMJ)):
    recusou = False
    try:
        roda_trecho(esp_c, cm_c)
    except AssertionError:
        recusou = True
    inv["controle_negativo_" + nome_ctrl] = {"recusou": recusou}
    if not recusou:
        falhas.append("instalar: o trecho da lista ACEITOU %s" % nome_ctrl)
# a raiz e o Audit do Nos tem de ser os da v410 selada (== os do candidato): a asserta do instalador e' EXTRAIDA e executada isolada contra os arquivos reais (passa) e contra um hash trocado (recusa)
i_kn = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_kn")
cod_kn = compile(ast.fix_missing_locations(ast.Module(body=stmts[i_kn:i_kn + 2], type_ignores=[])), "<instalar:raiz_e_audit_do_Nos>", "exec")
h16_ = lambda b: hashlib.sha256(b).hexdigest()[:16]


def roda_kn(esp):
    exec(cod_kn, {"os": os, "NOS": DL.NOS, "ESP": esp, "h16": h16_})


kn_passa = True
try:
    roda_kn(ESP)
except AssertionError:
    kn_passa = False
_ruim = copy.deepcopy(ESP); _ruim["kernel"]["raiz_sha16"] = "0" * 16
kn_recusa = False
try:
    roda_kn(_ruim)
except AssertionError:
    kn_recusa = True
inv["raiz_e_audit_do_Nos_sao_os_da_v410"] = {"passa_com_os_hashes_do_ESPERADOS": kn_passa, "recusa_com_hash_trocado": kn_recusa, "raiz_sha16": ESP["kernel"]["raiz_sha16"], "audit_sha16": ESP["kernel"]["audit_sha16"]}
if not (kn_passa and kn_recusa):
    falhas.append("instalar: a asserta da raiz/Audit do Nos nao passa com os hashes reais ou nao recusa o trocado")
# o reverter: a asserta da lista aceita a lista VAZIA (a dos ESPERADOS) e recusa a que traz um modulo
tr = ast.parse(REV)
linha_rev = next(n for n in tr.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_lista")
asr_rev = next(n for n in tr.body if isinstance(n, ast.Assert) and "_lista" in ast.get_source_segment(REV, n) and "bundle_sha256" in ast.get_source_segment(REV, n))
mod_aplic = ast.parse("_aplic = AP.get('modulos_novos_v411') or {}").body[0]


def roda_rev(lista_ap, pedras):
    ns_rev = {"AP": {"modulos_novos_v411": {"lista": list(lista_ap)}}, "esp": {"bundle_sha256": dict(pedras), "kernel": {"modulos_novos": len(pedras)}}}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[mod_aplic, linha_rev, asr_rev], type_ignores=[])), "<reverter:lista>", "exec"), ns_rev)


asr_ok = True
try:
    roda_rev([], {})
except AssertionError:
    asr_ok = False
asr_neg = False
try:
    roda_rev(["TGLExt/Outro.lean"], {"TGLExt/Outro.lean": "x" * 64})
except AssertionError:
    asr_neg = True
asr_neg2 = False
try:
    roda_rev([], {"TGLExt/Outro.lean": "x" * 64})
except AssertionError:
    asr_neg2 = True
inv["reverter_aceita_a_lista_vazia_e_recusa_um_modulo"] = {"aceita_a_vazia": asr_ok, "recusa_a_lista_com_um_modulo": asr_neg, "recusa_o_ESPERADOS_que_pina_um_modulo": asr_neg2}
if not (asr_ok and asr_neg and asr_neg2):
    falhas.append("reverter: a asserta da lista nao aceita a lista vazia ou nao recusa a que traz modulo")
rev_idx = re.findall(r"_lista\[0\]|NOVOS_V411\[0\]|nov\[0\]", REV + INS)
inv["nenhum_indice_[0]_sobre_a_lista_de_modulos"] = {"ocorrencias": rev_idx}
if rev_idx:
    falhas.append("indexa a lista de modulos novos por [0]: %s" % rev_idx)
dv = {"contrato": "DERIVACAO_v411", "executado": False, "arquivos": {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest() for f in ("instalar_v411.py", "reverter_v411.py", "rito_v411.sh")}, "invariantes": inv, "sintaxe": sint, "falhas": falhas,
      "n_modulos_novos_da_lista": 0, "tempo_build": tempo, "esp_sintetico": ESP_REAL is None,
      "nota": "[REAL] conferido por script SEM executar o instalador, o reverter nem o rito; os trechos da lista, da raiz/Audit e do reverter foram EXTRAIDOS por AST e executados isolados" + ("; ESPERADOS_v411.json AINDA NAO EXISTIA: os trechos foram exercitados contra um ESPERADOS SINTETICO (lista vazia; raiz e Audit do FORMAL_MAP); refazer depois do gerar_esperados" if ESP_REAL is None else ""),
      **DL.MARCA_ENSAIO}
_dp = DL.saida("DERIVACAO_v411.json")
open(_dp + ".tmp", "w", encoding="utf-8").write(json.dumps(dv, ensure_ascii=False, indent=1)); os.replace(_dp + ".tmp", _dp)
print("falhas:", falhas or "nenhuma", "| invariantes:", sum(len(x) if isinstance(x, list) else 1 for x in inv.values()), "| sintaxe:", sint, "| N modulos novos: 0 | ESPERADOS", "real" if ESP_REAL else "SINTETICO (ainda nao existe)")
sys.exit(1 if falhas else 0)
