# -*- coding: utf-8 -*-
"""8a afericao, complemento (8N0, lido do veredicto do verificador): com o MD gravado primeiro e o JSON por ultimo, uma falha NO JSON deixaria um MD orfao, e a
nova tentativa seria recusada pelo MD (o campo gerado muda a cada segundo). Agora: MD que existe SEM o JSON (a autoridade) e' de tentativa interrompida -> vai
para o lado (.incompleto_<data>), nunca e' apagado; com o JSON presente e diferente, recusa como antes. E a mensagem do JSON ja existente deixa de mandar
«gere um V1.x» (o gerador so grava V1): o congelado nao se sobrescreve; uma versao nova e' ato da gerencia com gerador novo. Backup de BYTES aqui."""
import ast, hashlib, os, time
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert hashlib.sha256(raw).hexdigest().startswith("ff530b8a9aa8eb2f"), "o gerador nao e' o da 8a (ff530b8a)"
bak = P + ".bak_antes_afer8b_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
PAIRS = [
    ('''    raise SystemExit("RECUSO: %s ja existe com outro conteudo (o congelado nao se sobrescreve; gere um V1.x)" % PJSON)''',
     '''    raise SystemExit("RECUSO: %s ja existe com outro conteudo (o congelado nao se sobrescreve; uma versao nova e' ato da gerencia com gerador novo)" % PJSON)'''),
    ('''if os.path.exists(PMD) and open(PMD, "rb").read() != md:
    raise SystemExit("RECUSO: %s ja existe com outro conteudo" % PMD)''',
     '''if os.path.exists(PMD) and open(PMD, "rb").read() != md:
    if os.path.exists(PJSON):
        raise SystemExit("RECUSO: %s ja existe com outro conteudo" % PMD)
    _orf = PMD + ".incompleto_" + time.strftime("%Y%m%d_%H%M%S")   # MD sem o JSON = tentativa interrompida: vai para o lado, nunca e' apagado (8a afericao)
    os.replace(PMD, _orf); print("AVISO: MD orfao de tentativa interrompida (sem o JSON) movido para", os.path.basename(_orf))'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8")
for i in range(40):
    try:
        open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P); break
    except PermissionError:
        time.sleep(0.5)
assert open(P, "rb").read() == b
print("ok", len(PAIRS), hashlib.sha256(b).hexdigest()[:16])
