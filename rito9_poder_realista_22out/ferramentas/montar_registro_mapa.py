"""Monta registro_mapa_rito9_poder_realista.json (so campos de `rotas.py modelo`; olhou_dados=false).

NAO registra nada no mapa (ato da gerencia/operador: rotas.py registrar <json> --quem ...). Numeros lidos dos dados.
Uso: python montar_registro_mapa.py <dir_work>
"""
import csv
import json
import os
import statistics
import sys

W = sys.argv[1]
S = os.path.join(W, "saida_rodada")


def rd(p):
    return list(csv.DictReader(open(p, encoding="utf-8", newline="")))


casos = rd(os.path.join(S, "n_req_por_caso.csv"))
ver = json.load(open(os.path.join(W, "veredito.json"), encoding="utf-8"))
pr = json.load(open(os.path.join(W, "PREREGISTRO.json"), encoding="utf-8"))
mc = rd(os.path.join(S, "verificacao_mc.csv"))
rob = rd(os.path.join(S, "robustez_numerica.csv"))


def ns(fam, ell=None):
    return sorted(int(r["n_req"]) for r in casos if r["familia"] == fam and r["n_req"] != "" and (ell is None or float(r["ell_km"]) == ell))


p1, p2, p3 = ns("P1"), ns("P2"), ns("P3")
med20 = ns("P2", 20)[len(ns("P2", 20)) // 2]
melhor = ver["melhor_caso_realista"]
b2 = min((r for r in casos if r["familia"] == "P2"), key=lambda r: (int(r["n_req"]), r["case_id"]))
der = {r["case_id"]: r for r in rd(os.path.join(W, "derivados_KK_por_caso.csv"))}[b2["case_id"]]
nkl = [int(r["n_req"]) * float(r["kl_h1_h0_cap"]) for r in casos if r["familia"] == "P2"]
rota_id = "d7.kilonova_fronteira_aguda"
seqs = pr["mapa_de_rotas"]["seqs_do_historico"]

reg = {
    "tipo": "RESULTADO",
    "rota_id": rota_id,
    "dominio": "QG",
    "titulo": (f"ESTUDO DE PODER REALISTA (oraculo, curva de emissao BNS): {ver['veredito']} — n_req P1 {p1[0]}-{p1[-1]}, P2 {p2[0]}-{p2[-1]} neutrinos; "
               f"a parede e a taxa K-K (2500 fusoes por neutrino esperado), nao a estatistica"),
    "pergunta": ("a arena BNS pode discriminar H1 = H0 (*) K_beta(ell) de H0 quando H0 e a curva de emissao realista (Cusinato 2022) em vez do sigma_e livre do esqueleto, "
                 "com o perfil H0 CONHECIDO (oraculo) e o limiar exato de 5 sigma?"),
    "dados": [
        "nenhum dado observacional; SYNTHETIC_DIAGNOSTIC_ONLY; observed_sigma = null",
        "beta = SEALED_CODATA_ALPHA * sqrt(e) lido do um.py instalado no Nos (linha %d: %s; so leitura), nunca literal" % (
            pr["beta"]["lido_no_preregistro"]["linha"], pr["beta"]["lido_no_preregistro"]["texto"]),
        "[KNOWN] Cusinato et al. 2022 (EPJA 58, 99; arXiv:2111.13005): 3-4 picos nos primeiros 10-15 ms (p8), PC um pico baixo ate 1 ms (p8), Gamma ~1 ms (p12), beta_nu ~100 ms (p14), MNS varios segundos (p9)",
        "[KNOWN] Kyutoku & Kashiyama (PRD 97, 103001; arXiv:1710.05922v3): >~2500 fusoes ate 200 Mpc e ~80 Mt ano por neutrino, R = 1 Mpc^-3 Myr^-1 (p1); Eq. 6 N_nu(D) com (D/100 Mpc)^-2 (p4); Eq. 8 (p5)",
        "fontes do Kimi lidas so para leitura (ESQUELETO, esqueleto .py/.json, PROVAS, PRE_REGISTRO, RT1, RELATORIO_R1, test_rito9): hashes no PREREGISTRO.json",
    ],
    "metodo": (
        "PRE-REGISTRO ANTES DA RODADA (PREREGISTRO.json + veredito.py + codigo pinados por sha256; PINS.json). H1 = H0 (*) K_beta(ell), K_beta = espera geometrica do excesso (N-1)ell/c, ell em {10,20,30} km [INPUT]. "
        "Celulas de largura ell/c: P1 = filtro IIR de P0 (exato). Familias H0: P1 so o surto (K 3-4 picos, S 10/14 ms, FWHM 1/2 ms, amplitudes decrescentes/iguais; 16 perfis); "
        "P2 = (1-f) P1 + f exp(-t/tau)/tau, tau 30/100/300/1000 ms, f 0.5/0.8 (128 perfis); P3 pico unico 0.5 ms (fora do veredito); bancadas fora do veredito: REF (H0 gaussiana do esqueleto, criterio exato), SENS_VETO, SENS_ZERO. "
        "Estatistica: LLR de forma completa, H0 conhecido; limiar = quantil 5 sigma unilateral da nula (convolucao n-vezes exata na rede de lambda por FFT, verificada por simulacao com amostragem por importancia, P0(A)=E1[exp(-Lambda);A]); "
        "n_req = menor n com mediana do LLR sob H1 >= limiar (poder >= 0.5). Veredito pinado: POWERED_BNS se algum caso P1/P2 tiver n_req <= 10/2500 neutrinos esperados; senao UNDERPOWERED_WALL_MEASURED; INCONCLUSIVE se porta numerica falhar. "
        "%d casos, 14 processos, rodada oficial unica." % ver["n_casos"]),
    "resultado": (
        f"{ver['veredito']}. n_req (neutrinos detectados, oraculo): P1 {p1[0]}-{p1[-1]}; P2 {p2[0]}-{p2[-1]} (mediana em ell=20 km: {med20}; em todos os 384 casos P2, n_req*KL(H1||H0) = {min(nkl):.2f}-{max(nkl):.2f} ~ 5^2/2); P3 {p3[0]}-{p3[-1]}. "
        f"Parede K-K: menor caso realista P2 ({b2['case_id']}, n={b2['n_req']}) = {float(der['fusoes_necessarias_ate_Deff']):.0f} fusoes ate 200 Mpc, {float(der['exposicao_Mt_ano']):.0f} Mt ano, "
        f"detector de {float(der['massa_detector_Mt_para_max_eventos']):.0f} Mt para 10 eventos, ou UM evento a <= {float(der['Dmax_um_evento_Mpc']):.2f} Mpc; menor caso P1 (idealizado, barreira de cauda gaussiana): "
        f"{melhor['case_id']} n={melhor['n_req']} = {melhor['fusoes_necessarias_ate_Deff']:.0f} fusoes (fator {melhor['fator_acima_do_alcance']:.0f} acima do alcance de 10 eventos). "
        f"Esqueleto do Kimi: o criterio CLT subestimou n (sigma_e=3 ms: exato 24/7/4 x CLT 12/2/1 em ell 10/20/30); o poder esta na forma (media: 26-359; forma: 1-321). "
        f"Sensibilidades: cauda de 0.1% no P1 +1 neutrino (10%: +5); ponto-zero incerto de 4 ms multiplica n_req por ~2.8 (P2-like, ell=20) a 5.9 (ell=10). "
        f"Verificacoes: {len(mc)} pontos de simulacao por importancia e {len(rob)} de robustez dentro da tolerancia; 0 falhas numericas; limite de Wald respeitado."),
    "veredito": ver["veredito"],
    "estatuto": "REAL (diagnostico sintetico com oraculo = limite superior do poder; nenhuma afirmacao sobre a natureza)",
    "status": "EM_CURSO",
    "olhou_dados": False,
    "defeito": (
        "oraculo: H0 e ponto-zero conhecidos (piso do poder; nuisance reais so encarecem); P1 herda barreira de cauda gaussiana (vales e cauda 'impossiveis' sob H0) e e a borda otimista; "
        "resolucao ideal, sem fundo, sem massa do neutrino, sem multiplicidade; H-KN/H-SEQ/H-DECOH/H-BRANCH/GW-CLOCK seguem CONJECTURE e nao foram testadas (K_beta e dado); "
        "n_req e neutrinos esperados (sem Poisson); taxa K-K e projecao de 2018 para 1 Mt, nao inventario de 2026; ell, larguras, amplitudes e fracoes sao [INPUT] dentro de faixas [KNOWN]."),
    "nao_refazer": (
        "nao tratar o 'bastam 1-2 neutrinos' do esqueleto como numero (era CLT com sigma_e livre); nao usar P1 como previsao (e a borda otimista); nao ler a parede como estatistica (e taxa x massa: "
        "2500 fusoes por neutrino); nao ajustar a GW170817; nao declarar 5 sigma de simulacao; nao refazer a rodada com os mesmos pinos (o resultado esta em saida_rodada e veredito.json)."),
    "proximo_passo": (
        "a gerencia decide: (a) registrar a parede de BNS como resultado ex-ante do Rito 9 (BNS = rito lento/inviavel na decada, nao teste de 5 sigma); (b) pre-registro separado da arena de supernova galactica "
        "(relogio GW do bounce, ~1e4 neutrinos, flash de nu_e sincronizado em <1 ms; nota no RESULTADO.md, fora do veredito) com perfil de emissao de SN e ell da proto-estrela definidos ANTES; "
        "(c) se alguem derivar l(Theta_GW) e sigma_e de um modelo BNS independente, rodar SENS_ZERO com a populacao real."),
    "onde": "Central de Patentes\\work\\rito9_poder_realista_22out\\ (RESULTADO.md, PREREGISTRO.json, veredito.py, veredito.json, saida_rodada\\*.csv, ferramentas\\)",
    "artefatos": [
        os.path.join(W, "RESULTADO.md"),
        os.path.join(W, "PREREGISTRO.json"),
        os.path.join(W, "PINS.json"),
        os.path.join(W, "veredito.py"),
        os.path.join(W, "veredito.json"),
        os.path.join(W, "derivados_KK_por_caso.csv"),
        os.path.join(S, "n_req_por_caso.csv"),
        os.path.join(S, "varredura_n.csv"),
        os.path.join(S, "verificacao_mc.csv"),
        os.path.join(S, "robustez_numerica.csv"),
        os.path.join(S, "MANIFEST_RODADA.json"),
    ],
    "refs": [f"seq{s}" for s in seqs if s in (1301, 1305, 1307, 1309, 1310, 1311, 1315, 1316, 1317, 1321)] + [
        "infra.bancada_um_modo_uso_kimi", "Kyutoku-Kashiyama arXiv:1710.05922", "Cusinato et al. arXiv:2111.13005"],
    "nota": (
        "Fora do veredito: nota de ordem de grandeza da arena alternativa (SN galactica) no RESULTADO.md secao 8 [DECLARADO/KNOWN]: flash de nu_e sincronizado ao bounce e ao pico de GW em <1 ms "
        "(Arnaud et al. 2001, hep-ph/0109027: 3.5+-0.5 ms e 0.1+-0.4 ms), instante do bounce por nu_anti-e ~10 ms (Super-K-class, Pagliaroli+) e +-3.5 ms 95% CL (IceCube, Halzen-Raffelt), taxa galactica 1.63+-0.46/seculo "
        "(Rozwadowska+). Processo: o um.py mudou desde a custodia de 21/10 (alpha identico); ensaios de desenvolvimento so em perfis fora das familias; nada escrito no mapa/quadro/memoria/tunel/site/git."),
}
out = os.path.join(W, "registro_mapa_rito9_poder_realista.json")
with open(out, "x", encoding="utf-8") as f:
    json.dump(reg, f, indent=2, ensure_ascii=False)
print("ok", out, "tamanhos:", {k: len(v) for k, v in reg.items() if isinstance(v, str)})
