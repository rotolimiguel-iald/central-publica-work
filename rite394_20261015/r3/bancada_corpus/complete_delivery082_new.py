from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_082_20260910'
DOC_DIR = (ROOT / sys.argv[1]).resolve()
assert DOC_DIR.is_relative_to(ROOT) and DOC_DIR.is_dir()
doc_reports = list(DOC_DIR.glob('PARECER*.md'))
assert len(doc_reports) == 1
doc_report = doc_reports[0]

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    tmp = path.with_name(path.name + '.tmp_new')
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

adendum = r'''# Revisões e precisões da entrega082

10/09/2026. [DERIVED — matemática escrita revisada] [REAL — evidência documental]. As notas/manifestos emitidos antes das revisões mantêm seu estatuto histórico de revisão pendente; a presente entrega os lê conjuntamente com os pareceres posteriores:

- [Setor finito](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_SETOR_FINITO_082_20260910_052417_739397/PARECER_SETOR_FINITO_SEM_DERIVADAS_082.md>).
- [Identificação CE](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_QUADRATICO_082_20260910_053047_6990258/PARECER_IDENTIFICACAO_CE_082.md>).
- [Classe CE e corrente da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_OBSTRUCAO_CE_CORRENTE_082_20260910_053437_900535/PARECER_CLASSE_CE_E_CORRENTE_GRADIENTE_082.md>).
- [Revisão da raiz das notas externas](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_082_20260910/PARECER_SETOR_FINITO_E_CE_082.md>).
- [Conferência documental do relatório](<__DOC__>).

Turing construiu o setor finito e foi revisado por Herschel; Singer construiu a identificação CE e foi revisado por Turing; a raiz construiu a nota da classe e da corrente e foi revisada por Herschel. A conferência documental posterior não é contada como nova aprovação matemática de resultados do próprio revisor.

O recibo finito tem 19 itens: 18 algébricos e 1 de preservação das quatro fontes. Uma execução Python puro, com frações e álgebra exterior; nenhuma reexecução ou Lean novo. Os dez Weyl do controle são uma base tensorial, não dez soluções escolhidas para substituir a prova de completude. O teste de dghost aplicado a uma contração nula não paga sozinho a variação em h; o argumento universal consta da nota e das revisões.

O código matemático tem pin final no recibo; a proveniência do preparador registra também seu destino antes da execução. Os valores coincidem no exame documental, sem converter essa comparação em uma nova execução. As funções aritméticas081 foram lidas e copiadas por AST, não importadas ou executadas da origem. Os auxiliares de captura/finalização082 são cópias novas, com mudanças medidas em PROVENIENCIA_AUXILIARES_082.json; o estatuto PREPARED_NOT_EXECUTED é o retrato anterior às execuções com recibo próprio.

Os símbolos têm tipos diferentes: Mcal é o módulo de Weyl/EOM; Mghost=antisym(∇C)=−g0⁻¹m na nota CE; a matriz M da nota finita é g0⁻¹m. J_W é um pseudoscalar quadrático e βo uma cúbica de ghosts, definidos localmente. Não são a involução J=Luz nem β_TGL. O complexo é CE invariante por h; horizontalidade só vale para a família q_V e para o alvo a aqui considerados.

A revisão independente da corrente explicitou, ao expandir a definição já dada, a correção finita

q6=(ε0_abcd/3!) [∇bar^aJ3 − h^{ae}∇bar_eJ_W + (tr H/2)∇bar^aJ_W] C^bC^cC^d,

com 𝒥(g0+t h)=t²J_W+t³J3+… e H=g0⁻¹h. A raiz conferiu essa expansão: os termos vêm do terceiro coeficiente de 𝒥, da métrica inversa e do volume. É explicitação aditiva da espécie h³C³, sem alterar a fonte congelada. A identidade resultante produz □bar J_W; não o identifica com −J_W nem cancela o resíduo por declaração.

O alvo não nulo em H(s0) é fechado para CE; a nulidade na cohomologia seguinte continua aberta. O setor sem derivadas inteiro está excluído, mas a imagem com jatos não foi determinada. Investigação083 excluída. Os originais, memórias canônicas e gate permanecem intactos.
'''.replace('__DOC__', doc_report.as_posix())
adendum_pin = emit(OUT / 'ADENDO_REVISOES_082.md', adendum.encode('utf-8'))

tunnel = r'''# Entrega082 — setor sem derivadas e diferencial CE

10/09/2026. Para a sessão que codifica um.py. [DERIVED — demonstrações escritas revisadas] [REAL — controles algébricos exatos].

Domínio obrigatório: complexo métrico mínimo natural orientado, quatro dimensões, referência espaço-forma FIXADA com K>0, κ real não nulo fixado, φ0 constante projetada e escalares herdados inertes. Cada elemento tem ordem finita de jatos. Não transportar por nome a outros fundos, φ=id, tensores espectadores ou K variável num anel restrito.

1. O setor de dois Weyl SEM derivadas e três ghosts residuais tem dez contrações, separadas em 8 + 2. Sua imagem no detector é Rher·R(k), R=24k³/z0−96k/z0³. Todos dão zero em k=2/z0, enquanto o alvo exige +8/z0². Nenhum desses candidatos cancela A6; setores com derivadas continuam abertos.
2. Em toda a diagonal E=q+2, (Hq(s0),d1) identifica-se com CE(g,Sym²Mcal)^h. Mcal é o quociente de Weyl/EOM; g é a álgebra matricial de Killing; h a isotropia. O complexo é invariante, não necessariamente relativo/horizontal.
3. Fórmulas nas classes: d1p=−Mghost p; d1Mghost=−Mghost²+Kpp♭; d1W_r=p∇W_r+𝔯(Mghost)W_r. Conservar as correções s0 da nota: p2, k2 e T_r,2−𝔯(H/2)W_r. Todos os índices de derivadas recebem curvatura. Mghost=antisym∇C=−g0⁻¹m; a matriz M da nota finita tem o sinal oposto.
4. O alvo a=J_Wν(p), ν=εp4/4!, é cociclo CE. −[A6]∈im d1 ⇔ [a]_CE=0. A não nulidade078 em H(s0) não decide essa segunda classe.
5. Família horizontal nova: q_V=εV p3/3!, dCE q_V=(div V)ν. Para V=∇J_W, s1q_grad+s0q6=(□J_W)ν. q6 é o coeficiente t6 da forma natural ativa ι_grad_g𝒥 vol_g avaliada em (tC)^3, e sua expansão está no adendo. A identidade inteira pode receber κ para engenharia zero. Nenhuma igualdade □J_W=−J_W foi assumida.

Validação: uma execução Python, 18 controles algébricos + 1 de integridade das quatro fontes; revisão estática, sem rerun; zero Lean. Generalidade dos jatos, CE e corrente são demonstrações escritas revisadas, não contagem de testes. Notas antigas com estatuto pendente são lidas com os pareceres posteriores.

Canônico relido: v338, quatro pins iguais081, 77/98 módulos acompanhados presentes, 21 ausentes. Nenhum um.py executado/importado, original ou gate alterado. H3 interno, fase/ramo e falsificadores preservados.083 excluída.

[Relatório](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_082_20260910/REEXAME_SUFICIENCIA.md>) · [Revisões e precisão de q6](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_082_20260910/ADENDO_REVISOES_082.md>) · [Memória](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_082_20260910/MEMORIA_DE_TRABALHO_082.md>) · [Desenho](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_082_20260910/DESENHO_DO_FECHAMENTO_ADENDO_082.md>) · [Manifesto](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_082_20260910/MANIFESTO_ENTREGA_082.json>).

Persistem imagem CE completa, primitiva admissível, próximos cortes, demais anomalias/QME, contratermos, compatibilidades, reconstrução pelos mesmos dados e rota UV. A integração dos módulos ausentes é obrigação distinta.
'''
tunnel_pin = emit(ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_082_ESPONTANEA_setor_sem_derivadas_e_diferencial_CE.md', tunnel.encode('utf-8'))
config = {
    'source_directories': [
        'SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779',
        'REVISAO_SETOR_FINITO_082_20260910_052417_739397',
        'COMPLEXO_CE_QUADRATICO_082_20260910',
        'REVISAO_CE_QUADRATICO_082_20260910_053047_6990258',
        'OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910',
        'REVISAO_OBSTRUCAO_CE_CORRENTE_082_20260910_053437_900535',
        'REVISOES_RAIZ_082_20260910', DOC_DIR.name],
    'new_exact_arithmetic_controls': 18,
    'new_source_integrity_controls': 1,
    'new_lean_compilations': 0,
    'status': 'ZERO_WEYL_DERIVATIVE_SECTOR_EXCLUDED__D1_IDENTIFIED_AS_KILLING_CE__TARGET_CE_CLASS_AND_GRADIENT_CURRENT_TYPED__FULL_CANCELLATION_OPEN',
    'written_results': [
        'All ten undifferentiated quadratic Weyl invariant contractions have detector image Rher times R(k)=24k^3/z0-96k/z0^3 and cannot cancel the target, by k=2/z0.',
        'The complete diagonal E=q+2 identifies with the Killing Chevalley-Eilenberg complex with coefficients Sym2 M, invariant under isotropy, including all finite jets, curvature and explicit s0 corrections.',
        'The target a=J_W volume(p4) is CE closed; cancellation in the next cut is equivalent to the vanishing of its secondary CE cohomology class, not settled by its nonzero s0 class.',
        'The horizontal natural gradient current obeys s1 qgrad+s0 q6=(Box J_W) volume(p4), with finite h3C3 q6 from the active metric completion; no identification with minus J_W.',
        'One exact rational/exterior execution with 18 algebraic controls and one source-integrity control; written mathematics and independent reviews; no rerun or Lean.'],
    'remaining': [
        'Compute the actual CE image with all quadratic Weyl jets and decide the target class under the same coefficient domain.',
        'Find an admissible combination and a finite primitive for r6+s1Q, or prove target exclusion in the complete relevant image; passing a detector is insufficient.',
        'Actual tower cohomology, remaining anomaly channels and higher lifts, admissibility and causal counterterms, interacting current/charge and QME.',
        'Compatible backgrounds, states and cutoffs, general gravitational reconstruction from the same selected data, and ultraviolet justification.',
        'Canonical integration and formal verification of approved constructions and the 21 absent tracked modules.'],
    'limits': 'Fixed oriented four-dimensional constant-curvature metric reference K>0, fixed nonzero real kappa and constant sigma projected out, inherited inert scalars. Finite sector exclusion does not cover derivative candidates. CE isotropy invariants are not relative cochains; no local finitude for the full Killing algebra or Whitehead shortcut. The quadratic jet module remains a quotient. The secondary CE target class is open, and the gradient current produces Box J rather than a proved cancellation. 18 algebraic plus one integrity controls, no rerun/Lean. No um execution/import, nature test, original or canonical memory write, or gate change. Investigation083 excluded.'
}
config_pin = emit(OUT / 'CONFIG_ENTREGA_082.json',
                   (json.dumps(config, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'adendum': adendum_pin, 'tunnel': tunnel_pin, 'config': config_pin}, ensure_ascii=True))
