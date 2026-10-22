# -*- coding: utf-8 -*-
"""R2.2: imprime o sha256 (16) dos entregáveis principais, lido do disco, para o RESULTADO. Só lê."""
import hashlib
import json
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
nomes = ['CANDIDATO_MANIFESTO_R2_2.json', 'implantar.py', 'reverter.py', 'implantacao_lib.py',
         'implantar_config_producao_r2_2.json', 'DIFF_R2_1_R2_2.patch', 'DIFF_R2_1_R2_2_APPLY_CHECK.json', 'TESTES_R2_2.md',
         'RUNBOOK_OPERADOR.md', 'runs/s5_ensaio_r2_2.json', 'runs/s5_ensaio_r2_2_rodada1_bug_P8b.json',
         'copia/testes_r2/RESULTADOS_TESTES.json', 'copia_r2_1/testes_r2/RESULTADOS_TESTES_parcial.json',
         'src_r2_2/test_r2_2.py', 'src_r2_2/test_app_r2_2.py']
out = {n: hashlib.sha256((R22 / n).read_bytes()).hexdigest()[:16] for n in nomes}
m = json.loads((R22 / 'CANDIDATO_MANIFESTO_R2_2.json').read_text(encoding='utf-8'))
out['mudancas'] = {Path(x['target']).name: (x['sha256_r2_1'][:16], x['sha256_r2_2'][:16]) for x in m['r2_2_mudancas']}
out['ferramentas'] = {Path(f['arquivo']).name: (f['sha256'][:16], f.get('sha256_citado_ate_r2_1', '')[:16]) for f in m['ferramentas']}
out['ferramentas_implantacao_conferem'] = all(hashlib.sha256(Path(f['arquivo']).read_bytes()).hexdigest() == f['sha256']
                                              for f in m['ferramentas_implantacao'])
chk = json.loads((R22 / 'DIFF_R2_1_R2_2_APPLY_CHECK.json').read_text(encoding='utf-8'))
out['patch'] = {'bytes': chk['patch_bytes'], 'all_equal': chk['all_equal'], 'n_files': len(chk['files'])}
print(json.dumps(out, ensure_ascii=False, indent=1))
