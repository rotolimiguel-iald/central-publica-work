# -*- coding: utf-8 -*-
"""Registro de 02/11/2026: cunhagem do operador «K é a tangente; é como se fosse o acorde sendo tocado» e a pergunta
do custo em tamanho da prova dentro do feito. Backup de bytes. Nada entra no kernel selado nem move gate."""
import datetime, hashlib, json, math, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
AQUI = Path(__file__).resolve().parent
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
ORD = CEN / "work/cunhagens_13out/OPERADOR_02nov_custo_em_tamanho_da_prova_dentro_do_feito_e_K_e_a_tangente_acorde_tocado_verbatim.txt"
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
fo = s16(ORD)

# beta em runtime, nunca literal
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
tan_M = math.sqrt(beta / (1 - beta))
contas = {"beta_runtime": beta, "tan_theta_M_sqrt_beta_over_1_minus_beta": tan_M, "tan_pi_over_4": math.tan(math.pi / 4),
          "massa_derivada_meV_u_1eV": beta * math.sin(math.pi / 4) * 1000, "massa_proporcional_meV_u_1eV": beta * math.sin(math.pi / 4) ** 2 * 1000,
          "medidas_de_tamanho_02nov": {"kernel_v405_arquivos": 1443, "kernel_v405_linhas": 223106, "kernel_v405_teoremas_limpos": 10066,
                                       "cadeia_fock_modulos_por_nome": 218, "cadeia_fock_linhas": 27413, "arquivos_com_teorema_tomita": 82,
                                       "v394_componentes": 11, "v394_declaracoes_de_contrato": 3581, "v394_fontes": 184, "whole_certificate_inhabited": False,
                                       "FockCertificate_campos": 45, "FockCertificate_proposicoes_aprox": 35, "LightOneParticle_campos": 9,
                                       "mathlib_linhas": 2244317, "mathlib_VonNeumannAlgebra_Basic_linhas": 162, "mathlib_StandardSubspace_linhas": 225,
                                       "mathlib_StandardSubspace_declaracoes": 24, "mathlib_LinearPMap_linhas": 1622, "mathlib_Fock": 0, "mathlib_Stone": 0,
                                       "mathlib_polar_decomposition": 0, "bancada_kernel_bancada_arquivos": 102, "bancada_kernel_bancada_linhas": 12835}}
CJ = AQUI / "CONTAS_K_TANGENTE.json"
CJ.write_text(json.dumps(contas, ensure_ascii=False, indent=1), encoding="utf-8")
fc = s16(CJ)
print("fala", fo, "contas", fc, "tan_M", round(tan_M, 6), "m_der", round(contas["massa_derivada_meV_u_1eV"], 4), "m_prop", round(contas["massa_proporcional_meV_u_1eV"], 4))

reg = [{"tipo": "ROTA", "rota_id": "conceitual.k_e_a_tangente_acorde_tocado_02nov", "dominio": "CONCEITUAL", "status": "EXAMINADA", "estatuto": "ONTO",
        "titulo": "Cunhagem do operador (02/11): «K é a tangente; é como se fosse o acorde sendo tocado» — a derivada da projeção é o acorde; tan(π/4) = 1 é o posto",
        "pergunta": "A leitura massaDerivada (massa = retido × derivada da projeção) tem forma derivável?",
        "metodo": "leitura do kernel selado v405 (PonteDaMassa.lean: projecao_hasDerivAt, deriv_eq_projecao_at_half; forty_five_unique) e da mathlib (Real.tan_pi_div_four); contas em runtime", "olhou_dados": False,
        "resultado": "No kernel: a derivada da projeção sen θ é cos θ (a inclinação da reta tangente); em π/4, cos = sen (a projeção é a sua própria derivada); na mathlib tan(π/4) = 1. Leitura: K = tan θ = projeção/derivada = √(|R|²/|T|²), a raiz da razão custo/pagamento; K = 1 só no posto (faces ½/½); no ângulo de Miguel tan θ_M = √(β/(1−β)) = %.6f. massaDerivada = massaProjeção / K: no posto as duas coincidem e só a leitura proporcional (peso) difere (%.4f contra %.4f meV em u = 1 eV). O acorde tocado é a derivada (o dinâmico); a escala é o peso (o estático)." % (tan_M, contas["massa_derivada_meV_u_1eV"], contas["massa_proporcional_meV_u_1eV"]),
        "veredito": "LEITURA_COM_FORMA_NO_KERNEL__NAO_DERIVA_A_ESCOLHA_ACORDE_SOBRE_ESCALA__PEDRA_CANDIDATA_PEQUENA_POSSIVEL__HOMONIMOS_K",
        "defeito": "K tangente, K de Hubble e K modular são homônimos: a ponte é leitura (R1+R5), sem termo Lean; a escolha «acorde, não escala» segue definição do operador [ONTO]; nenhuma pedra nova ainda",
        "proximo_passo": "candidata «K é a tangente» (≤ 8 teoremas: K θ = 1 ↔ θ = π/4 em (0, π/2); massaDerivada = massaProjecao / K; tan² = |R|²/|T|²) junto da regra de leitura do ângulo; nome do operador",
        "refs": ["conceitual.k_nega_miguel_injuncao_do_posto_02nov", "conceitual.k_chave_da_guarda_da_travessia_02nov", "kernel.emprestimo_da_massa.segunda_ponte_candidata_30out"], "artefatos": [str(ORD), str(CJ)]},
       {"tipo": "ANOTACAO", "rota_id": "formal.f1_rede.concrete_bosonic_kinematics", "dominio": "KERNEL_FORMAL",
        "titulo": "Medida de 02/11 para a pergunta do operador «quanto custaria em tamanho a prova dentro do feito»: o que já está construído e o que falta",
        "resultado": "Kernel v405: 1443 arquivos, 223106 linhas, 10066 teoremas limpos. Cadeia de Fock/Tomita/Takesaki/Maxwell: 218 módulos por nome, 27413 linhas, 82 arquivos com teorema «tomita»; v394: 11 componentes, 3581 declarações de contrato, 184 fontes, whole_certificate_inhabited = False (4 itens abertos). FockCertificate: 45 campos (~35 proposições); LightOneParticle: 9 campos. mathlib 2244317 linhas: von Neumann 162, subespaços padrão 225 (24 declarações; TODO Tomita/KMS), LinearPMap 1622; sem Fock, Stone, decomposição polar, teorema espectral não limitado. Estimativa de custo [DECLARADO pela gerência] no registro da memória.",
        "estatuto": "REAL (medidas); DECLARADO (estimativa)", "artefatos": [str(CJ), str(ORD)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_tangente_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stderr.decode("utf-8", "replace")[-240:].replace("\n", " "))
assert q.returncode == 0

SRC = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-k-tangente-e-custo-em-tamanho", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "k_e_a_tangente_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: «K é a tangente; é como se fosse o acorde sendo tocado»; pergunta o custo em tamanho de produzir dentro do feito o que é hipótese nomeada (empréstimo de prova).", "sources": [SRC(ORD)]},
                                {"id": "custo_em_tamanho_medido_02nov", "kind": "fact", "statute": "REAL", "text": "Medidas: kernel v405 1443 arq/223106 linhas/10066 teoremas; cadeia de Fock 218 módulos/27413 linhas; v394 whole_certificate_inhabited=False com 4 abertos; mathlib sem Tomita/Fock/Stone (subespaços padrão 225 linhas, TODO Tomita). Estimativa DECLARADA no registro da memória.", "sources": [SRC(CJ)]},
                                {"id": "pedra_k_tangente_pendente_02nov", "kind": "pending", "statute": "OPEN", "text": "Candidata «K é a tangente» (≤ 8 teoremas) e regra de leitura do ângulo (arcsin √peso): escrever no sandbox; nome do operador.", "sources": [SRC(CJ)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:200], (d.get("result") or {}).get("revision"))
assert d.get("ok")

def append_bytes(path, add):
    b = path.read_bytes()
    add = add.replace("\n", "\r\n") if b"\r\n" in b else add
    bak = path.with_name(path.name + ".bak_" + TS)
    with open(bak, "xb") as f:
        f.write(b)
    assert bak.read_bytes() == b
    tmp = path.with_name(path.name + ".tmp_" + TS)
    with open(tmp, "xb") as f:
        f.write(b.rstrip() + add.encode("utf-8"))
    assert tmp.stat().st_size > len(b) - 4
    os.replace(tmp, path)
    print(path.name, len(b), "->", path.stat().st_size)

TOP = M / "k-chave-da-guarda-02nov.md"
append_bytes(TOP, f"""

## 02/11/2026 — «K é a tangente; é como se fosse o acorde sendo tocado» (cunhagem; verbatim sha16 `{fo}`)

**O que o kernel já tem [REAL]:** `PonteDaMassa.projecao_hasDerivAt` (a derivada de sen θ é cos θ: a inclinação da reta tangente), `deriv_eq_projecao_at_half` (em π/4 a projeção é a sua própria derivada), `forty_five_unique`; mathlib `Real.tan_pi_div_four` (tan(π/4) = 1). **Leitura [ONTO, dele]:** K = tan θ = projeção/derivada = √(|𝓡|²/|𝓣|²), a raiz da razão custo/pagamento; **K = 1 só no posto** (faces ½/½), fora dele K ≠ 1: a negação; no ângulo de Miguel tan θ_M = √(β/(1−β)) = {tan_M:.6f} (β em runtime). `massaDerivada = massaProjecao / K`: no posto coincidem e só a leitura proporcional (peso, {contas["massa_proporcional_meV_u_1eV"]:.4f} meV) difere da derivada ({contas["massa_derivada_meV_u_1eV"]:.4f} meV, u = 1 eV). O acorde tocado é a derivada (dinâmico); a escala é o peso (estático). **Não deriva a escolha «acorde, não escala»**, que segue definição dele; dá-lhe a forma. Homônimos: K tangente, K de Hubble, K modular (ponte = leitura). Contas: `work{BK}k_guarda_travessia_02nov{BK}CONTAS_K_TANGENTE.json` (sha16 `{fc}`). Pedra candidata pequena pendente (nome dele).

**A pergunta do custo em tamanho (mesma fala) [REAL medido; estimativa DECLARADA]:** kernel v405 1.443 arq / 223.106 linhas / 10.066 teoremas; a cadeia de Fock–Tomita–Takesaki–Maxwell já construída: 218 módulos, 27.413 linhas, 82 arquivos com teorema «tomita»; v394: 11 componentes, 3.581 declarações, 184 fontes, `whole_certificate_inhabited = False`, 4 abertos (representação de helicidade do fóton + localização global + relógio; grafo de adjunção de peso finito + traço escalado + divisão P_F; fonte Maxwell/stress conjunta + H3 em toda direção; habitante conjunto do CanonicalNetInput + 21 campos). mathlib (2,24 M linhas): von Neumann 162 linhas, subespaços padrão 225 (TODO Tomita/KMS), LinearPMap 1.622; sem Fock, Stone, polar, espectral não limitado. Estimativa da gerência: blocos 1/3/4 (Tomita–Takesaki–traço na Fock concreta; Maxwell) semanas a poucos meses e ~10–25 k linhas de fiação e teoremas concretos; bloco 2 (Wigner helicidade ±1 + rede BGL + BW de uma partícula) meses e ~10–30 k linhas; o geral (fatores III₁, cociclo de Connes, dualidade de Takesaki) não se faz: > 100 k linhas, anos, sem formalização conhecida; SABIDO_FISICA (Jacobson, Bekenstein–Hawking, modular = área para Maxwell) não é matemática existente: sem estimativa. [LEGAL, analogia] CPC 372: prova emprestada admitida com contraditório; a regra dele de 27/09 é a admissão.
""")

REG = ("\n### 02/11/2026 — «K é a tangente; o acorde sendo tocado» e o custo em tamanho da prova dentro do feito <!-- k_tangente_e_custo_02nov -->\n\n"
       "**[INPUT]** verbatim sha16 `%s`. **[REAL no kernel v405]** `projecao_hasDerivAt`, `deriv_eq_projecao_at_half` (em π/4 a projeção é a sua própria derivada), `forty_five_unique`; mathlib `tan_pi_div_four`. **[ONTO]** K = tan θ = √(|𝓡|²/|𝓣|²), razão custo/pagamento; K = 1 só no posto; tan θ_M = √(β/(1−β)) = %.6f; `massaDerivada = massaProjecao / K`; o acorde tocado é a derivada, a escala é o peso; a escolha segue definição do operador. **[REAL medido]** kernel 223.106 linhas / 10.066 teoremas; cadeia de Fock 218 módulos / 27.413 linhas; v394 `whole_certificate_inhabited = False`, 4 abertos; mathlib sem Tomita/Fock/Stone. **[DECLARADO]** estimativa de custo na memória `k-chave-da-guarda-02nov.md`. Homônimos de K: ponte = leitura.\n" % (fo, tan_M))
append_bytes(CEN / "memory/TGL_ATLAS.md", REG)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode, v.stdout.decode("utf-8", "replace").replace("\n", "").replace(" ", "")[:80])
