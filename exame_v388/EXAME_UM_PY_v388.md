# EXAME DO um.py v388 — código e artigo (06/10/2026)

> Ordem do operador (06/10, via c1), verbatim: «vamos fazer um exame completo do um.py, desde o começo até o final, verificar inconsistências ou erros de código, verificar o texto do artigo se tudo está coerente e atualizado, inclusive o sumário, verificar se o artigo incorporou em texto todos os últimos testes e derivações, após isso concluso escreva o handoff de custodia para a sessão irmã que cuida do repositório».
> **Só leitura no Nós**: o um.py foi copiado por bytes para esta pasta e analisado na cópia; nada do Nós foi editado. Hashes lidos por script.

**Objeto:** `um.py` v388, sha16 `e64b00f4df75059b`, 33,801,035 B, 213,258 linhas. `ast.parse` OK (0.9s); pyflakes 1.7s.

## Resumo em dados

| gravidade | n |
|---|---|
| BLOQUEIA | 0 |
| CORRIGIR | 3 |
| NOTA | 186 |

**Pede nova versão (v389):** SIM — 3 achado(s) CORRIGIR; **nenhum BLOQUEIA**. O rito v388 e o selo continuam válidos; os CORRIGIR são de texto/rótulo, não de cálculo.

## Os achados CORRIGIR (a frase exata)

1. **[codigo · veredito_proibido_em_literal]** linha 8005 — evidência: «CLOCK_TORSION_CONFIRMED_ON_PHYSICAL_NET». string de SELO no core publicado (seals de um registro antigo): 'CLOCK_TORSION_CONFIRMED_ON_PHYSICAL_NET' -- a palavra proibida num rotulo emitido; e' checagem numerica na rede simulada, nao juizo da natureza, mas o rotulo diz CONFIRMED; o conferidor so guarda 'verdict'. Sugestao: renomear para ..._VERIFIED_ON_PHYSICAL_NET com errata ao lado (o nome antigo fica como registro)
2. **[artigo · versao_datada_no_titulo]** (pt)  — evidência: «Introdução: o que este código faz agora (v384) --- o kernel, os ritos e o mundo quântico na GPU». o titulo afirma 'agora' com versao anterior a v388
3. **[artigo · versao_datada_no_titulo]** (en)  — evidência: «Introduction: what this code does now (v384) --- the kernel, the rites and the quantum world on the GPU». o titulo afirma 'agora' com versao anterior a v388

## Código — o que se conferiu

- **Nomes indefinidos:** 0 (pyflakes: {"UnusedVariable": 54, "UnusedImport": 2, "RedefinedWhileUnused": 4}).
- **except nu:** 0; **except … pass:** 13 (todos limpeza ou com recusa fail-closed logo abaixo).
- **β literal como float no código:** 0. Dígitos de β em texto: {"comentario": 5, "string": 1} (um dentro de JSON de resultado embutido; comentários).
- **Palavras proibidas em literais:** 137 em guarda/negação; 11 candidatos revisados à mão → 1 CORRIGIR (rótulo de selo, um.py:8005), 10 NOTA (guardas e prova matemática).
- **Versão:** `UM_VERSION = "v388"` (linha [96]); selo `um_version` = v388; nenhuma versão futura real citada (o único «v390» é um arquivo do matplotlib).
- **Escada:** n_theorems_clean = n_theorems_expected = **6154** (= len(ext_flags)).
- **Kernel embutido (1214 arquivos):** byte-idêntico ao `Nós\tgl_kernel` (1214/1214) e ao sandbox v388 (1214/1214); contra o sandbox v376: difere só por `TGLExt.lean`, `TGL/Audit.lean` e a pedra nova (esperado). Lean embutido com `sorry`/`admit` fora de comentário: 0 arquivos.
- **Funções definidas duas vezes no mesmo escopo:** 0. **Registros vNNN atribuídos 2×:** 13 (todos try/except com o registro de falha dito).
- **Chaves do selo sem produtor literal:** 0 de 240; chaves do core sem literal: 0 de 377.
- **TODO/FIXME de código:** 0 (as 78 ocorrências são o «TODO» português e o TODO da mathlib citado). Linhas com «sorry» fora do kernel: 49 (guardas `sorryAx`).

## Artigo — o que se conferiu

- **PT:** txt `8900c4d46ddccfde` · tex `b5090ff7a79c6576` · toc `51d57238ab967499` · PDF `a7012a0da3a05950` (206 páginas).
- **EN:** txt `69fd247fc77696e3` · tex `cc8eb8a653f8ac5a` · toc `2a67168e18d6f57e` · PDF `8d670cecdea9cb5d` (210 páginas).
- **Sumário:** PT 90 entradas, EN 91; «Ao lado (v388)», «Três testes (v387)», «Ao lado (v387/v386/v385)», a Introdução e a Nota GPU listadas **uma vez cada**, em PT e EN, na ordem.
- **«pós-dição»:** PT 1 / EN 1 ocorrência(s) — todas na seção v387, como citação do operador e regra de reescrita; **0 como demérito**.
- **Front matter:** data da rodada `2026-10-06 12:21:19 4pt`; «6154» no resumo; GPU/GKLS no resumo e nas palavras-chave (W10); o resumo ainda diz «único postulado» (PT/EN, linhas 15 e 53) — NOTA: coberto pela errata ao lado da seção v385 (um.py:166491/170668); a remissão no resumo é decisão do operador.

### A lista de incorporação (n ocorrências; primeira linha do txt)

| item | PT | EN |
|---|---|---|
| livro de cobrancas v383 | 3 (l. 154) | 57 (l. 2) |
| pilar quantico v384 | 1 (l. 188) | 1 (l. 188) |
| Axioma / testemunha falsa v385 | 4 (l. 196) | 4 (l. 196) |
| [POSTO] (posto, nao postulado) | 35 (l. 71) | 14 (l. 71) |
| Verbo v386 (o Verbo seleciona) | 3 (l. 172) | 3 (l. 172) |
| ramo B reaberto | 12 (l. 123) | 10 (l. 123) |
| V1 do ramo B por hash | 1 (l. 896) | 1 (l. 902) |
| tres testes conjuntos | 5 (l. 17) | 4 (l. 17) |
| duas probabilidades | 8 (l. 151) | 8 (l. 151) |
| retrodicao sem ajuste / novidade de uso | 6 (l. 2) | 6 (l. 2) |
| Mercurio | 4 (l. 2) | 4 (l. 2) |
| Fase 8: N_eff 0,1195 | 1 (l. 170) | 1 (l. 170) |
| Fase 8: veredito/poder dito | 1 (l. 170) | 1 (l. 170) |
| Fase 9: ln B 9,17 | 1 (l. 63) | 1 (l. 63) |
| Fase 9: z_disc 4,28 | 1 (l. 63) | 1 (l. 63) |
| Fase 9: INCONCLUSIVE | 2 (l. 63) | 2 (l. 63) |
| Fase 9: contrafactual | 3 (l. 63) | 5 (l. 63) |
| beta escalar limitado inferiormente | 4 (l. 57) | 5 (l. 57) |
| beta_0 (constante da fronteira) | 1 (l. 61) | 1 (l. 61) |
| Teorema da Escala | 2 (l. 61) | 2 (l. 61) |
| Zenao (nome) | 8 (l. 2) | 8 (l. 2) |
| soma das metades (a operacao de Zenao) | 1 (l. 61) | 1 (l. 61) |
| Meia-Nat ponto fixo | 1 (l. 61) | 1 (l. 61) |
| errata alpha observa-se nao se deriva | 2 (l. 17) | 2 (l. 17) |

Números conferidos entre seções (mesma grandeza): Fase 9 — ln B 9,17, z_disc 4,28, z_δ −1,42, previsão 74,274 (seção v388) e 74,27 (seção v387: previsão antes da abertura) — coerentes; o «poder 5,91σ» da v387 é o poder PRÉVIO só com σ, não o z_disc medido (grandezas distintas, ditas). Fase 8 — ΔN_eff 0,1195 (seção v387) e 0,119 (tabela dos três testes, arredondado) — coerentes. Fase 4 — ln B 8,02 (tabela e seção) — coerente.

## NOTAs (resumo por categoria)

- `artigo:contagem_de_pedras_parte_C`: 1 — a frase conta o LEDGER citavel, nao todos os arquivos; dizer o recorte ou ampliar o ledger e' decisao do operador
- `artigo:front_matter_postulado_vs_POSTO`: 4 — COBERTO pela errata ao lado da secao v385 (um.py:166491 PT / 170668 EN: 'onde este artigo diz um unico postulado... leia-se posto; a etiqueta passa a ser [POSTO]') -- a regra da casa e' corrigir AO LADO, nunca por cima; resta ao operador decidir se o resumo ganha uma remissao para a errata (precedente de 30/08 no C:\IALD\CLAUDE.md: 'corrigir ao lado nao basta se o lado escolhido nao e o lado que se le')
- `artigo:secao_v387_superada_pela_v388`: 2 — secao datada (v387); a v388 (acima) registra a abertura; sem remissao cruzada
- `codigo:TODO_FIXME`: 78 — falso positivo: 'TODO' portugues ('O TODO E UM', 'TODOS') e o TODO da mathlib citado no texto -- nenhum TODO de codigo
- `codigo:beta_digitos_em_string`: 1 — texto/citacao/guarda; nao e' motor (o motor e' ALPHA*SQRT_E)
- `codigo:escada_ext_flags`: 1 — a escada bate (6154/6154); ha 37 bandeiras ext_* True fora da lista da escada (contadas por outros registros) -- dito
- `codigo:except_silencioso_pass`: 13 — except ... pass: todos de limpeza (fechar log, remover temporario, matar processo, reconfigurar stderr, gravar sidecar) ou com a recusa fail-closed logo abaixo (acquire_evidence -> _refuse se ausente)
- `codigo:kernel_vs_sandbox_v376`: 1 — o sandbox v376 (scratchpad da sessao 6da8f00d) foi reaproveitado ate a v387; difere da v388 exatamente pelas 2 costuras (TGLExt.lean, Audit.lean) e pela pedra nova -- esperado
- `codigo:pyflakes:RedefinedWhileUnused`: 4 — _tx7/_tx8 redefinidos entre trechos do artigo (o trecho v388 define _tx8 com def; o trecho mais antigo redefine com lambda); cada definicao e' usada antes da seguinte -- o artigo saiu certo (conferidor), mas o sombreamento e' fragil
- `codigo:pyflakes:UnusedImport`: 2 — import local nao usado (estilo)
- `codigo:pyflakes:UnusedVariable`: 54 — variavel local nao usada (estilo; sem efeito no rito)
- `codigo:registro_vNNN_duplicado`: 13 — pode ser try/except (fallback) -- ver as linhas
- `codigo:veredito_proibido_em_literal`: 10 — docstring de guarda: 'jamais CONFIRMED' (falso positivo do detector de contexto)
- `codigo:versao_futura_citada`: 2 — versao > v388 citada (plano/rota?)

## Fontes (sha16)

- `EXAME_CODIGO_v388.json` `1b5949cbdba95716`
- `EXAME_ARTIGO_v388.json` `4bc07e5db3399e46`
- `exame_codigo_v388.py` `4a682b71b7269361`
- `exame_artigo_v388.py` `3236aec70b2566d2`
- `consolidar_exame_v388.py` `ef3572ae458e1897`

*Estatuto:* exame estático [REAL — medido na cópia por bytes]; nenhuma afirmação sobre a natureza. NOT_FALSIFIED nunca é confirmação; o gate não se move.
