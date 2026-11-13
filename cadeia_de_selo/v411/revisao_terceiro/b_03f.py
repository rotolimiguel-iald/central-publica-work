from b_lib import *
import re
m = md()
for mm in re.finditer(r"nenhum dado observado|nenhum vetor observado|n[ãa]o l[êe] (?:esse )?vetor|abertura (?:é|e') de vers[ãa]o futura|parede de montagem|NO_OBSERVED_VECTOR_READ", m):
    s = mm.start(); print("md", s, "|", m[max(0, s-160): s+200].replace("\n", " "))
t = pt()
for mm in re.finditer(r"nenhum dado observado|nenhum vetor observado|n[ãa]o l[êe] esse vetor|abertura (?:é|e') de vers[ãa]o futura|parede de montagem|NO_ OBSERVED_ VECTOR_ READ|roda sem o resultado", t):
    s = mm.start(); print("pt", s, "|", t[max(0, s-90): s+120].replace("\r\n", " "))
