"""Deliver the verified sandbox proof with additive evidence and memory."""
import datetime as dt
import json
import re
import sys
from pathlib import Path
from diary_r1 import ROOT,WORK,PY,CLI,WHO,new,pin,append_bytes
import register_rule_tetelestai as register

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REGRA.P1'


def main():
    review=Path(sys.argv[1]).resolve()
    assert review.is_relative_to(OUT/'review')
    reviewed=json.loads(review.read_text(encoding='utf-8'))
    # The independent receipt schema is checked before invoking this script.
    assert reviewed.get('status') == 'PASS_FORMAL_SCOPE__CANDIDATE_FOR_MANAGEMENT', 'Independent review must pass explicitly'
    assert reviewed['input_pins_unchanged_after_build'] and reviewed['theorems']==60
    assert len(reviewed['builds'])==3
    assert all(m['exit_code']==0 and m['axioms_within_trio'] and m['axioms_match_constructor'] for m in reviewed['builds'])
    register.DEST=OUT
    claim=register.call([CLI,'ver','F1.REGRA.P1'])['reivindicacao']
    assert claim['quem']==WHO and 'TGL_ATLAS.md' in claim['nota']
    assert dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    candidates=sorted((OUT/'attempts').glob('*/RESULTADO_BUILD.json'))
    assert len(candidates)==1
    build_file=candidates[0]
    build=json.loads(build_file.read_text(encoding='utf-8'))
    assert build['passed'] and build['dependencies_unchanged']
    for module in build['modules']:
        assert module['exit_code']==0 and module['axioms_within_trio']
        source=OUT/'formal'/(module['module']+'.lean')
        assert pin(source)['sha256']==module['source']['sha256']
    sources=[OUT/'formal/RuleTruthContract.lean',OUT/'formal/TheRuleAndTheFigureOfTruth.lean']
    count=sum(len(re.findall(r'^theorem ',p.read_text(encoding='utf-8'),re.M)) for p in sources)
    assert count==60
    for p in sources:
        assert not re.search(r'\b(sorry|admit|sorryAx)\b',p.read_text(encoding='utf-8'))
    verbatim=json.loads((OUT/'VERBATIM_MANIFEST.json').read_text(encoding='utf-8'))
    main_text=sources[1].read_text(encoding='utf-8')
    for item in verbatim['sources']:
        p=Path(item['path'])
        assert pin(p)==item and p.read_text(encoding='utf-8') in main_text
    report=OUT/'PROVA_MATEMATICA_R1.md'
    principal=[*sources,OUT/'formal/RuleTruthAxioms.lean',OUT/'build_proof.py',build_file,
        review,OUT/'review/PARECER_ESCOPO_R1.md',report,OUT/'VERBATIM_MANIFEST.json',OUT/'NOS_VIVO.json',OUT/'MAPA.json']
    manifest=OUT/'MANIFESTO_PROVA_R1.json'
    new(manifest,{'unit':'F1.REGRA.P1','claim':claim,'primary':[pin(p) for p in principal],
        'attempt_artifacts':[pin(p) for p in sorted((OUT/'attempts').rglob('*')) if p.is_file()],
        'logical_builder_attempts':[pin(p) for p in sorted((OUT/'formal/attempts').rglob('*')) if p.is_file()],
        'scope':'60 theorems; the 101 constructor axiom reports include duplicates and auxiliaries. No canonical installation.'})
    result=OUT/'RESULTADO_PROVA_R1.json'
    new(result,{'unit':'F1.REGRA.P1','status':'ENTREGUE','mathematical_verdict':'PROVED_IN_EXPLICIT_MODEL',
        'theorem_count':count,'constructor_build':pin(build_file),'independent_review':pin(review),
        'manifest':pin(manifest),'report':pin(report),'sources':[pin(p) for p in sources],
        'passed':True,'axioms_allowed':['propext','Classical.choice','Quot.sound'],'sorry':0,
        'scope':['Uniqueness for fixed faithful reading and target under soundness and completeness.',
            'Exact literal satisfaction in Fix(R), not raw finite-time trajectory.',
            'Normalized satisfaction holds at n=0 independently of decay.',
            'Nonzero target and admissible face, not nonannihilation of every input or thermodynamic absolute-zero theorem.',
            'Philosophical and legal identification remains INPUT/ONTO; operator may name the candidate.'],
        'binary_reproduction':{'identical_modules':sum(m['olean_identical_constructor'] for m in reviewed['builds']),
            'total_modules':3,'limitation':'The concrete module .olean differs; source and axioms agree. Cause not determined.'},
        'production_changes':False,'gate_changed':False})
    marker='rule_proof_delivery_20261014'
    section='\n\n## 14/10/2026 — F1.REGRA.P1: prova do contrato da regra\n<!-- '+marker+' -->\n\n'
    section+='Em nome de codex-gerente-tgl, reivindicação 790 da F1.REGRA.P1; pedido humano «Exatamente isso, agora faça a prova».\n\n'
    section+='[REAL — verificação formal em sandbox] Dois módulos com 60 teoremas: build construtor e revisão/recompilação independente aprovados; axiomas apenas no trio permitido, zero sorry. Caracterização: para leitura fiel e objeto fixos, correção + completude determinam C(z) sse z=a. Realização ℝ²: R(a,b)=(a,0), T(a,b)=(a,exp(-1/2)b), alvo(1,0) não nulo; R²=R, RT=TR=R, T^n converge a R, e R(T^n(1,1)) é literalmente o alvo no tipo Fix(R). A trajetória bruta não satisfaz o alvo em nenhum n finito. Ponte matricial explícita e duas faces não nulas; controles negativos construídos.\n\n'
    section+='[ESCOPO] Satisfação normalizada já vale n=0 e independe de decay; λ governa a dinâmica, não a verdade do critério. A não aniquilação é da inscrição admissível/alvo; normalize(0,1)=0 é permitido e rejeitado. A escolha da leitura, do objeto e a identificação jurídico-física permanecem [INPUT/ONTO]. Não se afirma unicidade universal da interpretação.\n\n'
    section+='Prova explicada: `'+str(report)+'`. Resultado imutável: `'+str(result)+'`; SHA256 `'+pin(result)['sha256']+'`. Revisão: `'+str(review)+'`. Estado de entrega: ENTREGUE; aceite/instalação canônica da gerência não são presumidos. Nenhuma alteração de um.py, kernel, Bancada, dado ou gate.\n'
    surfaces=[ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    receipts=[append_bytes(p,section,marker) for p in surfaces]
    new(OUT/'MEMORY_DELIVERY_R1.json',{'claim':claim,'surfaces':receipts,'result':pin(result)})
    entry=OUT/'MAP_ENTRY_PROVA_R1.json'
    new(entry,{'tipo':'ROTA','rota_id':'conceitual.regra.prova_contrato','dominio':'FORMAL',
        'titulo':'Prova do contrato da regra e da satisfação — face finita',
        'pergunta':'Que estrutura matemática demonstra a regra relativa ao objeto da satisfação?',
        'dados':['Quatro cunhagens humanas pinadas','Kernel v392 e mathlib4.31','Modelo ℝ² explicitamente declarado'],
        'metodo':'Caracterização lógica, construção concreta, controles negativos e recompilação independente.',
        'resultado':'60 teoremas, só trio, zero sorry; igualdade literal na inscrição Fix(R), sem quitação bruta antecipada.',
        'veredito':'PROVADO_NO_MODELO_EXPLICITO','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,
        'defeito':'Não é prova de verdade ontológica universal. A leitura/alvo e a interpretação das condições são explícitos.',
        'nao_refazer':'Reaproveitar os dois módulos, os lemas do Tetelestai e a ponte matricial concreta.',
        'proximo_passo':'Revisão/aceite da gerência para eventual integração; nada se instala por esta entrega.',
        'onde':str(OUT),'artefatos':[str(result),str(manifest),str(report),str(review)],'refs':[1105,1106,1107,1108],
        'nota':'Declarações da definição e teoremas condicionais distinguidos; fontes, tentativas falhas e verbatim preservados.'})
    mapped=register.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',WHO+' / F1.REGRA.P1'],'MAP_RECEIPT_PROVA_R1.json')
    board=register.call([CLI,'avancar','F1.REGRA.P1','--quem',WHO,'--status','ENTREGUE','--evidencia',result,'--nota','Prova em sandbox:60teoremas,trio,zero sorry,recompilacao independente; escopo e limites declarados.'],'BOARD_DELIVERY_R1.json')
    transition={'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),
        'expected_revision':12,'event_id':'rule-proof-delivery-20261014',
        'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':'rule-proof-delivery-20261014','kind':'fact','statute':'REAL',
        'text':'F1.REGRA.P1 entregue:60teoremas Lean em sandbox, build e recompilacao independente aprovados, trio,zero sorry. Prova relativa a leitura fiel/alvo fixos e modelo concreto R². Ontologia/identificacao juridica permanece INPUT/ONTO; normalizacao satisfaz em n=0, dinamica bruta apenas converge. Nenhuma instalacao/gate. Missao da rede e pedidos externos conservam os estados anteriores.',
        'sources':[{'kind':'artifact','ref':str(p),'sha256':pin(p)['sha256']} for p in [result,report,review]]}]}}
    new(OUT/'ACOM_TRANSITION_R1.json',transition)
    memory=register.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_DELIVERY_R1.json',transition)
    assert memory['ok']
    released=register.call([CLI,'liberar','F1.REGRA.P1','--quem',WHO,'--nota','Prova e revisao entregues com memoria e mapa; aguarda aceite da gerencia.'],'RELEASE_R1.json')
    print(json.dumps({'result':pin(result),'report':str(report),'map':mapped,'board':board,'acom_revision':memory['result']['revision'],'release':released},ensure_ascii=False))


if __name__=='__main__':main()
