from pathlib import Path
from datetime import datetime
import os, json, hashlib, sys
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'REEXAME_SUFICIENCIA_078_20260910'
doc=Path(sys.argv[1]).resolve()
assert doc.is_relative_to(ROOT) and doc.is_dir() and doc.name.startswith('REVISAO_DOCUMENTAL_RELATORIO_078')
files=list(doc.glob('PARECER*.md'));assert len(files)==1
dp=files[0]
created=[]
def link(p,label):return '['+label+'](<'+p.as_posix()+'>)'
def new(p,s):
    p=p.resolve();assert p.is_relative_to(ROOT) and not p.exists()
    raw=s.encode('utf-8');q=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with q.open('xb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    assert q.read_bytes()==raw
    q.rename(p);assert p.read_bytes()==raw
    created.append({'path':p.as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
new(OUT/'ADENDO_REVISOES_078.md',"""# Adendo de revisões078

10/09/2026. [DERIVED — matemática escrita revisada] [REAL — controles simbólicos e documentais].

O certificado A6, de Singer, foi lido integralmente pela raiz e por Turing. O parecer independente e a revisão da raiz concordam no alcance: a classe específica construída em C5 não levanta para C6; outras classes com o mesmo líder não foram excluídas. A leitura de z como coordenada temporal sugeriu inicialmente uma troca de sinal; o revisor reconheceu e retirou essa objeção após conferir a ordem (τ,x,y,z), com z espacial. O sinal Λ=+3/ℓ² permanece na convenção efetivamente declarada e foi conferido diretamente.

A nota sobre potência e Mittag–Leffler, de Turing, deve ser consumida com ADENDO_DOMINIO_DAS_FIBRAS_E_INDUCAO_078.md. Herschel detectou a precisão necessária sobre a avaliação dos germes suaves; o autor publicou o adendo, e o revisor confirmou o conjunto. A indução de contratermos usa vértices anteriores e condições de normalização, não o contratermo ainda desconhecido. O arquivo .pending preservado na pasta é rascunho histórico, não texto aprovado a integrar.

A comparação dos quatro anéis é da raiz e foi revisada integralmente por Herschel, sem correção material. A prova suave por cortes e divisão exata não fornece automaticamente dependência analítica ou natural em B0. A não estabilização das imagens não foi convertida em lim¹ não nulo da torre real.

Os 122 controles consistem em 17 Weyl pontual e 105 Einstein linearizado/Killings. Turing fez revisão estática dos scripts e recibos; não há segundo CAS independente. O campo de estabilidade documental do recibo de Einstein mede o intervalo posterior ao cálculo simbólico, durante a construção daquele recibo. Os 17 controles pontuais, produzidos durante a investigação077, foram excluídos da entrega077 e entram agora. Os 420 controles CE permanecem da077.

O parecer documental dos três documentos da entrega e da captura é:
"""+link(dp,'Revisão documental078')+"""

As fontes autorais conservam seus estados históricos anteriores às revisões. Os pareceres e os adendos posteriores são a evidência que completa a presente entrega; nenhuma fonte foi reescrita para aparentar aprovação anterior.

O finalizador foi copiado da077, com substituições registradas em PROVENIENCIA_FINALIZADOR_078.json; a captura possui proveniência própria. O manifesto final verifica integridade documental, não novas provas matemáticas. Todos os arquivos canônicos permanecem somente leitura. Zero Lean, zero execução/importação de um.py, zero rito de natureza ou alteração de gate. Investigação079 excluída; objetivo geral aberto.
""")
new(ROOT/'TUNEL/DO_CHATGPT/ENTREGA_078_ESPONTANEA_residuo_A6_e_comparacao_de_completacoes.md',"""# Entrega078 — resíduo A6 e comparação de completações

10/09/2026. Para a sessão que codifica o um.py. [DERIVED — matemática escrita revisada] [REAL — 122 asserções simbólicas exatas].

Incorporar com as notas, adendos e revisões:

1. A6 é s0-fechado e não s0-exato na classe local regular que admite o teste construído. A avaliação numa solução de Einstein linearizada e quatro Killings dá −4k/z0 θ0θ1θ2θ3≠0, incluindo a exclusão de primitivas com antifields.
2. r6=A6−s0α6. A classe específica [T≤5] da077 não vem de H³(C6). Não declarar que todo levantamento do mesmo líder cúbico foi excluído; a liberdade de correções anteriores continua aberta.
3. Preservar s0u*=+H0u e a convenção com z espacial, Ric(g0)=+3g0/ℓ². Não confundir valência seis/ghost4/forma zero com a anomalia quântica local.
4. A contagem de potência para gráficos especificados não prova finitude de todas as cochains Q2. Consumir a nota de potência com seu adendo de domínio das fibras e de indução.
5. Na torre auxiliar ×x, lim¹ é o quociente aditivo de séries formais pelo anel nos casos polinomial e analítico; é zero nos casos formal e suave. O limite suave é o ideal plano. Nenhuma das quatro torres é ML. Não importar a resposta para o BRST gravitacional sem comparação admissível.

Há 17 controles pontuais de Weyl e 105 de Einstein linearizado/Killings; revisão independente estática, sem novo CAS e sem Lean. Os números do manifesto são documentais. A custódia temporal do recibo de Einstein foi delimitada no adendo.

O canônico recapturado permanece v338, com quatro pins iguais077; 77/98 módulos acompanhados presentes, 21 ausentes. Nenhum original executado ou alterado. A integração ausente é pendência distinta da suficiência matemática geral.

"""+link(OUT/'REEXAME_SUFICIENCIA.md','Relatório completo')+'\n\n'+
link(OUT/'ADENDO_REVISOES_078.md','Adendos e revisões')+'\n\n'+
link(OUT/'MEMORIA_DE_TRABALHO_078.md','Memória da etapa')+'\n\n'+
link(OUT/'DESENHO_DO_FECHAMENTO_ADENDO_078.md','Desenho do caminho crítico')+'\n\n'+
link(OUT/'MANIFESTO_ENTREGA_078.json','Manifesto de integridade')+"""

Ainda faltam os canais completos de cohomologia e sua comparação admissível, remoção de anomalia/contratermos/QME, compatibilidades, reconstrução pelos mesmos dados e rota UV. Fase, ramo, H3 interno e falsificadores existentes permanecem preservados. A investigação079 fica fora desta entrega.
""")
config={
'source_directories':[
'RESIDUO_PONTRYAGIN_S0_078_20260910',
'REVISAO_RESIDUO_PONTRYAGIN_078_20260910_033403_7284198',
'FINITUDE_POTENCIA_E_ML_078_20260910_032141_4248196',
'REVISAO_POTENCIA_ML_078_20260910_033833_847040',
'COMPARACAO_LIM1_COEFICIENTES_078_20260910',
'REVISAO_QUATRO_ANEIS_078_20260910_034444_267940',
'CONTROLE_WEYL_PONTUAL_078_20260910',
'CONTROLE_EINSTEIN_LINEARIZADO_078_20260910',
'REVISAO_ESTATICA_CONTROLES_078_20260910_034002_0294036',
'REVISOES_RAIZ_078_20260910',
doc.name],
'new_cas_controls':122,'new_lean_compilations':0,
'status':'SPECIFIC_C5_PONTRYAGIN_CLASS_OBSTRUCTED_AT_C6__COEFFICIENT_COMPLETIONS_COMPARED__ALTERNATIVE_LIFTS_AND_FULL_QUANTUM_THEORY_OPEN',
'written_results':[
'Explicit chain evaluation on a linearized Einstein solution and four background Killings proves [A6] nonzero in H4(s0) at valence6.',
'The specific C5 Pontryagin class constructed in077 is not in the image from C6; other C5 classes with the same cubic leader remain undecided.',
'122 exact symbolic controls: 17 Weyl point and 105 direct linearized Einstein/Killing identities, with independent static review.',
'Power counting and coefficient families refute automatic finite-dimensionality arguments for the full cochain category; domain and induction adendum included.',
'For the auxiliary multiplication-by-x tower, lim and lim1 are computed separately over polynomial, analytic, formal and smooth germ coefficients; no automatic transfer to the real BRST tower.'
],
'remaining':[
'Alternative admissible lower-order corrections with the same cubic leader, including antifield contributions, and subsequent lifts.',
'Actual truncation cohomology, admissible inverse-limit comparison and other anomaly-criterion channels.',
'Anomaly primitive, causal counterterms, interacting current/charge and QME.',
'Compatible references, states and cutoffs; general gravitational reconstruction from the same selected data; justification of the UV route.',
'Canonical integration and appropriate formal verification of approved written constructions and missing tracked modules.'
],
'limits':'Minimal classical local jet test on a constant-curvature reference with constant sigma background; no new physical Hadamard representation. A6 has ghost4/form0/valence6 and is not an unavoidable quantum anomaly. Auxiliary coefficient towers do not compute real gravitational BRST lim1. 122 CAS assertions and documentary checks have distinct scopes; no independent CAS rerun. No Lean, nature test, um execution/import, original or canonical-memory edit or gate change. Stage079 excluded.'
}
new(OUT/'CONFIG_ENTREGA_078.json',json.dumps(config,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(created,ensure_ascii=True))

