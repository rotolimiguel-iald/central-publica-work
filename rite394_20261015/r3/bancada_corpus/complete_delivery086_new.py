from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_086_20260910'
COR_REVIEW = (ROOT / sys.argv[1]).resolve()
DOC_REVIEW = (ROOT / sys.argv[2]).resolve()
assert all(p.is_relative_to(ROOT) and p.is_dir() for p in (COR_REVIEW,DOC_REVIEW))

def pin(path):
    raw=path.read_bytes()
    return {'path':path.as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def emit(path,text):
    raw=text.encode('utf-8')
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    tmp=path.with_name(path.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes()==raw
    tmp.rename(path)
    assert path.read_bytes()==raw
    return pin(path)

def link(label,path):
    return '['+label+'](<'+path.as_posix()+'>)'

cor_notes=sorted(COR_REVIEW.glob('*.md'))
doc_notes=sorted(DOC_REVIEW.glob('*.md'))
assert cor_notes and doc_notes
reviews=[
 ROOT/'REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md',
 ROOT/'REVISAO_CORRENTES_UMA_DERIVADA_086_20260910_065540_575112/PARECER_CLASSIFICACAO_E_NORMALIZACAO_086.md',
 ROOT/'REVISAO_PONTRYAGIN_CARACTERISTICO_086_20260910/PARECER_TRANSGRESSAO_GL_E_CONTRATO_CARACTERISTICO_086.md',
 ROOT/'REVISOES_RAIZ_086_20260910/PARECER_SIMBOLO_TRANSGRESSAO_E_CORRENTES_086.md',
] + cor_notes + doc_notes
sources=reviews+[OUT/'REEXAME_SUFICIENCIA.md',OUT/'MEMORIA_DE_TRABALHO_086.md',
                OUT/'DESENHO_DO_FECHAMENTO_ADENDO_086.md',OUT/'ESTADO_CANONICO_086.json',
                ROOT/'REEXAME_SUFICIENCIA_085_20260910/RESULTADO_ENTREGA_085.json']
before=[pin(p) for p in sources]
snapshot=json.loads((OUT/'ESTADO_CANONICO_086.json').read_bytes())
assert snapshot['seal_um_hash_matches'] and snapshot['all_read_sources_unchanged']
assert all(row['unchanged'] for row in snapshot['comparison_with_delivery085'])
previous=json.loads((ROOT/'REEXAME_SUFICIENCIA_085_20260910/RESULTADO_ENTREGA_085.json').read_bytes())

adendum='''# Adendo final086 — revisões, alcance e custódia

10/09/2026. [DERIVED — demonstrações escritas com revisões independentes específicas]. As fontes foram publicadas durante sua investigação e conservam suas marcas históricas de revisão pendente. Este adendo registra os pareceres posteriores ao lado, sem reescrever as notas.

A prova por símbolo, de Herschel, recebeu revisão integral de Turing. A classificação W·∇W, de Singer, recebeu revisão integral de Herschel. A transgressão GL e o contrato característico, de Turing, receberam revisão integral de Singer. A raiz leu as três notas e os três pareceres e registrou sua conferência separadamente. Não foram identificados erros materiais no domínio declarado.

Os corolários CE/cúbicos foram escritos pela raiz e receberam revisão específica de Singer. Sua contribuição histórica para a transgressão077 é explicitada na proveniência; a contagem077 e o ciclo então construído são consumidos junto com seus pareceres posteriores, não por autoaprovação. A revisão independente atual examina a dedução dos novos mapas086. A conferência da raiz sobre as outras notas não é aprovação de sua própria dedução.

'''
adendum+='\n\n'.join(link(p.stem,p) for p in reviews)+'\n\n'
adendum+='''[DERIVED] A pendência080 foi decidida negativamente no domínio fixado: não existe corrente natural quadrática finita com divV=J_W, e nenhuma correção admissível preserva o líder cúbico não nulo até C₆. A prova cobre todas as ordens FINITAS pelo símbolo principal; não se limita aos candidatos examinados em082–084. As notas anteriores conservam sua pendência histórica, agora resolvida por este arco.

[DERIVED] H³(C(g,N₂)^h,dCE)=0 e λ↦λ[J_Wν] injeta Rher em H⁴ CE. A imagem H³(C_N)→H³(C₃) é zero para N≥6 e também para a projeção do complexo formal definido por valência. Isso é functorialidade de projeções; não é permuta entre cohomologia e limite inverso. Não se afirmou H³(C_N)=0, nem H³ completo nulo, nem Mittag-Leffler para todos os alvos.

A inexistência de primitiva invariante é compatível com d tr(L DbarL)=J_Wvol na apresentação GL: essa primitiva ordinária tem defeito gauge on-shell e está em um complexo maior. A nota característica delimitou a rota bibliográfica; a prova por símbolo realizou a comparação adicional. J_W é o pseudoescalar, não J=Luz.

Precisão de normalização para integração: I086=(1/2)W²=I082/2; J permanece igual. A classificação com uma derivada usa spins j, e a classificação simbólica usa pesos inteiros2j. Os nomes Mcal, Mghost e as matrizes de conexão não são intercambiáveis. A filtração soma as ordens dos dois fatores e trata K fixado como grau zero, sem confundi-la com dimensão de engenharia.

[REAL — contabilidade] Zero novas execuções matemáticas, CAS, Lean ou testes de natureza086. Os cálculos foram demonstrações escritas reexaminadas; os números de verificações nos manifestos são documentais, de pins/caminhos/preservação. As contagens das execuções antigas não foram reapresentadas como novas.

O resultado085 foi emitido em @PREVIOUS_TIME@. Esta entrega086 o sucede e não altera nenhum artefato anterior. Investigações087 permanecem fora do presente resultado.

[REAL — canônico] Duas inspeções de leitura086 concordam com085: os quatro artefatos permanecem idênticos no caminho canônico, com683 arquivos embutidos e77 dos98 módulos acompanhados presentes. Os21 ausentes constam do snapshot. A lista AST é presença de fonte, não compilação nova. A atualização mencionada pelo operador ainda não foi localizada nesse caminho; não se presume inexistência de uma cópia de preparação externa.

A navegação canônica continua emv338. Sua divergência histórica sobre “última custódia completa” (v320 no índice e v336 no append do Atlas) foi preservada e não serve como prova de versão sucessora. Não foi feita auditoria dos recibos de custódia dessas duas versões para decidir essa frase.

[OPEN] Permanecem reconstrução geral pelos mesmos dados selecionados, matéria/conservação/área e atlas físico compatível, os grupos/setores/limites BRST ainda necessários à construção interagente, admissibilidade causal, QME e UV. Fase/ramo e H3 interno do um.py não são reabertos. Ghost quatro não é anomalia física de ghost um.

[REAL — preservação] A memória e o desenho foram registrados em arquivos novos de Chatgpt. Atlas, índice, memórias canônicas, acervo, programa, selo e gate ficaram intactos. Nenhum resultado de confirmação ou falsificação física é inferido desta investigação cohomológica. O objetivo geral permanece ativo.
'''
adendum=adendum.replace('@PREVIOUS_TIME@',previous['created_utc'])
emit(OUT/'ADENDO_REVISOES_086.md',adendum)

config={
 'source_directories':[
  'SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910',
  'REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684',
  'CORRENTES_WEYL_UMA_DERIVADA_086_20260910',
  'REVISAO_CORRENTES_UMA_DERIVADA_086_20260910_065540_575112',
  'PONTRYAGIN_CARACTERISTICO_E_LIMITE_BBH_086_20260910_062514_4956488',
  'REVISAO_PONTRYAGIN_CARACTERISTICO_086_20260910',
  'COROLARIOS_CE_E_LIDER_CUBICO_086_20260910',
  COR_REVIEW.relative_to(ROOT).as_posix(),
  'REVISOES_RAIZ_086_20260910',
  'INSPECAO_CANONICO_NAVEGACAO_086_20260910',
  DOC_REVIEW.relative_to(ROOT).as_posix()],
 'new_exact_arithmetic_controls':0,'new_source_integrity_controls':0,'new_lean_compilations':0,
 'status':'FINITE_NATURAL_QUADRATIC_DIVERGENCE_INJECTIVE__CE3_QUADRATIC_ZERO__CUBIC_LEADER_IMAGE_ZERO_FROM_C6__GENERAL_INTERACTING_GOAL_OPEN',
 'written_results':[
  'Strictness of the linear Einstein EOM image gives a derivative-compatible injection of the curved gauge-invariant associated graded into the flat effective Weyl module.',
  'All finite-order natural quadratic vectors have injective divergence; a nonzero vector has divergence order at least six, while J_W has nonzero order four. No finite natural current solves divV=J_W.',
  'Exactly one additional Weyl derivative yields A gradI+B gradJ, I=one-half W squared; both vectors and their divergences are independent, and J is outside their divergence image even allowing invariant Euler coefficients.',
  'Ordinary GL transgression is explicit off shell, but its quadratic primitive is not gauge invariant even on the linear shell; its larger-complex exactness does not supply a current in the effective natural module.',
  'Quadratic CE degree-three cohomology is zero; the Rher-line generated by J_W nu injects into degree-four CE cohomology, including inert nilpotent coefficients.',
  'The image of H3(C_N) in H3(C3) is zero for every N>=6; the defined formal complex has the same zero cubic image by composition, without an inverse-limit cohomology exchange.',
  'Specific independent written reviews, root rederivation and two read-only canonical inspections; no new mathematical execution or formal compilation.'],
 'remaining':[
  'Compute the remaining BRST sectors, degrees, later leaders and compatible truncation maps required by the interacting anomaly criterion; the full groups and inverse-limit issues remain open.',
  'Relate the fixed constant-sigma metric test to the physical system, admissible causal counterterms, interacting current/charge and QME.',
  'Realize general gravitational reconstruction, matter, conservation and area from the same selected data, with a compatible physical atlas.',
  'Justify the ultraviolet route independently of finite verification capacity.',
  'Locate and audit any newer coding-session successor; the inspected canonical v338 still lacks21 of98 tracked integration modules. Integrate and validate written086 results only with their full contracts.'],
 'limits':'Fixed oriented four-dimensional Lorentzian space-form K>0, nonzero real kappa, constant-sigma metric projection, inert inherited real algebra, finite jets per coefficient and no tensor spectators. Quadratic CE and the cubic image are computed, not the full interacting BRST, physical anomaly or QME. No original edits, new mathematical execution, CAS, Lean, nature test or gate change.'
}
emit(OUT/'CONFIG_ENTREGA_086.json',json.dumps(config,ensure_ascii=False,indent=2)+'\n')
tunnel='''# ENTREGA086 — divergência injetiva e destino do líder cúbico

10/09/2026. [DERIVED — demonstrações escritas com revisões independentes específicas]. Entrega para a sessão que integra o um.py; originais preservados.

A pendência080 sobre uma correção alternativa que conserve o líder cúbico está decidida no contrato fixado. A prova por estriteza das EOM, símbolo plano e realização métrica das duas quiralidades exclui divV=J_W para TODA corrente natural quadrática de ordem finita. A divergência também tem núcleo zero. K é real fixado e de grau zero nessa filtração; as ordens dos fatores são somadas. O anel Rher é inerte e pode conter nilpotentes.

Da forma normal084 e de N₂^g=0 em085 seguem H³(C(g,N₂)^h)=0 e a injeção λ↦λ[J_Wν] em H⁴ CE. Usando os mapas077/080/082, a imagem H³(C_N)→H³(C₃) é zero para todo N≥6: os líderes cúbicos não nulos não se prolongam. Isso não anula H³(C_N) inteiro e não calcula anomalia física/QME. A projeção do complexo formal se fatora por C₆, sem troca de cohomologia com limite inverso.

A classificação explícita W·∇W dá A gradI+B gradJ, com I=(1/2)W². Cuidado: I082=2I086; J não muda. A transgressão GL ordinária tem primitiva off-shell, mas ela falha na invariância gauge on-shell; não contradiz a impossibilidade na classe natural efetiva.

Ao integrar, conservar referência espaço-forma orientada4D, K>0 eκ fixos, projeção sigma constante, módulo Weyl/EOM real efetivo, coeficientes inertes, finitos jatos por coeficiente e ausência de espectadores. Mcal não é Mghost; J_W não é J=Luz. Não promover uma bandeira documental a compilação formal ou a resultado do sistema físico completo.

O canônico lido continua v338, com77/98 módulos acompanhados presentes;21 ausentes. A nova versão mencionada ainda não foi localizada nesse caminho. Zero execução matemática, CAS, Lean ou natureza086. Permanecem reconstrução pelos mesmos dados, demais setores/limites BRST, QME, integração e UV. Fase/ramo e H3 da tela continuam reconhecidos.

'''
tunnel+='\n\n'.join([
 link('Relatório086',OUT/'REEXAME_SUFICIENCIA.md'),
 link('Corolários e prova dos mapas',ROOT/'COROLARIOS_CE_E_LIDER_CUBICO_086_20260910/COHOMOLOGIA_CE3_E_IMAGEM_CUBICA_ZERO_APOS_C6.md'),
 link('Revisões e proveniência',OUT/'ADENDO_REVISOES_086.md'),
 link('Memória de trabalho',OUT/'MEMORIA_DE_TRABALHO_086.md'),
 link('Desenho do fechamento',OUT/'DESENHO_DO_FECHAMENTO_ADENDO_086.md'),
 link('Manifesto final',OUT/'MANIFESTO_ENTREGA_086.json')])+'\n'
emit(ROOT/'TUNEL/DO_CHATGPT/ENTREGA_086_ESPONTANEA_divergencia_injetiva_e_lider_cubico.md',tunnel)
assert before==[pin(p) for p in sources]
print(json.dumps({'adendum':pin(OUT/'ADENDO_REVISOES_086.md'),'source_directories':config['source_directories']},ensure_ascii=True))
