import fitz, re, collections
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
for n in ("050576","050579"):
    d=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_"+n+".pdf")
    cols=collections.Counter(); alph=set(); other=collections.Counter(); imgs=0; shad=0; pat=0
    for x in range(1,d.xref_length()):
        try: o=d.xref_object(x,compressed=False)
        except Exception: continue
        if "/Subtype /Image" in o or "/Subtype/Image" in o: imgs+=1
        if "/ShadingType" in o: shad+=1
        if "/PatternType" in o: pat+=1
        for m in re.findall(r"/(?:ca|CA) ([\d\.]+)",o): alph.add(m)
        if d.xref_is_stream(x):
            try: s=d.xref_stream(x)
            except Exception: continue
            if b"BT" in s or b" re" in s or b" m\n" in s or b" l\n" in s or b" w\n" in s:
                t=s.decode("latin1")
                for m in re.findall(r"((?:[\d\.\-]+ ){3})rg",t): cols["rg "+m.strip()]+=1
                for m in re.findall(r"((?:[\d\.\-]+ ){3})RG",t): cols["RG "+m.strip()]+=1
                for m in re.findall(r"([\d\.\-]+) g\b",t): cols["g "+m]+=1
                for m in re.findall(r"([\d\.\-]+) G\b",t): cols["G "+m]+=1
                for m in re.findall(r"((?:[\d\.\-]+ ){4})k\b",t): cols["k "+m.strip()]+=1
                for m in re.findall(r"\b(sc|scn|SC|SCN|sh)\b",t): other[m]+=1
    print(n,"images",imgs,"shadings",shad,"patterns",pat,"alpha",alph,"colors",dict(cols),"other",dict(other))
