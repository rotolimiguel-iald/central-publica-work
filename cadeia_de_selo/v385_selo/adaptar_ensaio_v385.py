# -*- coding: utf-8 -*-
"""Adapta o ensaio_v385.py (gerado pelo conversor): as memorias-topico da v385; a variante da reprodutibilidade (argumento BIT|DIFERENTE, passada ao montar);
o conferidor de textos da v385 no lugar do testar_formatos da v384; as marcas das ferramentas da v385. E corrige a contagem do manifesto no patch do indice
(o nome aparece na linha de carga E no remissivo: 2). Pares contados; backup de bytes; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
st = time.strftime("%Y%m%d_%H%M%S")


def aplica(nome, pares):
    P = os.path.join(HERE, nome)
    s0 = open(P, encoding="utf-8", newline="").read(); s = s0
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (nome, "a troca nao e unica", n, a[:100])
        s = s.replace(a, b)
    ast.parse(s)
    open(P + ".bak_" + st + "_adapt", "wb").write(s0.encode("utf-8"))
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
    print("OK", nome, len(pares), "trocas")


aplica("ensaio_v385.py", [
    ("TOPICOS = ('missao-ultima-flag-um-py.md', 'central-de-patentes-estado.md', 'beta-e-a-regra-matriz-02out.md', 'regra-dos-dois-regimes.md', 'v382-custodia-suspensa.md', 'v384-pilar-quantico-gpu-02out.md')",
     "TOPICOS = ('missao-ultima-flag-um-py.md', 'central-de-patentes-estado.md', 'um-posto-jamais-pressuposto-e-h2-17set.md', 'v384-pilar-quantico-gpu-02out.md')\n"
     "VAR = (sys.argv[1] if len(sys.argv) > 1 else 'BIT').upper(); assert VAR in ('BIT', 'DIFERENTE'), VAR   # a variante da reprodutibilidade no Nos sintetico"),
    ("ENV_S = dict(os.environ, PYTHONIOENCODING='utf-8', V385_NOS=NOS_S,", "ENV_S = dict(os.environ, PYTHONIOENCODING='utf-8', V385_SINT_REPRO=VAR, V385_NOS=NOS_S,"),
    ("roda('testar_formatos', ['testar_formatos_v385.py'], ENV_S)\n", ""),
    ("roda('superficies_idemp', ['superficies_v385.py'], ENV_R)\n",
     "roda('superficies_idemp', ['superficies_v385.py'], ENV_R)\nroda('conferir_textos', ['conferir_textos_v385.py'], ENV_S)\n"),
    ("RES['ferramentas'] = {'arvore_linha_v385': tools['arvore_da_prova.py'].count('- **O PILAR QUÂNTICO (v385)'), 'atlas_manifesto_v385': tools['atlas_indice.py'].count('v385_incorporacao_manifesto'),",
     "RES['ferramentas'] = {'arvore_linha_v385': tools['arvore_da_prova.py'].count('- **O AXIOMA (v385)'), 'atlas_manifesto_v385': tools['atlas_indice.py'].count('v385_incorporacao_manifesto'),"),
    ("RES['numeros_do_core_sintetico_nos_textos'] = json.load(open(os.path.join(SAI, 'testar_formatos_v385.json'), encoding='utf-8'))['numeros_de_V_no_diario']",
     "RES['textos'] = json.load(open(os.path.join(SAI, 'conferir_textos_v385.json'), encoding='utf-8')); RES['variante'] = VAR"),
    ("all(v for v in RES['numeros_do_core_sintetico_nos_textos'].values())", "RES['textos']['ok'] is True"),
    ("open(os.path.join(SAI, 'ensaio_resultado_v385.json'), 'w', encoding='utf-8')", "open(os.path.join(SAI, 'ensaio_resultado_v385_%s.json' % VAR), 'w', encoding='utf-8')"),
])
aplica("patch_arvore_indice_v385.py", [
    ("assert s.count('v385_incorporacao_manifesto') == 1 and s.count('_i385p') == 3", "assert s.count('v385_incorporacao_manifesto') == 2 and s.count('_i385p') == 3"),
])
