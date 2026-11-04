# -*- coding: utf-8 -*-
"""ANOTACAO na rota kernel.fechamento_construir_tudo_programa_02nov (ORDEM_004 secao 4 e ORDEM_005, entrega): resume o app v406, a F0.3 e H1-H4.
Numeros lidos dos artefatos. Grava o seq devolvido em registros_fechamento/anotacao_seq.json."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

PY = r"C:\Python314\python.exe"
W = Path(__file__).resolve().parent
T = Path(r"C:\IALD\TUNEL_CLAUDE_APP")
F03 = Path(r"C:\IALD\Central de Patentes\work\scientific_memory_sync_20261103_v406\RECIBO_PARADA_NO_GATE_v406.json")
rd = lambda p: json.loads(Path(p).read_bytes())
m = rd(W / "BUILDER_MEASUREMENTS.json")
rv = rd(W / "validation/review_final.json")
pk = m["packages"]
h4 = T / "H4_perguntas_agente_PI_D2.md"
n_h4 = len(re.findall(r"(?m)^#### B\d+\.\d+", h4.read_text(encoding="utf-8")))
art = [W / "LICOES_v406.md", W / "validation/review_final.json", W / "install_plan.json", F03, T / "H1_chamado_locaweb.md", T / "H2_iald_ia_br" / "H2_RECIBO.json", T / "H3_zenodo_v406" / "H3_RECIBO.json", h4]
nota = {
    "tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov",
    "titulo": "app v406 construido e aceito (nao instalado), F0.3 parada no gate de escrita, H1 a H4 prontos (03/11/2026)",
    "estatuto": "REAL", "olhou_dados": False,
    "resultado": ("release v406 do app: construida (R3-1, R3-2, janela P2 deslizada com limites/diz/nao_diz mantidos) e aceita por revisor independente na rodada 1 (%d checks PASS, 0 ALTO/MEDIO, 5 BAIXOS); shared %d B, folga minima declarada %d B; haiku55 folga %d tokens; "
                  "NAO instalada (reinicio do filho web e' do operador); F0.3: check = SEALED_ADVANCE_PENDING_SYNC, parada no gate (prepare/activate escrevem em Chatgpt\\); H1 a H4 da ORDEM 005 prontos, nada enviado (%d perguntas D2)"
                  % (len(rv["checks"]), pk["shared"]["prefix_bytes"], m["menor_folga_declarada_bytes"], pk["haiku_expanded"]["remaining_tokens"], n_h4)),
    "nota": "quem constroi nao aprova: a release v406 foi revisada por sonnet-app-v406-revisor; F0.3, H1, H2, H3 e H4 NAO tiveram revisao de terceiro (H2 e H3 conferidos por script e por mim; H4 e' so' perguntas). Achado para a gerencia: o BibTeX de A Ponte no README pinado cita 10.5281/zenodo.20999495 (= Um: Grande Atrator no DataCite); A Ponte = 10.5281/zenodo.20630106. Nada tocou um.py, selo, kernel, gate, cofre nem Chatgpt\\.",
    "proximo_passo": "OK do operador ao reinicio do filho web para instalar a v406 do app (depois verify_installed e torre.py gerar; a gerencia roda custodiar.py executar --versao v406 --publicar); F0.3 pelo caminho A, B ou C; H1 a H4 sao atos do operador",
    "refs": ["app.release.v406", "memoria.cientifica_sync.v406_gate_chatgpt", "app.release.v405"],
    "artefatos": [str(p) for p in art],
}
p = W / "registros_fechamento" / "anotacao_kernel_fechamento_v406.json"
with p.open("xb") as f:
    f.write(json.dumps(nota, ensure_ascii=False, indent=1).encode("utf-8"))
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(p), "--quem", "claude-app-orquestrador"], capture_output=True)
out = r.stdout.decode("utf-8", "replace")
print("rc", r.returncode, " ".join(out.split())[:300], r.stderr.decode("utf-8", "replace")[:300])
seq = re.search(r'"seq":\s*(\d+)', out)
(W / "registros_fechamento" / "anotacao_seq.json").write_text(json.dumps({"seq": int(seq.group(1)) if seq else None}), encoding="utf-8")
