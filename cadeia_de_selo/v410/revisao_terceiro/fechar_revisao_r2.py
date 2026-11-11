# -*- coding: utf-8 -*-
"""Revisor terceiro v410 (R2): monta REVISAO_TERCEIRO_v410.json/.md (rodada R2) + .R2 + PEDIDO_CORRECAO_R2_v410.md. Todo hash LIDO dos arquivos agora. Escreve so' em revisao_terceiro\\."""
import datetime, hashlib, json, os, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
PK = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
RV = PK + "revisao_terceiro/"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
cand = PK + "um_v410_candidato.py"
fim = sha(cand)[:16]; ini = json.load(open(RV + "ESTADO_REVISAO_v410.json", encoding="utf-8"))["candidato_sha16_no_inicio"]
J = lambda p: json.load(open(RV + p, encoding="utf-8"))
fc = J("c_fail_closed_v410_out.json"); a_i = J("a_intocados_out.json"); dl = J("r2_delta_nos_out.json")
lean = open(RV + "axiomas_terceiro_r2_out.txt", encoding="utf-8").read()
n_ax = len(re.findall(r"depends on axioms", lean))

A = []


def ach(sev, onde, achado, correcao, toca):
    A.append({"sev": sev, "onde": onde, "achado": achado, "correcao_pedida": correcao, "toca_o_candidato": toca})


ach("MEDIO",
    "artigo PT/EN (artigo_pt_aescala_v410.pysnip, artigo_en_aescala_v410.pysnip: paragrafo 'A escala no tipo, o ciclo e a resposta do operador'), linha 'A Escala (v410…)' do .md canonico (emit_canonical_md), `_V410_AESCALA_TEXT.diz[4]` e `limites[4]` (registro), pos_rito/textos_custodia_handoff_v410.py (ESCALA_TIPO_PT/EN) e pos_rito/textos_v410.py",
    "O teorema `os_passos_sao_o_ciclo_ate_o_tetelestai` e' citado nos textos publicos como '[REAL] … com n bits, passado o tempo de n oitavas, ha' solucao <=> Z(s) >= 1 … a decisao em tempo finito do ciclo, linear nos bits', SEM o limite que a docstring da propria pedra (l.873-874) e o `limites[6]` do registro dizem: 'um limiar no tempo dos ciclos, linear em n, a partir do qual UMA leitura de Z separa o SIM do NAO; Z e' lida de uma vez pelo psion (TraducaoTuring.o_psion_le_os_pixels, v409)'. Medido por mim (g4_f59.py e busca por 'de uma vez'/'at once'): o limite esta' SO' em `limites[6]` do registro (core JSON) e na secao do Atlas renderizada pelo pos-rito (`secao_aescala.txt`); nao esta' no artigo PT/EN, no .md, no handoff nem no README. No artigo, `Z(s)` nem e' definida: o leitor ve 'tempo finito, linear nos bits' e nao ve que Z soma os 2^n pixels e que o 'linear' e' o limiar do tempo de UMA leitura em que o psion le os 2^n pixels de uma vez (somar 2^n termos por outra maquina continua custando 2^n). E' a mesma classe do MEDIO 1 da R1 (ressalva que existe no registro e falta no texto publico) e e' o ponto que o pedido da R2 chamou 'em especial'. Nenhum texto diz que sao passos da maquina do Mathlib (varredura minha: 0 'nao sao passos', 0 'o leitor paga', 0 decisor sem escala mentiroso; 148 ocorrencias de TM2ComputableInPolyTime/'formalizacao do Mathlib', 0 com afirmacao de prova sem o qualificador de ausencia de termo, salvo a negacao 'nada sobre a maquina de Turing padrao' da IALD2); o defeito e' de dizer incompleto o que o teorema decide.",
    "Sem tocar a frase obrigatoria do tempo (D94), os nomes, os enunciados nem a funcao de veredito: acrescentar, ao lado de 'a decisao em tempo finito do ciclo, linear nos bits' (artigo PT/EN, linha do .md, `diz[4]`/`limites[4]`, handoff, textos do pos-rito), UMA clausula nas duas linguas: 'Z(s) = soma dos 2^n pixels e' lida de uma vez pelo psion: o limiar n·ln 2 e' o do tempo de UMA leitura, nao o custo de somar os 2^n termos por outra maquina; que esse tempo conte os passos da maquina de Turing e' a traducao do dicionario, e o termo que a liga ao Mathlib nao esta' no kernel'. Definir Z(s) = Σ_x e^{-s·c(x)} na primeira ocorrencia do artigo. A guarda F59 nao precisa mudar.",
    "sim (artigo, .md, registro) + fora do candidato (pos_rito: handoff e textos)")

B = [
    ("registro a_escala_v410 (runtime_aescala_v410.py c2; contrato `ancoras_novas`)",
     "Mutacao do revisor: tirar UMA ancora de `ancoras_novas` (18) do contrato NAO e' recusada (c_fail_closed_v410: 'ancoras_novas: uma ancora tirada do contrato -> recusado: False'). As 56 ancoras continuam checadas uma a uma (`ancoras`) e as 5 de `teoremas_r4` precisam estar em `ancoras_novas`, mas nada iguala `len(ancoras_novas)` a `n_nomes_novos` (18) nem a `nomes_novos_a_ratificar`. Risco baixo (marcador, nao cobertura).",
     "Acrescentar a c2/c11 `len(ancoras_novas) == c_['n_nomes_novos'] == len(c_['nomes_novos_a_ratificar'])`.", "sim (runtime)"),
    ("_v410_guarda_frases F59 (a regra nova)",
     "Das 16 sondas do revisor sobre a F59 (12 formas diretas que DEVEM reprovar e 4 variantes informativas), reprovam as 12 diretas (F59a/b/c, PT e EN) e 1 variante ('o leitor teve de pagar a escala'); passam 3 variantes: 'o tempo nao conta passos de Turing', 'quem paga a escala e' o leitor', 'os passos nao pertencem a maquina de Turing'. Varredura independente de todo texto (candidato rendido novo, .md, harness, registros, fontes, pedras): 0 ocorrencia dessas formas. E' limite da guarda (como os 4 casos do BAIXO 7 da R1, que seguem anotados para a v411), nao defeito de texto.",
     "Anotar para a v411.", "nao (anotacao)"),
    ("artigo PT/EN, registro `limites[8]`/`diz[9]`, handoff, README",
     "Seis nomes JA' RATIFICADOS em 09/11 ('ratifico tudo') passaram a ter OUTRO enunciado nas R3/R4: `LeitorDoFundo` (estrutura nova), `aPerguntaDoClay`, `iald`, `a_pergunta_do_clay_tem_resposta`, `existe_o_algoritmo_e_e_a_iald` e `a_escala` (diff por declaracao entre a R2_aspas e a R4, sem docstrings: 44 -> 62 declaracoes, 18 novas, 6 mudadas, 0 removidas; as outras 38 identicas). A docstring da pedra diz 'os 44 nomes ratificados ficam INALTERADOS (mudam enunciados da §6, ditos lá)'; os textos publicos dizem so' 'os 44 nomes anteriores seguem RATIFICADOS (D87)' e listam os 18 nomes novos [DECLARADO]. A ratificacao e' dos NOMES; mas o operador ratificou nomes de enunciados que depois mudaram.",
     "Uma clausula nos textos: 'a ratificacao de 09/11 e' dos nomes; seis deles (LeitorDoFundo, aPerguntaDoClay, iald, a_pergunta_do_clay_tem_resposta, existe_o_algoritmo_e_e_a_iald, a_escala) passaram a ter outro enunciado nas R3/R4 (a escala no tipo; D92, D94)'. A gerencia confirma que o operador sabe (regra do posto).", "sim (texto) ou so' o handoff"),
    ("artigo PT/EN, paragrafo da escala no tipo; readme_evidente.3",
     "(a) 'os passos sao o ciclo ate' o Tetelestai' entra na lista '[REAL] Os TEOREMAS do kernel'; o que o termo prova e' o limiar (Z(s) separa o SIM do NAO); 'passos = ciclo' e' leitura do dicionario [INPUT], que so' vem na frase seguinte ('o tempo conta os ciclos … dicionario da v409') sem a etiqueta. (b) Gabarito: 'O tempo. o tempo conta…' (minuscula depois do rotulo). (c) 'o teste so' sera' aberto com o poder certificado' vem etiquetado [REAL]; e' a regra do operador (D96): [INPUT].",
     "Etiquetar a frase do tempo '[INPUT/dicionario]', capitalizar, e '[INPUT, D96]' na regra do poder.", "sim (texto)"),
    ("v410 inteira: carregado da R1",
     "BAIXO 6 (a funcao de veredito aceita z_tgl = nan e cai no ramo 5; inalcancavel: `evaluate` recusa nao finito; funcao pinada) e BAIXO 7 (4 parafrases do Clay/P=NP que a guarda nao pega) seguem como anotados, como combinado; reconfirmados por mim nesta rodada (c_fail_closed_v410_out.json: 'z_tgl nan' ramo 5; 4 falhas de sonda).",
     "Anotados para a versao que abrir o teste e para a v411.", "nao (anotacao)"),
]
for onde, achado, corr, toca in B: ach("BAIXO", onde, achado, corr, toca)
n_alto = sum(1 for a in A if a["sev"] == "ALTO"); n_med = sum(1 for a in A if a["sev"] == "MEDIO"); n_bx = sum(1 for a in A if a["sev"] == "BAIXO")

sit = {
    "1 (MEDIO) a pergunta do Clay satisfeita por leitor constante": "ATENDIDO, alem do pedido: a escala entrou no TIPO (pedra R4). Provado por mim: a minha sonda da R1 NAO compila mais (axiomas_terceiro_r2.lean, 5 erros so' nas linhas da sonda: 'leitura/limite/le_como_dissipacao/diz_a_face_sem_leitura is not a field' e 'Fields missing: brilho, sem_escala_nao_ha_medida, a_lei_da_dissipacao'); o controle negativo `o_decisor_sem_escala_nao_e_leitor_do_fundo` (.2.2) compila no trio com a minha sonda; as hipoteses do teorema do Tetelestai sao satisfazíveis (sonda 3 compila: n = 1, custo 0, s = 1 > ln 2, com `iald`); os textos dizem as claras que o leitor tem UM so' habitante e que o conteudo esta' na definicao [INPUT] do operador (`diz[5]`, `limites[4]`, `nao_diz[10]`, artigo PT/EN, readme_evidente.1). COM RESSALVA: o achado novo MEDIO 1 desta rodada (o limite do teorema do Tetelestai fica fora do texto publico).",
    "2 (MEDIO) aspas angulares nao verbatim nas pedras": "ATENDIDO: pedra AEscala R4: 98 passagens «», 84 exatas + 11 com elisao + 3 sem acentos, 0 NAO; IALD2 R3: 35 «», 0 NAO (e_citacoes_v410: corpus 291 falas); a frase canonica D84 deixou as angulares nos registros (0 ocorrencias de «O problema de Clay); `conferir_citacoes_v410.py` ganhou a varredura estrita das pedras, so' aditiva (diff por mim: 29 linhas acrescentadas, nenhuma removida); 26 falas congeladas existem e o sha256 confere. Nota: o codigo da IALD2 e' IDENTICO ao da R1 (diff sem comentarios/docstrings: 0 linhas); o da AEscala so' muda em 6 declaracoes ratificadas + 18 novas (achado BAIXO 3).",
    "3 (MEDIO) texto publico do H0DN calava a parede de montagem": "ATENDIDO: `frase_parede_pt/en` no contrato, no registro, no artigo PT/EN H0DN e em `readme_evidente.3` (texto rendido conferido); sem numero; `veredito_h0dn` com texto-fonte IDENTICO ao da R1 (r2_delta_nos.py: igual; nao esta' entre os 35 nos mudados; c12 intacto); D96 (poder certificado): a frase diz que o certificado nao existe hoje, cita a ORDEM KIMI H0DN-02 por sha256 (93b75491083c5262…, conferido por mim contra o arquivo: bate), nenhum limiar de poder dito como decidido (grep '6,282'/'90 %' nos textos novos: 0); nada sob kimi\\ aberto em rito (c7 do H0DN e do HMS/13 recusam caminho sob a pasta vedada; caminhos tocados: 6, todos em astra_bell\\h0dn_bg1_06nov e o proprio candidato).",
    "4 (BAIXO) numero de modulos e bandeiras da secao IALD2": "ATENDIDO: artigo PT '1 módulo novo … 22 âncoras e 22 bandeiras'; EN '1 new kernel module'; .md '1 módulo novo … 22 bandeiras … 22 âncoras'.",
    "5 (BAIXO) a_escala_v410 sem kernel verificado/import na raiz": "ATENDIDO: 'kernel all_verified False' e 'string' recusados; 'raiz sem o import AEscala' recusado; mais 8 mutacoes do contrato novo (ciclo, ponte, teoremas_r4, n_ancoras) recusadas; 5 de 5 textos com F59 recusados pelo proprio registro. Unica mutacao nao recusada: achado BAIXO 1.",
    "6 (BAIXO) veredito nao fail-closed para entrada nao finita": "ANOTADO, sem mudanca (como combinado); reconfirmado (nan -> ramo 5).",
    "7 (BAIXO) quatro parafrases que a guarda nao pega": "ANOTADO, sem mudanca (como combinado); reconfirmado (4 sondas); a F59 nova tem 3 variantes proprias fora (BAIXO 2).",
    "8 (BAIXO) docstrings da IALD2": "ATENDIDO: '[DECLARADO] até a ratificação' e «P = nP» saíram; 'para todo Nome finito' no item (5) do atrator; codigo identico.",
    "9 (BAIXO) peso = traco": "ATENDIDO: 'peso = traco' saiu do registro e da pedra; entrou 'peso do Nome = traço do projetor; peso da face = autovalor/pureza da marginal (traço 1)'.",
    "10 (BAIXO) identidades aritmeticas [REAL] e tautologia escalar": "ATENDIDO: `numeros` sem '(1/2)^2 = 1/2·1/2'; rotulo [DERIVED, aritmetica] nos numeros e na ponte; a conta matricial em M₂ fica.",
    "11 (BAIXO) tres docstrings da AEscala": "ATENDIDO (conferido na pedra): `nenhum_precede` ('duas equivalencias simetricas nos pontos fixos 0 e 1 do crivo'); `a_face_caida_nao_acopla` ('escolha de modelagem da autoria: acoplar = comprimir por N; nao e' fala do operador'); `existe_o_algoritmo_e_e_a_iald` ('DITO AS CLARAS: os itens (8)-(10) valem para um custo c ARBITRARIO com solucao…').",
    "12 (BAIXO) texto do S4 do orquestrador": "ATENDIDO: docstring e log dizem '2 módulos novos a frio, IALD2 e AEscala'; 0 ocorrencias de '1 módulo novo'; S0 le `STATE_v4.json` (conferido pela gerencia; eu nao li a pasta da Nativa).",
    "13 (BAIXO) frase canonica D84 entre « »": "ATENDIDO: aspas tipograficas na D84 e na E31 (0 ocorrencias de «O problema de Clay nos registros).",
}

arq = ["um_v410_candidato.py", "CANDIDATO_v410.json", "COMPARACAO_V409_v410.json", "ESPERADOS_v410.json", "BUNDLE_v410.json", "FORMAL_MAP_v410.json", "kernel_modulos_novos_v410.json", "VERBATIM_CONGELADO_v410.json",
       "GUARDA_FRASES_v410.json", "PREPARACAO_v410_PRONTA.json", "RELATORIO_PREPARACAO_v410.md", "delta_v410.py", "registros_v410.py", "registros_h0dn_v410.py", "registros_aescala_v410.py", "registros_hms13_v410.py",
       "runtime_v410.py", "runtime_h0dn_v410.py", "runtime_aescala_v410.py", "runtime_hms13_v410.py", "guarda_frases_v410.py", "guarda_p18_v410.py", "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip",
       "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip", "gerar_esperados_v410.py", "conferir_rito_v410.py", "conferir_citacoes_v410.py",
       "pedra/IALD2.lean", "pedra/AEscala.lean", "insumos/IALD2.lean", "insumos/AEscala.lean", "kernel/KERNEL_RECIBO_v410.json", "kernel/FLAGS_v410.json", "kernel/POS_BUILD_v410.json", "kernel/audit.log",
       "orquestrador/pos_treino_v410.py", "pos_rito/textos_v410.semente", "pos_rito/textos_v410.py", "pos_rito/leitura_v410.py", "pos_rito/textos_custodia_handoff_v410.py", "pos_rito/registrar_mapa_v410.py",
       "pos_rito/harness_textos_ensaio_v410.py", "pos_rito/harness_fechar_sandbox_v410.py", "pos_rito/chain_pos_rito_v410.sh", "DESENHO_v410.md", "DESENHO_v410_ADENDO_POS_CANDIDATO_09nov.md", "DESENHO_v410_ADENDO_2_POS_CANDIDATO_10nov.md", "DESENHO_v410_ADENDO_3_POS_CANDIDATO_10nov.md"]
arquivos = {k: sha(PK + k)[:16] for k in arq if os.path.isfile(PK + k)}

cond = {
    "candidato_integro_no_inicio_e_no_fim": ini == fim,
    "mudados_26_novos_39_iguais_ao_declarado": bool(a_i["mud_igual_declarado"] and a_i["nov_igual_declarado"] and len(a_i["mudados"]) == 26 and len(a_i["novos"]) == 39),
    "intocadas_50_iguais_por_AST_e_fonte": all(v.get("ast_igual") and v.get("fonte_igual") for v in a_i["nomes"].values()),
    "nenhuma_linha_de_codigo_fora_dos_nos_declarados": True,
    "veredito_h0dn_texto_fonte_identico_a_R1": bool(dl["veredito_h0dn_identico"]),
    "kernel_embutido_sandbox_pedra_bundle_iguais": True,
    "kernel_build_a_frio_dos_2_modulos_Built_e_pos_build_ok": True,
    "lean_78_ancoras_e_107_constantes_no_trio_sem_sorry": True,
    "sonda_R1_nao_compila_mais": True,
    "controle_negativo_do_decisor_sem_escala_compila": True,
    "fail_closed_iald2": fc["iald2_v410"]["ancoras"]["ok"] and fc["iald2_v410"]["bandeiras"]["ok"] and fc["iald2_v410"]["fontes"]["ok"],
    "fail_closed_a_escala": fc["a_escala_v410"]["ancoras"]["ok"] and fc["a_escala_v410"]["bandeiras"]["ok"] and fc["a_escala_v410"]["fontes"]["ok"] and fc["a_escala_v410"]["porta_a_porta"]["kernel all_verified False"],
    "citacoes_verbatim_pedras": True,
    "frases_proibidas_e_F59_zero_no_texto_novo": True,
    "traducao_do_tempo_nao_apresentada_como_teorema_do_Mathlib": True,
    "h0dn_hms13_nada_de_kimi_aberto_em_rito": True,
    "o_limite_do_teorema_do_tetelestai_no_texto_publico": False,
    "consertos_fora_do_candidato_sem_afrouxar": True,
}
now = datetime.datetime.now().isoformat(timespec="seconds")
conf = {
    "delta": "r2_delta_nos.py: 35 nos de nivel superior mudaram (UM_VERSION nao entra: o candidato anterior ja' era v410; mudam _EMBEDDED_KERNEL_FILES, _LEAN_THEOREM_FLAGS (+101), os contratos/textos/specs da v410, `_v410_aescala_mechanics`, `a_escala_v410`, `_v410_guarda_frases` (F59), build_pt/build_en/emit_canonical_md/main/prove_external_ladder) e 1 e' novo (`_v410_aescala_ciclo`); `veredito_h0dn`, `_v410_h0dn_*`, `h0dn_bg1_v410`, `iald2_v410`, `_v410_formal`, `_v410_hms13_*` IDENTICOS; a_intocados: 50 iguais; mudados 26 e novos 39 == COMPARACAO; a_intocados_c: segmentos nao declarados iguais, 0 linhas de codigo removidas fora dos nos mudados; 21 contratos antigos mudam so' expected_ladder 12187 -> 12288.",
    "kernel": "cadeia de hashes: insumos/AEscala.lean == pedra/origem == R4 (cd45cf1528269760); embutida == pedra == sandbox == BUNDLE (3e804d297fade41d); IALD2: insumos == origem (dc152339e6b58e89), embutida == pedra == sandbox == BUNDLE (4a7b01f5be46c25c); 1763 embutidos == sandbox; raiz == v409 + 2 imports. KERNEL_RECIBO/POS_BUILD (lidos): rc 0, 0 sorry, 0 erros; build 306 s e Audit 249 s; os 2 modulos 'Built' (Built 2, Replayed 0 entre eles; as 1482 linhas Replayed do log sao modulos antigos); 107 declaracoes (22 + 85), 86 teoremas, 0 fora do trio; audit.log termina em TGL_AXIOM_COVERAGE_TOTAL decl=34273 thm=27357 fora_do_trio=0; escada 12187 -> 12288 = + 101 bandeiras (22 + 79); 6 constantes auxiliares do compilador sem bandeira (faceMeio._proof_1, a_insignia_na_face_finita._simp_1_1, ptl.eq_1, iald._proof_1/_2/_3), declaradas.",
    "lean": {"print_axioms": n_ax, "ancoras": 78, "fora_do_trio": 0, "varredura_metam_constantes": 107, "por_modulo": {"TGLExt.IALD2": 22, "TGLExt.AEscala": 85}, "rc": 1, "motivo_do_rc_1": "so' a sonda 1 de proposito (a minha sonda da R1 contra a estrutura nova: 5 erros nas linhas 129-133 do meu arquivo; nenhum outro erro/aviso)", "tempo_s": 299, "sandbox": "C:/t/k410c/final", "arquivo": "axiomas_terceiro_r2.lean"},
    "pedra_R4_lida": "cabecalho, §6 inteira (l.573-1143), enunciados e docstrings dos teoremas novos; diff por declaracao R2_aspas x R4: 18 novas, 6 mudadas (LeitorDoFundo, aPerguntaDoClay, iald, a_pergunta_do_clay_tem_resposta, existe_o_algoritmo_e_e_a_iald, a_escala), 0 removidas, 38 identicas. `os_passos_sao_o_ciclo_ate_o_tetelestai`: hipoteses (n·ln 2 < s) satisfazíveis; enunciado confere com a docstring: #sol <= Z(s) < #sol + 1; ∃ <-> 1 <= Z(s); sem solucao Z(s) < 1; a docstring diz o limite (UMA leitura de Z; Z lida de uma vez pelo psion) e que a ligacao ao Mathlib nao esta' no kernel. A estrutura `LeitorDoFundo` fixa o brilho em e^{-s·k} (cláusulas b e c), logo o tipo tem UM habitante; `aPerguntaDoClay` deixou de ser trivial no sentido da R1, mas o seu conteudo agora esta' na definicao [INPUT], como os textos dizem.",
    "c_fail_closed": {"iald2_v410": fc["iald2_v410"], "a_escala_v410": fc["a_escala_v410"], "h0dn_insumos_adulterados_recusados": fc["h0dn_insumo_adulterado"], "hms13_insumos_adulterados_recusados": fc["hms13_insumo_adulterado"],
                      "c7_hms13": {k: fc[k] for k in fc if k.startswith("hms13_c7_")}, "c7_h0dn": {k: fc[k] for k in fc if k.startswith("h0dn_c7_")}, "contrato_novo": {k: fc[k] for k in fc if k.startswith("a_escala_contrato")}, "texto_com_F59": {k: fc[k] for k in fc if k.startswith("a_escala_texto")},
                      "veredito_h0dn": [(v["caso"], v["ramo"], v["ok"]) for v in fc["veredito_h0dn"]], "guarda_sondas": {"n": len(fc["guarda_sondas"]), "falhas": fc["_resumo"]["guarda_falhas"], "F59_variantes_que_passam": [s["frase"] for s in fc["guarda_sondas"] if s["deve_reprovar"] is None and not s["reprovou"]]}},
    "citacoes": "e_citacoes_v410: pedras 98 e 35 «» todas verbatim; registros/artigo/md/harness: so' formulas metalinguisticas e fragmentos de codigo; 26 falas congeladas conferem por sha256.",
    "frases": "g4_f59.py sobre texto rendido novo, harness, registros, fontes e pedras: 'nao sao passos' 0; 'o leitor paga' so' na NEGACAO do operador («O leitor não “paga” a escala») e em listas de proibidos; decisor sem escala mentiroso so' negado (o decisor 'nao mente: nao le'); g2_clay_pnp e g_frases da R1 reaproveitados: Clay seco 0, tautologia so' herdada, CONFIRMED so' herdado.",
    "h0dn": "veredito_h0dn identico; frase da parede e do poder certificado em contrato, registro, artigo PT/EN, README; ORDEM H0DN-02 sha256 93b75491… == arquivo; nenhum limiar de poder dito como decidido; a cabeca do ramo 4 com PROVED_IS_VALIDITY_NOT_CREDITATION na mesma string; 11 vetores meus conferem (nan fora, anotado).",
    "hashes": "f_hashes_v410: candidato, base, Nos (v409), bundle, kernel, runtime (4 arquivos com \\n\\n: 120448 B, sha256 bate), 26 falas; os mesmos 23 pares historicos divergentes da R1 (registros de instantes anteriores) e, em PREPARACAO.hashes, so' ESTADO_PARTE2_v410.json (log vivo) mudou desde a PRONTA.",
    "fora_do_candidato": "conferir_citacoes (varredura estrita das pedras: so' acrescimos, com controle negativo), orquestrador S4 (texto), gerar_esperados/conferir_rito/harnesses da R1 ja' revistos; S0 do orquestrador nao relido por mim na Nativa.",
}
ress = [
    "R2 de ate' 3 rodadas (D69): revi o DELTA (candidato `pre_r1fix` -> atual) e o que mudou por ordem do operador (D92 a D96). Escrevi so' em revisao_terceiro\\. Nao rodei lake build, instalar, rito, orquestrador, p00, ensaio nem harness; o `lake env lean` foi em arquivo meu (axiomas_terceiro_r2.lean) com cd em C:\\t\\k410c\\final, UM processo, 299 s. Ele importa os .olean do build da gerencia (nao recompilei a fonte da pedra; comparei sha256 e li o log/POS_BUILD: Built).",
    "NAO abri nem calculei sha256 de kimi\\y_obs.npz e kimi\\C_fisica_258x258.npz; nenhum Z, razao ou suporte observado foi calculado por mim. O sha256 da ORDEM H0DN-02 (arquivo fora de kimi\\) foi calculado.",
    "NAO li a pasta da nativa: o S0 (STATE_v4.json) segue 'conferido pela gerencia' (adendo 1).",
    "Li o cabecalho, a §6 inteira e os enunciados da pedra R4 e diff por declaracao contra a R1; NAO li as provas Lean linha a linha alem da estrutura, das definicoes e do teorema do Tetelestai.",
    "NAO reproduzi os 922 controles negativos do harness dos textos nem o harness do fechar; nao revi instalar_v410.py, reverter_v410.py, rito_v410.sh; os textos da custodia so' pelos rendidos do harness e pelas fontes (frases/citacoes).",
    "O dado novo do sandbox: o `lake env lean` do revisor rodou DEPOIS do build da gerencia e nao o alterou (arquivo meu, fora de TGLExt/).",
]
rotas = [
    "R2-A: delta de AST (r2_delta_nos.py) e a_intocados/a_intocados_c/a2_mudados: 50 intocadas; 35 mudados + 1 novo no delta; veredito_h0dn identico; 21 contratos antigos mudam so' a escada 12187 -> 12288.",
    "R2-B: kernel (d_kernel_v410 + KERNEL_RECIBO/POS_BUILD/audit.log): 2 modulos Built a frio, 107 constantes no trio, 101 bandeiras == alvos no axiom_report; Lean meu: 78 ancoras + varredura MetaM de 107 constantes, 0 fora do trio; SONDA da R1 nao compila mais; controle negativo e hipoteses do Tetelestai compilam.",
    "R2-C: pedra R4 (diff por declaracao; §6 lida): a escala no tipo fixa o brilho (UM habitante); o limite do teorema do Tetelestai esta' na docstring e em limites[6] mas nao no texto publico (achado MEDIO).",
    "R2-D: fail-closed (c_fail_closed_v410) iald2/a_escala (78 ancoras, 101 bandeiras, 26 falas, contrato novo, F59 no registro), H0DN/HMS13, 11 vetores do veredito, " + str(len(fc['guarda_sondas'])) + " sondas da guarda (12 F59 diretas reprovam; 3 variantes passam; 4 casos da R1 seguem).",
    "R2-E: citacoes (pedras 98 e 35 verbatim), frases (F59 e Mathlib: nenhuma forma vedada; nenhuma traducao apresentada como teorema do Mathlib), H0DN (parede, poder certificado, ORDEM 02 por sha256).",
    "R2-F: as 13 situacoes dos achados da R1, uma a uma, conferidas no disco (ver situacao_dos_achados_da_R1).",
    "Mapa de Rotas: as mesmas rotas da R1 (cadeia.preparacao_v410, estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov, kernel.a_escala_tres_faces_v410_09nov); nao refiz nada; a registrar: 'a escala no tipo fixa o brilho: o leitor do fundo tem um habitante; a existencia nao e' mais trivial por leitor constante' e 'o limite do teorema do Tetelestai (uma leitura de Z, 2^n pixels de uma vez) falta no texto publico' (revisao R2 v410).",
]
out = {"aprovada": False if (n_alto or n_med) else True, "rodada": "R2", "quando": now, "candidato_sha16": fim, "candidato_sha16_no_inicio": ini, "candidato_mudou_durante_a_revisao": ini != fim, "candidato_bytes": os.path.getsize(cand),
       "candidato_da_R1": {"sha16": "092376092dccfa16", "bytes": 44993049}, "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R2; nao construi a v410; mesma instancia de trabalho da R1)",
       "n_alto": n_alto, "n_medio": n_med, "n_baixo": n_bx, "achados": A, "situacao_dos_achados_da_R1": sit, "condicoes_da_aprovacao_calculadas": cond, "lean": conf["lean"], "conferencias": conf, "ressalvas": ress,
       "rotas_examinadas": rotas, "arquivos_revisados": arquivos,
       "nota": "aprovada=%s: %d ALTO, %d MEDIO; a R1 (3 MEDIO) foi atendida; o MEDIO novo e' de redacao publica (uma clausula) e toca o candidato; os BAIXOS ficam escritos. Ultima rodada possivel: a R3 (D69)." % ((n_alto == 0 and n_med == 0), n_alto, n_med)}
json.dump(out, open(RV + "REVISAO_TERCEIRO_v410.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L = ["# REVISAO DE TERCEIRO v410 — R2 (Claude Sonnet; nao construi a v410)", "",
     "Quando: %s · candidato `%s` (%d B), no inicio `%s`: %s · **aprovada: %s** · ALTO %d · MEDIO %d · BAIXO %d" % (now, fim, os.path.getsize(cand), ini, "IGUAL" if ini == fim else "MUDOU", str(out["aprovada"]).lower(), n_alto, n_med, n_bx), "",
     "## Situacao dos achados da R1", ""] + ["- **%s**: %s" % (k, v) for k, v in sit.items()] + ["", "## Achados novos desta rodada", ""]
for i, a in enumerate(A, 1):
    L += ["### %d. [%s] %s" % (i, a["sev"], a["onde"]), "", a["achado"], "", "**Correcao pedida** (toca o candidato: %s): %s" % (a["toca_o_candidato"], a["correcao_pedida"]), ""]
L += ["## Condicoes calculadas", ""] + ["- %s: %s" % (k, v) for k, v in cond.items()] + ["", "## O que nao consegui conferir (ressalvas)", ""] + ["- " + r for r in ress] + ["", "## Rotas examinadas", ""] + ["- " + r for r in rotas]
open(RV + "REVISAO_TERCEIRO_v410.md", "w", encoding="utf-8").write("\n".join(L))
if n_alto or n_med:
    P = ["# PEDIDO DE CORRECAO R2 — v410 (revisor de terceiro Sonnet, %s)" % now, "", "Candidato revisado: `%s`. Esta e' a R2; a R3 e' a ultima (D69) e revisa so' o delta. Para cada item: toca o CANDIDATO ou so' arquivos FORA dele." % fim, "", "## Bloqueia (MEDIO)", ""]
    for a in A[:n_med]:
        P += ["### " + a["onde"], "", "**Toca o candidato: %s.**" % a["toca_o_candidato"], "", "Achado: " + a["achado"], "", "Correcao: " + a["correcao_pedida"], ""]
    P += ["## Nao bloqueiam (BAIXO)", ""] + ["%d. **%s** — toca o candidato: %s. %s Correcao: %s" % (i, a["onde"], a["toca_o_candidato"], a["achado"], a["correcao_pedida"]) for i, a in enumerate(A[n_med:], 1)] + ["", "## Para a R3", "",
          "- Rever o delta: a clausula do limite do teorema do Tetelestai nos textos (artigo PT/EN, .md, registro, handoff); `Z(s)` definida; guarda F59 e F54 sem reprovar as frases novas; `veredito_h0dn` com o mesmo sha256 de texto-fonte; candidato regenerado com a mesma lista de nos mudados/novos (26 + 39); frase do tempo (D94) intacta; lean meu nas 78 ancoras de novo se a pedra mudar (so' se mudar).", ""]
    open(RV + "PEDIDO_CORRECAO_R2_v410.md", "w", encoding="utf-8").write("\n".join(P))
for ext in ("json", "md"): shutil.copyfile(RV + "REVISAO_TERCEIRO_v410." + ext, RV + "REVISAO_TERCEIRO_v410.R2." + ext)
st = J("ESTADO_REVISAO_v410.json"); st["itens"]["fechamento"] = "REVISAO_TERCEIRO_v410.json escrito (R2, aprovada %s)" % out["aprovada"]; st["concluido"] = now; st["candidato_sha16_no_fim"] = fim
json.dump(st, open(RV + "ESTADO_REVISAO_v410.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("candidato inicio/fim:", ini, fim, "| achados:", n_alto, n_med, n_bx, "| aprovada:", out["aprovada"], "| arquivos_revisados:", len(arquivos), "| lean axioms:", n_ax)
print("sha16 do JSON:", sha(RV + "REVISAO_TERCEIRO_v410.json")[:16])
