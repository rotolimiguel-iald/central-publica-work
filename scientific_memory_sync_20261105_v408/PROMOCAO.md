# Promoção F0.3 v408 — procedimento vinculado à ORDEM_007

Adendo ao roteiro inicial. O recibo independente da reconstrução do staging está em W\review\QUEUE_RECONSTRUCTION.json. A promoção reutiliza os 13 arquivos, o índice e o descritor desse snapshot. A CLI remapeou somente snapshot_root e os 13 campos documents[].path no manifesto candidato. Os bytes finais planejados estão em Q\promotion\MANIFEST_FINAL.json. A CLI admite os passos separadamente, para o pai poder parar e examinar o destino antes da troca.

~~~powershell
$Q = 'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261105_v408'
$W = 'C:\IALD\Central de Patentes\work\iald_v408_20261105'
$python = 'C:\Python314\python.exe'
$cli = Join-Path $Q 'promote_v408.py'
& $python -B -X utf8 $cli plan
~~~

**Produção.** A coordenação registra em W\F03_WRITE_V408.json a instrução específica recebida do operador e a vincula ao plano. Os campos e pinos medidos estão em Q\promotion\CONTRATOS.json. O texto original autorizado fica em um .txt da raiz de W, referenciado por caminho absoluto e SHA-256. A identidade e o sentido da autorização cabem ao pai. Os campos do contrato apenas vinculam os recibos. Qualquer autorização mais estreita exige adequar o procedimento ao seu alcance. A F0.3 está em AGUARDA_OPERADOR para a produção. Após a instrução, coordenar a posse do quadro e o preflight vigentes com o pai. Para obter o nome efetivo a passar à CLI:

~~~powershell
$unidade = (& $python -B -X utf8 C:\IALD\PROGRAMA_IALD\iald.py ver F0.3.MEMORIA_CIENTIFICA_SYNC | ConvertFrom-Json)
$membro = $unidade.reivindicacao.quem
~~~

Somente quem efetivamente detém a reivindicação, com a unidade em curso e a missão vigente, roda a etapa seguinte. Executar uma linha por vez e conferir o código de saída zero.

~~~powershell
& $python -B -X utf8 $cli materialize --member $membro
& $python -B -X utf8 $cli verify-final
~~~

A primeira etapa prepara os 16 arquivos em Q, confere cada pino e publica o diretório inativo por rename sem sobrescrita no mesmo volume Windows. Se o destino existir, sua árvore deve coincidir integralmente com o plano. Uma interrupção antes do rename deixa apenas uma pasta de transferência em Q. A segunda etapa usa o verificador de 13/10 sobre o caminho de produção, confere os 32.625 trechos, as fontes atuais, a geração e os três pacotes com o staging. Seu recibo fica em **Q\promotion\VERIFY_FINAL_PATHS.json**.

**Re-revisão do pai.** Abrir o destino de PLAN.json, conferir o pino do manifesto final contra MANIFEST_FINAL.json, as 14 alterações de caminho, os 16 arquivos e o baseline ainda ativo. Executar a verificação independente diretamente contra a raiz final. Registrar o parecer efetivo em **W\review\QUEUE_FINAL_PATHS.json**, com identidade, geração, SHA do manifesto final, SHA do VERIFY_FINAL_PATHS e SHA esperado do ACTIVE. CONTRATOS.json especifica os campos. O PASS do staging já ficou incorporado.

~~~powershell
& $python -B -X utf8 $cli activate --member $membro
& $python -B -X utf8 $cli receipt
~~~

A ativação revalida o recibo final, o aceite vinculado, a autorização e a titularidade. Usa ScientificMemorySync.activate com o baseline da v407, process_lock e expected_active_sha256 na API existente. Divergência durante a troca recusa sobrescrita. Em caso de interrupção, ler primeiro o ponteiro e o recibo. A API só reconhece idempotentemente o alvo já ativo se ele coincidir exatamente. Nunca atualizar o baseline para vencer um conflito.

A última linha roda em outro processo. Resolve o ponteiro padrão, exige CURRENT, verifica as leituras em três modos, os pinos antigos e o backup dos bytes da v407. A fila é conferida por digest dos arquivos, sem abrir seus bancos via SQLite. Atividade concorrente legítima pode mudar esses bytes: nesse caso, preservar o estado, conciliar com o pai e registrar a diferença antes de declarar preservação. O recibo de sucesso da ORDEM_007 é **Q\DELIVERY_TECHNICAL_R1.json**, criado somente ao fim, com release, status, epoch, generation, manifesto e recibos por SHA-256. Ausência de autorização, revisão ou verificação deixa esse recibo por emitir.
