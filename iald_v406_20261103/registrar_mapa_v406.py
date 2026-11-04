# -*- coding: utf-8 -*-
"""Mapa de Rotas (ORDEM_004 secao 4): registra a ROTA e o RESULTADO de `app.release.v406` (nova) e da parada no gate da F0.3.
Numeros lidos dos artefatos por script. O registrador exige ROTA antes de RESULTADO. Uso: registrar_mapa_v406.py"""
import hashlib
import json
import subprocess
from pathlib import Path

PY = r"C:\Python314\python.exe"
W = Path(__file__).resolve().parent
OUT = W / "registros_fechamento"
OUT.mkdir(exist_ok=True)
F03 = Path(r"C:\IALD\Central de Patentes\work\scientific_memory_sync_20261103_v406\RECIBO_PARADA_NO_GATE_v406.json")
QUEM = "claude-app-orquestrador"
rd = lambda p: json.loads(Path(p).read_bytes())
m = rd(W / "BUILDER_MEASUREMENTS.json")
rv = rd(W / "validation/review_final.json")
pb = rd(W / "app/PREPARED_BINDING.json")
plan = rd(W / "install_plan.json")
busca = (W / "BUSCA_EXERCITADA_v406.txt").read_text(encoding="utf-8").strip().splitlines()[-1]
pk = m["packages"]
jev = rd(W / "app/science/memory_stage/manifest_install.json")["jev_control"]
f03 = rd(F03)
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
art = [str(W / n) for n in ("install_plan.json", "validation/review_final.json", "validation/review_app_independent.json", "validation/review_sources.json",
                             "review/revisor_sonnet-app-v406-revisor/PARECER_v406_R1.md", "LICOES_v406.md", "BUILDER_MEASUREMENTS.json", "BUSCA_EXERCITADA_v406.txt",
                             "app/DELIVERY_PREPARED.json", "app/science/memory_stage/jev_control_v406.json", "CUSTODIA_v406_ESTADO.json", "COPIA_DA_V405.json")]

rota = {
    "tipo": "ROTA", "rota_id": "app.release.v406", "dominio": "APP",
    "titulo": "release v406 do app: janela P2 do shared deslizada com os literais mantidos, R3-1 e R3-2; construida e aceita, nao instalada",
    "pergunta": "A release v406 cabe nos pacotes do app com a janela P2 deslizada sem perder limites/diz/nao_diz, e o que falta para instalar?",
    "dados": ["um.py v406 (pin %s) no espelho the_boundary, commit %s" % (m["release"]["um_py_sha256"][:16], m["release"]["espelho_commit"][:8]), "app instalado %s" % m["installed_release"]],
    "metodo": "so' as ferramentas da v405 (24 arquivos, COPIA_DA_V405.json); R3-1 (KEEP_FLAG sem delimitadores), R3-2 (max_chars 4500 na receita), janela P2 (SHARED_P2_SUFFIXES _v402.._v406; _v401 aposentado com limites/diz/nao_diz mantidos por fit_memory.compact(literal_suffixes)); prepare e finalize offline; contagem nativa (6 pedidos, 0 geracao); validate_plan; busca exercitada; revisor independente sonnet-app-v406-revisor (Q1-Q8) aceitou na rodada 1",
    "resultado": "shared %d B, folga minima declarada %d B (DeepSeek, reserva 148656); haiku55 folga %d tokens (v405: 172998); %d topicos, novos %s; catalogo %d TRUE, 16 nomes voltam ao literal; plano de %d arquivos, 0 .py de runtime, destino %s; jev_control_v406 sha256 %s; revisao: %s com %d checks mecanicos, 0 ALTO/MEDIO, 5 BAIXOS; %s" % (
        pk["shared"]["prefix_bytes"], m["menor_folga_declarada_bytes"], pk["haiku_expanded"]["remaining_tokens"], m["topics"]["core"], m["topics"]["new_v406"],
        m["kernel_formalization"]["catalog"]["true_fields"], len(plan["files"]), pb["target"], jev["sha256"][:16], rv["status"], len(rv["checks"]), busca),
    "veredito": "APP_V406_CONSTRUIDO_E_ACEITO_NAO_INSTALADO", "estatuto": "REAL", "status": "EM_CURSO", "olhou_dados": False,
    "defeito": "nao instalada: deploy_controlled.py acopla instalacao e reinicio do filho web (porta 8082) e a ORDEM_004 reserva o reinicio ao operador; BAIXOS do parecer: F1 (name_status PROVISORIO de projecao_transversal_v404 so' ponteiro no haiku55), F2 (nomes com sigma escapados), F3 (kernel_formalization so' contagem no shared e sonnet_public, herdado), F4 (DeepSeek com 106 B de folga real, por desenho), F5 (registro unconditional de falsidade_da_inercia_v401 so' ponteiro); sem resposta de modelo ao vivo nem celular fisico",
    "nao_refazer": "A v406 esta construida e aceita em work\\iald_v406_20261103: para instalar, claim deploy + deploy_controlled.py com o OK do operador ao reinicio; nao reconstruir. A v407 parte desta pasta (LICOES_v406.md): deslizar a janela de novo (sai _v402), corrigir protected_fields (F1).",
    "proximo_passo": "OK do operador ao reinicio do filho web -> claim deploy, deploy_controlled.py, submit/accept, claim verify, verify_installed.py, torre.py gerar; depois a gerencia roda custodiar.py executar --versao v406 --publicar (C21, C19, C20, C17C)",
    "onde": str(W) + "; app\\build\\fit_memory.py (compact, literal_suffixes); app\\prepare.py; release_cfg.py",
    "artefatos": art, "refs": ["app.release.v405", "app.release.v404"],
    "nota": "Construtora: claude-app-orquestrador (ORDEM_004 da gerencia c1); revisor sonnet-app-v406-revisor, 03/11/2026. Consulta ao mapa antes: 0 rotas. Nada tocou um.py, selo, kernel, gate, cofre nem Chatgpt\\.",
}
f03_rota = {
    "tipo": "ROTA", "rota_id": "memoria.cientifica_sync.v406_gate_chatgpt", "dominio": "MEMORIA",
    "titulo": "F0.3 na v406: sincronizar a memoria cientifica da fila a partir de uma sessao Claude (parada no gate de escrita em Chatgpt\\)",
    "pergunta": "Uma sessao Claude pode preparar e ativar o release v406 da memoria cientifica canonica da fila sem escrever dentro de Chatgpt\\?",
    "dados": ["helper scientific_memory_sync.py (work\\scientific_memory_sync_20261013)", "canonical_memory.py do orquestrador (so' leitura)", "um.py v406 selado"],
    "metodo": "check somente leitura do helper (python -B, sem bytecode) e leitura do codigo de prepare/activate para ver onde gravam",
    "resultado": "nao: prepare cria releases\\%s e activate reescreve ACTIVE.json, ambos sob Chatgpt\\IALD_ORQUESTRACAO_20260923\\state\\canonical_memory; o check mediu %s (selado %s %s; ativo %s %s)" % (
        f03["check_somente_leitura"]["epoch_selado"], f03["check_somente_leitura"]["status"], f03["check_somente_leitura"]["versao_selada"], f03["check_somente_leitura"]["epoch_selado"],
        f03["check_somente_leitura"]["ativo"]["release"], f03["check_somente_leitura"]["ativo"]["epoch"]),
    "veredito": "F03_V406_PARADA_NO_GATE_DE_ESCRITA_EM_CHATGPT", "estatuto": "REAL", "status": "BLOQUEADA", "olhou_dados": False,
    "defeito": "parede de permissao medida (gate da ORDEM_004 secao 2: Chatgpt\\ e' so' leitura para toda sessao Claude), nao falha tecnica; a unidade F0.3 nao foi reivindicada",
    "nao_refazer": "Nao tentar prepare/activate de sessao Claude: grava em Chatgpt\\. Caminhos do recibo: (A) a coordenadora do Codex quando a cota voltar (04/11/2026 06:37, segundo o DESPACHO); (B) o operador autoriza expressamente uma escrita unica; (C) decisao da gerencia.",
    "proximo_passo": "decisao do operador ou da gerencia sobre A, B ou C; enquanto isso a memoria canonica da fila fica na v404 e o C19/C20/C17C da custodia ficam pendentes",
    "onde": str(F03), "artefatos": [str(F03), r"C:\IALD\Central de Patentes\work\scientific_memory_sync_20261013\scientific_memory_sync.py", r"C:\IALD\Central de Patentes\work\custodia_v406_03nov\DESPACHO_CODEX_F03_v406.md"],
    "refs": ["app.release.v406"], "nota": "claude-app-orquestrador, 03/11/2026. Consulta ao mapa antes: 0 rotas. Nada foi escrito em Chatgpt\\.",
}


def registrar(nome, obj):
    p = OUT / (nome + ".json")
    with p.open("xb") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"))
    r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(p), "--quem", QUEM], capture_output=True)
    print(nome, "rc", r.returncode, " ".join(r.stdout.decode("utf-8", "replace").split())[:230], r.stderr.decode("utf-8", "replace")[:300])


for rid, obj in (("app.release.v406", rota), ("memoria.cientifica_sync.v406_gate_chatgpt", f03_rota)):
    aberta = dict(obj, veredito="ROTA_ABERTA_ORDEM_004_%s" % rid.replace(".", "_").upper(), status="EM_CURSO", resultado="rota aberta nesta etapa; o resultado entra no registro seguinte", defeito="ver o registro de resultado")
    registrar("rota_aberta_" + rid, aberta)
    registrar("rota_resultado_" + rid, dict(obj, tipo="RESULTADO"))
