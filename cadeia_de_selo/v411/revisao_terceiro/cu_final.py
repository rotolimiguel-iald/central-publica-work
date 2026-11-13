# -*- coding: utf-8 -*-
"""CU-FINAL: monta o registro da conferencia unica (CU.json e .md) e as copias identicas REVISAO_TERCEIRO_v411.json/.md (temporario + os.replace). Hashes lidos do disco AGORA."""
import hashlib, json, os, time
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
RT = os.path.join(V, "revisao_terceiro")
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
cand = os.path.join(V, "um_v411_candidato.py")
ini = json.load(open(os.path.join(RT, "ESTADO_REVISAO_v411.CU.json"), encoding="utf-8"))["inicio"]
fim16 = sha16(cand)
fimb = os.path.getsize(cand)
assert ini["candidato_sha16_no_inicio"] == "1203b1f9202020d6"

# ---------------- achados ABERTOS
A = []
A.append({"id": "CU-1", "sev": "MEDIO", "dentro_do_escopo": True,
          "onde": "gerar_relatorio_v411.py, linha 112 (o portao kernel do dicionario PORTOES), alterada pelo conserto C-10 (backup gerar_relatorio_v411.py.bak_20261112_194113_r1fix); o RELATORIO e o PREPARACAO_v411_PRONTA.json foram gerados com ela",
          "achado": "O conserto C-10 acrescentou all(k_ in KR for k_ in (rc, sorry, erros)), mas pos um comentario inline “# (C-10 da revisao de terceiro: ...)” no MEIO da expressao: tudo o que vem depois do “#” na mesma linha virou comentario, e com ele três condicoes: PB.get(ok) is True, all(PB.get(criterios).values()) e PB.get(n_modulos_compilados) == 0. Medido por AST (cu_e2.py): o portao tinha 12 condicoes e tem 10; sairam essas tres, entrou a das chaves. O arquivo compila, o relatorio passa, e o CONSERTO_R1_v411.md diz so' que o portao passou a exigir as chaves (a regressao nao esta dita). Efeito pratico hoje: nenhum, porque POS_BUILD_v411.json (lido agora) tem ok True, criterios todos True e n_modulos_compilados 0, e o portao p00 repete ok e criterios (p00_precondicoes_v411.py l.47, “nenhum_modulo_compilado” dentro dos criterios). Mesmo assim e' uma condicao que ficou mais frouxa sem ser dita: o item E do pedido a recusa, e o portao kernel do relatorio deixou de exigir o que o seu proprio nome e o resto da linha mostram exigir.",
          "correcao_pedida": "Tirar o comentario do meio da expressao (mover o “# (C-10 ...)” para o fim da linha 113, depois do ultimo parentese, ou para a linha de cima), regenerar o relatorio e o PREPARACAO por script e conferir por AST que o portao kernel volta a ter as 12 condicoes mais a das chaves (13). E' uma troca de lugar de um comentario; nada mais do conserto precisa mudar."})
A.append({"id": "CU-2", "sev": "BAIXO", "dentro_do_escopo": True,
          "onde": "core, cunhagens_v411.extras.textos_da_gerencia_citados[].nome (6 itens) e o candidato (as mesmas 6 cadeias, 2 vezes cada)",
          "achado": "Seis nomes de arquivos GERENCIA_11nov_* e GERENCIA_12nov_* (textos da gerencia a que o operador respondeu) ficam em claro no core. Nao sao falas dele nem transcricao (o texto nao esta' la; so' o nome e o sha256), nao aparecem no artigo, na forma canonica, no manifesto nem na saida do rito, e a decisao D183 manda citar os textos da gerencia por sha256. Mas o nome carrega palavras do tema da conversa, que e' o que a D181 quis tirar nas falas.",
          "correcao_pedida": "Citar esses seis textos por sha256 e papel, sem o nome do arquivo, como as onze ordens (decisao da gerencia; nao bloqueia)."})
A.append({"id": "CU-3", "sev": "BAIXO", "dentro_do_escopo": True,
          "onde": "artigo EN, secao nova, paragrafo O achado do suporte e a emenda (quadro_v411.py, texto EN trocado no B-09)",
          "achado": "“the weights frozen on 6 Nov are its (the collaboration's) and give zero weight to that component” e' correto mas duro de ler; o ingles diz o mesmo que o portugues.",
          "correcao_pedida": "Opcional: “are the collaboration's and give zero weight to that component”."})
R1_ABERTAS = [
    ("A-B1", "ressalva conhecida da R1 (escopo A); o pedido manda nao reabrir"), ("A-B2", "idem"), ("A-B3", "idem"), ("A-B4", "idem (a lista das falas fora do desenho saiu do core pelo D181; o achado perde o objeto no que sai, fica o registro)"),
    ("A-B5", "idem (a quarta entrada de erratas agora e' a E44; a lista foi ao lado)"), ("A-B6", "idem"),
    ("B-05", "o resumo do que o teste nao decide e' o aprovado; a custodia tem o texto pinado (D183/pedido secao 4)"),
    ("B-06", "as sete ressalvas em ingles ficam em portugues no EN"), ("B-07", "a regra (g) das citacoes do pos-rito"),
    ("B-09", "o resto do B-09 (os marcadores de espacamento 1pt, 4pt e 0pt como linhas no TXT, que ja' existiam na v410; a palavra decisivo no titulo da secao, palavra do operador D169): ordenado que fique"),
    ("C-03", "a cota de 10 s tem margem de cinco vezes nos ritos reais"), ("C-06", "a gerencia registra o sha16 dos modulos da G1 antes do rito e avisa a custodia"),
    ("C-07", "ressalva conhecida da R1 (escopo C)"), ("C-08", "o reverter nao restaura o artigo: herdado do molde"), ("C-09", "(b): o teto de 5 h nao encerra a arvore do um.py")]
for i, (rid, nota) in enumerate(R1_ABERTAS):
    A.append({"id": rid, "sev": "BAIXO", "dentro_do_escopo": False, "onde": "ver REVISAO_TERCEIRO_v411.R1.%s.json, achado %s" % (rid[0], rid),
              "achado": "Ressalva da R1 que o conserto nao fez, por ordem (pedido secao 4): %s." % nota, "correcao_pedida": "Nenhuma nesta versao; repetir na lista da versao seguinte."})
n_alto = sum(1 for a in A if a["sev"] == "ALTO")
n_medio = sum(1 for a in A if a["sev"] == "MEDIO")
n_baixo = sum(1 for a in A if a["sev"] == "BAIXO")

# ---------------- situacao dos achados da R1
S = []


def s(i, sev, sit, como):
    S.append({"id": i, "sev_na_R1": sev, "situacao": sit, "como_conferi": como})


for i in ("A-B1", "A-B2", "A-B3", "A-B4", "A-B5", "A-B6"):
    s(i, "BAIXO", "fica como ressalva", "nao reaberto (pedido secao 4); o escopo A foi aprovado na R1 e so' o delta do conserto foi relido (cu_a1_ast.py, cu_a2_show.py, cu_a3.py, cu_a5.py)")
s("B-01", "ALTO", "resolvido", "cu_c1.py e cu_c2.py sobre o rendido novo (dry_v411, PT e EN, txt e tex, e o PDF extraido): os dois blocos (os estresses; o esperado pelos agregados) terminam com o fecho dos quatro obrigatorios com o Z das Cefeidas livres no formato do topo ($4,38$ no txt, $4{,}38$ no tex, 4.38 no EN; o core diz 4,379645...); todo paragrafo novo ou alterado do tex (36 por idioma) com o primario traz os quatro, salvo O que o teste nao decide (descritivo; ja' era assim na R1, a guarda nao o acusa) e a E44 EN (cita o desenho D159, sem Z); a guarda do construtor sobre o texto inteiro acusa no novo o mesmo numero de paragrafos que no v410 selado (cu_c3.py)")
s("B-02", "MEDIO", "resolvido", "cu_c4.py: 14 frases minhas, PT e EN, com e sem cifrao, com e sem os quatro, provado na natureza no H0DN e neutras: todas como esperado; runtime_h0dn_v411.py l.54 passou a Z\\$?\\s+; guarda_frases ganhou 2 proibidas e 2 limpas em TeX (PROIBIDAS 29, LIMPAS 20, lido do modulo)")
s("B-03", "MEDIO", "resolvido", "cu_c6.py e cu_c7.py: a E44 PT e EN igual ao DESENHO (sha16 79234a941851d20b e 5a468bc7511570ab) no candidato, no core (h0dn erratas e cunhagens_v411.erratas), no tex (apos desfazer o escape), no txt (so' diferem os seis cifroes dos delimitadores de formula, convencao do txt), na linha do .md e no texto extraido do PDF; e' o ultimo paragrafo da secao nova (o seguinte abre a secao IALD ao quadrado)")
s("B-04", "BAIXO", "resolvido", "cu_c8.py: o fecho vem depois da frase ao lado do estatuto e no item O coracao, 2 de 2 em txt e tex, PT e EN")
s("B-05", "BAIXO", "fica como ressalva", "nao reaberto (pedido secao 4)")
s("B-06", "BAIXO", "fica como ressalva", "nao reaberto (pedido secao 4)")
s("B-07", "BAIXO", "fica como ressalva", "nao reaberto (pedido secao 4)")
s("B-08", "BAIXO", "resolvido", "a E44 inclui os dois trechos antigos sobre beta a 5 sigma (o paragrafo O que nao se declara, da v392, e a cadeia de maquina da estatuto_da_prova_v391); texto conferido byte a byte em cu_c6.py")
s("B-09", "BAIXO", "resolvido em parte; o resto fica como ressalva", "cu_c8.py: rotulos legiveis 5 de 5 no PT e no EN (sem chave de maquina); no EN “hers” saiu (its (the collaboration's)) e as datas sao 6 Nov e 11 Nov, sem dd/mm no paragrafo; o resto foi ordenado que ficasse")
s("C-01", "ALTO", "resolvido", "c_26_step0.py: FALTAM [] (runtime_v411.py saiu, entraram runtime_h0dn_v411.py, conferir_conversa_v411.py, guarda_conversa_v411.py e GUARDA_CONVERSA_BASE_v410.json); c_28_refs_sh.py: 34 ausentes, todos saidas do rito/da cadeia ou opcionais (patch_arvore_indice_v411.py e' guardado por [ -f ]), nenhum insumo obrigatorio; sh -n rc 0 no chain e no rito (cu_d1.py); li a cadeia inteira; os 22 scripts nomeados existem e compilam em memoria; os imports locais deles existem no sys.path que eles montam; os que rodam com -I nao importam nada de fora da stdlib (cu_d2.py); li a checagem estatica do p00 e os tres controles (l.92-143)")
s("C-02", "BAIXO", "resolvido", "li conferir_conversa_v411.pdf_tex_ok e _controles_pdf_tex: exigem o .tex PT e EN com a abertura do resumo ratificado e o titulo do quadro novo e cada .pdf com tamanho > 0 e mtime >= o inicio do rito, lido de rito_horarios_v411.txt (V411_RITO_HORARIOS, ou o do pacote, que o rito grava nas linhas 248 e 261 do rito_v411.sh, ou o do Nos); os controles (PDF velho, PDF vazio, TeX sem a abertura, TeX sem o titulo, mais base e restaurado) rodam em copia temporaria")
s("C-03", "BAIXO", "fica como ressalva", "nao reaberto (pedido secao 4)")
s("C-04", "BAIXO", "resolvido", "diff do harness_textos_ensaio_v411.py: duas variantes novas (sem a chave p2_ao_lado_da_v387; com o valor trocado), variante( 526 -> 531, falha( 53 -> 53 (cu_e4.py)")
s("C-05", "BAIXO", "resolvido", "diff do p00: _memory_md_conferido(idx_override) e o controle que injeta uma COPIA do indice com 196+ linhas e exige pendente (ver_ok so' relaxa quando ha override, nunca no caminho real); PRECONDICOES_v411.json: 33 de 33 [lido, nao reexecutado]")
s("C-06", "BAIXO", "fica como ressalva", "nao reaberto (pedido secao 4)")
s("C-07", "BAIXO", "fica como ressalva", "nao reaberto (pedido secao 4)")
s("C-08", "BAIXO", "fica como ressalva", "nao reaberto (pedido secao 4)")
s("C-09", "BAIXO", "(a) resolvido; (b) fica como ressalva", "cu_d4.py: orquestrador/pos_treino_v411.py compila em memoria, o diff contra o backup e' so' a linha 237 (not is_file() or sha16 != v); (b) nao reaberto")
s("C-10", "BAIXO", "NAO resolvido como declarado: a parte pedida entrou, mas o conserto introduziu uma regressao (CU-1)", "cu_e2.py: o portao kernel ganhou a exigencia das chaves e perdeu tres condicoes (comentario no meio da expressao, l.112)")
s("C-11", "BAIXO", "resolvido", "cu_d4.py: nenhum *DEPURACAO* em pos_rito; os dois resumos estao em C:\\t\\k411c\\conserto_r1\\depuracao com os sha16 declarados (639359d6b18c6f7c e de67be4bab227204)")

# ---------------- arquivos revisados (so' fontes; sha16 lido AGORA)
LISTA = ["um_v411_candidato.py", "delta_v411.py", "quadro_v411.py", "runtime_h0dn_v411.py", "registros_v411.py", "registros_h0dn_v411.py", "gerar_candidato_v411.py", "guarda_frases_v411.py", "guarda_conversa_v411.py",
         "conferir_conversa_v411.py", "GUARDA_CONVERSA_BASE_v410.json", "conferir_rito_v411.py", "p00_precondicoes_v411.py", "gerar_relatorio_v411.py", "gerar_esperados_v411.py", "ensaio_a_seco_v411.py", "teste_conferidor_positivo_v411.py",
         "_teste_quadro_v411.py", "conferir_instalar_rito_v411.py", "copiar_insumos_v411.py", "diff_e_pinos_v411.py", "rito_v411.sh", "pos_rito/chain_pos_rito_v411.sh", "pos_rito/leitura_v411.py", "pos_rito/registrar_mapa_v411.py",
         "pos_rito/harness_textos_ensaio_v411.py", "pos_rito/harness_fechar_sandbox_v411.py", "pos_rito/teste_textos_sem_candidato_v411.py", "pos_rito/teste_mapa_sem_candidato_v411.py", "pos_rito/textos_v411_novo.pysnip",
         "pos_rito/gerar_derivacao_pos_rito_v411.py", "orquestrador/pos_treino_v411.py", "DESENHO_v411.md", "TOPO_RATIFICADO_v411.json"]
ARQ = {}
for rel in LISTA:
    p = os.path.join(V, rel.replace("/", os.sep))
    assert os.path.isfile(p), rel
    ARQ[rel] = sha16(p)

REND = {}
for p in (r"C:\t\k411c\dry_v411\dry_v411_pt.tex", r"C:\t\k411c\dry_v411\dry_v411_pt.txt", r"C:\t\k411c\dry_v411\dry_v411_pt.pdf", r"C:\t\k411c\dry_v411\dry_v411_en.tex", r"C:\t\k411c\dry_v411\dry_v411_en.txt", r"C:\t\k411c\dry_v411\dry_v411_en.pdf",
          r"C:\t\k411c\dry_v411\core_ensaio.json", r"C:\t\k411c\falso_nos_v411\um_absoluto_forma_canonica.md", r"C:\t\k411c\falso_nos_v411\um_absoluto_manifest.md", r"C:\t\k411c\falso_nos_v411\rodada_v411_stdout.txt",
          os.path.join(V, "pos_rito", "HARNESS_TEXTOS_ENSAIO_v411.json"), os.path.join(V, "pos_rito", "CUSTODIA_v411_RASCUNHO.txt"), os.path.join(V, "PRONTO_POS_RITO_v411.json"), os.path.join(V, "PRECONDICOES_v411.json"),
          os.path.join(V, "PREPARACAO_v411_PRONTA.json"), r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos\README_PROJETADO_v411.md", r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos\HANDOFF_v411_CUSTODIA.md",
          os.path.join(V, "VERBATIM_CONGELADO_v411.json"), os.path.join(V, "um_v411_candidato.py.bak_20261112_195053")):
    REND[p] = sha16(p)

CONF = {
    "A": "Delta por AST de topo entre o candidato revisado na R1 (backup 21e87eb3df5098f8) e o final (1203b1f9202020d6): 1397 -> 1398 nos; 5 removidos (_V411_AB, _V411_FE, _v411_fala_do_autor_tex, _v411_fala_do_autor_md, _V411_FALA_DO_AUTOR), 6 novos (_v411_fecho_blocos, _v411_rotulo_agregado, _v411_errata_e44_tex, _V411_FALAS_CITADAS, _V411_TEXTOS_DA_GERENCIA, _v411_citar_falas), 14 mudados, 1378 iguais, ordem relativa dos comuns igual. Cada no foi lido e e' explicado por O1 a O5, B-01, B-02, B-03/B-08, B-04, B-09 ou D181; fora dos nos so' mudam linhas em branco (3); os tres blobs (_EMBEDDED_KERNEL_FILES, _V411_H0DN_INSUMOS, _V410_H0DN_INSUMOS) sao nos iguais; h0dn_bg1_v411 muda so' o docstring; as funcoes do gate nao estao entre os mudados; main muda so' o print da linha da v411; nenhum beta literal e nenhum numero do teste digitado nas linhas acrescentadas (cu_a3.py, cu_a5.py). No core do ensaio (sha16 faec6bf29a4a2987): h0dn_bg1_v411 com as 16 checagens verdadeiras (c1 a c16), all_verified, opened_once, e os valores iguais, por igualdade exata, ao RESULTADO_DA_ABERTURA_V411.json do clone publico (blob do HEAD == disco, sha16 573fbf87db2ccfe8): t, z_null, z_tgl, D, ramo, cabeca, Cefeidas livres, portao 1, estresses, coerencia e suporte (cu_a4.py a cu_a4c.py).",
    "B": "A D181 por meio meu (cu_b1.py; nao importa guarda_conversa_v411): as 11 falas da casa pela lista de VERBATIM_CONGELADO_v411.json (os 11 sha256 conferidos), a ordem da D181 (sha256 93d812a0...) e a fala fora do desenho; agulhas: o texto inteiro, 19 linhas ou frases de 24+ caracteres, 457 janelas de 6 palavras, 26 nomes (e radicais); formas cru, JSON ascii e utf8, repr, ascii(), unicode_escape; alvos: o fonte do candidato (texto cru e as cadeias decodificadas do AST), o core do ensaio (todas as cadeias e as chaves), artigo PT e EN (tex e txt), forma canonica, manifesto, saida do rito, cada um contra o seu correspondente na v410 selada do Nos. Resultado: 0 ocorrencias de texto inteiro ou linha de 24+ (salvo a fala curta de 17 caracteres, indice 10, cuja contagem e' IGUAL a da v410 em todo alvo: fonte 20=20, core 9=9, artigo 1=1; cu_b2.py), 0 nomes de arquivo de fala, 0 janelas de 6 palavras alem da base (a unica janela, da fala de indice 3, aparece 1 vez no candidato e 1 vez na v410; cu_b9.py), 0 informativos no topo. Controles do meu scan: o candidato antigo e' recusado (23 ocorrencias, 24 nomes, 399 janelas), linha plantada em tres formas, seis palavras plantadas, nome plantado recusados, o limpo passa (cu_b2.py). Estrutural (cu_b4.py): o item A fala do autor / The author's words nao esta' em nenhum rendido (PT, EN, md); a linha da v411 no stdout cita data e sha16 48612e7f3c9004f2, sem aspas angulares; o docstring idem; cunhagens_v411 com 11 itens (quando, sha256, papel, autor, citado_por_sha256 True, texto_transcrito False), 11 sha256 iguais aos dos arquivos lidos agora, chave v411_cun_ + sha16, nenhum texto, trecho ou nome de arquivo; veredito com OPERATOR_ORDERS ... CITED_BY_DATE_AND_SHA256_NOT_TRANSCRIBED, dez decisoes (D181 incluida) e quatro erratas (E44 incluida). So' DEPOIS, a guarda do construtor importada em memoria (cu_b6.py, sem gerar base): ok, 0 achados, 21 de 21 controles; concorda com o meu scan e recusa o candidato antigo (33 achados). Nada em rito le arquivo da casa (cu_b7.py: os nos mudados nao abrem arquivo). Aberto: CU-2.",
    "C": "Sobre o rendido do ensaio do candidato final (a tabela do pedido confere com o disco: 42 linhas, 0 divergencias, cu_g1.py). C.1 B-01 resolvido (cu_c1.py, cu_c2.py, cu_c3.py, cu_c5.py). C.2 B-02 resolvido (cu_c4.py). C.3 B-03/B-08 resolvido (cu_c6.py, cu_c7.py). C.4 B-04 resolvido (cu_c8.py). C.5 B-09 parte aceita resolvida (cu_c8.py). C.6 traducoes EN lidas (E44, fechos, rotulos, frase do estatuto): fieis; uma miudeza (CU-3). C.7 (cu_c9.py): nos 36 paragrafos novos ou alterados do tex PT e EN nenhum especial TeX nao escapado nos textos novos (o til de O selo pela propria tecnologia e' texto selado antigo, espaco amarrado), chaves balanceadas, cifroes pares, a cauda de cada paragrafo achada no texto extraido do PDF (PyMuPDF); logs do LaTeX: 0 erros, 10 refs indefinidas e 22/23 caixas cheias, iguais as do v410.",
    "D": "D.1 C-01 resolvido (ver situacao); chain lida inteira; checagem estatica do p00 lida (so' $PK/ e $SEL/ literais; ver ressalvas). D.2 C-02 resolvido. D.3: C-04, C-05, C-09 (a), C-11 como o conserto declara; C-10 nao: CU-1. D.4, o que o rito REAL pode recusar por causa do conserto: (i) nomes que o conferidor procura no Nos: um.py, um_absoluto.json, um_absoluto_pt/en .txt .toc .tex .pdf, forma canonica, manifesto, selo e tgl_kernel existem hoje (v410); rodada_v411_stdout.txt e rito_horarios_v411.txt nascem do rito (cu_d5.py); (ii) rito_horarios_v411.txt e' gravado pelo proprio rito_v411.sh em $PK (l.248 inicio, l.261 fim) e o conferidor le exatamente ali (V411_RITO_HORARIOS, depois o do pacote, depois o do Nos): o lugar confere; (iii) a guarda da conversa sobre a saida REAL: rodei a mesma guarda, em memoria, sobre os artefatos reais da v410 selada do Nos (fonte 45,9 MB, core 16,5 MB, artigo, forma canonica, manifesto 4,4 MB, saida do rito 278 KB): ok, 0 achados (cu_d3.py); a unica linha curta (12 a 23 caracteres) e' a de 17, com base 0 no stdout da v410 real e 0 no stdout do ensaio, e o stdout real so' acrescenta linhas de kernel; falso positivo nao esperado; (iv) nada novo depende de arquivo que so' existe no ensaio (ESPERADOS, GUARDA_CONVERSA_BASE_v410.json e os arquivos das falas sao da casa e existem; base() nao regera a base porque o JSON confere). Risco residual dito: os controles do PDF/TeX dependem de a abertura e o titulo estarem numa linha so' do .tex (determinista, igual no ensaio); fail-closed se nao.",
    "E": "Os 29 arquivos com backup *_r1fix (um por arquivo; o mais antigo e' o unico): diff de cada um contra o de hoje, lido (cu_e1.py); toda mudanca e' explicada por um item do conserto, exceto a regressao CU-1; nenhum assert saiu, nenhuma lista de proibidos encolheu, nenhum teste virou aviso; os controles do conserto so' cresceram (guarda_conversa: o plantio passou a todos os alvos e o fonte tem os literais adjacentes juntados). Contagens declaradas conferidas: guarda_frases 29 proibidas e 20 limpas (lido do modulo); guarda_conversa 6 controles no p00 e 21 nos rendidos (lido; todos True); conferidor 84 -> 89 itens (AST); p00 28 -> 33 (+3 C-01, +1 C-05, +1 D181; PRECONDICOES 33 de 33); harness dos textos variante( 526 -> 531 e falha( 53 -> 53; leitura P.append( 170 -> 170; harness do fechar _recusa_com_core( 57 -> 58. NAO reexecutados (vedado): p00, ensaio a seco, harnesses, testes sem candidato do pos-rito, orquestrador. Aberto: CU-1.",
    "F": "Os textos do pos-rito: HARNESS_TEXTOS_ENSAIO_v411.json (2976 cadeias), PRONTO_POS_RITO_v411.json (cadeias, incluindo os blocos do README, o paragrafo, as linhas de estatuto e o X_TEXTO), CUSTODIA_v411_RASCUNHO.txt, o README projetado e o handoff do ensaio: o meu scan (cu_f2.py) acha 0 ocorrencias de texto inteiro, de linha de 24+, de nome de arquivo de fala e 0 janelas de 6 palavras; toda ocorrencia do primario (45) leva a linha das Cefeidas livres com o numero no mesmo item, salvo uma (o item O que o teste nao decide do handoff, que e' descritivo, como no artigo) (cu_f3.py); o README_PROJETADO_v411.md mede 40.921 bytes (arquivo lido agora, gravado 22:08:15, depois do inicio da regeneracao), teto 40.960, folga 39; as fontes dos blocos do README (blocos_custodia_v411.py, as chaves do TOPO) nao mudaram no conserto. Fora do escopo, dito: HARNESS_FECHAR_SANDBOX_v411.json (registro da casa) traz nomes (nao texto) de arquivos de falas."}

RESSALVAS = [
    "Nao rodei, por vedado: p00, ensaio a seco, harnesses, testes sem candidato do pos-rito, gerar_relatorio, fechar_preparacao, o conferidor do rito, o orquestrador, o rito e a cadeia do pos-rito. Os resultados deles (PRECONDICOES 33 de 33, PREPARACAO pronta true com 30 portoes, harness dos textos 80 etapas, ensaio a seco TUDO PASSOU) foram LIDOS dos recibos e sao [DECLARADO pelo construtor]; o que refiz eu: a AST, os dois scans da D181, a guarda do construtor em memoria, as guardas de frases, a leitura da cadeia e dos diffs.",
    "O item D.4 e' por leitura e por simulacao em memoria sobre a v410 real selada e sobre o ensaio; nao ha como saber sem o rito real o que a saida real do v411 traz alem do que o ensaio emula (o kernel e' o da v410 byte a byte).",
    "Nao reli o que o escopo A aceitou na R1 (por ordem do pedido), nem os blobs base64 por dentro (conferi so' que os nos sao iguais por AST; decisao D183).",
    "O PDF foi lido so' como texto extraido (PyMuPDF); nao vi as paginas. Nao reproduzi a compilacao do LaTeX.",
    "Nao medi o README projetado de novo (nao posso rodar o teste de blocos, que escreve fora das minhas pastas): medi o arquivo projetado que ele grava (40.921 B) e conferi que o conserto nao tocou as fontes dos blocos.",
    "O CONSERTO_R1_v411.md fala de 29 arquivos com backup: confere (29 pares); o arquivo pos_rito/textos_v411.py (O4, l.299) nao tem backup proprio, e eu o li so' pelo pysnip (que o gera) e pelos textos rendidos.",
    "Nao abri work\\h0dn_bg1_v410_09nov\\kimi\\, nem a pasta da nativa, nem fiz POST na Bancada; o Nos so' foi lido."]
RESV_SEG = [
    "As ressalvas da R1 que ficam (listadas em achados, dentro_do_escopo false).",
    "CU-2 (nomes dos seis textos da gerencia no core) e CU-3 (frase EN).",
    "A checagem estatica do p00 (C-01) cobre so' os literais $PK/ e $SEL/ do chain: nao cobre os scripts chamados por $TOOLS/ nem os imports locais dos scripts; eu os conferi por fora (cu_d1.py e cu_d2.py) e deram limpo; vale incluir na versao seguinte.",
    "O fonte do candidato guarda 87 ocorrencias de nomes OPERADOR_10nov a 12nov de OUTRAS falas (herdadas do texto selado da v410, que tem 158): D181 vale so' para o novo, nenhuma e' nome das 11 nem da ordem; os quatro blobs base64 carregam 5 nomes por dentro (D183).",
    "HARNESS_FECHAR_SANDBOX_v411.json (registro da casa em work\\, espelhado pela custodia) traz nomes de arquivos de falas (18 ocorrencias, de 12 nomes), sem texto; a regra da casa de 25/10 e o aviso ao operador (pedido secao 4) cobrem work\\ em geral.",
    "O delta_v411.py le o texto das falas (decidido, D183); o orquestrador le a ordem de abrir para a frase de autorizacao (decidido, D183).",
    "Os controles do conferidor do PDF/TeX substituem a abertura e o titulo no .tex cru, e dependem de ela estar numa linha so': determinista no mesmo gerador, fail-closed; um comentario no codigo bastava."]
ROTAS = [
    {"consulta": "rotas.py consultar \"cadeia.preparacao_v411\" (feita antes de examinar)", "rota_id": "cadeia.preparacao_v411", "status": "EM_CURSO", "o_que_o_mapa_disse": "v411, frente POS-RITO, D174: o painel do README, a medida de 40921 B com folga de 39 B (README projetado), os harnesses nao rodados; n_registros 6; nao_refazer: a medida esta feita com o renderizador da custodia sobre um handoff de ensaio; proximo passo: a gerencia roda os harnesses"},
    {"examinado": "a conferencia do conserto da R1 e a D181 (cadeia.preparacao_v411): o delta do candidato por AST, a D181 por dois meios independentes, os achados B-01..B-04, B-08, B-09, C-01, C-02, C-04, C-05, C-09 (a), C-10, C-11, os 29 diffs do conserto, os textos do pos-rito e o que o rito real poderia recusar",
     "resultado": "um achado MEDIO novo, CU-1 (gerar_relatorio_v411.py l.112: um comentario no meio da expressao desligou tres condicoes do portao kernel do relatorio, mitigado pelo p00); tres BAIXOS; todo o resto confere", "registro_no_mapa": "da gerencia (nao registrei)"}]

agora = time.strftime("%Y-%m-%dT%H:%M:%S")
REG = {
    "aprovada": False, "candidato_sha16": fim16, "candidato_bytes": fimb,
    "revisor": "Sonnet 5.5 (agente de conferencia unica; NAO construiu a v411 nem fez o conserto da R1: quem constroi nao aprova)",
    "rodada": "conferência única do conserto da R1 (D109)", "quando": agora,
    "achados": A, "n_alto": n_alto, "n_medio": n_medio, "n_baixo": n_baixo,
    "situacao_dos_achados_da_R1": S, "arquivos_revisados": ARQ,
    "candidato_sha16_no_inicio": ini["candidato_sha16_no_inicio"], "candidato_mudou_durante_a_revisao": bool(fim16 != ini["candidato_sha16_no_inicio"]),
    "conferencias": CONF, "artefatos_renderizados_lidos": REND, "ressalvas": RESSALVAS, "ressalvas_para_a_versao_seguinte": RESV_SEG, "rotas_examinadas": ROTAS,
    "criterio_D109": "aprovada true so' se nao restar ALTO nem MEDIO dentro do escopo A a F; achado fora do escopo vai para as ressalvas da versao seguinte e nao bloqueia, salvo um ALTO para o rito. Restou 1 MEDIO dentro do escopo (CU-1, item E): aprovada false. Nenhum ALTO; nada para o rito: o defeito esta' no relatorio da preparacao, nao no que o rito sela.",
    "nota": "Tudo o que eu conferi nos itens A, B, C, D e F esta' limpo (a D181 sem uma transcricao, zero janelas alem da v410, o candidato so' mudou onde o conserto disse, o rendido traz os quatro obrigatorios e a E44 inteira, a cadeia do pos-rito nao tem mais o runtime_v411.py, o rito real nao tem razao nova para recusar). O unico bloqueio e' CU-1: um comentario no meio da linha 112 de gerar_relatorio_v411.py desligou PB.ok, os criterios do POS_BUILD e n_modulos_compilados no portao kernel do relatorio; o p00 repete essas condicoes, por isso o efeito pratico e' nulo hoje, mas e' condicao que ficou mais frouxa sem ser dita. A correcao e' mover o comentario e regerar o relatorio; depois disso nao ha outro achado meu. Este registro e' a unica conferencia (D109): nao ha nova rodada, e a decisao e' da gerencia e do operador."}


def md(R):
    L = []
    L.append("# REVISAO DE TERCEIRO v411 -- CONFERENCIA UNICA do conserto da R1 (D109)")
    L.append("")
    L.append("- aprovada: **%s**; candidato `%s` (%d bytes; no inicio `%s`; mudou durante a revisao: %s)" % ("SIM" if R["aprovada"] else "NAO", R["candidato_sha16"], R["candidato_bytes"], R["candidato_sha16_no_inicio"], R["candidato_mudou_durante_a_revisao"]))
    L.append("- revisor: %s; quando: %s" % (R["revisor"], R["quando"]))
    L.append("- abertos: ALTO %d, MEDIO %d, BAIXO %d (dos BAIXOS, 15 sao ressalvas da R1 que o conserto nao fez, por ordem)" % (R["n_alto"], R["n_medio"], R["n_baixo"]))
    L.append("")
    L.append("## Nota")
    L.append(R["nota"])
    L.append("")
    L.append("## Achados abertos")
    for a in R["achados"]:
        if a["id"].startswith("CU-"):
            L.append("### %s -- %s (dentro do escopo: %s)" % (a["id"], a["sev"], "sim" if a["dentro_do_escopo"] else "nao"))
            L.append("- **onde:** %s" % a["onde"])
            L.append("- **o que:** %s" % a["achado"])
            L.append("- **correcao pedida:** %s" % a["correcao_pedida"])
    L.append("")
    L.append("Ressalvas da R1 que ficam (BAIXO, fora do escopo): " + ", ".join(a["id"] for a in R["achados"] if not a["id"].startswith("CU-")) + ".")
    L.append("")
    L.append("## Situacao dos achados da R1")
    for x in R["situacao_dos_achados_da_R1"]:
        L.append("- **%s** (%s na R1): %s. %s" % (x["id"], x["sev_na_R1"], x["situacao"], x["como_conferi"]))
    L.append("")
    L.append("## Conferencias (itens A a F)")
    for k, v in R["conferencias"].items():
        L.append("### %s" % k)
        L.append(v)
    L.append("")
    L.append("## Ressalvas (o que NAO fiz)")
    for r in R["ressalvas"]:
        L.append("- " + r)
    L.append("")
    L.append("## Para a versao seguinte")
    for r in R["ressalvas_para_a_versao_seguinte"]:
        L.append("- " + r)
    L.append("")
    L.append("## Rotas examinadas")
    for r in R["rotas_examinadas"]:
        L.append("- " + json.dumps(r, ensure_ascii=False))
    L.append("")
    L.append("## Criterio")
    L.append(R["criterio_D109"])
    L.append("")
    L.append("## Arquivos revisados (sha16 lido no fim)")
    for k, v in R["arquivos_revisados"].items():
        L.append("- `%s` `%s`" % (k, v))
    L.append("")
    L.append("## Artefatos renderizados lidos")
    for k, v in R["artefatos_renderizados_lidos"].items():
        L.append("- `%s` `%s`" % (k, v))
    return "\n".join(L) + "\n"


def grava(path, data):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    assert os.path.getsize(tmp) == len(data) > 0
    os.replace(tmp, path)


jb = (json.dumps(REG, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
mb = md(REG).encode("utf-8")
grava(os.path.join(RT, "REVISAO_TERCEIRO_v411.CU.json"), jb)
grava(os.path.join(RT, "REVISAO_TERCEIRO_v411.CU.md"), mb)
grava(os.path.join(RT, "REVISAO_TERCEIRO_v411.json"), jb)
grava(os.path.join(RT, "REVISAO_TERCEIRO_v411.md"), mb)
print("gravado: aprovada", REG["aprovada"], "| alto/medio/baixo", n_alto, n_medio, n_baixo, "| candidato", fim16, fimb, "| mudou:", REG["candidato_mudou_durante_a_revisao"])
for n in ("REVISAO_TERCEIRO_v411.CU.json", "REVISAO_TERCEIRO_v411.json", "REVISAO_TERCEIRO_v411.CU.md", "REVISAO_TERCEIRO_v411.md"):
    p = os.path.join(RT, n)
    print(n, sha16(p), os.path.getsize(p))
