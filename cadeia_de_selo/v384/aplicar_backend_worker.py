import ast, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
p = "pilar_quantico_worker.py"
s = open(p, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:90]); s = s.replace(old, new)
rep('''class Engine:
    def __init__(self, torch, dev):
        self.t = torch; self.dev = dev; self.C = torch.complex128
''', '''class Engine:
    def __init__(self, torch, dev, magma_up_to_n=1024):
        self.t = torch; self.dev = dev; self.C = torch.complex128; self.magma_up_to_n = int(magma_up_to_n)

    def _nonherm(self, fn, A):
        """Autovalores NAO Hermitianos com a biblioteca escolhida pelo tamanho (congelada na especificacao): MAGMA ate magma_up_to_n, cuSOLVER acima.
        O cuSOLVER padrao do PyTorch 2.11 derrubou o processo (violacao de acesso) em n = 64 no estresse de 03/10; o MAGMA nao. Depois, volta ao padrao."""
        t = self.t
        t.backends.cuda.preferred_linalg_library("magma" if A.shape[-1] <= self.magma_up_to_n else "cusolver")
        try:
            return fn(A)
        finally:
            t.backends.cuda.preferred_linalg_library("default")
''')
rep('''        ev = self.t.linalg.eigvals(S)
        return ev.cpu().numpy()''', '''        ev = self._nonherm(self.t.linalg.eigvals, S)
        return ev.cpu().numpy()''')
rep('''        lam, V = t.linalg.eig(Phi)''', '''        lam, V = self._nonherm(t.linalg.eig, Phi)''')
rep('''        E = Engine(torch, dev)
        prog.set(phase="engine_selftest", force=True)''', '''        E = Engine(torch, dev, (((spec or {}).get("linalg") or {}).get("nonhermitian_eig_backend") or {}).get("magma_up_to_n", 1024))
        R["env"]["linalg_magma_up_to_n"] = E.magma_up_to_n
        prog.set(phase="engine_selftest", force=True)''')
assert not re.search(r"(?<![A-Za-z_])t\.linalg\.eig\(", s) and "self.t.linalg.eigvals(S)" not in s and s.count("self._nonherm(") == 2
ast.parse(s)
open(p + ".tmp", "w", encoding="utf-8", newline=chr(10)).write(s); os.replace(p + ".tmp", p); print("ok")
