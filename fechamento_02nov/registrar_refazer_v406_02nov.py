# -*- coding: utf-8 -*-
"""02/11/2026, 21:5x: o refazer da v406 fechou (candidato fe33b019b4f06494; ensaio TUDO PASSOU; conferidor negativo nao bate / positivo bate; citacoes conferem; p00 106 ok, 0 falhas, 3 pendentes do B(n)). Registra: Mapa (anotacao), ACOM (a referencia da
preparacao, rev 1 -> 2), memoria (append curto). Backup de bytes. Escrito pelo Write (nao por heredoc)."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = "C:/Python314/python.exe"; CEN = Path("C:/IALD/Central de Patentes"); M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
V6 = CEN / "work/cadeia_de_selo/v406"
cand = json.loads((V6 / "CANDIDATO_v406.json").read_text(encoding="utf-8")); assert cand["sha16"] == s16(V6 / "um_v406_candidato.py")
pre = json.loads((V6 / "PRECONDICOES_v406.json").read_text(encoding="utf-8")); ch = pre["checagens"]
n_ok = sum(1 for c in ch if c.get("ok") is True); n_f = [c["checagem"][:60] for c in ch if c.get("ok") is False]; n_p = sum(1 for c in ch if c.get("ok") is None)
ens = (V6 / "ensaio_out.txt").read_text(encoding="utf-8", errors="replace").rstrip().splitlines()[-1]
assert not n_f and "TUDO PASSOU" in ens, (n_f, ens)
txt = ("v406: refazer fechado sobre o candidato %s (42,7 MB; 32 patches): comparar ok (28 nos mudados com explicacao, 0 removidos, 15 novos); ensaio a seco TUDO PASSOU (fechamento_v406 14/14; as quatro chaves lidas do kernel = True; rede_fock_v394 com a troca dita; escada 11860; gate identico); "
       "ESPERADOS gerados; conferidor: negativo nao bate / positivo TUDO BATE; citacoes conferem; DIFF_v405_v406 e PINOS_BN; conferencia do instalar/rito 83 invariantes; p00 %d ok, 0 falhas, %d pendentes (o B(n) pre-selo). Revisao de terceiro (Sonnet) lancada; pos-rito e bateria em adaptacao." % (cand["sha16"], n_ok, n_p))
print(txt[:200])
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL", "titulo": txt[:220], "pergunta": "O candidato v406 passa a cadeia antes do rito?",
        "dados": [str(V6 / "ensaio_a_seco_v406.json"), str(V6 / "PRECONDICOES_v406.json"), str(V6 / "ESPERADOS_v406.json"), str(V6 / "conferir_citacoes_v406.json")], "olhou_dados": True,
        "metodo": "refazer_candidato_v406.sh --regerar (gerador, comparar AST, ensaio a seco emulado, esperados, conferidor negativo/positivo, citacoes verbatim, diff e pinos, conferencia do instalar/rito, p00).",
        "resultado": txt, "veredito": "CADEIA_PRE_RITO_VERDE__B_N_PRE_SELO_E_REVISAO_PENDENTES", "estatuto": "REAL (medido pelos scripts da cadeia; o selo so' depois do rito)", "status": "EM_CURSO",
        "proximo_passo": "B(n) pre-selo (B15) -> gerar_relatorio (PRONTA) -> revisao de terceiro aprovada -> fechar_preparacao -> orquestrador (instalar, rito, pos-rito, G1 --publicar).",
        "onde": str(V6), "artefatos": [str(V6 / "CANDIDATO_v406.json"), str(V6 / "ensaio_a_seco_v406.json"), str(V6 / "PRECONDICOES_v406.json"), str(V6 / "refazer_out_v406.txt")], "refs": []}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_v406_refazer_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300); print("mapa rc", q.returncode); assert q.returncode == 0
SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(V6 / "SESSION_REFERENCE_prep_v406.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode(), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "prep-v406-refazer-verde-02nov", "actor": {"id": "claude-c1", "kind": "agent"},
       "changes": {"records": [{"id": "prep-v406-refazer-verde", "kind": "fact", "statute": "REAL", "text": txt, "sources": [SRCD(V6 / "CANDIDATO_v406.json"), SRCD(V6 / "ensaio_a_seco_v406.json"), SRCD(V6 / "PRECONDICOES_v406.json")]}],
                   "flow": {"phase": "preparacao_v406__pre_rito_verde__b_n_e_revisao_pendentes", "next_action": "B(n) pre-selo; gerar_relatorio (PRONTA); revisao de terceiro; fechar_preparacao; orquestrador"}}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode(), capture_output=True)
d = json.loads(r.stdout.decode("utf-8")); print("acom prep", rev, d.get("ok"), (d.get("result") or {}).get("revision")); assert d.get("ok"), d
p = M / "construir-tudo-o-fechamento-02nov.md"; b = p.read_bytes()
add = ("\n\n**02/11, 21:5x — v406: cadeia pré-rito VERDE.** Candidato vigente `%s` (o `2763d152…` foi regenerado por uma citação entre « » que era paráfrase; regra: a fala do operador verbatim ou nada). Ensaio a seco TUDO PASSOU; conferidor negativo não bate / positivo bate; citações conferem; p00 %d ok, 0 falhas, 3 pendentes (B(n) pré-selo, B15). Lições: offsets do `ast` são em BYTES (docstring com acentos cortou um byte); `full_static_witness_exists` mora em `qg_closure.gate`; o heredoc do Bash colapsa `\\\\` (escrever scripts pelo Write); a origem de um insumo pinado não se edita depois da cópia (o MEDIDO do DESENHO foi para `DESENHO_v406_MEDIDO_02nov.md`). Orquestrador `pos_treino_v406.py` adaptado (tarefa `IALD_pos_treino_v406`, DESABILITADA até a preparação fechar); Bancada religada (pid 83760) com recibo. **How to apply:** depois do B(n) e da revisão do Sonnet aprovada: `gerar_relatorio_v406.py` → `fechar_preparacao_v406.py` → habilitar e rodar a tarefa do orquestrador; vigiar S4 (rito, 2–4 h)." % (cand["sha16"], n_ok)).encode("utf-8")
if b"\r\n" in b:
    add = add.replace(b"\n", b"\r\n")
open(p.with_name(p.name + ".bak_" + TS), "xb").write(b); tmp = p.with_name(p.name + ".tmp_" + TS); open(tmp, "xb").write(b.rstrip() + add); os.replace(tmp, p); print(p.name, len(b), "->", p.stat().st_size)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)
