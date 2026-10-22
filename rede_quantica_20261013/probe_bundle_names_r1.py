"""Discover generated names after import transposition, without editing proofs."""
import datetime as dt
import json
import os
import subprocess
import time
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
BUNDLE = OUT/'network_bundle_r4'
DEST = BUNDLE/'name_probe_r1'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
assert not DEST.exists()
DEST.mkdir()
source = DEST/'GeneratedNames.lean'
new(source, '''import TGLExt.F1Fecho394.CanonicalWeylAssemblyR5
import Lean
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, _) in env.constants.toList do
    if "F1Rede.LightRay".isPrefixOf n.toString then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\\t" ++ n.toString ++ "\\t" ++ String.intercalate "," (axs.toList.map Name.toString))
''')
paths = [BUNDLE/'lib']+sorted(KERNEL.glob('.lake/packages/*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']
env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)))
command = [str(LEAN), str(source)]
start = dt.datetime.now(dt.timezone.utc).isoformat()
t0 = time.perf_counter()
result = subprocess.run(command, cwd=DEST, env=env, capture_output=True)
end = dt.datetime.now(dt.timezone.utc).isoformat()
new(DEST/'STDOUT.log',result.stdout.decode('utf-8'))
new(DEST/'STDERR.log',result.stderr.decode('utf-8'))
new(DEST/'RECEIPT.json',dict(command=command, LEAN_PATH=env['LEAN_PATH'], start_utc=start,
    end_utc=end,seconds=time.perf_counter()-t0,exit_code=result.returncode,source=pin(source),
    stdout=pin(DEST/'STDOUT.log'),stderr=pin(DEST/'STDERR.log'),script=pin(__file__)))
print(result.stdout.decode('utf-8'))
assert result.returncode == 0
