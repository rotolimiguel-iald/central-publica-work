# -*- coding: utf-8 -*-
# C1: comparacao palavra a palavra. (A) PDF aceita x PDF final; (B) md aceita x md final; (C) PDF final x md final (sanidade).
# Normalizacao propria do revisor: NFC, junta hifenizacao de fim de linha, tira hifen interno dos tokens (compostos),
# remove a linha de cabecalho repetida da tabela no PDF, remove marcas de markdown.
import difflib, json, pathlib, re, unicodedata, collections

K = pathlib.Path("C:/IALD/Central de Patentes/work/ro106_folhas_27out")
E = K / "REVISAO" / "evidencias_FINAIS"

HDR_PDF = ["Fig.", "Folha substituída", "Folha de substituição", "Diferenças em relação à folha substituída"]


def tokens_from_text(s: str):
    s = unicodedata.normalize("NFC", s).replace("\f", "\n").replace("\u00ad", "")
    # junta hifenizacao: letra + '-' + quebra + letra
    s = re.sub(r"(?<=\w)[-\u2010\u2011]\n(?=\w)", "", s)
    s = s.replace("\n", " ")
    toks = s.split()
    # tira hifen interno (compostos grafados com ou sem hifen pela quebra de linha)
    return [re.sub(r"[-\u2010\u2011]", "", t) for t in toks]


def pdf_tokens(path: pathlib.Path):
    raw = path.read_text(encoding="utf-8")
    # remove a linha de cabecalho da tabela (repete a cada pagina), contando
    n_hdr = 0
    lines = raw.split("\n")
    out = []
    i = 0
    while i < len(lines):
        if lines[i:i + 4] == HDR_PDF:
            n_hdr += 1
            i += 4
            continue
        out.append(lines[i])
        i += 1
    return tokens_from_text("\n".join(out)), n_hdr


def md_tokens(path: pathlib.Path):
    s = path.read_text(encoding="utf-8")
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"^\|[-:| ]+\|\s*$", " ", s, flags=re.M)   # linha separadora da tabela
    s = re.sub(r"(?m)^> ", "", s)
    s = re.sub(r"(?m)^# ", "", s)
    s = s.replace("**", "").replace("|", " ")
    s = re.sub(r"  \n", "\n", s)
    return tokens_from_text(s)


def diff(a, b, la, lb, ctx=4):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        out.append({
            "op": tag,
            la: " ".join(a[i1:i2]), lb: " ".join(b[j1:j2]),
            "contexto_antes": " ".join(a[max(0, i1 - ctx):i1]),
            "contexto_depois": " ".join(a[i2:i2 + ctx]),
            "pos_" + la: [i1, i2], "pos_" + lb: [j1, j2],
        })
    return out, sm.ratio()


res = {}
for pct in ("050576", "050579"):
    tag = {"050576": "576", "050579": "579"}[pct]
    a_pdf, ha = pdf_tokens(E / f"txt_{tag}_aceita.fitz.txt")
    b_pdf, hb = pdf_tokens(E / f"txt_{tag}_final.fitz.txt")
    a_md = md_tokens(K / f"CARTA_REGRA_26_4_{pct}.md")
    b_md = md_tokens(K / f"CARTA_REGRA_26_4_{pct}_FINAL.md")
    d_pdf, r_pdf = diff(a_pdf, b_pdf, "aceita", "final")
    d_md, r_md = diff(a_md, b_md, "aceita", "final")
    d_x, r_x = diff(b_md, b_pdf, "md_final", "pdf_final")
    res[pct] = {
        "n_tokens": {"pdf_aceita": len(a_pdf), "pdf_final": len(b_pdf), "md_aceita": len(a_md), "md_final": len(b_md)},
        "cabecalho_tabela_repetido": {"pdf_aceita": ha, "pdf_final": hb},
        "A_pdf_aceita_x_pdf_final": {"similaridade": round(r_pdf, 6), "diferencas": d_pdf},
        "B_md_aceita_x_md_final": {"similaridade": round(r_md, 6), "diferencas": d_md},
        "C_md_final_x_pdf_final": {"similaridade": round(r_x, 6), "diferencas": d_x},
    }
    print("=" * 100)
    print(pct, "tokens:", res[pct]["n_tokens"], "cabecalhos tabela removidos:", ha, hb)
    for nome, d, r in (("A) PDF aceita x PDF final", d_pdf, r_pdf), ("B) MD aceita x MD final", d_md, r_md), ("C) MD final x PDF final", d_x, r_x)):
        print("-" * 100)
        print(nome, "| similaridade", round(r, 6), "| blocos diferentes:", len(d))
        for x in d:
            ks = [k for k in x if not k.startswith("pos_") and not k.startswith("contexto") and k != "op"]
            print("  [", x["op"], "] ", " || ".join(f"{k}: «{x[k]}»" for k in ks), "  (antes: «" + x["contexto_antes"] + "»)")
(E / "rf_03_comparar.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
