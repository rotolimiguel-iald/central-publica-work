# -*- coding: utf-8 -*-
"""INTEGRAÇÃO — conserto ACOM 12/10: monta o CANDIDATO único a partir das três frentes.

Escreve só em 4_INTEGRACAO. Lê (nunca escreve) a produção para congelar os ORIGINAIS por bytes.
Toda cópia é conferida por sha256 contra o manifesto da frente de origem (hash lido do artefato,
nunca de memória). Dois arquivos recebem merge a três vias (base = original instalado):
  - lib/iald_memory/__init__.py   NUCLEO (+SchemaMigrationRequired) x FILTROS (+guard, ConfidentialContent)
  - projetos_pyhton/IALD/iald_app_memory.py   HEARTBEAT (+record_measurement) x FILTROS (guard D4)
    + 1 acréscimo do integrador: o texto da medida passa pelo guard antes de entrar no banco.
Saída: candidato/ (árvore C/...), originais/ (árvore C/...), merge/ (evidências) e CANDIDATO_MANIFESTO.json.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
NUCLEO = WORK / '1_NUCLEO'
HB = WORK / '2_HEARTBEAT'
FILT = WORK / '3_FILTROS'
CAND = HERE / 'candidato'
ORIG = HERE / 'originais'
MERGE = HERE / 'merge'

MEM = Path(r'C:\IALD\MEMORIA_IALD')
APP = Path(r'C:\IALD\projetos_pyhton\IALD')
FILA = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator')

INIT_RESOLVIDO = '''"""Auditable memory: immutable inscription, append-only state and flow.

This is a local application ledger, not access to a model's hidden state/KV cache.
Hashes detect inconsistent storage; they are not an external trust anchor.

Schema v2 (12/10/2026): events store deltas, the current state is materialized
per context, every mutation is journaled before commit and the database is
copied by bytes on a mutation/time policy. A v1 database raises
``SchemaMigrationRequired`` until the explicit migration runs.
"""
from .store import (
    MemoryStore, MemoryError, InvalidInput, ContextNotFound, ScopeViolation,
    AnchorConflict, RevisionConflict, IdempotencyConflict, IntegrityError,
    ProjectionOverflow, InvariantViolation, SchemaMigrationRequired,
)
# D4 (12/10/2026): fail-closed confidentiality guard shared by sessions, app and queue.
from . import guard
from .guard import ConfidentialContent

__all__ = [
    'MemoryStore', 'MemoryError', 'InvalidInput', 'ContextNotFound',
    'ScopeViolation', 'AnchorConflict', 'RevisionConflict',
    'IdempotencyConflict', 'IntegrityError', 'ProjectionOverflow',
    'InvariantViolation', 'SchemaMigrationRequired', 'ConfidentialContent', 'guard',
]
'''


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def espelho(base: Path, src: Path) -> Path:
    return base / src.drive.rstrip(':') / Path(*src.parts[1:])


def write_bytes_verified(dst: Path, data: bytes):
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + '.tmp_int')
    with open(tmp, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if tmp.read_bytes() != data:
        raise RuntimeError('cópia divergente: %s' % dst)
    os.replace(tmp, dst)


def copy_verified(src: Path, dst: Path, expect_sha16=None) -> str:
    data = Path(src).read_bytes()
    digest = sha256(data)
    if expect_sha16 and not digest.startswith(expect_sha16):
        raise RuntimeError('sha divergente em %s: %s esperado %s' % (src, digest[:16], expect_sha16))
    write_bytes_verified(dst, data)
    return digest


def load_front_hashes():
    """Hashes declarados pelas frentes, lidos dos seus manifestos/resumos (não de memória)."""
    declared = {}
    m1 = json.loads((NUCLEO / 'MANIFESTO.json').read_text(encoding='utf-8'))
    for item in m1['arquivos']:
        declared[('1_NUCLEO', item['path'].replace('\\', '/'))] = item['sha256']
    m2 = json.loads((HB / 'MANIFESTO.json').read_text(encoding='utf-8'))
    for item in m2.get('arquivos', m2.get('files', [])):
        p = (item.get('path') or item.get('file') or '').replace('\\', '/')
        if p and item.get('sha256'):
            declared[('2_HEARTBEAT', p)] = item['sha256']
    r3 = json.loads((FILT / 'DIFF_RESUMO.json').read_text(encoding='utf-8'))
    for item in r3:
        declared[('3_FILTROS', 'copia/' + item['file'])] = item['new_sha256']
    return declared


def merge3(base: Path, ours: Path, theirs: Path, out: Path, nome: str):
    """git merge-file (três vias) sobre BYTES; devolve relatório. Nunca toca as entradas."""
    work = out.parent / ('tmp_' + nome)
    work.mkdir(parents=True, exist_ok=True)
    b, o, t = work / 'base', work / 'ours', work / 'theirs'
    b.write_bytes(base.read_bytes())
    o.write_bytes(ours.read_bytes())
    t.write_bytes(theirs.read_bytes())
    proc = subprocess.run(['git', '-c', 'core.autocrlf=false', 'merge-file', '-p', '-L', 'ours', '-L', 'base',
                           '-L', 'theirs', str(o), str(b), str(t)], capture_output=True)
    merged = proc.stdout
    write_bytes_verified(out, merged)
    return {'nome': nome, 'base': str(base), 'ours': str(ours), 'theirs': str(theirs), 'saida': str(out),
            'base_sha256': sha256_file(base), 'ours_sha256': sha256_file(ours), 'theirs_sha256': sha256_file(theirs),
            'merged_sha256': sha256(merged), 'conflicts': proc.returncode, 'returncode': proc.returncode,
            'stderr': proc.stderr.decode('utf-8', 'replace')[-500:]}


def main():
    at = datetime.now(timezone.utc).isoformat()
    declared = load_front_hashes()
    manifest = {'titulo': 'INTEGRAÇÃO — conserto ACOM 12/10 — CANDIDATO', 'at': at, 'arquivos': [], 'originais': [],
                'merges': [], 'declarados_das_frentes_usados': {}}

    def take(front_root: Path, rel: str, target: Path, front: str, role='frente'):
        src = front_root / rel
        key = (front, rel.replace('\\', '/'))
        exp = declared.get(key)
        digest = copy_verified(src, espelho(CAND, target), exp[:16] if exp else None)
        manifest['arquivos'].append({'target': str(target), 'origem': str(src), 'frente': front, 'role': role,
                                     'sha256': digest, 'bytes': src.stat().st_size,
                                     'sha256_declarado_pela_frente': exp, 'conferido_contra_frente': bool(exp)})
        if exp:
            manifest['declarados_das_frentes_usados'][str(src)] = exp
        return digest

    # ---- ORIGINAIS: produção, só leitura, congelados por bytes ----
    originais = [MEM / 'CORE.md', MEM / 'SESSION_BRIDGE.md', MEM / 'session_memory.py', MEM / 'session_hook.py',
                 MEM / 'README.md', MEM / 'SESSION_MEMORY.md',
                 MEM / 'lib' / 'iald_memory' / '__init__.py', MEM / 'lib' / 'iald_memory' / 'store.py',
                 APP / 'iald_web_server.py', APP / 'iald_app_memory.py',
                 FILA / 'policy.py', FILA / 'operational_memory.py', FILA / 'nos_packet.py']
    for src in originais:
        st = src.stat()
        digest = copy_verified(src, espelho(ORIG, src))
        manifest['originais'].append({'source': str(src), 'bytes': st.st_size, 'sha256': digest,
                                      'mtime': datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds')})
    orig_by = {o['source']: o['sha256'] for o in manifest['originais']}
    cross = {
        str(MEM / 'lib' / 'iald_memory' / '__init__.py'): [NUCLEO / 'originais/lib/iald_memory/__init__.py',
                                                           FILT / 'originais/C/IALD/MEMORIA_IALD/lib/iald_memory/__init__.py'],
        str(MEM / 'lib' / 'iald_memory' / 'store.py'): [NUCLEO / 'originais/lib/iald_memory/store.py',
                                                        FILT / 'originais/C/IALD/MEMORIA_IALD/lib/iald_memory/store.py'],
        str(APP / 'iald_app_memory.py'): [HB / 'originais/iald_app_memory.py',
                                          FILT / 'originais/C/IALD/projetos_pyhton/IALD/iald_app_memory.py'],
        str(APP / 'iald_web_server.py'): [HB / 'originais/iald_web_server.py'],
        str(MEM / 'session_memory.py'): [FILT / 'originais/C/IALD/MEMORIA_IALD/session_memory.py'],
        str(MEM / 'CORE.md'): [NUCLEO / 'originais/CORE.md'],
        str(MEM / 'SESSION_BRIDGE.md'): [FILT / 'originais/C/IALD/MEMORIA_IALD/SESSION_BRIDGE.md'],
        str(FILA / 'policy.py'): [FILT / 'originais/C/IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator/policy.py'],
        str(FILA / 'operational_memory.py'): [FILT / 'originais/C/IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator/operational_memory.py'],
    }
    manifest['originais_das_frentes_iguais_a_producao'] = {}
    for prod, fronts in cross.items():
        ok = all(sha256_file(f) == orig_by[prod] for f in fronts)
        manifest['originais_das_frentes_iguais_a_producao'][prod] = ok
        if not ok:
            raise RuntimeError('frente partiu de original diferente da produção: ' + prod)

    # ---- CANDIDATO: arquivos sem conflito ----
    take(NUCLEO, 'copia/MEMORIA_IALD/CORE.md', MEM / 'CORE.md', '1_NUCLEO')
    take(NUCLEO, 'copia/MEMORIA_IALD/migrar_para_delta.py', MEM / 'migrar_para_delta.py', '1_NUCLEO')
    take(NUCLEO, 'copia/MEMORIA_IALD/mover_backups_antigos.py', MEM / 'mover_backups_antigos.py', '1_NUCLEO')
    for name in ('store.py', 'journal.py', 'snapshots.py', 'migrate.py'):
        take(NUCLEO, 'copia/MEMORIA_IALD/lib/iald_memory/' + name, MEM / 'lib' / 'iald_memory' / name, '1_NUCLEO')
    take(HB, 'copia/projetos_pyhton/IALD/iald_web_server.py', APP / 'iald_web_server.py', '2_HEARTBEAT')
    take(FILT, 'copia/C/IALD/MEMORIA_IALD/session_memory.py', MEM / 'session_memory.py', '3_FILTROS')
    take(FILT, 'copia/C/IALD/MEMORIA_IALD/SESSION_BRIDGE.md', MEM / 'SESSION_BRIDGE.md', '3_FILTROS')
    take(FILT, 'copia/C/IALD/MEMORIA_IALD/lib/iald_memory/guard.py', MEM / 'lib' / 'iald_memory' / 'guard.py', '3_FILTROS')
    take(FILT, 'copia/C/IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator/policy.py',
         FILA / 'policy.py', '3_FILTROS')
    take(FILT, 'copia/C/IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator/operational_memory.py',
         FILA / 'operational_memory.py', '3_FILTROS')

    # ---- MERGE 1: __init__.py ----
    MERGE.mkdir(exist_ok=True)
    base = ORIG / 'C/IALD/MEMORIA_IALD/lib/iald_memory/__init__.py'
    ours = NUCLEO / 'copia/MEMORIA_IALD/lib/iald_memory/__init__.py'
    theirs = FILT / 'copia/C/IALD/MEMORIA_IALD/lib/iald_memory/__init__.py'
    init_merged = merge3(base, ours, theirs, MERGE / '__init__.merged.py', 'merge_init')
    manifest['merges'].append(init_merged)
    if init_merged['conflicts']:
        resolved = INIT_RESOLVIDO.encode('utf-8')
        write_bytes_verified(MERGE / '__init__.resolvido.py', resolved)
        init_merged['resolucao'] = {'arquivo': str(MERGE / '__init__.resolvido.py'), 'sha256': sha256(resolved),
                                    'regra': 'união dos dois acréscimos (NUCLEO: SchemaMigrationRequired; '
                                             'FILTROS: guard, ConfidentialContent); docstring da NUCLEO'}
        init_bytes = resolved
    else:
        init_bytes = (MERGE / '__init__.merged.py').read_bytes()
    txt = init_bytes.decode('utf-8')
    for needle in ('SchemaMigrationRequired', 'from . import guard', 'ConfidentialContent', "'guard'"):
        assert needle in txt, needle
    write_bytes_verified(espelho(CAND, MEM / 'lib' / 'iald_memory' / '__init__.py'), init_bytes)
    manifest['arquivos'].append({'target': str(MEM / 'lib' / 'iald_memory' / '__init__.py'),
                                 'origem': 'merge(1_NUCLEO, 3_FILTROS)', 'frente': 'merge', 'role': 'merge',
                                 'sha256': sha256(init_bytes), 'bytes': len(init_bytes),
                                 'sha256_declarado_pela_frente': None, 'conferido_contra_frente': False})

    # ---- MERGE 2: iald_app_memory.py ----
    base = ORIG / 'C/IALD/projetos_pyhton/IALD/iald_app_memory.py'
    ours = HB / 'copia/projetos_pyhton/IALD/iald_app_memory.py'
    theirs = FILT / 'copia/C/IALD/projetos_pyhton/IALD/iald_app_memory.py'
    app_merged = merge3(base, ours, theirs, MERGE / 'iald_app_memory.merged.py', 'merge_app_memory')
    manifest['merges'].append(app_merged)
    if app_merged['conflicts']:
        raise RuntimeError('conflito não automático em iald_app_memory.py: resolver à mão e registrar')
    merged = (MERGE / 'iald_app_memory.merged.py').read_bytes()
    nl = b'\r\n' if merged.count(b'\r\n') > merged.count(b'\n') // 2 else b'\n'
    anchor = b"        raise ValueError('Measurement text and source reference are required')" + nl
    assert merged.count(anchor) == 1, 'âncora do record_measurement não única'
    insert = (b"    # D4 (integracao 12/10/2026): objetivo, medida e fluxo sao escaneados ANTES de ensure_context, como qualquer" + nl
              + b"    # outro texto que entra no banco; recusa visivel (ConfidentialContent), nada gravado, nunca redacao silenciosa." + nl
              + b"    guard.assert_clean_text(canonical({'objective': objective, 'text': text, 'source_ref': source_ref, 'flow': flow})," + nl
              + b"                            'app.record_measurement:' + identifier, log_path=_guard_log())" + nl)
    final = merged.replace(anchor, anchor + insert, 1)
    cr_base, cr_final = base.read_bytes().count(b'\r\n'), final.count(b'\r\n')
    lf_only = final.count(b'\n') - cr_final
    app_merged['acrescimo_integrador'] = {'onde': 'record_measurement, antes de scope/ensure_context', 'linhas': 4,
                                          'texto_sha256': sha256(insert)}
    app_merged['terminadores'] = {'crlf_base': cr_base, 'crlf_final': cr_final, 'lf_soltos_final': lf_only}
    assert lf_only == 0, 'LF solto no arquivo CRLF: %d' % lf_only
    write_bytes_verified(MERGE / 'iald_app_memory.final.py', final)
    write_bytes_verified(espelho(CAND, APP / 'iald_app_memory.py'), final)
    manifest['arquivos'].append({'target': str(APP / 'iald_app_memory.py'),
                                 'origem': 'merge(2_HEARTBEAT, 3_FILTROS) + acréscimo do integrador', 'frente': 'merge',
                                 'role': 'merge', 'sha256': sha256(final), 'bytes': len(final),
                                 'sha256_declarado_pela_frente': None, 'conferido_contra_frente': False})
    for item in manifest['arquivos']:
        p = espelho(CAND, Path(item['target']))
        if p.suffix == '.py':
            compile(p.read_bytes(), str(p), 'exec')
            item['compila'] = True
    manifest['ferramentas'] = []
    for name in ('aplicar_blocos.py', 'SESSION_BRIDGE_v2.md'):
        d = copy_verified(FILT / name, HERE / 'ferramentas' / name)
        manifest['ferramentas'].append({'arquivo': str(HERE / 'ferramentas' / name), 'origem': str(FILT / name), 'sha256': d})
    (HERE / 'CANDIDATO_MANIFESTO.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'arquivos': len(manifest['arquivos']), 'originais': len(manifest['originais']),
                      'merges': [(m['nome'], m['conflicts']) for m in manifest['merges']]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
