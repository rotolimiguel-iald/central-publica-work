from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'REEXAME_SUFICIENCIA_087_20260910'
assert len(sys.argv)==4, 'Pass criterion review, documentary review and current canonical note paths.'
criterion_review, document_review, canonical_note = [Path(x).resolve() for x in sys.argv[1:]]
for p in (criterion_review,document_review,canonical_note):
    assert p.is_relative_to(ROOT) and p.is_file()

def new(path, data):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    raw=data.encode('utf-8') if isinstance(data,str) else data
    assert raw
    tmp=path.with_name(path.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes()==raw
    tmp.rename(path)
    assert path.read_bytes()==raw

def link(label,path):
    path=Path(path)
    assert path.is_file()
    return '['+label+'](<'+path.as_posix()+'>)'

sources = [
 'CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910',
 'COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612',
 'CLASSE_PAR_BRST_COMPLETA_087_20260910',
 'CONTRATO_CRITERIO_ANOMALIAS_087_20260910',
 'REVISAO_CE_LINEAR_087_20260910_072356_6364824',
 'REVISAO_RELATIVO_QUADRATICO_087_20260910',
 'REVISAO_CLASSE_PAR_BRST_087_20260910',
 'REVISOES_RAIZ_087_20260910',
 criterion_review.parent.name,
 document_review.parent.name,
 canonical_note.parent.name,
]
assert len(sources)==len(set(sources))
reviews={
 'N₁ de Herschel — revisão Turing':'REVISAO_CE_LINEAR_087_20260910_072356_6364824/PARECER_ACICLICIDADE_LINEAR_E_D1_087.md',
 'N₂ de Turing — revisão Singer':'REVISAO_RELATIVO_QUADRATICO_087_20260910/PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md',
 'Composição H⁴ da raiz — revisão Herschel':'REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md',
 'Consumo efetivo da revisão N₂ na composição':'REVISAO_CLASSE_PAR_BRST_087_20260910/ADENDO_CONSUMO_REVISAO_N2_087.md',
 'Revisão da raiz dos setores CE':'REVISOES_RAIZ_087_20260910/PARECER_CE_LINEAR_QUADRATICO_E_ALCANCE_087.md'
}
adendo='# Adendo087 — revisões e alcance final\n\n10/09/2026. [DERIVED — matemática escrita com revisões delimitadas]. [REAL — custódia documental].\n\n'
adendo+='As referências a revisão pendente nas fontes são retratos da emissão original. As etapas abaixo foram agora publicadas e lidas pela raiz, sem alterar essas fontes congeladas.\n\n'
adendo+='\n'.join('- '+link(label,ROOT/path)+'.' for label,path in reviews.items())+'\n\n'
adendo+='A '+link('revisão delimitada do critério074',criterion_review)+' confere as cinco condições suficientes, a filtração por formas e o contrato causal072. As outras importações catalogadas na auditoria conservam o alcance das fontes e não são promovidas a nova auditoria integral. A '+link('revisão documental dos narrativos',document_review)+' examina relatório, memória e desenho; não substitui as revisões matemáticas.\n\n'
adendo+='A '+link('inspeção complementar do canônico',canonical_note)+' e a '+link('captura087',OUT/'ESTADO_CANONICO_087.json')+' registram o estado disponível do programa. O reexame não declara um sucessor não encontrado como auditado. A ausência de 21 nomes no pacote rastreado é uma pendência de integração no canônico, não uma contagem de 21 problemas físicos.\n\n'
adendo+='## Precisões mantidas\n\n'
adendo+='s completo significa BV–BRST CLÁSSICO completo por valência. H⁴ contém a linha livre da densidade par, mas seu grupo inteiro não foi classificado. Pontryagin completo é s-exato por uma primitiva que começa em valência inferior. Esses resultados não contradizem a classificação CE quadrática e não identificam ghost quatro com anomalia física de ghost um.\n\n'
adendo+='O setor linear acíclico e o quadrático com graus4/7/10 são cohomologias CE após o primeiro diferencial por valência. A prova da classe par é adicional e usa a conexão entre truncamentos, incluindo possíveis primitivas com antifields. O detector em C₆ evita trocar limite inverso com cohomologia.\n\n'
adendo+='O critério074 exige, entre outros canais, H¹(Ē;H⁴(s))=0; não exige H⁴(s)=0. A classe par não refuta esse critério. Uma alternativa suficiente continua sendo uma primitiva local admissível da anomalia concreta. Descida natural, eliminação cohomológica e admissibilidade causal são obrigações diferentes.\n\n'
adendo+='A referência desta bancada tem sigma constante projetado e coeficientes inertes; o sistema físico Q2 com sigma não constante conserva seu contrato próprio. Fase/ramo e H3 interno do programa não foram reabertos. QME, UV e reconstrução geral dos mesmos dados continuam abertos. Nenhum resultado087 é declarado incorporado ao um.py.\n\n'
adendo+='Somente arquivos novos em Chatgpt. Atlas, índice vivo e memórias canônicas permanecem fontes únicas somente de leitura; a memória de trabalho e o adendo ao desenho novos acompanham esta entrega para integração pela casa responsável. Zero nova execução matemática, CAS, Lean, programa canônico, rito de natureza ou alteração de gate. Os controles finais são documentais.\n'
new(OUT/'ADENDO_REVISOES_087.md',adendo)

config={
 'source_directories':sources,
 'new_exact_arithmetic_controls':0,
 'new_source_integrity_controls':0,
 'new_lean_compilations':0,
 'status':'LINEAR_CE_ACYCLIC__QUADRATIC_RELATIVE_AND_CE_CLASSIFIED__CLASSICAL_BRST_EVEN_H4_LINE_NONZERO__INTERACTING_QME_OPEN',
 'written_results':[
  'The finite-jet linear Weyl coefficient module N1 has zero isotropy-invariant CE cohomology in every degree; this is the m=1 diagonal after d1, not zero H(s0).',
  'The quadratic relative complex has free rank two in degree4 and vanishes otherwise; its full isotropy-invariant CE cohomology has ranks2/4/2 in degrees4/7/10.',
  'Curved scalar generation by I_r,J_r and the triangular box recurrence with diagonal2 give the relative quotient with finite primitives and inert inherited coefficients, including nilpotents.',
  'The full natural even Weyl-square ghost4 density supplies a free inherited-coefficient line in classical BRST H4(C_N) for every N>=6 and in the formal complex, detected already in C6 and including antifield primitives.',
  'The full Pontryagin ghost4 density is classical-BRST exact; its lower-valence primitive explains why its CE leading class is nevertheless nonzero.',
  'The anomaly sufficiency criterion is typed by ghost and form degrees. Nonzero H4(s) alone does not disprove the criterion; causal admissibility and the physical nonconstant-sigma system remain distinct.',
  'Independent source reviews, composition review, limited criterion review, narrative review and stable canonical read-only comparison accompany the delivery.'
 ],
 'remaining':[
  'Resolve the remaining full classical BRST and horizontal coefficient groups required by the sufficient anomaly criterion, or construct an admissible primitive of the actual consistent anomaly.',
  'Pass from the fixed constant-sigma metric test to the physical nonconstant-sigma system and satisfy causal normalization, insertions, contacts, interacting observables/state and QME.',
  'Realize geometry, matter, conservation, area and a compatible physical atlas from the same selected data for general gravitational reconstruction.',
  'Justify the ultraviolet route independently of finite verification capacity.',
  'Locate and audit any newer coding-session successor and integrate the tracked remaining modules with their contracts; the inspected canonical file is still v338.'
 ],
 'limits':'Written mathematics with delimited independent reviews, not new Lean or CAS. Fixed oriented four-dimensional Lorentzian space-form K>0, nonzero real kappa, projected constant sigma, inert inherited real algebra and finite jets per coefficient. No exhaustive full BRST classification, physical anomaly computation, quantum operator, QME or UV closure. No original edits, canonical execution, nature test or gate change.'
}
new(OUT/'CONFIG_ENTREGA_087.json',json.dumps(config,ensure_ascii=False,indent=2)+'\n')

tunnel='# ENTREGA087 — CE linear/quadrático e classe par no BRST clássico\n\n10/09/2026. [DERIVED — matemática escrita revisada; não incorporada ao canônico].\n\n'
tunnel+='O '+link('reexame completo',OUT/'REEXAME_SUFICIENCIA.md')+' acompanha a '+link('memória de trabalho',OUT/'MEMORIA_DE_TRABALHO_087.md')+', o '+link('adendo ao desenho',OUT/'DESENHO_DO_FECHAMENTO_ADENDO_087.md')+' e o '+link('adendo de revisões',OUT/'ADENDO_REVISOES_087.md')+'.\n\n'
tunnel+='Avanço087: N₁ CE é acíclico; N₂ relativo tem somente grau4 de posto2, e CE inteiro graus4/7/10 de postos2/4/2. A densidade par completa de Weyl fornece uma linha livre em H⁴ do BRST CLÁSSICO completo, com detector em C₆; Pontryagin completo é s-exato. As demonstrações e revisões específicas estão vinculadas no relatório.\n\n'
tunnel+='A identificação CE e a conclusão BRST completa são etapas distintas. A segunda inclui todas as primitivas com antifields e não troca cohomologia com limite inverso. O teste fixa sigma constante projetado e jatos finitos por coeficiente. Não transportar por nome para o fundo físico sigma=id.\n\n'
tunnel+='O critério de anomalias exige a cohomologia horizontal com coeficientes em H(s), além dos outros graus; a nova linha em H⁴ não é, sozinha, uma anomalia física nem refuta o critério. A próxima integração deve conservar as hipóteses e a admissibilidade causal. QME, UV e reconstrução geral dos mesmos dados continuam abertos.\n\n'
tunnel+='Canônico disponível: v338, quatro arquivos de referência idênticos à captura086,683 arquivos embutidos e77 dos98 módulos rastreados presentes. Não foi executado/importado um.py. Os21 nomes ausentes do canônico são rastreamento de integração. Nenhuma incorporação087 é presumida.\n\n'
tunnel+='Zero nova execução matemática/CAS/Lean/rito; integridade documental medida no manifesto final da pasta do reexame. Somente arquivos novos em Chatgpt, sem tocar originais, Atlas, memórias canônicas, selo ou gate.\n'
new(ROOT/'TUNEL/DO_CHATGPT/ENTREGA_087_ESPONTANEA_ce_linear_quadratico_e_classe_par_brst.md',tunnel)
print(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'sources':sources,'new_only':True},ensure_ascii=True))
