# RESULTADO R3.6 (13/11/2026) -- o elo B(n) para a versao SEM pedra nova

Construtor: claude-construtor-r36, a servico da gerencia c1. Quem construiu nao aprova: falta a revisao independente. Hashes lidos dos arquivos por script (sha16).

## Por que
O ensaio do B(n) da v411 parou no T17 (12 PASSA, 1 NAO_EXECUTADO, 1 FALHA). A v411 e' a primeira versao sem modulo Lean novo desde que o B(n) existe e a R3.5 nao tem caminho para isso: recusa `pedras vazias`, exige o job do lake da raiz TGLExt (o lake nao o imprime quando nada e' compilado) e exigia o ANTES do kernel que o recibo gerado sem build nao trazia.

## O que mudou
- `R3_6\sincronizar_bancada.py` (bf5ad5c99d05fa57) = a R3.5 (02b22ba5c6d35c71, intocada) mais UM contrato explicito e separado, `KERNEL_RECIBO_R3_6` (versao sem pedra nova), so' em `verificar_kernel_recibo`: exige `versao_sem_pedra_nova: true`, `pedras` vazia, sem `modulos_de_auditoria`, raiz e Audit com antes == depois, so' o job do `TGL.Audit` no build log (mais a linha final) e a afirmacao positiva de que a impressao do manifesto pinado pelo selo == a do kernel anterior. A chave `versao_sem_pedra_nova` so' existe nesse contrato. R3_2 e R3_4: identicos (a unica diferenca admitida e' recusar a chave nova).
- `kernel\KERNEL_RECIBO_v411.json` (8ae51a512155f8ef, contrato KERNEL_RECIBO_R3_6): `formal_files_antes` (1764 arquivos, do manifesto v410 em custodia, conferido contra o pino), `nos_kernel_impressao` (49403b07f4e0ffae, cruzada com o recibo pre-selo da falha, o pre-selo pinado e o manifesto do Nos hoje), `toolchain.lake_version` MEDIDA com `lake --version` (cwd C:/t/k411c/final; unico comando lake), `arvore` = C:/t/k411c/arvore (refeita por refazer_arvore_v411_pos_selo.py, rc 0) e `varredura_tokens` recontada nela (1761 .lean, 156 em O16, zero juncao, zero token proibido). Nenhum build nem Audit refeito.
- `PINOS_BN_v411.json` (23b14e703f0a8dbf): `kernel_recibo` repinado, `esboco_R3_6` acrescentado (`esboco_R3_5` fica), `nota_r36`. `pos_rito\chain_pos_rito_v411.sh` (470ae9a6400e7e5c): usa `esboco_R3_6`; `sh -n` rc 0; nao executada.

## O que foi conferido (CONTROLES_R3_6.json, 8cfb95f4c59fe3a8; python -I -B -X utf8; veredito R3_6_CONFERIDA_POR_SCRIPT)
- Confinamento por AST: True. So' `verificar_kernel_recibo` difere entre as funcoes; atribuicoes de topo que diferem: KERNEL_CONTRATOS_ADMITIDOS, KERNEL_CONTRATO_R3_6, REVISAO; nenhum comando da R3.5 sumiu dentro da funcao (3 reescritos: docstring, a recusa `pedras vazias` virou `elif`, o `pino.update`); so' o docstring da funcao sumiu dos textos.
- Diferencial no caminho antigo (recibo REAL da v410 e mutacoes em copias): 35/35; mesmo par (passa, detalhe) em 32; 3 diferem, todos a chave `versao_sem_pedra_nova` num recibo R3_2/R3_4 (a R3.5 ignora, a R3.6 recusa); 0 diferencas nao admitidas; PASSA nas duas em 3.
- Caminho novo, insumos REAIS da v411: positivos 2/2; negativos 47/47, cada um recusado pelo motivo esperado (o trecho do detalhe e' conferido), inclusive o log sem a linha do TGL.Audit, sem a linha final, com sorry plantado, a arvore com juncao (a falha original), o Nos adulterado (arquivo formal mudado/novo/a menos) e a afirmacao positiva (so' ela alcanca um sha em maiuscula).

## O que NAO foi conferido (limites)
- A suite completa de 596 controles da R3.5 (sandbox de Bancada inteiro) NAO foi re-rodada; so' o diferencial de `verificar_kernel_recibo`, o confinamento por AST e o contrato novo.
- A equivalencia do caminho antigo e' medida por 35 casos, nao provada para toda entrada.
- A R3.6 nao foi rodada contra a producao nem pela cadeia; o ensaio do passo 10 e o aplicar sao da gerencia. Nada foi gravado na Bancada nem no Nos.
- Desvios ditos: a frase `nos_kernel_impressao.definicao` e' a do recibo da v410 com «selo v410» no lugar de «selo v409» (o selo que o Nos tinha na etapa 2; a ferramenta nao a le); PRONTO_POS_RITO_v411.json e outros que pinam o chain ou o PINOS_BN estao desatualizados e sao da gerencia.
