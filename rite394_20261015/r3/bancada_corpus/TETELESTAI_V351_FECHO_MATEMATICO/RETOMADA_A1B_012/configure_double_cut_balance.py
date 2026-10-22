from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_average_fixed_pair_fiche.py').read_text(encoding='utf8')
a=s.index("pat='");b=s.index('\nqueries=',a)
s=s[:a]+"pat='scalarTomitaResolvent_doubleCut_balance|double.{0,20}cut.{0,20}balance|quadratic.{0,20}tracial|compatibilidade.{0,20}meia'"+s[b:]
s=s.replace('search_average_fixed_pair','search_double_cut_balance')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V351ModularImplementation.lean','scalarTomitaImaginaryPower_eq_regular_implementation'),('TGLExt/V350CorePolarInclusion.lean','scalarTomitaPolar_core_commutes'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_mem'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_nonneg'),('TGLExt/V350ScalarTomitaPositiveRoot.lean','scalarTomitaPositiveRoot'),('TGLExt/V350ResolventSquareRoot.lean','resolventSquareRoot_domain'),('TGLExt/V350PositiveRootIntertwining.lean','positive_sqrt_intertwines'),('TGLExt/V351RegularDomainCut.lean','regularDomainCut_tendsto_identity'),('TGLExt/V351PerturbedWeightNorm.lean','scalarWeight_inverseCutoff_perturbed_norm'),('TGLExt/V351InverseLimitTracialExtension.lean','scalarInverseLimitWeight_tracial_iff_core')]
"""+s[b:]
s=s.replace("end=s.index(' :=',m.start());providers.append", "end=statement_end(s,m.start());providers.append")
marker='providers=[]'
s=s.replace(marker,"""def statement_end(s,start):
    depth=0
    for j in range(start,len(s)):
        if depth==0 and (s.startswith(' :=',j) or s.startswith(' where',j)):
            return j
        if s[j] in '([{': depth+=1
        elif s[j] in ')]}': depth-=1
    raise ValueError('Statement delimiter not located')
providers=[]""")
a=s.index('cp=K/');b=s.index('\nd=dict(',a)
s=s[:a]+"""cp=K/'TGLExt/V351InverseLimitTracialExtension.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('theorem scalarInverseLimitWeight_tracial_iff_core'))
target='ADAPTAR/OPEN: proposed next exact bounded balance for epsilon,eta>0 in SAME H_nu: (1-T) C_epsilon q_eta = T p_epsilon D_eta, where T=scalarTomitaResolvent P, C_epsilon=pi(B_epsilon), D_eta=antiunitaryConjugate J (pi(B_eta)), p_epsilon=1-epsilon C_epsilon, q_eta=1-eta D_eta, B_epsilon=regularInverseGeneratorCutoff P epsilon. Names C,D,p,q here are notation, not new global definitions. This identity is NOT paid by equal group names or commutation. Delta32 equality of original groups has author rc0 and independent review pending at fiche time. CorePolarInclusion already pays C/D cross commutation on the SAME GNS: do not reprove right action or commutant inclusion. The real missing step is recovering the bounded balance from the actual spectral/group realization, or an equally concrete quadratic equality directly on finiteDualStarCore. Next consumption: original root graph x=sqrt(T)u, B_nu*x=sqrt(1-T)u plus positive_sqrt_intertwines, two cut limits -> Q(B_nu Lambda(a))=Q(J Lambda(a)), including infinity; existing tracial_iff_core then extends. This is a proof strategy, not a compiled consequence. No h=Delta_nu, new GNS, arbitrary product of unbounded operators, new field assuming balance, or full joint CFC unless a located concrete consumer truly requires it. Existing regularSineResolvent_tendsto is a particular regular spectral construction, NOT a generic inverse theorem recovering T_nu from U_t. Do not count conditional form rearrangements as payment of balance.'
"""+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_AVERAGE_FIXED_PAIR','OPEN__FICHE_BEFORE_DOUBLE_CUT_BALANCE').replace('REAPROVEITAMENTO_A1B_MEDIA_PAR_FIXO','REAPROVEITAMENTO_A1B_BALANCO_DOS_CORTES')
s=s.replace('ficha anterior ao par fixo de Tomita','ficha anterior ao balanço limitado dos cortes')
s=s.replace('Consulta2 V2 lida; delta29 fornece a ação direita da média, usada no quadrado auto-adjunto.','Consulta curta do revisor após31 e antes32 lida: balanço limitado proposto, não provado. Principal relê CorePolarInclusion para evitar nova prova de comutação já disponível. Novo extrator respeita parênteses antes de procurar :=, evitando truncamento em argumentos nomeados; fichas históricas preservadas.')
p=R/'prepare_double_cut_balance_fiche.py';assert not p.exists()
b=s.encode('utf8');t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
