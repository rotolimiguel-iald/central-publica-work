# -*- coding: utf-8 -*-
"""gw_stack.py -- o EMPILHAMENTO e a REGRA DE VEREDITO da Fase 6 (ECO V3, «a transformada radical»), compartilhados pelo executor (rodar_fase6.py) e pela Bancada
residente (bancada/gw.py), para que o número da rodada selada e o número da consulta em tempo real saiam da MESMA função.
Combina H1+L1 por evento (coerente, variância inversa, viés subtraído), empilha por evento, jackknife por evento, fator de dispersão on/off, e lê por LEITURA
(R1 √β, R2 sin 2θ_M, R3 β) o poder, a sistemática relativa e z_excl = (recuperação − â)/σ_usado. CONFIRMED proibido por construção."""
import math
import numpy as np

LAWS = ("MAY", "KMS", "DEC"); CTRL = ("x0.5", "x2")   # V5 (01/10, tarde): + DEC2025 = 2GM_f/(β c³), do acervo do operador; estágios sem a lei devolvem n_eventos = 0 (V3/V4 intocadas)


def empilhar(cego, aberto, sub, CR, READ, filtro=None, sigma_regra="max"):
    """cego/aberto: os JSON dos estágios (aberto pode ser None → só o poder). sub ∈ {'todos', 'maio', 'o4'}. filtro(serie_cega) → bool (opcional).
    sigma_regra: 'max' (pré-registrado: max(σ_off, σ_jack)) | 'off' | 'jack' — as outras duas são só consulta, nunca veredito."""
    C = {r["key"]: r for r in cego["per_series"] if r.get("status") == "OK"}
    A = {r["key"]: r for r in (aberto["per_series"] if aberto else []) if r.get("status") == "OK"}
    out = {}
    for law in LAWS:
        ev = {}
        for k, c in C.items():
            if sub != "todos" and c["src"] != sub: continue
            if filtro is not None and not filtro(c): continue
            L = c["laws"].get(law)
            if not L or not L["used"]: continue
            a = A.get(k); Lo = a["laws"][law] if a else None
            if aberto and (Lo is None or not np.isfinite(Lo["a_on"]) or Lo["snr_anchor"] < CR["snr_ancoragem_min"]): continue
            w = 1.0 / L["sigma"] ** 2
            e = ev.setdefault(c["event"], dict(w=0.0, a=0.0, r1=0.0, r2=0.0, mis={}, fam=0.0, wfam=0.0, ctrl={cc: dict(w=0.0, a=0.0, x=0.0) for cc in CTRL}, dets=[], snr=c.get("snr_net"), Mf=c.get("Mf_det"), era=c.get("era"), src=c.get("src")))
            e["w"] += w; e["r1"] += w * L["recovery_R1"]; e["r2"] += w * L["recovery_R2"]; e["dets"].append(k[-2:])
            for mk, mv in L["mismatch_induced"].items(): e["mis"][mk] = e["mis"].get(mk, 0.0) + w * mv
            if L["family_induced"] is not None: e["fam"] += w * L["family_induced"]; e["wfam"] += w
            if aberto: e["a"] += w * (Lo["a_on"] - L["bias"])
            for cc in CTRL:
                ct = L["controls"][cc]; wc = 1.0 / ct["sigma"] ** 2 if ct["sigma"] > 0 else 0.0; e["ctrl"][cc]["w"] += wc; e["ctrl"][cc]["x"] += wc * ct["xtalk_from_R1"]
                if aberto: e["ctrl"][cc]["a"] += wc * (Lo["a_on_controls"][cc] - ct["bias"])
        n = len(ev)
        if n == 0: out[law] = dict(n_eventos=0); continue
        W = np.array([e["w"] for e in ev.values()]); a_ev = np.array([e["a"] / e["w"] for e in ev.values()]); r1 = np.array([e["r1"] / e["w"] for e in ev.values()]); r2 = np.array([e["r2"] / e["w"] for e in ev.values()])
        sw = W.sum(); a_c = float((W * a_ev).sum() / sw); s_off = float(1 / math.sqrt(sw)); rec1 = float((W * r1).sum() / sw); rec2 = float((W * r2).sum() / sw)
        if aberto and n > 2:
            jk = np.array([((W * a_ev).sum() - W[i] * a_ev[i]) / (sw - W[i]) for i in range(n)]); s_jack = float(math.sqrt((n - 1) / n * ((jk - jk.mean()) ** 2).sum()))
            z_i = (a_ev - a_c) * np.sqrt(W); disp = float(math.sqrt((z_i ** 2).sum() / (n - 1)))
        else: s_jack, disp = float("nan"), float("nan")
        if sigma_regra == "off" or not np.isfinite(s_jack): s_used = s_off
        elif sigma_regra == "jack": s_used = s_jack
        else: s_used = max(s_off, s_jack)
        keys = sorted(set(mk for e in ev.values() for mk in e["mis"])); mis_c = {mk: float(sum(e["mis"].get(mk, 0.0) for e in ev.values()) / sw) for mk in keys}
        wf = sum(e["wfam"] for e in ev.values()); fam_c = float(sum(e["fam"] for e in ev.values()) / wf) if wf > 0 else None
        sys_abs = max([abs(v) for v in mis_c.values()] + ([abs(fam_c)] if fam_c is not None else [0.0]))
        ctrl = {}
        for cc in CTRL:
            wc = np.array([e["ctrl"][cc]["w"] for e in ev.values()]); swc = wc.sum()
            ctrl[cc] = dict(a=float(sum(e["ctrl"][cc]["a"] for e in ev.values()) / swc) if (aberto and swc > 0) else None, sigma=float(1 / math.sqrt(swc)) if swc > 0 else None,
                            xtalk_from_R1=float(sum(e["ctrl"][cc]["x"] for e in ev.values()) / swc) if swc > 0 else None)
            ctrl[cc]["z"] = (ctrl[cc]["a"] / ctrl[cc]["sigma"]) if (ctrl[cc]["a"] is not None and ctrl[cc]["sigma"]) else None
        por_leitura = {}
        for rn, rd in READ.items():
            ae = rd["a_esperado"]; rec = {"R1_peso1": rec1, "R2_peso2_2theta": rec2, "R3_quadrado": rec1 * ae}[rn]
            por_leitura[rn] = dict(a_esperado=ae, recuperacao=rec, recuperacao_relativa=rec / ae, poder=abs(rec) / s_used, sistematica_relativa=sys_abs / abs(ae),
                                   z_excl=((rec - a_c) / s_used) if aberto else None, z_det=(a_c / s_used) if aberto else None)
        por_evento = [dict(evento=k, a=(float(a_ev[i]) if aberto else None), sigma=float(1 / math.sqrt(W[i])), peso=float(W[i] / sw), dets=e["dets"], snr=e["snr"], Mf_det=e["Mf"], era=e["era"], src=e["src"])
                      for i, (k, e) in enumerate(ev.items())]
        out[law] = dict(n_eventos=n, n_series=int(sum(len(e["dets"]) for e in ev.values())), a=a_c if aberto else None, sigma_off=s_off, sigma_jack=s_jack, fator_dispersao=disp, sigma_usado=s_used, sigma_regra=sigma_regra,
                        z_det=(a_c / s_used) if aberto else None, recuperacao_R1=rec1, recuperacao_R2=rec2, descasamento=mis_c, familia=fam_c, sistematica_abs=sys_abs, controles=ctrl, por_leitura=por_leitura,
                        eventos=sorted(ev.keys()), por_evento=por_evento)
    return out


def veredito(st, rn, CR):
    """A regra pré-registrada, por (subamostra, lei, leitura). Devolve (veredito, razões)."""
    P = st["por_leitura"][rn]; V = "TGL_ECHO_RADICAL_V3__"
    if st["n_eventos"] < CR["min_eventos"]: return V + "INSUFFICIENT_SAMPLE", ["n_eventos %d < %d" % (st["n_eventos"], CR["min_eventos"])]
    if P["sistematica_relativa"] > CR["sistematica_max_relativa"]: return V + "INCONCLUSIVE_SYSTEMATICS", ["sistematica_relativa %.3f > %.1f" % (P["sistematica_relativa"], CR["sistematica_max_relativa"])]
    if P["poder"] < CR["poder_min"]: return V + "NOT_FALSIFIED_UNDERPOWERED", ["poder %.2f < %.0f" % (P["poder"], CR["poder_min"])]
    if P["z_det"] is None: return V + "NOT_FALSIFIED_UNDERPOWERED", ["estágio aberto ausente: só o poder está lido"]
    zc = [c["z"] for c in st["controles"].values() if c.get("z") is not None]
    if any(abs(z) >= CR["z_det"] for z in zc) and abs(P["z_det"]) < CR["z_det"]: return V + "INCONCLUSIVE_SYSTEMATICS", ["DELAY_CONTROL_RESPONDS: z controles %s" % ", ".join("%.1f" % z for z in zc)]
    lo, hi = CR["janela_recuperacao"]; in_win = lo <= P["recuperacao_relativa"] <= hi; same_sign = (st["a"] * P["a_esperado"]) > 0
    if abs(P["z_det"]) >= CR["z_det"] and in_win and same_sign: return V + "DETECTED_AT_DELAY_LAW", ["z_det %.2f; recuperação relativa %.2f" % (P["z_det"], P["recuperacao_relativa"])]
    if P["z_excl"] * (1 if P["a_esperado"] > 0 else -1) >= CR["z_excl"] and in_win: return V + "FALSIFIED_AT_DELAY_LAW", ["z_excl %.2f; |a| mais perto de 0 que de %.3f" % (P["z_excl"], P["recuperacao"])]
    return V + "NOT_FALSIFIED_POWERED", ["z_det %.2f; z_excl %.2f; poder %.2f" % (P["z_det"], P["z_excl"], P["poder"])]
