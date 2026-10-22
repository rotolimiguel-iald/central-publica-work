# -*- coding: utf-8 -*-
# Deriva leitura_v390.py (da leitura_v388: escada, pedra, conferidor), superficies_v390.py, patch_arvore_indice_v390.py e chain_pos_rito_v390.sh (dos da v389), com asserts.
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
S8 = r"C:\IALD\Central de Patentes\work\v388_selo"; S9 = r"C:\IALD\Central de Patentes\work\v389_selo"; S0 = r"C:\IALD\Central de Patentes\work\v390_selo"
rd = lambda d, n: open(os.path.join(d, n), encoding="utf-8").read()


def wr(n, s):
    open(os.path.join(S0, n), "w", encoding="utf-8", newline="\n").write(s); print("ok", n)


def rep(s, pairs):
    for a, b in pairs:
        assert s.count(a) >= 1, (a[:90], s.count(a)); s = s.replace(a, b)
    return s


# ---- leitura (da v388)
s = rd(S8, "leitura_v388.py")
s = rep(s, [("# A LEITURA da rodada v388 (molde: leitura_v387.py)", "# A LEITURA da rodada v390 (molde: leitura_v388.py)"), ("(work\\v388_pacote)", "(work\\v390_pacote)"), ('"v388_pacote"', '"v390_pacote"'),
            ("REG = (\"beta_runs_bounded_below_v388\", \"hubble_ratio_opening_v388\")", "REG = (\"fundacao_v390\",)"),
            ("'APLICADO_AO_CANONICO_*.json ausente no pacote v388'", "'APLICADO_AO_CANONICO_*.json ausente no pacote v390'"),
            ("'ESPERADOS_v388.json'", "'ESPERADOS_v390.json'"), ("'CANDIDATO_v388.json'", "'CANDIDATO_v390.json'"), ("'rodada_v388_stdout.txt'", "'rodada_v390_stdout.txt'"),
            ("'rodada_v388_stdout.txt ausente ou vazio'", "'rodada_v390_stdout.txt ausente ou vazio'"), ("'a base substituida != a v387 selada'", "'a base substituida != a v389 selada'"),
            ("if len([l for l in out.splitlines() if '[v388]' in l]) != 2:\n        P.append('o stdout nao tem as 2 linhas [v388]')",
             "if len([l for l in out.splitlines() if '[v390]' in l]) != 1:\n        P.append('o stdout nao tem a linha [v390]')"),
            ("'rito_horarios_v388.txt'", "'rito_horarios_v390.txt'"), ("if V['um_version'] != 'v388':\n        P.append('o selo nao e v388')", "if V['um_version'] != 'v390':\n        P.append('o selo nao e v390')"),
            ("'conferencia_rito_v388.json'", "'conferencia_rito_v390.json'"), ("'a conferencia do rito nao foi achada em v388_selo/conferidor'", "'a conferencia do rito nao foi achada em v390_selo/conferidor'"),
            ("V['n_ver'] = len(ESP['vereditos_v387'])", "V['n_ver'] = len(ESP['vereditos_v389'])")])
i = s.index("    br = core.get('beta_runs_bounded_below_v388')"); j = s.index("    qp = core.get('quantum_pillar_v384')")
s = s[:i] + ("    fd = core.get('fundacao_v390') or {}\n"
             "    V['fd'] = {k: fd.get(k) for k in ('verdict', 'kernel_flags_ok', 'kernel_flags_total', 'leitura', 'recusa', 'passagem', 'estatuto_do_fecho', 'not_claimed', 'borchers', 'pedra')}\n"
             "    V['pedra16'] = ESP['pedra_sha16']; V['verbatins'] = CM['verbatins']; V['ledger'] = ESP['ledger']\n"
             "    V['tl9'] = (core.get('text_label_errata_v389') or {}).get('verdict')\n") + s[j:]
s = rep(s, [("print(json.dumps({k: v for k, v in V.items() if k not in ('ho',)}", "print(json.dumps({k: v for k, v in V.items() if k not in ('fd',)}")])
assert "v388" not in s.replace("molde: leitura_v388.py", ""), [l for l in s.splitlines() if "v388" in l]
wr("leitura_v390.py", s)
# ---- superficies (da v389)
s = rd(S9, "superficies_v389.py")
s = rep(s, [("import leitura_v389, textos_v389 as T", "import leitura_v390, textos_v390 as T"), ("NOS = leitura_v389.NOS", "NOS = leitura_v390.NOS"), ("leitura_v389.ler()", "leitura_v390.ler()"),
            ("MARCA_BAK = '_sup389'", "MARCA_BAK = '_sup390'"), ("'<!-- adendo_v389_selada -->'", "'<!-- adendo_v390_selada -->'"), ("'<!-- atlas_v389_selada -->'", "'<!-- atlas_v390_selada -->'"),
            ("MARCA = '**v389 SELADA %s `%s`'", "MARCA = '**v390 SELADA %s `%s`'"), ("SUPERFICIES v389:", "SUPERFICIES v390:"), ("ja tem a v389 (idempotente)", "ja tem a v390 (idempotente)")])
i = s.index("for nome, bloco, marca in (('missao-ultima-flag-um-py.md'"); j = s.index("# ---- MEMORY.md")
s = s[:i] + (
    "for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.marca_topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.marca_central(V)),\n"
    "                           ('superposicao-e-a-passagem-07out.md', T.topico_superposicao(V), None), ('o-fechamento-lema3-impossiveis.md', T.topico_lema3(V), None)):\n"
    "    append(os.path.join(UMEM, nome), bloco, marca or bloco.split(chr(10), 2)[1][:60])\n") + s[j:]
i = s.index("TROCAS = ["); j = s.index("]\nif any(MARCA in l for l in lines):")
s = s[:i] + (
    "TROCAS = [  # (o trecho que identifica a linha, a linha nova) -- a velha vai inteira ao MEMORY_2\n"
    "    ('(missao-ultima-flag-um-py.md)', \"- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — \" + T.marca_missao(V) + \"íntegra anterior no MEMORY_2.md (movida %s)\" % V['data'][:5]),\n"
    "    ('[HANDOFF v383 — ', \"- [HANDOFF v383](handoff-v383-custodia.md) — íntegra no MEMORY_2.md (movida %s)\" % V['data'][:5]),\n"
    "    ('[HANDOFF v381 — A REGRA MATRIZ no kernel', \"- [HANDOFF v381 (no kernel)](handoff-v381-custodia.md) — íntegra no MEMORY_2.md (movida %s)\" % V['data'][:5]),\n") + s[j:]
s = rep(s, [("kh = [i for i, l in enumerate(lines) if '(handoff-v388-custodia.md)' in l and l.startswith('- [HANDOFF v388')]",
             "kh = [i for i, l in enumerate(lines) if '(handoff-custodia-conjunta-v383-v389-06out.md)' in l and l.startswith('- [HANDOFF CUSTÓDIA CONJUNTA v383')]"),
            ("tornadas velhas pela v389", "tornadas velhas pela v390"), ("(v389) -->", "(v390) -->")])
wr("superficies_v390.py", s)
# ---- patch arvore/indice (da v389)
s = rd(S9, "patch_arvore_indice_v389.py")
s = rep(s, [("import leitura_v389, textos_v389", "import leitura_v390, textos_v390"), ("leitura_v389.ler()", "leitura_v390.ler()"), ("textos_v389.", "textos_v390."), ("_p389", "_p390"),
            ("TAG_A = '- **AS ERRATAS DE TEXTO E RÓTULO (v389)'", "TAG_A = '- **A FUNDAÇÃO — A SUPERPOSIÇÃO É A PASSAGEM (v390)'"),
            ("l.startswith(\"L.append('- **O ACOPLAMENTO CORRE COM A ESCALA (v388)\")", "l.startswith(\"L.append('- **AS ERRATAS DE TEXTO E RÓTULO (v389)\")"), ("('ancora v388'", "('ancora v389'"),
            ("'L.append(%s)   # v389'", "'L.append(%s)   # v390'"), ("+linha (v389)", "+linha (v390)"), ("a linha v389 ja esta", "a linha v390 ja esta"),
            ("if 'v389_incorporacao_manifesto' not in s:", "if 'v390_incorporacao_manifesto' not in s:"), ("i = acha('_i388p = ')", "i = acha('_i389p = ')"),
            ("_i389p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v389_incorporacao_manifesto.json'); _i389 = json.load(open(_i389p, encoding='utf-8')) if os.path.exists(_i389p) else {}   # v389",
             "_i390p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v390_incorporacao_manifesto.json'); _i390 = json.load(open(_i390p, encoding='utf-8')) if os.path.exists(_i390p) else {}   # v390"),
            ("'_V389TXT = %s   # v389'", "'_V390TXT = %s   # v390'"), ("i = acha(\" ('O acoplamento corre com a escala; a Fase 9 aberta (v388):'\")", "i = acha(\" ('As erratas de texto e rótulo do exame da v388 (v389):'\")"),
            ("\" (%s, _V389TXT),\"", "\" (%s, _V390TXT),\""), ("i = acha(\"       '- **β escalar ≥ β₀; Fase 9 aberta (v388)\")", "i = acha(\"       '- **Erratas de texto e rótulo; o exame da v388 (v389)\")"),
            ("s.count('v389_incorporacao_manifesto') == 1 and s.count('_i389p') == 3 and s.count('_V389TXT') == 2, (s.count('v389_incorporacao_manifesto'), s.count('_i389p'), s.count('_V389TXT'))",
             "s.count('v390_incorporacao_manifesto') == 1 and s.count('_i390p') == 3 and s.count('_V390TXT') == 2, (s.count('v390_incorporacao_manifesto'), s.count('_i390p'), s.count('_V390TXT'))"),
            ("+manifesto +verbete +remissivo (v389)", "+manifesto +verbete +remissivo (v390)"), ("a v389 ja esta (idempotente)", "a v390 ja esta (idempotente)")])
wr("patch_arvore_indice_v390.py", s)
# ---- a cadeia (da v389)
s = rd(S9, "chain_pos_rito_v389.sh").replace("v389", "v390").replace("v388", "v389")
s = rep(s, [('TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md"',
             'TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md superposicao-e-a-passagem-07out.md o-fechamento-lema3-impossiveis.md"')])
wr("chain_pos_rito_v390.sh", s)
