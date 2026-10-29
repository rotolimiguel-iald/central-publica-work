# -*- coding: utf-8 -*-
"""conferir_instalar_rito_v404.py -- confere, SEM EXECUTAR o instalador, o reverter nem o rito, os scripts instalar_v404.py, reverter_v404.py e rito_v404.sh (derivados dos da v399, a cadeia de CONTEUDO, por derivar_encanamento_v404.py, com as licoes da v403): (1) sintaxe (ast.parse; sh -n);
(2) invariantes: cada um traz os marcadores da v404 (nomes da v404, o sidecar nos backups, o recibo pre_selo do B(n) lido do pino e a Bancada que JA pina a v403...) e NENHUM rotulo velho onde seria erro;
(3) a CONDICAO DO MODULO NOVO (UM): o trecho do instalador que le kernel_modulos_novos_v404.json (a LISTA, de dois elementos) e a confere contra ESPERADOS e contra o Nos e' EXTRAIDO por AST e EXECUTADO aqui, isolado, contra os arquivos reais (ele tem de PASSAR com N = 3 e RECUSAR se a lista tiver um modulo
que o ESPERADOS nao pina); o mesmo para a lista do reverter (aceita a lista de dois elementos; recusa a que difere dos ESPERADOS); o rito so' cita a lista. Escreve DERIVACAO_v404.json. uso: python -I -B -X utf8 conferir_instalar_rito_v404.py"""
import ast, copy, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v404 as DL  # noqa: E402
rd = lambda p: open(os.path.join(HERE, p), "rb").read().decode("utf-8")
INS, REV, RITO = rd("instalar_v404.py"), rd("reverter_v404.py"), rd("rito_v404.sh")
ESPP = os.path.join(HERE, "ESPERADOS_v404.json")
ESP = json.load(open(ESPP, encoding="utf-8")) if os.path.exists(ESPP) else None
falhas, inv, sint = [], {}, {}


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


exige("instalar_v404.py", INS, ["PINO_RECIBO_PRE_SELO_v404.json", "utilizavel_como_recibo_pre_selo_do_B_n", "kernel_modulos_novos_v404.json", "NOVOS_V404", "modulos_novos_v404", 'ESP["kernel"]["modulos_novos"]', "um_absoluto_selo_acom.json", "pilar_anterior_v403_",
                              "APLICADO_AO_CANONICO_%s.json", "ESPERADOS_v404.json", "CANDIDATO_v404.json", "um_v404_candidato.py", "canonical_contracts.json", 'PINO["versao_nos"] == "v403"', "base_v403", '"Testemunho"', "base_v403_sha16", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "Caminho, Vida e VerdadeAdendo", '"version") == "v403"'],
      ["PINO_RECIBO_PRE_SELO_v403", "kernel_modulos_novos_v403", "NOVOS_V403", "um_v403_candidato", 'PINO["versao_nos"] == "v399"', 'PINO["versao_nos"] == "v398"', "base_v398", "Testemunho [nome provisorio]", "[nomes provisorios; o primeiro e' o do Codex, ORDEM 025]"])
exige("reverter_v404.py", REV, ["APLICADO_AO_CANONICO_*.json", "backup ausente ou alterado", "quarentena_pedras_", "tentativa_v404_rito_falhou_", "RECIBO_REVERSAO_", "rodada_v404_stdout.txt", "ESPERADOS_v404.json", "um_absoluto_selo_acom.json", "modulos_novos_v404", "ESPERADOS_v403.json"],
      ["tentativa_v403_rito_falhou_", "modulos_novos_v403", "rodada_v403_stdout"])
exige("rito_v404.sh", RITO, ["echo 1 | python um.py", "trap 'religar; rm -f", "TEMPO ESPERADO (v404", "kernel_modulos_novos_v404.json", "rodada_v404_stdout.txt", ".rito_v404.pid", "ESPERADOS_v404.json", ".servidor_parado_pelo_rito", "cadeia_de_selo/v403\" \"/c/IALD/Central de Patentes/work/cadeia_de_selo/v404", "TGLExt/ProjecaoTransversalDaMeiaNat", "TGLExt/Jo8v32"],
      ["rodada_v403_stdout", ".rito_v403.pid", "rito_v403", "TGLExt/Testemunho, nome PROVISORIO", "do Codex, ORDEM 025"])
# sintaxe
for f in ("instalar_v404.py", "reverter_v404.py"):
    try:
        ast.parse(rd(f)); sint[f] = "ok"
    except SyntaxError as e:
        sint[f] = "ERRO: %s" % e; falhas.append("%s: %s" % (f, e))
r = subprocess.run(["sh", "-n", os.path.join(HERE, "rito_v404.sh")], capture_output=True, text=True)
sint["rito_v404.sh"] = "ok" if r.returncode == 0 else "rc=%d %s" % (r.returncode, r.stderr[:200])
if r.returncode:
    falhas.append("rito_v404.sh: sh -n rc=%d" % r.returncode)
if r.returncode == 0:
    sint["rito_v404.sh"] = "ok (sh -n rc=0)"
# (3) o trecho do instalador sobre a LISTA dos modulos novos, extraido por AST e executado isolado contra os arquivos reais
NJ = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v404.json"), encoding="utf-8"))
tree = ast.parse(INS)
stmts = list(tree.body)
i0 = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_nj")
i1 = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assert) and "algum dos modulos novos" in ast.get_source_segment(INS, n))
trecho = ast.Module(body=stmts[i0:i1 + 1], type_ignores=[])
cod = compile(ast.fix_missing_locations(trecho), "<instalar:lista_dos_modulos_novos>", "exec")


def roda_trecho(esp):
    ns = {"os": os, "json": json, "hashlib": hashlib, "HERE": HERE, "NOS": DL.NOS, "ESP": esp}
    exec(cod, ns)
    return ns["_N"], ns["NOVOS_V404"]


n_passa = lista = None
try:
    n_passa, lista = roda_trecho(ESP) if ESP else (None, None)
except AssertionError as e:
    falhas.append("instalar: o trecho da lista de modulos novos RECUSOU com N=2: %s" % (e,))
inv["trecho_da_lista_do_instalador"] = {"passa_com_N_igual_a_dois": n_passa == 2, "lista": lista if ESP and n_passa is not None else None}
if ESP and n_passa != 2:
    falhas.append("instalar: o trecho da lista nao passou com N = 2 (%r)" % (n_passa,))
if ESP:
    # controle negativo: a lista traz um modulo que o ESPERADOS NAO pina => o trecho tem de RECUSAR (fail-closed)
    for nome_ctrl, nj_ruim in (("modulo_que_o_ESPERADOS_nao_pina", {"novos": ["TGLExt/Testemunho.lean"]}), ("lista_vazia", {"novos": []}), ("lista_com_dois", {"novos": list(NJ["novos"]) + ["TGLExt/Outro.lean"]})):
        ns = {"os": os, "json": type("J", (), {"load": staticmethod(lambda fh, _x=nj_ruim: copy.deepcopy(_x))}), "hashlib": hashlib, "HERE": HERE, "NOS": DL.NOS, "ESP": ESP}
        recusou = False
        try:
            exec(cod, ns)
        except AssertionError:
            recusou = True
        inv["controle_negativo_" + nome_ctrl] = {"recusou": recusou}
        if not recusou:
            falhas.append("instalar: o trecho da lista ACEITOU %s" % nome_ctrl)
# o reverter: a asserta da lista aceita a lista de um elemento (a dos ESPERADOS) e recusa a que difere
rev_idx = re.findall(r"_lista\[0\]|NOVOS_V404\[0\]|nov\[0\]", REV) + re.findall(r"NOVOS_V404\[0\]|_NJ\[\"novos\"\]\[0\]", INS)
inv["nenhum_indice_[0]_sobre_a_lista_de_modulos"] = {"ocorrencias": rev_idx}
if rev_idx:
    falhas.append("indexa a lista de modulos novos por [0]: %s" % rev_idx)
tr = ast.parse(REV)
linha_rev = next(n for n in tr.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_lista")
asr_rev = next(n for n in tr.body if isinstance(n, ast.Assert) and "_lista" in ast.get_source_segment(REV, n) and "pedras_sha256" in ast.get_source_segment(REV, n))
mod_aplic = ast.parse("_aplic = AP.get('modulos_novos_v404') or {}").body[0]


def roda_rev(lista_ap, pedras):
    ns_rev = {"AP": {"modulos_novos_v404": {"lista": list(lista_ap)}}, "esp": {"pedras_sha256": dict(pedras)}}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[mod_aplic, linha_rev, asr_rev], type_ignores=[])), "<reverter:lista>", "exec"), ns_rev)


ped = {p: "x" * 64 for p in NJ["novos"]}
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
inv["reverter_aceita_a_lista_de_um_elemento_e_recusa_a_que_difere"] = {"aceita": asr_ok, "recusa_a_que_difere": asr_neg}
if not (asr_ok and asr_neg):
    falhas.append("reverter: a asserta da lista nao aceita a lista de um elemento ou nao recusa a que difere")
tm = open(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt")) else ""
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", tm, re.M)}
tempo = {"estado": "medido", "build_s": mm.get("epoch_build_fim", 0) - mm.get("epoch_inicio", 0), "audit_s": mm.get("epoch_audit_fim", 0) - mm.get("epoch_build_fim", 0)} if mm else {"estado": "ausente"}
dv = {"contrato": "DERIVACAO_v404", "executado": False, "arquivos": {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest() for f in ("instalar_v404.py", "reverter_v404.py", "rito_v404.sh")}, "invariantes": inv, "sintaxe": sint, "falhas": falhas,
      "n_modulos_novos_da_lista": len(NJ["novos"]), "tempo_build": tempo, "nota": "[REAL] conferido por script SEM executar o instalador, o reverter nem o rito; o trecho da lista foi EXTRAIDO por AST e executado isolado"}
json.dump(dv, open(os.path.join(HERE, "DERIVACAO_v404.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("falhas:", falhas or "nenhuma", "| invariantes:", sum(len(x) if isinstance(x, list) else 1 for x in inv.values()), "| sintaxe:", sint, "| N modulos novos:", len(NJ["novos"]))
sys.exit(1 if falhas else 0)
