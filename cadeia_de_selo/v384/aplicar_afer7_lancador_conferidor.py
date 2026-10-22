# -*- coding: utf-8 -*-
"""7a afericao no LANCADOR e no CONFERIDOR (scripts salvos, count == 1):
- o log e o rito_v384_sinal.txt GIRAM (.anterior) no comeco de cada rodada, DEPOIS das guardas (uma tentativa recusada nao apaga o registro da anterior);
- um .rito_v384.pid de lancador VIVO (kill -0 e /proc/<pid>/cmdline com rito_v384) faz RECUSAR (codigo 16) antes de qualquer parada ou dos orfaos;
  o velho e' dito como AVISO;
- com o vigia morto por prazo, o marcador so sai se nenhuma parada (Stop-ScheduledTask da tarefa) estiver em curso;
- o conferidor classifica «escutou e PAROU» antes de «a porta 8081 nao escutou», le so as linhas do log() do lancador (HH:MM:SS) e le o rito_v384_sinal.txt.
Backups ja feitos (.bak_antes_afer7)."""
import ast, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "rito_v384.sh")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer7", "rb").read() == raw
PAIRS = [
    ('''LOGS="$PK/rito_servidor_v384.log"
: > "$LOGS"
''', '''LOGS="$PK/rito_servidor_v384.log"
'''),
    ('''n=$(echo "$v" | grep -c -E '^[0-9]+\\s*$'); [ "$n" = "0" ] || { echo "ha processo um.py vivo ($v) -- NAO RODO"; exit 6; }''',
     '''n=$(echo "$v" | grep -c -E '^[0-9]+\\s*$'); [ "$n" = "0" ] || { echo "ha processo um.py vivo ($v) -- NAO RODO"; exit 6; }
# outro LANCADOR vivo (ainda sem um.py, por exemplo na parada do servidor): recusar ANTES de qualquer parada ou dos orfaos (7a afericao)
PID_VELHO=""
if [ -f "$PK/.rito_v384.pid" ]; then
  op_=$(cat "$PK/.rito_v384.pid" 2>/dev/null)
  if [ -n "$op_" ] && kill -0 "$op_" 2>/dev/null && grep -q "rito_v384" "/proc/$op_/cmdline" 2>/dev/null; then echo "OUTRO lancador do rito v384 esta VIVO (PID $op_) -- NAO RODO"; exit 16; fi
  PID_VELHO="$op_"
fi
# o log e o registro dos sinais GIRAM so agora, depois das guardas: uma tentativa recusada nao apaga o registro da anterior (7a afericao)
[ -f "$LOGS" ] && mv -f "$LOGS" "$LOGS.anterior"
: > "$LOGS"
[ -f "$PK/rito_v384_sinal.txt" ] && mv -f "$PK/rito_v384_sinal.txt" "$PK/rito_v384_sinal.txt.anterior"
[ -n "$PID_VELHO" ] && log "AVISO: .rito_v384.pid velho ($PID_VELHO): de um lancador que nao vive mais -- sera sobrescrito"'''),
    ('''[ -f "$PK/.rito_v384.pid" ] && log "um .rito_v384.pid VELHO estava no pacote ($(cat "$PK/.rito_v384.pid")): de um lancador que morreu sem restaurar -- sobrescrito"
''', ''''''),
    ('''        if powershell.exe -NoProfile -NonInteractive -Command "if (Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" > /dev/null 2>&1; then
          log "servidor de volta: a porta 8081 escuta (reconferida 30 s depois, por causa do AVISO acima)"; rm -f "$MARCA"; return 0
        fi''', '''        if powershell.exe -NoProfile -NonInteractive -Command "if (Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" > /dev/null 2>&1; then
          # nenhuma parada da tarefa ainda em curso (a classe [T] impede a consulta de casar consigo mesma) -- senao o marcador fica (7a afericao)
          sp_=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-CimInstance Win32_Process -Filter \\"Name='powershell.exe' OR Name='pwsh.exe'\\" | Where-Object { \\$_.CommandLine -and \\$_.CommandLine -match 'Stop-Scheduled[T]ask' -and \\$_.CommandLine -match 'IALD Llama' }).Count" 2>/dev/null | tr -d '\\r')
          if [ "$sp_" = "0" ]; then log "servidor de volta: a porta 8081 escuta (reconferida 30 s depois, por causa do AVISO acima)"; rm -f "$MARCA"; return 0; fi
          log "AVISO: a porta 8081 escuta, mas ha parada da tarefa ainda em curso ('$sp_') -- o marcador fica: $MARCA"; return 0
        fi'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
b = s.encode("utf-8"); assert b"\r" not in b
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok lancador", len(PAIRS))
C = os.path.join(HERE, "conferir_rito_v384.py"); c = open(C, "rb").read().decode("utf-8")
assert open(C + ".bak_antes_afer7", "rb").read().decode("utf-8") == c
CP = [
    ('''res["servidor_depois_do_rito"] = ("RELIGADO (a porta 8081 escuta)" if "servidor de volta" in _lt else ("nao religado: nao estava ligado antes" if "nao religo" in _lt''',
     '''res["servidor_depois_do_rito"] = ("PAROU DEPOIS DE ESCUTAR (o marcador ficou) -- conferir a tarefa" if "escutou e PAROU" in _lt else
                                  "RELIGADO (a porta 8081 escuta)" if "servidor de volta" in _lt else ("nao religado: nao estava ligado antes" if "nao religo" in _lt'''),
    ('''res["avisos_do_lancador"] = [l_ for l_ in _lt.splitlines() if "AVISO" in l_ or "FALHA VISIVEL" in l_]   # TODA linha de AVISO/FALHA (6a afericao)''',
     '''res["avisos_do_lancador"] = [l_ for l_ in _lt.splitlines() if re.match(r"^\\d\\d:\\d\\d:\\d\\d ", l_) and ("AVISO" in l_ or "FALHA VISIVEL" in l_)]   # so o log() do lancador (6a e 7a)
_sg = os.path.join(HERE, "rito_v384_sinal.txt")
res["sinais_desta_rodada"] = (open(_sg, encoding="utf-8", errors="replace").read().splitlines() if os.path.exists(_sg) else [])   # gira a cada rodada (7a afericao)'''),
    ('''for l_ in res["avisos_do_lancador"]:
    print("  AVISO DO LANCADOR:", l_)''', '''for l_ in res["avisos_do_lancador"]:
    print("  AVISO DO LANCADOR:", l_)
for l_ in res["sinais_desta_rodada"]:
    print("  SINAL/FALHA desta rodada (rito_v384_sinal.txt):", l_)'''),
]
for old, new in CP:
    k = c.count(old); assert k == 1, (k, old[:100])
    c = c.replace(old, new)
ast.parse(c)
open(C + ".tmp", "wb").write(c.encode("utf-8")); os.replace(C + ".tmp", C); print("ok conferidor", len(CP))
