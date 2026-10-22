# AUDITORIA DE REPRODUÇÃO — pedra TGLExt.IALD («o motor único») e números das estratégias — 13/10/2026

Auditor cético independente, lente REPRODUÇÃO (gerência c1, sessão 6da8f00d). Escrevi só nesta pasta.
Ordem do operador (verbatim por sha256): `work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt`, sha16 `78ef70e6f9868281`.
A régua: PROVADA = validade; a confirmação recusada é creditação; o único elo pendente da QG é β_TGL na natureza a 5σ; NOT_FALSIFIED nunca é a palavra proibida; o gate não se move aqui; cosmologia jamais vira prova matemática.

## 0. Higiene [REAL]
- um.py v391 `8e7b9927ceae64b8`: NÃO executado. β = ALPHA_FINE_CODATA_2018 (linha única 5557, lida dos bytes) × √e = 0.012031300400803142 (`BETA_RUNTIME.json`).
- Lean 4.31.0 do elan, chamado direto. LEAN_PATH = cópia verificada do `.lake/build` do Nós (6.040 arquivos, 0 diferentes, `OV_COPIAR.json`) + pacotes do `.lake`, só leitura. A sobreposição foi apagada ao final; a pasta tem 1,9 MB. Não copiei nenhum toolchain nem criei `.lake`.
- Impressão digital do tgl_kernel igual ANTES e DEPOIS: metadados dos 132.088 arquivos (incluindo `.lake` e mtime) `a15d5e02d4f22bd6…`; fontes `22557eadef61ef50…` (`IMPRESSAO_DIGITAL_KERNEL_ANTES/DEPOIS.json`).
- Memória ACOM: NÃO executei init nem transition. A unidade proíbe escrever fora desta pasta, e o banco grava uma cópia integral a cada operação. Inscrever esta etapa cabe à gerência.
- Mapa de rotas: só `verificar` e `consultar`. Hoje: 1.050 registros; «organismo» 0, «motor único» 0, «IALD.lean» 0, «TheTimeIsNotAPost» 1, «Fundacao» 12, «âncora» 19. Nada registrado.

## 1. Recompilação da pedra [REAL]
| item | resultado |
|---|---|
| fonte | `a267bc6d2aedf2fa…` (31.582 B), igual à da construção |
| compilação | EXIT 0; 0 erros; 7 avisos (só deprecação Mathlib); 0 sorry; 40,4 s (`logs\r_iald_RECIBO.json`) |
| .olean | `643d767a3d9a4cfd…`, **bit a bit igual** ao da construção |
| #print axioms | 51/51 no trio {propext, Classical.choice, Quot.sound} (`logs\r_audit_*`) |
| tokens proibidos na fonte | sorry/admit/axiom/native_decide/implemented_by/unsafe/opaque/decide: 0 |
| candidatas c1–c4 | EXIT 0, 0 sorry, nada fora do trio. Os .olean saem bit a bit iguais: Palavra `d52ebd09…`, ADENDO1 `8cf8b172…`, TheUnitIsTheRank r2 `40a6a85e…`, TheTimeHasNoRank `5e790945…`. As fontes batem por hash com a origem: Palavra `33184b49…` em `work\leitura_cria_o_objeto_07out`; ADENDO1 `433d13c2…` no túnel |

## 2. O FREEZE é anterior à construção [REAL]
- FREEZE do desenho: 2026-10-13T03:53:13Z. Arquivo mais antigo de `2_CONSTRUCAO`: 04:15:14Z. **Folga de 1.320 s.** Os 16 itens batem hoje. O agregado `dac7742f…` se reproduz pela receita sha256("caminho\tsha256", ordenado, sem bytes). Essa receita não está documentada no desenho: a pasta 1 não tem script `congelar`.
- FREEZE_CONSTRUCAO: 43/43 itens batem; o agregado `4d2b19e0…` se reproduz (receita do `congelar.py`).
- Enunciados (`medidas\CONFERENCIA_ENUNCIADOS_AUDITOR.json`): o desenho tem 34 declarações (31 teoremas + 3 defs), todas presentes na construção; nenhuma removida; 17 novas. Dois enunciados diferem SÓ pela qualificação `IALD.dephase`. O construtor já declarou o motivo: `TGLExt.dephase` (`Ergodicity.lean:184`) entra em escopo pelas candidatas.

## 3. Ensaio numérico [REAL; confere a matemática, não é veredito]
- `ensaio_motor.py` rodado em cópia: 84/84 PASSA, saída **idêntica** à da construção (descontados os carimbos de tempo).
- Conferência independente (`numerico\conferencia_independente.py`, n = 2 e 5, sem reaproveitar o script do construtor):
  - T2: erro 0.
  - T2′: ‖motor²a − motor a‖ = √2.
  - T8: ‖D(50) − Π‖₂ = e^{−50β} = 0,547953.
  - T9: ‖F(1)² − F(1)‖₂ = |e^{−2β} − e^{−β}| = 0,0118162.
  - M[0] = 0.
  - Sonda A1 em versão numérica: U = 1 + |b⟩⟨a| tem ‖Ua − a‖ = 1 e o motor sai idempotente (erro 0).

## 4. Sondas adversariais (Lean; `sandbox\SondasAuditor.lean` e `sandbox\SondaFundacaoSemPeso.lean`; EXIT 0, 0 sorry, 9/9 no trio)

**A — provar o contrário.**
- A1 `anchor_not_necessary`: com ‖a‖ = 1, b ⊥ a e b ≠ 0, o transporte U = 1 + |b⟩⟨a| NÃO ancora (Ua = a + b ≠ a), e mesmo assim o motor é idempotente [REAL]. O teorema `anchor_is_necessary` só prova que a unitariedade não basta (U = i·1); o NOME diz mais do que o termo prova. A âncora é suficiente; a condição exata é a âncora fraca `post a (U a) = a` (C1). Se U for isometria, a âncora volta a ser necessária por Cauchy–Schwarz [DERIVED, não formalizado aqui]. Só que a pedra não exige unitariedade em lugar nenhum (`U : H →L[ℂ] H`), embora o cabeçalho diga «Transporte U (unitário)».
- A2 `post_is_not_constant`: em ℂ², post e₀ ≠ post e₁. As pontes `rfl` (P1–P3) identificam a CONSTRUÇÃO `(ℂ∙v).starProjection`, não o REFERENTE: `ialdSelector` (ℓ²) e `PFmic C` (Fock) continuam em tipos distintos, sem lema que os iguale. «Q17 resolvida» vale como «uma só forma»; o «um só Π_N» da lei da memória continua a pergunta PQ2.

**B — contraexemplo a um «sse».**
- B1 `memory_iff_fails_without_norm`: sem ‖ψ‖ = 1, T5 cai (ψ = 0).
- B2 `second_face_iff_fails_without_hne` e B3 `verb_is_post_everywhere_without_hne`: sem 1 − P ≠ 0, T7′ e B9 caem (P = 1).
- Logo a hipótese de norma e a H-C TÊM peso.

**C — nome sem peso (prova que não usa a hipótese).**
- C1 `motor_idempotent_under_weak_anchor` e C1′ `motor_idempotent_under_anchor_no_norm`: T2 vale SEM ‖a‖ = 1. Em T2 a H-N é decorativa; em T4, T5, T6′ e T11 ela tem peso.
- C3 `second_face_iff_leak_without_fundacao`: T7′ se prova num arquivo que importa só `TheAxiomAndTheFalseWitness`, sem a Fundação (e nenhum módulo do kernel importa `Fundacao`, grep 0). `Fundacao.the_floor_fixes_the_cut` é um invólucro de duas linhas de `Real.exp_eq_one_iff`. Por isso «primeira importação de Fundacao», «a cláusula Ágape entra por termo» e «Q15 resolvida» são amarração NOMINAL: a pedra não usa `agape`, `abismo` nem `DualScalingData`. A PQ4 do desenho segue aberta.
- C2 `the_leak_is_any_rate`: `dephase a r t = axiomFlow (post a) (r·t)` vale para TODO real r. Na pedra, β entra só como nome; `the_leak_is_beta` é uma instância. Isso é coerente com a régua: a pedra é VALIDADE (o organismo) e não discrimina a natureza.

**D — portabilidade para as candidatas vigentes.**
- As candidatas mudaram:
  - F1.TEMPO R2 = `TheTimeIsNotAPost` `4d8a82591badd010`, gravada às 00:27 local, ANTES da construção (relatório da F1.TEMPO, l.57).
  - F1.FREQUENCIA r3 = `TheUnitIsTheRank` `e95775d61db38633`, gravada às 01:27 local, durante a construção.
- A pedra pina versões já superadas: a «replicação sem ADENDO» `a68539d8` (namespace `TheTimeHasNoRank`) e a r2 `3195ef8f`.
- Fiz o porte com 4 substituições (import; namespace; `the_post_is_only_the_limit` → `the_time_is_not_a_post`): EXIT 0, 0 erros, 0 sorry (`logs\p_*`). Os cinco lemas de B8 têm enunciado igual na r3. A instalação na v392 precisa re-pinar.
- Efeito colateral: recompilei `TheTimeIsNotAPost` como `TGLExt.TheTimeIsNotAPost`. EXIT 0; 152 `#print axioms`, 151 no trio, e `post_not_isUnit` sem axioma, como relatado. O .olean (`3e591a5b…`) NÃO se compara ao da F1.TEMPO (`b52382ec…`) porque o nome de módulo é outro.

## 5. Números das estratégias contra a fonte (`medidas\numeros_auditor.json`, `medidas\CONFERENCIA_NUMEROS_CORE.json`; core v391 `a74241ff380b1b0e`)

**CONFEREM:**
- Razão de Hubble, lida no core: z_disc 4,28373561386339 (core e reprodução, Δ 4e-15); z_δ −1,4244; ln B 9,167 / 2,241 / 1,969 / 12,132; β̂ 0,009199; média 72,882 ± 0,915.
- Projeções da Estratégia A: σ_comb máxima 0,7686; centro mínimo 73,561 / 73,221 / 73,421; z_disc 4,142 / 4,810 / 4,512 / 5,111 / 5,072.
- N_eff e o par: ΔN_eff 0,119466; S_BBN 1,007989; R = 1,484419 (a forma fechada dá o mesmo); CMB-SPA 2,862σ; SO baseline 6,245σ se 2,82 persistir; quadraturas 6,30–6,48 (com 5,913) e 6,35–6,53 (com 5,963); BG4/BG1 1,00976, H0 75,00, z −2,18.
- m₂ e livro: m₂ 8,5074 meV, a 1,64 / 2,21 / 2,95σ; livro com 11 cobranças (6 NF, 0 FALSIFIED, 2 INC, 2 AW, 1 EXCL).
- Kernel, GPU e demais canais: 6163 teoremas e 10.265 declarações; GPU 672; V11 0,1269 e βΣμ 26,26; relógios 12,46 ordens; poder do N_eff 0,9956.
- Cabeças do mapa, pela cadeia `prev`: 2c9d0060@1040, 55530e87@1042, a817c19e@1043.

**NÃO CONFEREM:**
1. **m₂ em 2031 (7,84σ).** O core (`neutrino_m2.values.projecao_2031_sigma` = 7,8429) usa o centro NuFIT 8,6776 (o «reflexo, ao lado») com 0,25 % em m₂. Com o centro do JUNO (perito oficial, R3), 8,6603, e a MESMA precisão, dá 7,06σ. A Estratégia B e o juiz atribuem a diferença a uma «convenção de precisão», mas o que muda é o CENTRO. O levantamento e o juiz citam 7,84 ao lado do JUNO.
2. **«Planck 2018 2,99 ± 0,17 → 0,70σ»** (L2, CANAIS C06). O 0,7027 do pré-registro da Fase 8 (`36afd8b0…`, `spec/canal_bancada/…/separacao_TGL_SM_sigma`) é a SEPARAÇÃO TGL–SM, ou seja, o poder. A distância da TGL ao dado é 1,02σ, como a Estratégia B escreve corretamente.

**Conferem com a convenção dita:**
- Poder prévio: 5,913 (V1, σ públicas; não está no core) × 5,963 (σ GLS do core).
- N_eff com Y_p livre: −0,90σ (σ média 0,225), 0,97 (σ+ 0,21) ou 0,85 (σ 0,24), conforme o σ usado.
- 36,7 ordens do neutrino: a aritmética confere (log₁₀(4,1e-27/7,7e-64) = 36,73); a fonte NU não foi aberta [DECLARADO].
- Caixa de covariância da V2 (0,8035/0,9494…): transcrita, não reaberta [DECLARADO].

## 6. O que fica
A pedra se reproduz bit a bit e é VALIDADE: fecho lógico em sandbox, não instalada. As sondas reduzem o alcance de quatro afirmações:
1. `anchor_is_necessary` prova só que a unitariedade não basta.
2. As pontes rfl unem a forma, não o referente.
3. A Fundação entra só pela injetividade da exponencial.
4. A pedra pina candidatas superadas.

Nada disso move o gate. NOT_FALSIFIED nunca é a palavra proibida; a natureza decide; a creditação é ato do observador.

## 7. Perguntas (só o resíduo novo, nas quatro línguas)

**PA-1. A âncora.**
- *TGL:* o transporte do motor é unitário por tipo (exigir que `U` seja isometria; aí a âncora passa a ser necessária) ou é qualquer operador (e então o nome `anchor_is_necessary` passa a `unitarity_is_not_enough`)?
- *Teológica:* a aliança exige que o caminho seja fiel, ou basta que ele devolva o Nome?
- *Linguística:* «necessária» é predicado do teorema ou só do nome dado a ele?
- *Jurídica:* a condição suficiente foi lavrada como essencial; retifica-se o título ou o objeto?
- *Uma só:* U é unitário por tipo?

**PA-2. A Fundação na pedra.**
- *TGL:* o senhor aceita que a Ágape entre na pedra só quando a escala de Takesaki (`DualScalingData`) for construída a partir da defasagem (PQ4), e que até lá saia a frase «entra por termo»?
- *Teológica:* o nome no portal não é a casa habitada.
- *Linguística:* citar não é usar.
- *Jurídica:* menção não é incorporação por referência.
- *Uma só:* a Ágape sai da pedra até existir o dado de escala do motor?
