from pathlib import Path
import datetime
import hashlib
import json
import os

REV = Path(__file__).resolve().parent
RUN = Path((REV / 'paired_right_integrated_latest_run.txt').read_text().strip())
REPORT = REV / 'REVIEW_PAIRED_RIGHT_INTEGRATED.md'
assert RUN.resolve().is_relative_to(REV)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    return json.loads(p.read_bytes())
def link(label, p):
    return f'[{label}](<{p.resolve().as_posix()}>)'
def atomic(p, raw):
    assert p.resolve().is_relative_to(REV)
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + stamp)
        with backup.open('xb') as f:
            f.write(old)
        assert backup.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp_' + stamp)
    with tmp.open('xb') as f:
        f.write(raw)
    assert tmp.read_bytes() == raw
    os.replace(tmp, p)
    assert p.read_bytes() == raw

assert not REPORT.exists()
s = load(RUN / 'static_verification.json')
assert s['mode'] == 'STATIC_ONLY_BUILD_NOT_CONSUMED'
assert s['all_three_import_rewrites_literal'] and s['python_AST_outside_embedded_equal']
assert s['gate_extension_bytes_equal'] and s['surface_count'] == 34
assert s['source_Audit_added'] == 29 and s['source_Audit_parent_no_loss']
now = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text = f'''# Revisão integrada — pares direitos e adjunto original

Estrato preliminar {now}. **Inspeção estática concluída; compilação integrada, stream Audit e controles finais ainda pendentes de conferência.** O marcador conclusivo fica reservado ao adendo final.

[REAL] Nenhum achado P0–P2 nesta inspeção estática. As três fontes TGLExt/V350 são idênticas às DEV revisadas após somente a substituição mecânica dos imports. Seus bytes coincidem com o dicionário embutido. As hipóteses, nomes e 29 alvos permanecem os mesmos da revisão DEV; nenhuma recompilação foi repetida.

O dicionário tem **{s['embedded_files']} arquivos**, com apenas três novas entradas e mudanças nas duas raízes. A fonte `TGL/Audit.lean` preserva os 6901 nomes anteriores e acrescenta exatamente os 29 do auditor próprio, totalizando **{s['source_Audit_distinct']} nomes distintos na fonte**. Essa medição ainda não é certificação do novo stream compilado.

O AST Python fora de `_EMBEDDED_KERNEL_FILES` coincide com a cópia mãe; `gate_extension.py` permanece byte a byte. Os deltas dos três scripts executados pelo autor são exatamente os previstos no exame DEV: batch544→573, três módulos antes das raízes e um grupo de fronteira adicional. A lógica de hashes atuais/históricos Audit não mudou; confrontá-los ao novo stream dependerá dos relatórios finais. Os cinco helpers congelados coincidem com os hashes já inspecionados no DEV.

[REAL] As 34 memórias e seus backups/prefixos continuam iguais à mãe, sem nova custódia ou relatório integrado autoral presentes na captura. O recorder prevê backup imediato de bytes e append/replace atômico por arquivo; exige também o parecer integrado final. Sua execução e a do verifier não foram realizadas pelo revisor nem são declaradas concluídas. O original canônico e a base foram relidos apenas para hash.

| Pin | SHA256 lido |
| --- | --- |
| Cópia integrada | `{s['working_sha256']}` |
| Mãe right_regularization_custody.json | `{s['parent_custody_sha256']}` |
| Original canônico/base | `{s['original_sha256']}` |
| Parecer DEV preservado | `{s['own_DEV_review_sha256']}` |
| Captura estática | `{sha(RUN / 'static_verification.json')}` |

{link('Evidência estática e pins', RUN / 'static_verification.json')}; {link('fiação por AST', RUN / 'gate_wiring.json')}. A fiação mantém as seis flags maiores como fronteira anexa; elas não são entradas diretas do avaliador legado, que lê qgc_, qgp_ e o feed. O resultado da fronteira nos novos controles ainda será conferido.

[OPEN — pendências desta integração] Conferir os registros finais fonte/binário/log/streams, a preservação dos 189 registros não raízes e as cinco novas compilações esperadas, o Audit atual com seus 29 acréscimos e os controles atualizados. Os JSONs do build/testes em andamento não foram consumidos como evidência final. Não houve execução/importação de monólito, helpers autorais ou escrita em memórias pelo revisor.

Limites matemáticos herdados: pares no F original e VNA gerada igual a π(N)' não identificam R=Jπ(b)J, núcleo no gráfico de F, inclusão inversa por J, plenitude de álgebra de Hilbert ou KMS/traço. Nada promove o gate ou encerra runtime/objetivo integral.
'''
atomic(REPORT, text.encode('utf-8'))
pin = {'timestamp': now, 'status': 'STATIC_ONLY__FINAL_EVIDENCE_PENDING',
       'report': str(REPORT), 'report_sha256': sha(REPORT),
       'static_verification_sha256': sha(RUN / 'static_verification.json')}
atomic(RUN / 'preliminary_review_pin.json', (json.dumps(pin, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps(pin, ensure_ascii=False))
