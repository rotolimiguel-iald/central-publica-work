# -*- coding: utf-8 -*-
"""medir_pinos_r3_3.py (R3.3, 13/10/2026) -- mede POR SCRIPT o sha256 do que a R3.3 cita (nunca de memoria) e grava R3_3/PINOS_R3_3.json.
So le fora de R3_3. Confere a base R3.2 (a408d49292f55008 etc.) e as fontes pinadas na bateria contra o disco.
uso: python -I -B -X utf8 medir_pinos_r3_3.py"""
import sys
sys.dont_write_bytecode = True
import datetime, hashlib, json
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
V = AQUI.parent
R32 = V / "R3_2"
AUD = Path("C:/IALD/PROGRAMA_IALD/auditorias/F0.6")
BASE_ESPERADA = {"sincronizar_bancada.py": "a408d49292f55008"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


nomes_r33 = ["sincronizar_bancada.py", "montar_sandbox.py", "controles_negativos_r3_3.py", "CONTROLES_NEGATIVOS_R3_3.json", "CRITERIOS_V392.json",
             "DIFF_R3_2_R3_3.patch", "VERIFICACAO_DIFF_R3_3.json", "ERRATA_R3_3.md", "RESULTADO_R3_3.md", "registro_mapa_F0.6_R3_3.json",
             "_construcao/medir_pinos_r3_3.py", "_construcao/gerar_diff_r3_3.py", "_construcao/controles_stdout_rodada1.txt"]
entradas = []
for n in nomes_r33:
    p = AQUI / n
    entradas.append(dict(rotulo="R3.3: " + n, path=str(p), existe=p.is_file(), sha256=(sha(p) if p.is_file() else None)))
base = []
for n in ("sincronizar_bancada.py", "montar_sandbox.py", "controles_negativos_r3_2.py", "CONTROLES_NEGATIVOS_R3_2.json", "RESULTADO_R3_2.md", "PINOS_R3_2.json"):
    p = R32 / n
    base.append(dict(rotulo="R3.2 (base, registro): " + n, path=str(p), sha256=sha(p)))
aud = []
for p in (AUD / "AUDITORIA_F0_6_C1_a70d70d5.md", AUD / "art_a70d70d5" / "AUDITORIA_VINCULO_R3_2_C1.md", AUD / "art_a70d70d5" / "ATAQUES_NOVOS_R3_2_AUDITOR.json",
          AUD / "art_a70d70d5" / "ataques_novos_r3_2.py"):
    aud.append(dict(rotulo="reauditoria da R3.2: " + p.name, path=str(p), sha256=sha(p)))
conf = {k: dict(esperado=v, medido=sha(R32 / k)[:16], confere=sha(R32 / k).startswith(v)) for k, v in BASE_ESPERADA.items()}
out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.3 (13/10/2026)", base_conferida=conf, entradas=entradas, base_r3_2=base, auditoria=aud,
           nota="sha256 medidos por script; nada de memoria; o RESULTADO e o registro do mapa podem nao existir quando o medidor roda cedo")
(AQUI / "PINOS_R3_3.json").write_bytes(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps(conf), sum(1 for e in entradas if e["existe"]), "de", len(entradas))
