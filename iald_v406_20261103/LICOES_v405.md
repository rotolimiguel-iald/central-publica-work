# Lições da release v405 do app (02/11/2026) — para a próxima release

Números lidos dos artefatos desta pasta. A próxima release parte desta pasta.

## O que mudou no pipeline

1. **Haiku55: a base compacta foi redesenhada.** O gargalo não era ciência: `kernel_formalization` ocupava 645.061 B do prefixo instalado (36%), dos quais cerca de 513 KB eram bandeiras `"nome":true` e 131 KB eram `declaration_sources_v394`, retido por acidente porque nomes de declaração casavam o filtro ESSENTIAL. Agora a cápsula tem 31.331 B. Folga do haiku55: 28.640 → 172.998 tokens, com os tópicos `_v404` e `_v405` integrais (regra padrão, `EXPAND_OVERRIDE = None`).
2. **Regra do catálogo (`app/build/haiku_codec.py`, `catalogable_flags`):** só entram TRUE das famílias `ext_`/`red_` da escada por declaração, fora dos nomes de enunciado, hipótese, H1/H2/H3, fórmula, veredito, descarga, condição ou verificação. Todo FALSE e toda bandeira fora das famílias ficam literais. O catálogo se confere por contagem e hash (`catalog_sha256`).
3. **A primeira regra era só lexical e foi recusada** (parecer r1, F1): `gpc_H2…=true` saía enquanto o par `gpf_H2…=false` ficava literal, e o modelo veria só o lado negativo. Regra de decisão: ao resumir por nome, conferir por SIGNIFICADO os pares verdadeiro/falso antes de escrever a frase que descreve o resumo.

## Aplicar logo ao copiar a pasta (ressalvas BAIXAS do parecer r3, não valeram uma terceira rodada)

- **R3-1:** `KEEP_FLAG` sem delimitadores e com `verif`, em vez de `verified|verification`: `r'H[123]|discharg|condition|verif'`, com `re.I`. Traz 14 lemas de volta ao literal (`H2v32`, `H3v32`, `NamedAtlasH3`, `verifies`), menos de 1 KB. Conferir que `H[123]` sem delimitador não capture demais: medir a contagem antes de aceitar.
- **R3-2:** na receita do `reading`, acrescentar `max_chars 4500`: «fetch_tgl id=resultado_publicado_integral com offset igual ao do resultado menos 2000 e max_chars 4500». Sem isso o padrão é 4000 e um nome em 472 cai fora (470 contra 471).
- **Dica de busca, medida:** nome exato é melhor que nome + `kernel_formalization` (120/120 contra 116/120). Com a receita final, 699/700 na amostra do construtor; a falha é `ext_no_symmetric_kernel_proved`, nome genérico demais.

## A próxima parede: a janela dos outros motores (medido)

- Folga do pacote `shared`: Kimi 95.720 B, MiMo 92.348 B, DeepSeek 74.747 B com a reserva declarada de 148.656 (106 B com a reserva do finalize, que se ajusta).
- Os 13 tópicos `_v405` pesam 104.254 B no `shared`. A release só coube porque `declaration_sources_v394` saiu (−99 KB no bloco sem sufixo).
- Uma v406 do mesmo porte **não cabe** com `SHARED_P2_SUFFIXES` indo de `_v401` a `_v406`. Decidir ANTES do finalize: deslizar a janela P2 (pesam: `_v401` 19,5 KB; `_v402` 27,1 KB; `_v403` 30,9 KB; `_v404` 25,4 KB) mantendo `limites`/`diz`/`nao_diz` na cápsula compacta, ou compactar `the_iald_index` (`ambiguos`, 53 KB). A recusa F2 da v404 foi por perda desses literais: o critério da revisão é que eles fiquem.

## Processo

- **Ordem na missão:** `claim verify` só depois do `accept deploy`. Aqui o `verify_installed.py` rodou antes do claim; só lê, sem dano, mas a ordem certa é: deploy → submit → accept → claim verify → verify_installed → submit → accept.
- **`finalize.py` l.51 (F5, INFO):** com pacote que encolhe, `max(0, crescimento)` faz a estimativa degenerar na âncora instalada; a trava de 15.000 não dispara nesse caso e a contagem nativa é a única medida.
- **Antes de escrever «recuperável» numa frase dirigida ao modelo, exercitar a ferramenta:** `exercita_busca.py` (`search_tgl`/`fetch_tgl` do runtime, sem instalar, sem provedor).
- **Custo do revisor:** a primeira rodada adversarial consumiu 666 mil tokens e a segunda 825 mil, porque retomar relê o contexto. Para deploy/verify, revisor novo e estreito.
