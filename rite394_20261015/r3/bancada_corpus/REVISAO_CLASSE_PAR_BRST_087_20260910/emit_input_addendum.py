from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
out = Path(__file__).resolve().parent
base = out.parent
files = [out / "PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md", out / "REGISTRO_REVISAO_CLASSE_PAR_087.json", base / "REVISAO_RELATIVO_QUADRATICO_087_20260910/PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md", base / "REVISAO_RELATIVO_QUADRATICO_087_20260910/REGISTRO_REVISAO_RELATIVO_CE_087.json", base / "COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md"]

def pin(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

def publish(p, data):
    assert p.parent == out and not p.exists()
    tmp = p.with_name(p.name + ".tmp_new")
    with tmp.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == data
    os.replace(tmp, p)
    assert p.read_bytes() == data

before = [pin(p) for p in files]
review = before[2]
report = out / "ADENDO_CONSUMO_REVISAO_N2_087.md"
receipt = out / "REGISTRO_ADENDO_REVISAO_N2_087.json"
text = f'''# Adendo: consumo do parecer independente da entrada N₂087

10/09/2026. /root/selected_geometry_design. [REAL — leitura e custódia documental; não é uma nova demonstração].

Após congelar o parecer da composição da classe par, li integralmente o [parecer específico de Singer sobre N₂](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_RELATIVO_QUADRATICO_087_20260910/PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md>). Ele examina a entrada relativa/CE inteira e não identifica erro material, conservando o contrato de referência e de finitude. Seus bytes medidos nesta emissão: {review['bytes']}; SHA-256 {review['sha256']}.

O parecer confirma em particular a independência das duas classes I₀ν e J₀ν em H⁴ CE sobre Rher, que é a entrada necessária à minha revisão da composição. A autoria e os dois exames permanecem separados: Singer revisou N₂; meu parecer examina a composição da raiz, a conexão entre C₆ e C₅ e o detector da linha par no BV–BRST clássico. Não afirmo que Singer tenha revisto essa composição.

A referência temporal à revisão N₂ ainda separada/pendente no parecer anterior deve ser lida no seu corte de emissão. Este adendo registra agora o consumo efetivo daquele parecer, sem editar qualquer fonte congelada ou ampliar a conclusão matemática. Não se reaprova minha autoria086.

O recibo registra os pins antes/depois dos dois pareceres, seus recibos e da fonte N₂. Zero execução matemática, CAS, Lean, um.py ou recaptura canônica. QME, admissibilidade causal e operador quântico renormalizado continuam fora do alcance.
'''
publish(report, text.encode("utf-8"))
after = [pin(p) for p in files]
assert before == after
data = {"status": "PASS_DOCUMENTARY", "created_utc": datetime.now(timezone.utc).isoformat(), "scope": "Consumption of newly published independent N2 review; no extension of mathematical review scope", "before": before, "after": after, "source_pins_unchanged": True, "report": pin(report), "helper": pin(Path(__file__).resolve()), "execution_counts": {"mathematical": 0, "CAS": 0, "Lean": 0, "um": 0, "canonical_recapture": 0}}
publish(receipt, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status": data["status"], "files_unchanged": len(files), "report": pin(report), "receipt": pin(receipt)}, ensure_ascii=False, indent=2))
