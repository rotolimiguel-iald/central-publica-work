# -*- coding: utf-8 -*-
# T06_PANTHEON_FORMATO -- so os 5 testes 'Rounding' de fix_pantheon_rounding_r1.py (extraidos por AST, sem o passo de reescrita)
# contra a COPIA de bancada/pantheon_cov.py. Matrizes sinteticas. Porte parametrizado de H_BANCADA\scripts\pantheon_rounding_tests.py.
# uso: t06_pantheon_rounding.py <candidate> <fix_pantheon_rounding_r1.py> <saida.json>
import ast, datetime, hashlib, io, json, sys, unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
cand, FIX, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
sys.dont_write_bytecode = True
sys.path.insert(0, str(cand))
from bancada import pantheon_cov as pc
assert Path(pc.__file__).resolve().is_relative_to(cand)
src = FIX.read_bytes().decode("utf-8")
tree = ast.parse(src)
cls = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Rounding"][0]
code = ast.get_source_segment(src, cls)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


ns = {"unittest": unittest, "np": np, "pc": pc, "patch": patch, "sha": sha}
exec(compile(code, "Rounding_from_fix_pantheon_rounding_r1", "exec"), ns)
stream = io.StringIO()
r = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ns["Rounding"]))
res = dict(teste="T06_PANTHEON_FORMATO", quando=datetime.datetime.now().isoformat(timespec="seconds"), fix_script_sha256=sha(FIX.read_bytes()),
           pantheon_cov_copy_sha256=sha((cand / "bancada" / "pantheon_cov.py").read_bytes()), tests=r.testsRun, success=r.wasSuccessful(),
           failures=len(r.failures), errors=len(r.errors), log=stream.getvalue(), veredito=("PASSA" if r.wasSuccessful() and r.testsRun == 5 else "FALHA"))
with out.open("x", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(stream.getvalue())
print(json.dumps({k: res[k] for k in ("veredito", "tests", "success", "failures", "errors")}))
sys.exit(0 if res["veredito"] == "PASSA" else 1)
