# -*- coding: utf-8 -*-
"""MANIFESTO_R2.json: sha256 (lido do arquivo) de cada entregável da R2 e dos backups R1 dos scripts reescritos."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAIZES = ['candidato_r2', 'testes_r2_src', 'evidencias_r2', 'ensaio_implantacao_r2\\sim', 'revisores_r2']
SOLTOS = ['CANDIDATO_MANIFESTO_R2.json', 'DIFF_R2.patch', 'DIFF_R1_R2.patch', 'DIFF_R2_APPLY_CHECK.json', 'gerar_candidato_r2.py',
          'gerar_manifesto_r2.py', 'implantar.py', 'reverter.py', 'implantacao_lib.py', 'implantar_config_producao.json',
          'ferramentas\\aplicar_blocos.py', 'r2_producao_somente_leitura.py', 'RESULTADO_INTEGRACAO_R2.md', 'RESULTADO_INTEGRACAO.md',
          'testes_r2\\montar_suite.py', 'testes_r2\\rodar.py', 'testes_r2\\TESTES.md', 'testes_r2\\RESULTADOS_TESTES.json',
          'testes_r2\\SUITE_MANIFEST.json', 'testes_r2\\src_integracao\\test_integracao.py', 'testes_r2\\src_integracao\\rodar_fila55.py',
          'ensaio_implantacao_r2\\rodar_ensaio_r2.py', 'ensaio_implantacao_r2\\ENSAIO_R2_RECIBO.json',
          'ensaio_implantacao_r2\\ENSAIO_R2_RECIBO_rodada1.json', 'ensaio_implantacao_r2\\ENSAIO_R2_RECIBO_rodada2.json']
PULAR = ('raiz', 'sb_session', '__pycache__', 'sim_run')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    files = set()
    for r in RAIZES:
        for p in (HERE / r).rglob('*'):
            if p.is_file() and not any(x in p.relative_to(HERE).parts for x in PULAR):
                files.add(p)
    for s in SOLTOS:
        files.add(HERE / s)
    files |= set(HERE.glob('*.bak_r1_*')) | set((HERE / 'ferramentas').glob('*.bak_r1_*'))
    out = []
    for p in sorted(files):
        st = p.stat()
        out.append({'path': str(p.relative_to(HERE)), 'bytes': st.st_size, 'sha256': sha(p),
                    'mtime': datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds')})
    m = {'titulo': 'INTEGRAÇÃO R2 — conserto ACOM 12/10 — MANIFESTO', 'gerado_em': datetime.now(timezone.utc).isoformat(),
         'gerado_por': 'gerar_manifesto_r2.py (hashes lidos dos arquivos)', 'producao_nao_tocada': True,
         'n_arquivos': len(out), 'arquivos': out}
    (HERE / 'MANIFESTO_R2.json').write_text(json.dumps(m, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(len(out), sha(HERE / 'MANIFESTO_R2.json')[:16])


if __name__ == '__main__':
    main()
