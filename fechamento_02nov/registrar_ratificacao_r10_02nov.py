# -*- coding: utf-8 -*-
"""02/11/2026: a integração R3 fechou no sandbox (300/300, physicalFockCertificate no trio). Preenche §4–§5 da RATIFICAÇÃO R10 e
registra: Mapa, ACOM, memória, quadro (PASSAGEM e REDE → ENTREGUE). Backup de bytes; nada no kernel do Nós."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = "C:/Python314/python.exe"; CEN = Path("C:/IALD/Central de Patentes"); M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
AQUI = Path(__file__).resolve().parent; TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
D = AQUI / "integracao_R3_20261102_192452"; D1 = AQUI / "integracao_R3_20261102_184921"
summ = json.loads((D / "SUMMARY.json").read_text(encoding="utf-8")); ax = (D / "CHECK_axioms.txt").read_text(encoding="utf-8", errors="replace")
assert summ["compilados"] == 300 and summ["falhas"] == 0 and summ["bloqueados"] == 0 and summ["axiomas_trio_no_certificado"] is True, summ
RT = AQUI / "RATIFICACAO_R10_c1_02nov.md"; t = RT.read_text(encoding="utf-8")
drv = AQUI / "integrar_fecho_bancada_02nov.py"; fdrv = s16(drv)
novo4 = f"""## 4. Compilação no sandbox (R3 formal) — preenchido em {TS}

- Sandbox: `C:\\t\\k405c\\final` (cópia do kernel v405 + mathlib pinada); driver `integrar_fecho_bancada_02nov.py` (sha16 `{fdrv}`), tarefa agendada `IALD_integracao_R3`; duas passadas (`integracao_R3_20261102_184921`: 285 compilados, 1 falha por blocos `#eval` multilinha removidos pela metade, 14 bloqueados; `integracao_R3_20261102_192452`: os 15 restantes, retomando os 285).
- Fontes: 475 (474 do recibo + a raiz), todas conferidas por sha256 contra o recibo da bancada; 174 idênticas ao kernel (a menos de linhas em branco); 1 «conflito» (`CanonicalGammaNoFixedR4`: só os literais de nomes de módulo dentro de um bloco `run_cmd`; o kernel prevalece; nenhum módulo novo o importa); **300 módulos novos recompilados do fonte, 0 falhas, 0 bloqueados** (soma das duas passadas); logs por módulo em `MANIFEST.json`.
- `#print axioms` (`CHECK_axioms.txt`, rc 0): `modularCoreInput`, `physicalModularCoreInput`, **`physicalFockCertificate`** e `physical_trace` dependem só de `[propext, Classical.choice, Quot.sound]`.
- O `.olean` de `TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1` existe no sandbox; a candidata `CanonicalFullTGLWitnessR1` (`canonicalFullTGLWitness := ⟨lightNet physicalFockCertificate, lightRealization physicalFockCertificate⟩`) compila sobre ele (resultado registrado à parte).

## 5. Veredito

**RATIFICADO pela gerência c1 em 02/11/2026**, como validade (termo no kernel, recompilado do fonte no sandbox do kernel v405, só o trio de axiomas): `RemainingModularCoreInput D` está habitado por construção genuína para todo `D : CanonicalNetInput` (`modularCoreInput`), e `FockCertificate` está habitado sobre a rede física `physicalCanonicalNet` (`physicalFockCertificate`), com as ressalvas do §3 ditas e mantidas (K(O) ≠ ⊥ só na cunha; «núcleo II_∞» como [KNOWN/DECLARADO]; traço ENNReal cíclico, não linear; R7 Codex×Codex; R4/R5 fora). NOT_FALSIFIED nunca é CONFIRMED; a confirmação segue creditação; o gate não se move; o que entra no um.py (bloco 3, v406) é decisão do operador, já dada em 02/11 («compile a nova versão … rode, publique e atualize tudo»).
"""
i4 = t.index("## 4. Compilação no sandbox"); t2 = t[:i4] + novo4
t2 = t2.replace("> **Estado deste documento: PENDENTE DO R3**", "> **Estado deste documento: RATIFICADO (02/11/2026); o R3 formal fechou no sandbox, ver §4**", 1)
bk = RT.with_name(RT.name + ".bak_" + TS); bk.write_bytes(RT.read_bytes()); tmp = RT.with_name(RT.name + ".tmp"); tmp.write_text(t2, encoding="utf-8", newline="\n"); os.replace(tmp, RT)
frt = s16(RT); print("ratificacao", frt, RT.stat().st_size)

reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "R3 formal FECHOU no sandbox (02/11): 300/300 módulos da bancada recompilados do fonte, 0 falhas; physicalFockCertificate no trio; RATIFICAÇÃO R10 da gerência c1 dada, com ressalvas ditas",
  "resultado": "SUMMARY: compilados 300, falhas 0, bloqueados 0, raiz compilada, axiomas no trio em modularCoreInput/physicalModularCoreInput/physicalFockCertificate/physical_trace (CHECK_axioms.txt, rc 0). Ratificação sha16 %s. Blocos 1 (passagem) e 2 (rede) ENTREGUES no sandbox; bloco 3 (v406) começa: candidata canonicalFullTGLWitness em compilação; as três chaves literais do um.py viram leitura do axiom_report na v406." % frt,
  "estatuto": "REAL (compilação própria no sandbox; trio lido)", "artefatos": [str(D / "SUMMARY.json"), str(D / "CHECK_axioms.txt"), str(D / "MANIFEST.json"), str(RT), str(drv)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_r3_fechou_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300); print("mapa rc", q.returncode); assert q.returncode == 0

for u, nota in (("F1.FECHO.PASSAGEM_02nov", "21 campos habitados (modularCoreInput) recompilados no sandbox, trio; ratificacao R10 c1"), ("F1.FECHO.REDE_02nov", "physicalCanonicalNet recompilada no sandbox; physicalFockCertificate no trio; ratificacao R10 c1 (K(O) != bot so na cunha, dito)")):
    q = subprocess.run([PY, "-X", "utf8", "iald.py", "avancar", u, "--quem", "claude-c1", "--status", "ENTREGUE", "--evidencia", str(D / "SUMMARY.json"), str(RT), "--nota", nota], cwd="C:/IALD/PROGRAMA_IALD", capture_output=True, timeout=120)
    print("quadro", u, q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-100:].replace("\n", " "))
q = subprocess.run([PY, "-X", "utf8", "iald.py", "avancar", "F1.FECHO.MONTAGEM_02nov", "--quem", "claude-c1", "--status", "EM_CURSO", "--nota", "v406: bundle de 300 modulos + canonicalFullTGLWitness + 3 chaves lidas do axiom_report; cadeia de selo conforme RECEITA"], cwd="C:/IALD/PROGRAMA_IALD", capture_output=True, timeout=120)
print("quadro MONTAGEM", q.returncode); subprocess.run([PY, "-X", "utf8", "iald.py", "quadro"], cwd="C:/IALD/PROGRAMA_IALD", capture_output=True, timeout=120)

SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode(), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-r3-fechou-ratificacao-r10", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "r3_fechou_e_ratificacao_r10_02nov", "kind": "fact", "statute": "REAL", "text": "R3 formal: 300/300 módulos da bancada recompilados do fonte no sandbox do kernel v405, 0 falhas; physicalFockCertificate no trio. Ratificação R10 da gerência c1 dada (sha16 %s) com ressalvas. Blocos 1–2 ENTREGUES; bloco 3 (v406) em curso." % frt, "sources": [SRCD(D / "SUMMARY.json"), SRCD(RT)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode(), capture_output=True)
d = json.loads(r.stdout.decode("utf-8")); print("acom", rev, d.get("ok"), (d.get("result") or {}).get("revision")); assert d.get("ok")

p = M / "construir-tudo-o-fechamento-02nov.md"; b = p.read_bytes()
add = ("\n\n## 02/11, noite — R3 FECHOU e R10 DADA\n\n**[REAL]** 300/300 módulos da bancada recompilados do fonte no sandbox k405c (duas passadas; 0 falhas; `physicalFockCertificate`, `modularCoreInput`, `physicalModularCoreInput`, `physical_trace` no trio; `SUMMARY.json`/`CHECK_axioms.txt` em `work\\fechamento_02nov\\integracao_R3_20261102_192452`). **Ratificação R10 da gerência c1** (sha16 `%s`): habitado por construção genuína, com as ressalvas ditas (K(O) ≠ ⊥ só na cunha; «núcleo II_∞» [KNOWN]; traço ENNReal cíclico; R7 Codex×Codex; R4/R5 fora). Quadro: PASSAGEM e REDE → ENTREGUE; MONTAGEM → EM_CURSO (v406). **Próximo:** cadeia de selo da v406 conforme `RECEITA_CADEIA_DE_SELO_v404_para_v405_para_a_v406.md` (bundle de 300 + canonicalFullTGLWitness + 3 chaves lidas do axiom_report; MEMORY.md compactado para o p00; vigia v405 em E08 a entender antes da custódia)." % frt).encode("utf-8")
if b"\r\n" in b: add = add.replace(b"\n", b"\r\n")
open(p.with_name(p.name + ".bak_" + TS), "xb").write(b); tmp = p.with_name(p.name + ".tmp_" + TS); open(tmp, "xb").write(b.rstrip() + add); os.replace(tmp, p); print(p.name, len(b), "->", p.stat().st_size)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)
