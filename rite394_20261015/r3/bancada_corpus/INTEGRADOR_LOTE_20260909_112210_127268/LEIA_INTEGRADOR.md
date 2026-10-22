# Integração mecânica em cópia — seis módulos, 09/09/2026

O integrador lê um.py como bytes e AST; nunca importa nem executa seu código. A cópia gerada é um artefato estático de trabalho, não uma rodada selada do programa.

## Transformação autorizada

Somente a atribuição _EMBEDDED_KERNEL_FILES recebe alteração: seis textos Lean novos, seis imports adicionais em TGLExt.lean e 100 comandos #print axioms adicionais em TGL/Audit.lean. Flags Python, gate, sentinelas e restante do código são preservados. Os namespaces e enunciados são mantidos; apenas imports locais entre módulos novos ganham TGLExt.

A configuração registra hashes lidos dos módulos aprovados, de seus BUILD_RESULT e do um.py de origem. Qualquer alteração desses dados faz o integrador recusar a geração.

A geração exige confirmação do snapshot pelo root. CONFIG_SNAPSHOT_APROVADO.json registra essa confirmação, incluindo a autorização condicional satisfeita do módulo de cone-volume.

## Reproduzir a geração e os checks

1. Executar integrate_approved_copy.py com o caminho da CONFIG_SNAPSHOT_APROVADO.json. O script cria uma pasta COPIA_INTEGRADA nova; não sobrepõe a cópia já existente.
2. Executar build_transposed.py prepare com a nova pasta COPIA_INTEGRADA. O script extrai por AST as fontes efetivamente embutidas, prepara fontes/agregadores e emite BUILD_PLAN.json com comandos e ambiente exatos.
3. Executar build_transposed.py run com esse BUILD_PLAN.json. O script chama Lean diretamente: seis módulos, TGLExt.lean copiado, TGL/Audit.lean copiado e auditoria dedicada das 100 declarações de teorema adicionadas. Nem o um.py de origem nem a cópia são executados.

Os módulos novos são compilados contra cópias binárias das dependências TGLExt/TGL alcançáveis e binários existentes da Mathlib. Um diretório TGLExt local sombreia outros diretórios desse namespace no LEAN_PATH; por isso o preparador faz cópias de bytes, sem junctions ou hardlinks. Os módulos canônicos não são reconstruídos.

## Limites e artefatos

INTEGRATION_RESULT.json registra comparação de AST fora da tabela, bytes do restante, fontes antigas preservadas, hashes e extração inversa das seis novas strings. A presença dos teoremas na auditoria não cria novas flags JSON individuais; isso é uma opção explícita desta integração mecânica.

A auditoria completa exige retorno zero, presença de seus nomes de axiomas esperados e sentinelas, e axiomas contidos no trio. As saídas canônicas adicionais são preservadas no log. Os módulos novos e sua auditoria dedicada exigem também ausência de mensagens extras.

Todo build/erro anterior permanece em pasta própria. Para repetir após falha, preparar uma build nova. Os scripts alterados têm backups binários imediatos na mesma pasta. Fontes e binários de entrada são conferidos antes/depois; dependências transitivas da Mathlib não são integralmente reauditas nesta bancada.

Esta entrega não atesta runtime, selftest completo, emissão de artigo, selo, gate executado ou confirmação física. Tampouco autoriza rodar a cópia futuramente sem conferir seus caminhos de saída, dependências e o escopo de escrita da rodada.
