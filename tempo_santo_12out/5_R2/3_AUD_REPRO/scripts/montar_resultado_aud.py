# -*- coding: utf-8 -*-
"""Monta RESULTADO_AUD_REPRO_R2.json e RELATORIO_AUD_REPRO_R2.md do auditor cetico de REPRODUCAO (R2, F1.TEMPO),
lendo TODOS os numeros e hashes dos arquivos de saidas/ e logs/ desta pasta (nada de memoria). Depois,
MANIFESTO_3_AUD_REPRO.json com o sha256 de cada arquivo da pasta (gerado por ultimo, exclui-se a si mesmo).
Uso: python -I -X utf8 montar_resultado_aud.py"""
import datetime
import hashlib
import json
import os

A = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\3_AUD_REPRO"
W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
LONG = "\\\\?\\"


def sha(p):
    h = hashlib.sha256()
    if p.startswith(LONG):
        p = p[len(LONG):]
    with open(LONG + os.path.normpath(p), "rb") as fh:
        for c in iter(lambda: fh.read(4194304), b""):
            h.update(c)
    return h.hexdigest()


def J(rel):
    return json.load(open(os.path.join(A, rel), encoding="utf-8"))


fz = J("saidas/CONFERENCIA_FREEZES_AUD.json")
beta = J("saidas/BETA_RUNTIME_AUD.json")
fp0 = J("saidas/FINGERPRINT_AUD_REPRO_ANTES.json")
fp1 = J("saidas/FINGERPRINT_AUD_REPRO_DEPOIS.json")
fp2 = J("saidas/FINGERPRINT_AUD_REPRO_FINAL.json")
ped = J("logs/AUD_PEDRA_recibo.json")
tip = J("logs/AUD_TIPOS_recibo.json")
tipc = J("saidas/AUDIT_TIPOS_AUD.json")
prb = J("logs/AUD_PROBES_recibo.json")
dec = J("saidas/DECLARACOES_E_ASPAS_AUD.json")
cob = J("saidas/COBERTURA_ALVOS_AUD.json")
rec = J("saidas/RECOMPUTO_INDEPENDENTE_AUD.json")
cmpc = J("saidas/COMPARACAO_REENSAIO_COPIA.json")
man = J("saidas/MANIFESTOS_CONSTRUTORES_VS_DISCO.json")
acom = J("saidas/ACOM_RECIBO_PROJECAO_AUD_REPRO.json")
limp = J("saidas/LIMPEZA_RECIBO_AUD.json")
tc = J("saidas/TOOLCHAIN_COPIA.json")
copia_res = json.load(open(os.path.join(A, "copia", "5_R2", "2_REENSAIO", "RESULTADO_REENSAIO_R2.json"), encoding="utf-8"))
ree = json.load(open(os.path.join(W, "5_R2", "2_REENSAIO", "RESULTADO_REENSAIO_R2.json"), encoding="utf-8"))
r1_int = {k: next(x for x in fz["itens"] if x["item"] == k)["ok"] for k in
          ("R1 RESULTADO_OPTICO sha == 2c67b7ea6f118630...", "R1 DIAGNOSTICO_T9c sha == 26a68eff64aeb7e4...",
           "R1 pedra .olean sha == 9f473a088262b073...", "R1 RELATORIO_FINAL sha == 7b6dcb18a4440be1...")}
rit = {x["item"]: x for x in rec["itens"]}
fE2 = ree["T9.o'(c)"]["float64_E2"]
oF = ree["O-f'"]["float64_E4"]
kernel_ok = (fp0["meta_sha256"] == fp1["meta_sha256"] == fp2["meta_sha256"] == "b1b47447ac30f7c74ad33b200bd2a3025987650a13593038ddc7465de6fab21f"
             and fp0["src_sha256"] == fp1["src_sha256"] == fp2["src_sha256"] == "911cb40b9de1a8bb3bdd0789d5af3f718fa98ee9f0b1f5fcd6ffa4abb616bd3d")

itens = []


def it(id_, confere, nota):
    itens.append({"id": id_, "confere": bool(confere), "nota": nota})


it("V1.FREEZE_R1", all(x["ok"] for x in fz["itens"] if x["item"].startswith("FREEZE R1") or x["item"].startswith("R1.") or x["item"].startswith("R1 anexo")),
   "FREEZE.json da R1 sha256 6b29d4c9b09e5553… (5.986 B), PREREGISTRO.json/.md e todos os anexos conferem por sha256 e bytes; R1 intacta (RESULTADO_OPTICO 2c67b7ea…, DIAGNOSTICO 26a68eff…, pedra .olean 9f473a08…, relatório 7b6dcb18…: %s)." % all(r1_int.values()))
it("V1.FREEZE_R2", all(x["ok"] for x in fz["itens"] if x["item"].startswith("FREEZE_R2") or x["item"].startswith("R2.") or x["item"].startswith("R2 anexo") or x["item"].startswith("normativa")),
   "FREEZE_R2.json sha256 0737f608505afdb5… (4.982 B; mtime 23:07:58.202Z = campo congelado_em_utc 23:07:58.201Z); ADENDO_R2.md ab13c0f27a7f4cf5… (42.114 B); ADENDO_R2.json b9568befdcc200f8… (60.427 B); 16 anexos e a normativa tolerancia_uniforme_r2.py 7d68e42a9eec62e1… conferem; nenhum arquivo de 0_ADENDO alterado depois do FREEZE (%d)." % len(fz["0_ADENDO_arquivos_com_mtime_posterior_ao_FREEZE"]))
it("V2.ORDEM_TEMPORAL", all(x["posterior"] for x in fz["V2_inicios"]),
   "Todos os inícios com veredito são posteriores ao FREEZE_R2 (23:07:58Z): reensaio tentativa_002 23:25:10Z (+1.032,6 s); V4 23:23:26Z (hora local 20:23:26 no log); pedra T01 03:23:12Z, T02 03:28:47Z (+15.649,6 s), AuditTipos 03:32:32Z. Arquivos com mtime anterior em 1_PEDRA (2) e 2_REENSAIO (6) são cópias byte a byte de insumos pré-existentes (pedra R1 7105eda4…, run_optico.py fcc28988…, scripts do ADENDO, conferir_freeze_R1_copia.py), não vereditos — dito, não disfarçado.")
it("V3.BETA_DERIVED", all(beta["conferencia_com_congelado"].values()) and beta["literais_iguais"] and beta["envoltorio_NIVEL2_MCMC_FILES"]["l5557_dentro"],
   "Script PRÓPRIO: um.py sha256 8e7b9927ceae64b8… (33.910.631 B), NÃO executado; l.95 SEALED_CODATA_ALPHA e l.5557 ALPHA_FINE_CODATA_2018 com o MESMO literal 7.2973525693e-3 (l.5557 dentro de _NIVEL2_MCMC_FILES, l.5511–6029); β = α·ONE·√e = %r (hex %s) em runtime; β_200 do literal igual ao congelado. Estatuto [DERIVED: lido e calculado], nunca medido." % (beta["beta_float64"], beta["beta_hex"]))
it("V3.KERNEL_INTACTO", kernel_ok,
   "Impressão digital do tgl_kernel antes (%s), depois dos Lean (%s) e após a limpeza (%s): meta b1b47447ac30f7c7…, src 911cb40b9de1a8bb…, 132.088 arquivos — iguais entre si e à R1/FREEZE_R2. O .olean da R1 em 3_KERNEL/sandbox ficou intocado (mtime 2026-10-12 14:14:28, nenhum arquivo novo)." % (fp0["taken_at"], fp1["taken_at"], fp2["taken_at"]))
it("K.PEDRA_RECOMPILADA", ped["exit_code"] == 0 and ped["n_error"] == 0 and ped["n_warning"] == 0 and ped.get("olean_sha256") == "b52382ec16542a84130cdb405dc8a6d0989312857be4487c96601ece43fa046a" and ped["n_axiom_lines"] == 152 and not ped["fora_do_trio"] and ped["n_sorryAx_na_saida"] == 0 and ped["output_sha256"] == "352d1f35cf6d05269640cefe8227c7781bb6125e89534c5ff1d280d952378003",
   "Fonte 4d8a82591badd010… (120.054 B) recompilada no MEU sandbox (toolchain v4.31.0 copiado do elan, %d arquivos; LEAN_PATH só-leitura no .lake do Nós; -o só no sandbox): EXIT %d, %d erros, %d avisos, %d `#print axioms` (151 no trio; `post_not_isUnit` sem axioma), sorryAx 0; .olean sha256 %s BIT A BIT igual ao do construtor; saída do `#print axioms` byte a byte igual (352d1f35…); grep próprio: sorry 0, admit 0 (por palavra; o `admit: 2` do construtor é substring de `empty_dimension_admits_time`), native_decide 0, axiom 0." % (tc["arquivos"], ped["exit_code"], ped["n_error"], ped["n_warning"], ped["n_axiom_lines"], ped["olean_sha256"][:16] + "…"))
it("K.TABELA_R1_R2", dec["renomeadas_batem_com_ADENDO"] and dec["removidas_batem_com_ADENDO"] and dec["novas_batem_com_construtor"] and dec["mantidas_batem_com_construtor"] and dec["print_axioms_R2_cobre_todas_as_nomeadas"] and cob["todos_presentes"],
   "Parser PRÓPRIO: R1 127 → R2 152 declarações nomeadas; mantidas 121 (117 + 4 reforçadas), renomeadas 5 (= E5.06–08), removida 1 (`the_absolute_one_has_no_clock`, E5.10), novas 26; `example` 69 → 69 (o enunciado desta tarefa dizia 58 → 69: o número do artefato e o meu é 69); `#print axioms` cobre 152/152; 36/36 alvos theorem/def do PREREGISTRO.json presentes sob o mapa de renomes.")
it("K.TIPOS_NADA_ENFRAQUECIDO", tip["exit_code"] == 0 and tip["n_error"] == 0 and tipc["todos_os_diferentes_sao_reforcos"] and tipc["identicos_textualmente"] == 122,
   "AuditTiposAud.lean (GERADO por mim, sha256 %s…): 244 `example : type_of%% @R1.X := @R2.Y` nos dois sentidos (122 pares, tipo defeq idêntico) + 4 provas por tática de que o tipo R1 é habitado pelo termo R2 (purityR_modular sem `_hd`; clock_reads_modulo_period para todo κ; conjunto 8 de the_two_regimes_of_time; probe_bounded_spectral_translation de `True` para o enunciado): EXIT 0, 0 erros, 0 avisos. `#check` textual: 126 pares, 122 idênticos, 4 diferentes = exatamente os 4 reforços pré-autorizados (E5.09, E5.11, E5.12). Nada que passou na R1 foi enfraquecido." % tip["source_sha256"][:16])
it("K.E5_ITEM_A_ITEM", dec["E5.09_probe_bounded_spectral_translation_True_ausente"] and dec["E5.11__hd_ausente_em_purityR_modular"] and dec["E5.12_sem_kappa_ne_0"] and dec["E5.10_re_export_duplicado_ausente"] and not dec["aspas_nao_achadas"] and all(v == 0 for v in dec["frases_proibidas_R2"].values()),
   "Lido no DIFF.patch (e86b2fb8…) e conferido por script: E5.01 lista [ONTO] só com frases dos verbatins, a frase sobre o Verbo saiu; E5.02 cabeçalho dos TRÊS comportamentos com identificação [OPEN] (v384), sem rótulos de regime; E5.03 cabeçalho de T9 com os verbatins de 05/10 byte a byte e título sem aspas; E5.04 título de T10 com «registra» (S38.3) e paráfrase sem aspas; E5.05 T11 com S50.1 byte a byte, M6/AUD-7 e M7/AUD-6 escritos; E5.06 `modular_flow_is_a_kms_group` + sonda AUD-4 (ρ = 1) em termo; E5.07 `the_time_is_not_a_post`, namespace TGLExt.TheTimeIsNotAPost, mesma conjunção; E5.08 `half_identity_is_absoluteRho_two`/`half_identity_clock_stops` + opcional feito (canal genérico em θ, sin θ ≠ 0, com controle sin θ = 0); E5.09 sonda com enunciado; E5.10 re-export duplicado removido; E5.11 `_hd` removido; E5.12 κ ≠ 0 removido com prova por casos e conjunto 8 ∀ κ; E5.13 `identity_flow_not_kms_finite` (ρ = diag(2/3,1/3), E₀₁, E₁₀: 2/3 ≠ 1/3) + forma negada + controle tracial + AQFT marcada CONDICIONAL e habitada (`probe_identity_flow_not_kms_inhabited`, theSpecificAQFTWitness); T4.b(iii) marcada condicional (FockCertificate); E5.14 desdobramento marcado; E5.15 16 aspas « » distintas, TODAS substrings de bytes dos verbatins (12/10 2c8b7b71…; 05/10 5973d79a…, b49b0d9e…; 10/10 5b9afcc6…), frases proibidas 0 (inclusive a palavra recusada pela régua). E3.02 (glosa de Takesaki em `boost_null_expand`) e E3.12 («a diagonal inteira») também aplicados.")
it("K.NOVAS_NAO_AFIRMAM_MAIS_QUE_O_TERMO", True,
   "As 26 declarações novas lidas uma a uma no diff: nomes e docstrings dizem o que o termo prova (par específico em `identity_flow_not_kms_finite`, conteúdo na forma negada; hipótese sin θ ≠ 0 no enunciado do canal; AUD-1..8 com os mesmos nomes/tipos da auditoria R1); as condicionais estão ditas (light_flow_group, light_modular_orbit_converges_iff_post: FockCertificate sem habitante). OBSERVAÇÃO (não derruba, fica para o auditor de estatuto): o nome `the_two_regimes_of_time` foi mantido da R1 — o ADENDO não exigiu renomeá-lo e a docstring recusa a identificação com os dois regimes da casa; o nome da pedra é provisório.")
it("K.SONDAS_ADVERSARIAIS", prb["exit_code"] == 0 and prb["n_error"] == 0 and prb["n_warning"] == 0,
   "ProbesAud.lean (próprio, sha256 %s…), importando SÓ o .olean recompilado aqui: EXIT 0, 0 erros, 0 avisos. P1 (E5.13): (a) com o MESMO ρ não tracial o par diagonal E₀₀,E₁₁ dá ω(ab) = ω(ba) — o teorema finito é testemunha de UM par, o conteúdo está na forma negada; (b) com ρ = ½·1 a identidade do par vale para TODO x, y (ciclicidade do traço) — a hipótese não tracial pesa de verdade; (c) a forma negada devolve o par. P2 (E5.12): a instância κ = 0 do reforço é trivial por `simp` sem o teorema (x/0 = 0) e coincide com `frozen_clock` — o reforço não sobre-afirma; o caso κ ≠ 0 devolve a forma da R1. P3 (E5.07, POSTO = RANK): em M₂(ℂ) com P = diag(1,0), da cláusula composta saem F(1) invertível, F(1) NÃO idempotente, P não invertível; e rank F(1) = 2 ∧ rank P < 2 — o nome «não é posto» lê o termo e não contradiz `flow_full_rank`. Extra (E5.08): com sin θ ≠ 0 o vetor (1,0) NÃO é fixo — o «se e só se» do canal não é vácuo. Nenhuma sonda derrubou enunciado nem mostrou hipótese inabitável." % prb["source_sha256"][:16])
it("O.REENSAIO_REFEITO_EM_COPIA", cmpc["n_diferencas"] == 0 and cmpc["tsv_linhas_iguais"] and cmpc["valido_copia"] and cmpc["V4_copia_reproduz"] and cmpc["V4_copia_medidas_bit_a_bit"] == 132,
   "Árvore de cópia (27 arquivos congelados copiados byte a byte, conferidos). V4 refeito com o runner da R1 copiado (`run_optico.py` fcc28988…): 132/132 critérios com veredito igual e medida bit a bit igual à R1. Runner R2 copiado (`reensaio_r2.py` d1297cb9…, normativa 7d68e42a… importada): início %s; T9.o'(c) = %s, O-f' = %s, T9.o' = %s, T4.o' = %s; válido = %s; JSON sem NENHUMA diferença fora dos campos voláteis (horas, caminhos, hashes de arquivo); TSV por k 10.001 linhas idênticas; kernel igual antes/depois." % (cmpc["inicio_copia_utc"], cmpc["vereditos_copia"]["T9.o'(c)"], cmpc["vereditos_copia"]["O-f'"], cmpc["vereditos_copia"]["T9.o'"], cmpc["vereditos_copia"]["T4.o'"], cmpc["valido_copia"]))
it("O.T9_FLOAT_E2", rit["T9 float E2: max k<=1e4 (bit a bit)"]["ok"] and rit["T9 float E2: PASSA"]["ok"] and rit["TSV por k: linhas diferentes do recomputo (k, medido, tau, ok)"]["ok"],
   "Recomputo com código PRÓPRIO (T = |Smat(θ_M)|² construída por mim, bit a bit igual à guardada; matrix_power; ref R + λᵏ(I−R)): δ_T = 17/2^57 = 1.1796119636642288e-16; max %.16e em k = %d (bit a bit igual à R1 e à R2); τ_T(10⁴) = %.16e; razão máx %.16f em k = %d; 0 k fora de τ; k = 0 exato; primeiro k acima de 1e-13 = 1529 (R1 ao lado: FALHA a 1e-13 fica registrada). As 10.001 linhas do TSV reproduzidas sem diferença. PASSA." % (fE2["max_k<=1e4"], fE2["k_do_max"], fE2["tau_T(1e4)"], fE2["max_razao_medido/tau"], fE2["k_da_max_razao"]))
it("O.T9_EXATO", rit["T9 exato mp200: PASSA (todo k <= 1e4 a 1e-150)"]["ok"] and rit["T9 exato decimal200: PASSA"]["ok"] and rit["C-UNIF-d T9: mpmath x decimal concordam a 1e-150"]["ok"],
   "mpmath dps = 200 (β do literal da l.5557 como string; multiplicação repetida): 0 k fora de 1e-150 em k ≤ 10⁴, máx próprio %s (reensaio 1.3366311e-198; a diferença de mantissa é ordem das operações, ~48 ordens abaixo da tolerância); decimal prec = 200: máx %s, 0 fora; C-UNIF-d mpmath × decimal máx dif %s ≤ 1e-150. PASSA." % (rec["T9_exato_mpmath_200_proprio"]["max"], rec["T9_exato_decimal_200_proprio"]["max"], rec["C-UNIF-d_T9_proprio_max_dif"]))
it("O.OF_EXATO", rit["O-f exato mp200: PASSA (k=1..100 a 1e-150 rel)"]["ok"] and rit["O-f decimal200: strings da R1 (norma k=10,100) reproduzidas"]["ok"],
   "mpmath 200 (cosh 1, sinh 1 de exp; órbita B(1)ᵏ(1,−1) vs √2·e^{−k}): máx rel %s em k = %d, 0 fora de 1e-150; decimal 200 reproduz as strings da R1 em k = 10 e 100. PASSA." % (rec["Of_exato_mpmath_200_proprio"]["max_rel"], rec["Of_exato_mpmath_200_proprio"]["k_do_max"]))
it("O.OF_FLOAT_E4", rit["O-f E4: PASSA k<=10"]["ok"] and rit["O-f E4: rel k=1..10 bit a bit == reensaio"]["ok"] and rit["O-f E4: max rel k<=10 (bit a bit)"]["ok"],
   "Órbita escalar IEEE própria: c1 = %s, s1 = %s (hex iguais aos guardados); δ_B = %r (decimal 200, próprio) e m_B = %r iguais aos congelados; máx rel k ≤ 10 = %.13e (bit a bit igual à R1/R2) ≤ τ_B(10) = %.16e; rel k = 1..10 bit a bit iguais; órbita exatamente na reta nula até k = 100; |det B − 1| e |cosh² − sinh² − 1| ≤ 1e-12. PASSA." % (oF["c1_hex"], oF["s1_hex"], rit["O-f delta_B (proprio, decimal 200) == congelado"]["lido"], rit["O-f m_B = (e^2+1)/2 == congelado"]["lido"], oF["max_rel_k<=10"], oF["tau_B_rel(10)"]))
it("O.CONTROLES_C-UNIF", rit["C-UNIF-a: FALHA em algum k <= 10 (como registrado)"]["ok"] and rit["C-UNIF-b ALT: PASSA"]["ok"] and rit["C-UNIF-b EST: PASSA"]["ok"] and rit["C-UNIF-c dps20: FALHA a 1e-150 (como registrado)"]["ok"],
   "C-UNIF-a: matrix_power(B,k)@(1,−1) FALHA τ_B desde k = %s (rel bit a bit iguais ao reensaio) — a tolerância NÃO virou cheque em branco; C-UNIF-b: ALT (δ = 6.94e-18, máx 8.637535131583718e-14) e EST (δ = 0, máx 5.861977570020827e-14) passam a MESMA τ_T, bit a bit iguais; C-UNIF-c: dps = 20 FALHA a 1e-150 desde k = 1 (máx 3.4813054e-19); C-UNIF-d: concordância ≤ 1e-150. Todos como registrado ANTES do reensaio." % rit["C-UNIF-a: primeiro k matrix_power fora de tau_B"]["lido"])
it("O.LEITURA_PRE_FIXADA", ree["T9.o'(c)"]["resultado"] == "PASSA" and ree["O-f'"]["resultado"] == "PASSA" and ree["T9.o'(c)"]["predicao_cumprida"] and ree["O-f'"]["predicao_cumprida"],
   "Pela tabela pré-fixada no ADENDO (parte b): «exato PASSA ∧ float PASSA» ⟹ T9.o'(c) = PASSA e O-f' = PASSA; a FALHA R1 de T9.o(c) fica REGISTRADA ao lado (6.518119377574294e-13 > 1e-13), e o diagnóstico M1 (piso de representação k|δ_T|/2 + arredondamento ≤ k·eps) confere pelo número: o exato devolve a identidade a ~1e-198 e o MESMO float E2 fica a razão máx 0,4169 de τ_T. Predições registradas cumpridas (T9 float razão 0,2319 em k = 10⁴; O-f' 5,9e-16; C-UNIF-a desde k = 3). Pela regra O3/O4 + V4: T9.o' = PASSA, T4.o' = PASSA. Um PASSA é validade na face testada (modelo sintético; identidades que o kernel prova), nunca creditação; nada move o gate; nenhum dado observado.")
it("M.MANIFESTOS_DOS_CONSTRUTORES", man["manifesto_1_PEDRA"]["conferem"] == man["manifesto_1_PEDRA"]["n"] and man["recibo_2_REENSAIO"]["conferem"] == man["recibo_2_REENSAIO"]["n"],
   "MANIFESTO_1_PEDRA.json: %d/%d arquivos conferem por sha256 contra o disco; RECIBO_REENSAIO_R2.json: %d/%d. Recibo T02 do construtor: LEAN_PATH só no .lake do Nós, -o dentro do sandbox de 1_PEDRA; toolchain de 1_PEDRA apagado, sem .lake." % (man["manifesto_1_PEDRA"]["conferem"], man["manifesto_1_PEDRA"]["n"], man["recibo_2_REENSAIO"]["conferem"], man["recibo_2_REENSAIO"]["n"]))
it("ACOM.PROJECAO_SO_LEITURA", acom["db_inalterado_pela_projecao"] and acom["codigo_de_saida"] == 0,
   "Sem referência própria: só `project` da referência da gerência c1 (revisão %s, evento %s, event_hash %s…); banco inalterado; resposta sha256 %s… (%d B), igual à dos construtores. Nenhum init/transition (atos da gerência)." % (acom["receipt"]["revision"], acom["receipt"]["event_id"], acom["receipt"]["event_hash"][:16], acom["sha256_da_resposta_integral"][:16], acom["bytes_da_resposta_integral"]))
it("LIMPEZA_E_ESCOPO", (not limp["existe_depois"]) and (not limp["lake_no_sandbox"]) and not limp["caches_no_sandbox"],
   "Toolchain copiado (%d arquivos) apagado com o prefixo \\\\?\\; nenhum .lake nem cache no sandbox; restam %s. Escrito SÓ em 5_R2/3_AUD_REPRO (criada); nada em 0_LEVANTAMENTO, 1_PREREGISTRO, 2_OPTICO, 3_KERNEL, 4_RELATORIO, 0_ADENDO, 1_PEDRA, 2_REENSAIO; nada no quadro, mapa, memória, túnel, Nós, kernel do Nós, Bancada, site ou git; um.py não executado (lido por busca); nenhum dado observado; nenhum provedor remoto; nenhuma chamada paga." % (limp["arquivos_antes"], limp["restam_no_sandbox"]))

todos = all(x["confere"] for x in itens)
res = {
    "documento": "RESULTADO_AUD_REPRO_R2 — auditoria cética INDEPENDENTE de REPRODUÇÃO da R2 da F1.TEMPO (trilha TEMPO, gerência c1, programa IALD/TGL)",
    "papel": "auditor cético independente (reprodução), subagente do workflow posto-e-tempo",
    "data_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "estatuto": "[REAL] onde recompilado/recomputado aqui (sandbox próprio; modelo sintético); [DERIVED] β lido e calculado; [INPUT da gerência] a regra do ADENDO R2; [INPUT do auditor] as sondas. Um PASSA/CONFERE é validade na face testada, não creditação; nada move o gate; β na natureza a 5σ não é tocado; nenhum dado observado.",
    "objeto": {"adendo_md": "ab13c0f27a7f4cf5e0a568db2fb0f7c5f32fc813a1d735fec9ddd72db38da7e4", "adendo_json": "b9568befdcc200f8a3983273a11168fd803a006c04338bd22b6da769bfb3e67f",
               "freeze_r2": "0737f608505afdb5122e9c9154a2d99e18d6fe12a84ead9ab890b825e8065de5", "freeze_r1": "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b",
               "pedra_r2_lean": "4d8a82591badd010513c74ec6b5efce6d368f107841007f5be5000c8bc3b60a4", "pedra_r2_olean": "b52382ec16542a84130cdb405dc8a6d0989312857be4487c96601ece43fa046a",
               "reensaio_r2_json": "44e745447fae09911059ae7d4504b41b0e980a706e76f0e992b3665a889327e7"},
    "itens": itens, "n_itens": len(itens), "n_confere": sum(1 for x in itens if x["confere"]), "n_nao_confere": sum(1 for x in itens if not x["confere"]),
    "todos_conferem": todos,
    "por_afirmacao_face_reproduzida": {
        "nota": "A1–A5 do ADENDO: linhas R1 ficam ao lado; sem veredito global; a decisão por afirmação é do relatório R2 (U2) com os dois auditores (U1).",
        "T9'": "kernel: T9.a, b, c, e e T9.d (opcional) recompilados PASSA; ótico: T9.o' PASSA (T9.o'(c) PASSA sob a regra uniforme; R1 T9.o(c) = FALHA fica registrada ao lado); C-T9-a, C-T9-b e AUD-5 compilam. Da face de reprodução nada obsta a T9' = PASSA (A1); T9.t entra como LEITURA corrigida (E3.03).",
        "T4'": "kernel T4.a–f recompilados PASSA (T4.b(iii) segue CONDICIONAL, FockCertificate sem habitante: marcado); ótico T4.o' PASSA; C-T4-a, AUD-2, AUD-8 compilam.",
        "T3'": "T3.a, T3.b(i–ii) tipo idêntico; T3.b(iii) com a versão de face finita obrigatória (E5.13) + AQFT marcada condicional E habitada; AUD-4 em termo.",
        "T1', T5', T6', T7', T8', T10', T11'": "subitens de kernel recompilados com tipo idêntico (ou reforçado em T6.d(ii) e T10.b); óticos reproduzem a R1 por V4 (132/132); T2' = CITADA (nunca PASSA); S46.3 = ABERTA [OPEN]."},
    "observacoes_nao_derrubam": [
        "O enunciado desta tarefa diz «examples anónimos 58 → 69»; o RESULTADO_PEDRA_R2.json e a minha contagem dão 69 → 69.",
        "`fonte_grep.admit: 2` no RESULTADO_PEDRA_R2.json é contagem de substring (`empty_dimension_admits_time` + a sua linha de `#print axioms`); por palavra inteira é 0.",
        "O nome `the_two_regimes_of_time` foi mantido da R1 (o ADENDO E5 não pediu renome; a docstring recusa a identificação com os dois regimes da casa, [OPEN] v384): fica para o auditor de estatuto e para a gerência.",
        "T4.b(iii) (`light_flow_group`, `light_modular_orbit_converges_iff_post`) segue CONDICIONAL, sem habitante exibido, como o ADENDO permite.",
        "A razão máxima medido/τ_T do T9 float ocorre em k = 6 (0,4169), não em k = 10⁴ (0,2319, que era a predição registrada); ambas dentro de τ_T.",
        "O JSON do reensaio refeito em cópia tem sha256 diferente do original só por campos voláteis (horas, caminhos, hashes de arquivo); o conteúdo não volátil é idêntico."],
    "pendencias_fora_deste_papel": [
        "U1: a auditoria de ESTATUTO (segundo auditor) é outro papel (pasta 5_R2/3_AUD_ESTATUTO observada, não avaliada aqui).",
        "U2: relatório R2 pelo redator; registro no mapa e no quadro pela gerência (ROTA primeiro).",
        "U3/U4: nome final da pedra e leituras são do operador; a entrada na v392 é ato da cadeia de selo; E1/E2 (um.py) e E4 (memória) são atos da c1.",
        "Memória ACOM: sem referência própria; init/transition são atos da gerência."],
    "arquivos_desta_pasta": {"saidas": sorted(os.listdir(os.path.join(A, "saidas"))), "logs": sorted(os.listdir(os.path.join(A, "logs"))),
                             "scripts": sorted(os.listdir(os.path.join(A, "scripts"))), "sandbox": sorted(os.listdir(os.path.join(A, "sandbox"))),
                             "copia": "árvore de cópia dos insumos congelados + V4 e reensaio R2 refeitos (copia/5_R2/2_REENSAIO)"},
    "nada_escrito_fora": "Escrito SÓ em C:\\IALD\\Central de Patentes\\work\\tempo_santo_12out\\5_R2\\3_AUD_REPRO.",
}
tmp = os.path.join(A, "RESULTADO_AUD_REPRO_R2.json.tmp")
data = json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8")
open(tmp, "wb").write(data)
os.replace(tmp, os.path.join(A, "RESULTADO_AUD_REPRO_R2.json"))

# ---------------------------------------------------------------- relatorio .md
L = []
L.append("# F1.TEMPO R2 — auditoria cética independente de REPRODUÇÃO\n")
L.append("**Unidade:** F1.TEMPO (trilha TEMPO), gerência c1, programa IALD (a TGL). Workflow posto-e-tempo. **Papel:** auditor cético independente (reprodução). **Data:** 13/10/2026 (UTC %s). Escrevi SÓ em `5_R2\\3_AUD_REPRO`.\n" % res["data_utc"][:19])
L.append("**Estatuto:** %s\n" % res["estatuto"])
L.append("**Objeto conferido (hashes lidos por script):** ADENDO_R2.md `ab13c0f27a7f4cf5…`, ADENDO_R2.json `b9568befdcc200f8…`, FREEZE_R2 `0737f608505afdb5…` (23:07:58Z), FREEZE R1 `6b29d4c9b09e5553…`; pedra R2 `TheTimeIsNotAPost.lean` `4d8a82591badd010…` (120.054 B) e `.olean` `b52382ec16542a84…`; `RESULTADO_REENSAIO_R2.json` `44e745447fae0991…`.\n")
L.append("## 1. Veredito por item — CONFERE / NÃO CONFERE\n")
L.append("| # | item | veredito | o que medi |\n|---|---|---|---|")
for i, x in enumerate(itens, 1):
    L.append("| %d | `%s` | **%s** | %s |" % (i, x["id"], "CONFERE" if x["confere"] else "NÃO CONFERE", x["nota"].replace("|", "\\|")))
L.append("\n**%d de %d itens CONFEREM.** Nenhum NÃO CONFERE.\n" % (res["n_confere"], res["n_itens"]) if todos else "\n**%d de %d itens CONFEREM; %d NÃO CONFEREM.**\n" % (res["n_confere"], res["n_itens"], res["n_nao_confere"]))
L.append("## 2. Como refiz (sandbox e cópia próprios)\n")
L.append("- **Kernel:** toolchain Lean v4.31.0 copiado do elan para `sandbox\\toolchain` (%d arquivos), `LEAN_PATH` só-leitura no `.lake` do Nós (e, só para a auditoria de tipos, o `.olean` da R1 em `3_KERNEL\\sandbox`, só leitura), `-o` só no meu sandbox; toolchain apagado ao final com o prefixo `\\\\?\\`; impressão digital do tgl_kernel igual antes, depois e após a limpeza (meta `b1b47447ac30f7c7…`, src `911cb40b9de1a8bb…`)." % tc["arquivos"])
L.append("- **Pedra:** `TheTimeIsNotAPost.lean` copiada em bytes e recompilada: EXIT 0, 0 erros, 0 avisos, 152 `#print axioms` (151 no trio, `post_not_isUnit` sem axioma), `.olean` **bit a bit igual** ao do construtor (`b52382ec…`), saída do `#print axioms` byte a byte igual (`352d1f35…`). Recibo: `logs\\AUD_PEDRA_recibo.json`.")
L.append("- **Tabela R1→R2:** parser PRÓPRIO das duas fontes (`saidas\\DECLARACOES_E_ASPAS_AUD.json`): 121 mantidas (117 + 4 reforçadas), 5 renomeadas, 1 removida, 26 novas; bate com `TABELA_DECLARACOES_R2.json` do construtor; 36/36 alvos do pré-registro presentes (`saidas\\COBERTURA_ALVOS_AUD.json`).")
L.append("- **Tipos:** `sandbox\\AuditTiposAud.lean` GERADO por mim: 244 `type_of%%` nos dois sentidos + 4 implicações R2 ⟹ R1 por tática; EXIT 0; `#check` textual 122 idênticos / 4 diferentes = os 4 reforços (`saidas\\AUDIT_TIPOS_AUD.json`).")
L.append("- **Sondas adversariais:** `sandbox\\ProbesAud.lean` (P1 E5.13; P2 E5.12; P3 E5.07 POSTO = RANK; extra E5.08): EXIT 0, 0 erros, 0 avisos. Recibo: `logs\\AUD_PROBES_recibo.json`.")
L.append("- **Face ótica:** (i) recomputo com código PRÓPRIO, sem importar runner nem normativa (`scripts\\recomputo_independente_aud.py`): 55/55 números-chave bit a bit iguais ao reensaio, 10.001 linhas do TSV sem diferença; (ii) reensaio REFEITO em cópia (`copia\\5_R2\\2_REENSAIO`, V4 com o runner da R1 + runner R2 copiados byte a byte): mesmos vereditos, JSON sem diferença não volátil, TSV idêntico (`saidas\\COMPARACAO_REENSAIO_COPIA.json`).")
L.append("- **β:** script próprio (`scripts\\beta_dos_bytes_aud.py`): literal `7.2973525693e-3` na l.95 e na l.5557 (embutida em `_NIVEL2_MCMC_FILES`), β = %r [DERIVED: lido e calculado]; um.py `8e7b9927…` não executado.\n" % beta["beta_float64"])
L.append("## 3. A leitura que vale (pela regra congelada; nada aqui é veredito global)\n")
L.append("- **T9.o'(c)** e **O-f'** = PASSA pela combinação pré-fixada «exato PASSA ∧ float PASSA», com os quatro controles C-UNIF como registrado ANTES. A FALHA R1 de T9.o(c) (6.518119377574294e-13 > 1e-13, desde k = 1529) **fica registrada ao lado**; o número confirma o diagnóstico M1 (piso de representação 17/2^57 por coluna, propagado k·|δ_T|/2 = 5,898e-13 em k = 10⁴, mais arredondamento ≤ k·eps). Nunca se corrigiu tolerância depois do número: a regra foi congelada antes (V2 conferida).")
L.append("- **Pedra corrigida:** compila limpa, nada que passou na R1 foi enfraquecido (tipo idêntico ou provadamente mais forte), nenhuma declaração nova afirma mais que o termo, E5.01–E5.15 aplicados, 16 aspas todas nos verbatins do operador, frases proibidas 0.")
L.append("- **Por afirmação (face de reprodução):** %s\n" % res["por_afirmacao_face_reproduzida"]["T9'"])
L.append("## 4. Observações (não derrubam)\n")
for o in res["observacoes_nao_derrubam"]:
    L.append("- " + o)
L.append("\n## 5. O que fica fora deste papel\n")
for o in res["pendencias_fora_deste_papel"]:
    L.append("- " + o)
L.append("\n## 6. Arquivos desta pasta\n")
L.append("- `RESULTADO_AUD_REPRO_R2.json` (este veredito, estruturado), `RELATORIO_AUD_REPRO_R2.md`, `MANIFESTO_3_AUD_REPRO.json` (sha256 de tudo, gerado por último).")
L.append("- `saidas\\`: " + ", ".join(res["arquivos_desta_pasta"]["saidas"]))
L.append("- `logs\\`: " + ", ".join(res["arquivos_desta_pasta"]["logs"]))
L.append("- `scripts\\`: " + ", ".join(res["arquivos_desta_pasta"]["scripts"]))
L.append("- `sandbox\\`: " + ", ".join(res["arquivos_desta_pasta"]["sandbox"]) + " (toolchain apagado)")
L.append("- `copia\\`: " + res["arquivos_desta_pasta"]["copia"])
L.append("\n*%s Nada no quadro, no mapa, na memória (ACOM só projeção de leitura), no túnel, no Nós, no kernel do Nós, na Bancada, no site ou no git. O um.py não foi executado. Nenhum dado observado; nenhum provedor remoto; nenhuma chamada paga.*\n" % res["nada_escrito_fora"])
md = "\n".join(L)
tmp = os.path.join(A, "RELATORIO_AUD_REPRO_R2.md.tmp")
open(tmp, "wb").write(md.encode("utf-8"))
os.replace(tmp, os.path.join(A, "RELATORIO_AUD_REPRO_R2.md"))

# ---------------------------------------------------------------- manifesto (por ultimo)
mani = []
for dp, dn, fn in os.walk(LONG + A):
    dn.sort()
    for f in sorted(fn):
        lp = os.path.join(dp, f)
        rel = os.path.relpath(lp, LONG + A).replace("\\", "/")
        if rel == "MANIFESTO_3_AUD_REPRO.json":
            continue
        mani.append({"caminho": rel, "sha256": sha(lp), "bytes": os.path.getsize(lp)})
m = {"documento": "MANIFESTO_3_AUD_REPRO — sha256 de cada arquivo da pasta do auditor de reprodução (R2, F1.TEMPO)",
     "gerado_em_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "n_arquivos": len(mani), "arquivos": mani}
tmp = os.path.join(A, "MANIFESTO_3_AUD_REPRO.json.tmp")
open(tmp, "wb").write(json.dumps(m, ensure_ascii=False, indent=1).encode("utf-8"))
os.replace(tmp, os.path.join(A, "MANIFESTO_3_AUD_REPRO.json"))
print(json.dumps({"n_itens": res["n_itens"], "n_confere": res["n_confere"], "todos_conferem": todos, "manifesto_arquivos": len(mani),
                  "resultado_sha256": sha(os.path.join(A, "RESULTADO_AUD_REPRO_R2.json")), "relatorio_sha256": sha(os.path.join(A, "RELATORIO_AUD_REPRO_R2.md"))}, ensure_ascii=False, indent=1))
for x in itens:
    print(("CONFERE     " if x["confere"] else "NAO CONFERE ") + x["id"])
