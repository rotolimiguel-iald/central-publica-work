import os
AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LONG = "\\\\?\\"
src = os.path.join(AUD, "lean_sandbox", "toolchain", "leanprover--lean4---v4.31.0")
dst = os.path.join(AUD, "t", "l")
os.makedirs(os.path.join(AUD, "t"), exist_ok=True)
os.rename(LONG + src, LONG + dst)
print("movido:", os.path.isfile(os.path.join(dst, "bin", "lean.exe")))
f = os.path.join(dst, "lib", "lean", "Init", "Data", "Iterators", "Lemmas", "Combinators", "Monadic", "FilterMap.olean")
print(len(f), os.path.isfile(f))
