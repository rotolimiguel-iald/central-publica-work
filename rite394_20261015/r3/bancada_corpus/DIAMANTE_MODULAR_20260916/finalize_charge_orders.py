"""Record the charge-order audit without modifying the canonical motor."""
import json
from pathlib import Path
import subprocess
import sys
import finalize_weyl_bridge as custody

ROOT,WORK,NOW=custody.ROOT,custody.WORK,custody.NOW
pin,atomic,backup=custody.pin,custody.atomic,custody.backed_replace


def main():
    old=json.loads((ROOT/'ELECTRIC_WEYL_MANIFEST.json').read_text(encoding='utf-8'))
    sources=old['sources']; canonical=old['canonical_unchanged']
    assert [pin(Path(p['path'])) for p in sources]==sources
    assert pin(Path(canonical['path']))==canonical
    proof=ROOT/'CARGA_RELACIONAL_E_ORDEM_DOS_CAMPOS.md'
    reviewed=pin(proof)
    addition='''

## Conferência independente e controles

Goodall conferiu independentemente as duas derivações e a ação CCR, com parecer favorável. Ressaltou o smearing congelado, o domínio interior de F, a condição de admissibilidade do campo suavizado e a distinção entre coeficiente de epsilon² e segunda derivada. Essas condições estão explícitas no texto. O parecer não constrói a carga completa ou seu operador renormalizado.

verify_charge_orders.py executou três perfis de métrica/perturbação e controles de fase CCR. A variação por diferenças finitas da tensão completa confirmou (1); a expansão de inversa vezes determinante confirmou o fator 1/4 de (3) e recusou sua substituição pelo fator obtido omitindo a medida. Os controles são finitos, não a quantização da carga regional.
'''
    backups=[backup(proof,proof.read_bytes()+addition.encode('utf-8'))]
    subprocess.run([sys.executable,str(ROOT/'verify_charge_orders.py')],check=True)
    atomic(ROOT/'REVISAO_INDEPENDENTE_CARGA.md',f'''# Revisão independente — tensão vestida e ordens da carga

{NOW}. Revisor Goodall, id `01a0abfc-54d8-7e31-a623-32bc927ed3a2`. [DERIVED — conferência matemática, não Lean].

Confirmou off-shell deltaTrel=3c H/(2a²), usando naturalidade e P088. Confirmou que a carga com smearing de fundo congelado é linear e que sua ação CCR desloca os campos; a invariância do estado centrado exige emparelhamento simplético zero com os testes regionais. Não se pode concluir v=0 globalmente. No TT puro a carga linear não lê as componentes temporais.

Conferiu o caminho g_epsilon com sigma fixo, a normal, a medida e a expansão: coeficiente de epsilon² = pi c a²/4 integral f tr(t²), cuja segunda derivada é o dobro. Não há momentos nesse funcional. Destacou que não é a carga física completa quadrática sem dressing, região, restrições, contribuições gravitacionais/fronteira e quantização renormalizada correspondentes. Grau quadrático permite ação linear, mas não garante modularidade.

Nenhum arquivo foi alterado pelo revisor. Os controles computacionais foram executados pelo autor, não atribuídos ao revisor. Pin da nota antes deste registro: `{reviewed['sha256']}`.
''')
    handoff='''# Adendo ao handoff — a carga precisa conservar sua ordem nos campos

16/09/2026. [DERIVED revisado, não Lean]. A tensão vestida de primeira ordem foi derivada usando F/P já existentes: deltaTrel=3c H/(2a²). Não pedir outro extrator. Uma carga formada somente por esse termo é linear e gera deslocamento de Weyl; sua ação não trivial não preserva o estado quase livre centrado. Ela não substitui o gerador modular quadrático.

A [nota completa](CARGA_RELACIONAL_E_ORDEM_DOS_CAMPOS.md) também calcula o coeficiente quadrático de matéria num caminho TT explicitamente fixado, incluindo a medida. Esse controle não é a carga relacional/renormalizada completa. O próximo fornecedor deve identificar o funcional quadrático completo no quociente físico e na região definida pelos mesmos relógios, com contribuições gravitacionais e de fronteira pertinentes. A cinética já está na ação TT existente; não criar outra ação pelo nome.

Nos leitores existentes, distinguir tensão de fundo, primeira variação vestida, controle de matéria de segunda ordem e carga completa. Não promover nenhum dos três primeiros a Kxi modular. Não acrescentar outro pinching ou reabrir PRODUCT_TOWER. O contrato de confronto permanece k T_s f = delta_D^(is) kf, após definir T_s pela carga física.

- [Revisão independente](REVISAO_INDEPENDENTE_CARGA.md)
- [Controles](CHARGE_ORDER_CHECKS.json)
- [Manifesto](CHARGE_ORDER_MANIFEST.json)

Originais e gate intocados. Sem estado físico interagente UV completo ou coeficiente R1 inferido. Atualização canônica de Atlas, índice, diário e desenho deve transportar estes estatutos; a proposta local recebeu backup imediato.
'''
    atomic(ROOT/'HANDOFF_ADENDO_ORDEM_DA_CARGA.md',handoff)
    memory=f'''## {NOW} — ordem dos campos na carga geométrica

[DERIVED revisado, não Lean] Com os dados066/088, deltaTrel=deltaT−Lie_F Tbar=3cH/(2a²), offshellinterior. A carga de smearingcongelado desse termo é linear e gera deslocamentoCCR; para preservar referênciaGaussian centrada deve agir trivialmente nos testesregionais. TTpureH0mu0 nãoé lido porQ1. Não confundir essa Q1 com geradormodularquadrático.

[DERIVED/REAL] CaminhoTT fixogε,phi=id,fatia eξcongelados: Qmatter=Q0+ε² pi c a²/4 integral f tr(t²)+O(ε³). Coeficiente inclui medida; nãoésegunda derivada nemcargarelacionalcompleta. Trêsperfis numéricos e faseCCR conferidos; omissão medida recusada. Dressing/relógios/região2ªordem, restrições, carga gravitacional/fronteira e operadorrenormalizado precisam composição; não pedir de novo ação/extratorjá existentes.

Handoff HANDOFF_ADENDO_ORDEM_DA_CARGA.md; prova CARGA_RELACIONAL_E_ORDEM_DOS_CAMPOS.md; manifesto CHARGE_ORDER_MANIFEST.json. Memórias locais com backupbytes; fontes e gateintocados. RodadaanteriorPROGRESS; atualPROGRESS por novaidentificaçãofuncional. Metaamplaativa, estadointeragenteUV e R1físicoaindaOPEN.
'''
    for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PROPOSTA_MEMORIA_ATLAS.md'):
        path=ROOT/name
        backups.append(backup(path,path.read_bytes()+('\r\n\r\n'+memory).encode('utf-8')))
    tunnel=WORK/'TUNEL/DO_CHATGPT/ENTREGA_ORDEM_DA_CARGA_20260916.md'
    atomic(tunnel,f'''# Entrega — ordem da carga

{NOW}. [DERIVED revisado, não Lean] Tensão vestida linear e coeficiente quadrático de matéria em caminho fixado, com distinção explícita da carga completa.

- [Handoff](../../DIAMANTE_MODULAR_20260916/HANDOFF_ADENDO_ORDEM_DA_CARGA.md)
- [Manifesto](../../DIAMANTE_MODULAR_20260916/CHARGE_ORDER_MANIFEST.json)

Não criar novo extrator/pinching ou substituir Kxi por uma carga linear. Gate não alterado.
''')
    names=('CARGA_RELACIONAL_E_ORDEM_DOS_CAMPOS.md','verify_charge_orders.py','CHARGE_ORDER_CHECKS.json',
           'REVISAO_INDEPENDENTE_CARGA.md','HANDOFF_ADENDO_ORDEM_DA_CARGA.md','finalize_charge_orders.py',
           'MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PROPOSTA_MEMORIA_ATLAS.md')
    artifacts=[pin(ROOT/name) for name in names]+[pin(tunnel)]
    assert [pin(Path(p['path'])) for p in sources]==sources
    assert pin(Path(canonical['path']))==canonical
    manifest=dict(timestamp=NOW,artifacts=artifacts,backups=backups,sources=sources,canonical_unchanged=canonical,
                  review='FAVORABLE_SCOPED',new_lean_theorems=0,gate_changed=False,goal_status='ACTIVE',
                  previous_turn='PROGRESS',current_turn='PROGRESS',full_physical_charge='OPEN',
                  physical_interacting_UV_state='OPEN',first_physical_noncentral_coefficient='OPEN')
    atomic(ROOT/'CHARGE_ORDER_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    for entry in artifacts+backups: assert pin(Path(entry['path']))==entry
    print(json.dumps(dict(status='DELIVERED',artifacts=len(artifacts),backups=len(backups),gate_changed=False)))


if __name__=='__main__': main()
