# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 10/11/2026 — conferência da terceira e da quarta emendas à R6: SÓ comentários mudaram em relação à candidata
da segunda emenda (a última compilada: rodada 5). Só lê; não escreve nada. uso: python conferir_so_docstring.py"""
import hashlib, re, sys
from pathlib import Path

R6 = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R6_a_constante_da_escala")
novo_b = (R6 / "AEscala.lean").read_bytes()
velho_b = (R6 / "_build" / "pre_emenda3_fala19" / "AEscala.lean").read_bytes()
sha = lambda b: hashlib.sha256(b).hexdigest()
novo, velho = novo_b.decode("utf-8"), velho_b.decode("utf-8")
print("candidata nova :", len(novo_b), "B sha256", sha(novo_b))
print("segunda emenda :", len(velho_b), "B sha256", sha(velho_b))
assert sha(velho_b) == "e356e2927133e9e79fe7309cfb74ce88bc3a752043bd600a29257f845ab819fe"
assert b"\r\n" not in novo_b

def sem_comentarios(s):
    """retira os comentários de bloco do Lean (/- ... -/, com aninhamento) e os de linha (-- ...)."""
    out, i, n, prof = [], 0, len(s), 0
    while i < n:
        if s.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and s.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if s.startswith("--", i):
            j = s.find("\n", i)
            i = n if j < 0 else j
            continue
        out.append(s[i]); i += 1
    assert prof == 0, "comentario de bloco nao fechado"
    return "".join(out)

cn, cv = sem_comentarios(novo), sem_comentarios(velho)
norm = lambda s: re.sub(r"[ \t]+\n", "\n", s)
print("codigo fora de comentario identico (byte a byte, sem espacos de fim de linha):", norm(cn) == norm(cv))
assert norm(cn) == norm(cv), "MUDOU CODIGO"
RX = re.compile(r"^(theorem|def|structure)\s+([A-Za-z_][A-Za-z0-9_'.]*)", re.M)
dn, dv = [m.group(0) for m in RX.finditer(novo)], [m.group(0) for m in RX.finditer(velho)]
print("declaracoes:", len(dn), "| iguais e na mesma ordem:", dn == dv)
assert dn == dv and len(dn) == 79
pn, pv = re.findall(r"^#print axioms .*$", novo, re.M), re.findall(r"^#print axioms .*$", velho, re.M)
print("#print axioms:", len(pn), "| iguais:", pn == pv)
assert pn == pv and len(pn) == 79
imp = re.findall(r"^import .*$", novo, re.M)
print("imports:", imp)
assert imp == re.findall(r"^import .*$", velho, re.M)
assert "sorry" not in cn and not re.search(r"^\s*axiom\s", cn, re.M)
print("sorry fora de comentario: 0 | axiom: 0")

# o que a ordem pede no texto
sem_aspas = re.sub("\u00ab[^\u00bb]*\u00bb", "", novo)
low = re.sub(r"\s+", " ", sem_aspas).lower()
for proib in ("posto nunca é escala", "posto não é escala", "nunca é escala", "posto jamais é escala"):
    assert proib not in low, "frase da autoria a corrigir: " + proib
print("frase da autoria dizendo que posto NUNCA e' escala: nenhuma")
nt = re.sub(r"\s+", " ", novo)
chk = {
 "VINTE E UMA falas": nt.count("## As VINTE E UMA falas do operador"),
 "DOIS DOMINIOS": nt.count("DOIS DOMÍNIOS (terceira emenda; fala 19"),
 "O FECHO": nt.count("O FECHO (quarta emenda; falas 20 e 21"),
 "fala 19 por bytes": nt.count("não mudo o que eu disse antes e não vejo contradição, na tônica a escala é a unidade posta"),
 "fala 20 por bytes": nt.count("compreendo bem o que vc quis dizer, e é esse confronto de ideias que nos faz avançar, porque agora ficou claro que escala=relatividade"),
 "fala 21 por bytes": nt.count("«o que é relativo, o que é par, sem o par não há escala»"),
 "the_scale_is_free": nt.count("TonicaDoHamiltoniano.the_scale_is_free"),
 "the_ratio_survives_the_rescaling": nt.count("TonicaDoHamiltoniano.the_ratio_survives_the_rescaling"),
 "the_tonic_lands_on_the_posted_unit": nt.count("TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit"),
 "LeiDoDiminuto.tonica (citada)": nt.count("`LeiDoDiminuto.tonica`"),
 "objetos DISTINTOS": nt.count("São objetos DISTINTOS, e esta pedra NÃO deriva um do outro"),
 "lei unica OPEN": nt.count("a lei ÚNICA dos dois domínios (a tônica e o tempo) NÃO é teorema desta pedra: fica [OPEN]"),
 "relatividade ONTO": nt.count("A identificação da escala com a RELATIVIDADE é leitura dele [ONTO]"),
 "E0": novo.count("E₀"),
 "DEZENOVE (não deve ficar)": nt.count("DEZENOVE"),
 "DEZOITO (não deve ficar)": nt.count("DEZOITO"),
}
for k, v in chk.items(): print(f"   {k}: {v}")
assert chk["VINTE E UMA falas"] == 1 and chk["DOIS DOMINIOS"] == 1 and chk["O FECHO"] == 1
assert chk["fala 19 por bytes"] == 2 and chk["fala 20 por bytes"] == 2 and chk["fala 21 por bytes"] == 2
assert chk["the_scale_is_free"] == 2 and chk["the_ratio_survives_the_rescaling"] == 1 and chk["the_tonic_lands_on_the_posted_unit"] == 2
assert chk["objetos DISTINTOS"] == 1 and chk["lei unica OPEN"] == 1 and chk["relatividade ONTO"] == 1
assert chk["E0"] == 0 and chk["DEZENOVE (não deve ficar)"] == 0 and chk["DEZOITO (não deve ficar)"] == 0
# linhas que mudaram (por contagem)
import difflib
d = list(difflib.unified_diff(velho.split("\n"), novo.split("\n"), lineterm="", n=0))
mais = sum(1 for l in d if l.startswith("+") and not l.startswith("+++"))
menos = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
print(f"diff contra a segunda emenda: +{mais} linhas, -{menos} linhas (todas em comentario)")
print("CONFERIDO: so' docstring e cabecalho mudaram; codigo, declaracoes, imports e auditoria identicos")
