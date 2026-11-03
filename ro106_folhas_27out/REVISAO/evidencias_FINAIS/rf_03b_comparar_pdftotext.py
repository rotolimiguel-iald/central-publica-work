# -*- coding: utf-8 -*-
# C1 (controle cruzado): mesma comparacao PDF aceita x PDF final, agora sobre o extrator pdftotext (poppler) em modo -raw,
# e tambem sobre a "forma comprimida" (sem espacos nem hifens) em nivel de caractere, que ignora quebra de linha e hifenizacao.
import difflib, json, pathlib, re, unicodedata

K = pathlib.Path("C:/IALD/Central de Patentes/work/ro106_folhas_27out")
E = K / "REVISAO" / "evidencias_FINAIS"


def toks(s):
    s = unicodedata.normalize("NFC", s).replace("\f", "\n").replace("\u00ad", "")
    s = re.sub(r"(?<=\w)[-\u2010\u2011]\n(?=\w)", "", s).replace("\n", " ")
    return [re.sub(r"[-\u2010\u2011]", "", t) for t in s.split()]


def squeeze(s):
    s = unicodedata.normalize("NFC", s).replace("\u00ad", "")
    return re.sub(r"[\s\-\u2010\u2011\f]", "", s)


out = {}
for tag in ("576", "579"):
    r = {}
    for ext in ("pdftotext_raw", "fitz"):
        a = (E / f"txt_{tag}_aceita.{ext}.txt").read_text(encoding="utf-8")
        b = (E / f"txt_{tag}_final.{ext}.txt").read_text(encoding="utf-8")
        ta, tb = toks(a), toks(b)
        sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
        dif = [(op, " ".join(ta[i1:i2]), " ".join(tb[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
        # forma comprimida, nivel de caractere
        sa, sb = squeeze(a), squeeze(b)
        sm2 = difflib.SequenceMatcher(None, sa, sb, autojunk=False)
        dif2 = [(op, sa[i1:i2], sb[j1:j2]) for op, i1, i2, j1, j2 in sm2.get_opcodes() if op != "equal"]
        r[ext] = {"tokens_aceita": len(ta), "tokens_final": len(tb), "blocos_token": dif, "blocos_caractere_comprimido": dif2}
        print("=" * 100)
        print(tag, ext, "tokens", len(ta), "->", len(tb), "| blocos (token):", len(dif), "| blocos (caractere, comprimido):", len(dif2))
        for op, x, y in dif2:
            print(f"   [{op}] aceita: «{x[:260]}»  ||  final: «{y[:260]}»")
    out[tag] = r
(E / "rf_03b_comparar_pdftotext.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
