# Gera registro_mapa_pedras_v402.json (campos de `rotas.py modelo`) e VALIDA contra as regras do mapa SEM gravar nada.
# Uso: C:\Python314\python.exe -X utf8 -I gera_registro.py
import importlib.util, json, os

W = r"C:\IALD\Central de Patentes\work\pedras_v402"
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
ax = json.load(open(os.path.join(W, "AXIOMAS.json"), encoding="utf-8"))
A, B = ax["pedras"]


def cov(P):
    c = P["audit_incremental"]
    return "%d constantes, %d teoremas, fora_do_trio=%d, sorry=%d" % (c["decl"], c["thm"], c["fora_do_trio"], c["sorry"])


common_art = [
    os.path.join(W, "AXIOMAS.json"),
    os.path.join(W, "RESULTADO.md"),
    os.path.join(W, "build_log.txt"),
]

recA = {
    "tipo": "ROTA",
    "rota_id": "kernel.v402_queda_sem_geometria",
    "dominio": "KERNEL_FORMAL",
    "titulo": "Pedra «a queda sem geometria» (TGLExt.QuedaSemGeometria, nome provisorio): o peso cai estritamente (nats = s), a seta e' o sinal de s, o piso e' o posto, a entrega custa, o regime angular so le; transporte da H3 de uma tela a todas sob IsotropicPost; composicao por citacao, em sandbox",
    "pergunta": "Pode-se tipar no kernel, sem geometria, a queda do Um posto (a fala de 26/10) como perda de peso sob a escala dual, com a seta como unica direcao distinguida, e reduzir a H3 em toda tela a uma tela por orbita mais uma isotropia nomeada?",
    "dados": [
        os.path.join(CUN, "OPERADOR_26out_o_um_se_poe_e_cai_a_queda_sem_geometria_verbatim.txt"),
        os.path.join(CUN, "OPERADOR_26out_e_isso_faca_a_prova_prossiga_verbatim.txt"),
        os.path.join(NOS, "ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md") + " (itens 5 e 6, so citado)",
        "TGLExt/Fundacao.lean, NoFullWitness.lean, FalsidadeDaInercia.lean, TheGreatAttractor.lean, SMatrix.lean, O16/WickBoostRotation_v2.lean, O16/PolarMinimalPeriod_v2.lean, IALDJones.lean, Palavra.lean, LiganteLeiCampoCurvo.lean e LiganteLeiCampoCurvoTestemunha.lean do sandbox k402 (byte a byte iguais ao kernel do Nos v401)",
    ],
    "metodo": "Composicao por citacao de DualScalingData.scaling, Fundacao.(the_floor_fixes_the_cut, the_fall_never_lands, abismo), NoFullWitness.(leakage_strictly_loses, beta_forbids_full_static_witness), FalsidadeDaInercia.leak_below_every_epsilon, TheGreatAttractor.um_is_the_great_attractor, SMatrix.Smat_mul, Wick016.rotation_two_pi, PolarPeriod016.faithful_period_iff, Palavra, IALDJones.(orbita) e LiganteLeiCampoCurvo.NamedAtlasH3; lemas de cola declarados no cabecalho; lake build dos dois modulos + auditoria incremental de axiomas (collectAxioms) no sandbox C:\\t\\k402\\final",
    "resultado": "Build completed successfully (9451 jobs); %s; %d #print axioms, todos no trio; fidelidade dos verbatins %d de %d por bytes. sha16 do .lean %s. Nada instalado no Nos nem no um.py; Nos e adendo de 04/09 nao tocados." % (cov(A), A["print_axioms_no_build"], A["fidelidade_verbatins"]["trechos_conferidos_como_substring_das_fontes"], A["fidelidade_verbatins"]["trechos_entre_aspas_distintos"], A["lean_sha16"]),
    "veredito": "PEDRA_QUEDA_SEM_GEOMETRIA_COMPILED_AND_PROVED_IN_SANDBOX__NOT_INSTALLED",
    "estatuto": "REAL (teoremas sobre os dados e hipoteses nomeados); KNOWN (lei de escala de Takesaki; isotropia do vacuo de Bisognano-Wichmann/Poincare); INPUT (a fala e a parabola); ONTO (a leitura 1+3; o labirinto como regime angular); OPEN (dimensao 3; IsotropicPost do atlas curvo; o parametro s da acao dual como fase de um corpo fisico)",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": "IsotropicPost e' hipotese NOMEADA, nao termo do kernel: num atlas curvo nenhum grupo leva um ponto noutro (so a versao uma tela por orbita), e a H3 nao e' automatica (AuditF23Flat.s8_h3_is_load_bearing: com fonte anisotropica ela falha). O 'chao' da parabola e' o POSTO (peso 1 = omega(I), corte a = 0), NUNCA o infimo 0 (o 0 e' o abismo, sem fundo; decisao da gerencia, 26/10/2026); a queda que sabe que tem um chao e' a queda do que nao e' o posto. A dimensao 3 nao e' provada (1+3 e' leitura ONTO). O peso tau nao e' a massa (rota kernel.ordem025.ponte_escala_dual). Grafia do operador conservada nos bytes (gemetrica, relaxamaneto, labirito, geomtria); 'Lorentz vem da queda da fase' e' titulo do escriba (E5), a cunhagem dele e' 'Lorentz vem do potencial da fase de queda...'.",
    "nao_refazer": "A queda como perda estrita de peso (nats = s; independente do portador), a seta como sinal de s, o contraste angular (periodico, sem limite; faithful_period_iff) e a reducao da NamedAtlasH3 a uma tela por orbita + IsotropicPost estao tipados e compilados; nao reprovar a mesma composicao. NAO prova a dimensao 3, nem a H3 em toda tela e direcao, nem a identificacao do fluxo dual com um corpo.",
    "proximo_passo": "Revisao independente das duas pedras (quem construiu nao aprova); o operador nomeia e decide a instalacao numa versao. Decisoes da gerencia aplicadas (26/10/2026): chao = posto (nunca o infimo 0); IsotropicPost fica como hipotese NOMEADA (a isotropia e' carga: s8_h3_is_load_bearing); 1+3 e' leitura ONTO, a dimensao 3 nao e' provada.",
    "onde": os.path.join(W, "QuedaSemGeometria.lean"),
    "artefatos": [os.path.join(W, "QuedaSemGeometria.lean"), os.path.join(W, "audit_incremental_queda_log.txt")] + common_art,
    "refs": ["kernel.v401_falsidade_da_inercia", "formal.f2_3.curved_field_ligand", "kernel.ordem025.ponte_escala_dual"],
    "nota": "Consulta previa ao Mapa: queda (3 rotas sem relacao direta), esperanca condicional (1 rota, GKLS), isotropia (0), operador do nome/nameOp/relaxamento (0). Nao registrado: o registro e' da gerencia. Sandbox C:\\t\\k402\\final (copia de C:\\t\\k401c).",
}

recB = {
    "tipo": "ROTA",
    "rota_id": "kernel.v402_esperanca_condicional_e_nome",
    "dominio": "KERNEL_FORMAL",
    "titulo": "Pedra «esperanca condicional = nome» (TGLExt.EsperancaCondicional, nome provisorio): o Operador do Nome (nameOp) de rho* E a esperanca diagonal em M2(C); preserva o Um, reler nao acrescenta (mesma forma do observador), a compressao pelo espelho e' o Nome (Jones), indice 1/b condicional; composicao por citacao, em sandbox",
    "pergunta": "Ja se tipou no kernel a equacao do operador «esperanca condicional=nome»? O que existe e o que falta compor?",
    "dados": [
        os.path.join(CUN, "OPERADOR_26out_esperanca_condicional_e_nome_verbatim.txt"),
        os.path.join(CUN, "OPERADOR_26out_e_isso_faca_a_prova_prossiga_verbatim.txt"),
        "TGLExt/TheNameOperator.lean, PostoAdendo.lean, Posto.lean, CondExpect.lean, IALDJones.lean, IALD.lean, TheObserverReadsTheAngle.lean e TGL/NameIndex.lean, TGL/TransportData.lean do sandbox k402 (byte a byte iguais ao kernel do Nos v401)",
    ],
    "metodo": "Levantamento por grep do que ja existe (nameOp v162, A1c v392, CondExpect, NameIndex v27, IALDJones v371, IALD); composicao por citacao de name_op_unital/idem/fix_mul, A1c_nameOp_rhoStar_eq_diagExpect, diagExpect_bimod, eD_Lmul_eD, eTr_Lmul_eTr, name_index_eq_csc_sq, name_index_mul_sin_sq e observing_adds_nothing; forma comum RereadAddsNothing; lake build + auditoria incremental de axiomas no sandbox C:\\t\\k402\\final",
    "resultado": "Build completed successfully (9451 jobs); %s; %d #print axioms, todos no trio; fidelidade dos verbatins %d de %d por bytes. sha16 do .lean %s. A tipagem JA EXISTIA em grande parte (nameOp v162; A1c v392); o que se acrescenta e' a cláusula unica, a lei de Jones do Nome em M2 e o liame ao observing_adds_nothing. Nada instalado." % (cov(B), B["print_axioms_no_build"], B["fidelidade_verbatins"]["trechos_conferidos_como_substring_das_fontes"], B["fidelidade_verbatins"]["trechos_entre_aspas_distintos"], B["lean_sha16"]),
    "veredito": "PEDRA_ESPERANCA_CONDICIONAL_E_NOME_COMPILED_AND_PROVED_IN_SANDBOX__NOT_INSTALLED",
    "estatuto": "REAL (teoremas sobre as hipoteses explicitas); KNOWN (esperanca condicional: Umegaki, Tomiyama; Jones 1983; Pimsner-Popa 1986); INPUT (a equacao e as quatro linguas como letra da gerencia); ONTO (o Nome como o que a algebra do observador retem); LEGAL (ponteiro CC art. 125, a conferir); OPEN (instancia do contorno com sin2(theta_M) otimo; caso III1)",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": "O indice 1/b e' CONDICIONAL as duas hipoteses do kernel (hpp, hopt); nenhuma instancia e' construida (NameIndex). Nao se prova que toda esperanca condicional seja um nameOp (trExpect nao e'); a bimodularidade geral de nameOp p sobre os fixos nao esta tipada (so a de M2). Rotas mortas do Lema 3 (kernel.lema3.rotas_mortas, 20-23): [M:N]=sqrt(e) no vao de Jones, S_dpartial=log(indice) (Pimsner-Popa e' tracial II1), HSMI com vacuo unico sem esperanca normal nem indice (Lechner-Scotford): a pedra NAO e' rota para o Lema 3 e vive na face finita.",
    "nao_refazer": "O Operador do Nome (nameOp, v162) e a ponte A1c (nameOp rho* = diagExpect em M2) ja estavam no kernel; a pedra so os compoe com a lei de Jones, o indice e o liame ao observador. Nao refazer o levantamento nem reprovar a composicao.",
    "proximo_passo": "Revisao independente; o operador decide a instalacao numa versao. Decisao da gerencia aplicada (26/10/2026): o Nome e' nameOp (a esperanca condicional, o operador que le); o projetor de Jones e' a mesma coisa vista como projetor no GNS (eD_Lmul_eD); o posto e' o peso que ela preserva (E(1)=1): tres faces de um objeto fixo, nao tres definicoes. A bimodularidade geral de nameOp p e o caso III1 seguem abertos.",
    "onde": os.path.join(W, "EsperancaCondicional.lean"),
    "artefatos": [os.path.join(W, "EsperancaCondicional.lean"), os.path.join(W, "audit_incremental_esperanca_log.txt")] + common_art,
    "refs": ["quantica.inventario_gkls_um_py_kernel", "kernel.lema3.rotas_mortas", "formal.iald_o_motor_unico", "kernel.v402_queda_sem_geometria"],
    "nota": "Consulta previa ao Mapa: esperanca condicional (1 rota, GKLS), operador do nome/nameOp (0), Jones (3, uma delas as rotas mortas do Lema 3). Nao registrado: o registro e' da gerencia.",
}

records = [recA, recB]
with open(os.path.join(W, "registro_mapa_pedras_v402.json"), "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=1)
print("registro_mapa_pedras_v402.json escrito")

# validacao SEM gravar: usa as proprias regras do rotas.py
spec = importlib.util.spec_from_file_location("rotas_mod", r"C:\IALD\MAPA_DE_ROTAS\rotas.py")
rotas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rotas)
regs = rotas._parse(rotas._ler_bytes(rotas.LIVRO))
ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}
seqs = {r["seq"] for r in regs}
for rec in records:
    r = rotas._valida(dict(rec), ids, seqs)
    ids.add(r["rota_id"])
    print("VALIDO:", r["rota_id"], "| artefatos:", len(r["artefatos"]))
print("(nada foi gravado no livro; o registro e' da gerencia)")
