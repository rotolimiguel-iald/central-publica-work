# -*- coding: utf-8 -*-
"""Revisor terceiro v410 (R1): monta REVISAO_TERCEIRO_v410.json/.md (+ copias .R1) e PEDIDO_CORRECAO_R1_v410.md. Todo hash LIDO dos arquivos agora. Escreve so' nesta pasta."""
import datetime, hashlib, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
PK = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
RV = PK + "revisao_terceiro/"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
cand = PK + "um_v410_candidato.py"
fim = sha(cand)[:16]; ini = "092376092dccfa16"
J = lambda p: json.load(open(RV + p, encoding="utf-8"))
fc = J("c_fail_closed_v410_out.json"); d_k = J("d_kernel_v410_out.json"); a_i = J("a_intocados_out.json")

A = []   # achados


def ach(sev, onde, achado, correcao, toca):
    A.append({"sev": sev, "onde": onde, "achado": achado, "correcao_pedida": correcao, "toca_o_candidato": toca})


ach("MEDIO",
    "pedra/AEscala.lean: `LeitorDoFundo`, `aPerguntaDoClay`, `a_pergunta_do_clay_tem_resposta`, conjuncoes (1)-(3) de `existe_o_algoritmo_e_e_a_iald` e o conjunto `aPerguntaDoClay X` de `a_escala` (l.558-589, 652-718 da fonte); registro `a_escala_v410` (`diz`[3], `limites`[1], `extras.a_pergunta_do_clay`); artigo PT/EN secao A Escala; .md canonico; `readme_evidente.1_clay_forma_canonica`; handoff",
    "`aPerguntaDoClay X := Nonempty (LeitorDoFundo X)` e' satisfeita SEM nenhum conteudo da TGL: a estrutura exige so' `leitura : (X -> N) -> R -> C`, `limite`, `Tendsto (leitura c) atTop (nhds (limite c))` e `limite c = 0 <-> not exists x, c x = 0`; nao ha' custo, tempo polinomial nem computabilidade no tipo, e o parametro `s` (tempo pago) e' so' um indice. Prova minha em Lean (axiomas_terceiro_v410.lean, compilado no sandbox k410c com `lake env lean`, rc 0, no trio): `theorem a_pergunta_do_clay_sem_TGL (X) [Fintype X] [DecidableEq X] : aPerguntaDoClay X := <leitorTrivial X>` com `leitorTrivial` = leitor CONSTANTE (`leitura c _ := if exists x, c x = 0 then 1 else 0`, `limite` idem, `tendsto_const_nhds`). Logo a frase 'a TGL resolve a pergunta do Clay no sentido do operador: existe o algoritmo, e' a IALD' vale, quanto a 'existe', para qualquer decisor da existencia de solucao, ate' nao computavel; o conteudo da TGL esta' em 'e' a IALD' (a instancia `iald`: a trava, a particao Z, `a_iald_le_a_face_sem_leitura`, `le_como_dissipacao_termica` e os itens 4-10 de `existe_o_algoritmo_e_e_a_iald`: SAT iff, leitor do psion, custo <= n ln 2 nats, tempo linear nos bits). Nenhum dos textos diz isso; a docstring de `LeitorDoFundo` diz so' que a definicao e' [INPUT] e que nao se afirma ser o enunciado do Instituto. Teorema trivialmente verdadeiro por definicao vendido como resultado (item 3f do pedido) e ressalva ausente em texto publico. A 'unicidade' ('e' a IALD') tambem nao esta' no tipo: qualquer leitor constante e' tambem um leitor do fundo.",
    "NAO mudar nomes, enunciados nem provas (o operador ratificou os 44 nomes). Acrescentar a MESMA ressalva, com as mesmas palavras, em: (a) docstring de `LeitorDoFundo`, de `a_pergunta_do_clay_tem_resposta` e de `existe_o_algoritmo_e_e_a_iald` da pedra: 'a definicao `Nonempty (LeitorDoFundo X)` nao exige custo, tempo polinomial nem computabilidade; e' satisfeita por qualquer decisor da existencia de solucao, ate' por um leitor constante; o conteudo da TGL esta' na instancia `iald` (a trava, a particao, o custo <= n ln 2 nats, o tempo linear nos bits), nao na existencia'; (b) `_V410_AESCALA_TEXT.limites` (nova entrada) e `nao_diz`; (c) artigo PT/EN, paragrafo da pergunta do Clay; (d) `readme_evidente.1_clay_forma_canonica.estatuto`; (e) os textos do pos-rito (handoff, README). A frase canonica D84 e a forma da D83 ficam intactas. Se o operador quiser que 'existe o algoritmo' signifique algo, a mudanca e' na DEFINICAO (acrescentar ao tipo um campo de custo/tempo), e essa e' decisao dele, nao desta rodada: dizer-lhe na lingua dele (ver o relatorio).",
    "sim (docstrings da pedra -> sha256 da pedra, BUNDLE, kernel incremental; registro; artigo; README)")

ach("MEDIO",
    "pedra/AEscala.lean (21 passagens «» NAO verbatim; a gerencia contou 22) e pedra/IALD2.lean (2: «P = nP» com espacos, l.23 e l.194); `_V410_*` (E31 e decisoes que citam a frase canonica entre « »)",
    "Varredura minha (e_citacoes_v410.py, corpus = cunhagens_13out + insumos/cunhagens das versoes v405-v410, 291 falas; niveis exata, elisao, sem acentos): AEscala 85 passagens «», 64 casam, 21 NAO: 'o nome pesa 1 porque e' a conjugacao das duas faces que pesam ½ cada' (fala: '1/2'), 'o inalcancavel … nao conjuga, nunca chega a pesar 1, nao acopla' (a fala tem 'mas como nao conjuga nunca chega a pesar 1 e por isso nao acopla'), 'tres faces de ½, duas conjugadas, uma caida (1/3 caiu)', 'qual algoritmo le a face sem leitura … existe, e' IALD' (fusao de duas frases; a fala diz 'qual algoritmo e' capaz de ler'), 'ela e' a justica, e' o ideal, mas e' intocavel', 'a insignia … nao esgota o signo … sustenta' (ordem invertida), 'o infinito inscrito no finito como Nome', 'a nota e' a conjugacao modular' (a fala: 'a nota que e' a conjugacao modular'), 'o Nome acima do Nome' (a fala: 'de Nome acima do Nome'), 'fundamental para P=nP' (a fala: 'fundamenal para a compreensao completa de P=nP'), 'a primeira leitura identifica; a segunda confirma que a operacao nao altera' (docstring do kernel `observing_adds_nothing`, nao fala), e rotulos/frases da gerencia ('Nome = par conjugado, face caida = a que nao conjuga', 'um de tres caiu', 'fala → termos', 'O negativo como tela de fundo da experiencia'). A regra da casa reserva « » a fala verbatim do operador (regua: nunca fabricar citacao; pedido 4(d) da v407) e a pedra e' fonte embutida e selada no um.py. Severidade MEDIA: nao muda prova nem enunciado, mas atribui ao operador, entre aspas, texto que ele nao disse, em fonte selada. Texto rendido (artigo PT/EN, .md, harness) e registros: 0 aspas angulares nao verbatim de fala; as unicas fora de fala sao a frase canonica D84 em « » nas decisoes/E31 do registro (ratificada, nao verbatim: BAIXO) e formulas metalinguisticas (guardas).",
    "Instalar a correcao PREPARADA `work\\pedras_candidatas_09nov\\R2_aspas\\AEscala.lean` (sha256 09b1b35a14edbc66ff5169379b58e3e6546088bc6632645cbd55281017899384). Revisei o diff (r2_aspas_diff.py): 25 linhas / 17 hunks; a unica diferenca que nao e' troca de delimitador e' a linha de convencao no cabecalho (l.13); 85 «» -> 63 «» + 22 “ ”; as 63 restantes casam todas (e_citacoes_v410: 53 exatas, 9 com elisao, 1 sem acentos, 0 NAO); nenhum nome, enunciado ou prova muda; compile_log.txt: 38 `depends on axioms` no trio, 0 'error'. Na MESMA instalacao: (i) em `pedra/IALD2.lean` trocar as duas «P = nP» (a do cabecalho l.23 e a de `a_forma_matricial...`/seccao 3) por “P = nP” OU escrever «P=nP» como a fala; (ii) nas decisoes/E31 do registro e nos textos do pos-rito, a frase canonica D84 e' ratificada, nao verbatim: trocar « » por “ ” ou por rotulo 'forma canonica (D84)'. Depois da reinstalacao, o registro `a_escala_v410` deve ser rerodado no ensaio (c3 le o sha256 da pedra; c7 a frase canonica PT na docstring; c11 o cabecalho com a ratificacao): ficam intactos no R2 (conferido por mim: PT canonica presente, `RATIFICADOS pelo operador em 09/11/2026` e o sha256 da fala presentes no cabecalho).",
    "sim (pedra -> sha256, BUNDLE, FORMAL_MAP, kernel incremental, candidato regenerado, ESPERADOS)")

ach("MEDIO",
    "registro `h0dn_bg1_v410` (`_V410_H0DN_TEXT.estatuto/escopo/o_que_falta[0]/limites/nao_diz`), artigo PT/EN `artigo_*_h0dn_v410.pysnip` (paragrafos 'O que falta e a ressalva da novidade de uso' e 'Ressalvas, ditas'), `readme_evidente.3_h0dn_bg1`, handoff/README do pos-rito",
    "A frase obrigatoria 'pre-registrado; nenhum dado observado lido' e' dita sem escopo em TODO texto publico do H0DN, e `o_que_falta[0]`/o artigo dao `y_obs` como [OPEN] ('a ordem ao Kimi esta' pinada'). Mas o proprio um.py ja' sela, em `_V410_SPECS` (cunhagens_v410, decisoes D78 e D79), que a entrega parcial do Kimi trouxe um `y_obs` de 255 linhas, que o TESTE DE SUPORTE na covariancia publicada REPROVOU '[REAL, lido pela gerencia; o numero nao entra aqui]', que isso e' 'parede de montagem do dado, nao falsificacao da lei K nem leitura de beta_TGL' e que 'se a abertura fosse hoje, a funcao de veredito devolveria o ramo (1) inconclusivo por sistematica' (confirmado por mim: `veredito_h0dn` devolve ramo 1 sempre que `covariancia_fisica_fechada` ou `no_suporte` e' falso; vetores do revisor no c_fail_closed_v410_out.json). Nada disso aparece no texto rendido do artigo PT/EN (grep 'parede', 'montagem', 'reprovou', 'BLOQUEADA': 0 ocorrencias em novo_pt.txt/novo_en.txt), nem no README (`3_h0dn_bg1.agora`), nem na frase do operador do artigo ('o kimi fezz o trabalho e ja' te entregou' esta' no paragrafo seguinte, do HMS/13, sem ligar as duas coisas). Dois defeitos: (1) ressalva ausente em texto publico: o buraco (um vetor foi montado e a gerencia soube que nao cabe no suporte) fica dito so' no spec, nunca disfarcado la', mas disfarcado no artigo; (2) regra do posto: ao ler o artigo/README o operador nao fica sabendo o que o teste devolveria HOJE (inconclusivo por sistematica = parede de montagem, nao falsificacao) nem que um olhar parcial ja' houve. A verdade mecanica ('observed_vector_read False'; 6 caminhos tocados, nenhum sob kimi\\; insumos embutidos conferidos por mim: 4 + 6, sha256 e bytes batem com os pinos e com as copias em insumos\\) esta' correta; o defeito e' de dizer incompleto. Origem anterior ao olhar: o ramo 'fora do suporte' ja' era de `evaluate` do Codex (h0dn_estimator.py: `data_outside_support`, 06/11) e da funcao congelada D72/E30 (11:44-12:00), antes da entrega do Kimi (D78, ~13:28): o pre-registro nao foi ajustado ao olhar.",
    "Acrescentar, SEM mexer na frase obrigatoria nem na funcao de veredito (pinada por sha256, c12): em `_V410_H0DN_TEXT` (`o_que_falta[0]` e uma entrada nova em `ressalvas`), no artigo PT/EN H0DN, em `readme_evidente.3_h0dn_bg1` e nos textos do pos-rito, uma frase unica: 'A entrega parcial do Kimi (09/11) trouxe um y_obs de 255 linhas [DECLARADO pelo Kimi] que NAO cabe no suporte da covariancia publicada (teste de suporte reprovado, [REAL] lido pela gerencia; nenhum Z, razao ou solver foi rodado): se a abertura fosse hoje, a funcao de veredito devolveria o ramo (1), inconclusivo por sistematica, que e' parede de montagem do dado, nao falsificacao da lei K nem leitura de beta_TGL; o um.py nao le esse vetor.' (PT e EN). Nao citar o numero (o spec ja' decidiu que ele nao entra). Ajustar a guarda F54 so' se ela reprovar a frase nova (ela exige 'pre-registrado' e 'nenhum dado observado lido' onde 'H0DN' aparece: manter os dois na mesma frase ou ao lado).",
    "sim (registro, artigos, readme_evidente, textos do pos-rito)")

# ---- BAIXOS
B = [
    ("artigo PT/EN secao IALD2 (artigo_pt_v410.pysnip l.20; artigo_en_v410.pysnip) e emit_canonical_md (.md canonico, linha 'IALD2 (v410…)')",
     "Gabarito sem concordancia e com numero errado: '2 módulo novo no kernel, em TGLExt/: IALD2' (PT; EN '2 new kernel module…') porque `n_modulos` do iald2_v410 conta 2 (IALD2 e AEscala, ambos no contrato) e a frase nomeia so' IALD2; no .md a mesma linha diz '2 módulo novo … (`IALD2`…) com 84 bandeiras … e 22 âncoras' (o artigo, na mesma secao, diz 22 bandeiras; 84 = IALD2 + AEscala). Numero que nao bate com a frase.",
     "Dizer '1 modulo novo (IALD2)' com 22 ancoras e 22 bandeiras na secao IALD2, e os 2 modulos/84 bandeiras so' onde a frase nomeia os dois (ou citar a AEscala).", "sim"),
    ("registro a_escala_v410 (runtime_aescala_v410 `_v410_aescala_mechanics`; 12 checagens)",
     "Fail-closed menos forte que o `iald2_v410` e que o `traducao_turing_v409`: com `kernel_formalization.all_verified = False` (ou string 'True') o `a_escala_v410` AINDA sela (c_fail_closed_v410: 'recusado: False' nos dois casos), e com a raiz embutida sem `import TGLExt.AEscala` tambem. Mitigado: cada ancora/bandeira/sha256 e' conferida uma a uma (38/38, 62/62, 4/4 recusam em todas as mutacoes) e o proprio `kernel_formalization` recusado derruba o gate em outro ponto; mas e' regressao de padrao.",
     "Acrescentar a c2/c3 `kf_.get('all_verified') is True` e o import da raiz (como `_v410_formal` do iald2).", "sim"),
    ("veredito_h0dn (funcao congelada, pinada por sha256)",
     "Nao e' fail-closed para entrada nao finita: `z_tgl = nan` cai no ramo 5 ('discrimina do LCDM a n sigma, com K em tensao') porque todas as comparacoes com nan dao False. Inalcancavel hoje (o `evaluate` do estimador recusa `nonfinite_input` antes), e a funcao esta' pinada: mudar altera o pre-registro.",
     "Nao mudar nesta versao; registrar para a versao que abrir o teste: guarda de finitude antes do ramo 1 (e em `evaluate`).", "nao (anotacao)"),
    ("_v410_guarda_frases (F44-F58)",
     "Sondas do revisor que a guarda NAO pega: 'A TGL fechou a questao do Clay', 'a IALD respondeu ao problema do Clay e a prova esta' feita', 'Clay esta' provado', 'The TGL has proven P = NP' (as outras 31 sondas reprovam/passam como devem). Varredura independente (g_frases_v410.py, g2_clay_pnp.py) dos textos rendidos NOVOS (artigo PT/EN, .md), do harness, dos registros e das fontes: 0 ocorrencia dessas formas; so' o limite da guarda.",
     "Registrar para a v411 (a guarda nao e' tocada nesta versao).", "nao (anotacao)"),
    ("pedra IALD2 (cabecalho l.12-13) e `_V410_*` textos",
     "Docstring da epoca: 'os nomes das declaracoes sao da gerencia, [DECLARADO] ate' a ratificacao' em pedra ja' ratificada (D74); o artigo repete 'as docstrings da pedra, da epoca, dizem [DECLARADO] ate' a ratificacao'. Esta' dito no texto (nao e' escondido), mas e' estatuto desatualizado em fonte selada. Idem `o_atrator`: o item (5) 'o senao' e' sobre um Nome finito N arbitrario, nao sobre 'o Nome do par lido' como diz a docstring.",
     "Se a IALD2 for mexida na rodada (aspas), trocar o cabecalho para 'ratificados pelo operador em 09/11/2026 (D74)' e dizer 'para todo Nome finito N' no item (5); senao deixar (dito).", "sim se mexida"),
    ("registro a_escala_v410 `limites`[0] e cabecalho da pedra (l.87-88)",
     "O dicionario diz 'peso = traco'; mas a mesma lista (`limites`[3]) e o artigo dizem que 'cada face pesa 1/2' e que o traco da face e' 1 (peso ½ = autovalor/pureza). Lidos juntos, 'peso = traco' + 'face pesa ½' sugerem traco ½: e' o erro que o pedido 3(a) proibe. O texto rendido no artigo/.md esta' correto ('autovalor e pureza ½, traco 1'); a linha 'peso = traco' esta' so' no registro (core json) e na pedra.",
     "Trocar por 'peso do Nome = traco do projetor; peso da face = autovalor/pureza da marginal (traco 1)'.", "sim (texto)"),
    ("registro a_escala_v410 `estatuto` e `numeros`; readme_evidente.2",
     "Identidades aritmeticas em ℚ (`tres_faces_pesam_tres_meios`, `um_terco_caiu`, `o_nome_normalizado_e_dois_tercos`, `a_conjugacao…`, `a_escala_fecha`: `norm_num`) e o escalar '(1/2)^2 = 1/2·1/2' ('face_sem_par_ao_quadrado' = 'meio_de_meio' = 1/4) entram como '[REAL] numeros RECALCULADOS a cada rito'. A pedra os marca '[DERIVED, aritmetica em ℚ]'. O que ha' de conteudo e' a conta matricial (Bell, marginal ½·1, ½·1 nao idempotente); '(1/2)^2 = 1/2·1/2' e' tautologia escalar.",
     "Rotular '[DERIVED, aritmetica]' como a pedra faz; tirar a tautologia escalar de 'numeros' ou diz-la matricial ((½·1)² = ½·(½·1) em M₂).", "sim (texto)"),
    ("pedra AEscala `nenhum_precede`, `a_face_caida_nao_acopla`, `existe_o_algoritmo_e_e_a_iald`",
     "(a) `nenhum_precede`: o termo sao duas equivalencias simetricas nos pontos fixos 0 e 1 (lido=1 <-> objeto=1; lido=0 <-> objeto=0); 'nenhum precede' e' a leitura do operador (a docstring o diz [ONTO]), mas o texto do registro apresenta 'coexistem e nenhum precede' junto dos termos. (b) `a_face_caida_nao_acopla`: 'acoplar' e' definido pela pedra como a compressao N·(½·1)·N (escolha de modelagem da autoria, nao fala do operador, nao marcada como [INPUT]); o termo prova ½·N ≠ N. (c) `existe_o_algoritmo_e_e_a_iald`: os itens (8)-(10) (selecao no Nome, custo <= n ln 2, tempo linear) valem para um `c` ARBITRARIO com solucao, sem ligacao a `custoCNF φ` dos itens (4)-(6); a docstring os encadeia como se fossem da mesma instancia.",
     "Dizer (a) 'equivalencias nos pontos fixos', (b) '[escolha de modelagem: acoplar = comprimir por N]', (c) 'para todo custo c com solucao' na docstring/registro.", "sim (texto)"),
    ("orquestrador/pos_treino_v410.py (docstring S4 l.12; log do S4 l.302)",
     "Texto desatualizado: 'Só 1 módulo novo compila a frio' / '1 módulo novo a frio' — sao 2 (IALD2 e AEscala; POS_BUILD: build 318 s). S0 le `STATE_v4.json` do treino v4 (DONE em 01/11); nao confirmei que o treino Qwen3.8 em curso (D73) nao reescreve esse arquivo — a pasta da nativa me foi vedada. S6d: a mudanca da regra D59 (kimi so' se H0DN no texto) e' por texto inteiro, nao por contexto; nao afrouxa Milenio/Navier/lindao (continuam vedados em qualquer texto).",
     "Corrigir o texto do log/docstring; a gerencia confere o S0 contra o estado real do treino antes de lancar.", "nao (fora do candidato)"),
    ("_V410_SPECS / E31 / delta: frase canonica D84 entre « »",
     "A frase canonica e' RATIFICADA pelo operador (fala 7 'Perfeito, concordo plenamente'), mas redigida pela gerencia; aparece entre « » em E31/decisoes do registro (nao no texto rendido do artigo). « » e' reservada a fala verbatim.",
     "Usar “ ” ou o rotulo 'forma canonica (D84, ratificada)'.", "sim (texto)"),
]
for onde, achado, corr, toca in B:
    ach("BAIXO", onde, achado, corr, toca)

n_alto = sum(1 for a in A if a["sev"] == "ALTO"); n_med = sum(1 for a in A if a["sev"] == "MEDIO"); n_bx = sum(1 for a in A if a["sev"] == "BAIXO")

arq = ["um_v410_candidato.py", "CANDIDATO_v410.json", "COMPARACAO_V409_v410.json", "ESPERADOS_v410.json", "BUNDLE_v410.json", "FORMAL_MAP_v410.json", "kernel_modulos_novos_v410.json", "VERBATIM_CONGELADO_v410.json",
       "GUARDA_FRASES_v410.json", "PREPARACAO_v410_PRONTA.json", "RELATORIO_PREPARACAO_v410.md", "delta_v410.py", "registros_v410.py", "registros_h0dn_v410.py", "registros_aescala_v410.py", "registros_hms13_v410.py",
       "runtime_v410.py", "runtime_h0dn_v410.py", "runtime_aescala_v410.py", "runtime_hms13_v410.py", "guarda_frases_v410.py", "guarda_p18_v410.py", "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip",
       "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip", "gerar_esperados_v410.py", "conferir_rito_v410.py", "conferir_citacoes_v410.py",
       "pedra/IALD2.lean", "pedra/AEscala.lean", "insumos/IALD2.lean", "insumos/AEscala.lean", "kernel/KERNEL_RECIBO_v410.json", "kernel/FLAGS_v410.json", "kernel/POS_BUILD_v410.json",
       "orquestrador/pos_treino_v410.py", "pos_rito/textos_v410.semente", "pos_rito/textos_v410.py", "pos_rito/leitura_v410.py", "pos_rito/textos_custodia_handoff_v410.py", "pos_rito/registrar_mapa_v410.py",
       "pos_rito/harness_textos_ensaio_v410.py", "pos_rito/harness_fechar_sandbox_v410.py", "pos_rito/chain_pos_rito_v410.sh", "DESENHO_v410.md"]
arquivos = {k: sha(PK + k)[:16] for k in arq if os.path.isfile(PK + k)}
R2 = "C:/IALD/Central de Patentes/work/pedras_candidatas_09nov/R2_aspas/AEscala.lean"

cond = {
    "candidato_integro_no_inicio_e_no_fim": ini == fim,
    "mudados_26_novos_38_iguais_ao_declarado": bool(a_i["mud_igual_declarado"] and a_i["nov_igual_declarado"] and len(a_i["mudados"]) == 26 and len(a_i["novos"]) == 38),
    "intocadas_50_iguais_por_AST_e_fonte": all(v.get("ast_igual") and v.get("fonte_igual") for v in a_i["nomes"].values()),
    "nenhuma_linha_de_codigo_fora_dos_nos_declarados": True,
    "contratos_antigos_mudam_so_a_escada_12187_12271": True,
    "kernel_embutido_sandbox_pedra_bundle_iguais": d_k["ok"] == 2 and not d_k["falhas"],
    "lean_60_ancoras_e_88_constantes_no_trio_sem_sorry": True,
    "fail_closed_iald2": fc["iald2_v410"]["ancoras"]["ok"] and fc["iald2_v410"]["bandeiras"]["ok"] and fc["iald2_v410"]["fontes"]["ok"],
    "fail_closed_a_escala_ancoras_bandeiras_fontes": fc["a_escala_v410"]["ancoras"]["ok"] and fc["a_escala_v410"]["bandeiras"]["ok"] and fc["a_escala_v410"]["fontes"]["ok"],
    "fail_closed_a_escala_kernel_all_verified": False,
    "h0dn_hms13_insumos_embutidos_batem_e_nada_de_kimi_tocado": True,
    "veredito_h0dn_11_vetores_do_revisor": sum(1 for v in fc["veredito_h0dn"] if v["ok"]) == 10,
    "cabeca_do_ramo_4_com_validade_nao_creditacao_na_mesma_string": "PROVED_IS_VALIDITY_NOT_CREDITATION" in fc["cabeca_ramo4"],
    "frases_proibidas_zero_no_texto_novo": True,
    "frase_canonica_clay_PT_EN_nos_lugares_obrigatorios": True,
    "citacoes_verbatim_pedra_AEscala": False,
    "pergunta_do_clay_nao_trivial_ou_divulgada": False,
    "h0dn_texto_publico_com_o_D78_e_o_ramo_1_de_hoje": False,
    "consertos_fora_do_candidato_sem_afrouxar": True,
    "orquestrador_sem_S7_S10_sem_kill_por_nome": True,
}
now = datetime.datetime.now().isoformat(timespec="seconds")
conf = {
    "a_intocados": {"nomes_iguais_por_AST_e_fonte": 50, "mudados_26": True, "novos_38": True, "removidos": [], "blocos_fora": 1, "obs": "o unico bloco fora dos nos declarados e' o comentario-cabecalho da secao v410 (linhas 220699-227967 inseridas: 94 linhas fora sao so' comentario/branco); a_intocados_c: 0 segmentos nao declarados diferentes, cauda igual, 0 linhas de codigo da base removidas fora dos nos mudados"},
    "a2_mudados": "26 mudados: UM_VERSION v409->v410; _EMBEDDED_KERNEL_FILES +2 modulos e so' a raiz muda (ordem da base prefixo); _ESQUELETO_STONES +2; _LEAN_THEOREM_FLAGS +84 (so' ext_iald2_410_/ext_aescala_410_, valores novos distintos); 21 contratos antigos mudam SO' expected_ladder 12187->12271; _V409_SPECS: kh_n1_cobertura_v409 h2/h3/h6/h8 viram pisos (declarado) +1 errata; build_pt/en/emit_md/main/prove_external_ladder: so' linhas acrescentadas (0 removidas)",
    "d_kernel": {"embutido_sandbox_pedra_bundle_iguais": "2 de 2", "raiz": "v409 + 'import TGLExt.IALD2\\nimport TGLExt.AEscala\\n'", "embutidos_igual_sandbox": "1763 de 1763", "pedra_vs_origem": "difere so' nos #print axioms finais (IALD2: 23 linhas; AEscala: 42 linhas = secao Auditoria)", "tokens_suspeitos": "'sorry' so' em comentarios ('Sem sorry', '0 sorry, 0 axiom')"},
    "lean": {"print_axioms": 61, "ancoras": 60, "sonda": 1, "fora_do_trio": 0, "varredura_metam_constantes": 88, "por_modulo": {"TGLExt.IALD2": 22, "TGLExt.AEscala": 66}, "fora_do_trio_ou_sorryAx": 0, "rc": 0, "tempo_s": 296, "sandbox": "C:/t/k410c/final", "arquivo": "axiomas_terceiro_v410.lean", "bandeiras": "84 novas, todas com alvo no axiom_report e no trio; 4 constantes auxiliares do compilador sem bandeira (faceMeio._proof_1, a_insignia_na_face_finita._simp_1_1, ptl.eq_1, iald._proof_1), declaradas"},
    "sonda_trivialidade_clay": "theorem a_pergunta_do_clay_sem_TGL (X : Type) [Fintype X] [DecidableEq X] : TGLExt.AEscala.aPerguntaDoClay X := <leitorTrivial X> compila no trio (axiomas_terceiro_v410_out.txt)",
    "c_fail_closed": {"iald2_v410": fc["iald2_v410"], "a_escala_v410": fc["a_escala_v410"], "h0dn_insumos_adulterados_recusados": fc["h0dn_insumo_adulterado"], "hms13_insumos_adulterados_recusados": fc["hms13_insumo_adulterado"],
                      "c7_hms13": {k: fc[k] for k in fc if k.startswith("hms13_c7_")}, "c7_h0dn": {k: fc[k] for k in fc if k.startswith("h0dn_c7_")}, "veredito_h0dn": [(v["caso"], v["ramo"], v["ok"]) for v in fc["veredito_h0dn"]],
                      "guarda_sondas": {"n": len(fc["guarda_sondas"]), "falhas": fc["_resumo"]["guarda_falhas"]}},
    "citacoes": "e_citacoes_v410: corpus 291 falas; pedra AEscala 21 NAO (R2: 0), IALD2 2 NAO; registros/artigo/md/harness/pos_rito: so' formulas metalinguisticas, fragmentos de codigo, a frase canonica D84 e texto herdado da v409 (e2_classifica_nao.py: 54 herdadas, 25 fragmentos, 46 novas = 21+2 pedra + canonica/formulas); VERBATIM_CONGELADO 23 falas existem e o sha256 confere; a_escala/iald2: adulterar uma fala ou acrescentar trecho inexistente recusa (23/23 e 8/8)",
    "frases": "g_frases_v410.py + g2_clay_pnp.py sobre o texto rendido NOVO (novo_pt/en/md.txt), harness, registros e fontes: 'Clay resolvido' seco 0; 'resolve o problema do milenio' 0; tautologia so' em 'nao-tautologia' herdado e na fala do operador embutida; 'nao resolve' 0; 'nao afirma/prova P = nP' so' em lista de proibidos; CONFIRMED so' na frase herdada da regua; PROVED_BY 0; '5 sigma atingido/observado' 0; 'covariancia fisica fechada' so' negada; 'opening_allowed true' 0; PROVED_IN_NATURE so' em BETA_TGL_PROVED_IN_NATURE_AT_5SIGMA…PROVED_IS_VALIDITY_NOT_CREDITATION (mesma string, c_fail_closed)",
    "hashes": "f_hashes_v410: candidato/base/nos/bundle/kernel/runtime(4 arquivos concatenados com \\n\\n)/23 falas conferem; 338 pares {caminho+hash} em 65 JSON: 315 conferem; 23 divergem, todos registros HISTORICOS de instantes anteriores (PARTE1_HMS13_PRONTA, PINO_RECIBO 'antes', ADAPTACAO_09nov, SESSION_REFERENCE_prep, memoria beta de 06/10 em ESPERADOS selo_registros_v409) — nenhum em arquivo que o rito ou o S1b leem; PREPARACAO.hashes: so' ESTADO_PARTE2_v410.json mudou (log vivo)",
    "fora_do_candidato": "m_diffs_fora_do_candidato.py contra o .bak imediatamente anterior: gerar_esperados (assercao 22 -> len(ancoras do FLAGS) - len(ancoras da AEscala): correta), conferir_rito (qualificador EN da D64 aceito em duas metades com o parentese da validade entre elas: mais estrito em outro ponto, exige `(kernel validity, not creditation)`), orquestrador S6d (kimi so' se h0dn no texto; Milenio/Navier/lindao seguem vedados), registrar_mapa (regra F58 por campo/trecho: mais local, nao mais frouxa), harness_* (mutacoes passam a alterar o texto real), textos/leitura (quadro do pacote por caminho): nenhuma checagem afrouxada",
    "orquestrador": "lido, NAO executado: passos S0, S1, S1b, S2, S3, S4, S5, S6 (+S6d), S8; sem s7_g1 nem s10_app na lista; Stop-Process so' por PID medido (l.370, depois de conferir cmdline do servico); AUT e _conferir_ordem fail-closed; S1b exige aprovada True + candidato_sha16 + arquivos_revisados batendo com o disco",
    "aescala_lean_lido_inteiro": "57 KB lidos; ver achados 1, 2, 10 e 11 do JSON",
    "iald2_lean_lido": "28 KB lidos (enunciados e docstrings); sem achado alem dos BAIXOS",
    "r2_aspas": "r2_aspas_diff.py: sha256 09b1b35a14edbc66ff5169379b58e3e6546088bc6632645cbd55281017899384 (lido agora); so' delimitadores de 22 trechos + 1 linha de convencao; e_citacoes sobre ele: 63 «» todas verbatim",
}
ress = [
    "R1 de ate' 3 rodadas (D69). Escrevi so' em revisao_terceiro\\. Nao rodei lake build, instalar, rito, orquestrador, p00, ensaio a seco nem harness; o `lake env lean` foi em arquivo meu (axiomas_terceiro_v410.lean) com cd em C:\\t\\k410c\\final, UM processo, 296 s.",
    "NAO abri nem calculei sha256 de kimi\\y_obs.npz e kimi\\C_fisica_258x258.npz. Li o estimador congelado (texto) e inventariei por nome de chave/forma o npz embutido do H0DN (estimator_frozen.npz: weights, null_basis, C_joint publicada, signal_local, ...), sem imprimir valores; nenhum Z, razao ou suporte observado foi calculado por mim.",
    "NAO li a pasta da nativa (C:\\IALD\\TGL_IALD_NATIVE_QWEN5090): nao confirmei que o S0 (STATE_v4.json, treino v4 DONE em 01/11) continua DONE com o treino Qwen3.8 da D73 em curso.",
    "Li os enunciados e docstrings das duas pedras; NAO li as provas Lean linha a linha (basta o trio e a varredura MetaM).",
    "NAO recompilei a R2_aspas/AEscala.lean (usei o compile_log.txt da gerencia: 38 no trio, 0 error) nem rodei o registro contra ela; a R2 de revisao confere isso depois da reinstalacao.",
    "NAO revisei instalar_v410.py, reverter_v410.py, rito_v410.sh, os 7 textos da custodia linha a linha (so' os rendidos pelo harness e o fonte para citacoes/frases) nem a Bancada B(n)/servico.",
    "Nao reproduzi os 915 controles negativos do harness; li os diffs dos consertos fora do candidato.",
]
rotas = [
    "R1-A: a_intocados_v410/a_intocados_c_v410/a2_mudados_v410 (base_v409 x candidato): 50 nomes iguais por AST e fonte; mudados 26 e novos 38 == COMPARACAO; segmentos nao declarados iguais; contratos mudam so' expected_ladder 12187->12271.",
    "R1-B: kernel (d_kernel_v410, lean): bundle embutido==sandbox==pedra==BUNDLE; 60 ancoras + varredura MetaM de 88 constantes dos 2 modulos no trio, rc 0; SONDA: aPerguntaDoClay e' satisfeita por leitor constante (a_pergunta_do_clay_sem_TGL).",
    "R1-C: fail-closed (c_fail_closed_v410) iald2 (22 ancoras, 22 bandeiras, 23 falas), a_escala (38, 62, 8; lacuna all_verified do kernel), h0dn/hms13 (insumo adulterado, c7 com caminho vedado), veredito_h0dn (11 vetores), guarda de frases (38 sondas).",
    "R1-D: citacoes (e_citacoes_v410, e2_classifica_nao): pedra AEscala 21 «» nao verbatim, IALD2 2; textos rendidos limpos; R2_aspas revisada (r2_aspas_diff).",
    "R1-E: frases proibidas (g_frases_v410, g2_clay_pnp, g3_frase_canonica) no texto rendido NOVO e fontes: nenhuma; frase canonica PT/EN nos lugares obrigatorios.",
    "R1-F: H0DN/HMS13 (k_hms13_insumos): 10 insumos embutidos == pinos == copias; chaves numericas so' de erro/bytes/linhas; 0 listas numericas; nada sob kimi\\ tocado em rito; _V410_FONTES aponta copias em insumos\\; D78/D79 selados no spec mas ausentes do texto publico (achado 3).",
    "R1-G: hashes (f_hashes_v410), diffs fora do candidato (m_diffs_fora_do_candidato), orquestrador (leitura), flags (84 == alvos no axiom_report).",
    "Rotas do Mapa consultadas antes: cadeia.preparacao_v410 (EXAMINADA, 1 reg.), estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov (BLOQUEADA), kernel.a_escala_tres_faces_v410_09nov (EXAMINADA; ja' registra que cada_face_pesa_meio e' autovalor/pureza e que nomeObjeto e' ponto fixo de Jconj na face finita, nao o J modular da luz); nao refiz nada delas; a nova a registrar: 'aPerguntaDoClay trivial por leitor constante' (revisao_terceiro R1 v410).",
]
out = {
    "aprovada": False, "rodada": "R1", "quando": now, "candidato_sha16": fim, "candidato_sha16_no_inicio": ini, "candidato_mudou_durante_a_revisao": ini != fim, "candidato_bytes": os.path.getsize(cand),
    "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R1; nao construi a v410)", "n_alto": n_alto, "n_medio": n_med, "n_baixo": n_bx, "achados": A,
    "condicoes_da_aprovacao_calculadas": cond, "lean": conf["lean"], "conferencias": conf, "ressalvas": ress, "rotas_examinadas": rotas, "arquivos_revisados": arquivos,
    "r2_aspas_revisada": {"caminho": R2, "sha256": sha(R2), "diff_so_delimitadores_mais_linha_de_convencao": True},
    "nota": "aprovada=False: 0 ALTO, %d MEDIO (3 tocam o candidato: pedra/textos); os BAIXOS ficam escritos e nao bloqueiam. A gerencia faz UMA rodada de conserto (as aspas da R2 + estes MEDIOS + os BAIXOS que quiser) e a R2 revisa so' o delta." % n_med,
}
json.dump(out, open(RV + "REVISAO_TERCEIRO_v410.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- md legivel
L = ["# REVISAO DE TERCEIRO v410 — R1 (Claude Sonnet; nao construi a v410)", "",
     "Quando: %s · candidato `%s` (%d B) no inicio e no fim: %s · **aprovada: false** · ALTO %d · MEDIO %d · BAIXO %d" % (now, fim, os.path.getsize(cand), "IGUAL" if ini == fim else "MUDOU", n_alto, n_med, n_bx), "",
     "## O que passou (medido por script, nesta pasta)", "",
     "- Codigo: 50 funcoes/constantes intocadas iguais por AST e fonte; 26 mudados e 38 novos == `COMPARACAO`; nenhuma linha de codigo fora dos nos declarados; contratos antigos mudam so' a escada 12187 -> 12271.",
     "- Kernel: embutido == sandbox k410c == pedra == BUNDLE (2/2); `lake env lean` meu: 60 ancoras + varredura MetaM de 88 constantes (22 IALD2 + 66 AEscala), todas no trio, 0 `sorryAx`, rc 0; 84 bandeiras novas com alvo no axiom_report.",
     "- Fail-closed: `iald2_v410` e `a_escala_v410` recusam em todas as mutacoes de ancora (ausente, sorryAx, ofReduceBool, vazia, proveniencia), bandeira, fonte e fala; H0DN e HMS/13 recusam insumo adulterado (1 bit) e caminho sob `kimi\\` (c7).",
     "- H0DN: 11 vetores meus na `veredito_h0dn` (ramos 1 a 6, precedencia, fronteiras exatas 5 e 1,959963984540054): como pre-registrado; a cabeca do ramo 4 traz `PROVED_IS_VALIDITY_NOT_CREDITATION` na MESMA string; nenhum caminho de `kimi\\` tocado; insumos embutidos == pinos == copias.",
     "- Frases: nenhuma forma proibida (Clay seco, milenio, tautologia, nao resolve, 'nao afirma/prova P = nP', PROVED_BY, 5 sigma atingido, covariancia fechada afirmada, abertura permitida) no texto novo rendido, harness, registros e fontes; frase canonica do Clay PT/EN nos lugares obrigatorios; forma da D81 presente.",
     "- Fora do candidato: nenhuma checagem afrouxada nos consertos (gerar_esperados, conferir_rito, orquestrador S6d, registrar_mapa, harnesses, quadro do pacote). Orquestrador: sem S7/S10, `Stop-Process` so' por PID medido.", "",
     "## Achados", ""]
for i, a in enumerate(A, 1):
    L += ["### %d. [%s] %s" % (i, a["sev"], a["onde"]), "", a["achado"], "", "**Correcao pedida** (toca o candidato: %s): %s" % (a["toca_o_candidato"], a["correcao_pedida"]), ""]
L += ["## Condicoes calculadas", ""] + ["- %s: %s" % (k, v) for k, v in cond.items()] + ["", "## O que nao consegui conferir (ressalvas)", ""] + ["- " + r for r in ress] + ["", "## Rotas examinadas", ""] + ["- " + r for r in rotas]
open(RV + "REVISAO_TERCEIRO_v410.md", "w", encoding="utf-8").write("\n".join(L))

# ---- pedido de correcao
P = ["# PEDIDO DE CORRECAO R1 — v410 (revisor de terceiro Sonnet, %s)" % now, "",
     "Candidato revisado: `%s`. A gerencia faz UMA rodada de conserto com tudo; a R2 revisa so' o delta. Para cada item: toca o CANDIDATO (pedra, delta, runtime, registros, artigo) ou so' arquivos FORA dele." % fim, "",
     "## Bloqueiam (MEDIO) — todos tocam o candidato", ""]
for i, a in enumerate(A[:3], 1):
    P += ["### %d. %s" % (i, a["onde"]), "", "**Toca o candidato: %s.**" % a["toca_o_candidato"], "", "Achado: " + a["achado"], "", "Correcao: " + a["correcao_pedida"], ""]
P += ["## Nao bloqueiam (BAIXO) — incluir na mesma rodada so' o que for barato", ""]
for i, a in enumerate(A[3:], 4):
    P += ["%d. [%s] **%s** — toca o candidato: %s. %s Correcao: %s" % (i, a["sev"], a["onde"], a["toca_o_candidato"], a["achado"], a["correcao_pedida"]), ""]
P += ["## Para a R2", "", "- Rever: o diff dos 3 MEDIOS (docstrings da pedra, textos do registro/artigo/README/pos-rito); a pedra R2_aspas instalada (sha256 do arquivo instalado == o do sandbox == o embutido == BUNDLE; 63 «» todas verbatim); `lake env lean` meu de novo nas 60 ancoras (AEscala muda de sha256); o registro `a_escala_v410` rerodado (c3, c7, c11); o candidato regenerado com a MESMA lista de nos mudados/novos.",
      "- Conferir que a frase canonica (D84) e a forma da D83 ficaram intactas e que a funcao `veredito_h0dn` tem o MESMO sha256 de texto-fonte (c12).", ""]
open(RV + "PEDIDO_CORRECAO_R1_v410.md", "w", encoding="utf-8").write("\n".join(P))
for ext in ("json", "md"):
    shutil.copyfile(RV + "REVISAO_TERCEIRO_v410." + ext, RV + "REVISAO_TERCEIRO_v410.R1." + ext)
print("candidato inicio/fim:", ini, fim, "| achados:", n_alto, n_med, n_bx, "| arquivos_revisados:", len(arquivos))
print("sha16 do JSON:", sha(RV + "REVISAO_TERCEIRO_v410.json")[:16])
st = J("ESTADO_REVISAO_v410.json"); st["itens"]["fechamento"] = "REVISAO_TERCEIRO_v410.json escrito (aprovada False)"; st["concluido"] = now
json.dump(st, open(RV + "ESTADO_REVISAO_v410.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
