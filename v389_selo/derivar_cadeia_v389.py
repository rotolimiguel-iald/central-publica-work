# -*- coding: utf-8 -*-
# Deriva leitura_v389.py, superficies_v389.py, patch_arvore_indice_v389.py e chain_pos_rito_v389.sh dos da v388 (troca de nomes/ancoras/topicos), com asserts de contagem.
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
S8 = r"C:\IALD\Central de Patentes\work\v388_selo"; S9 = r"C:\IALD\Central de Patentes\work\v389_selo"
rd = lambda n: open(os.path.join(S8, n), encoding="utf-8").read()


def wr(n, s):
    open(os.path.join(S9, n), "w", encoding="utf-8", newline="\n").write(s); print("ok", n)


def rep(s, pairs):
    for a, b in pairs:
        assert s.count(a) >= 1, (a[:90], s.count(a)); s = s.replace(a, b)
    return s


# ---- leitura
s = rd("leitura_v388.py")
s = rep(s, [("# A LEITURA da rodada v388 (molde: leitura_v387.py)", "# A LEITURA da rodada v389 (molde: leitura_v388.py)"), ('"v388_pacote"', '"v389_pacote"'),
            ("REG = (\"beta_runs_bounded_below_v388\", \"hubble_ratio_opening_v388\")", "REG = (\"text_label_errata_v389\",)"),
            ("'APLICADO_AO_CANONICO_*.json ausente no pacote v388'", "'APLICADO_AO_CANONICO_*.json ausente no pacote v389'"),
            ("'ESPERADOS_v388.json'", "'ESPERADOS_v389.json'"), ("'CANDIDATO_v388.json'", "'CANDIDATO_v389.json'"), ("'rodada_v388_stdout.txt'", "'rodada_v389_stdout.txt'"),
            ("'rodada_v388_stdout.txt ausente ou vazio'", "'rodada_v389_stdout.txt ausente ou vazio'"), ("'a base substituida != a v387 selada'", "'a base substituida != a v388 selada'"),
            ("if len([l for l in out.splitlines() if '[v388]' in l]) != 2:\n        P.append('o stdout nao tem as 2 linhas [v388]')",
             "if len([l for l in out.splitlines() if '[v389]' in l]) != 1:\n        P.append('o stdout nao tem a linha [v389]')"),
            ("'rito_horarios_v388.txt'", "'rito_horarios_v389.txt'"), ("if V['um_version'] != 'v388':\n        P.append('o selo nao e v388')", "if V['um_version'] != 'v389':\n        P.append('o selo nao e v389')"),
            ("'conferencia_rito_v388.json'", "'conferencia_rito_v389.json'"), ("'a conferencia do rito nao foi achada em v388_selo/conferidor'", "'a conferencia do rito nao foi achada em v389_selo/conferidor'"),
            ("V['n_ver'] = len(ESP['vereditos_v387'])", "V['n_ver'] = len(ESP['vereditos_v388'])")])
i = s.index("    br = core.get('beta_runs_bounded_below_v388')"); j = s.index("    qp = core.get('quantum_pillar_v384')")
s = s[:i] + ("    tl = core.get('text_label_errata_v389') or {}\n"
             "    V['tl'] = {'verdict': tl.get('verdict'), 'exam': tl.get('exam'), 'seal': tl.get('seal'), 'ledger': tl.get('ledger'),\n"
             "               'sites': [(x.get('id'), x.get('new_present'), x.get('old_absent')) for x in (tl.get('text_sites') or [])], 'files': {k: (v or {}).get('sha256') for k, v in (tl.get('files') or {}).items()}}\n"
             "    if not V['tl']['sites'] or not all(a and b for _, a, b in V['tl']['sites']):\n        P.append('as trocas de texto nao conferiram no registro v389')\n"
             "    V['exame'] = CM['exame']; V['ledger'] = CM['ledger']\n") + s[j:]
s = rep(s, [("print(json.dumps({k: v for k, v in V.items() if k not in ('ho',)}", "print(json.dumps({k: v for k, v in V.items() if k not in ('tl',)}")])
s = rep(s, [("do pacote (work\\v388_pacote)", "do pacote (work\\v389_pacote)")])
_ok388 = ("molde: leitura_v388.py", "a base substituida != a v388 selada", "ESP['vereditos_v388']")
assert all(any(o in l for o in _ok388) for l in s.splitlines() if "v388" in l), [l for l in s.splitlines() if "v388" in l]
wr("leitura_v389.py", s)
# ---- superficies
s = rd("superficies_v388.py")
s = rep(s, [("import leitura_v388, textos_v388 as T", "import leitura_v389, textos_v389 as T"), ("NOS = leitura_v388.NOS", "NOS = leitura_v389.NOS"), ("leitura_v388.ler()", "leitura_v389.ler()"),
            ("MARCA_BAK = '_sup388'", "MARCA_BAK = '_sup389'"), ("'<!-- adendo_v388_selada -->'", "'<!-- adendo_v389_selada -->'"), ("'<!-- atlas_v388_selada -->'", "'<!-- atlas_v389_selada -->'"),
            ("MARCA = '**v388 SELADA %s `%s`'", "MARCA = '**v389 SELADA %s `%s`'"), ("SUPERFICIES v388:", "SUPERFICIES v389:"), ("ja tem a v388 (idempotente)", "ja tem a v389 (idempotente)")])
i = s.index("for nome, bloco, marca in (('missao-ultima-flag-um-py.md'"); j = s.index("# ---- MEMORY.md")
s = s[:i] + (
    "for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.marca_topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.marca_central(V))):\n"
    "    append(os.path.join(UMEM, nome), bloco, marca or bloco.split(chr(10), 2)[1][:60])\n") + s[j:]
i = s.index("TROCAS = ["); j = s.index("]\nif any(MARCA in l for l in lines):")
s = s[:i] + (
    "TROCAS = [  # (o link que identifica a linha, a linha nova) -- a velha vai inteira ao MEMORY_2\n"
    "    ('(missao-ultima-flag-um-py.md)', \"- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — \" + T.marca_missao(V) + \"íntegra anterior no MEMORY_2.md (movida %s)\" % V['data'][:5]),\n"
    "    ('(handoff-v387-custodia.md)', \"- [HANDOFF v387](handoff-v387-custodia.md) — íntegra no MEMORY_2.md (movida %s)\" % V['data'][:5]),\n") + s[j:]
s = rep(s, [("kh = [i for i, l in enumerate(lines) if '(handoff-v387-custodia.md)' in l and l.startswith('- [HANDOFF v387')]",
             "kh = [i for i, l in enumerate(lines) if '(handoff-v388-custodia.md)' in l and l.startswith('- [HANDOFF v388')]"),
            ("tornadas velhas pela v388", "tornadas velhas pela v389"), ("(v388) -->", "(v389) -->")])
wr("superficies_v389.py", s)
# ---- patch arvore/indice
s = rd("patch_arvore_indice_v388.py")
s = rep(s, [("import leitura_v388, textos_v388", "import leitura_v389, textos_v389"), ("leitura_v388.ler()", "leitura_v389.ler()"), ("textos_v388.", "textos_v389."), ("_p388", "_p389"),
            ("TAG_A = '- **O ACOPLAMENTO CORRE COM A ESCALA (v388)'", "TAG_A = '- **AS ERRATAS DE TEXTO E RÓTULO (v389)'"),
            ("l.startswith(\"L.append('- **OS TRÊS TESTES CONJUNTOS (v387)\")", "l.startswith(\"L.append('- **O ACOPLAMENTO CORRE COM A ESCALA (v388)\")"), ("('ancora v387'", "('ancora v388'"),
            ("'L.append(%s)   # v388'", "'L.append(%s)   # v389'"), ("+linha (v388)", "+linha (v389)"), ("a linha v388 ja esta", "a linha v389 ja esta"),
            ("if 'v388_incorporacao_manifesto' not in s:", "if 'v389_incorporacao_manifesto' not in s:"), ("i = acha('_i387p = ')", "i = acha('_i388p = ')"),
            ("_i388p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v388_incorporacao_manifesto.json'); _i388 = json.load(open(_i388p, encoding='utf-8')) if os.path.exists(_i388p) else {}   # v388",
             "_i389p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v389_incorporacao_manifesto.json'); _i389 = json.load(open(_i389p, encoding='utf-8')) if os.path.exists(_i389p) else {}   # v389"),
            ("'_V388TXT = %s   # v388'", "'_V389TXT = %s   # v389'"), ("i = acha(\" ('Os três testes conjuntos; Fases 9 e 8 por hash (v387):'\")", "i = acha(\" ('O acoplamento corre com a escala; a Fase 9 aberta (v388):'\")"),
            ("\" (%s, _V388TXT),\"", "\" (%s, _V389TXT),\""), ("i = acha(\"       '- **Os três testes conjuntos (v387)\")", "i = acha(\"       '- **β escalar ≥ β₀; Fase 9 aberta (v388)\")"),
            ("s.count('v388_incorporacao_manifesto') == 1 and s.count('_i388p') == 3 and s.count('_V388TXT') == 2, (s.count('v388_incorporacao_manifesto'), s.count('_i388p'), s.count('_V388TXT'))",
             "s.count('v389_incorporacao_manifesto') == 1 and s.count('_i389p') == 3 and s.count('_V389TXT') == 2, (s.count('v389_incorporacao_manifesto'), s.count('_i389p'), s.count('_V389TXT'))"),
            ("+manifesto +verbete +remissivo (v388)", "+manifesto +verbete +remissivo (v389)"), ("a v388 ja esta (idempotente)", "a v389 ja esta (idempotente)")])
wr("patch_arvore_indice_v389.py", s)
# ---- a cadeia
s = rd("chain_pos_rito_v388.sh").replace("v388", "v389").replace("v387", "v388")
s = rep(s, [('TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md fase9-razao-de-hubble-05out.md beta-escalar-limitado-inferiormente-06out.md"',
             'TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md"')])
wr("chain_pos_rito_v389.sh", s)
