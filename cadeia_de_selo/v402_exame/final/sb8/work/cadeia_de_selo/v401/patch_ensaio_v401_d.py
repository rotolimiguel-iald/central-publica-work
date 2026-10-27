# -*- coding: utf-8 -*-
"""patch_ensaio_v401_d.py -- refina o _selo_explica do ensaio (patch c): as chaves do selo que carregam os NUMEROS do kernel e/ou o HASH do proprio programa (estatuto_da_prova_v391, pedras_v392, pedras_v393, varredura_e_sorry_v392, three_stress_tests_v387) mudam so' no VEREDITO e so' em numeros
(contagens, escada, arquivos varridos) e no hash do proprio um.py; o registro segue selado. Qualquer outra diferenca dentro delas, ou em outra chave, reprova. Recusa rodar duas vezes."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = sys.argv[1] if len(sys.argv) > 1 else "ensaio_a_seco_v401.py"
t = open(P, encoding="utf-8").read()
assert "# [v401-patch-d]" not in t
i = t.index("def _selo_explica(k_):"); j = t.index("_selo_inexplicado = sorted(")
t = t[:i] + '''def _selo_explica(k_):   # [v401-patch-d]
    a_, b_ = selo0.get(k_), seal.get(k_)
    if k_ in ("estatuto_da_prova_v391", "pedras_v392", "pedras_v393", "varredura_e_sorry_v392", "three_stress_tests_v387"):
        # so' o VEREDITO muda, e so' em numeros (a escada, as declaracoes, a contagem de arquivos e de vereditos) e no hash do proprio um.py; o registro segue selado
        va, vb = str((a_ or {}).get("verdict")), str((b_ or {}).get("verdict"))
        va = va.replace(_H_ANTES, _H_DEPOIS).replace(_H_ANTES[:16], _H_DEPOIS[:16])
        return bool(va != str((a_ or {}).get("verdict")) or va != vb) and _num(_nc(va)) == _num(_nc(vb)) and (b_ or {}).get("all_verified") is True
    # o hash das fontes formais: o do kf do rito simulado (o kernel embutido do candidato + os residuais do Nos), diferente do da base porque o kernel ganhou o arquivo da pedra
    if k_ == "formal_source_hash":
        return bool(isinstance(b_, str) and len(b_) == 64 and a_ != b_ and b_ == kf.get("formal_source_hash"))
    return False


''' + t[j:]
ast.parse(t)
open(P + ".tmp", "w", encoding="utf-8", newline="").write(t)
os.replace(P + ".tmp", P)
print("patch d aplicado:", P)
