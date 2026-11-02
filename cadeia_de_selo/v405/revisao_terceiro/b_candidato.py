# -*- coding: utf-8 -*-
import ast,re,sys,hashlib
sys.stdout.reconfigure(encoding="utf-8")
R="C:/IALD/Central de Patentes/work/cadeia_de_selo/v405/"
s=open(R+"um_v405_candidato.py",encoding="utf-8").read()
tr=ast.parse(s)
vals={}
for n in tr.body:
    if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ("_V405_IDENTIDADE_TXT","_V405_IDENTIDADE_EN_TXT","_V405_ENSAIO_ORIGINAL_SHA16","UM_VERSION"):
        try: vals[n.targets[0].id]=ast.literal_eval(n.value)
        except Exception as e: print("nl",n.targets[0].id,e)
print({k:(v if len(str(v))<40 else len(v)) for k,v in vals.items()})
md=open("C:/IALD/Central de Patentes/work/cadeia_de_selo405/insumos/cunhagens/A_IDENTIDADE_revisao_da_gerencia_01nov_r2.md",encoding="utf-8").read()
i=md.index("## O texto (r2)"); j=md.index("\n---",i)
c=md[i+len("## O texto (r2)"):j].strip("\n").replace("\u27e6","").replace("\u27e7","").strip("\n")+"\n"
t=vals["_V405_IDENTIDADE_TXT"]
print("r2 == candidato",t==c, "⟦ no md:",md[i:j].count("\u27e6"))
en=open(R+"A_IDENTIDADE_traducao_en_da_gerencia.txt",encoding="utf-8",newline="").read()
print("en == candidato",vals["_V405_IDENTIDADE_EN_TXT"]==en or vals["_V405_IDENTIDADE_EN_TXT"].replace("\r","")==en.replace("\r",""))
# artigo no candidato
pt=open(R+"artigo_pt_v405.pysnip",encoding="utf-8").read(); enn=open(R+"artigo_en_v405.pysnip",encoding="utf-8").read()
print("pt no candidato",pt.strip() in s.replace("\r\n","\n"), "en no candidato",enn.strip() in s.replace("\r\n","\n"))
for f in ("runtime_v405.py",):
    r=open(R+f,encoding="utf-8").read()
    # bloco funcional
    k=r.index("def _v405_guarda_frases"); print("runtime no candidato",r[k:].strip()[:200] in s, r[k:].strip() in s.replace("\r\n","\n"))
# frases proibidas e assemelhadas no que o candidato tem de NOVO: linhas novas
import difflib
b=open(R+"base_v404/um.py",encoding="utf-8").read()
print(len(s),len(b))
pats=[r"levant",r"no-go",r"NO_GO",r"[uú]nica entrada",r"tudo derivad",r"sem hip[oó]tese",r"hip[oó]teses descarregad",r"descarreg",r"AGORA DERIVAD",r"agora derivad",r"incomensur",r"cunhagem do operador como teorema",r"cunhagem como teorema",r"e' teorema na forma",r"o que permanece"]
novo=[n for n in tr.body if (isinstance(n,(ast.FunctionDef)) and "v405" in n.name) or (isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and "V405" in n.targets[0].id)]
print(len(novo))
ln=s.split("\n")
txt="\n".join("\n".join(ln[n.lineno-1:n.end_lineno]) for n in novo)
print("texto novo",len(txt))
for p in pats:
    ms=list(re.finditer(p,txt))
    print("==",p,len(ms))
    for m in ms[:6]:
        print("   ",txt[max(0,m.start()-90):m.end()+90].replace("\n"," "))
