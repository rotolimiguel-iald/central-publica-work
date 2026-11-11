# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 10/11/2026 — conferências da quinta e da sexta emendas à R6. Só lê; não escreve nada.
(A) SEXTA: fora dos comentários, o código da FINAL é idêntico ao da candidata da quinta emenda (_build\\candidata_emenda5).
(B) QUINTA: fora dos comentários, a FINAL difere da candidata da quarta emenda (a última compilada, rodada 7) SÓ pela seção nova
    SingularidadeDaInformacao e pelas duas linhas de #print axioms dos dois nomes novos.
uso: python conferir_emendas_5_6.py"""
import hashlib, re, difflib
from pathlib import Path

R6 = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R6_a_constante_da_escala")
fin_b = (R6 / "AEscala.lean").read_bytes()
e5_b = (R6 / "_build" / "candidata_emenda5" / "AEscala.lean").read_bytes()
e4_b = (R6 / "_build" / "pre_emenda5_falas22_23" / "AEscala.lean").read_bytes()
sha = lambda b: hashlib.sha256(b).hexdigest()
fin, e5, e4 = fin_b.decode("utf-8"), e5_b.decode("utf-8"), e4_b.decode("utf-8")
print("FINAL (emendas 5 e 6)     :", len(fin_b), "B sha256", sha(fin_b))
print("candidata da quinta emenda:", len(e5_b), "B sha256", sha(e5_b))
print("candidata da quarta emenda:", len(e4_b), "B sha256", sha(e4_b))
assert sha(e4_b) == "285462a07d19ff503c5d24c044d15054753d5bb09b2b640e03bd967c2dd56c11"
assert b"\r\n" not in fin_b

def sem_comentarios(s):
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
    return re.sub(r"\n{2,}", "\n", re.sub(r"[ \t]+\n", "\n", "".join(out)))

cf, c5, c4 = sem_comentarios(fin), sem_comentarios(e5), sem_comentarios(e4)
# (A)
print("(A) codigo fora de comentario: FINAL == candidata da quinta emenda:", cf == c5)
assert cf == c5, "a sexta emenda mudou codigo"
RX = re.compile(r"^(theorem|def|structure)\s+([A-Za-z_][A-Za-z0-9_'.]*)", re.M)
df, d5, d4 = [m.group(2) for m in RX.finditer(fin)], [m.group(2) for m in RX.finditer(e5)], [m.group(2) for m in RX.finditer(e4)]
assert df == d5 and len(df) == 81
# (B)
lf, l4 = cf.split("\n"), c4.split("\n")
sm = difflib.SequenceMatcher(None, l4, lf, autojunk=False)
ins, rem = [], []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag in ("replace", "delete"): rem += l4[i1:i2]
    if tag in ("replace", "insert"): ins += lf[j1:j2]
print("(B) linhas de codigo retiradas em relacao a quarta emenda:", len(rem), "| acrescentadas:", len(ins))
assert not rem, rem[:5]
bloco = "\n".join(ins)
assert ins[0] == "section SingularidadeDaInformacao" and "end SingularidadeDaInformacao" in ins, ins[:3]
assert ins[-2:] == ["#print axioms TGLExt.AEscala.o_nome_e_a_singularidade_da_informacao",
                    "#print axioms TGLExt.AEscala.o_nome_das_solucoes_e_a_singularidade_do_sinal"], ins[-2:]
novos = [n for n in df if n not in d4]
print("    declaracoes: quarta emenda", len(d4), "-> final", len(df), "| novas:", novos)
assert novos == ["o_nome_e_a_singularidade_da_informacao", "o_nome_das_solucoes_e_a_singularidade_do_sinal"] and d4 == df[:79]
assert "sorry" not in cf and not re.search(r"^\s*axiom\s", cf, re.M)
print("    sorry fora de comentario: 0 | axiom: 0 | imports:", re.findall(r"^import (\S+)", fin, re.M))
assert re.findall(r"^import .*$", fin, re.M) == re.findall(r"^import .*$", e4, re.M)
# as três frases antigas da sexta emenda e as duas aspas a mais (só na FINAL)
nt = re.sub(r"\s+", " ", fin)
chk = {
 "EP-02 'a partir do qual' (deve ser 0)": nt.count("a partir do qual"),
 "EP-02 'passado o qual (s > n·ln 2)'": nt.count("passado o qual (s > n·ln 2)"),
 "EP-02 no limiar exato Z = 1": nt.count("Z(n·ln 2) = 2^n·e^{−n·ln 2} = 1"),
 "EP-08 'o que o TERMO diz é o brilho de UM pixel de custo 1'": nt.count("o que o TERMO diz é o brilho de UM pixel de custo 1"),
 "EP-08 'vem de `os_passos_sao_o_ciclo_ate_o_tetelestai`'": nt.count("não é este enunciado: vem de `os_passos_sao_o_ciclo_ate_o_tetelestai`"),
 "PAR-11 «A Escala» (deve ser 0)": fin.count("«A Escala»"),
 "PAR-11 “A Escala”": fin.count("“A Escala”"),
 "«O QUE SOU» (deve ser 0)": fin.count("«O QUE SOU»"),
 "“O QUE SOU”": fin.count("“O QUE SOU”"),
 "VINTE E QUATRO falas": nt.count("## As VINTE E QUATRO falas do operador"),
 "nome RATIFICADO pelo operador na fala 24": fin.count("nome RATIFICADO pelo operador na fala 24"),
 "'a ratificar' (deve ser 0)": nt.count("a ratificar"),
 "fala 24 por bytes": fin.count("«isso, lindo, confirmo tudo»"),
}
for k, v in chk.items(): print(f"   {k}: {v}")
assert chk["EP-02 'a partir do qual' (deve ser 0)"] == 0 and chk["EP-02 'passado o qual (s > n·ln 2)'"] == 1 and chk["EP-02 no limiar exato Z = 1"] == 1
assert chk["EP-08 'o que o TERMO diz é o brilho de UM pixel de custo 1'"] == 1 and chk["EP-08 'vem de `os_passos_sao_o_ciclo_ate_o_tetelestai`'"] == 1
assert chk["PAR-11 «A Escala» (deve ser 0)"] == 0 and chk["PAR-11 “A Escala”"] == 1 and chk["«O QUE SOU» (deve ser 0)"] == 0 and chk["“O QUE SOU”"] == 2
assert chk["VINTE E QUATRO falas"] == 1 and chk["nome RATIFICADO pelo operador na fala 24"] == 1 and chk["'a ratificar' (deve ser 0)"] == 0
# o que mudou de comentário entre a quinta e a final, por contagem
d = list(difflib.unified_diff(e5.split("\n"), fin.split("\n"), lineterm="", n=0))
mais = sum(1 for l in d if l.startswith("+") and not l.startswith("+++"))
menos = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
print(f"diff FINAL x quinta emenda: +{mais} linhas, -{menos} linhas (todas em comentario)")
print("CONFERIDO: (A) a sexta emenda e a nota da fala 24 so' mexem em comentario; (B) a quinta so' acrescenta a secao nova e as 2 linhas da Auditoria")
