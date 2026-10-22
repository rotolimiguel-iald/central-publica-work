# -*- coding: utf-8 -*-
"""Congela o pre-registro: grava FREEZE.json com sha256 e tamanho de PREREGISTRO.json e PREREGISTRO.md, a hora UTC
e os hashes de todos os demais arquivos da pasta. Antes, exige a verificacao de integridade (verificar_preregistro.py,
exit 0) e a impressao digital do tgl_kernel igual antes e depois. Recusa sobrescrever. Grava so nesta pasta."""
import datetime, hashlib, json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(AQUI, "FREEZE.json")


def falha(m):
    raise SystemExit("FALHA VISIVEL: " + m)


def h(p):
    b = open(p, "rb").read()
    return len(b), hashlib.sha256(b).hexdigest()


if os.path.exists(ALVO):
    falha("FREEZE.json ja existe; nada se altera depois do FREEZE")
r = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(AQUI, "verificar_preregistro.py")], capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0 or "VERIFICACAO_DE_INTEGRIDADE_PASSOU" not in r.stdout:
    falha("verificacao de integridade nao passou: " + r.stdout[-400:] + r.stderr[-400:])
a = json.load(open(os.path.join(AQUI, "IMPRESSAO_DIGITAL_KERNEL_ANTES.json"), encoding="utf-8"))
d = json.load(open(os.path.join(AQUI, "IMPRESSAO_DIGITAL_KERNEL_DEPOIS.json"), encoding="utf-8"))
chaves = ("n_arquivos", "bytes_total", "sha256_metadados", "n_lean_fora_lake", "sha256_conteudo_lean")
igual = all(a[k] == d[k] for k in chaves)
if not igual:
    falha("impressao digital do tgl_kernel mudou")
nj, hj = h(os.path.join(AQUI, "PREREGISTRO.json"))
nm, hm = h(os.path.join(AQUI, "PREREGISTRO.md"))
outros = {}
for dp, dns, fns in os.walk(AQUI):
    dns.sort()
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, AQUI).replace("\\", "/")
        if rel in ("FREEZE.json", "PREREGISTRO.json", "PREREGISTRO.md") or rel.endswith(".tmp") or "__pycache__" in rel:
            continue
        n, s = h(p)
        outros[rel] = [n, s]
F = {
 "unidade": "F1.FREQUENCIA (trilha POSTO)", "gerencia": "c1", "autor": "pré-registrador (subagente)",
 "congelado_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "PREREGISTRO.json": {"bytes": nj, "sha256": hj},
 "PREREGISTRO.md": {"bytes": nm, "sha256": hm},
 "antes_de_qualquer_ensaio": True, "testes_rodados_pelo_pre_registrador": 0,
 "verificacao_de_integridade": r.stdout.strip().splitlines()[-1].split()[0] + " (verificar_preregistro.py)",
 "tgl_kernel_impressao_digital": {"antes": [a["sha256_metadados"][:16], a["sha256_conteudo_lean"][:16]], "depois": [d["sha256_metadados"][:16], d["sha256_conteudo_lean"][:16]], "igual": igual},
 "demais_arquivos_da_pasta": outros,
 "regra": "nada nesta pasta muda depois deste FREEZE; mudança só por pré-registro aditivo novo, com razão, preservando este",
}
txt = json.dumps(F, ensure_ascii=False, indent=1) + "\n"
b = txt.encode("utf-8")
tmp = ALVO + ".tmp"
open(tmp, "wb").write(b)
if open(tmp, "rb").read() != b:
    falha("temporario nao confere")
os.replace(tmp, ALVO)
if open(ALVO, "rb").read() != b:
    falha("gravado nao confere")
print(txt)
