# -*- coding: utf-8 -*-
"""gw.py -- o banco RESIDENTE de ondas gravitacionais da Bancada Um (Fase 6, 01/10/2026; ordem do operador: «todo esse banco de dados novo (gweco) […] já o
vincule à bancada para vc poder trabalhar com eles em tempo real dentro do sistema carregado com os dados reais»).

O que fica na RAM, com sha256: as janelas de 32 s @ 4096 Hz de cada série (evento × detector) da amostra pré-registrada da Fase 6 — o cache de maio/2026 (O1–O3,
só leitura, casa da IALD nativa) e o O4 baixado do GWOSC (fontes_externas/gwosc_o4) —, pré-condicionadas e branqueadas EXATAMENTE como no pipeline
echo_anchored_v3.py (mesmas constantes: passa-alta 15 Hz, Tukey 0,1, Welch 4 s Hann, banda 20–1024 Hz, PSD em t_rel ∈ (−14,4; −2,0) s); os remanescentes por evento
(M_f, a_f HBR2016, atrasos MAY/KMS, modo 220) exportados do WSL; e os estágios da rodada (cego, aberto, PODER, RESULTADO), com o empilhamento e a regra de
veredito da MESMA função que o executor usa (bancada/gw_stack.py), para consulta em tempo real com filtros — consulta é consulta: o veredito selado é o do
RESULTADO por hash. O que NÃO vive aqui: os moldes (lalsimulation) e o ajuste — isso roda no WSL (/opt/lal_env) e entra por arquivo. CONFIRMED proibido."""
import csv
import io
import hashlib
import json
import math
import os
import subprocess
import sys
import threading
import time
import uuid

import numpy as np
from scipy.signal import butter, sosfiltfilt, windows

from bancada import gw_stack
from bancada.canonical import read_alpha, require_current

FS = 4096.0; SEG_S = 2.5; T_PEAK = 2.0; F_LO, F_HI = 20.0, 1024.0
HP_HZ, TUKEY_ALPHA, PSD_T = 15.0, 0.1, (-14.4, -2.0)
ALPHA, ALPHA_PROVENANCE = read_alpha(); BETA = ALPHA * math.sqrt(math.e)
SRC_MAIO = r"C:\IALD\projetos_pyhton\IALD\strain_cache"
ARQUIVOS = ("PREREGISTRO_FASE6_ECO_RADICAL_20261001.json", "PODER_FASE6_ANTES_DE_ABRIR.json", "ECHO_V3_CEGO.json", "ECHO_V3_ABRIR.json",
            "RESULTADO_FASE6_ECO_RADICAL_20261001.json", "AMOSTRA_FASE6.json", "remanescentes_v3.json",
            "EMENDA_V4_FASE6_20261001.json", "PODER_V4_ANTES_DE_ABRIR.json", "ECHO_V4_CEGO.json", "ECHO_V4_ABRIR.json", "RESULTADO_V4_FASE6_20261001.json", "DIAG_CONTROLES_POSTHOC.json",
            "EMENDA_V5_FASE6_20261001.json", "PODER_V5_ANTES_DE_ABRIR.json", "ECHO_V5_CEGO.json", "ECHO_V5_ABRIR.json", "RESULTADO_V5_FASE6_20261001.json")



def sha256_bytes(b): return hashlib.sha256(b).hexdigest()


def read_strain_bytes(data):
    """Validate a 32s/4096Hz real finite series from exactly the hashed bytes."""
    with np.load(io.BytesIO(data), allow_pickle=False) as packet:
        if not {'t', 'strain', 'fs'} <= set(packet.files):
            raise ValueError('GW_FIELDS_MISSING')
        t, strain, frequency = packet['t'], packet['strain'], packet['fs']
    if frequency.shape != () or frequency.dtype.kind not in 'fiu':
        raise ValueError('GW_FS_SCALAR_REQUIRED')
    fs = float(frequency)
    if not math.isfinite(fs) or fs != FS:
        raise ValueError('GW_FS_CONTRACT_4096')
    if t.ndim != 1 or strain.ndim != 1 or t.shape != strain.shape or len(t) != 131072:
        raise ValueError('GW_SHAPE_CONTRACT_32_SECONDS')
    if t.dtype.kind not in 'fiu' or strain.dtype.kind not in 'fiu':
        raise ValueError('GW_REAL_ARRAYS_REQUIRED')
    t, strain = t.astype(float), strain.astype(float)
    if not np.isfinite(t).all() or not np.isfinite(strain).all():
        raise ValueError('GW_NONFINITE')
    # GPS timestamps around 1e9 s have representational precision ~2.4e-7 s.
    if not np.allclose(t, t[0] + np.arange(len(t)) / fs, rtol=0, atol=5e-7):
        raise ValueError('GW_TIME_GRID_INVALID')
    return t, strain, fs


# ---- o pré-condicionamento e o branqueamento: cópia fiel do pipeline (echo_anchored_v3.py), sem lal ----
def precondition(x, fs):
    x = x - np.mean(x); sos = butter(8, HP_HZ, btype="highpass", fs=fs, output="sos"); y = sosfiltfilt(sos, x)
    return y * windows.tukey(len(y), alpha=TUKEY_ALPHA)


def mad(x): return float(1.4826 * np.median(np.abs(x - np.median(x))))


def welch(x, fs, seg=4 * 4096):
    w = np.hanning(seg); step = seg // 2; n = (len(x) - seg) // step + 1; P = np.zeros(seg // 2 + 1)
    for i in range(n):
        xs = x[i * step:i * step + seg]; P += np.abs(np.fft.rfft((xs - xs.mean()) * w)) ** 2
    P *= 2.0 / (n * fs * np.sum(w ** 2)); return np.fft.rfftfreq(seg, 1 / fs), P


def band_mask(fr, lo, hi, ramp_lo=4.0, ramp_hi=50.0):
    m = np.ones_like(fr); m[fr < lo - ramp_lo] = 0; m[fr > hi + ramp_hi] = 0
    a = (fr >= lo - ramp_lo) & (fr < lo + ramp_lo); m[a] = 0.5 * (1 - np.cos(np.pi * (fr[a] - (lo - ramp_lo)) / (2 * ramp_lo)))
    b = (fr > hi - ramp_hi) & (fr <= hi + ramp_hi); m[b] = 0.5 * (1 + np.cos(np.pi * (fr[b] - (hi - ramp_hi)) / (2 * ramp_hi)))
    return m


def whiten32(x, fs, f, P):
    N = len(x); fr = np.fft.rfftfreq(N, 1 / fs); ft = np.fft.rfft(x)
    Pi = np.maximum(np.interp(fr, f, P, left=P[1], right=P[-1]), 1e-50)
    return np.fft.irfft(ft / np.sqrt(Pi * fs / 2) * band_mask(fr, F_LO, F_HI), n=N)


class GWResidente:
    def __init__(self, raiz):
        self.raiz = raiz
        self.inv = os.path.join(raiz, "investigacao", "fase6_eco_radical_01out")
        self.src = {"maio": SRC_MAIO, "o4": os.path.join(raiz, "fontes_externas", "gwosc_o4", "strain_32s")}
        self.estado = dict(estado="na_fila", carregados=0, total=0, bytes=0, segundos=None, erro=None, nan=[], ausentes=[])
        self.series = {}
        self.eventos = {}
        self.remanescentes = {}
        self.lock = threading.Lock()
        self._arq = {}
        self.tarefas = {}

    # ---------- carga ----------
    def carregar(self):
        """Reexecutável: recarrega TUDO do disco (séries novas do download entram sem reiniciar o servidor); a troca das tabelas é atômica por série (lock)."""
        t0 = time.time()
        with self.lock:
            if self.estado.get("estado") == "carregando": return
            self.estado.update(estado="carregando", carregados=0, total=0, bytes=0, segundos=None, erro=None, nan=[], ausentes=[])
        try:
            cat = os.path.join(self.inv, "catalogo_v3.csv")
            if not os.path.exists(cat):
                self.estado.update(estado="sem_catalogo", erro="catalogo_v3.csv ausente (preparar_amostra.py)"); return
            cat_bytes = open(cat, "rb").read()
            rows = list(csv.DictReader(io.StringIO(cat_bytes.decode("utf-8-sig"))))
            self.catalogo_sha256 = sha256_bytes(cat_bytes)
            self._ler_remanescentes()
            evs = {}
            for r in rows:
                f = lambda k: (float(r[k]) if r.get(k) not in (None, "") else None)
                evs[r["commonName"]] = dict(nome=r["commonName"], catalogo=r["catalog.shortName"], versao=r["version"], gps=f("GPS"), m1=f("mass_1_source"), m2=f("mass_2_source"), chi_eff=f("chi_eff"),
                                           Mf_fonte=f("final_mass_source"), z=f("redshift"), snr=f("network_matched_filter_snr"), p_astro=f("p_astro"), far=f("far"), era=r["era"], src=r["src"], dets=[], nan=[])
            self.estado.update(total=2 * len(evs))
            for name, ev in evs.items():
                for det in ("H1", "L1"):
                    p = os.path.join(self.src[ev["src"]], "%s_%s_4096_32s.npz" % (name, det)); key = "%s_%s" % (name, det)
                    if not os.path.exists(p):
                        self.estado["ausentes"].append(key); continue
                    b = open(p, "rb").read()
                    try:
                        t, s, fs = read_strain_bytes(b)
                    except ValueError as exc:
                        self.series[key] = dict(key=key, status="INVALID_FORMAT", erro=str(exc), sha256=sha256_bytes(b))
                        self.estado["nan"].append(key)
                        continue
                    rec = dict(key=key, evento=name, det=det, caminho=p, bytes=len(b), sha256=sha256_bytes(b), src=ev["src"], era=ev["era"], gps=ev["gps"], t0=float(t[0]), fs=fs, n=int(len(s)))
                    if np.isnan(s).any() or abs(fs - FS) > 1e-6:
                        rec.update(status="NAN_OR_FS", nan=int(np.isnan(s).sum())); ev["nan"].append(det); self.estado["nan"].append(key)
                    else:
                        trel = t - ev["gps"]; sp = precondition(s, fs); f_psd, P_psd = welch(sp[(trel > PSD_T[0]) & (trel < PSD_T[1])], fs); w = whiten32(sp, fs, f_psd, P_psd)
                        sel = (trel > PSD_T[0]) & (trel < PSD_T[1]); sd = float(np.std(w[sel])); i0 = int(round((0.0 - T_PEAK - trel[0]) * fs)); d_on = w[i0:i0 + int(SEG_S * fs)]
                        rec.update(status="OK", raw=s, white=w, psd_f=f_psd, psd_P=P_psd, sd_off=sd, mad_on=mad(d_on), peak_over_sd=float(np.max(np.abs(d_on[:int(1.8 * fs)])) / sd)); ev["dets"].append(det)
                    with self.lock:
                        self.series[key] = rec; self.estado["carregados"] += 1; self.estado["bytes"] += len(b)
            self.eventos = evs
            self.estado.update(estado="residente", segundos=round(time.time() - t0, 1))
        except Exception as e:
            self.estado.update(estado="erro", erro=repr(e))

    def _ler_remanescentes(self):
        p = os.path.join(self.inv, "remanescentes_v3.json")
        if os.path.exists(p):
            self.remanescentes = json.load(open(p, encoding="utf-8")).get("eventos", {})

    def _arquivo(self, nome):
        """JSON da pasta da Fase 6, lido por mtime (recarrega quando o arquivo muda); devolve (obj, sha16, mtime) ou (None, None, None)."""
        p = os.path.join(self.inv, nome)
        if not os.path.exists(p): self._arq.pop(nome, None); return None, None, None
        mt = os.path.getmtime(p); c = self._arq.get(nome)
        if c and c[2] == mt: return c
        b = open(p, "rb").read(); obj = json.loads(b.decode("utf-8")); c = (obj, sha256_bytes(b)[:16], mt); self._arq[nome] = c; return c

    # ---------- consultas ----------
    def resumo(self):
        por = {}
        for ev in self.eventos.values():
            k = "%s/%s" % (ev["era"], ev["src"]); por[k] = por.get(k, 0) + 1
        arqs = {}
        for n in ARQUIVOS:
            obj, sh, mt = self._arquivo(n)
            arqs[n] = dict(presente=obj is not None, sha16=sh, modificado=(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mt)) if mt else None))
        n_ok = sum(1 for s in self.series.values() if s.get("status") == "OK")
        return dict(estado=self.estado, n_eventos=len(self.eventos), por_era_src=por, n_series_ok=n_ok, n_series_nan=len(self.estado["nan"]), n_remanescentes=len(self.remanescentes),
                    gib_residente=round(2 * 8 * 131072 * n_ok / 2 ** 30, 3), catalogo_sha256=getattr(self, "catalogo_sha256", None), arquivos=arqs,
                    pipeline="WSL /opt/lal_env: investigacao/fase6_eco_radical_01out/echo_anchored_v3.py (lalsuite 7.7.1; moldes e ajuste); a Bancada guarda as séries, os remanescentes e os estágios",
                    constantes=dict(fs=FS, seg_s=SEG_S, t_peak=T_PEAK, banda=[F_LO, F_HI], hp_hz=HP_HZ, tukey=TUKEY_ALPHA, psd_t=PSD_T, beta=BETA))

    def _res(self, versao="v3"):
        """Os estágios da versão pedida: v3 (a rodada pré-registrada) ou v4 (a emenda, grade ±2σ, não cega)."""
        V = versao.upper()
        cego, cs, _ = self._arquivo("ECHO_%s_CEGO.json" % V); ab, as_, _ = self._arquivo("ECHO_%s_ABRIR.json" % V)
        pre, ps, _ = self._arquivo({"V3": "PREREGISTRO_FASE6_ECO_RADICAL_20261001.json", "V4": "EMENDA_V4_FASE6_20261001.json", "V5": "EMENDA_V5_FASE6_20261001.json"}[V])
        return cego, cs, ab, as_, pre, ps

    def lista_eventos(self, filtros=None):
        f = filtros or {}; cego, cs, ab, as_, pre, ps = self._res()
        C = {r["key"]: r for r in (cego["per_series"] if cego else []) if r.get("status") == "OK"}; A = {r["key"]: r for r in (ab["per_series"] if ab else []) if r.get("status") == "OK"}
        out = []
        for name, ev in sorted(self.eventos.items()):
            if f.get("era") and ev["era"] not in (f["era"] if isinstance(f["era"], list) else [f["era"]]): continue
            if f.get("src") and ev["src"] != f["src"]: continue
            if f.get("snr_min") is not None and (ev["snr"] or 0) < float(f["snr_min"]): continue
            if f.get("snr_max") is not None and (ev["snr"] or 0) > float(f["snr_max"]): continue
            rm = self.remanescentes.get(name) or {}
            if f.get("Mf_min") is not None and (rm.get("Mf_det") or 0) < float(f["Mf_min"]): continue
            if f.get("Mf_max") is not None and (rm.get("Mf_det") or 1e9) > float(f["Mf_max"]): continue
            row = dict(ev); row.update(Mf_det=rm.get("Mf_det"), a_f=rm.get("a_f_HBR2016"), tau_ms=rm.get("tau_ms"), lag=rm.get("lag"), f_qnm_hz=rm.get("f_qnm_220_hz"), tau_d_ms=rm.get("tau_d_220_ms"))
            for det in ev["dets"]:
                s = self.series["%s_%s" % (name, det)]; row["qualidade_" + det] = dict(sd_off=round(s["sd_off"], 3), mad_on=round(s["mad_on"], 3), pico_sd=round(s["peak_over_sd"], 2))
            eco = {}
            for key in ("%s_H1" % name, "%s_L1" % name):
                c = C.get(key); a = A.get(key)
                if not c: continue
                for law in gw_stack.LAWS:
                    L = c["laws"].get(law)
                    if not L: continue
                    e = eco.setdefault(law, {}); det = key[-2:]
                    e[det] = dict(bias=round(L["bias"], 3), sigma=round(L["sigma"], 3), recR1=round(L["recovery_R1"], 3), recR2=round(L["recovery_R2"], 3), usada=L["used"],
                                  a=(round(a["laws"][law]["a_on"] - L["bias"], 3) if a else None), snr_ancoragem=(round(a["laws"][law]["snr_anchor"], 1) if a else None))
            row["eco"] = eco; out.append(row)
        return dict(n=len(out), estagios=dict(cego=cs, aberto=as_, preregistro=ps), eventos=out)

    def serie(self, key, branqueada=True, t0=-0.5, dur=1.0, n_max=4000):
        s = self.series.get(key)
        if not s: raise ValueError("série desconhecida: " + key)
        if s.get("status") != "OK": return dict(key=key, status=s["status"], nan=s.get("nan"))
        x = s["white"] if branqueada else s["raw"]; fs = s["fs"]; i0 = int(round((t0 + s["gps"] - s["t0"]) * fs)); i1 = int(round((t0 + dur + s["gps"] - s["t0"]) * fs))
        i0 = max(0, i0); i1 = min(len(x), i1); seg = x[i0:i1]; k = max(1, int(math.ceil(len(seg) / n_max)))
        if k > 1:   # envelope min/max por bloco, para o gráfico não mentir ao decimar
            m = (len(seg) // k) * k; blk = seg[:m].reshape(-1, k); y = np.empty(2 * blk.shape[0]); y[0::2] = blk.min(1); y[1::2] = blk.max(1)
            tt = s["t0"] - s["gps"] + (i0 + np.repeat(np.arange(blk.shape[0]) * k + k / 2, 2)) / fs
        else:
            y = seg; tt = s["t0"] - s["gps"] + np.arange(i0, i1) / fs
        return dict(key=key, branqueada=bool(branqueada), fs=fs, t0=t0, dur=dur, decimacao=k, n=int(len(y)), t_rel=[round(float(v), 6) for v in tt], y=[float(v) for v in y],
                    sd_off=s["sd_off"], mad_on=s["mad_on"], pico_sd=s["peak_over_sd"], sha256=s["sha256"])

    def espectro(self, key, f_max=1024.0, n_max=1200):
        s = self.series.get(key)
        if not s or s.get("status") != "OK": raise ValueError("série sem PSD: " + key)
        f, P = s["psd_f"], s["psd_P"]; sel = f <= f_max; f = f[sel]; P = P[sel]; k = max(1, int(math.ceil(len(f) / n_max)))
        return dict(key=key, f_hz=[float(v) for v in f[::k]], asd=[float(math.sqrt(max(v, 0.0))) for v in P[::k]], decimacao=k, nota="ASD = √PSD (Welch, Hann 4 s, 50%) do strain pré-condicionado, em t_rel ∈ (−14,4; −2,0) s")

    def resultados(self):
        out = {}
        for n in ARQUIVOS:
            obj, sh, mt = self._arquivo(n)
            if obj is None: out[n] = None; continue
            if n.startswith("ECHO_V"):
                st = {}
                for r in obj["per_series"]: st[r.get("status")] = st.get(r.get("status"), 0) + 1
                out[n] = dict(sha16=sh, estagio=obj.get("stage"), executado=obj.get("executed"), segundos=round(obj.get("runtime_s", 0)), n_series=len(obj["per_series"]), por_status=st, ausentes=obj.get("missing_series"), instrumento=obj.get("instrument"))
            elif n.startswith("RESULTADO"):
                res = {sub: {law: {k: v for k, v in st.items() if k not in ("eventos", "por_evento")} for law, st in sl.items()} for sub, sl in obj["resultados"].items()}
                out[n] = dict(sha16=sh, executado=obj.get("executado"), preregistro_sha256=obj.get("preregistro_sha256"), veredito_principal=obj.get("veredito_principal"), vereditos=obj.get("vereditos"), resultados=res, leituras=obj.get("leituras"))
            elif n.startswith("PODER"):
                out[n] = dict(sha16=sh, gravado=obj.get("gravado"), poder={sub: {law: {k: v for k, v in st.items() if k not in ("eventos", "por_evento")} for law, st in sl.items()} for sub, sl in obj["poder"].items()})
            elif n.startswith("PREREGISTRO") or n.startswith("EMENDA"):
                out[n] = dict(sha16=sh, criado=obj.get("criado"), n_eventos=obj["amostra"]["n_eventos"], por_era=obj["amostra"]["por_era"], n_series=obj["amostra"]["n_series"], leituras=obj["leituras"], criterios=obj["criterios"], pipeline_sha256=obj["pipeline"]["sha256"], visto_antes=obj.get("visto_antes"))
            else:
                out[n] = dict(sha16=sh, n=obj.get("n"), criado=obj.get("criado") or obj.get("created"))
        return out

    def empilhar(self, sub="todos", filtros=None, sigma_regra="max", versao="v3"):
        """Consulta em tempo real: o MESMO empilhamento do executor, com filtros; versao v3 (pré-registrada) ou v4 (emenda). NÃO é o veredito selado (esse é o do RESULTADO por hash)."""
        if versao not in ("v3", "v4", "v5"): raise ValueError("versao deve ser v3, v4 ou v5")
        cego, cs, ab, as_, pre, ps = self._res(versao)
        if cego is None: return dict(erro="estágio cego ausente: nada a empilhar (rodar a Fase 6)")
        if not pre or not pre.get("criterios") or not pre.get("leituras"):
            raise ValueError("GW_PREREGISTERED_CONTRACT_MISSING")
        CR = pre["criterios"]; READ = pre["leituras"]; f = filtros or {}
        rm = self.remanescentes; inc = set(f.get("incluir") or []); exc = set(f.get("excluir") or [])
        def filtro(c):
            ev = self.eventos.get(c["event"]) or {}
            if inc and c["event"] not in inc: return False
            if c["event"] in exc: return False
            if f.get("era") and c.get("era") not in (f["era"] if isinstance(f["era"], list) else [f["era"]]): return False
            if f.get("snr_min") is not None and (c.get("snr_net") or 0) < float(f["snr_min"]): return False
            if f.get("snr_max") is not None and (c.get("snr_net") or 0) > float(f["snr_max"]): return False
            if f.get("Mf_min") is not None and (c.get("Mf_det") or 0) < float(f["Mf_min"]): return False
            if f.get("Mf_max") is not None and (c.get("Mf_det") or 1e9) > float(f["Mf_max"]): return False
            if f.get("det") and c.get("det") != f["det"]: return False
            return True
        res = gw_stack.empilhar(cego, ab, sub, CR, READ, filtro=filtro, sigma_regra=sigma_regra)
        for law, st in res.items():
            if st.get("n_eventos"): st["vereditos_de_consulta"] = {rn: dict(zip(("veredito", "razoes"), gw_stack.veredito(st, rn, CR))) for rn in READ}
            st.pop("por_evento", None) if not f.get("por_evento") else None
        return dict(consulta=True, versao=versao, aviso="consulta em tempo real com filtros: NÃO é o veredito selado (RESULTADO por hash); CONFIRMED proibido", sub=sub, filtros=f, sigma_regra=sigma_regra,
                    estagios=dict(cego=cs, aberto=as_, preregistro=ps, preregistrado=pre is not None), criterios=CR, resultados=res)

    # ---------- a rodada (WSL), como tarefa ----------
    def rodar(self, stage="cego", pool=40, n_off=32):
        raise ValueError("EXPLICIT_RITE_DISPATCH_REQUIRED: use the authorized pinned rite executor")
        tid = uuid.uuid4().hex[:12]; log = os.path.join(self.raiz, "estado", "gw_rodada_%s.log" % tid)
        args = [sys.executable, os.path.join(self.inv, "rodar_fase6.py"), "--pool", str(int(pool)), "--n_off", str(int(n_off))] + (["--so-cego"] if stage == "cego" else [])
        t = dict(tarefa=tid, estado="rodando", inicio=time.strftime("%Y-%m-%d %H:%M:%S"), stage=stage, log=log, comando=" ".join(args))
        self.tarefas[tid] = t
        def run():
            with open(log, "w", encoding="utf-8") as fh:
                r = subprocess.run(args, stdout=fh, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", cwd=self.inv)
            t.update(estado="pronta" if r.returncode == 0 else "falhou", rc=r.returncode, fim=time.strftime("%Y-%m-%d %H:%M:%S"))
            try: t["cauda"] = open(log, encoding="utf-8", errors="replace").read()[-3000:]
            except Exception: pass
        threading.Thread(target=run, daemon=True).start()
        return t
