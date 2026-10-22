# Capturas atuais e manifesto selado: correspondência medida

09/09/2026. Inspeção própria somente leitura. Nenhum `um.py` foi executado/importado, nenhuma compilação foi iniciada e nenhum original foi modificado.

**[REAL — medição] A captura atual da auditoria reproduz o hash do manifesto. A captura atual do build não reproduz seu hash.** Essa diferença é uma incompatibilidade de correspondência entre artefatos históricos; não demonstra falha de compilação ou falsidade de uma prova.

## Origem e procedimento exato

No `um.py` canônico, as linhas 118960 e 118962 calculam SHA-256 de `build["stdout"].encode("utf-8")` e `audit["stdout"].encode("utf-8")`. As linhas 118967–118974 escrevem um arquivo com cabeçalho, marcador STDOUT, payload, marcador STDERR e outro payload. Portanto o hash do arquivo completo não deve ser comparado ao hash de STDOUT.

Esta inspeção:

1. Leu os bytes de cada captura, sem regravá-los.
2. Decodificou UTF-8 e substituiu cada CRLF por LF uma vez, para remover a tradução de fim de linha da escrita textual em Windows.
3. Tomou os caracteres depois de `--- STDOUT ---` seguido de LF e antes do último LF seguido de `--- STDERR ---` e LF. Esse LF anterior ao marcador é acrescentado pelo escritor; não pertence ao payload. Nenhum `strip`, `trim` ou remoção de espaços foi aplicado.
4. Codificou exatamente essa substring em UTF-8 e calculou SHA-256. Conferiu também os comprimentos declarados no cabeçalho e os códigos de saída registrados.

O script `inspect_captures.py` preserva a implementação completa desse procedimento. O JSON acompanha os hashes dos arquivos inteiros para custódia, além dos hashes dos payloads.

| Comparação | Build | Auditoria |
|---|---|---|
| SHA-256 medido do STDOUT | `175e31e56dc4a7ba10725ef5fb0ade18c01cdf4a592171a8838e6e6c3f29ef02` | `832191e1ad38852df4c4124ffe940368e0869494e03e209cea16c2ce70c301dc` |
| SHA-256 esperado pelo manifesto | `d122af385b118f8d8945b504846aacf62e9674b2d7fecfd0ca592dfd42f33ce9` | `832191e1ad38852df4c4124ffe940368e0869494e03e209cea16c2ce70c301dc` |
| Correspondência | False | True |
| Caracteres medidos / declarados | 1401585 / 1401585 | 594281 / 594281 |
| Código de saída na captura | 0 | 0 |
| Linhas `warning:` / `error:` | 178 / 0 | 0 / 0 |

## O que continua correspondendo ao selo

O programa canônico mede 9860115 bytes e SHA-256 `e2f9a889c2dcf6f444b8fa3f91d28eb70c9a6d9aed06644abcef7e58a6267303`. O pin de `um.py` no selo confere. O manifesto mede 703039 bytes e SHA-256 `acb48b230f130720888cea7120f33cb5ee3edf8a267f7654edeb3694e6634a9d`; seu pin no selo também confere. Ambos mantêm a referência à rodada v337, com timestamp declarado `2026-09-09 14:09:22`.

O manifesto informa `lake_build_ok=True`, ausência de `sorryAx`, `trustCompiler` e axiomas TGL próprios. Foram lidas 4931 entradas de axiomas, das quais 0 têm axiomas fora de propext, Classical.choice e Quot.sound. Isso é leitura e comparação do recibo existente, não uma nova compilação independente.

## Por que a captura pode ser posterior ao manifesto

[REAL — fonte lida] `_unified_main` chama `main()` e depois `selftest_fail_closed` (`um.py`:162167–162169). O autoteste chama o mesmo verificador duas vezes, nas linhas 113921 e 113928; esse verificador regrava os mesmos nomes de captura nas linhas 118967–118974. O stdout da rodada registra o autoteste final aprovado. As capturas atuais têm mtime posterior ao timestamp do manifesto.

[DERIVED — explicação compatível com a estrutura observada] A regravação após o `main` explica que a captura do build presente não seja o payload selado anteriormente. Não foi reconstruído o payload ausente nem atribuída a ele a captura atual. A auditoria permanecer igual é compatível com a repetição dos mesmos enunciados; não prova igualdade dos logs de build.

## Consequência para o reexame

O programa e seu manifesto seguem ligados por pins conferidos. O build atual registra sucesso e warnings; a auditoria atual registra sucesso sem warnings e corresponde ao hash selado. A afirmação estrita que não se pode fazer é: **“o arquivo atual `tgl_kernel_build_capture.txt` reproduz o STDOUT de build hashado nesse manifesto.”** A inspeção não revoga os resultados matemáticos nem inventa uma recompilação faltante.

Todos os seis arquivos de entrada foram medidos antes e depois, sem alteração durante esta inspeção. Nenhum dado foi refeito e nenhum gate foi movido.
