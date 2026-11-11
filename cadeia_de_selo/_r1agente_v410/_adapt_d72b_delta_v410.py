# -*- coding: utf-8 -*-
"""_adapt_d72b_delta_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410): (1) o recibo dos nomes da gerencia (refeito 11:24) lista 11 falas; o AO LADO das decisoes (11:44) acrescentou a 12a e a 13a:
o delta passa a exigir recibo SUBCONJUNTO do DESENHO (o AO LADO mais recente manda) e lista FALAS_FORA_DO_RECIBO para a gerencia; (2) o texto da D72 nao escreve os tokens de veredito proibidos do H0DN
letra por letra (a guarda os pegaria no proprio texto da decisao): TOKENS_PROIBIDOS_H0DN montados por concatenacao, como TOKENS_PROIBIDOS_V410. Trocas exatas; backup de bytes; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "delta_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
bk = P + ".bak_" + TS + "_d72b"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")
TROCAS = [
    ('assert N_FALAS_V410 == len(_REC_NOMES["falas"]) and set(NOMES_V410_DO_DESENHO) == {os.path.basename(f_["arquivo"]) for f_ in _REC_NOMES["falas"]}, "as falas do DESENHO nao sao as do recibo da gerencia"\n',
     '_FALAS_RECIBO = {os.path.basename(f_["arquivo"]) for f_ in _REC_NOMES["falas"]}\n'
     'assert _FALAS_RECIBO <= set(NOMES_V410_DO_DESENHO), ("o recibo da gerencia lista fala que o DESENHO (com os AO LADO) nao lista", sorted(_FALAS_RECIBO - set(NOMES_V410_DO_DESENHO)))\n'
     'FALAS_FORA_DO_RECIBO = sorted(set(NOMES_V410_DO_DESENHO) - _FALAS_RECIBO)   # (09/11: as falas 12 e 13 entraram pelo AO LADO das decisoes DEPOIS do recibo dos nomes refeito as 11:24; o DESENHO + AO LADO manda; dito a gerencia no relatorio)\n', 1),
    ('"com o sha256 do texto-fonte no registro e 4 vetores deterministicos, observed_vector_read = False (nenhum arquivo observado e\' procurado nesta versao), a guarda (FIVE_SIGMA_OBSERVED, DETECTED, H0DN_CONFIRMS e as frases de 5 sigma atingido proibidos; a aritmetica do agregado "\n',
     '"com o sha256 do texto-fonte no registro e 4 vetores deterministicos, observed_vector_read = False (nenhum arquivo observado e\' procurado nesta versao), a guarda (os tokens de veredito de TOKENS_PROIBIDOS_H0DN e as frases que dao o teste por feito, proibidos; a aritmetica do agregado "\n', 1),
    ('TOKENS_PROIBIDOS_V409 = TOKENS_PROIBIDOS_V410                  # (alias dos scripts bumpados)\n',
     'TOKENS_PROIBIDOS_V409 = TOKENS_PROIBIDOS_V410                  # (alias dos scripts bumpados)\n'
     'TOKENS_PROIBIDOS_H0DN = ("FIVE_SIGMA_" + "OBSERVED", "DETEC" + "TED", "H0DN_" + "CONFIRMS")   # D72: tokens proibidos no veredito e no texto do registro H0DN (montados por concatenacao: a guarda varre este texto)\n', 1),
]
for velho, novo, n in TROCAS:
    c = t.count(velho); assert c == n, ("troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140]); t = t.replace(velho, novo)
nb = t.encode("utf-8"); ast.parse(nb)
tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P); assert open(P, "rb").read() == nb
print("delta_v410.py (d72b):", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk))
