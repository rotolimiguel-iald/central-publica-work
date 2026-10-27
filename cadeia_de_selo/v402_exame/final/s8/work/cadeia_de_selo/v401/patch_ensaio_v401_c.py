# -*- coding: utf-8 -*-
"""patch_ensaio_v401_c.py -- o selo da v401 difere do da v400 SELADA em chaves que carregam os NUMEROS do kernel (a pedra acrescenta 12 bandeiras, 14 declaracoes, 1 arquivo) e o HASH das fontes formais: o ensaio EXPLICA chave por chave --
(i) estatuto_da_prova_v391: so' o hash do proprio um.py; (ii) as chaves cujo valor so' muda em numeros (veredito com contagens): pedras_v392, pedras_v393, varredura_e_sorry_v392, three_stress_tests_v387; (iii) formal_source_hash: o hash da arvore formal, que muda porque o kernel ganhou o arquivo da pedra
(igual ao hash formal do kf do rito simulado). Qualquer outra chave que mude reprova. Recusa rodar duas vezes."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = sys.argv[1] if len(sys.argv) > 1 else "ensaio_a_seco_v401.py"
t = open(P, encoding="utf-8").read()
assert "# [v401-patch-c]" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n)
    t = t.replace(old, new)


sub('''        return J_(a_).replace(_H_ANTES, _H_DEPOIS).replace(_H_ANTES[:16], _H_DEPOIS[:16]) == J_(b_)
    return False
''', '''        return J_(a_).replace(_H_ANTES, _H_DEPOIS).replace(_H_ANTES[:16], _H_DEPOIS[:16]) == J_(b_)
    # [v401-patch-c] as chaves que carregam os NUMEROS do kernel (a pedra acrescenta bandeiras, declaracoes e um arquivo): o valor muda so' em numeros, e o registro segue selado
    if k_ in ("pedras_v392", "pedras_v393", "varredura_e_sorry_v392", "three_stress_tests_v387"):
        return bool(a_ != b_ and _num(_nc(J_(a_))) == _num(_nc(J_(b_))) and ((core_s.get(k_) or {}).get("all_verified") is True))
    # o hash das fontes formais: o do kf do rito simulado (o kernel embutido do candidato + os residuais do Nos), diferente do da base porque o kernel ganhou o arquivo da pedra
    if k_ == "formal_source_hash":
        return bool(isinstance(b_, str) and len(b_) == 64 and a_ != b_ and b_ == kf.get("formal_source_hash"))
    return False
''')
ast.parse(t)
open(P + ".tmp", "w", encoding="utf-8", newline="").write(t)
os.replace(P + ".tmp", P)
print("patch c aplicado:", P)
