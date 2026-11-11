# -*- coding: utf-8 -*-
"""_fix_f55_f53b_e30_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410): tres correcoes apontadas pelo CONTROLE NEGATIVO da guarda (o instrumento funcionando):
(1) F55 so' via «não falsificado» ANTES de «5 sigma»: passa a ver as duas ordens (PT e EN); (2) F53b nao cobria «detectou»; (3) o texto da E30 cita «H0DN» sem a frase obrigatoria da D72.
Por arquivo (a ferramenta Bash colapsa barras no heredoc). Backup de bytes; trocas exatas; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(nome, trocas, suf):
    P = os.path.join(HERE, nome)
    b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
    bk = P + ".bak_" + TS + suf; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for v, n, k in trocas:
        c = t.count(v); assert c == k, (nome, c, v[:100]); t = t.replace(v, n)
    nb = t.encode("utf-8"); ast.parse(nb); tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
    print(nome, len(b0), "->", len(nb), hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk))


OLD55 = r"NOT_FALSIFIED[A-Z_]*?(?:_5_?SIGMA|_AT_5_SIGMA|_ABOVE_5|_FIVE_SIGMA)|n[ãa]o[ _-]?falsificad[oa][^\n]{0,40}?\b(?:a|acima\s+de|mais\s+que|em)\s+5\s*(?:σ|sigma)|not[ _-]?falsified[^\n]{0,40}?\b(?:at|above|beyond)\s+(?:5|five)\s*(?:σ|-?sigma)"
NEW55 = (r"NOT_FALSIFIED[A-Z_]*?(?:_5_?SIGMA|_AT_5_SIGMA|_ABOVE_5|_FIVE_SIGMA)|n[ãa]o[ _-]?falsificad[oa][^\n]{0,40}?\b(?:a|acima\s+de|mais\s+que|em)\s+5\s*(?:σ|sigma)|\b(?:acima\s+de|mais\s+que|a)\s+5\s*(?:σ|sigma)[^\n]{0,40}?n[ãa]o[ _-]?falsificad"
         r"|not[ _-]?falsified[^\n]{0,40}?\b(?:at|above|beyond)\s+(?:5|five)\s*(?:σ|-?sigma)|\b(?:at|above|beyond)\s+(?:5|five)\s*(?:σ|-?sigma)[^\n]{0,40}?not[ _-]?falsified")
OLD53 = r"\bDETECTED\b|\bdetectad[oa]s?\b|\bdetected\b|\bconfirm(?:a|ou|ad[oa]s?|s|ed)\b"
NEW53 = r"\bDETECTED\b|\bdetect(?:ou|a|ad[oa]s?|ed|s)\b|\bconfirm(?:a|ou|ad[oa]s?|s|ed)\b"
troca("runtime_v410.py", [(OLD55, NEW55, 1), (OLD53, NEW53, 1)], "_fix1")
troca("delta_v410.py", [
    ("a D72 escrevia o ramo z_null >= 5 e |z_tgl| <= 1,96 da funcao de veredito do H0DN com a palavra popperiana na cabeca; errado:",
     "a D72 escrevia o ramo z_null >= 5 e |z_tgl| <= 1,96 da funcao de veredito do H0DN (pré-registrado; nenhum dado observado lido) com a palavra popperiana na cabeca; errado:", 1),
], "_fix1")
