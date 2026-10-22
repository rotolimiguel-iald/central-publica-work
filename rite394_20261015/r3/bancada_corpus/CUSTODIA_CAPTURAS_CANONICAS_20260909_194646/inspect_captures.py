from pathlib import Path
import datetime
import hashlib
import json
import os
import re

OUT=Path(__file__).resolve().parent
WORK=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
BASE=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
assert OUT.is_relative_to(WORK)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pin(path):
    data=path.read_bytes()
    return {'path':path.as_posix(),'bytes':len(data),'sha256':sha(data),
            'mtime_utc':datetime.datetime.fromtimestamp(path.stat().st_mtime,datetime.timezone.utc).isoformat()}

def new_file(path,data):
    tmp=path.with_name(path.name+'.tmp')
    assert not path.exists() and not tmp.exists()
    with tmp.open('xb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==data
    tmp.rename(path)
    assert path.read_bytes()==data

source=BASE/'um.py'; manifest_path=BASE/'tgl_kernel_proof_manifest.json'
seal_path=BASE/'um_absoluto_selo.json'
all_paths=[source,manifest_path,seal_path,BASE/'tgl_kernel_build_capture.txt',BASE/'tgl_kernel_audit_capture.txt',BASE/'rodada_v337_stdout.txt']
before=[pin(p) for p in all_paths]
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
seal=json.loads(seal_path.read_text(encoding='utf-8'))
captures=[]
for stem in ['build','audit']:
    path=BASE/f'tgl_kernel_{stem}_capture.txt'
    raw=path.read_bytes()
    decoded=raw.decode('utf-8')
    normalized=decoded.replace('\r\n','\n')
    begin_marker='--- STDOUT ---\n'
    end_marker='\n--- STDERR ---\n'
    begin=normalized.index(begin_marker)+len(begin_marker)
    end=normalized.rindex(end_marker)
    stdout=normalized[begin:end]
    header=normalized[:begin]
    declared=int(re.search(r'# len\(stdout\)=(\d+)',header).group(1))
    returncode=int(re.search(r'# returncode: (-?\d+)',header).group(1))
    expected=manifest[f'{stem}_stdout_sha256']
    row={'kind':stem,'capture':pin(path),'normalization':'UTF-8 decode, then CRLF replaced by LF once; no strip/trim.',
         'stdout_start_marker':begin_marker,'stdout_end_marker':end_marker,
         'stdout_chars_measured_python':len(stdout),'stdout_chars_declared':declared,
         'stdout_sha256_measured':sha(stdout.encode('utf-8')),'stdout_sha256_in_manifest':expected,
         'stdout_hash_matches_manifest':sha(stdout.encode('utf-8'))==expected,
         'returncode_in_capture':returncode,
         'warning_lines':len(re.findall(r'^warning:',stdout,re.M)),
         'error_lines':len(re.findall(r'^error:',stdout,re.M))}
    captures.append(row)

trio={'propext','Classical.choice','Quot.sound'}
bad=[name for name,axs in manifest['axiom_report'].items() if not set(axs)<=trio]
source_text=source.read_text(encoding='utf-8')
source_lines=source_text.splitlines()
anchors=[]
for i,line in enumerate(source_lines,1):
    if any(token in line for token in ['def selftest_fail_closed','res = verify_tgl_kernel_formalization()',
       'res2 = verify_tgl_kernel_formalization()', 'res["build_stdout_sha256"]',
       'res["audit_stdout_sha256"]', 'for _nm, _pr in', '_fh.write("# cmd:',
       'def _unified_main()', '_st = selftest_fail_closed()']):
        anchors.append({'line':i,'text':line})

report={'status':'CURRENT_CAPTURE_LINEAGE_CHECKED_BUILD_PAYLOAD_DIFFERS_FROM_SEALED_MANIFEST',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'files_read_before':before,'seal_timestamp':seal['timestamp'],'manifest_timestamp':manifest['timestamp'],
 'source_matches_seal':before[0]['sha256']==seal['sha256']['um.py'],
 'manifest_matches_seal':before[1]['sha256']==seal['sha256']['tgl_kernel_proof_manifest.json'],
 'manifest_statuses':manifest['statuses'],'manifest_axiom_entries':len(manifest['axiom_report']),
 'entries_outside_standard_trio':bad,'captures':captures,'writer_and_selftest_anchors':anchors,
 'interpretation':'A captura build atual nao reproduz o payload hashado no manifesto selado. Isto nao e evidencia de falha de compilacao ou falsidade de teorema. A captura informa exit0; ha chamadas posteriores do verificador no selftest que regravam os mesmos arquivos.',
 'new_compilation_executed':False,'um_executed_or_imported':False,'originals_written':False,
 'authorship':'Inspecao propria; sem aprovacao atribuida a terceiros.'}
after=[pin(p) for p in all_paths]
assert before==after, 'An input changed during the inspection'
report['inputs_unchanged_during_inspection']=True
b,a=captures
note=f'''# Capturas atuais e manifesto selado: correspondência medida

09/09/2026. Inspeção própria somente leitura. Nenhum `um.py` foi executado/importado, nenhuma compilação foi iniciada e nenhum original foi modificado.

**[REAL — medição] A captura atual da auditoria reproduz o hash do manifesto. A captura atual do build não reproduz seu hash.** Essa diferença é uma incompatibilidade de correspondência entre artefatos históricos; não demonstra falha de compilação ou falsidade de uma prova.

## Origem e procedimento exato

No `um.py` canônico, as linhas 118960 e 118962 calculam SHA-256 de `build["stdout"].encode("utf-8")` e `audit["stdout"].encode("utf-8")`. As linhas 118967–118974 escrevem um arquivo com cabeçalho, marcador STDOUT, payload, marcador STDERR e outro payload. Portanto o hash do arquivo completo não deve ser comparado ao hash de STDOUT.

Esta inspeção:

1. Leu os bytes de cada captura, sem regravá-los.
2. Decodificou UTF-8 e substituiu cada CRLF por LF uma vez, para remover a tradução de fim de linha da escrita textual em Windows.
3. Tomou os caracteres depois de `--- STDOUT ---` seguido de LF e antes do último LF seguido de `--- STDERR ---` e LF. Esse LF anterior ao marcador é acrescentado pelo escritor; não pertence ao payload. Nenhum `strip`, `trim` ou remoção de espaços foi aplicado.
4. Codificou exatamente essa substring em UTF-8 e calculou SHA-256. Conferiu também os comprimentos declarados no cabeçalho e os códigos de saída registrados.

O script `inspect_captures.py` preserva a implementação completa desse procedimento. O JSON acompanha os hashes dos arquivos inteiros para custódia, além dos hashes dos payloads.

| Comparação | Build | Auditoria |
|---|---|---|
| SHA-256 medido do STDOUT | `{b['stdout_sha256_measured']}` | `{a['stdout_sha256_measured']}` |
| SHA-256 esperado pelo manifesto | `{b['stdout_sha256_in_manifest']}` | `{a['stdout_sha256_in_manifest']}` |
| Correspondência | {b['stdout_hash_matches_manifest']} | {a['stdout_hash_matches_manifest']} |
| Caracteres medidos / declarados | {b['stdout_chars_measured_python']} / {b['stdout_chars_declared']} | {a['stdout_chars_measured_python']} / {a['stdout_chars_declared']} |
| Código de saída na captura | {b['returncode_in_capture']} | {a['returncode_in_capture']} |
| Linhas `warning:` / `error:` | {b['warning_lines']} / {b['error_lines']} | {a['warning_lines']} / {a['error_lines']} |

## O que continua correspondendo ao selo

O programa canônico mede {before[0]['bytes']} bytes e SHA-256 `{before[0]['sha256']}`. O pin de `um.py` no selo confere. O manifesto mede {before[1]['bytes']} bytes e SHA-256 `{before[1]['sha256']}`; seu pin no selo também confere. Ambos mantêm a referência à rodada v337, com timestamp declarado `{manifest['timestamp']}`.

O manifesto informa `lake_build_ok=True`, ausência de `sorryAx`, `trustCompiler` e axiomas TGL próprios. Foram lidas {len(manifest['axiom_report'])} entradas de axiomas, das quais {len(bad)} têm axiomas fora de propext, Classical.choice e Quot.sound. Isso é leitura e comparação do recibo existente, não uma nova compilação independente.

## Por que a captura pode ser posterior ao manifesto

[REAL — fonte lida] `_unified_main` chama `main()` e depois `selftest_fail_closed` (`um.py`:162167–162169). O autoteste chama o mesmo verificador duas vezes, nas linhas 113921 e 113928; esse verificador regrava os mesmos nomes de captura nas linhas 118967–118974. O stdout da rodada registra o autoteste final aprovado. As capturas atuais têm mtime posterior ao timestamp do manifesto.

[DERIVED — explicação compatível com a estrutura observada] A regravação após o `main` explica que a captura do build presente não seja o payload selado anteriormente. Não foi reconstruído o payload ausente nem atribuída a ele a captura atual. A auditoria permanecer igual é compatível com a repetição dos mesmos enunciados; não prova igualdade dos logs de build.

## Consequência para o reexame

O programa e seu manifesto seguem ligados por pins conferidos. O build atual registra sucesso e warnings; a auditoria atual registra sucesso sem warnings e corresponde ao hash selado. A afirmação estrita que não se pode fazer é: **“o arquivo atual `tgl_kernel_build_capture.txt` reproduz o STDOUT de build hashado nesse manifesto.”** A inspeção não revoga os resultados matemáticos nem inventa uma recompilação faltante.

Todos os seis arquivos de entrada foram medidos antes e depois, sem alteração durante esta inspeção. Nenhum dado foi refeito e nenhum gate foi movido.
'''
new_file(OUT/'NOTA_CORRESPONDENCIA_CAPTURAS.md',note.encode('utf-8'))
report['note']=pin(OUT/'NOTA_CORRESPONDENCIA_CAPTURAS.md')
report['script']=pin(Path(__file__))
new_file(OUT/'EVIDENCIA_CAPTURAS.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'status':report['status'],'note':report['note'],
                  'evidence':pin(OUT/'EVIDENCIA_CAPTURAS.json'),
                  'source_matches_seal':report['source_matches_seal'],
                  'manifest_matches_seal':report['manifest_matches_seal'],
                  'capture_results':captures},ensure_ascii=False))
