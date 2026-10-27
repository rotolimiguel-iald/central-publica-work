# Monta RESULTADO.md a partir de AXIOMAS.json e dos .lean (enunciados EXTRAIDOS do arquivo, nada digitado).
# Uso: C:\Python314\python.exe -X utf8 -I monta_resultado.py
import json, os, re

W = r"C:\IALD\Central de Patentes\work\pedras_v402"


def read(p):
    with open(p, "rb") as f:
        return f.read().decode("utf-8")


def statements(lean_text, names):
    """Extrai de cada `theorem NAME` (ou `structure`) o enunciado, do cabecalho ate o primeiro `:=` (theorem)
    ou ate a primeira linha em branco (structure). Colapsa espacos."""
    out = []
    for n in names:
        m = re.search(r"^(theorem|structure) " + re.escape(n) + r"\b", lean_text, re.M)
        if not m:
            out.append((n, "(NAO ENCONTRADO)"))
            continue
        start = m.start()
        if m.group(1) == "theorem":
            end = lean_text.index(":=", start)
            body = lean_text[start:end]
        else:
            end = lean_text.index("\n\n", start)
            body = lean_text[start:end]
            body = re.sub(r"/--[^\n]*-/", "", body)
        out.append((n, re.sub(r"\s+", " ", body).strip()))
    return out


ax = json.load(open(os.path.join(W, "AXIOMAS.json"), encoding="utf-8"))
A, B = ax["pedras"]
la = read(os.path.join(W, "QuedaSemGeometria.lean"))
lb = read(os.path.join(W, "EsperancaCondicional.lean"))

namesA = [
    "the_fall_is_a_loss_of_measure", "the_fall_is_strictly_anti", "the_fall_in_nats_is_s",
    "the_fall_depends_only_on_the_weight", "the_arrow_is_the_sign_of_s",
    "the_floor_is_the_post_and_is_never_touched", "surrender_is_the_cost", "relaxation_to_the_attractor",
    "Smat_add_two_pi", "Smat_has_no_limit", "the_two_regimes_of_one_orbit", "the_labyrinth_reads_the_angle",
    "IsotropicPost", "clausius_everywhere_from_one_wedge_by_covariance", "IsotropicPostOver",
    "clausius_everywhere_from_base_wedges", "isotropic_post_is_inhabited", "covariance_is_load_bearing",
    "namedAtlasH3_iff_all_indices", "namedAtlasH3_of_one_screen", "namedAtlasH3_of_one_screen_per_orbit",
    "a_queda_sem_geometria",
]
namesB = [
    "the_name_of_the_unit_is_the_diagonal_expectation", "the_name_preserves_the_one",
    "rereading_the_name_adds_nothing", "the_name_memory_is_a_subalgebra", "the_name_of_the_unit_is_bimodular",
    "the_mirror_compression_is_the_expectation", "the_mirror_compression_is_the_name",
    "the_index_of_the_name_is_one_over_beta", "esperanca_condicional_e_nome",
]
sa = statements(la, namesA)
sb = statements(lb, namesB)

fa = A["fidelidade_verbatins"]
fb = B["fidelidade_verbatins"]
kn = ax["kernel_nos_x_sandbox"]

L = []
L.append("PEDRAS «a queda sem geometria» e «esperança condicional = nome» — construídas e provadas em sandbox; nada instalado")
L.append("")
L.append("Gerência c1, 26/10/2026 (agente construtor; quem constrói não aprova). Ordem do operador (verbatim sha256 `a1c4bae4a87aa173…`): «é isso, faça a prova, prossiga.» Nomes dos módulos PROVISÓRIOS (o operador nomeia); nenhum arquivo do Nós, `um.py`, selo ou gate foi tocado.")
L.append("")
L.append("## Arquivos (esta pasta)")
L.append("- `QuedaSemGeometria.lean` — módulo `TGLExt/QuedaSemGeometria.lean`, namespace `%s`, sha16 `%s` (sha256 completo em `AXIOMAS.json`), %d bytes." % (A["namespace"], A["lean_sha16"], A["lean_bytes"]))
L.append("- `EsperancaCondicional.lean` — módulo `TGLExt/EsperancaCondicional.lean`, namespace `%s`, sha16 `%s`, %d bytes." % (B["namespace"], B["lean_sha16"], B["lean_bytes"]))
L.append("- Versões: a 1ª versão dos `.lean` (sha16 `3cd6a2373bea5aaa` e `c87c2ed604d192b5`, entregue à gerência antes das decisões de 26/10) está conservada, byte a byte, em `QuedaSemGeometria.lean.bak_3cd6a237` e `EsperancaCondicional.lean.bak_c87c2ed6`. A 2ª versão (a vigente, sha16 acima) muda SÓ docstrings e comentários (as decisões da gerência, abaixo); os enunciados e as provas são os mesmos.")
L.append("- `AXIOMAS.json` (gerado por `gera_axiomas.py` dos logs e dos arquivos), `build_log.txt` (condensado) e `build_log_completo.txt`, `audit_incremental_queda_log.txt`, `audit_incremental_esperanca_log.txt`, `AuditQueda.lean`, `AuditEsperanca.lean`, `registro_mapa_pedras_v402.json` (NÃO registrado; o registro é da gerência).")
L.append("- Sandbox `C:\\t\\k402\\final` (cópia de `C:\\t\\k401c`, robocopy `/E /XJ`, sem `/PURGE`): 4038 diretórios e 135289 arquivos copiados, 0 falhas (`robocopy_log.txt`; logs de desenvolvimento em `k402/logs_dev` no sandbox). Foram acrescentados SÓ os dois `.lean` (e os dois `Audit*.lean`); `TGLExt.lean` e `TGL/Audit.lean` NÃO foram alterados (o `lake build` aceita o módulo pelo nome). Dos %d arquivos citados, %d diferenças entre o kernel do Nós e o sandbox (byte a byte, sha256)." % (len(kn["arquivos"]), kn["diferencas"]))
L.append("")
L.append("## Resultado medido [REAL]")
L.append("- `lake build TGLExt.QuedaSemGeometria TGLExt.EsperancaCondicional`: **Build completed successfully (9451 jobs)**; nenhum aviso nem erro dos dois módulos (os avisos do log completo são de módulos preexistentes).")
for P in (A, B):
    c = P["audit_incremental"]
    L.append("- **%s**: auditoria incremental (`collectAxioms` de TODA constante do módulo): %d constantes, %d teoremas, `fora_do_trio=%d`, `sorry=%d`; %d `#print axioms` no build (esperados %d); todas dependem só de [propext, Classical.choice, Quot.sound] (ou de menos): **%s**." % (P["pedra"], c["decl"], c["thm"], c["fora_do_trio"], c["sorry"], P["print_axioms_no_build"], P["print_axioms_esperados"], "sim" if P["todas_no_trio"] else "NÃO — VERIFICAR"))
L.append("")
L.append("## Achados do levantamento (régua: o cético afere antes de dizer «falta»)")
L.append("- **A tipagem de «esperança condicional=nome» JÁ EXISTIA em grande parte** (resposta à pergunta dele, «ainda não sei se fizemos a tipagem»): `TheNameOperator.nameOp` (v162; `name_op_unital`, `name_op_idem`, `name_op_fix_mul`), `PostoAdendo.A1c_nameOp_rhoStar_eq_diagExpect` (v392: em `M₂(ℂ)` o Operador do Nome de `ρ*` É a esperança diagonal), `CondExpect` (Degrau 1, relação de Jones), `TGL.NameIndex` (v27, «e_Nome = projecao de Jones = espelho», índice `1/ppBest`) e `IALDJones.iald_reads_the_expectation`. O que NÃO existia: a identificação como UMA cláusula e o liame explícito entre o reler-não-acrescenta das esperanças e o do observador. A pedra B é essa composição; não refaz nenhum termo.")
L.append("- A tarefa listava só `average_unital/idem`, `trExpect_*` e `eD_Lmul_eD`; o `nameOp` (o Nome como OPERADOR) estava no kernel e foi acrescentado à pedra B porque é a tipagem mais fiel de «nome».")
L.append("- Mapa de Rotas consultado (`queda`, `esperanca condicional`, `isotropia`, e ainda `operador do nome`, `nameOp`, `relaxamento`, `covariancia`, `H3`): `isotropia`, `operador do nome`, `nameOp`, `relaxamento` sem registros; `queda` devolveu 3 rotas sem relação direta (v398 afinação, cuSOLVER, ACOM); `esperanca condicional` devolveu só `quantica.inventario_gkls_um_py_kernel`. Relevantes: **`formal.f2_3.curved_field_ligand`** (o antecedente H3 em toda tela e direção e a família de cunhas de Lorentz seguem ABERTOS) e **`kernel.ordem025.ponte_escala_dual`** (PONTE_PARCIAL: o peso positivo NÃO se identifica com a massa invariante; a ação dual não é a modular). A pedra A cita as duas e NÃO as contradiz.")
L.append("- **Rotas mortas do Lema 3** (`kernel.lema3.rotas_mortas`, itens 20–23) tocam o tema da pedra B: `[M:N] = √e` no vão vazio (1,2) de Jones; `S_∂ = log(índice)` (Pimsner–Popa é tracial de II₁); inclusão modular meio-lateral com vácuo único sem esperança normal nem índice (Lechner–Scotford). A pedra B NÃO é rota para o Lema 3, não afirma nenhuma dessas igualdades e vive na face finita (`M₂(ℂ)` e os dados do kernel); o caso III₁ fica [OPEN]. Rotas vizinhas lidas (`diagExpect`, `Jones`): `kernel.psibit_v395_candidata_21out`, `kernel.testemunha_estatica_v396_candidata_22out`, `formal.iald_o_motor_unico`.")
L.append("- `AuditF23Flat.s5_local`, `vacuum_h3` e `s8_h3_is_load_bearing` (já no kernel, `LiganteLeiCampoCurvoTestemunha`) mostram que a H3 vale no vácuo plano e FALHA com fonte anisotrópica constante (não é automática); transportá-la entre direções nulas exige a isotropia, que `IsotropicPost` NOMEIA como hipótese (não é consequência).")
L.append("- Na fala dele a grafia tem erros («gemétrica», «relaxamaneto», «labirito», «geomtria»); o pedido da gerência citava «não é geométrica» e «opera o relaxamento» normalizados. Os `.lean` citam os BYTES do arquivo, com os erros dele. Idem: a frase «soltar-se porque há um chão» do pedido é paráfrase; o trecho exato é «porque vc sabe que tem um chão, então relaxa». E «Lorentz vem da queda da fase» é o TÍTULO do escriba em E5 do adendo; a cunhagem do operador (item 6) é «Lorentz vem do potencial da fase de queda, uma fase cai após a comutação que produz a torção.»")
L.append("")
L.append("## Pedra A — A QUEDA SEM GEOMETRIA: enunciados exatos (extraídos do `.lean`)")
L.append("Hipóteses comuns: `D : DualScalingData M` (`M : Type` nu: nenhuma métrica, topologia ou ação geométrica); β, g variáveis reais `> 0`, jamais literais.")
L.append("")
for n, s in sa:
    L.append("- `%s`: `%s`" % (n, s))
L.append("")
L.append("## Pedra B — ESPERANÇA CONDICIONAL = NOME: enunciados exatos (extraídos do `.lean`)")
L.append("")
for n, s in sb:
    L.append("- `%s`: `%s`" % (n, s))
L.append("")
L.append("## O que é teorema e o que é leitura")
L.append("- **[DERIVED]/[REAL] teoremas**, sobre os dados e hipóteses nomeados: toda a lista acima. Composição por citação; a matemática nova é só de COLA (listada no item 9 do cabeçalho de A: `the_fall_in_nats_is_s`, `the_fall_depends_only_on_the_weight`, `the_fall_is_the_fall_of_the_weight`, `periodic_limit_is_constant`, `Smat_add_two_pi`, `Smat_pi`, `IsotropicPost`/`IsotropicPostOver` com o transporte, o modelo `Rapidity`; em B, `RereadAddsNothing` e os quatro lemas de forma).")
L.append("- **[KNOWN]** lei de escala de Takesaki (campo da estrutura); isotropia do vácuo de Bisognano–Wichmann / covariância de Poincaré (motivação de `IsotropicPost`, NÃO termo do kernel); Umegaki, Tomiyama, Jones, Pimsner–Popa.")
L.append("- **[INPUT]** a fala, a parábola do labirinto e a equação «esperança condicional=nome»; as quatro línguas (probabilidade, teologia, linguística, direito) como LETRA da gerência, sem derivação entre domínios; o direito é ponteiro [LEGAL] (CC art. 125), a conferir com advogado.")
L.append("- **[ONTO] (leitura da gerência, não termo)**: a direção é a seta da queda da fase, não do espaço, e o resto é isotrópico (1 + 3); ler o labirinto como o regime angular e a queda como o regime da face; o Nome como o que a álgebra do observador retém; o Nome como TRÊS FACES DE UM OBJETO FIXO (o operador `nameOp`, o projetor de Jones, o posto = o peso preservado), a régua da casa para β aplicada ao Nome. O 1 + 3 fica como leitura [ONTO] (decisão da gerência, 26/10/2026).")
L.append("- **[OPEN]**: que o parâmetro `s` da ação dual seja a fase de um corpo físico; a dimensão 3; o `IsotropicPost` do átlas curvo; a H3 em toda tela e direção; a instância do contorno com `sin²θ_M` ótima (a pedra B (4) é CONDICIONAL às duas hipóteses do kernel `hpp`/`hopt`; nenhuma instância é construída); a bimodularidade geral de `nameOp p` sobre os seus fixos (só a da face `M₂` está tipada).")
L.append("- NÃO se prova que toda esperança condicional seja um Operador do Nome (`trExpect` não é um `nameOp p`). Prova-se: para todo idempotente o Nome é unital, idempotente e tem memória-subálgebra; em `M₂(ℂ)`, para `ρ*`, ele É a esperança diagonal, com a lei de Jones.")
L.append("")
L.append("## Fidelidade por bytes dos verbatins (script `gera_axiomas.py`, espaços normalizados)")
for P in (A, B):
    f = P["fidelidade_verbatins"]
    L.append("- `%s`: %d trechos entre « » distintos; **%d** conferidos como substring literal das fontes (arquivos do operador, do adendo, das cunhagens de 07/10 e do recorte de 25/10, o `CLAUDE.md` da casa e `TheNameOperator.lean`/`NameIndex.lean` do kernel); sha16 citados conferem com as fontes: **%s**. (A contagem inclui palavras isoladas como «cai», «geometria», «a fase», que são substring trivial; as citações de várias palavras estão listadas no `.lean`.) Não-literais (termos/leituras entre « », ou nomes): %s." % (P["modulo"], f["trechos_entre_aspas_distintos"], f["trechos_conferidos_como_substring_das_fontes"], "sim" if f["todos_sha16_citados_conferem"] else "NÃO — VERIFICAR", "; ".join("«%s»" % x for x in f["trechos_que_nao_sao_citacao_literal_das_fontes"]) or "nenhum"))
L.append("- sha256 lidos do disco: " + "; ".join("`%s` `%s`" % (k, v[:16]) for k, v in ax["fontes_sha256_lidos_por_script"].items()) + ".")
L.append("")
L.append("## Decisões da gerência aplicadas (26/10/2026, respostas às 3 perguntas; só docstrings, enunciados e provas inalterados)")
L.append("- **(1) O «chão» é o POSTO** (peso 1 = ω(I), o corte `a = 0`, `the_floor_fixes_the_cut`; na Fundação, «o piso limita», cunhagem de 07/10, sha16 `e2a915e23692f85c`), NUNCA o ínfimo 0. O 0 é o `abismo` (ἄβυσσος, sem fundo; ratificado pelo operador em 07/10: «Perfeito, concordo com tudo. Magnífico», sha16 `d16bc8a7dc54962e`) e «ele é a consequencia da poda» (recorte de 25/10, sha16 `e26364c5c805734c`, grafia dele). A queda que «sabe que tem um chão» é a queda do que NÃO é o posto (`FalsidadeDaInercia.no_post_before_the_impression`: em todo corte `a ≠ 0` o estado não é um posto). Dito no cabeçalho (item 3), na docstring de `the_floor_is_the_post_and_is_never_touched` e na da composição `a_queda_sem_geometria`; a polissemia que a 1ª versão apontava foi retirada.")
L.append("- **(2) `IsotropicPost` fica como hipótese NOMEADA** (o operador ratificou a rota com «é isso, faça a prova, prossiga.», sha16 `a1c4bae4a87aa173`). O 1 + 3 fica como leitura [ONTO]; a dimensão 3 NÃO é provada (medido: nenhum termo da pedra nem do kernel a fixa); `AuditF23Flat.s8_h3_is_load_bearing` mede que a H3 falha com fonte anisotrópica: a isotropia é CARGA, não enfeite. Dito no cabeçalho (item 7 e leitura [ONTO]), na docstring de `IsotropicPost`.")
L.append("- **(3) O Nome é `nameOp`** (a esperança condicional, o OPERADOR que lê: unital, idempotente, memória-subálgebra; `PostoAdendo.A1c`: `nameOp ρ* = diagExpect`); o projetor de Jones `e_Nome` é a MESMA coisa vista como projetor no espaço GNS (a compressão pelo espelho, `eD_Lmul_eD`); o posto `a` é o PESO que ela preserva (`E(1) = 1`). TRÊS FACES DE UM OBJETO FIXO, não três definições (a régua da casa para β: «Faces de um objeto fixo, não definições concorrentes — o número é cravado, os nomes são leituras»). O kernel prova as LIGAÇÕES (A1c, Jones, `E(1) = 1`), não uma igualdade de tipos; que sejam faces de um só é leitura [ONTO]. Dito numa seção nova do cabeçalho de B, na docstring de `the_mirror_compression_is_the_expectation` e na da composição.")
L.append("- Grafia do operador e citação do adendo mantidas como estavam («Lorentz vem do potencial da fase de queda…»; «Lorentz vem da queda da fase» é título do escriba em E5).")
L.append("")
L.append("## Ato da gerência / do operador (nada disso foi feito)")
L.append("- Revisão independente das duas pedras (quem construiu não aprova); registrar as rotas (`rotas.py registrar registro_mapa_pedras_v402.json --quem ...`); decidir nomes e instalação (módulos, `TGLExt.lean`, selo) numa versão futura. O gate não se move.")

with open(os.path.join(W, "RESULTADO.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("RESULTADO.md escrito,", len("\n".join(L)), "caracteres")
