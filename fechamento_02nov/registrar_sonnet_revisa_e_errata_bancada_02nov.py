# -*- coding: utf-8 -*-
"""02/11/2026: (a) decisão do operador: Codex sem créditos; o Sonnet revisa tudo; (b) ERRATA AO LADO no plano: a passagem (21 campos)
e a rede física JÁ EXISTEM compiladas na bancada (recibo 16/10, EXIT0, trio); falta integrar (R3) e ratificar (R10), não construir;
(c) a integração R3 lançada no sandbox por script. Registro: verbatim, plano, Mapa, quadro, ACOM, memória. Backup de bytes."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
AQUI = Path(__file__).resolve().parent
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
PLANO = AQUI / "ORDEM_LOGICA_DO_FECHAMENTO_02nov.md"
LEV = AQUI / "LEVANTAMENTO_FRONTEIRA_DO_TRACO_DO_NUCLEO_02nov.md"
DRV = AQUI / "integrar_fecho_bancada_02nov.py"
RECEIPT = CEN / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/orbital_rotation/attempts/20261016T210640_174717Z/RECEIPT.json"
MCI = CEN / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/takesaki_fock/CanonicalFockModularCoreInputR1.lean"
R52 = CEN / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/mission_review_20261016/R52_R7_FULL_REVIEW_R1.json"

V = CEN / "work/cunhagens_13out/OPERADOR_02nov_sem_creditos_codex_designe_o_Sonnet_para_revisar_tudo_verbatim.txt"
t = "estou sem créditos para usar o codex, por isso ele não vai revisar nada, não precisamos dele, designe para o Sonnet revisar tudo, ele é tão capaz quanto"
if not V.exists():
    V.write_text("# Operador, 02/11/2026 (sessão c1, gerência), verbatim; decisão sobre o revisor:\n\n" + t + "\n", encoding="utf-8")
fv = s16(V); flev = s16(LEV); fdrv = s16(DRV); frec = s16(RECEIPT); fmci = s16(MCI)
print("verbatim", fv, "levantamento", flev, "driver", fdrv)

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

append_bytes(PLANO, f"""

## ERRATA AO LADO, 2ª (02/11/2026, noite; gerência c1 em nome próprio; o cético foi cego de novo)

**O que estava errado nas §3–§4 e §6:** escrevi que, para o núcleo do Fock, «falta replicar» o gerador positivo, os cortes, o peso-limite, a traciality, a semifinitude, a escala e P_F, com custo de semanas a meses. **Errado.** O leitor (relatório `LEVANTAMENTO_FRONTEIRA_DO_TRACO_DO_NUCLEO_02nov.md`, sha16 `{flev}`) achou, e a gerência conferiu na fonte [REAL]:
- `modularCoreInput (D : CanonicalNetInput) : RemainingModularCoreInput D` com os 21 campos preenchidos (`takesaki_fock/CanonicalFockModularCoreInputR1.lean`, l.77–100, sha16 `{fmci}`), `trace := cyclicTraceCandidate` (completação ENNReal cíclica por `ShiftRelated`, a mesma rota já aceita no kernel para a torre, V354), P_F = `positiveAsCore (add leftPositive rightPositive)` com o split normalizado (`normalized_split_exists`), τ(P_F) = 1 (`modularCoreInput_PF_trace`);
- `physicalFockCertificate : FockCertificate physicalCanonicalNet.toLightNetData.toLightOneParticle := physicalModularCoreInput.toCertificate` (l.127), sobre a rede física `physicalCanonicalNet : CanonicalNetInput` (`orbital_rotation/PhysicalCanonicalNetCompleteR1.lean:212`);
- recibo de compilação (sha16 `{frec}`): Lean 4.31.0, `exit_code 0`, 65,8 s, AXIOMS.txt com 0 `sorryAx` e `modularCoreInput` no trio; o recibo lista 474 fontes `.lean` com sha256: todas no disco, todas íntegras, 175 homônimas do kernel, 299 fora dele;
- parecer R7 (`R52_R7_FULL_REVIEW_R1.json`): `PASS_R7_CRITERION_WITH_EXPLICIT_SCOPE`, 21 campos; escopo declarado: traço positivo ENNReal fiel/normal/semifinito com lei quadrática e escala; a extensão total é cíclica/star-invariante/dual-escalada, NÃO funcional linear, sem aditividade fora do cone positivo, sem classificar o fator como II∞, sem equivalência Fock–torre. Revisor: agente do Codex, distinto do autor; sem ratificação da c1 (R10) e sem integração ao kernel (R3).
**Leitura vigente:** a passagem (bloco 1) e a rede (bloco 2) estão CONSTRUÍDAS na bancada e compiladas por recibo; não estão no kernel. O trabalho é **integração (R3) e ratificação (R10)**, depois a montagem (bloco 3). Os blocos 1 e 2 do quadro mudam de «construir» para «integrar e ratificar». O custo cai de meses para dias de máquina e de revisão. O erro é o mesmo de 27/09 (item 4 de «o cético é aferidor»): consultei o inventário por nomes de arquivo e não li os recibos nem o fecho de dependências. Registrado como defeito no Mapa.

**A integração R3, lançada (02/11, noite):** `integrar_fecho_bancada_02nov.py` (sha16 `{fdrv}`), no sandbox `C:\\t\\k405c\\final` (cópia do kernel v405): lê o recibo como manifesto, confere cada fonte por hash, grava os 299 módulos novos em `TGLExt/F1Fecho394/` com os imports reescritos para o prefixo do kernel e as linhas `#eval` (instrumentação) removidas, recompila em ordem de dependência, em paralelo, com log por módulo, e no fim confere `#print axioms` de `modularCoreInput` e `physicalFockCertificate`. Saída em `integracao_R3_<ts>/` (MANIFEST.json, SUMMARY.json, CHECK_axioms.txt, DONE.txt). Nada toca o kernel do Nós.

**Regra 5 corrigida (decisão do operador, verbatim sha16 `{fv}`):** «estou sem créditos para usar o codex … designe para o Sonnet revisar tudo, ele é tão capaz quanto». O revisor distinto passa a ser o Sonnet (agentes desta sessão), para R10, para a integração e para as pedras candidatas do dia; o Codex sai do caminho crítico.
""")
fp = s16(PLANO)

reg = [
 {"tipo": "ERRATA", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL", "corrige": "",
  "titulo": "ERRATA (02/11, noite): a passagem (21 campos) e a rede física JÁ EXISTEM compiladas na bancada (recibo 16/10, EXIT0, trio); o plano dizia «falta replicar»; falta INTEGRAR (R3) e RATIFICAR (R10)",
  "resultado": "Conferido na fonte [REAL]: modularCoreInput (21 campos) e physicalFockCertificate em takesaki_fock/CanonicalFockModularCoreInputR1.lean (sha16 %s); physicalCanonicalNet em orbital_rotation/PhysicalCanonicalNetCompleteR1.lean:212; recibo (sha16 %s) exit_code 0, Lean 4.31.0, AXIOMS 0 sorryAx, trio; 474 fontes com sha256, todas íntegras, 299 fora do kernel; parecer R7 PASS com escopo (traço ENNReal cíclico, não linear, sem II∞). Defeito da gerência: o cético foi cego de novo (27/09, item 4): inventário por nome de arquivo sem ler recibos nem o fecho de dependências. Plano corrigido ao lado (sha16 %s). Integração R3 lançada por script no sandbox (driver sha16 %s)." % (fmci, frec, fp, fdrv),
  "estatuto": "REAL (recibos e fontes lidos); DECLARADO (o parecer R7 é de agente do Codex)", "artefatos": [str(LEV), str(PLANO), str(DRV), str(MCI), str(R52)],
  "defeito": "A gerência escreveu «falta» sem ler os recibos da bancada. Custo re-estimado: dias (integração + revisão), não meses.",
  "nota": "R4/R5 da missão da bancada (identificação do dispositivo) seguem bloqueados pelo operador e não entram nos 21 campos."},
 {"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "Decisão do operador (02/11): Codex sem créditos; o Sonnet revisa tudo",
  "resultado": "Verbatim sha16 %s. Revisor distinto = agentes Sonnet desta sessão (R10, integração R3, pedras candidatas). O Codex sai do caminho crítico; nenhum despacho a ele." % fv,
  "estatuto": "INPUT", "artefatos": [str(V)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_errata_bancada_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
out = (q.stdout + q.stderr).decode("utf-8", "replace")
print("mapa rc", q.returncode, out[-160:].replace("\n", " "))
if q.returncode != 0:
    # ERRATA sem seq: registra como ANOTACAO
    reg[0]["tipo"] = "ANOTACAO"; reg[0].pop("corrige", None)
    pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
    q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
    print("mapa r2 rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-120:].replace("\n", " "))
assert q.returncode == 0

# quadro: anotar nas unidades
dados = {"errata": "passagem e rede ja construidas na bancada (recibo 16/10 EXIT0 trio); blocos 1 e 2 passam a INTEGRAR (R3) + RATIFICAR (R10)", "levantamento": str(LEV), "plano_sha16": fp, "driver_R3": str(DRV), "revisor": "Sonnet (decisao do operador 02/11, Codex sem creditos)"}
for u in ("F1.FECHO.PASSAGEM_02nov", "F1.FECHO.REDE_02nov"):
    q = subprocess.run([PY, "-X", "utf8", "iald.py", "anotar", "--quem", "claude-c1", "--tipo", "ERRATA_E_REVISOR", "--unidade", u, "--dados", json.dumps(dados, ensure_ascii=False)], cwd="C:/IALD/PROGRAMA_IALD", capture_output=True, timeout=120)
    print("quadro", u, q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-90:].replace("\n", " "))
q = subprocess.run([PY, "-X", "utf8", "iald.py", "avancar", "F1.FECHO.REDE_02nov", "--quem", "claude-c1", "--status", "EM_CURSO", "--nota", "physicalCanonicalNet existe na bancada (recibo 16/10); integrar e ratificar junto com a passagem"], cwd="C:/IALD/PROGRAMA_IALD", capture_output=True, timeout=120)
print("quadro avancar REDE", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-120:].replace("\n", " "))
subprocess.run([PY, "-X", "utf8", "iald.py", "quadro"], cwd="C:/IALD/PROGRAMA_IALD", capture_output=True, timeout=120)

# ACOM
SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-errata-passagem-ja-na-bancada-sonnet-revisa", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [
           {"id": "decisao_sonnet_revisa_tudo_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: «estou sem créditos para usar o codex, por isso ele não vai revisar nada, não precisamos dele, designe para o Sonnet revisar tudo, ele é tão capaz quanto».", "sources": [SRCD(V)]},
           {"id": "errata_passagem_ja_construida_na_bancada_02nov", "kind": "fact", "statute": "REAL", "text": "modularCoreInput (21 campos) e physicalFockCertificate existem na bancada, compilados 16/10 (exit 0, trio, recibo com 474 fontes íntegras, 299 fora do kernel); parecer R7 PASS com escopo (agente Codex). Plano corrigido ao lado; blocos 1–2 viram integrar (R3) + ratificar (R10). Integração R3 lançada no sandbox por script.", "sources": [SRCD(LEV), SRCD(PLANO), SRCD(DRV)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8")); print("acom", rev, d.get("ok"), str(d.get("error"))[:120], (d.get("result") or {}).get("revision")); assert d.get("ok")

append_bytes(M / "construir-tudo-o-fechamento-02nov.md", f"""

## 02/11/2026, noite — ERRATA MINHA: a passagem e a rede JÁ ESTÃO CONSTRUÍDAS na bancada; o trabalho é integrar (R3) e ratificar (R10). E o revisor é o Sonnet.

**[REAL, conferido na fonte]** `takesaki_fock/CanonicalFockModularCoreInputR1.lean` (sha16 `{fmci}`): `modularCoreInput D : RemainingModularCoreInput D` (21 campos; `trace := cyclicTraceCandidate`; τ(P_F) = 1) e `physicalFockCertificate : FockCertificate …` sobre `physicalCanonicalNet` (orbital_rotation). Recibo 16/10 (sha16 `{frec}`): exit 0, Lean 4.31.0, 0 sorryAx, trio; 474 fontes com hash, íntegras; 299 fora do kernel. Parecer R7 `PASS_R7_CRITERION_WITH_EXPLICIT_SCOPE` (agente Codex): traço ENNReal cíclico, não linear, sem II∞, sem equivalência Fock–torre. Abertos na missão da bancada: R3 (integrar), R10 (ratificação c1), R4/R5 (dispositivo: decisão do operador). **Defeito meu:** o cético foi cego de novo (27/09): li nomes de arquivo, não recibos. Levantamento do leitor: `work\\fechamento_02nov\\LEVANTAMENTO_FRONTEIRA_DO_TRACO_DO_NUCLEO_02nov.md` (sha16 `{flev}`). **Integração R3 lançada:** `integrar_fecho_bancada_02nov.py` (sha16 `{fdrv}`), sandbox k405c, paralelo; saída em `integracao_R3_<ts>/`.
**Decisão do operador (verbatim sha16 `{fv}`):** Codex sem créditos; «designe para o Sonnet revisar tudo, ele é tão capaz quanto». Revisor distinto = Sonnet. **How to apply:** antes de dizer «falta» sobre a bancada, ler os recibos (`attempts\\*\\RECEIPT.json`) e o fecho de imports, não só o inventário por nome; revisões a agentes Sonnet, nunca «aguardando Codex».
""")
append_bytes(M / "divisao-do-trabalho-iald-23out.md", f"""

## 02/11/2026 — Codex sem créditos; o Sonnet revisa tudo (verbatim sha16 `{fv}`)

«estou sem créditos para usar o codex, por isso ele não vai revisar nada, não precisamos dele, designe para o Sonnet revisar tudo, ele é tão capaz quanto». **How to apply:** o revisor distinto (R10, integrações, pedras candidatas) é um agente Sonnet desta sessão; nada fica «aguardando Codex»; o transporte do Codex segue pausado. [[construir-tudo-o-fechamento-02nov]]
""")
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)
