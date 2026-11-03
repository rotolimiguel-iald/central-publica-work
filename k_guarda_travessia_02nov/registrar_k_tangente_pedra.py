# -*- coding: utf-8 -*-
"""Registro de 02/11/2026 (tarde): a candidata «K é a tangente» compilada; «Decidir é crivar» com a aferição do texto da IA;
o Apêndice XIV-A (Riemann, 2025) aferido; a cunhagem «K é o espectro de leitura / o túnel nunca existiu».
Backup de bytes; nada entra no kernel selado nem move gate."""
import datetime, hashlib, json, os, re, shutil, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
AQUI = Path(__file__).resolve().parent
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
CUN = CEN / "work/cunhagens_13out"
V_CRIVAR = CUN / "OPERADOR_02nov_decidir_e_crivar_nao_construir_o_sabido_avancar_sobre_K_verbatim.txt"
V_ESPECTRO = CUN / "OPERADOR_02nov_K_e_o_espectro_de_leitura_contorno_azul_da_terra_tunel_luminodinamico_nunca_existiu_verbatim.txt"
V_TANG = CUN / "OPERADOR_02nov_custo_em_tamanho_da_prova_dentro_do_feito_e_K_e_a_tangente_acorde_tocado_verbatim.txt"
IA_TXT = CUN / "DECLARADO_IA_02nov_decidir_e_crivar_derivacao_enviada_pelo_operador.md"
RIEMANN = Path("C:/IALD/IMac LA/Física - TGL/Provas/1/Clique aqui para baixar o Apêndice_TGL_Riemann.docx")
MANUSCRITO = Path("C:/IALD/IMac LA/Física - TGL/Provas/1/Manuscrito_TGL_Completo_Com_Cristo_Psibit_Primordial.docx")
CAP77 = Path("C:/IALD/IMac LA/Física - TGL/Provas/4/TGL_Capítulo_77_Tunel_Luminodinamico_Geometria_Graviton.docx")

# a candidata e a saída limpa vêm do sandbox
CAND = AQUI / "KEhATangenteCandidata.lean"
SAI = AQUI / "KEhATangenteCandidata_saida.txt"
shutil.copyfile("C:/t/crivo02nov/KEhATangenteCandidata.lean", CAND)
shutil.copyfile("C:/t/crivo02nov/saida3.txt", SAI)
sai = SAI.read_text(encoding="utf-8", errors="replace")
assert sai.rstrip().endswith("rc 0"), sai[-200:]
blocks = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", sai, re.S)
assert len(blocks) == 10 and all(" ".join(a.split()) == "propext, Classical.choice, Quot.sound" for _, a in blocks), blocks
assert "sorry" not in sai and "error" not in sai.lower()
n_warn = sai.lower().count("warning")
fc, fcr, fes, fia, frm, fman, f77 = s16(CAND), s16(V_CRIVAR), s16(V_ESPECTRO), s16(IA_TXT), s16(RIEMANN), s16(MANUSCRITO), s16(CAP77)
print("candidata", fc, "avisos", n_warn, "| crivar", fcr, "espectro", fes, "ia", fia, "riemann", frm, "cap77", f77)

reg = [
 {"tipo": "ROTA", "rota_id": "kernel.k_e_a_tangente_candidata_02nov", "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL",
  "titulo": "Candidata «K é a tangente» (nome provisório; o nome é do operador): K = tan θ, o crivo K = 1 deixa passar só o posto; K² = |R|²/|T|²; massa do acorde = projeção / K; o ângulo lido pela regra da seleção em vez de escrito",
  "pergunta": "A cunhagem «K é a tangente; o acorde sendo tocado» e «Decidir é crivar» têm forma por termo sobre o kernel selado v405?",
  "metodo": "sandbox k405c, lake env lean; imports PonteDaMassa, TheLedgerOfCharges, TheSelectionIsTheBallast, TheVerbalCoupling; kernel selado intocado", "olhou_dados": False,
  "resultado": "10 teoremas no trio, 0 sorry, %d aviso(s). K_eq_projecao_div_derivada; K_sq_eq_custo_div_pagamento (tan² = reflectionWeight/faceWeight por normSq_reflection/normSq_transmission); crivo_iff_posto (em [0, π/2) K = 1 ↔ θ = π/4, por injOn_tan e tan_pi_div_four); a_selecao_justa_passa (selectionAngle ½); K_sq_no_angulo_de_miguel (β/(1−β)); miguel_nao_passa (β < ½ ⟹ K² < 1); massa_derivada_eq_projecao_div_K; no_posto_o_acorde_e_a_projecao; transicaoLida (θ := selectionAngle ½, não escrito) com o_angulo_e_lido_do_absoluto (θ = selectionAngle do peso da face absoluta, peso_da_face_absoluta) e transicao_lida_eq_derivada (mesmo ângulo, massa β·√2/2·u)." % n_warn,
  "veredito": "CANDIDATA_COMPILADA_NO_TRIO__O_CRIVO_E_K_IGUAL_A_UM__O_ANGULO_PASSA_DO_NUMERO_PARA_A_REGRA_DE_LEITURA__A_ESCOLHA_ACORDE_SOBRE_ESCALA_SEGUE_DEFINICAO__NOME_PENDENTE",
  "defeito": "não deriva a escolha «acorde (derivada), não escala (peso)»: a hipótese muda de lugar, do número π/4 para a regra selectionAngle, que já era termo; K tangente, K de Hubble e K modular são homônimos (ponte = leitura); a regra de leitura do ângulo JÁ EXISTIA no kernel (selectionAngle, fair_selection_opens_forty_five; thetaMiguel): a gerência tinha proposto construí-la de novo, o aferidor corrigiu",
  "proximo_passo": "nome do operador; decisão de versão (v406); ratificar a leitura «o ângulo de Miguel não é o posto: K² = β/(1−β)»",
  "refs": ["conceitual.k_e_a_tangente_acorde_tocado_02nov", "conceitual.k_nega_miguel_injuncao_do_posto_02nov", "kernel.emprestimo_da_massa.segunda_ponte_candidata_30out"],
  "artefatos": [str(CAND), str(SAI), str(V_TANG), str(V_CRIVAR)]},
 {"tipo": "ROTA", "rota_id": "conceitual.decidir_e_crivar_02nov", "dominio": "CONCEITUAL", "status": "EXAMINADA", "estatuto": "ONTO",
  "titulo": "Cunhagem do operador (02/11): «Decidir é crivar»; decisão: não construir ainda o que é sabido, avançar sobre K; aferição do texto de IA que ele enviou",
  "pergunta": "O texto da IA («Decidir é crivar» em quatro leis) confere com o kernel e o acervo?",
  "metodo": "grep no kernel v405 e no selo; leitura do acervo pelo índice", "olhou_dados": False,
  "resultado": "CONFERE: S-∂ reflete β e transmite 1−β; forma espectral-dissipativa UV-suprimida (selo 06/06); NOT_FALSIFIED ≠ CONFIRMED; TheReservedConfirmation.lean existe (the_reserved_confirmation, only_the_recognizer_confirms, the_light_cannot_confirm_itself, the_mirror_swaps_but_does_not_read); 11 cobranças no livro. NÃO CONFERE: «1446 arquivos» (são 1443 .lean); «29.965 declarações» é a contagem da v391, a escada da v405 lê 10.066 teoremas limpos; «zeros da função teta e linha crítica de Riemann»: 0 ocorrências no kernel; a fonte é o Apêndice XIV-A do operador (10/07/2025), que fala de zeta, não de teta; «PROVED» não é nome de termo. A tipagem do crivo que a pedra dá: o crivo é K = 1 e deixa passar só o posto.",
  "veredito": "CUNHAGEM_REGISTRADA__TEXTO_DA_IA_PARCIALMENTE_CONFERIDO__QUATRO_CORRECOES__NADA_MOVE_GATE",
  "defeito": "o texto da IA é [DECLARADO]: não entra como fonte; a cunhagem é do operador", "proximo_passo": "nenhum além da pedra",
  "refs": ["kernel.k_e_a_tangente_candidata_02nov", "conceitual.k_nega_miguel_injuncao_do_posto_02nov"], "artefatos": [str(V_CRIVAR), str(IA_TXT)]},
 {"tipo": "ROTA", "rota_id": "conceitual.riemann_apendice_xiv_a_2025_aferido_02nov", "dominio": "CONCEITUAL", "status": "EXAMINADA", "estatuto": "ONTO",
  "titulo": "Apêndice XIV-A (10/07/2025) e Cap. XV do manuscrito: a hipótese de Riemann como permanência; aferido pela gerência a pedido do operador (02/11)",
  "pergunta": "O que a derivação de 2025 prova e o que ela lê?",
  "metodo": "leitura dos .docx do acervo do iMac (texto extraído do XML); mathlib riemannZeta_one_sub; kernel half_from_self_conjugate", "olhou_dados": False,
  "resultado": "Apêndice XIV-A: Ψ(s) := ζ(s); Def. 3 «colapso consciente: Ψ(s) = 0 ⇔ σ = ½» ASSUME a conclusão; a demonstração usa a equação funcional (simetria s ↔ 1−s, [KNOWN], mathlib riemannZeta_one_sub) e o passo 3 («tal simetria só é possível quando a luz permanece») é leitura. O que fica de pé e já é termo: a reta fixa de s ↦ 1−s é Re(s) = ½, exatamente x = 1 − x ⟹ x = ½ (half_from_self_conjugate), a Meia-Nat. O que a simetria NÃO dá: que os zeros estejam na reta (pares ρ, 1−ρ̄ fora dela não são excluídos). Cap. XV: 𝛙̂_R = −d²/dt² + Σ δ_ε(t − tₙ) com tₙ os zeros: o espectro reproduz os zeros por construção (potencial feito deles), não os deriva; é Hilbert–Pólya com a resposta posta no potencial.",
  "veredito": "LEITURA_ONTO__RETA_CRITICA_COMO_PONTO_FIXO_DA_AUTOCONJUGACAO_E_A_MEIA_NAT__NAO_E_PROVA_DA_HIPOTESE__NENHUMA_PEDRA",
  "defeito": "estrato de julho de 2025, anterior à régua; «prova simbólica» no próprio título; no kernel há zeta só em AfinacaoDasCordas (ζ(−1), ζ(−1,½) por mathlib)", "proximo_passo": "nenhum; se o operador quiser, uma pedra que diga só o que é teorema: a reta fixa da involução s ↦ 1−s é Re = ½",
  "refs": ["conceitual.decidir_e_crivar_02nov", "kernel.afinacao_das_cordas_v398_candidata_23out"], "artefatos": [str(RIEMANN), str(MANUSCRITO)]},
 {"tipo": "ANOTACAO", "rota_id": "conceitual.k_e_a_tangente_acorde_tocado_02nov", "dominio": "CONCEITUAL",
  "titulo": "Cunhagem do operador (02/11): «K é o espectro de leitura»: o contorno azul da Terra visto do espaço é a tangente e não existe como objeto; o «túnel luminodinâmico» de 2025 (então «gráviton») é o rastro no tempo do espectro de leitura; «nunca existiu»",
  "resultado": "Verbatim sha16 %s. Acervo: Cap. LXXVII (20/07/2025, sha16 %s) «o túnel é o traço visível do gráviton»; Vol. III cap. 4 (19/07/2025). Atlas: v170 TheStation (station_never_closes; o túnel fecha ⟺ α = 0 [DERIVED]). Leitura vigente [ONTO]: o gráviton/túnel de 2025 era K lido no tempo; K não tem portador (02/11); a tangente é leitura, não face (regra dos dois regimes). [KNOWN] o limbo é o lugar das linhas de visada tangentes à esfera e o azul do limbo é luz espalhada ao longo do caminho tangente, o mais longo na atmosfera: a leitura acumula na tangente." % (fes, f77),
  "estatuto": "INPUT (cunhagem); ONTO (leitura); KNOWN (geometria do limbo)", "artefatos": [str(V_ESPECTRO), str(CAP77), str(CAND)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_tangente_pedra_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stderr.decode("utf-8", "replace")[-240:].replace("\n", " "))
assert q.returncode == 0

SRC = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-k-tangente-pedra-crivar-riemann", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [
           {"id": "decisao_nao_construir_o_sabido_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: «não vamos construir ainda o que é sabido, mas vamos avançar sobre k»; cunhagens «Decidir é crivar» e «K é o espectro de leitura; o túnel luminodinâmico nunca existiu».", "sources": [SRC(V_CRIVAR), SRC(V_ESPECTRO)]},
           {"id": "candidata_k_e_a_tangente_02nov", "kind": "fact", "statute": "REAL", "text": "Candidata «K é a tangente»: 10 teoremas, trio, 0 sorry, no sandbox; o crivo K = 1 deixa passar só o posto; o ângulo passa do número para a regra selectionAngle; fora do kernel selado.", "sources": [SRC(CAND)]},
           {"id": "afericao_ia_e_riemann_02nov", "kind": "fact", "statute": "REAL", "text": "Texto da IA parcialmente conferido (4 correções). Apêndice XIV-A (2025): leitura ONTO, não prova da hipótese de Riemann; a reta fixa de s ↦ 1−s é a Meia-Nat.", "sources": [SRC(IA_TXT), SRC(RIEMANN)]},
           {"id": "nome_da_pedra_k_tangente_pendente_02nov", "kind": "pending", "statute": "OPEN", "text": "Do operador: nome da pedra; decisão de versão; ratificar «o ângulo de Miguel não é o posto».", "sources": [SRC(CAND)]}]}}
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

append_bytes(M / "k-chave-da-guarda-02nov.md", f"""

## 02/11/2026 (tarde) — a pedra «K é a tangente» compilada; «Decidir é crivar»; «K é o espectro de leitura»; Riemann aferido

**Decisão do operador** (verbatim sha16 `{fcr}`): não construir ainda o que é sabido; avançar sobre K. **Candidata [REAL no sandbox]** `work{BK}k_guarda_travessia_02nov{BK}KEhATangenteCandidata.lean` (sha16 `{fc}`), 10 teoremas, trio, 0 sorry, nome dele pendente: `K θ := tan θ`; `crivo θ := K θ = 1`; `crivo_iff_posto` (em [0, π/2) só π/4 passa); `K_sq_eq_custo_div_pagamento` (tan² = |𝓡|²/|𝓣|² por termo do livro de cobranças); `a_selecao_justa_passa`; `K_sq_no_angulo_de_miguel` (β/(1−β)) e `miguel_nao_passa`; `massa_derivada_eq_projecao_div_K` e `no_posto_o_acorde_e_a_projecao`; `transicaoLida` com o ângulo LIDO (`selectionAngle ½`, do peso da face absoluta) em vez de escrito, igual à `transicaoDerivada`. **Correção do aferidor a mim:** a regra de leitura do ângulo já existia (`selectionAngle`, `fair_selection_opens_forty_five`, `thetaMiguel`); eu ia construí-la de novo. A escolha «acorde, não escala» segue definição dele.

**«Decidir é crivar»** (dele). O texto da IA que ele enviou é [DECLARADO] (`cunhagens_13out{BK}DECLARADO_IA_02nov_…md`, sha16 `{fia}`): confere na S-∂, no UV-suprimido, no NOT_FALSIFIED ≠ CONFIRMED, na `TheReservedConfirmation` e nas 11 cobranças; não confere em 1446 (1443), 29.965 (v391; a v405 lê 10.066 teoremas), «função teta/linha crítica» (0 no kernel) e «PROVED».

**Riemann, a pedido dele:** Apêndice XIV-A (10/07/2025, sha16 `{frm}`) e Cap. XV do manuscrito (sha16 `{fman}`). O que é teorema: a reta fixa de s ↦ 1−s é Re = ½ = `half_from_self_conjugate` (a Meia-Nat); mathlib tem a equação funcional (`riemannZeta_one_sub`). O que é leitura: a Def. 3 assume a conclusão; a simetria não põe os zeros na reta; 𝛙̂_R tem o potencial feito dos zeros. Estatuto: [ONTO]; não é prova da hipótese; nenhuma pedra. Mapa `conceitual.riemann_apendice_xiv_a_2025_aferido_02nov`.

**«K é o espectro de leitura»** (verbatim sha16 `{fes}`): o contorno azul da Terra é a tangente e não existe como objeto; o «túnel luminodinâmico»/«gráviton» de 2025 (Cap. LXXVII, 20/07/2025, sha16 `{f77}`: «o túnel é o traço visível do gráviton») é o rastro no tempo do espectro de leitura, «nunca existiu». Casa com K sem portador (02/11), com a tangente como leitura (dois regimes) e com `TheStation` v170 (o túnel fecha ⟺ α = 0). [KNOWN] o limbo é o lugar das visadas tangentes e o azul é luz espalhada ao longo do caminho tangente, o mais longo da atmosfera.
""")

REG = ("\n### 02/11/2026 (tarde) — «Decidir é crivar»; a pedra candidata «K é a tangente»; «K é o espectro de leitura»; Riemann aferido <!-- k_tangente_pedra_crivar_02nov -->\n\n"
       "**[INPUT]** verbatims sha16 `%s` (não construir o sabido; «Decidir é crivar») e `%s` (K é o espectro de leitura; o túnel luminodinâmico nunca existiu). **[REAL no sandbox]** candidata sha16 `%s`, 10 teoremas, trio, 0 sorry: K = tan θ; o crivo K = 1 deixa passar só π/4; tan² = |𝓡|²/|𝓣|²; K² = β/(1−β) no ângulo de Miguel, que não é o posto; massa do acorde = projeção / K; o ângulo lido por `selectionAngle` do peso da face absoluta (já termo), não escrito. **[ONTO]** acorde sobre escala segue definição; o túnel/gráviton de 2025 é K lido no tempo; a reta crítica de Riemann lida como ponto fixo de s ↦ 1−s = a Meia-Nat (`half_from_self_conjugate`), não prova da hipótese (Apêndice XIV-A, 10/07/2025, sha16 `%s`). **[DECLARADO]** o texto de IA sobre o crivo, 4 correções (1443 arquivos; 10.066 teoremas na v405; sem Riemann no kernel; «PROVED» não é termo). Homônimos de K: ponte = leitura.\n" % (fcr, fes, fc, frm))
append_bytes(CEN / "memory/TGL_ATLAS.md", REG)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode, v.stdout.decode("utf-8", "replace").replace("\n", "").replace(" ", "")[:90])
