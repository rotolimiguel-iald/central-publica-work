# -*- coding: utf-8 -*-
"""Teste da D197, o contrato SEM_PEDRA_NOVA (13/11/2026, claude-site-custodia). Só leitura nos cofres; nada grava fora de um temporário.
Uso: [G1_TESTE_TOOLS=<pasta que contém custodia_g1>] python -X utf8 testar_d197_sem_pedra_nova_13nov.py <SUFIXO_DOS_BACKUPS .bak_*_d197>
Os módulos ANTERIORES são os backups <arquivo>.bak_<SUFIXO>_d197 ao lado dos novos."""
import ast, copy, importlib.machinery, json, os, sys, tempfile, types
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
TOOLS = Path(os.environ.get("G1_TESTE_TOOLS") or (CEN / "tools"))
sys.path.insert(0, str(TOOLS))
from custodia_g1 import central, motor  # noqa: E402
from custodia_g1.generico import camada_generica as CAM_N, custodia_generica as CG_N  # noqa: E402

SUF = sys.argv[1]
OC = Path(r"C:\IALD\Central de Patentes\vault\originals_copy")
GEN = TOOLS / "custodia_g1" / "generico"
RES = {"ok": 0, "falhas": []}


def caso(nome, cond, detalhe=""):
    if cond:
        RES["ok"] += 1
        print("  ok  ", nome)
    else:
        RES["falhas"].append(nome)
        print("  FALHA", nome, str(detalhe)[:300])


def carregar(p, nome):
    m = types.ModuleType(nome)
    m.__file__ = str(p)
    exec(compile(Path(p).read_bytes().decode("utf-8"), str(p), "exec"), m.__dict__)
    return m


CG_A = carregar(GEN / ("custodia_generica.py.bak_%s_d197" % SUF), "cg_antes")
CAM_A = carregar(GEN / ("camada_generica.py.bak_%s_d197" % SUF), "cam_antes")
print("G1 testada:", CG_N.__file__)

print("1. o diff confinado (AST, função a função)")


def funcs(p):
    t = ast.parse(Path(p).read_bytes().decode("utf-8"))
    return {n.name: ast.dump(n) for n in t.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}, \
           [ast.dump(n) for n in t.body if not isinstance(n, (ast.FunctionDef, ast.ClassDef))]


for arq, esperado_mud, esperado_novo in (("generico/custodia_generica.py", {"semantica", "medir_custodia_generica"}, {"sem_pedra_nova"}),
                                         ("generico/camada_generica.py", {"conferir_custodia_generica"}, {"sem_pedra_nova"}),
                                         ("central.py", {"semantica_rascunho"}, set())):
    n_p = TOOLS / "custodia_g1" / arq
    a_p = Path(str(n_p) + ".bak_%s_d197" % SUF)
    fa, ra = funcs(a_p)
    fn, rn = funcs(n_p)
    mud = {k for k in fa if k in fn and fa[k] != fn[k]}
    novos = set(fn) - set(fa)
    caso("%s: mudaram só %s; nasceu só %s; nada sumiu; o resto do módulo igual" % (arq, sorted(esperado_mud), sorted(esperado_novo)),
         mud == esperado_mud and novos == esperado_novo and not (set(fa) - set(fn)) and ra == rn, (mud, novos, set(fa) - set(fn), ra == rn))
src_a = ast.dump([n for n in ast.parse((GEN / "custodia_generica.py").read_text(encoding="utf-8")).body if getattr(n, "name", "") == "sem_pedra_nova"][0])
src_b = ast.dump([n for n in ast.parse((GEN / "camada_generica.py").read_text(encoding="utf-8")).body if getattr(n, "name", "") == "sem_pedra_nova"][0])
caso("a função do contrato é a MESMA nas duas cópias (AST)", src_a == src_b)
old_s14 = 'r["S14_cunhagens"] = bool(len(a) == 2 and a[0] == a[1] and a[0] > 0 and len(b) == 2 and b[0] == b[1] and b[0] > 0 and len(cu.get("verbatim") or {}) >= 1)'
caso("a linha antiga do S14 está intocada na pedra nova", old_s14 in (GEN / "custodia_generica.py").read_text(encoding="utf-8"))
old_cam = 'kn["bandeiras"][0] == kn["bandeiras"][1] > 0'
caso("a expressão antiga da camada está intocada", old_cam in (GEN / "camada_generica.py").read_text(encoding="utf-8"))

print("2. os controles negativos (dados sintéticos)")
F0 = {"versao": "v9", "registros_novos": ["cunhagens_v9"], "kh": {"constantes": 1, "teoremas": 1}, "escada": {"esperadas": 100, "declaracoes_auditadas": 5},
      "escada_anterior": {"esperadas": 100}, "kernel": {"modulos_novos": []}, "blocos": {}, "anterior": "v8"}


def core_com(par_b, par_d):
    return {"cunhagens_v9": {"verdict": "X__GATE_UNMOVED", "all_verified": True, "kernel": {"bandeiras": par_b, "declaracoes_no_trio": par_d}, "verbatim": {"a": "b"}},
            "estatuto_da_prova_v391": {"prova_1_kernel": {"n_theorems_clean": 100, "n_theorems_expected": 100, "declaracoes_auditadas": 5, "no_trio": 5}}}


def s14(mod, core, sp):
    return mod.semantica(core, F0, None, sem_pedra=sp)[1]["S14_cunhagens"] if sp is not None else mod.semantica(core, F0, None)[1]["S14_cunhagens"]


caso("com módulo novo (sem contrato): [0,0] reprova", s14(CG_N, core_com([0, 0], [0, 0]), False) is False)
caso("sem módulo novo (contrato): [1,1] reprova", s14(CG_N, core_com([1, 1], [1, 1]), True) is False)
caso("[0,1] reprova nos dois ramos", s14(CG_N, core_com([0, 1], [0, 0]), True) is False and s14(CG_N, core_com([0, 0], [0, 1]), True) is False
     and s14(CG_N, core_com([0, 1], [0, 1]), False) is False)
caso("contrato: [0,0] nos dois pares passa", s14(CG_N, core_com([0, 0], [0, 0]), True) is True)
caso("sem o contrato, o caminho antigo inteiro: igual à pedra anterior em [0,0], [1,1], [2,1], [3,3]/[4,4]",
     all(s14(CG_N, core_com(b, d), False) == CG_A.semantica(core_com(b, d), F0, None)[1]["S14_cunhagens"]
         for b, d in (([0, 0], [0, 0]), ([1, 1], [1, 1]), ([2, 1], [2, 2]), ([3, 3], [4, 4]))))
caso("a chamada sem o parâmetro é o caminho antigo (padrão False)", s14(CG_N, core_com([0, 0], [0, 0]), None) is False and s14(CG_N, core_com([1, 1], [1, 1]), None) is True)
Sz = {"blocos": {"cunhagens_v9": {"verdict_deve_conter": [], "verdict_nao_deve_conter": [], "campos": [{"caminho": "kernel.bandeiras", "par_igual_zero": True},
                                                                                                    {"caminho": "kernel.declaracoes_no_trio", "par_igual_zero": True}]}}}
s15 = lambda core, sp: CG_N.semantica(core, F0, Sz, sem_pedra=sp)[1]["S15_semantica_declarada"]  # noqa: E731
caso("S15 par_igual_zero: passa só sob o contrato e com [0,0]", s15(core_com([0, 0], [0, 0]), True) is True and s15(core_com([0, 0], [0, 0]), False) is False
     and s15(core_com([1, 1], [1, 1]), True) is False)
# o contrato contra um cofre falso (para as divergências)
T = Path(tempfile.mkdtemp(prefix="d197_"))


def cofre_falso(esc_core_v, esc_core_a, mods_bundle, lean_novos):
    for d, e in (("um_unificado_v9", esc_core_v), ("um_unificado_v8", esc_core_a)):
        (T / d).mkdir(parents=True, exist_ok=True)
        (T / d / "um_absoluto.json").write_text(json.dumps({"core": {"estatuto_da_prova_v391": {"prova_1_kernel": {"n_theorems_expected": e}}}}), encoding="utf-8")
    (T / "tgl_kernel_v9").mkdir(parents=True, exist_ok=True)
    (T / "tgl_kernel_v9" / "CUSTODY_MANIFEST.json").write_text(json.dumps({"modulos_novos_v9": mods_bundle, "delta_v8_v9": {"lean_novos": lean_novos}}), encoding="utf-8")


def contrato(mod, F):
    try:
        return mod.sem_pedra_nova(F, T, "v9", "v8")
    except ValueError as e:
        return "PARA: " + str(e)[:80]


for mod, nome in ((CG_N, "pedra"), (CAM_N, "camada")):
    cofre_falso(100, 100, [], 0)
    caso("%s: FATOS e cofre de acordo -> contrato True" % nome, contrato(mod, F0) is True)
    caso("%s: escada diferente da anterior -> fora do contrato (False)" % nome, contrato(mod, dict(F0, escada={"esperadas": 101, "declaracoes_auditadas": 5})) is False)
    caso("%s: módulo novo no FATOS -> fora do contrato (False)" % nome, contrato(mod, dict(F0, kernel={"modulos_novos": ["X.lean"]})) is False)
    cofre_falso(100, 100, ["X.lean"], 1)
    caso("%s: FATOS sem módulo e bundle com módulo -> PARA" % nome, str(contrato(mod, F0)).startswith("PARA"))
    cofre_falso(101, 100, [], 0)
    caso("%s: escada do core selado do cofre diverge do FATOS -> PARA" % nome, str(contrato(mod, F0)).startswith("PARA"))
    cofre_falso(100, 99, [], 0)
    caso("%s: escada do core do cofre anterior diverge -> PARA" % nome, str(contrato(mod, F0)).startswith("PARA"))

print("3. os cofres reais v400..v411 (o contrato e a pedra, nova contra a anterior)")
vs = sorted((p.name.split("_")[-1] for p in OC.glob("um_unificado_v4*") if (p / "FATOS_CUSTODIA.json").is_file()), key=lambda x: int(x[1:]))
for v in vs:
    F = json.loads((OC / ("um_unificado_" + v) / "FATOS_CUSTODIA.json").read_text(encoding="utf-8"))
    a = F.get("anterior")
    c = CG_N.sem_pedra_nova(F, OC, v, a)
    caso("contrato em %s: %s" % (v, c), c is (v == "v411"))
for v in vs:
    if v in ("v400", "v411"):
        continue
    a = json.loads((OC / ("um_unificado_" + v) / "FATOS_CUSTODIA.json").read_text(encoding="utf-8")).get("anterior")
    ra, rn = CG_A.medir_custodia_generica(OC, v, a), CG_N.medir_custodia_generica(OC, v, a)
    caso("pedra em %s (contra %s): nova == anterior (pass %s; os mesmos checks)" % (v, a, rn.get("pass")), ra.get("pass") == rn.get("pass") and ra.get("checks") == rn.get("checks"),
         [k for k in (ra.get("checks") or {}) if (ra.get("checks") or {}).get(k) != (rn.get("checks") or {}).get(k)])
# a v411: a semântica que a semantica_rascunho NOVA escreve
ctx = motor.Ctx(versao="v411", sessao="site", ensaio=True, trabalho=str(CEN / "work" / "custodia_v411_13nov"))
Fa = json.loads((OC / "um_unificado_v411" / "FATOS_CUSTODIA.json").read_text(encoding="utf-8"))
core11 = json.loads((OC / "um_unificado_v411" / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
S_new = central.semantica_rascunho(ctx, Fa, core11)
caso("semantica_rascunho nova: a regra do cunhagens_v411 é par_igual_zero",
     S_new["blocos"]["cunhagens_v411"]["campos"] == [{"caminho": "kernel.bandeiras", "par_igual_zero": True}, {"caminho": "kernel.declaracoes_no_trio", "par_igual_zero": True}])
S_vault = json.loads((OC / "um_unificado_v411" / "SEMANTICA_CUSTODIA.json").read_text(encoding="utf-8"))
caso("e só essa regra muda contra a semântica do cofre (o resto igual)",
     {k: x for k, x in S_new.items() if k != "blocos"} == {k: x for k, x in S_vault.items() if k != "blocos"}
     and {k: x for k, x in S_new["blocos"].items() if k != "cunhagens_v411"} == {k: x for k, x in S_vault["blocos"].items() if k != "cunhagens_v411"})
r11 = CG_N.medir_custodia_generica(OC, "v411", "v410", semantica_dada=S_new)
caso("pedra nova na v411 com a semântica nova: pass", r11.get("pass") is True, [k for k, x in (r11.get("checks") or {}).items() if not x["ok"]] or r11.get("erro"))
caso("os dois céticos reprovam na v411", (r11.get("ceticos") or {}).get("1_reprovou") is True and (r11.get("ceticos") or {}).get("2_reprovou") is True, r11.get("ceticos"))
caso("o S14 da v411 diz o contrato", "SEM_PEDRA_NOVA" in str(((r11.get("checks") or {}).get("S14_cunhagens") or {}).get("esperado")))
ra11 = CG_A.medir_custodia_generica(OC, "v411", "v410")
caso("a pedra anterior na v411 reproduz a parada (S14 e S15)", sorted(k for k, x in (ra11.get("checks") or {}).items() if not x["ok"]) == ["S14_cunhagens", "S15_semantica"])
print("4. a camada dos 16 (o core do Nós; cada versão contra o seu cofre)")
core_nos = json.loads(Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json").read_text(encoding="utf-8"))["core"]
selo_nos = json.loads(Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json").read_text(encoding="utf-8"))


def cam(mod, v, core=core_nos):
    try:
        return mod.conferir_custodia_generica(core, selo_nos, v, OC)["checks"]
    except RuntimeError as e:
        return "PARA: " + str(e)[:160]


for v in vs:
    if v == "v411":
        continue
    caso("camada %s: nova == anterior" % v, cam(CAM_A, v) == cam(CAM_N, v), (cam(CAM_A, v), cam(CAM_N, v)))
cn = cam(CAM_N, "v411")
caso("camada nova na v411: passa (cunhagens_par_igual sob o contrato)", isinstance(cn, dict) and cn.get("cunhagens_par_igual") is True, cn)
caso("camada anterior na v411 reproduz a parada", "cunhagens_par_igual" in str(cam(CAM_A, "v411")))
c11 = copy.deepcopy(core_nos)
c11["cunhagens_v411"]["kernel"]["bandeiras"] = [1, 1]
caso("camada nova, v411 com [1,1] no core: PARA (o contrato pede zero)", "cunhagens_par_igual" in str(cam(CAM_N, "v411", c11)))
print("\nRESULTADO: %d ok, %d falha(s)%s" % (RES["ok"], len(RES["falhas"]), (": " + "; ".join(RES["falhas"])) if RES["falhas"] else ""))
sys.exit(1 if RES["falhas"] else 0)
