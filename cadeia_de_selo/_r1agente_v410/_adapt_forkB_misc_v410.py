# -*- coding: utf-8 -*-
"""_adapt_forkB_misc_v410.py -- (claude-construtor-v410, fork B, 06/11/2026) adapta a v410 os scripts de infraestrutura do fork B que a subida mecanica deixou certos no CORPO (conferido no diff do bump) e com texto
da v409 nos comentarios/docstrings, e os que tem conteudo da v409: simular_arvore_do_nos (a chamada iald2_v410 + _v410_rodar_specs depois dos da v409, na ordem do main; as chaves da v410 no relatorio),
varredura_fock_omega (a secao do artigo da v410 vai de 06/11/2026 a 05/11/2026; «v410» deixa de contar como passagem futura: v411+), regerar/refazer_candidato (o preparo do bundle e' o _06nov; os tempos MEDIDOS lidos dos arquivos),
o deposito do construtor e o fecho da preparacao (a prosa da v410: a moldura da D64, as ressalvas, D63/D65/D69/D70, E29; numeros e hashes LIDOS dos arquivos), a inscricao ACOM da gerencia (so' adaptada) e o teste do caminho positivo.
Em cada arquivo a marca [A ADAPTAR v410] sai e a marca antiga (a da v409, subida) e' retirada. Trocas de contagem exata; backup de bytes; CRLF respeitado. NADA e' executado (os atos da gerencia seguem dela)."""
import hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_forkB_util_v410 import adaptar, linha, texto, NOTA_FORKB, HERE  # noqa: E402
import delta_v410 as DL  # noqa: E402

mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read(), re.M)}
BUILD_S = mm["epoch_build_fim"] - mm["epoch_inicio"]; AUDIT_S = mm["epoch_audit_fim"] - mm.get("epoch_audit_inicio", mm["epoch_build_fim"])
SHA_CARIMBO_V409 = hashlib.sha256(open(os.path.join(DL.V409, "carimbar_stdout_v409.py"), "rb").read()).hexdigest()[:16]
NOME_IALD2 = "com o NOME do modulo dado pelo operador em 06/11/2026 e os nomes das declaracoes da gerencia, [DECLARADO] ate a ratificacao (D63)"
MOLD = ("A moldura vale em todo texto: a IALD le o codigo (le o par como par, uno, com a Meia-Nat); ao quadrado e' ela mesma (reler nao acrescenta); o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); "
        "a maquina de Turing padrao sem o leitor fica fora; a forma de matriz finita e' o signo; validade no kernel, nao creditacao; o gate nao se move. ")
RESS = ("As ressalvas vao ditas: com o leitor que so' conta vale NP contido em P com o leitor (Cook-Levin [KNOWN]) e a igualdade relativizada nao esta' provada para o contador (E28); que a IALD, a Torre ou o operador SEJAM o funtor, e que o codigo SEJA um vetor de H1, "
        "sao leituras do operador, nao termos; o funtor nao e' idempotente (a leitura e'); o par finito (Bell 4x4) e o par de Fock sao espacos distintos, com a mesma Meia-Nat; a instancia do seletor e' de forma (D70); de uma fala de 06/11 so' o trecho entra (D65); "
        "nenhum teste com a natureza entra; a regra do 4,44 vale em qualquer texto que o cite. Os nomes: o NOME do modulo, IALD2, e' do operador (06/11/2026); os nomes das declaracoes sao da gerencia c1 e ficam [DECLARADO] ate a ratificacao (D63).")


def sem_marca_velha(rel):
    t = texto(rel)
    if "[ADAPTADO v410, 05/11/2026, claude-construtor-v410]" not in t:
        return []
    return [(linha(rel, "# [ADAPTADO v410, 05/11/2026, claude-construtor-v410]") + "\n", "", 1)]


def so_notas(rel, nota, extra=()):
    adaptar(rel, sem_marca_velha(rel) + list(extra), nota + "; " + NOTA_FORKB)


# ---------------- os que so' mudam nas notas (o corpo da subida esta' certo: conferido no diff do bump)
so_notas("acom_conferencias_v410.py", "reexporta as conferencias da v409 por caminho (a v410 NAO muda a secao do selo pela propria tecnologia; o corpo da subida de rotulo esta certo; conferido no diff do bump)",
         [("# adaptado a v410 (04/11/2026, claude-construtor-v410): a v410 NAO muda a secao do selo pela propria tecnologia;", "# adaptado a v410 (06/11/2026, claude-construtor-v410, fork B): a v410 NAO muda a secao do selo pela propria tecnologia;", 1)])
so_notas("regras_v410.py", "regras de permissao da cadeia v410 (RECUSA sem V410_REGRAS_AUTORIZADAS=sim; ato da gerencia; nao executado)",
         [("# regras_v410.py -- ESCRITO em 05/11/2026 pela preparacao da cadeia v410 (claude-construtor-v410) e NAO EXECUTADO", "# regras_v410.py -- ESCRITO em 06/11/2026 pela preparacao da cadeia v410 (claude-construtor-v410, fork B) e NAO EXECUTADO", 1)])
so_notas("kernel/refazer_audit_v410.sh", "refaz SO' o Audit do sandbox k410c (para uma queda de energia que corte o Audit; na v410 o build e o Audit de 06/11 terminaram com rc 0: NAO executado)",
         [("# refaz SO' o Audit do sandbox da v410 (o build terminou com rc 0 as 17:05:33; a queda de energia de ~17:10 cortou o Audit). claude-construtor-v410, 05/11/2026.",
           "# refaz SO' o Audit do sandbox da v410, se uma queda cortar o Audit depois de um build com rc 0 (molde: o da v409, escrito depois da queda de energia de 05/11 ~17:10). claude-construtor-v410, fork B, 06/11/2026.", 1)])
so_notas("refazer_sandbox_v410_pos_selo.sh", "pos-selo: chama refazer_arvore_v410_pos_selo.py (NAO executado na preparacao)")
so_notas("guardas_estaticas_bancada_v410.py", "o corpo da v409 serve sem mudanca de logica (so' as linhas unicas de ALPHA_FINE_CODATA_2018 e UM_VERSION sao lidas); o pino do esboco vem do CANDIDATO_v410.json",
         [("# (nota herdada da v409 [claude-construtor-v409-r2, 04/11/2026], rotulos subidos)", "# (nota herdada da v408 [claude-construtor-v408-r2, 04/11/2026], rotulos subidos, reconferida pelo fork B do claude-construtor-v410 em 06/11/2026)", 1)])
l4 = linha("carimbar_stdout_v410.py", '"""carimbar_stdout_v410.py -- [copia na cadeia v410')
n4 = re.sub(r"\[copia na cadeia v410, 05/11/2026, claude-construtor-v410: o corpo e' o do carimbador da v409 \(sha16 do arquivo da v409, lido pelo adaptador: [0-9a-f]{16}\);",
            "[copia na cadeia v410, 06/11/2026, claude-construtor-v410: o corpo e' o do carimbador da v409 (sha16 do arquivo da v409, lido pelo adaptador: %s);" % SHA_CARIMBO_V409, l4)
assert n4 != l4
so_notas("carimbar_stdout_v410.py", "o carimbador do stdout do rito: corpo da v409, rotulo v410", [(l4, n4, 1)])
l4 = linha("copiar_logs_do_kernel_v410.py", '"""copiar_logs_do_kernel_v410.py -- CONFERIDOR IDEMPOTENTE')
l5 = linha("copiar_logs_do_kernel_v410.py", "A construcao (construir_kernel_v410.sh:")
so_notas("copiar_logs_do_kernel_v410.py", "conferidor idempotente dos logs do kernel da v410 (le KH_N1_v410.json e LOGS_COPIADOS_v410.json); nada de bundle no corpo",
         [(l4, l4.replace("(adaptado em 05/11/2026 a v410;", "(adaptado em 06/11/2026 a v410;"), 1), (l5, l5.replace("do modulo novo do bundle (TraducaoTuring)", "do modulo novo do bundle (IALD2)"), 1)])
l5 = linha("refazer_arvore_v410_pos_selo.py", "POS-SELO: so' roda DEPOIS de a v410 estar no Nos")
l6 = linha("refazer_arvore_v410_pos_selo.py", "Molde escrito em 24/10/2026 (refazer_arvore_v39x_pos_selo.py)")
so_notas("refazer_arvore_v410_pos_selo.py", "pos-selo: refaz C:/t/k410c/arvore a partir do Nos v410 e confere contra KERNEL_RECIBO_v410.json (o corpo le tudo do recibo; NAO executado na preparacao)",
         [(l5, l5.replace("foi feita so' por leitura em 05/11/2026 (pos_build_kernel_v410.py e p00)", "foi feita so' por leitura em 06/11/2026 (pos_build_kernel_v410.py e p00)"), 1), (l6, l6.replace("adaptado a v410 em 05/11/2026 (claude-construtor-v410)", "adaptado a v410 em 06/11/2026 (claude-construtor-v410, fork B)"), 1)])
l6 = linha("purga_v410.py", "sem os padroes). Sai com rc 0 so' se ZERO ocorrencias.")
so_notas("purga_v410.py", "so' leitura; conta os padroes da fala de 25/10 e da fala excluida na pasta v410 e em C:\\t\\k410c (o corpo nao depende de versao); corre por fora (~20 min)",
         [(l6, l6.replace("por isso a validacao de preparacao (05/11/2026) foi so' de sintaxe", "por isso a validacao de preparacao (06/11/2026) foi so' de sintaxe"), 1)])
l4 = linha("pino_memoria_py_v410.py", '"""pino_memoria_py_v410.py (adaptado em 05/11/2026:')
so_notas("pino_memoria_py_v410.py", "pina o memoria.py da fila (ato da gerencia antes do p00; nao executado pelo construtor)", [(l4, l4.replace('"""pino_memoria_py_v410.py (adaptado em 05/11/2026:', '"""pino_memoria_py_v410.py (adaptado em 06/11/2026:'), 1)])
l4 = linha("fim_de_cadeia_v410.sh", "# fim_de_cadeia_v410.sh -- (adaptado em 05/11/2026, claude-construtor-v410;")
so_notas("fim_de_cadeia_v410.sh", "o que vem depois do refazer_candidato: B(n) pre-selo, servico estatico, derivacao do pos-rito, harnesses e previa do X (o corpo nao depende do numero de modulos)",
         [(l4, l4.replace("(adaptado em 05/11/2026, claude-construtor-v410;", "(adaptado em 06/11/2026, claude-construtor-v410, fork B;"), 1)])

# ---------------- regerar e refazer_candidato (o preparo do bundle e' o _06nov; os tempos medidos)
rel = "regerar_v410.sh"
l4 = linha(rel, "# regerar_v410.sh -- refaz, NA ORDEM, tudo o que depende do BUNDLE PEQUENO")
l7 = linha(rel, "# O QUE ESTE SCRIPT NAO FAZ (decisao da gerencia): montar o sandbox.")
l10 = linha(rel, "# O build leva ~5 min e o Audit ~4 min no sandbox")
so_notas(rel, "regera, na ordem, o que depende do bundle de um modulo (guarda do sandbox, build, pos_build, insumos, refazer_candidato); o sandbox nasce de copiar_k410c.sh + preparar_bundle_v410_06nov.py", [
    (l4, "# regerar_v410.sh -- refaz, NA ORDEM, tudo o que depende do BUNDLE PEQUENO de um modulo (adaptado em 06/11/2026 da v409: la' eram os 2 modulos da traducao e do par; aqui o kernel novo e' UM modulo em TGLExt/: IALD2, " + NOME_IALD2 + ", normalizado por preparar_bundle_v410_06nov.py):", 1),
    (l7, l7.replace("`preparar_bundle_v410_05nov.py`", "`preparar_bundle_v410_06nov.py`"), 1),
    (l10, "# O build leva ~%d min e o Audit ~%d min no sandbox (medido em 06/11/2026: kernel/construir_marcas.txt, %d s e %d s: incremental sobre a v409 compilada, so' o modulo novo a frio). Depois: python -I -B -X utf8 purga_v410.py (tem de dar ZERO; leva ~20 min, por fora)." % (round(BUILD_S / 60.0), round(AUDIT_S / 60.0), BUILD_S, AUDIT_S), 1)])
rel = "refazer_candidato_v410.sh"
l5 = linha(rel, "# USAR quando mudar qualquer script/texto que entra no candidato")
l7 = linha(rel, "# [v410, adaptado em 05/11/2026, claude-construtor-v410] o candidato e' o do BUNDLE PEQUENO")
n7 = ("# [v410, adaptado em 06/11/2026, claude-construtor-v410, fork B] o candidato e' o do BUNDLE PEQUENO de um modulo em TGLExt/ (IALD2; registro com funcao iald2_v410 + specs cunhagens_v410/kh_n1_cobertura_v410); os 2 modulos da v409, os 4 do terminal (v408), os 9 do psion (v407) e os 301 do fecho (v406) ficam no kernel como registro; nenhuma chave antiga muda. "
      + l7[l7.index("O passo 9 (p00) imprime PENDENTE"):])
so_notas(rel, "refaz, na ordem, tudo o que depende do texto do candidato v410 (gerador, comparacao, ensaio, ESPERADOS, conferidor, citacoes, pinos, instalar/rito, p00)",
         [(l5, l5.replace("preparar_bundle_v410_05nov.py", "preparar_bundle_v410_06nov.py"), 1), (l7, n7, 1)])

# ---------------- simular_arvore_do_nos (a chamada da v410 na ordem do main; as chaves da v410 no relatorio)
rel = "simular_arvore_do_nos_v410.py"
l4 = linha(rel, "# (v410, 05/11/2026, claude-construtor-v410, fork B) molde v409/simular_arvore_do_nos_v409.py;")
l7 = linha(rel, "v394 a v410 sobre esse kf (mais os quatro registros com funcao da v403")
so_notas(rel, "simula a arvore do Nos depois do rito e roda os registros da v394 a v410 (iald2_v410 e os specs da v410 depois dos da v409, na ordem do main)", [
    (l4 + "\n", "# (v410, 06/11/2026, claude-construtor-v410, fork B) molde v409/simular_arvore_do_nos_v409.py; bundle de 1 modulo em TGLExt/ (IALD2), registro iald2_v410 + specs cunhagens_v410/kh_n1_cobertura_v410 chamados NA ORDEM DO MAIN depois dos da v409 (traducao_turing_v409 e os specs da v409, herdados); a chave do lema (v407) segue conferida como herdada; nenhuma chave antiga muda.\n", 1),
    (l7, l7.replace("e o `tetelestai_terminal_v408` herdados e o `traducao_turing_v409` novo).", "o `tetelestai_terminal_v408` e o `traducao_turing_v409` herdados e o `iald2_v410` novo)."), 1),
    ("um.traducao_turing_v409(core); um._v409_rodar_specs(core)   # (v410: a traducao_turing_v409 vem logo depois dos specs da v409, como no main;",
     "um.traducao_turing_v409(core); um._v409_rodar_specs(core); um.iald2_v410(core); um._v410_rodar_specs(core)   # (v410: o iald2_v410 vem logo depois dos specs da v409, como no main, e os specs da v410 depois dele; a traducao_turing_v409, herdada, logo depois dos specs da v408;", 1),
    ('for k in ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408",', 'for k in ("iald2_v410", "cunhagens_v410", "kh_n1_cobertura_v410", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408",', 1)])

# ---------------- varredura_fock_omega (a D64 segue proibindo o par na face de Fock dito em aberto)
rel = "varredura_fock_omega_v410.py"
l3 = linha(rel, '"""varredura_fock_omega_v410.py -- (claude-construtor-v410, 05/11/2026 ~22h50; pedido da gerencia apos a R2 do Sonnet)')
so_notas(rel, "a varredura da v409 (pedido da gerencia depois da R2 do Sonnet) reaproveitada na v410: a D64 segue proibindo o par na face de Fock dito em aberto; a secao do artigo da v410 vai de 06/11/2026 a 05/11/2026; «v410» deixa de contar como passagem futura (v411 em diante)", [
    (l3, l3.replace("(claude-construtor-v410, 05/11/2026 ~22h50; pedido da gerencia apos a R2 do Sonnet)", "(claude-construtor-v409, 05/11/2026 ~22h50, pedido da gerencia apos a R2 do Sonnet; reaproveitada na v410 pelo claude-construtor-v410, 06/11/2026)"), 1),
    ('ABERTO = re.compile(r"\\bOPEN\\b|\\baberto\\b|\\baberta\\b|\\bem\\s+abert|\\bpendente|ainda\\s+n[ãa]o|por\\s+fazer|\\bv41[0-9]\\b|\\bopen\\b|\\bpending\\b|not\\s+yet", re.I)',
     'ABERTO = re.compile(r"\\bOPEN\\b|\\baberto\\b|\\baberta\\b|\\bem\\s+abert|\\bpendente|ainda\\s+n[ãa]o|por\\s+fazer|\\bv41[1-9]\\b|\\bopen\\b|\\bpending\\b|not\\s+yet", re.I)   # (v410: a versao corrente, v410, nao conta como passagem futura)', 1),
    ('        i0_ = next((i_ for i_ in idx_ if "05/11/2026" in linhas_[i_]), None)\n        i1_ = next((i_ for i_ in idx_ if i0_ is not None and i_ > i0_ and "04/11/2026" in linhas_[i_]), len(linhas_))',
     '        i0_ = next((i_ for i_ in idx_ if "06/11/2026" in linhas_[i_]), None)   # (a secao da v410 comeca na data dela e vai ate a da v409)\n        i1_ = next((i_ for i_ in idx_ if i0_ is not None and i_ > i0_ and "05/11/2026" in linhas_[i_]), len(linhas_))', 1)])

# ---------------- o teste do caminho positivo (so' o docstring)
rel = "teste_conferidor_positivo_v410.py"
l8 = linha(rel, "fechamento do sidecar. Um 'TUDO BATE' aqui diz que as expressoes do conferidor")
l9 = linha(rel, "as 82 ancoras e os dois modulos do bundle; nenhuma chave antiga muda)")
l11 = linha(rel, "Molde: teste_conferidor_positivo_v409.py (cadeia v409), adaptado em 05/11/2026 a v410")
so_notas(rel, "so' o docstring: o registro novo iald2_v410 e os herdados (traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407, fechamento_v406); o corpo da v409 serve", [
    (l8, l8.replace("e, na v410, o registro traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados,", "e, na v410, o registro iald2_v410, o traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados,"), 1),
    (l9, l9.replace("as 82 ancoras e os dois modulos do bundle; nenhuma chave antiga muda)", "as ancoras da pedra IALD2 e o modulo do bundle; nenhuma chave antiga muda)"), 1),
    (l11, l11.replace("adaptado em 05/11/2026 a v410 (claude-construtor-v410)", "adaptado em 06/11/2026 a v410 (claude-construtor-v410, fork B)"), 1)])

# ---------------- o deposito do construtor (o texto MONTADO dos arquivos; a prosa da v410)
rel = "depositar_construtor_v410.py"
t = texto(rel)
l3 = linha(rel, '"""depositar_construtor_v410.py -- (claude-construtor-v410, 05/11/2026)')
lres = linha(rel, 'res = ("candidato %s (%s B, base v409 %s); pronta=%s; portoes que passaram (%d de %d): %s; que nao passaram: %s; kernel recibo %s (bundle de %s modulos novos em TGLExt/: TraducaoTuring e ParNaFaceDeFock);')
lsub = linha(rel, '_PREFIXO_SUBST = ("SUBSTITUI o deposito do PRONTA anterior (%s):')
ltxt = linha(rel, 'txt = (_PREFIXO_SUBST + "v410 (A traducao as classes de Turing e o par na face de Fock) preparada em 05/11/2026')
lmold = linha(rel, '       + "A moldura vale em todo texto: P = nP e\' teorema da TGL no modo selecao')
lress = linha(rel, '       "O par na face de Fock esta\' ligado nesta versao (ParNaFaceDeFock;')
lr2 = linha(rel, 'r2 = subprocess.run([PY, "-X", "utf8", MEM, "depositar", "--quem", "claude-construtor-v410"')
ltit = linha(rel, '         "titulo": "v410 preparada (A traducao as classes de Turing e o par na face de Fock, 05/11/2026)')
lper = linha(rel, '         "pergunta": "as pedras TraducaoTuring e ParNaFaceDeFock (2 modulos, 82 ancoras)')
ldad = linha(rel, '         "dados": ["kernel do Nos v409 selado (copia em C:\\\\t\\\\k410c\\\\final)"')
lmet = linha(rel, '         "metodo": "bundle de 2 modulos em TGLExt/ (molde: a v409)')
lprox = linha(rel, '         "proximo_passo": "atos da gerencia: pino_memoria_py_v410.py')
lref = linha(rel, '         "onde": HERE, "artefatos": [PR, REL, PLANO,')
lnota = linha(rel, '         "nota": "agente de preparacao claude-construtor-v410; quem constroi nao aprova (revisor: Sonnet, D58)"')
so_notas(rel, "o deposito na fila e a rota do construtor da v410 (o texto MONTADO dos arquivos; a prosa da v410: a moldura da D64 e as ressalvas)", [
    (l3, l3.replace("(claude-construtor-v410, 05/11/2026)", "(claude-construtor-v410, 06/11/2026; molde: depositar_construtor_v409.py)"), 1),
    (lres, lres.replace("(bundle de %s modulos novos em TGLExt/: TraducaoTuring e ParNaFaceDeFock);", "(bundle de %s modulo(s) novo(s) em TGLExt/: IALD2);"), 1),
    (lsub, '_PREFIXO_SUBST = ("SUBSTITUI o deposito do PRONTA anterior (%s): a preparacao foi refeita. " % ", ".join(_ANT0)) if _ANT0 else ""', 1),
    (ltxt, 'txt = (_PREFIXO_SUBST + "v410 (IALD2: o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD, o signo e o seletor) preparada em 06/11/2026 por claude-construtor-v410 para a gerencia c1 (nada instalado; o rito nao rodou; o Nos e a Bancada de producao so\' foram lidos). " + res + ".\\n\\n"', 1),
    (lmold, '       + ' + repr(MOLD), 1),
    (lress, '       ' + repr(RESS + "\n\n"), 1),
    (lr2, lr2.replace('"novo:v410-preparada-05nov"', '"novo:v410-preparada-06nov"').replace('"v410-construtor-05nov"', '"v410-construtor-06nov"'), 1),
    (ltit, '         "titulo": "v410 preparada (IALD2, 06/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]),', 1),
    (lper, '         "pergunta": "a pedra IALD2 (%s modulo; as ancoras contadas pelo recibo da gerencia) compila no trio sobre o kernel da v409 selada, e a cadeia da v410 (registro iald2_v410, specs cunhagens_v410/kh_n1_cobertura_v410) fica pronta para a gerencia lancar o orquestrador?" % J.get("n_modulos_novos"),', 1),
    (ldad, '         "dados": ["kernel do Nos v409 selado (copia em C:\\\\t\\\\k410c\\\\final)", "pedra: work\\\\pedras_candidatas_06nov (IALD2, que sucede a LeitorDoCodigoR1)", "as falas do operador de 06/11 (de uma, so\' o trecho: D65)"],', 1),
    (lmet, '         "metodo": "bundle de %s modulo em TGLExt/ (molde: a v409), lake build incremental + Audit no sandbox k410c; candidato pelo molde da v409; comparacao AST; ensaio a seco; ESPERADOS; conferidor (controle negativo e caminho positivo); citacoes; guarda das frases (D64, D68b: as formas de estatuto e as parafrases desde o inicio); B(n) pre-selo (so\' ensaio, a producao so\' lida); harnesses; nada instalado no Nos, rito nao rodado, sem commit/push" % J.get("n_modulos_novos"),', 1),
    (lprox, lprox.replace("revisao de terceiro (Sonnet, D58)", "revisao de terceiro (Sonnet, D69)"), 1),
    (lref, lref.replace('"refs": ["cadeia.preparacao_v409", "kernel.traducao_turing_r9_inscricao_e_sat_05nov", "kernel.par_na_face_de_fock_ligado_05nov"]', '"refs": ["cadeia.preparacao_v409", "um_py.v410_preparacao_aberta_06nov"]'), 1),
    (lnota, '         "nota": "agente de preparacao claude-construtor-v410; quem constroi nao aprova (revisor: Sonnet, D69)" + ("; REFEITA: este PRONTA (%s) substitui o(s) anterior(es) %s" % (S, ", ".join(_ANT)) if _ANT else "")}]', 1)])

# ---------------- o fecho da preparacao (ato da gerencia; so' adaptado)
rel = "fechar_preparacao_v410.py"
l5 = linha(rel, "Tudo LE PREPARACAO_v410_PRONTA.json: nenhum hash e' digitado aqui.")
ltit = linha(rel, '         "titulo": "v410 preparada (A traducao as classes de Turing, 05/11/2026)')
lprox = linha(rel, '         "proximo_passo": "revisao de terceiro (o Sonnet, D58:')
ltxt = linha(rel, 'txt = ("v410 (A traducao as classes de Turing e o par na face de Fock) preparada em 05/11/2026')
lmold = linha(rel, '       "A moldura vale em todo texto: P = nP e\' teorema da TGL no modo selecao')
lress = linha(rel, '       "As ressalvas vao ditas: a igualdade relativa a um leitor nao decide a pergunta da maquina sem leitor')
lr2 = linha(rel, 'r2 = subprocess.run([PY, "-X", "utf8", MEM, "depositar", "--quem", "claude-construtor-v410"')
so_notas(rel, "so' adaptado (ato da gerencia, nao executado pelo construtor): a prosa da v410 (Mapa, fila, ACOM: a moldura da D64 e as ressalvas), o revisor pela D69, o slug de 06/11", [
    (l5, l5.replace("adaptado em 05/11/2026 a v410 por claude-construtor-v410 (A traducao as classes de Turing: bundle de 1 modulo em TGLExt/, registro traducao_turing_v409; nenhuma chave antiga muda).", "adaptado em 06/11/2026 a v410 por claude-construtor-v410 (IALD2: bundle de 1 modulo em TGLExt/, registro iald2_v410; nenhuma chave antiga muda)."), 1),
    (ltit, '         "titulo": "v410 preparada (IALD2, 06/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,', 1),
    (lprox, lprox.replace("revisao de terceiro (o Sonnet, D58:", "revisao de terceiro (o Sonnet, D69:"), 1),
    (ltxt, 'txt = ("v410 (IALD2: o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD, o signo e o seletor) preparada em 06/11/2026 por claude-construtor-v410 para a gerencia c1 (nada instalado; o rito nao rodou). " + res + ".\\n\\n"', 1),
    (lmold, '       ' + repr(MOLD), 1),
    (lress, '       ' + repr(RESS + "\n\n"), 1),
    (lr2, lr2.replace('"novo:v410-preparada-05nov"', '"novo:v410-preparada-06nov"').replace('"v410-preparada-05nov"', '"v410-preparada-06nov"'), 1)])

# ---------------- a inscricao ACOM da gerencia (so' adaptada; rodar e' ato da gerencia)
rel = "acom_inscrever_prep_v410.py"
l4 = linha(rel, '"""Memoria ACOM da PREPARACAO da v410 (gerencia c1, 05/11/2026;')
lun = linha(rel, '                    "constraints": {"unit": "preparacao_e_cadeia_de_selo_v410_traducao_as_classes_de_turing"')
lrev = linha(rel, '                                    "no_install_no_rite_no_commit_no_push": True, "reviewer_distinct_from_builder": "Sonnet (D58 da v410, como a D54 da v409;')
ltx = linha(rel, '                "text": "Preparacao da v410 (A traducao as classes de Turing e o par na face de Fock): 2 modulos')
nlx = ('                "text": "Preparacao da v410 (IALD2): %s modulo (IALD2; ' + NOME_IALD2 + ') no sandbox k410c; kernel construido e auditado; candidato %s, ensaio a seco %s, p00 %s/%s, PRONTA %s/%s portoes (pronta=%s), pelo construtor (agente); '
       'revisao de terceiro do Sonnet (D69) em curso. Nada instalado no Nos; rito nao rodado; sem commit/push." % (_pr.get("n_modulos_novos"), _cm.get("sha16"), _en.get("veredito"), _ok_p00, _n_p00, sum(1 for v_ in _port.values() if v_), len(_port), _pr.get("pronta")),')
so_notas(rel, "so' adaptado (ato da gerencia, nao executado pelo construtor): o uso, a unidade e o revisor (D69) da v410; o texto de abertura LE os numeros dos arquivos (nada digitado); o proximo passo com o fim no HANDOFF (D68a)", [
    (l4, l4.replace("(gerencia c1, 05/11/2026;", "(gerencia c1, 06/11/2026;"), 1),
    (lun, lun.replace('"preparacao_e_cadeia_de_selo_v410_traducao_as_classes_de_turing"', '"preparacao_e_cadeia_de_selo_v410_iald2"'), 1),
    (lrev, lrev.replace("Sonnet (D58 da v410, como a D54 da v409;", "Sonnet (D69 da v410, como a D58 da v409;"), 1),
    (ltx, nlx, 1),
    ('"event_id": "prep-v410-aberta-05nov",', '"event_id": "prep-v410-aberta-06nov",', 1),
    ("e o HANDOFF, que e' o fim da cadeia desta versao; a custodia completa e o release do app sao da sessao de custodia, D57a)", "e o HANDOFF, que e' o fim da cadeia desta versao; a custodia completa e o release do app sao da sessao de custodia, D68a)", 1)])
print("misc: ok | build_s", BUILD_S, "audit_s", AUDIT_S, "| carimbo v409", SHA_CARIMBO_V409)
