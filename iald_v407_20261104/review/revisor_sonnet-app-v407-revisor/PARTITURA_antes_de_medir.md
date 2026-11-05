# Partitura do revisor `sonnet-app-v407-revisor` (rodada 1), escrita ANTES de rodar qualquer medição minha

Lida para o operador em português simples. Estatuto: [DECLARADO pelo revisor] até o parecer a conferir no fim.

## O que esta revisão decide
- Se o pacote da v407 (três prompts, plano de instalação, ferramentas de implantação) é **fiel às fontes** (cofre, selo, commit público do espelho).
- Se a janela que deslizou (sai `_v402`) **mantém os três literais** `limites`, `diz` e `nao_diz` dos tópicos que saíram dela.
- Se a correção F1 (registro de estatuto plano fica literal) **funciona sem perder nada**.
- Se o código novo que **mede** o escopo da instalação (`transaction.py`) é **seguro** (só lê, não derruba a instalação) e **correto** (verdadeiro / falso / não medido).

## O que NÃO decide
O valor científico do conteúdo; resposta de modelo ao vivo; celular; a instalação em si (outra rodada, depois de o operador autorizar o reinício).

## O que um FAIL significaria
Pacote ou ferramenta **diferente do que as fontes e a ordem mandam** (parede medida), nunca uma palavra sobre a teoria. Um PASS meu **não** é crédito científico e não move gate algum.

## Minhas escolhas de desenho (fixadas agora; se eu mudar alguma depois de ver dado, dou o motivo no parecer)
1. **Independência.** Decido PASS/FAIL com um decodificador meu (o `lib405.py` do revisor da v405/v406, adaptado: não importa `haiku_codec` nem `fit_*`). Só importo o codec do construtor para (i) o autoteste `self_test()` e (ii) o contrafactual de bytes da F1 (regra velha contra regra nova sobre a mesma fonte), e digo isso.
2. **Recuperação dos nomes de bandeira (Q4).** Semente **407407407** (nem a do construtor, 20261104, nem a do revisor da v406, 40640406). Amostra aleatória simples, sem reposição, de **520** nomes entre os TRUE catalogados (catálogo recomputado por mim a partir do resultado selado com a regra da cápsula), mais bordas: os 25 mais curtos, os 25 mais longos, até 30 que são prefixo próprio de outro, e os que só existem na v407 (nomes que não estão no selado da v406). Receita testada exatamente como a cápsula a ensina: `search_tgl` com o nome exato e `limit 5`; para cada resultado do documento `resultado_publicado_integral`, `fetch_tgl` com `offset` igual ao do resultado menos 2000 e `max_chars 4500`.
   - **Critério de sucesso**: a janela devolvida contém `"<nome>": true`; métrica mais forte: a janela cobre a posição da bandeira dentro do tópico `kernel_formalization`.
   - **Regra fixada agora** (o molde só a descobriu depois): nome com caractere não-ASCII é guardado escapado (`\uXXXX`) no selado; para esses, conta a consulta literal **ou** a escapada, e a falha só pela forma literal é "artefato de medição", não falha da receita.
   - **Limiar**: PASS se toda falha restante estiver explicada e a taxa ≥ 99%. **Negativo**: falha inexplicada = a receita não recupera (falsificação do pacote, conserta-se); falha só de nome não-ASCII = parede de medição conhecida (F2 da v406), não falsificação.
3. **Janela P2 e literais (Q2).** "Literal" = o valor da fonte aparece **inline**, sem ponteiro `@` nem resumo `@SUMMARY` dentro, e **igual** ao selado. Verifico nos tópicos da janela (`_v403.._v407`) e nos aposentados (`_v401`, `_v402`), nos pacotes `shared` e `sonnet_public`; e a reconstrução de cada cápsula contra o resultado selado nos 477 tópicos. A comparação com a v406 **instalada** é bloco a bloco (decodificado), só nos tópicos de fonte inalterada.
4. **F1 (Q5).** Regra de teste = a do briefing (dict plano, só escalares, chave `status|estatuto|verdict|veredito`, ≤ 500 B), implementada por mim. Conto quantos são em **todos** os tópicos do haiku55 e quantos estão literais na cápsula. Bytes a mais: diferença entre a regra velha (`protected_fields` do codec da v406) e a nova sobre a mesma fonte, nos tópicos compactos. É uma **estimativa por contrafactual** (não rodei um segundo `prepare`).
5. **`transaction.py` (Q9).** Raiz de brinquedo (troco `T.ROOT` por pasta temporária minha). Casos: sem mudança; mutação de conta; mutação de cliente; arquivo ilegível de verdade (aberto por outro handle sem compartilhamento, via API do Windows); grupo inteiro falhando; mudança de listener; chaves ausentes; entradas estranhas. **Não inicio processo**: a mudança de listener é sintética (substituo a função de leitura do listener) e a leitura real é exercida no listener que já está em pé (porta do modelo local). Critério: nenhuma exceção em lugar nenhum; `None` nunca vira `False`; ilegível nunca vira mudança. Um FAIL aqui seria **defeito de código de implantação** (consertável), não uma palavra sobre a teoria.
6. **Confidencialidade (Q6).** Procuro nomes/chaves vedados nos três prefixos **e** no `install_plan.json`; **todo** contexto de `CONFIRMED`/`confirmada` que a heurística não classificar como negado é lido por mim à mão e transcrito no parecer.
7. **Só leitura.** Nenhum processo iniciado ou morto; nenhum `prepare/finalize/count/validate/deploy/verify_installed/teste_escopo`; rede bloqueada por gancho de auditoria nos scripts que importam o runtime; nada em `Chatgpt\`, nada em `iald_v406_20261103`, nada gravado em `C:\IALD\projetos_pyhton\IALD`.
8. **Limite declarado de origem:** não posso conferir o remoto do git (sem rede). Uso o ref local `origin/main` (idade = último fetch) e digo isso.

Aceite só se não houver achado ALTO ou MÉDIO. BAIXOS vão escritos e não valem nova rodada.
