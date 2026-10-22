from pathlib import Path
import os,json,hashlib
root=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
out=Path(__file__).resolve().parent
source=root/'AUDITORIA_INTEGRACAO_77_20260909_175126_146774'/'audit_integration_77.py'
original=source.read_bytes(); text=original.decode('utf8')
body=text.split('out=savej("AUDITORIA_INTEGRACAO_77.json",result)')[0]
replacements=[
 ('Independent static audit of 77 integrated modules','Static audit by a separate scanner of 83 integrated modules'),
 ('FOLDER=BASE/"COPIA_INTEGRADA_20260909_174634_173402"','assert len(sys.argv)==3, "Pass copy83 folder and its preparer folder"\nFOLDER=Path(sys.argv[1]).resolve()\nassert FOLDER.is_relative_to(BASE)'),
 ('PREPARER=BASE/"INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582"','PREPARER=Path(sys.argv[2]).resolve()\nassert PREPARER.is_relative_to(BASE)'),
 ('"three_stages_63_9_5"','"four_stages_63_9_5_6"'),
 ('==[63,9,5]','==[63,9,5,6]'),
 ('{"modules":77,"theorems":1065,"other_declarations":293,"local_instances":7,"total":1358}','{"modules":83,"theorems":1178,"other_declarations":328,"local_instances":12,"total":1506}'),
 ('{"modules":5,"theorems":93,"other_declarations":29,"local_instances":0,"total":122}','{"modules":6,"theorems":113,"other_declarations":35,"local_instances":5,"total":148}'),
 ('==[606,669,678,683]','==[606,669,678,683,689]'),
 ('==[602,665,674,679]','==[602,665,674,679,685]'),
 ('len(declarations)==1358','len(declarations)==1506'),
 ('len(expected_full)==5557','len(expected_full)==5670'),
 ('len(plan["cached_modules"])==72 and len(plan["runs"])==8 and [r["module"] for r in plan["runs"][:5]]','len(plan["cached_modules"])==77 and len(plan["runs"])==9 and [r["module"] for r in plan["runs"][:6]]'),
 ('len(cr["runs"])==8','len(cr["runs"])==9'),
 ('"FullTGLAudit":5557,"NewModulesAudit":1358','"FullTGLAudit":5670,"NewModulesAudit":1506')
]
for a,b in replacements:
    assert body.count(a)==1,(a,body.count(a))
    body=body.replace(a,b)
labels={
 'all_77_sources_preserved':'all_83_sources_preserved',
 'measured_77_1065_293_1358':'measured_83_1178_328_1506',
 'delta5_93_29_122':'delta6_113_35_148',
 'embedded_counts_606_669_678_683':'embedded_counts_606_669_678_683_689',
 'lean_counts_602_665_674_679':'lean_counts_602_665_674_679_685',
 'among77':'among83',
 'cumulative_77_imports':'cumulative_83_imports',
 'cumulative_1065_theorem_audits':'cumulative_1178_theorem_audits',
 'dedicated_audit_all1358':'dedicated_audit_all1506',
 'plan_all77':'plan_all83',
 'plan_all1358':'plan_all1506',
 'plan_FullTGLAudit5557':'plan_FullTGLAudit5670',
 'dedicated_audit_seven_instances':'dedicated_audit_twelve_instances',
 'prepared_72_cache_5_new_3_aggregates':'prepared_77_cache_6_new_3_aggregates',
 'prepared_sources_match_all77':'prepared_sources_match_all83',
 'combined_PASS_8_clean_exits':'combined_PASS_9_clean_exits',
 'all77_compiled_artifacts':'all83_compiled_artifacts'
}
for a,b in labels.items():
    assert a in body,a
    body=body.replace(a,b)
tail='''out=savej("AUDITORIA_INTEGRACAO_83.json",result)
note=f"""# Auditoria estática da integração83

{status}

[REAL — medido] {totals['modules']} módulos; {totals['theorems']} teoremas e {totals['other_declarations']} outras declarações, incluindo {totals['local_instances']} instâncias locais nomeadas; {totals['total']} termos explícitos auditados.

A genealogia foi percorrida: canônico → lote63 → delta9 → delta5 → delta6. O scanner deste script, separado do integrador, confere nomes, transposições e hashes. A configuração e os recibos de cada camada são lidos; o delta de uma camada não substitui o inventário cumulativo.

AST e bytes fora da tabela de arquivos embutidos foram comparados em toda a cadeia. Sentinelas, flags e gate são preservados. Dentro da tabela, entram seis módulos e acréscimos nos agregadores. Não foi executado/importado nenhum um.py.

Verificações: {result['checks_passed']}/{result['checks_total']}. Arquivos embutidos: {len(final)}; arquivos Lean: {sum(k.endswith('.lean') for k in final)}. Resultado conjunto lido: {combined['status'] if combined else 'AUSENTE'}.

O limite de auditoria permanece explícito: dependências externas transitivas não foram todas recompiladas ou integralmente hashadas. A compilação incremental reaproveita cache com genealogia conferida. Não há afirmação de rodada do programa, novo selo ou veredito físico.

[Recibo completo](<{(OUT/'AUDITORIA_INTEGRACAO_83.json').as_posix()}>).
"""
report=save("RELATORIO_INTEGRACAO_83.md",note)
manifest=savej("MANIFESTO_AUDITORIA_83.json",{"status":status,"artifacts":[out,report],"script":rec(Path(__file__))})
print(json.dumps({"status":status,"counts":result["counts"],"delta":result["delta_counts"],"failed_checks":result["failed_checks"],"final":result["final_integrated"],"outputs":[out,report,manifest]},ensure_ascii=False,indent=2))
'''
result=(body+tail).encode('utf8')
def new(p,b):
    assert p.resolve().is_relative_to(root) and not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.replace(t,p);assert p.read_bytes()==b
new(out/'audit_integration_83.py',result)
new(out/'AUDITOR_PROVENANCE.json',(json.dumps({'source':{'path':source.as_posix(),'bytes':len(original),'sha256':hashlib.sha256(original).hexdigest()},'result':{'bytes':len(result),'sha256':hashlib.sha256(result).hexdigest()},'exact_replacements':replacements,'label_replacements':labels,'report_tail_rewritten':True,'auditor_executed':False},ensure_ascii=False,indent=2)+'\n').encode())
print(out/'audit_integration_83.py')
