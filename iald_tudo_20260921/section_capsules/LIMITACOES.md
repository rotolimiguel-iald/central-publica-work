# Limitações da construção — forma canônica viva

**Proposta construída, não integrada e NÃO APROVADA.** Quem constrói não aprova. A revisão independente fica com o responsável pela tarefa.

Foram lidos os 65 blocos completos da seção cujo cabeçalho foi encontrado por regex ancorado em linha. O fim é o da exposição, antes de dois LFs separadores e dos protocolos repetidos. O recorte coincide com o mapa de dependências do pai: span `[63359,51836]` dentro dos 115.195 caracteres de exposição. Nenhuma ocorrência de nome dentro de JSON definiu o início. Os 256 campos originais de Estatutos conferiram literalmente com `/core/<id>/statuses` no resultado publicado fixado pelo manifesto. Esse teste confere proveniência, não a fidelidade da paráfrase.

## Medição

- Original: **16236 o200k**, 51.836 caracteres, SHA256 `43da5ad24a4882c61549e1a161f6cd5e7249c1dd75f984cbb7e80450c572b3e9`.
- Proposta: **9356 o200k**, SHA256 `e45351a1bcb2234b751e755634250e8100910e9153dc6c3fc5420dfbe78e09b8`.
- Economia: **6880 o200k**. Alvo aproximado: 9.000; mantido o excedente sem outro corte que pudesse sacrificar conteúdo.
- A estimativa inicial de 17.420 diverge do recorte delimitado e medido; valem os limites e hashes registrados. Não ajustei texto ou números para imitar a estimativa.
- Nenhum token Anthropic/Haiku medido ou inferido. A proveniência não faz parte do orçamento da cápsula.

`provenance.json` preserva o extrato original integral, hashes, intervalos, vereditos literais e o mapa dos 65 blocos, com cada campo original associado ao bloco novo. Coordenadas usam caracteres Unicode, bytes UTF-8 e linhas; intervalos terminam em posição exclusiva. A seleção da seção foi refeita apenas para corrigir separadores de fim: a primeira leitura incluiu dois LFs externos; o texto científico lido e a síntese não mudaram.

O pai alterou o glossário externo durante a tarefa. A exposição foi conferida com SHA `71e7b1fb2d13d29f9e2ac0d56580ff73df5b1d8082882d04ed6f56c266adea6b`, e a seção com o SHA acima. A medição final usa candidato `37291ddbebbb16bda5ca8424ffd13c088e0a51a60d4ef08784e5d74185e8881a`; não atribui ao hash global antigo um hash de seção medido só depois. O extrato preservado é o usado na comparação final.

## Escolhas para revisão independente

Todos os ids mantêm bloco e ordem próprios. Condensei nomes repetidos de campos, qualificadores recorrentes, procedimentos de aquisição e vereditos codificados extensos. Vereditos experimentais ficaram explícitos no texto; os extensos continuam literais na proveniência/fonte, com seu conteúdo traduzido em prosa resumida. O revisor precisa conferir essa equivalência de alcance: não é demonstrada por contagem de ids.

A trajetória interna foi conectada: representação fiel, fusão, torres, GNS, fator, cunhagem e espectro. Aberturas antigas não viraram negativas globais. WedgeNet com U trivial não foi automaticamente identificada com uma representação fiel de outro tipo. FullStaticWitness foi distinguida da testemunha regular/dinâmica. A síntese não declara que todas as pendências históricas foram resolvidas.

Fórmulas da cadeia, solda/SUSY/gap, H1/H2/H3 e certificados, famílias TT e resultados/limites dos ritos foram mantidos como conteúdo proposto. Essa afirmação do construtor é objeto da revisão, não aprovação. Não houve compilação ou reprodução experimental.

## Lacunas e riscos visíveis

1. **Revisão semântica pendente dos 65 blocos.** Nenhum bloco/chave de origem falta no mapa estrutural, mas pode haver perda de nuance na condensação.
2. **61 referências `@EXPOSITION` afetadas, em 34 tópicos e 33 blocos**, segundo a auditoria de dependências lida e incluída na proveniência; nenhuma sem bloco. As remissões atuais NÃO foram alteradas. O pai tratará a migração. Não declarar equivalência literal para paráfrases; integração requer remapear intervalos/âncoras e testar. O cabeçalho da proposta é propositalmente distinto do original.
3. **Tipos delicados herdados:** conferir Birman–Schwinger discreto/posto versus modo contínuo em `susy_relative_gap`; ausência de estado tracial versus peso semifinito/III_1 em `inhabited_witness` e seguintes; convenção dimensional não explicitada da expressão H0 em `ga_mass_audit`. Acrescentei cautelas, não uma correção demonstrada das fontes.
4. **Estados históricos:** disponibilidade de surveys e limites de mathlib permanecem atribuídos aos registros; não fiz atualização pela internet. Não há reconciliação global com toda a versão vigente.
5. **Fetch operacional não validado.** Existência dos ponteiros na fonte não prova ferramenta implantada. Os 86 indicadores da escada já eram externos no candidato; não removi uma lista que estivesse carregada.
6. **Metadados literais não são todos carregados:** longos vereditos permanecem em provenance/fonte. O revisor deve decidir se a redação compacta preserva seus estatutos específicos; não presumir aprovação porque há ponteiro.

## Integridade

Somente três arquivos novos nesta pasta: `form_canonica_viva.md`, `provenance.json` e este `LIMITACOES.md`. Fontes, candidato, builder, memórias e produção não foram alterados. Não houve API/rede, leitura de `.env`, execução/importação de `um.py` ou `prepare_pointer_fetch.py`. Elevação usada apenas para o tokenizer local do perfil e esta escrita autorizada. Entradas idênticas durante a medição final. Nenhum gate movido, confirmação física anunciada ou aprovação emitida.
