import faulthandler, sys, importlib.util, time
faulthandler.enable(all_threads=True)
spec = importlib.util.spec_from_file_location("w", "pilar_quantico_worker.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
import torch, numpy as np
torch.use_deterministic_algorithms(True); torch.set_num_threads(4)
E = w.Engine(torch, torch.device("cuda"))
print("engine ok", flush=True)
r = w.engine_selftest(E, 1e-9); print("selftest", r["all_ok"], flush=True)
print(w.run_timing(E, "teste_tempo_v2", reps={8: 2}), flush=True)
