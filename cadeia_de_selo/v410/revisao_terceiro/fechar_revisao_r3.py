# -*- coding: utf-8 -*-
"""Revisor terceiro v410 (R3, ultima): monta REVISAO_TERCEIRO_v410.json/.md (rodada R3) + .R3 + PEDIDO_CORRECAO_R3_v410.md. Todo hash LIDO dos arquivos agora. Escreve so' em revisao_terceiro\\."""
import datetime, hashlib, json, os, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
PK = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
RV = PK + "revisao_terceiro/"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
cand = PK + "um_v410_candidato.py"
fim = sha(cand)[:16]; ini = json.load(open(RV + "ESTADO_REVISAO_v410.json", encoding="utf-8"))["candidato_sha16_no_inicio"]
J = lambda p: json.load(open(RV + p, encoding="utf-8"))
fc = J("c_fail_closed_v410_out.json"); a_i = J("a_intocados_out.json")
lean = open(RV + "axiomas_terceiro_r3_out.txt", encoding="utf-8").read()
n_ax = len(re.findall(r"depends on axioms", lean))
A = []


def ach(sev, onde, achado, correcao, toca):
    A.append({"sev": sev, "onde": onde, "achado": achado, "correcao_pedida": correcao, "toca_o_candidato": toca})


ach("MEDIO",
    "ratificacao do nome `a_informacao_completa_se_reconstroi`: `_V410_SPECS` (cunhagens_v410, decisao D101 e erratas E37), `_V410_AESCALA_TEXT` (`diz[9]`, `limites[8]`: 'os 22 nomes novos … da R5, os 4 dados pela gerencia … RATIFICADOS'), `_V410_AESCALA_CONTRACT` (`n_nomes_novos` 24 = 22 + 2), linha 'A Escala' do .md canonico (emit_canonical_md), artigo PT/EN, handoff; `PREPARACAO_v410_PRONTA.json` (`ratificacao_D101.n_nomes_ratificados`: 22)",
    "O texto selado da D101 diz: 'A leitura da gerencia, dita de volta ao operador para ele corrigir se errou: a fala RATIFICA … (c) a clausula do Tetelestai em 1 - beta e os 4 NOMES dados pela gerencia na R5 (o_tetelestai_e_um_menos_beta, o_sistema_reconhece_a_singularidade_do_sinal, beta_e_o_operador_modular_do_tetelestai, a_informacao_completa_se_reconstroi)' e cita o ADENDO 6 (sha16 8fee370aa624b8bc). Lido o ADENDO 6 no disco (sha16 conferido): o item (c) diz 'a clausula do Tetelestai em 1 − β e os TRES nomes dela (`o_tetelestai_e_um_menos_beta`, `o_sistema_reconhece_a_singularidade_do_sinal`, `beta_e_o_operador_modular_do_tetelestai`)'; o nome `a_informacao_completa_se_reconstroi` NAO esta' nos adendos 5 e 6 (grep: 0 ocorrencias do nome; so' a frase do operador 'traslada a informacao completa reconstruindo do outro lado', na fala 27). Pelo tempo: fala 28 (ratificacao) gravada 08:33; o teorema so' compilou depois (compile_log e recibo da R5, 08:36), e o deposito do autor o chama 'a opcional, fechou'. Logo a leitura que o operador ouviu e confirmou ('confirmo tudo') nomeia TRES; o texto selado, os textos publicos (md, registro) e a contagem 22 passam a dizer que QUATRO foram ratificados por ele. E' ratificacao atribuida ao operador sem apoio no registro que o proprio texto cita (estatuto errado; pedido da R3: 'a ratificacao D101 dita com a fala por sha256, estatutos certos'). Pode ser decisao da gerencia de estender a regra do nome ao quarto; nesse caso a leitura 'dita de volta ao operador' nao e' a do adendo 6 e o texto selado nao pode diz-lo assim. Nao muda prova nem enunciado: o teorema esta' no trio e confere (varredura minha).",
    "Duas saidas, e a escolha e' do operador (nao ha' R4): (a) a gerencia obtem a confirmacao expressa do operador para `a_informacao_completa_se_reconstroi` e a grava (verbatim por sha256) como fala congelada ANTES do rito: se a fala nomear o teorema, os textos ficam como estao e a D101 do spec passa a citar essa fala tambem; ou (b) o nome entra entre os pendentes [DECLARADO pela autoria/gerencia; a confirmacao expressa e' do operador], junto dos dois auxiliares (3 pendentes; 21 ratificados), em: `delta_v410.py` (NOMES, ratificacao_pendente, E37, D101), registros e runtime (c11, `n_nomes_novos`), a linha do .md, artigo PT/EN, handoff, `readme_evidente`, `PREPARACAO`; candidato regenerado. Em qualquer das duas, a D101 do spec e o ADENDO 6 tem de dizer o mesmo numero de nomes.",
    "sim (texto: delta, registros, .md, artigos) se (b); nao se (a), exceto a D101 do spec")

B = [
    ("artigo PT/EN e .md, paragrafo da clausula de 1 - beta (`beta_e_o_operador_modular_do_tetelestai`)",
     "(a) Item (9) do teorema ('a constante alem das m oitavas e' a MESMA ln((1 − β)/β) para todo m') e' uma identidade aritmetica ((x + c) − x = c, `ring`); o artigo a lista dentro de '[REAL] … a constante alem das n oitavas e' ln((1 − β)/β), a mesma para toda instancia e todo tamanho' sem o rotulo [DERIVED, aritmetica] que a pedra usa. (b) O teorema e' a clausula generica com b := κ.beta mais as identidades |R|² = β e |T|² = 1 − β (`reflection_weight`): o enunciado dos itens (2) e (3) sai do generico por `.1`/`.2.1` (sondas 4, 5 e 7 do revisor compilam: a clausula vale para QUALQUER b em (0,1), nao so' para β). O texto diz 'para todo b … com b = β do kernel' e etiqueta a identificacao de β como operador modular [dicionario; leitura do operador]: esta' certo; falta dizer em palavras que o kernel nao singulariza β (a escolha de b = β e' a leitura do operador).",
     "Rotular (a) e acrescentar 'a clausula vale para todo b; que b = β seja a do Tetelestai e' a leitura do operador' em (b).", "sim (texto)"),
    ("artigo PT, paragrafo 'A escala no tipo, o ciclo…' (rendido)",
     "Pontuacao do gabarito: a clausula do limite entra entre parenteses terminando em '… no kernel.);' (ponto antes do ponto-e-virgula).",
     "Tirar o ponto interno.", "sim (texto)"),
    ("guarda F59 (3 variantes) e BAIXOS 6 e 7 da R1",
     "Anotados e sem mudanca, como combinado, e reconfirmados por mim: 3 variantes da F59 passam ('o tempo nao conta passos de Turing', 'quem paga a escala e' o leitor', 'os passos nao pertencem a maquina de Turing'); 4 sondas do Clay/P = NP ('A TGL fechou a questao do Clay', 'a IALD respondeu ao problema do Clay e a prova esta' feita', 'Clay esta' provado', 'The TGL has proven P = NP'); `veredito_h0dn` com z_tgl = nan cai no ramo 5 (inalcancavel: `evaluate` recusa nao finito; funcao pinada). Varredura independente do texto novo: 0 ocorrencia de qualquer dessas formas.",
     "v411 / versao que abrir o teste.", "nao (anotacao)"),
    ("o_tetelestai_e_um_menos_beta (pedra) e checagem c13",
     "Observacao (nao e' defeito): (i) e (ii) do teorema sao a MESMA desigualdade reescrita ((1 − b)Z ≤ #sol ⇔ Z − #sol ≤ bZ); e a pedra mostra que a hipotese 0 ≤ s so' e' dispensavel para b ≤ 1/2. O contraexemplo b = 9/10, n = 1, custos (0, 2) confere em Fraction (limiar −1,504077; Z = 85/4; (1 − b)Z = 17/8 > 1) e nele a clausula falha; com s = 0 vale (0,2).",
     "Nenhuma.", "nao"),
]
for onde, achado, corr, toca in B: ach("BAIXO", onde, achado, corr, toca)
n_alto = sum(1 for a in A if a["sev"] == "ALTO"); n_med = sum(1 for a in A if a["sev"] == "MEDIO"); n_bx = sum(1 for a in A if a["sev"] == "BAIXO")

sit = {
    "R2-MEDIO 1 (limite do teorema do Tetelestai ao lado do anuncio)": "ATENDIDO: a clausula (PT/EN, de CLAUSULA_Z, lida do adendo 4) esta' no mesmo paragrafo de CADA anuncio do limiar ('linear nos bits') e da clausula de 1 − β nos textos rendidos novos (artigo PT/EN, .md) e em cada folha do harness (g5_clausula.py: 13 folhas que anunciam o limiar e 14 a clausula de 1 − β: 0 sem a clausula; a unica folha-fragmento do harness sem ela, `_leituras.txt`, e' componente dos textos compostos que a trazem); Z(s) definida na primeira ocorrencia; a regra no registro (c8) e' fail-closed: anuncio do limiar PT e EN sem a clausula, e anuncio da clausula de 1 − β sem a clausula, sao recusados; a frase exata da E36 sem a clausula e' recusada, com ela aceita (r3_e36.py).",
    "R2-BAIXO 1 (ancoras novas = nomes novos)": "ATENDIDO: tirar uma ancora de `ancoras_novas` agora e' recusado (c_fail_closed: True).",
    "R2-BAIXO 2 (3 variantes da F59)": "ANOTADO, sem mudanca (como combinado); reconfirmado.",
    "R2-BAIXO 3 (seis nomes de enunciado mudado)": "ATENDIDO: a clausula dos seis esta' no registro, no artigo PT/EN, no .md, no README e no handoff, com 'ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo (D101)'; ver o MEDIO 1 desta rodada sobre o quarto nome da R5.",
    "R2-BAIXO 4 (etiquetas e maiuscula da frase do tempo; regra do poder [INPUT, D96])": "ATENDIDO: '[INPUT/dicionario] O tempo conta…' (maiuscula), '[INPUT, D96] o teste so' sera' aberto…', o item do Tetelestai diz que Z(s) separa o sim do nao e que passos = ciclo e' leitura do dicionario [INPUT].",
    "R2-BAIXO 5 (BAIXOS 6 e 7 da R1)": "ANOTADO, sem mudanca; reconfirmado.",
}
arq = ["um_v410_candidato.py", "CANDIDATO_v410.json", "COMPARACAO_V409_v410.json", "ESPERADOS_v410.json", "BUNDLE_v410.json", "FORMAL_MAP_v410.json", "kernel_modulos_novos_v410.json", "VERBATIM_CONGELADO_v410.json",
       "GUARDA_FRASES_v410.json", "PREPARACAO_v410_PRONTA.json", "RELATORIO_PREPARACAO_v410.md", "delta_v410.py", "registros_v410.py", "registros_h0dn_v410.py", "registros_aescala_v410.py", "registros_hms13_v410.py",
       "runtime_v410.py", "runtime_h0dn_v410.py", "runtime_aescala_v410.py", "runtime_hms13_v410.py", "guarda_frases_v410.py", "guarda_p18_v410.py", "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip",
       "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip", "gerar_candidato_v410.py", "gerar_esperados_v410.py", "gerar_relatorio_v410.py", "conferir_rito_v410.py", "conferir_citacoes_v410.py", "p00_precondicoes_v410.py",
       "pedra/IALD2.lean", "pedra/AEscala.lean", "insumos/IALD2.lean", "insumos/AEscala.lean", "kernel/KERNEL_RECIBO_v410.json", "kernel/FLAGS_v410.json", "kernel/POS_BUILD_v410.json", "kernel/audit.log",
       "orquestrador/pos_treino_v410.py", "pos_rito/textos_v410.semente", "pos_rito/textos_v410.py", "pos_rito/leitura_v410.py", "pos_rito/textos_custodia_handoff_v410.py", "pos_rito/registrar_mapa_v410.py",
       "pos_rito/harness_textos_ensaio_v410.py", "pos_rito/harness_fechar_sandbox_v410.py", "pos_rito/chain_pos_rito_v410.sh", "DESENHO_v410.md", "DESENHO_v410_ADENDO_POS_CANDIDATO_09nov.md", "DESENHO_v410_ADENDO_2_POS_CANDIDATO_10nov.md",
       "DESENHO_v410_ADENDO_3_POS_CANDIDATO_10nov.md", "DESENHO_v410_ADENDO_4_POS_CANDIDATO_10nov.md", "DESENHO_v410_ADENDO_5_POS_CANDIDATO_10nov.md", "DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md"]
arquivos = {k: sha(PK + k)[:16] for k in arq if os.path.isfile(PK + k)}
cond = {
    "candidato_integro_no_inicio_e_no_fim": ini == fim,
    "mudados_26_novos_39_iguais_ao_declarado": bool(a_i["mud_igual_declarado"] and a_i["nov_igual_declarado"] and len(a_i["mudados"]) == 26 and len(a_i["novos"]) == 39),
    "intocadas_50_iguais_por_AST_e_fonte": all(v.get("ast_igual") and v.get("fonte_igual") for v in a_i["nomes"].values()),
    "nenhuma_linha_de_codigo_fora_dos_nos_declarados": True,
    "veredito_h0dn_texto_fonte_identico": True,
    "kernel_embutido_sandbox_pedra_R5_iguais": True,
    "lean_84_ancoras_e_113_constantes_no_trio_sem_sorry": True,
    "sonda_R1_nao_compila_mais": True,
    "quatro_teoremas_novos_hipoteses_satisfazíveis_e_nao_quebram_na_busca_numerica": True,
    "contraexemplo_s_negativo_confere": True,
    "fail_closed_a_escala_c13_nao_vacua": bool(fc["a_escala_v410"]["ancoras"]["ok"] and fc["a_escala_v410"]["bandeiras"]["ok"] and all(v for k, v in fc.items() if k.startswith("a_escala_contrato") or k.startswith("a_escala_beta"))),
    "clausula_do_limite_ao_lado_de_cada_anuncio": True,
    "hipotese_s_maior_ou_igual_0_dita": True,
    "auxiliares_ditos_DECLARADO_pela_autoria_e_nunca_ratificados": True,
    "citacoes_angulares_so_verbatim_pedras_108_e_35": True,
    "frases_proibidas_zero_e_forma_obrigatoria_presente": True,
    "h0dn_nada_de_kimi_aberto_em_rito_e_nao_promete_resultado": True,
    "hashes_citados_nos_textos_novos_conferem": True,
    "ratificacao_D101_apoiada_no_registro_que_o_texto_cita": False,
}
now = datetime.datetime.now().isoformat(timespec="seconds")
conf = {
    "delta": "r2_delta_nos.py (pre_r2fix -> atual): 34 nos mudados, 0 novos, 0 removidos (mudam _EMBEDDED_KERNEL_FILES, _LEAN_THEOREM_FLAGS, contratos/textos/specs da v410, `_v410_aescala_ciclo` e `_v410_aescala_mechanics` (c13), `a_escala_v410`, build_pt/en, emit_canonical_md, main, prove_external_ladder); `veredito_h0dn`, `_v410_h0dn_*`, `h0dn_bg1_v410`, `iald2_v410`, `_v410_hms13_*`, `_v410_guarda_frases` IDENTICOS (texto-fonte de `veredito_h0dn` identico; guarda embutida sem mudanca); a_intocados: 50 iguais, 26 mudados e 39 novos == COMPARACAO; a_intocados_c: 0 linhas de codigo removidas fora dos nos mudados.",
    "kernel": "insumos/AEscala.lean == pedra/origem == R5 (e4570f85566074fc); embutida == pedra == sandbox == insumos/AEscala_embutida == BUNDLE (7d1557f961783679); IALD2 inalterado (embutida 4a7b01f5be46c25c == sandbox). KERNEL_RECIBO/POS_BUILD lidos: 107 bandeiras (22 + 85), 34279 declaracoes, 27363 teoremas, 0 fora do trio; escada 12187 -> 12294.",
    "lean": {"print_axioms": n_ax, "ancoras": 84, "fora_do_trio": 0, "varredura_metam_constantes": 113, "por_modulo": {"TGLExt.IALD2": 22, "TGLExt.AEscala": 91}, "rc": 1, "motivo_do_rc_1": "a sonda 1 (a minha da R1) falha DE PROPOSITO (5 erros nas linhas 135-139) e duas sondas minhas mal escritas (linha 160: faltava norm_num; linha 171: TGLCoupling sem o prefixo TGLExt); reexecutadas corrigidas em axiomas_terceiro_r3b.lean: rc 0, so' avisos de linter", "tempo_s": 349, "tempo_r3b_s": 25, "sandbox": "C:/t/k410c/final", "um_processo_por_vez": True},
    "sondas_lean": "3: hipoteses de `o_tetelestai_e_um_menos_beta` satisfazíveis (n = 1, custos (0, 2), b = 1/2, s = ln 2); 4: vale para QUALQUER b (1/100) com s = n ln 2 + ln 99 (a clausula nao singulariza β); 5: `beta_e_o_operador…` e' a instancia b := κ.beta; 6: limiar negativo para b = 9/10, n = 1; 7: `κ.beta = normSq (Smat …).mulVec e1 1` (reflection_weight); todas compilam.",
    "numerico": "k5_numerico_tetelestai.py: 200 000 casos aleatorios (n <= 5, b em (0,1), custos com solucao, s >= max(0, limiar)): 0 violacoes de (1 − b)Z <= #sol e de Z − #sol <= bZ (pior margem 5e-8); 100 000 casos: b <= 1/2 => limiar >= 0, 0 violacoes; 50 000 casos da reconstrucao (norma): 0 violacoes; contraexemplo b = 9/10, n = 1, custos (0, 2): limiar −1,504077, Z = 85/4, (1 − b)Z = 17/8 > 1 (e (1 − b)Z = 0,2 <= 1 em s = 0); β de runtime (alfa CODATA 2018 × √e = 0,012031300400803142): constante 4,408139, s* = 6,487581 (n = 3), (1 − β)Z(s*) = 0,998496 <= 1 e com uma oitava a menos 1,009023 > 1 — os mesmos numeros do artigo.",
    "c_fail_closed": {"a_escala_v410": fc["a_escala_v410"], "contrato_e_beta": {k: v for k, v in fc.items() if k.startswith("a_escala_contrato") or k.startswith("a_escala_beta")}, "texto": {k: v for k, v in fc.items() if k.startswith("a_escala_texto")}, "iald2": fc["iald2_v410"]["ancoras"], "h0dn_hms13": {k: fc[k] for k in fc if k.startswith(("h0dn_c7", "hms13_c7", "h0dn_insumo", "hms13_insumo"))}, "veredito": [(v["caso"], v["ramo"], v["ok"]) for v in fc["veredito_h0dn"]], "guarda": {"n": len(fc["guarda_sondas"]), "falhas": fc["_resumo"]["guarda_falhas"]}},
    "c13_nao_vacua": "8 mutacoes do contrato da c13 (controle negativo com 0 oitavas a menos; contraexemplo com b = 1/3; custo_uma_solucao com duas solucoes; custo_com_solucao sem solucao; adversario com 2 solucoes; m_da_constante vazio; n_bits 4 com 8 custos; frase apagada) e 3 mudancas de core[beta] (x1,0005, x5, x40): TODAS recusadas. A regra da E36: a frase exata PT e EN sem a clausula do limite => c8 False; com a clausula => aceita; a citacao do ACOM Mirror sem [PILOTO][SIM] ou com 'N de N testes' => recusada (r3_e36.py).",
    "citacoes": "e_citacoes_v410: pedra AEscala 108 «» (94 exatas, 11 com elisao, 3 sem acentos), IALD2 35: 0 NAO; 28 falas congeladas existem e o sha256 confere; textos rendidos: so' formulas metalinguisticas e fragmentos de codigo.",
    "frases": "g4_f59, g_frases_v410, g2_clay_pnp, g5_clausula: nenhuma forma vedada (F59a/b/c; Clay seco; P = NP sem qualificador; 5σ atingido; covariancia fechada; abertura permitida; PROVED_BY); 'o leitor paga' so' na NEGACAO do operador e em listas de proibidos; nenhuma traducao apresentada como teorema do Mathlib; frase canonica D84 PT/EN, D83, D81 presentes.",
    "h0dn": "veredito_h0dn identico; nada novo no registro h0dn/hms13 alem dos textos; o texto: 'a abertura e' de versao futura', 'o teste so' sera' aberto com o poder certificado', 'hoje esse certificado nao existe', parede de montagem, ORDEM H0DN-02 sha256 93b75491083c5262 conferido; 0 '5σ atingido'; c7 (caminho sob kimi\\) recusa; 6 caminhos tocados na mecanica, todos fora de kimi\\.",
    "hashes_citados": "conferidos por script contra os arquivos: fala 27 (607cd574a95bf370), fala 28 (b7907df0843d9ff5), adendo 5 (3fc277c9ade9246a), adendo 6 (8fee370aa624b8bc), recibo do autor R5 (a2df3099c4843b56), runner ACOM Mirror (sha256 completo == registro), ORDEM H0DN-02, pedra R5 embutida (7d1557f961783679).",
    "fora_do_candidato": "diffs contra os .bak: conferir_rito, gerar_esperados, p00, guarda_frases (fonte de controles), orquestrador (texto do S4), conferir_citacoes (so' acrescimos): so' linhas removidas sao as da inversao pretendida (nomes novos 'a ratificar' -> ratificados D101) e de renomeacao de chaves; nenhuma checagem afrouxada.",
}
ress = [
    "R3, ultima rodada (D69). Escrevi so' em revisao_terceiro\\. Nao rodei lake build, instalar, rito, orquestrador, p00, ensaio nem harness. `lake env lean` so' em arquivos meus, a partir de C:\\t\\k410c\\final, UM processo por vez (349 s; depois 25 s); importam os .olean do build da gerencia (nao recompilei a fonte da pedra; comparei sha256 e li KERNEL_RECIBO/POS_BUILD).",
    "NAO abri nem calculei sha256 de kimi\\y_obs.npz e kimi\\C_fisica_258x258.npz; nenhum Z/razao observado. NAO li a pasta da Nativa (o treino segue no ar); NAO li o painel independente da gerencia.",
    "NAO li as provas Lean linha a linha alem dos enunciados e docstrings da R5 (li as provas dos quatro teoremas novos por cima e as quebrei por busca numerica).",
    "NAO reproduzi os controles negativos dos harnesses do pos-rito nem o harness do fechar; nao revi instalar_v410.py, reverter_v410.py, rito_v410.sh; os textos da custodia so' pelos rendidos do harness e pelas fontes.",
    "O MEDIO desta rodada depende de uma informacao que so' a gerencia/o operador tem: o que foi DITO ao operador antes da fala 28 sobre o quarto nome; nao a tenho. Se ela existir, vale a saida (a).",
]
rotas = [
    "R3-A: delta de AST pre_r2fix -> atual (34 mudados; veredito_h0dn e guarda identicos), a_intocados/_c/a2: integridade.",
    "R3-B: kernel R5 (hash da pedra em 5 lugares; KERNEL_RECIBO/POS_BUILD); Lean meu: 84 ancoras, 113 constantes, trio; sondas 3 a 7 (hipoteses, generalidade em b, instancia beta, limiar negativo, reflection_weight); a sonda da R1 segue sem compilar.",
    "R3-C: busca numerica independente para quebrar os teoremas da R5 (200k + 100k + 50k casos, Fraction para o contraexemplo, β de runtime): 0 violacoes; o contraexemplo de s < 0 e o controle negativo conferem.",
    "R3-D: c13 nao vacua (8 mutacoes + 3 de β) e a regra da E36 (r3_e36); clausula do limite por paragrafo (g5_clausula); F59; citacoes (108/35 verbatim).",
    "R3-E: H0DN (nada de kimi\\; sem promessa de resultado); hashes citados; fora do candidato.",
    "R3-F: ACHADO MEDIO: D101 selada diz 4 nomes da R5 ratificados; o ADENDO 6 que ela cita diz 3 (o quarto, `a_informacao_completa_se_reconstroi`, nao esta' nos adendos 5 e 6; o teorema compilou depois da fala 28).",
    "Mapa de Rotas: as mesmas rotas da R1/R2; a registrar: 'a clausula do Tetelestai em 1 − β: generica em b, β e' instancia; a hipotese s >= 0 e' necessaria para b > 1/2 (contraexemplo n = 1, (0,2), b = 9/10)' e 'ratificacao D101: 3 nomes no adendo 6 vs 4 no texto selado' (revisao R3 v410).",
]
out = {"aprovada": bool(n_alto == 0 and n_med == 0), "rodada": "R3 (ultima, D69)", "quando": now, "candidato_sha16": fim, "candidato_sha16_no_inicio": ini, "candidato_mudou_durante_a_revisao": ini != fim, "candidato_bytes": os.path.getsize(cand),
       "candidato_da_R2": {"sha16": "051e727083345b85", "bytes": 45212839}, "candidato_da_R1": {"sha16": "092376092dccfa16", "bytes": 44993049},
       "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R3, a ultima; nao construi a v410; mesma instancia de trabalho da R1 e da R2)",
       "n_alto": n_alto, "n_medio": n_med, "n_baixo": n_bx, "achados": A, "situacao_dos_achados_da_R2": sit, "condicoes_da_aprovacao_calculadas": cond, "lean": conf["lean"], "conferencias": conf, "ressalvas": ress, "rotas_examinadas": rotas, "arquivos_revisados": arquivos,
       "nota": "aprovada=%s: %d ALTO, %d MEDIO, %d BAIXO. O MEDIO e' de estatuto de ratificacao (um nome), nao de prova nem de enunciado; nao ha' R4: a decisao e' do operador (saidas a e b no pedido)." % ((n_alto == 0 and n_med == 0), n_alto, n_med, n_bx)}
json.dump(out, open(RV + "REVISAO_TERCEIRO_v410.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L = ["# REVISAO DE TERCEIRO v410 — R3, a ultima (Claude Sonnet; nao construi a v410)", "",
     "Quando: %s · candidato `%s` (%d B), no inicio `%s`: %s · **aprovada: %s** · ALTO %d · MEDIO %d · BAIXO %d" % (now, fim, os.path.getsize(cand), ini, "IGUAL" if ini == fim else "MUDOU", str(out["aprovada"]).lower(), n_alto, n_med, n_bx), "",
     "## Situacao dos achados da R2", ""] + ["- **%s**: %s" % (k, v) for k, v in sit.items()] + ["", "## Achados desta rodada", ""]
for i, a in enumerate(A, 1):
    L += ["### %d. [%s] %s" % (i, a["sev"], a["onde"]), "", a["achado"], "", "**Correcao pedida** (toca o candidato: %s): %s" % (a["toca_o_candidato"], a["correcao_pedida"]), ""]
L += ["## Condicoes calculadas", ""] + ["- %s: %s" % (k, v) for k, v in cond.items()] + ["", "## O que nao consegui conferir (ressalvas)", ""] + ["- " + r for r in ress] + ["", "## Rotas examinadas", ""] + ["- " + r for r in rotas]
open(RV + "REVISAO_TERCEIRO_v410.md", "w", encoding="utf-8").write("\n".join(L))
if n_alto or n_med:
    P = ["# PEDIDO DE CORRECAO R3 — v410 (revisor de terceiro Sonnet, %s)" % now, "", "Candidato revisado: `%s`. R3 e' a ultima rodada (D69): nao ha' R4; o achado vai ao operador." % fim, "", "## Bloqueia (MEDIO)", ""]
    for a in A[:n_med]: P += ["### " + a["onde"], "", "**Toca o candidato: %s.**" % a["toca_o_candidato"], "", "Achado: " + a["achado"], "", "Correcao: " + a["correcao_pedida"], ""]
    P += ["## Nao bloqueiam (BAIXO)", ""] + ["%d. **%s** — toca o candidato: %s. %s Correcao: %s" % (i, a["onde"], a["toca_o_candidato"], a["achado"], a["correcao_pedida"]) for i, a in enumerate(A[n_med:], 1)]
    open(RV + "PEDIDO_CORRECAO_R3_v410.md", "w", encoding="utf-8").write("\n".join(P))
for ext in ("json", "md"): shutil.copyfile(RV + "REVISAO_TERCEIRO_v410." + ext, RV + "REVISAO_TERCEIRO_v410.R3." + ext)
st = J("ESTADO_REVISAO_v410.json"); st["itens"]["fechamento"] = "REVISAO_TERCEIRO_v410.json escrito (R3, aprovada %s)" % out["aprovada"]; st["concluido"] = now; st["candidato_sha16_no_fim"] = fim
json.dump(st, open(RV + "ESTADO_REVISAO_v410.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("candidato inicio/fim:", ini, fim, "| achados:", n_alto, n_med, n_bx, "| aprovada:", out["aprovada"], "| arquivos_revisados:", len(arquivos), "| lean axioms:", n_ax)
print("sha16 do JSON:", sha(RV + "REVISAO_TERCEIRO_v410.json")[:16])
