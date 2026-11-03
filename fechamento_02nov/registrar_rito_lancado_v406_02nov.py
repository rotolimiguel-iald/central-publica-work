# -*- coding: utf-8 -*-
"""02/11/2026, 23:3x: revisao de terceiro APROVADA (R3, Sonnet: 0 ALTO, 0 MEDIO, 1 BAIXO) sobre o candidato ddcb91930982d614; preparacao PRONTA (17 portoes) e FECHADA; o orquestrador instalou o candidato no Nos (S3) e lancou o rito (S4) as 23:27.
Registra: Mapa (anotacao, inclusive as rotas examinadas pelo revisor, que nao escreve no Mapa), ACOM (referencia da gerencia e da preparacao), memoria (append curto). Backup de bytes. Escrito pelo Write."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = "C:/Python314/python.exe"; CEN = Path("C:/IALD/Central de Patentes"); M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
V6 = CEN / "work/cadeia_de_selo/v406"; NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
rev = json.loads((V6 / "revisao_terceiro/REVISAO_TERCEIRO_v406.json").read_text(encoding="utf-8")); assert rev["aprovada"] is True
pr = json.loads((V6 / "PREPARACAO_v406_PRONTA.json").read_text(encoding="utf-8")); assert pr["pronta"] is True and pr["candidato_sha16"] == rev["candidato_sha16"]
um_nos = s16(NOS / "um.py"); assert um_nos == rev["candidato_sha16"], (um_nos, rev["candidato_sha16"])
est = json.loads((V6 / "orquestrador/ESTADO.json").read_text(encoding="utf-8")); passos = est["passos"]
assert passos.get("S3_instalar", {}).get("ok") is True
txt = ("v406: revisao de terceiro APROVADA na R3 (Sonnet; R1: 1 ALTO + 3 MEDIO corrigidos; R2: 1 MEDIO nos textos corrigido; R3: 0/0/1 BAIXO para a proxima versao) sobre o candidato %s; preparacao PRONTA (17 portoes) e fechada (marcador %s); "
       "o orquestrador pos_treino_v406 (tarefa IALD_pos_treino_v406) passou S0-S2, INSTALOU o candidato no Nos (S3, recibo %s; um.py do Nos = %s) e lancou o rito v406 (S4) as %s; estimativa 2 a 4 h (301 modulos a frio: build 1736 s no sandbox); depois: pos-rito 0-14 com a Bancada (B15) e a custodia G1 --publicar."
       % (rev["candidato_sha16"], s16(V6 / "PREPARACAO_v406_PRONTA.json"), passos["S3_instalar"].get("recibo"), um_nos, passos["S3_instalar"].get("quando")))
print(txt[:220])
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL", "titulo": txt[:230], "pergunta": "A v406 esta' instalada e o rito em curso?",
        "dados": [str(V6 / "revisao_terceiro/REVISAO_TERCEIRO_v406.json"), str(V6 / "PREPARACAO_v406_PRONTA.json"), str(V6 / "orquestrador/ESTADO.json")], "olhou_dados": True,
        "metodo": "revisao de terceiro em tres rodadas (PEDIDO_REVISAO_v406.md; revisor Sonnet, outra instancia; rotas examinadas: %s); gerar_relatorio (17 portoes); fechar_preparacao; orquestrador (S0 treino DONE, S1 PRONTA, S1b revisao, S2 pre-voo, S3 instalar, S4 rito)." % "; ".join(str(r)[:80] for r in (rev.get("rotas_examinadas") or [])[:8]),
        "resultado": txt, "veredito": "INSTALADO__RITO_EM_CURSO", "estatuto": "REAL (lido do ESTADO do orquestrador e do Nos); o selo so' depois do rito", "status": "EM_CURSO",
        "proximo_passo": "esperar RITO_RC=0 e o selo v406 com o pin do candidato; pos-rito 0-14; G1 --publicar; manual da gerencia; relatorio ao operador com a partitura (a condicao da fala da passagem nao foi testada; o nome da candidata e' provisorio).",
        "onde": str(V6), "artefatos": [str(V6 / "revisao_terceiro/REVISAO_TERCEIRO_v406.json"), str(V6 / "revisao_terceiro/REVISAO_TERCEIRO_v406.md"), str(V6 / "PREPARACAO_v406_PRONTA.json"), str(V6 / "RELATORIO_PREPARACAO_v406.md")], "refs": []}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_v406_rito_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300); print("mapa rc", q.returncode); assert q.returncode == 0
SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
for REF, ev in ((str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK), "c1-02nov-v406-instalada-rito-em-curso"), (str(V6 / "SESSION_REFERENCE_prep_v406.json").replace("/", BK), "prep-v406-rito-lancado")):
    g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode(), capture_output=True)
    rv = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
    req = {"operation": "transition", "reference": REF, "expected_revision": rv, "event_id": ev, "actor": {"id": "claude-c1", "kind": "agent"},
           "changes": {"records": [{"id": ev + "-fato", "kind": "fact", "statute": "REAL", "text": txt, "sources": [SRCD(V6 / "revisao_terceiro/REVISAO_TERCEIRO_v406.json"), SRCD(V6 / "PREPARACAO_v406_PRONTA.json")]}],
                       "flow": {"phase": "v406_instalada__rito_em_curso", "next_action": "RITO_RC=0 -> pos-rito 0-14 (Bancada B15) -> G1 --publicar -> relatorio ao operador"}}}
    r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode(), capture_output=True)
    d = json.loads(r.stdout.decode("utf-8")); print("acom", REF[-40:], rv, d.get("ok"), (d.get("result") or {}).get("revision")); assert d.get("ok"), d
p = M / "construir-tudo-o-fechamento-02nov.md"; b = p.read_bytes()
add = ("\n\n**02/11, 23:3x — v406 INSTALADA no Nós; rito em curso.** Revisão de terceiro (Sonnet) APROVADA na R3 (R1: 1 ALTO + 3 MÉDIO; R2: 1 MÉDIO nos textos; todos corrigidos; sobra 1 BAIXO: a E14 cita `reading_v395/v396` como guarda do token UNINHABITED, mas eles guardam o texto; corrigir na v407). Candidato final **`%s`**; preparação PRONTA (17 portões: kernel, candidato, AST, ensaio, conferidor ×2, citações, guarda de frases, instalar/rito estático, p00, B(n) pré-selo B15, serviço estático 36/36, dois harnesses, refazer limpo, purga ×2) e fechada; `pos_treino_v406.py` (tarefa `IALD_pos_treino_v406`) instalou às 23:27 (recibo `%s`) e lançou o rito (S4). **How to apply:** vigiar `orquestrador\\orquestrador.log` ([S4_rito] e seguintes) e `Nós\\rodada_v406_stdout.txt` (RITO_RC=0); se parar, nada se restaura sozinho: a gerência decide; ao fim, o relatório ao operador lê a partitura: a condição da fala da passagem («se funcionar sob compressão…») NÃO foi testada; o nome `CanonicalFullTGLWitnessR1` é provisório; K(O) ≠ ⊥ só na cunha." % (rev["candidato_sha16"], passos["S3_instalar"].get("recibo"))).encode("utf-8")
if b"\r\n" in b:
    add = add.replace(b"\n", b"\r\n")
open(p.with_name(p.name + ".bak_" + TS), "xb").write(b); tmp = p.with_name(p.name + ".tmp_" + TS); open(tmp, "xb").write(b.rstrip() + add); os.replace(tmp, p); print(p.name, len(b), "->", p.stat().st_size)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)
