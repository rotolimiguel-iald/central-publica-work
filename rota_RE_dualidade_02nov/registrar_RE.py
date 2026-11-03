# -*- coding: utf-8 -*-
"""Registro da derivacao da R-E, do custo geometrico contra Landauer e do qubit no um.py (gerencia c1, 02/11/2026): Mapa, ACOM, memoria, Atlas ao lado. Nada move gate, rito ou kernel."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
AQUI = Path(__file__).resolve().parent
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
NOTA, CR, CL = AQUI / "DERIVACAO_RE_02nov.md", AQUI / "CONTAS_RE.json", AQUI / "CONTAS_LANDAUER.json"
MQC = CEN / "patents/BR102026003460-6_MQC/runner/one_mqc.py"
c, l = json.loads(CR.read_text(encoding="utf-8")), json.loads(CL.read_text(encoding="utf-8"))

reg = [
 {"tipo": "RESULTADO", "rota_id": "discriminante.ordem018.f2.r_e", "dominio": "D1_FUNDO_COSMOLOGICO", "status": "EXAMINADA", "estatuto": "DERIVED",
  "titulo": "R-E derivada: K nao age na luminosidade nem no angulo; eta = 1; nao discrimina",
  "metodo": "kernel: dephase_preserves_trace, leakVerb, Verbo L = raiz(beta)*raiz(K); hipotese nomeada H1 (K comuta com o momento do foton, por simetria do estado); conferencia aritmetica sem H1; nenhum dado novo aberto",
  "olhou_dados": False,
  "resultado": "f_L = f_A, Alternativa A. Alternativa B sem mecanismo: k(0,15)-1 = %.4f%% contra 8,38%%, 1/%.0f. Leitores que nao sao luminosidade: Delta chi2 = %.2f a favor de K comum, valores declarados. K separa leitores com regua primordial dos sem regua." % (100 * c["k_menos_1_z015"], c["fator_que_falta_escada"], c["delta_chi2_K_comum_contra_so_luminosidade"]),
  "veredito": "RE_DERIVADA__K_NAO_AGE_EM_L_NEM_A__ETA_1__ALTERNATIVA_B_SEM_MECANISMO__NAO_DISCRIMINA__SEM_PEDRA",
  "defeito": "sem pedra de kernel; H1 nomeada; pedra do traco e de dimensao finita; H0 publicados nao lidos por hash",
  "nao_refazer": "nao procurar eta diferente de 1 como sinal da TGL; nao aplicar K so a luminosidade",
  "proximo_passo": "leitura do operador: H1 (so fase) ou mudanca de face", "artefatos": [str(NOTA), str(CR)]},
 {"tipo": "ANOTACAO", "rota_id": "discriminante.ordem018.f2.r_f", "dominio": "D1_FUNDO_COSMOLOGICO", "titulo": "Sob H1 da derivacao R-E: alternativa A, gamma_T = 0", "resultado": "Numero e energia conservados pela defasagem na base de momento; T(z) = T0(1+z).", "estatuto": "DERIVED", "artefatos": [str(NOTA)]},
 {"tipo": "ANOTACAO", "rota_id": "discriminante.ordem018.f2.r_g", "dominio": "D1_FUNDO_COSMOLOGICO", "titulo": "Derivacao R-E escolhe a alternativa A para lentes: leem K*H_fundo", "resultado": "f_t = f_phi = 1. Justifica TDCOSMO e masers no composto da Fase 9, que antes era escolha sem justificativa.", "estatuto": "DERIVED", "artefatos": [str(NOTA)]},
 {"tipo": "ANOTACAO", "rota_id": "discriminante.ordem018.r_h_sirenes", "dominio": "D1_FUNDO_COSMOLOGICO", "titulo": "Ponte GW sob H1 para o graviton: sirenes leem K*H_fundo = 74,27", "resultado": "Sem regua e sem escada. Separacao do fundo 68,53; 5 sigma pede sigma(H0) = %.2f km/s/Mpc; hoje 11." % c["sigma_sirenes_para_5s"], "estatuto": "DERIVED", "artefatos": [str(NOTA)]},
 {"tipo": "ROTA", "rota_id": "hubble.k_sem_portador_fisico_02nov", "dominio": "D1_FUNDO_COSMOLOGICO", "status": "EXAMINADA", "estatuto": "REAL",
  "titulo": "Onde K poderia morar: seis moradas, cinco caem, uma aberta sem mecanismo",
  "pergunta": "Que portador fisico sustenta H0_local = K*H0_fundo?",
  "dados": ["FIRAS, theta*, limite de Delta N_eff de Goldstein & Hill, fundo nu da Fase 9"], "metodo": "contas de ordem com o fundo da Fase 9; nenhum dado aberto", "olhou_dados": False,
  "resultado": "Transporte da escada 143x pequeno; corpo cinza K^3 = %.3f contra FIRAS; lei como metrica com regua parada ~%.0f sigma em theta*; H primordial Delta N_eff %.2f a %.2f contra 0,107; regua por rho+p %.2f%% contra -7,73%%. Aberta: luz muda de face preservando Planck." % (c["fator_de_diluicao_corpo_cinza"], c["sigmas_theta"], c["dNeff_BBN_se_H_primordial"], c["dNeff_CMB_se_H_primordial"], 100 * c["regua_fechamento"]),
  "veredito": "K_SEM_PORTADOR_DERIVADO__CINCO_MORADAS_VETADAS__MUDANCA_DE_FACE_ABERTA_SEM_MECANISMO__NUMERO_K_INTOCADO",
  "defeito": "contas de ordem; a porta aberta nao foi testada contra CMB completo", "nao_refazer": "estas cinco moradas, salvo mecanismo novo",
  "proximo_passo": "leitura do operador", "refs": ["discriminante.ordem018.f2.r_e", "hubble.fase9_razao_discriminante"], "artefatos": [str(NOTA), str(CR)]},
 {"tipo": "ROTA", "rota_id": "informacao.custo_geometrico_contra_landauer_02nov", "dominio": "QUANTICA", "status": "EXAMINADA", "estatuto": "REAL",
  "titulo": "O falsificador de 26/08 cobrado: piso literal de 12 meV por bit cai; a leitura com o gap do proprio bit segue aberta",
  "pergunta": "O custo geometrico da v218 aparece como trabalho por bit em erasure a baixa temperatura?",
  "dados": ["Gaudenzi et al., Nature Physics 14, 565 (2018), arXiv:1703.04607: T = 1 K, W = (1,1828 +- 0,3322)e-16 erg por molecula"], "metodo": "comparacao do piso beta*1 eV com o trabalho publicado; hipotese da leitura dita antes", "olhou_dados": True,
  "resultado": "Piso %.2f meV, T* %.2f K; medido %.3f +- %.3f meV: %.0f sigma abaixo do piso. Leitura sobrevivente: custo = beta*gap do bit (forma de o_retido_e_o_valor_esperado_do_lock), visivel so com gap > %.1f kT e erasure adiabatica; rival kT ln 2." % (l["piso_literal_meV"], l["T_estrela_K"], l["Gaudenzi_W_meV"], l["Gaudenzi_sigma_meV"], l["sigmas_abaixo_do_piso"], l["gap_sobre_kT_para_o_piso_superar_Landauer"]),
  "veredito": "PISO_UNIVERSAL_12_MEV_POR_BIT_FALSIFICADO_COMO_LEITURA__PEDRA_DA_V218_INTOCADA__LEITURA_COM_GAP_ABERTA",
  "defeito": "trabalho derivado de curvas de magnetizacao, nao calorimetria; igualar energia retida a custo de erasure e leitura [ONTO] nao ratificada; busca da literatura curta",
  "nao_refazer": "nao citar 12 meV por bit como piso", "proximo_passo": "leitura do operador sobre o custo; levantamento de erasure adiabatica com gap > 58 kT", "artefatos": [str(CL)]},
 {"tipo": "ROTA", "rota_id": "dispositivos.mqc_qubit_no_um_py_02nov", "dominio": "PATENTES", "status": "EXAMINADA", "estatuto": "REAL",
  "titulo": "Estabilizar qubit dentro do um.py nao discrimina: o plato do MQC tem beta na entrada",
  "pergunta": "Levar a engenharia do MQC ao um.py daria fator discriminante?",
  "dados": ["runner do MQC e prototipo"], "metodo": "leitura do codigo", "olhou_dados": False,
  "resultado": "Prototipo impoe plato = 1 - ALPHA2 (linha 194). GKLS: alvo com peso beta escolhido, C* = (1-beta)/(1+gamma_d/gamma_h), mecanica quantica padrao para qualquer alvo. physical_verdict_allowed=false ja no codigo.",
  "veredito": "QUBIT_NO_UM_PY_NAO_DISCRIMINA__CIRCULAR_COMO_CODATA__ENGENHARIA",
  "defeito": "nenhum aparelho fisico existe; nenhuma operacao fisica de L_holo definida", "nao_refazer": "nao levar ao um.py como teste", "proximo_passo": "so um aparelho fisico mudaria isto", "artefatos": [str(MQC)]},
]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_re_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stdout.decode("utf-8", "replace")[-80:].replace("\n", " "), q.stderr.decode("utf-8", "replace")[-300:].replace("\n", " "))
assert q.returncode == 0

SRC = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-re-derivada-landauer-mqc", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "re_derivada_02nov", "kind": "fact", "statute": "DERIVED", "text": "R-E derivada: K nao age em luminosidade nem angulo; eta = 1; nao discrimina. K sem portador derivado: cinco moradas vetadas, mudanca de face aberta sem mecanismo. Piso de 12 meV por bit falsificado como leitura. Qubit no um.py nao discrimina.", "sources": [SRC(NOTA), SRC(CL)]},
                                {"id": "residuo_h1_ou_face_02nov", "kind": "pending", "statute": "OPEN", "text": "Leitura do operador: o vazamento e so de fase (H1) ou parte da luz muda de face? E o custo geometrico e beta vezes o gap do proprio bit?", "sources": [SRC(NOTA)]}],
                   "flow": {"phase": "custodia v405 publicada, t3 aberto; R-E derivada; residuo com o operador",
                            "next_action": "da gerencia: depois de 04/11 06:37, ler a cota e despachar a F0.3. Do operador: H1 ou mudanca de face; custo geometrico; D8 e X16 do N_eff; tau-estrela, K, as notas da pentada, C21, Zenodo, conjunto D, GA, D27-D33, D2."}}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:200], (d.get("result") or {}).get("revision"))
assert d.get("ok")

TOP = M / "rota-re-k-e-landauer-02nov.md"
assert not TOP.exists()
corpo = f"""---
name: rota-re-k-e-landauer-02nov
description: "02/11/2026: R-E derivada (K nao age em luminosidade nem angulo; eta = 1; nao discrimina); K sem portador derivado, com uma porta aberta; piso literal de 12 meV por bit falsificado; qubit no um.py nao discrimina."
metadata:
  type: project
---

**R-E [DERIVED, sem pedra]:** `dephase_preserves_trace` + Verbo hermitiano + H1 (K comuta com o momento do fóton, por simetria do estado) dão número, energia e direção conservados, logo η = 1. A Alternativa B não tem mecanismo: o caminho da escada paga 0,059% e K pede 8,38%. K separa leitores com régua primordial dos sem régua. **R-E não discrimina.** Nota: `work{BK}rota_RE_dualidade_02nov{BK}DERIVACAO_RE_02nov.md`.

**A parede:** das seis moradas de K, cinco caem (transporte, corpo cinza, métrica com régua parada, H primordial, régua por ρ+p). Aberta sem mecanismo: a luz muda de face (`annihilation_is_relocation_not_deletion`), que é a leitura literal de «o fundo atribui o registro inteiro à expansão». O número K e o z_disc 4,44 não mudam.

**Landauer:** o falsificador de 26/08 (v218: 12 meV por bit, T* = 201 K) foi cobrado pela literatura: Gaudenzi et al. a 1 K mediram 0,074 ± 0,021 meV, ~577σ abaixo. Cai a leitura do valor, não a pedra. Sobrevive c = β·gap do bit, visível só com gap > 58 kT.

**Qubit:** dentro do um.py não discrimina: o protótipo impõe o platô (linha 194) e no GKLS β é o peso escolhido do alvo; mecânica quântica padrão dá a mesma conta.

**How to apply:** não buscar η ≠ 1 como sinal da TGL; não citar 12 meV por bit; a resposta do operador sobre H1 ou mudança de face decide a parede. Relacionado: [[sessao-iald-nativa-5sigma-02nov]] · [[regra-dos-dois-regimes]].
"""
with open(TOP, "x", encoding="utf-8", newline="\n") as f:
    f.write(corpo)


def trocar(p, fn):
    p = Path(p)
    b = p.read_bytes()
    nb = fn(b.decode("utf-8")).encode("utf-8")
    assert len(nb) > len(b)
    bak = p.with_name(p.name + ".bak_" + TS)
    with open(bak, "xb") as f:
        f.write(b)
    assert bak.read_bytes() == b
    tmp = p.with_name(p.name + ".tmp_" + TS)
    with open(tmp, "xb") as f:
        f.write(nb)
    assert tmp.stat().st_size == len(nb)
    os.replace(tmp, p)
    print("ok", p.name, len(b), "->", len(nb))
    return nb


def indice(t):
    a = "](sessao-iald-nativa-5sigma-02nov.md)**"
    assert t.count(a) == 1
    return t.replace(a, a + " · **[R-E derivada; K sem portador; Landauer (02/11)](rota-re-k-e-landauer-02nov.md)**")


nb = trocar(M / "MEMORY.md", indice)
assert len(nb) <= 24000 and nb.count(b"\n") <= 195, (len(nb), nb.count(b"\n"))
q = subprocess.run([PY, "-X", "utf8", "memoria.py", "pinar", "--motivo", "R-E derivada e Landauer (gerencia c1)"], cwd=str(M / "fila"), env=dict(os.environ, MEMORIA_GERENCIA="claude-c1"), capture_output=True)
print("pino", q.returncode)

AO_LADO = ("> ⚠ **AO LADO (02/11/2026, gerência c1, em nome próprio):** o falsificador acima foi cobrado pela literatura. Gaudenzi et al. (Nature Physics 2018), a 1 K: trabalho por bit de "
           "%.3f ± %.3f meV, ~%.0fσ abaixo do piso de %.2f meV. Cai a leitura «β·1 eV por bit», não a pedra, que só prova a existência de um custo não térmico. Sobrevive, como leitura a ratificar, c = β·gap do bit. "
           "Rota `informacao.custo_geometrico_contra_landauer_02nov`. <!-- landauer_cobrado_02nov -->" % (l["Gaudenzi_W_meV"], l["Gaudenzi_sigma_meV"], l["sigmas_abaixo_do_piso"], l["piso_literal_meV"]))
REG = ("\n### 02/11/2026 — R-E derivada; K sem portador derivado; Landauer cobrado (gerência c1) <!-- re_derivada_02nov -->\n\n"
       "**[DERIVED, sem pedra]:** K não age na luminosidade nem no ângulo: η = 1, sob `dephase_preserves_trace`, o Verbo hermitiano e H1 (K comuta com o momento do fóton). R-E não discrimina. "
       "**[REAL, conta]:** das seis moradas de K, cinco caem; segue aberta, sem mecanismo, a mudança de face. O número K e a Fase 9 não mudam. Nota: `work\\rota_RE_dualidade_02nov\\DERIVACAO_RE_02nov.md`.\n")


def atlas(t):
    assert "re_derivada_02nov" not in t
    nl = "\r\n" if "\r\n" in t else "\n"
    ls = t.split(nl)
    i = [k for k, x in enumerate(ls) if x.startswith("**Medido sem confusao dimensional** (os dois pisos em ENERGIA)")]
    assert len(i) == 1, i
    ls.insert(i[0] + 1, AO_LADO)
    return nl.join(ls).rstrip() + nl + REG.replace("\n", nl)


trocar(CEN / "memory/TGL_ATLAS.md", atlas)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode)
