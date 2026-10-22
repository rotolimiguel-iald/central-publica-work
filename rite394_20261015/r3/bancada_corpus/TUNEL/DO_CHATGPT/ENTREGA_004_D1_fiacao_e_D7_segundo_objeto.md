[REAL — leitura e controles sintéticos] D1 mapeada; [DERIVED] no-go de D7 para fotometria sob dephasing puro; [OPEN] ponte para um observável de coerência e decisão do operador.

# ENTREGA 004 — D1 e D7

05/09/2026 · bancada ChatGPT → gerência Claude · responde à ORDEM 004.

O parecer completo é `D1_D7_PARECER.md`. Nenhuma proposta foi aplicada ao programa e nenhum pré-registro experimental foi adotado.

## Critérios de aceitação

| Critério | Estatuto | Evidência e limite |
|---|---|---|
| D1.1 Censo de consumidores | PAGO para nomes/chaves explícitos; NÃO PAGO como prova irrestrita de fluxo dinâmico | 60 linhas no censo, classificadas com função e papel; serializações integrais de contêineres propagam resultados sem citar chaves. |
| D1.2 Consequências de sai/fica | PAGO [REAL/DERIVED] | Três expressões decisórias extraídas por AST, 16 combinações sintéticas verificadas. O gate QG não lê janela/identidade; argumentos e chamada única documentados. Mantidos seus inputs, seu veredito não muda. Hashes e campos de identidade no selo podem mudar. |
| D1.3 Melhor argumento bilateral | PAGO | Preservação do requisito convencional legado versus separação entre sombra aposentada e fechamento interno; não se confunde teste de consistência com falsificador empírico. |
| D1.4 Proposta ao nível de diff | PAGO, NÃO APLICADA | Três diffs extraídos; ajustes de docstring, reading, MODEL_AXIOMS, contorno e emissores PT/EN especificados no parecer. Não foi produzido um patch editorial completo e aplicável do arquivo inteiro. |
| D1.5 Decisão binária | PAGO | Pergunta ao operador no fim da seção D1; não respondida em seu nome. |
| D7.1 Derivação e quatro candidatos | PAGO [DERIVED sob hipóteses] | Duas bandas, drift, espectro e Etherington examinados; dephasing de coerência não é perda de fluxo. |
| D7.2 Forma/magnitude/pré-registro se existir | PAGO como possibilidade CONDICIONAL de visibilidade; NÃO PAGO como nova D_L derivada | V/V₀=exp[−βτ★(Δω)²T/2]; hipótese cosmológica adicional escrita; cálculo ilustrativo e rascunho não executável, dependente de desenho instrumental. |
| D7.3 No-go da classe | PAGO [DERIVED] | Motor atual é fator constante para z>0; dephasing puro preserva todo observável diagonal. Não é no-go de todas as extensões possíveis da TGL. |
| D7.4 Controles exatos | PAGO [REAL] | Frações racionais: populações preservadas, probabilidade interferométrica 3/4 e retenção 1/16 ao dobrar o gap. |
| D7.5 Decisão do operador | PAGO | Autorizar ou não desenvolvimento/pré-registro de coerência e escolher sistema/dado alvo. |

## Reprodução

O script `audit_d1_d7.py` analisa AST; não importa nem executa `um.py`. Para refazer sem alterar os artefatos desta entrega, copie o script e o snapshot para uma **nova subpasta de Chatgpt** e execute `C:/Python314/python.exe -B audit_d1_d7.py` nela. Ele recusa sobrescrever saídas. A prova de expressão é sintética, não execução do rito com dados.

## Axiomas e limites

Esta entrega não acrescenta Lean, logo contagem de teoremas Lean novos = 0 e não há `#print axioms` novo. As demonstrações escritas têm hipóteses numeradas. O cálculo não mede dephasing real nem decide física. Não foi aberto conjunto observacional novo; a leitura autorizada do fonte incluiu constantes preexistentes, que não foram usadas em um teste observacional. A pesquisa externa foi teórica, com fontes no parecer.

Tentativa falha preservada: `audit_d1_d7.py.bak_*` contém a primeira versão, que falhou com `NameError: _v3_keys` na avaliação de um gerador por escopo de `eval`. A versão atual fornece o ambiente sintético também aos globais e passou. A falha é registrada aqui; não foi inventado log de uma saída que não havia sido gravada.

## Arquivos e SHA256 lidos agora

- `C:\IALD\Central de Patentes\Chatgpt\D1_D7_PARECER.md` — `B34DBA1250111EFC2EDECB2F8A23D36BEF80C2F487784FCDC8417AFE95A64C7D`.
- `C:\IALD\Central de Patentes\Chatgpt\D1_CENSO_CONSUMIDORES.md` — `89A278B83B0F87A605AE14CB6289B41D0F88BCD15B31D5C252DA9850166DBDB3`.
- `C:\IALD\Central de Patentes\Chatgpt\D1_D7_CONTROLES.json` — `F9B809B3D1E10F303C0E2281C2EC12B4B6F41D90C34B9EA60814CCF903A4A262`.
- `C:\IALD\Central de Patentes\Chatgpt\D1_PROPOSTA_DIFF.md` — `6987F7C9F6073CC7F47FA9C631FFB46BDE4508EABE92703E864833F44AA6237B`.
- `C:\IALD\Central de Patentes\Chatgpt\audit_d1_d7.py` — `E7765C0C24085DD99E5B3996EDD8D9F1AA2CB836F043DC341A88FB388DEA7F82`.
- `C:\IALD\Central de Patentes\Chatgpt\um_ordens003_004_snapshot.py` — `09D6BEC30171A9C1F522CADB0BD7189545CF03F1B8297A3A0DEB39A21922D140`.
- `C:\IALD\Central de Patentes\Chatgpt\publish_order004.py` — `97BE1153D44D586A3327ECCEAB8B604443F46AF93DCA16E67838E3E1DF23C69A`.

## Perguntas reservadas ao operador

D1: autoriza retirar a janela das três condições decisórias, mantendo-a integralmente no contorno — sim ou não?

D7: autoriza desenvolver um teste de coerência para pré-registro — sim ou não; se sim, qual sistema/dado alvo deseja reservar?
