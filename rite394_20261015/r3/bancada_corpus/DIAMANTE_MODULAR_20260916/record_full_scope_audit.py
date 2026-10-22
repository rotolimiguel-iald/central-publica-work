"""Record a documentary completion audit; no new theorem or motor flag."""
import json
from pathlib import Path
import finalize_weyl_bridge as c

root,work=c.ROOT,c.WORK
old=json.loads((root/'CHARGE_ORDER_MANIFEST.json').read_text(encoding='utf-8'))
canonical=c.pin(Path(old['canonical_unchanged']['path']))
assert canonical==old['canonical_unchanged']
source_paths=[
    work/'POSITIVIDADE_BRST_FORMAL_072_20260910/ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md',
    work/'FOCK_HADAMARD_QUARTETOS_073_20260910/FOCK_DOMINIO_WICK_E_P0.md',
    work/'COMUTANTE_FOCK_SUAVE_073_20260910/COMUTANTE_ESCALAR_E_CARGA_CONDICIONAL.md',
    work/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
    work/'INTERACAO_LOCAL_SOMAVEL_20260909_143042_266556/MAPA_MODULAR_UV.md',
    work/'CURVED_CONNECTION_20260909_124927_233677/OBJETO_UV_E_ROTAS.md',
    work.parent/'memory/TGL_INDICE_VIVO.md']
sources=[c.pin(p) for p in source_paths]
addition=f'''\n\n## {c.NOW} — auditoria do objetivo inteiro

[REAL — leitura documental] Conferidas072,comutante073,contratoFock073,índicevivo§4b e fonteum.py(prove_the_renormalization_wall e programasindependentes). Atualização importante: não repetir P0 como ausente a partir do balanço histórico072; Fock073 o realiza no alcance da polarização/domínio indicados. Estadointeragente072 é formal e condicionalP0–P2; não soma série z=1, não fornece vácuoUVnão perturbativo. Comutante073 não constrói implementaçãoQME/carga. Comentários históricos do motor não reabrem os objetos posteriores de core/torre.

[AUDITORIA — não novo teorema] AUDITORIA_DO_ALVO_COMPLETO.md confronta todas exigências. Recuperação documental e resultadoslineares disponíveis; cargacompleta, estadofísicointeragenteUV e coeficienteR1físico não demonstrados. Nenhum controle finito pode preencher essa lacuna por contagem. Pergunta enviada ao operador para fixar o parâmetro do primeirocoeficiente (acoplamento/raio/geometria); aguardando resposta sem presumir escolha. Goalativo, turnoanteriorPROGRESS, auditoriaPROGRESS documental; nãoháprocessoativoemespera nem encerramento daQG.

Busca por nomes encontrou acesso negado em dependências077; não foi alegada varredura exaustiva. SógravaçõesChatgpt; fontes/gateintocados. Manifesto FULL_SCOPE_AUDIT_MANIFEST.json. Proposta de correção para memóriascanônicas porgerência.
'''
backups=[]
for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PROPOSTA_MEMORIA_ATLAS.md'):
    p=root/name
    backups.append(c.backed_replace(p,p.read_bytes()+addition.encode('utf-8')))
tunnel=work/'TUNEL/DO_CHATGPT/AUDITORIA_ALVO_COMPLETO_20260916.md'
c.atomic(tunnel,f'''# Auditoria documental do alvo completo

{c.NOW}. Não acrescenta provas ou flags. A representação073 atualiza P0, mas não transforma o estado formal condicional072 em uma QFT interagente UV completa. Essa diferença deve ser preservada no índice/artigo do motor.

- [Auditoria requisito por requisito](../../DIAMANTE_MODULAR_20260916/AUDITORIA_DO_ALVO_COMPLETO.md)
- [Manifesto](../../DIAMANTE_MODULAR_20260916/FULL_SCOPE_AUDIT_MANIFEST.json)

Não reabrir torre/core/GNS; não contar novos controles lineares como solução da obrigação interagente. Gate e fontes intactos.
''')
names=('AUDITORIA_DO_ALVO_COMPLETO.md','MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md',
       'PROPOSTA_MEMORIA_ATLAS.md','record_full_scope_audit.py')
artifacts=[c.pin(root/n) for n in names]+[c.pin(tunnel)]
assert [c.pin(p) for p in source_paths]==sources
manifest=dict(timestamp=c.NOW,artifacts=artifacts,backups=backups,sources=sources,canonical_read_only=canonical,
              classification='DOCUMENTARY_PROGRESS_NOT_NEW_THEOREM',goal_status='ACTIVE',goal_complete=False,
              gate_changed=False,question_pending='EXPANSION_PARAMETER',
              source_read_scope={'Fock073':'opening_contract_only','index':'section4b_and_context',
                                 'canonical':'named_functions_source_not_runtime',
                                 '072':'full_text_in_chunks_with_tail_reread',
                                 'commutant073':'full_text'},
              unverified_requirements=['INTERACTING_UV_PHYSICAL_STATE','COMPLETE_REGIONAL_CHARGE','PHYSICAL_R1'])
c.atomic(root/'FULL_SCOPE_AUDIT_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for entry in artifacts+backups+sources: assert c.pin(Path(entry['path']))==entry
print(json.dumps({'status':'AUDIT_RECORDED','complete':False,'question_pending':True,'artifacts':len(artifacts),'backups':len(backups)}))
