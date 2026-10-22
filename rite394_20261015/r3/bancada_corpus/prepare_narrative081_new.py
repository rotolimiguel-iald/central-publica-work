from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_081_20260910'
REVIEW = ROOT / 'REVISOES_RAIZ_081_20260910'
INDEPENDENCE_REVIEW = (ROOT / sys.argv[1]).resolve()
assert INDEPENDENCE_REVIEW.is_relative_to(ROOT) and INDEPENDENCE_REVIEW.is_dir()
independence_reports = list(INDEPENDENCE_REVIEW.glob('PARECER*.md'))
assert len(independence_reports) == 1
independence_report = independence_reports[0]
REVIEW.mkdir(exist_ok=False)

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temporary = path.with_name(path.name + '.tmp_new')
    with temporary.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == raw
    temporary.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

sources = [
 ROOT / 'COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md',
 ROOT / 'REVISAO_REDUCAO_QUADRATICA_081_20260910_050052_914909/PARECER_H3_E5_E_REPRESENTANTES_QUADRATICOS_081.md',
 ROOT / 'DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md',
 ROOT / 'DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/compute_odd_weyl081.py',
 ROOT / 'DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTROLES_DETECTOR_WEYL_QUADRATICO_081.json',
 ROOT / 'REVISAO_DETECTOR_WEYL_QUADRATICO_081_20260910/PARECER_DETECTOR_IMPAR_E_CLASSE_E5_081.md',
 ROOT / 'INDEPENDENCIA_RESIDUO_E_IMAGEM_081_20260910/DUAS_AVALIACOES_E_SUBMODULO_LIVRE_E6.md',
 independence_report, OUT / 'ESTADO_CANONICO_081.json']
before = [pin(path) for path in sources]
snapshot = json.loads(sources[-1].read_bytes())
assert snapshot['present'] == 77 and snapshot['embedded_files'] == 683
assert len(snapshot['absent']) == 21 and snapshot['seal_um_hash_matches']
assert all(row['unchanged'] for row in snapshot['comparison_with_delivery080'])
arithmetic = json.loads(sources[4].read_bytes())
assert arithmetic['check_count'] == 14 and arithmetic['all_checks_pass']
algebraic = [item for item in arithmetic['checks'] if item['name'] != 'all_sources_unchanged']
assert len(algebraic) == 13 and len(arithmetic['checks']) - len(algebraic) == 1

root_review = r'''# Revisão da raiz081 — redução E5 e imagem quadrática não nula

10/09/2026. [DERIVED — revisão matemática escrita] [REAL — leitura de fontes e recibos].

Li integralmente a redução de H³(s0)E5, sua revisão independente, a nota final do candidato, o script de controle, o recibo e o parecer independente. Não identifiquei erro material no domínio fixado. A nota de independência de duas classes é de minha autoria e possui parecer externo próprio; esta revisão não substitui esse parecer.

Na redução E5, o ciclo linear de ghost−1 é P[p] com PH=0. A aplicação pontual da fatoração079 está justificada: os coeficientes de B ficam à esquerda, e B div H=0 vale no ponto pela identidade diferencial de Bianchi. Subtrair B div conserva o ciclo e reduz a ordem. O símbolo fornece uma primitiva polinomial por inteiros positivos, não por divisão pela covariável quadrática. A ordem r em p se torna no máximo r−1 em q e conserva o peso auxiliar r+3. Isso demonstra a nulidade do módulo linear inteiro, antes dos invariantes.

A contagem em Sym⁵ tem somente os padrões(1,1,1,0,0) e(1,1,1,1,−1). O segundo some; não é necessária uma resolução KT inteira. A exatidão finita dos invariantes e a extensão Rher⊗R fornecem a apresentação por Sym²M⊗Λ³G. M continua quociente por relações, não uma coleção livre de jatos. Os representantes Weyl, seus jatos de fundo e C,m são s0-fechados antes das EOM; seus produtos naturais representam todas as classes. As primitivas h³C², h*hC³ e C*C⁴ permanecem permitidas e pagam as relações mistas.

No candidato, J_W=tr(W1∧W1)/vol_g0 é o pseudoscalar que a fonte chama J, e Bgh=ε CCm/2 é a cúbica de ghosts chamada β. A expressão b5=κJ_W Bgh tem ghost3/E5, engenharia zero e s0b5=0 para C livre porque W(g0)=0. Nenhum coeficiente é escolhido em função da frequência k do teste.

Conferi os sinais da geometria escrita: R0i0j=k²fQij/2 e R3i3j=−f''Qij/2; a EDO dá Ricij=f'Qij/z, e o Schouten fpQ/(2z) deixa E=(k²f−f'/z)/2. As componentes mistas dão B=kf'/2; as quatro formas Weyl e a contração −2ηaaηbb somam16EB. A divisão pela forma volume fornece J_W=4k(z/ℓ)^4 f'(k²f−f'/z). Diferenciar a ℓ fixo antes de aplicar os dados dá J'_W=4k³−28k/z0². Essa derivação é escrita: o script recebe as formas E/B, sem calcular Γ ou Riemann a partir da métrica.

Os Killing escolhidos fecham a subálgebra usada; sc=C∂C dá dθθi=θiθ3/z0. A contração epsilon dá Bgh=−6θ012/z0 e sua variação −18θ0123/z0². A série natural completa do pseudoscalar conserva o termo s0J3: s1J_W+s0J3=C∂J_W. Somente após avaliar os Killing esse termo some. O sinal θ3θ012=−θ0123 produz κ(6J'_W/z0−18J_W/z0²), isto é, κ(24k³/z0−96k/z0³). A metade da diferença entre k e −k conserva o valor, com a mesma orientação.

O teste anula todas as fronteiras de s0 no domínio, incluindo antifields, por soluções e Killing em uma vizinhança. Portanto o valor não nulo em k=1/z0 prova uma classe não nula em δ(Kcal), e não apenas um polinômio não nulo. Isso não identifica essa classe com −[A6].

Conferi estaticamente o código: aritmética de Fraction e máscaras exteriores; derivada total antes da especialização; Sym²W de dimensão55 e dez emparelhamentos sem derivadas com Λ³G. A apresentação E5 não tem dimensão dez demonstrada. Os14 registros são13 algébricos e1 de integridade das cinco fontes. O pin do próprio script foi lido apenas ao fim da execução matemática; não há pin inicial a inventar. A revisão atual confere o pin final e as janelas posteriores registradas. Não reexecutei o cálculo, Lean ou um.py.

Aceito esses resultados no fundo espaço-forma fixado, escalares inertes herdados e jatos finitos por elemento. Ficam abertos a imagem inteira de d1, cancelamento, jatos/coeficientes mais gerais, QME, admissibilidade causal e UV. Nenhum original ou memória canônica foi alterado.
'''
root_pin = emit(REVIEW / 'PARECER_REDUCAO_E5_E_DETECTOR_081.md', root_review.encode('utf-8'))
report = r'''# Suficiência081 — representantes quadráticos e uma imagem não nula distinta do resíduo

10/09/2026. [DERIVED — demonstrações escritas revisadas] [REAL — controles exatos e custódia documental].

**A liberdade restante foi reduzida a quadráticos de Weyl e sua imagem comprovadamente não é zero.** Toda classe E5 admite representante sem antifields, fechado por s0, enquanto os antifields continuam nas relações entre classes. Construímos um candidato explícito com imagem não nula; duas avaliações mostram que essa imagem e [A6] são independentes. Portanto esse candidato sozinho não cancela o resíduo. O problema de outros candidatos permanece aberto.

## 1. Estado canônico e domínio

A [captura081](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_081_20260910/ESTADO_CANONICO_081.json>) relê por bytes e AST, sem executar/importar um.py. Os quatro canônicos permanecem iguais080: v338, 683 arquivos embutidos, 77 dos98 módulos acompanhados presentes,21 ausentes; selo correspondente e parede UV aberta. Não houve nova rodada canônica. H3 interno, fase/ramo e falsificadores já reconhecidos permanecem preservados.

As provas desta entrega usam o mesmo complexo métrico mínimo de zeroformas naturais orientadas: dimensão quatro, referência espaço-forma K>0 FIXADA, κ real não nulo fixado, φ0 constante projetada e escalares inertes herdados. A ordem de jatos é finita por elemento. Não se afirma extensão a K variável num anel restrito, tensores espectadores, φ=id ou uma categoria causal com condições adicionais ainda não pagas.

## 2. Todas as classes E5 têm representantes quadráticos fechados

Se L é o complexo linear de jatos, a fatoração das identidades de Einstein por Bianchi dá

H⁻¹(L,s0)=0.

O argumento vale também para um ciclo dado apenas no ponto: escrever coeficientes à esquerda permite reduzir a ordem por P→P−B div, conservando PH=0. A primitiva termina em ordem finita e não divide por p².

Em Sym⁵L, ghost3 só admite(1,1,1,0,0) e(1,1,1,1,−1). Eliminado o segundo padrão,

H³(s0)_(E5,nat) ≅ Rher⊗[Sym²M⊗Λ³G]^Lorentz,

com M=H⁰(L,s0) gerado por jatos de Weyl modulo suas relações e G=V⊕Λ²V, os dados de Killing. M não foi declarado livre nem o módulo quadrático finito.

Consequentemente, qualquer ciclo b5 pode ser escrito

b5=Q(W1,∇bar W1,…;C,m)+s0χ5,   s0Q=0,

com Q quadrático nos jatos de Weyl e cúbico nos ghosts. O fechamento de Q vale antes das equações de movimento. As relações entre classes continuam usando as EOM e as primitivas com antifields h³C², h*hC³ e C*C⁴. A conclusão trata também ciclos mistos; não supõe que seu pedaço antifield feche sozinho.

[Demonstração E5](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md>) · [Revisão independente da aplicação](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_REDUCAO_QUADRATICA_081_20260910_050052_914909/PARECER_H3_E5_E_REPRESENTANTES_QUADRATICOS_081.md>).

## 3. Uma classe admitida tem imagem não nula

Para manter os tipos explícitos, chamamos aqui J_W o pseudoscalar tr(W1∧W1)/vol_g0, e Bgh a cúbica ε_abcd C^aC^b m^cd/2. São os símbolos J e β definidos localmente na nota do candidato. Tome

b5=κ J_W Bgh.

Ele tem ghost3, valência5, engenharia zero e s0b5=0 universalmente no fundo declarado. Nenhum coeficiente depende de k. Na família TT078, com z0=ℓ,

Lk(s1b5)=κ(24k³/z0−96k/z0³).

Em k=1/z0 o valor é−72κ/z0⁴≠0. Como Lk anula todas as fronteiras de s0, isso prova [s1b5]≠0. Em C5, b5 é ciclo e projeta a zero em C3; sua imagem pela conexão é [s1b5]. Logo

δ(Kcal)≠0.

Essa conclusão refuta a hipótese de que o detector ímpar anulasse a imagem de TODOS os quadráticos fechados. Ela não estabelece −[A6]∈δ(Kcal).

A ponte entre BRST e a derivada de Lie foi mantida inteira: s1J_W+s0J3=C·∂J_W, obtida da série do pseudoscalar da métrica ativa. O termo s0J3 só desaparece na avaliação por Killing. O cálculo de J'_W também mantém o fator conforme e deriva antes de impor os dados iniciais.

[Candidato e prova](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_DETECTOR_WEYL_QUADRATICO_081_20260910/PARECER_DETECTOR_IMPAR_E_CLASSE_E5_081.md>) · [Revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_081_20260910/PARECER_REDUCAO_E5_E_DETECTOR_081.md>).

## 4. A imagem construída e o resíduo são independentes

Ponha a=[A6] e b=[s1b5]. Aplique os funcionais nas frequências1/z0 e2/z0, mantendo o MESMO fundo e coeficientes:

| Avaliação | a | b |
|---|---|---|
| ℓ_(1/z0) | −4/z0² | −72κ/z0⁴ |
| ℓ_(2/z0) | −8/z0² | 0 |

A matriz tem determinante−576κ/z0⁶, uma unidade em Rher. Portanto a,b são independentes sobre o próprio anel herdado, inclusive com nilpotentes. A nota dá uma retração explícita; eles geram um submódulo livre cindido Rher² de H⁴(A6,s0), para Rher não nulo. O restante desse grupo não foi calculado.

Isso prova −a∉Rher b: nenhum múltiplo escalar do candidato exibido, acrescido de fronteiras, cancela o resíduo. Não prova −a∉δ(Kcal), pois outras classes de E5 ainda podem contribuir.

Qualquer candidato a cancelamento precisa ter

ℓ_(2/z0)(d1[z5])=+8/z0².

O candidato κJ_W Bgh contribui zero nesse teste. A nova condição é um filtro para outros candidatos; não foi estendida a uma anulação de toda a imagem.

[Prova das duas avaliações](<C:/IALD/Central de Patentes/Chatgpt/INDEPENDENCIA_RESIDUO_E_IMAGEM_081_20260910/DUAS_AVALIACOES_E_SUBMODULO_LIVRE_E6.md>) · [Revisão independente](<__INDEPENDENCE_REVIEW__>).

## 5. Verificação executada e seus limites

O [recibo081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTROLES_DETECTOR_WEYL_QUADRATICO_081.json>) contém14 registros:13 controles algébricos exatos e1 de integridade das cinco fontes, em uma execução Python puro. Houve revisão estática independente; nenhum rerun e zero Lean novo.

O script recebe as formas Weyl E/B. Sua derivação a partir de Riemann/Ricci/Schouten é demonstração escrita revisada, não um cálculo completo de geometria feito pelo script. As cinco fontes têm pins antes/depois; o próprio script possui somente pin final da execução matemática. A conferência atual não inventa um pin inicial.

A contagem Sym²W, dimensão55, produz dez emparelhamentos tensoriais sem derivadas com Λ³G. Isso não é a dimensão da cohomologia E5 nem classificação de todos os jatos. As duas avaliações do item4 são consequência algébrica escrita; não foram contadas como nova execução desse recibo.

## 6. Próxima obrigação e objetivo completo

Pela080, δ(Kcal)=im d1E5. Pela081, podemos escolher representantes Q quadráticos de Weyl, e sabemos que essa imagem tem uma direção não nula independente de [A6]. Falta decidir se OUTRAS classes fornecem a direção necessária: construir Q admissível e a6 finito com r6+s1Q=s0a6, ou provar exclusão de −[A6] para toda a imagem pertinente.

A redução E4 por cotas de representação não exclui automaticamente jatos altos nos produtos quadráticos: produtos de tipos grandes podem conter tipos pequenos. A investigação082 sobre famílias sem derivadas e a ação do diferencial fica EXCLUÍDA desta entrega081.

Continuam também a torre real e os demais canais de anomalia, contratermos causais, corrente/carga interagentes e QME, compatibilidade entre fundos/estados/cortes, reconstrução gravitacional geral pelos mesmos dados selecionados e justificação UV. A incorporação dos21 módulos pendentes é uma obrigação distinta.

Somente arquivos novos sob Chatgpt foram escritos. Originais, Atlas, índice, memórias canônicas, selo e gate permanecem intactos; nenhum um.py executado/importado e nenhum teste de natureza. As memórias novas registram o progresso com seus limites, sem substituir documentos anteriores.
'''.replace('__INDEPENDENCE_REVIEW__', independence_report.as_posix())
report_pin = emit(OUT / 'REEXAME_SUFICIENCIA.md', report.encode('utf-8'))
memory = '''# Memória de trabalho081 — representantes E5 e duas direções de E6

10/09/2026. Documento novo; nenhuma memória anterior ou Atlas alterado.

[REAL] Captura081: quatro canônicos iguais080, v338,683 arquivos embutidos,77/98 módulos acompanhados presentes e21 ausentes; selo corresponde, UV aberto. Leitura AST/bytes, sem execução/importação.

[DERIVED] Na categoria fixa080, Bianchi paga H⁻¹(L)=0; H³(s0)E5≅Rher⊗[Sym²M⊗Λ³G]^Lorentz. M é o quociente real dos jatos Weyl, G=V⊕Λ²V. Toda classe b5 admite Q quadrático Weyl s0-fechado off-shell, com b5=Q+s0χ5. Fronteiras mistas com antifields preservadas; módulo quadrático não declarado livre/finito.

[DERIVED] Candidato b5=κJ_W Bgh (J_W=trW1²/vol, Bgh=εCCm/2, nomes J eβ na fonte): s0b5=0; Lk(s1b5)=κ(24k³/z0−96k/z0³). δ(Kcal)≠0. Duas avaliaçõesk1=1/z0,k2=2/z0 provam independência de a=[A6] e b=[s1b5]; det−576κ/z0⁶ e retração explícita. Somando livreRher² em H⁴(A6,s0). −a não está na linhaRher b; não se exclui a imagem inteira.

[REAL] Recibo14=13 controles algébricos+1 integridade das cinco fontes. Script tem pin próprio somente final da execução; fontes têm antes/depois. Revisão estática, zero rerun/Lean. Derivação geométrica escrita; formas Weyl são entradas do script.

[OPEN] Procurar outros Q com ℓ_(2/z0)(d1Q)=+8/z0² e pagar identidade completa r6+s1Q=s0a6. Jatos altos, imagem total, torre/anomalia, contratermos/QME, compatibilidades, reconstrução pelos mesmos dados e UV. H3 interno, fase/ramo e falsificadores preservados.082 excluída; fundoφ=id,K variável/tensores espectadores não cobertos.

[Relatório081](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_081_20260910/REEXAME_SUFICIENCIA.md>)
'''
memory_pin = emit(OUT / 'MEMORIA_DE_TRABALHO_081.md', memory.encode('utf-8'))
design = '''# Adendo081 ao desenho do fechamento

10/09/2026. [DERIVED — caminho crítico atualizado em arquivo novo].

O objetivo integral mantém reconstrução geral pelos mesmos dados, conteúdo do registro e setor quântico interagente/UV. A parte fase/ramo já paga não é reaberta.

Na frente de cohomologia local:080 reduz δ(Kcal) à imagem de d1 em E5;081 representa TODAS as classes E5 por quadráticos de Weyl s0-fechados, preservando relações e primitivas com antifields. O módulo quadrático não foi classificado em base finita.

Há uma imagem explícita não nula: b=[s1κJ_W Bgh]. Duas avaliações mostram que ela é independente de a=[A6], com somando livreRher². Assim a simples alegação de que todo d1 seria anulado pelo detector está refutada, e o candidato encontrado sozinho não cancela o resíduo.

Próxima obrigação verificável: encontrar outro Q admissível com r6+s1Q=s0a6, ou provar que −a está fora de TODA im d1. O teste k=2/z0 exige ℓ(d1Q)=+8/z0²; o candidatoκJ_W Bgh contribui zero. O teste é necessário, não suficiente. Não cortar arbitrariamente as ordens de jatos.

Mesmo um prolongamento C6 não conclui valências superiores, comparação da torre, anomalias/QME, contatos e contratermos. Persistem compatibilidades físicas, reconstrução geral, rotaUV e21 módulos não incorporados. Domíniofixo: espaço-formaK>0,κ≠0,φ0 constante,escalares inertes herdados; não transportar paraφ=id ouK variável por nome.

13 controles algébricos+1integridade, demonstrações escritas revisadas,zeroLean. Nenhum original ou gate alterado. Investigação082 separada.

[Relatório e provas](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_081_20260910/REEXAME_SUFICIENCIA.md>)
'''
design_pin = emit(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_081.md', design.encode('utf-8'))
after = [pin(path) for path in sources]
assert before == after
record = {'created_utc': datetime.now(timezone.utc).isoformat(),
 'status': 'ROOT_REVIEW_OF_E5_AND_DETECTOR__INDEPENDENCE_HAS_SEPARATE_EXTERNAL_REVIEW',
 'sources_before': before, 'sources_after': after, 'all_sources_unchanged': True,
 'root_review': root_pin, 'narratives': [report_pin, memory_pin, design_pin],
 'writer': pin(Path(__file__)), 'arithmetic_rerun': False, 'new_lean_compilations': 0,
 'originals_written': False, 'um_executed_or_imported': False, 'stage082_excluded': True}
record_pin = emit(REVIEW / 'REGISTRO_RAIZ_REDUCAO_E5_E_DETECTOR_081.json',
 (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'root_review': root_pin, 'report': report_pin, 'memory': memory_pin,
 'design': design_pin, 'record': record_pin}, ensure_ascii=True))
