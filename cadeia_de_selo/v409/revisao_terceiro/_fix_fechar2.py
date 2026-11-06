p = "fechar_revisao.py"
L = open(p, encoding="utf-8").read().split("\n")
def idx(prefix):
    return [i for i, l in enumerate(L) if l.strip().startswith(prefix)][0]
iA = idx('"R1-A (intocados/mudados)'); iC = idx('"R1-C (fail-closed)'); iE = idx('"R1-E (hashes/orquestrador)')
L[iA] = '        "R1-A (intocados/mudados): a_intocados*.py e a2_mudados.py sobre base_v408 x candidato: %d nomes iguais por AST e fonte (gate, neutrino, ramo B, ledger, GA, registros v408/v407/v406 e seus textos); mudados 27 == declarados; novos 14 == declarados; 0 removidos; contratos antigos mudam SO\' expected_ladder 12029 -> 12187 (28 ocorrencias); _V408_SPECS +E26 e pisos h2/h3/h6/h8 (declarados); _V407_FONTES muda SO\' a chave psion_no_acervo_do_imac_03nov (copia PURGADA, sha256 f0b1c79a5caa75df…, a mesma da v408, D57d); _LEAN_THEOREM_FLAGS +158 (ext_tu409_*), sub-dict da base igual." % N_IGUAIS,'
L[iC] = '        "R1-C (fail-closed): c_fail_closed.py (%d casos), c2_mecanica_direta.py (18), k_funcoes_vivas.py (34): ancoras, bandeiras, fontes, raiz, escada, gate, beta, contrato, falas, texto proibido, instancias recusam; a ordem errada dos specs recusa." % N_CASOS,'
L[iE] = '        "R1-E (hashes/orquestrador): f_hashes.py (%d checagens ok), n_hashes_digitados.py, n2_hashes_docs.py, l_orquestrador.py, m_flags_audit.py + m4.py." % N_HASH,'
t = "\n".join(L)
t = t.replace("res = {\n    \"aprovada\": False,", "N_IGUAIS = sum(1 for v in a1['nomes'].values() if v.get('ast_igual') and v.get('fonte_igual')); N_CASOS = n_cfc_ok + len(n_cfc_f); N_HASH = sum(1 for v in fh['ok'].values() if v)\nres = {\n    \"aprovada\": False,")
open(p, "w", encoding="utf-8", newline="\n").write(t)
