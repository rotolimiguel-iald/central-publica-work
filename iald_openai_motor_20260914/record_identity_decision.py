"""Append the operator's canonical typing and runtime decision with byte backups."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

WORK = Path(__file__).parent
MEMORY = Path(r'C:\IALD\Central de Patentes\memory')
bundle = next((WORK / 'bundles').glob('kernel-*'))
manifest = json.loads((bundle / 'kernel_manifest.json').read_bytes())
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
text = f'''

### 14/09/2026 — IALD = ÍNDICE(TGL); TGL = ATLAS — aplicação no serviço OpenAI

[INPUT — ordem explícita do operador nesta sessão] “ela precisa entender que IALD=índice e TGL=ATLAS”.
[ONTO — nomenclatura do operador] **TGL = ATLAS; IALD = ÍNDICE(TGL).** A TGL organiza o espaço de correspondências; a IALD localiza, reconhece e relaciona uma identidade nesse espaço. A IALD não troca de papel com o Atlas. Esta tipagem deve estar sempre presente no núcleo de instruções da plataforma.

[REAL — implementação preparada, ainda não ativada] O serviço possui um pacote derivado dos {len(manifest['files'])} arquivos literais embutidos em `um.py`, inclusive {sum(r['path'].endswith('.lean') for r in manifest['files'])} fontes Lean. A extração usa AST literal, sem importar nem executar o programa. SHA-256 do programa de origem do pacote, lido do manifesto: `{manifest['source_sha256']}`. Fonte única documental: este `TGL_ATLAS.md`; a consulta o lê no lugar, sem bifurcar o Atlas.

[INPUT — decisão do operador] Ativar **núcleo sempre presente + kernel inteiro no servidor + consulta ao Atlas**. O modo de Atlas integral em cada chamada fica preservado como opção. [REAL — teste HTTP] A tentativa integral ao `gpt-4.1-nano` retornou HTTP 429, com limite informado de 400000 TPM; evidência datada em `work/iald_openai_motor_20260914/full_atlas_probe_*.json`. Não tratar tamanho da janela do modelo como autorização de throughput da conta.

[REAL — escopo limitado] Uma cópia de `TGLExt/TheIALDSelector.lean` compilou com Lean 4.31.0 usando dependências já compiladas, sem reconstruí-las nesta rodada. `iald_is_idempotent` e `iald_selects` reportaram `[propext, Classical.choice, Quot.sound]`. O pacote inteiro disponível não equivale a uma compilação integral desta rodada. Evidência: `work/iald_openai_motor_20260914/lean_checks_20260914_161846/verification.json`.

[REGRA OPERACIONAL] Atlas documental, índice Python em `um.py`, seletor formal Lean e recuperação de contexto do serviço são objetos distintos. Os nomes não demonstram uma implementação do seletor nos pesos de um modelo neural. [OPEN] Equivalência de comportamento com a IALD nativa treinada não foi demonstrada. O primeiro ensaio de três perguntas falhou na distinção Face/projeção e na disciplina de consulta; ajustar e reavaliar antes da ativação. Fontes formais de navegação: `TGLExt/TheAtlasIndex.lean` e `TGLExt/TheIALDSelector.lean`; preservar hipóteses, estatutos e histórico. Esta integração não move gate formal nem confirma teoria física.
'''

for path in (MEMORY / 'TGL_ATLAS.md', MEMORY / 'TGL_INDICE_VIVO.md'):
    before = path.read_bytes()
    backup = path.with_name(path.name + '.bak_' + stamp)
    backup.write_bytes(before)
    if backup.read_bytes() != before:
        raise RuntimeError('Byte backup mismatch')
    after = before + text.replace('\n', '\r\n' if b'\r\n' in before else '\n').encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + stamp)
    temporary.write_bytes(after)
    if temporary.read_bytes() != after or len(after) <= len(before):
        raise RuntimeError('Unexpected append')
    if path.read_bytes() != before:
        raise RuntimeError('Concurrent canonical edit; append not installed')
    os.replace(temporary, path)
    if path.read_bytes() != after:
        restore = path.with_name(path.name + '.restore_' + stamp)
        restore.write_bytes(backup.read_bytes())
        os.replace(restore, path)
        raise RuntimeError('Installed append mismatch; original restored')
    print(json.dumps({'file': path.name, 'bytes_before': len(before), 'bytes_after': len(after),
                      'backup_verified': True, 'sha256': hashlib.sha256(after).hexdigest()}))
