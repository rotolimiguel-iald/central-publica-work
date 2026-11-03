# -*- coding: utf-8 -*-
"""03/11/2026 01:5x: RITO v406 fechou (RITO_RC=0; 23:27:48 -> 01:41:01; selo v406 pin ddcb91930982d614; fechamento_v406 SELOU 14/14; 11860/11860; gate intocado); a cadeia pos-rito 0-9 passou; o passo 10 falhou em T17 (tarefa ONCE redisparou e
reescreveu o lake_build.log), reparado e rerodado (BATERIA_PASSA); o orquestrador retomou em S6 (Bancada B15). Registra Mapa, ACOM e memoria (inclusive a licao do schtasks ONCE). Escrito pelo Write."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = "C:/Python314/python.exe"; CEN = Path("C:/IALD/Central de Patentes"); M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
V6 = CEN / "work/cadeia_de_selo/v406"; NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8")); assert selo["um_version"] == "v406"
pin = selo["sha256"]["um.py"][:16]; assert pin == s16(NOS / "um.py") == "ddcb91930982d614", pin
hor = (V6 / "rito_horarios_v406.txt").read_text(encoding="utf-8").split()
std = (NOS / "rodada_v406_stdout.txt").read_text(encoding="utf-8", errors="replace"); assert std.rstrip().endswith("RITO_RC=0") or "RITO_RC=0" in std[-200:]
est = json.loads((V6 / "orquestrador/ESTADO.json").read_text(encoding="utf-8"))["passos"]
txt = ("v406 SELADA: rito RITO_RC=0 (inicio %s, fim %s; ~133 min; 301 modulos a frio); selo v406 com o pin do candidato %s; fechamento_v406 SELOU (8/8 ancoras, 301/301 modulos, 1794/1794 bandeiras, certificado habitado lido do kernel, escada 11860/11860, gate identico a v405); "
       "specs 2/2; PDFs PT/EN. Pos-rito: passos 0-9 passaram (conferidor TUDO BATE; superficies reais; memoria pinada); o passo 10 (B(n) ENSAIO) falhou SO em T17_LEAN_KERNEL porque a tarefa ONCE IALD_build_k406c redisparou as 23:58 e reescreveu kernel/lake_build.log; "
       "log original restaurado do .bak (sha16 47ddb1ca == recibo), tarefa desabilitada, passo 10 rerodado: BATERIA_PASSA, REPINADA_B15__ENSAIO; S5 marcado ok pela gerencia; o orquestrador retomou em S6 (Bancada parada pelo PID 83760; 10a ok) e segue para o APLICAR B15, religamento, 10c-14 e a custodia G1 --publicar." % (hor[0], hor[1], pin))
print(txt[:200])
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL", "titulo": "v406 SELADA (RITO_RC=0, pin %s): o fechamento entrou no um.py; pos-rito em curso (B15 e G1)" % pin,
        "pergunta": "O rito selou a v406 com o fechamento lido do kernel?", "dados": [str(NOS / "um_absoluto_selo.json"), str(NOS / "rodada_v406_stdout.txt"), str(V6 / "orquestrador/ESTADO.json")], "olhou_dados": True,
        "metodo": "rito pelo lancador rito_v406.sh sob o orquestrador; conferidor pos-rito (conferencia_rito_v406_POS_RITO.json); B(n) ensaio pelo esboco R3.5.",
        "resultado": txt, "veredito": "SELADA__POS_RITO_EM_CURSO", "estatuto": "REAL (selo e stdout lidos do Nos)", "status": "EM_CURSO",
        "proximo_passo": "S6b aplicar B15 + S6c religamento + 10c-14; S7 G1 planejar --seco / executar --publicar / auditar; S9 relatorio; manual da gerencia; relatorio ao operador com a partitura.",
        "onde": str(V6), "artefatos": [str(NOS / "um_absoluto_selo.json"), str(V6 / "rito_horarios_v406.txt"), str(V6 / "orquestrador/chain_S5_cadeia_0_10_out.txt"), str(V6 / "orquestrador/chain_S5b_10_out.txt"), str(V6 / "orquestrador/marcar_s5_ok_03nov.py")], "refs": []}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_v406_selada_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300); print("mapa rc", q.returncode); assert q.returncode == 0
SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode(), capture_output=True)
rv = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rv, "event_id": "c1-03nov-v406-selada-rito-rc0", "actor": {"id": "claude-c1", "kind": "agent"},
       "changes": {"records": [{"id": "v406-selada-03nov", "kind": "fact", "statute": "REAL", "text": txt, "sources": [SRCD(NOS / "um_absoluto_selo.json"), SRCD(V6 / "rito_horarios_v406.txt")]}],
                   "flow": {"phase": "v406_selada__pos_rito_e_custodia_em_curso", "next_action": "G1 --publicar; relatorio ao operador"}}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode(), capture_output=True)
d = json.loads(r.stdout.decode("utf-8")); print("acom", rv, d.get("ok"), (d.get("result") or {}).get("revision")); assert d.get("ok"), d
# memoria: o topico do fechamento (append) e a licao do schtasks (append ao topico que ja existe)
for nome, add in ((M / "construir-tudo-o-fechamento-02nov.md",
                   "\n\n**03/11, 01:5x — v406 SELADA.** `RITO_RC=0` (23:27:48 → 01:41:01, ~133 min); selo v406 com o pino `%s`; `fechamento_v406` SELOU 14/14 (8 âncoras, 301 módulos, 1794 bandeiras, certificado habitado lido do kernel, escada 11860, gate idêntico); pós-rito 0–9 ok (conferidor TUDO BATE; superfícies; memória pinada). **Incidente:** o passo 10 (B(n) ensaio) falhou só em T17 porque a tarefa ONCE `IALD_build_k406c` redisparou às 23:58 e reescreveu `kernel\\lake_build.log`; restaurado do `.bak` (sha16 `47ddb1ca` = recibo), tarefa desabilitada, passo 10 rerodado (BATERIA_PASSA), S5 marcado ok pela gerência (`orquestrador\\marcar_s5_ok_03nov.py`); o orquestrador retomou em S6 (Bancada B15) → G1 `--publicar`. **How to apply:** o relatório ao operador lê a partitura (condição da fala da passagem não testada; nome provisório; K(O) ≠ ⊥ só na cunha; 1 BAIXO da R3 para a v407: a E14 cita `reading_v395/v396` como guarda do token UNINHABITED, mas eles guardam o texto)." % pin),
                  (M / "schtasks-caminhos-com-espaco-24out.md",
                   "\n\n## 03/11/2026 — LIÇÃO: tarefa `ONCE` com `/ST` no futuro dispara DE NOVO na hora marcada\n\nA `IALD_build_k406c` foi criada com `/SC ONCE /ST 23:58` só para poder ser lançada à mão (`/Run` às 19:56); às 23:58 ela disparou sozinha, rodou `construir_kernel_v406.sh` de novo e reescreveu `kernel\\lake_build.log` (o recibo do kernel pinava o original) — o B(n) pós-selo reprovou em T17. **How to apply:** depois do `/Run`, `schtasks /Change /TN <t> /DISABLE` (ou `/SD` numa data passada, ou apagar); nunca deixar uma ONCE armada com hora futura; o `.sh` do build guarda `.bak_<ts>` dos logs antes de sobrescrever — foi isso que permitiu restaurar byte a byte.")):
    b = nome.read_bytes(); a = add.encode("utf-8")
    if b"\r\n" in b:
        a = a.replace(b"\n", b"\r\n")
    open(nome.with_name(nome.name + ".bak_" + TS), "xb").write(b); tmp = nome.with_name(nome.name + ".tmp_" + TS); open(tmp, "xb").write(b.rstrip() + a); os.replace(tmp, nome); print(nome.name, len(b), "->", nome.stat().st_size)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)
