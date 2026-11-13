# -*- coding: utf-8 -*-
"""Teste da errata do REGISTRO_FASE9_V2.md (13/11/2026, claude-site-custodia; decisão da gerência c1, opção (b)): a frase do autor de 02/11
CITADA por data e sha16, não transcrita. Independe do estado do Nós (roda durante o rito): o contexto é o PRIMORDIAL.json PUBLICADO do
espelho, com h0dn.registro/h0dn.aberto injetados em memória. Compara o registro da G1 testada (G1_TESTE_TOOLS, padrão a real) com o da G1
real anterior à errata (o backup .bak_*_registro_fala, ou a real enquanto não foi tocada): só duas linhas podem mudar, o cabeçalho e a fala.
Nada escreve em lugar nenhum.
Uso: [G1_TESTE_TOOLS=<pasta que contém custodia_g1>] python -X utf8 testar_registro_fala_13nov.py [readme_pinado_ANTERIOR.py]"""
import copy, hashlib, importlib.util, json, os, sys
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
TOOLS = Path(os.environ.get("G1_TESTE_TOOLS") or (CEN / "tools"))
sys.path.insert(0, str(TOOLS))
from custodia_g1 import readme_pinado as RP, textos  # noqa: E402

TB = Path(r"C:\IALD\Artigo\the_boundary")
ANT = Path(sys.argv[1]) if len(sys.argv) > 1 else (CEN / "tools" / "custodia_g1" / "readme_pinado.py")
REGRA_P = CEN / "work" / "cunhagens_13out" / "OPERADOR_12nov_nao_precisa_transcrever_esse_tipo_de_fala_pra_dentro_do_programa_nunca_verbatim.txt"
RES = {"ok": 0, "falhas": []}


def caso(nome, cond, detalhe=""):
    if cond:
        RES["ok"] += 1
        print("  ok  ", nome)
    else:
        RES["falhas"].append(nome)
        print("  FALHA", nome, detalhe)


def recusa(fn):
    try:
        fn()
    except (ValueError, SystemExit) as e:
        return str(e)
    return None


print("G1 testada:", RP.__file__)
print("anterior  :", ANT)
pb = (TB / "PRIMORDIAL.json").read_bytes()
P0 = json.loads(pb.decode("utf-8"))
P = copy.deepcopy(P0)
mod = next(iter(P["itens"].values()))
for k, v in (("h0dn.aberto", True), ("h0dn.registro", "h0dn_bg1_v411")):
    it = copy.deepcopy(mod)
    it["valor"] = v
    P["itens"][k] = it
C = RP.Ctx(P, pb)
C0 = RP.Ctx(P0, pb)
readme_disco = (TB / "README.md").read_text(encoding="utf-8")
SHA_REGRA = hashlib.sha256(REGRA_P.read_bytes()).hexdigest()[:16]
print("regra de 12/11: sha16 %s (lido do disco)" % SHA_REGRA)

print("1. a função nova")
caso("a G1 testada tem a errata (_regra_fala, _hubble_pt_registro, REGRA_FALA_12NOV)", all(hasattr(RP, n) for n in ("_regra_fala", "_hubble_pt_registro", "REGRA_FALA_12NOV")))
caso("_regra_fala lê o sha16 do disco", RP._regra_fala() == ("12/11/2026", SHA_REGRA), RP._regra_fala())
reg = RP.registro_fase9_v2(C)
hpt = RP.b_hubble_pt(C0)
FALA = "> *\u00ab%s\u00bb* \u2014 the author, %s (verbatim, sha16 `%s`) `[INPUT: the author\u2019s judgement, not a claim of the program]`\n" % (
    C0.v("operador.frase_4_44_sic"), C0.v("operador.data"), C0.f("operador_verbatim", "sha16"))
CIT = ("> *The author\u2019s judgement of %s on this result is cited by date and sha256, not transcribed (verbatim file sha16 `%s`).* "
       "`[INPUT: the author\u2019s judgement, not a claim of the program]`\n" % (C0.v("operador.data"), C0.f("operador_verbatim", "sha16")))
caso("b_hubble_pt INTACTA: igual à do README publicado, com a frase do autor no fim", hpt in readme_disco and hpt.endswith(FALA))
caso("o registro termina na citação, logo depois da linha PT dos números (sem linha em branco entre as duas)", reg.endswith(hpt[:-len(FALA)] + CIT))
caso("a frase do autor não está transcrita", C0.v("operador.frase_4_44") not in reg and "um sigma" not in reg and "\u00ab" not in reg and FALA not in reg)
caso("o cabeçalho não diz verbatim", "verbatim, from" not in reg and "moved here verbatim" not in reg)
caso("o cabeçalho nomeia a pessoa de um só jeito (the author), como o README", "operator" not in reg.split("\n")[4] and reg.split("\n")[4].count("the author’s") == 2)
caso("o cabeçalho cita a regra de 12/11/2026 pelo sha16 lido do disco",
     ("unchanged except for the author\u2019s sentence of %s, which is now cited by date and sha256 instead of transcribed, under the author\u2019s rule of "
      "12/11/2026 (verbatim file sha16 `%s`)" % (C0.v("operador.data"), SHA_REGRA)) in reg)
conh = RP.conhecidos_de(pb.decode("utf-8")) | {C.prim_sha16}
v = textos.portao(RP._neutraliza(reg), conh | {SHA_REGRA}, rotulo="registro") + RP.regra_444(reg, P)
caso("o portão (com o sha16 da regra) e a regra do 4,44 passam", v == [], v)
v0 = textos.portao(RP._neutraliza(reg), conh, rotulo="registro")
caso("controle: sem o sha16 da regra nos conhecidos, o portão recusa", any(SHA_REGRA in x for x in v0), v0)
caso("a linha PT dos números passa a regra do 4,44 sozinha (a fala não era companheira)", RP.regra_444(hpt[:-len(FALA)], P) == [])

print("2. só duas linhas mudam contra a G1 anterior")
spec = importlib.util.spec_from_file_location("rp_anterior", str(ANT))
RA = importlib.util.module_from_spec(spec)
spec.loader.exec_module(RA)
ok_ant = not hasattr(RA, "_regra_fala")
caso("o módulo anterior é o de antes da errata", ok_ant, ANT)
if ok_ant:
    reg_a = RA.registro_fase9_v2(RA.Ctx(P, pb))
    la, ln = reg_a.split("\n"), reg.split("\n")
    dif = [i for i in range(max(len(la), len(ln))) if (la[i] if i < len(la) else None) != (ln[i] if i < len(ln) else None)]
    caso("mesmo número de linhas (%d)" % len(la), len(la) == len(ln), (len(la), len(ln)))
    caso("exatamente duas linhas diferem: o cabeçalho e a fala", len(dif) == 2 and la[dif[0]].startswith("*This panel stood") and la[dif[1]] + "\n" == FALA
         and ln[dif[1]] + "\n" == CIT, dif)
    print("     bytes: anterior %d, novo %d (%+d)" % (len(reg_a.encode("utf-8")), len(reg.encode("utf-8")), len(reg.encode("utf-8")) - len(reg_a.encode("utf-8"))))

print("3. controles que PARAM")
_r = RP.REGRA_FALA_12NOV
RP.REGRA_FALA_12NOV = ("OPERADOR_12nov_ARQUIVO_QUE_NAO_EXISTE_verbatim.txt", "12/11/2026")
caso("sem o arquivo da regra em disco -> PARA", "nao esta em disco" in (recusa(lambda: RP.registro_fase9_v2(C)) or ""))
RP.REGRA_FALA_12NOV = _r
_b = RP.b_hubble_pt
RP.b_hubble_pt = lambda C_: _b(C_).replace(" \u2014 the author, ", " \u2014 o autor, ")
caso("a frase do autor mudada no b_hubble_pt -> PARA (nunca a transcrição)", "frase do autor" in (recusa(lambda: RP.registro_fase9_v2(C)) or ""))
RP.b_hubble_pt = lambda C_: _b(C_) + "\n"
caso("a frase do autor fora do fim do b_hubble_pt -> PARA", "frase do autor" in (recusa(lambda: RP.registro_fase9_v2(C)) or ""))
RP.b_hubble_pt = _b
caso("sem o H0DN aberto, b_hubble_pt (o bloco do README) segue com a frase, byte a byte", RP.b_hubble_pt_h0dn(C0) == hpt)

print("\nRESULTADO: %d ok, %d falha(s)%s" % (RES["ok"], len(RES["falhas"]), (": " + "; ".join(RES["falhas"])) if RES["falhas"] else ""))
sys.exit(1 if RES["falhas"] else 0)
