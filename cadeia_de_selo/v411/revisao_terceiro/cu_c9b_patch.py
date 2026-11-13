import re
p = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\revisao_terceiro\cu_c9.py"
s = open(p, encoding="utf-8").read()
old = s[s.index("        q = re.sub(r\"\$[^$]*\$\", \" \", p)\n        q = re.sub(r\"\\[a-zA-Z]+"):s.index("        a = alnum(q)")]
new = '''        ult = p.rfind("$")
        q = p
        q = re.sub(r"\\(?:begin|end)\{[^}]*\}", " ", q)
        q = re.sub(r"\\(?:vspace|hspace)\*?\{[^}]*\}", " ", q)
        q = re.sub(r"\\\\(?:\[[^\]]*\])?", " ", q)
        q = re.sub(r"\$[^$]*\$", "\x00", q)
        q = q.split("\x00")[-1]
        q = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", q)
        q = q.replace("{", " ").replace("}", " ").replace("\\\\", " ")
'''
s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
print("patched")
