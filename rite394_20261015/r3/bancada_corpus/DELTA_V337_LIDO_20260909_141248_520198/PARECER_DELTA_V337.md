# Delta científico e estrutural do programa vivo v337

[REAL — leitura por AST/literais e verificação de recibos existentes] O programa vivo diverge do snapshot v336. A cópia28 continua corretamente vinculada ao seu snapshot auditado; não se deve afirmar que o cânone vivo ainda tem os mesmos bytes.

## Alterações medidas

A tabela passa de 605 a 606 entradas, com uma única fonte nova: TGLExt/TheNameIsTheCharacterization.lean. As fontes antigas alteradas são somente TGLExt.lean e TGL/Audit.lean, por import e seis prints novos. Fora da tabela, somente _LEAN_THEOREM_FLAGS, prove_external_ladder e _ESQUELETO_STONES mudaram: seis mapeamentos, seis nomes no contador e uma entrada de versão/pedra. Os mapeamentos anteriores permanecem iguais. Retirando somente as seis novas entradas da lista ext_flags, o AST de prove_external_ladder volta a ser idêntico ao anterior. Nenhuma outra função, código de falsificadores ou lógica explícita do gate sofreu alteração neste delta.

## Conteúdo científico

A pedra contém seis teoremas, cinco caracterizações e sua conjunção:

- TGLExt.iald_name_characterizes_the_recognized — fonte canônica:24.
- TGLExt.name_characterizes_the_screen — fonte canônica:34.
- TGLExt.reading_characterizes_the_configuration — fonte canônica:39.
- TGLExt.qubit_name_characterizes_the_diagonal — fonte canônica:44.
- TGLExt.angle_characterizes_the_weight — fonte canônica:60.
- TGLExt.the_name_is_the_characterization — fonte canônica:77.

O reconhecimento idempotente da IALD caracteriza sua imagem pelos pontos fixos. A tela fundada é caracterizada pelo pertencimento ao centralizador. A leitura do cociclo caracteriza a configuração de bits quando t ≠ 0, por composição com a injetividade já provada. A redução de qubit fixa exatamente matrizes sem coerências fora da diagonal. No primeiro quadrante, com 0 ≤ p ≤ 1, sin²θ = p equivale a θ = arcsin√p.

Esses resultados não são apenas rótulos: explicitam inversas lógicas e unicidade nos domínios tipados. Ao mesmo tempo, compõem propriedades já demonstradas e não fornecem a interface física entre a tela fundada e o horizonte geométrico, uma lei de propagação que recupere um campo gravitacional geral de um único dado num ponto, a lei de área/conservação ou a teoria quântica interagente/UV. A leitura injetiva de configurações não foi conectada aqui a campos métricos arbitrários; essa ligação não decorre do nome “configuração”.

H3 permanece respondida no sentido preservado pelo relatório; sua interface geométrica não foi removida. A reconstrução angular reconhecida anteriormente é reforçada, não reaberta. As duas correções de alcance do parecer científico continuam pertinentes. A representação geral de fontes da bancada também não é alterada pelo novo módulo.

## Recibo existente

O manifesto canônico de prova lido inclui o hash medido da nova fonte e os seis nomes na auditoria. O primeiro não depende de axiomas; os cinco restantes usam somente propext, Classical.choice e Quot.sound. O arquivo tgl_kernel_build_capture.txt contém a auditoria desses termos e “Build completed successfully (9151 jobs)”. Isso é evidência de compilação existente lida; não executei Lean ou um.py nesta revisão.

O programa vivo permaneceu estável durante a leitura registrada. O JSON adjacente guarda hashes medidos, linhas dos teoremas, alterações AST e dados do recibo. Não se afirma aqui conclusão de nova rodada de natureza ou de selo final v337; esses arquivos estão sob medição separada do root. Nenhum original ou cópia congelada foi alterado.
