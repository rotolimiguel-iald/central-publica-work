"""Package the weighted Weyl obstruction using the existing custody helpers."""
import json
from pathlib import Path
import subprocess
import sys
import finalize_weyl_bridge as custody

ROOT, WORK, NOW = custody.ROOT, custody.WORK, custody.NOW
pin, atomic, backed_replace = custody.pin, custody.atomic, custody.backed_replace


def main():
    previous = json.loads((ROOT/'WEYL_BRIDGE_MANIFEST.json').read_text(encoding='utf-8'))
    sources = previous['sources']
    assert [pin(Path(p['path'])) for p in sources] == sources
    canonical = previous['canonical_unchanged']
    assert pin(Path(canonical['path'])) == canonical
    note = ROOT/'WEYL_ELETRICO_E_PESO_CONFORME.md'
    reviewed = pin(note)
    extension = '''

## Parecer e controles recebidos

A derivação do Weyl elétrico e a exclusão do peso escalar receberam conferência independente favorável de Goodall. O revisor explicitou a variação do fator métrico no termo Rg/6, confirmou o sinal na convenção da fonte e a necessidade de projetar TT somente depois da continuação e soma antipodal. O relato integral de escopo está em REVISAO_INDEPENDENTE_PESO_CONFORME.md. Isso é revisão escrita, não Lean.

O script verify_electric_weyl.py e ELECTRIC_WEYL_CHECKS.json registram controles de nove pares modo/tempo, incluindo três linearizações da curvatura exata de Bianchi IX para o harmônico homogêneo n=2. Nos outros modos, verificam derivadas temporais, normalização e razão de variâncias; não fingem testar uma geometria não linear que não foi implementada.
'''
    proof_text = note.read_bytes().decode('utf-8').replace(
        'Multiplicar ambos os modos pelo mesmo fator temporal',
        'Multiplicar ambos os modos pelo mesmo fator temporal não nulo')
    backups = [backed_replace(note, (proof_text+extension).encode('utf-8'))]
    subprocess.run([sys.executable,str(ROOT/'verify_electric_weyl.py')],check=True)
    atomic(ROOT/'REVISAO_INDEPENDENTE_PESO_CONFORME.md', f'''# Revisão independente — peso conforme do Weyl inteiro

{NOW}. Revisor Goodall, id `01a0abfc-54d8-7e31-a623-32bc927ed3a2`, separado do autor. Parecer recebido por ferramenta; fontes não foram editadas pelo revisor.

[DERIVED, não Lean] Conferência independente favorável do cálculo de curvatura e do argumento ponderado. Derivou δR0i0j=t''/2, δRicij=(t''−Δt+6t)/2, δRic00=δR=0; a variação de (R/6)gij fornece +t. Logo E=(t''+Δt−2t)/4 na convenção da fonte066. Confirmou o modo elétrico, hbar na variância e derivada positiva. Confirmou que o magnético força w=1 e o elétrico contradiz esse peso. O termo wψ, analítico de ordem zero, conserva o argumento de continuação.

Confirmou a ortogonalidade S/V à leitura TT e ressaltou a ordem: continuar a Ward tensorial, somar centros, somente então projetar globalmente. A hipótese é sobre os unitários de Weyl dos campos suavizados. Não presumir domínios de comutadores ilimitados.

Alcance: família Lie+wψ com w constante real, sem misturas, no estado067 e diamantes especificados com L!=pi/2. Não determina o Kxi físico nem a teoria interagente/UV. O manifesto conserva o pin da nota antes do adendo deste parecer: `{reviewed['sha256']}`.

Em segunda conferência, o revisor leu integralmente a nota, o script e o JSON, conferiu seus três hashes e validou a independência do controle Bianchi IX: sem reutilizar a fórmula linear, obtém δRic3_11=6t e δC0101=(t''−8t)/4 para n=2. O controle cobre uma componente real homogênea em três tempos, não todos os harmônicos ou uma solução não linear Einstein–sigma. Considerou o alcance honesto e sem correção impeditiva. Sugeriu acrescentar “não nulo” ao fator de reescala comum; a explicitação foi incorporada.

Os controles foram executados pelo autor, com resultado em ELECTRIC_WEYL_CHECKS.json. A revisão matemática e a conferência dos hashes pelo revisor não devem ser descritas como uma nova execução independente dos controles.
''')
    addition=f'''## {NOW} — peso conforme escalar testado no Weyl inteiro

[DERIVED — conferência independente, não Lean] A família DxiC=Lie_xi C+w psi_g C, w constante real comum, é excluída no estado linear067 e nos diamantes interiores com L!=pi/2. O magnético obriga w=1, mas Var(aE_n)=hbar c_n²[p_n²(lambda_n+6)²+16tanh²eta] tem derivada positiva. Weyl elétrico calculado antes de usar EOM: E=(t''+Delta_gamma t−2t)/4. Corrige ao lado o espaço de possibilidades da nota anterior: a*b magnético permanece estacionário, mas não conserva simultaneamente o elétrico. Não é proibição de ações com misturas/outros termos e não identifica Kxi renormalizado.

[REAL — execução] Nove pares modo/tempo passaram; três controles usam curvatura não linear Bianchi IX diagonal e recuperam o harmônicoTT n2 por diferenças centrais. Nenhum número é sigma experimental/R1/taxaLindblad. Ponte dephasing–torre não foi refeita. Handoff: HANDOFF_ADENDO_PESO_CONFORME.md; prova WEYL_ELETRICO_E_PESO_CONFORME.md; manifesto ELECTRIC_WEYL_MANIFEST.json. Originais e gate intocados, meta ampla ativa. Rodada anterior classificada PROGRESS; rodada atual também produz nova evidência, sem impasse. Memórias canônicas recebem proposta pela gerência.
'''
    for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PROPOSTA_MEMORIA_ATLAS.md'):
        path=ROOT/name
        backups.append(backed_replace(path,path.read_bytes()+('\r\n\r\n'+addition).encode('utf-8')))
    tunnel=WORK/'TUNEL/DO_CHATGPT/ENTREGA_PESO_CONFORME_WEYL_20260916.md'
    atomic(tunnel,f'''# Entrega — peso conforme escalar e Weyl inteiro

{NOW}. [DERIVED revisado, não Lean] Amplia o teste anterior de w=0 para todo peso escalar constante comum. O peso que torna o magnético estacionário falha no elétrico. Não refaz torre ou motor.

- [Handoff](../../DIAMANTE_MODULAR_20260916/HANDOFF_ADENDO_PESO_CONFORME.md)
- [Prova](../../DIAMANTE_MODULAR_20260916/WEYL_ELETRICO_E_PESO_CONFORME.md)
- [Manifesto](../../DIAMANTE_MODULAR_20260916/ELECTRIC_WEYL_MANIFEST.json)

Restrito ao estado067, diamantes especificados e ação Lie+wψ sem misturas. Kxi físico e UV permanecem OPEN. Gate não alterado.
''')
    names=('WEYL_ELETRICO_E_PESO_CONFORME.md','HANDOFF_ADENDO_PESO_CONFORME.md',
           'verify_electric_weyl.py','ELECTRIC_WEYL_CHECKS.json','REVISAO_INDEPENDENTE_PESO_CONFORME.md',
           'finalize_electric_weyl.py','MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PROPOSTA_MEMORIA_ATLAS.md')
    artifacts=[pin(ROOT/n) for n in names]+[pin(tunnel)]
    assert [pin(Path(p['path'])) for p in sources]==sources
    assert pin(Path(canonical['path']))==canonical
    manifest=dict(timestamp=NOW,artifacts=artifacts,backups=backups,sources=sources,
                  canonical_unchanged=canonical,reviewed_note=reviewed,delivered_note=pin(note),
                  review='FAVORABLE_SCOPED_MATHEMATICAL',new_lean_theorems=0,gate_changed=False,
                  goal_status='ACTIVE',previous_turn='PROGRESS',current_turn='PROGRESS',
                  physical_geometric_action='OPEN',interacting_UV_completion='OPEN')
    atomic(ROOT/'ELECTRIC_WEYL_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    for p in artifacts+backups:
        assert pin(Path(p['path']))==p
    print(json.dumps(dict(status='DELIVERED',artifacts=len(artifacts),backups=len(backups),gate_changed=False)))


if __name__=='__main__':
    main()
