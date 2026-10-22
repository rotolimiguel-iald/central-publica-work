# -*- coding: utf-8 -*-
"""Fabrica os scripts GENERICOS da cadeia pos-rito v383 a partir dos ATUAIS da v382 (que levam as correcoes das afericoes): leitura, espera, manifesto,
superficies, chain_pos_rito, arquivar. Primeiro v382 -> v383 nos nomes; depois as trocas de CONTEUDO (count conferido): o livro de ONZE; as NOVE rotas do
eco FORA do livro; a BASE v381 e a v382 selada so no Nos (a origem substituida); a memoria da suspensao. Nada e executado aqui.
textos_v383.py, handoff_v383.py, registrar_resultado_v383.py e patch_arvore_indice_v383.py sao feitos a parte."""
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__)); V2 = os.path.join(os.path.dirname(HERE), "v382_selo")


def rd(n):
    return open(os.path.join(V2, n), encoding="utf-8", newline="").read().replace("v382", "v383").replace("V382", "V383")


def wr(n, s, py=True):
    if py:
        ast.parse(s)
    p = os.path.join(HERE, n); assert not os.path.exists(p), p
    open(p, "w", encoding="utf-8", newline="").write(s); print("ok", n)


def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:110], s.count(a), n); s = s.replace(a, b)
    return s


# 0. leitura
s = rd("leitura_v382.py")
s = subs(s, [
    ("        P.append('base lida (%s) != origem v381 de ESPERADOS (%s)' % (V['base16'], ESP['origem_sha16']))\n",
     "        P.append('base lida (%s) != origem de ESPERADOS -- a v382 selada so no Nos (%s)' % (V['base16'], ESP['origem_sha16']))\n"
     "    V['base_build16'] = ESP['base_build_sha16']; V['v382_16'] = ESP['v382_so_local_sha16']   # v383: a BASE do candidato (v381) e a v382 so local (a origem substituida no Nos)\n"
     "    if V['base16'] != V['v382_16']:\n"
     "        P.append('a origem substituida (%s) nao e a v382 so local de ESPERADOS (%s)' % (V['base16'], V['v382_16']))\n"
     "    V['v382_stdout_no_nos'] = os.path.exists(os.path.join(nos, 'rodada_v382_stdout.txt'))\n", 1),
    ("    _eco = lc.get('delayed_echo_pairs') or {}; V['eco_n'] = _eco.get('n'); V['eco_ext'] = _eco.get('extinguished'); V['eco_inc'] = _eco.get('inconclusive')\n"
     "    if V['eco_n'] != 9 or (V['eco_ext'] or 0) + (V['eco_inc'] or 0) != 9:\n"
     "        P.append('a contagem do eco como copia atrasada nao fecha (%s)' % _eco)\n",
     "    _er = lc.get('echo_routes_outside_the_ledger') or {}; V['rot_n'] = _er.get('n'); V['rot_exc'] = _er.get('excluded_by_data'); V['rot_inc'] = _er.get('inconclusive')\n"
     "    V['rot_ids'] = ', '.join('%s %s' % (r.get('id'), r.get('state')) for r in (_er.get('routes') or []))\n"
     "    if V['rot_n'] != 9 or (V['rot_exc'] or 0) + (V['rot_inc'] or 0) != 9 or _er.get('not_charges_of_the_theory') is not True or _er.get('sources_in_core_ok') is not True:\n"
     "        P.append('as rotas do eco fora do livro nao fecham (%s)' % {k: _er.get(k) for k in ('n', 'excluded_by_data', 'inconclusive', 'not_charges_of_the_theory', 'sources_in_core_ok')})\n"
     "    _bl = lc.get('base_and_local_seal') or {}\n"
     "    if _bl.get('base') != 'v381' or _bl.get('v382_local_only_sha16') != V['v382_16']:\n"
     "        P.append('a base declarada (%s) ou a v382 so local (%s) nao batem' % (_bl.get('base'), _bl.get('v382_local_only_sha16')))\n"
     "    V['decisao'] = str((lc.get('operator_decision_20261002') or {}).get('verbatim') or 'AUSENTE')\n"
     "    if V['decisao'] != 'prefiro a primeira opção':\n"
     "        P.append('a decisao do operador nao esta no modulo, verbatim (%s)' % V['decisao'])\n", 1),
    ("    if 'THE_TGL_IS_OPTICS_NOT_SEMI_BOTH_SIDES_READ' not in V['the_ledger_of_charges_v383'] or 'KERNEL_32_OF_32' not in V['the_ledger_of_charges_v383'] or 'NOT_A_CONFIRMATION' not in V['the_ledger_of_charges_v383']:\n",
     "    if ('THE_TGL_IS_OPTICS_NOT_SEMI_BOTH_SIDES_READ' not in V['the_ledger_of_charges_v383'] or 'KERNEL_32_OF_32' not in V['the_ledger_of_charges_v383'] or 'NOT_A_CONFIRMATION' not in V['the_ledger_of_charges_v383']\n"
     "            or 'THE_9_ECHO_ROUTES_ARE_NOT_CHARGES_OF_THE_THEORY' not in V['the_ledger_of_charges_v383'] or 'BASE_V381' not in V['the_ledger_of_charges_v383']):\n", 1),
    ("    if V['n_ledger'] != 20 or V['kf_on'] != 32", "    if V['n_ledger'] != 11 or V['kf_on'] != 32", 1),
    ("o livro lido nao tem vinte cobrancas / 32 bandeiras", "o livro lido nao tem onze cobrancas / 32 bandeiras", 1),
])
assert "delayed_echo" not in s and "eco_n" not in s
wr("leitura_v383.py", s)
# 1. espera (generica)
wr("espera_rito_v383.py", rd("espera_rito_v382.py"))
# 2. manifesto
s = rd("manifesto_v382.py")
s = subs(s, [
    ("'base_v381': V['base16'], ", "'base_build_v381': V['base_build16'], 'substituida_no_nos_v382_so_local': V['base16'], ", 1),
    ("'n_print': {'TheLedgerOfCharges': V['n_loc'], 'ThePsionAndTheViscosity': V['n_psv']}}, ",
     "'n_print': {'TheLedgerOfCharges': V['n_loc'], 'ThePsionAndTheViscosity': V['n_psv']}, "
     "'rotas_fora_do_livro': {'n': V['rot_n'], 'excluidas_pelos_dados': V['rot_exc'], 'inconclusivas': V['rot_inc'], 'ids': V['rot_ids'], 'nao_sao_cobrancas_da_teoria': True}, "
     "'decisao_do_operador': V['decisao']}, ", 1),
])
wr("manifesto_v383.py", s)
# 3. superficies: + a memoria da suspensao (resolvida); o texto da linha da missao
s = rd("superficies_v382.py")
s = subs(s, [
    ("('beta-e-a-regra-matriz-02out.md', T.topico_regra(V)), ('regra-dos-dois-regimes.md', T.topico_regimes(V))",
     "('beta-e-a-regra-matriz-02out.md', T.topico_regra(V)), ('regra-dos-dois-regimes.md', T.topico_regimes(V)), ('v382-custodia-suspensa.md', T.topico_suspensao(V))", 1),
    ("(O LIVRO DE COBRANÇAS tipado: a TGL é ótica, lê a face e o custo; nenhum desfecho move a regra; ψ com norma 1 e a viscosidade; o pré-registro dos dois lados por hash; gate intocado)",
     "(O LIVRO DE COBRANÇAS tipado, onze cobranças; os nove pares do eco fora do livro, por decisão do operador; ψ com norma 1 e a viscosidade; o pré-registro V1.4 por hash; a v382 só no Nós; gate intocado)", 1),
])
wr("superficies_v383.py", s)
# 4. chain: a copia da memoria da suspensao no ensaio; a linhagem diz o que foi a v382
s = rd("chain_pos_rito_v382.sh")
s = subs(s, [
    ('"$UMEM/beta-e-a-regra-matriz-02out.md" "$UMEM/regra-dos-dois-regimes.md" "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md"; do cp -p "$f" "$ENS/"; done',
     '"$UMEM/beta-e-a-regra-matriz-02out.md" "$UMEM/regra-dos-dois-regimes.md" "$UMEM/v382-custodia-suspensa.md" "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md"; do cp -p "$f" "$ENS/"; done', 1),
    ('echo "== FIM $(date +%T)"',
     'n=$(grep -c "v382" "$NOS/MEMORIA_DA_LINHAGEM.md" || true); echo "  $n  MEMORIA_DA_LINHAGEM.md (v382, selada so no Nos)"; [ "$n" -gt 0 ] || parar "a linhagem nao diz o que foi a v382"\n'
     'echo "== FIM $(date +%T)"', 1),
])
wr("chain_pos_rito_v383.sh", s, py=False)
# 5. arquivar
wr("arquivar_v383.py", rd("arquivar_v382.py"))
print("FABRICADO v383_selo (leitura, espera, manifesto, superficies, chain, arquivar)")
