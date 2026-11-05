# -*- coding: utf-8 -*-
"""Evidencia irma do estado da custodia da v407 (licao do F3 do parecer r1 da v405: separar custodia EM CURSO de CONCLUIDA). So leitura do plano da G1 e da conferencia final da custodia; grava uma vez.
A ORDEM_006 diz que a custodia da v407 esta PUBLICADA [DECLARADO pela sessao de custodia]; aqui fica o que o plano da G1 lista de fato, sem adjetivo."""
import hashlib
import json
from pathlib import Path

W = Path(__file__).resolve().parent
plano = Path(r"C:\IALD\Central de Patentes\work\custodia_G1\PLANO_v407.json")
conf = Path(r"C:\IALD\Central de Patentes\work\custodia_v407_04nov\CONFERENCIA_FINAL_v407.json")
d = json.loads(plano.read_bytes())
c = json.loads(conf.read_bytes())
estado = {
    "status": "CUSTODIA_V407_PLANO_G1_COMPLETO" if d.get("completo") else "CUSTODIA_V407_PLANO_G1_COM_PENDENTES",
    "plano_g1": {"path": str(plano), "sha256": hashlib.sha256(plano.read_bytes()).hexdigest()},
    "conferencia_final_da_custodia": {"path": str(conf), "sha256": hashlib.sha256(conf.read_bytes()).hexdigest(), "chaves": sorted(c)[:20] if isinstance(c, dict) else None},
    "ordem_006": "C:\\IALD\\TUNEL_CLAUDE_APP\\ORDEM_006_release_v407_do_app.md (sha16 0e832dc6eebc3ad6) declara a custodia v407 PUBLICADA [DECLARADO]",
    "leitura": "O selo, o cofre e o commit do espelho da v407 estao custodiados e conferidos por este pipeline (sources_verified.json: commit pinado = HEAD local = origin/main, remote_checked). "
              "O plano da G1 ainda lista pendentes (E16-E19 e C18-C17C); o C21 (esta release do app) e' o item que depende deste pacote; a troca do servico web e' do operador.",
    "campos_do_plano": {k: d.get(k) for k in ("versao", "corrente", "relacao_espelho", "contagem", "completo", "pendentes", "pendentes_do_operador") if k in d},
}
with (W / "CUSTODIA_v407_ESTADO.json").open("xb") as f:
    f.write(json.dumps(estado, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps({k: estado["campos_do_plano"].get(k) for k in ("versao", "completo", "pendentes", "relacao_espelho")}, ensure_ascii=False))
