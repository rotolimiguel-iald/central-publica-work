# -*- coding: utf-8 -*-
"""03/11/2026 06:3x, gerencia c1: transicao ACOM da referencia da gerencia (etapa material concluida: custodia v406 PUBLICADA; t3 aberto), no molde do pedido de 28/10.
Projeta antes para ler a revisao corrente (CAS); registros com fonte por sha256 e estatuto; fluxo com fase e proxima acao. Pedido e recibo gravados ao lado. Escrito pelo Write."""
import hashlib, json, subprocess, time
from pathlib import Path
PY = r"C:\Python314\python.exe"; SM = r"C:\IALD\MEMORIA_IALD\session_memory.py"
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
W = Path(r"C:\IALD\Central de Patentes\work\custodia_v406_03nov"); TS = time.strftime("%Y%m%dT%H%M%S")


def sm(payload):
    q = subprocess.run([PY, "-X", "utf8", SM], input=json.dumps(payload, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    raw = (q.stdout + q.stderr).decode("utf-8", "replace")
    return json.loads(raw)


def art(p):
    p = Path(p); return {"kind": "artifact", "ref": "%s#sha256:%s" % (str(p), hashlib.sha256(p.read_bytes()).hexdigest())}


proj = sm({"operation": "project", "reference": REF}); assert proj.get("ok"), proj
rev = proj["result"]["receipt"]["revision"]; print("revisao corrente:", rev)
CEN = r"C:\IALD\Central de Patentes"
pedido = {
    "operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev,
    "event_id": "c1-03nov-v406-custodia-publicada-t3-aberto",
    "changes": {
        "records": [
            {"id": "c1-v406-custodia-publicada-03nov", "kind": "fact", "statute": "REAL",
             "text": ("v406 ddcb91930982d614 PUBLICADA em 03/11/2026: the_boundary a381c4d1 = origin/main; Central 42f3b0c9 = origin/main; site v406 no ar (subidas verificadas 20261103_025919 e "
                      "20261103_055922); Central publica 22/22 no quadro das 06:10; leitor de IA R1; conferencia final 13/13; ACOM t1/t2 da custodia; rota custodia.v406; Nos vivo; TORRE_v406.json; "
                      "auditar rc 0. Orquestrador pos_treino_v406 S0-S8 ok (S5, S6c e S7 com decisao da gerencia dita na ESTADO.json); tarefa desabilitada. G1: 37 passos aplicados; "
                      "C19 parou na classificacao do quadro: 7 DEFASADOS fora desta custodia (ACTIVE.json v404 e DELIVERY v406: so o Codex, sem cota ate 04/11 06:37; JEV v406 nasce com a release do app, "
                      "C21, decisao do operador; Torre: CLAUDE.md de Haja_Luz e da Nativa acima do teto de 262.144 B; missao ACOM de 12/10 recusada pelo guarda). t3 aberto, como na v405. "
                      "Validade no kernel nao e' creditacao; gate intocado; NOT_FALSIFIED nunca e' CONFIRMED."),
             "sources": [art(CEN + r"\work\cadeia_de_selo\v406\orquestrador\ESTADO.json"), art(CEN + r"\work\custodia_G1\runs\v406_20261103_055852\RELATORIO.json"),
                         art(r"C:\IALD\Site\tgl\v3.0_bancada\subidas\20261103_055922\RELATORIO.md"), art(CEN + r"\organismo\ESTADO_DO_ORGANISMO.json")]},
            {"id": "c1-v406-sete-paradas-consertadas-ao-lado-03nov", "kind": "fact", "statute": "REAL",
             "text": ("A G1 parou sete vezes na custodia v406 e a gerencia consertou AO LADO, com backup de bytes e conferencia rodando a ferramenta: prosa do handoff (43), rev1 da semantica com "
                      "mudados_permitidos para rede_fock_v394 (44), EXCL_RAIZ e sufixo do C8 em central.py (45-46), estacao witness_layers_v367 do runner (47), camadas v395/v396 do modulo dos 16 (48), "
                      "o Range do hospedeiro em subir_site.py (49) e a ordem das pernas na retomada em site.py (50). Licoes 43-50 no livro da G1."),
             "sources": [art(CEN + r"\work\custodia_G1\LICOES_v400_25out.md"), art(CEN + r"\work\custodia_v406_03nov\RECIBO_SEMANTICA_REV1_v406.json"),
                         art(CEN + r"\work\custodia_v406_03nov\RECIBO_ERRATA_SUBIR_SITE_RANGE_v406.json")]},
            {"id": "c1-hospedeiro-range-intermitente-03nov", "kind": "fact", "statute": "REAL",
             "text": ("O hospedeiro do site (nginx/1.24, Lw-X-Id) respondeu 200 (arquivo inteiro) a pedidos Range em 03/11/2026 05:35 nos mesmos caminhos que em 02/11 03:54 respondiam 206, com "
                      "bytes e sha256 iguais aos locais e .htaccess identico; a subida 20261103_052210 (86 arquivos integros) foi revertida e o ar ficou incoerente (site v406, Central v405) ate' 06:09; "
                      "medido depois: o 206 oscila para 200 em pedidos consecutivos no mesmo no'. Parede do hospedeiro, nao dos arquivos. A subida 20261103_055922 (83 arquivos) saiu com 0 avisos. "
                      "Avisar a Locaweb e' decisao do operador; a frase «this site answers 206 (measured)» do read-brief.md fica a conferir."),
             "sources": [art(r"C:\IALD\Site\tgl\v3.0_bancada\subidas\20261103_052210\RELATORIO.md"), art(r"C:\IALD\Site\tgl\v3.0_bancada\subidas\20261102_035422\RELATORIO.md"),
                         art(CEN + r"\work\custodia_v406_03nov\RECIBO_ERRATA_SUBIR_SITE_RANGE_v406.json")]},
            {"id": "c1-memoria-triada-03nov", "kind": "fact", "statute": "REAL",
             "text": ("Fila da memoria triada pela gerencia em 03/11/2026 06:01: linha da custodia v406 no indice trocada para PUBLICADA (ato manual, backup de bytes, re-pinada); 15 depositos "
                      "promovidos (9 da custodia v406, 4 das patentes de 02/11 — a regra «as patentes sao lidas em conjunto» ganhou topico e linha no indice —, release v405 do app, preparacao da v406); "
                      "topico licoes-custodia-v406-03nov criado; verificar ok."),
             "sources": [art(CEN + r"\work\custodia_v406_03nov\RECIBO_TRIAGEM_FILA_03nov.json")]},
        ],
        "flow": {"phase": "custodia_v406_publicada__t3_aberto__codex_sem_cota_ate_04nov_0637__gates_do_operador",
                 "next_action": ("04/11 06:37: ler a cota do Codex; se houver, despacho unico F0.3 (work\\custodia_v406_03nov\\DESPACHO_CODEX_F03_v406.md) e depois `custodiar.py executar --versao v406 "
                                 "--publicar` para C19/C20/C17C. Do operador: nomes das pedras (CanonicalFullTGLWitnessR1), D2 [LEGAL], README pinado com o 4,44 (D39; nunca sozinho), D34-D40, "
                                 "release do app v406 (C21), motor continuo da v407 com pre-registro, Locaweb/Range. Nada de fisica nova sem ordem; gate intocado.")},
    },
}
(W / ("acom_c1_%s_transition.request.json" % TS)).write_text(json.dumps(pedido, ensure_ascii=False, indent=1), encoding="utf-8")
r = sm(pedido)
(W / ("acom_c1_%s_transition.receipt.json" % TS)).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
print("transition ok:", r.get("ok"), "| recibo:", json.dumps((r.get("result") or {}).get("receipt") or r, ensure_ascii=False)[:400])
assert r.get("ok"), r
