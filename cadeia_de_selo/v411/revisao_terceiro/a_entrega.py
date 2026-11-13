"""A: grava a entrega REVISAO_TERCEIRO_v411.R1.A.json e .md (sha16 de fechamento lidos do disco)."""
import datetime, hashlib, json, os
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
R = os.path.join(V, "revisao_terceiro")
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
cand_fim = sha16(os.path.join(V, "um_v411_candidato.py"))
cand_ini = "21e87eb3df5098f8"

fontes = ["um_v411_candidato.py", "base_v410/um.py", "gerar_candidato_v411.py", "registros_v411.py", "registros_h0dn_v411.py", "runtime_h0dn_v411.py", "quadro_v411.py", "delta_v411.py", "v411_pins.py",
          "guarda_frases_v411.py", "guarda_p18_v411.py", "guarda_material_privado_v411.py", "_teste_h0dn_offline_v411.py", "VERBATIM_CONGELADO_v411.json", "DESENHO_v411.md", "TOPO_RATIFICADO_v411.json"]
arquivos_revisados = {f: sha16(os.path.join(V, f.replace("/", os.sep))) for f in fontes}
rend = r"C:\t\k411c\falso_nos_v411"
artefatos = {}
for f in ("um_absoluto.json", "um_absoluto_selo.json", "um.py", "um_absoluto_pt.txt", "um_absoluto_en.txt", "um_absoluto_forma_canonica.md", "rodada_v411_stdout.txt"):
    artefatos["C:\\t\\k411c\\falso_nos_v411\\" + f] = sha16(os.path.join(rend, f))
for f in ("ESPERADOS_v411.json", "CANDIDATO_v411.json", "COMPARACAO_V410_v411.json", "DIFF_v410_v411.diff", "MANIFESTO_INSUMOS_v411.json", "kernel\\KERNEL_RECIBO_v411.json", "kernel\\POS_BUILD_v411.json", "DIFF_KERNEL_v411.txt",
          "TESTE_H0DN_OFFLINE_v411.json", "TESTE_H0DN_OFFLINE_v411_registro.json", "PREPARACAO_v411_PRONTA.json", "A2_MEDIDA_v411.json", "GUARDA_MATERIAL_PRIVADO_v411.json"):
    artefatos[f] = sha16(os.path.join(V, f))

achados = [
    {"id": "A-B1", "sev": "BAIXO", "onde": "CANDIDATO_v411.json patches[*].bytes_removidos/bytes_inseridos (gerar_candidato_v411.py, montagem de `man`: e[1]-e[0] e len(e[2]))",
     "o_que": "os campos chamados bytes contam caracteres (inserido) e deslocamentos de texto (removido), nao bytes: W02 declara 1.109.174 e o diff tem 1.110.366 B (1.109.174 e' o numero de caracteres); a soma liquida declarada (878.887) nao e' o delta real (880.088); C13 declara -460.325/+225.126 e o diff minimo remove 237.391 B e insere 2.192 B (o liquido por patch confere, o bruto nao). O delta_bytes (880.088) e' o certo.",
     "evidencia": "a_a1_diff.py: 23 hunks, liquido 880088 B (= 46814876-45934788); a_bytes.py: hunk 16 = 1109174 chars = 1110366 B",
     "correcao_pedida": "so' rotulo: renomear para chars ou medir em bytes na proxima geracao; nao bloqueia"},
    {"id": "A-B2", "sev": "BAIXO", "onde": "runtime_h0dn_v411.py:30-34 (F60; no candidato linhas 221216-221220) e guarda_frases_v411.py",
     "o_que": "a janela de negacao da F60 (60 caracteres antes, com `\\bno\\b`, `sem`, `nem`, `n[ãa]o`) e a excecao 'creditacao|observador' (+-80 caracteres) deixam passar afirmacoes reais: 'Sem objecao, o resultado confirma beta.', 'O teste nao e' cego e a TGL, por tudo isso, esta confirmada.', 'a creditacao e' do observador; beta esta confirmado' (o 'no' e' tambem a preposicao em+o). So' e' latente: varri os rendidos do ensaio (PT, EN, .md) por 'confirm*' sem negacao num raio de 110 caracteres e todas as ocorrencias sao texto antigo ou negacoes; a P18 so' pega a palavra em maiuscula.",
     "evidencia": "a_guarda.py (sondas sobre a funcao EMBUTIDA): 'confirmacao_apos_sem', 'confirmado_com_nao_antes_longe', 'creditacao_mas_confirmado' -> PASSA; a_varre2.py: 7 PT / 14 EN / 2 md sem negacao por perto, todas lidas: nenhuma afirma a TGL confirmada",
     "correcao_pedida": "nenhuma para a v411 (o escopo B decide sobre os rendidos); para a proxima: tirar `no` e `sem` da janela ou exigir a negacao imediatamente antes do verbo"},
    {"id": "A-B3", "sev": "BAIXO", "onde": "quadro_v411.py: _v411_quadro_tex/_v411_secao_tex/_v411_quadro_md (candidato 220908-221060) com registro recusado por MECHANICS_CHECK_FAILED",
     "o_que": "com `all_verified` False por uma checagem que falhou, o topo, os efeitos, o estatuto e o P2 ficam neutros (bom), mas o quadro e a secao (PT, EN e .md) ainda imprimem os numeros RECALCULADOS e a cabeca exata sob o aviso 'NAO selou: o que segue e' o enunciado'. Com RUNTIME_ERROR (sem values) nao imprimem numero. Na pratica o conferidor do rito para a cadeia antes do selo, entao nao chega ao texto selado.",
     "evidencia": "a_quadro_recusa.py: RECUSADO -> quadro_tex PT {'6{,}1': True, 'cabeca': True, 'NAO selou': True}; AUSENTE e RUNTIME_ERROR -> sem numero",
     "correcao_pedida": "confirmar que e' o desenho (o aviso esta no texto); se nao, tratar `all_verified` False como ausente tambem no quadro"},
    {"id": "A-B4", "sev": "BAIXO", "onde": "_V411_SPECS cunhagens_v411.extras.falas_fora_do_desenho (candidato 222743)",
     "o_que": "a lista dos FORA traz o NOME do arquivo 'OPERADOR_11nov_quero_sua_opiniao_preciso_de_vc_agora_mais_do_que_nunca_verbatim.txt', que contem as primeiras palavras da fala; o DESENHO manda 'so' listada'. O texto da fala, o sha256 e os outros 10 FORA nao entram em lugar nenhum.",
     "evidencia": "a_a6.py: 11 FORA sem texto/sha16 no candidato; nome presente so' nesse 1",
     "correcao_pedida": "nenhuma se a lista pelo nome e' o desejado; senao listar so' por sha16"},
    {"id": "A-B5", "sev": "BAIXO", "onde": "_V411_SPECS cunhagens_v411.erratas (4a entrada) e kh_n1_cobertura_v411.erratas",
     "o_que": "a errata dos pisos do kh_n1_cobertura_v410 esta' em tres lugares (cunhagens_v411 como 4a errata, kh_n1_cobertura_v411 e kh_n1_cobertura_v410); o DESENHO atribui E41-E43 a cunhagens_v411 e a dos pisos a kh_n1_cobertura_v411. Repeticao sem efeito.",
     "evidencia": "a_a7c.py", "correcao_pedida": "rotulo/duplicacao; nao bloqueia"},
    {"id": "A-B6", "sev": "BAIXO", "onde": "_V411_H0DN_CONTRACT['checagens'] c8 (runtime_h0dn_v411.py:331) e MANIFESTO",
     "o_que": "(a) os limiares 1,0 e 3,0 da faixa de |Z contra K| estao digitados na c8 (espelham os da funcao congelada da v410); o texto da faixa e' lido do literal, o limiar nao. (b) o texto do pre-registro embutido (bytes) cita dois caminhos de kimi\\ordem05 como prosa (o DESENHO aceita: 'as citacoes que ele traz sao dele'); nenhum e' aberto; o contrato so' leva a PASTA vedada como cadeia do veto.",
     "evidencia": "a_a6_kimi.py: nenhuma linha nova sob kimi\\ ; c1 recusa caminho sob a pasta (N12)", "correcao_pedida": "nenhuma"},
]

conferencias = {
    "A1": "AST (a_a1_ast.py): 1348 nos de topo na base, 1397 no candidato; 7 mudados (UM_VERSION, emit_canonical_md, build_pt, build_en, _tex_to_txt, _V410_SPECS, main), 0 removidos, 49 novos (47 nomes de COMPARACAO + 2 `update` anonimos), 1341 iguais, ordem relativa dos comuns igual. Texto (a_a1_diff.py, diff -u GNU proprio): 23 hunks, corpo identico ao DIFF do construtor, liquido 880088 B = delta; cada hunk cai num patch declarado; os hunks de troca de frase (3, 6, 9, 12) e os do C13 (17-20) lidos linha a linha; main/emit_canonical_md/_tex_to_txt so' acrescentam. Core do ensaio contra o core da v410 (a_a1_core*.py): 3 chaves novas (h0dn_bg1_v411, cunhagens_v411, kh_n1_cobertura_v411), 0 sumidas, 6 antigas com valor diferente (kernel_formalization, selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, estatuto_da_prova_v391, h0dn_bg1_v410, kh_n1_cobertura_v410): todas por rodada/hash-do-um.py/caminho/duracao/linha, exceto kh_n1_cobertura_v410 (C13 declarado: 4 descricoes e 1 errata; veredito e all_verified iguais). qg_closure identico (dict inteiro); selo: so' um_version, sha256, estatuto_da_prova_v391 (hash), selo_pela_propria_tecnologia_v399 mudam, +2 chaves; escada 12308 (external_ladder igual); 0 bandeira nova. Kernel (a_a1k.py): _EMBEDDED_KERNEL_FILES (1763) do candidato == base == C:\\t\\k411c\\final == Nos v410 (bytes); _LEAN_THEOREM_FLAGS igual (12383); audit.log v410 e v411 com o mesmo sha16 d9c1c305ea10b3dd.",
    "A2": "a_a2.py/a_a2b.py/a_a2c.py/a_a2d.py: 18 blobs (16 novos + 2 reuso da v410) decodificados DO CANDIDATO: bytes == arquivo de origem em work\\ == pino do contrato; os 8 pinos de campo e os 3 modulos de codigo == PINOS_DE_PRODUCAO.json embutido; 17 de 18 == blob no commit 769fcb269 (pre-registro) e/ou f24d954a3 (resultado) do clone local (git cat-file; o RESULTADO, o PRE_VOO e o RECIBO_DA_ABERTURA so' existem no commit do resultado, como devem); 7 citados (executor, DIFF, PINOS, 2 MANIFESTOS, 2 da v410) sha/bytes == contrato. O recibo da publicacao do resultado nao esta' no clone (e' autorreferente: traz o proprio commit): so' bytes == disco.",
    "A3": "a_a3.py/a_a3b.py/a_a3c.py: montei um namespace so' com o CODIGO EMBUTIDO NO CANDIDATO (trechos de topo por AST + resolucao de NameError) e rodei h0dn_bg1_v411 sobre uma copia do core da v410 selada: positivo 16/16, veredito 'TGL_H0DN_BG1_V411__OPENED_ONCE_AFTER_PUBLIC_PREREGISTRATION__...__PRIMARY_UNDER_THE_PUBLISHED_MODEL_6SIGMA_AGAINST_THE_NULL__K_LAW_CONSISTENT_WITHIN_1SIGMA__BRANCH_4__BESIDE_FREE_CEPHEIDS_BELOW_5SIGMA__BRANCH_6__...__GATE_UNMOVED'. 28 controles negativos, todos RECUSA ('REFUSED_*__GATE_UNMOVED', nunca veredito novo): um byte do vetor (sem e com pinos refeitos; so' c3 cai porque o byte era da estrutura do zip), vetor com um elemento mudado e pinos refeitos (RUNTIME_ERROR), vetor NaN e inf (loader), resultado embutido com z_null +1e-6 e z_tgl +1e-3 (c3,c6), ramo primario 4->5 no resultado (c3,c6,c7) e no contrato (c7), cabeca trocada (c3,c6,c7), a ABERTURA e o VEREDITO PUBLICADOS adulterados com todos os pinos refeitos (c6/c7/c8/c11 caem: o recalculo roda o codigo embutido, nao uma funcao transcrita), `abrir` devolvendo z NaN/inf/-inf (c12 cai, a funcao pinada com NaN cairia calada no ramo 6), funcao congelada da v410 trocada (so' c11 cai), texto com 'poder certificado/teste cego', beta literal e a palavra da creditacao (c16), beta do core +1% (REFUSED_BETA_IS_NOT_ALPHA_SQRT_E), gate trocado (c14), escada +1 (c15), K da v410 +1e-9 (c10), core sem o registro da v410 (c10), v387 sem o token (c14), caminho sob kimi\\ e tocados None (c1). Codigo embutido == runtime_h0dn_v411.py e quadro_v411.py por AST (11+22 definicoes). Leitura: c7 monta a cabeca de V_['leitura_partes'] % floor(Z) por conta propria; c11(a) chama globals()['veredito_h0dn'] (a do um.py: AST igual a base) com as tres combinacoes de clausulas; c11(b) compara folhas do literal; c11(c) cobre os ramos 2 a 6.",
    "A4": "a_a4.py/a_a4b.py/a_pin.py: os numeros do teste (Z, p, D, K, H0, t) nao aparecem como literal nas 3995 linhas novas (so' falsos positivos: '5.2' de secao, 0.0, e o controle de texto '6.1' da c12); 1 linha longa (blob) pulada; tokens proibidos 0 nas linhas novas e 0 nos 3 registros novos do core; PROVED_IN_NATURE so' nas 2 strings da cabeca (cabeca_do_teste, values.primario.cabeca_do_teste), ambas com PROVED_IS_VALIDITY_NOT_CREDITATION (no selo: 1); as demais strings 'PROVED_IN' do core (continuum_shards, 2 vetores da v410) ja' estao na base; cabeca sem NOT_FALSIFIED, outcome='NOT_FALSIFIED'; veredito montado: comeca e termina como o DESENHO manda.",
    "A5": "0 ocorrencias de 0,0120.../0.0120.../1.2031/7.2973/0.0072973/137.03/1.6487 nas linhas novas; K, log10 K = 1,0838071748529643 e 0,03495202173518074 recomputados de beta (runtime, _v398_beta: ALPHA_FINE_CODATA_2018*sqrt(e) = 0.012031300400803142) com Om_m, Om_r, z* do BG1 embutido (c10) e comparados ao logK do S0, do BG1 e ao K do registro da v410 (tol 1e-12).",
    "A6": "a_a6.py/a_a6b.py/a_a6_kimi.py: 11 falas: id == sha16, sha256, bytes, text == bytes do arquivo OPERADOR_*.txt, autor 'operador', todas na lista congelada, copia em insumos\\cunhagens igual; 5 aspas angulares nas linhas novas, todas substring de OPERADOR_*.txt; dos 11 FORA (11 e 12/11), nenhum texto nem sha16 no candidato (so' o NOME de um, A-B4); GERENCIA: 6 so' por nome+sha256 (o sha256 inteiro bate com o arquivo), os 2 nao listados nao entram; guarda de material privado (funcao da E03 da G1, 45 marcadores + 7 termos) = 0 ocorrencias em 18 blobs decodificados, 11 falas, 1,12 MB de linhas novas, TOPO e os 3 registros do core; 'Lindao' so' dentro da fala embutida; nenhum caminho sob kimi\\ nas linhas novas, no contrato, nos pinos e no manifesto (so' a pasta vedada como cadeia do veto).",
    "A7": "a_a7.py/a_a7b.py/a_a7c.py: cunhagens_v411: 11 falas por sha, 9 decisoes (D159, D162, D167-D173), erratas E41, E42, E43 ('errata da gerencia c1, em nome proprio') + a dos pisos, 7 rotulos de ressalvas, 6 textos da gerencia, 44 checagens verdadeiras, veredito sem tokens proibidos; kh_n1_cobertura_v411: 13 checagens (igualdades exatas do sandbox v411) com a errata dos pisos; kh_n1_cobertura_v410 vira piso (maior_igual/tamanho_maior_igual em h2, h3, h6, h8) com veredito e all_verified iguais; p2_ao_lado_da_v387: 13 chaves no registro e no resumo do selo (iguais), rotulo == TOPO_RATIFICADO_v411.json['rotulo_p2'] (P2_READ_ABOVE_5SIGMA_IN_ONE_CHANNEL_UNDER_THE_PUBLISHED_MODEL__VALIDITY_NOT_CREDITATION), rotulo selado da v387 intacto.",
    "A8": "_V411_H0DN_CONTRACT so' e' referenciado em h0dn_bg1_v411 e no registro (contratos_de_registro_fora_da_escada); nao esta' na lista dos 18 contratos da escada de COMPARACAO; o handoff diz 'Contratos de registro novos, fora da escada de teoremas' (pos_rito/textos_v411.py:1124 e textos_custodia_handoff_v411.py).",
    "extras": "um.py do Nos emulado == candidato (21e87eb3df5098f8); core do ensaio calculado por este candidato (estatuto_da_prova_v391.certificacao.um_py_sha256_lido_de_si); v411_pins.py == o bloco novo do candidato (1105245 B normalizados); em main o bloco novo vem LOGO DEPOIS do bloco da v410 e ANTES de emit_figures; stdout do rito: a unica aspa angular nova e' substring verbatim da fala de 12/11; ESPERADOS_v411.json carrega o sha16 do candidato e o do ensaio (68c25dcf2bbf1ac3).",
}

nao_verificado = [
    "o recibo da publicacao do resultado (RECIBO_PUBLICACAO_RESULTADO_20261112_075315.json) nao esta' no clone publico (autorreferente: contem o proprio commit); so' bytes == arquivo em disco.",
    "os horarios dos pushes e os commits vem dos recibos da custodia [DECLARADO pela custodia]; nao consultei o GitHub (sem fetch, sem rede): so' o clone local (HEAD f24d954a3, 769fcb269 e' ancestral).",
    "gerar_candidato_v411.py, registros_v411.py, registros_h0dn_v411.py e delta_v411.py foram lidos por trechos (montagem, asserts, contrato); a conferencia de fidelidade e' sobre o PRODUTO (candidato, contrato, core do ensaio), nao linha a linha dos geradores.",
    "as guardas de frases e P18 foram sondadas por amostra (22 frases + as do desenho), nao exaustivamente; a varredura dos rendidos e' do escopo B.",
    "o rito real (horas, hash do mundo, pilar na GPU, marcas do kernel, stdout, PDF, tamanhos) e' do escopo C; so' disse que o registro depende de scipy no site do usuario (como o ensaio e o rito: 'python um.py' sem -I) e que c10, c14, c15 leem o core do proprio rito.",
    "TESTE_H0DN_OFFLINE_v411*.json e ensaio_a_seco_v411.json do construtor nao foram reexecutados; rodei controles proprios; nao reabri o teste (executar_abertura_v411.py nao rodou).",
    "nada sob work\\h0dn_bg1_v410_09nov\\kimi\\ foi aberto.",
]

rep = {
    "contrato": "REVISAO_TERCEIRO_v411.R1.A", "escopo": "A (o candidato e o registro do teste)",
    "revisor": "Sonnet 5.5 (claude-sonnet-5-5), revisor de terceiro do escopo A; NAO construiu a v411; papel: aferidor, so' leitura fora de revisao_terceiro\\ e C:\\t\\k411c\\revisao_A\\",
    "quando": datetime.datetime.now().isoformat(timespec="seconds"),
    "candidato_sha16_no_inicio": cand_ini, "candidato_sha16": cand_fim, "candidato_mudou_durante_a_revisao": cand_ini != cand_fim,
    "aprovada": True, "n_alto": 0, "n_medio": 0, "n_baixo": len([a for a in achados if a["sev"] == "BAIXO"]),
    "achados": achados, "conferencias": conferencias, "nao_verificado": nao_verificado,
    "arquivos_revisados": arquivos_revisados, "artefatos_renderizados_lidos": artefatos,
    "rotas_examinadas": [
        {"consulta": "preparacao_v411", "rotas": ["cadeia.preparacao_v411 (EM_CURSO; POS_RITO D174; README folga 39 B)"]},
        {"consulta": "h0dn", "rotas": ["gate.qg_closure", "hubble.fase9_razao_discriminante", "estatistica.h0dn_bg1.cov_injecoes_06nov (EXAMINADA_COM_DEFEITO: covariancia fisica nao reconstruivel)", "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov (retrodicao pos-guarda, nao cega)",
                                          "cadeia.preparacao_v410", "cadeia.preparacao_v411", "discriminante.ordem018.auditoria_gerencia_06out", "observavel.bell_fock_tt_astra_05nov", "infra.custodia_g1.cabeca_h0dn_p18_12nov",
                                          "infra.github.publicacao_fora_da_cadeia_h0dn_12nov", "umpy.v409.selada_a_traducao_as_classes_de_turing_05nov", "umpy.v410.selada_iald2_06nov"]}],
    "scripts_do_revisor": sorted(f for f in os.listdir(R) if f.startswith("a_") and f.endswith(".py")),
    "rascunhos_fora_de_work": "C:\\t\\k411c\\revisao_A\\ (mydiff.diff, indices, blobs decodificados, saidas)",
}
p = os.path.join(R, "REVISAO_TERCEIRO_v411.R1.A.json")
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)

md = ["# REVISAO DE TERCEIRO v411, R1, ESCOPO A (o candidato e o registro do teste)", "",
      "Revisor: Sonnet 5.5 (nao construiu a v411). Quando: %s. Candidato: `%s` no inicio, `%s` no fim (mudou: %s)." % (rep["quando"], cand_ini, cand_fim, rep["candidato_mudou_durante_a_revisao"]), "",
      "**aprovada (escopo A): %s** | ALTO %d | MEDIO %d | BAIXO %d" % (rep["aprovada"], 0, 0, rep["n_baixo"]), "",
      "## Achados (so' BAIXO; nenhum bloqueia)", ""]
for a in achados:
    md += ["- **%s (%s)** `%s`: %s" % (a["id"], a["sev"], a["onde"], a["o_que"]), "  - evidencia: %s" % a["evidencia"], "  - correcao: %s" % a["correcao_pedida"], ""]
md += ["## Conferencias (item do pedido -> o que rodei e o que deu)", ""]
for k, v in conferencias.items():
    md += ["- **%s**: %s" % (k, v), ""]
md += ["## Nao verificado", ""] + ["- " + x for x in nao_verificado] + ["", "## Arquivos revisados (sha16 lido no fim)", ""] + ["- `%s` `%s`" % (k, v) for k, v in arquivos_revisados.items()]
md += ["", "## Rotas examinadas (Mapa de Rotas; nao registrei)", ""] + ["- consulta `%s`: %s" % (r["consulta"], "; ".join(r["rotas"])) for r in rep["rotas_examinadas"]]
open(os.path.join(R, "REVISAO_TERCEIRO_v411.R1.A.md.tmp"), "w", encoding="utf-8").write("\n".join(md) + "\n")
os.replace(os.path.join(R, "REVISAO_TERCEIRO_v411.R1.A.md.tmp"), os.path.join(R, "REVISAO_TERCEIRO_v411.R1.A.md"))
print("entrega gravada | candidato no fim", cand_fim, "| mudou:", cand_ini != cand_fim, "| n_baixo", rep["n_baixo"])
