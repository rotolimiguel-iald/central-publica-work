import ast
p = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v400_exame\final\guardas_e_bn_v400.py"
s = open(p, "rb").read().decode("utf-8")
i = s.index('assert cand.count(b"\r')
j = s.index('"ancora do controle n3"', i) + len('"ancora do controle n3"')
s = s[:i] + 'assert cand.count(b"\\r\\n\\r\\ndef _beta_runtime() -> float:") == 1, "ancora do controle n3"' + s[j:]
ast.parse(s)
open(p, "wb").write(s.encode("utf-8"))
print("ok")
