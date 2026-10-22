# -*- coding: utf-8 -*-
"""11a verificacao (estreita, do v11 -> v12; resultado em aferidor11/resultado_aferidor11.json): dois defeitos de REDACAO que tocam o rascunho e um de registro.
- 11.1: «recusada depois da fase 0» -> «a partir da fase 0» (as recusas 13, 14 e 15 sao da propria fase 0);
- 11.2: a 17 da troca do .fase0 pelo log real vem DEPOIS de o log real girar (sem perda: o registro fica no .fase0); a frase «so depois da ultima recusa»
  passa a dizer «das guardas» e a ordem dos giros; o comentario do lancador (:206) corrigido AO LADO;
- 11.4: o afericao10_resultado.json entra nas evidencias do rascunho (a 9 e a 10 obrigatorias).
Backups de BYTES feitos e conferidos aqui."""
import ast, hashlib, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert hashlib.sha256(raw).hexdigest().startswith("cb9ce018585e8ef4"), "o gerador nao e' o verificado na 11a (cb9ce018)"
bak = P + ".bak_antes_afer11_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
PAIRS = [
    ('''e só depois da última recusa o log real da rodada anterior e o registro dos sinais vão para .anterior e o da tentativa toma o lugar do real (se um desses giros falhar, FALHA VISÍVEL e RECUSA — código 17);''',
     '''e só depois da última recusa das guardas o registro dos sinais e o log real da rodada anterior vão para .anterior (nessa ordem) e o da tentativa toma o lugar do real (se um desses giros falhar, FALHA VISÍVEL e RECUSA — código 17);'''),
    ('''o log de uma tentativa recusada depois da fase 0 (códigos 10 a 15 e as 17 dos giros dos sinais e do log, que vêm antes de o log real sair do lugar — os sinais giram primeiro) fica no .fase0,''',
     '''o log de uma tentativa recusada a partir da fase 0 (códigos 10 a 15 e as 17 dos giros: a dos sinais e a do log real vêm antes de o log real sair do lugar, porque os sinais giram primeiro; a da troca do .fase0 pelo log real vem depois, sem perda) fica no .fase0,'''),
    ('''("afericao_9", os.path.join(ESTD, "afericao9_resultado.json")),''',
     '''("afericao_9", os.path.join(ESTD, "afericao9_resultado.json")), ("afericao_10", os.path.join(ESTD, "afericao10_resultado.json")),'''),
    ('''EV_OPC = {"afericao_9"}   # 8a afericao: a 6, a 7 e a 8 obrigatorias''',
     '''EV_OPC = set()   # 11a: todas as afericoes obrigatorias (8a: a 6, a 7 e a 8; 11a: tambem a 9 e a 10)'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:160])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8")
for i in range(40):
    try:
        open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P); break
    except PermissionError:
        time.sleep(0.5)
assert open(P, "rb").read() == b
print("ok gerador", len(PAIRS), hashlib.sha256(b).hexdigest()[:16], "| backup", os.path.basename(bak))
L = os.path.join(HERE, "rito_v384.sh"); lr = open(L, "rb").read()
if not os.path.exists(L + ".bak_antes_afer11"):
    open(L + ".bak_antes_afer11", "wb").write(lr)
assert open(L + ".bak_antes_afer11", "rb").read() == lr
ls = lr.decode("utf-8")
old = "# Os SINAIS giram PRIMEIRO (10a afericao): toda recusa 17 acontece com o log real ainda no lugar, e o registro dela fica no .fase0\n"
new = ("# Os SINAIS giram PRIMEIRO (10a afericao): toda recusa 17 acontece com o log real ainda no lugar, e o registro dela fica no .fase0\n"
       "# [ERRATA AO LADO, 11a: «toda» vale para a 17 dos sinais e a do log real; a da troca do .fase0 pelo log real vem DEPOIS de o log real girar -- sem perda:\n"
       "#  o registro dela fica no .fase0, e a tentativa seguinte o acrescenta ao .fase0.anterior sem tocar o .anterior do log real]\n")
assert ls.count(old) == 1
ls = ls.replace(old, new); lb = ls.encode("utf-8")
open(L + ".tmp", "wb").write(lb); assert os.path.getsize(L + ".tmp") == len(lb); os.replace(L + ".tmp", L); assert open(L, "rb").read() == lb
print("ok lancador (comentario ao lado)")
