# -*- coding: utf-8 -*-
"""As correcoes da 2a passada do aferidor na cadeia do selo v383 (trocas exatas, count conferido; backup de bytes de cada script antes):
B-M1 o DECIDIDO que nao couber no indice falha A VISTA (a folga do indice e feita a parte, compactar_memory_para_v383.py);
B-M2 o arquivamento inclui os pacotes v382 e v382_selo (o AFERIDOR e o APLICADO da v382 deixam de depender do scratchpad) e o handoff aponta para o ARQUIVO da Central;
b1 as marcas de backup passam a 383; b2 _i383p/_i383; b3 o comentario historico da espera volta a v382; b4 «nucleo da rodada v383»; b5 as contagens LIDAS de V;
b6 «os V1 a V1.3 ficam locais» marcado [DERIVED de leitura, gerencia; a confirmar pelo operador]; b7 comentarios e o diff do candidato no arquivo."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); ST = time.strftime("%Y%m%d_%H%M%S")
ARQ = "C:\\\\IALD\\\\Central de Patentes\\\\work\\\\cadeia_de_selo"


def edit(n, reps, py=True):
    p = os.path.join(HERE, n); raw = open(p, "rb").read()
    bak = p + ".bak_" + ST + "_afer2"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    s = raw.decode("utf-8")
    for a, b, k in reps:
        c = s.count(a); assert c == k, (n, c, k, a[:110]); s = s.replace(a, b)
    if py:
        ast.parse(s)
    open(p + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(p + ".tmp", p); print("ok", n)


DER = " [DERIVED de leitura, gerência; a confirmar pelo operador]"
edit("textos_v383.py", [
    ("sobre a opção da gerência de tirar do livro os nove pares do eco, que não são cobranças da teoria: ", "sobre a opção da gerência de tirar do livro os {rot_n} pares do eco, que não são cobranças da teoria: ", 1),
    ("O LIVRO DE COBRANÇAS (onze cobranças; a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra; os nove pares do eco FORA do livro, por decisão do operador)",
     "O LIVRO DE COBRANÇAS ({n_ledger} cobranças; a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra; os {rot_n} pares do eco FORA do livro, por decisão do operador)", 1),
    ("NÃO foi custodiada: levava os nove pares do eco no livro, ao lado;", "NÃO foi custodiada: levava os {rot_n} pares do eco no livro, ao lado;", 1),
    ("Os nove pares do eco como cópia atrasada saíram do livro, por decisão do operador:", "Os {rot_n} pares do eco como cópia atrasada saíram do livro, por decisão do operador:", 1),
    ("O LIVRO DE COBRANÇAS (ONZE; A TGL É ÓTICA:", "O LIVRO DE COBRANÇAS ({n_ledger} COBRANÇAS; A TGL É ÓTICA:", 1),
    ("OS NOVE PARES DO ECO FORA DO LIVRO (DECISÃO DO OPERADOR)", "OS {rot_n} PARES DO ECO FORA DO LIVRO (DECISÃO DO OPERADOR)", 1),
    ("o livro de cobranças (onze; os nove pares do eco fora do livro, por decisão do operador) e a viscosidade tipados", "o livro de cobranças ({n_ledger} cobranças; os {rot_n} pares do eco fora do livro, por decisão do operador) e a viscosidade tipados", 1),
    ("O livro de cobranças (onze; o eco fora do livro), ψ e a viscosidade", "O livro de cobranças ({n_ledger} cobranças; o eco fora do livro), ψ e a viscosidade", 1),
    ("o livro concreto: {n_ledger} cobranças ({counts}); os nove pares do eco fora do livro, como rotas examinadas, por decisão do operador.**",
     "o livro concreto: {n_ledger} cobranças ({counts}); os {rot_n} pares do eco fora do livro, como rotas examinadas, por decisão do operador.**", 1),
    ('+ _DECISAO + " (os nove pares do eco fora do livro, como rotas examinadas) [INPUT]. " + core_txt(V))',
     '+ _DECISAO + " (os " + str(V["rot_n"]) + " pares do eco fora do livro, como rotas examinadas) [INPUT]. " + core_txt(V))', 1),
    ("a viscosidade βg; os nove pares do eco fora do livro (decisão do operador); ", "a viscosidade βg; os {rot_n} pares do eco fora do livro (decisão do operador); ", 1),
    ("a decisão cumprida — os nove pares do eco fora do livro, como rotas examinadas", "a decisão cumprida — os {rot_n} pares do eco fora do livro, como rotas examinadas", 1),
    ("e os pré-registros V1 a V1.3 ficam fora do espelho;", "e os pré-registros V1 a V1.3 ficam fora do espelho" + DER + ";", 1),
])
edit("handoff_v383.py", [
    ("O LIVRO DE COBRANÇAS (onze cobranças; a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra; os nove pares do eco FORA do livro, como rotas examinadas, por decisão do operador)",
     "O LIVRO DE COBRANÇAS (%(n_ledger)s cobranças; a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra; os %(rot_n)s pares do eco FORA do livro, como rotas examinadas, por decisão do operador)", 1),
    ("`scratchpad\\\\v383\\\\AFERIDOR_v383.txt`", "`" + ARQ + "\\\\v383\\\\AFERIDOR_v383.txt`", 1),
    ("`scratchpad\\\\v382\\\\AFERIDOR_v382.txt`", "`" + ARQ + "\\\\v382\\\\AFERIDOR_v382.txt`", 1),
    ("«prefiro a primeira opção»: os nove pares do eco não são cobranças da teoria)", "«prefiro a primeira opção»: os %(rot_n)s pares do eco não são cobranças da teoria)", 1),
    ("os nove pares do eco como cópia atrasada não são cobranças da teoria: são rotas examinadas fora do livro", "os %(rot_n)s pares do eco como cópia atrasada não são cobranças da teoria: são rotas examinadas fora do livro", 1),
    ("os V1 a V1.3 ficam locais (traziam os pares do eco no livro).", "os V1 a V1.3 ficam locais (traziam os pares do eco no livro)" + DER + ".", 1),
    ('— **%s, para a sessão do site**: onze cobranças; os nove pares do eco fora do livro (decisão do operador); a v382 só no Nós, NÃO custodiar; ψ com norma 1 e a viscosidade; o pré-registro V1.4 por hash; `%s`" % (V["data"][:5], V["s16"]))',
     '— **%s, para a sessão do site**: %s cobranças; os %s pares do eco fora do livro (decisão do operador); a v382 só no Nós, NÃO custodiar; ψ com norma 1 e a viscosidade; o pré-registro %s por hash; `%s`" % (V["data"][:5], V["n_ledger"], V["rot_n"], V["pr_label"], V["s16"]))', 1),
    ('"_handoff382"', '"_handoff383"', 2),
    ('''        print("MEMORY.md: a marca DECIDIDO ficaria acima de 24 000 B (%d) -- nao gravo; a memoria-topico da suspensao ja diz a decisao" % len(novo2))''',
     '''        print("FALHA A VISTA: a marca DECIDIDO ficaria acima de 24 000 B (%d) -- nao gravo; liberar folga no indice (regra dos dois arquivos) e marcar a linha da suspensao a mao" % len(novo2)); sys.exit(3)''', 1),
])
edit("superficies_v383.py", [
    ("MARCA_BAK = '_sup382'", "MARCA_BAK = '_sup383'", 1),
    ("    # (2) a linha da missao ganha o marcador v376 (na frente; o texto antigo fica)", "    # (2) a linha da missao ganha o marcador v383 (na frente; o texto antigo fica)", 1),
    ("'%s %s %s (O LIVRO DE COBRANÇAS tipado, onze cobranças; os nove pares do eco fora do livro, por decisão do operador; ψ com norma 1 e a viscosidade; o pré-registro V1.4 por hash; a v382 só no Nós; gate intocado)** · ' % (MARCA, V['teor'], V['compl'])",
     "'%s %s %s (O LIVRO DE COBRANÇAS tipado, %s cobranças; os %s pares do eco fora do livro, por decisão do operador; ψ com norma 1 e a viscosidade; o pré-registro %s por hash; a v382 só no Nós; gate intocado)** · ' % (MARCA, V['teor'], V['compl'], V['n_ledger'], V['rot_n'], V['pr_label'])", 1),
])
edit("registrar_resultado_v383.py", [
    ("sem sorry; onze cobrancas; os nove pares do eco FORA do livro", "sem sorry; %s cobrancas; os %s pares do eco FORA do livro", 1),
    ('gate intocado" % (V["n_loc"], V["n_psv"], V["kf_on"], V["kf_n"]),', 'gate intocado" % (V["n_loc"], V["n_psv"], V["kf_on"], V["kf_n"], V["n_ledger"], V["rot_n"]),', 1),
    ('dados=["core v381 (', 'dados=["nucleo da rodada v383, base v381 (', 1),
    ('os nove pares do eco como copia atrasada NAO sao cobrancas da teoria (decisao do operador): rotas examinadas fora do livro, %s excluidas pelos dados e %s inconclusivas;',
     'os %s pares do eco como copia atrasada NAO sao cobrancas da teoria (decisao do operador): rotas examinadas fora do livro, %s excluidas pelos dados e %s inconclusivas;', 1),
    ('% (V["rot_exc"], V["rot_inc"])', '% (V["rot_n"], V["rot_exc"], V["rot_inc"])', 1),
    ("o stdout da v382 e os pre-registros V1-V1.3 ficam locais", "o stdout da v382 e os pre-registros V1-V1.3 ficam locais [DERIVED de leitura, gerencia; a confirmar pelo operador]", 1),
])
edit("patch_arvore_indice_v383.py", [
    ("(_p382)", "(_p383)", 1), ("'.tmp_p382_'", "'.tmp_p383_'", 1), ("'_p382'", "'_p383'", 1), ("'%s.bak_%s_p382_%d'", "'%s.bak_%s_p383_%d'", 1),
    ("_i382p", "_i383p", 3), ("_i382 = ", "_i383 = ", 1),
    ("; os nove pares do eco fora do livro, como rotas examinadas (decisão do operador); o nome", "; os \" + str(V['rot_n']) + \" pares do eco fora do livro, como rotas examinadas (decisão do operador); o nome", 1),
])
edit("chain_pos_rito_v383.sh", [("(backups _p382 ao lado)", "(backups _p383 ao lado)", 1), ("(backups .bak_<STAMP>_sup382 ao lado;", "(backups .bak_<STAMP>_sup383 ao lado;", 1)], py=False)
edit("espera_rito_v383.py", [("# v383 (aferidor B1/C2)", "# v382 (aferidor B1/C2)", 2)])
edit("arquivar_v383.py", [
    ('for sub in ("v383", "v383_selo"):', 'for sub in ("v382", "v382_selo", "v383", "v383_selo"):   # v383 (aferidor, B-M2): a v382 selada so no Nos tambem se arquiva -- o AFERIDOR e o APLICADO dela nao dependem do scratchpad', 1),
    ('txt_ok = ext == ".txt" and ("stdout" in fn or "_out" in fn or fn in ("AFERIDOR_v383.txt", "rito_horarios_v383.txt"))',
     'txt_ok = ext == ".txt" and ("stdout" in fn or "_out" in fn or fn.startswith(("AFERIDOR_", "rito_horarios_", "diff_candidato_")))', 1),
])
print("cadeia v383: correcoes da 2a passada aplicadas")
