from pathlib import Path
from datetime import datetime
import os,json,hashlib,sys
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'REEXAME_SUFICIENCIA_076_20260910'
rd=Path(sys.argv[1]).resolve()
assert rd.is_relative_to(ROOT) and rd.is_dir() and rd.name.startswith('REVISAO_DOCUMENTAL_RELATORIO_076')
notes=list(rd.glob('PARECER*.md'))
assert len(notes)==1
review=notes[0]
created=[]
def new(p,text):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    b=text.encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with t.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert t.read_bytes()==b
    t.rename(p)
    assert p.read_bytes()==b
    created.append({'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
def link(p,label):
    return '['+label+'](<'+p.as_posix()+'>)'
new(OUT/'ADENDO_REVISOES_076.md',"""# Adendo de revisões076

10/09/2026. [DERIVED — matemática escrita revisada] [REAL — integridade documental].

As notas da etapa076 foram consumidas com revisões específicas:
- módulos/setor K e homotopia formal do alvo: autoria Singer, revisão Herschel e leitura integral da raiz;
- levantamento das correntes sigma: autoria Singer, revisão Herschel, com precisão de lift cotangente/Rees, e leitura integral da raiz;
- mudança de base, teste global SU2 e sequência de completação: autoria Turing, revisão escrita da raiz;
- transgressão BRST característica: autoria da raiz, revisão independente escrita de Singer, lida integralmente pela raiz.

Os estados “aguardando revisão” dos manifestos e textos autorais permanecem como registros anteriores. Este adendo os acompanha com os pareceres posteriores; não foram sobrescritos. A revisão de uma nota não foi reaproveitada como aprovação de outra.

Precisões de consumo: seis correntes não provam dim H³=6; o volume S³ é globalmente não trivial no setor orientado usado pelo teste e formalmente exato junto a φ0; O4 deve agir conjuntamente nos coeficientes e classes. A mudança de base finita não é uma isomorfia já demonstrada para toda a completação. O termo lim¹ e os mapas de truncagem permanecem visíveis.

Na transgressão, −DS S⁻¹ inclui sS, preservando compatibilidade com g0. A relação sT_0³=A_P refere-se aos ciclos característicos de ghost4. A classe diagonal de Euler(g0), em ghost0/forma4, permanece. Grau total4 não é a anomalia de grau total5.

As duas primeiras tentativas de criação por patch foram distintas: na etapa076 houve um patch inválido do criador da transgressão, rejeitado antes de qualquer escrita. A versão subsequente usou geração das linhas do patch e foi executada com sucesso. Nenhuma fonte ou arquivo existente foi modificado por essa falha.

""".replace('As duas primeiras tentativas de criação por patch foram distintas: na etapa076 houve','Na etapa076 houve')+
link(review,'Parecer documental independente do conjunto')+"""

Os controles finais de hashes e vínculos são documentais. Zero CAS/Lean/diagramas/natureza novos; nenhum um.py executado/importado. Originais, Atlas, índice, memórias canônicas, selo e gate permanecem intactos. Trabalho077 posterior não integra esta custódia.
""")
new(ROOT/'TUNEL/DO_CHATGPT/ENTREGA_076_ESPONTANEA_modulos_BRST_correntes_e_transgressao_caracteristica.md',"""# Entrega076 — representantes e relações para a cohomologia

10/09/2026. Destinada à sessão que codifica o um.py. [DERIVED — demonstrações escritas revisadas]. O canônico relido permanece v338 com os mesmos quatro pins da075; nenhum programa original foi executado ou alterado.

Incorporar com os antecedentes e adendos:
1. E_N=C_N=0 no setor K de tensores ativos/antifields e c não derivado; ciclos A_L.
2. Primitiva formal τ3=sK2 do volume S³, inclusive quando φ0 varia.
3. Levantamentos α_X=𝒥_X^μη_μ+(φ*·X)η das seis correntes de Killing, sα_X=0 off-shell. Preservar densitização e o lift cotangente dos antifields.
4. Transgressão total com transporte métrico S incluindo sS: s(T_P)_0³=A_P para Euler/Pontryagin ativas. A classe diagonal de Euler(g0) permanece.
5. Mudança de base no domínio separado finito, teste da classe global SU2 e sequência de lim¹/lim para as truncagens naturais.

Não converter esses itens em “anomalia removida”, QME ou dimensão de H³ igual a seis. As relações de chegada e a geração dos módulos completos ainda precisam ser demonstradas na classe natural formal efetiva. A primitiva da anomalia de grau total5 e sua admissibilidade causal continuam abertas.

O objetivo geral mantém reconstrução gravitacional pelos mesmos dados selecionados, compatibilidade entre fundos/estados e rota UV. Fase, ramo, H3 interno e os falsificadores existentes são preservados.

"""+link(OUT/'REEXAME_SUFICIENCIA.md','Relatório completo')+'\n\n'+
link(OUT/'ADENDO_REVISOES_076.md','Revisões e precisões')+'\n\n'+
link(OUT/'MEMORIA_DE_TRABALHO_076.md','Memória da etapa')+'\n\n'+
link(OUT/'DESENHO_DO_FECHAMENTO_ADENDO_076.md','Caminho crítico')+'\n\n'+
link(OUT/'MANIFESTO_ENTREGA_076.json','Manifesto de integridade')+"""

Todas as escritas desta entrega são arquivos novos da bancada. Eventuais revisões de rascunhos dos próprios revisores têm backups de bytes preservados. Originais intactos; gate não movido.
""")
new(OUT/'CONFIG_ENTREGA_076.json',json.dumps({
 'source_directories':[
 'MODULOS_BRST_EBAR_076_20260910',
 'REVISAO_MODULOS_EBAR_076_20260910_024011_189592',
 'REVISAO_CORRENTES_KILLING_076_20260910_024518_164234',
 'MUDANCA_BASE_BRST_076_20260910_024632_6031800',
 'TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910',
 'REVISAO_TRANSGRESSAO_BRST_076_20260910',
 'REVISOES_RAIZ_076_20260910',
 rd.name],
 'new_cas_controls':0,'new_lean_compilations':0,
 'status':'WRITTEN_BRST_CYCLES_AND_FORMAL_PRIMITIVES__FINITE_BASE_CHANGE_AND_COMPLETION_SEQUENCE__FULL_ANOMALY_OPEN',
 'written_results':[
 'Explicit K sector with E_N=C_N=0 and density cycles; formal primitive of the S3 volume cycle.',
 'Six explicit off-shell Killing-current BV lifts with signs, densities and cotangent/Rees transport.',
 'Natural formal characteristic transgression and ghost-three primitives of Euler/Pontryagin ghost-four cycles.',
 'Finite separated base-change theorem, joint target invariants and global oriented S3 class lost at the formal diagonal.',
 'Exact inverse-limit comparison for natural valence truncations, with lim1 terms retained.'
 ],
 'remaining':[
 'Full natural formal H3/H4 generators and relations, cohomology of truncations and transition maps, other required degrees and E2 groups.',
 'Admissible total anomaly primitive and compatible all-order causal counterterms; current/charge implementation and QME.',
 'Perturbative agreement and compatible background/state/cutoff families.',
 'General gravitational reconstruction from the same selected TGL data and justified UV route.',
 'Canonical integration and appropriate formal verification of absent modules and written constructions.'
 ],
 'limits':'Written mathematics with separate reviews in explicit categories. Six currents are not dim H3; ghost-four characteristic exactness is not anomaly-degree-five exactness; finite tensor base change is not completed base change. No CAS/Lean/diagrams/nature tests; originals and canonical memories read-only. No gate modification or full-goal completion. Stage077 excluded.'
},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(created,ensure_ascii=True))

