# -*- coding: utf-8 -*-
# Prototipo: tempo e precisao do hamiltoniano modular de um intervalo da cadeia escalonada (staggered) de Dirac, com mpmath.
import mpmath as mp, time, sys
def G_even(j, m):
    # G(2j) = (2/pi) (-1)^j Q_{j-1/2}(1+2m^2)   [Heine]
    q = mp.legenq(j - mp.mpf(1)/2, 0, 1 + 2*m*m, type=3); assert abs(mp.im(q)) <= mp.mpf(10)**(-mp.mp.dps+5)*(1+abs(q)); return (2/mp.pi) * (-1)**j * mp.re(q)
def G_quad(r, m):
    return mp.quad(lambda k: mp.cos(k*r)/mp.sqrt(mp.cos(k)**2 + m*m), [-mp.pi, -mp.pi/2, 0, mp.pi/2, mp.pi]) / (2*mp.pi)
def correl(N, m):
    Gs = {}
    def G(r):
        r = abs(r)
        if r % 2: return mp.mpf(0)
        if r not in Gs: Gs[r] = G_even(r//2, m) if m != 0 else None
        return Gs[r]
    C = mp.matrix(N, N)
    for i in range(N):
        for j in range(N):
            r = i - j
            if r == 0: s1 = mp.mpf(0)
            elif r % 2:
                if m == 0: s1 = -(2/mp.pi) * mp.sin(r*mp.pi/2) / r
                else: s1 = -(G(r+1) + G(r-1)) / 2
            else: s1 = mp.mpf(0)
            mass = (m * (-1)**i * G(r)) if (m != 0 and r % 2 == 0) else mp.mpf(0)
            C[i, j] = (mp.mpf(1)/2 if r == 0 else 0) - (s1 + mass)/2
    return C
if __name__ == '__main__':
    mp.mp.dps = 40
    m = mp.mpf('0.05')
    for r in (0, 2, 4, 10):
        print('G check r=%d' % r, mp.nstr(G_even(r//2, m), 20), mp.nstr(G_quad(r, m), 20))
    # massless limit of S1 from G at tiny m
    mt = mp.mpf('1e-12'); print('S1(1) m->0:', mp.nstr(-(G_even(1, mt) + G_even(0, mt))/2, 15), 'exato', mp.nstr(-(2/mp.pi), 15))
    for N, dps in ((32, 50), (64, 70)):
        mp.mp.dps = dps; t = time.time()
        C = correl(N, mp.mpf('0.02')); t1 = time.time()
        E, Q = mp.eigsy(C); t2 = time.time()
        nu = [E[k] for k in range(N)]
        print('N=%d dps=%d  correl %.1fs  eigsy %.1fs  nu_min %s  nu_max-1 %s' % (N, dps, t1-t, t2-t1, mp.nstr(min(nu), 5), mp.nstr(max(nu)-1, 5)))
