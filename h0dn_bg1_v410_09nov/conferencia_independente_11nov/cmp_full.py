import json, math
r = json.load(open("resultado_D.json"))
exp = {"T1": {"publicado": 6.823355474280428, "c_livre": 5.316943561403229},
       "S0": {"publicado": 6.710150598579069, "c_livre": 5.191312010024399}}
rnd = {"T1": {"publicado": 6.823355, "c_livre": 5.316944}, "S0": {"publicado": 6.710151, "c_livre": 5.191312}}
for k in ("T1", "S0"):
    for m in ("publicado", "c_livre"):
        D = r[k][m]["D"]
        print("%s %-9s D=%.12f  esp_cheio=%.12f dif=%.2e  esp_arred6=%.6f dif=%.2e  %s" % (
            k, m, D, exp[k][m], abs(D - exp[k][m]), rnd[k][m], abs(D - rnd[k][m]),
            "CONFERE" if abs(D - rnd[k][m]) < 1e-6 else "NAO CONFERE"))
# incidental: K = E(z*)^(2 beta/3) com Omega congelados (so localizar/conferir o numero)
alpha = 0.0072973525693; beta = alpha * math.sqrt(math.e); z = 1089.95
Om, Or = 0.3023480225765346, 8.934068872870022e-05
E2 = 1 + Om * ((1 + z) ** 3 - 1) + Or * ((1 + z) ** 4 - 1)
K = math.exp((2 * beta / 3) * 0.5 * math.log(E2))
print("incidental: K(lei)=%.16f  K(BG1.json)=1.0838071748529643  dif=%.2e ; log10K=%.15f" % (K, abs(K - 1.0838071748529643), math.log10(K)))
