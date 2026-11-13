from b_lib import *
import re, collections
C = core()["core"]
L = C["the_ledger_of_charges_v383"]
rows = L["ledger"]
print("n linhas do livro:", len(rows)); print(list(rows[0].keys()))
cnt = collections.Counter()
for r in rows:
    oc = r.get("outcome") or r.get("status")
    cnt[oc] += 1
    print("  ", r.get("id") or r.get("charge") or "", "|", oc, "|", str(r.get("how", ""))[:40])
print(dict(cnt))
print("counts do registro:", L["counts"], "in_rule", L["counts_in_rule"], "n_in_rule", L["n_in_rule"], "n_beside", L["n_beside"])
e = C["estatuto_da_prova_v391"]["prova_2_ritos"]
print("estatuto:", e["ledger"], e["n_cobrancas"], e["falsificadas"])
print("FALSIFIED no livro:", cnt.get("FALSIFIED", 0))
