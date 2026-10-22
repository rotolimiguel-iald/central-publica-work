$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\IALD\projetos_pyhton\IALD'
$taskStamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$taskAppend = @'


## Adendo 13/09/2026 — cadastro Google e acesso Apple

[REAL — observado no navegador] O operador entrou na conta Google. O fluxo em https://play.google.com/console/signup foi iniciado como organização, tipo "Uma empresa ou corporação", nome público IALD. A criação do perfil para pagamentos parou no campo obrigatório D-U-N-S de nove dígitos. Nenhum número foi inventado; nenhuma tentativa foi consumida com um número não verificado. Não foram concluídos o perfil, o pagamento da taxa ou a conta de desenvolvedor.

[INPUT] O operador informou não ter o D-U-N-S. [REAL] Não foi localizado nos documentos consultados. Isso não comprova inexistência de número já atribuído pela D&B.

A documentação do Google https://support.google.com/googleplay/android-developer/answer/13634888?hl=pt-BR indica serviço gratuito e encaminha o Brasil à CIAL Dun & Bradstreet. O link regional redirecionou a https://pt.cialdnb.com/customer-support . Em https://pt.cialdnb.com/duns-number , "Inicie sua solicitação" abriu o atendimento por chat. A página menciona prazo de até 30 dias úteis; não foi contratada a modalidade rápida paga. A consulta https://my.dnb.com/lookup mostrou-se restrita a empresas dos Estados Unidos e não foi usada com dados brasileiros.

Foi solicitada autorização específica, ainda sem resposta no momento deste registro, para enviar ao atendimento CIAL a mensagem: "Solicito a consulta de eventual D-U-N-S existente ou a emissão gratuita para IALD LTDA, CNPJ 62.757.606/0001-23, Goiânia/GO, Brasil, para cadastro no Google Play Console. Não desejo contratar serviços pagos. Qual é o formulário necessário?" Nenhuma mensagem foi enviada. O chatbot apresentou a pergunta de finalidade e o seletor DUNS Requestor; aguarda continuação após autorização. Confirmar dados de contato e endereço se forem exigidos, sem misturar com o Escritório Miguel.

[REAL] App Store Connect permanece em https://appstoreconnect.apple.com/login . "Inicie sessão com o iPhone" falhou com "Não foi possível verificar sua identidade. Tente novamente." antes de mostrar QR code. A causa não foi comprovada. O operador esqueceu a senha e quer usar o iPhone. Foi indicada a recuperação oficial no aparelho já conectado à mesma Conta Apple: Ajustes > seu nome > Início de Sessão e Segurança > Alterar Senha, usando o código do aparelho, conforme https://support.apple.com/pt-br/102656 . O próprio operador deve fazer isso e digitar a senha diretamente no portal; não pedir senha ou códigos em mensagens.

As abas Apple, Google e CIAL foram preservadas para retomada. As autorizações anteriores de criar a chave Android e criar/enviar o repositório privado já foram concedidas e executadas: não repetir essas perguntas. Nenhuma nova compilação, assinatura Apple, publicação ou instalação em aparelho ocorreu neste adendo. O modelo e o servidor não foram alterados.
'@
$taskTargets = @(
    (Join-Path $taskRoot 'iald-app\HANDOFF_CODEX_PROSSIGA_20260913.md'),
    (Join-Path $taskRoot 'iald-app\HANDOFF_CODEX.md'),
    (Join-Path $taskRoot 'CLAUDE.md')
)
$taskUtf8 = [Text.UTF8Encoding]::new($false)
$taskAddition = $taskUtf8.GetBytes($taskAppend.Replace("`r`n", "`n").Replace("`n", "`r`n"))
foreach ($taskPath in $taskTargets) {
    $taskOriginal = [IO.File]::ReadAllBytes($taskPath)
    if ($taskUtf8.GetString($taskOriginal).Contains('## Adendo 13/09/2026 — cadastro Google e acesso Apple')) {
        Write-Output "Adendo já existe: $taskPath"
        continue
    }
    $taskBackup = "$taskPath.bak_$taskStamp"
    [IO.File]::WriteAllBytes($taskBackup, $taskOriginal)
    $taskBackupBytes = [IO.File]::ReadAllBytes($taskBackup)
    if ([Convert]::ToBase64String($taskOriginal) -cne [Convert]::ToBase64String($taskBackupBytes)) { throw 'Backup divergente' }
    $taskMerged = [byte[]]::new($taskOriginal.Length + $taskAddition.Length)
    [Array]::Copy($taskOriginal, 0, $taskMerged, 0, $taskOriginal.Length)
    [Array]::Copy($taskAddition, 0, $taskMerged, $taskOriginal.Length, $taskAddition.Length)
    $taskTemp = "$taskPath.tmp_$taskStamp"
    [IO.File]::WriteAllBytes($taskTemp, $taskMerged)
    if ((Get-Item -LiteralPath $taskTemp).Length -ne $taskMerged.Length) { throw 'Tamanho temporário divergente' }
    [IO.File]::Move($taskTemp, $taskPath, $true)
    $taskAfter = [IO.File]::ReadAllBytes($taskPath)
    if ([Convert]::ToBase64String($taskAfter) -cne [Convert]::ToBase64String($taskMerged)) {
        [IO.File]::Copy($taskBackup, $taskPath, $true)
        throw 'Verificação final falhou; backup restaurado'
    }
    Write-Output "Atualizado com backup em bytes: $taskPath ($($taskOriginal.Length) -> $($taskAfter.Length) bytes)"
}
