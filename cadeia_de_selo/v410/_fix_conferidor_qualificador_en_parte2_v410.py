# -*- coding: utf-8 -*-
"""_fix_conferidor_qualificador_en_parte2_v410.py -- ACHADO da retomada dos passos 4 a 9 (09/11, noite): o caminho positivo do conferidor nao dava TUDO BATE por UMA checagem (a moldura): o conferidor exigia o qualificador EN da D64 literal na secao nova do artigo,
e o artigo EN (artigo_en_v410.pysnip, no candidato) traz o qualificador com o parentese da validade ANTES do ponto e virgula: relative to the reader (the machine with the reader) (kernel validity, not creditation); the standard Turing machine without the reader stays outside.
O texto do candidato esta' certo (as duas metades do qualificador na mesma frase, com a validade dita); a checagem do conferidor passa a aceitar a forma literal OU a forma com o parentese da validade entre as duas metades (as metades LIDAS de DL.FRASE_QUALIFICADOR_EN).
Nao muda o candidato. Backup de BYTES; temporario -> conferir tamanho -> substituir; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "conferir_rito_v410.py"); BS = chr(92)
b0 = open(P, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
a = 'all(p_ in _sec410["en"] for p_ in (DL.FRASE_QUALIFICADOR_EN, "(kernel validity, not creditation)", "the gate does not move"))'
b = ('(DL.FRASE_QUALIFICADOR_EN in _sec410["en"] or bool(re.search(re.escape(DL.FRASE_QUALIFICADOR_EN.split("; ", 1)[0]) + r"' + BS + 's*' + BS + '(kernel validity, not creditation' + BS + ');' + BS + 's*" + re.escape(DL.FRASE_QUALIFICADOR_EN.split("; ", 1)[1]), _ws(_sec410["en"]))))'
     ' and all(p_ in _sec410["en"] for p_ in ("(kernel validity, not creditation)", "the gate does not move"))')
assert t.count(a) == 1, t.count(a); t = t.replace(a, b)
nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8"); ast.parse(nb)
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_pre_qualificador_en", "wb").write(b0)
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) > len(b0); os.replace(P + ".tmp", P)
print("conferir_rito_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16], "| CRLF", crlf)
