# -*- coding: utf-8 -*-
"""R2.1: MANIFESTO_R2_1.json — sha256 LIDO de cada entregável (candidato, ferramentas, config, patch, testes, scripts,
resultados). Não lista as cópias de teste nem o ensaio (regeráveis) nem as cópias de referência do R2."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

R21 = Path(__file__).resolve().parents[1]
RAIZES = ['candidato_r2_1', 'src_r2_1', 'scripts', 'runs']
SOLTOS = ['CANDIDATO_MANIFESTO_R2_1.json', 'DIFF_R2_R2_1.patch', 'DIFF_R2_R2_1_APPLY_CHECK.json', 'implantar.py', 'reverter.py',
          'implantacao_lib.py', 'implantar_config_producao_r2_1.json', 'TESTES_R2_1.md', 'RESULTADO_R2_1.md',
          'registro_mapa_F9.MEMORIA_ACOM_R2_1.json', 'copia/testes_r2/RESULTADOS_TESTES.json', 'copia/testes_r2/TESTES.md',
          'copia_r2/testes_r2/RESULTADOS_TESTES_parcial.json']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


files = set()
for r in RAIZES:
    files |= {p for p in (R21 / r).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
files |= {R21 / s for s in SOLTOS if (R21 / s).exists()}
out = [{'path': str(p.relative_to(R21)), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(files)]
m = {'titulo': 'R2.1 — conserto ACOM 12/10 — MANIFESTO', 'gerado_em': datetime.now(timezone.utc).isoformat(),
     'gerado_por': 'scripts/gerar_manifesto_r2_1.py (hashes lidos)', 'producao_nao_tocada': True, 'n_arquivos': len(out),
     'arquivos': out}
(R21 / 'MANIFESTO_R2_1.json').write_text(json.dumps(m, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(len(out), sha(R21 / 'MANIFESTO_R2_1.json')[:16])
