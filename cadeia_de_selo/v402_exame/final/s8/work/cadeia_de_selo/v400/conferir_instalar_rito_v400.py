# -*- coding: utf-8 -*-
"""conferir_instalar_rito_v400.py -- confere, SEM EXECUTAR o instalador, o reverter nem o rito, os scripts instalar_v400.py, reverter_v400.py e rito_v400.sh (derivados dos da v399 por derivar_encanamento_v400.py): (1) sintaxe (ast.parse; sh -n);
(2) invariantes: cada um traz os marcadores da v400 (nomes da v400, o sidecar nos backups, o recibo pre_selo do B(n) lido do pino e a Bancada que AINDA pina a v398...) e NENHUM rotulo velho (da v399) onde seria erro;
(3) a CONDICAO DOS ZERO MODULOS NOVOS: o trecho do instalador que le kernel_modulos_novos_v400.json (a LISTA, vazia) e a confere contra ESPERADOS e contra o Nos e' EXTRAIDO por AST e EXECUTADO aqui, isolado, contra os arquivos reais (ele tem de PASSAR com N = 0 e RECUSAR se a lista tiver um modulo
que o ESPERADOS nao pina); o mesmo para a lista do reverter (sem indexar [0]); o rito so' cita a lista. Escreve DERIVACAO_v400.json. uso: python -I -B -X utf8 conferir_instalar_rito_v400.py"""
import ast, copy, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
rd = lambda p: open(os.path.join(HERE, p), "rb").read().decode("utf-8")
INS, REV, RITO = rd("instalar_v400.py"), rd("reverter_v400.py"), rd("rito_v400.sh")
ESPP = os.path.join(HERE, "ESPERADOS_v400.json")
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


exige("instalar_v400.py", INS, ["PINO_RECIBO_PRE_SELO_v400.json", "utilizavel_como_recibo_pre_selo_do_B_n", "kernel_modulos_novos_v400.json", "NOVOS_V400", "modulos_novos_v400", 'ESP["kernel"]["modulos_novos"]', "um_absoluto_selo_acom.json", "pilar_anterior_v399_",
                              "APLICADO_AO_CANONICO_%s.json", "ESPERADOS_v400.json", "CANDIDATO_v400.json", "um_v400_candidato.py", "canonical_contracts.json", 'PINO["versao_nos"] == "v398"', "base_v398", '"Testemunho"', "base_v399_sha16"],
      ["PINO_RECIBO_PRE_SELO_v399", "kernel_modulos_novos_v399", "NOVOS_V399", "um_v399_candidato", "base_v398_sha16", 'PINO["versao_nos"] == "v399"', "UM modulo novo"])
exige("reverter_v400.py", REV, ["APLICADO_AO_CANONICO_*.json", "backup ausente ou alterado", "quarentena_pedras_", "tentativa_v400_rito_falhou_", "RECIBO_REVERSAO_", "rodada_v400_stdout.txt", "ESPERADOS_v400.json", "um_absoluto_selo_acom.json", "modulos_novos_v400", "ESPERADOS_v399.json"],
      ["tentativa_v399_rito_falhou_", "modulos_novos_v399", "rodada_v399_stdout"])
exige("rito_v400.sh", RITO, ["echo 1 | python um.py", "trap 'religar; rm -f", "TEMPO ESPERADO (v400)", "kernel_modulos_novos_v400.json", "rodada_v400_stdout.txt", ".rito_v400.pid", "ESPERADOS_v400.json", ".servidor_parado_pelo_rito", "cadeia_de_selo/v399\" \"/c/IALD/Central de Patentes/work/cadeia_de_selo/v400"],
      ["rodada_v399_stdout", ".rito_v399.pid", "rito_v399", "1 modulo novo de kernel"])
# sintaxe
for f in ("instalar_v400.py", "reverter_v400.py"):
    try:
        ast.parse(rd(f)); sint[f] = "ok"
    except SyntaxError as e:
        sint[f] = "ERRO: %s" % e; falhas.append("%s: %s" % (f, e))
r = subprocess.run(["sh", "-n", os.path.join(HERE, "rito_v400.sh")], capture_output=True, text=True)
sint["rito_v400.sh"] = "ok" if r.returncode == 0 else "rc=%d %s" % (r.returncode, r.stderr[:200])
if r.returncode:
    falhas.append("rito_v400.sh: sh -n rc=%d" % r.returncode)
if r.returncode == 0:
    sint["rito_v400.sh"] = "ok (sh -n rc=0)"
# (3) o trecho do instalador sobre a LISTA dos modulos novos, extraido por AST e executado isolado contra os arquivos reais
NJ = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v400.json"), encoding="utf-8"))
tree = ast.parse(INS)
stmts = list(tree.body)
i0 = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_nj")
i1 = next(i for i, n in enumerate(stmts) if isinstance(n, ast.Assert) and "algum dos modulos novos" in ast.get_source_segment(INS, n))
trecho = ast.Module(body=stmts[i0:i1 + 1], type_ignores=[])
cod = compile(ast.fix_missing_locations(trecho), "<instalar:lista_dos_modulos_novos>", "exec")


def roda_trecho(esp):
    ns = {"os": os, "json": json, "hashlib": hashlib, "HERE": HERE, "NOS": DL.NOS, "ESP": esp}
    exec(cod, ns)
    return ns["_N"], ns["NOVOS_V400"]


n_passa = None
try:
    n_passa, lista = roda_trecho(ESP) if ESP else (None, None)
except AssertionError as e:
    falhas.append("instalar: o trecho da lista de modulos novos RECUSOU com N=0: %s" % (e,))
inv["trecho_da_lista_do_instalador"] = {"passa_com_N_igual_a_zero": n_passa == 0, "lista": lista if ESP and n_passa is not None else None}
if ESP:
    # controle negativo: a lista traz um modulo que o ESPERADOS NAO pina => o trecho tem de RECUSAR (fail-closed)
    nj_ruim = {"novos": ["TGLExt/Testemunho.lean"]}
    ns = {"os": os, "json": type("J", (), {"load": staticmethod(lambda fh: copy.deepcopy(nj_ruim))}), "hashlib": hashlib, "HERE": HERE, "NOS": DL.NOS, "ESP": ESP}
    recusou = False
    try:
        exec(cod, ns)
    except AssertionError:
        recusou = True
    inv["controle_negativo_lista_com_modulo_que_o_ESPERADOS_nao_pina"] = {"recusou": recusou}
    if not recusou:
        falhas.append("instalar: o trecho da lista ACEITOU um modulo que o ESPERADOS nao pina")
# o reverter: nada indexa a lista por [0]; a asserta tem de aceitar a lista vazia (ESPERADOS.pedras_sha256 vazio)
rev_idx = re.findall(r"_lista\[0\]|NOVOS_V400\[0\]|nov\[0\]", REV) + re.findall(r"NOVOS_V400\[0\]|_NJ\[\"novos\"\]\[0\]", INS)
inv["nenhum_indice_[0]_sobre_a_lista_de_modulos"] = {"ocorrencias": rev_idx}
if rev_idx:
    falhas.append("indexa a lista de modulos novos por [0]: %s" % rev_idx)
ns_rev = {"AP": {"modulos_novos_v400": {"lista": []}}, "esp": {"pedras_sha256": {}}}
linha_rev = next(n for n in ast.parse(REV).body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_lista")
asr_rev = next(n for n in ast.parse(REV).body if isinstance(n, ast.Assert) and "_lista" in ast.get_source_segment(REV, n) and "pedras_sha256" in ast.get_source_segment(REV, n))
asr_ok = True
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=[ast.parse("_aplic = AP.get('modulos_novos_v400') or {}").body[0], linha_rev, asr_rev], type_ignores=[])), "<reverter:lista>", "exec"), ns_rev)
except AssertionError:
    asr_ok = False
inv["reverter_aceita_a_lista_vazia"] = {"ok": asr_ok}
if not asr_ok:
    falhas.append("reverter: a asserta da lista RECUSOU a lista vazia")
tm = open(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt")) else ""
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", tm, re.M)}
tempo = {"estado": "medido", "build_s": mm.get("epoch_build_fim", 0) - mm.get("epoch_inicio", 0), "audit_s": mm.get("epoch_audit_fim", 0) - mm.get("epoch_build_fim", 0)} if mm else {"estado": "ausente"}
dv = {"contrato": "DERIVACAO_v400", "executado": False, "arquivos": {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest() for f in ("instalar_v400.py", "reverter_v400.py", "rito_v400.sh")}, "invariantes": inv, "sintaxe": sint, "falhas": falhas,
      "n_modulos_novos_da_lista": len(NJ["novos"]), "tempo_build": tempo, "nota": "[REAL] conferido por script SEM executar o instalador, o reverter nem o rito; o trecho da lista foi EXTRAIDO por AST e executado isolado"}
json.dump(dv, open(os.path.join(HERE, "DERIVACAO_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("falhas:", falhas or "nenhuma", "| invariantes:", sum(len(x) if isinstance(x, list) else 1 for x in inv.values()), "| sintaxe:", sint, "| N modulos novos:", len(NJ["novos"]))
sys.exit(1 if falhas else 0)
