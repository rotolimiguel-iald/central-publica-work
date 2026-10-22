import datetime
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911")
REVIEW = ROOT / "revisao"
RUN = REVIEW / "full_runtime_formal_stage_20260913_093418_886098"
evidence_path = RUN / "evidence.json"
raw = evidence_path.read_bytes()
e = json.loads(raw)
assert all(e["verification"].values())
assert e["snapshots_stable_at_end"] and not e["findings"]
assert all(x["literal_equal"] for x in e["file_comparison"])
assert len(e["gate_entries"]) == 11
now = datetime.datetime.now().astimezone()

def link(label, path):
    return f"[{label}](<{Path(path).as_posix()}>)"

capture_rows = []
for label, key in [("Build", "build_capture"), ("Audit", "audit_capture")]:
    c = e[key]
    capture_rows.append(f"| {label} | {c['returncode']} | {c['bytes']:,} | {c['mtime']} | `{c['sha256']}` |")
gate_rows = []
for g in e["gate_entries"]:
    source = g["source_hits"][0]
    gate_rows.append(f"| `{g['flag']}` | `{g['declaration']}` | `{source['file']}:{source['line']}` |")
binary_rows = []
for b in e["materialized_root_binaries"]:
    binary_rows.append(f"- `{Path(b['path']).name}`: `{b['sha256']}`, mtime {b['mtime']}.")

text = f"""# Revisão parcial da etapa formal da rodada integral

Data do parecer: {now.isoformat()}. Captura independente: {e['timestamp']}.
Estatuto: **[REAL — inspeção independente de fontes e capturas autorais; etapa formal parcial]**.

**Nenhum achado P0–P2 no escopo conferido.** As capturas frescas de build e Audit registram rc0; a cobertura de axiomas corresponde exatamente aos 7.133 nomes únicos solicitados por `#print axioms`. Os onze fornecedores formais do gate estão presentes e auditados. Isto encerra esta verificação formal, sem declarar concluídos o processo integral, os probes, o autoteste, o selo ou os JSONs finais.

## Evidência própria e método

Usei somente leitura de arquivos, análise AST sem execução do monólito, comparação de bytes e parsing independente das capturas. Não iniciei Lean/Lake, não importei/executiei `um.py`, não consumi a sessão 94059 nem interrompi o processo do autor. As únicas escritas foram em `revisao/`.

Evidência detalhada: {link('evidence.json', evidence_path)}; SHA256 `{hashlib.sha256(raw).hexdigest()}`. Script de verificação: {link('review_full_runtime_formal_stage.py', REVIEW / 'review_full_runtime_formal_stage.py')}. A evidência contém o mapa completo nome→axiomas, os 922 pares de fontes, os onze fornecedores e pins das capturas, manifestos e raízes. As capturas atuais foram preservadas na mesma subpasta. A verificação própria terminou rc0; isso é execução do script de leitura, **não recompilação independente**.

## Capturas frescas e integridade

| Captura | rc | Bytes | mtime BRT | SHA256 do arquivo capturado |
|---|---:|---:|---|---|
{chr(10).join(capture_rows)}

Os cabeçalhos registram `lake build` e `lake env lean TGL/Audit.lean`. Ambos são posteriores ao início da tentativa 02, `{e['process_manifest_at_read']['started']}`. Não há linhas de erro nas capturas atuais. Os comprimentos de stdout/stderr recuperados coincidem com os comprimentos em caracteres declarados pelo gravador. O JSON distingue hash dos bytes da captura de hash UTF-8 do stdout recuperado com normalização CRLF; não os equipara ao hash de um stream bruto separado.

O build termina com `Build completed successfully (9467 jobs).` Há 208 eventos visíveis `Built` e 499 `Replayed`; não interpretei 9.467 jobs como 9.467 recompilações novas. A preparação informa cache herdado. Os avisos incluem lint e `aesop ... has local changes`: não houve auditoria nova de todo o pacote aesop nem revalidação dos 127.078 arquivos do inventário de preparação. Esse limite de proveniência permanece explícito.

`ROOT/um.py` e `ROOT/r/um.py` são byte a byte iguais, SHA256 `{e['root_copy']['sha256']}`, também igual ao pin do contrato ativo. Os **922 arquivos embutidos**, incluindo **218 módulos TGLExt/V350**, coincidem literalmente em bytes com os materializados em `r/tgl_kernel`. A fonte `TGL/Audit.lean` e suas listas de comandos coincidem com o embutido. As duas raízes binárias foram lidas e pinadas:

{chr(10).join(binary_rows)}

Os rc1 de `r/failed_attempt_01` foram identificados e excluídos; não são a evidência da tentativa 02. Os manifestos de preparação, com caminho e estado antigos, foram tratados como histórico de preparação. O hash canônico neles declarado foi preservado como dado de origem; esta etapa não fez nova releitura do original externo nem revalidou toda a cadeia de binários das dependências.

## Cobertura formal e onze entradas do contrato

Foram encontrados **7.140 comandos/mensagens `#print axioms`, 7.133 nomes únicos e sete repetições consistentes**. Nenhum nome faltante, extra ou com conjuntos conflitantes. O parser reconhece os **50 resultados `does not depend on any axioms`**, incluindo `TGLExt.comm_of_fixed'`; apóstrofos não truncam nomes. Todos os conjuntos retornados estão contidos em `propext`, `Classical.choice`, `Quot.sound`; os conjuntos vazios são válidos. Não apareceu axioma fora da lista permitida. A saída do build também cobre o mesmo conjunto auditado.

Há ainda 656 comandos `#check`; 174 nomes únicos desses comandos não têm impressão individual de axiomas no Audit existente. O rc0 confere sua elaboração, não fornece para cada um uma lista individual de axiomas. A cobertura exata acima refere-se aos comandos explícitos `#print axioms`. Essa distinção não foi convertida em nova exigência matemática; todos os onze fornecedores do gate têm impressão explícita.

| Entrada consumida | Declaração auditada | Fonte materializada |
|---|---|---|
{chr(10).join(gate_rows)}

Cada linha foi extraída das listas do próprio monólito por AST, localizada em uma fonte embutida/materializada e confrontada com o Audit fresco; todas têm exatamente o trio permitido. A ligação dessas seis entradas `qgc` e cinco `qgp` ao avaliador principal mantém o escopo da auditoria anterior. A cobertura formal está confirmada aqui; não antecipei os valores persistidos no futuro JSON final da rodada.

## Limite do parecer

O contrato lido tem SHA256 `{e['contract']['sha256']}`. Nenhuma obrigação original-S/KMS, UV ou flag adicional foi criada ou cobrada como bloqueio do gate principal. A separação já estabelecida entre suas entradas e o anexo `kernel_frontier` permanece; uma subdecisão literal não foi tratada como prova nova.

**[OPEN — nesta revisão]** Restante dos cálculos, probes, autoteste, emissão de selo e JSONs finais. O manifesto da tentativa 02 foi lido como registro de início/estado, sem consulta ou controle da sessão/processo. Este parecer não certifica o término da rodada, não promove gate e não declara confirmação física. Os pareceres anteriores, originais, fontes, memórias e custódias permaneceram intocados.
"""
text = text.replace("importei/executiei", "importei/executei")
target = REVIEW / "REVIEW_FULL_RUNTIME_FORMAL_STAGE.md"
assert not target.exists(), "Relatório já existe; preservar e tratar por adendo separado."
payload = text.encode("utf-8")
tmp = target.with_name(target.name + ".tmp_" + now.strftime("%Y%m%d_%H%M%S_%f"))
with tmp.open("xb") as f:
    f.write(payload)
assert tmp.read_bytes() == payload and len(payload) > 1000
os.replace(tmp, target)
assert target.read_bytes() == payload
pin = {"report": str(target), "report_sha256": hashlib.sha256(payload).hexdigest(),
       "bytes": len(payload), "evidence": str(evidence_path),
       "evidence_sha256": hashlib.sha256(raw).hexdigest(),
       "formal_stage_only": True, "findings_P0_P2": [], "final_runtime_reviewed": False}
pin_path = RUN / "report_pin.json"
pin_tmp = RUN / "report_pin.json.tmp"
with pin_tmp.open("xb") as f:
    f.write(json.dumps(pin, ensure_ascii=False, indent=2).encode("utf-8"))
os.replace(pin_tmp, pin_path)
print(json.dumps(pin, ensure_ascii=False, indent=2))
