# -*- coding: utf-8 -*-
"""R2.2: MANIFESTO_R2_2.json — sha256 LIDO de cada entregável (candidato, ferramentas, config, patch, testes, scripts,
resultados, runbook). Não lista as cópias de teste nem o ensaio (regeráveis) nem a cópia de referência da R2.1."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
RAIZES = ['candidato_r2_2', 'src_r2_2', 'scripts', 'runs']
SOLTOS = ['CANDIDATO_MANIFESTO_R2_2.json', 'DIFF_R2_1_R2_2.patch', 'DIFF_R2_1_R2_2_APPLY_CHECK.json', 'implantar.py',
          'reverter.py', 'implantacao_lib.py', 'implantar_config_producao_r2_2.json', 'TESTES_R2_2.md', 'RESULTADO_R2_2.md',
          'RUNBOOK_OPERADOR.md', 'registro_mapa_F9.MEMORIA_ACOM_R2_2.json', 'copia/testes_r2/RESULTADOS_TESTES.json',
          'copia/testes_r2/TESTES.md', 'copia_r2_1/testes_r2/RESULTADOS_TESTES_parcial.json']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


files = set()
for r in RAIZES:
    files |= {p for p in (R22 / r).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
files |= {R22 / s for s in SOLTOS if (R22 / s).exists()}
out = [{'path': str(p.relative_to(R22)), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(files)]
m = {'titulo': 'R2.2 — conserto ACOM 12/10 — MANIFESTO', 'gerado_em': datetime.now(timezone.utc).isoformat(),
     'gerado_por': 'scripts/gerar_manifesto_r2_2.py (hashes lidos)', 'producao_nao_tocada': True, 'n_arquivos': len(out),
     'nota': 'candidato_r2_2/C/IALD/projetos_pyhton/IALD/iald_web_server.py carrega a chave de producao (o que se instala); '
             'nenhum outro arquivo da pasta a contem (conferido por script)',
     'arquivos': out}
(R22 / 'MANIFESTO_R2_2.json').write_text(json.dumps(m, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(len(out), sha(R22 / 'MANIFESTO_R2_2.json')[:16])
