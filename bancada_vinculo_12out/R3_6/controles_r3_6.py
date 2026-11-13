# -*- coding: utf-8 -*-
"""controles_r3_6.py (R3.6, 13/11/2026) -- a conferencia POR SCRIPT do conserto R3.6 do elo B(n) (sincronizar_bancada.py): o contrato novo KERNEL_RECIBO_R3_6, o da VERSAO SEM PEDRA NOVA.
Carrega os DOIS modulos (R3_5 e R3_6) por importlib e confere, SEM gravar nada na Bancada nem no Nos (tudo em memoria ou em copias numa pasta temporaria propria, desfeita no fim):
  1. CONFINAMENTO por AST: toda funcao/classe de nivel de modulo e' identica (ast.dump) nas duas revisoes, exceto verificar_kernel_recibo; as atribuicoes de nivel de modulo sao identicas exceto REVISAO,
     KERNEL_CONTRATOS_ADMITIDOS e a constante nova KERNEL_CONTRATO_R3_6; dentro de verificar_kernel_recibo nenhum comando da R3.5 sumiu (so' 3 foram reescritos: o docstring, a recusa `pedras vazias` e o
     pino.update) e todo texto de recusa da R3.5 segue no codigo da R3.6;
  2. DIFERENCIAL no caminho antigo: as duas revisoes devolvem o MESMO par (passa, detalhe) para o recibo REAL da v410 e para dezenas de mutacoes dele (em copias; a contagem exata esta no JSON); a unica diferenca admitida e' a chave
     `versao_sem_pedra_nova` posta num recibo R3_2/R3_4 (a R3.5 a ignora; a R3.6 recusa);
  3. CAMINHO NOVO com os insumos REAIS da v411 (o recibo novo, o Nos, CRITERIOS_v411.json, o recibo pre-selo da falha): o POSITIVO passa e cada NEGATIVO e' recusado PELO MOTIVO esperado (o trecho do detalhe e' conferido).
Todo o resto da suite de 596 controles da R3.5 NAO e' re-rodado aqui (limite dito no RESULTADO_R3_6.md). uso: C:\\Python314\\python.exe -I -B -X utf8 controles_r3_6.py   (grava CONTROLES_R3_6.json ao lado)"""
import sys
sys.dont_write_bytecode = True
import ast, copy, datetime, difflib, hashlib, importlib.util, json, os, re, shutil, tempfile
from pathlib import Path
assert sys.flags.isolated and sys.flags.dont_write_bytecode and sys.flags.utf8_mode, "rode com python -I -B -X utf8"

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
SRC5, SRC6 = BASE / "R3_5" / "sincronizar_bancada.py", AQUI / "sincronizar_bancada.py"
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
CADEIA = BASE.parent / "cadeia_de_selo"
V410, V411 = CADEIA / "v410", CADEIA / "v411"
SAIDA = AQUI / "CONTROLES_R3_6.json"
sha_b = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: Path(p).read_bytes()


def carregar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M5, M6 = carregar("sync_r3_5", SRC5), carregar("sync_r3_6", SRC6)
assert M5.REVISAO.startswith("R3.5") and M6.REVISAO.startswith("R3.6"), (M5.REVISAO, M6.REVISAO)
TMP = Path(tempfile.mkdtemp(prefix="r36_ctl_"))
_contador = [0]
RESULT = {"revisao_dos_controles": "R3.6 (13/11/2026)", "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "interpretador": sys.executable,
          "flags": {"isolated": sys.flags.isolated, "dont_write_bytecode": sys.flags.dont_write_bytecode, "utf8_mode": sys.flags.utf8_mode},
          "modulos": {"R3_5": {"path": str(SRC5), "sha256": sha_b(rd(SRC5)), "bytes": len(rd(SRC5)), "REVISAO": M5.REVISAO}, "R3_6": {"path": str(SRC6), "sha256": sha_b(rd(SRC6)), "bytes": len(rd(SRC6)), "REVISAO": M6.REVISAO}},
          "nada_gravado_na_bancada_nem_no_nos": True}


def cabeca(t, n=260):
    t = str(t).replace("\n", " ")
    return t if len(t) <= n else t[:n] + "..."


# ============================================================================================ 1. CONFINAMENTO por AST
def nomes_alvo(n):
    if isinstance(n, ast.Assign):
        alvos = n.targets
    else:
        alvos = [n.target]
    out = []
    for a in alvos:
        out.append(",".join(sorted(x.id for x in ast.walk(a) if isinstance(x, ast.Name))) or ast.dump(a))
    return "|".join(out)


def blocos(src):
    arv = ast.parse(src)
    corpo = list(arv.body)
    doc = None
    if corpo and isinstance(corpo[0], ast.Expr) and isinstance(getattr(corpo[0], "value", None), ast.Constant) and isinstance(corpo[0].value.value, str):
        doc = corpo[0].value.value
        corpo = corpo[1:]
    defs, atrib, outros = {}, {}, []
    for n in corpo:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            k = n.name
            while k in defs:
                k += "#"
            defs[k] = (ast.dump(n), n.lineno)
        elif isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            k = nomes_alvo(n)
            while k in atrib:
                k += "#"
            atrib[k] = (ast.dump(n), n.lineno)
        else:
            outros.append((ast.dump(n), n.lineno, type(n).__name__))
    return arv, doc, defs, atrib, outros


def confinamento():
    s5, s6 = SRC5.read_text(encoding="utf-8"), SRC6.read_text(encoding="utf-8")
    a5, doc5, d5, t5, o5 = blocos(s5)
    a6, doc6, d6, t6, o6 = blocos(s6)
    dif_defs = sorted(k for k in set(d5) | set(d6) if (d5.get(k) or (None,))[0] != (d6.get(k) or (None,))[0])
    dif_atrib = sorted(k for k in set(t5) | set(t6) if (t5.get(k) or (None,))[0] != (t6.get(k) or (None,))[0])
    outros_iguais = [x[0] for x in o5] == [x[0] for x in o6]
    esperado_defs, esperado_atrib = ["verificar_kernel_recibo"], sorted(["REVISAO", "KERNEL_CONTRATOS_ADMITIDOS", "KERNEL_CONTRATO_R3_6"])
    nomes_iguais = (sorted(d5) == sorted(d6))
    # dentro da funcao que muda: nenhum comando da R3.5 some; so' 3 sao reescritos
    f5 = next(n for n in a5.body if isinstance(n, ast.FunctionDef) and n.name == "verificar_kernel_recibo")
    f6 = next(n for n in a6.body if isinstance(n, ast.FunctionDef) and n.name == "verificar_kernel_recibo")
    b5, b6 = [ast.dump(s) for s in f5.body], [ast.dump(s) for s in f6.body]
    sm = difflib.SequenceMatcher(None, b5, b6, autojunk=False)
    ops, reescritos_r35, so_removidos = [], [], 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        antigos = [{"linha_r3_5": f5.body[i].lineno, "comando": cabeca(ast.unparse(f5.body[i]), 110)} for i in range(i1, i2)]
        novos = [{"linha_r3_6": f6.body[j].lineno, "comando": cabeca(ast.unparse(f6.body[j]), 110)} for j in range(j1, j2)]
        ops.append({"op": tag, "r3_5": antigos, "r3_6": novos})
        if tag == "delete":
            so_removidos += i2 - i1
        reescritos_r35 += [ast.unparse(f5.body[i]).split("\n")[0] for i in range(i1, i2)]
    esperados_reescritos = 3
    eh_doc = lambda s: s.startswith(("'", '"'))
    n_doc = sum(1 for s in reescritos_r35 if eh_doc(s))
    n_pedras_if = sum(1 for s in reescritos_r35 if s.startswith("if not isinstance(pedras, list) or not pedras:"))
    n_pino = sum(1 for s in reescritos_r35 if s.startswith("pino.update("))
    # todo texto de recusa da R3.5 (as constantes de texto da funcao) segue no codigo da R3.6
    cs5 = {n.value for n in ast.walk(f5) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    cs6 = {n.value for n in ast.walk(f6) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    sumiram = sorted(cs5 - cs6)
    so_o_docstring = (len(sumiram) == 1 and sumiram[0] == ast.get_docstring(f5, clean=False))
    novos_textos = sorted(cs6 - cs5)
    ped_vazias_unica = (s5.count('return falha("pedras vazias")') == 1 and s6.count('return falha("pedras vazias")') == 1)
    linhas_doc = {nome: [l for l in (doc or "").split("\n") if re.match(r"\s*import\b", l)] for nome, doc in (("R3_5", doc5), ("R3_6", doc6))}
    linhas_doc_f = [l for l in (ast.get_docstring(f6, clean=False) or "").split("\n") if re.match(r"\s*import\b", l)]
    u = list(difflib.unified_diff(s5.split("\n"), s6.split("\n"), lineterm="", n=0))
    add = sum(1 for l in u if l.startswith("+") and not l.startswith("+++"))
    rem = sum(1 for l in u if l.startswith("-") and not l.startswith("---"))
    ok = (nomes_iguais and dif_defs == esperado_defs and dif_atrib == esperado_atrib and outros_iguais and so_removidos == 0 and (n_doc, n_pedras_if, n_pino) == (1, 1, 1)
          and len(reescritos_r35) == esperados_reescritos and so_o_docstring and ped_vazias_unica and not linhas_doc["R3_6"] and not linhas_doc_f)
    return {"ok": ok, "mesmos_nomes_de_funcao_e_classe": nomes_iguais,
            "funcoes_ou_classes_que_diferem": dif_defs, "esperado": esperado_defs,
            "atribuicoes_de_nivel_de_modulo_que_diferem": dif_atrib, "esperado_atrib": esperado_atrib,
            "demais_comandos_de_topo_identicos": outros_iguais, "docstring_do_modulo_difere": doc5 != doc6,
            "dentro_de_verificar_kernel_recibo": {"comandos_r3_5": len(f5.body), "comandos_r3_6": len(f6.body), "comandos_da_r3_5_removidos_sem_substituto": so_removidos,
                                                  "comandos_da_r3_5_reescritos": len(reescritos_r35), "docstring": n_doc, "recusa_pedras_vazias_agora_elif": n_pedras_if, "pino_update": n_pino, "operacoes": ops},
            "textos_da_r3_5_que_sumiram_da_funcao": [cabeca(x, 80) for x in sumiram], "so_o_docstring_da_funcao_sumiu": so_o_docstring, "textos_novos_na_r3_6": len(novos_textos),
            "recusa_pedras_vazias_presente_uma_vez_em_cada": ped_vazias_unica,
            "linhas_do_docstring_que_comecam_por_import": {"modulo_R3_6": linhas_doc["R3_6"], "funcao_R3_6": linhas_doc_f},
            "diff_unificado_linhas": {"acrescentadas": add, "removidas": rem}}


RESULT["confinamento"] = confinamento()
print("confinamento:", RESULT["confinamento"]["ok"], flush=True)

# ============================================================================================ insumos reais
nos_info = M6.ler_nos(str(NOS), "v411")
RESULT["nos_hoje"] = {"dir": str(NOS), "um_py_sha256": nos_info["um_py"]["sha256"], "selo_sha256": nos_info["selo"]["sha256"], "selo_um_version": nos_info["selo"]["um_version"],
                      "manifesto_do_kernel_sha256": nos_info["kernel"]["sha256"], "impressao_formal": nos_info["kernel"]["impressao_formal"], "n_formal_files": nos_info["kernel"]["n_formal_files"]}


def criterios_de(caminho, versao):
    raw = rd(caminho)
    return M6.carregar_criterios(Path(caminho), sha_b(raw), versao)


def gravar(obj, nome):
    _contador[0] += 1
    p = TMP / ("%03d_%s.json" % (_contador[0], nome))
    p.write_bytes(json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"))
    return p


def flip(h):
    return h[:-1] + ("0" if h[-1] != "0" else "1")


def chamar(M, kp, versao, ni, sha_esp, rps, sandbox, cr):
    r = M.verificar_kernel_recibo(kp, versao, ni, sha_esp, rps, sandbox, cr)
    return bool(r[0]), r[1], r[2]


# ---------------------------------------------------------------------------- v410 (o recibo REAL do caminho antigo)
K410 = V410 / "kernel" / "KERNEL_RECIBO_v410.json"
D410 = json.loads(rd(K410).decode("utf-8"))
CR410 = criterios_de(V410 / "vinculo" / "CRITERIOS_v410.json", "v410")
REC410_APLICAR = json.loads(rd(V410 / "bancada_B3" / "RECIBO_SINCRONIZACAO_v410_20261111_022226.json").decode("utf-8"))
RPS410 = {"kernel_anterior": REC410_APLICAR["recibo_pre_selo"]["kernel_anterior"]}
SHA410 = sha_b(rd(K410))
# ---------------------------------------------------------------------------- v411 (o recibo NOVO)
K411 = V411 / "kernel" / "KERNEL_RECIBO_v411.json"
D411 = json.loads(rd(K411).decode("utf-8"))
CR411 = criterios_de(V411 / "vinculo" / "CRITERIOS_v411.json", "v411")
FALHA = json.loads(rd(V411 / "bancada_B3_ensaio_20261113_023032" / "RECIBO_SINCRONIZACAO_v411_20261113_023032.json").decode("utf-8"))
RPS411 = {"kernel_anterior": FALHA["recibo_pre_selo"]["kernel_anterior"]}
SHA411 = sha_b(rd(K411))
RESULT["insumos"] = {"recibo_v410": {"path": str(K410), "sha256": SHA410, "contrato": D410["contrato"]}, "criterios_v410": {"path": CR410["path"], "sha256": CR410["sha256"]},
                     "recibo_pre_selo_da_v410": "kernel_anterior lido de bancada_B3\\RECIBO_SINCRONIZACAO_v410_20261111_022226.json (aplicar)",
                     "recibo_v411": {"path": str(K411), "sha256": SHA411, "contrato": D411["contrato"], "versao_sem_pedra_nova": D411.get("versao_sem_pedra_nova")},
                     "criterios_v411": {"path": CR411["path"], "sha256": CR411["sha256"]},
                     "recibo_pre_selo_da_v411": "kernel_anterior lido do recibo da falha bancada_B3_ensaio_20261113_023032\\RECIBO_SINCRONIZACAO_v411_20261113_023032.json"}

# ============================================================================================ 2. DIFERENCIAL no caminho antigo
DIF = []


def dif_caso(nome, rec, sha_esp=None, rps=RPS410, sandbox=True, cr=CR410, versao="v410", relacao="IGUAL", trecho=None, quer_passa=None):
    """as duas revisoes sobre o MESMO recibo e os MESMOS argumentos. relacao: IGUAL (mesmo par) ou ADMITIDA_R35_PASSA_R36_RECUSA (a unica diferenca admitida)."""
    kp = rec if isinstance(rec, Path) else gravar(rec, nome)
    p5, d5, _ = chamar(M5, kp, versao, nos_info, sha_esp, rps, sandbox, cr)
    p6, d6, pino6 = chamar(M6, kp, versao, nos_info, sha_esp, rps, sandbox, cr)
    if relacao == "IGUAL":
        ok = (p5 == p6 and d5 == d6)
        if quer_passa is not None:
            ok = ok and (p6 is quer_passa)
        if trecho is not None:
            ok = ok and (trecho in d6)
    else:
        ok = (p5 is True and p6 is False and "versao_sem_pedra_nova" in d6 and "so existe no contrato KERNEL_RECIBO_R3_6" in d6 and "R3.6" in d6)
    DIF.append({"nome": nome, "relacao_esperada": relacao, "r3_5": {"passa": p5, "detalhe": cabeca(d5)}, "r3_6": {"passa": p6, "detalhe": cabeca(d6)}, "mesmo_par": (p5 == p6 and d5 == d6), "ok": ok,
                "pino_r3_6_versao_sem_pedra_nova": (pino6 or {}).get("versao_sem_pedra_nova") if p6 else None})
    print("dif", nome, ok, "" if ok else (cabeca(d5, 150) + " || " + cabeca(d6, 150)), flush=True)


def mut(fn, base=None):
    d = copy.deepcopy(base if base is not None else D410)
    fn(d)
    return d


def _pedra_flip(d):
    d["pedras"][0]["sha256"] = flip(d["pedras"][0]["sha256"])


def _tc(d):
    d["toolchain"]["lean_version"][0] += " x"


def _crit(d):
    d["criterios"]["j1_declaracoes"]["medido"] += 1


def _fa_sha(d):
    c = next(k for k in sorted(d["formal_files_antes"]) if k.startswith("TGLExt/") and k.endswith(".lean"))
    d["formal_files_antes"][c] = flip(d["formal_files_antes"][c])


dif_caso("v410_real_positivo_sha_e_pre_selo", K410, sha_esp=SHA410, sandbox=False, quer_passa=True)
dif_caso("v410_real_positivo_sandbox", K410, quer_passa=True)
dif_caso("pedras_vazias", mut(lambda d: d.__setitem__("pedras", [])), trecho="pedras vazias", quer_passa=False)
dif_caso("uma_pedra_a_menos", mut(lambda d: d.__setitem__("pedras", d["pedras"][:-1])), quer_passa=False)
dif_caso("sha_de_pedra_trocado", mut(_pedra_flip), quer_passa=False)
dif_caso("raiz_sha256_depois_trocado", mut(lambda d: d["raiz"].__setitem__("sha256_depois", flip(d["raiz"]["sha256_depois"]))), quer_passa=False)
dif_caso("audit_sha256_depois_trocado", mut(lambda d: d["audit"].__setitem__("sha256_depois", flip(d["audit"]["sha256_depois"]))), quer_passa=False)
dif_caso("sorry_1", mut(lambda d: d.__setitem__("sorry", 1)), quer_passa=False)
dif_caso("erros_1", mut(lambda d: d.__setitem__("erros", 1)), quer_passa=False)
dif_caso("rc_1", mut(lambda d: d.__setitem__("rc", 1)), quer_passa=False)
dif_caso("sem_formal_files_antes", mut(lambda d: d.pop("formal_files_antes")), trecho="sem os campos", quer_passa=False)
dif_caso("sem_nos_kernel_impressao", mut(lambda d: d.pop("nos_kernel_impressao")), trecho="sem os campos", quer_passa=False)
dif_caso("formal_files_antes_sha_trocado", mut(_fa_sha), quer_passa=False)
dif_caso("nos_kernel_impressao_depois_trocado", mut(lambda d: d["nos_kernel_impressao"].__setitem__("depois", flip(d["nos_kernel_impressao"]["depois"]))), quer_passa=False)
dif_caso("nos_kernel_impressao_antes_trocado", mut(lambda d: d["nos_kernel_impressao"].__setitem__("antes", flip(d["nos_kernel_impressao"]["antes"]))), quer_passa=False)
dif_caso("toolchain_trocada", mut(_tc), quer_passa=False)
dif_caso("toolchain_sem_lake_version", mut(lambda d: d["toolchain"].pop("lake_version")), quer_passa=False)
dif_caso("criterio_trocado", mut(_crit), quer_passa=False)
dif_caso("contrato_desconhecido", mut(lambda d: d.__setitem__("contrato", "KERNEL_RECIBO_R9")), trecho="contrato=", quer_passa=False)
dif_caso("chave_proibida_um_py_sha256", mut(lambda d: d.__setitem__("um_py_sha256", "0" * 64)), trecho="PROIBIDOS", quer_passa=False)
dif_caso("versao_do_recibo_errada", mut(lambda d: d.__setitem__("versao", "v409")), trecho="e da versao", quer_passa=False)
dif_caso("arvore_com_juncao_o_sandbox_do_build", mut(lambda d: d.__setitem__("arvore", "C:/t/k411c/final")), quer_passa=False)
dif_caso("modulos_de_auditoria_no_R3_2", mut(lambda d: d.__setitem__("modulos_de_auditoria", [d["pedras"][0]["path"]])), quer_passa=False)
dif_caso("contrato_R3_4_do_mesmo_recibo", mut(lambda d: d.__setitem__("contrato", "KERNEL_RECIBO_R3_4")), quer_passa=True)
dif_caso("sha_esperado_errado", K410, sha_esp="0" * 64, quer_passa=False)
dif_caso("sem_sha_e_sem_sandbox", K410, sandbox=False, quer_passa=False)
dif_caso("sem_recibo_pre_selo_e_sem_sandbox", K410, sha_esp=SHA410, rps=None, sandbox=False, quer_passa=False)
dif_caso("recibo_pre_selo_de_outro_kernel", K410, rps={"kernel_anterior": dict(RPS410["kernel_anterior"], impressao_formal=flip(RPS410["kernel_anterior"]["impressao_formal"]))}, quer_passa=False)
dif_caso("sem_criterios", K410, cr=None, quer_passa=False)
dif_caso("criterios_com_x19_trocado", K410, cr=dict(CR410, x19="sim"), quer_passa=False)
dif_caso("versao_do_alvo_errada", K410, versao="v411", quer_passa=False)
dif_caso("recibo_ausente", TMP / "nao_existe.json", quer_passa=False)
# a unica diferenca admitida: a chave versao_sem_pedra_nova num recibo que NAO e do contrato novo (a R3.5 a ignora; a R3.6 recusa)
dif_caso("ADMITIDA_chave_true_no_R3_2", mut(lambda d: d.__setitem__("versao_sem_pedra_nova", True)), relacao="ADMITIDA_R35_PASSA_R36_RECUSA")
dif_caso("ADMITIDA_chave_false_no_R3_2", mut(lambda d: d.__setitem__("versao_sem_pedra_nova", False)), relacao="ADMITIDA_R35_PASSA_R36_RECUSA")
dif_caso("ADMITIDA_chave_true_no_R3_4", mut(lambda d: d.update(contrato="KERNEL_RECIBO_R3_4", versao_sem_pedra_nova=True)), relacao="ADMITIDA_R35_PASSA_R36_RECUSA")
RESULT["diferencial_no_caminho_antigo"] = {"n": len(DIF), "n_ok": sum(1 for c in DIF if c["ok"]), "n_mesmo_par": sum(1 for c in DIF if c["mesmo_par"]),
                                           "n_diferem_admitidos": sum(1 for c in DIF if not c["mesmo_par"] and c["relacao_esperada"] != "IGUAL"),
                                           "n_diferem_nao_admitidos": sum(1 for c in DIF if not c["mesmo_par"] and c["relacao_esperada"] == "IGUAL"),
                                           "n_passa_nas_duas": sum(1 for c in DIF if c["r3_5"]["passa"] and c["r3_6"]["passa"]), "casos": DIF}

# ============================================================================================ 3. CAMINHO NOVO (insumos reais da v411)
NEG, POS = [], []
RAIZ_FA = ("TGLExt.lean", "TGL/Audit.lean")


def imp_de(fa):
    return M6.impressao_formal(fa)


def m411(fn):
    d = copy.deepcopy(D411)
    fn(d)
    return d


def nos_com(fn):
    ni = dict(nos_info)
    ni["_kernel_man"] = copy.deepcopy(nos_info["_kernel_man"])
    fn(ni["_kernel_man"]["formal_files_sha256"])
    return ni


def pos_caso(nome, rec, sha_esp="AUTO", rps=RPS411, sandbox=False, cr=CR411, versao="v411", ni=None, exige=()):
    kp = rec if isinstance(rec, Path) else gravar(rec, nome)
    sha_esp = sha_b(rd(kp)) if sha_esp == "AUTO" else sha_esp
    passa, det, pino = chamar(M6, kp, versao, ni or nos_info, sha_esp, rps, sandbox, cr)
    ok = passa and all(t in det for t in exige) and (pino or {}).get("versao_sem_pedra_nova") is True and "kernel_igual_ao_anterior" in (pino or {})
    POS.append({"nome": nome, "esperado": "PASSA", "obtido": "PASSA" if passa else "RECUSA", "ok": ok, "detalhe": cabeca(det, 700),
                "pino": {k: (pino or {}).get(k) for k in ("versao_sem_pedra_nova", "kernel_igual_ao_anterior", "antes")} if passa else None})
    print("pos", nome, ok, "" if ok else cabeca(det, 300), flush=True)


def neg_caso(nome, rec, trecho, sha_esp="AUTO", rps=RPS411, sandbox=False, cr=CR411, versao="v411", ni=None, modulo=None):
    M = modulo or M6
    kp = rec if isinstance(rec, Path) else gravar(rec, nome)
    sha_esp = sha_b(rd(kp)) if sha_esp == "AUTO" else sha_esp
    passa, det, _ = chamar(M, kp, versao, ni or nos_info, sha_esp, rps, sandbox, cr)
    ok = (not passa) and (trecho in det)
    NEG.append({"nome": nome, "esperado": "RECUSA com o trecho %r" % trecho, "obtido": "PASSA" if passa else "RECUSA", "motivo_confere": (trecho in det), "ok": ok, "detalhe": cabeca(det, 420)})
    print("neg", nome, ok, "" if ok else cabeca(det, 300), flush=True)


def recalc_antes(d, fa):
    d["formal_files_antes"] = fa
    d["nos_kernel_impressao"]["antes"] = d["nos_kernel_impressao"]["depois"] = imp_de(fa)


def log_copia(campo, fn_texto, nome):
    p = Path(D411[campo]["path"])
    texto = rd(p).decode("utf-8")
    novo = fn_texto(texto)
    assert novo != texto, ("a mutacao do log nao mudou nada", nome)
    q = TMP / ("%s_%s.log" % (campo, nome))
    q.write_bytes(novo.encode("utf-8"))
    return q


def sem_job_do_modulo(texto, modulo):
    n = [0]

    def rep(m):
        if m.group(1) == modulo:
            n[0] += 1
            return m.group(0).replace("Replayed", "Seen").replace("Built", "Seen")
        return m.group(0)
    novo = M6.RE_LAKE_JOB.sub(rep, texto)
    assert n[0] >= 1, ("o job do modulo nao esta no log", modulo)
    return novo


def rec_com_log(campo, q):
    def f(d):
        d[campo]["path"] = str(q).replace("\\", "/")
        d[campo]["sha256"] = sha_b(rd(q))
    return m411(f)


# --- o POSITIVO e variantes positivas
pos_caso("v411_real_sha_pinado_e_pre_selo_da_falha", K411, exige=("VERSAO SEM PEDRA NOVA", "49403b07f4e0ffae", "1764 arquivos formais", "TGL.Audit"))
pos_caso("v411_real_em_sandbox_sem_pre_selo_e_sem_sha", K411, sha_esp=None, rps=None, sandbox=True, exige=("VERSAO SEM PEDRA NOVA", "ANTES nao cruzado"))

# --- NEGATIVOS: o recibo e o contrato
neg_caso("uma_pedra_inventada", m411(lambda d: d.__setitem__("pedras", [{"path": "TGLExt/Inventada.lean", "sha256": "1" * 64, "declaracoes": ["TGLExt.Inventada.x"]}])), "pedras tem de ser a lista VAZIA")
neg_caso("pedras_nao_e_lista", m411(lambda d: d.__setitem__("pedras", None)), "pedras tem de ser a lista VAZIA")
neg_caso("sem_versao_sem_pedra_nova", m411(lambda d: d.pop("versao_sem_pedra_nova")), "exige versao_sem_pedra_nova=true")
neg_caso("versao_sem_pedra_nova_false", m411(lambda d: d.__setitem__("versao_sem_pedra_nova", False)), "exige versao_sem_pedra_nova=true")
neg_caso("versao_sem_pedra_nova_int_1", m411(lambda d: d.__setitem__("versao_sem_pedra_nova", 1)), "exige versao_sem_pedra_nova=true")
neg_caso("versao_sem_pedra_nova_texto_true", m411(lambda d: d.__setitem__("versao_sem_pedra_nova", "true")), "exige versao_sem_pedra_nova=true")
neg_caso("modulos_de_auditoria_lista_vazia", m411(lambda d: d.__setitem__("modulos_de_auditoria", [])), "nao tem modulos_de_auditoria")
neg_caso("modulos_de_auditoria_com_um_caminho", m411(lambda d: d.__setitem__("modulos_de_auditoria", ["TGLExt/Auditoria.lean"])), "nao tem modulos_de_auditoria")
neg_caso("raiz_antes_diferente_de_depois", m411(lambda d: d["raiz"].__setitem__("sha256_antes", flip(d["raiz"]["sha256_antes"]))), "versao sem pedra nova: raiz.sha256_antes")
neg_caso("audit_antes_diferente_de_depois", m411(lambda d: d["audit"].__setitem__("sha256_antes", flip(d["audit"]["sha256_antes"]))), "versao sem pedra nova: audit.sha256_antes")
neg_caso("raiz_antes_e_depois_trocados_juntos", m411(lambda d: d["raiz"].update(sha256_antes=flip(d["raiz"]["sha256_antes"]), sha256_depois=flip(d["raiz"]["sha256_depois"]))), "formal_files_sha256 do manifesto pinado pelo selo")
neg_caso("contrato_R3_2_com_a_chave_nova", m411(lambda d: d.__setitem__("contrato", "KERNEL_RECIBO_R3_2")), "so existe no contrato KERNEL_RECIBO_R3_6")
neg_caso("contrato_R3_4_com_a_chave_nova", m411(lambda d: d.__setitem__("contrato", "KERNEL_RECIBO_R3_4")), "so existe no contrato KERNEL_RECIBO_R3_6")
neg_caso("contrato_R3_2_sem_a_chave_pedras_vazias", m411(lambda d: (d.__setitem__("contrato", "KERNEL_RECIBO_R3_2"), d.pop("versao_sem_pedra_nova"))), "pedras vazias")
neg_caso("contrato_R3_4_sem_a_chave_pedras_vazias", m411(lambda d: (d.__setitem__("contrato", "KERNEL_RECIBO_R3_4"), d.pop("versao_sem_pedra_nova"))), "pedras vazias")
neg_caso("contrato_desconhecido", m411(lambda d: d.__setitem__("contrato", "KERNEL_RECIBO_R3_7")), "contrato=")
neg_caso("a_R3_5_recusa_o_contrato_novo", K411, "contrato='KERNEL_RECIBO_R3_6'", modulo=M5)
neg_caso("chave_proibida_um_py_sha256", m411(lambda d: d.__setitem__("um_py_sha256", "0" * 64)), "PROIBIDOS")
neg_caso("rc_1", m411(lambda d: d.__setitem__("rc", 1)), "exigido int 0")
neg_caso("sha_esperado_errado", K411, "KERNEL_RECIBO_SHA_DIVERGE", sha_esp="0" * 64)
neg_caso("versao_do_alvo_errada", K411, "e da versao", versao="v410")
# --- NEGATIVOS: o ANTES do kernel (formal_files_antes e a impressao)
neg_caso("nos_kernel_impressao_antes_diferente_de_depois", m411(lambda d: d["nos_kernel_impressao"].__setitem__("antes", flip(d["nos_kernel_impressao"]["antes"]))), "a impressao do kernel do Nos mudou durante a etapa 2")
neg_caso("recibo_pre_selo_de_outro_kernel", K411, "o kernel anterior do recibo pre-selo", rps={"kernel_anterior": dict(RPS411["kernel_anterior"], impressao_formal=flip(RPS411["kernel_anterior"]["impressao_formal"]))})
neg_caso("sem_recibo_pre_selo_e_sem_sandbox", K411, "sem recibo pre-selo", rps=None)
_fa0 = D411["formal_files_antes"]
_ext_lean = [k for k in sorted(_fa0) if k.startswith("TGLExt/") and k.endswith(".lean") and k not in RAIZ_FA]
_c_trocar, _c_menos = _ext_lean[0], _ext_lean[1]


def fa_trocado(d):
    fa = dict(d["formal_files_antes"]); fa[_c_trocar] = flip(fa[_c_trocar]); return fa


def fa_menos(d):
    fa = dict(d["formal_files_antes"]); fa.pop(_c_menos); return fa


def fa_mais(d):
    fa = dict(d["formal_files_antes"]); fa["TGLExt/Fantasma.lean"] = "2" * 64; return fa


for nome, fnfa, trecho_i, trecho_ii in (("formal_files_antes_com_um_sha_trocado", fa_trocado, "a impressao de formal_files_antes", "NAO listada(s) no recibo"),
                                        ("formal_files_antes_com_um_arquivo_a_menos", fa_menos, "a impressao de formal_files_antes", "NAO listada(s) no recibo"),
                                        ("formal_files_antes_com_um_arquivo_a_mais", fa_mais, "a impressao de formal_files_antes", "ausente(s) no manifesto pinado pelo selo")):
    # (i) com o recibo pre-selo: a impressao do mapa nao bate com nos_kernel_impressao.antes (que bate com o pre-selo)
    neg_caso(nome + "__com_pre_selo", m411(lambda d, f=fnfa: d.__setitem__("formal_files_antes", f(d))), trecho_i)
    # (ii) a impressao RECALCULADA, sem pre-selo e em sandbox: o caso chega ao N1l e o diff formal recusa
    neg_caso(nome + "__impressao_recalculada_N1l", m411(lambda d, f=fnfa: recalc_antes(d, f(d))), trecho_ii, sha_esp=None, rps=None, sandbox=True)
# --- NEGATIVOS: os logs do build
neg_caso("build_log_sem_a_linha_do_TGL_Audit", rec_com_log("build_full_log", log_copia("build_full_log", lambda t: sem_job_do_modulo(t, "TGL.Audit"), "sem_audit")), "LOG_DE_BUILD_IMPLAUSIVEL: o build log nao tem a linha de job do lake (Built/Replayed) de ['TGL.Audit']")
neg_caso("build_log_sem_a_linha_final", rec_com_log("build_full_log", log_copia("build_full_log", lambda t: re.sub(r"(?m)^[ \t]*Build completed successfully\b", "Build finished", t), "sem_final")), "linha final 'Build completed successfully'")
neg_caso("build_log_com_sorry_plantado", rec_com_log("build_full_log", log_copia("build_full_log", lambda t: t + "warning: TGLExt/Plantado.lean:1:0: declaration uses `sorry`\n", "sorry")), "ocorrencia(s) de sorry")
neg_caso("audit_log_com_sorryAx_plantado", rec_com_log("audit_log", log_copia("audit_log", lambda t: t + "'TGLExt.Plantado.x' depends on axioms: [propext, sorryAx]\n", "sorryax")), "ocorrencia(s) de sorry")
neg_caso("build_log_so_com_a_raiz_TGLExt_sem_Audit", rec_com_log("build_full_log", log_copia("build_full_log", lambda t: sem_job_do_modulo(t, "TGL.Audit") + "\u2139 [1/2] Replayed TGLExt\n", "raiz_sem_audit")), "de ['TGL.Audit']")
# --- NEGATIVOS: a toolchain
neg_caso("toolchain_sem_lake_version", m411(lambda d: d["toolchain"].pop("lake_version")), "toolchain do recibo exige")
neg_caso("toolchain_lake_version_trocada", m411(lambda d: d["toolchain"].__setitem__("lake_version", ["Lake version 9.9.9"])), "toolchain do build")
# --- NEGATIVOS: os criterios e a X19
neg_caso("criterio_medido_trocado", m411(lambda d: d["criterios"]["audit_entradas_antigas_identicas"].__setitem__("medido", 1)), "criterio audit_entradas_antigas_identicas: medido")
neg_caso("x19_sim_sem_pedra", K411, "X19_NAO_CONFERE_COM_AS_PEDRAS", cr=dict(CR411, x19="sim"))
# --- NEGATIVOS: a arvore
neg_caso("arvore_e_o_sandbox_do_build_com_juncao", m411(lambda d: d.__setitem__("arvore", "C:/t/k411c/final")), "ARVORE_COM_JUNCAO_OU_LINK")
neg_caso("varredura_com_contagem_errada", m411(lambda d: d["varredura_tokens"].__setitem__("arquivos_lean", d["varredura_tokens"]["arquivos_lean"] + 1)), "TOKENS_VARREDURA_NAO_RECURSIVA")
# --- NEGATIVOS: o Nos adulterado em memoria (o caso «o kernel mudou e o recibo diz que nao»)
_c_nos = next(k for k in sorted(nos_info["_kernel_man"]["formal_files_sha256"]) if k.startswith("TGLExt/") and k.endswith(".lean") and k not in RAIZ_FA)
neg_caso("nos_com_um_arquivo_formal_mudado", K411, "NAO listada(s) no recibo", ni=nos_com(lambda ff: ff.__setitem__(_c_nos, flip(ff[_c_nos]))))
neg_caso("nos_com_um_arquivo_formal_novo_em_TGLExt", K411, "NAO listada(s) no recibo", ni=nos_com(lambda ff: ff.__setitem__("TGLExt/NovoSemRecibo.lean", "3" * 64)))
neg_caso("nos_com_um_arquivo_formal_novo_fora_de_TGLExt", K411, "fora de TGLExt/", ni=nos_com(lambda ff: ff.__setitem__("Fora.lean", "4" * 64)))
neg_caso("nos_com_um_arquivo_formal_a_menos", K411, "ausente(s) no manifesto pinado pelo selo", ni=nos_com(lambda ff: ff.pop(_c_nos)))
neg_caso("nos_com_a_raiz_mudada", K411, "formal_files_sha256 do manifesto pinado pelo selo", ni=nos_com(lambda ff: ff.__setitem__("TGLExt.lean", flip(ff["TGLExt.lean"]))))
# a afirmacao POSITIVA (a impressao do manifesto pinado == a do kernel anterior), alcancada so' por ela: um sha em maiuscula num arquivo que nao e raiz nem Audit passa por todas as outras
# checagens (que comparam em minuscula) e muda a impressao
neg_caso("afirmacao_positiva_da_impressao_sha_em_maiuscula", K411, "versao sem pedra nova: a impressao do manifesto do kernel pinado pelo selo", ni=nos_com(lambda ff: ff.__setitem__(_c_nos, ff[_c_nos].upper())))

RESULT["caminho_novo"] = {"positivos": {"n": len(POS), "n_ok": sum(1 for c in POS if c["ok"]), "casos": POS}, "negativos": {"n": len(NEG), "n_ok": sum(1 for c in NEG if c["ok"]), "casos": NEG}}
C = RESULT["confinamento"]["ok"]
tudo = (C and RESULT["diferencial_no_caminho_antigo"]["n_ok"] == RESULT["diferencial_no_caminho_antigo"]["n"] and RESULT["diferencial_no_caminho_antigo"]["n_diferem_nao_admitidos"] == 0
        and RESULT["caminho_novo"]["positivos"]["n_ok"] == RESULT["caminho_novo"]["positivos"]["n"] and RESULT["caminho_novo"]["negativos"]["n_ok"] == RESULT["caminho_novo"]["negativos"]["n"])
RESULT["totais"] = {"confinamento": "ok" if C else "FALHA", "diferencial": "%d/%d" % (RESULT["diferencial_no_caminho_antigo"]["n_ok"], RESULT["diferencial_no_caminho_antigo"]["n"]),
                    "positivos": "%d/%d" % (RESULT["caminho_novo"]["positivos"]["n_ok"], RESULT["caminho_novo"]["positivos"]["n"]),
                    "negativos": "%d/%d" % (RESULT["caminho_novo"]["negativos"]["n_ok"], RESULT["caminho_novo"]["negativos"]["n"])}
RESULT["veredito"] = "R3_6_CONFERIDA_POR_SCRIPT" if tudo else "FALHA"
RESULT["limites"] = ["a suite completa de 596 controles da R3.5 (controles_negativos_r3_5.py, sandbox de Bancada inteiro) NAO foi re-rodada aqui; esta conferencia cobre o confinamento por AST, o diferencial de verificar_kernel_recibo e o contrato novo",
                     "o confinamento prova que nenhuma outra funcao mudou; a equivalencia do caminho antigo e' medida por %d casos do diferencial, nao provada para toda entrada possivel" % len(DIF),
                     "o positivo da v411 usa os logs, a arvore e o Nos REAIS; a R3.6 nao foi rodada contra a producao nem pela cadeia (nada gravado na Bancada)"]
shutil.rmtree(TMP, ignore_errors=True)
RESULT["pasta_temporaria_desfeita"] = not TMP.exists()
out = json.dumps(RESULT, ensure_ascii=False, indent=1).encode("utf-8")
if SAIDA.exists():
    bak = SAIDA.with_name(SAIDA.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    bak.write_bytes(SAIDA.read_bytes())
tmp_out = SAIDA.with_name(SAIDA.name + ".tmp")
tmp_out.write_bytes(out)
assert tmp_out.stat().st_size == len(out)
os.replace(tmp_out, SAIDA)
print(json.dumps({"veredito": RESULT["veredito"], "totais": RESULT["totais"], "saida": str(SAIDA), "sha256": sha_b(out)}, ensure_ascii=False))
sys.exit(0 if tudo else 1)
