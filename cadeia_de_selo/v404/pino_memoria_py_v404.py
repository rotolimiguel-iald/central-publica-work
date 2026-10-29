# -*- coding: utf-8 -*-
"""pino_memoria_py_v404.py -- pina, LENDO do arquivo, o memoria.py (a FILA DA MEMORIA) que o pos-rito da v404 vai usar (pausa do vigia, pinar, verificar). Nada e digitado: o sha256 e' calculado aqui.
O sha16 que a gerencia c1 declarou na ordem (7c4fc5853f41f1d3) entra como [DECLARADO] ao lado e so' vale se for IGUAL ao lido; a --help do programa e' guardada para o pos-rito ler a sintaxe sem adivinhar.
Escreve SO PINO_MEMORIA_PY_v404.json nesta pasta. uso: python -I -B -X utf8 pino_memoria_py_v404.py"""
import datetime, hashlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
MEMD = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
MEMPY = os.path.join(MEMD, "fila", "memoria.py")
DECLARADO = "7c4fc5853f41f1d3"   # [DECLARADO] a ordem da gerencia c1 (26/10/2026); o valor que vale e' o LIDO abaixo
b = open(MEMPY, "rb").read()
h = hashlib.sha256(b).hexdigest()
ajuda = {}
for c in ("pinar", "verificar", "vigiar"):
    r = subprocess.run([sys.executable, "-X", "utf8", MEMPY, c, "--help"], capture_output=True, text=True, encoding="utf-8")
    ajuda[c] = {"rc": r.returncode, "stdout_sha16": hashlib.sha256(r.stdout.encode("utf-8")).hexdigest()[:16], "linhas": len(r.stdout.splitlines())}
out = {"contrato": "PINO_MEMORIA_PY_v404", "path": MEMPY, "sha256": h, "sha16": h[:16], "bytes": len(b), "declarado_pela_gerencia_sha16": DECLARADO, "igual_ao_declarado": h[:16] == DECLARADO,
       "ajuda_dos_subcomandos": ajuda, "lido_em": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
       "uso_no_pos_rito": "MEMORIA_GERENCIA=claude-c1 python memoria.py pinar --motivo \"pos-rito v404\"; a PAUSA_VIGIA.json e' criada ANTES da superficie que escreve o MEMORY.md e removida DEPOIS do pino; depois memoria.py verificar (rc 0)"}
assert out["igual_ao_declarado"], ("o memoria.py mudou desde a ordem da gerencia", h[:16], DECLARADO)
json.dump(out, open(os.path.join(HERE, "PINO_MEMORIA_PY_v404.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("PINO_MEMORIA_PY_v404:", h[:16], "igual ao declarado:", out["igual_ao_declarado"])
