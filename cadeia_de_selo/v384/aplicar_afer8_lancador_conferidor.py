# -*- coding: utf-8 -*-
"""8a afericao no LANCADOR e no CONFERIDOR (scripts salvos, count == 1):
- a VEZ: o .rito_v384.pid e' gravado LOGO depois da guarda (antes da fase 0) e removido em qualquer saida antecipada (trap proprio, trocado pelo religar depois);
- o LOG da tentativa vai para um arquivo proprio da fase 0 e so GIRA para o lugar do log real (.anterior) depois da ULTIMA recusa -- uma tentativa recusada em
  qualquer ponto nao tira do lugar o log nem o registro de sinais da rodada anterior;
- a reconferencia depois de um AVISO conta tambem o stop_iald_llama.ps1 (a mesma consulta da espera de 60 s);
- o AVISO do PID velho e' rotulado AVISO_PID_VELHO (nao e' do religamento);
- o cabecalho: o codigo 16, o giro depois da ultima recusa, o marcador que fica com parada em curso, e conferir /proc/<pid>/cmdline antes de abortar;
- o conferidor: «escuta, mas ha parada» classificado a parte; «RELIGADO COM AVISO» so pelos AVISOs do religamento e do vigia (o AVISO_PID_VELHO e' listado,
  nao conta).
  [ERRATA AO LADO, gerencia, 04/10, depois de rodar: a linha original dizia «le tambem o rito_v384_sinal.txt.anterior se o atual estiver vazio» -- isso NAO foi
  feito, de proposito: ler o .anterior misturaria rodadas. O registro dos sinais so recebe linha com RITO_INICIADO=1 ou no mata_um (ambos depois do giro), logo
  a fase 0 nunca escreve nele; o que mudou no conferidor foi so o comentario.]
Backups ja feitos (.bak_antes_afer8)."""
import ast, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "rito_v384.sh")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer8", "rb").read() == raw
PAIRS = [
    (r'''# PowerShell: o numero e' o PID do MSYS, nao o do Windows -- o TaskStop da ferramenta da gerencia NAO para o lancador. O mata_um so encerra a arvore DESTA rodada (descendentes do lancador). (3a a 5a afericoes, 03-04/10/2026)''',
     r'''# PowerShell: o numero e' o PID do MSYS, nao o do Windows -- o TaskStop da ferramenta da gerencia NAO para o lancador; ANTES de abortar, conferir que
# /proc/$(cat .rito_v384.pid)/cmdline contem rito_v384. O mata_um so encerra a arvore DESTA rodada (descendentes do lancador), fail-closed. Com outro lancador
# vivo, RECUSA (codigo 16). O log da tentativa vai para .fase0 e so gira para o lugar do log real (.anterior) depois da ULTIMA recusa. Depois de um AVISO no
# religamento, o marcador so sai se a porta ainda escutar 30 s depois E nenhuma parada (Stop-ScheduledTask ou stop_iald_llama.ps1) estiver em curso.
# (3a a 8a afericoes, 03-04/10/2026)'''),
    (r'''# o log e o registro dos sinais GIRAM so agora, depois das guardas: uma tentativa recusada nao apaga o registro da anterior (7a afericao)
[ -f "$LOGS" ] && mv -f "$LOGS" "$LOGS.anterior"
: > "$LOGS"
[ -f "$PK/rito_v384_sinal.txt" ] && mv -f "$PK/rito_v384_sinal.txt" "$PK/rito_v384_sinal.txt.anterior"
[ -n "$PID_VELHO" ] && log "AVISO: .rito_v384.pid velho ($PID_VELHO): de um lancador que nao vive mais -- sera sobrescrito"''',
     r'''# a VEZ: o PID deste lancador gravado JA (antes da fase 0) e removido em qualquer saida antecipada; o religar o remove no fim (8a afericao)
echo $$ > "$PK/.rito_v384.pid"
trap 'rm -f "$PK/.rito_v384.pid"' EXIT
# a fase 0 escreve num log PROPRIO; o log real (e o registro dos sinais) so gira depois da ULTIMA recusa (8a afericao)
LOGF="$LOGS"; LOGS="$PK/rito_servidor_v384.log.fase0"; : > "$LOGS"
[ -n "$PID_VELHO" ] && log "AVISO_PID_VELHO: .rito_v384.pid velho ($PID_VELHO): de um lancador que nao vive mais -- sobrescrito"'''),
    (r'''echo $$ > "$PK/.rito_v384.pid"   # abortar = kill -TERM $(cat .rito_v384.pid) NO GIT BASH (e' PID do MSYS, nao do Windows) (5a e 6a afericoes)
''', r'''# (o .rito_v384.pid ja foi gravado logo depois da guarda; abortar = kill -TERM $(cat .rito_v384.pid) NO GIT BASH, conferindo antes o /proc/<pid>/cmdline)
'''),
    (r'''# 2. o vigia: se o servidor reaparecer durante o rito, e' encerrado e o fato fica no log''',
     r'''# a ROTACAO, so agora, depois da ULTIMA recusa: o log real da rodada anterior (e o registro dos sinais) so sai do lugar quando esta rodada vai mesmo rodar
[ -f "$LOGF" ] && mv -f "$LOGF" "$LOGF.anterior"
mv -f "$LOGS" "$LOGF"; LOGS="$LOGF"
[ -f "$PK/rito_v384_sinal.txt" ] && mv -f "$PK/rito_v384_sinal.txt" "$PK/rito_v384_sinal.txt.anterior"
# 2. o vigia: se o servidor reaparecer durante o rito, e' encerrado e o fato fica no log'''),
    (r'''\$_.CommandLine -and \$_.CommandLine -match 'Stop-Scheduled[T]ask' -and \$_.CommandLine -match 'IALD Llama' }).Count''',
     r'''\$_.CommandLine -and ((\$_.CommandLine -match 'Stop-Scheduled[T]ask' -and \$_.CommandLine -match 'IALD Llama') -or \$_.CommandLine -match 'stop_iald_llam[a]\.ps1') }).Count'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
b = s.encode("utf-8"); assert b"\r" not in b
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok lancador", len(PAIRS))
C = os.path.join(HERE, "conferir_rito_v384.py"); c = open(C, "rb").read().decode("utf-8")
assert open(C + ".bak_antes_afer8", "rb").read().decode("utf-8") == c
CP = [
    ('''res["servidor_depois_do_rito"] = ("PAROU DEPOIS DE ESCUTAR (o marcador ficou) -- conferir a tarefa" if "escutou e PAROU" in _lt else''',
     '''res["servidor_depois_do_rito"] = ("PAROU DEPOIS DE ESCUTAR (o marcador ficou) -- conferir a tarefa" if "escutou e PAROU" in _lt else
                                  "ESCUTA, MAS HAVIA PARADA DA TAREFA EM CURSO (o marcador ficou) -- conferir a tarefa" if "ha parada da tarefa ainda em curso" in _lt else'''),
    ('''if res["avisos_do_lancador"] and res["servidor_depois_do_rito"].startswith("RELIGADO"):
    res["servidor_depois_do_rito"] = "RELIGADO COM AVISO: " + " | ".join(res["avisos_do_lancador"])''',
     '''_av_rel = [l_ for l_ in res["avisos_do_lancador"] if "AVISO_PID_VELHO" not in l_]   # o PID velho nao e' do religamento (8a afericao)
if _av_rel and res["servidor_depois_do_rito"].startswith("RELIGADO"):
    res["servidor_depois_do_rito"] = "RELIGADO COM AVISO: " + " | ".join(_av_rel)'''),
    ('''res["sinais_desta_rodada"] = (open(_sg, encoding="utf-8", errors="replace").read().splitlines() if os.path.exists(_sg) else [])   # gira a cada rodada (7a afericao)''',
     '''res["sinais_desta_rodada"] = (open(_sg, encoding="utf-8", errors="replace").read().splitlines() if os.path.exists(_sg) else [])   # gira so quando a rodada vai rodar (8a)'''),
]
for old, new in CP:
    k = c.count(old); assert k == 1, (k, old[:100])
    c = c.replace(old, new)
ast.parse(c)
open(C + ".tmp", "wb").write(c.encode("utf-8")); os.replace(C + ".tmp", C); print("ok conferidor", len(CP))
