# -*- coding: utf-8 -*-
"""gerar_pino_das_pedras_v403.py -- escreve pedras_sha16_da_ordem.json (o pino de cada pedra da v403) LENDO o sha16 do arquivo da pedra (v403_kernel\\pedras\\*.lean) e CONFERINDO contra o que o PLANO_v403.md §1 deu (tabela «módulo | sha16 | bytes»).
O arquivo manda; se o plano e o arquivo divergem, ABORTA (nada e' digitado de memoria). Reexecutavel: se o JSON ja existe e e' igual, fica; se difere, aborta.
uso: python -I -B -X utf8 gerar_pino_das_pedras_v403.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PED = os.path.join(os.path.dirname(HERE), "v403_kernel", "pedras")
PLANO = open(os.path.join(HERE, "PLANO_v403.md"), encoding="utf-8").read()
CHAVES = {"caminho": "Caminho", "vida": "Vida", "verdade_adendo": "VerdadeAdendo"}
pino = {}
for k, nome in CHAVES.items():
    b = open(os.path.join(PED, nome + ".lean"), "rb").read()
    h = hashlib.sha256(b).hexdigest()
    m = re.search(r"\|\s*`TGLExt/%s\.lean`\s*\|\s*`([0-9a-f]{16})`\s*\|\s*(\d+)\s*\|" % re.escape(nome), PLANO)
    assert m, ("a tabela do plano nao traz a pedra", nome)
    assert h[:16] == m.group(1) and len(b) == int(m.group(2)), ("o arquivo da pedra DIVERGE do plano", nome, h[:16], m.group(1), len(b), m.group(2))
    pino[k] = h[:16]
out = os.path.join(HERE, "pedras_sha16_da_ordem.json")
novo = json.dumps(pino, ensure_ascii=False)
if os.path.exists(out):
    assert open(out, encoding="utf-8").read().strip() == novo, "pedras_sha16_da_ordem.json ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "w", encoding="utf-8", newline="\n").write(novo + "\n"); assert os.path.getsize(out + ".tmp") > 0; os.replace(out + ".tmp", out)
print(novo)
