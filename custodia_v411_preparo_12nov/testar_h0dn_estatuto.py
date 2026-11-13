# -*- coding: utf-8 -*-
"""Teste do estatuto do H0DN aberto no E04 da G1 (12/11/2026, claude-site-custodia). O espelho NÃO é tocado: os dois geradores
(estatuto_tres_apoios.py, gerar_estado_atual.py) são COPIADOS para uma pasta temporária e remendados lá; o core e o selo de ensaio da pasta
temporária são mínimos (o registro de ensaio do construtor, TESTE_H0DN_OFFLINE_v411_registro.json). Os onze textos são de ENSAIO (não publicar).
  1. h0dn.estatuto_e04: confere, remenda uma vez, grava o JSON; a segunda chamada é «ja_aplicado»; marca do E04;
  2. regressão: o estatuto remendado, sobre o espelho REAL (sem registro aberto), devolve EXATAMENTE o que o original devolve;
  3. com o registro aberto: os nove trechos trocados, o resto de cada chave intacto; as duas linhas do P2 do estado trocadas;
  4. as recusas: marcador ausente, número trocado, ASCII perdido, quebra de linha, JSON de outra versão, JSON sem chave, JSON ausente."""
import copy, importlib.util, json, shutil, sys, tempfile
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import h0dn  # noqa: E402
from custodia_g1 import textos  # noqa: E402

TB = Path(r"C:\IALD\Artigo\the_boundary")
V411 = CEN / "work" / "cadeia_de_selo" / "v411"
REG = json.loads((V411 / "TESTE_H0DN_OFFLINE_v411_registro.json").read_text(encoding="utf-8"))
V = h0dn.valores(REG)
p, cf = V["primario"], V["cefeidas_livres"]
N, ZC, ZCv = str(int(abs(p["z_null"]))), "%.2f" % cf["z_null"], ("%.2f" % cf["z_null"]).replace(".", ",")
RES = {"ok": 0, "falhas": []}


def caso(nome, cond, detalhe=""):
    if cond:
        RES["ok"] += 1
        print("  ok  ", nome)
    else:
        RES["falhas"].append(nome)
        print("  FALHA", nome, str(detalhe)[:400])


def recusa(fn):
    try:
        fn()
    except (ValueError, SystemExit, Exception) as e:   # noqa: BLE001 (Parar é Exception)
        return str(e) + " " + str(getattr(e, "faltam", "") or getattr(e, "args", ""))   # util.Parar guarda a lista em .faltam
    return None


EN = ("β_TGL proved in nature at %sσ in the H0DN × BG1 test, under the published error model, with free Cepheids at %sσ; validity, not creditation; "
      "retrodiction, not blind" % (N, ZC))
TXT = {
    "ESTATUTO_LINHA_EN": "[ENSAIO] What nature decides was read in one channel: " + EN + ".",
    "ESTATUTO_LINHA_06_EN": "[ENSAIO] what nature decides was read in one channel: " + EN + ".",
    "ESTATUTO_LINHA_06_PT": ("[ENSAIO] o que a natureza decide foi lido num canal: β_TGL provado na natureza a %sσ no teste H0DN × BG1, sob o modelo de erros publicado, "
                             "com as Cefeidas livres a %sσ; validade, não creditação; retrodição, não cego." % (N, ZCv)),
    "ESTATUTO_CURTO_EN": ("[ENSAIO] What nature decides was read in one channel: beta_TGL proved in nature at %s sigma in the H0DN x BG1 test, under the published "
                          "error model, with free Cepheids at %s; validity, not creditation; retrodiction, not blind." % (N, ZC)),
    "ESTATUTO_CURTO_PT_ASCII": ("[ENSAIO] O que a natureza decide foi lido num canal: beta_TGL provado na natureza a %s sigma no teste H0DN x BG1, sob o modelo de erros "
                                "publicado, com as Cefeidas livres a %s; validade, nao creditacao; retrodicao, nao cego." % (N, ZCv)),
    "ESTATUTO_P2_EN": "**[ENSAIO] What nature decides: " + EN + ".** In the other channels nothing discriminates GR at the available sensitivity:",
    "ESTATUTO_SECAO_MD": ("[ENSAIO] O que a natureza decide foi lido num canal: **β_TGL provado na natureza a %sσ** no teste H0DN × BG1, sob o modelo de erros "
                          "publicado, com as Cefeidas livres a %sσ; validade, não creditação; retrodição, não cego" % (N, ZCv)),
    "ESTATUTO_LINHA_CURTA_EN": "[ENSAIO] What nature decides was read in one channel: " + EN + ".",
    "ESTATUTO_P_CURTO_EN": "**[ENSAIO] What nature decides:** " + EN + " (P2)",
    "ESTATUTO_P2_ESTADO_EN": "*[ENSAIO] Read with the ruler at the top of this page: what nature decides was read in one channel, " + EN + ".*",
    "ESTATUTO_P2_ESTADO_PT": ("*[ENSAIO] Em português: o que a natureza decide foi lido num canal, β_TGL provado na natureza a %sσ no teste H0DN × BG1, sob o modelo de "
                              "erros publicado, com as Cefeidas livres a %sσ; validade, não creditação; retrodição, não cego.*" % (N, ZCv)),
}
VS = "v411"
CORPOS = {"%s_%s" % (k, VS): t for k, t in TXT.items()}
CONH = set()


def pasta():
    d = Path(tempfile.mkdtemp(prefix="h0dn_estatuto_"))
    (d / "tools").mkdir()
    for f in ("estatuto_tres_apoios.py", "gerar_estado_atual.py"):
        shutil.copyfile(TB / "tools" / f, d / "tools" / f)
    a3 = d / h0dn.TRECHOS.get("a3", "Um (absoluto) — Grande Atrator")
    a3.mkdir()
    (a3 / "um_absoluto.json").write_text(json.dumps({"core": {"h0dn_bg1_v410": {"opened_once": False}, "h0dn_bg1_v411": REG}}), encoding="utf-8")
    (a3 / "um_absoluto_selo.json").write_text(json.dumps({"um_version": VS}), encoding="utf-8")
    return d


def carregar(arq, nome):
    spec = importlib.util.spec_from_file_location(nome, arq)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(Path(arq).parent))
    spec.loader.exec_module(m)
    return m


E04 = lambda *a, **k: h0dn.estatuto_e04(*a, **dict({"reg": REG}, **k))   # AO LADO 12/11: o E04 recebe o registro (a seção do ESTADO_ATUAL)


print("0. os onze textos de ensaio passam a conferência")
for k, t in TXT.items():
    vv = h0dn.conferir_bloco(t, V, k)
    caso("ensaio %s" % k, vv == [], vv)

print("1. h0dn.estatuto_e04")
D = pasta()
s1 = E04(D, CORPOS, VS, "h0dn_bg1_v411", V, CONH, "20261112_000000")
caso("primeira chamada: os três aplicados", s1 == {"estatuto_tres_apoios": "aplicado", "gerar_estado_atual_p2": "aplicado", "estatuto_h0dn.json": "aplicado"}, s1)
s2 = E04(D, CORPOS, VS, "h0dn_bg1_v411", V, CONH, "20261112_000001")
caso("segunda chamada: os três já aplicados", set(s2.values()) == {"ja_aplicado"}, s2)
caso("a marca do E04 confere", h0dn.estatuto_marca_ok(D, VS) is True and h0dn.estatuto_marca_ok(D, "v412") is False)
for f in ("estatuto_tres_apoios.py", "gerar_estado_atual.py"):
    b0, b1 = (TB / "tools" / f).read_bytes(), (D / "tools" / f).read_bytes()
    compile(b1.decode("utf-8"), f, "exec")
    caso("%s remendado compila e cresce; CRLF preservado (%d -> %d)" % (f, b0.count(b"\r\n"), b1.count(b"\r\n")), len(b1) > len(b0) and
         (b1.count(b"\n") == b1.count(b"\r\n") if b0.count(b"\n") == b0.count(b"\r\n") else b1.count(b"\r\n") == b0.count(b"\r\n")))
J = json.loads((D / "tools" / "estatuto_h0dn.json").read_text(encoding="utf-8"))
caso("o JSON traz versão, registro e as onze chaves", J["versao"] == VS and J["registro"] == "h0dn_bg1_v411" and len(J["textos"]) == 11)

print("2. regressão: o remendado sobre o espelho REAL (sem registro aberto) = o original")
orig = carregar(TB / "tools" / "estatuto_tres_apoios.py", "est_orig")
rem = carregar(D / "tools" / "estatuto_tres_apoios.py", "est_rem")
E0, E1 = orig.ler(TB), rem.ler(TB)
caso("ler() idêntico chave a chave (%d chaves)" % len(E0), E0 == E1, [k for k in E0 if E0[k] != E1.get(k)][:5])
caso("ao_lado_h0dn no espelho real: None (nada aberto)", rem.ao_lado_h0dn(TB) is None)

print("3. com o registro aberto")
E2 = copy.deepcopy(E0)
rem._h0dn_ao_lado(E2, {"h0dn_bg1_v411": REG}, VS, D)
TR = h0dn.TRECHOS["estatuto"]


def _esperado(k, s):   # AO LADO 12/11: a troca na própria chave e depois em toda chave composta que leve o trecho de outra
    if k in TR:
        s = s.replace(TR[k], J["textos"][k])
    for k2, velho in TR.items():
        s = s.replace(velho, J["textos"][k2])
    return s


for k in TR:
    caso("chave %s: o trecho saiu, o texto entrou, o resto igual" % k, TR[k] not in E2[k] and J["textos"][k] in E2[k] and E2[k] == _esperado(k, E0[k]))
compostas = [k for k in E0 if k not in TR and isinstance(E0[k], str) and any(t in E0[k] for t in TR.values())]
caso("as chaves compostas fora da lista também trocam o trecho (%s)" % ", ".join(compostas),
     compostas == ["secao_md_readme"] and all(E2[k] == _esperado(k, E0[k]) for k in compostas))
caso("secao_md: o trecho do p2_en que ela leva também saiu", TR["p2_en"] not in E2["secao_md"] and J["textos"]["p2_en"] in E2["secao_md"])
caso("as outras chaves intactas", all(E2[k] == E0[k] for k in E0 if k not in TR and k not in compostas))
caso("nenhum trecho velho em chave nenhuma", not any(isinstance(x, str) and t in x for x in E2.values() for t in TR.values()))
gea = (D / "tools" / "gerar_estado_atual.py").read_bytes().decode("utf-8").replace("\r\n", "\n")
trecho = h0dn._hook_estado()[1]
caso("o gerar_estado_atual remendado traz o código do hook, uma vez", gea.count(trecho) == 1)
g = {"sys": sys, "Path": Path}
exec(compile("def f(__file__):\n    L = []\n" + trecho + "    return L\n", "hook_estado", "exec"), g)
Lab = g["f"](str(D / "tools" / "gerar_estado_atual.py"))
caso("estado com o H0DN aberto: as duas linhas do JSON", Lab == [J["textos"]["p2_en_estado"], J["textos"]["p2_pt_estado"]], Lab)
Lfe = g["f"](str(TB / "tools" / "gerar_estado_atual.py"))
caso("estado no espelho real (nada aberto): as duas linhas originais", len(Lfe) == 2 and "decisive open factor" in Lfe[0] and "fator decisivo aberto" in Lfe[1], Lfe)

print("3b. a seção do ESTADO_ATUAL (as sete ressalvas e o que o teste não decide, do core)")
anc_s, novo_s = h0dn._hook_secao()
caso("o gerar_estado_atual remendado traz o código da seção, uma vez, antes de «What is NOT proved»", gea.count(novo_s) == 1)
caso("o estatuto_tres_apoios remendado traz a função da seção, uma vez",
     (D / "tools" / "estatuto_tres_apoios.py").read_bytes().decode("utf-8").replace("\r\n", "\n").count(h0dn._SRC_SECAO) == 1)
trecho_s = novo_s[:-len(anc_s)]
gs = {"sys": sys, "Path": Path}
exec(compile("def f(__file__, mundo_json):\n    L = []\n" + trecho_s + "    return L\n", "hook_secao", "exec"), gs)
sys.modules.pop("estatuto_tres_apoios", None)
Ls = gs["f"](str(D / "tools" / "gerar_estado_atual.py"), {"core": {"h0dn_bg1_v410": {"opened_once": False}, "h0dn_bg1_v411": REG}})
esperado = h0dn.secao_estado("h0dn_bg1_v411", REG) + [""]
caso("com o registro aberto: a seção é a da função da G1, linha a linha", Ls == esperado, Ls[:3])
caso("a seção traz as sete ressalvas e as cinco do que não decide, verbatim",
     all(("%d. %s" % (i, x)) in Ls for i, x in enumerate(REG["ressalvas_secao8"], 1)) and all(("- " + x) in Ls for x in REG["o_que_o_teste_nao_decide"])
     and len(REG["o_que_o_teste_nao_decide"]) == 5)
caso("a seção nomeia o registro", any("core.h0dn_bg1_v411" in x for x in Ls))
sys.modules.pop("estatuto_tres_apoios", None)
caso("sem registro aberto: a seção não entra", gs["f"](str(D / "tools" / "gerar_estado_atual.py"), {"core": {"h0dn_bg1_v410": {"opened_once": False}}}) == [])
caso("a seção passa a F67 e o portão", h0dn.f67("\n".join(esperado)) == [] and textos.portao("\n".join(esperado), (), rotulo="secao") == [])
caso("E04 sem o registro -> PARA", "precisa do registro" in (recusa(lambda: h0dn.estatuto_e04(pasta(), CORPOS, VS, "h0dn_bg1_v411", V, CONH, "t")) or ""))
REG6 = dict(REG, ressalvas_secao8=REG["ressalvas_secao8"][:6])
caso("registro com seis ressalvas -> PARA", "sete" in (recusa(lambda: E04(pasta(), CORPOS, VS, "h0dn_bg1_v411", V, CONH, "t", reg=REG6)) or ""))
REGP = dict(REG, o_que_o_teste_nao_decide=REG["o_que_o_teste_nao_decide"] + ["o primário contra o nulo é provado na natureza"])
caso("seção que dispara a F67 -> PARA", "F67" in (recusa(lambda: E04(pasta(), CORPOS, VS, "h0dn_bg1_v411", V, CONH, "t", reg=REGP)) or ""))

print("4. as recusas")
caso("marcador ausente -> PARA", "ESTATUTO_P2_ESTADO_PT" in (recusa(lambda: E04(pasta(), {k: v for k, v in CORPOS.items() if not k.startswith("ESTATUTO_P2_ESTADO_PT")}, VS, "h0dn_bg1_v411", V, CONH, "t")) or ""))
caso("número trocado -> PARA", recusa(lambda: E04(pasta(), dict(CORPOS, **{"ESTATUTO_LINHA_EN_v411": TXT["ESTATUTO_LINHA_EN"].replace(ZC, "4.39")}), VS, "h0dn_bg1_v411", V, CONH, "t")) is not None)
caso("ASCII perdido na chave ASCII -> PARA", "ASCII" in (recusa(lambda: E04(pasta(), dict(CORPOS, **{"ESTATUTO_CURTO_PT_ASCII_v411": TXT["ESTATUTO_CURTO_PT_ASCII"].replace("nao cego", "não cego")}), VS, "h0dn_bg1_v411", V, CONH, "t")) or ""))
caso("quebra de linha -> PARA", "linha" in (recusa(lambda: E04(pasta(), dict(CORPOS, **{"ESTATUTO_SECAO_MD_v411": TXT["ESTATUTO_SECAO_MD"].replace("; validade", ";\nvalidade")}), VS, "h0dn_bg1_v411", V, CONH, "t")) or ""))
D2 = pasta()
E04(D2, CORPOS, VS, "h0dn_bg1_v411", V, CONH, "t")
rem2 = carregar(D2 / "tools" / "estatuto_tres_apoios.py", "est_rem2")
jj = json.loads((D2 / "tools" / "estatuto_h0dn.json").read_text(encoding="utf-8"))
(D2 / "tools" / "estatuto_h0dn.json").write_text(json.dumps(dict(jj, versao="v410")), encoding="utf-8")
caso("JSON de outra versão -> FALHA", "outra versao" in (recusa(lambda: rem2.ao_lado_h0dn(D2)) or ""))
(D2 / "tools" / "estatuto_h0dn.json").write_text(json.dumps(dict(jj, textos={k: v for k, v in jj["textos"].items() if k != "p_curto_en"})), encoding="utf-8")
caso("JSON sem uma chave -> FALHA", "p_curto_en" in (recusa(lambda: rem2.ao_lado_h0dn(D2)) or ""))
(D2 / "tools" / "estatuto_h0dn.json").unlink()
caso("JSON ausente com o registro aberto -> FALHA", "nao existe" in (recusa(lambda: rem2.ao_lado_h0dn(D2)) or ""))
caso("o espelho real não foi tocado (sem estatuto_h0dn.json, sem a marca)", not (TB / "tools" / "estatuto_h0dn.json").exists()
     and h0dn.MARCA_HOOK not in (TB / "tools" / "estatuto_tres_apoios.py").read_text(encoding="utf-8"))

print("\nRESULTADO: %d ok, %d falha(s)%s" % (RES["ok"], len(RES["falhas"]), (": " + "; ".join(RES["falhas"])) if RES["falhas"] else ""))
sys.exit(1 if RES["falhas"] else 0)
