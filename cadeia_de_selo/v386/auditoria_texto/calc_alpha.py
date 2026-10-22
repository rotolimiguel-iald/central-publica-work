import math
ALPHA_FINE_CODATA_2018 = 1/137.035999084
a = ALPHA_FINE_CODATA_2018
print("alpha_CODATA2018      =", repr(a))
print("alpha^2               =", repr(a*a))
print("alpha*sqrt(e)         =", repr(a*math.sqrt(math.e)))
print("sqrt(e)               =", repr(math.sqrt(math.e)))
print("alpha*sqrt(e) 6 digits=", f"{a*math.sqrt(math.e):.6f}")
print("alpha^2 6 digits      =", f"{a*a:.6f}")
print("ratio (a*sqrt e)/a^2  =", repr(a*math.sqrt(math.e)/(a*a)))
