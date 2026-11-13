from b_lib import *
import re
C = core()["core"]
t = C["three_stress_tests_v387"]
print(json.dumps(t["ledger"], ensure_ascii=False)[:3500])
print("n_verdicts", t["n_verdicts"], t["n_not_falsified"], t["n_inconclusive"], t["n_awaiting"])
print(t["falsified_substring_reading"][:300] if isinstance(t["falsified_substring_reading"], str) else t["falsified_substring_reading"])
