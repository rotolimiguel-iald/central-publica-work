# -*- coding: utf-8 -*-
"""patch_montar_r3_2.py -- aplica as mudancas R3.2 ao montar_sandbox.py (copiado da R3.1). Roda uma vez; confere cada ancora (count == 1)."""
import sys
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "montar_sandbox.py"
t = P.read_text(encoding="utf-8")
BS = "\\"


def troca(x, y):
    global t
    assert t.count(x) == 1, x[:100]
    t = t.replace(x, y)


troca('"""montar_sandbox.py (R3.1, 13/10/2026) -- R3.1:',
      '"""montar_sandbox.py (R3.2, 13/10/2026) -- R3.2: o recibo do kernel sintetico no contrato KERNEL_RECIBO_R3_2 (+ varredura_tokens recursiva,\n'
      'plano 12-ter item 3; a arvore sintetica ganha TGLExt/O16/SinteticoO16.lean, fora do manifesto, so para a recontagem recursiva); o build log\n'
      'sintetico traz as linhas de job do lake de cada pedra, da raiz e do Audit e a linha final (R31-4); fx/custodia_v391/ guarda o selo v391 e o\n'
      'manifesto do kernel v391 (copias do nos/ antes do "selo" do sandbox: o --selo-anterior e o --kernel-manifesto-anterior da R31-3).\n'
      'R3.1:')
troca('KERNEL_CONTRATO = "KERNEL_RECIBO_R3_1"', 'KERNEL_CONTRATO = "KERNEL_RECIBO_R3_2"')
troca('revisao="R3.1 (13/10/2026)"', 'revisao="R3.2 (13/10/2026)"')
troca('ks_sha = {}\n',
      '# R3.2 (plano 12-ter item 3): um .lean numa SUBPASTA (TGLExt/O16), fora do manifesto e fora das pedras: so existe para que a recontagem\n'
      '# RECURSIVA dos .lean da arvore (5; 1 em TGLExt/O16) difira da nao recursiva\n'
      'ARVORE_EXTRA = {"TGLExt/O16/SinteticoO16.lean": "-- SINTETICO (sandbox R3.2): um .lean em TGLExt/O16, fora do manifesto; so para a varredura recursiva' + BS + 'n"}\n'
      'ks_sha = {}\n')
troca('rec["fx"]["kernel_src"] = dict(dir=str(KS), sha256=ks_sha)',
      'for rel, txt in ARVORE_EXTRA.items():\n'
      '    gravar_novo(KS / rel, txt.encode("utf-8"))\n'
      'N_LEAN = sum(1 for q in KS.rglob("*.lean"))\n'
      'N_LEAN_O16 = sum(1 for q in (KS / "TGLExt" / "O16").rglob("*.lean"))\n'
      'rec["fx"]["kernel_src"] = dict(dir=str(KS), sha256=ks_sha, extra_fora_do_manifesto=sorted(ARVORE_EXTRA), arquivos_lean=N_LEAN, arquivos_lean_em_TGLExt_O16=N_LEAN_O16)')
# o build log sintetico: as linhas do lake (R31-4)
i = t.index('log_b = (')
j = t.index('.encode("utf-8")', i) + len('.encode("utf-8")')
velho = t[i:j]
assert "Build completed successfully (simulado)" in velho, velho
novo = ('log_b = ("build_full.log SINTETICO (fixture R3.2 13/10/2026): nenhum kernel foi construido aqui; as linhas imitam o formato do lake 4.31' + BS + 'n"\n'
        '         "' + BS + 'u2714 [1/4] Built TGLExt.PedraSinteticaA (1s)' + BS + 'n"\n'
        '         "' + BS + 'u2714 [2/4] Built TGLExt.PedraSinteticaB (1s)' + BS + 'n"\n'
        '         "' + BS + 'u2714 [3/4] Built TGLExt (1s)' + BS + 'n"\n'
        '         "' + BS + 'u2714 [4/4] Built TGL.Audit (1s)' + BS + 'n"\n'
        '         "Build completed successfully (4 jobs).' + BS + 'n").encode("utf-8")')
t = t[:i] + novo + t[j:]
troca('            formal_files_antes=dict(ff_v391),',
      '            varredura_tokens=dict(recursiva=True, arquivos_lean=N_LEAN, arquivos_lean_em_TGLExt_O16=N_LEAN_O16,\n'
      '                                  nota="plano 12-ter item 3: a varredura de tokens proibidos e recursiva (inclui TGLExt/O16); o B(n) reconta"),\n'
      '            formal_files_antes=dict(ff_v391),')
troca('contrato KERNEL_RECIBO_R3_1: nenhum kernel', 'contrato KERNEL_RECIBO_R3_2: nenhum kernel')
troca('p = RAIZ / "SANDBOX_MANIFEST_R3_1.json"', 'p = RAIZ / "SANDBOX_MANIFEST_R3_2.json"')
troca('# b1/ (manifesto original) e b2/ (manifesto re-apontado para nos/)',
      '# R3.2 (R31-3): a "custodia" da v391 no sandbox: o selo e o manifesto do kernel v391, que o --selo-anterior e o --kernel-manifesto-anterior\n'
      '# apontam depois do "selo" do sandbox (quando nos/ ja e o v392); na producao, as copias da custodia (the_boundary_BACKUPS/um_v391_*)\n'
      'rec["fx"]["custodia_v391"] = dict(selo=gravar_novo(RAIZ / "fx" / "custodia_v391" / "um_absoluto_selo.json", selo_raw),\n'
      '                                  kernel_manifest=gravar_novo(RAIZ / "fx" / "custodia_v391" / "tgl_kernel_proof_manifest.json", kman_raw))\n'
      '# b1/ (manifesto original) e b2/ (manifesto re-apontado para nos/)')
P.write_bytes(t.encode("utf-8"))
print("montar_sandbox.py R3.2: ok")
