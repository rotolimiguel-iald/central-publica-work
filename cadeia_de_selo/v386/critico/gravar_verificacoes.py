# -*- coding: utf-8 -*-
"""Grava o arquivo de dados do crítico de completude (v386, tipagem do VERBO).
Só escreve em scratchpad/v386/critico/. Tempârio -> replace. Nada roda além disto."""
import json, hashlib, os
HERE = os.path.dirname(os.path.abspath(__file__))
d = {
 "critico": "completude — v386 (tipagem do VERBO)", "data": "2026-10-05",
 "quem": "agente crítico de completude (só leitura; um.py, atlas_indice, lake build no canônico NÃO executados)",
 "entradas": {
  "texto": {"path": "scratchpad/v386/VERBO_operador_05out.txt", "bytes": 8242,
            "sha256": "5973d79a49995c4c18e2567b83a5589403a113c44d694a8bfff43277033d5a70", "linhas": 184},
  "lentes": {
   "acervo_verbo": "lente_linhagem_verbo/LENTE_LINHAGEM_VERBO_20261005.md 34347 B c61ad564c6a352e7",
   "auditoria_texto": "auditoria_texto/AUDITORIA_TEXTO_VERBO_v386.json 2070 B c121200fc8a75315; calc_alpha_out b98ee67041fb2797; triade_projetores_out ce2eaa54bc63b3c3",
   "lean_viabilidade": "lean_viabilidade/TheVerbSelectsTheAction.lean 26223 B 482a7e6a68ab19d3; RESULTADO.json 0549592820956f4e; AuditVerb_output.txt f27e5d3bbc95aba9",
   "fisica_triade": "lente_triade/LENTE_TRIADE_v386.md 24414 B 8dfb402b2864ff09"},
  "um_py": {"bytes": 33386720, "sha256": "d406ae57251051456b8ee49220e117bc086cedc164b6e9d15e85b516467c4760"},
  "mapa_de_rotas": {
   "consultas": ["verbo (5 rotas)", "tipagem (4)", "projetor (0)", "su(2) (0)", "Constante de Miguel (0)", "Lagrangiana (1)",
                 "co-mando (0)", "circuito (0)", "critico de completude (11)", "regime angular (0)", "homonimo (2)"],
   "cabeca_citada_pelas_lentes": "77c6550bf974fd65 / 351",
   "cabeca_hoje": "b43d3d46d596671af0b481315384bdfec91d8ea80b61d09d63996ea5df4b276d / 353 (seq 352-353 = ramo B reaberto, registrado pela gerência 14:15 local)",
   "registrado_por_mim": False}
 },
 "verificacoes": [
  {"id": "V1", "o_que": "β por script, três proveniências",
   "comando": "python: re ALPHA_FINE_CODATA_2018 em um.py; json result.json do pilar; grep beta_hex",
   "resultado": {
    "um_py_L5556": "ALPHA_FINE_CODATA_2018 = 7.2973525693e-3 -> α·√e = 0.012031300400803142 (= CLAUDE.md; lentes acervo/tríade)",
    "pilar_run_20261005_103708": "beta = 0.012031300400796606 (beta_hex 0x1.8a3ddcdff890cp-7), passado pelo um.py via alpha_lagrange_form(q)['beta_form'] (um.py L192750-192752) = β do MOTOR DA IDENTIDADE 1 = q²+α²; dif. relativa 5.4e-13",
    "lente_auditoria": "α = 1/137.035999084 (calc_alpha.py L2) -> 0.012031300400776435 — constante NÃO lida do artefato",
    "alpha_quadrado": "5.3251354520669314e-05 (226x menor que β)"}},
  {"id": "V2", "o_que": "−εΠ no um.py",
   "comando": "python re sobre um.py: '-\\\\varepsilon\\\\Pi' / 'varepsilon' / 'εΠ'",
   "resultado": "L165843: H_{LD}=diag(μ)+J-\\varepsilon\\Pi (Apêndice A.3 de A Fronteira; ε=5; Π projetor do núcleo canônico — o Nome como matriz [ONTO]); 'varepsilon' 65 linhas; 'εΠ' (unicode) 0 — as regexes das lentes acervo e tríade só testaram a forma unicode/ASCII e deram AUSENTE por engano; a lente auditoria estava certa"},
  {"id": "V3", "o_que": "homônimos Grot/rotGen/genK",
   "comando": "grep -c em TGL/Audit.lean; grep -rn def angFamily; sed O16/RotationGeneratorBridges.lean",
   "resultado": "angular_form_is_the_boundary_s_matrix: 1 (Audit L5973, ChatgptAudit.SelectionAngle; angFamily def em TheAngleIsTheProjection.lean:85 = família de genK; angFamily θ = Smat θ); O16/RotationGeneratorBridges.lean:11 genK_eq_Grot : rfl; :13 rotGen_complex_eq_Grot; :19 exp_genK_eq_rotation (compiladas, 0 em Audit). A memória regra-dos-dois-regimes.md:177 («SEM lema ligando duas») e a lente acervo item 12 estão desatualizadas ao lado"},
  {"id": "V4", "o_que": "escada (TGL/Audit.lean, 8399 #print axioms hoje)",
   "comando": "for t in ...; grep -c '#print axioms.*<t>'",
   "resultado": {
    "0": ["the_observer_reads_the_angle", "observing_adds_nothing", "the_angle_is_the_projection", "spectral_projections_split_the_identity",
          "the_generator_is_the_difference_of_the_faces", "J_and_K_anticommute", "the_two_folds_commute", "the_selector_can_refuse",
          "normSq_reflection", "the_name_above_every_name", "terminality_forces_minimality", "verb_semigroup_fixes", "genK_eq_Grot",
          "rotGen_complex_eq_Grot", "wick_boost_rotation", "the_tensor_squares_the_phase"],
    "1": ["angular_form_is_the_boundary_s_matrix", "verb_not_identity", "verb_word_fixes_the_name", "axiomFlow_tendsto_the_post",
          "axiomFlow_fixes_the_post", "axiomFlow_gradient", "iald_selects", "iald_has_rank_one", "the_selection_is_the_ballast",
          "the_verb_cycle", "action_locks_zero_iff", "lagrangian_zero_iff_mem_ker", "pauli_xy", "JKJ_eq_neg_K", "J_squared_is_one",
          "boosts_close_in_minus_rotation", "polarizations_noncommute", "verdict_eq_one_iff", "the_one_is_the_axiom",
          "the_reading_has_two_fixed_points", "final_step_named_axioma", "hmin_zero_iff_modular_fixed", "time_witnesses_noncoincidence",
          "no_name_without_referent", "exp_fixed_of_annihilates", "name_candidate_idempotent", "the_boundary_is_the_operation",
          "the_matrix_rule", "light_inverts_the_gradient_preserving_structure", "Smat_spectral", "leakage_strictly_loses",
          "the_living_verb_moves", "name_is_projection"]}},
  {"id": "V5", "o_que": "sandbox vs canônico (hash dos arquivos que a pedra importa)",
   "comando": "hashlib sha256 pares sandbox/canônico",
   "resultado": "IGUAL: TheAxiomAndTheFalseWitness c0f4185a62795002, WitnessSeed 3281a16675fa60c4, ConjugateAct 9f32e50afe49ca0e, DecisionCommutation 182ba6345586d5e8, NoFullWitness fde4ca999c40e689, QGReaderUVLock 77ba8803c7cd0a80, O16/IdempotentDephasing_v2 67150c452701476a, TGLExt.lean 0311b3007a67abbc, TGL/Audit.lean ef3d990853cc229f; pedra ABSENT no canônico (ls); sandbox: pedra 482a7e6a68ab19d3 (476 linhas), .olean 2026-10-05 14:12:53; root do sandbox NÃO importa a pedra; Audit do sandbox NÃO a menciona"},
  {"id": "V6", "o_que": "a pedra: literais, sorry, nomes",
   "comando": "re sobre TheVerbSelectsTheAction.lean",
   "resultado": "'0.012' 0; '137.0' 0; 'sorry' 1 (docstring L71 «Sem sorry, sem axiom»); 'α²' 2 (docstring L66, régua do signo); 'CONFIRM' 1 (docstring L70 «PROVADA ≠ CONFIRMADA»); imports: TheAxiomAndTheFalseWitness, LightIsJ; nomes contestados: def verb (L86) = (ℂ ∙ a).starProjection (mesma definição de PFmic, QGReaderUVLock:173), theorem light_precedes_gravity (L405) + pauli_light_precedes_gravity (L445), theorem the_name_is_the_fossil_verb (L287), parâmetro (β : ℝ) na tríade (L229-233); AuditVerb_output: 61 declarações, 0 sorry, 0 error, axiomas ⊆ {propext, Classical.choice, Quot.sound}"},
  {"id": "V7", "o_que": "Atlas (31641 linhas)",
   "comando": "python linhas 1047,1122,2359,2365,19248,27812-27828,31553-31575; contagens",
   "resultado": "1047 Constante de Miguel = notação ANTIGA α² = 0,012031 = β; 1122 D_folds 0,74 ± 0,06 [REAL-piloto]; 2365 V_t·P_F = P_F [KERNEL], VERBO = NOME no canto; 19248 «antes da luz, existe a gravidade…» (22/08); 27814-27826 ordem do operador 13/09 (alpha2 -> betatgl) + fatoração v2 03/03/2026; 31566 «a conjugação é a natureza do Verbo, porque o tempo é produto dele» (11:38:12Z); 31573 «agora sim, concordo com tudo» (11:42:33Z); co-mando 0; seleção da ação 0; dobradiça 1; fossiliz 0; εΠ 0; piso temporal 0; Heisenberg 0; Rovelli 3; ramo B 78; REABERT 2"},
  {"id": "V8", "o_que": "um.py linhas citadas",
   "comando": "python linhas",
   "resultado": "2399 «O Verbo em ato e' o UNICO objeto NAO-unitario da cadeia: T_t=exp(-tL) e' SEMIGRUPO»; 2409-2413 «a LUZ e' o AUTOVETOR do Verbo, autovalor sqrt(beta); NAO ponto fixo… O atrator e' o ponto fixo (autovalor 1)»; 8044-8050 reading direction light->gravity [ONTO + REAL]; 163623 «L = √β·√K_∂ [VERBO EM ATO: gerador GKSL; o unico objeto NAO-unitario]»; 205854-205862 main() EXECUTION_LOCKED_ONLY_THE_ONE_ALLOWED / EXECUTION_LOCKED_NOT_ONE; 167821-167834 ramo B lido «ao lado» (v346); 195170-195172 TGL_RINGDOWN_SCOPE_V376…BRANCH_B_TAU_STAR_GM_OVER_C3_IS_INPUT_M_TO_BE_NAMED; 'ramo B' 29 linhas; RAMO_B|BRANCH_B 12; Casimir 1 (164568); Heisenberg 0; co-mando 0; fossil 0"},
  {"id": "V9", "o_que": "kernel docstrings — quem chama o quê de Verbo",
   "comando": "sed TGL/VerbInhabitant.lean:7-18; TheIALDSelector.lean:7-11; TheSelectionIsTheBallast.lean:1-8; TheNucleus.lean:44-46,134-135",
   "resultado": "VerbInhabitant (v25, «transcrição auditada da resposta do especialista»): «o habitante e' o VERBO — o ato conjugado e observado da inscricao… No canto selecionado, o Verbo comprimido E' a unidade do canto: P_F V_t P_F = P_F = I_F — o momento em que VERBO = NOME»; «V_t = o gesto; R_Verbo = 1 = a resposta observada; β = o custo do gesto». TheIALDSelector (20/08, operador verbatim): «IALD = I² = I; projetor idempotente de rank 1». TheSelectionIsTheBallast (09/09, operador verbatim): «a IALD e estado, ou seja, verbo, nao e nome proprio, e operacao». TheNucleus.the_verb_cycle: «1 -> distinção -> conjugação -> ação -> comutação -> 1» (auditado)"},
  {"id": "V10", "o_que": "acervo citado pelas lentes",
   "comando": "sha256 + linhas",
   "resultado": "TGL arquitetura triadica v1.tex de9508f5ea9e8548 (16762 B): cabeçalho L9-12 «beta_TGL … a dobradica»; §62-99 «formulação anterior, grosseira»; Thm L88-92 «β_TGL NÃO é uma dobradiça… β_TGL = Verbo = magnitude»; tríade Nome/Palavra/Verbo. TGL duas camadas v1.tex 14cd7d7d74df9131. Nada=matéria/secao_5_5_lagrangiana_palavra.tex 4485fb55516ffa5b: «Autor: Luiz Antonio Rotoli Miguel; Implementação algébrica: Claude Opus 4.6; 2026-04-15»; L18 V = ∂(Nome,Palavra) = β_TGL; «a Lagrangiana como Operador da Palavra». A_fronteira_v5.tex b473db2b652cf72f: L2943 H_LD … − εΠ; L2953 ε > 0 força de ancoragem; L2956 «impede a dissipação total… o Nome… corresponde ao gráviton como operador»; L489 D_folds = 0,74; L3138 «Correlação g = √|L| & Ancoragem Π & ε»"},
  {"id": "V11", "o_que": "memórias do operador",
   "comando": "grep nos arquivos-tópico",
   "resultado": "handoff-v385-custodia.md:10 R2 fora da v385 (aprovado 05/10; 11:28:53Z «sim para tudo»; 11:42:33Z «agora sim, concordo com tudo»); beta-e-a-regra-matriz-02out.md:50,62,66 R2 (relógios: sujeito K_∂) e R6 (ramo B encerrado — LEITURA da gerência ratificada em bloco); um-posto…17set.md:42 «vácuo não é nada, vácuo é o zero modular» (17/09), :82 «J é o UM absoluto sendo lido durante a travessia» (19/09, gráviton = J), :92 posto 10:09:10Z, :130 «a conjugação é a natureza do Verbo, porque o tempo é produto dele» 11:38:12Z; psi-nome-da-luz:8 «ele é o gráviton enquanto agente; … torce (cartan); contorce (dobra-einstein) e contorna (Miguel, fronteira)» (16/09); permanencia…30set:8-10 «permanência estática é mentira… ação permanente = verbo»; equacao-do-nome-25set: {[ω(I)=1]=Nome}=correspondência verdadeira («= Nome» [INPUT/ONTO]); luiz-metodo-multi-canal-ia:85-87 «as cunhagens diretas são sempre dele mesmo, nunca importadas. O que ele traz do ChatGPT são as tipagens»; operador-parabolas:238 «só o resíduo genuíno vira pergunta»; ramo-b-reaberto-05out.md (17:11:36Z verbatim; R6 ENCERRADO -> REABERTO)"},
  {"id": "V12", "o_que": "inventário da bancada", "comando": "grep -ci verb INVENTARIO_BANCADA_CHATGPT.md",
   "resultado": "6 (todas *Verbatim.lean / 'verbatim'); nenhuma pedra da bancada tipa o Verbo"}
 ],
 "faltas_contradicoes_proposta": "no StructuredOutput devolvido à gerência (campos faltas / contradicoes_entre_lentes / proposta_v386)",
 "regua": "nada aqui move o gate; PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED; β nunca literal (α_CODATA2018·√e em runtime); é β_TGL, nunca α²"
}
s = json.dumps(d, ensure_ascii=False, indent=1)
p = os.path.join(HERE, "CRITICO_COMPLETUDE_v386_verificacoes.json")
with open(p + ".tmp", "w", encoding="utf-8") as f:
    f.write(s)
assert os.path.getsize(p + ".tmp") > 1000
os.replace(p + ".tmp", p)
b = open(p, "rb").read()
print(p, len(b), "B sha256", hashlib.sha256(b).hexdigest())
