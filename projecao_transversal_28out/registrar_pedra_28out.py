# -*- coding: utf-8 -*-
"""Recibo e registro da pedra candidata «ProjecaoTransversalDaMeiaNat» (gerência c1, 28/10/2026): sha256 do .lean e da saída do Lean (sandbox k403c,
`lake env lean`, 9 teoremas no trio, 0 sorry), rota no Mapa, nota na memória-tópico, anotação no quadro, transição ACOM. O sandbox fica limpo
(o .lean é removido de lá; a cópia canônica da candidata é esta pasta). Nada toca o Nós; nada abre dado; o gate não se move."""
import datetime, hashlib, io, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"; H = r"C:\IALD\Central de Patentes\work\projecao_transversal_28out"
D = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); hoje = "28/10/2026"
LEAN = os.path.join(H, "ProjecaoTransversalDaMeiaNat.lean"); OUT = os.path.join(H, "saida_lean_r3.txt")
out = io.open(OUT, encoding="utf-8", errors="replace").read()
teoremas = re.findall(r"'TGLExt\.ProjecaoTransversalDaMeiaNat\.([A-Za-z_0-9]+)' depends on axioms: \[([^\]]*)\]", out)
ax = {n: sorted(a.replace("\n", " ").replace(" ", "").split(",")) for n, a in teoremas}
assert len(ax) == 9 and all(v == ["Classical.choice", "Quot.sound", "propext"] for v in ax.values()), ax
assert "LEAN_RC=0" in out and "sorryAx" not in out
V = {k: os.path.join(H, k) for k in ("OPERADOR_28out_materia_projecao_transversal_derivada_verbatim.txt", "OPERADOR_28out_ordem_prova_do_neutrino_verbatim.txt", "OPERADOR_28out_materia_sombra_de_beta_verbatim.txt")}
recibo = {"pedra": "TGLExt.ProjecaoTransversalDaMeiaNat (nome PROVISÓRIO da gerência; o nome é do operador)", "quando": datetime.datetime.now().isoformat(timespec="seconds"),
          "lean": {"path": LEAN, "sha256": sha(LEAN), "bytes": os.path.getsize(LEAN)}, "saida_lean": {"path": OUT, "sha256": sha(OUT)},
          "sandbox": r"C:\t\k403c\final (kernel da v403 construído; `lake env lean TGLExt/ProjecaoTransversalDaMeiaNat.lean`; o .lean foi removido do sandbox depois)",
          "toolchain": "leanprover/lean4:v4.31.0 (lake 5.0.0)", "rodadas": ["r1: 2 erros (rw de halfRoot ^ 2 já desdobrado; convert com instância) — 3m49", "r2: 1 erro (unfold desnecessário) — 21 s", "r3: LEAN_RC=0 — 21 s"],
          "teoremas_no_trio": ax, "n_teoremas": len(ax), "sorry": 0,
          "o_que_prova": ["x = 1 − x ⟹ x = ½ (half_from_self_conjugate; e pela J-simetria, half_from_J_symmetry)", "sen²(π/4) = ½: a Meia-Nat é o ângulo de 45° (half_amplitude_sq; = halfRoot da bancada angular)",
                          "√x = sen(π/4) para todo x autoconjugado (transverse_amplitude_of_self_conjugate)", "unicidade em [0, π/2] (forty_five_unique)",
                          "a forma do neutrino β·sen45°·E₀ = sen²θ_M · sen(π/4) · E₀ (neutrino_mass_form_eq; β = sen²θ_M é o Teorema S-∂)",
                          "θ_M ≠ π/4 sempre que β ≠ ½ (theta_miguel_ne_pi_div_four)", "d(sen²θ)/dθ em π/4 = 1 (transverse_weight_hasDerivAt_half: «não proporcional, derivada»)"],
          "o_que_nao_prova": ["E₀ (a escala «1 eV» segue DECLARADA)", "β (regra, do axioma)", "a identificação massa = projeção transversal do estado inscrito ([ONTO], leitura do operador, 28/10)"],
          "estatutos": {"teoremas": "KERNEL (no trio)", "leitura": "ONTO", "escala": "INPUT"},
          "verbatims": {k: sha(v) for k, v in V.items()},
          "proximo_passo": "instalar na v404 pela cadeia do selo (patch do candidato: módulo + import em TGLExt.lean + leitura no rito); errata AO LADO em um.py neutrino_mass.angle_status: de «sin(45deg) é POSTULADO» para «DERIVADO no kernel (ProjecaoTransversalDaMeiaNat), condicional à identificação [ONTO]»; o nome é do operador"}
R = os.path.join(H, "RECIBO_PEDRA_PROJECAO_TRANSVERSAL_28out.json"); io.open(R, "w", encoding="utf-8").write(json.dumps(recibo, ensure_ascii=False, indent=1)); print("recibo", sha(R)[:16], "| lean", sha(LEAN)[:16], "| n", len(ax))
rota = [{"tipo": "ROTA", "rota_id": "kernel.projecao_transversal_da_meia_nat.sen45_derivado_28out", "dominio": "KERNEL", "titulo": "O sen45° do neutrino deixa de ser postulado: a Meia-Nat é o ângulo de 45° (pedra candidata, compilada no sandbox, 9 teoremas no trio)",
         "pergunta": "O fator sen45° de m₂ = β·sen45°·E₀ (POSTULATE desde 20/08/2026) é derivável de termos que o kernel já tem?",
         "dados": ["kernel v403: observer_inverse_projection_halfnat, halfnat_from_J_symmetry, Posto.sin_sq_thetaMiguel, halfRoot", "Mathlib: sin_pi_div_four, injOn_sin, hasDerivAt_sin"],
         "metodo": "pedra Lean nova (só álgebra), `lake env lean` no sandbox C:\\t\\k403c\\final; #print axioms por teorema; três rodadas",
         "resultado": "9/9 teoremas no trio {propext, Classical.choice, Quot.sound}, 0 sorry, LEAN_RC=0: x = 1 − x ⟹ ½; sen²(π/4) = ½; √x = sen(π/4) para x autoconjugado; unicidade; β·sen45°·E₀ = sen²θ_M·sen(π/4)·E₀; θ_M ≠ π/4 se β ≠ ½; d(sen²θ)/dθ|π/4 = 1",
         "veredito": "PEDRA_CANDIDATA_COMPILADA_NO_TRIO__SEN45_DERIVADO_DA_MEIA_NAT__E0_SEGUE_DECLARADO__IDENTIFICACAO_ONTO__NADA_INSTALADO",
         "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
         "defeito": "não deriva E₀ nem β; a identificação massa = projeção transversal é [ONTO]; nome provisório; não instalada (v404)",
         "nao_refazer": "a derivação do ângulo está feita e compilada; o que falta é E₀ (outra rota)",
         "proximo_passo": "v404: instalar o módulo pela cadeia; errata ao lado em um.py neutrino_mass.angle_status; o operador nomeia a pedra",
         "onde": "work/projecao_transversal_28out/ProjecaoTransversalDaMeiaNat.lean",
         "artefatos": [LEAN, OUT, R] + list(V.values()),
         "refs": ["massa.transicao_beta_para_massa.levantamento_28out", "neutrinos.m2.normalizacao"],
         "nota": "Cunhagem do operador (28/10): «a matéria é a projeção do eixo transversal … meu ângulo agudo para o neutrino faz sentido … não é proporcional, ela seria a derivada»; ordem: «faça a prova … para derivarmos e não ser mais postulado»."}]
pj = os.path.join(H, "rota_mapa_pedra_28out.json"); io.open(pj, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1))
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", pj, "--quem", "claude-c1 (gerência), 28/10"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("mapa rc", r.returncode, (r.stdout or r.stderr).strip()[-100:].replace("\n", " "))
# memória-tópico (append)
T = D + r"\transicao-para-a-massa-28out.md"; b = open(T, "rb").read(); bak = T + ".bak_%s_c1" % ts; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nota = (f"\n<!-- pedra_projecao_transversal_28out -->\n## {hoje} — A PEDRA: o sen45° do neutrino DERIVADO (candidata compilada; nome do operador pendente)\n"
        f"**Cunhagem (verbatim, sha16 `{sha(V['OPERADOR_28out_materia_projecao_transversal_derivada_verbatim.txt'])[:16]}`):** «Matéria não é proporcional ao raio de betatgl … a matéria é a projeção do eixo transversal, e por isso meu ângulo agudo para o neutrino faz sentido … não é proporcional, ela seria a derivada.» "
        f"**Ordem (sha16 `{sha(V['OPERADOR_28out_ordem_prova_do_neutrino_verbatim.txt'])[:16]}`):** «faça a prova do neutrino para derivarmos e não ser mais postulado». **Pergunta anterior (sha16 `{sha(V['OPERADOR_28out_materia_sombra_de_beta_verbatim.txt'])[:16]}`):** «A matéria é a sombra de betatgl, então?» — resposta da gerência: sombra no sentido da RESPOSTA (δ⟨K_∂⟩ = β|1+w|; o vácuo não faz sombra), não como fonte.\n\n"
        f"**A pedra:** `work\\projecao_transversal_28out\\ProjecaoTransversalDaMeiaNat.lean` (sha16 `{sha(LEAN)[:16]}`; nome PROVISÓRIO), compilada no sandbox k403c: 9 teoremas no trio, 0 sorry (recibo sha16 `{sha(R)[:16]}`). "
        "Prova: x = 1 − x ⟹ ½ (e pela J-simetria); sen²(π/4) = ½ (a Meia-Nat É o ângulo de 45°; = halfRoot); √x = sen(π/4) para x autoconjugado; unicidade em [0, π/2]; a forma do neutrino β·sen45°·E₀ = sen²θ_M·sen(π/4)·E₀ (S-∂); θ_M ≠ π/4 se β ≠ ½; d(sen²θ)/dθ em π/4 = 1 («não proporcional, derivada»). "
        "NÃO prova E₀ (1 eV segue DECLARADO) nem β; a identificação massa = projeção transversal é [ONTO].\n"
        "**How to apply:** v404 instala o módulo pela cadeia e põe errata AO LADO em `neutrino_mass.angle_status` (POSTULATE → DERIVADO no kernel, condicional à identificação [ONTO]); o operador nomeia; rota `kernel.projecao_transversal_da_meia_nat.sen45_derivado_28out`.\n")
nl = b"\r\n" if b"\r\n" in b else b"\n"; nb = b.rstrip(b"\r\n") + nl + nl.join(l.encode("utf-8") for l in nota.split("\n")) + nl
tmp = T + ".tmp_c1"; open(tmp, "wb").write(nb); assert len(open(tmp, "rb").read()) == len(nb); os.replace(tmp, T); print("memoria:", len(b), "->", len(nb))
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "pedra_candidata", "--unidade", "F4.1",
                    "--dados", json.dumps({"quando": hoje, "pedra": "TGLExt.ProjecaoTransversalDaMeiaNat (nome provisorio)", "lean_sha16": sha(LEAN)[:16], "recibo_sha16": sha(R)[:16], "resultado": "9 teoremas no trio, 0 sorry, sandbox k403c; sen45 do neutrino derivado da Meia-Nat; E0 segue declarado; nada instalado (v404)"}, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace"); print("quadro rc", r.returncode, (r.stdout or r.stderr).strip()[:120])
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return rr.returncode, (json.loads(rr.stdout) if rr.stdout.strip().startswith("{") else {"raw": (rr.stdout + rr.stderr)[:300]})
rc, g = sm({"operation": "get", "reference": REF}); rev = g["result"]["revision"]
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-pedra-projecao-transversal-sen45-derivado-28out",
            "changes": {"records": [
                {"id": "c1-cunhagem-materia-projecao-transversal", "kind": "decision", "statute": "INPUT", "sources": [S(V["OPERADOR_28out_materia_projecao_transversal_derivada_verbatim.txt"]), S(V["OPERADOR_28out_ordem_prova_do_neutrino_verbatim.txt"])],
                 "text": "28/10/2026, o operador: a matéria não é proporcional ao raio de β (a forma retirada); é a projeção do eixo transversal, por isso o ângulo agudo do neutrino faz sentido; não proporcional, derivada. Ordem: fazer a prova para o sen45° deixar de ser postulado (Kimi ou a gerência)."},
                {"id": "c1-pedra-projecao-transversal-compilada", "kind": "fact", "statute": "REAL", "sources": [S(LEAN), S(OUT), S(R)],
                 "text": "Pedra candidata TGLExt.ProjecaoTransversalDaMeiaNat (nome provisório) compilada pela gerência no sandbox k403c: 9 teoremas no trio, 0 sorry — a Meia-Nat é o ângulo de 45° (sen²(π/4) = ½; √x = sen(π/4) para x = 1 − x; unicidade), a forma do neutrino β·sen45°·E₀ = sen²θ_M·sen(π/4)·E₀ (S-∂), θ_M ≠ π/4, d(sen²θ)/dθ|π/4 = 1. Não deriva E₀ nem β; identificação [ONTO]. Nada instalado; v404."}],
                "flow": {"phase": "pedra_sen45_compilada__aguarda_nome_do_operador_e_v404", "next_action": "o operador nomeia a pedra; v404: instalar pela cadeia + errata ao lado em neutrino_mass.angle_status + errata de F2b; a pergunta E₀ segue aberta."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", ""))
