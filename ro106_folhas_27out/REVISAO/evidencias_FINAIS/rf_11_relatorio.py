# -*- coding: utf-8 -*-
# Monta REVISAO_RO106_CARTAS_FINAIS.md e .json a partir das saidas dos scripts rf_01..rf_10 (hashes e numeros lidos por script, nunca de memoria).
# Revisor sonnet-ro106-revisor-final. Somente leitura sobre K; escreve apenas em K/REVISAO/.
import collections, datetime, difflib, hashlib, json, pathlib, re, unicodedata

K = pathlib.Path("C:/IALD/Central de Patentes/work/ro106_folhas_27out")
R = K / "REVISAO"
E = R / "evidencias_FINAIS"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def comma(x, nd=4):
    return f"{x:.{nd}f}".replace(".", ",")


# ------------------------------------------------------------------ hashes
ARQ = {
    "576_final_pdf": "CARTA_REGRA_26_4_050576_FINAL.pdf", "576_final_md": "CARTA_REGRA_26_4_050576_FINAL.md",
    "579_final_pdf": "CARTA_REGRA_26_4_050579_FINAL.pdf", "579_final_md": "CARTA_REGRA_26_4_050579_FINAL.md",
    "576_aceita_pdf": "CARTA_REGRA_26_4_050576.pdf", "576_aceita_md": "CARTA_REGRA_26_4_050576.md",
    "579_aceita_pdf": "CARTA_REGRA_26_4_050579.pdf", "579_aceita_md": "CARTA_REGRA_26_4_050579.md",
    "576_anexo": "FOLHAS_SUBSTITUTIVAS_050576.pdf", "579_anexo": "FOLHAS_SUBSTITUTIVAS_050579.pdf",
    "576_conferencia": "CONFERENCIA_050576.json", "579_conferencia": "CONFERENCIA_050579.json",
    "576_depositado": "entrada/aprendizado/04_DESENHOS_como_depositado.pdf", "579_depositado": "entrada/mqc/04_DESENHOS_CINZA_como_depositado.pdf",
    "gerador_final": "fontes/carta_final.py", "gerador_base": "fontes/carta.py",
}
H = {k: {"arquivo": v, "sha256": sha(K / v)} for k, v in ARQ.items()}
for k in H:
    H[k]["sha16"] = H[k]["sha256"][:16]
ESPERADO = {"576_aceita_md": "dbe1caff15ed32e4", "576_aceita_pdf": "a72a89c3571cb828", "579_aceita_md": "29029f0a6e2b0c4c", "579_aceita_pdf": "2378f978494f2fdf",
            "576_anexo": "884d978a39b20d1a", "579_anexo": "4faa43ca81442fc5", "576_conferencia": "d171e2bc9be9668e", "579_conferencia": "529ca8412ad6baa1",
            "576_depositado": "1c09a448482ccc81", "579_depositado": "2ef675ed2a3d2a7c"}
for k, v in ESPERADO.items():
    assert H[k]["sha16"] == v, (k, H[k]["sha16"], v)

# ------------------------------------------------------------------ C1: multiconjunto removido/acrescentado == so as 4 diferencas
def toks(s):
    s = unicodedata.normalize("NFC", s).replace("\f", "\n").replace("\u00ad", "")
    s = re.sub(r"(?<=\w)[-\u2010\u2011]\n(?=\w)", "", s).replace("\n", " ")
    return [re.sub(r"[-\u2010\u2011]", "", t) for t in s.split()]


def md_toks(p):
    s = unicodedata.normalize("NFC", pathlib.Path(p).read_text(encoding="utf-8"))
    s = re.sub(r"^\|[-:| ]+\|\s*$", " ", s, flags=re.M)
    s = re.sub(r"(?m)^> ", "", s)
    s = re.sub(r"(?m)^# ", "", s)
    s = s.replace("**", "").replace("|", " ")
    s = re.sub(r"  \n", "\n", s)
    return toks(s)


NOTA = "Minuta preparada pela Central de Patentes em 27/10/2026 (rodada 2, após revisão), para liberação do operador. Não enviada. Assinatura, local e data são do operador; a suficiência jurídica é do agente de PI [LEGAL]."
VELHO_LOCAL = "[local], [data]"
NOVO_LOCAL = "Goiânia, 4 de novembro de 2026"
VELHO_ASS = "[ASSINATURA E IDENTIFICAÇÃO — a preencher pelo operador]"
NOVO_ASS = "ROTOLI MIGUEL, Luiz Antonio — Requerente Assinado eletronicamente no envio pelo ePCT."
VELHO_3C = "todos os números, letras e sinais de referência com altura mínima de 0,32 cm;"
NOVO_3C = "algarismos, maiúsculas e letras com haste com altura mínima de 0,32 cm (inclusive nos sinais de referência);"

C1 = {}
for pct, tag in (("050576", "576"), ("050579", "579")):
    velho = [NOTA, VELHO_LOCAL, VELHO_ASS] + ([VELHO_3C] if tag == "579" else [])
    novo = [NOVO_LOCAL, NOVO_ASS] + ([NOVO_3C] if tag == "579" else [])
    Cold = collections.Counter(t for s in velho for t in toks(s))
    Cnew = collections.Counter(t for s in novo for t in toks(s))
    r = {}
    # PDF (texto PyMuPDF), tirando as linhas de cabecalho repetidas da tabela
    def pdf_t(p):
        raw = pathlib.Path(p).read_text(encoding="utf-8")
        hdr = ["Fig.", "Folha substituída", "Folha de substituição", "Diferenças em relação à folha substituída"]
        ln = raw.split("\n")
        out, i, n = [], 0, 0
        while i < len(ln):
            if ln[i:i + 4] == hdr:
                n += 1
                i += 4
                continue
            out.append(ln[i])
            i += 1
        return toks("\n".join(out)), n

    pa, na = pdf_t(E / f"txt_{tag}_aceita.fitz.txt")
    pb, nb = pdf_t(E / f"txt_{tag}_final.fitz.txt")
    ma = md_toks(K / H[f"{tag}_aceita_md"]["arquivo"])
    mb = md_toks(K / H[f"{tag}_final_md"]["arquivo"])
    for nome, a, b in (("pdf", pa, pb), ("md", ma, mb)):
        ca, cb = collections.Counter(a), collections.Counter(b)
        rem, add = ca - cb, cb - ca
        ok_rem, ok_add = rem == (Cold - Cnew), add == (Cnew - Cold)
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        blocos = sum(1 for op in sm.get_opcodes() if op[0] != "equal")
        r[nome] = {"tokens_aceita": len(a), "tokens_final": len(b), "blocos_de_diferenca": blocos,
                   "removido_igual_ao_esperado": ok_rem, "acrescentado_igual_ao_esperado": ok_add,
                   "removido_total_tokens": sum(rem.values()), "acrescentado_total_tokens": sum(add.values())}
        assert ok_rem and ok_add, (pct, nome, rem - (Cold - Cnew), (Cold - Cnew) - rem, add - (Cnew - Cold), (Cnew - Cold) - add)
    r["cabecalho_tabela_repetido_pdf"] = {"aceita": na, "final": nb}
    # diff literal por linhas dos md
    la = pathlib.Path(K / H[f"{tag}_aceita_md"]["arquivo"]).read_text(encoding="utf-8").split("\n")
    lb = pathlib.Path(K / H[f"{tag}_final_md"]["arquivo"]).read_text(encoding="utf-8").split("\n")
    ops = [(op, i1 + 1, i2, j1 + 1, j2) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if op != "equal"]
    r["md_linhas_diferentes"] = [{"op": op, "aceita_linhas": f"{i1}-{i2}", "final_linhas": f"{j1}-{j2}"} for op, i1, i2, j1, j2 in ops]
    # par. 4 e tabela
    def par4(t):
        m = re.search(r"\*\*4\. Declaração\.\*\*.*?(?=\n\n\*\*5\.)", t, flags=re.S)
        return m.group(0)
    ta_, tb_ = "\n".join(la), "\n".join(lb)
    r["par4_sha16"] = {"aceita": hashlib.sha256(par4(ta_).encode()).hexdigest()[:16], "final": hashlib.sha256(par4(tb_).encode()).hexdigest()[:16]}
    r["par4_igual"] = par4(ta_) == par4(tb_)
    r["tabela_linhas"] = {"aceita": sum(1 for x in la if x.startswith("|")), "final": sum(1 for x in lb if x.startswith("|")),
                          "iguais": [x for x in la if x.startswith("|")] == [x for x in lb if x.startswith("|")]}
    assert r["par4_igual"] and r["tabela_linhas"]["iguais"]
    # extrator cruzado: pdftotext -raw (sem tirar cabecalho; o multiconjunto nao depende da ordem)
    # (o poppler desfaz a hifenizacao por conta propria, p.ex. «op-/erador» vira «op» «erador»; por isso a conferencia e por caractere, sem espaco nem hifen)
    def sq(t):
        return re.sub(r"[\s\-‐‑­]", "", unicodedata.normalize("NFC", t))
    ra = collections.Counter(sq((E / f"txt_{tag}_aceita.pdftotext_raw.txt").read_text(encoding="utf-8")))
    rb = collections.Counter(sq((E / f"txt_{tag}_final.pdftotext_raw.txt").read_text(encoding="utf-8")))
    co, cn = collections.Counter(sq(" ".join(velho))), collections.Counter(sq(" ".join(novo)))
    r["pdftotext_raw_caracteres_igual_ao_esperado"] = ((ra - rb) == (co - cn)) and ((rb - ra) == (cn - co))
    assert r["pdftotext_raw_caracteres_igual_ao_esperado"], (pct, (ra - rb) - (co - cn), (co - cn) - (ra - rb), (rb - ra) - (cn - co), (cn - co) - (rb - ra))
    C1[pct] = r
PAR4 = C1["050576"]["par4_sha16"]["final"]
assert PAR4 == C1["050579"]["par4_sha16"]["final"] == C1["050576"]["par4_sha16"]["aceita"]

# ------------------------------------------------------------------ C3: alturas
alt = j(E / "rf_08_alturas_por_glifo.json")
cf = j(K / "CONFERENCIA_050579.json")
fol = cf["medidas_das_folhas_novas"]["folhas"]
linhas_med = sum(f["linhas_cap_alg_asc_medidas"] for f in fol)
min_json = min(f["altura_minima_caractere_cm_texto_vivo"] for f in fol)
abaixo_json = sum((f["linhas_abaixo_0_32"] if not isinstance(f["linhas_abaixo_0_32"], list) else len(f["linhas_abaixo_0_32"])) for f in fol)
xlinhas = [(f["folha"], it) for f in fol for it in f["so_altura_x_abaixo_0_32 (letras sem haste; fora do critério)"]]
assert linhas_med == 393 and abs(min_json - 0.351) < 1e-9 and abaixo_json == 0 and len(xlinhas) == 1
M = alt["050579"]["classes"]
A = alt["050576"]["classes"]
cls_alg, cls_cap, cls_asc, cls_x = "algarismo", "maiuscula (latina/grega)", "minuscula com haste (b d f h k l)", "minuscula sem haste (a c e m n o r s u v w x z)"
for D in (M, A):
    assert D[cls_alg]["abaixo_0_32"] == [] and D[cls_cap]["abaixo_0_32"] == [] and D[cls_asc]["abaixo_0_32"] == []
    assert D[cls_x]["minimo_cm"] < 0.32 and D[cls_x]["maximo_cm"] < 0.32
spans = j(E / "rf_07_spans_pequenos.json")
assert spans["050579"]["spans_menores_que_13_5_pt"] == [] and spans["050576"]["spans_menores_que_13_5_pt"] == []
tam579 = spans["050579"]["tamanhos_pt_fonte_caracteres"]
tam576 = spans["050576"]["tamanhos_pt_fonte_caracteres"]

# ------------------------------------------------------------------ C4/C5: anexos e orientacao
an = j(E / "rf_05_anexos.json")
ori = j(E / "rf_06_orientacao.json")
for pct in ("050576", "050579"):
    assert an[pct]["confere"] and an[pct]["paginas"] == an[pct]["paginas_esperadas"]
    assert all(x["paisagem_medida"] == x["paisagem_declarada_na_carta"] for x in ori[pct])
figs576 = {f["folha"]: f["figuras_no_texto"] for f in an["050576"]["folhas"]}
figs579 = {f["folha"]: f["figuras_no_texto"] for f in an["050579"]["folhas"]}
assert figs576 == {1: [1], 2: [2, 3], 3: [4, 5], 4: [6, 7], 5: [8], 6: [9]}
assert figs579 == {i: [i] for i in range(1, 9)}
dep576 = {f["folha"]: f["figuras_no_texto"] for f in an["050576"]["depositado"]["folhas"]}
dep579 = {f["folha"]: f["figuras_no_texto"] for f in an["050579"]["depositado"]["folhas"]}
assert dep576 == {1: [1, 2], 2: [3, 4], 3: [5, 6], 4: [7, 8], 5: [9]} and dep579 == {1: [1, 2, 3], 2: [4, 5, 6], 3: [7, 8]}

# tabela de figuras da carta FINAL (md) x medido nos anexos e nos depositados, figura a figura
def tabela_md(p):
    linhas = [l for l in pathlib.Path(p).read_text(encoding="utf-8").split("\n") if re.match(r"^\|\s*\d+\s*\|", l)]
    out = {}
    for l in linhas:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        out[int(c[0])] = (c[1], c[2])
    return out


for pct, tag, depm, newm, nfig, ndep, nnew in (("050576", "576", dep576, figs576, 9, 5, 6), ("050579", "579", dep579, figs579, 8, 3, 8)):
    tb = tabela_md(K / H[f"{tag}_final_md"]["arquivo"])
    assert sorted(tb) == list(range(1, nfig + 1)), tb.keys()
    for fig, (dp, nw) in tb.items():
        d_sheet = [s for s, fs in depm.items() if fig in fs]
        n_sheet = [s for s, fs in newm.items() if fig in fs]
        assert len(d_sheet) == 1 and len(n_sheet) == 1
        assert dp == f"{d_sheet[0]}/{ndep}", (pct, fig, dp, d_sheet)
        assert nw == f"{n_sheet[0]}/{nnew}", (pct, fig, nw, n_sheet)

# nada do outro PCT dentro de cada carta final (md e texto do PDF)
OUTRO = {"576": ["050579", "BR102026003460", "8 folhas", "1/8", "MQC"], "579": ["050576", "BR102026005477", "6 folhas", "1/6", "Aprendizado", "PHO"]}
for tag, termos in OUTRO.items():
    for t in (K / H[f"{tag}_final_md"]["arquivo"]).read_text(encoding="utf-8"), (E / f"txt_{tag}_final.fitz.txt").read_text(encoding="utf-8"):
        assert not [x for x in termos if x in t], (tag, [x for x in termos if x in t])

# RO/106 originais: sha256 x marcos_fixos.json; linhas do CONTROLE_GERAL; cores nas descricoes
RO = {"576": K.parent.parent / "EPCT/BR102026005477-1_APRENDIZADO_CONTINUO/RECIBOS/PCTBR2026050576-ro106-1-pt-20261009.pdf",
      "579": K.parent.parent / "EPCT/BR102026003460-6_MQC/RECIBOS/PCTBR2026050579-ro106-1-pt-20261009.pdf"}
marcos = (K.parent.parent / "andamentos/marcos_fixos.json").read_text(encoding="utf-8")
RO_S = {}
for tag, p in RO.items():
    RO_S[tag] = sha(p)
    assert RO_S[tag] in marcos, tag
cg = (K.parent.parent / "EPCT/CONTROLE_GERAL.md").read_text(encoding="utf-8").split("\n")
CG = {}
for tag, pct, ref in (("576", "PCT/BR2026/050576", "BR102026005477-1"), ("579", "PCT/BR2026/050579", "BR102026003460-6")):
    ls = [i + 1 for i, l in enumerate(cg) if pct in l and ref in l and "04/10" in l]
    assert ls, tag
    CG[tag] = ls[0]
import fitz
APPB579 = K.parent.parent / "EPCT/BR102026003460-6_MQC/RECIBOS/DOCUMENTOS_OFICIAIS_WIPO_20261004/PCTBR2026050579-appb-000003-pt-20261004.pdf"
t579 = "\n".join(pg.get_text("text") for pg in fitz.open(APPB579))
COR = {"azul": t579.count("azul"), "vermelh": t579.count("vermelh"), "verde": t579.count("verde")}
assert sum(COR.values()) == 9, COR
assert A["outra letra minuscula (Script Small L)"]["minimo_cm"] == 0.0 and A["outra letra minuscula (Greek Phi Symbol)"]["minimo_cm"] == 0.0

# ------------------------------------------------------------------ C2/C6
mk = j(E / "rf_04b_marcas_tres_extratores.json")
for k, v in mk.items():
    assert v["marcas"] == [] and v["pessoais"] == [], k
dados_pdf = j(E / "rf_04_marcas_e_dados.json")
for t in ("576_final", "579_final"):
    assert dados_pdf[t]["annots"] == [] and dados_pdf[t]["links"] == [] and dados_pdf[t]["embfiles"] == []
meta = j(E / "rf_02_texto_pdf.json")
for t in ("576_final", "579_final"):
    assert not any(meta[t]["metadata"].get(x) for x in ("title", "author", "subject", "keywords")) and meta[t]["xmp_len"] == 0 and meta[t]["paginas"] == 2

# ------------------------------------------------------------------ evidencias
EV = {}
for p in sorted(E.iterdir()):
    if p.is_file():
        EV[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()[:16]

agora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

MQC_ALG, MQC_CAP, MQC_ASC, MQC_X = M[cls_alg], M[cls_cap], M[cls_asc], M[cls_x]
APR_ALG, APR_CAP, APR_ASC, APR_X = A[cls_alg], A[cls_cap], A[cls_asc], A[cls_x]

SUB = {
    "AGORA": agora,
    "H576P": H["576_final_pdf"]["sha16"], "H576M": H["576_final_md"]["sha16"], "H579P": H["579_final_pdf"]["sha16"], "H579M": H["579_final_md"]["sha16"],
    "H576P_S": H["576_final_pdf"]["sha256"], "H579P_S": H["579_final_pdf"]["sha256"], "H576M_S": H["576_final_md"]["sha256"], "H579M_S": H["579_final_md"]["sha256"],
    "A576P": H["576_aceita_pdf"]["sha16"], "A576M": H["576_aceita_md"]["sha16"], "A579P": H["579_aceita_pdf"]["sha16"], "A579M": H["579_aceita_md"]["sha16"],
    "X576": H["576_anexo"]["sha16"], "X579": H["579_anexo"]["sha16"], "X576_S": H["576_anexo"]["sha256"], "X579_S": H["579_anexo"]["sha256"],
    "D576": H["576_depositado"]["sha16"], "D579": H["579_depositado"]["sha16"],
    "G_FINAL": H["gerador_final"]["sha16"], "G_BASE": H["gerador_base"]["sha16"],
    "PAR4": PAR4,
    "RO576": RO_S["576"][:16], "RO579": RO_S["579"][:16], "CG576": str(CG["576"]), "CG579": str(CG["579"]),
    "COR_AZUL": str(COR["azul"]), "COR_VERM": str(COR["vermelh"]), "COR_VERDE": str(COR["verde"]),
    "A_L_N": str(A["outra letra minuscula (Script Small L)"]["n"]), "A_PHI_N": str(A["outra letra minuscula (Greek Phi Symbol)"]["n"]),
    "N_TOK_576_A": str(C1["050576"]["pdf"]["tokens_aceita"]), "N_TOK_576_F": str(C1["050576"]["pdf"]["tokens_final"]),
    "N_TOK_579_A": str(C1["050579"]["pdf"]["tokens_aceita"]), "N_TOK_579_F": str(C1["050579"]["pdf"]["tokens_final"]),
    "B_PDF_576": str(C1["050576"]["pdf"]["blocos_de_diferenca"]), "B_PDF_579": str(C1["050579"]["pdf"]["blocos_de_diferenca"]),
    "B_MD_576": str(C1["050576"]["md"]["blocos_de_diferenca"]), "B_MD_579": str(C1["050579"]["md"]["blocos_de_diferenca"]),
    "REM_576": str(C1["050576"]["pdf"]["removido_total_tokens"]), "ADD_576": str(C1["050576"]["pdf"]["acrescentado_total_tokens"]),
    "REM_579": str(C1["050579"]["pdf"]["removido_total_tokens"]), "ADD_579": str(C1["050579"]["pdf"]["acrescentado_total_tokens"]),
    "MDL_576": "; ".join(f"aceita {x['aceita_linhas']} -> final {x['final_linhas']}" for x in C1["050576"]["md_linhas_diferentes"]),
    "MDL_579": "; ".join(f"aceita {x['aceita_linhas']} -> final {x['final_linhas']}" for x in C1["050579"]["md_linhas_diferentes"]),
    "TAB_576": str(C1["050576"]["tabela_linhas"]["final"]), "TAB_579": str(C1["050579"]["tabela_linhas"]["final"]),
    "JSON_MIN": comma(min_json, 3), "JSON_LIN": str(linhas_med), "JSON_X_TXT": xlinhas[0][1]["texto"], "JSON_X_H": comma(xlinhas[0][1]["h_max_cm"], 3), "JSON_X_F": str(xlinhas[0][0]),
    "M_ALG_N": str(MQC_ALG["n"]), "M_ALG_MIN": comma(MQC_ALG["minimo_cm"]), "M_CAP_N": str(MQC_CAP["n"]), "M_CAP_MIN": comma(MQC_CAP["minimo_cm"]),
    "M_ASC_N": str(MQC_ASC["n"]), "M_ASC_MIN": comma(MQC_ASC["minimo_cm"]), "M_X_N": str(MQC_X["n"]), "M_X_MIN": comma(MQC_X["minimo_cm"]), "M_X_MAX": comma(MQC_X["maximo_cm"]),
    "A_ALG_N": str(APR_ALG["n"]), "A_ALG_MIN": comma(APR_ALG["minimo_cm"]), "A_CAP_N": str(APR_CAP["n"]), "A_CAP_MIN": comma(APR_CAP["minimo_cm"]),
    "A_ASC_N": str(APR_ASC["n"]), "A_ASC_MIN": comma(APR_ASC["minimo_cm"]), "A_X_N": str(APR_X["n"]), "A_X_MIN": comma(APR_X["minimo_cm"]), "A_X_MAX": comma(APR_X["maximo_cm"]),
}

MD = r"""# REVISÃO INDEPENDENTE FINAL — cartas da Regra 26.4 (respostas aos RO/106 de 09/10/2026)

Revisor: `sonnet-ro106-revisor-final` (não preparou o kit, as folhas nem as cartas). Data: @@AGORA@@. Pasta K = `C:\IALD\Central de Patentes\work\ro106_folhas_27out`. Prazo fatal 09/12/2026 [DERIVED]. Escopo: só as quatro diferenças permitidas frente às cartas aceitas e as checagens C1 a C7. Nada foi enviado, assinado, regenerado nem alterado; escrevi só em `K\REVISAO\` (este arquivo, o `.json` e `evidencias_FINAIS\`); sem rede, sem provedor, sem `.env`, sem credenciais, sem `C:\Escritorio`. Estatutos: o medido é [REAL]; suficiência jurídica é [LEGAL]; o que a gerência informou e eu não reli na fonte é [DECLARADO].

## VEREDITO

| PCT | cartas revistas (sha16 lido por script) | veredito |
|---|---|---|
| PCT/BR2026/050576 (Aprendizado Contínuo) | `CARTA_REGRA_26_4_050576_FINAL.pdf` `@@H576P@@`; `.md` `@@H576M@@` | **ACEITA** |
| PCT/BR2026/050579 (MQC) | `CARTA_REGRA_26_4_050579_FINAL.pdf` `@@H579P@@`; `.md` `@@H579M@@` | **ACEITA** |

Nenhum reparo necessário nas duas. As cartas finais diferem das aceitas só nas quatro diferenças permitidas (C1); não sobrou rascunho (C2); a frase nova do item 3(c) é verdadeira contra a medida (C3); número do pedido, referência, data, requerente, total de folhas, anexo e tabela de figuras estão certos e não trocados (C4); batem com as decisões do operador de 02/11/2026 (C5); não há dado pessoal além do que já consta do RO/106 (C6). Há sete observações não bloqueantes (O1 a O7, abaixo), para a gerência decidir; nenhuma delas exige regenerar. ACEITA aqui quer dizer que tentei achar um defeito material e não achei; não quer dizer que o INPI aceitará (isso é [LEGAL], do agente de PI).

## A partitura, lida antes do resultado (regra do posto do assistente)

Na língua do operador: esta revisão decide só quatro coisas, e todas são de fato, não de opinião. (1) A carta final é a carta aceita mais as quatro mudanças que ele autorizou, e nada além. (2) Não sobrou rascunho nem dado pessoal. (3) Os números, as datas, o anexo e a tabela de cada carta pertencem àquele pedido e não ao outro, e conferem com o formulário do INPI. (4) A frase nova sobre a altura das letras no MQC diz o que foi medido. Ela NÃO decide se o INPI vai aceitar a resposta (isso é do agente de PI), NÃO libera a frase B4 (essa é dele), NÃO envia nada e NÃO mede de novo as folhas. Um RECUSADA significaria um defeito material que eu consigo apontar com número ou trecho na carta, nunca uma falsificação de teoria; ACEITA significa o contrário: procurei e não achei. As escolhas do meu desenho, ditas antes: comparei o texto por palavra com dois extratores de PDF (PyMuPDF e poppler) e por caractere sem espaço nem hífen, ignorando só quebra de linha, hifenização e paginação (pontuação, dígitos e acentos contam); li as páginas também como imagem; medi a altura das letras pelo contorno da fonte vezes o corpo do texto, não pelo pixel, em quatro classes (algarismo, maiúscula, minúscula com ascendente, minúscula sem ascendente), lendo «letras com haste» como a gerência lê (ascendente) e testando também a leitura larga de «haste» (ver O1). Onde a leitura larga muda o resultado, digo qual dos dois é: ambiguidade de palavra (parede medida), não falsificação da afirmação pretendida.

## Mapa de rotas (consulta feita antes, só leitura)

`rotas.py consultar "RO/106"` devolveu 5 rotas (livro de 1650 registros, cabeça `eac85d927e114b22`); `"Regra 26.4"` e `"folhas de substituição"`, 2 cada; `"carta final"`, 0. A única que trata desta frente é `pi.pct.ro106_mqc_aprendizado_09dez` (EM_CURSO, 1 registro, 12/10/2026, veredito `RO106_ABERTO__CENTRAL_REGENERA__TRANSMISSAO_SO_COM_REVISAO_ACEITA_E_FRASE_B4`): prazo-base 09/12/2026 [DERIVED]; defeito registrado: as descrições citam cores (MQC 9 menções; conferi no appb depositado: azul @@COR_AZUL@@, vermelho @@COR_VERM@@, verde @@COR_VERDE@@) e tratar isso sem matéria nova é decisão [LEGAL]; pode vir convite da Regra 26.3ter; «não refazer»: a medição das figuras e a localização dos desenhos depositados. As outras (`patentes.atualizacao_12out.levantamento`, `pi.pct.controles_entrega009_19out`, `pct.ordem009.despacho`, `infra.estado_da_casa_fila_operador`) são contexto. O mapa NÃO tem registro das revisões R2/R3, das decisões de 02/11 nem das cartas finais: a gerência registra (bloco no fim).

## C1 — diferenças de conteúdo além das quatro

**Resposta: não há.** [REAL]

Método: texto dos PDFs por PyMuPDF e, de controle, por `pdftotext -raw`; NFC; hifenização de fim de linha unida; hífen interno de compostos tirado; linha de cabeçalho da tabela (repetida na 2.ª página) tirada e contada; `difflib.SequenceMatcher` por palavra; depois, a prova mais forte: o multiconjunto de palavras removidas (aceita menos final) é IGUAL ao das palavras da nota «Minuta…», de «[local], [data]», do marcador «[ASSINATURA…]» (e, no MQC, da frase antiga do 3(c)) e o multiconjunto das acrescentadas é IGUAL ao de «Goiânia, 4 de novembro de 2026», do bloco do requerente (e, no MQC, da frase nova do 3(c)); qualquer palavra a mais ou a menos quebraria a igualdade (o script a verifica com `assert`: `evidencias_FINAIS\rf_11_relatorio.py`).

| | 050576 | 050579 |
|---|---|---|
| PDF aceita → final (palavras normalizadas) | @@N_TOK_576_A@@ → @@N_TOK_576_F@@; removidas @@REM_576@@, acrescentadas @@ADD_576@@; @@B_PDF_576@@ blocos de diferença, todos nas diferenças (1), (2), (3) | @@N_TOK_579_A@@ → @@N_TOK_579_F@@; removidas @@REM_579@@, acrescentadas @@ADD_579@@; @@B_PDF_579@@ blocos, todos em (1), (2), (3), (4) |
| md aceita → final | @@B_MD_576@@ blocos; `diff` literal por linha: @@MDL_576@@ | @@B_MD_579@@ blocos; `diff` literal por linha: @@MDL_579@@ |
| parágrafo 4 («não acrescentam matéria nova») | idêntico: sha16 `@@PAR4@@` nas quatro cartas (aceita e final, os dois PCT) | idêntico (mesmo sha16) |
| linhas da tabela de figuras | @@TAB_576@@ linhas idênticas, uma a uma | @@TAB_579@@ linhas idênticas, uma a uma |
| controle cruzado | o mesmo vale no texto de `pdftotext -raw`, por multiconjunto de caracteres sem espaço nem hífen (o poppler desfaz a hifenização à sua maneira: removido = nota + local/data + marcador; acrescentado = data + bloco do requerente); a comparação por caractere sem espaço nem hífen só acusa esses mesmos trechos e a mudança de lugar do cabeçalho repetido da tabela (paginação) | idem, mais o 3(c) |

As quatro diferenças, onde caem: (1) nota «Minuta preparada pela Central… Não enviada.» removida; (2) «[local], [data]» → «Goiânia, 4 de novembro de 2026»; (3) «[ASSINATURA E IDENTIFICAÇÃO — a preencher pelo operador]» → «ROTOLI MIGUEL, Luiz Antonio — Requerente» + «Assinado eletronicamente no envio pelo ePCT.»; (4) só no 050579, item 3(c): «todos os números, letras e sinais de referência com altura mínima de 0,32 cm» → «algarismos, maiúsculas e letras com haste com altura mínima de 0,32 cm (inclusive nos sinais de referência)». Paginação mudou (3 → 2 páginas no 050576; o bloco de assinatura agora fica na 2.ª página junto do último parágrafo; 2 → 2 no 050579), como permitido. PDF final × md final: 1 bloco (050576) e 3 (050579), todos de apresentação e já presentes nos PDFs aceitos: cabeçalho da tabela («Figura / Folha substituída (como depositada)» no md, «Fig. / Folha substituída» no PDF), «𝒜_C» (md) × «A_C» (PDF), «α²» × «α2» (sobrescrito extraído como dígito). Também li as quatro páginas finais como imagem (`pg_*_final_p*.png`): conferem com o texto.

## C2 — marcas de rascunho nos PDFs finais

**Resposta: nenhuma.** [REAL] Três extratores (PyMuPDF, `pdftotext -raw`, `-layout`) e os dois md: zero ocorrências de «minuta», «não enviada», «a preencher», «[LEGAL]», «[local]», «[data]», «[ASSINATURA», «rascunho», «TODO», «XXX», «liberação do operador», «operador», «preench». Nas cartas aceitas o mesmo teste acusa as marcas que elas têm («Minuta», «Não enviada», «a preencher», «[LEGAL]», «[local]», «[data]», «[ASSINATURA», «liberação do operador», «operador»): controle positivo, o teste enxerga o que procura. Colchetes que restam e por que são conteúdo: 050576: `[1]`, `[3]`, `[4]`, `[5]` (rótulos de caixa da Fig. 1), `[033]` (parágrafo da descrição; texto conferido no appb: «Estratificação gravitacional … VACUUM … GRAVITON … PHOTON»), e `[15]`; 050579: `[0056]` (parágrafo da descrição; contém «AC = −Tr(ρ log ρ) + λ Tr(ρ · PΠ) (22)») e `[15]`. O `[15]` não está na lista do pedido: é o número do documento IB/313 na lista do ePCT (título do visualizador «(IB/313) Notification of Defects in the International Application [15]», lido nas capturas de 07/10 das duas pastas `RECIBOS`), não um campo a preencher (ver O5). Sem anotações, links, anexos embutidos, JavaScript nem criptografia; todas as fontes embutidas; 2 páginas A4 em cada; sem título, autor nem XMP nos metadados (só «XeTeX output» e «MiKTeX-dvipdfmx»); sem caractere de substituição nem de uso privado.

## C3 — a frase nova do item 3(c) do MQC contra `CONFERENCIA_050579.json`

**Resposta: verdadeira.** [REAL] E a frase antiga era falsa para as minúsculas sem ascendente, como a gerência diz. Duas medidas, a do preparador e a minha:

- No JSON do preparador: `medidas_das_folhas_novas`: @@JSON_LIN@@ linhas de texto classificadas maiúscula/algarismo/ascendente, mínimo **@@JSON_MIN@@ cm**, **0** linhas abaixo de 0,32 cm; a única linha só de altura-x abaixo de 0,32 é «@@JSON_X_TXT@@» na folha @@JSON_X_F@@, **@@JSON_X_H@@ cm**. O critério declarado lá (`obs_altura`): «letras minusculas sem haste (altura-x) nao entram [LEGAL: leitura usual da Regra 11.13(h)]»; note que o preparador chama «sem haste» justamente as de altura-x (a c e m n o r s u v w x z), o que sustenta a leitura pretendida «com haste = ascendente».
- Minha medida independente (não usa o p90 por linha dele): altura de cada glifo de texto vivo acima da linha de base = contorno da fonte (FreeType; Arial Narrow do Windows, STIXGeneral do matplotlib) × corpo do trecho no PDF. Todos os trechos do anexo do MQC têm 14 ou 15 pt (nenhum sub ou sobrescrito reduzido; nenhum trecho abaixo de 13,5 pt):

| classe (anexo `FOLHAS_SUBSTITUTIVAS_050579.pdf`) | glifos | mínimo | abaixo de 0,32 cm |
|---|---:|---:|---:|
| algarismos | @@M_ALG_N@@ | **@@M_ALG_MIN@@ cm** | 0 |
| maiúsculas (latinas e gregas; o mínimo é 𝒜 em STIX, folha 5) | @@M_CAP_N@@ | **@@M_CAP_MIN@@ cm** | 0 |
| minúsculas com ascendente (b d f h k l) | @@M_ASC_N@@ | **@@M_ASC_MIN@@ cm** | 0 |
| minúsculas SEM ascendente (a c e m n o r s u v w x z) | @@M_X_N@@ | **@@M_X_MIN@@ a @@M_X_MAX@@ cm** | todos |

Logo: a frase nova («algarismos, maiúsculas e letras com haste … 0,32 cm») é verdadeira na leitura «haste = ascendente» (mínimos por classe: maiúsculas @@M_CAP_MIN@@, algarismos @@M_ALG_MIN@@, ascendentes @@M_ASC_MIN@@ cm; todos acima de 0,32). A frase antiga («todos os números, letras e sinais de referência com altura mínima de 0,32 cm») era falsa se «altura» da minúscula for a altura-x: @@M_X_N@@ glifos medem @@M_X_MIN@@ a @@M_X_MAX@@ cm. (Se o critério de «altura» for a das maiúsculas e ascendentes da fonte, e não a altura-x das minúsculas, a antiga também seria verdadeira; essa é a escolha [LEGAL] «altura-x» que as revisões anteriores já registraram.) Mesma conta no Aprendizado, para a frase que lá já estava aceita: algarismos mín. @@A_ALG_MIN@@ cm (@@A_ALG_N@@), maiúsculas @@A_CAP_MIN@@ (@@A_CAP_N@@), ascendentes @@A_ASC_MIN@@ (@@A_ASC_N@@), sem ascendente @@A_X_MIN@@ a @@A_X_MAX@@ cm (@@A_X_N@@); os @@A_L_N@@ «ℓ» e @@A_PHI_N@@ «ϕ» não foram mapeados pelo contorno (ver «não conferido»). «Inclusive nos sinais de referência»: no MQC não há sinal de referência numérico nem entre colchetes (o JSON lista `colchetes: []`); as designações de painel «(a)…(d)» têm «a» e «c» sem ascendente (@@M_X_MIN@@ cm), que a frase, por dizer «com haste», não afirma (ver O1).

## C4 — número do pedido, referência, datas, requerente, folhas, anexo, tabela

**Resposta: certos e não trocados.** [REAL] Fonte: os RO/106 originais (`EPCT\…\RECIBOS\PCTBR20260505{76,79}-ro106-1-pt-20261009.pdf`, sha256 iniciados em `@@RO576@@` e `@@RO579@@`, que coincidem com os pinados em `andamentos\marcos_fixos.json`), lidos na imagem; os IB/313 [15] (capturas de 07/10); `EPCT\CONTROLE_GERAL.md` linhas @@CG576@@ e @@CG579@@; PDFs de entrada e anexos.

| item | 050576 (carta → fonte) | 050579 (carta → fonte) |
|---|---|---|
| pedido internacional | PCT/BR2026/050576 → RO/106 e IB/313: igual | PCT/BR2026/050579 → igual |
| ref. do processo do requerente | BR102026005477 → RO/106: igual (CONTROLE_GERAL: BR102026005477-1) | BR102026003460 → igual (BR102026003460-6) |
| data do depósito | 04 de outubro de 2026 → RO/106 e IB/313 (04.10.2026): igual | igual |
| requerente | ROTOLI MIGUEL, Luiz Antonio → igual ao RO/106 | igual |
| RO/106 expedido | 09 de outubro de 2026 → igual; prazo «DOIS MESES a partir da data de expedição» | igual |
| IB/313 [15] | de 07 de outubro de 2026 → «Date of mailing 07.10.2026»; Desenhos a, d, f, h, k marcados, a carta cita «a», «d», «f», «h» e «k» | 07.10.2026; Desenhos d, f, h, k marcados (sem «a»), a carta cita «d», «f», «h» e «k» |
| RO/106, Anexo C1 | item 1; Desenhos d e k marcados → a carta cita «d» e «k» | idem |
| folhas depositadas | 5 (1/5 a 5/5, Figuras 1 a 9) → entrada: 5 páginas, `@@D576@@`; figuras por folha [1,2],[3,4],[5,6],[7,8],[9] = a coluna «Folha substituída» da tabela | 3 (1/3 a 3/3, Figuras 1 a 8) → entrada: 3 páginas, `@@D579@@`; figuras [1,2,3],[4,5,6],[7,8] = a tabela |
| folhas de substituição / total | 6, n/N com N = 6 → anexo: 6 páginas A4, «1/6»…«6/6»; figuras por folha 1:[1] 2:[2,3] 3:[4,5] 4:[6,7] 5:[8] 6:[9] = a coluna «Folha de substituição» | 8, N = 8 → anexo: 8 páginas A4, «1/8»…«8/8», figura n na folha n = a tabela |
| folhas em paisagem | 1/6 e 6/6 → medido pela direção do texto: exatamente 1 e 6 | 1/8, 4/8 e 8/8 → medido: exatamente 1, 4 e 8 |
| anexo citado | `FOLHAS_SUBSTITUTIVAS_050576.pdf` (6 folhas): existe; sha16 `@@X576@@` = o aceito | `FOLHAS_SUBSTITUTIVAS_050579.pdf` (8 folhas): existe; sha16 `@@X579@@` = o aceito |
| troca entre os PCT | a carta 050576 não contém «050579», «BR102026003460», «MQC», «8 folhas», «1/8» | a carta 050579 não contém «050576», «BR102026005477», «Aprendizado», «6 folhas», «1/6», «PHO» |

## C5 — as decisões do operador de 02/11/2026

**Resposta: batem.** [REAL] (registro das decisões: `work\decisoes_patentes_02nov\DECISOES_OPERADOR_02nov.md`; `EPCT\CONTROLE_GERAL.md`, adendo «decisoes_operador_02nov».)

- «PHO» como no depositado (050576): a folha 1/6 do anexo traz «VACUUM/GRAV/PHO» (nenhuma folha traz «PHOT»); o depositado 1/5, visto em imagem, mostra «VACUUM/GRAV/PHO»; a carta (Fig. 1) declara «VACUUM/GRAV/PHO». A variante PHOT não é a citada.
- Setas: na imagem da folha 1/6 (girada para leitura) a ponta entre [1] e [3] fica em [1] e a de [4]-[5] fica em [4]; o depositado 1/5, em imagem, mostra o mesmo; a carta diz «[3] para [1] e [5] para [4]» e, no 3(d), «as setas reproduzem o sentido visível no depositado».
- Colchetes: a folha 1/6 tem `[1]` a `[7]` em texto vivo; as demais folhas não têm colchetes; a carta usa os rótulos como estão e o item 4 declara os sinais de referência «os do pedido internacional tal como depositado».
- MQC, Figura 8: o anexo, folha 8/8, tem «𝒜» (U+1D49C, 1 vez) e «ℰ» (U+2130, 2 vezes) em script; o depositado, em imagem, mostra caixas vazias onde iriam o 𝒜 e o ℰ; a carta (quadro, Fig. 8) declara «nos símbolos A_C (…) e E_Ψ (…) o depositado mostra caixa de glifo ausente e as folhas desenham o símbolo em script» e indica onde constam na descrição ([0056], equação (22); Tabela 1).
- «Não acrescentam matéria nova»: parágrafo 4 idêntico ao aceito, byte a byte do trecho (sha16 `@@PAR4@@`), nos dois PCT.

## C6 — dados pessoais nos PDFs finais

**Resposta: nenhum além do nome do requerente e da referência.** [REAL] Padrões testados: CPF, CNPJ, e-mail, telefone, URL e sequências de 11 e 14 dígitos nos três extratores; ORCID, RG/OAB, CEP e logradouro no texto do PyMuPDF. O único logradouro e o único CEP são os do INPI (Rua Mayrink Veiga, 9, 20º andar, Centro, Rio de Janeiro/RJ, CEP [dado pessoal removido], igual ao bloco «Nome e endereço do Organismo receptor» do RO/106). «Goiânia» aparece só como local da assinatura (cidade; o endereço residencial que consta do destinatário do RO/106 NÃO aparece na carta). Metadados dos PDFs sem autor, título nem XMP; sem anotações nem anexos. (Cuidado meu: não deixei cópia das páginas do RO/106 em `work\`, porque a 1.ª página traz o endereço residencial; apaguei as renderizações que fiz.)

## C7 — o que mais poderia embaraçar ou ficar inconsistente

**Resposta: nada que bloqueie; sete observações (O1 a O7), abaixo.** Conferi e está coerente: a data «4 de novembro de 2026» vem depois do RO/106 (09/10), do IB/313 (07/10) e do depósito (04/10) e antes do prazo fatal 09/12/2026; «dentro do prazo de dois meses (Regra 26.2)» é verdadeiro nessa data; nenhuma frase em primeira pessoa da Central, nenhuma referência a ferramenta interna (os termos «IALD» e «script» que a busca acusou são o nome de uma série da legenda da Fig. 5 do MQC e a palavra «script» no sentido de letra cursiva; ver O6); o endereçamento é o do RO/106; todo número do quadro de figuras confere (C4).

## Observações não bloqueantes (para a gerência; nenhuma é reparo necessário)

- **O1 [redação; 3(c) nas duas cartas].** «Letras com haste» é termo ambíguo de tipografia. Na leitura «haste ascendente» (b d f h k l) a frase é verdadeira (C3). Na leitura larga (qualquer traço vertical: n, m, r, u, p, q) as minúsculas sem ascendente medem (altura-x) @@M_X_MIN@@ a @@M_X_MAX@@ cm no MQC e @@A_X_MIN@@ a @@A_X_MAX@@ cm no Aprendizado, e a frase seria falsa. É a frase que o Aprendizado já tinha (aceita na R3) e que a decisão (4) manda igualar; por isso não é reparo. Em favor da leitura pretendida: no JSON do preparador «sem haste» designa as de altura-x. Se a gerência reabrir, sugestão: «letras com haste ascendente». Qual dos dois: ambiguidade de palavra (parede medida), não falsificação da afirmação na leitura pretendida.
- **O2 [cosmético].** «a requerente» (item 1, as duas cartas): o requerente é pessoa física, homem (ROTOLI MIGUEL, Luiz Antonio), e o próprio formulário RO/106 diz «ao requerente». Sem efeito jurídico; trocar seria uma quinta diferença, fora da lista permitida.
- **O3 [LEGAL, já decidido pelo operador em 02/11].** Colchetes `[1]` a `[7]` mantidos na Fig. 1 do Aprendizado. O IB/313 marca «h» (números, letras e linhas de referência com clareza e simplicidade) nos dois PCT, e o registro da gerência cita a Regra 11.13(e) como a que veda colchetes junto de números e letras [DECLARADO; não li a fonte]. A carta não afirma ter resolvido «h» além de tamanho e não sobreposição (3(c), 3(d)). Se o RO ler os colchetes como o defeito «h», pode voltar com nova exigência; o operador decidiu «se houver a exigência a gente corrige». O negativo possível, então, não é defeito da carta: é risco do RO, aceito por ele.
- **O4 [data].** «4 de novembro de 2026» é data futura em relação a hoje (02/11/2026). Se o envio cair em outro dia, a data da carta fica diferente do carimbo do ePCT; sem efeito jurídico conhecido [LEGAL leve]; conferir no momento do envio.
- **O5 [rótulos].** `[15]` (item 1) é o número do IB/313 na lista do ePCT; o INPI identifica o formulário pelo nome e pela data que a carta também cita; inofensivo. `[033]` e `[0056]` são parágrafos da descrição depositada, conferidos no texto do appb.
- **O6 [cosmético].** No PDF, «A_C» e «E_Ψ» saem com sublinhado (notação de código) e «em script» pode soar como programa de computador; sugestão se reabrir: «𝒜 com índice C», «ℰ com índice Ψ» e «em letra cursiva (script)». As cartas aceitas são iguais.
- **O7 [operacional: o que enviar].** Por PCT, só estes dois arquivos: 050576: `CARTA_REGRA_26_4_050576_FINAL.pdf` `@@H576P@@` + `FOLHAS_SUBSTITUTIVAS_050576.pdf` `@@X576@@`; 050579: `CARTA_REGRA_26_4_050579_FINAL.pdf` `@@H579P@@` + `FOLHAS_SUBSTITUTIVAS_050579.pdf` `@@X579@@`. Na pasta K há arquivos parecidos que NÃO devem ir: as cartas sem sufixo (ainda com «Minuta… Não enviada» e «[local], [data]»), as `_PHOT` e as variantes PHOT das folhas.

## Escolhas [LEGAL] abertas (herdadas das revisões anteriores; não são minhas e não bloqueiam)

Substituição integral das folhas (5 → 6 e 3 → 8); critério da altura-x (O1); curva da Fig. 3 mantida como depositada; cores citadas nas descrições (MQC 9 menções, 6 pedidos, registrado no Mapa em 12/10); símbolos em script na Fig. 8 do MQC (leitura da Central, que o operador pode corrigir antes da B4); possível convite da Regra 26.3ter; a assinatura «eletronicamente no envio pelo ePCT» e a Regra 92.1; a citação «Regra 11.13(j)» (parágrafo da folha de lado, nas duas cartas). Seções 207 e 325 das Instruções Administrativas: [DECLARADO pela gerência].

## O que NÃO foi conferido

1. A suficiência jurídica da resposta frente ao RO/106 e ao IB/313 [LEGAL; agente de PI].
2. O texto das Regras 11.13 (inclusive a letra do parágrafo citado como «(j)» e o «(e)» do registro da gerência), 26.2, 26.4, 26.5, 92.1 e das Seções 207/325: sem rede; as citações das cartas não foram conferidas na fonte [DECLARADO pela gerência].
3. Que «Assinado eletronicamente no envio pelo ePCT» satisfaz a exigência de assinatura [LEGAL].
4. Nada foi transmitido nem testado no ePCT (proibido): comportamento do portal com os PDFs, com os nomes de arquivo, tamanho.
5. As folhas não foram remedidas por inteiro (hashes aceitos conferidos); verifiquei só o que as cartas finais afirmam sobre elas: total, orientação, figura por folha, «PHO», setas, colchetes, símbolos em script, altura por glifo, corpo do texto, ausência de rascunho.
6. A altura por glifo usa o contorno da fonte vezes o corpo do texto vivo (acima da linha de base), não a tinta renderizada; os @@A_L_N@@ «ℓ» e os @@A_PHI_N@@ «ϕ» do Aprendizado não foram mapeados pelo contorno (altura de projeto da fonte CM ≈ 0,351 cm, não medida); texto desenhado como caminho vetorial, se houvesse, não entraria (as folhas não têm imagem e o texto é vivo).
7. Se o envio de fato ocorrerá em 04/11/2026 (O4).
8. A memória ACOM: não usei (sem referência própria e escrever fora de `REVISAO\` era proibido); não registrei no Mapa (a gerência registra).

## Hashes (sha16 lidos por script agora; sha256 completo no `.json`)

- `CARTA_REGRA_26_4_050576_FINAL.pdf` `@@H576P@@` · `.md` `@@H576M@@`
- `CARTA_REGRA_26_4_050579_FINAL.pdf` `@@H579P@@` · `.md` `@@H579M@@`
- aceitas (conferidas intactas): 050576 `.pdf` `@@A576P@@`, `.md` `@@A576M@@`; 050579 `.pdf` `@@A579P@@`, `.md` `@@A579M@@`
- anexos: `FOLHAS_SUBSTITUTIVAS_050576.pdf` `@@X576@@`; `FOLHAS_SUBSTITUTIVAS_050579.pdf` `@@X579@@` (os hashes aceitos)
- gerador `fontes\carta_final.py` `@@G_FINAL@@`; base `fontes\carta.py` `@@G_BASE@@`
- entrada (desenhos depositados): Aprendizado `@@D576@@`; MQC `@@D579@@`

## Para registro no Mapa (a gerência registra; eu não)

Sugestão de rota: `pi.pct.ro106_cartas_finais_02nov` (PATENTES, EXAMINADA, estatuto REAL para o medido e LEGAL para a suficiência): veredito `CARTAS_FINAIS_050576_050579_ACEITAS_QUATRO_DIFERENCAS_SO`; artefatos: as quatro cartas finais, os dois anexos e este arquivo; defeito: nenhum necessário; observações O1 a O7; não refazer: a comparação com as aceitas, a medição por glifo e a leitura dos RO/106; próximo passo: frase B4 do operador, uma por PCT, com a lista de envio de O7.

## Evidências

Pasta `REVISAO\evidencias_FINAIS\` (scripts `rf_01` a `rf_11`, saídas `.json`, textos extraídos `txt_*`, páginas finais e imagens de conferência `pg_*`, `anexo_*`, `depositado_*`; sha16 de cada um no `.json`).
"""

for k, v in SUB.items():
    MD = MD.replace(f"@@{k}@@", v)
assert "@@" not in MD, re.findall(r"@@\w+@@", MD)

out_json = {
    "revisor": "sonnet-ro106-revisor-final",
    "data": agora,
    "escopo": "cartas finais da Regra 26.4 (RO/106 de 09/10/2026): 4 diferencas permitidas frente as aceitas; C1..C7",
    "nada_enviado_nada_regenerado": True,
    "veredito": {"PCT/BR2026/050576": "ACEITA", "PCT/BR2026/050579": "ACEITA"},
    "reparos_necessarios": [],
    "mapa_de_rotas": {"consultas": {"RO/106": 5, "Regra 26.4": 2, "folhas de substituição": 2, "carta final": 0}, "livro_registros": 1650, "cabeca": "eac85d927e114b22",
                      "rota_relevante": "pi.pct.ro106_mqc_aprendizado_09dez (EM_CURSO, 1 registro, 12/10/2026)",
                      "sem_registro_de": ["revisoes R2/R3", "decisoes de 02/11", "cartas finais", "esta revisao"]},
    "hashes": H,
    "C1": C1, "C2": {"marcas_de_rascunho": "nenhuma", "extratores": list(mk.keys()), "colchetes": {k: v["colchetes"] for k, v in mk.items() if k.endswith("fitz")}},
    "C3": {"preparador": {"linhas": linhas_med, "minimo_cm": min_json, "abaixo_0_32": abaixo_json, "so_altura_x_abaixo_0_32": [{"folha": f, **it} for f, it in xlinhas]},
           "independente_mqc": {k: {"n": v["n"], "minimo_cm": v["minimo_cm"], "maximo_cm": v["maximo_cm"]} for k, v in M.items() if k in (cls_alg, cls_cap, cls_asc, cls_x)},
           "independente_aprendizado": {k: {"n": v["n"], "minimo_cm": v["minimo_cm"], "maximo_cm": v["maximo_cm"]} for k, v in A.items() if k in (cls_alg, cls_cap, cls_asc, cls_x)},
           "tamanhos_mqc": tam579, "tamanhos_aprendizado": tam576, "frase_nova_verdadeira_na_leitura_haste_ascendente": True,
           "frase_antiga_falsa_para_minusculas_sem_ascendente_se_altura_for_altura_x": True},
    "C4": {"anexos": {k: {"sha16": v["sha16"], "confere": v["confere"], "paginas": v["paginas"]} for k, v in an.items()},
           "figuras_por_folha_anexo_050576": figs576, "figuras_por_folha_anexo_050579": figs579,
           "figuras_por_folha_depositado_050576": dep576, "figuras_por_folha_depositado_050579": dep579,
           "paisagem_medida_igual_declarada": True},
    "C5": {"PHO": True, "setas_3_para_1_e_5_para_4": True, "colchetes_na_folha_1": True, "simbolos_em_script_fig8_mqc": True, "par4_identico": True, "par4_sha16": PAR4},
    "C6": {"dados_pessoais": "nenhum alem do nome do requerente e da referencia; endereco do INPI legitimo", "metadados_pdf_sem_autor_titulo_xmp": True},
    "C7": {"observacoes_nao_bloqueantes": ["O1 haste ambigua", "O2 a requerente", "O3 colchetes e item h (LEGAL, decidido pelo operador)", "O4 data futura 04/11", "O5 [15] numero ePCT", "O6 A_C/E_Psi em texto e 'script'", "O7 lista exata de envio"]},
    "nao_conferido": ["suficiencia juridica (LEGAL)", "texto das Regras 11.13/26.2/26.4/26.5/92.1 e Secoes 207/325 (sem rede)", "assinatura eletronica no ePCT (LEGAL)", "transmissao/ePCT (proibido)",
                      "folhas nao remedidas por inteiro", "glifos l e phi do Aprendizado nao mapeados pelo contorno", "data efetiva do envio", "memoria ACOM nao usada; Mapa nao registrado"],
    "evidencias_sha16": EV,
}
(R / "REVISAO_RO106_CARTAS_FINAIS.md").write_bytes(MD.encode("utf-8"))
(R / "REVISAO_RO106_CARTAS_FINAIS.json").write_bytes(json.dumps(out_json, indent=1, ensure_ascii=False).encode("utf-8"))
for n in ("REVISAO_RO106_CARTAS_FINAIS.md", "REVISAO_RO106_CARTAS_FINAIS.json"):
    p = R / n
    print(n, p.stat().st_size, "bytes sha16", sha(p)[:16])
