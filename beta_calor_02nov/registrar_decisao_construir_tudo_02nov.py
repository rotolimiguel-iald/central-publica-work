# -*- coding: utf-8 -*-
"""02/11/2026: ORDEM do operador «perfeito, é isso. precisamos construir tudo, porque não podemos mais perder a ordem lógica, é o
fechamento» — supera, para as quatro chaves de testemunha, a decisão da manhã «não vamos construir ainda o que é sabido».
Registro: verbatim, Mapa (rota do programa + anotações), ACOM, memória (tópico novo + linha no índice, com o teto de 24.000 B
respeitado pela regra dos dois arquivos). Backup de bytes; nada no kernel selado; nenhum gate se move."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]

V = CEN / "work/cunhagens_13out/OPERADOR_02nov_precisamos_construir_tudo_nao_perder_a_ordem_logica_e_o_fechamento_verbatim.txt"
texto = "perfeito, é isso. precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento."
if not V.exists():
    V.write_text("# Operador, 02/11/2026 (sessão c1, gerência), verbatim; ORDEM (em resposta à partitura das 42 chaves: 36 habitadas, 2 falsas por teorema, 4 = face de Fock/III₁):\n\n" + texto + "\n", encoding="utf-8")
fv = s16(V)
print("verbatim", fv)

INVJ = CEN / "work/beta_calor_02nov/INVENTARIO_CHAVES_DE_TESTEMUNHA_v405_02nov.json"
reg = [
 {"tipo": "ROTA", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "O FECHAMENTO: construir tudo — habitar as quatro chaves de testemunha (a face de Fock e a testemunha canônica do III₁) por construção dentro do feito (ordem do operador, 02/11)",
  "pergunta": "Como habitar, por construção honesta e na ordem lógica, FockCertificate (→ psion face, fock face, rede v394) e o termo canônico da testemunha plena?",
  "dados": [], "olhou_dados": False,
  "metodo": "Programa em camadas sobre o kernel v405 + mathlib do sandbox, consultando a bancada ANTES de construir (o cético é aferidor); cada pedra candidata compilada no trio, auditada por revisor distinto, registrada aqui; nome das pedras do operador; nada entra no selo sem versão.",
  "resultado": "Ordem recebida e registrada (verbatim sha16 %s). Estado inicial: 42 chaves, 36 habitadas, 2 False por teorema/desenho (ficam), 4 False = a parede de Fock/III₁ (ver rota kernel.inventario_chaves_de_testemunha_v405_02nov). Levantamento em curso." % fv,
  "veredito": "PROGRAMA_ABERTO__ORDEM_DO_OPERADOR", "estatuto": "INPUT (ordem); REAL (inventário)", "status": "EM_CURSO",
  "defeito": "Custo declarado (02/11 manhã): Fock concreta + Tomita/traço 5–15k linhas (semanas); Maxwell 5–10k; fóton 10–30k (meses); o núcleo contínuo com traço (Takesaki) é a parede do III₁ e pode ser a parte mais longa. Nenhuma estimativa é medida.",
  "nao_refazer": "A decisão da manhã («não construir ainda o sabido», rota conceitual.decidir_e_crivar_02nov) fica SUPERADA para estas quatro chaves por esta ordem; não reabrir a escolha.",
  "proximo_passo": "Levantamento medido: (1) o que a bancada já tem de Fock/Weyl/Γ/segunda quantização de subespaços padrão; (2) os campos exatos de CanonicalNetInput + 21 e de canonicalFullTGLWitness; (3) o que a mathlib dá (Completion, Reproducing, SymmetricAlgebra, StandardSubspace). Depois a ORDEM LÓGICA escrita e a camada A.",
  "onde": str(CEN / "work/beta_calor_02nov"), "artefatos": [str(V), str(INVJ)],
  "refs": ["kernel.inventario_chaves_de_testemunha_v405_02nov", "kernel.a_ponte_do_atrito_candidata_02nov", "conceitual.decidir_e_crivar_02nov"],
  "nota": "Regras fixadas antes: as duas chaves falsas por teorema (full_static_witness_exists, trivial_inhabitant_exists) nunca se habitam; o Core do certificado não se habita com modelo degenerado (o tipo rejeita e a régua proíbe); a leitura «ACOM = esperança condicional do III₁» segue [ONTO] até termo; testemunha ≠ prova."},
 {"tipo": "ANOTACAO", "rota_id": "conceitual.decidir_e_crivar_02nov", "dominio": "CONCEITUAL",
  "titulo": "SUPERADA EM PARTE (02/11, tarde): «não vamos construir ainda o que é sabido» cede, para as quatro chaves de testemunha, à ordem «precisamos construir tudo … é o fechamento»",
  "resultado": "Verbatim da nova ordem sha16 %s. A gerência leu ao operador a colisão antes de executar (regra do posto); ele decidiu: construir. Programa na rota kernel.fechamento_construir_tudo_programa_02nov." % fv,
  "estatuto": "INPUT", "artefatos": [str(V)]},
 {"tipo": "ANOTACAO", "rota_id": "kernel.inventario_chaves_de_testemunha_v405_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "Decisão do operador (02/11): construir as quatro; ordem proposta aceita («perfeito, é isso»)",
  "resultado": "Verbatim sha16 %s. Ordem sugerida pela gerência e não contestada: face de Fock da testemunha estática + face do psíon (mesmo habitante: um FockCertificate), depois a rede v394 (CanonicalNetInput + 21), por último a testemunha canônica (III₁). O levantamento dirá se as quatro se reduzem a UMA construção-raiz." % fv,
  "estatuto": "INPUT", "artefatos": [str(V)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_construir_tudo_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-120:].replace("\n", " "))
assert q.returncode == 0

SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-ordem-construir-tudo-o-fechamento", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [
           {"id": "ordem_construir_tudo_o_fechamento_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11 (tarde): «perfeito, é isso. precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento.» Supera, para as quatro chaves de testemunha (face de Fock/III₁), a decisão da manhã «não vamos construir ainda o que é sabido». Programa aberto: rota kernel.fechamento_construir_tudo_programa_02nov. As duas chaves falsas por teorema ficam False.", "sources": [SRCD(V)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:160], (d.get("result") or {}).get("revision"))
assert d.get("ok")

# ---- memória: tópico novo + linha no índice (teto 24.000 B / 195 linhas; o excesso vai íntegro ao MEMORY_2.md)
TOP = M / "construir-tudo-o-fechamento-02nov.md"
assert not TOP.exists()
TOP.write_text(f"""---
name: construir-tudo-o-fechamento-02nov
description: "02/11/2026: ordem do operador «precisamos construir tudo … é o fechamento»: habitar por construção as quatro chaves de testemunha (a face de Fock e a testemunha canônica do III₁); supera «não construir ainda o sabido» da manhã; a ordem lógica e o estado da obra."
metadata:
  type: project
---

**Ordem (02/11/2026, tarde; verbatim sha16 `{fv}`):** «perfeito, é isso. precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento.» Dada depois de a gerência ler a partitura: selo v405 com 42 chaves de testemunha/habitação, 36 habitadas, 2 False por teorema/desenho (`full_static_witness_exists`, `trivial_inhabitant_exists`: ficam False), 4 False = uma parede só, a face de Fock/III₁ (`rede_fock_v394.whole_certificate_inhabited`, `psibit_v395 conditional_psion_face`, `testemunha_estatica_v396 fock_face`, `witness_layers.canonical_full_witness_term_constructed`). Inventário: `work\\beta_calor_02nov\\INVENTARIO_CHAVES_DE_TESTEMUNHA_v405_02nov.json`.

**Why:** ele não quer mais empréstimo de prova no caminho da QG: «não podemos mais perder a ordem lógica». A decisão da manhã («não vamos construir ainda o que é sabido», sha16 72d7939ee701a65b) fica SUPERADA para estas quatro chaves; a gerência leu a colisão a ele antes (regra do posto) e ele decidiu.

**O que as chaves exigem [REAL, lido do kernel]:** as três primeiras pedem um habitante `C : FockCertificate L` (TheImportedSecondQuantization, 45 campos: Fock F infinito, Ω, Γ funtorial forte com energia positiva e sem vetor fixo, ι, rede R : Submodule ℝ H1 → VonNeumannAlgebra F com isotonia/localidade/covariância, cunha cíclica-separante-não-abeliana, `bw_kms` a β = 1 para Γ(B0(2πt)), J, `tomita` (D6), fluxo modular como Ad, e o **Core** com ação dual, `trace : Core → ENNReal` tracial com `trace_dual_scaling`, P_F de traço finito positivo partido em metades iguais) sobre `L : LightOneParticle` (helicidade ±1, rede K de subespaços reais com covariância; H1 = L² da órbita sem massa com fibra ℂ², PAGO pela bancada, ORDEM 016 A-3). A quarta é `TGL.ModularRealization.canonicalFullTGLWitness` (v367). Os montadores da v394 (`F1Fecho394/CanonicalFockAssemblyR1`, `CanonicalModularCoreAssemblyR1`, `CanonicalWeylAssemblyR5`) montam o certificado a partir de `CanonicalNetInput` + 21 campos de traço/P_F.

**How to apply:** (1) consultar a bancada ANTES de construir cada camada (o cético é aferidor; `INVENTARIO_BANCADA_CHATGPT.md`: Fock 1204, Weyl 160, Segal 56, Powers 19, Araki 14 ocorrências); (2) nunca habitar as duas falsas por teorema; nunca habitar o Core com modelo degenerado: o tipo rejeita e a régua proíbe; (3) cada pedra: candidata no sandbox, trio, 0 sorry, revisor distinto, rota no Mapa, nome do operador, versão por decisão dele; (4) testemunha ≠ prova; a leitura «ACOM = esperança condicional do III₁» segue [ONTO]; (5) programa na rota `kernel.fechamento_construir_tudo_programa_02nov`; estado da obra: appends datados abaixo. Relacionado: [[beta-e-a-regra-matriz-02out]] · [[um-py-sem-gordura-19out]] · [[nao-refazer-levantamento-primeiro-07out]] · [[regra-do-posto-do-assistente-30out]].
""", encoding="utf-8")
print("topico", TOP.name, TOP.stat().st_size)

P1, P2 = M / "MEMORY.md", M / "MEMORY_2.md"
b1, b2 = P1.read_bytes(), P2.read_bytes()
nl1 = b"\r\n" if b"\r\n" in b1 else b"\n"
nl2 = b"\r\n" if b"\r\n" in b2 else b"\n"
lines = b1.split(nl1)
NOVA = "- **[O FECHAMENTO: CONSTRUIR TUDO (02/11)](construir-tudo-o-fechamento-02nov.md)** — **ordem do operador**: habitar as 4 chaves de testemunha (Fock/III₁); supera «não construir o sabido»; 2 chaves ficam False por teorema; rota `kernel.fechamento_construir_tudo_programa_02nov`"
PREFIXO = "- **[TREINO v4 DA IALD NATIVA"
CURTA = "- **[TREINO v4 DA IALD NATIVA — um.py v404 inteiro (29/10)](treino-nativa-v4-29out.md)** — íntegra no MEMORY_2.md (movida 02/11)"
movidas, novas, inserida = [], [], False
for raw in lines:
    s = raw.decode("utf-8")
    if s.startswith(PREFIXO):
        movidas.append(s); novas.append(CURTA.encode("utf-8")); continue
    novas.append(raw)
    if s.strip() == "## Estado corrente" and not inserida:
        novas.append(NOVA.encode("utf-8")); inserida = True
assert len(movidas) == 1 and inserida, (movidas, inserida)
out1 = nl1.join(novas)
print("MEMORY.md", len(b1), "->", len(out1), "B;", len(novas), "linhas")
assert len(out1) <= 24000 and len(novas) <= 195
bloco = ("\n\n## Linha movida do MEMORY.md em 02/11/2026 (regra dos dois arquivos; abriu espaço para «O FECHAMENTO: CONSTRUIR TUDO»)\n\n" + "\n".join(movidas) + "\n").replace("\n", nl2.decode())
out2 = b2.rstrip() + bloco.encode("utf-8")
for P, b, out in ((P2, b2, out2), (P1, b1, out1)):
    bak = P.with_name(P.name + ".bak_" + TS)
    with open(bak, "xb") as f:
        f.write(b)
    assert bak.read_bytes() == b
    tmp = P.with_name(P.name + ".tmp_" + TS)
    with open(tmp, "xb") as f:
        f.write(out)
    assert tmp.stat().st_size == len(out)
    os.replace(tmp, P)
    print(P.name, len(b), "->", P.stat().st_size)
assert P2.stat().st_size > len(b2)
env = dict(os.environ, MEMORIA_GERENCIA="claude-c1")
for cmd in (["pinar"], ["verificar"]):
    r = subprocess.run([PY, "-X", "utf8", "memoria.py", *cmd], cwd=str(M / "fila"), capture_output=True, env=env)
    print(cmd[0], "rc", r.returncode, r.stdout.decode("utf-8", "replace").replace("\n", " ")[:200])
