from pathlib import Path
import hashlib, json, os
from datetime import datetime

root = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911')
out = root / 'revisao'
stamp = datetime.now().astimezone().isoformat(timespec='seconds')
tag = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
names = ['ScalarRightAdjointPair', 'ScalarPairedRightAlgebra', 'ScalarRightPairVector',
         'ScalarRightHilbertCore', 'ScalarRightGraphCore']
pins = {str(root / 'kernel' / 'TGLV350' / (n+'.lean')):
        hashlib.sha256((root / 'kernel' / 'TGLV350' / (n+'.lean')).read_bytes()).hexdigest()
        for n in names}

body = f'''# Consulta separada — CFC, quadrados direitos e o teste (P)

{stamp}. [DERIVED — proposta matemática por leitura das interfaces; NÃO compilada nem certificada em Lean.] Esta nota guarda e desenvolve a sugestão do operador, após encerrada a revisão independente dos12 de RealPhaseVariational. Nenhuma fonte concreta em debug foi lida ou aceita. Não altera o parecer dos12 nem os pareceres/custódias anteriores.

Escreva M=π(N), E=scalarPairedRightAlgebra P, j=scalarRightPairVector P, F=scalarTomitaAdjoint P original. A seguir a=a*∈E é um operador limitado; não é Δ nem o bloco A da projeção de gráfico.

## A ponte que torna a proposta efetiva

1. **Estabilidade a provar.** Se T∈M′ é limitado, auto-adjunto e comuta com a, então Ta∈E é auto-adjunto e j(Ta)=Tj(a). Com v=j(a), as duas identidades do par de a têm o mesmo vetor, pela unicidade e a=a*. Para todo x∈nν, TaΛx=Tπ(x)v=π(x)Tv. Como (Ta)*=aT=Ta, essa mesma igualdade dá o vetor adjunto. Isto constrói um ScalarRightAdjointPair, sem supor T∈E. A pertinência dos CFC reais de a a M′ vem do fechamento normado do comutante/limites de polinômios.

2. **Suporte do vetor, sem PVM.** v∈closure(Ran a): para as médias e_h∈nν, h>0, aΛ(e_h)=π(e_h)v→v por scalarGNSAverage_tendsto. Não se exige cota uniforme para Λ(e_h), nem ker a=0. Esta é a condição que faltaria para afirmar gε(a)v→v em um Hilbert abstrato arbitrário.

3. **Uma construção por funções racionais basta.** Para ε>0, tome Tε=(a²+εI)⁻¹ por CFC contínuo, bε=Tε a, dε=a bε=gε(a), com gε(t)=t²/(t²+ε), e cε=a dε. Pelo passo1 bε∈E; portanto dε,cε∈E. Todos são auto-adjuntos e comutam. Pelas identidades de produto de j:

   j(bε)=Tεv; j(dε)=aTεv; j(cε)=a²Tεv=gε(a)v.

   Há uma decomposição exata em diferenças de quadrados de elementos auto-adjuntos de E:

   cε = ¼[(a+dε)² − (a−dε)²].

   Assim não é preciso construir já a parte positiva ou a raiz de a dentro da álgebra E, que não foi declarada fechada em norma. Tampouco é usada uma inversa limitada de a: somente a²+εI tem inversa limitada para cada ε>0.

4. **Convergência forte apenas no suporte necessário.** O CFC dá ‖I−gε(a)‖≤1 e ‖(I−gε(a))a‖≤√ε/2, pela desigualdade ε|t|/(t²+ε)≤√ε/2. Logo gε(a)→I fortemente em closure(Ran a), por aproximação de vetores da imagem e cota uniforme. Aplicando2, j(cε)→j(a). Como cε=cε*, também Fj(cε)=j(cε): a aproximação ocorre no gráfico de F, não apenas em norma Hilbert.

## Consequência precisa e ligação a (P)

O resultado existente scalarRightSelfadjointVectors_closure identifica o fecho dos j(a), a=a*, com Fix F. Com os quatro passos acima, **o espaço linear real gerado pelos j(b²), b=b*∈E, tem fecho Fix F**. Não se afirma densidade do cone de quadrados sozinho, nem convergência de uma única família de quadrados para um vetor de sinal arbitrário.

Complexificando e usando a decomposição de D(F) em Fix F+i Fix F (F fechado e involutivo), obtém-se um núcleo de gráfico para F no espaço complexo gerado pelos quadrados. Equivalentemente, pode-se compor a aproximação dos a=a* com a decomposição a=(a+a*)/2+i(a−a*)/(2i) e scalarRightPairGraph_closure_eq_original. É uma prova adicional proposta; não se deduz de scalarRightPairVector_products_dense isoladamente.

Para ζ,ζ♭ do teste (P), basta então verificar a identidade de pareamento em quadrados e passar por continuidade no gráfico. Nas convenções complexas do kernel, ela é ⟨Fj(c),ζ⟩=⟨ζ♭,j(c)⟩. Se K,K* já satisfazem K j(a)=aζ e K* j(a)=aζ♭ em E, a identidade vale em produtos:

⟨j(b*a*),ζ⟩ = ⟨j(a*),Kj(b)⟩ = ⟨K*j(a*),j(b)⟩ = ⟨ζ♭,j(ab)⟩.

Tomando a=b=b* obtém-se o teste nos quadrados. A densidade de gráfico recém-proposta estende o teste a D(F), o que coloca ζ em D(F†) com F†ζ=ζ♭. Na aplicação concreta deve-se usar a identificação do adjunto máximo de F com S original; não substituir S por uma involução homônima. A construção dos pares K/K* e essa identificação/domínios continuam a ser conferidas na aplicação de (P).

## Estatuto e próximos lemas

[REAL — fontes lidas, sem nova execução Lean] Interfaces usadas: ScalarRightAdjointPair.right/adjoint; scalarGNSAverage_tendsto; scalarRightAdjointPair_vector_unique; scalarRightPairVector_of_pair/mul/star/original_adjoint; scalarPairedRightAlgebra_mem_commutant; scalarRightSelfadjointVectors_closure; scalarRightPairGraph_closure_eq_original.

[OPEN — formalização nova] (i) estabilidade sob T auto-adjunto comutante; (ii) j(a)∈closure(Ran a); (iii) corte racional e aproximação por diferenças de quadrados no gráfico; (iv) densidade real dos quadrados e extensão do teste. São obrigações concretas propostas, sem assumir inversa modular, KMS, igualdade de ideais ou continuidade de F. Os pins desta leitura estão no JSON acompanhante. Nenhuma memória/helper autoral foi executado; escritas só revisao.
'''

def put(path, data):
    assert path.resolve().is_relative_to(out.resolve())
    if path.exists():
        prior = path.read_bytes()
        bak = path.with_name(path.name + '.bak_' + tag)
        bak.write_bytes(prior)
        assert bak.read_bytes() == prior
        data = prior + b'\n\n---\n\n' + data
    temp = path.with_name(path.name + '.tmp_' + tag)
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    os.replace(temp, path)

note = out / 'CONSULTA_CFC_QUADRADOS_TESTE_P.md'
put(note, body.encode('utf-8'))
evidence = {'timestamp': stamp, 'status': 'DERIVED_PROPOSAL_NOT_LEAN_CHECKED',
            'source_sha256': pins, 'note_sha256': hashlib.sha256(note.read_bytes()).hexdigest(),
            'no_author_writes': True, 'no_new_compilation': True}
pinpath = out / ('consulta_cfc_quadrados_p_pins_' + tag + '.json')
put(pinpath, (json.dumps(evidence, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps({'note':str(note), 'pins':str(pinpath), 'sha256':evidence['note_sha256']}))
