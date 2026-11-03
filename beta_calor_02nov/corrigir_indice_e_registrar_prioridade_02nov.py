# -*- coding: utf-8 -*-
"""02/11/2026 (2ª parte): (a) a linha do índice para «O FECHAMENTO: CONSTRUIR TUDO» não coube no teto (24.084 > 24.000 B); a regra dos
dois arquivos: duas linhas (TREINO v4; CONJUNTO D) vão íntegras ao MEMORY_2.md e ficam como ponteiro; (b) a PRIORIDADE do operador
(«a construção da passagem para o contínuo é o que mais importa … virar essa chave de conjectura para provado»): verbatim, Mapa, append
no tópico. O Mapa/ACOM/tópico da ordem «construir tudo» já foram gravados pelo script anterior (não se repetem)."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]

# (b) prioridade: verbatim + Mapa
V = CEN / "work/cunhagens_13out/OPERADOR_02nov_a_passagem_para_o_continuo_e_o_que_mais_importa_virar_a_chave_de_conjectura_para_provado_verbatim.txt"
texto = "a construção da passagem para o contínuo é o que mais importa, porque deixa de ser conjectura sob hipótese se funcionar sob compressão elevando o potencial do resultado do código final em 1=1=HAJA_LUZ; isso é o que mais importa, virar essa chave de conjectura para provado"
if not V.exists():
    V.write_text("# Operador, 02/11/2026 (sessão c1, gerência), verbatim; PRIORIDADE dentro da ordem «construir tudo»:\n\n" + texto + "\n", encoding="utf-8")
fv = s16(V)
print("verbatim", fv)
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "PRIORIDADE do operador (02/11): «a construção da passagem para o contínuo é o que mais importa … virar essa chave de conjectura para provado»",
  "resultado": "Verbatim sha16 %s. Leitura da gerência: a «chave» é a face de Fock/III₁ (o habitante do FockCertificate, de que dependem a face do psíon, a face de Fock da testemunha estática, a rede v394 e, por lightRealization, a testemunha canônica); hoje os teoremas dessa face são CONDICIONAIS a um C não exibido (conjectura sob hipótese); exibido C, viram incondicionais (provado). A ordem do programa muda: a passagem (os 21 campos de traço/P_F do Core + o RemainingModularCoreInput) vai para o bloco 1; «sob compressão» = o traço semifinito do núcleo construído como limite de compressões por projeções finitas (a leitura dele; correlato: peso normal semifinito determinado pelos cantos finitos [KNOWN])." % fv,
  "estatuto": "INPUT; ONTO (leitura da compressão)", "artefatos": [str(V)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_prioridade_passagem_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-100:].replace("\n", " "))
assert q.returncode == 0

def append_bytes(path, add):
    b = path.read_bytes(); add_b = add.encode("utf-8")
    if b"\r\n" in b: add_b = add_b.replace(b"\n", b"\r\n")
    bk = path.with_name(path.name + ".bak_" + TS)
    with open(bk, "xb") as f: f.write(b)
    assert bk.read_bytes() == b
    tmp = path.with_name(path.name + ".tmp_" + TS)
    with open(tmp, "xb") as f: f.write(b.rstrip() + add_b)
    assert tmp.stat().st_size > len(b) - 4
    os.replace(tmp, path); print(path.name, len(b), "->", path.stat().st_size)

append_bytes(M / "construir-tudo-o-fechamento-02nov.md", f"""

## 02/11/2026 — PRIORIDADE: «a construção da passagem para o contínuo é o que mais importa … virar essa chave de conjectura para provado» (verbatim sha16 `{fv}`)

**A chave** é a face de Fock/III₁: um habitante `C : FockCertificate L`. Hoje `the_psion_face_of_the_psibit`, `lightRealization`, `lightNet`, `lightBoost` e tudo a jusante são CONDICIONAIS a C (conjectura sob hipótese); exibido C, viram incondicionais (provado como validade; a confirmação segue creditação). **Ordem do programa (reordenada por ele):** bloco 1 = a passagem (o Core com ação dual, `trace` tracial com `trace_dual_scaling`, P_F finito partido em metades: os 21 campos de traço/P_F, `RemainingModularCoreInput`), «sob compressão»: o traço do núcleo como limite de compressões por projeções finitas [leitura dele; correlato KNOWN: peso normal semifinito determinado nos cantos finitos]; bloco 2 = `CanonicalNetInput` (a rede K da luz com a cola da cunha); bloco 3 = montagem (montadores v394 já existem) → as três chaves + `canonicalFullTGLWitness`; bloco 4 = Maxwell/H3 (item 3 do contrato v394). **O que já existe no kernel [REAL]:** o Fock bosônico concreto `F1Rede.BosonicFock` (vácuo, Γ, infinito, ações de grupo, continuidade) e os montadores `F1Fecho394/Canonical{{Fock,Weyl,ModularCore}}Assembly`; na bancada (F1.FECHO 15–16/10): `takesaki_fock/*` (WeightStarDensity, FullWeightStarCore, ModularBridge R1–R7, ModularGraphEquality), `gns_coefficient_tomita/*` (PolarRightClosure R1–R10, Cutoff R10–R11), `gamma_unbounded/*` (ExponentialTomita, WeylExponentialGraphCore), `orbital_rotation/PhysicalFockNetRealization R1–R2`. Consultar antes de construir.
""")

# (a) o índice: duas linhas vão íntegras ao MEMORY_2.md; entra a linha nova
P1, P2 = M / "MEMORY.md", M / "MEMORY_2.md"
b1, b2 = P1.read_bytes(), P2.read_bytes()
nl1 = b"\r\n" if b"\r\n" in b1 else b"\n"
nl2 = b"\r\n" if b"\r\n" in b2 else b"\n"
lines = b1.split(nl1)
NOVA = "- **[O FECHAMENTO: CONSTRUIR TUDO (02/11)](construir-tudo-o-fechamento-02nov.md)** — **ordem do operador**: habitar as 4 chaves de testemunha (Fock/III₁); a passagem para o contínuo primeiro; 2 chaves ficam False por teorema"
alvos = {
 "- **[TREINO v4 DA IALD NATIVA": "- **[TREINO v4 DA IALD NATIVA — um.py v404 inteiro (29/10)](treino-nativa-v4-29out.md)** — íntegra no MEMORY_2.md (movida 02/11)",
 "- **[CONJUNTO D AUTORIZADO (29/10)]": "- **[CONJUNTO D AUTORIZADO (29/10)](conjunto-d-autorizado-29out.md)** — teste cego sob o V1 do ramo B; nada aberto antes do PODER com hash · íntegra no MEMORY_2.md (movida 02/11)",
}
assert not any(l.decode("utf-8").startswith("- **[O FECHAMENTO: CONSTRUIR TUDO") for l in lines)
movidas, novas, inserida = [], [], False
for raw in lines:
    s = raw.decode("utf-8")
    hit = next((k for k in alvos if s.startswith(k)), None)
    if hit:
        movidas.append(s); novas.append(alvos[hit].encode("utf-8")); continue
    novas.append(raw)
    if s.strip() == "## Estado corrente" and not inserida:
        novas.append(NOVA.encode("utf-8")); inserida = True
assert len(movidas) == 2 and inserida, (len(movidas), inserida)
out1 = nl1.join(novas)
print("MEMORY.md", len(b1), "->", len(out1), "B;", len(novas), "linhas")
assert len(out1) <= 24000 and len(novas) <= 195
bloco = ("\n\n## Linhas movidas do MEMORY.md em 02/11/2026 (regra dos dois arquivos; abriram espaço para «O FECHAMENTO: CONSTRUIR TUDO»)\n\n" + "\n".join(movidas) + "\n").replace("\n", nl2.decode())
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
    print(cmd[0], "rc", r.returncode, r.stdout.decode("utf-8", "replace").replace("\n", " ")[:160])
