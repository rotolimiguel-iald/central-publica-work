"""Read final compiler evidence; write only this bridge's author audit/report.
Does not execute Lean, a recorder of memories, or the monolith.
"""
from pathlib import Path
from datetime import datetime
import hashlib, json, re, os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO')
NOW = datetime.now().astimezone()
STAGES = [('V351AntiunitaryResolventPhase','20260914_103607_852475',13),
          ('V351ScalarTomitaImaginaryConjugation','20260914_103720_643295',3)]
TRIO = {'propext','Classical.choice','Quot.sound'}

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def write_new(p,b):
    assert p.is_relative_to(ROOT) and not p.exists(), p
    tmp=p.with_name(p.name+'.tmp')
    tmp.write_bytes(b)
    assert tmp.read_bytes()==b
    os.replace(tmp,p)

def parse(text):
    result={}
    for m in re.finditer(r"(?m)^'(.+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",text):
        assert m[1] not in result
        result[m[1]]=[a.strip() for a in (m[2] or '').split(',') if a.strip()]
    return result

ficha_path=ROOT/'REAPROVEITAMENTO_A1_TRANSPORTE_ANTIUNITARIO.json'
ficha=load(ficha_path)
assert ficha['status']=='FICHA_ANTES_DO_CODIGO__OPEN'
protected=[]
for p in ficha['protected_five']:
    actual=pin(p['path'])
    assert actual==p
    protected.append(actual)
deps_path=ROOT/'DEPENDENCIAS_A1_TRANSPORTE_ANTIUNITARIO.json'
deps=load(deps_path)
for d in deps['entries']:
    for k in ['source','object','object_origin']:
        assert pin(d[k]['path'])==d[k],(d['module'],k)
modules=[]
all_axioms={}
history=[]
for stem,attempt,count in STAGES:
    src=ROOT/'kernel/TGLExt'/(stem+'.lean')
    obj=ROOT/'build/TGLExt'/(stem+'.olean')
    folder=ROOT/'attempts'/attempt
    run=load(folder/'run.json')
    source=src.read_text(encoding='utf-8-sig')
    stdout=(folder/'stdout.txt').read_text(encoding='utf-8-sig')
    stderr=(folder/'stderr.txt').read_text(encoding='utf-8-sig')
    targets=['TGLV350.Regular.'+t for t in re.findall(r'(?m)^#print axioms\s+(\S+)',source)]
    amap=parse(stdout)
    assert run['returncode']==0 and len(targets)==count and set(amap)==set(targets)
    assert all(set(v)<=TRIO for v in amap.values())
    assert not stderr.strip() and not re.search(r'\b(?:error|warning):',stdout)
    assert pin(src)['sha256']==run['source_sha256']
    assert src.read_bytes()==(folder/(stem+'.lean')).read_bytes()
    clean=re.sub(r'/\-[\s\S]*?\-/|--[^\n]*','',source)
    assert not re.search(r'\b(?:sorry|axiom|native_decide|trustCompiler)\b',clean)
    declarations=[]
    for target in targets:
        name=target.split('.')[-1]
        m=re.search(r'(?m)^(def|theorem)\s+'+re.escape(name)+r'(?=\s|[(:])',source)
        assert m
        declarations.append(dict(name=target,line=source[:m.start()].count('\n')+1,
                                 kind=m[1],statement=source[m.start():].split(' :=',1)[0].split(' where',1)[0]))
    for path in sorted((ROOT/'attempts').glob('*/'+stem+'.lean')):
        if path.parent.name==attempt or not (path.parent/'run.json').exists():
            continue
        previous=load(path.parent/'run.json')
        output=(path.parent/'stdout.txt').read_text(encoding='utf-8-sig')
        history.append(dict(module=stem,attempt=path.parent.name,run=pin(path.parent/'run.json'),
                            source_snapshot=pin(path),stdout=pin(path.parent/'stdout.txt'),
                            returncode=previous['returncode'],accepted=False,
                            category='missing_inherited_object_before_elaboration' if 'object file' in output and 'does not exist' in output
                            else 'elaboration_failure',partial_axioms_excluded=True))
    modules.append(dict(module=stem,source=pin(src),object=pin(obj),run=pin(folder/'run.json'),
                        source_snapshot=pin(folder/(stem+'.lean')),stdout=pin(folder/'stdout.txt'),
                        stderr=pin(folder/'stderr.txt'),returncode=0,command=run['command'],
                        lean_path=run['lean_path'],lean_version=run['lean_version'],
                        declarations=declarations,axioms=amap))
    assert not set(amap)&set(all_axioms)
    all_axioms.update(amap)
assert len(all_axioms)==16
assert len(history)==4 and all(h['returncode']==1 for h in history)
rows='\n'.join(f"| `{m['module']}` | {len(m['declarations'])} | `{m['source']['sha256']}` | `{m['object']['sha256']}` |" for m in modules)
report=f'''# A1 — ponte antiunitária do grupo do resolvente

{NOW.isoformat()} — **[REAL: autoria compilada, revisão independente pelo principal PENDENTE]**.

Foram concluídos dois módulos novos, **16 declarações = 13+3**, todos rc0 sem warnings e somente `propext`, `Classical.choice`, `Quot.sound`. O segundo módulo prova, para todo SiteProfile P e t real, no GNS e com o J originais:

    J U_t J⁻¹ = U_t.

Esta entrega é uma construção da bancada para revisão independente; não se apresenta como parecer independente de sua própria autoria.

## Consumidor e reuso

A ficha `REAPROVEITAMENTO_A1_TRANSPORTE_ANTIUNITARIO.md/json` foi criada antes do primeiro fonte novo. Consumidor: `regular_dual_weight_modular_implementation`. Reutilizei `antiunitaryConjugate` e sua multiplicatividade, `antiunitary_inner_conj`, `StarAlgHom.map_cfc` real, as fases/grupo já entregues e `scalarTomitaPolar_conjugate_resolvent` do J/T efetivos. Não reconstruí raiz, resolvente ou GNS; não usei nem editei os módulos de escala/intertwining do principal.

A generalização necessária é representar a conjugação como `→⋆ₐ[ℝ]`, pois conjugação antiunitária não é homomorfismo complexo. O novo transporte de CFC real usa a API da biblioteca e o complexo é recomposto por partes real e imaginária. A continuidade da conjugação vem das duas composições semilineares limitadas.

## Conteúdo e hipóteses

`V351AntiunitaryResolventPhase` trabalha em H : Type, Hilbert complexo completo. J é uma equivalência semilinear isométrica conjugada. **Não se supõe J²=I**. A identidade escalar `star(g_t(1−x))=g_t(x)` é válida para todos t,x reais, incluindo as pontas, por simetria do amortecimento e `Real.log_inv`.

Para T auto-adjunto e `antiunitaryConjugate J T = 1−T`, o módulo prova invariância de C_t=g_t(T) e B=T(1−T) sob conjugação. A conjugação de i e a troca x↦1−x cancelam os dois sinais; o resultado é U_t, não U_−t.

Para o transporte do grupo são usadas as hipóteses exatas já exigidas na sua construção: `0≤T≤1`, T injetivo e I−T injetivo. De JB=BJ, JC_t=C_tJ e U_tB=C_t, a igualdade JU_t=U_tJ é provada na imagem densa de B e estendida por continuidade. **Nenhuma inversa limitada de B nem gap** é introduzido.

`V351ScalarTomitaImaginaryConjugation` descarrega essas hipóteses pelos fornecedores concretos. Seus três alvos recebem somente P,t e o vetor quando pertinente: comutação pontual, conjugação com J.symm e igualdade dos operadores limitados complexos por `antiunitaryConjugate`. Não é apenas uma igualdade de pareamentos e não usa outro J auxiliar.

## Pins e reprodução

Compilação pelo `compile_a1.py` existente, Lean 4.31.0. Tentativas finais: `{STAGES[0][1]}` e `{STAGES[1][1]}`. O auditor JSON contém comandos, streams, hipóteses textuais, locadores e os 16 mapas de axiomas.

| Módulo | Declarações | SHA256 fonte | SHA256 objeto |
|---|---:|---|---|
{rows}

`DEPENDENCIAS_A1_TRANSPORTE_ANTIUNITARIO.json` registra 427 fornecedores de projeto. Três objetos herdados estavam ausentes na bancada e foram copiados do build V350 após igualdade byte a byte das fontes: `GenericAntilinearAdjoint`, `V350AntiunitaryPositiveConjugation`, `V350ScalarTomitaPolarInvolution`. Não foram recompilados nem modificados. Os demais objetos foram reutilizados e seus pins reconferidos.

Quatro tentativas rc1 do primeiro módulo permanecem preservadas: uma por objeto herdado ausente antes da elaboração; três por tipagem/simplificação, com prints parciais recusados. A última correção substituiu `simp` recursivo sobre escalares reais por transporte explícito com `congrArg`, sem aumentar heartbeats/recursão. O segundo módulo passou na primeira tentativa. Não há `sorry`, `axiom`, `native_decide` ou `trustCompiler` nos fontes finais. Somente as tentativas rc0 finais contam como evidência.

## Fronteira

Os cinco módulos/39 declarações anteriores ficaram byte a byte intactos. Não foi alterado nenhum módulo de escala do principal, programa terminal, memória, Atlas ou arquivo canônico. Não houve integração nem execução do monólito.

Esta ponte paga a conjugação antiunitária necessária à implementação modular. A escala funcional e o consumo dos geradores permanecem a cargo do principal. **A identificação da ação com AdΛ, o gerador h, a perturbação e o traço A1(b) continuam OPEN**; o presente grupo invariável sob J não os prova sozinho.
'''
report_path=ROOT/'RELATORIO_A1_TRANSPORTE_ANTIUNITARIO.md'
write_new(report_path,report.encode('utf-8'))
audit=dict(timestamp=NOW.isoformat(),status='AUTHOR_RC0__INDEPENDENT_REVIEW_PENDING',
           modules=modules,checked_declarations=16,axioms=all_axioms,
           allowed_axioms=sorted(TRIO),history_excluded=history,
           dependencies=pin(deps_path),ficha=[pin(ficha_path),pin(ROOT/'REAPROVEITAMENTO_A1_TRANSPORTE_ANTIUNITARIO.md')],
           five_previous_sources_preserved=protected,report=pin(report_path),
           compile_helper=pin(ROOT/'compile_a1.py'),new_source_modules=2,
           independent_review_performed=False,integrated=False,full_program_run=False,
           A1_b='OPEN',AdLambda_identification='OPEN',memory_written=False,
           scaling_modules_modified=False)
audit_path=ROOT/'AUDITORIA_A1_TRANSPORTE_ANTIUNITARIO.json'
write_new(audit_path,(json.dumps(audit,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'report':pin(report_path),'audit':pin(audit_path),
                  'modules':[{'name':m['module'],'source':m['source']['sha256'],
                              'object':m['object']['sha256']} for m in modules]},ensure_ascii=False))
