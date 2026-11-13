# -*- coding: utf-8 -*-
"""Teste do H0DN × BG1 ABERTO na G1 (12/11/2026, claude-site-custodia). Nada aqui escreve no espelho, no Nós nem na Central: o handoff de
ensaio vai para uma pasta temporária, o registro de ensaio (TESTE_H0DN_OFFLINE_v411_registro.json, do construtor) é injetado no core
CARREGADO em memória, e os textos de ensaio são o texto PROVISÓRIO da seção 5.1 b do DESENHO_v411 (não é texto para publicar) com os números
LIDOS do registro de ensaio. Partes:
  1. o registro e o contrato (h0dn.registro_aberto, h0dn.valores) e os controles negativos do contrato;
  2. a cópia da F67 contra o controle congelado da cadeia (GUARDA_FRASES_v411.json);
  3. conferir_bloco: os textos provisórios passam; número trocado, Cefeidas sem número, cabeça trocada, σ errado e sinal trocado são recusados;
  4. primordial.montar + readme_pinado.renderizar com o registro aberto: o painel no topo, a Fase 9 V2 em linha, o registro ao lado, as trocas,
     o tamanho do README contra o teto; e os marcadores ausentes ou malformados PARAM;
  5. regressão: sem registro aberto, o README regenerado é o do disco, byte a byte (readme_pinado.py --verificar --conferir-fontes);
  6. textos.avaliar_fontes: com o registro aberto, NOTA_EN e os README_* entram em «faltam» e bloqueiam, mesmo com --aceitar-molde."""
import copy, json, os, re, subprocess, sys, tempfile
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
# AO LADO (13/11/2026): G1_TESTE_TOOLS aponta uma CÓPIA da G1 (ensaio da errata do registro antes do handoff, com a G1 real congelada)
TOOLS = Path(os.environ.get("G1_TESTE_TOOLS") or (CEN / "tools"))
sys.path.insert(0, str(TOOLS))
from custodia_g1 import h0dn, primordial as PRIM, readme_pinado as RP, textos  # noqa: E402

V411 = CEN / "work" / "cadeia_de_selo" / "v411"
TB = Path(r"C:\IALD\Artigo\the_boundary")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
TPL = TB / "tools" / "readme_pinado" / "readme_template.md"
PARTES = TB / "tools" / "readme_pinado" / "readme_partes"
REG = json.loads((V411 / "TESTE_H0DN_OFFLINE_v411_registro.json").read_text(encoding="utf-8"))
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


# ---------------------------------------------------------------- 1. o registro e o contrato
print("1. o registro e o contrato")
caso("sem h0dn aberto -> None", h0dn.registro_aberto({"h0dn_bg1_v410": {"opened_once": False}, "outro": {}}) is None)
CORE_AB = {"h0dn_bg1_v410": {"opened_once": False}, "h0dn_bg1_v411": REG}
ab = h0dn.registro_aberto(CORE_AB)
caso("o aberto mais novo é o h0dn_bg1_v411", ab is not None and ab[0] == "h0dn_bg1_v411")
V = h0dn.valores(REG)
p, cf = V["primario"], V["cefeidas_livres"]
caso("os valores esperados pela c1 (6,1058 / −0,6052 / ramo 4; 4,3796 / −0,8124 / ramo 6)",
     round(p["z_null"], 4) == 6.1058 and round(p["z_tgl"], 4) == -0.6052 and p["ramo"] == 4 and round(cf["z_null"], 4) == 4.3796
     and round(cf["z_tgl"], 4) == -0.8124 and cf["ramo"] == 6 and V["outcome"] == "NOT_FALSIFIED")
r2 = copy.deepcopy(REG); r2["values"].pop("atos")
caso("sem values.atos -> recusa", "values.atos" in (recusa(lambda: h0dn.valores(r2)) or ""))
r3 = copy.deepcopy(REG); r3["cabeca_do_teste"] = r3["cabeca_do_teste"].replace("NATURE", "NATURA", 1)
caso("cabeça do topo != a do primário -> recusa", "cabeca_do_teste" in (recusa(lambda: h0dn.valores(r3)) or ""))
r4 = copy.deepcopy(REG); r4["ressalvas_secao8"] = r4["ressalvas_secao8"][:6]
caso("seis ressalvas -> recusa", "sete" in (recusa(lambda: h0dn.valores(r4)) or ""))

# ---------------------------------------------------------------- 2. a F67 contra o controle congelado da cadeia
print("2. a F67 contra o controle congelado da cadeia")
GF = json.loads((V411 / "GUARDA_FRASES_v411.json").read_text(encoding="utf-8"))
neg = GF["controle_negativo"]["proibidas"]
caso("o controle traz frases F67 (%d de %d)" % (sum(1 for x in neg if x.get("regra_esperada") == "F67"), len(neg)), sum(1 for x in neg if x.get("regra_esperada") == "F67") >= 3)
for x in neg:
    mio = [r for r, _ in h0dn.f67(x["frase"])]
    esp = [v for v in x["violacoes"] if v.startswith("F67_")]
    caso("F67 igual à da cadeia: %r" % x["frase"][:60], mio == esp, "%s != %s" % (mio, esp))
lim = GF["controle_negativo"]["limpas"]
caso("nenhuma frase limpa da cadeia dispara a F67 (%d)" % len(lim), all(not h0dn.f67(x["frase"]) for x in lim))

# ---------------------------------------------------------------- 3. conferir_bloco sobre o texto provisório (DESENHO 5.1 b)
print("3. conferir_bloco")
DES = (V411 / "DESENHO_v411.md").read_text(encoding="utf-8")
pt0 = re.search(r"> PT — “(.+?)”\n", DES).group(1)
en0 = re.search(r"> EN — “(.+?)”\n", DES).group(1)
f2 = lambda x: "%.2f" % abs(x)
menos = lambda x: ("−" if x < 0 else "") + f2(x)
n = str(int(abs(p["z_null"])))
EN = (en0.replace("⟨Z against K⟩", menos(p["z_tgl"])).replace("⟨Z against the null⟩", f2(p["z_null"])).replace("⟨n⟩", n)
      .replace("⟨Z of the free Cepheids⟩", f2(cf["z_null"])))
PT = (pt0.replace("⟨Z contra K⟩", menos(p["z_tgl"]).replace(".", ",")).replace("⟨Z contra o nulo⟩", f2(p["z_null"]).replace(".", ","))
      .replace("⟨n⟩", n).replace("⟨Z das Cefeidas livres⟩", f2(cf["z_null"]).replace(".", ",")))
caso("o texto provisório foi montado sem placeholder", "⟨" not in EN + PT)
PAINEL = "**[ENSAIO, não publicar] H0DN × BG1, opened once on 12/11/2026.** " + EN + "\n\n*PT — " + PT + "*"
v0 = h0dn.conferir_bloco(PAINEL, V, "painel", painel=True)
caso("o painel provisório (EN e PT) passa", v0 == [], v0)
caso("6,12 no lugar de 6,11 -> recusa", any("arredondado" in x for x in h0dn.conferir_bloco(PAINEL.replace(f2(p["z_null"]), "6.12"), V, "p")))
caso("Cefeidas sem o número -> F67", any("cefeidas_livres_com_o_numero" in x for x in h0dn.conferir_bloco(
    EN.replace("with free Cepheids the same data give %sσ" % f2(cf["z_null"]), "with free Cepheids the data say less"), V, "p")))
caso("cabeça com um caractere trocado -> recusa", any("cabeça" in x for x in h0dn.conferir_bloco(
    "the head `%s`, under the published error model, free Cepheids 4.38, validity, not creditation, retrodiction, not blind"
    % V["cabeca"].replace("NATURE", "NATURA", 1), V, "p")))
caso("a cabeça exata passa", not any("cabeça" in x for x in h0dn.conferir_bloco("`%s`" % V["cabeca"], V, "p")))
caso("«proved in nature at 7σ» -> recusa", any("inteiro" in x for x in h0dn.conferir_bloco(EN.replace("in nature at %sσ" % n, "in nature at 7σ"), V, "p")))
caso("Cefeidas com o sinal trocado -> recusa", any("sinal" in x for x in h0dn.conferir_bloco(EN.replace("give %sσ" % f2(cf["z_null"]), "give −%sσ" % f2(cf["z_null"])), V, "p")))
caso("painel sem o Z das Cefeidas -> recusa a presença", any("cefeidas_livres.z_null" in x for x in h0dn.conferir_bloco(
    PAINEL.replace(f2(cf["z_null"]), "x").replace(f2(cf["z_null"]).replace(".", ","), "x"), V, "p", painel=True)))
caso("a NOTA da Fase 9 V2 (4,44) não colide com as Cefeidas (4,38)", h0dn.conferir_bloco("z_disc = 4.44, calibrated", V, "p") == [])

# ---------------------------------------------------------------- 4. primordial + README com o registro aberto
print("4. primordial.montar e readme_pinado com o registro aberto (handoff de ensaio)")
selo_v = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))["um_version"]
z = json.loads((TB / "PRIMORDIAL.json").read_text(encoding="utf-8"))["itens"]
hz = lambda k: "%.2f" % z[k]["valor"]
FASE9 = ("Record of 23/10/2026: the Phase 9 V2 Hubble-ratio test gives z_disc = %s calibrated, z_δ = %s, ln B = %s (a Bayes factor, not a σ), "
         "`NOT_FALSIFIED_POWERED`, below the 5σ step; the full panel is in `REGISTRO_FASE9_V2.md`.\n"
         "*PT — registro de 23/10/2026: Fase 9 V2, z_disc = %s calibrado, z_δ = %s, ln B = %s (ln B não é σ), `NOT_FALSIFIED_POWERED`, abaixo do degrau de 5σ; "
         "o painel inteiro está em `REGISTRO_FASE9_V2.md`.*"
         % (hz("hubble.z_disc"), hz("hubble.z_delta"), hz("hubble.lnB_lcdm"), hz("hubble.z_disc").replace(".", ","), hz("hubble.z_delta").replace(".", ","),
            hz("hubble.lnB_lcdm").replace(".", ",")))
P5 = ("PROVED = validity in the kernel; CONFIRMED is accreditation, the one refused word; β_TGL proved in nature at %s σ in the H0DN × BG1 test, "
      "under the published error model (validity, not creditation), with free Cepheids at %sσ, below 5; retrodiction, not blind." % (n, f2(cf["z_null"]))).replace("%s σ" % n, "%sσ" % n)
STATUS = ("What nature decides was read in one channel: β_TGL proved in nature at %sσ in the H0DN × BG1 test under the published error model, with free Cepheids at %sσ; "
          "validity, not creditation; retrodiction, not blind. *PT — β_TGL provado na natureza a %sσ no teste H0DN × BG1, sob o modelo de erros publicado, com as "
          "Cefeidas livres a %sσ; validade, não creditação; retrodição, não cego.*" % (n, f2(cf["z_null"]), n, f2(cf["z_null"]).replace(".", ",")))
PARAG = ("O teste H0DN × BG1 foi aberto uma vez em 12/11/2026, depois do pré-registro público: o primário fica a %s contra o nulo sob o modelo de erros publicado; "
         "as Cefeidas livres ficam a %s; validade, não creditação; retrodição, não cego." % (f2(p["z_null"]).replace(".", ","), f2(cf["z_null"]).replace(".", ",")))
RITOS = ("| Hubble ratio, H0DN × BG1 (v411) | `NOT_FALSIFIED`, branch 4: β_TGL proved in nature at %sσ under the published error model; free Cepheids %s, branch 6; validity, not creditation; retrodiction, not blind | the creditation |\n"
         "| Hubble ratio, Phase 9 V2 | `NOT_FALSIFIED_POWERED` (record, below the H0DN panel) | β in nature at 5σ: that test did not reach the step |" % (n, f2(cf["z_null"])))
PARAG_EN = ("**The H0DN × BG1 test:** opened once on 2026-11-12, after the public pre-registration (commit `769fcb26`); the result is in the panel at the top, "
            "with the free-Cepheids line beside it; the seven caveats and what the test does not decide: `ESTADO_ATUAL.md`.")   # o texto (b) da c1, 12/11
MARC = {"README_PAINEL_H0DN": PAINEL, "README_FASE9_V2": FASE9, "README_PRIMORDIAL_5SIGMA": P5, "README_STATUS_5SIGMA": STATUS,
        "README_H0DN": PARAG, "README_H0DN_EN": PARAG_EN, "README_RITOS": RITOS}
for k, t in MARC.items():
    vv = h0dn.conferir_bloco(t, V, k, painel=(k == "README_PAINEL_H0DN"))
    caso("o texto de ensaio %s passa na conferência" % k, vv == [], vv)
HO = (NOS / ("HANDOFF_%s_CUSTODIA.md" % selo_v)).read_text(encoding="utf-8")
TMP = Path(tempfile.mkdtemp(prefix="h0dn_g1_"))


def handoff(marc):
    corpo = HO + "\n\n" + "".join("<!-- INICIO_%s_%s -->\n%s\n<!-- FIM_%s_%s -->\n\n" % (k, selo_v, t, k, selo_v) for k, t in marc.items())
    hp = TMP / ("HANDOFF_%d.md" % len(list(TMP.iterdir())))
    hp.write_text(corpo, encoding="utf-8")
    return hp


_fonte_orig = PRIM.Construtor.fonte
INJ = {"reg": None}


def _fonte(self, nome, caminho, json_=True, papel=""):
    r = _fonte_orig(self, nome, caminho, json_, papel)
    if nome == "core" and INJ["reg"] is not None:
        r["core"]["h0dn_bg1_v411"] = INJ["reg"]
    return r


PRIM.Construtor.fonte = _fonte
INJ["reg"] = REG
P = PRIM.montar({"handoff": str(handoff(MARC))})
it = P["itens"]
caso("PRIMORDIAL: h0dn.aberto e o registro", it.get("h0dn.aberto", {}).get("valor") is True and it["h0dn.registro"]["valor"] == "h0dn_bg1_v411")
caso("PRIMORDIAL: os números são os do registro", it["h0dn.primario.z_null"]["valor"] == p["z_null"] and it["h0dn.cefeidas_livres.z_null"]["valor"] == cf["z_null"])
caso("PRIMORDIAL: os sete textos vêm do handoff", all(it["h0dn.readme." + i]["fonte"] == "handoff" for i in ("painel", "fase9_v2", "primordial_5sigma", "status_5sigma", "paragrafo", "paragrafo_en", "ritos")))
pb = PRIM.serializar(P)
C = RP.Ctx(P, pb)
readme_disco = (TB / "README.md").read_text(encoding="utf-8")
portas = RP.extrair_portas(readme_disco)
texto, segs = RP.renderizar(C, TPL, PARTES, portas)
i_selo, i_pain, i_f9 = texto.find("**PRIMORDIAL · seal"), texto.find("[ENSAIO, não publicar] H0DN"), texto.find("Record of 23/10/2026")
caso("README: o selo, depois o painel do H0DN, depois a linha da Fase 9 V2", 0 < i_selo < i_pain < i_f9, (i_selo, i_pain, i_f9))
caso("README: o painel inteiro da Fase 9 V2 saiu (EN, PT e a frase do autor)",
     "> **Hubble-ratio test**" not in texto and "*PT \u2014 Raz\u00e3o de Hubble (Fase 9 V2" not in texto and "the author\u2019s judgement" not in texto)
caso("README: a frase do 5σ da linha do PRIMORDIAL saiu e a nova entrou", "is the open step" not in texto and ("> " + P5 + "\n") in texto)
caso("README: o estado trocado", "the decisive open factor is **" not in texto and STATUS in texto)
caso("README: a linha dos ritos trocada", "(the panel at the top)" not in texto and RITOS in texto)
caso("README: o parágrafo do H0DN na parte P = nP trocado", RP.H0DN_FRASE_VELHA_P_IGUAL_NP not in texto and PARAG in texto)
caso("README: o parágrafo do H0DN é bloco GERADO", any(t == "gerado" and nm == "bloco:h0dn_paragrafo" for t, nm, _ in segs))
caso("README: a linha EN do H0DN na parte P = nP trocada", RP.H0DN_LINHA_VELHA_P_IGUAL_NP_EN not in texto and (chr(10) + PARAG_EN + chr(10)) in texto)
caso("README: a linha EN do H0DN é bloco GERADO", any(t == "gerado" and nm == "bloco:h0dn_paragrafo_en" and ct == PARAG_EN for t, nm, ct in segs))
reg_txt = RP.registro_fase9_v2(C)
P_velho = json.loads((TB / "PRIMORDIAL.json").read_text(encoding="utf-8"))
C_velho = RP.Ctx(P_velho, (TB / "PRIMORDIAL.json").read_bytes())
hub_velho = RP.b_primordial(C_velho)
hub_velho = hub_velho[hub_velho.index("> **Hubble-ratio test**"):]
# AO LADO (13/11/2026, decisão da gerência c1, opção (b)): a frase do autor de 02/11 entra CITADA por data e sha16 (regra do operador de 12/11)
hpt_velho = RP.b_hubble_pt(C_velho)
FALA_V = "> *«%s»* — the author, %s (verbatim, sha16 `%s`) `[INPUT: the author’s judgement, not a claim of the program]`\n" % (
    C_velho.v("operador.frase_4_44_sic"), C_velho.v("operador.data"), C_velho.f("operador_verbatim", "sha16"))
CIT_V = ("> *The author’s judgement of %s on this result is cited by date and sha256, not transcribed (verbatim file sha16 `%s`).* "
         "`[INPUT: the author’s judgement, not a claim of the program]`\n" % (C_velho.v("operador.data"), C_velho.f("operador_verbatim", "sha16")))
REGRA_P = CEN / "work" / "cunhagens_13out" / "OPERADOR_12nov_nao_precisa_transcrever_esse_tipo_de_fala_pra_dentro_do_programa_nunca_verbatim.txt"
import hashlib  # noqa: E402
SHA_REGRA = hashlib.sha256(REGRA_P.read_bytes()).hexdigest()[:16]
caso("b_hubble_pt INTACTA: a do README de hoje, com a frase do autor no fim", hpt_velho in readme_disco and hpt_velho.endswith(FALA_V))
caso("REGISTRO_FASE9_V2: o painel EN do README de hoje e o PT igual, exceto a frase do autor, trocada pela citação",
     hub_velho in readme_disco and hub_velho in reg_txt and (hpt_velho[:-len(FALA_V)] + CIT_V) in reg_txt and reg_txt.endswith(CIT_V))
caso("REGISTRO_FASE9_V2: a frase do autor não está transcrita (nem o trecho, nem a linha)", C_velho.v("operador.frase_4_44") not in reg_txt
     and "um sigma" not in reg_txt and FALA_V not in reg_txt and "«" not in reg_txt)
caso("REGISTRO_FASE9_V2: o cabeçalho não diz verbatim e cita a regra de 12/11/2026 pelo sha16 lido do disco (%s)" % SHA_REGRA,
     "verbatim, from" not in reg_txt and "moved here verbatim" not in reg_txt
     and ("under the author’s rule of 12/11/2026 (verbatim file sha16 `%s`)" % SHA_REGRA) in reg_txt
     and "operator" not in reg_txt.split("\n")[4]
     and ("unchanged except for the author’s sentence of %s" % C_velho.v("operador.data")) in reg_txt)
caso("REGISTRO_FASE9_V2: a linha PT dos números da Fase 9 V2 igual (o z_disc com os companheiros)", hpt_velho[:-len(FALA_V)] in reg_txt and RP.regra_444(hpt_velho[:-len(FALA_V)], P) == [])
vreg = textos.portao(RP._neutraliza(reg_txt), RP.conhecidos_de(pb.decode("utf-8")) | {C.prim_sha16, SHA_REGRA}, rotulo="reg") + RP.regra_444(reg_txt, P)
caso("REGISTRO_FASE9_V2 passa o portão e a regra do 4,44", vreg == [], vreg)
vreg0 = textos.portao(RP._neutraliza(reg_txt), RP.conhecidos_de(pb.decode("utf-8")) | {C.prim_sha16}, rotulo="reg")
caso("controle: sem o sha16 da regra nos conhecidos, o portão recusa o registro", any(SHA_REGRA in x for x in vreg0), vreg0)
_regra_orig = RP.REGRA_FALA_12NOV
RP.REGRA_FALA_12NOV = ("OPERADOR_12nov_ARQUIVO_QUE_NAO_EXISTE_verbatim.txt", "12/11/2026")
caso("controle: sem o arquivo da regra em disco, o registro PARA", "nao esta em disco" in (recusa(lambda: RP.registro_fase9_v2(C)) or ""))
RP.REGRA_FALA_12NOV = _regra_orig
_bh_orig = RP.b_hubble_pt
RP.b_hubble_pt = lambda C_: _bh_orig(C_).replace(" — the author, ", " — o autor, ")
caso("controle: a frase do autor mudada no b_hubble_pt, o registro PARA (nunca a transcrição)", "frase do autor" in (recusa(lambda: RP.registro_fase9_v2(C)) or ""))
RP.b_hubble_pt = _bh_orig
vger = [x for t, nm, ct in segs if t == "gerado" for x in textos.portao(RP._neutraliza(ct), RP.conhecidos_de(pb.decode("utf-8")) | {C.prim_sha16}, rotulo=nm)]
caso("README: os segmentos gerados passam o portão", vger == [], vger[:4])
caso("README: a regra do 4,44", RP.regra_444(texto, P) == [], RP.regra_444(texto, P)[:3])
nb, nb0 = len(texto.encode("utf-8")), len(readme_disco.encode("utf-8"))
print("     README de ensaio: %d bytes (hoje %d; teto %d; folga de hoje %d; crescimento líquido do ensaio %+d)" % (nb, nb0, RP.TETO, RP.TETO - nb0, nb - nb0))
caso("a medida do teto existe (o ensaio é informativo)", nb > 0)
caso("sem README_RITOS -> PARA com o nome do marcador", "INICIO_README_RITOS_" + selo_v in (recusa(lambda: PRIM.montar({"handoff": str(handoff({k: t for k, t in MARC.items() if k != "README_RITOS"}))})) or ""))
caso("README_H0DN com «*» -> PARA", "README_H0DN" in (recusa(lambda: PRIM.montar({"handoff": str(handoff(dict(MARC, README_H0DN="*" + PARAG)))})) or ""))
caso("README_H0DN_EN sem o começo «**The H0DN × BG1 test:**» -> PARA", "README_H0DN_EN" in (recusa(lambda: PRIM.montar({"handoff": str(handoff(dict(MARC, README_H0DN_EN=PARAG_EN.replace("**The H0DN × BG1 test:** ", "The test: "))))})) or ""))
caso("README_H0DN_EN em duas linhas -> PARA", "README_H0DN_EN" in (recusa(lambda: PRIM.montar({"handoff": str(handoff(dict(MARC, README_H0DN_EN=PARAG_EN.replace("; the result", ";" + chr(10) + "the result"))))})) or ""))
caso("sem README_H0DN_EN -> PARA com o nome do marcador", "INICIO_README_H0DN_EN_" + selo_v in (recusa(lambda: PRIM.montar({"handoff": str(handoff({k: t for k, t in MARC.items() if k != "README_H0DN_EN"}))})) or ""))
caso("README_FASE9_V2 sem o apontador -> PARA", "REGISTRO_FASE9_V2.md" in (recusa(lambda: PRIM.montar({"handoff": str(handoff(dict(MARC, README_FASE9_V2=FASE9.replace("`REGISTRO_FASE9_V2.md`", "the record"))))})) or ""))
caso("painel com número trocado -> PARA", "README_PAINEL_H0DN" in (recusa(lambda: PRIM.montar({"handoff": str(handoff(dict(MARC, README_PAINEL_H0DN=PAINEL.replace(f2(p["z_null"]), "6.12"))))})) or ""))
INJ["reg"] = None
PRIM.Construtor.fonte = _fonte_orig

# ---------------------------------------------------------------- 5. regressão: sem registro aberto, o README de hoje, byte a byte
print("5. regressão (o espelho de hoje, sem registro aberto)")
P0 = PRIM.montar({})
caso("PRIMORDIAL de hoje sem item h0dn.*", not any(k.startswith("h0dn.") for k in P0["itens"]))
r = subprocess.run([sys.executable, "-X", "utf8", str(TOOLS / "custodia_g1" / "readme_pinado.py"), "--verificar", "--conferir-fontes", "--primordial",
                    str(TB / "PRIMORDIAL.json"), "--template", str(TPL), "--partes", str(PARTES), "--readme", str(TB / "README.md"), "--pino",
                    str(TB / "PINO_README.json"), "--nos", str(NOS), "--espelho", str(TB)], capture_output=True, text=True, encoding="utf-8", cwd=str(CEN))
ult = (r.stdout.strip().splitlines() or ["?"])[-1]
caso("readme_pinado.py --verificar --conferir-fontes: CONFERE (rc 0)", r.returncode == 0 and "CONFERE" in ult, r.stdout[-600:] + r.stderr[-300:])
print("     ", ult)

# ---------------------------------------------------------------- 6. textos.avaliar_fontes
print("6. textos.avaliar_fontes")


class _H:
    def __init__(self, corpos):
        self.corpos = corpos
        self.marcadores = set(corpos)
        self.problemas = []

    def paragrafos_prontos(self):
        return []


class _BD:
    titulo_pt = "ensaio"


class _Ctx:
    def __init__(self, corpos, aceitar):
        self.handoff, self.bloco_diario, self.versao, self.aceitar_molde = _H(corpos), _BD(), "v411", aceitar


_core_orig = textos._core_da_versao
base = {"%s_v411" % k: "x" for k in textos.MARCADORES_OPCIONAIS}
try:
    textos._core_da_versao = lambda ctx: CORE_AB
    o = textos.avaliar_fontes(_Ctx(dict(base), True), {"E04", "E08"})
    esp = {"%s_v411" % k for k in h0dn.TODOS}
    caso("aberto, sem os marcadores do H0DN: faltam e bloqueia mesmo com --aceitar-molde", esp <= set(o["faltam"]) and o["bloqueia"] is True, o["faltam"])
    o = textos.avaliar_fontes(_Ctx(dict(base, **{k: "x" for k in esp}), False), {"E04", "E08"})
    caso("aberto, com todos os marcadores: não bloqueia", o["bloqueia"] is False and not o["faltam"], o)
    o = textos.avaliar_fontes(_Ctx(dict(base, **{k: "x" for k in esp if not k.startswith("README_")}), False), {"E04"})
    caso("aberto, só a E04 pendente: os README_* não são pedidos", o["bloqueia"] is False, o["faltam"])
    textos._core_da_versao = lambda ctx: {"h0dn_bg1_v410": {"opened_once": False}}
    o = textos.avaliar_fontes(_Ctx(dict(base), False), {"E04", "E08"})
    caso("não aberto: nada do H0DN é pedido", o["bloqueia"] is False and "h0dn_aberto" not in o, o)
finally:
    textos._core_da_versao = _core_orig

# ---------------------------------------------------------------- 7. o acervo (TOPO_RATIFICADO_v411.json; AO LADO, 12/11/2026)
print("7. os textos ratificados, lidos com o acervo")
TOP = json.loads((V411 / "TOPO_RATIFICADO_v411.json").read_text(encoding="utf-8"))
CORE_REAL = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
A = h0dn.acervo(CORE_REAL)
caso("o acervo lido do core: 11 cobranças, 0 falsificadas, 6/2/2/1; z_disc 4,44", A["n_cobrancas"] == 11 and A["falsificadas"] == 0
     and A["categorias"] == {"NOT_FALSIFIED": 6, "INCONCLUSIVE": 2, "AWAITING": 2, "EXCLUDED_IN_READING": 1} and "%.2f" % A["z_disc"] == "4.44", A)
fxr = lambda x, pt: (("−" if x < 0 else "") + "%.2f" % abs(x)).replace(".", "," if pt else ".")


def encher(t, pt):
    m = {"⟨Z contra K⟩": fxr(p["z_tgl"], 1), "⟨Z against K⟩": fxr(p["z_tgl"], 0), "⟨Z contra o nulo⟩": fxr(p["z_null"], 1), "⟨Z against the null⟩": fxr(p["z_null"], 0),
         "⟨n⟩": n, "⟨Z das Cefeidas livres⟩": fxr(cf["z_null"], 1), "⟨Z of the free Cepheids⟩": fxr(cf["z_null"], 0),
         "⟨N cobranças⟩": str(A["n_cobrancas"]), "⟨N charges⟩": str(A["n_cobrancas"]),
         "⟨não falsificadas⟩": str(A["categorias"]["NOT_FALSIFIED"]), "⟨not falsified⟩": str(A["categorias"]["NOT_FALSIFIED"]),
         "⟨inconclusivas⟩": str(A["categorias"]["INCONCLUSIVE"]), "⟨inconclusive⟩": str(A["categorias"]["INCONCLUSIVE"]),
         "⟨à espera de dado⟩": str(A["categorias"]["AWAITING"]), "⟨awaiting data⟩": str(A["categorias"]["AWAITING"]),
         "⟨excluídas na leitura⟩": str(A["categorias"]["EXCLUDED_IN_READING"]), "⟨excluded in reading⟩": str(A["categorias"]["EXCLUDED_IN_READING"]),
         "⟨z_disc⟩": fxr(A["z_disc"], pt), "⟨z_delta⟩": fxr(A["z_delta"], pt), "⟨lnB⟩": fxr(A["lnB"], pt)}
    for k_, v_ in m.items():
        t = t.replace(k_, v_)
    return t


for k in ("pt", "en", "painel_readme_pt", "painel_readme_en", "estado_pt", "estado_en"):
    t = encher(TOP[k], k.endswith("pt"))
    vv = h0dn.conferir_bloco(t, V, k, painel=k.startswith("painel"), acervo=A) + textos.portao(RP._neutraliza(t), set(), rotulo=k)
    caso("ratificado %s (%d B): F67, números do registro e do acervo, portão" % (k, len(t.encode("utf-8"))), "⟨" not in t and vv == [], vv)
caso("11 trocado por 12 -> recusa", any("cobranças" in x for x in h0dn.conferir_bloco(encher(TOP["estado_pt"], 1).replace(" 11 ", " 12 "), V, "e", acervo=A)))
caso("«nenhuma falsificada» com 1 falsificada no livro -> recusa", any("falsificada" in x for x in h0dn.conferir_bloco(
    encher(TOP["estado_pt"], 1), V, "e", acervo=dict(A, falsificadas=1))))
caso("inconclusivas 3 no lugar de 2 -> recusa", any("INCONCLUSIVE" in x for x in h0dn.conferir_bloco(encher(TOP["pt"], 1).replace("inconclusivas: 2", "inconclusivas: 3"), V, "a", acervo=A)))
caso("z_disc 4,45 no lugar de 4,44 -> recusa", any("fase9_v2.z_disc" in x for x in h0dn.conferir_bloco(encher(TOP["pt"], 1).replace("4,44", "4,45"), V, "a", acervo=A)))
caso("livro que não fecha -> recusa o acervo", recusa(lambda: h0dn.acervo({**CORE_REAL, "estatuto_da_prova_v391": {"prova_2_ritos": dict(
    CORE_REAL["estatuto_da_prova_v391"]["prova_2_ritos"], n_cobrancas=12)}})) is not None)
r444 = RP.regra_444(encher(TOP["en"], 0), json.loads((TB / "PRIMORDIAL.json").read_text(encoding="utf-8")))
print("     a regra do 4,44 do README sobre o resumo EN ratificado (informativo; o resumo não passa pelo README):", r444 or "passa")

print("\nRESULTADO: %d ok, %d falha(s)%s" % (RES["ok"], len(RES["falhas"]), (": " + "; ".join(RES["falhas"])) if RES["falhas"] else ""))
sys.exit(1 if RES["falhas"] else 0)
