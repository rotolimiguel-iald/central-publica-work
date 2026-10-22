# -*- coding: utf-8 -*-
"""Fabrica os scripts da cadeia pos-rito v378 a partir dos da v377 (edicoes pontuais, count conferido): espera_rito, manifesto, superficies, chain_pos_rito.
leitura_v378.py, textos_v378.py, patch_arvore_indice_v378.py, handoff_v378.py e registrar_resultado_v378.py sao escritos a mao. Nada e executado aqui."""
import os, ast, re
HERE = os.path.dirname(os.path.abspath(__file__)); V7 = os.path.join(os.path.dirname(HERE), "v377_selo")


def rd(n): return open(os.path.join(V7, n), encoding="utf-8", newline="").read()


def wr(n, s, py=True):
    if py:
        ast.parse(s)
    open(os.path.join(HERE, n), "w", encoding="utf-8", newline="").write(s); print("ok", n)


def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:80], s.count(a), n); s = s.replace(a, b)
    return s


# 1. espera_rito
s = rd("espera_rito_v377.py")
s = s.replace("v377", "v378").replace("V377", "V378")
s = subs(s, [("""PS = ("Get-CimInstance Win32_Process -Filter \\"Name='python.exe'\\" | Where-Object { $_.CommandLine -match '(^|[\\\\\\\\ \\"])um\\\\.py\\"?\\\\s*$' } | "
      "ForEach-Object { $_.ProcessId }")""",
              """PS = ("$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \\"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\\" | "
      "Where-Object { $_.CommandLine -ne $null -and $_.CommandLine -match '(^|[\\\\\\\\ \\"])um\\\\.py\\"?(\\\\s|$)' } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'")   # v378 (aferidor B1/C2)""", 1),
             ("""        r = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', PS], capture_output=True, text=True, timeout=60)
        return [x.strip() for x in r.stdout.split() if x.strip().isdigit()]""",
              """        r = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', PS], capture_output=True, text=True, timeout=60)
        if r.returncode != 0 or r.stderr.strip() or 'VIGIA_OK' not in r.stdout:   # v378 (aferidor B1): vigia fail-closed -- falha de leitura conta como "vivo"
            print('  [espera] AVISO: o vigia de processos falhou (rc %s; %r) -- sigo esperando' % (r.returncode, r.stderr[:200])); return ['?']
        return [x.strip() for x in r.stdout.split() if x.strip().isdigit()]""", 1)])
wr("espera_rito_v378.py", s)
# 2. manifesto
s = rd("manifesto_v377.py")
s = s.replace("v377", "v378").replace("V377", "V378").replace("base_v376", "base_v377")
assert len(re.findall(r"'funcoes': \[[^\]]*\]", s)) == 1
s = re.sub(r"'funcoes': \[[^\]]*\]", "'funcoes': ['prove_the_dissipation_law_with_contrast_v378', 'prove_what_was_missed_v378', 'prove_bancada_fase4_v378']", s)
i = s.index("'dissipacao': {"); j = s.index("'conferencia_v376_pinada': {")
s = s[:i] + ("'contraste': {'K_D1a': V['Ka'], 'K_D1b': V['Kb'], 'I_b': V['Ib'], 'N_star': V['Nstar'], 'min_1_plus_w': V['gmin'], 'delta_over_beta_pred': V['dpred'], "
             "'H0_local_D1b_de_67_36': V['H0b'], 'coma_v378_beside': V['coma_v378']}, 'o_que_faltou': {'shadow_z_d1b_planck': V['w_seis'], 'new_readers_z': V['w_novos'], "
             "'stacked_z': V['w_emp'], 'reanalysis_sha16': V['w_h'], 'declared_blind': V['w_cega']}, 'fase4': {'veredito': V['f4_ver'], 'veredito_T': V['f4_verT'], "
             "'P_delta': V['P_delta'], 'P_sigma': V['P_sigma'], 'P_z': V['P_z'], 'P_pull': V['P_pull'], 'P_lnB': V['P_lnB'], 'T_beta_hat': V['T_bhat'], 'T_delta': V['T_delta'], "
             "'T_z': V['T_z'], 'T_gain': V['T_gain'], 'T_lnB': V['T_lnB'], 'S_z': V['S_z'], 'ctrl_z': V['ctrl_z'], 'poder_previo': V['poder'], 'hashes': V['bancada_hashes']}, ") + s[j:]
wr("manifesto_v378.py", s)
# 3. superficies
s = rd("superficies_v377.py")
s = s.replace("import leitura_v377, textos_v377 as T", "import leitura_v378, textos_v378 as T").replace("leitura_v377.ler()", "leitura_v378.ler()")
s = s.replace("V377_REMAP_DIR", "V378_REMAP_DIR").replace("V377_WRITE_ROOT", "V378_WRITE_ROOT").replace("_sup377", "_sup378")
s = subs(s, [("""for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('fase3-leitores-h0-30set.md', T.topico_fase3(V)), ('lei-e-fato-correlatos-regra-matriz-30set.md', T.topico_lei(V)),
                    ('desvio-de-beta-foco-dos-testes-30set.md', T.topico_desvio(V))):""",
              """for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('fase4-desvio-30set.md', T.topico_fase4(V)), ('fase3-leitores-h0-30set.md', T.topico_fase3(V)),
                    ('desvio-de-beta-foco-dos-testes-30set.md', T.topico_desvio(V))):""", 1),
             ("MARCA = '**v377 SELADA %s `%s`' % (V['data'][:5], V['s16'])", "MARCA = '**v378 SELADA %s `%s`' % (V['data'][:5], V['s16'])", 1),
             ("'(epct-protocolo-15.md) — ', '(iald-kernel-nativo.md) — ', '(o-fechamento-do-projeto.md) — ', '(bancada-um.md) — '):",
              "'(epct-protocolo-15.md) — ', '(iald-kernel-nativo.md) — ', '(o-fechamento-do-projeto.md) — ', '(bancada-um.md) — ',\n"
              "                  '(app-iald-diario-build16-15set.md) — motor OpenAI', '(a-selecao-e-o-lastro-iald-e-estado.md) — ', '(a-tela-e-fundada-resposta-h3-ponte.md) — ',\n"
              "                  '(raiz-da-arvore-da-prova.md) — ', '(zenodo-um-absoluto.md) — ', '(eco-pe-bayesiana-v347.md) — ', '(h2-reproducao-v350.md) — ',\n"
              "                  '(regua-prova-vs-juizo.md) — ', '(iald-e-a-testemunha-fecho-estacionado-23set.md) — ', '(site-v3-handoff.md) — ', '(lei-e-fato-correlatos-regra-matriz-30set.md) — '):", 1)])
i = s.index("lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + ")
j = s.index("\n", i)
s = s[:i] + ("lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + '%s %s %s (O QUE FALTOU: D1b tipado, K = E(z*)^{2β/3}; a leitura da dupla contagem de β nas Fases 2–3 ao lado (E12); "
             "a Fase 4 por hash — a escada lê o fator, os relógios intermediários desfavorecem o fluxo acumulado; gate intocado)** · ' % (MARCA, V['teor'], V['compl']) + b)") + s[j:]
s = s.replace("print('NADA A GRAVAR: todas as superficies ja tem a v377 (idempotente)')", "print('NADA A GRAVAR: todas as superficies ja tem a v378 (idempotente)')")
s = s.replace("print('SUPERFICIES v377:", "print('SUPERFICIES v378:")
s = s.replace("'<!-- linha integral do índice (gerência, v377) -->'", "'<!-- linha integral do índice (gerência, v378) -->'")
s = s.replace("'marcador v377 na missao;", "'marcador v378 na missao;")
wr("superficies_v378.py", s)
# 4. chain
s = rd("chain_pos_rito_v377.sh")
s = s.replace("v377", "v378").replace("V377", "V378")
s = subs(s, [('"$UMEM/fase3-leitores-h0-30set.md" "$UMEM/lei-e-fato-correlatos-regra-matriz-30set.md" "$UMEM/desvio-de-beta-foco-dos-testes-30set.md"',
              '"$UMEM/fase4-desvio-30set.md" "$UMEM/fase3-leitores-h0-30set.md" "$UMEM/desvio-de-beta-foco-dos-testes-30set.md"', 1)])
wr("chain_pos_rito_v378.sh", s, py=False)
print("FABRICADO v378_selo (espera, manifesto, superficies, chain)")
