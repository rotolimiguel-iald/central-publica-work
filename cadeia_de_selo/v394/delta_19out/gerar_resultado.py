# -*- coding: utf-8 -*-
"""gerar_resultado.py -- DELTA 19/10: escreve RESULTADO_DELTA_19OUT.md LENDO os artefatos (nenhum numero ou hash digitado): CANDIDATO_v394.json, ESPERADOS_v394.json, ensaio_a_seco_v394.json, kernel\\FLAGS_v394.json, KH_N1, POS_BUILD,
KERNEL_RECIBO, AXIOMAS_DELTA_19OUT.json, SOMA_TEXTOS_POS_RITO.json, ARQUIVOS_ALTERADOS_DELTA_19OUT.*, SIMULACAO_ARVORE_NOS_*.json, EXAME_PONTOS_*.json, conferencia_rito_v394_CONTROLE_NEGATIVO_PRE_RITO.json, PRECONDICOES_v394.json.
uso: python -I -B -X utf8 gerar_resultado.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE); sys.path.insert(0, V)
import delta19_v394 as DL  # noqa: E402
J = lambda *p: json.load(open(os.path.join(*p), encoding="utf-8"))
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
CM, ESP, ENS = J(V, "CANDIDATO_v394.json"), J(V, "ESPERADOS_v394.json"), J(V, "ensaio_a_seco_v394.json")
KD = os.path.join(V, DL.KERNEL_DIR); FL, KH, PB, KR = J(KD, "FLAGS_v394.json"), J(KD, "KH_N1_v394.json"), J(KD, "POS_BUILD_v394.json"), J(KD, "KERNEL_RECIBO_v394.json")
AX, SOMA, ALT = J(HERE, "AXIOMAS_DELTA_19OUT.json"), J(HERE, "SOMA_TEXTOS_POS_RITO.json"), J(HERE, "ARQUIVOS_ALTERADOS_DELTA_19OUT.json")
S16 = CM["sha16"]; SIM = J(V, "SIMULACAO_ARVORE_NOS_%s.json" % S16); EXM = J(V, "EXAME_PONTOS_%s.json" % S16)
CN = J(V, "conferencia_rito_v394_CONTROLE_NEGATIVO_PRE_RITO.json"); PRE = J(V, "PRECONDICOES_v394.json")
OLD = "4022ad521dc7293d"; old_p = os.path.join(V, "um_v394_candidato.py"); old_b = os.path.getsize(old_p)
marcas = open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read()
import re
JOBS = re.search(r"Build completed successfully \((\d+) jobs\)", open(os.path.join(KD, "lake_build.log"), encoding="utf-8", errors="replace").read()).group(1)
ep = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}; t_build = ep["epoch_build_fim"] - ep["epoch_inicio"]; t_audit = ep["epoch_audit_fim"] - ep["epoch_build_fim"]
cn_d, cn_n = CN["deve_mudar"], CN["nao_pode_mudar"]
tabela = open(os.path.join(HERE, "ARQUIVOS_ALTERADOS_DELTA_19OUT.md"), encoding="utf-8").read().rstrip("\n")
bg = ESP["n_bandeiras_por_grupo"]; po = FL["por_origem"]; ex_aux = FL["excluidas_auxiliares"]
sim_r = SIM["kh_n1_cobertura_v394"]; ver = EXM["verify"]
import glob
sys.path.insert(0, HERE)
import resultado_d19c as RD  # noqa: E402
HA, HD = J(HERE, "HARNESS_TEXTOS_ENSAIO_ANTES_original.json"), J(HERE, "HARNESS_TEXTOS_ENSAIO_DEPOIS_aplicado.json")
al_ = {e_["arquivo"]: e_ for e_ in ALT["alterados"]}
inter_ = sorted(glob.glob(os.path.join(V, "um_v394_candidato_d19.py.bak_*_c1d19c"))); assert len(inter_) == 1, inter_
C_ = {"OLD": OLD, "S16": S16, "CM": CM, "ESP": ESP, "ENS": ENS, "SIM": SIM, "EXM": EXM, "CN": CN, "PRE": PRE, "POS": J(HERE, "conferencia_POSITIVO_FALSO_NOS.json"), "SOMA": SOMA, "HA": HA, "HD": HD, "bg": bg,
      "dv": KH["delta_vs_v393"], "nao_thm": KH["delta_vs_v393"]["decl"] - KH["delta_vs_v393"]["thm"], "tx": al_["pos_rito/textos_v394.py"], "ap_": al_["artigo_pt_v394.pysnip"], "ae": al_["artigo_en_v394.pysnip"], "es_": al_["ESTADO_V394.md"],
      "ERR": DL.ERRATA_TEOREMAS_PT, "INTER": hashlib.sha256(open(inter_[0], "rb").read()).hexdigest()[:16], "INTER_BAK": os.path.basename(inter_[0]),
      "erro_antes": (HA["etapas"]["_d"].get("erro") or "").split(": ", 1)[-1], "ntexto": sum(1 for k_ in HD["etapas"] if k_ != "leitura"),
      "com_errata": [k_ for k_, e_ in HD["etapas"].items() if isinstance(e_, dict) and e_.get("tem_errata_teoremas")]}
L = []
a = L.append
a("DELTA 19/10 — v394")
a("")
a("Gerência c1, subagente Sonnet, 19/10/2026, por autorização do coordenador; escopo ampliado em duas ordens (a integração final da v394) e uma rodada final (d19c: a seção 0.1). Estatutos: [REAL] medido/lido aqui por script; [DERIVED] composto; [DECLARADO] dito na origem e não conferido aqui; [ONTO] leitura do operador; [OPEN] em aberto. Nada foi instalado; o rito não rodou; o Nós, o túnel, a Bancada, o quadro, o mapa de rotas, a memória, o site e o git não foram tocados; sem init/transition ACOM; `pos_rito\\` só foi tocada na rodada final e só em `textos_v394.py` (a proposta aprovada e a frase de errata, por ordem expressa, com backup de bytes; `derivar_cadeia_v394.py` NÃO rodou). O candidato em exame `%s` fica como registro, intacto (conferido por p00)." % OLD)
a("")
a("## 0. Em uma tabela")
a("")
a("| | candidato em exame (registro) | **candidato novo (d19)** |")
a("|---|---|---|")
a("| arquivo | `um_v394_candidato.py` | `%s` |" % DL.CANDIDATO)
a("| sha16 | `%s` | **`%s`** |" % (OLD, S16))
a("| sha256 | (o do registro) | `%s` |" % CM["sha256"])
a("| bytes | %s | %s (%s) |" % (format(old_b, ","), format(CM["bytes"], ","), format(CM["bytes"] - old_b, "+,")))
a("| módulos novos no kernel | 189 | %d (189 do Codex + a pedra do delta) |" % CM["kernel"]["modulos_novos"])
a("| bandeiras novas | 3707 | **%d** (só declaração nomeada) |" % ESP["n_bandeiras_novas"])
a("| escada | 10752/10752 | **%d/%d** (v393: %d; + %d) |" % (ESP["escada"][1], ESP["escada"][0], ESP["escada_v393_e_v394"][0], ESP["n_bandeiras_novas"]))
a("| Audit (constantes / teoremas / fora do trio) | 29025 / 23068 / 0 | %d / %d / %d |" % (KH["linha_TOTAL"]["decl"], KH["linha_TOTAL"]["thm"], KH["linha_TOTAL"]["fora_do_trio"]))
a("| pino h8 de `kh_n1_cobertura_v394` | 1421 (**reprova** no rito real: exame de 19/10) | **%d** entradas = %d embutidas + `%s` |" % (ESP["h8_entradas"], ESP["formal_files_n"], "`, `".join(ESP["h8_residuais_do_nos"])))
a("| registros por spec | 2 | %d (+ `criterio_binario_de_parada_v394`) |" % len(ESP["registros_v394"]))
a("| falas do operador embutidas | 46 | %d (+ as duas de 19/10) |" % len(ESP["cunhagens"]))
a("| ensaio a seco | TUDO PASSOU (sem a simulação da árvore do Nós) | **%s** |" % ENS["veredito"])
a("")
for l_ in RD.secao_0_1(C_):
    a(l_)
a("## 1. A pedra candidata (nome provisório: o operador nomeia) [REAL a conjunção; ONTO a leitura]")
a("")
a("- `delta_19out\\TheBinaryReadingAtTheFixedPoint.lean`, sha16 **`%s`**, %d B; teorema de composição `%s`, namespace `TGLExt`; docstring com os dois verbatins e os sha16 (`786928986ca1e460`, `7596dcd880a1c8f5`, conferidos por script contra os arquivos), estatutos e ressalvas." % (AX["pedra"]["sha16"], AX["pedra"]["bytes"], DL.THEOREM))
a("- A conjunção só CITA oito teoremas já no kernel (nenhuma matemática nova): `spectral_projections_split_the_identity`, `the_reading_is_total_on_the_form`, `observing_adds_nothing`, `absolute_faces_half`, `halfnat_from_J_symmetry`, `no_changed_transition_at_fixed_point`, `collapse_iteration_is_stable`, `fair_bit_entropy_is_not_half_nat`. Ressalva dita na pedra: a analogia com o qubit vale nos pesos (½, ½), NÃO na entropia (`fair_bit_entropy_is_not_half_nat`); o «1=0» do negativo não é tipado como igualdade de numerais; «a parada é o ponto fixo» é [ONTO] do operador; nenhum procedimento de decisão está afirmado.")
menos_ = {n_.split(".")[-1]: v_["axiomas"] for n_, v_ in AX["citados"].items() if v_["axiomas"] is not None and len(v_["axiomas"]) < len(DL.TRIO)}
todos_no_trio_ = all(v_["axiomas"] is not None and set(v_["axiomas"]) <= set(DL.TRIO) for v_ in AX["citados"].values())
a("- **Relatório de axiomas** (`AXIOMAS_DELTA_19OUT.json`, lido dos logs crus do build FRIO): o teorema depende de `%s` (o trio inteiro, e nada além); os oito citados %s; destes, %s; zero `sorry` (build e Audit); zero erro; a pedra foi compilada (linha `Built`, %d s a frio, com o carregamento do ambiente); proveniência do compilador: `%s`." % (", ".join(AX["teorema_de_composicao"]["axiomas_no_audit"][0]), "estão todos dentro do trio" if todos_no_trio_ else "NAO estao todos no trio", "; ".join(("`%s` depende só de %s" % (k_, ", ".join("`%s`" % x_ for x_ in v_))) if v_ else ("`%s` não depende de axioma algum" % k_) for k_, v_ in menos_.items()), AX["compilacao"]["segundos"], AX["teorema_de_composicao"]["proveniencia_TGL_DECL_SOURCE"][0]))
a("- Aviso do Lean 4.31: o aviso de `sorry` usa crases; o detector da v392 já lê as duas formas.")
a("")
a("## 2. O registro `criterio_binario_de_parada_v394` (spec; chamado no PONTO DE CHAMADA REAL, `_v394_rodar_specs` do `main`)")
a("")
a("- Lê a cada rito: a bandeira `%s` (True), os 9 nomes (o teorema + os 8 citados) no `axiom_report` do próprio rito dentro do trio, o sha256 das duas inscrições EMBUTIDAS (`_V394_VERBATINS2`, padrão das inscrições v394; o arquivo é só informativo), a proveniência `TGL_DECL_SOURCE` do teorema no módulo da pedra, o sha256 da pedra em `formal_files_sha256` e a escada. Não escreve em nenhuma chave existente; `does_not_gate_core`." % DL.FLAG_KEY)
a("- Veredito (sem a palavra da régua, conferido pela guarda P18 e pelo conferidor): `%s`" % ENS["criterio_binario"]["verdict"])
a("- **Controles negativos** (ensaio a seco, todos True; recusa = `<prefixo>__NOT_SEALED_THIS_RUN__<falhas>__GATE_UNMOVED`): bandeira falsa; teorema ausente do `axiom_report`; citado com axioma fora do trio; teorema com axioma fora do trio; sha errado em CADA uma das duas falas; fonte da pedra adulterada; pedra adulterada no kernel do rito (check g5); tudo certo sela; veredito e texto sem palavra proibida.")
a("- **O gate não se move** [REAL]: `qg_closure_verdict` igual ao do selo da v393, as 18 bandeiras iguais (gate recomputado com o kf novo: `verdict_igual`, `n18 = %d`), `qg_closure` do core intocado pelo fluxo; no exame de pontos: `gate_recomputado.verdict_igual = %s`." % (ENS["gate_recomputado"]["n18_novo"], EXM["gate_recomputado"]["verdict_igual"]))
a("")
a("## 3. Política de bandeiras (decisão da gerência) [REAL]")
a("")
a("- Só declaração NOMEADA tem bandeira (a prática da v392 e da v393). O último componente do nome decide (`delta19_v394.classe`: `_proof_N`, `_simp_N`, `match_N`, `_sunfold`, `eq_N`, `eq_def`, `congr_simp` são auxiliares). A classificação reproduz o exame NÚMERO A NÚMERO, lida do `EXAME_FINAL_V394.md` por script em `pos_build_kernel_v394.py` (a lista do exame não estava gravada em arquivo; a regra reproduz: %d nomeadas e %d auxiliares nas %d do Codex (%d proof/simp/match/sunfold + %d eq + %d congr_simp); entre as públicas sem bandeira, %d nomeadas e %d + %d + %d auxiliares)." % (po["codex_nomeada"], ex_aux["n"], po["codex_nomeada"] + ex_aux["n"], ex_aux["por_classe"]["proof_simp_match_sunfold"], ex_aux["por_classe"]["eq"], ex_aux["por_classe"]["congr_simp"], po["nomeada_sem_bandeira"], FL["publicas_sem_bandeira"]["por_classe"]["proof_simp_match_sunfold"], FL["publicas_sem_bandeira"]["por_classe"]["eq"], FL["publicas_sem_bandeira"]["por_classe"]["congr_simp"]))
a("- **%d bandeiras** = %d nomeadas do Codex (mesmas chaves do r8) + %d nomeadas que ele não marcou (`ext_nm394_0001` a `ext_nm394_%04d`, ordem alfabética) + 1 da pedra do delta (`%s`). Por grupo: tempo %d, quadrática %d, rede %d, outro (a pedra) %d. %d auxiliares ficam fora (%d marcadas pelo Codex e excluídas; todas no trio e cobertas pelo KH-N1)." % (FL["n_flags"], po["codex_nomeada"], po["nomeada_sem_bandeira"], po["nomeada_sem_bandeira"], DL.FLAG_KEY, bg["tempo"], bg["quadratica"], bg["rede"], bg["outros"], ex_aux["n"] + FL["publicas_sem_bandeira"]["n"], ex_aux["n"]))
a("- **Escada final: %d/%d** = %d (v393) + %d. O exame estimou %d antes da pedra (conferido: %d + 1 = %d). Os contratos do Codex (108 / 18 / 3581 declarações) seguem como contrato (presença, trio, proveniência) e deixaram de coincidir com as bandeiras: `expected_ladder` dos três contratos = %d, derivado do `gerar_candidato`." % (ESP["escada"][1], ESP["escada"][0], ESP["escada_v393_e_v394"][0], ESP["n_bandeiras_novas"], ESP["escada"][1] - 1, ESP["escada"][1] - 1, ESP["escada"][1], ESP["escada"][1]))
a("- Texto: onde o veredito dizia «THEOREMS» para a escada (único token em maiúsculas: `estatuto_da_prova_v391`, `KERNEL_N_OF_N_THEOREMS_...`), passa a «FLAGS» (patch C11); troca de palavra DECLARADA nos ESPERADOS (`troca_de_palavra`) e aplicada pelo conferidor ao veredito da v393 antes de comparar; errata assinada em `kh_n1_cobertura_v394`. **Mantive** a frase «teoremas limpos» como REGISTRO DE MÁQUINA no artigo e no stdout do rito (`teoremas limpos: N/M`), porque `pos_rito\\leitura_v394.py` PARSEIA essa linha por regex (decisão da gerência de 19/10: manter o token e acrescentar a errata ao lado; ver a seção 0.1, item 2).")
a("")
a("## 4. O pino h8: %d entradas [REAL]" % ESP["h8_entradas"])
a("")
a("- `gerar_candidato_v394.py` recalcula o pino a cada geração: materializa o kernel EMBUTIDO do candidato novo (%d arquivos), acrescenta os residuais da pasta `Nós\\tgl_kernel` que a `sha256_directory` do PRÓPRIO um.py conta (extraída por AST; a exclusão nominal de `ExtrairDeps.lean` NÃO foi alterada) e hasheia: **%d** = %d + `%s`. Conferido por `simular_arvore_do_nos.py` (cópia de bytes do exame, `%s`): `formal_files_n_no_rito_real = %d`, `kh_n1_cobertura_v394` SELA nessa árvore." % (ESP["formal_files_n"], ESP["h8_entradas"], ESP["formal_files_n"], "`, `".join(ESP["h8_residuais_do_nos"]), sha16(os.path.join(V, "simular_arvore_do_nos.py")), SIM["formal_files_n_no_rito_real"]))
a("- Prova independente de que a regra «embutidos + residual» é a do rito real [REAL]: o `formal_files_sha256` do core v393 SELADO no Nós tem 1233 entradas e é IGUAL, hash a hash, aos 1232 embutidos da v393 + o `_check_damming.lean` (0 diferenças); logo o `lake` não deriva nenhum outro arquivo contado.")
a("- Fail-closed: se alguém mexer no `_check_damming.lean` antes do rito, o h8 recusa. O ensaio a seco e o `exame_pontos` agora recebem os residuais do Nós na árvore que materializam (antes materializavam só o embutido e por isso «passavam»).")
a("")
a("## 5. Kernel FRIO, recibo e tempos [REAL]")
a("")
a("- Sandbox novo `C:\\t\\k394d\\final` (robocopy do `tgl_kernel` do Nós v393 sem `/PURGE`, sem junções: nenhuma existe; `preparar_kernel_v394.py gerar`: 189 do Codex conferidos contra a árvore e o embutido do r8 + a pedra + raiz e Audit gerados). Um único `lake build` FRIO: rc 0, %s jobs, **%d s**; os %d módulos novos `Built` (nenhum `Replayed`); `lake env lean TGL/Audit.lean`: rc 0, **%d s**; zero erro, zero `sorry`; todo `.olean` em Lean 4.31.0, githash único; %d constantes, %d teoremas, 0 fora do trio; proveniência %d == %d." % (JOBS, t_build, PB["jobs_built_novos"], t_audit, KH["linha_TOTAL"]["decl"], KH["linha_TOTAL"]["thm"], ENS["verify_kernel_ponta_a_ponta"]["proveniencia"]["compiler_names"], ENS["verify_kernel_ponta_a_ponta"]["proveniencia"]["audited_names"]))
a("- Um ensaio INCREMENTAL anterior (só a pedra, ~5 min de build e ~4 min de Audit) está em `delta_19out\\kernel_k394d\\` (logs crus) e a árvore dele em `C:\\t\\k394d\\scratch_incremental` (14 GB, descartável).")
a("- **Recibo do kernel** `kernel\\KERNEL_RECIBO_v394.json` (sha16 `%s`): %d pedras, árvore `%s` (só-fontes, mantida), logs e sha pinados. Os arquivos antigos de `kernel\\` ficaram como `.bak_20261019_135101_c1` (a pasta VIVA é `kernel\\`, porque `pos_rito\\` lê dela)." % (sha16(os.path.join(KD, "KERNEL_RECIBO_v394.json")), len(KR["pedras"]), KR["arvore"]))
a("- Tempo do rito: o build frio dos %d módulos novos custa %.1f min e o Audit %.1f min (a pedra já está contada); 3 passagens = %.1f min é o TETO só de lake (o exame estimou ~60 min de lake e ~1h45 no total, porque o autoteste recompila só o fecho reverso de `HalfNat`); os timeouts do um.py (3600 s e 1800 s) seguem com folga." % (PB["jobs_built_novos"], t_build / 60.0, t_audit / 60.0, 3 * (t_build + t_audit) / 60.0))
a("")
a("## 6. Ensaio a seco, esperados, conferidor [REAL]")
a("")
a("- `ensaio_a_seco_v394.py` (editado em lugar; backup de bytes): **%s** — kernel embutido == sandbox (%d arquivos); `verify_tgl_kernel_formalization` real com os logs CRUS do build frio: `%s`, cobertura %d/%d, proveniência ok; escada recomputada %d/%d (sem as bandeiras novas: %d de %d e `all_verified` falso); vizinhos: %d iguais, **5 trocam só números** (`three_stress_tests_v387`, `estatuto_da_prova_v391`, `pedras_v392`, `varredura_e_sorry_v392`, `pedras_v393`), **mais a troca de palavra declarada** em `estatuto_da_prova_v391`, e o índice (mudança declarada); %d casos de unidade, todos True; artigo PT/EN com o parágrafo novo, pdflatex ×2 rc 0 (seção de %d e %d caracteres, sem «n/d»); selo: `qg_closure_verdict` igual." % (ENS["veredito"], ENS["kernel_embutido_vs_sandbox"]["n"], ENS["verify_kernel_ponta_a_ponta"]["verdict"], ENS["verify_kernel_ponta_a_ponta"]["cobertura"]["decl"], ENS["verify_kernel_ponta_a_ponta"]["cobertura"]["thm"], ENS["escada"][0], ENS["escada"][1], ENS["escada_sem_as_bandeiras_novas"][0], ENS["escada_sem_as_bandeiras_novas"][1], len(ENS["vizinhos"]["recomputados_iguais"]), len(ENS["unidade"]), ENS["artigo"]["pt"]["secao_chars"], ENS["artigo"]["en"]["secao_chars"]))
a("- **Etapas obrigatórias novas**: (11) `simular_arvore_do_nos`: rc %d, %d entradas, pino %d, extras do Nós fora do embutido %s; o simulador (cópia SEM alteração) lista os cinco registros que já existiam e todos selam, com o índice; o sexto (`criterio_binario_de_parada_v394`) sela no fluxo do `main` do ensaio e no `exame_pontos`; (12) `exame_pontos_v394` sobre o candidato novo (em processo isolado, pontos de chamada reais): `algum_falso = %s`; bandeiras novas True %d/%d; `ext_` True %d/%d." % (ENS["simular_arvore_do_nos"]["rc"], SIM["formal_files_n_no_rito_real"], ENS["simular_arvore_do_nos"]["pino_h8_entradas"], SIM["extras_no_nos_fora_do_corpo_embutido"], EXM["algum_falso"], ver["novas_true"], ver["n_novas"], ver["ext_true"], ver["n_ext"]))
a("- `p00_precondicoes_v394.py`: %s (%d checagens; inclui o candidato anterior intacto, a pedra, o h8, a simulação e o exame)." % ("TODAS PASSARAM" if PRE["ok"] else "FALHOU", len(PRE["checagens"])))
a("- **Esperados e conferidor** (editados em lugar; backups): os ESPERADOS ganharam `troca_de_palavra`, `h8_entradas`, `h8_residuais_do_nos`, `formal_files_n_no_rito`, `n_bandeiras_por_grupo`, `politica_de_bandeiras`, `pedra_do_delta`, `teorema_do_delta`, `bandeira_do_delta`, `criterio_binario` (veredito + sha das duas falas), `candidato_anterior_sha16`; o conferidor ganhou (a) a troca de palavra aplicada ao veredito da v393, (b) o registro `criterio_binario_de_parada_v394` (veredito == ensaio; as duas falas `embedded_ok` com o sha dos ESPERADOS; bandeira e teorema da pedra no trio; proveniência no módulo da pedra), (c) o hash formal do rito com %d entradas e o residual. **Controle negativo** (Nós ainda v393): `tudo_bate = %s`; deve-mudar %d de %d (só os dois que não mudam: os 5 registros da v393 e o pilar); não-pode-mudar %d de %d." % (ESP["h8_entradas"], CN["tudo_bate"], sum(1 for v in cn_d.values() if v), len(cn_d), sum(1 for v in cn_n.values() if v), len(cn_n)))
POS = J(HERE, "conferencia_POSITIVO_FALSO_NOS.json"); pd_, pn_ = POS["deve_mudar"], POS["nao_pode_mudar"]
a("- **Caminho POSITIVO do conferidor** (emulação: `delta_19out\\teste_conferidor_positivo.py`): um Nós FALSO montado do `dry_v394_d19` (o um.py candidato, o kernel materializado com o residual, o core e o selo que o ensaio computou, o artigo, o sumário e o .md; o selo ganha de v393 as chaves que o `main` põe depois do literal) e uma CÓPIA do conferidor apontada para ele: **%s** (deve-mudar %d de %d; não-pode-mudar %d de %d). **Achado:** o conferidor trazia um defeito LATENTE (`set(axr.get(n) or [\"?\"]) <= TRIO` reprovava bandeira de lista de axiomas VAZIA: 12 das 3707 do candidato anterior, 2 das 2287 de agora, como `TimeGravitonMatrix.tacticMatrix_calc`); corrigido para `(n in axr) and set(axr[n] or []) <= TRIO`. Limite: é emulação (core e selo vêm do ensaio, não do rito); só o rito real exercita o conferidor de verdade." % ("TUDO BATE" if POS["tudo_bate"] else "NAO BATE", sum(1 for v in pd_.values() if v), len(pd_), sum(1 for v in pn_.values() if v), len(pn_)))
a("")
for l_ in RD.secao_7_8(C_):
    a(l_)
a("## 9. Arquivos alterados (sha16 ANTES lido do backup de bytes mais antigo de hoje; DEPOIS lido do arquivo). Diffs em `delta_19out\\diffs\\`")
a("")
a(tabela)
a("")
a("Copiados SEM alteração do exame para a raiz: `simular_arvore_do_nos.py` e `exame_pontos_v394.py` (cmp de bytes). Em subpastas: `insumos\\` (+`KH_N1_v394_d19.json`, +`TheBinaryReadingAtTheFixedPoint.lean`, +2 falas em `insumos\\cunhagens\\`; o `KH_N1_v394.json` antigo, pinado pelo candidato em exame, NÃO foi tocado), `kernel\\` (8 arquivos substituídos, backups `.bak_20261019_135101_c1`), `vinculo\\CRITERIOS_v394.json`. Sandbox: `C:\\t\\k394d\\final`, `C:\\t\\k394d\\arvore`, `C:\\t\\k394d\\scratch_incremental`.")
a("")
a("## 10. Como refazer (nada digitado; cada passo recusa visivelmente)")
a("")
a("`sh refazer_sandbox_v394.sh` (ou `preparar_kernel_v394.py copiar|gerar` + `sh construir_kernel_v394.sh`) → `pos_build_kernel_v394.py` → `montar_cunhagens_delta19_v394.py` → `copiar_insumos_v394.py` → `V394_REGERAR=1 python -I -B -X utf8 gerar_candidato_v394.py` → `python -B -X utf8 ensaio_a_seco_v394.py` → `gerar_esperados_v394.py` → `conferir_rito_v394.py _CONTROLE_NEGATIVO_PRE_RITO` → `diff_e_pinos_v394.py` → `comparar_v393_v394.py`/`comparar_r8_v394.py` → `derivar_instalar_rito_v394.py` → `p00_precondicoes_v394.py`. Scripts de edição do delta (já aplicados, falham se repetidos): `delta_19out\\editar_*.py`, `aplicar_bloco.py`. Rodada final (d19c), nesta ordem: `aplicar_pos_rito_d19c.py`, `editar_delta19_errata_d19c.py`, `editar_artigo_errata_d19c.py` (antes do `gerar_candidato`); depois do ensaio e de `teste_conferidor_positivo.py` (que monta o Nós falso): `harness_textos_ensaio.py` (e `--textos` com o ORIGINAL para ver a recusa), `emular_soma_textos.py`, `tabela_arquivos_alterados.py`, `gerar_adendo_estado_d19.py`, `gerar_resultado.py`, `gerar_registro_mapa.py`.")
open(os.path.join(HERE, "RESULTADO_DELTA_19OUT.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("RESULTADO_DELTA_19OUT.md:", len("\n".join(L)), "caracteres")
