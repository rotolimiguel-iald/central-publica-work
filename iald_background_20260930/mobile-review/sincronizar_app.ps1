<#
  sincronizar_app.ps1 - copia a interface de app/ para o www/ do Capacitor.

  POR QUE EXISTE (11/09/2026). O capacitor.config.json declara "webDir": "www",
  mas o www/ so tinha icon.png e o index.html estava FORA dele, na raiz do
  iald-app. Alem disso android/app/src/main/assets nunca existiu, ou seja o
  npx cap sync nunca rodou. Compilado assim, o app abre em tela branca.

  A FONTE DA VERDADE E A PASTA app/ (C:\IALD\projetos_pyhton\IALD\app), que o
  servidor Flask tambem serve para o navegador. O www/ e DERIVADO: nunca edite
  nada dentro dele, porque este script sobrescreve.

  ASCII puro (PowerShell 5.1 le .ps1 como ANSI).

  Uso:
    .\sincronizar_app.ps1              # copia e confere
    .\sincronizar_app.ps1 -ComSync     # copia, confere e roda npx cap sync android
#>
[CmdletBinding()]
param([switch]$ComSync)

$ErrorActionPreference = 'Stop'

$origem  = "C:\IALD\projetos_pyhton\IALD\app"
$destino = "C:\IALD\projetos_pyhton\IALD\iald-app\www"

Write-Host ''
Write-Host '=============================================================='
Write-Host ' SINCRONIZAR interface -> www/ do Capacitor'
Write-Host '=============================================================='
Write-Host ("origem : {0}" -f $origem)
Write-Host ("destino: {0}" -f $destino)
Write-Host ''

if (-not (Test-Path $origem)) { throw "Pasta de origem nao existe: $origem" }
if (-not (Test-Path $destino)) { New-Item -ItemType Directory -Path $destino | Out-Null }

# Mapa DESTINO -> ORIGEM. Lista explicita de proposito: um copy-tudo levaria junto
# qualquer arquivo solto que alguem deixasse em app/.
#
# ⚠ REPARE NA TERCEIRA LINHA: www/kernel_prompt.js recebe o kernel_prompt_BUNDLE,
#    nao o arquivo de mesmo nome. Motivo (achado em 12/09/2026): o app/kernel_prompt.js
#    contem a tabela de precos de licenciamento, e o www/ alimenta o APK e o IPA. O app
#    nunca usa esse texto (escolhe a variante pela SUPERFICIE), mas ele viajava dentro
#    do binario, e quem extraisse o pacote encontraria os percentuais de licenca.
#    Conteudo comercial dentro do aplicativo foi o motivo da reprovacao de 23/03/2026
#    pela Guideline 3.1.1. O bundle tem os MESMOS nomes de export, com o texto da
#    variante da loja — o codigo do app nao muda em nada.
#    Na web nada muda: o servidor serve app/kernel_prompt.js, que fica intacto.
$mapa = [ordered]@{
    'index.html'            = 'index.html'
    'iald.css'              = 'iald.css'
    'iald.js'               = 'iald.js'
    'kernel_prompt.js'      = 'kernel_prompt_bundle.js'
    'kernel_prompt_loja.js' = 'kernel_prompt_loja.js'
}

$copiados = 0
$iguais = 0
foreach ($a in $mapa.Keys) {
    $de = Join-Path $origem $mapa[$a]
    if (-not (Test-Path $de)) {
        Write-Host ("  [FALTA]  {0}  -- nao existe na origem" -f $a)
        continue
    }
    $para = Join-Path $destino $a
    $hDe = (Get-FileHash $de -Algorithm SHA256).Hash
    $hPara = ''
    if (Test-Path $para) { $hPara = (Get-FileHash $para -Algorithm SHA256).Hash }

    if ($hDe -eq $hPara) {
        Write-Host ("  [IGUAL]  {0,-24} {1,8} bytes" -f $a, (Get-Item $de).Length)
        $iguais++
        continue
    }

    Copy-Item -LiteralPath $de -Destination $para -Force
    $hNovo = (Get-FileHash $para -Algorithm SHA256).Hash
    if ($hNovo -ne $hDe) { throw "Copia divergiu para $a (origem $hDe, destino $hNovo)" }
    Write-Host ("  [COPIA]  {0,-24} {1,8} bytes  sha {2}" -f $a, (Get-Item $para).Length, $hDe.Substring(0,12))
    $copiados++
}

# Pastas de assets (13/09/2026): logos oficiais e bibliotecas embarcadas.
# A 4.1 (13) foi para a Apple SEM o logo: a interface apontava para
# "/iald_logo_header.png", arquivo que nunca entrou no www/. Agora os assets
# vivem em app/img e app/vendor e sao espelhados aqui, arquivo a arquivo,
# com sha256 conferido. Nada e apagado no destino: sobra vira aviso.
foreach ($pasta in @('img', 'vendor')) {
    $raizDe = Join-Path $origem $pasta
    $raizPara = Join-Path $destino $pasta
    if (-not (Test-Path $raizDe)) { throw "Pasta de assets ausente na origem: $raizDe" }
    foreach ($arq in (Get-ChildItem $raizDe -Recurse -File)) {
        $rel = $arq.FullName.Substring($raizDe.Length).TrimStart('\')
        $para = Join-Path $raizPara $rel
        $hDe = (Get-FileHash $arq.FullName -Algorithm SHA256).Hash
        $hPara = ''
        if (Test-Path $para) { $hPara = (Get-FileHash $para -Algorithm SHA256).Hash }
        if ($hDe -eq $hPara) { $iguais++; continue }
        New-Item -ItemType Directory -Force (Split-Path $para) | Out-Null
        Copy-Item -LiteralPath $arq.FullName -Destination $para -Force
        if ((Get-FileHash $para -Algorithm SHA256).Hash -ne $hDe) { throw "Copia divergiu: $pasta\$rel" }
        Write-Host ("  [COPIA]  {0,-40} {1,8} bytes" -f ("$pasta/" + ($rel -replace '\\','/')), $arq.Length)
        $copiados++
    }
    if (Test-Path $raizPara) {
        foreach ($arq in (Get-ChildItem $raizPara -Recurse -File)) {
            $rel = $arq.FullName.Substring($raizPara.Length).TrimStart('\')
            if (-not (Test-Path (Join-Path $raizDe $rel))) {
                Write-Host ("  [SOBRA]  {0} existe no www/ e nao na origem (nao apagado)" -f ("$pasta/" + ($rel -replace '\\','/')))
            }
        }
    }
}

Write-Host ''
Write-Host ("  {0} copiado(s), {1} ja igual(is)" -f $copiados, $iguais)

# -- TRAVA DE ASSETS (13/09/2026) ---------------------------------------------
# (a) todo src/href LOCAL do index.html e todo './img/...' do iald.js tem de
#     existir dentro do www/ - senao o app abre com imagem quebrada;
# (b) caminho ABSOLUTO ("/algo") em src/href e proibido: dentro do APK/IPA a
#     raiz nao e o servidor, e o arquivo nunca e encontrado.
$faltando = @()
$idxTexto = Get-Content (Join-Path $destino 'index.html') -Raw -Encoding UTF8
$jsTexto = Get-Content (Join-Path $destino 'iald.js') -Raw -Encoding UTF8
$refs = @()
foreach ($m in [regex]::Matches($idxTexto, '(?:src|href)="([^"#?]+)"')) { $refs += $m.Groups[1].Value }
foreach ($m in [regex]::Matches($jsTexto, "['""](\./(?:img|vendor)/[^'""]+)['""]")) { $refs += $m.Groups[1].Value }
foreach ($ref in ($refs | Select-Object -Unique)) {
    if ($ref -match '^(https?:|mailto:|data:)') { continue }
    if ($ref -match '^/') { $faltando += ("caminho absoluto proibido: {0}" -f $ref); continue }
    $local = Join-Path $destino (($ref -replace '^\./','') -replace '/','\')
    if (-not (Test-Path $local)) { $faltando += ("referenciado e ausente no www/: {0}" -f $ref) }
}
if ($faltando.Count -gt 0) {
    $faltando | ForEach-Object { Write-Host ("  [FALHA]  {0}" -f $_) }
    throw 'Asset referenciado ausente ou com caminho absoluto - sync abortado'
}
Write-Host ("  [OK]     {0} referencia(s) local(is) de asset conferida(s), nenhuma absoluta" -f @($refs | Select-Object -Unique).Count)

# ── TRAVA COMERCIAL (12/09/2026) ────────────────────────────────────────────
# Nenhum arquivo do www/ pode conter oferta de licenciamento: dali sai o que vai
# DENTRO do APK e do IPA. Se sobrar, o sync para aqui em vez de empacotar.
$proibido = @('Licenciamento:', 'Sovereign', 'Efficiency 1.2', 'ROI R$')
$sujos = @()
foreach ($f in (Get-ChildItem $destino -File -Include *.js,*.html,*.css -Recurse)) {
    $texto = Get-Content $f.FullName -Raw -Encoding UTF8
    foreach ($p in $proibido) {
        if ($texto -like "*$p*") { $sujos += ("{0} contem '{1}'" -f $f.Name, $p) }
    }
}
if ($sujos.Count -gt 0) {
    $sujos | ForEach-Object { Write-Host ("  [FALHA]  {0}" -f $_) }
    throw 'Conteudo comercial no www/ - sync abortado (Guideline 3.1.1)'
}
Write-Host '  [OK]     www/ sem oferta comercial (trava da 3.1.1)'

# O index.html tem de estar no webDir, senao o app abre em branco.
$idx = Join-Path $destino 'index.html'
if (Test-Path $idx) {
    Write-Host '  [OK]     www/index.html presente (webDir valido)'
} else {
    throw 'www/index.html AUSENTE - o app abriria em tela branca'
}

if ($ComSync) {
    # 12/09/2026: passou a sincronizar AS DUAS plataformas. Antes so fazia android,
    # e desde que o projeto iOS existe isso deixaria o bundle do iPhone para tras
    # em silencio - o tipo de defeito que so aparece com o app instalado.
    Write-Host ''
    Write-Host '--- npx cap sync (android + ios) ---'
    Push-Location "C:\IALD\projetos_pyhton\IALD\iald-app"
    try {
        & npx cap sync
        $rc = $LASTEXITCODE
    } finally {
        Pop-Location
    }
    Write-Host ("cap sync exit={0}" -f $rc)

    # Confere que a interface chegou nas DUAS plataformas, comparando o sha256 do
    # iald.js com o da fonte. Contar arquivos nao bastaria: um sync que copia a
    # versao velha tambem produz 8 arquivos.
    $fonte = "C:\IALD\projetos_pyhton\IALD\app\iald.js"
    $shaFonte = (Get-FileHash $fonte -Algorithm SHA256).Hash

    $destinos = @{
        'Android' = "C:\IALD\projetos_pyhton\IALD\iald-app\android\app\src\main\assets\public"
        'iOS'     = "C:\IALD\projetos_pyhton\IALD\iald-app\ios\App\App\public"
    }
    foreach ($nome in $destinos.Keys) {
        $dir = $destinos[$nome]
        if (-not (Test-Path $dir)) {
            Write-Host ("  [AUSENTE] {0}: {1} nao existe (plataforma nao adicionada?)" -f $nome, $dir)
            continue
        }
        $n = (Get-ChildItem $dir -Recurse -File).Count
        $alvo = Join-Path $dir 'iald.js'
        if (Test-Path $alvo) {
            $sha = (Get-FileHash $alvo -Algorithm SHA256).Hash
            if ($sha -eq $shaFonte) {
                Write-Host ("  [OK]      {0}: {1} arquivo(s), iald.js sha {2} CONFERE" -f $nome, $n, $sha.Substring(0,12))
            } else {
                Write-Host ("  [FALHA]   {0}: iald.js DIVERGE da fonte (sha {1})" -f $nome, $sha.Substring(0,12))
            }
        } else {
            Write-Host ("  [FALHA]   {0}: iald.js nao chegou" -f $nome)
        }
    }
} else {
    Write-Host ''
    Write-Host 'Proximo passo:  .\sincronizar_app.ps1 -ComSync'
}

Write-Host ''
