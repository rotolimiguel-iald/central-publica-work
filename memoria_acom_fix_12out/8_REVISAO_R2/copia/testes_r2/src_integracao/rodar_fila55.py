# -*- coding: utf-8 -*-
"""FILA 55 (origem, 10/10) contra o candidato — com INJEÇÃO DE CONFIGURAÇÃO, não de lógica.

11 casos de test_coordination/test_transport resolvem a memória canônica ativa da fila
(BASE/state/canonical_memory: ponteiro ACTIVE.json -> releases/<epoch>, 140 MB, snapshot_root ABSOLUTO em
produção). Como fez a auditoria de 12/10 (AUDITORIA_F9_MEMORIA_ACOM_C1.md, seção FILA), apontamos as constantes
ACTIVE/RELEASES do módulo para o estado instalado, que o próprio código abre só para leitura (mode=ro); a guarda
da auditoria registra READ_OUTSIDE/SQLITE_RO_OUTSIDE e não bloqueia. Nada em produção é escrito: o Runtime dos
testes nasce num diretório temporário. Dependência de ambiente R11 da especificação, documentada aqui.
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from iald_orchestrator import canonical_memory  # noqa: E402

PROD_STATE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\canonical_memory')
canonical_memory.ACTIVE = PROD_STATE / 'ACTIVE.json'
canonical_memory.RELEASES = PROD_STATE / 'releases'

MODULES = ['test_coordination', 'test_optional_work', 'test_transport', 'test_maximum_coordination',
           'test_request_controls', 'test_provider_memory.AllAdapterMemoryTests', 'test_canonical_memory']

if __name__ == '__main__':
    print('[rodar_fila55] canonical_memory.ACTIVE =', canonical_memory.ACTIVE, file=sys.stderr)
    suite = unittest.defaultTestLoader.loadTestsFromNames(MODULES)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
