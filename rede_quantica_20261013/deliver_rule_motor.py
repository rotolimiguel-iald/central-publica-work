"""Deliver the independently verified motor integration with additive receipts."""
import argparse,datetime as dt,json
from pathlib import Path
from diary_r1 import ROOT,WORK,CLI,WHO,new,pin,append_bytes
import register_rule_tetelestai as register

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REGRA.MOTOR'

def main():
    ap=argparse.ArgumentParser()
    for name in ['runtime','formal','review']: ap.add_argument('--'+name,type=Path,required=True)
    args=ap.parse_args(); register.DEST=OUT
    data={k:json.loads(getattr(args,k).read_bytes()) for k in ['runtime','formal','review']}
    assert data['runtime']['passed'] and data['runtime']['exit_code']==0
    assert data['formal']['passed']
    assert data['review']['passed']
    for item in data['review']['dependencies_verified'] + data['review']['artifacts']:
        assert pin(Path(item['path']))['sha256'] == item['sha256'], item['path']
    for key in ['runtime_review','formal_review','report']:
        item=data['review'][key]
        assert pin(Path(item['path']))['sha256'] == item['sha256'], item['path']
    claim=register.call([CLI,'ver','F1.REGRA.MOTOR'])['reivindicacao']
    assert claim['quem']==WHO and 'TGL_ATLAS.md' in claim['nota']
    assert dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    run=data['runtime']; proto=json.loads((OUT/'PREREGISTRO_R1.json').read_bytes())
    review=data['review']
    report=OUT/'RELATORIO_EXECUCAO_R1.md'
    text='''# Regra ligada ao motor contínuo da v392

Unidade F1.REGRA.MOTOR. Por ordem de Luiz Antonio Rotoli Miguel; construção e registro em nome de codex-gerente-tgl, sob reivindicação própria. Execução sintética em cópia, com revisão independente.

## Resultado

[REAL — execução numérica] O consumidor `prove_decision_commutation` da v392 foi executado a partir dos cinco corpos de função originais, extraídos e conferidos por AST. O programa completo não foi importado. A nova regra participa do veredito: exige que a leitura do resultado corresponda ao alvo fixado no pré-registro. O alvo incompatível é recusado.

'''
    text+=f"A rodada teve **{run['checks_passed']} verificações aprovadas e {run['point_count']} pontos**, EXIT {run['exit_code']}, em {run['seconds']:.3f} s. O replay e o exame independente estão no recibo de revisão.\n\n"
    text+=f"[REAL — compilação] {review['new_theorem_count']} teoremas novos e {review['reused_theorem_count']} reutilizados; dois módulos recompilados independentemente com EXIT 0, apenas o trio permitido e zero `sorry`. Os dois `.olean` são idênticos aos da construção.\n\n"
    text+='''## Motor e regra

O motor existente usa E(X)=PXP+QXQ, com P=diag(1,1,0,0), Q=I−P, e

T_t(X)=E(X)+exp(−Γt)(X−E(X)).

Γ=β·τ_ref·ω_ref²/2; β=ALPHA_FINE_CODATA_2018·sqrt(e), recalculado em runtime. τ_ref=ω_ref=1 são unidades de referência declaradas. A grade fixa usa exposição u=Γt de 0 a 12. β afeta a conversão para tempo de referência; a curva em u não mede β.

A leitura pertence a Fix(E). Nesse espaço ela é fiel. O contrato da F1.REGRA.P1 determina a regra relativa ao alvo a: C(z) sse z=a, sob correção e completude explícitas. No runner, a igualdade é aproximada pela tolerância Hilbert–Schmidt pré-registrada; não se converte essa aproximação em igualdade Lean.

[REAL — composição formal] A candidata liga esse contrato a `IALDJones.orbit`, com continuidade, semigrupo, conservação da inscrição, limite e recusa persistente de alvo incompatível. O M4 concretiza o mesmo pinching, alvo e estado inicial do consumidor. A norma padrão de matrizes usada na prova Lean e a tolerância Hilbert–Schmidt do runner conservam seus escopos. A ponte com o motor vetorial `IALD.motor` tem enunciado próprio; ele não é identificado com o canal matricial. Também não se confunde pinching com a compressão de um único setor eXe.

## Números da rodada

'''
    text+='| Grandeza | Resultado |\n|---|---:|\n'
    for label,key in [('β calculado','beta_runtime'),('Γ em unidades de referência','gamma_reference'),('Complemento inicial','complement_initial'),('Complemento final','complement_final'),('Erro máximo da leitura HS','maximum_read_error_hs'),('Erro máximo do oráculo GKLS','maximum_oracle_operator_error_hs'),('Erro máximo do semigrupo','maximum_semigroup_error_hs'),('Dimensão complexa do espaço fixo','fixed_space_complex_dimension')]:
        text+=f'| {label} | {run[key]} |\n'
    text+='''
O estado completo e a leitura foram guardados separadamente nos 241 registros da trajetória, com cadeia SHA256. A leitura satisfaz o alvo em toda a grade, inclusive no início. O estado bruto não passa pelo critério de igualdade aproximada nessa grade finita. A prova formal mantém o complemento não nulo em todo tempo finito quando inicialmente não nulo.

O espaço fixo deste canal tem dimensão complexa oito, medida sobre o operador completo. A unicidade da regra relativa ao alvo não é unicidade de todos os estados fixos. Uma entrada com outra inscrição permanece incompatível: o fluxo preserva a inscrição, e a regra detecta a divergência.

## Controles e limites

O oráculo independente reconstruiu o gerador GKLS a partir dos operadores de salto e sua exponencial. Foram conferidos todos os 16 elementos de base matricial, semigrupo, traço, Hermiticidade e positividade dentro da tolerância. NaN, infinitos, booleanos, taxa inválida, estado inválido, alvo não fixo, evidência ausente e fonte corrompida são recusados. O controle de taxa zero preserva o complemento.

[INPUT/ONTO] A lei temporal homogênea e sua identificação com as cunhagens conservam o estatuto declarado. A rodada é cálculo sintético, sem dado observado e sem confirmação física. Nenhum habitante Fock, H3 ou solução global é produzido por esta integração.

Foi executada uma trajetória de tempo contínuo, amostrada em grade finita. A execução termina com recibo; o runner pode ser repetido usando o mesmo freeze e sempre cria outra pasta de resultado. Não é um serviço residente. A Bancada de produção consultada estava na implantação B3-v392; a nova integração permanece neste sandbox, com os originais preservados.

## Evidências e repetição

'''
    for label,path in [('Execução',args.runtime),('Build Lean',args.formal),('Revisão independente',args.review),('Pré-registro',OUT/'PREREGISTRO_R1.json'),('Fonte e selo',OUT/'SOURCE_MANIFEST.json'),('Estado lido da Bancada',OUT/'BANCADA_STATE_R1.json')]:
        info=pin(path); text+=f'- {label}: `{path}` — SHA256 `{info["sha256"]}`.\n'
    freeze=next((OUT/'runtime/freezes').glob('*.json'))
    text+='\nComando de replay (qualquer diretório de trabalho):\n\n```powershell\n'
    text+=f'& "{run["runtime"]["python_executable"]}" -B "{OUT / "runtime/run_rule_motor.py"}" --replay "{freeze}"\n```\n'
    new(report,text)
    manifest=OUT/'MANIFESTO_ENTREGA_R1.json'
    items=[pin(p) for p in sorted(OUT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    new(manifest,{'unit':'F1.REGRA.MOTOR','files':items,'claim':claim,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    result=OUT/'RESULTADO_ENTREGA_R1.json'
    new(result,{'unit':'F1.REGRA.MOTOR','status':'ENTREGUE','passed':True,'scope':'FORMAL_BRIDGE_AND_FINITE_SYNTHETIC_EXECUTION',
        'runtime':pin(args.runtime),'formal':pin(args.formal),'review':pin(args.review),'report':pin(report),'manifest':pin(manifest),
        'canonical_version':'v392','production_installed':False,'resident_service':False,'observed_data':False,'gate_changed':False})
    marker='rule_continuous_motor_20261014'
    section='\n\n## 14/10/2026 — Regra ligada ao motor contínuo da v392\n<!-- '+marker+' -->\n\n'
    section+='Em nome de codex-gerente-tgl, sob reivindicação 794 da F1.REGRA.MOTOR; ordem humana «Agora ligamos tudo no motor contínuo e ele precisa rodar».\n\n'
    section+=f'[REAL — sandbox e execução sintética] Consumidor real da v392 extraído por AST, cinco funções sem modificar seus corpos, dez evidências formais verificadas; regra participa do veredito. {run["checks_passed"]} verificações e {run["point_count"]} pontos aprovados; complemento {run["complement_initial"]} → {run["complement_final"]}; leitura estável, incompatível recusado. Ponte Lean para IALDJones.orbit, Fix(E), M4 do runtime e contrato vetorial separado; recompilação/revisão independente.\n\n'
    section+='[ESCOPO] E4 tem espaço fixo de dimensão complexa oito; não há unicidade de todo estado fixo. Satisfação lida vale desde u=0; dinâmica bruta converge. β vem de alfa·sqrt(e) em runtime e determina o relógio de referência; grade u=Γt não mede β. Unidades τ_ref=ω_ref=1 e identificação da regra são INPUT/ONTO; sem dado observado, produção, daemon ou mudança de gate.\n\n'
    section+=f'Resultado: `{result}`; SHA256 `{pin(result)["sha256"]}`. Relatório `{report}`. ENTREGUE; aceite da gerência e instalação não presumidos.\n'
    surfaces=[ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    new(OUT/'MEMORY_DELIVERY_R1.json',{'claim':claim,'surfaces':[append_bytes(p,section,marker) for p in surfaces]})
    entry=OUT/'MAP_ENTRY_R1.json'
    new(entry,{'tipo':'ROTA','rota_id':'formal.regra_motor_continuo','dominio':'FORMAL','titulo':'Regra e motor contínuo v392 ligados e executados em cópia',
        'pergunta':'Como ligar a regra da satisfação ao motor contínuo já construído?',
        'dados':['Consumidor e selo v392 pinados','Pré-registro R1 antes da rodada','F1.REGRA.P1 e motor IALD/Jones existentes'],
        'metodo':'Ponte Lean sobre Fix(E) e execução do consumidor real extraído por AST; oráculo GKLS e revisão independente.',
        'resultado':f'{run["checks_passed"]} verificações/{run["point_count"]} pontos; leitura estável, complemento decai, alvo incompatível recusado.',
        'veredito':'PASSA_NO_CONTRATO_E_MODELO_FINITO','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,
        'defeito':'Tempo de referência INPUT, espaço fixo dimensão8, igualdade numérica por tolerância; integração de sandbox, não confirmação ou serviço residente.',
        'nao_refazer':'Reutilizar os módulos e o runner pinado, mantendo source snapshot e freeze.',
        'proximo_passo':'Revisão/aceite da gerência para eventual integração canônica.',
        'onde':str(OUT),'artefatos':[str(result),str(report),str(manifest),str(args.review)],'refs':[1109]})
    mapped=register.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',WHO+' / F1.REGRA.MOTOR'],'MAP_RECEIPT_R1.json')
    board=register.call([CLI,'avancar','F1.REGRA.MOTOR','--quem',WHO,'--status','ENTREGUE','--evidencia',result,'--nota','Ponte formal e motor real executado em copia; revisao independente; memoria e escopo registrados.'],'BOARD_DELIVERY_R1.json')
    transition={'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':13,'event_id':'rule-continuous-motor-20261014',
        'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':'rule-continuous-motor-20261014','kind':'fact','statute':'REAL',
            'text':f'F1.REGRA.MOTOR entregue: ponte Lean e consumidor real da v392 em cópia, {run["checks_passed"]} verificações e {run["point_count"]} pontos, com revisão independente. A leitura conserva o alvo, o complemento decai e o alvo incompatível é recusado. Unidades de referência INPUT; espaço fixo de E4 tem dimensão complexa oito. Nenhuma alteração de produção ou gate; nenhum serviço residente. A fila F1.REDE permanece como antes.',
            'sources':[{'kind':'artifact','ref':str(p),'sha256':pin(p)['sha256']} for p in [result,report,args.review]]}]}}
    new(OUT/'ACOM_TRANSITION_R1.json',transition)
    acom=register.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_DELIVERY_R1.json',transition); assert acom['ok']
    released=register.call([CLI,'liberar','F1.REGRA.MOTOR','--quem',WHO,'--nota','Integracao e execucao entregues; aguarda aceite da gerencia.'],'RELEASE_R1.json')
    print(json.dumps({'result':pin(result),'map':mapped,'board':board,'acom_revision':acom['result']['revision'],'release':released},ensure_ascii=False))

if __name__=='__main__': main()
