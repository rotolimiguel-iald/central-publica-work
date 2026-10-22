# -*- coding: utf-8 -*-
"""Monta o harness das suítes a partir do CANDIDATO (4_INTEGRACAO/candidato), das suítes da origem
(iald_memoria_acom_20261010) e dos testes novos das três frentes. Toda cópia que vem do candidato é
conferida por sha256 contra CANDIDATO_MANIFESTO.json: a suíte testa exatamente os bytes que serão instalados.
A produção é lida (módulos de apoio e superfícies D5), nunca escrita.

Layout (cada teste encontra o código onde já o procurava):
  suite/core/iald_memory/*            lib v2 do candidato (6 módulos)
  suite/sessions/                      session_memory.py (cand.), session_hook.py (orig.), SESSOES 17 + FILTROS novos (24)
  suite/app/                           iald_app_memory.py + iald_web_server.py (cand.), 6 apoios (prod.), APP 31 (HB reescrita) + app_filters 9
  suite/queue/iald_orchestrator/       pacote instalado (prod.) com policy.py/operational_memory.py do cand.; FILA 55 + filtros 5
  suite/blocos/test_blocks.py          ROOT = testes/ (aplicar_blocos.py, SESSION_BRIDGE_v2.md, blocos/copias, originais/...)
  suite/integracao/test_integracao.py  testes novos da integração (ponta a ponta N=300, migração 3 contextos, merges)
  hb/tests/, hb/copia/                 suítes NOVA (12) e STUB (3) da frente HEARTBEAT (hb_fixture lê hb/copia/...)
  nucleo/copia/MEMORIA_IALD, nucleo/tests  CORE 20 + test_store_v2 34 (NUCLEO = tests.parent)
"""
from __future__ import annotations
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent          # 4_INTEGRACAO/testes
INT = HERE.parent                                # 4_INTEGRACAO
WORK = INT.parent                                # memoria_acom_fix_12out
CAND = INT / 'candidato' / 'C'
ORIG = INT / 'originais' / 'C'
ORIGEM = Path(r'C:\IALD\Central de Patentes\work\iald_memoria_acom_20261010')
APP_PROD = Path(r'C:\IALD\projetos_pyhton\IALD')
QUEUE_PROD = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator')
NUCLEO = WORK / '1_NUCLEO'
HB = WORK / '2_HEARTBEAT'
FILT = WORK / '3_FILTROS'
SUITE = HERE / 'suite'
SUPERFICIES = {
    'CLAUDE_global.md': r'C:\Users\rotol\.claude\CLAUDE.md',
    'AGENTS.md': r'C:\Users\rotol\.codex\AGENTS.md',
    'CLAUDE_nativa.md': r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md',
    'README.md': r'C:\IALD\PROGRAMA_IALD\README.md',
    'COORDINATOR.md': r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\COORDINATOR.md',
    'MEMORY.md': r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md',
}
FILA55 = ['test_coordination', 'test_optional_work', 'test_transport', 'test_maximum_coordination',
          'test_request_controls', 'test_provider_memory.AllAdapterMemoryTests', 'test_canonical_memory']


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def put(src, dst, manifest, role, expect=None):
    src, dst = Path(src), Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if expect and digest != expect:
        raise RuntimeError('sha divergente do manifesto do candidato: %s' % src)
    tmp = dst.with_name(dst.name + '.tmp_suite')
    tmp.write_bytes(data)
    if tmp.read_bytes() != data:
        raise RuntimeError('cópia divergente: ' + str(dst))
    os.replace(tmp, dst)
    manifest.append({'role': role, 'source': str(src), 'target': str(dst), 'sha256': digest, 'bytes': len(data)})


def main():
    cand_manifest = json.loads((INT / 'CANDIDATO_MANIFESTO.json').read_text(encoding='utf-8'))
    cand_sha = {Path(a['target']).as_posix().lower(): a['sha256'] for a in cand_manifest['arquivos']}

    def cand(path_c):
        """path_c = caminho de produção; devolve (origem no candidato, sha esperado)."""
        p = Path(path_c)
        return CAND / Path(*p.parts[1:]), cand_sha[p.as_posix().lower()]

    manifest = []
    # ---- core (lib v2 do candidato) ----
    for name in ('__init__.py', 'store.py', 'journal.py', 'snapshots.py', 'migrate.py', 'guard.py'):
        src, exp = cand(r'C:\IALD\MEMORIA_IALD\lib\iald_memory\\' + name)
        put(src, SUITE / 'core' / 'iald_memory' / name, manifest, 'candidato', exp)
    # ---- sessions ----
    src, exp = cand(r'C:\IALD\MEMORIA_IALD\session_memory.py')
    put(src, SUITE / 'sessions' / 'session_memory.py', manifest, 'candidato', exp)
    put(ORIG / 'IALD/MEMORIA_IALD/session_hook.py', SUITE / 'sessions' / 'session_hook.py', manifest, 'original')
    for name in ('test_sessions.py', 'test_hooks.py'):
        put(ORIGEM / 'sessions' / name, SUITE / 'sessions' / name, manifest, 'teste_origem')
    for name in ('test_filters.py', 'test_guard.py'):
        put(FILT / 'suite' / 'sessions' / name, SUITE / 'sessions' / name, manifest, 'teste_frente_3')
    # ---- app ----
    for prod_name in ('iald_app_memory.py', 'iald_web_server.py'):
        src, exp = cand(str(APP_PROD / prod_name))
        put(src, SUITE / 'app' / prod_name, manifest, 'candidato', exp)
    for name in ('iald_app_providers.py', 'iald_auto_router.py', 'iald_task_bridge.py',
                 'iald_motores.py', 'iald_memoria_operador.py', 'iald_jev_control.py'):
        put(APP_PROD / name, SUITE / 'app' / name, manifest, 'apoio_instalado')
    put(HB / 'tests' / 'app' / 'test_app_memory.py', SUITE / 'app' / 'test_app_memory.py', manifest, 'teste_origem_reescrito_frente_2')
    put(FILT / 'suite' / 'app' / 'test_app_filters.py', SUITE / 'app' / 'test_app_filters.py', manifest, 'teste_frente_3')
    # ---- queue ----
    queue = SUITE / 'queue'
    for entry in sorted(QUEUE_PROD.iterdir()):
        if entry.suffix == '.py' and '.bak_' not in entry.name:
            put(entry, queue / 'iald_orchestrator' / entry.name, manifest, 'apoio_instalado')
    for prod_name in ('policy.py', 'operational_memory.py'):
        src, exp = cand(str(QUEUE_PROD / prod_name))
        put(src, queue / 'iald_orchestrator' / prod_name, manifest, 'candidato', exp)
    for entry in sorted((ORIGEM / 'queue').iterdir()):
        if entry.is_file() and '.bak_' not in entry.name and (
                (entry.name.startswith('test_') and entry.suffix == '.py') or entry.name in ('transport_cli.py',)):
            put(entry, queue / entry.name, manifest, 'teste_origem')
        # fixtures que o Runtime lê ao lado do pacote (BASE/provenance.json etc.), como na validação da origem
        if entry.is_file() and entry.name in ('provenance.json', 'coordinator.json', 'transport.json', 'SOURCE_MANIFEST.json'):
            put(entry, queue / entry.name, manifest, 'fixture_origem')
    put(FILT / 'suite' / 'queue' / 'test_filters_queue.py', queue / 'test_filters_queue.py', manifest, 'teste_frente_3')
    # A FILA 55 (11 casos de test_coordination/test_transport) resolve a memória canônica ativa da fila por caminho
    # ABSOLUTO (snapshot_root fixado no manifesto): uma cópia não resolve. Como a auditoria de 12/10, o runner
    # rodar_fila55.py injeta CONFIGURAÇÃO (ACTIVE/RELEASES -> estado instalado, lido só em mode=ro) [R11].
    put(HERE / 'src_integracao' / 'rodar_fila55.py', queue / 'rodar_fila55.py', manifest, 'runner_integracao')
    # ---- blocos (ROOT = testes/) ----
    put(FILT / 'suite' / 'blocos' / 'test_blocks.py', SUITE / 'blocos' / 'test_blocks.py', manifest, 'teste_frente_3')
    put(INT / 'ferramentas' / 'aplicar_blocos.py', HERE / 'aplicar_blocos.py', manifest, 'ferramenta')
    put(INT / 'ferramentas' / 'SESSION_BRIDGE_v2.md', HERE / 'SESSION_BRIDGE_v2.md', manifest, 'ferramenta')
    put(ORIG / 'IALD/MEMORIA_IALD/SESSION_BRIDGE.md', HERE / 'originais' / 'C' / 'IALD' / 'MEMORIA_IALD' / 'SESSION_BRIDGE.md', manifest, 'original')
    for name, prod in SUPERFICIES.items():
        put(prod, HERE / 'blocos' / 'copias' / name, manifest, 'superficie_D5_copia_de_leitura')
    # ---- heartbeat (frente 2) ----
    hb = HERE / 'hb'
    for name in ('hb_fixture.py', 'test_heartbeat_v2.py', 'test_heartbeat_stub_server.py'):
        put(HB / 'tests' / name, hb / 'tests' / name, manifest, 'teste_frente_2')
    for name in ('__init__.py', 'store.py', 'journal.py', 'snapshots.py', 'migrate.py', 'guard.py'):
        src, exp = cand(r'C:\IALD\MEMORIA_IALD\lib\iald_memory\\' + name)
        put(src, hb / 'tests' / 'core' / 'iald_memory' / name, manifest, 'candidato', exp)
    src, exp = cand(str(APP_PROD / 'iald_app_memory.py'))
    put(src, hb / 'tests' / 'app' / 'iald_app_memory.py', manifest, 'candidato', exp)
    src, exp = cand(str(APP_PROD / 'iald_web_server.py'))
    put(src, hb / 'copia' / 'projetos_pyhton' / 'IALD' / 'iald_web_server.py', manifest, 'candidato', exp)
    (hb / 'tests' / 'tmp').mkdir(parents=True, exist_ok=True)   # as suítes da frente 2 criam temporários em tests/tmp
    # ---- núcleo (frente 1): NUCLEO = tests.parent ----
    nucleo = HERE / 'nucleo'
    for rel in ('CORE.md', 'migrar_para_delta.py', 'mover_backups_antigos.py'):
        src, exp = cand(r'C:\IALD\MEMORIA_IALD\\' + rel)
        put(src, nucleo / 'copia' / 'MEMORIA_IALD' / rel, manifest, 'candidato', exp)
    for name in ('__init__.py', 'store.py', 'journal.py', 'snapshots.py', 'migrate.py', 'guard.py'):
        src, exp = cand(r'C:\IALD\MEMORIA_IALD\lib\iald_memory\\' + name)
        put(src, nucleo / 'copia' / 'MEMORIA_IALD' / 'lib' / 'iald_memory' / name, manifest, 'candidato', exp)
    for name in ('test_store.py', 'test_store_v2.py', 'store_v1_frozen.py', 'store_v1_frozen.sha256'):
        put(NUCLEO / 'tests' / name, nucleo / 'tests' / name, manifest, 'teste_frente_1' if name.startswith('test_') else 'fixture_frente_1')
    (nucleo / 'evidencias').mkdir(exist_ok=True)
    # ---- integração (novos) ----
    put(HERE / 'src_integracao' / 'test_integracao.py', SUITE / 'integracao' / 'test_integracao.py', manifest, 'teste_integracao')
    put(NUCLEO / 'tests' / 'store_v1_frozen.py', SUITE / 'integracao' / 'store_v1_frozen.py', manifest, 'fixture_frente_1')
    (SUITE / '__init__.py').touch(exist_ok=True)
    # conferência final: todo 'candidato' na suíte é byte-igual ao candidato
    for item in manifest:
        if item['role'] == 'candidato':
            assert sha256_file(item['target']) == item['sha256'] == sha256_file(item['source']), item
    out = {'at': datetime.now(timezone.utc).isoformat(), 'fila55_modulos': FILA55, 'files': manifest}
    (HERE / 'SUITE_MANIFEST.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'files': len(manifest), 'candidato': sum(i['role'] == 'candidato' for i in manifest)}))


if __name__ == '__main__':
    main()
