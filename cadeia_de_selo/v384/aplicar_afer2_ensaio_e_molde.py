# -*- coding: utf-8 -*-
"""As correcoes da 2a passada no ENSAIO A SECO (a checagem de nomes como na v383: nomes ligados no enunciado e antes dele no main), no GERADOR (a linha W08b sem a
marca v384, para o ensaio nao a executar fora do contexto), no LANCADOR (vigia que morre com o pai; a tarefa conferida; religar so se estava ligada; orfaos do
trabalhador encerrados antes e depois; VRAM conferida contra limiar), no INSTALADOR (recusa com trabalhador vivo) e no CONFERIDOR (beta, o arquivo do pilar no selo,
o terceiro balde vazio)."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))


def patch(fn, pairs, py=True):
    p = os.path.join(HERE, fn); s = open(p, encoding="utf-8").read()
    open(p + ".bak_antes_afer2", "w", encoding="utf-8", newline="").write(s)
    for old, new in pairs:
        c = s.count(old); assert c == 1, (fn, c, old[:100]); s = s.replace(old, new)
    if py:
        ast.parse(s)
    open(p + ".tmp", "w", encoding="utf-8", newline=chr(10)).write(s); os.replace(p + ".tmp", p); print("ok", fn)


# ---- o ensaio: a checagem de nomes da v383 (assigned_before + locais do enunciado)
patch("ensaio_a_seco_v384.py", [
    ('''bad = []
for st in comeca + contem:
    for node in ast.walk(st):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if st in contem and node.lineno not in tagged:
                continue
            if not (hasattr(um, node.id) or hasattr(builtins, node.id) or node.id in ("core", "_QP_ST_V384")):
                bad.append((node.lineno, node.id))''',
     '''def assigned_before(lineno):
    a = set()
    for node in ast.walk(main):
        if getattr(node, "lineno", 10 ** 9) < lineno:
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store): a.add(node.id)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)): a.add(node.name)
            if isinstance(node, ast.arg): a.add(node.arg)
    return a


bad = []
for st in comeca + contem:
    ab = assigned_before(st.lineno); loc = {m.id for m in ast.walk(st) if isinstance(m, ast.Name) and isinstance(m.ctx, ast.Store)}
    for node in ast.walk(st):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if st in contem and node.lineno not in tagged:
                continue
            if not (hasattr(um, node.id) or hasattr(builtins, node.id) or node.id in ab or node.id in loc or node.id in ("core", "_QP_ST_V384")):
                bad.append((node.lineno, node.id))'''),
])
# ---- o gerador: a linha W08b sem a marca (o comentario acima, com a marca, fica)
patch("gerar_candidato_v384.py", [
    ('''add("W08b_terceiro_balde_selo", "G_SELO", A08b, '    seal["not_sealed_this_run"] = {"formais": _formais, "recusas_de_dado": _recusas, "computacao_nao_concluida": _computacao}   # v384: o terceiro balde' + CRLF,''',
     '''add("W08b_terceiro_balde_selo", "G_SELO", A08b, '    seal["not_sealed_this_run"] = {"formais": _formais, "recusas_de_dado": _recusas, "computacao_nao_concluida": _computacao}   # o terceiro balde (ver o comentario acima)' + CRLF,'''),
])
# ---- o lancador
patch("rito_v384.sh", [
    ('''religar() {
  [ -f "$PK/.vigia_ativo" ] && rm -f "$PK/.vigia_ativo"
  log "RELIGANDO o servidor do modelo nativo pela tarefa agendada (como no boot)"''',
     '''orfaos() {
  # encerra qualquer trabalhador do pilar quantico vivo (orfao de uma rodada morta) -- a GPU nao pode ter dois (afericao 2)
  o=$(powershell.exe -NoProfile -NonInteractive -Command "Get-CimInstance Win32_Process -Filter \\"Name='python.exe' OR Name='pythonw.exe'\\" | Where-Object { \\$_.CommandLine -and \\$_.CommandLine -match 'pilar_quantico_worker\\.py' } | ForEach-Object { \\$_.ProcessId }" 2>/dev/null | tr -d '\\r')
  for p in $o; do log "ORFAO do pilar quantico encontrado (PID $p) -- encerrando a arvore"; taskkill //T //F //PID "$p" >> "$LOGS" 2>&1; done
}

religar() {
  [ -f "$PK/.vigia_ativo" ] && rm -f "$PK/.vigia_ativo"
  orfaos
  if [ "$TAREFA_EXISTE" != "1" ] || [ "$ESTAVA_LIGADO" != "1" ]; then
    log "nao religo: a tarefa existe=$TAREFA_EXISTE ; o servidor estava ligado antes=$ESTAVA_LIGADO (restauro o estado anterior, nao mais que isso)"; return 0
  fi
  log "RELIGANDO o servidor do modelo nativo pela tarefa agendada (como no boot)"'''),
    ('''# 1. parar o servidor: a TAREFA primeiro (parada deliberada nao conta como falha para o reinicio automatico), depois o supervisor e os orfaos
log "PARANDO o servidor do modelo nativo: tarefa agendada, supervisor e llama-server (ordem do operador, 03/10)"''',
     '''# 0. o estado de antes (para restaurar exatamente ele) e os orfaos de rodadas mortas
TAREFA_EXISTE=$(powershell.exe -NoProfile -NonInteractive -Command "if (Get-ScheduledTask -TaskName 'IALD Llama Server' -ErrorAction SilentlyContinue) { '1' } else { '0' }" 2>/dev/null | tr -d '\\r')
ESTAVA_LIGADO=$(powershell.exe -NoProfile -NonInteractive -Command "if (@(Get-Process llama-server -ErrorAction SilentlyContinue).Count -gt 0) { '1' } else { '0' }" 2>/dev/null | tr -d '\\r')
log "antes: tarefa existe=$TAREFA_EXISTE ; servidor ligado=$ESTAVA_LIGADO"
orfaos
# 1. parar o servidor: a TAREFA primeiro (parada deliberada nao conta como falha para o reinicio automatico), depois o supervisor e os orfaos
log "PARANDO o servidor do modelo nativo: tarefa agendada, supervisor e llama-server (ordem do operador, 03/10)"'''),
    ('''if [ "$vivos" != "0" ]; then
  log "O SERVIDOR NAO PAROU -- NAO RODO (fail-closed); religando o estado anterior"
  religar; exit 10
fi''', '''if [ "$vivos" != "0" ]; then
  log "O SERVIDOR NAO PAROU -- NAO RODO (fail-closed); religando o estado anterior"
  religar; exit 10
fi
if [ -n "$mem" ] && [ "$mem" -gt 6000 ] 2>/dev/null; then
  log "a VRAM usada ($mem MiB) passa de 6000 MiB com o servidor parado: ha outro processo na GPU -- NAO RODO (fail-closed)"
  religar; exit 11
fi'''),
    ('''touch "$PK/.vigia_ativo"
(
  while [ -f "$PK/.vigia_ativo" ]; do''', '''touch "$PK/.vigia_ativo"
PAI=$$
(
  t_ini=$(date +%s)
  while [ -f "$PK/.vigia_ativo" ]; do
    # o vigia morre com o lancador (se o sh for morto a forca, o trap nao roda) e nunca passa de 8 h
    kill -0 "$PAI" 2>/dev/null || { echo "$(date +%H:%M:%S) VIGIA: o lancador morreu -- o vigia sai" >> "$LOGS"; break; }
    [ $(( $(date +%s) - t_ini )) -gt 28800 ] && { echo "$(date +%H:%M:%S) VIGIA: 8 h -- o vigia sai" >> "$LOGS"; break; }'''),
], py=False)
# ---- o instalador: recusa com trabalhador do pilar vivo
patch("instalar_v384.py", [
    ('''"Where-Object { $_.CommandLine -ne $null -and $_.CommandLine -match '(^|[\\\\\\\\ \\"])um\\\\.py\\"?(\\\\s|$)' } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],''',
     '''"Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\\\\\ \\"])um\\\\.py\\"?(\\\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],'''),
])
# ---- o conferidor: beta conferido; o arquivo do pilar no selo; o terceiro balde vazio
patch("conferir_rito_v384.py", [
    ('''    "o selo registra o mesmo veredito e o mesmo sha256 do resultado": sq.get("verdict") == V("quantum_pillar_v384") and sq.get("result_sha256") == qp.get("result_sha256"),''',
     '''    "o selo registra o mesmo veredito e o mesmo sha256 do resultado": sq.get("verdict") == V("quantum_pillar_v384") and sq.get("result_sha256") == qp.get("result_sha256"),
    "o beta do trabalhador e' o do core (bit a bit) e a marca da rodada esta no resultado": qp.get("beta_matches_core") is True and bool(qp.get("run_id")),
    "o resultado do pilar esta no Nos e no hash do selo": (lambda p_: os.path.exists(p_) and (selo.get("sha256") or {}).get("um_absoluto_pilar_quantico.json") == hashlib.sha256(open(p_, "rb").read()).hexdigest() == qp.get("result_sha256"))(os.path.join(NOS, "um_absoluto_pilar_quantico.json")),
    "o terceiro balde da custodia de sentido existe e esta vazio": (selo.get("not_sealed_this_run") or {}).get("computacao_nao_concluida") == [],'''),
])
