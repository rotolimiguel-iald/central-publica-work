# -*- coding: utf-8 -*-
"""testar_motor_v400.py -- teste rapido do motor de derivacao (protecao dos nomes nascidos no um.py e mapa 398->399, 399->400). Escrito pela ferramenta Write (as barras nao colapsam)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v400_motor as M

casos = {
    "TGL_SELO_PELA_PROPRIA_TECNOLOGIA_V399__": "TGL_SELO_PELA_PROPRIA_TECNOLOGIA_V399__",
    "OPERATOR_DECLARATION_V399_NOT_SEALED": "OPERATOR_DECLARATION_V399_NOT_SEALED",
    "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED": "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED",
    "selo_pela_propria_tecnologia_v399": "selo_pela_propria_tecnologia_v399",
    "delta_v399": "delta_v400", "ESPERADOS_v399": "ESPERADOS_v400", "V398N": "V399N", "E398": "E399", "v399": "v400", "v398": "v399",
    "registros_v399": "registros_v399", "dry_v399_": "dry_v400_", "kh_n1_cobertura_v398": "kh_n1_cobertura_v398", "_V398_NOMES_REGISTROS": "_V398_NOMES_REGISTROS",
    "import registros_v399 as RG": "import registros_v400 as RG", "registros_v399.py": "registros_v400.py", "base_v398": "base_v399", "sonico_v398": "sonico_v398",
}
ruim = []
for ent, esp in casos.items():
    got = M.bump(ent)
    print("%-52s -> %-52s %s" % (ent, got, "ok" if got == esp else "ESPERADO " + esp))
    if got != esp:
        ruim.append(ent)
print("n protegidos (identificadores do um.py):", len(M.prot_um()))
sys.exit(1 if ruim else 0)
