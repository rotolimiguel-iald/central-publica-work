"""Incorporate the final reviewer precisions without losing the prior receipt."""
import json
import subprocess
import sys
from pathlib import Path
import finalize_weyl_bridge as c

root=c.ROOT
manifest_path=root/'CHARGE_ORDER_MANIFEST.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
proof=root/'CARGA_RELACIONAL_E_ORDEM_DOS_CAMPOS.md'
text=proof.read_text(encoding='utf-8')
text=text.replace('É uma identidade local linear off-shell na categoria de fundos em que F está definido.',
                  'É uma identidade local linear off-shell nas perturbações, no fundo especificado e no interior onde F existe. A expressão geral sob δW=δX=0 é −c X̄H/2; o coeficiente 3c/(2a²) usa este fundo.')
text=text.replace('O fluxo modular construído anteriormente age como W(f)↦W(S_sf), pela segunda quantização do operador modular de uma partícula.',
                  'O fluxo modular construído anteriormente age como W(v)↦W(S_sv), com S_s=δ_D^(is) sobre o subespaço real fechado L(D) de uma partícula. Aqui v é o vetor de uma partícula associado ao teste, ou seu limite em L(D). Não foi demonstrado que S_s preserve a classe original de testes suaves compactos; a segunda quantização fornece o fluxo na álgebra de von Neumann.')
new_backups=[c.backed_replace(proof,text)]
review=root/'REVISAO_INDEPENDENTE_CARGA.md'
add='''

Conferência final da redação/script/JSON: favorável, sem erro fatal. O revisor pediu duas precisões incorporadas: o fator 3c/(2a²) usa o fundo especificado (a identidade geral é −c Xbar H/2); o fluxo de uma partícula age no subespaço real fechado L(D), sem afirmar preservação da classe original de testes compactos. Conferiu os dois hashes então correntes e o conteúdo dos três perfis; não reexecutou o script. Não há mudança das conclusões ou promoção do escopo.
'''
new_backups.append(c.backed_replace(review,review.read_bytes()+add.encode('utf-8')))
subprocess.run([sys.executable,str(root/'verify_charge_orders.py')],check=True)
memory='\n\n'+c.NOW+' — Precisões finais do parecer da carga: coeficiente 3c/(2a²) restrito ao fundo especificado; fórmula geral −c Xbar H/2. Fluxo modular em L(D) fechado, sem supor preservação de testes suaves compactos. Redação e revisão corrigidas ao lado, controles reexecutados; escopo e gate inalterados.\n'
for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PROPOSTA_MEMORIA_ATLAS.md'):
    p=root/name
    new_backups.append(c.backed_replace(p,p.read_bytes()+memory.encode('utf-8')))
manifest['artifacts']=[c.pin(Path(p['path'])) for p in manifest['artifacts']]+[c.pin(Path(__file__))]
manifest['backups']+=new_backups
manifest['clarifications']={'timestamp':c.NOW,'reviewer_precisions':'SPECIFIED_BACKGROUND_AND_COMPLETED_REAL_SUBSPACE','checks_rerun':True}
backup_manifest=c.backed_replace(manifest_path,json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for entry in manifest['artifacts']+manifest['backups']:
    assert c.pin(Path(entry['path']))==entry
print(json.dumps({'status':'REVIEW_PRECISIONS_INCORPORATED','manifest_backup':backup_manifest['path'],'artifacts':len(manifest['artifacts'])}))
