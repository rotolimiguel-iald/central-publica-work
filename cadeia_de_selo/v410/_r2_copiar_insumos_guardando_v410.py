# -*- coding: utf-8 -*-
"""_r2_copiar_insumos_guardando_v410.py -- roda copiar_insumos_v410.py; quando ele recusa («o insumo ja existe e DIFERE da origem: nao sobrescrevo»), guarda o insumo velho AO LADO (rename de bytes, nada apagado: <nome>.bak_<TS>_antes_da_r5) e roda de novo, ate' passar ou ate' 12 voltas.
So' guarda arquivo que esteja DENTRO de insumos/ desta pasta. (R2/R5, 10/11: o kernel a frio da R5 mudou a pedra embutida, o FLAGS e o KH_N1.)"""
import os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); INS = os.path.join(HERE, "insumos"); TS = time.strftime("%Y%m%d_%H%M%S")
PY = sys.executable
for volta in range(12):
    r = subprocess.run([PY, "-I", "-B", "-X", "utf8", os.path.join(HERE, "copiar_insumos_v410.py")], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode == 0:
        print("copiar_insumos: RC 0 na volta", volta); print(out.strip()[-900:]); break
    m = re.search(r"DIFERE da origem: nao sobrescrevo', '([^']+)'", out)
    if not m:
        print("copiar_insumos: RC", r.returncode, "SEM a recusa esperada:"); print(out.strip()[-1500:]); sys.exit(1)
    p = os.path.abspath(m.group(1).replace("\\\\", "\\"))
    assert os.path.dirname(p) == os.path.abspath(INS) or os.path.abspath(INS) + os.sep in p, ("o arquivo recusado nao esta' em insumos/", p)
    assert os.path.isfile(p), p
    dst = p + ".bak_" + TS + "_antes_da_r5"; assert not os.path.exists(dst), dst
    os.rename(p, dst); print("guardado ao lado:", os.path.relpath(p, HERE), "->", os.path.basename(dst))
else:
    print("copiar_insumos: nao passou em 12 voltas"); sys.exit(1)
