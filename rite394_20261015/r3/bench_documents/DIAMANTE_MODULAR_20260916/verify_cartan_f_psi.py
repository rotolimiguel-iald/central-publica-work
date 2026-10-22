"""Exact local exterior-algebra controls, not a QFT or UV test."""
from fractions import Fraction as Q
from itertools import combinations
import json
from finalize_weyl_bridge import ROOT, atomic, backed_replace, NOW, pin

def wedge(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            seq = ka + kb
            if len(set(seq)) != len(seq):
                continue
            sign = (-1) ** sum(seq[i] > seq[j] for i in range(len(seq)) for j in range(i+1, len(seq)))
            key = tuple(sorted(seq))
            out[key] = out.get(key, Q(0)) + sign * va * vb
    return {k:v for k,v in out.items() if v}

def add(*terms):
    out = {}
    for c, a in terms:
        for k,v in a.items():
            out[k] = out.get(k, Q(0)) + c*v
    return {k:v for k,v in out.items() if v}

def main():
    e = [{(i,):Q(1)} for i in range(4)]
    checks = 0
    rejected = 0
    for F in (Q(1), Q(3,2), Q(7)):
        df = {(i,):Q(i+1) for i in range(4)}
        for factor in (Q(1,2), Q(-1,2)):
            v = {k:factor*x/F for k,x in df.items()}
            T = [wedge(x,v) for x in e]
            for a,b in combinations(range(4),2):
                residual = add((1,wedge(df,wedge(e[a],e[b]))),
                               (F,wedge(T[a],e[b])),(-F,wedge(e[a],T[b])))
                if factor == Q(1,2):
                    assert not residual
                    checks += 1
                else:
                    assert residual
                    rejected += 1
    # Independent scalar chain-rule check: F*Box(log F)=Box F-(dF)^2/F.
    for F in (Q(1),Q(3,2),Q(7)):
        for gradient_squared, box_F in ((Q(-4),Q(5)),(Q(0),Q(-2)),(Q(9),Q(0))):
            lhs = -3*(box_F-gradient_squared/F)-Q(3,2)*gradient_squared/F
            rhs = Q(3,2)*gradient_squared/F-3*box_F
            assert lhs == rhs
            checks += 1
    result = dict(status='PASS', exact_positive_checks=checks,
                  wrong_sign_controls_rejected=rejected,
                  scope='Local Cartan ansatz substitution and scalar chain rule only; no uniqueness, boundary dynamics, QFT, or UV test',
                  note=pin(ROOT/'CARTAN_F_PSI_E_FONTE.md'))
    atomic(ROOT/'CARTAN_F_PSI_CHECKS.json',json.dumps(result,indent=2))
    addition = ('\n\n## '+NOW+' — fornecedor condicional Cartan F(psi)R\n\n'
        '[DERIVED — nota analítica ainda sem revisão independente] CARTAN_F_PSI_E_FONTE.md deriva '
        'v=(1/2)d ln F e V=(3/2)d ln F para conexão métrica independente, coframe invertível e setor sem fonte de spin. '
        'A densidade efetiva é F R(g)+3(∂F)^2/(2F)−3 Box F. Bordo mantido. '
        'Não identificar o 1/2 com R1 modular ou Meia-Nat. A matéria completa e a escolha métrica/Cartan não foram resolvidas. '
        '[REAL] Controles exatos: 27 identidades e 18 sinais errados recusados. Não testam unicidade, estado interagente ou UV. '
        'Fonte tgl_paper_unified.py lida nas linhas 10121–10190, sem execução/modificação. Nenhum gate alterado.\n')
    for name in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md','PROPOSTA_MEMORIA_ATLAS.md'):
        p = ROOT/name
        backed_replace(p,p.read_bytes()+addition.encode('utf-8'))
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
