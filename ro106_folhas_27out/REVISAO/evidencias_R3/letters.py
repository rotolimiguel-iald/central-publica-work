import fitz, re, unicodedata, collections
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
def toks(s):
    s=unicodedata.normalize("NFKC",s); s=re.sub(r"[*`|>#_]","",s)
    return collections.Counter(re.findall(r"[^\W_]+",s.lower()))
for n in ("CARTA_REGRA_26_4_050576","CARTA_REGRA_26_4_050576_PHOT","CARTA_REGRA_26_4_050579"):
    md=open(W+"\\"+n+".md",encoding="utf-8").read()
    pdf="\n".join(p.get_text() for p in fitz.open(W+"\\"+n+".pdf"))
    a=toks(md); b=toks(pdf)
    only_md=sorted(k for k in a if a[k]>b[k]); only_pdf=sorted(k for k in b if b[k]>a[k])
    print(n,"pages",len(fitz.open(W+"\\"+n+".pdf")),"| tokens md-not-in-pdf:",only_md[:15],"| pdf-not-in-md:",only_pdf[:15])
    # personal data check: look for cpf/cnpj/email/phone patterns
    print("   personal-data patterns in pdf:",re.findall(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b|[\w.]+@[\w.]+|\(\d{2}\)\s?\d{4,5}-\d{4}",pdf))
