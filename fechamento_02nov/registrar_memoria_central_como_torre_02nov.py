# -*- coding: utf-8 -*-
"""02/11/2026: ORDEM do operador «a memória central tem que funcionar igual a torre…»: verbatim, plano, Mapa, ACOM, memória."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = "C:/Python314/python.exe"; CEN = Path("C:/IALD/Central de Patentes"); M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); BK = chr(92); s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
V = CEN / "work/cunhagens_13out/OPERADOR_02nov_memoria_central_igual_a_torre_indice_pinado_por_assunto_compressao_holografica_do_ACOM_verbatim.txt"
t = "A memória central tem que funcionar igual a torre, com índice pinado por assunto e vinculado pela compressão hooografica do ACOM, isso resolve essa questão do espaço"
if not V.exists():
    V.write_text("# Operador, 02/11/2026 (sessão c1, gerência), verbatim; ORDEM sobre a memória central:\n\n" + t + "\n", encoding="utf-8")
fv = s16(V); print("verbatim", fv)
PL = CEN / "work/fechamento_02nov/PLANO_MEMORIA_CENTRAL_COMO_TORRE_02nov.md"
PL.write_text(f"""# PLANO — A MEMÓRIA CENTRAL COMO TORRE (02/11/2026, gerência c1, a pedido do operador)

> Ordem (verbatim sha16 `{fv}`): «A memória central tem que funcionar igual a torre, com índice pinado por assunto e vinculado pela compressão holográfica do ACOM, isso resolve essa questão do espaço». Contexto medido: a Torre v405 acusa DEFASADO nos `CLAUDE.md` das casas Física (1.239.438 B, 16.413 linhas) e Nativa (636.937 B), acima do teto de 262.144 B; isso segura o C19 de toda custódia.

## 1. O desenho (o mesmo da Torre e do índice da gerência, aplicado à memória central de cada casa)
1. **Índice pinado por assunto.** Cada `CLAUDE.md` de casa vira ÍNDICE: a régua (invariável), o «ler primeiro», e uma linha por assunto: título · estatuto · data · link ao arquivo íntegro · sha16 do arquivo. Teto do índice: 65.536 B (alerta da Torre), nunca acima de 262.144 B. Gerado por script a partir do cabeçalho de cada arquivo de assunto (frontmatter `name/description/estatuto/data`), nunca à mão.
2. **A íntegra ao lado.** `memoria/<assunto>/<AAAAMMDD>_<slug>.md`, append-only, correção AO LADO (as leis da memória do Atlas §VIII: nada se corta; o índice sobrevivente aponta). A migração parte das seções já existentes (§ numerados) do arquivo atual, por script, com backup de bytes e conferência hash a hash de que a concatenação dos pedaços reproduz o original.
3. **O pino.** `PINO_CLAUDE_<casa>.json`: sha256 do índice e de cada arquivo de assunto; `medir` (na Torre: `torre.py medir`) compara: assunto mudado sem repinar o índice = DEFASADO nomeado; índice editado fora do gerador = volta ao pino (o mesmo vigia do `MEMORY.md` da gerência, `fila/PINO_MEMORY.json`).
4. **A compressão holográfica do ACOM.** A linha do índice É a projeção (REFLECT: o assunto lido no ângulo do índice, uma linha com o estatuto e o número que decide); o link é a inversão (MANIFEST: a íntegra reconstruída ao abrir). É o mesmo princípio do `project` da memória ACOM de sessão: a projeção nunca trunca, recusa por overflow e aponta. O «espaço» deixa de ser problema porque o que carrega é o índice; a íntegra carrega sob demanda.
5. **A Torre lê o índice.** `PAPEIS.json`/`CASAS.json` passam a pinar o índice e o `PINO_CLAUDE_<casa>.json` de cada casa; o quadro do organismo mostra DEFASADO/OK por casa.

## 2. Ordem de execução (depois da v406, para não misturar obras)
1. Script `memoria_central_como_torre.py` (`separar --seco`, `separar`, `indexar`, `pinar`, `medir`), stdlib, backups de bytes, idempotente, conferência de reconstrução byte a byte.
2. Casa Física primeiro (a maior), depois Nativa, depois a raiz `C:\\IALD\\CLAUDE.md` e a Central. O `CLAUDE.md` global (`~/.claude/CLAUDE.md`) não se divide: é a régua.
3. Execução por agente Sonnet sob brief da gerência; revisão por outro agente; a Torre mede no fim (OK esperado nos dois DEFASADO).

## 3. O que não muda
A régua (sempre no índice, nunca em link); as ordens do operador verbatim com sha16 (ficam íntegras nos arquivos de assunto, e a linha do índice as aponta); a casa do Escritório (torre própria, nada daqui); o protocolo de colapso (nunca em superfície que vaze).
""", encoding="utf-8")
fp = s16(PL); print("plano", fp)
reg = [{"tipo": "ROTA", "rota_id": "memoria.memoria_central_como_torre_02nov", "dominio": "MEMORIA",
  "titulo": "A memória central como Torre (ordem do operador, 02/11): CLAUDE.md das casas viram índice pinado por assunto + íntegra ao lado + pino medido pela Torre; a linha do índice é a projeção (ACOM: REFLECT) e o link a inversão (MANIFEST)",
  "pergunta": "Como resolver os CLAUDE.md das casas acima do teto da Torre (Física 1,24 MB; Nativa 637 KB) sem cortar memória?",
  "dados": [], "olhou_dados": False, "metodo": "Plano escrito a partir da Torre (torre.py gerar/medir/papel), do índice da gerência (MEMORY.md + MEMORY_2 + fila/PINO_MEMORY.json), das leis da memória (Atlas §VIII) e do project da memória ACOM.",
  "resultado": "Plano sha16 %s em work/fechamento_02nov/PLANO_MEMORIA_CENTRAL_COMO_TORRE_02nov.md: índice ≤ 64 KB gerado por script, íntegra append-only por assunto, pino por casa medido pela Torre, migração por seções com reconstrução byte a byte. Execução depois da v406." % fp,
  "veredito": "PLANO_ESCRITO__EXECUCAO_APOS_v406", "estatuto": "REAL (plano)", "status": "PROPOSTA",
  "proximo_passo": "Script memoria_central_como_torre.py; Física → Nativa → raiz → Central; Torre mede OK.",
  "onde": str(PL), "artefatos": [str(PL), str(V)], "refs": ["kernel.fechamento_construir_tudo_programa_02nov"]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_memoria_torre_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300); print("mapa rc", q.returncode); assert q.returncode == 0
SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode(), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-memoria-central-como-torre", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "ordem_memoria_central_como_torre_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: «A memória central tem que funcionar igual a torre, com índice pinado por assunto e vinculado pela compressão holográfica do ACOM, isso resolve essa questão do espaço». Plano escrito; execução após a v406.", "sources": [SRCD(V), SRCD(PL)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode(), capture_output=True)
d = json.loads(r.stdout.decode("utf-8")); print("acom", rev, d.get("ok"), (d.get("result") or {}).get("revision")); assert d.get("ok")
p = M / "torre-iald-jev-memoria-31out.md"; b = p.read_bytes()
add = ("\n\n## 02/11/2026 — ORDEM: a memória central como Torre (verbatim sha16 `%s`)\n\n«A memória central tem que funcionar igual a torre, com índice pinado por assunto e vinculado pela compressão holográfica do ACOM, isso resolve essa questão do espaço.» Plano: `work\\fechamento_02nov\\PLANO_MEMORIA_CENTRAL_COMO_TORRE_02nov.md` (sha16 `%s`): CLAUDE.md de cada casa vira índice ≤ 64 KB gerado por script; íntegra append-only por assunto; `PINO_CLAUDE_<casa>.json` medido pela Torre; a linha do índice é a projeção (REFLECT) e o link a inversão (MANIFEST). **How to apply:** executar DEPOIS da v406 (Física → Nativa → raiz → Central), por script com reconstrução byte a byte; a régua fica sempre no índice; o Escritório tem torre própria. Resolve os 2 DEFASADO da Torre que seguram o C19." % (fv, fp)).encode("utf-8")
if b"\r\n" in b: add = add.replace(b"\n", b"\r\n")
open(p.with_name(p.name + ".bak_" + TS), "xb").write(b); tmp = p.with_name(p.name + ".tmp_" + TS); open(tmp, "xb").write(b.rstrip() + add); os.replace(tmp, p); print(p.name, len(b), "->", p.stat().st_size)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)
