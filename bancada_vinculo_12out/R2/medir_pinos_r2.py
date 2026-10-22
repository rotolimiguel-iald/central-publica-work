# -*- coding: utf-8 -*-
"""medir_pinos_r2.py (R2, 13/10/2026) -- escreve R2\\PINOS_R2.json: todo hash LIDO do artefato por script (nunca digitado): os entregaveis R2,
as copias dos originais R1 (conferidas iguais aos originais), os recibos do sandbox em raiz curta, o estado (so lido) da producao, do Nos e
do livro de eventos, e a auditoria que motivou a R2. uso: medir_pinos_r2.py <raiz curta do sandbox>"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, datetime
from pathlib import Path
AQUI = Path(__file__).resolve().parent
R1 = AQUI.parent
RAIZ = Path(sys.argv[1]).resolve()
AUD = Path(r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\aud_vinculo_bancada")


def pin(p):
    p = Path(p)
    if not p.is_file():
        return dict(path=str(p), AUSENTE=True)
    b = p.read_bytes()
    return dict(path=str(p), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))


out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R2 (13/10/2026)", nota="hashes lidos do artefato por este script; [REAL]",
           entregaveis_R2={}, originais_R1={}, bateria_R1_pinada_pela_R2={}, sandbox={}, producao_so_lida={}, nos_so_lido={}, quadro_so_lido={}, auditoria={})
for n in ("sincronizar_bancada.py", "BATERIA_VINCULO.json", "gerar_bateria.py", "gerar_canais_mcp.py", "montar_sandbox.py", "controles_negativos_r2.py", "rodar_sandbox_r2.sh",
          "CONTROLES_NEGATIVOS_R2.json", "DIFF_R1_R2.patch", "RESULTADO_R2.md", "REMISSOES_PLANO.md", "medir_pinos_r2.py"):
    out["entregaveis_R2"][n] = pin(AQUI / n)
for p in sorted((AQUI / "originais_R1").rglob("*")):
    if p.is_file():
        rel = p.relative_to(AQUI / "originais_R1")
        d = pin(p)
        o = pin(R1 / rel)
        d["igual_ao_original_R1"] = d.get("sha256") == o.get("sha256")
        out["originais_R1"][str(rel)] = d
for p in sorted((R1 / "bateria").glob("*.py")):
    out["bateria_R1_pinada_pela_R2"][p.name] = pin(p)
sb = RAIZ / "SANDBOX_MANIFEST_R2.json"
out["sandbox"]["SANDBOX_MANIFEST_R2.json"] = pin(sb)
for sub in ("1a", "1b", "2"):
    for p in sorted((RAIZ / "s" / sub).glob("*.json")):
        out["sandbox"]["s/%s/%s" % (sub, p.name)] = pin(p)
    for p in sorted((RAIZ / "s" / sub / "recibos").glob("*.json")):
        out["sandbox"]["s/%s/recibos/%s" % (sub, p.name)] = pin(p)
for n in ("canonical_contracts.json", "CONTRATO_CANONICO_B3.md"):
    out["sandbox"]["b2/" + n] = pin(RAIZ / "b2" / n)
for p in sorted((RAIZ / "b2").glob("canonical_contracts.json.bak_*")):
    out["sandbox"]["b2/" + p.name] = pin(p)
for p in sorted((RAIZ / "b2" / "estado" / "sincronizacao").glob("*.json")):
    out["sandbox"]["b2/estado/sincronizacao/" + p.name] = pin(p)
for n in ("um.py", "um_absoluto_selo.json"):
    out["sandbox"]["nos_v392/" + n] = pin(RAIZ / "nos_v392" / n)
for n in ("KERNEL_RECIBO_v392_SINTETICO_VALIDO.json", "eventos_sandbox.jsonl"):
    out["sandbox"]["fx/" + n] = pin(RAIZ / "fx" / n)
for p in sorted((RAIZ / "canais").glob("*")):
    out["sandbox"]["canais/" + p.name] = pin(p)
PROD = Path(r"C:\IALD\Bancada_Um")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
for n in ("canonical_contracts.json", "bancada/canonical.py", "CONTRATO_CANONICO_B2.md", "um_bancada.py", "mcp_um.py"):
    out["producao_so_lida"][n] = pin(PROD / n)
for n in ("um.py", "um_absoluto_selo.json", "um_absoluto.json"):
    out["nos_so_lido"][n] = pin(NOS / n)
out["quadro_so_lido"]["eventos.jsonl"] = pin(Path(r"C:\IALD\PROGRAMA_IALD\eventos.jsonl"))
out["quadro_so_lido"]["PLANO_V392.md"] = pin(Path(r"C:\IALD\PROGRAMA_IALD\exame_12out\J_SINTESE\PLANO_V392.md"))
out["auditoria"]["AUDITORIA_VINCULO_BANCADA_C1.md"] = pin(AUD / "AUDITORIA_VINCULO_BANCADA_C1.md")
out["auditoria"]["ATAQUES.json"] = pin(AUD / "ataques" / "ATAQUES.json")
out["auditoria"]["ATAQUES2.json"] = pin(AUD / "ataques" / "ATAQUES2.json")
out["auditoria"]["A2_CAMINHOS.json"] = pin(AUD / "ataques" / "A2_CAMINHOS.json")
out["verbatim_operador_12out"] = pin(R1.parent / "cunhagens_12out" / "OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt")
s = json.dumps(out, ensure_ascii=False, indent=1)
(AQUI / "PINOS_R2.json").write_text(s, encoding="utf-8")
print("PINOS_R2.json", hashlib.sha256(s.encode("utf-8")).hexdigest()[:16], "entradas:", sum(len(v) for v in out.values() if isinstance(v, dict)))
