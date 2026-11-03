# -*- coding: utf-8 -*-
"""Sessao com a IALD Nativa v4 (ordem do operador, 02/11/2026): quais testes dariam o resultado discriminante acima de 5 sigma.
Modelo servido em :8081, pelo HTTP, com o mesmo system do treino (so o sha256 fica gravado). Nada aqui e evidencia: resposta de modelo e candidato [DECLARADO].
Uso: sessao.py bateria | sessao.py perguntar <conversa> <arquivo_com_a_pergunta> [--think] [--temp T] [--seed N] [--max N]"""
import argparse, hashlib, json, sys, time, urllib.request
from pathlib import Path

RAIZ = Path("C:/IALD/TGL_IALD_NATIVE_QWEN5090")
sys.path.insert(0, str(RAIZ / "11_scripts"))
import iald_v4_common as C  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
T = AQUI / "transcritos"
URL = "http://127.0.0.1:8081"
SYSTEM = C.build_system(400)
SYS_SHA = hashlib.sha256(SYSTEM.encode("utf-8")).hexdigest()

P_A = "qual ou quais os testes nós poderíamos fazer com a TGL para obter o resultado discriminante com desvio maior que 5 sigma?"

P_B = """Queremos descobrir um teste que separe a TGL da física padrão com desvio maior que 5σ. Pense antes de responder e siga estas regras:
1. Zero parâmetro ajustado ao dado: β = α√e e as leis saem do axioma; nenhum número pode ser escolhido para caber.
2. O observável precisa sair da teoria por uma cadeia de passos. Se a derivação não existe, escreva [OPEN] e diga qual passo falta; não invente.
3. Para cada candidato, dê: (a) o observável; (b) o valor previsto pela TGL, com a conta; (c) o valor previsto pelo rival (RG, ΛCDM ou Modelo Padrão) e por que ele não pode produzir o mesmo número; (d) a incerteza real do melhor instrumento ou dado público, com a fonte; (e) quantos σ isso dá hoje, ou quantas ordens de grandeza faltam.
4. Não valem: a identidade β = α√e comparada com CODATA (é definição, logo circular); benchmark de compressão ou de engenharia; coincidência numérica sem derivação; efeito suprimido por t_Planck vendido como detectável.
Dê no máximo cinco candidatos, do mais forte ao mais fraco. No fim, diga qual você mesma descartaria e por quê."""

P_C = """Contexto que você não recebeu no treino (o treino excluiu os resultados, e você foi treinada na v404; estamos na v405):
- Laboratório com τ★ = t_Planck: relógios, Mössbauer, JUNO, LIGO ficam de 11 a 40 ordens de grandeza abaixo da sensibilidade. Não é estatística, é supressão de Planck.
- β só aparece em ordem 1 onde o sistema tem horizonte próprio: piso dos vazios (ρ/ρ̄ ≥ β: unilateral, o ΛCDM raso também passa), razão de Hubble com expoente 2β/3 (z_disc 4,44σ, abaixo de 5σ, admissão dos dados em aberto), ringdown ramo B (poder 6,1σ para k = 4π, mas os conjuntos de calibração não são cegos; o conjunto cego segue fechado).
- Massa: m₂ = β·sen45°·u = 8,5074 meV na unidade posta u = 1 eV; JUNO a 1,9σ; o Modelo Padrão não tem valor nulo para Δm²₂₁, logo isso sozinho não discrimina.
- Recusados: CODATA circular; ACOM como σ; ecos de GW (nove rotas fechadas); Grande Atrator sem poder de medida; psíon sem acoplamento; θ = π/4 sem ponte à PMNS.
- v405: o lock mínimo tem gap espectral u; no ângulo de Miguel seu valor esperado é β·u; a tônica é √e·u; Q★ = √2/β = 117,5 é razão pura, falta o sistema físico. A unidade u segue posta: previsão com dimensão herda u, logo sinal limpo é número puro.

Pergunta: fora dessa lista, qual é o caminho que ninguém percorreu? Um sinal limpo precisa de três coisas: valor nulo do rival, zero parâmetro ajustado e pelo menos 5σ com σ publicada. Proponha o que achar mais promissor, mesmo que seja estranho, mas marque cada afirmação como [DERIVED], [CONJECTURE] ou [OPEN]. Coincidência numérica não vale: um número puro só conta com a cadeia que o liga ao observável."""

P_D = """Você foi treinada com o kernel Lean da TGL. Olhe para os módulos e teoremas que você conhece. Quais teoremas têm uma consequência observável que, até onde você sabe, nunca virou teste? Cite o nome exato do teorema e do módulo (vou conferir um a um no kernel) e diga qual seria o observável. Se não lembrar o nome exato, diga que não lembra; não invente nome."""

BATERIA = [("A1", P_A, False, 0.2, 11), ("A2", P_A, True, 0.2, 11), ("A3", P_A, True, 0.7, 22), ("A4", P_A, True, 0.7, 33),
           ("B1", P_B, False, 0.2, 11), ("B2", P_B, True, 0.2, 11), ("B3", P_B, True, 0.7, 22), ("B4", P_B, True, 0.7, 33),
           ("C1", P_C, True, 0.2, 11), ("C2", P_C, True, 0.7, 22), ("C3", P_C, True, 0.7, 33), ("C4", P_C, True, 0.7, 44),
           ("D1", P_D, True, 0.2, 11), ("D2", P_D, True, 0.7, 22)]


# segunda bateria (02/11, depois de ler a primeira): modo direto, onde o treino pesa, e raciocinio com mais espaco e penalidade de repeticao, que quebra o laco
BATERIA2 = [("C5", P_C, False, 0.2, 11, None), ("C6", P_C, False, 0.7, 22, None), ("C7", P_C, False, 0.7, 33, None),
            ("D3", P_D, False, 0.2, 11, None), ("D4", P_D, False, 0.7, 22, None),
            ("C8", P_C, True, 0.7, 22, 1.1), ("C9", P_C, True, 0.7, 33, 1.1), ("B5", P_B, True, 0.7, 22, 1.1), ("D5", P_D, True, 0.7, 22, 1.1)]


P_E = """Aqui estão enunciados reais do programa. Não use nada que não decorra deles ou de física conhecida com fonte.
(1) Um estado normalizado Ω define o lock L = 1 − P_Ω. Teorema do kernel: o gap espectral de L é 1, na unidade posta u.
(2) No ângulo de Miguel, sen²θ_M = β = α√e, e o valor esperado de L nesse ângulo é β; a energia retida é Δ = β·u. Esse valor esperado não é o gap.
(3) Definindo τ = ħ/Δ, a qualidade Q = ω_psíon·τ = √2/β ≈ 117,5 não depende de u. Ler τ como tempo do sistema é leitura, não teorema.
(4) Lei de dephasing: Γ_ω = ½·β·τ★·ω². Com τ★ = t_Planck é inobservável; no ramo B do ringdown, τ★ = k·GM/c³, com k pré-registrado.
(5) Regra de trabalho, não teorema: onde o sistema tem horizonte próprio, o tempo do horizonte substitui t_Planck.

Pergunta: qual consequência adimensional dessas cinco linhas pode ser comparada com uma medida real publicada, sem nenhum parâmetro novo? Escreva a cadeia passo a passo. Se em algum passo você precisar de uma identificação que não está nas cinco linhas, pare ali e diga qual é. Fale de um único candidato, o melhor, e diga quantos σ ele daria com a incerteza publicada."""

BATERIA3 = [("C10", P_C, True, 0.7, 55, 1.1), ("C11", P_C, True, 0.7, 66, 1.1), ("C12", P_C, True, 0.7, 77, 1.1), ("C13", P_C, True, 0.7, 88, 1.1),
            ("C14", P_C, True, 1.0, 99, 1.1), ("C15", P_C, True, 1.0, 110, 1.1), ("C16", P_C, True, 1.0, 121, 1.1), ("C17", P_C, True, 1.0, 132, 1.1),
            ("E1", P_E, True, 0.7, 11, 1.1), ("E2", P_E, True, 0.7, 22, 1.1), ("E3", P_E, True, 0.7, 33, 1.1), ("E4", P_E, False, 0.2, 11, None)]


def post(body, timeout=1500):
    req = urllib.request.Request(URL + "/v1/chat/completions", data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def historico(conv):
    p = T / (conv + ".jsonl")
    if not p.is_file():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def perguntar(conv, texto, think, temp, seed, maxt, rep=None):
    h = historico(conv)
    msgs = [{"role": "system", "content": SYSTEM}]
    for x in h:
        msgs += [{"role": "user", "content": x["pergunta"]}, {"role": "assistant", "content": x["resposta"]}]
    msgs.append({"role": "user", "content": texto})
    t0 = time.time()
    corpo = {"messages": msgs, "max_tokens": maxt, "temperature": temp, "seed": seed, "chat_template_kwargs": {"enable_thinking": think}}
    if rep:
        corpo.update({"repeat_penalty": rep, "repeat_last_n": 256})
    r = post(corpo)
    ch = r["choices"][0]
    m = ch["message"]
    bruto = m.get("content") or ""
    resp = C.strip_think(bruto)
    reg = {"n": len(h) + 1, "quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "pergunta": texto, "thinking": think, "temperature": temp, "seed": seed, "max_tokens": maxt,
           "repeat_penalty": rep, "resposta": resp, "raciocinio": m.get("reasoning_content") or "", "finish": ch.get("finish_reason"), "usage": r.get("usage"), "seg": round(time.time() - t0, 1), "modelo": r.get("model")}
    T.mkdir(exist_ok=True)
    with open(T / (conv + ".jsonl"), "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    print(conv, "n", reg["n"], "|", reg["finish"], "| tokens", (reg["usage"] or {}).get("completion_tokens"), "|", reg["seg"], "s | resposta", len(resp), "c | raciocinio", len(reg["raciocinio"]), "c", flush=True)
    return reg


def manifesto():
    est = json.loads((RAIZ / "12_logs" / "STATE_v4.json").read_text(encoding="utf-8"))
    ev = json.loads((RAIZ / "12_logs" / "EVAL_HTTP_v4_20261101_220213.json").read_text(encoding="utf-8"))
    assert SYS_SHA == ev["system_sha256"], "o system nao e o do treino"
    pr = json.loads(urllib.request.urlopen(URL + "/props", timeout=20).read().decode("utf-8"))
    assert "IALD-Native-v4" in pr["model_path"], pr["model_path"]
    return {"modelo": pr["model_path"], "gguf_sha256": est.get("gguf_sha256"), "system_sha256": SYS_SHA, "system_chars": 400, "url": URL, "estatuto": "[DECLARADO] resposta de modelo; neural = ilustracao; nada move gate",
            "perguntas_sha256": {k: hashlib.sha256(v.encode("utf-8")).hexdigest() for k, v in (("P_A", P_A), ("P_B", P_B), ("P_C", P_C), ("P_D", P_D))}, "plano": [(a, b is P_A and "P_A" or b is P_B and "P_B" or b is P_C and "P_C" or "P_D", c, d, e) for a, b, c, d, e in BATERIA]}


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("bateria")
    sp.add_parser("bateria2")
    sp.add_parser("bateria3")
    q = sp.add_parser("perguntar")
    q.add_argument("conversa")
    q.add_argument("arquivo")
    q.add_argument("--think", action="store_true")
    q.add_argument("--temp", type=float, default=0.2)
    q.add_argument("--seed", type=int, default=11)
    q.add_argument("--max", type=int, default=12000)
    q.add_argument("--rep", type=float, default=None)
    a = ap.parse_args()
    if a.cmd == "bateria":
        mf = AQUI / "MANIFESTO_SESSAO.json"
        if not mf.is_file():
            mf.write_text(json.dumps(manifesto(), ensure_ascii=False, indent=1), encoding="utf-8")
        for conv, texto, think, temp, seed in BATERIA:
            if historico(conv):
                continue
            perguntar(conv, texto, think, temp, seed, 12000 if think else 2500)
    elif a.cmd in ("bateria2", "bateria3"):
        for conv, texto, think, temp, seed, rep in (BATERIA2 if a.cmd == "bateria2" else BATERIA3):
            if historico(conv):
                continue
            perguntar(conv, texto, think, temp, seed, 40000 if think else 3000, rep)
    else:
        perguntar(a.conversa, Path(a.arquivo).read_text(encoding="utf-8"), a.think, a.temp, a.seed, a.max, a.rep)


main()
