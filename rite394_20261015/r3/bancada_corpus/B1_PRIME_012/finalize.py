from support import *
import re
A=json.loads((ROOT/"AUDITORIA_B1_PRIME.json").read_text("utf-8"))
assert A["all_axioms_subset_of_trio"] and A["main_consumes_existing_three_faces"]
F=json.loads((ROOT/"REAPROVEITAMENTO_B1_PRIME.json").read_text("utf-8"))
P=json.loads((ROOT/"PROVENIENCIA_COPIA.json").read_text("utf-8"))
source=Path(P["source"]);checks=[]
for row in P["files"]:
    if row["path"].startswith(".lake/"):continue
    p=source/row["path"]; h=digest(p)
    checks.append(dict(path=str(p),sha256=h,unchanged=h==row["sha256"]))
for row in F["sources"]+[F["proposed_consumer"]["anchor"]]+F["orders"]:
    p=Path(row["path"]);h=digest(p)
    checks.append(dict(path=str(p),sha256=h,unchanged=h==row["sha256"]))
assert all(x["unchanged"] for x in checks),"Source changed during work; report before finalizing"
record(ROOT/"INTEGRIDADE_ORIGENS.json",dict(time_utc=stamp(),checked=len(checks),all_unchanged=all(x["unchanged"] for x in checks),files=checks))
proposal=dict(flag="ext_pb_same_beta_four_faces_kernel_proved",theorem="TGLExt.the_same_beta_reads_four_faces",status="PROPOSED_NOT_INSTALLED",source="TGLExt/TheSameBetaReadsFourFaces.lean",import_line="import TGLExt.TheSameBetaReadsFourFaces",audit_line="#print axioms TGLExt.the_same_beta_reads_four_faces",exact_role="Condicional formal: EOM fornecida sobre operadores importados e mesmo beta de B1. Nao prova natureza, xi=1/6, K=gerador modular ou variacao de acao.",required_integration_checks=["Recompilacao e revisao independentes pelo operador", "Checar nome completo presente no relatorio e axiomas subconjunto do trio", "Validar hipoteses e consumidor da EOM antes de interpretar fisicamente"],gate_change=False)
record(ROOT/"PROPOSTA_CONSUMIDOR.json",proposal)
attempts=[]
for p in sorted((ROOT/"attempts").glob("*/run.json")):
    row=json.loads(p.read_text("utf-8"));attempts.append(dict(record=str(p),returncode=row["returncode"],seconds=row["seconds"]))
files=[ROOT/"kernel"/"TGLExt"/n for n in ["TheSameBetaReadsFourFaces.lean","ActionCouplingControls.lean","AuditSameBetaFourFaces.lean"]]
files += [ROOT/n for n in ["REAPROVEITAMENTO_B1_PRIME.md","REAPROVEITAMENTO_B1_PRIME.json","AUDITORIA_B1_PRIME.json","AUDITORIA_B1_PRIME.md","LIMITES.md","PROPOSTA_CONSUMIDOR.json","PROVENIENCIA_COPIA.json","INTEGRIDADE_ORIGENS.json","ERROS_E_CORRECOES.md","ADENDO_REAPROVEITAMENTO.md"]]
links=[]
for p in files: links.append(f"- [{p.name}](<{p.as_posix()}>) — SHA256 `{digest(p)}` ({p.stat().st_size} bytes)")
main=(ROOT/"kernel/TGLExt/TheSameBetaReadsFourFaces.lean").read_text("utf-8").splitlines()
line=next(i+1 for i,s in enumerate(main) if s.startswith("theorem the_same_beta_reads_four_faces"))
text="[REAL — candidato AUTORAL compilado e auditado; exame independente e aceite final pendentes]\n\n"
text+="B1 prime: ActionCouplingData separa xi, curvatura, operador de campo e K_boundary importado. A EOM nomeada e hipotese explicita; the_same_beta_reads_four_faces consome diretamente the_same_beta_reads_three_faces e conserva todas as suas clausulas. A quarta face e o acoplamento ao gerador fornecido pelo dado. Nao ha derivacao de funcional de acao nem de uma realizacao fisica.\n\n"
text+=f"Lean {A['lean_version']}. {len(A['expected_names'])} nomes com #print axioms efetivo, todos subconjunto de propext/Classical.choice/Quot.sound; {A['semantic_controls_count']} sondas adulteradas recusadas por incompatibilidade de tipo, com paredes semanticas provadas. {A['compiled_local_objects_count']} objetos TGL/TGLExt produzidos nesta raiz; caches de terceiros copiados por bytes, nao recompilacao integral da Mathlib. Nenhum maxHeartbeats novo foi imposto nos tres modulos.\n\n"
text+="PAGO no escopo condicional: tipo de operadores/secoes, xi proprio, K_boundary importado, EOM, consumo direto de B1, auditoria efetiva, controles de coeficiente/sinal/xi/alpha/gerador/curvatura, parede sem EOM, parede sem fonte nao nula, liberdade de xi e modelo algebrico com fonte nao nula. PROPOSTO: ext_pb_same_beta_four_faces_kernel_proved. NAO PAGO por esta entrega: K_boundary como gerador efetivo de um fluxo da torre, d'Alembertiano de uma metrica, derivacao variacional, solucao fisica, xi=1/6, revisao independente e incorporacao.\n\n"
text+=f"Fonte principal: linha {line}. A ficha MD/JSON antecede o codigo segundo metadados locais e registro das chamadas; nao ha carimbo externo de tempo. Nenhuma ficha anterior foi reescrita.\n\n"
text+="Tentativas de compilacao preservadas:\n"+"\n".join(f"- rc={r['returncode']}; {r['seconds']:.2f}s; {r['record']}" for r in attempts)+"\n\n"
text+="Erros de descoberta preservados como relato: AGENTS.md locais ausentes; leitura canônica/Artigo A recusada por acesso negado; dois nomes tentativos de modulo inexistentes, substituidos pelos nomes efetivamente inventariados; inventario Python inicial com escape invalido corrigido. Esses erros nao contaram como prova nem como controle negativo. A copia historica de um.py foi lida, nunca executada/importada.\n\n"
text+="Reproducao, exclusivamente a partir desta raiz (PowerShell):\n```powershell\n"
text+=f"Set-Location -LiteralPath '{ROOT}'\npython .\\build.py TGLExt.TheSameBetaReadsFourFaces TGLExt.ActionCouplingControls TGLExt.AuditSameBetaFourFaces\npython .\\negative_controls.py\npython .\\audit.py\n```\n\n"
text+="O build incremental pode reaproveitar objetos locais. Para recompilacao independente, o operador pode copiar fontes/configuracao/pacotes para outra raiz propria sem .lake/build; a gerencia decide a incorporacao. A entrega nao escreve no tunel nem modifica um.py/D1/gate/A2/B3/Atlas/canonico.\n\n"
text+="Arquivos e SHA256 lidos agora:\n\n"+"\n".join(links)+"\n\n"
text+="Falhas de desenvolvimento, erro do wrapper de console e correção da pasta vazia do cache estão registrados em ERROS_E_CORRECOES.md, com os respectivos snapshots e logs preservados.\n\n"
text+="MANIFESTO_B1_PRIME.json inventaria os artefatos autorais finais e os recibos. O proprio manifesto e selado em HASHES_ENTREGA.json (nenhum hash autocircular).\n"
atomic(ROOT/"ENTREGA_B1_PRIME.md",text)
manifest_files=[]
exclude={"MANIFESTO_B1_PRIME.json","HASHES_ENTREGA.json"}
for p in sorted(ROOT.rglob("*")):
    if not p.is_file():continue
    rel=p.relative_to(ROOT)
    if rel.parts[0] in ["tmp","__pycache__"]:continue
    if ".bak_" in p.name or ".tmp_" in p.name:continue
    if rel.parts[0]=="kernel":
        if rel.as_posix() not in ["kernel/TGLExt/"+n for n in ["TheSameBetaReadsFourFaces.lean","ActionCouplingControls.lean","AuditSameBetaFourFaces.lean"]]:continue
    if p.name in exclude:continue
    manifest_files.append(dict(path=rel.as_posix(),bytes=p.stat().st_size,sha256=digest(p)))
manifest=dict(status=A["status"],time_utc=stamp(),root=str(ROOT),scope="ORDEM012 B1 prime adendo001 §§4 e 5.2",files=manifest_files,base_and_cache_inventory="PROVENIENCIA_COPIA.json",compiled_objects_inventory="AUDITORIA_B1_PRIME.json",backups="Preservados; nao integram candidato de integracao",no_independent_review_claimed=True,proposed_flag=proposal,attempts=attempts,source_integrity="INTEGRIDADE_ORIGENS.json",limits="LIMITES.md")
record(ROOT/"MANIFESTO_B1_PRIME.json",manifest)
keys=[ROOT/"MANIFESTO_B1_PRIME.json",ROOT/"ENTREGA_B1_PRIME.md"]+files
record(ROOT/"HASHES_ENTREGA.json",dict(time_utc=stamp(),files=[dict(path=str(p),sha256=digest(p),bytes=p.stat().st_size) for p in keys]))
for p in [ROOT/"MANIFESTO_B1_PRIME.json",ROOT/"kernel/TGLExt/TheSameBetaReadsFourFaces.lean",ROOT/"AUDITORIA_B1_PRIME.json",ROOT/"REAPROVEITAMENTO_B1_PRIME.md",ROOT/"LIMITES.md"]: print(p.name,digest(p))
print('DELIVERED AUTHOR WORK ONLY')
