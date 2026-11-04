"""Compara duas fotografias da arvore canonical_memory (baseline_f03.py): o que foi ACRESCENTADO, REMOVIDO ou ALTERADO. Somente leitura.
Uso: python diff_f03.py antes.json depois.json [prefixo_esperado_de_novos]"""
import json
import sys
from pathlib import Path

a = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
b = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
esperado = sys.argv[3] if len(sys.argv) > 3 else None
A, B = a["arquivos"], b["arquivos"]
novos = sorted(set(B) - set(A))
removidos = sorted(set(A) - set(B))
alterados = sorted(k for k in set(A) & set(B) if (A[k]["bytes"], A[k].get("sha256"), A[k]["mtime_ns"]) != (B[k]["bytes"], B[k].get("sha256"), B[k]["mtime_ns"]))
fora = [k for k in novos if esperado and not k.replace("\\", "/").startswith(esperado)]
print("antes: %d arquivos | depois: %d arquivos" % (len(A), len(B)))
print("novos: %d | removidos: %d | alterados: %d" % (len(novos), len(removidos), len(alterados)))
print("novos fora do prefixo esperado (%s): %d" % (esperado, len(fora)))
for k in fora[:20]:
    print("   NOVO FORA:", k)
for k in removidos[:20]:
    print("   REMOVIDO:", k)
for k in alterados[:20]:
    print("   ALTERADO:", k, "| sha antes", (A[k].get("sha256") or "-")[:12], "depois", (B[k].get("sha256") or "-")[:12])
print("ACTIVE antes:", a["active"].get("release"), a["active_sha256"][:16], "| depois:", b["active"].get("release"), b["active_sha256"][:16])
print("releases antes %d depois %d; novos releases: %s" % (len(a["releases"]), len(b["releases"]), sorted(set(b["releases"]) - set(a["releases"]))))
mudou = [r for r in a["manifests_sha256"] if a["manifests_sha256"][r] != b["manifests_sha256"].get(r)]
print("manifests de releases anteriores alterados:", mudou)
