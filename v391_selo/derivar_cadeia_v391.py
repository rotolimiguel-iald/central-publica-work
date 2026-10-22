# -*- coding: utf-8 -*-
# Deriva leitura_v391.py, superficies_v391.py, patch_arvore_indice_v391.py, chain_pos_rito_v391.sh, fechar_v391.py e errata_claude_md_v391.py dos da v390, com asserts.
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
S0 = r"C:\IALD\Central de Patentes\work\v390_selo"; S1 = r"C:\IALD\Central de Patentes\work\v391_selo"
rd = lambda d, n: open(os.path.join(d, n), encoding="utf-8").read()


def wr(n, s):
    open(os.path.join(S1, n), "w", encoding="utf-8", newline="\n").write(s); print("ok", n)


def rep(s, pairs):
    for a, b in pairs:
        assert s.count(a) >= 1, (a[:100], s.count(a)); s = s.replace(a, b)
    return s


# ---- leitura
s = rd(S0, "leitura_v390.py")
s = rep(s, [("# A LEITURA da rodada v390 (molde: leitura_v388.py)", "# A LEITURA da rodada v391 (molde: leitura_v390.py)"), ("(work\\v390_pacote)", "(work\\v391_pacote)"), ('"v390_pacote"', '"v391_pacote"'),
            ('REG = ("fundacao_v390",)', 'REG = ("estatuto_da_prova_v391",)'), ("'APLICADO_AO_CANONICO_*.json ausente no pacote v390'", "'APLICADO_AO_CANONICO_*.json ausente no pacote v391'"),
            ("'ESPERADOS_v390.json'", "'ESPERADOS_v391.json'"), ("'CANDIDATO_v390.json'", "'CANDIDATO_v391.json'"), ("'rodada_v390_stdout.txt'", "'rodada_v391_stdout.txt'"),
            ("'rodada_v390_stdout.txt ausente ou vazio'", "'rodada_v391_stdout.txt ausente ou vazio'"), ("'a base substituida != a v389 selada'", "'a base substituida != a v390 selada'"),
            ("if len([l for l in out.splitlines() if '[v390]' in l]) != 1:\n        P.append('o stdout nao tem a linha [v390]')",
             "if len([l for l in out.splitlines() if '[v391]' in l]) != 1:\n        P.append('o stdout nao tem a linha [v391]')"),
            ("'rito_horarios_v390.txt'", "'rito_horarios_v391.txt'"), ("if V['um_version'] != 'v390':\n        P.append('o selo nao e v390')", "if V['um_version'] != 'v391':\n        P.append('o selo nao e v391')"),
            ("'conferencia_rito_v390.json'", "'conferencia_rito_v391.json'"), ("'a conferencia do rito nao foi achada em v390_selo/conferidor'", "'a conferencia do rito nao foi achada em v391_selo/conferidor'"),
            ("V['n_ver'] = len(ESP['vereditos_v389'])", "V['n_ver'] = len(ESP['vereditos_v390'])")])
i = s.index("    fd = core.get('fundacao_v390') or {}"); j = s.index("    qp = core.get('quantum_pillar_v384')")
s = s[:i] + ("    ep = core.get('estatuto_da_prova_v391') or {}\n"
             "    V['ep'] = {k: ep.get(k) for k in ('verdict', 'falhas', 'a_regua', 'prova_1_kernel', 'prova_2_ritos', 'prova_3_gpu', 'certificacao', 'nao_declarado')}\n"
             "    V['verbatim'] = CM['verbatim']; V['fd390'] = (core.get('fundacao_v390') or {}).get('verdict')\n") + s[j:]
s = rep(s, [("print(json.dumps({k: v for k, v in V.items() if k not in ('fd',)}", "print(json.dumps({k: v for k, v in V.items() if k not in ('ep',)}")])
_proib = ("v390_pacote", "rodada_v390", "ESPERADOS_v390", "CANDIDATO_v390", "conferencia_rito_v390", "rito_horarios_v390", "'[v390]'", "v390_selo", "'v390'")
assert not any(x in s for x in _proib), [l for l in s.splitlines() if any(x in l for x in _proib)]
wr("leitura_v391.py", s)
# ---- superficies
s = rd(S0, "superficies_v390.py")
s = rep(s, [("import leitura_v390, textos_v390 as T", "import leitura_v391, textos_v391 as T"), ("NOS = leitura_v390.NOS", "NOS = leitura_v391.NOS"), ("leitura_v390.ler()", "leitura_v391.ler()"),
            ("MARCA_BAK = '_sup390'", "MARCA_BAK = '_sup391'"), ("'<!-- adendo_v390_selada -->'", "'<!-- adendo_v391_selada -->'"), ("'<!-- atlas_v390_selada -->'", "'<!-- atlas_v391_selada -->'"),
            ("MARCA = '**v390 SELADA %s `%s`'", "MARCA = '**v391 SELADA %s `%s`'"), ("SUPERFICIES v390:", "SUPERFICIES v391:"), ("ja tem a v390 (idempotente)", "ja tem a v391 (idempotente)"),
            ("tornadas velhas pela v390", "tornadas velhas pela v391"), ("(v390) -->", "(v391) -->")])
i = s.index("for nome, bloco, marca in (('missao-ultima-flag-um-py.md'"); j = s.index("# ---- MEMORY.md")
s = s[:i] + (
    "for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.marca_topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.marca_central(V)),\n"
    "                           ('estatuto-da-prova-07out.md', T.topico_estatuto(V), None)):\n"
    "    append(os.path.join(UMEM, nome), bloco, marca or bloco.split(chr(10), 2)[1][:60])\n") + s[j:]
i = s.index("TROCAS = ["); j = s.index("]\nif any(MARCA in l for l in lines):")
s = s[:i] + (
    "TROCAS = [  # (o trecho que identifica a linha, a linha nova) -- a velha vai inteira ao MEMORY_2\n"
    "    ('(missao-ultima-flag-um-py.md)', \"- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — \" + T.marca_missao(V) + \"íntegra anterior no MEMORY_2.md (movida %s)\" % V['data'][:5]),\n"
    "    ('[Fases 1–3 (30/09)](fase1-eff-30set.md) · ', \"- [Fases 1–4 (30/09)](fase1-eff-30set.md) — íntegra no MEMORY_2.md (movida %s)\" % V['data'][:5]),\n") + s[j:]
assert "v390" not in s, [l for l in s.splitlines() if "v390" in l]
wr("superficies_v391.py", s)
# ---- patch arvore/indice
s = rd(S0, "patch_arvore_indice_v390.py")
s = rep(s, [("import leitura_v390, textos_v390", "import leitura_v391, textos_v391"), ("leitura_v390.ler()", "leitura_v391.ler()"), ("textos_v390.", "textos_v391."), ("_p390", "_p391"),
            ("TAG_A = '- **A FUNDAÇÃO — A SUPERPOSIÇÃO É A PASSAGEM (v390)'", "TAG_A = '- **O ESTATUTO DA PROVA (v391)'"),
            ("l.startswith(\"L.append('- **AS ERRATAS DE TEXTO E RÓTULO (v389)\")", "l.startswith(\"L.append('- **A FUNDAÇÃO — A SUPERPOSIÇÃO É A PASSAGEM (v390)\")"), ("('ancora v389'", "('ancora v390'"),
            ("'L.append(%s)   # v390'", "'L.append(%s)   # v391'"), ("+linha (v390)", "+linha (v391)"), ("a linha v390 ja esta", "a linha v391 ja esta"),
            ("if 'v390_incorporacao_manifesto' not in s:", "if 'v391_incorporacao_manifesto' not in s:"), ("i = acha('_i389p = ')", "i = acha('_i390p = ')"),
            ("_i390p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v390_incorporacao_manifesto.json'); _i390 = json.load(open(_i390p, encoding='utf-8')) if os.path.exists(_i390p) else {}   # v390",
             "_i391p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v391_incorporacao_manifesto.json'); _i391 = json.load(open(_i391p, encoding='utf-8')) if os.path.exists(_i391p) else {}   # v391"),
            ("'_V390TXT = %s   # v390'", "'_V391TXT = %s   # v391'"), ("i = acha(\" ('As erratas de texto e rótulo do exame da v388 (v389):'\")", "i = acha(\" ('A Fundação: a superposição é a passagem (a cláusula Ágape) (v390):'\")"),
            ("\" (%s, _V390TXT),\"", "\" (%s, _V391TXT),\""), ("i = acha(\"       '- **Erratas de texto e rótulo; o exame da v388 (v389)\")", "i = acha(\"       '- **A Fundação; a cláusula Ágape; o GLOBAL_LIFT como superposição (v390)\")"),
            ("s.count('v390_incorporacao_manifesto') == 1 and s.count('_i390p') == 3 and s.count('_V390TXT') == 2, (s.count('v390_incorporacao_manifesto'), s.count('_i390p'), s.count('_V390TXT'))",
             "s.count('v391_incorporacao_manifesto') == 1 and s.count('_i391p') == 3 and s.count('_V391TXT') == 2, (s.count('v391_incorporacao_manifesto'), s.count('_i391p'), s.count('_V391TXT'))"),
            ("+manifesto +verbete +remissivo (v390)", "+manifesto +verbete +remissivo (v391)"), ("a v390 ja esta (idempotente)", "a v391 ja esta (idempotente)")])
wr("patch_arvore_indice_v391.py", s)
# ---- a cadeia
s = rd(S0, "chain_pos_rito_v390.sh").replace("v390", "v391").replace("v389", "v390")
s = rep(s, [('TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md superposicao-e-a-passagem-07out.md o-fechamento-lema3-impossiveis.md"',
             'TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md estatuto-da-prova-07out.md"')])
wr("chain_pos_rito_v391.sh", s)
# ---- fechar
s = rd(S0, "fechar_v390.py")
_a = s.index('"""'); _b = s.index('"""', _a + 3) + 3
s = s[:_a] + ('"""fechar_v391.py -- DEPOIS da cadeia pos-rito (molde: fechar_v390.py): (1) o manifesto de incorporacao v391 -> v391_selo e a pasta das ferramentas; (2) o ARQUIVO do\n'
              'pacote e da cadeia -> work\\\\cadeia_de_selo\\\\v391 (+_selo); (3) o HANDOFF (memory\\\\handoff-v391-custodia.md + Nos\\\\HANDOFF_v391_CUSTODIA.md) para a sessao do site.\n'
              'Guarda: a leitura sem problema. Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""') + s[_b:]
s = rep(s, [("import leitura_v390 as L", "import leitura_v391 as L"), ("import textos_v390 as T", "import textos_v391 as T"), ("_f390", "_f391")])
i = s.index("KD = os.path.join(WK, \"v390_kernel\")"); j = s.index("TOOLS = os.path.join(WK, \"cadeia_de_selo\")")
s = s[:i] + "OD = PK   # v391: o verbatim do operador mora no proprio pacote; nenhum kernel novo\n" + s[j:]
s = rep(s, [('m = {"stamp": ST, "versao": "v390", "instalacao": os.path.basename(app), "base_v389": V["base16"],', 'm = {"stamp": ST, "versao": "v391", "instalacao": os.path.basename(app), "base_v390": V["base16"],'),
            ('     "kernel": {"sandbox": KS, "pedra_sha16": V["pedra16"], "build_full_log_sha16": s16(os.path.join(KD, "build_full.log"))}, "patches": V["patches"], "teoremas": V["teor"],',
             '     "kernel": "nenhum kernel novo na v391", "patches": V["patches"], "teoremas": V["teor"],'),
            ('     "registros_v390": {k: V[k] for k in L.REG}, "fundacao": V["fd"], "verbatins": V["verbatins"], "ledger": V["ledger"], "pilar": V["pilar"],',
             '     "registros_v391": {k: V[k] for k in L.REG}, "estatuto": V["ep"], "verbatim": V["verbatim"], "fundacao_v390": V["fd390"], "pilar": V["pilar"],'),
            ('     "ordem": {f: s16(os.path.join(OD, f)) for f in sorted(os.listdir(OD)) if os.path.isfile(os.path.join(OD, f))},\n', '     "ordem": {"OPERADOR_07out_estatuto_verbatim.txt": s16(os.path.join(PK, "OPERADOR_07out_estatuto_verbatim.txt"))},\n'),
            ('"v390_incorporacao_manifesto.json"', '"v391_incorporacao_manifesto.json"')])
i = s.index("for f in sorted(os.listdir(KD)):"); j = s.index("for raiz, dirs, fs in os.walk(HERE):")
s = s[:i] + s[j:]
s = s.replace('os.path.join(TOOLS, "v390", os.path.relpath(p, PK))', 'os.path.join(TOOLS, "v391", os.path.relpath(p, PK))')
s = s.replace('os.path.join(TOOLS, "v390_selo", os.path.relpath(p, HERE))', 'os.path.join(TOOLS, "v391_selo", os.path.relpath(p, HERE))')
s = s.replace('grava(os.path.join(TOOLS, "v390", "MANIFESTO_ARQUIVO_v390.json")', 'grava(os.path.join(TOOLS, "v391", "MANIFESTO_ARQUIVO_v391.json")')
i = s.index("stone_nos = os.path.join(NOS, \"tgl_kernel\", \"TGLExt\", \"Fundacao.lean\")"); j = s.index("assert \"CONF\" + \"IRMED\" not in doc")
s = s[:i] + (
    "doc = (\"---\\nname: handoff-v391-custodia\\ndescription: \\\"HANDOFF v391 (%s) para a sessão do site: o estatuto da prova — provada (validade); a confirmação recusada é creditação; `%s`; custódia + README/site + pendências do operador\\\"\\n\"\n"
    "       \"metadata:\\n  type: project\\n---\\n\\n# HANDOFF v391 — CUSTÓDIA (%s)\\n\\n\"\n"
    "       \"**O que é:** `um.py` **v391** `%s` (%s B) sobre a v390 `%s`; %s; COMPLETA; rc %s; selftest PASSED; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); pilar %s pela chave. \"\n"
    "       \"Selo `%s`.\\n\\n**O que entrou e o que mediu:** %s.\\n\\n\"\n"
    "       \"**Para a sessão do site (custódia):** o `um.py` v391, `rodada_v391_stdout.txt`, o selo, o core, o .md canônico e o manifesto, os artigos PT/EN (%s) e o verbatim do operador \"\n"
    "       \"(`work\\\\v391_pacote\\\\OPERADOR_07out_estatuto_verbatim.txt`, sha16 `%s`) — com PORTA gerada por script; backup da versão no espelho, fora do repo; blob conferido; o um.py tem > 5 MB (a porta é o raw). \"\n"
    "       \"O README e o site com o estatuto da prova foram preparados pela gerência c1 (sem subir; ver a memória `estatuto-da-prova-07out.md`). Commit/push = operador.\\n\\n\"\n"
    "       \"**Pendências SÓ do operador:** vetar ou ratificar a v391; a custódia; subir o README e o site; commit/push. A Fase 9 (bandeiras do V1, executor D6) segue fora, decisão dele.\\n\\n\"\n"
    "       \"Pacote `work\\\\v391_pacote`; cadeia `work\\\\v391_selo`; arquivo `work\\\\cadeia_de_selo\\\\v391` (+`_selo`). NOT_FALSIFIED nunca é confirmação; o gate não se move.\\n\\n\"\n"
    "       \"[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v390-custodia]]\\n\") % (\n"
    "    V[\"data\"], V[\"s16\"], V[\"data\"], V[\"s16\"], format(V[\"umb\"], \",\"), V[\"base16\"], V[\"teor\"], V[\"rc\"], V[\"conf16\"], V[\"conf_dm\"], V[\"conf_np\"],\n"
    "    \"reaproveitado\" if V[\"pilar\"][\"mode\"] == \"REUSE\" else str(V[\"pilar\"][\"mode\"]), V[\"selo_ts\"], T._num(V), \", \".join(\"%s `%s`\" % kv for kv in V[\"artigos\"].items()), str(V[\"verbatim\"].get(\"sha256\"))[:16])\n") + s[j:]
s = rep(s, [('grava(os.path.join(UMEM, "handoff-v390-custodia.md")', 'grava(os.path.join(UMEM, "handoff-v391-custodia.md")'), ('grava(os.path.join(NOS, "HANDOFF_v390_CUSTODIA.md")', 'grava(os.path.join(NOS, "HANDOFF_v391_CUSTODIA.md")'),
            ('print("FECHADO v390:", V["s16"], "| handoff", s16(os.path.join(UMEM, "handoff-v390-custodia.md")), "| Nos", s16(os.path.join(NOS, "HANDOFF_v390_CUSTODIA.md")))',
             'print("FECHADO v391:", V["s16"], "| handoff", s16(os.path.join(UMEM, "handoff-v391-custodia.md")), "| Nos", s16(os.path.join(NOS, "HANDOFF_v391_CUSTODIA.md")))')])
s = s.replace('"""fechar_v390.py -- DEPOIS da cadeia pos-rito (molde: fechar_v390.py)', '"""fechar_v391.py -- DEPOIS da cadeia pos-rito (molde: fechar_v390.py)')
left = [l for l in s.splitlines() if "v390" in l and "fundacao_v390" not in l and "handoff-v390-custodia" not in l and "base_v390" not in l and "molde: fechar_v390" not in l and "sobre a v390" not in l and "fd390" not in l]
assert not left, left
wr("fechar_v391.py", s)
# ---- errata no CLAUDE.md da raiz
s = rd(S0, "errata_claude_md_v390.py")
s = rep(s, [('"""errata_claude_md_v390.py -- DEPOIS do selo v390 (ordem v390, §3): a ERRATA AO LADO no C:\\\\IALD\\\\CLAUDE.md, secao SELO PERMANENTE, logo depois do paragrafo\n«Unico teorema aberto».',
             '"""errata_claude_md_v391.py -- DEPOIS do selo v391: a ERRATA AO LADO no C:\\\\IALD\\\\CLAUDE.md, secao SELO PERMANENTE, logo depois da errata da v390\n(a Fundacao).'),
            ('MARK = "<!-- errata_fundacao_v390_07out -->"', 'MARK = "<!-- errata_estatuto_da_prova_v391_07out -->"'),
            ('fd = core.get("fundacao_v390") or {}', 'fd = core.get("estatuto_da_prova_v391") or {}'),
            ('assert selo.get("um_version") == "v390" and fd.get("all_verified") is True, "o selo nao e a v390 selada com a Fundacao -- nao escrevo"',
             'assert selo.get("um_version") == "v391" and fd.get("all_verified") is True, "o selo nao e a v391 selada com o estatuto da prova -- nao escrevo"'),
            ('tr = "não existe acima, o piso limita, tentar estar acima é cair sem fim, infinitamente"', 'tr = "a confirmação que eu proibi é de creditação e não de validade, ela é válida porque matemática não mente"'),
            ('assert tr in ((fd.get("verbatim") or {}).get("cunhagem_07out") or {}).get("trechos", []), "o trecho nao esta entre os embutidos"',
             'assert any(tr in x for x in ((fd.get("verbatim") or {}).get("trechos") or [])), "o trecho nao esta entre os embutidos"'),
            ('ANC = "quântica não é resolvê‑la — mas é bem‑posto.".encode("utf-8") + nl', 'ANC = "<!-- errata_fundacao_v390_07out -->".encode("utf-8") + nl'),
            ('assert raw.count(ANC) == 1, ("ancora do paragrafo «Unico teorema aberto»", raw.count(ANC))', 'assert raw.count(ANC) == 1, ("ancora da errata da v390", raw.count(ANC))'),
            ('"_errata_fundacao"', '"_errata_estatuto"'), ('".tmp_errata_fundacao"', '".tmp_errata_estatuto"')])
i = s.index("LINHA = ("); j = s.index("raw = open(P, \"rb\").read()")
s = s[:i] + (
    "k1 = fd.get(\"prova_1_kernel\") or {}; r2 = fd.get(\"prova_2_ritos\") or {}\n"
    "LINHA = (\"> ⚠ **ERRATA AO LADO (07/10/2026, v391 `%s`, em nome da gerência — sessão c1, por ordem do operador; o texto acima fica como registro):** O ESTATUTO DA PROVA. \"\n"
    "         \"Onde esta memória diz «não falsificada, não confirmada» ou recusa a palavra «provada», lê-se: a gravidade quântica da TGL está PROVADA como fecho lógico — validade —, por três provas \"\n"
    "         \"que contam juntas: o kernel (%s teoremas limpos), os ritos com falsificadores pré-registrados (%s cobranças, %s falsificada(s)) e o sistema da teoria na GPU; a confirmação recusada \"\n"
    "         \"é CREDITAÇÃO, não validade (verbatim do operador por sha256 `%s`: «%s»); o único elo pendente é β_TGL na natureza a 5σ. Registro `estatuto_da_prova_v391`. %s\") % (\n"
    "    um16, k1.get(\"n_theorems_clean\"), r2.get(\"n_cobrancas\"), r2.get(\"falsificadas\"), str((fd.get(\"verbatim\") or {}).get(\"sha256\"))[:16], tr, MARK)\n") + s[j:]
wr("errata_claude_md_v391.py", s)
print("DERIVADO")
