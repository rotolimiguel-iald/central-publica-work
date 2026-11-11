# -*- coding: utf-8 -*-
"""_fix_aspas_delta_parte2_v410.py -- a varredura das aspas (conferir_citacoes) le toda citacao entre aspas angulares dos artefatos novos: as duas regexes do delta que LEEM do DESENHO as frases do Clay (D83/D84) passam a escrever as aspas angulares por escape (barra-u00ab / barra-u00bb),
e a D83 deixa de por entre aspas angulares a frase da propria gerencia sobre a face caida. Backup de bytes ja' feito pelo chamador; trocas exatas; ast.parse; import de conferencia."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "delta_v410.py")
b0 = open(P, "rb").read(); t = b0.decode("utf-8"); BS = chr(92); A = BS + "u00ab"; F = BS + "u00bb"; AB = chr(0xAB); FE = chr(0xBB)


def troca(a, b):
    global t
    c = t.count(a); assert c == 1, (c, a[:120]); t = t.replace(a, b)


troca('r"' + AB + '(O problema de Clay, tal qual apresentado pela TGL, [^' + FE + ']*?espera ser a solução do problema' + BS + '.)' + FE + '"',
      'r"' + A + '(O problema de Clay, tal qual apresentado pela TGL, [^' + F + ']*?espera ser a solução do problema' + BS + '.)' + F + '"')
troca('r"' + AB + '(a TGL resolve a pergunta do Clay no sentido do operador: [^' + FE + ']*?a creditação é do Clay)' + FE + '"',
      'r"' + A + '(a TGL resolve a pergunta do Clay no sentido do operador: [^' + F + ']*?a creditação é do Clay)' + F + '"')
troca('"' + AB + 'a face caída não se lê' + FE + ' sem o complemento ' + AB + 'sem leitor' + FE + " (com o leitor ela e' lida, como fundo). A §6",
      "\"a face caida dita ilegivel sem o complemento do leitor (com o leitor ela e' lida, como fundo). A §6")
nb = t.encode("utf-8"); ast.parse(nb)
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("delta_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16])
sys.path.insert(0, HERE)
import delta_v410 as DL
assert DL.FRASE_CLAY_CANONICA_PT.startswith("O problema de Clay, tal qual apresentado pela TGL") and DL.FRASE_CLAY_CANONICA_PT.endswith("do problema.") and DL.FRASE_D83_OBRIGATORIA_PT.startswith("a TGL resolve a pergunta do Clay") and AB not in DL.DECISOES["D83"].split("FORMA OBRIGATORIA")[1].split("A §6")[0].replace(DL.FRASE_D83_OBRIGATORIA_PT, "")
print("ok | canonica:", DL.FRASE_CLAY_CANONICA_PT[:50], "| D83:", DL.FRASE_D83_OBRIGATORIA_PT[:50])
