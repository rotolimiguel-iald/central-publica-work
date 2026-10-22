# -*- coding: utf-8 -*-
"""R2.2, passo 2: escreve implantar_config_producao_r2_2.json a partir da config R2.1 (só muda candidato, manifesto,
pasta de recibos e recibos anteriores). Caminhos montados por pathlib (sem barra invertida em string). NÃO executa nada."""
import json
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
WORK = R22.parent
src = json.loads((WORK / '9_R2_1' / 'implantar_config_producao_r2_1.json').read_text(encoding='utf-8'))
cfg = dict(src)
cfg['_comentario'] = ('Configuração de PRODUÇÃO do implantar.py — R2.2 de 13/10 (conserto ACOM 12/10; revisão independente '
                      'R2.1). Ato do operador: siga o RUNBOOK_OPERADOR.md desta pasta; rode primeiro com --dry-run (só lê: '
                      'trava de recibos, CAS dos alvos, banco, a Tarefa Agendada e os processos). Raízes = identidade '
                      '(produção). Recibos com carimbo em recibos_producao_r2_2; a trava também lê os recibos da R2.1 e '
                      'do R2 (recibos_dirs_anteriores).')
cfg['candidato_root'] = str(R22 / 'candidato_r2_2' / 'C')
cfg['manifesto_candidato'] = str(R22 / 'CANDIDATO_MANIFESTO_R2_2.json')
cfg['recibos_dir'] = str(R22 / 'recibos_producao_r2_2')
cfg['recibos_dirs_anteriores'] = [str(WORK / '9_R2_1' / 'recibos_producao_r2_1'),
                                  str(WORK / '4_INTEGRACAO' / 'recibos_producao_r2')]
assert cfg['recibos_dirs_anteriores'][1] in src['recibos_dirs_anteriores']
order = ['_comentario', 'candidato_root', 'manifesto_candidato', 'raizes', 'app_root_processos', 'gerir_processos',
         'exigir_app_parado', 'arquivo_D', 'keep_backups', 'recibos_dir', 'recibos_dirs_anteriores', 'superficies',
         'memory_md', 'ordem_operador', 'bridge_v2', 'aplicar_blocos', 'processos_backend', 'tarefa_agendada', 'porta',
         'silencio_s', 'esperar_parada_s', 'esperar_inicio_s']
assert set(order) == set(cfg), set(cfg) ^ set(order)
out = {k: cfg[k] for k in order}
for k in out:
    if k not in ('_comentario', 'candidato_root', 'manifesto_candidato', 'recibos_dir', 'recibos_dirs_anteriores'):
        assert out[k] == src[k], k
(R22 / 'implantar_config_producao_r2_2.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: out[k] for k in ('candidato_root', 'manifesto_candidato', 'recibos_dir', 'recibos_dirs_anteriores')},
                 ensure_ascii=False, indent=1))
