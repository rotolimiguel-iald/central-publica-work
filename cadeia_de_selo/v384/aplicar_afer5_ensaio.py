# -*- coding: utf-8 -*-
"""5a afericao no ENSAIO A SECO: a variante sem_cache_d128 exige a frase PROPRIA do ramo; o artigo de SUCESSO nao pode trazer a frase da referencia na CPU
(ela e' so dos vereditos anulados pela CPU); o comentario e a docstring dizem que o W08c leva a marca na linha e que os enunciados do terceiro balde saem do
fluxo e sao conferidos por nome e executados a parte. Backup ja feito (.bak_antes_afer5)."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "ensaio_a_seco_v384.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer5", "rb").read() == raw
PAIRS = [
    ('''(3) o FLUXO PRINCIPAL: as instrucoes de main() que COMECAM numa linha marcada v384 sao EXECUTADAS''',
     '''(3) o FLUXO PRINCIPAL: as instrucoes de main() que COMECAM numa linha marcada v384 (exceto as do terceiro balde, que leem variaveis locais do main e sao
    conferidas por nome e executadas A PARTE, em bloco, com core sintetico) sao EXECUTADAS'''),
    ('''# os enunciados do TERCEIRO BALDE leem variaveis locais do main (_not_sealed, _formais, _recusas, _computacao): nao vao ao fluxo executado; o bloco inteiro roda
# a parte, abaixo (4a afericao)''', '''# os enunciados do TERCEIRO BALDE (W08, W08b e o W08c, que leva a marca v384 na linha) leem variaveis locais do main (_not_sealed, _formais, _recusas,
# _computacao): saem do fluxo executado, sao conferidos por nome e o bloco inteiro roda a parte, abaixo (4a e 5a afericoes)'''),
    ('''                           {"pt": ["não foi guardado para reaproveitamento"], "en": ["not stored for reuse"]})}''',
     '''                           {"pt": ["não foi guardado para reaproveitamento", "o cache só guarda o resultado completo com ele"],
                            "en": ["not stored for reuse", "the cache keeps only a complete result with it"]})}'''),
    ('''                           "faltam": [w for w in DEVE[lang] if w not in txt and w not in tex],''',
     '''                           "faltam": [w for w in DEVE[lang] if w not in txt and w not in tex],
                           # o SUCESSO nao traz a frase da referencia na CPU (so os vereditos anulados pela CPU a trazem; 5a afericao)
                           "nao_devia_ter": [w for w in {"pt": ["A referência na CPU, nesta rodada", "A referência na CPU não estava presente"],
                                                         "en": ["The CPU reference, in this run", "The CPU reference was not present"]}[lang] if w in txt],'''),
    ('''mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"]]''',
     '''mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v.get("nao_devia_ter")]'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s)
open(P + ".tmp", "wb").write(s.encode("utf-8")); os.replace(P + ".tmp", P); print("ok", len(PAIRS))
