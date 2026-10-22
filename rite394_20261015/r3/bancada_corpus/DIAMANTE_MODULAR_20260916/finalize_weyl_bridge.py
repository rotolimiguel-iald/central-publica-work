"""Finalize the scoped Weyl handoff, with immediate byte backups."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
NOW = datetime.now().astimezone().isoformat()


def pin(path):
    data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def atomic(path, data, replace=False):
    path.resolve().relative_to(WORK.resolve())
    if path.exists() and not replace:
        raise FileExistsError(path)
    if isinstance(data, str):
        data = data.encode('utf-8')
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    with os.fdopen(fd, 'wb') as stream:
        stream.write(data)
    assert Path(tmp).read_bytes() == data
    os.replace(tmp, path)
    assert path.read_bytes() == data


def backed_replace(path, data):
    previous = path.read_bytes()
    backup = path.with_name(path.name+'.bak_'+STAMP)
    atomic(backup, previous)
    if isinstance(data, str):
        data = data.encode('utf-8')
    assert len(data) >= len(previous), 'Only expansions/appends expected'
    atomic(path, data, replace=True)
    return pin(backup)


def main():
    audit = json.loads((ROOT/'REGIONAL_STATE_SOURCE_AUDIT.json').read_text(encoding='utf-8'))
    sources = [Path(item['path']) for item in audit['sources_before_finalize']]
    before = [pin(p) for p in sources]
    assert before == audit['sources_before_finalize'], 'Source changed: inspect before reuse'
    canonical_before = pin(Path(audit['canonical_current']['path']))
    assert canonical_before == audit['canonical_current'], 'Canonical advanced: inspect first'
    proof = ROOT/'TESTE_GEOMETRICO_WEYL_ESTADO_067.md'
    reviewed = pin(proof)
    text = proof.read_bytes().decode('utf-8')
    marker = 'Se essa transformação fosse o fluxo modular'
    assert text.count(marker) == 1
    text = text.replace(marker, r'''**Hipótese em operadores limitados.** Para cada teste tensorial real compacto q no diamante, use o unitário de Weyl \(W_{\mathcal C}(s q)=\exp[i s\mathcal C(q)]\), que pertence à álgebra regional porque \(\mathcal C\) é um campo linear local físico. A identificação proposta exige \(\sigma_t^\omega(W_{\mathcal C}(s q))=W_{\mathcal C}(s T_tq)\), onde Tt é o transporte dual do pullback tensorial, incluindo a transformação da densidade de teste. Na representação quase livre regular, as expectativas de produtos desses unitários são diferenciáveis nos parâmetros reais de teste; suas derivadas mistas recuperam a covariância de dois pontos e a identidade de Ward abaixo. Não é preciso presumir um domínio comum para os geradores não limitados.

Se essa transformação fosse o fluxo modular''')
    marker = 'Os setores S/V são ortogonais a esta leitura TT.'
    text = text.replace(marker, r'''Curl é formalmente autoadjunto nos tensores TT reais da esfera sem bordo: integração por partes e a antissimetria de epsilon dão \(\langle U,\operatorname{curl}V\rangle=\langle\operatorname{curl}U,V\rangle\). Portanto \(\langle S_n,\tfrac12\operatorname{curl}Y_m\rangle=\delta_{nm}\) numa base ortonormal que respeita as degenerescências. Os setores S/V são ortogonais a esta leitura TT: sua contribuição tem traços e gradientes simetrizados, cuja contração integrada com um TT se anula por traço zero e divergência zero.''')
    text = text.replace('Em termos de derivações, a diferença atua em algum observável local.',
                        'A conclusão segura é a desigualdade dos fluxos em algum unitário de Weyl local. Se houver um domínio comum invariante no qual ambos os geradores implementem derivações, então a diferença dessas derivações também não pode se anular em todo esse domínio gerador; essa afirmação adicional depende do domínio, não presumido aqui.')
    text += '\n\n## Revisão independente incorporada\n\nO parecer favorável, com alcance e leituras, está em REVISAO_INDEPENDENTE_WEYL.md. As precisões sobre unitários limitados, domínio de derivações e autoadjunticidade de curl foram incorporadas antes desta entrega. Não foi compilação Lean.\n'
    backups = [backed_replace(proof, text)]
    subprocess.run([sys.executable, str(ROOT/'verify_weyl_ward.py')], check=True)
    review = f'''# Revisão independente — teste Weyl e critério espectral

{NOW}. Revisor Goodall, id `01a0abfc-54d8-7e31-a623-32bc927ed3a2`, separado do autor. Parecer recebido por ferramenta; não alterou fontes nem reexecutou os controles.

**[DERIVED — parecer matemático, não Lean]** Favorável às duas provas no alcance declarado. Não encontrou erro fatal.

Confirmou a derivada do modo reconstruído; cálculo de C(1,3) no cilindro; curl-curl e isolamento TT; exclusão S/V por integração por partes; cone analítico da covariância e continuação da identidade de Ward; SO(4), centros antipodais e conclusão estritamente para peso adicional zero, sem misturas e L≠π/2. Confirmou também a prova condicional por Fubini de que hD sem espectro pontual implica centralizador Fock escalar. Essa hipótese continua OPEN para o estado 067.

**Precisão exigida antes da entrega:** formular a hipótese geométrica nos unitários exp(i s C(q)), com transporte dual dos testes. A regularidade quase livre permite recuperar a Ward por derivação das expectativas; não se presume domínio comum de campos/geradores não limitados. A redação sobre derivações também deveria explicitar o domínio. Pediu ainda explicitar a autoadjunticidade de curl para o isolamento do modo. As três precisões foram incorporadas. A conclusão de desigualdade de fluxos limitados é suficiente para a nota.

O revisor leu integralmente as duas notas, o script e o JSON, além das fontes pertinentes. O parecer não estabelece ação física de Kξ, espectro de δD, interação/UV, taxa de Lindblad ou coeficiente R1.

Pin medido da nota Weyl antes das precisões: `{reviewed['sha256']}` ({reviewed['bytes']} bytes). O manifesto conserva esse pin e o entregue. Prova do centralizador não foi alterada após o parecer.
'''
    atomic(ROOT/'REVISAO_INDEPENDENTE_WEYL.md', review)
    addition = f'''## {NOW} — teste Weyl da ação geométrica na referência 067

[DERIVED — revisão independente favorável, não Lean] Modos TT existentes dão W_n=A_n cosh(eta)cosh(eta')exp[-ip_n(eta-eta')]. Invariância modular pelo pullback tensorial ordinário de C(1,3), sem peso adicional/misturas, levaria via continuação analítica e centros antipodais a estacionariedade em tempo conforme, contradita por dlogV/deta=2tanh(eta). Escopo: mesmos estado linear067, fundo, diamantes interiores e L!=pi/2. Hipótese formulada em unitários de Weyl limitados; não pressupor domínio comum de geradores. Não é exclusão de toda ação geométrica: a leitura a*b_n é estacionária e foi controlada. Ação de Kxi renormalizado ainda precisa ser determinada.

[DERIVED — condicional] Ausência de espectro pontual de log(delta_D) implica centralizador Fock CI por Fubini e separação. Hipótese espectral OPEN para067; não usar standardness como substituto. No-go Weyl não localiza o observável detector no centralizador e 2tanh(eta) NÃO é R1 ou taxa física.

[REAL — controles] verify_weyl_ward.py passou em nove modo/tempo e quatro raios; controle falso de estacionariedade sem peso recusado e reescala estacionária preservada. Não são experimentos ou análise estatística. Nenhuma alteração de um.py, gate ou originais. Handoff desta etapa: HANDOFF_TESTE_WEYL_E_PONTE_FISICA.md; revisão REVISAO_INDEPENDENTE_WEYL.md; manifesto WEYL_BRIDGE_MANIFEST.json. Não duplicar pinching/torre já recebidos em v358. Meta ampla ativa; progresso efetivo, não impasse. Memórias canônicas recebem proposta pela gerência.
'''
    for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PROPOSTA_MEMORIA_ATLAS.md'):
        path = ROOT/name
        backups.append(backed_replace(path, path.read_bytes()+('\r\n\r\n'+addition).encode('utf-8')))
    tunnel = WORK/'TUNEL/DO_CHATGPT/ENTREGA_TESTE_WEYL_20260916.md'
    atomic(tunnel, f'''# Entrega — teste Weyl da ponte física

{NOW}. [DERIVED revisado, não Lean] Ação conforme tensorial ordinária sem peso adicional recusada no estado linear067, no alcance indicado. Não refaz PRODUCT_TOWER nem o pinching já aceito.

- [Handoff completo](../../DIAMANTE_MODULAR_20260916/HANDOFF_TESTE_WEYL_E_PONTE_FISICA.md)
- [Prova e hipóteses](../../DIAMANTE_MODULAR_20260916/TESTE_GEOMETRICO_WEYL_ESTADO_067.md)
- [Revisão independente](../../DIAMANTE_MODULAR_20260916/REVISAO_INDEPENDENTE_WEYL.md)
- [Manifesto](../../DIAMANTE_MODULAR_20260916/WEYL_BRIDGE_MANIFEST.json)

O fluxo modular local existe na realização construída. Ação geométrica completa, espectro regional e estado interagente/UV não foram inferidos desta obstrução. Gate canônico não alterado. Proposta de memória acompanha a entrega.
''')
    names = ['TESTE_GEOMETRICO_WEYL_ESTADO_067.md','CENTRALIZADOR_FOCK_E_ESPECTRO.md',
             'HANDOFF_TESTE_WEYL_E_PONTE_FISICA.md','REVISAO_INDEPENDENTE_WEYL.md',
             'verify_weyl_ward.py','WEYL_WARD_CHECKS.json','finalize_weyl_bridge.py',
             'MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PROPOSTA_MEMORIA_ATLAS.md']
    artifacts = [pin(ROOT/name) for name in names]+[pin(tunnel)]
    assert before == [pin(p) for p in sources]
    assert canonical_before == pin(Path(canonical_before['path']))
    manifest = dict(timestamp=NOW, artifacts=artifacts, backups=backups, sources=before,
                    canonical_unchanged=canonical_before, reviewed_proof=reviewed,
                    proof_delivered=pin(proof), review='FAVORABLE_WITH_PRECISIONS_INCORPORATED',
                    new_lean_theorems=0, gate_changed=False, classification='PROGRESS',
                    goal_status='ACTIVE', physical_interacting_UV_state='OPEN',
                    exact_geometric_modular_bridge='OPEN', physical_centralizer_spectrum='OPEN')
    atomic(ROOT/'WEYL_BRIDGE_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    link_count = 0
    for path in [ROOT/name for name in names[:4]]+[tunnel]:
        for href in re.findall(r'\]\(([^)\n]+)\)', path.read_text(encoding='utf-8')):
            if href.startswith(('https://','http://','#','\\')):
                continue
            assert (path.parent/href).is_file(), (path,href)
            link_count += 1
    for entry in artifacts+backups+before:
        assert pin(Path(entry['path'])) == entry
    print(json.dumps(dict(status='DELIVERED', artifacts=len(artifacts), backups=len(backups),
                          local_links=link_count, gate_changed=False), ensure_ascii=False))


if __name__ == '__main__':
    main()
