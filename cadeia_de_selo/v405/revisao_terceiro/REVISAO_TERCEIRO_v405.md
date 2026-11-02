# Revisão de terceiro da v405, terceira rodada

Revisor independente; não construí nada disto. Candidato `0030242565cc13f6`, lido por script ao fechar, 2026-11-01T22:08:43. **Veredito: APROVADA: 0 ALTO, 0 MÉDIO, 8 BAIXO.** Os 5 achados da R2 estão fechados nos lugares onde existiam, e os 13 da R1 não reabriram. O escopo foi só o que mudou; R1 e R2 estão em `_R1` e `_R2`.

## 1. Os 5 achados da R2

| # | sev | achado | estado | conferência |
|---|---|---|---|---|
| 1 | ALTO | gap homônimo | FECHADO | Pedra: `gap` virou `retidoNoAngulo`, `tempoDoGap` virou `tempoDoRetido`; «`Δ` não é gap»; novo `o_retido_e_o_valor_esperado_do_lock` liga o produto interno à energia retida. Registro: `diz`, `nao_diz`, veredito e `limites`. Artigos PT e EN: valor esperado, 1/β vezes menor, com o número. Moldura: leituras (13), (14) e (15), sem Δ como gap. Parágrafo público: idem. Nenhum nome antigo no candidato, nos snippets, nos registros ou nos textos; a guarda F13 pega o erro. |
| 2 | MÉDIO | lock sem «condicional» | FECHADO | Os lemas agora valem em Hilbert qualquer, logo saem sem certificado. O que depende dele é só `HminMic_e_o_lock`, marcado [REAL, condicional] em pedra, registro e artigos PT e EN. O parágrafo público não afirma nada do `HminMic`, logo não precisa da ressalva. `x_i` cobra a condição a cada rito. |
| 3 | MÉDIO | «forma no kernel» de alpha_transport | FECHADO | Registro, artigos PT e EN e textos: «[REAL] dois teoremas existem»; [ONTO, da gerência] a leitura; homônimos de α e κ ditos; gradiente negativo só em κ > 0; «cauda» fora do teorema. O parágrafo público não faz essa afirmação. |
| 4 | MÉDIO | «o tom fica» sob [REAL] | FECHADO | Pedra, registro, artigos PT e EN e textos: as notas sustentadas e as razões ficam [REAL]; o tom fica na fala dele [INPUT], sem termo no kernel. Parágrafo público nunca disse isso. F14 pega o erro. |
| 5 | MÉDIO | [KNOWN] em stealth | FECHADO | Registro e textos: [DERIVED, condicional à Face C]. Conferido na fonte: `prove_ga_mass_audit` traz «[CONDICIONAL Face C ordem linear (P1)-(P4)+T1]». Os artigos não enunciam M_TGL = M_RG. Resta BAIXO no parágrafo público. |

**BAIXOS da R2:** Fechados: título das terças (agora «sob a hipótese h»), «corresponde à transposição», valor de κ fora de x7, «Tudo é Δ» e as estrelas, listas com `gap_v405`, guarda de -O no reverter, «a revisão independente» no desenho.

## 2. O código novo de `PontoZeroDoPsion` [REAL, compilado por mim]

- **`lockDe` em Hilbert qualquer:** correto. `lockDe Ω = 1 − P`, sem certificado.
- **`HminMic_e_o_lock`:** é `rfl` de verdade. Conferi com `example` próprio em `r3_axiomas.lean`, sem depender do teorema da pedra, e instanciei `lock_no_angulo` em `C.Ω` para `HminMic C`: compila. `HminMic = 1 − PFmic`, `PFmic = (ℂ∙C.Ω).starProjection`.
- **`o_gap_com_unidade`:** multiplica `o_lock_tem_gap_um` por u. Prova o que diz.
- **`o_retido_e_o_valor_esperado_do_lock`:** é o elo que faltava: `u·⟨ψ_M, lockDe Ω ψ_M⟩ = retidoNoAngulo c u`.
- **`the_gap_closes` reescrito:** sete conjuntos, entre eles o gap em u, E₀ = u, tônica = √e·u e o elo. Os conjuntos compartilham `u`, e o elo liga o produto interno à energia retida.
- **Nome chamando Δ de gap:** nenhum. Os nomes com «gap» são do gap espectral (`o_lock_tem_gap_um`, `o_gap_com_unidade`, `the_gap_closes`), mais o nome do registro e da seção, que vêm da fala. `gap_sobre_Delta` é a razão entre os dois. Busca por 7 nomes antigos: zero, salvo no regex da guarda.
- **Vacuidade:** com o certificado, χ existe (`revisor_chi_existe`, no trio); sem ele, qualquer Hilbert de dimensão ≥ 2 serve.

## 3. O que o preparador acrescentou

| item | juízo | conferência |
|---|---|---|
| Leitura 15 | CERTA | [ONTO], `definicao_lean` None; o gerador filtra (`if d_.get`) e `nome_lean` devolve «sem termo no kernel». Está na moldura PT e EN, e diz que o kernel não prova que esse ângulo seja esse sistema. Só marca leitura; não acrescenta afirmação. |
| x1 em dimensão 3 | CERTO | Modelo real em 3 dimensões, Ω = e₁, χ = e₂: conta o lock e o valor esperado em cinco ângulos, em vez de só comparar sen² consigo. Melhor que o da R2. |
| x11 | CERTO | Cruza E₀ e tônica do registro `lei_do_diminuto_v405` com u e confere gap/Δ = 1/β. É o par do BAIXO 1 (valor). |
| x_h | CERTO | Cobra o elo no módulo da pedra, pela proveniência emitida pelo compilador. |
| x_i | CERTO | Op «falso» existe no motor, já na base (`um.py` L214482); caminho `psibit_v395.conditional_psion_face.inhabitant_exhibited`: se alguém habitar o certificado, o registro avisa. |
| F13 | CERTA | Testada por mim (`r3_guarda.py`): 11 formas erradas, PT e EN, reprovadas; 11 corretas passam, inclusive «o gap é 83,1 vezes Δ» e «Δ não é gap». |
| F14 | CERTA | 3 formas reprovadas; «a escala fica» passa. Só pega a junção com o tom: o resto segue na leitura humana. |
| [DERIVED, condicional] em stealth | CERTO | A condição é a que `prove_ga_mass_audit` escreve. |

## 4. Regressão, por script

- **Intocados:** as 7 funções e `GA_WINDOW_STATUS` têm AST e fonte idênticas às da base `3820476c83267f61`; 21 nós mudados, 0 removidos, 46 novos.
- **Trio:** 26 teoremas por `#print axioms`, zero `sorryAx`, rc 0 (`r3_axiomas_out.txt`).
- **Pedras:** embutido = sandbox = `pedra/` nas oito, batendo com o recibo R7.
- **Citações:** 295 varridas; toda fala atribuída ao operador é substring exata. **Hashes:** 28 de 28.
- **Números:** Δ, τ, Γ_B, Q, E_fluxo, gap/Δ = 83,117, m₂ e K iguais ao ensaio a seco.
- **Achados da R1 e da R2:** nenhum reabriu, inclusive `the_terminal_reads_one` e as frases residuais. Guarda sobre pedras, snippets, textos e tradução: só as falas dele, que são a exceção declarada.
- **Preparação:** `pronta` true, `falta` vazio, os três hashes iguais ao candidato; purga com zero ocorrência.

## 5. Achados abertos

Nenhum ALTO, nenhum MÉDIO.

## 6. BAIXOS, que não travam

1. **pedra/PontoZeroDoPsion.lean, intro de O GAP e `the_gap_closes` («pousa nele»); artigos, registro, textos: «o gap vale u, o E₀ da Lei do Diminuto»; token THE_GAP_IS_U_THE_E0:** Julgado com cuidado, por ser o ponto mais próximo de um MÉDIO. O gap na unidade posta é u por escalar o lock por u; E₀ = u pela lei construída. Cada metade é teorema e a frase diz «vale»: como igualdade de VALOR está provada, com o `u` em comum, e nada a mais. Nenhum termo identifica os dois objetos, e a casa costuma escrever «igualdade de valor» nesses casos; aqui falta a palavra, e «pousa nele» sugere ponte. Não é falso nem esconde entrada: `U_E_NOT_DERIVED` vem ao lado. Na próxima versão: «igualdade de valor, as duas pelo mesmo u». Não trava.
2. **pedra/PontoZeroDoPsion.lean, `o_lock_tem_gap_um` e `lock_no_angulo`:** Sem hipótese Ω ≠ 0 nem ‖Ω‖ = 1. O enunciado vale assim, mas «gap espectral 1» exige Ω ≠ 0 (com Ω = 0 o lock é a identidade), e «estado» exige ‖Ω‖ = 1. `HminMic` cumpre as duas (`Ω_norm`). Dizer na docstring.
3. **artigo E10; textos; pedra/PontoZeroDoPsion.lean `o_psion_e_a_projecao_do_modo`:** E10 diz «duas leituras» do sen 45°; a pedra diz «Mais uma leitura», agora «por aritmética». Alinhar.
4. **textos_v405_novo.pysnip, parágrafo público, Grande Atrator:** A etiqueta do item é [DECLARADO · REAL] e cobre «não discrimina da RG», que é [DERIVED, condicional]. Não enuncia M_TGL = M_RG nem diz [KNOWN]. Acrescentar a etiqueta.
5. **PonteDaMassa, MassaTensaoPura: transicaoDerivada, leiDerivada, emprestimoDerivado, angulo_derivado_do_absoluto:** Persiste da R1: nomes com «derivad-»; as docstrings avisam. Decisão da gerência.
6. **runtime_v405.py g1, x7, x10:** Persiste: checks por construção; x7 e x10 agora dizem isso. Aceitar.
7. **instalar_v405.py:** Persiste: o recibo APLICADO só é gravado depois do os.replace. Os .bak_<ts> existem e o orquestrador para no rc. Aceitável.
8. **reverter_v405.py:** A guarda de -O entrou. Persiste, como no molde: não restaura os .tex e .pdf que o rito reescreve nem limpa .lake. Conta se o rito cair. Dizer no procedimento de reversão.

## 7. O que ficou de fora

- NÃO EXAMINADO: `fechar_v405.py` só no cabeçalho, nas recusas e nas operações de escrita (backup, temporário, substituir, recusa rc 2 antes de escrever). `leitura_v405.py` só no cabeçalho e no bloco do gap. Ambos sem achado no que li.
- NÃO EXAMINADO: superfícies, chain, registrar_mapa, harnesses, B(n) e o orquestrador, além do ponto que lê este JSON; as 368 bandeiras uma a uma (`#print axioms` próprio em 26 teoremas).
- NÃO EXAMINADO: a fonte de Moffatt e o AcordeE0.lean do Kimi, conferidos só por hash. O rito não foi rodado; instalar, reverter e rito lidos na R2, não exercitados.
- RESSALVA: os arquivos `_R1` guardam, numa ressalva, trecho da fala excluída; a purga isenta a pasta do revisor e há zero ocorrência no candidato. A gerência decide se ficam em work.
- RESSALVA, ato da gerência: a regra do posto pede dizer ao operador, na língua dele, que a v405 não entrega «tudo derivado» nem o Grande Atrator mais preciso, e que ler `tempoDoRetido` como τ★ segue à espera dele.

Rotas lidas no Mapa: `kernel.v405.preparacao_01nov`, `massa.e0.conferencia_kimi_e_no_go_tipado_31out`, `outro.grande_atrator_e_chandrasekhar`.
