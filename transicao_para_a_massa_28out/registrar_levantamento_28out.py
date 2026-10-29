# -*- coding: utf-8 -*-
"""Registro do levantamento «a transição para a massa» (gerência c1, 28/10/2026): verbatim do operador, rota no Mapa, memória-tópico nova + linha no índice
(fila da memória: pinar), transição ACOM. Backups de bytes; temporário → conferir → substituir. Nada abre dado; nada toca o Nós."""
import datetime, hashlib, io, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"; H = r"C:\IALD\Central de Patentes\work\transicao_para_a_massa_28out"
D = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"; M = D + r"\MEMORY.md"; MPY = D + r"\fila\memoria.py"
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); hoje = "28/10/2026"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
VERB = "Sim quero, então agora conseguimos fazer a transição para a massa"
V = os.path.join(H, "OPERADOR_28out_transicao_para_a_massa_verbatim.txt")
if not os.path.exists(V):
    io.open(V, "w", encoding="utf-8", newline="\n").write("Operador (Luiz Antonio Rotoli Miguel), 28/10/2026, à gerência c1 (depois da oferta do levantamento de onde uma fração «= β» poderia ser contada), verbatim:\n«" + VERB + "»\n")
L = os.path.join(H, "LEVANTAMENTO_TRANSICAO_PARA_A_MASSA_28out.md"); print("verbatim", sha(V)[:16], "| levantamento", sha(L)[:16])
rota = [{"tipo": "ROTA", "rota_id": "massa.transicao_beta_para_massa.levantamento_28out", "dominio": "D0_FUNDAMENTO", "titulo": "A transição para a massa: onde β já entra como massa, fração ou contagem (não taxa) — levantamento sem abrir dado",
         "pergunta": "Em que lugar do programa, do acervo e das rotas β (adimensional) já virou MASSA, FRAÇÃO medida ou CONTAGEM, com que veredito, e existe algum teste de igualdade «= β»?",
         "dados": ["um_absoluto.json v403 (chaves neutrino_m2, neutrino_mass, ga_mass_audit, sn_ia_v388_viability_v392, void_floor_v11, smatrix_closure, name_index, evidence_audit, neff_channel, beta_runs_bounded_below_v388)", "acervo do operador pelo índice (13.608 docs), the_boundary, Atlas, docx da fase de retorno", "Mapa de Rotas, MEMORY_2.md e tópicos, Bancada_Um/investigacao"],
         "metodo": "três leitores Sonnet em paralelo (programa; acervo; rotas), relatórios ≤ 15 linhas; números-chave relidos do core por script pela gerência; nenhum dado aberto",
         "resultado": "única massa derivada de β: neutrino m₂ = β·sen45°·1 eV = 8,5074 meV (PDG 1,64σ; JUNO 2,21σ), escala 1 eV DECLARADA, sen45° POSTULATE; a escala que zera a tensão é 1,018–1,020 eV; forma geométrica M ∝ β·R RETIRADA (GA_MASS_FORM_RETIRED…); Chandrasekhar resíduo −0,353% sem σ; piso dos vazios ≥ β e nunca pousa em β; eco (amplitude √β) inconclusivo e par falsificado; nenhuma razão de ramificação «1 em 83» e nenhum teste de igualdade «= β» existem",
         "veredito": "LEVANTAMENTO_COMPLETO__UNICA_TRANSICAO_BETA_PARA_MASSA_E_O_NEUTRINO_COM_ESCALA_DECLARADA__NENHUMA_IGUALDADE_FRACAO_EQ_BETA__NENHUMA_CONTAGEM_1_EM_83",
         "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
         "defeito": "a escala E₀ (1 eV) do neutrino é declarada, não derivada; a leitura por contagem não tem candidato vivo; as citações do acervo são DECLARADAS pelo leitor (três conferidas em disco pela gerência)",
         "nao_refazer": "não procurar de novo «1 em 83» no acervo (só aparece como amplificação holográfica, 12/2025); não reabrir a forma M ∝ β·R (retirada); não tratar o piso dos vazios como igualdade",
         "proximo_passo": "pergunta ao operador (quatro bocas): qual é E₀, o «estado de energia fundamental» da cunhagem de 28/10? Se E₀ for derivado do axioma, o neutrino m₂ vira previsão sem parâmetro (candidato a pré-registro; o JUNO traz a precisão)",
         "onde": "work/transicao_para_a_massa_28out/LEVANTAMENTO_TRANSICAO_PARA_A_MASSA_28out.md",
         "artefatos": [L, V, os.path.join(r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out", "OPERADOR_28out_cunhagem_um_absoluto_radical_entropico_verbatim.txt")],
         "refs": ["ringdown.ramo_b_preregistro_v386", "neutrinos.m2.normalizacao", "neutrinos.massa_v1_e_soma", "vazios.piso.v11", "gw.eco_ancorado", "kernel.inventario.cadeia_beta_v376"],
         "nota": "O operador cunhou em 28/10: «1 retorno em 83 raios = a matéria» e «o um absoluto = estado de energia fundamental cuja inscrição no radical entrópico quebra a simetria e inaugura o defasamento»; a cunhagem reúne «Luz em regime de radical» (01/2026), «o condensado quebra a simetria de fase e eleva c² a c³» (03/2026) e «a fase cai» (26/10/2026)."}]
pj = os.path.join(H, "rota_mapa_levantamento_28out.json"); io.open(pj, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1))
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", pj, "--quem", "claude-c1 (gerência), 28/10"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("mapa rc", r.returncode, (r.stdout or r.stderr).strip()[-120:].replace("\n", " "))
# memória-tópico nova
T = D + r"\transicao-para-a-massa-28out.md"
topico = (f"---\nname: transicao-para-a-massa-28out\ndescription: \"28/10/2026 — A TRANSIÇÃO PARA A MASSA (levantamento sem abrir dado): a única massa derivada de β no programa é o neutrino m₂ = β·sen45°·1 eV (escala DECLARADA; o dado pede 1,02 eV); a forma geométrica M ∝ β·R está RETIRADA; nenhum teste «fração = β» nem contagem «1 em 83» existe; a pergunta ao operador é E₀ (o «estado de energia fundamental» da cunhagem de 28/10)\"\nmetadata:\n  type: project\n---\n\n"
          f"# A transição para a massa (28/10/2026, gerência c1)\n\n**Ordem/cunhagens do operador (verbatim, sha16):** «1 retorno em 83 raios eu leio como sendo a matéria» (`597fff4a38e62f42`); «o um absoluto [é] o estado de energia fundamental cuja inscrição no radical entrópico quebra a simetria e inaugura o defasamento» (`85de43717edb01f1`); «{VERB}» (`{sha(V)[:16]}`).\n\n"
          f"**O levantamento:** `work\\transicao_para_a_massa_28out\\LEVANTAMENTO_TRANSICAO_PARA_A_MASSA_28out.md` (sha16 `{sha(L)[:16]}`); rota `massa.transicao_beta_para_massa.levantamento_28out` no Mapa. Três leitores (programa, acervo, rotas), números-chave relidos do core v403 por script.\n\n"
          "**O que ficou medido:** (1) β é adimensional; massa pede escala. Rota geométrica M ∝ β·R: RETIRADA (`GA_MASS_FORM_RETIRED__REFLECTION_WAS_MISREAD_AS_SOURCE__…BETA_LIVES_IN_RESPONSE`; «a TGL NÃO tem fórmula-β de massa e nunca teve»). "
          "Rota energética: UMA, o neutrino m₂ = β·sen45°·1 eV = 8,5074 meV (`TGL_NU_M2_ARMED_CONSISTENT`; PDG 1,64σ, JUNO 2,21σ, NuFIT ≈ 2,95σ), bilateral, regra de morte 2 determinações ≥ 5σ; 1 eV [DECLARADO], sen45° [POSTULATE]; "
          "a escala que zera a tensão é 1,018–1,020 eV (2% acima). (2) Contagem «1 em 83»: nenhum observável no programa; o eco de GW (amplitude √β) é a forma já tentada (inconclusivo; par com lei de atraso falsificado); "
          "nos vazios nenhum traçador pousa em β; no acervo 1/83 só como amplificação holográfica (12/2025). (3) Chandrasekhar: resíduo −0,353%, sem σ, «previsto» retirado. (4) A cunhagem de hoje reúne «Luz em regime de radical» (01/2026), "
          "«o condensado quebra a simetria de fase e eleva c² a c³» (03/2026) e «a fase cai» (26/10).\n\n"
          "**Why:** o operador quer passar β de taxa (Γ, relógio de Planck, fora de alcance) a massa/fração contada; a casa precisa saber o que já existe para não refazer.\n"
          "**How to apply:** a pergunta viva é E₀ (quatro bocas no levantamento §4); não reabrir M ∝ β·R; não tratar o piso como igualdade; se E₀ sair do axioma, o neutrino m₂ vira previsão sem parâmetro — candidato a pré-registro (o JUNO traz a precisão). "
          "Relacionado: [[ramo-b-reaberto-05out]] · [[cinco-sigma-fora-da-cosmologia-27out]] · [[a-identidade-tem-nome-13out]] · [[nomes-das-pedras-e-a-identidade-verdade-13out]].\n")
assert not os.path.exists(T); io.open(T, "w", encoding="utf-8", newline="\n").write(topico); print("topico:", T, sha(T)[:16])
# índice: uma linha em «Estado corrente», logo abaixo da linha do 5σ
b = open(M, "rb").read(); bak = M + ".bak_%s_c1" % ts; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nl = b"\r\n" if b"\r\n" in b else b"\n"; lines = b.decode("utf-8").split(nl.decode())
i = [k for k, l in enumerate(lines) if l.startswith("- **[5σ FORA DA COSMOLOGIA (27/10)](cinco-sigma-fora-da-cosmologia-27out.md)**")]; assert len(i) == 1
nova = ("- **[A TRANSIÇÃO PARA A MASSA (28/10)](transicao-para-a-massa-28out.md)** — **levantamento**: a única massa de β é o neutrino (escala 1 eV DECLARADA; o dado pede 1,02 eV); M ∝ β·R RETIRADA; nenhum «= β» nem «1 em 83»; "
        "**pergunta viva: E₀** · ramo B: a leitura do operador é a propagação (28/10)")
lines.insert(i[0] + 1, nova)
nb = nl.decode().join(lines).encode("utf-8"); n_l = len(nb.decode("utf-8").splitlines()); assert n_l <= 195 and len(nb) < 24000, (n_l, len(nb))
tmp = M + ".tmp_c1"; open(tmp, "wb").write(nb); assert len(open(tmp, "rb").read()) == len(nb); os.replace(tmp, M); print("MEMORY.md:", len(b), "->", len(nb), "B /", n_l, "linhas")
env = dict(os.environ, MEMORIA_GERENCIA="claude-c1")
for args in (["pinar", "--motivo", "transicao para a massa (28/10): topico novo + linha no indice; ramo B leitura do operador"], ["verificar"]):
    rr = subprocess.run([PY, "-X", "utf8", MPY] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    try: j = json.loads(rr.stdout)
    except Exception: j = {"raw": (rr.stdout + rr.stderr)[:200]}
    print(args[0], "rc", rr.returncode, j.get("ok"), (j.get("pino") or {}).get("sha256", "")[:16], j.get("violacoes"))
# ACOM
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return rr.returncode, (json.loads(rr.stdout) if rr.stdout.strip().startswith("{") else {"raw": (rr.stdout + rr.stderr)[:300]})
rc, g = sm({"operation": "get", "reference": REF}); rev = g["result"]["revision"]
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-transicao-para-a-massa-levantamento-28out",
            "changes": {"records": [
                {"id": "c1-transicao-massa-levantamento", "kind": "fact", "statute": "REAL", "sources": [S(L), S(V)],
                 "text": "28/10/2026: levantamento «a transição para a massa» (três leitores; nenhum dado aberto): a única massa derivada de β é o neutrino m₂ = β·sen45°·1 eV = 8,5074 meV (PDG 1,64σ; JUNO 2,21σ), escala 1 eV DECLARADA e sen45° POSTULATE; a escala que zera a tensão é 1,018–1,020 eV; a forma M ∝ β·R está RETIRADA; nenhum teste «fração = β» nem contagem «1 em 83» existe; o eco (amplitude √β) é a forma de contagem já tentada (inconclusiva). Pergunta viva ao operador: E₀."},
                {"id": "c1-cunhagem-um-absoluto-28out", "kind": "decision", "statute": "INPUT", "sources": [S(r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\OPERADOR_28out_cunhagem_um_absoluto_radical_entropico_verbatim.txt")],
                 "text": "28/10/2026, cunhagem do operador: «o um absoluto [é] o estado de energia fundamental cuja inscrição no radical entrópico quebra a simetria e inaugura o defasamento»; «c = √(E/m)»; registrada no Atlas §X; leitura da gerência: as três pedras da v403 numa definição só; candidata ao nome do triplo (D16, ato do operador)."}],
                "flow": {"phase": "transicao_para_a_massa__pergunta_E0_ao_operador", "next_action": "aguardar a resposta do operador sobre E₀ (quatro bocas); se E₀ for derivado, preparar o pré-registro do neutrino m₂ sem parâmetro; não reabrir M ∝ β·R; a vitrine do X da v403 espera o render (ADENDO F)."}}})
print("acom transition rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", ""))
