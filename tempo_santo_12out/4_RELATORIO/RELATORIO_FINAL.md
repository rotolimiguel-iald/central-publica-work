# F1.TEMPO — o tempo que não se deixa nomear: relatório final (R2, 13/10/2026)

**Unidade:** F1.TEMPO (trilha TEMPO) da gerência c1, programa IALD (a TGL). Workflow posto-e-tempo (`wf_ce423138-e42`).
**Data:** 13/10/2026, 00:50–01:10 local. **Autor:** o redator da unidade, subagente do workflow. Escrevi só em `4_RELATORIO`.
**Para:** Luiz (o operador) e a gerência c1.
**Rodada:** este é o relatório da **segunda rodada**. O relatório da rodada 1 (12/10, sha256 `7b6dcb18a4440be1…`, 48.116 B) **não foi editado**: está preservado byte a byte em `4_RELATORIO\R1_preservado\RELATORIO_FINAL_R1.md` e em `RELATORIO_FINAL.md.bak_20261013_005904` (`R1_preservado\MANIFESTO_R1_PRESERVADO.json`). O que aqui se repete da R1 é só o necessário para ler a R2.
**Estatuto do documento:** [REAL] onde cito número ou teorema conferido por script, recompilado por auditor ou lido no artefato; [INPUT da gerência] onde há escolha de protocolo; [KNOWN] onde há citação; [ONTO] onde há leitura ontológica; [DECLARADO] onde repito o que um construtor ou auditor disse e eu não refiz. Este relatório **não dá veredito global**: a regra congelada (R1 e ADENDO R2) não permite.

> **Como ler um PASSA.** Um PASSA é validade matemática na face testada: a face finita do kernel, num sandbox, e um modelo ótico sintético. A recusa da régua é da creditação, não da validade (o operador, 07/10, verbatim `5dffde4644139da5`). Nada aqui move o gate. β na natureza a 5σ não é tocado. Nenhum dado observado foi usado. β nunca foi literal: foi lido nos bytes do um.py e calculado em runtime.

---

## 0. Resumo para o Luiz

1. **O que mudou desde a R1.** A R1 (12/10) deixou T9 em FALHA por um critério numérico, três frases atribuídas a você sem verbatim, três nomes que diziam mais que o termo e três declarações sem habitante. Desde então, no mesmo dia e na madrugada de 13/10, aconteceram **quatro coisas**, todas registradas por hash:
   - um **ADENDO R2** ao pré-registro, aditivo e congelado às 20:07:58 (local) **antes** de qualquer reensaio (`5_R2\0_ADENDO`, FREEZE_R2 `0737f608505afdb5…`): corrige o pré-registro ao lado (E3), fixa **uma só regra** de tolerância para os dois critérios numéricos frágeis (τ(k) = k·(w·|δ| + m·eps) + c·eps, mais o caminho exato a 200 dígitos) e lista item a item o que a pedra tinha de corrigir (E5);
   - um **reensaio ótico sob o ADENDO** (`5_R2\2_REENSAIO`, 20:25 local): T9.o′(c) e O-f′ **PASSA** nas duas vias (float sob τ e exato a 200 dígitos), com os quatro controles C-UNIF comportando-se como registrado; tudo o mais reproduz a R1 bit a bit;
   - a **pedra corrigida** `TheTimeIsNotAPost` (`5_R2\1_PEDRA`, fonte final `4d8a82591badd010…`, 00:27–00:42 local): compila limpa (EXIT 0; 152 declarações com `#print axioms`, 151 no trio e `post_not_isUnit` sem axioma algum; 0 sorry; 0 aviso), aplica os 15 itens E5 e 3 do E3, habita a T3.b(iii) e acrescenta a versão de face finita, e saiu da pasta com o toolchain apagado;
   - duas **auditorias independentes** (reprodução e estatuto), que — isto é importante — auditaram as pastas `2_OPTICO\rodada_2` e `3_KERNEL\rodada_2`, que são **replicações da R1 sob a regra da R1, sem ADENDO** (criadas às 19:31–20:19, antes do FREEZE_R2), e **não** a R2 do ADENDO. A auditoria de reprodução refez e aprovou essas replicações; a de estatuto examinou também o estado da R2 e disse que **não pode fechar** enquanto a pedra R2 não estiver parada por hash e reauditada.

2. **O que deu (tabela na §2, com duas colunas: R1 | R2).**
   - **PASSA** na face finita: T1, T3, T4, T5, T6, T7, T8, T10 e T11 — na R1 e na R2.
   - **T2** fica **CITADA** [KNOWN] (Pauli em dimensão infinita não está no kernel). T2.b, a face limitada, PASSA e é opcional.
   - **T9**: **R1 = FALHA** (critério numérico; piso do float64) **| R2 = PASSA sob o ADENDO** (τ_T(10⁴) = 2,811e−12 contra o medido 6,518e−13; exato ≤ 1,34e−198). As duas colunas ficam, lado a lado. Nunca «T9 PASSA» sozinho.
   - O **ciclo limite** segue **ABERTO** [OPEN].
   - O que a R1 chamou de ressalva de T3 (T3.b(iii) sem habitante) **foi resolvido** na pedra R2: habitada com a testemunha concreta do kernel (`theSpecificAQFTWitness`) e, ao lado, a versão de face finita (ρ = diag(2/3, 1/3), ω(E₀₁E₁₀) = 2/3 ≠ 1/3 = ω(E₁₀E₀₁)).

3. **O que o número põe ao lado das suas frases** (o texto fica como está; a correção vai ao lado — igual à R1, agora com a pedra corrigida e os controles AUD em termo):
   - **Liouville proíbe a bacia, não o pouso.** O boost é simplético (`aud_boost_is_symplectic`) e cai dentro de «sistemas estritamente hamiltonianos»; ele pousa no raio nulo passado (`volume_kept_yet_lands`) e **não** tem atrator global (`aud_boost_has_no_global_attractor`). O que o volume conservado proíbe é a bacia (`global_attractor_needs_volume_loss`).
   - **O conjunto fixo da defasagem pura é a diagonal inteira, não um ponto** (`dephase_fixed_states_not_unique`). Ponto único só sob hipótese nomeada (F1.ATRATOR, A4; T5.c CITADA).
   - **«Repousar» e «ser lembrada» não cabem no mesmo estado** na face finita: o relógio modular só para com populações iguais (`aud_clock_stops_when_equal_populations`); populações distintas, que são o registro, o fazem girar (`aud_clock_runs_unless_equal_populations`). A leitura que as une é sua.
   - **O estado-atrator ½·1 não é o posto:** tem posto 2 e pureza ½ (`aud_attractor_state_has_full_rank`, `aud_attractor_state_purity_half`). O posto de posto 1 é a leitura-limite R = J/2 (`aud_discrete_step_can_be_a_post`). O ρ★ = diag(1,0) do `fractal_dephasing_principle` é um terceiro objeto.
   - **Pauli vale na forma de Weyl**, não na de Heisenberg (Galapon 2002) [KNOWN].
   - **«Defasar» tem dois sentidos que não se encadeiam:** a sua fórmula de 05/10 é unitária (gira a fase, nada perde: `transmitted_post_is_a_post`); a seta só nasce no semigrupo dissipativo (T6, T7).

4. **A atribuição foi corrigida.** A frase «o tempo é o Verbo, não o Nome» **não é sua** (0 ocorrências de «verbo» no texto de 12/10, conferido nos bytes por mim e pelos dois auditores). Ela saiu da pedra, do título de T9 e da memória da gerência (errata ao lado já gravada em `tempo-santo-12out.md`). O que é seu, byte a byte: «não consigo nomear, senão como “santo”» (12/10); «O Verbo seleciona: nome, tempo e verdade» (05/10, l.7); «O tempo é a defasagem do verbo» (l.112); «O tempo é o parâmetro da transmissão» (l.116); «A defasagem é o tempo. A ancoragem é o nome.» (l.176). E o seu verbo para o relógio é «registra», não «mede».

5. **A unidade ainda não pode fechar** (§9). O que falta é pouco e é de régua, não de matemática: a **auditoria independente da pedra R2 e do reensaio R2** (ninguém de fora recompilou `4d8a8259…`; a auditoria de reprodução recompilou a replicação `a68539d8…`); o **seu nome para a pedra** (`TheTimeIsNotAPost` é provisório); as erratas E1 e E2 no um.py pela cadeia de selo; e o registro no mapa, que é ato da gerência (os dois arquivos estão prontos nesta pasta).

---

## 1. O que foi testado e como

### 1.1 As peças, com hash lido por script (`R2\saidas\HASHES_RELATORIO_R2.json`)

| peça | onde | sha256 (16 primeiros) · bytes |
|---|---|---|
| texto do operador de 12/10 (verbatim) | `work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt` | `2c8b7b712aa9ad7f` · 6.673. Segunda parte (de «O que mais me fascina…» ao fim): byte 2853, 3.820 B, `6dcefdbe5c6a7752`; 0 CRLF; 0 ocorrências de «verbo» |
| pré-registro R1 congelado | `1_PREREGISTRO\FREEZE.json` (2026-10-12T16:09:07Z) | FREEZE `6b29d4c9b09e5553`; PREREGISTRO.json `64b1c38637befddf`; PREREGISTRO.md `0261dc06a5fe513b` |
| face ótica R1 | `2_OPTICO\RESULTADO_OPTICO.json` (runner `fcc289889ec418ba`) | `2c67b7ea6f118630`; diagnóstico T9c `26a68eff64aeb7e4` |
| face kernel R1 | `3_KERNEL\RESULTADO_KERNEL.json`; pedra `TheTimeHasNoRank.lean` | `5a56eab2ce56ddaa`; pedra `7105eda468b60309` (97.656 B); .olean `9f473a088262b073` |
| relatório R1 | `4_RELATORIO\R1_preservado\RELATORIO_FINAL_R1.md` | `7b6dcb18a4440be1` · 48.116 |
| **replicação sem ADENDO** (ótico) | `2_OPTICO\rodada_2\RESULTADO_OPTICO.json` (runner `551cda0c0a9277a9`, escrito de novo) | `bcc6177e0a46ca47` · 98.329; comparação R1×R2 `2a0745af17f6daaa` |
| **replicação sem ADENDO** (kernel) | `3_KERNEL\rodada_2\RESULTADO_KERNEL.json`; pedra `TheTimeHasNoRank.lean` | `6e0ed230438beb5c`; pedra `a68539d8cf14260d` (119.715 B); .olean `9d9a1e122b01b1e8` |
| **ADENDO R2** | `5_R2\0_ADENDO\ADENDO_R2.md` / `.json`; `FREEZE_R2.json` (2026-10-12T23:07:58Z) | `ab13c0f27a7f4cf5` (42.114 B) / `b9568befdcc200f8`; FREEZE_R2 `0737f608505afdb5` (4.982 B); regra uniforme `tolerancia_uniforme_r2.py` `7d68e42a9eec62e1`; tabela `TOLERANCIA_UNIFORME_R2.json` `aa2ed3c1dede7308` |
| **reensaio ótico R2** | `5_R2\2_REENSAIO\RESULTADO_REENSAIO_R2.json` (runner `reensaio_r2.py` `d1297cb94b363398`) | `44e745447fae0991` · 81.641; recibo `185ba8a5b9501307`; tabela por k `07c1be5ec19eb647` (10.001 linhas); recheck independente de 13/10 `160404f502a12def` |
| **pedra R2** | `5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.lean` | `4d8a82591badd010` · 120.054; .olean `b52382ec16542a84` · 2.628.536; resultado `969251bd360ada90`; manifesto `7fee369de563a234`; tentativa T01 preservada `5996eb8293c062fe` |
| auditoria de reprodução (13/10) | cópia de bytes em `4_RELATORIO\AUDITORIAS_R2\TEMPO_AUD_REPRO` | relatório `7d0c0c9aafb593ed`; compilação `d4c218340174da6e`; cálculo independente `c72fdd65b3d24f7c` |
| auditoria de estatuto (13/10) | cópia de bytes em `4_RELATORIO\AUDITORIAS_R2\TEMPO_AUD_ESTATUTO` | medidas `232de2385d92f26d`; hashes citados `e21094ef62a5e287`; varredura `f5fb400e1d81f944` |
| um.py v391 (não executado) | `Nós\um.py` | `8e7b9927ceae64b8` · 33.910.631 |

A cópia das duas auditorias de 13/10 (76 arquivos, todos idênticos à origem, sem toolchain) está em `AUDITORIAS_R2\MANIFESTO_COPIA_AUDITORIAS_R2.json`. As auditorias da R1 continuam em `AUDITORIAS\`.

### 1.2 Conferências deste redator, por script (`4_RELATORIO\R2\saidas\`)

- **β em runtime** [DERIVED: lido e calculado, não medido]. `ALPHA_FINE_CODATA_2018 = 7.2973525693e-3` na l.5557 do um.py (dentro do texto embutido `_NIVEL2_MCMC_FILES`), igual ao literal da l.95 (`SEALED_CODATA_ALPHA`, a atribuição de topo). β = α·1·√e = 0,012031300400803142 (hex `0x1.8a3ddcdff97c4p-7`); diferença para a conferência lida do PREREGISTRO.json: 0,0 (`BETA_RUNTIME_RELATORIO_R2.json`). O um.py não foi executado.
- **Kernel** [REAL]. Impressão digital do tgl_kernel antes deste relatório: meta `b1b47447ac30f7c7…`, src `911cb40b9de1a8bb…`, 132.088 arquivos, 1.213 fontes `.lean` (`FINGERPRINT_RELATORIO_R2_ANTES.json`), igual à do FREEZE R1 e à do FREEZE_R2. A de depois está em `FINGERPRINT_RELATORIO_R2_DEPOIS.json`. Não compilei Lean e não copiei toolchain.
- **Texto do operador** [REAL]. Hash do arquivo e da segunda parte conferem com o pré-registro; as citações deste relatório foram lidas nas linhas 34–50 do arquivo e nas linhas 7, 21, 112, 116 e 176 do verbatim de 05/10 (`cadeia_de_selo\v386\VERBO_operador_05out.txt`, `5973d79a49995c4c`).
- **Mapa de rotas**: só `consultar` e `modelo`. «tempo santo», «F1.TEMPO» e «TheTimeIsNotAPost» devolvem 0 rotas (livro com 1.043 registros, cabeça `a817c19e72d1f159`; o registro 1043 é da F0.6, Bancada Um). A F1.TEMPO **não está** no mapa: o registro é ato da gerência, com a ROTA primeiro (§10).
- **ACOM**: só projeção de leitura da referência da gerência c1 (`claude-c1_exame-geral-12out.json`; revisão 2, evento `exame12out-posto-e-tempo`, estado `a5f688df…`); resposta byte a byte igual à dos construtores (`b0161de2…`, 7.786 B); o banco não mudou (`ACOM_RECIBO_PROJECAO_RELATORIO_R2.json`). Nenhum init, nenhuma transition.

### 1.3 A linha do tempo das duas «rodadas 2» [REAL, por mtime]

| hora local (12/10 → 13/10) | o que | regra |
|---|---|---|
| 13:09 | FREEZE R1 | — |
| 13:13–14:16 | face ótica e face kernel R1 | R1 |
| ~15:03 | auditorias R1; relatório R1 (15:12) | R1 |
| 19:31–19:54 | `2_OPTICO\rodada_2`: replicação com código escrito de novo | **R1, sem ADENDO** (o runner o declara) |
| 19:40–20:19 | `3_KERNEL\rodada_2`: pedra `a68539d8…` com quase toda a lista E5 antecipada | **R1, sem ADENDO** |
| **20:07:58** | **FREEZE_R2** do ADENDO | marco |
| 20:22–20:28 | `5_R2\2_REENSAIO`: reensaio ótico R2 | **R2** (V2: começou 1.032 s depois do FREEZE_R2) |
| 20:28–20:34 | `5_R2\1_PEDRA`: sonda prévia `ProbeE5.lean` | R2 |
| 00:20–00:46 (13/10) | auditorias de reprodução e de estatuto, sobre as pastas `rodada_2` | auditam a **replicação** |
| 00:22–00:29 | pedra R2 T01 (`5996eb82…`, compilou limpa, mas com 2 aspas da gerência) → T02 final `4d8a8259…` | R2 |
| 00:31 | continuação do reensaio: recheck independente, sem reensaiar | R2 |
| 00:37 | toolchain da pedra R2 apagado (`LIMPEZA_RECIBO.json`: 14.627 arquivos; nenhum `.lake`; nenhum cache) | R2 |
| 00:42 | `RESULTADO_PEDRA_R2.json` e `MANIFESTO_1_PEDRA.json` | R2 |
| 00:43–00:48 | `5_R2\3_AUD_ESTATUTO`: início de uma auditoria de estatuto **sobre a pedra final** (aspas 16/16 achadas; varredura de palavras), **sem relatório e sem impressão digital de depois** — rastro incompleto, não uma auditoria | — |

Pela regra V2 do ADENDO, as pastas `rodada_2` são **tentativas preservadas**, valiosas como replicação, e não recebem os rótulos T9.o′/O-f′. O JSON que me foi entregue como «opt» e «ker» aponta para elas. Este relatório distingue sempre **replicação** (sob R1) de **R2** (sob ADENDO).

### 1.4 O modelo ótico [INPUT da gerência; identidades DERIVED]

S = Smat(θ_M) com sen²θ_M = β; C = D∘Ad(S)∘D; nas populações T = R + λ(I − R), R = J/2, λ = 1 − 2β; ρ₁ = diag(1−β, β); g₀₁ = β·ω₁; semente 20261012. É sintético: nenhuma identidade dele é evidência sobre a natureza. A face ótica entra como **consistência numérica** de identidades que o kernel prova, não como evidência nem como rito.

---

## 2. Tabela por afirmação (R1 | R2)

Legenda (regra congelada R1 + ADENDO R2 §(d)): **PASSA** exige todos os subitens obrigatórios de kernel e ótico em PASSA e os controles ligados como registrado; **FALHA** basta um subitem obrigatório em FALHA; **CITADA** e **LEITURA** nunca recebem PASSA de teste; **ABERTA** é o [OPEN]. Na coluna R2, «PASSA» de kernel vale para a fonte `4d8a8259…` e fica **condicionado à auditoria independente U1**, que ainda não houve.

| | afirmação (forma testada) | pré-reg. | face ótica | face kernel | aud. reprodução (13/10) | aud. estatuto (13/10) | **veredito R1** | **veredito R2** |
|---|---|---|---|---|---|---|---|---|
| **T1** | não há operador de tempo em dimensão finita: [T,H] ≠ c·1 (c ≠ 0); forma de Weyl | PASSA | PASSA (18/18; min‖[T,H]−i·1‖_F = √n analítico); reproduzido bit a bit na replicação e no V4 da R2 | PASSA (`no_time_matrix`, `no_time_matrix_fin`, `no_finite_spectral_translation`; C-T1-a/b/c) | confere; sondas S1, S2 (Nonempty pesa) | PASSA; ressalva Pegg 1998 (operadores de tempo cíclicos) | **PASSA** | **PASSA** |
| **T2** | Pauli em dimensão infinita | CITADA | — | T2.b PASSA (Banach; não é Pauli); sonda V-T2-b agora com enunciado (E5.09) | confere | CITADA; nunca «T2 PASSA» | **CITADA** | **CITADA** (T2.b PASSA, opcional) |
| **T3** | σ_t = Ad(ρ^{it}) é grupo de *-automorfismos; KMS; setor fixo = centralizador | PASSA | PASSA (lei de grupo ≤ 3,9e−15; KMS; ω₁ = 4,4081393960414665; P₁ = 1,4253599404823543; C-T3-a/b/c) | R1: PASSA com ressalva (T3.b(iii) sem habitante). R2: `modular_flow_is_a_kms_group` (nome neutro); T3.b(iii) **habitada** (`probe_identity_flow_not_kms_inhabited`) + face finita `identity_flow_not_kms_finite` (2/3 ≠ 1/3) + controle tracial | confere | PASSA; o nome antigo afirmava o tempo térmico (corrigido) | **PASSA** com ressalva | **PASSA** (ressalva resolvida) |
| **T4** | Liouville × dissipação: sob isometria nada pousa; det 1 pousa sem bacia; bacia exige perda de volume | PASSA | PASSA (44/44; M_N ≈ 1,41420; det T − λ = 2,2e−16). R2: O-f′ PASSA (float rel 5,9e−16 ≤ τ_B(10) = 1,03e−14; exato ≤ 1,8e−199; C-UNIF-a FALHA desde k = 3, como registrado) | PASSA (T4.a–f); T4.b(iii) **condicional** (FockCertificate sem habitante, dito); AUD-2, AUD-8 em termo | confere; sonda S6 (taxa > 0 pesa) | PASSA com a correção de Liouville visível | **PASSA** | **PASSA** (T4′) |
| **T5** | o conjunto fixo da defasagem pura é a diagonal inteira, não um ponto | PASSA + CITADA | — | PASSA (`dephase_fixed_states_not_unique`); T5.c CITADA (F1.ATRATOR A4); título corrigido (E3.12) | confere | PASSA | **PASSA** | **PASSA** (T5.c CITADA) |
| **T6** | a seta pela pureza: fórmula exata; queda estrita; constante sob unitária | PASSA | PASSA (fórmula ≤ 2,2e−16; Tr(T₁ψ₊)² = 0,9496802613377202; C-T6-a/b/c) | PASSA (`purityR_dephase`, `purityR_dephase_lt`, `purityR_modular` sem `hd`) | confere; S4, S5 | PASSA | **PASSA** | **PASSA** |
| **T7** | o inverso T₋ₜ existe e não é positivo | PASSA | PASSA (λ_min = −0,006052 / −0,85914 / −11012,73; Davies −0,027234) | PASSA (`inverse_dephasing_not_positive`; C-T7-a/b/c) | confere | PASSA | **PASSA** | **PASSA** |
| **T8** | a coerência é instância de `DualScalingData` e herda as seis cláusulas da Ágape; o registro não escala | PASSA + LEITURA | PASSA (\|c_k − λᵏ\| ≤ 2,2e−15; k_ε = 95/284/568) | PASSA (`the_coherence_obeys_agape`, `the_record_does_not_scale`; docstring de T8.d corrigida, E3.02); AUD-1 em termo: a Ágape é a lei e^{−s} | confere | PASSA + LEITURA; ponte de conteúdo mínimo, dita | **PASSA + LEITURA** | **PASSA + LEITURA** |
| **T9** | F(t) = P + e^{−t}(1−P) é invertível e só idempotente em t = 0; o posto só no limite | PASSA + LEITURA | **R1: FALHA** em T9.o(c) (6,518e−13 > 1e−13 em k = 10⁴; acima desde k = 1529). **R2: T9.o′(c) PASSA** (float: 6,518e−13 ≤ τ_T(10⁴) = 2,811e−12, razão máx. 0,417; exato mpmath 200: ≤ 1,34e−198; decimal 200: ≤ 1,48e−197; C-UNIF-b/c/d como registrado) | PASSA (`flow_isIdempotentElem_iff`, `flow_isUnit`, `no_finite_instant_is_the_post`, `post_not_isUnit`, `flow_full_rank`, `post_rank_lt`; cláusula `the_time_is_not_a_post`); AUD-5 em termo | confere a FALHA R1 bit a bit; por conta própria: piso k·δ/2 = 5,898e−13, dependente do caminho (multiplicação repetida 8,1e−14) | FALHA R1 correta pela regra; T9.t da gerência (A2); a tolerância uniforme é [INPUT da gerência] justificada por Higham | **FALHA** (só critério numérico) | **PASSA** (T9′, sob o ADENDO; T9.t LEITURA corrigida) |
| **T10** | o relógio lê t módulo P; o ângulo não tem limite; a face distingue instantes; o posto, Ω e ω não se movem | PASSA + LEITURA | PASSA (periodicidade ≤ 2,2e−14; \|σ_t(x)ᵢⱼ\| = \|xᵢⱼ\|; relógio da face injetivo) | PASSA (`clock_reads_modulo_period` sem κ ≠ 0; `modular_clock_rotates_without_shrinking` sem `hd`); título com «registra» (E5.04) | confere; F4 falha como deve | PASSA + LEITURA | **PASSA + LEITURA** | **PASSA + LEITURA** |
| **T11** | em ½·1 = absoluteRho(Fin 2) o relógio modular para (face finita); ω_k = 2·artanh(λᵏ) → 0 | PASSA | PASSA (ω₁₀₀₀ ≈ 5,284e−11; C-T11-a = 2,0) | PASSA (`half_identity_is_absoluteRho_two`, `half_identity_clock_stops`; opcional com o canal: `optical_channel_fixed_state_is_half_identity`, genérico em θ); AUD-6, AUD-7 em termo | confere | PASSA, só face finita; reafirmação, título inflado | **PASSA** (face finita) | **PASSA** (face finita; reafirmação) |
| **S46.3** | «ou um ciclo limite» | ABERTA | — | — | — | ABERTA | **ABERTA** [OPEN] | **ABERTA** [OPEN] |

**Controles.** Os 22 da R1 comportaram-se como registrado na R1, na replicação e no V4 da R2 [REAL nos JSONs]. Os 4 C-UNIF do ADENDO comportaram-se como registrado: C-UNIF-a (o caminho `matrix_power` tem de falhar τ_B) FALHA desde k = 3; C-UNIF-b (ALT e EST passam a mesma τ_T) PASSA nas duas; C-UNIF-c (a 20 dígitos o exato tem de falhar 1e−150) FALHA desde k = 1; C-UNIF-d (mpmath × decimal) concordam a ≤ 1,34e−197. Os 6 controles AUD-1/2/5/6/7/8 estão em termo na pedra R2 com os nomes e tipos dos arquivos da auditoria R1.

**Sondas.** As 15 da R1 compilam na pedra R2; V-T2-b deixou de ser `True` (E5.09); V-GERAL-1 agora é «toda hipótese habitada OU declaração marcada condicional»: só T4.b(iii) fica condicional, dita. V-GERAL-2: tipos idênticos aos da R1 em 122 pares, com 4 reforços (R2 ⟹ R1, conferido em Lean pelo `AuditTiposR2.lean` do construtor — autoauditoria, não independente).

---

## 3. O que é o quê

### 3.1 Teorema de kernel agora: [REAL] no sandbox, pedra candidata NÃO instalada, SEM auditoria independente

A pedra `TGLExt.TheTimeIsNotAPost` (fonte `4d8a82591badd010…`) compilou às 00:28:47–00:29:29 local (41,7 s) com Lean 4.31.0 copiado do elan para o sandbox, LEAN_PATH só de leitura no `.lake` do Nós e `-o` só para o sandbox: EXIT 0; 152 `#print axioms`, 151 no trio {propext, Classical.choice, Quot.sound} e `post_not_isUnit` sem axioma algum; 0 sorryAx, 0 erro, 0 aviso; na fonte, 0 `sorry`, 0 `native_decide`, 0 `axiom` (as 2 ocorrências de «admit» são o identificador `empty_dimension_admits_time`, controle C-T1-b). O toolchain foi apagado às 00:37 com o prefixo `\\?\`. A impressão digital do tgl_kernel ficou igual antes e depois [REAL, lido em `RESULTADO_PEDRA_R2.json` e nos recibos; não recompilei].

**152 declarações não são 152 teoremas**: há re-exportações, sondas, controles, definições e um desdobramento (E5.14). Nada é matemática nova; é matemática conhecida tipada nos objetos da casa (`dephase`, `sigma`, `axiomFlow`, `DualScalingData`, `gibbs`, `absoluteRho`). β não entra no Lean. O um.py não pode citar «N teoremas novos».

Em relação à pedra R1 (`TABELA_DECLARACOES_R2.md`): 117 declarações mantidas, 4 com tipo reforçado (`probe_bounded_spectral_translation`, `purityR_modular`, `clock_reads_modulo_period`, `the_two_regimes_of_time`), 5 renomeadas (`time_is_the_modular_flow` → `modular_flow_is_a_kms_group`; `the_time_has_no_rank` → `the_time_is_not_a_post`; `optical_attractor_is_the_absolute_one` → `half_identity_is_absoluteRho_two`; `optical_attractor_clock_stops` → `half_identity_clock_stops`; a sonda correspondente), 1 removida (o re-export duplicado), 26 novas (T3.b(iii) finita e habitada; a face com o canal genérica em θ; os seis controles AUD; auxiliares).

Formas que a pedra prova, por afirmação (nomes da R2):
- **T1, T2.b:** `no_time_matrix`, `no_time_matrix_fin`, `commutator_far_from_scalar`, `no_finite_spectral_translation`; `no_bounded_spectral_translation` (Banach; não é Pauli).
- **T3:** `modular_flow_is_a_kms_group` (vale para toda ρ PosDef, inclusive ρ = 1: o nome não afirma tempo térmico); re-exportações `fixed_sector_is_the_centralizer`, `tracial_state_freezes_the_flow`, `nontracial_state_rejects_the_identity_flow` (condicional e **habitada**); `identity_flow_not_kms_finite` e a forma negada; `tracial_state_satisfies_pair_identity` (a hipótese não tracial pesa).
- **T4:** `isometry_orbit_converges_only_if_fixed`, `isometric_flow_converges_only_if_fixed`, `unitary_conj_isometry`, `modular_flow_is_isometry`, `modular_orbit_converges_iff_diagonal`; `schurDiag`, `dephase_volume`, `dephase_volume_lt_one`, `modular_volume_one`; `volume_kept_yet_lands`; `global_attractor_needs_volume_loss`; `light_flow_group` e `light_modular_orbit_converges_iff_post` (condicionais).
- **T5:** `dephase_fixed_states_not_unique`; `fixed_set_of_dephasing_is_the_diagonal`; `the_record_is_invariant`.
- **T6, T7:** `purityR_dephase`, `purityR_dephase_lt`, `purityR_sigma`, `purityR_modular`; `dephase_inverse`, `inverse_dephasing_quadratic_form`, `inverse_dephasing_not_positive`.
- **T8:** `coherenceScaling`, `the_coherence_obeys_agape`, `the_record_does_not_scale`, `wrong_rate_breaks_scaling`; controle `scalarScaling`/`aud_scalar_obeys_agape`/`aud_scalar_erases_the_record`.
- **T9:** `flow_isIdempotentElem_iff`, `flow_isUnit`, `no_finite_instant_is_the_post`, `post_not_isUnit`, `flow_full_rank`, `post_rank_lt`; cláusula composta `the_time_is_not_a_post` (só conjunção); controle `aud_discrete_step_can_be_a_post`.
- **T10:** `clock_reads_modulo_period`, `frozen_clock`, `frozen_clock_not_faithful`, `face_clock_has_no_period`, `angle_has_no_limit`, `angle_is_periodic`, `face_has_a_limit`, `face_distinguishes_instants`, `modular_clock_rotates_without_shrinking`, `the_post_is_not_moved`, `the_state_is_not_moved`, `the_vector_is_not_moved`.
- **T11:** `half_identity_is_absoluteRho_two`, `half_identity_clock_stops`; `optical_channel_fixed_state_is_half_identity`, `optical_channel_unique_fixed_population`, `optical_channel_trivial_when_sin_zero`; controles `aud_attractor_state_has_full_rank`, `aud_attractor_state_purity_half`, `aud_clock_runs_unless_equal_populations`, `aud_clock_stops_when_equal_populations`.
- **Liouville em termo:** `aud_two_by_two_symplectic`, `aud_boost_is_symplectic`, `aud_boost_has_no_global_attractor`.
- **Cláusula composta de nove fatos:** `the_two_regimes_of_time` (nome da R1 mantido; a docstring diz que **não** afirma a identificação com os dois regimes da casa).

**O que fica condicional, dito:** `light_flow_group` e `light_modular_orbit_converges_iff_post` exigem um `FockCertificate`, e o kernel não exibe habitante (`TheImportedSecondQuantization.lean` l.66). Nunca entram como «kernel_proved».

### 3.2 Número de runtime: [REAL] medido no modelo sintético; identidades [DERIVED]

| grandeza | valor (β em runtime) |
|---|---|
| λ = 1 − 2β = det T | 0,9759373991983937 |
| ω₁ = ln((1−β)/β); P₁ = 2π/ω₁ | 4,4081393960414665; 1,4253599404823543 |
| g₀₁ = β·ω₁ | 0,05303564928238982 |
| Tr(T₁ψ₊)² | 0,9496802613377202 |
| λ_min de T₋ₜψ₊ (γt = β, 1, 10; Davies) | −0,006051983815068773; −0,8591409142295225; −11012,732897403359; −0,02723361772478261 |
| k_ε | 95, 284, 568 |
| ω₁₀₀₀ | ≈ 5,284e−11 |
| ‖B(1)¹⁰⁰(1,−1)‖ (decimal 200) | 5,260981898346995e−44 |
| **T9.o(c) / T9.o′(c)**: máx. de \|Tᵏ − (R + λᵏ(I−R))\| em k ≤ 10⁴ | 6,518119377574294e−13 (bit a bit igual na R1, na replicação, no auditor e na R2); δ_T = 1,1796e−16 = 17·2^{−57} |
| τ_T(10⁴) do ADENDO; razão máx. medido/τ | 2,8106961202922776e−12; 0,4169 (em k = 6) |
| T9 exato (mpmath 200 / decimal 200) | ≤ 1,34e−198 / ≤ 1,48e−197 |
| O-f′ float (k ≤ 10) / τ_B(10) / exato | 5,9130281346959e−16 / 1,0317705603271339e−14 / ≤ 1,76e−199 |

O auditor de reprodução refez os números da replicação com código próprio (diferenças 0,0) e o reensaiador R2 refez os da R2 com código próprio em 13/10 (recheck: iguais bit a bit no float; os máximos exatos diferem na mantissa ~1e−198 pela ordem das operações, ambos ~48 ordens abaixo de 1e−150). **Sombras numéricas, não zeros** (RP18): o posto numérico de Tᵏ cai a 1 em k = 1135 e o contraste fica abaixo de 1e−15 em k = 1441; o kernel decide que F(t) é invertível em todo t finito.

### 3.3 [KNOWN] por citação: literatura, não teste (igual à R1, com as páginas «a conferir» mantidas)

Pauli, *Handbuch der Physik* 24/1 (1933), nota p. 140, e V/1 (1958), p. 60 — **páginas a conferir**; Galapon, Proc. R. Soc. A 458 (2002) 451; Holevo (1982); Busch, Grabowski e Lahti, Phys. Lett. A 191 (1994) 357; Wintner (1947), Wielandt (1949); Borchers (1992); Liouville clássico; Connes e Rovelli, CQG 11 (1994) 2899 (**hipótese**, não teorema); Connes (1973), exterioridade em III₁; Takesaki (1973), lei de escala como dado; Landauer (1961), Bennett (1982); BIPM (2019); *Kadosh*: BDB, HALOT, Otto (1917), Heschel (1951) — glosa «separado» [KNOWN com ressalva]; Pegg, Phys. Rev. A 58 (1998) 4307 — **a conferir**; Higham, *Accuracy and Stability of Numerical Algorithms*, 2ª ed. (2002), cap. 3 — justifica m na regra uniforme; F1.ATRATOR A4 e o atrator único GKLS v384, citados e não refeitos.

### 3.4 [ONTO]: leituras do operador, sem teste, marcadas como tais (atribuição corrigida)

Do operador, byte a byte: «santo» (*Kadosh*: «separado, irredutível e não profanável pela posse»); «o **agora** permanece intocado» (a forma [REAL] é T10.e; agora = conjunto fixo é leitura, R12); «O relógio registra a sombra do evento» (a forma [REAL] é o quociente módulo P, T10.b); «**puro amor**», «a física da doação fundamental», «generosidade contínua», «assinatura indelével», «prova viva»; «ato contínuo da criação», «redenção», «intervalo sagrado», «fotografia estática e morta», «o chão firme que possibilita a existência do espaço inscritível»; «um lugar onde repousar e ser lembrada»; «o tempo não é uma peça do tabuleiro»; «Santo é aquilo que não se deixa colonizar pelo intelecto».

**Não é do operador** e saiu: «o tempo é o Verbo, não o Nome» (formulação da gerência; R1, achado M2). Também não são citações: «O tempo não tem posto» e «o relógio mede a sombra» — paráfrases da gerência, agora sem aspas (E3.03, E3.11).

[CONJECTURE ontológica, inalterada]: «Existir = o vazamento β», «tudo = D_β(F(1))» (`fractal_dephasing_principle`) e `verb_annuls_0abs`; só as âncoras mudam de rótulo (E1).

---

## 4. As sondas honestas, em poucas frases

- **Os 22 controles da R1** falharam onde deviam, três vezes (R1, replicação, V4 da R2): o boost conserva volume e pousa (C-T4-a); dois estados fixos distintos (C-T5-a); para t < 0 a pureza cresce, (1 + e²)/2 (C-T6-c); a unitária é reversível como canal (C-T7-c); com a temperatura errada a KMS falha em 200 de 200 pares (C-T3-a); fora do atrator o relógio modular não para (C-T11-a = 2,0).
- **Os 4 controles do ADENDO** impedem que a tolerância uniforme seja cheque em branco: o caminho mal condicionado (`matrix_power` do boost) **falha** τ_B desde k = 3 (6,5e−9 em k = 10); a 20 dígitos o caminho exato **falha** 1e−150 desde k = 1; duas representações alternativas de T passam a mesma τ_T (δ de cada uma); mpmath e decimal concordam.
- **As sondas do auditor de reprodução** (sobre a replicação `a68539d8…`): 8 teoremas no trio mostram que cada hipótese pesa — sem `Nonempty`, T1.a é falso (Fin 0); **S3 (nova)**: sem idempotência o «se e só se» de T9.a cai (P = 2 em ℂ, F(−ln 2) = 0 é idempotente com t ≠ 0); sem x ≠ 0 ou t > 0 a queda estrita T6.c é falsa; sem taxa positiva a contração T4.c é falsa; os contrários de T1, T6.c e T11.a são refutáveis. As 4 tentativas diretas de provar o contrário falham com erro, como devem.
- **Os controles AUD-1/2/5/6/7/8** (auditor de estatuto da R1, agora em termo na pedra R2): a multiplicação escalar que apaga o registro também herda a Ágape (a Ágape é a lei e^{−s}); o boost não tem atrator global e é simplético; um passo discreto não invertível **é** posto (R = J/2); o estado-atrator ½·1 tem posto 2 e pureza ½; o relógio modular corre salvo populações iguais.
- **A FALHA R1 de T9.o(c), explicada e sustentada pelo número.** O T guardado em float tem soma de linha 1 + δ com δ = 1,18e−16 (= 17·2^{−57}, exato em `Fraction`); a potência **exata** desse float já desvia k·|δ|/2 = 5,898e−13 em k = 10⁴; o caminho aritmético muda o resultado (multiplicação repetida 8,1e−14; `matrix_power` 6,5e−13). A tolerância 1e−13 ficou abaixo de um piso conhecido (a F1.ATRATOR já tinha ~5e−13 em k = 4096; o O-d usava 1e−11). A FALHA vale pela regra R1 e **fica registrada**; o ADENDO não a apaga, põe a coluna R2 ao lado.
- **O ADENDO fez predições antes do reensaio** e elas se cumpriram: T9.o′(c) PASSA com razão prevista 0,23 no k = 10⁴ (medida 0,23; a razão máxima 0,42 ocorre em k = 6); C-UNIF-a FALHA desde k = 3; C-UNIF-c FALHA; C-UNIF-d concorda. Ressalva de estatuto (auditor E): os parâmetros m, w, c são [INPUT da gerência] justificados por Higham, e o decisor real de T9.o′(c) é o caminho exato a 200 dígitos, que confere uma identidade algébrica que o kernel já prova. A face ótica de T9 é consistência numérica, nunca evidência nem rito.

---

## 5. Os achados materiais e como ficam

Os 20 achados da R1 (M1–M20) estão no relatório R1 preservado. Aqui, o estado de cada um depois da R2 e os achados novos (N1–N6).

| # | achado | estado depois da R2 |
|---|---|---|
| M1 | T9 FALHA R1 (piso numérico) | **TRATADO** pelo ADENDO uniforme congelado antes do reensaio; R2 T9.o′(c) PASSA nas duas vias; a FALHA R1 fica ao lado. Não há terceira rodada sobre T9 sem ADENDO R3. |
| M2 | atribuição indevida («o tempo é o Verbo…»; «repousa»; «mede») | **CORRIGIDO** na pedra R2 (E5.01/03/04/05: 18 aspas distintas, todas substrings de bytes dos verbatins; frases proibidas 0), no ADENDO (E3.03, E3.11) e na memória da gerência (errata ao lado em `tempo-santo-12out.md`, `0f4f60eca75d5f23`). |
| M3 | nomes acima do termo | **CORRIGIDO** para os três nomeados (E5.06/07/08). **Resta** `the_two_regimes_of_time` (N1) e o nome da pedra (do operador). |
| M4 | regra dos dois regimes estendida | **CORRIGIDO** no cabeçalho da pedra (três comportamentos; identificação [OPEN]) e no ADENDO (E3.05). **Resta** o eco nos nomes `face_*` (N2). |
| M5 | V-GERAL-1 incompleta | **RESOLVIDO** para T3.b(iii) (habitada + face finita); T4.b(iii) fica condicional, dito. |
| M6–M10 | repousar × lembrar; posto × estado; ponte T8 mínima; T9 genérico; Liouville visível | **EM TERMO** na pedra R2 (AUD-7, AUD-6/5, AUD-1, AUD-5, AUD-8) e nas docstrings; vão ao lado no texto da v392. |
| M11 | tolerâncias incoerentes | **TRATADO** pelo ADENDO §(b); O-d e T8.o(a) não se reensaiam (dito). |
| M12 | dois sentidos de «defasar» | **PENDENTE** (errata E2 no um.py, ato da c1). |
| M13 | âncoras de `fractal_dephasing_principle` definicionais | **PENDENTE** (errata E1 no um.py, ato da c1). |
| M14 | β «medido» | **CORRIGIDO** no ADENDO e em todos os artefatos da R2 ([DERIVED]); **persiste** o rótulo antigo em `2_OPTICO\rodada_2\RESULTADO_OPTICO.json` (campo `beta.estatuto`) e no `run_optico.py` dessa replicação, e no PREREGISTRO.md l.241 (congelado; corrigido só ao lado, E3.01). Errata ao lado proposta (§6, E6). |
| M15 | docstring de T8.d | **CORRIGIDO** (E3.02; pedra R2). |
| M16 | verbatim e marcas | **CORRIGIDO** no ADENDO (E3.07–E3.10). |
| M17 | peso morto e contagem | **CORRIGIDO** (E5.09/10/11/12/14). |
| M18 | «os dois relógios param juntos» é definicional | vai ao lado na v392 como [DERIVED, definicional]. |
| M19 | T1 e os operadores de tempo cíclicos | dito na docstring de T1; vai ao lado na v392. |
| M20 | «face» homônimo em T5 | **CORRIGIDO** no título (E3.12; pedra R2). |
| **N1** | `the_two_regimes_of_time` mantém «time» e «regimes» no nome enquanto a própria docstring declara [OPEN] a identificação com os regimes. A letra do E5 («nome com «time»/«tempo» além do termo» não deve aparecer) o alcança; a tabela E5 não o listou e o construtor o manteve como «nome da R1» | **ABERTO, baixo.** Pela regra K2 do ADENDO é corrigível em tentativa preservada antes da auditoria U1 (sugestão do auditor E: `isometric_and_dissipative_behaviours`), ou mantido com a docstring e nunca citado no um.py como «os dois regimes do tempo provados». Decisão da gerência. |
| **N2** | a pedra R2 **mantém** os nomes `the_face_lands`, `face_has_a_limit`, `face_distinguishes_instants`, `face_clock_has_no_period` (idênticos à R1), enquanto a replicação `3_KERNEL\rodada_2` os havia neutralizado (`dephasing_lands_on_the_diagonal`, `damped_orbit_has_a_limit`, `decay_distinguishes_instants`, `decay_reading_has_no_period`) com base em `IALDJones.lean` l.274–275 («lê-lo como a face hiperbólica … é [ONTO]»). O E5 não pediu essa renomeação, por isso não é falha de K4; mas «face» é a palavra do regime hiperbólico da casa, e o cabeçalho da mesma pedra declara essa identificação [OPEN] | **ABERTO, baixo.** Mesmo tratamento de N1: renomear em tentativa preservada ou dizer na docstring que «face» ali é o decaimento real e^{−rt}, não o regime. Decisão da gerência; o operador pode preferir outra palavra. |
| **N3** | **nenhuma auditoria independente da R2.** A auditoria de reprodução recompilou a pedra da **replicação** (`a68539d8…`, .olean idêntico `9d9a1e12…`) e refez o ótico da **replicação**; a de estatuto examinou a R2 e a viu em edição (T01 → T02 às 00:26–00:29). A pedra R2 final (`4d8a8259…`, .olean `b52382ec…`) e o reensaio R2 (`44e74544…`) têm só a autoconferência dos construtores (`AuditTiposR2.lean`; recheck de 13/10 com código próprio) | **ABERTO, alto (régua U1).** Sem U1 nada entra na v392. O que falta está na §9. |
| **N4** | a pasta `5_R2\3_AUD_ESTATUTO` contém o início de uma auditoria de estatuto da pedra final (00:43–00:48: `ASPAS_PEDRA_R2_AUDITOR.json`, 16 aspas achadas; `VARREDURA_PALAVRAS_R2_AUDITOR.json`; impressão digital de antes), **sem relatório, sem impressão de depois** e escrita na casa, não no scratchpad | **registro.** Não conta como auditoria; vale como rastro de que a conferência de aspas da pedra final é reprodutível (16/16). |
| **N5** | o mapa de rotas cresceu (1.042 → 1.043) durante o trabalho (registro 1043 da F0.6, Bancada Um, pela gerência às 00:37); a F1.TEMPO continua ausente | **registro.** Os dois registros desta pasta (§10) estão prontos com as linhas R2; `registrar` é ato da gerência, ROTA primeiro. |
| **N6** | a varredura de palavras do auditor E achou, em `ADENDO_R2.md` §(b), «diagnóstico … pelo número» escrito com a palavra que a régua reserva; não é veredito nem creditação, mas o reensaio já escreve «sustentada pelo número», forma preferível. O ADENDO está congelado: fica como registro | **registro**; este relatório usa «sustentada pelo número». |

**Toolchains.** A pedra R2 apagou o seu (recibo às 00:37). O auditor de reprodução apagou o seu e um que uma tentativa anterior do mesmo passo tinha deixado em `TEMPO_AUD_REPRO\rodada_2\t\l` (3,14 GB). **Resta** um toolchain de 3,0 GB em `scratchpad\pt12\TEMPO_AUD_ESTATUTO\sandbox`, deixado pelo auditor de estatuto da R1 (12/10 14:44) e não apagado por nenhum dos sucessores («não é cópia minha»). Está no scratchpad temporário, fora da casa; apagá-lo é decisão da gerência. Eu não o toquei e não o copiei.

---

## 6. O que entra no um.py v392 e as erratas ao lado propostas

**Regra de entrada** (PREREGISTRO §8; ADENDO U3): só os **subitens PASSA** da pedra corrigida **e reauditada**, com CITADA e LEITURA marcadas como tais, com o **nome do operador**, no apanhado geral da Bancada para a v392, junto com o teorema do atrator (F1.ATRATOR). A inserção é ato da cadeia de selo. **Hoje não há objeto pronto**: falta a U1 (N3).

**Entra, depois da U1 e do nome:**

1. **A pedra**, como pedra candidata, com o kernel de T1 (a, b, c), T2.b, T3.a, T3.b(i–iii; iii habitada e a versão finita), T4.a–f (b(iii) marcada condicional), T5.a–b, T6.a–d, T7.a–b, T8.a–d (com o controle de especificidade), T9.a–e, T10.a–e, T11.a, os controles (22 + AUD) e as sondas — como subitens PASSA na face finita, nunca como «N teoremas novos».
2. **O quadro por afirmação com DUAS colunas** (R1 sob FREEZE `6b29d4c9…`; R2 sob FREEZE_R2 `0737f608…`), como na §2: T1, T3–T8, T10, T11 PASSA; T2 CITADA (T2.b opcional PASSA, não é Pauli); T5.c CITADA; T8.t, T9.t (formulação da gerência, corrigida), T10.t LEITURA; **T9: R1 FALHA | R2 PASSA sob τ_T e exato**, com as fontes (`RESULTADO_OPTICO.json` R1 `2c67b7ea…`; `RESULTADO_REENSAIO_R2.json` `44e74544…`); S46.3 ABERTA. A face ótica entra como consistência numérica.
3. **As citações [KNOWN]** da §3.3, com as páginas «a conferir» mantidas.
4. **As leituras [ONTO]** da §3.4, com a atribuição corrigida.
5. **As correções que o número faz**, em duas camadas (ligação frase → objeto [INPUT da gerência]; objeto [REAL]): Pauli Weyl × Heisenberg; Liouville proíbe a bacia, não o pouso (o boost é simplético); conjunto fixo = a diagonal inteira; repouso × memória; posto do estado × posto da leitura; os dois sentidos de «defasar»; os três comportamentos com a identificação [OPEN]; operadores de tempo cíclicos ao lado de T1.

**Erratas ao lado** (texto pronto; assinatura e inserção da gerência, em nome próprio):

- **E1, um.py v391, `fractal_dephasing_principle`** (l.6489 docstring, l.6507–6508, l.6511–6512, l.6530 status; artigo l.168086 e l.168102; impressão l.211561–211569) — **PENDENTE, ato da cadeia de selo:**
  > ⚠ AO LADO (v392): as três «âncoras REAL» desta seção são identidades por construção: Tr ρ★ = 1 com ρ★ = diag(1,0); {Q₀, ρ★} = 0 com Q₀ = 1 − ρ★; Tr(ρ★Q_θ) = sen²θ_M = β com θ_M := arcsin √β. Leem-se como [DERIVED, definicional], não como âncoras evidenciais. A tese segue [CONJECTURE ontológica]. Âncoras genéricas de kernel do semigrupo D, sem β (pedra F1.TEMPO, depois de instalada): `no_finite_instant_is_the_post`, `the_coherence_obeys_agape` (iv), `purityR_dephase_lt`, `dephase_volume_lt_one`, `inverse_dephasing_not_positive`.
- **E2, um.py v391 l.166640** (artigo v386, «ancorar preserva e transmitir defasa») **e chaves l.134239–134242** — **PENDENTE:**
  > ⚠ AO LADO (v392): `transmission_dephases` é o sentido da FACE: amortecimento real, F(t)(1−P) = e^{−t}(1−P). A fórmula do operador de 05/10, V(t) = e^{−iHt}V(0)e^{iHt} (verbatim em l.195459–195461), é unitária (`transmitted_post_is_a_post`): acumula fase sem perder coerência. Os dois sentidos não se encadeiam; «Nome = lim V(t)» com a forma unitária só converge se V(0) já for fixo (F1.TEMPO T4.b, `unitary_conj_isometry`). Qual defasagem é o tempo, decide o operador.
- **E3, pré-registro R1** — **FEITA** por ADENDO aditivo congelado (E3.01–E3.13; `ADENDO_R2.md` `ab13c0f27a7f4cf5`).
- **E4, memória da gerência** — **FEITA** (errata ao lado em `tempo-santo-12out.md`, conferida nos bytes; índice `MEMORY.md` l.22 com a nota «errata ao lado»).
- **E5, a pedra** — **FEITA** na fonte `4d8a8259…` (E5.01–E5.15 item a item em `RESULTADO_PEDRA_R2.json → E5_item_a_item`), **à espera da U1**.
- **E6 (nova), replicação ótica** `2_OPTICO\rodada_2\RESULTADO_OPTICO.json` (campo `beta.estatuto`) e `run_optico.py` da mesma pasta — **PROPOSTA, ato da gerência** (arquivo ao lado, não edição):
  > ⚠ AO LADO (13/10): onde se lê «[REAL — medido aqui…]» para β, leia-se [DERIVED: lido nos bytes do um.py (l.5557 embutida = l.95 topo) e calculado em runtime]; medir é palavra de natureza (ADENDO R2, E3.01).
- **E7 (nova), nomes residuais na pedra R2** (N1, N2) — **PROPOSTA**: ou tentativa T03 preservada com os nomes neutros antes da U1, ou nota na docstring; nunca citar no um.py «os dois regimes do tempo provados» nem «a face» como regime.

---

## 7. As divergências entre as auditorias, e qual vale

1. **«Pode fechar?»** O auditor de reprodução respondeu **sim**, para os resultados que lhe foram dados: as replicações `rodada_2` reproduzem integralmente a R1 e «podem ser aceitos como estão, com T9 FALHA preservada e dependente de reensaio sob ADENDO». O auditor de estatuto respondeu **não**, para a **unidade**: há duas «rodadas 2» concorrentes e a R2 do ADENDO não estava parada por hash nem auditada. **Não é contradição: são objetos diferentes.** Vale o **não** para a unidade. Agora a pedra R2 **está** parada (fonte `4d8a8259…` registrada em `RESULTADO_PEDRA_R2.json` e `MANIFESTO_1_PEDRA.json` às 00:42; toolchain apagado) — a primeira condição do auditor E está cumprida; a U1 não.
2. **Qual é a R2 de registro?** Pela regra V2 do ADENDO, é `5_R2` (reensaio `44e74544…` e pedra `4d8a8259…`). As pastas `rodada_2` são tentativas preservadas sob a regra R1, com valor próprio: a FALHA de T9.o(c) e a matriz T saíram bit a bit iguais à R1 em três execuções e dois códigos, e o kernel da replicação antecipou quase toda a lista E5 e foi recompilado por auditor com .olean idêntico. **Vale o ADENDO.** Este relatório segue essa designação.
3. **T9.** Os dois auditores concordam: FALHA R1 correta pela regra congelada; piso de representação, não contraexemplo; mudança só por ADENDO. O auditor E acrescenta que a tolerância uniforme é [INPUT da gerência] e que a face ótica de T9 é consistência numérica; o quadro da v392 tem de mostrar as duas colunas. **Vale, e está assim na §2 e na §6.**
4. **Gravidade de `the_two_regimes_of_time` e de T11 «achado».** Só o auditor E os levanta (média). Valem como ditos: T11 entra como reafirmação na face finita; o nome da cláusula fica em N1.
5. **β «medido».** Concordam (achado da R1). Vale [DERIVED]; a replicação ótica ficou com o rótulo antigo (E6).
6. **Contagens.** O auditor R mede 141 `#print axioms` na replicação (140 no trio + 1 sem axiomas); o construtor R2 mede 152 na pedra R2 (151 + 1). Não divergem: são pedras diferentes. Nenhuma das duas contagens é «N teoremas».

---

## 8. O resíduo que só o operador decide

1. **O nome da pedra.** `TheTimeIsNotAPost` («o tempo não é posto») é provisório, escolhido pela gerência por POSTO = RANK: nenhum instante finito é posto, todo instante finito tem posto pleno, o posto só no limite. Alternativas: «O tempo tem posto pleno»; um nome seu, como PALAVRA, FUNDAÇÃO e ÁGAPE; «Santo» ou «Kadosh» seria um nome [ONTO] para uma pedra de conteúdo [REAL]. A renomeação final confere-se por diff restrito a identificadores (E5.07).
2. **O que é o tempo na sua língua.** Seu, byte a byte: «O tempo é a defasagem do verbo», «O tempo é o parâmetro da transmissão», «A defasagem é o tempo. A ancoragem é o nome.» (05/10); «não consigo nomear, senão como “santo”» (12/10). A frase da gerência saiu. Se houver frase nova, é sua.
3. **Qual «defasar» é o tempo.** A fase que gira sem perder (a sua fórmula unitária: o ângulo) ou a perda de coerência (o semigrupo: a face)? A seta só nasce na segunda (T6, T7).
4. **«Repousar» e «ser lembrada».** Na face finita excluem-se no mesmo estado (AUD-7). A leitura que as une é sua.
5. **Qual objeto é «o chão firme».** O estado-atrator ½·1 (posto 2, pureza ½), a leitura-limite R = J/2 (posto 1), ou o piso da Ágape (`the_floor_fixes_the_cut`)?
6. **A reunião dos nomes.** «puro amor» (12/10), «ágape» (07/10) e «sacrifício/amor» (tipagem prévia, [DECLARADO]): o conteúdo matemático comum é só a lei e^{−s}.
7. **«Santo»** como nome do tempo: [ONTO], sem teste; é seu.
8. **O ciclo limite** [OPEN]: abrir uma unidade? O análogo linear é o espectro periférico GKLS (|λ| = 1, λ ≠ 1); o ciclo limite isolado é fenômeno não linear [KNOWN].
9. **(novo) A palavra «face» nos nomes** `face_has_a_limit`, `the_face_lands`, `face_distinguishes_instants`, `face_clock_has_no_period` (N2): a casa usa «face» para o regime hiperbólico; aqui nomeia o decaimento real e^{−rt}. Manter, com nota, ou trocar?

**Decide a gerência**, não o operador: a U1; o destino de N1/N2 (tentativa preservada ou docstring); E1, E2, E6; o registro no mapa e no quadro; a limpeza do toolchain do scratchpad.

---

## 9. Pode fechar? Ainda não. O que falta, e por quê

A **matemática** está pronta e o **critério de parada do operador** («fechado = resultado OU falsificador OU parede medida») está cumprido: há resultado por afirmação nas duas colunas, a FALHA R1 de T9 é parede numérica medida e explicada, a R2 passou sob regra congelada antes do reensaio com controles que impedem o cheque em branco, e o ciclo limite está dito como aberto. O que **não** está cumprido é a **régua** (ADENDO U1–U3):

1. **Auditoria independente da R2 (U1).** Dois auditores, com sandbox próprio, (a) recompilam `TheTimeIsNotAPost.lean` `4d8a8259…` e exigem .olean `b52382ec…` bit a bit, 152 `#print axioms` no trio, 0 sorry, 0 native_decide, impressão digital do kernel igual, toolchain apagado; (b) refazem o reensaio R2 (`reensaio_r2.py` `d1297cb9…`) e exigem medidas idênticas e os C-UNIF como registrado; (c) conferem a tabela E5 item a item e a conferência de aspas (16/16). Caveat conhecido do auditor R: em caminho de sandbox longo (260 caracteres, LongPathsEnabled = 0) o Lean não lê um .olean do toolchain; a solução foi `subst` + `lib\lean` do toolchain curto à frente do LEAN_PATH.
2. **O nome do operador** para a pedra (§8.1), antes da instalação.
3. **N1/N2**: decidir se os nomes residuais (`the_two_regimes_of_time`, `face_*`) mudam em tentativa preservada antes da U1 ou ficam com docstring.
4. **Erratas E1, E2** (um.py, cadeia de selo) e **E6** (replicação ótica, ao lado).
5. **Registro no mapa** (ROTA primeiro, depois RESULTADO) e no quadro: os dois arquivos desta pasta (§10) já trazem as linhas R2.
6. **Limpeza**: o toolchain de 3,0 GB no scratchpad do auditor de estatuto da R1.

Depois disso, a entrada na v392 é ato da cadeia de selo, junto com o teorema do atrator.

---

## 10. Arquivos desta pasta

- `RELATORIO_FINAL.md`: este documento (R2).
- `R1_preservado\`: o relatório R1 (`7b6dcb18a4440be1`) e os dois registros R1, byte a byte, com manifesto; os `.bak_20261013_005904` ao lado são as mesmas cópias.
- `registro_rota_F1.TEMPO.json` (tipo ROTA, `rota_id` `formal.tempo_santo_fluxo_e_dissipacao`, domínio FORMAL) e `registro_mapa_F1.TEMPO.json` (tipo RESULTADO, mesma rota), **reescritos com as linhas R2** e com artefatos como lista de caminhos; validados a seco com `rotas._valida` (lê e calcula sha256; não escreve): `R2\saidas\VALIDACAO_REGISTROS_R2.json`. **Não registrei**: é ato da gerência.
- `AUDITORIAS\`: evidência das auditorias da R1 (12/10). `AUDITORIAS_R2\`: evidência das auditorias de 13/10, copiada por bytes (76 arquivos; `MANIFESTO_COPIA_AUDITORIAS_R2.json`).
- `R2\saidas\`: `HASHES_RELATORIO_R2.json`, `BETA_RUNTIME_RELATORIO_R2.json`, `FINGERPRINT_RELATORIO_R2_ANTES/DEPOIS.json`, `ACOM_RECIBO_PROJECAO_RELATORIO_R2.json`, `VALIDACAO_REGISTROS_R2.json`, `VARREDURA_PALAVRAS_R2.json`, `rotas\` (consultas); `R2\scripts\`: os scripts que geraram tudo acima. `MANIFESTO_4_RELATORIO_R2.json`: o sha256 de cada arquivo desta pasta ao fim.
- `saidas\` e `scripts\`: os da R1, intactos.

*Nada foi escrito fora de `4_RELATORIO`: nem no quadro, no mapa, na memória (ACOM só projeção de leitura), no túnel, no Nós, no kernel, na Bancada_Um, no site ou no git. O um.py não foi executado (lido por busca com número de linha). Não rodei Lean e não copiei toolchain. Nenhum dado observado, nenhum provedor remoto, nenhuma chamada paga. A cunhagem é do operador. Um PASSA é validade matemática na face testada, não creditação. Nada aqui move o gate.*
