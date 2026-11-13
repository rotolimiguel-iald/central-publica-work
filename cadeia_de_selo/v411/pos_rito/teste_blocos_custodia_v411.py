# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411-posrito, a servico da gerencia c1] o TESTE dos textos da custodia (blocos_custodia_v411.py) SEM o core da v411: o registro do ensaio offline no lugar dele
# [AO LADO, 12/11/2026 tarde, mesmo autor] D174: o painel inteiro (controle: sem a frase do acervo e' recusado); os apontadores do H0DN; a medida com o handoff de ENSAIO da v411 (sufixo _v411) e o teto de 40.960 B
# [AO LADO, 12/11/2026 11h, mesmo autor] aditivo 4: os textos saem de TOPO_RATIFICADO_v411.json; o acervo (estatuto_da_prova_v391) entra no core de teste; controles novos (falsificada, soma, marcador que sobra)
"""teste_blocos_custodia_v411.py -- monta os textos da custodia com o core da v410 selada (so' leitura, do Nos: a Fase 9 V2, o acervo e as bandeiras) e o registro `h0dn_bg1_v411` do ensaio offline
(TESTE_H0DN_OFFLINE_v411_registro.json, no lugar do core da v411, que ainda nao existe); confere cada texto com as MESMAS funcoes da custodia, com a F67 estrita e com a guarda de frases da v411; roda os controles
negativos (cada um TEM de ser recusado); e MEDE o README projetado pelo renderizador da custodia (primordial.montar + readme_pinado.renderizar, como o testar_h0dn_marcadores.py dela), com e sem o corte da frase
do acervo do painel curto (aditivo 4, item 3). Nada e' escrito no Nos, no espelho, na Central nem na pasta da cadeia: a saida vai para C:\\t\\k411c\\ensaio_topo_proposto\\pos_rito_blocos\\. rc 0 so' se tudo passar.
uso: python -B -X utf8 teste_blocos_custodia_v411.py [--sem-readme]"""
import copy
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, PK)
import blocos_custodia_v411 as B  # noqa: E402
from custodia_g1 import h0dn as H0DN, textos as TXG1  # noqa: E402

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
TB = r"C:\IALD\Artigo\the_boundary"
OUT = r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos"
os.makedirs(OUT, exist_ok=True)
RES = {"ok": 0, "falhas": []}


def caso(nome, cond, det=""):
    if cond:
        RES["ok"] += 1
    else:
        RES["falhas"].append({"caso": nome, "detalhe": str(det)[:600]})
        print("  FALHA", nome, str(det)[:300])


t0 = time.time()
CORE10 = json.loads(open(os.path.join(NOS, "um_absoluto.json"), "rb").read().decode("utf-8"))["core"]
REG = json.loads(open(os.path.join(PK, "TESTE_H0DN_OFFLINE_v411_registro.json"), "rb").read().decode("utf-8"))
CORE = {k: CORE10[k] for k in ("teste_de_veracidade_fase9_v397", "kernel_formalization", "estatuto_da_prova_v391")}
CORE["h0dn_bg1_v411"] = REG
CTX = B.contexto_do_core(CORE)
T, rel = B.montar(CORE, CTX)
V = B.conferir(T, CORE)
TJ, FONTE = B.ler_topo()

# ---- 1. todo texto passa, e e' o que a lista da custodia pede
caso("os marcadores sao os da custodia + os dois extras", set(T) == set(B.MARCADORES_CUSTODIA) | set(B.MARCADORES_EXTRAS), sorted(T))
for mk, v in V.items():
    caso("o texto %s passa (forma, F67 e F67 estrita, numeros, cabeca, sigma, portao, 4,44, guarda v411)" % mk, v == [], v)
p, cf = REG["values"]["primario"], REG["values"]["cefeidas_livres"]
zc_en, zc_pt = "%.2f" % cf["z_null"], ("%.2f" % cf["z_null"]).replace(".", ",")
for mk in ("README_PAINEL_H0DN", "README_PRIMORDIAL_5SIGMA", "README_STATUS_5SIGMA", "README_RITOS", "NOTA_EN", "ESTATUTO_LINHA_EN", "ESTATUTO_CURTO_EN", "ESTATUTO_P2_EN", "X_TEXTO"):
    caso("%s traz o numero das Cefeidas livres lido do registro" % mk, zc_en in T[mk] or zc_pt in T[mk])
NN = B.numeros(CORE)
caso("D174: o painel e' o render INTEIRO do arquivo ratificado, com a frase do acervo", T["README_PAINEL_H0DN"] == B.preencher(TJ["painel_readme_en"], "en", NN, TJ) + "\n" + B.preencher(TJ["painel_readme_pt"], "pt", NN, TJ)
     and B.preencher(B.FRASE_DO_ACERVO["en"], "en", NN, TJ) in T["README_PAINEL_H0DN"] and B.preencher(B.FRASE_DO_ACERVO["pt"], "pt", NN, TJ) in T["README_PAINEL_H0DN"])
at = REG["values"]["atos"]
caso("D174: as duas linhas do H0DN da parte do Clay sao apontadores (sem decimal), com a data e o commit curto lidos dos atos", all(not re.search(r"\d[.,]\d", T[k]) for k in ("README_H0DN", "README_H0DN_EN"))
     and at["commit_do_pre_registro"][:8] in T["README_H0DN"] and at["commit_do_pre_registro"][:8] in T["README_H0DN_EN"] and at["inicio_da_abertura_utc"][:10] in T["README_H0DN_EN"]
     and T["README_H0DN_EN"].startswith("**The H0DN × BG1 test:** ") and "reservations" in T["README_H0DN_EN"] and T["README_H0DN"].endswith("estão na leitura inteira."))
caso("D174: README_H0DN_EN esta' na lista da G1 (nao e' mais extra) e o trecho do handoff nao o duplica", "README_H0DN_EN" in B.MARCADORES_CUSTODIA and "README_H0DN_EN" not in B.MARCADORES_EXTRAS)
est_en = B.preencher(TJ["estado_en"], "en", B.numeros(CORE), TJ); est_pt = B.preencher(TJ["estado_pt"], "pt", B.numeros(CORE), TJ)
caso("a NOTA traz a frase de estado EN inteira, verbatim", est_en in T["NOTA_EN"])
caso("ESTATUTO_LINHA_EN e' a frase de estado EN (so' o negrito acrescentado)", T["ESTATUTO_LINHA_EN"].replace("**", "") == est_en)
caso("ESTATUTO_CURTO_EN e CURTO_PT_ASCII sao a frase de estado em ASCII", T["ESTATUTO_CURTO_EN"] == B.ascii_de(est_en) and T["ESTATUTO_CURTO_PT_ASCII"] == B.ascii_de(est_pt) and T["ESTATUTO_CURTO_EN"].isascii() and T["ESTATUTO_CURTO_PT_ASCII"].isascii())
caso("as duas linhas do estado terminam na frase de estado inteira", T["ESTATUTO_P2_ESTADO_EN"].endswith(est_en[0].lower() + est_en[1:] + "*") and T["ESTATUTO_P2_ESTADO_PT"].endswith(est_pt[0].lower() + est_pt[1:] + "*"))
caso("o rotulo do P2 e' o do arquivo (rotulo_p2) e P2_NOT_DETERMINED fica, dito como registro selado", TJ["rotulo_p2"] in T["ESTATUTO_P2_EN"] and "P2_NOT_DETERMINED" in T["ESTATUTO_P2_EN"] and "three_stress_tests_v387" in T["ESTATUTO_P2_EN"])
caso("o p2_en termina antes de «the tensions measured …»; a secao_md sem ponto final; o p_curto antes de «, and the tensions …»", T["ESTATUTO_P2_EN"].endswith("in either direction:") and not T["ESTATUTO_SECAO_MD"].endswith(".") and not T["ESTATUTO_P_CURTO_EN"].endswith("."))
caso("a creditacao e' a palavra do operador («do observador que reler» / «the observer who rereads») onde a formula fala de quem credita", "observer who rereads" in T["NOTA_EN"] and "observador que reler" in T["ESTATUTO_SECAO_MD"] and "whoever observes from outside" not in json.dumps(T, ensure_ascii=False))
caso("o painel curto nao traz o numero da Fase 9 V2; a linha logo abaixo traz, com «not a σ» em EN", "4.44" not in T["README_PAINEL_H0DN"] and "4,44" not in T["README_PAINEL_H0DN"] and "not a σ" in T["README_FASE9_V2"])
caso("os textos sao RATIFICADOS (a fonte e' o arquivo, com o sha256 lido)", rel["ratificada"] is True and rel["proposta"] is False and rel["fonte"]["sha256"] == FONTE["sha256"])
caso("nenhum numero digitado no arquivo-fonte fora dos marcadores (painel e estado)", not any(re.search(r"\d[.,]\d", re.sub("⟨[^⟩]*⟩", "", TJ[k])) for k in ("painel_readme_en", "painel_readme_pt", "estado_en", "estado_pt")))
caso("beta nunca literal em texto nenhum", not any(re.search(r"0[.,]0120", t) for t in T.values()))
caso("«nenhuma foi falsificada» so' com falsificadas == 0 no core (lido)", CORE["estatuto_da_prova_v391"]["prova_2_ritos"]["falsificadas"] == 0 and "none was falsified" in T["NOTA_EN"])


# ---- 2. controles negativos (cada um TEM de ser recusado)
def recusa(mk, t, rotulo, quer=None):
    v = B.conferir({mk: t}, CORE)[mk]
    ok = bool(v) and (quer is None or any(quer in x for x in v))
    caso("controle negativo: %s" % rotulo, ok, v[:3])


recusa("README_PAINEL_H0DN", T["README_PAINEL_H0DN"].replace(" Beside it: free Cepheids **%sσ**, below 5." % zc_en, "").replace(" Ao lado: Cefeidas livres %sσ, abaixo de 5." % zc_pt, ""), "o painel sem a linha das Cefeidas livres", "cefeidas")
caso("o controle dos ritos acha a oracao das Cefeidas para tirar", ("; beside it, free Cepheids give %sσ, below 5" % zc_en) in T["README_RITOS"])
recusa("README_RITOS", T["README_RITOS"].replace("; beside it, free Cepheids give %sσ, below 5" % zc_en, ""), "a linha dos ritos sem as Cefeidas livres", "cefeidas")
recusa("README_PRIMORDIAL_5SIGMA", T["README_PRIMORDIAL_5SIGMA"].replace(", under the published error model", ""), "o primordial sem «under the published error model»", "modelo_publicado")
recusa("README_PAINEL_H0DN", T["README_PAINEL_H0DN"].replace(B.preencher(B.FRASE_DO_ACERVO["en"], "en", NN, TJ), "").replace(B.preencher(B.FRASE_DO_ACERVO["pt"], "pt", NN, TJ), ""), "D174: o painel sem a frase do acervo", "render INTEIRO")
recusa("README_H0DN_EN", T["README_H0DN_EN"].replace("the result is in the panel at the top", "the primary lies 6.11σ against the null"), "D174: a linha EN do H0DN com decimal", "sem decimal")
recusa("README_H0DN_EN", T["README_H0DN_EN"].replace("**The H0DN × BG1 test:** ", "The test: "), "D174: a linha EN do H0DN sem o comeco que a G1 exige", "comecar por")
recusa("README_STATUS_5SIGMA", T["README_STATUS_5SIGMA"].replace("validity, not creditation; ", "").replace("validade, não creditação; ", ""), "o estado sem «validade, não creditação»", "validade_nao_creditacao")
recusa("README_PAINEL_H0DN", T["README_PAINEL_H0DN"].replace("%.2f" % p["z_null"], "6.12", 1), "o painel com o Z do primario trocado (6,12)", "arredondado")
recusa("README_PAINEL_H0DN", T["README_PAINEL_H0DN"].replace("at %dσ" % int(p["z_null"]), "at 7σ"), "«proved in nature at 7σ»", "inteiro")
recusa("README_STATUS_5SIGMA", T["README_STATUS_5SIGMA"].replace(". *Provada", ".\n\n*Provada"), "o estado com linha em branco", "linha em branco")
recusa("README_H0DN", "*" + T["README_H0DN"] + "*", "o H0DN com asterisco", "«*»")
recusa("README_PRIMORDIAL_5SIGMA", T["README_PRIMORDIAL_5SIGMA"] + "\nsegunda linha", "o primordial em duas linhas", "uma linha")
recusa("README_RITOS", T["README_RITOS"] + "\ntexto solto", "os ritos com linha que nao e' de tabela", "tabela")
recusa("README_FASE9_V2", T["README_FASE9_V2"].replace("`NOT_FALSIFIED_POWERED`, ", ""), "a Fase 9 V2 sem NOT_FALSIFIED_POWERED (a regra do 4,44)", "NOT_FALSIFIED_POWERED")
recusa("README_FASE9_V2", T["README_FASE9_V2"].split("\n")[0].replace("(a Bayes factor, not a σ)", "(which is not σ)"), "a linha EN da Fase 9 V2 com a forma antiga «which is not σ» (sem «not a σ» nem Bayes)", "Bayes")
recusa("README_FASE9_V2", T["README_FASE9_V2"].replace("`%s`" % B.REGISTRO_FASE9_V2_MD, "the record"), "a Fase 9 V2 sem o apontador", B.REGISTRO_FASE9_V2_MD)
recusa("README_FASE9_V2", T["README_FASE9_V2"] + " {{ONDE_FICA_O_PAINEL_DA_FASE9}}", "chaves duplas", "«{{»")
recusa("README_PAINEL_H0DN", T["README_PAINEL_H0DN"] + " z_disc = 4.44σ.", "o painel curto com o numero da Fase 9 V2", "Fase 9 V2")
recusa("ESTATUTO_CURTO_EN", T["ESTATUTO_CURTO_EN"].replace(" sigma", "σ", 1), "o CURTO_EN com σ (o trecho e' ASCII)", "ASCII")
recusa("ESTATUTO_LINHA_EN", T["ESTATUTO_LINHA_EN"].replace("the test is not blind", "this was a blind test"), "«blind test» afirmado", "F63")
recusa("ESTATUTO_LINHA_06_PT", T["ESTATUTO_LINHA_06_PT"] + " O teste tem poder certificado.", "«poder certificado»", "F61")
recusa("ESTATUTO_SECAO_MD", T["ESTATUTO_SECAO_MD"] + ". Hoje, enfim, sabemos: a TGL foi confirmada pela natureza", "a palavra da creditacao afirmada", "F60")
recusa("NOTA_EN", T["NOTA_EN"].replace("validity, not creditation", "validity"), "a NOTA sem «validity, not creditation»", "creditacao")
recusa("X_TEXTO", T["X_TEXTO"].replace("; beside it, free Cepheids give %sσ, below 5" % zc_en, ""), "o X sem a linha das Cefeidas livres (EN)", "cefeidas")
recusa("ESTATUTO_P_CURTO_EN", T["ESTATUTO_P_CURTO_EN"].replace("a retrodiction without fit; the test is not blind; ", ""), "o P_CURTO sem retrodicao nem «not blind» (F67 estrita)", "F67 estrita")


def recusa_montar(rotulo, core_mut, quer, topo_mut=None):
    orig = B.ler_topo
    if topo_mut is not None:
        B.ler_topo = lambda: (topo_mut, FONTE)
    try:
        B.montar(core_mut, CTX); caso("controle negativo: %s RECUSA" % rotulo, False, "montou")
    except ValueError as e:
        caso("controle negativo: %s RECUSA" % rotulo, quer in str(e), e)
    finally:
        B.ler_topo = orig


c1 = copy.deepcopy(CORE); c1["h0dn_bg1_v411"] = {k: v for k, v in REG.items() if k != "p2_ao_lado_da_v387"}
recusa_montar("sem p2_ao_lado_da_v387", c1, "p2_ao_lado_da_v387")
c2 = copy.deepcopy(CORE); c2["h0dn_bg1_v411"]["all_verified"] = False
recusa_montar("registro nao selado", c2, "all_verified")
c3 = copy.deepcopy(CORE); c3["estatuto_da_prova_v391"]["prova_2_ritos"]["falsificadas"] = 1
recusa_montar("o livro com uma cobranca falsificada (a frase «nenhuma foi falsificada» nao sai)", c3, "falsificada")
c4 = copy.deepcopy(CORE); c4["estatuto_da_prova_v391"]["prova_2_ritos"]["ledger"]["INCONCLUSIVE"] += 1
recusa_montar("as categorias do livro que nao somam as cobrancas", c4, "nao somam")
tj5 = copy.deepcopy(TJ); tj5["painel_readme_en"] = tj5["painel_readme_en"] + " ⟨marcador sem leitor⟩"
recusa_montar("um marcador que sobra no texto emitido", CORE, "sobrou marcador", tj5)
tj6 = copy.deepcopy(TJ); tj6["rotulo_p2"] = "OUTRO_ROTULO"
recusa_montar("o rotulo do P2 do arquivo diferente do do registro", CORE, "rotulo do P2", tj6)

# ---- 3. o trecho do handoff (marcadores lidos pelo parser da custodia)
SEC = B.secao_handoff(T, rel)
RX = re.compile(r"<!-- INICIO_(?P<id>[A-Za-z0-9_]+) -->\r?\n(?P<corpo>.*?)<!-- FIM_(?P=id) -->", re.S)
lidos = {m.group("id"): m.group("corpo").strip("\n") for m in RX.finditer(SEC)}
caso("o trecho do handoff traz cada texto entre os seus marcadores, igual ao montado", all(lidos.get("%s_v411" % k) == v for k, v in T.items()) and len(lidos) == len(T), sorted(set(lidos) ^ {"%s_v411" % k for k in T}))
vsec = TXG1.portao(SEC, {FONTE["sha256"]}, rotulo="secao") + ["guarda %s" % r for r, _ in B.GF.violacoes(SEC)]
caso("o trecho inteiro passa no portao da G1 e na guarda de frases da v411", vsec == [], vsec[:4])

# ---- 4. o README projetado (D174): o handoff de ENSAIO o mais perto possivel do real da v411 -- os sete textos da prosa (os do S6d: TITULO_EN, ARCO_EN, ARCO_PT...), o PARAGRAFO da v411 com o titulo de textos_v411,
#      os textos da abertura, todos com o sufixo _v411, no arquivo HANDOFF_v411_CUSTODIA.md de uma pasta de ensaio -- e o renderizador da custodia, com o selo carregado dizendo v411 (so' em memoria). Criterio: o README
#      inteiro em ate' 40.960 B (o teto da G1); se nao couber, a cadeia PARA (nada e' cortado).
MED = {}
TETO = 40960


def _titulo_paragrafo_v411():
    import ast as _ast
    arv = _ast.parse(open(os.path.join(HERE, "textos_v411.py"), encoding="utf-8").read())
    for no in arv.body:
        if isinstance(no, _ast.Assign) and any(isinstance(t_, _ast.Name) and t_.id == "_TITULO_PARAGRAFO_V411" for t_ in no.targets):
            return _ast.literal_eval(no.value)
    raise ValueError("textos_v411.py sem _TITULO_PARAGRAFO_V411")


def handoff_de_ensaio_v411():
    """o handoff de ENSAIO da v411 (o corpo do fechar so' existe com o core real; o README so' le dele os marcadores, o titulo do ultimo PARAGRAFO_*_v411 e o nome/sha16 do arquivo)."""
    import textos_custodia_handoff_v411 as TC
    import hashlib as _h
    core = copy.deepcopy(CORE); core["external_ladder"] = copy.deepcopy(CORE10["external_ladder"]); core["kh_n1_cobertura_v411"] = copy.deepcopy(CORE10["kh_n1_cobertura_v410"])
    core["cunhagens_v411"] = {"verbatim": {"fala_%d" % i_: {"quando": "12/11/2026 (ensaio)"} for i_ in range(TC.DL.N_FALAS_V411)}}
    esc = core["external_ladder"]["n_theorems_clean"]; pin = _h.sha256(b"um.py de ENSAIO da medida do README").hexdigest()
    selo = {"um_version": "v411", "sha256": {"um.py": pin}}; esp = {"candidato_sha16": pin[:16], "vereditos_novos_v411": {"h0dn_bg1_v411": REG["verdict"]}}
    diario = "## 12/11/2026 — **v411 SELADA** `%s` — O teste decisivo (v411): nenhum módulo novo, escada %d → %d\n" % (pin[:16], esc, esc)
    TEXTOS, readme, Bx, relx, nums = TC.compor(core, selo, esp, diario, None, PK)
    tit = _titulo_paragrafo_v411()
    corpo = ("# HANDOFF v411 — CUSTÓDIA (ENSAIO da medida do README; não é o handoff real)\n\n**O que é:** `um.py` **v411** `%s` (1 B) sobre a v410 `5d9497a721c3589e`; %d/%d; COMPLETA; rc 0; selftest PASSED; gate intocado; ensaio.\n\n"
             "<!-- INICIO_PARAGRAFO_H0DN_v411 -->\n%s\n\n> (o corpo do parágrafo pronto da v411 só sai do core real; o README só lê dele o título)\n<!-- FIM_PARAGRAFO_H0DN_v411 -->\n\n" % (pin[:16], esc, esc, tit)
             + "".join("<!-- INICIO_%s_v411 -->\n%s\n<!-- FIM_%s_v411 -->\n\n" % (k_, t_, k_) for k_, t_ in TEXTOS)
             + readme + "\n\n" + B.secao_handoff(Bx, relx, "v411") + "\n")
    hp = os.path.join(OUT, "HANDOFF_v411_CUSTODIA.md")
    open(hp + ".tmpw", "wb").write(corpo.encode("utf-8")); os.replace(hp + ".tmpw", hp)
    return hp, dict(TEXTOS), tit, Bx


def projetar(hp):
    from custodia_g1 import primordial as PRIM, readme_pinado as RP
    _orig = PRIM.Construtor.fonte

    def _fonte(self, nome, caminho, json_=True, papel=""):
        r = _orig(self, nome, caminho, json_, papel)
        if nome == "core":
            r["core"]["h0dn_bg1_v411"] = REG
        if nome == "selo":
            r["um_version"] = "v411"   # (so' em memoria: o Nos e' a v410; o renderizador procura os marcadores com o sufixo da versao do selo)
        return r
    PRIM.Construtor.fonte = _fonte
    try:
        P = PRIM.montar({"handoff": hp})
        pb = PRIM.serializar(P); C = RP.Ctx(P, pb)
        readme_disco = open(os.path.join(TB, "README.md"), "rb").read().decode("utf-8")
        texto, segs = RP.renderizar(C, os.path.join(TB, "tools", "readme_pinado", "readme_template.md"), os.path.join(TB, "tools", "readme_pinado", "readme_partes"), RP.extrair_portas(readme_disco))
        reg_txt = RP.registro_fase9_v2(C)
    finally:
        PRIM.Construtor.fonte = _orig
    return texto, segs, readme_disco, reg_txt, P, C, pb, RP


if "--sem-readme" not in sys.argv:
    hp, TX7, TIT, BX = handoff_de_ensaio_v411()
    caso("o handoff de ensaio usa os MESMOS textos da abertura que este teste confere (a NOTA difere SO' pela clausula das inscricoes, que o core de ensaio do S6d traz)",
         all(BX[k_] == T[k_] for k_ in T if k_ != "NOTA_EN") and re.sub(r" and the \d+ inscriptions of \d\d/\d\d", "", BX["NOTA_EN"]) == T["NOTA_EN"], [k_ for k_ in T if BX[k_] != T[k_]])
    texto, segs, readme_disco, reg_txt, P, C, pb, RP = projetar(hp)
    nb, nb0 = len(texto.encode("utf-8")), len(readme_disco.encode("utf-8"))
    vg = [x for tp, nm, ct in segs if tp == "gerado" for x in TXG1.portao(RP._neutraliza(ct), RP.conhecidos_de(pb.decode("utf-8")) | {C.prim_sha16}, rotulo=nm)]
    for nome_, conteudo_ in (("README_PROJETADO_v411.md", texto), ("REGISTRO_FASE9_V2_PROJETADO.md", reg_txt)):
        open(os.path.join(OUT, nome_) + ".tmpw", "wb").write(conteudo_.encode("utf-8")); os.replace(os.path.join(OUT, nome_) + ".tmpw", os.path.join(OUT, nome_))
    um = re.match(r"(.+?\.)(?:\s|$)", TX7["ARCO_EN"]); mt = re.search(r"^###\s*(.+?)\s*(?:—|-)\s*par", TIT, re.M)   # (os MESMOS recortes do b_mudou e do primordial.py da G1, lidos)
    mudou = {"primeira_frase_do_ARCO_EN": um.group(1) if um else None, "bytes_primeira_frase": len(um.group(1).encode("utf-8")) if um else None,
             "titulo_do_PARAGRAFO_v411": mt.group(1).strip() if mt else None, "bytes_titulo": len(mt.group(1).strip().encode("utf-8")) if mt else None,
             "nome_do_handoff": os.path.basename(hp), "bytes_nome": len(os.path.basename(hp).encode("utf-8"))}
    mudou["bytes_frase_mais_titulo"] = (mudou["bytes_primeira_frase"] or 0) + (mudou["bytes_titulo"] or 0)
    linha_en_hoje = "**The H0DN × BG1 test:** pre-registered; no observed data read; it was not opened"
    MED = {"readme_hoje_bytes": nb0, "readme_projetado_bytes": nb, "teto_bytes": TETO, "folga_projetada": TETO - nb, "crescimento_liquido_bytes": nb - nb0, "cabe": nb <= TETO,
           "a_linha_EN_do_H0DN_trocada_no_render": (T["README_H0DN_EN"] in texto and linha_en_hoje not in texto),
           "nota_da_linha_EN": "o renderizador da custodia de hoje (readme_pinado.py, H0DN_LINHA_VELHA_P_IGUAL_NP_EN e o bloco h0dn_paragrafo_en) JA' troca a linha EN; a medida acima ja' a inclui (nada somado a parte)",
           "o_que_mudou_no_readme": mudou, "bytes_de_cada_bloco_novo": {mk: len(T[mk].encode("utf-8")) for mk in ("README_PAINEL_H0DN", "README_FASE9_V2", "README_PRIMORDIAL_5SIGMA", "README_STATUS_5SIGMA", "README_H0DN", "README_H0DN_EN", "README_RITOS")},
           "handoff_de_ensaio": hp, "handoff_de_ensaio_sha256": __import__("hashlib").sha256(open(hp, "rb").read()).hexdigest(), "readme_projetado": os.path.join(OUT, "README_PROJETADO_v411.md"),
           "renderizador": "custodia_g1.primordial.montar + readme_pinado.renderizar (os da custodia, so' leitura; em memoria: o registro do ensaio offline no core e o selo dizendo v411)"}
    caso("README projetado: o painel do H0DN logo depois do selo, depois a linha da Fase 9 V2", 0 < texto.find("**PRIMORDIAL · seal") < texto.find("**Hubble-ratio test H0DN × BG1**") < texto.find("> Record, Phase 9 V2"))
    caso("README projetado: o painel inteiro, com a frase do acervo", T["README_PAINEL_H0DN"] in texto)
    caso("README projetado: o painel inteiro da Fase 9 V2 saiu do topo e esta' no registro ao lado", "> **Hubble-ratio test** (Phase 9 V2" not in texto and "> **Hubble-ratio test**" in reg_txt)
    caso("README projetado: as trocas entraram (primordial, estado, ritos, as duas linhas do H0DN)", ("> " + T["README_PRIMORDIAL_5SIGMA"] + "\n") in texto and T["README_STATUS_5SIGMA"] in texto and T["README_RITOS"] in texto and T["README_H0DN"] in texto and T["README_H0DN_EN"] in texto)
    caso("README projetado: «What changed» traz a primeira frase do ARCO_EN da v411 e o titulo do PARAGRAFO da v411", bool(um and mt) and um.group(1) in texto and mt.group(1).strip() in texto)
    caso("README projetado: a primeira frase do ARCO_EN mais o titulo cabem em 185 B (D174, D)", mudou["bytes_frase_mais_titulo"] <= 185, mudou)
    caso("README projetado: os segmentos gerados passam no portao", vg == [], vg[:3])
    caso("README projetado: a regra do 4,44", RP.regra_444(texto, P) == [], RP.regra_444(texto, P)[:3])
    caso("README projetado: a F67 da custodia no README inteiro", H0DN.f67(texto) == [], H0DN.f67(texto)[:3])
    caso("README projetado: o README inteiro em ate' 40.960 B (senao a cadeia PARA; nada e' cortado)", nb <= TETO, nb)

out = {"contrato": "TESTE_BLOCOS_CUSTODIA_v411", "quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "duracao_s": round(time.time() - t0, 1), "ok": RES["ok"], "falhas": RES["falhas"], "TUDO_PASSOU": not RES["falhas"],
       "substituto_do_core": "core da v410 selada (Nos, so' leitura: teste_de_veracidade_fase9_v397, kernel_formalization, estatuto_da_prova_v391) + TESTE_H0DN_OFFLINE_v411_registro.json no lugar de h0dn_bg1_v411; sem cunhagens_v411 (a NOTA sai sem a clausula das inscricoes)",
       "fonte": rel["fonte"], "relatorio": {k: v for k, v in rel.items() if k != "fonte"}, "textos": T, "bytes": {k: len(v.encode("utf-8")) for k, v in T.items()}, "conferencias": V, "readme": MED}
p_ = os.path.join(OUT, "TESTE_BLOCOS_CUSTODIA_v411.json")
open(p_ + ".tmpw", "wb").write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")); os.replace(p_ + ".tmpw", p_)
print("teste dos blocos da custodia: %d ok, %d falha(s); README %s" % (RES["ok"], len(RES["falhas"]), ("%d B (hoje %d; liquido %+d; teto %d; folga %d)" % (MED["readme_projetado_bytes"], MED["readme_hoje_bytes"], MED["crescimento_liquido_bytes"], MED["teto_bytes"], MED["folga_projetada"])) if MED else "nao medido"))
print("saida:", p_)
sys.exit(0 if not RES["falhas"] else 1)
