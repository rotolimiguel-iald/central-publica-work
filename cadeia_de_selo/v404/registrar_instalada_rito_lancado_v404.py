# -*- coding: utf-8 -*-
"""registrar_instalada_rito_lancado_v404.py -- gerencia c1, 28/10/2026: registra a etapa material «v404 INSTALADA no Nos e rito lancado» no Mapa de Rotas
(ANOTACAO na rota da preparacao), no quadro do programa (iald.py anotar) e na memoria ACOM da sessao (transition). Numeros e hashes LIDOS dos arquivos
(APLICADO_AO_CANONICO_*.json, CANDIDATO, PRECONDICOES, o log do lancador do rito e o pino do MEMORY.md). Nada do Nos e' tocado.
uso: python -X utf8 registrar_instalada_rito_lancado_v404.py   (sem -I: o rotas.py e o session_memory.py sao chamados em processo proprio)"""
import glob, hashlib, io, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
H = os.path.dirname(os.path.abspath(__file__))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rj = lambda p: json.load(open(p, encoding="utf-8"))
apl = sorted(glob.glob(os.path.join(H, "APLICADO_AO_CANONICO_*.json")))[-1]; A = rj(apl); A["n_backups"] = len(A["backups"]); A["modulos_novos"] = A["modulos_novos_v404"]["n"]
CM = rj(os.path.join(H, "CANDIDATO_v404.json")); PC = rj(os.path.join(H, "PRECONDICOES_v404.json"))
assert A["um_py_novo"]["sha16"] == CM["sha16"] == "e7f0a7213715d0de" and all(c["ok"] for c in PC["checagens"]), "o recibo da instalacao ou as precondicoes nao batem"
NOS_UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
assert sha(NOS_UM)[:16] == A["um_py_novo"]["sha16"], "o um.py do Nos nao e' o instalado"
log = io.open(os.path.join(H, "rito_servidor_v404.log"), encoding="utf-8", errors="replace").read()
m = re.search(r"(\d\d:\d\d:\d\d) inicio do rito \S+ \(um\.py (\w{16})\)", log); assert m and m.group(2) == A["um_py_novo"]["sha16"], "o log do lancador nao mostra o inicio do rito com o um.py instalado"
inicio = m.group(1)
pino = rj(os.path.join(os.environ["USERPROFILE"], ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "PINO_MEMORY.json"))
hoje = time.strftime("%d/%m/%Y")
comp = os.path.join(H, "compactar_indice_memoria_v404.py")
titulo = "%s %s: candidato final %s INSTALADO no Nos (%d backups de bytes, %d modulos novos) e rito lancado; p00 %d/%d depois da compactacao do indice da memoria (decisao da gerencia)" % (
    hoje, inicio, CM["sha16"], A["n_backups"], A["modulos_novos"], sum(1 for c in PC["checagens"] if c["ok"]), len(PC["checagens"]))
resultado = ("(1) Revisao da gerencia c1 sobre a preparacao do agente claude-prep-v404 (quem constroi nao aprova): delta_v404.py, registros_v404.py, runtime_v404.py, artigo PT/EN e os textos do pos-rito lidos; hashes do candidato, das duas pedras (1e53257273395c7c, 18df8f686e524845) e do Nos conferidos por script; "
             "os numeros digitados na errata E8 (conjunto A de 31 eventos NOT_BLIND; conjunto D n = 14) conferidos no um.py selado; varredura da regua (pos-dicao, alfa = beta/raiz(e), beta literal, confirmacao) sem achado. "
             "(2) A unica precondicao reprovada era real: o MEMORY.md (191 linhas, 23.701 B) nao comportava a linha do handoff; pela regra dos dois arquivos OITO linhas sairam INTEGRAS para o MEMORY_2.md (handoff v402 dobrado na consolidada v392-v402; cunhagens 07-11/10; consolidada dos handoffs; memoria cientifica da fila com os marcadores mantidos na mesma linha; nomes das pedras; G1; consulta diaria; transicao para a massa) "
             "e ficaram ponteiros curtos: %d linhas / %d B, pino %s (seq 100). (3) p00 TODAS PASSARAM. (4) instalar_v404.py rc 0 (%s; um.py do Nos = %s; %d modulos novos). (5) rito_v404.sh lancado no Git Bash em segundo plano (echo 1 | python um.py no Nos; stdout canonico rodada_v404_stdout.txt); inicio do rito %s; o lancador parou o servidor do modelo nativo e o religa no fim. "
             "O B(n) pre-selo (PINO_RECIBO_PRE_SELO_v404.json) segue valido: a Bancada pina B12-v403." % (pino["linhas"], pino["bytes"], pino["sha256"][:16], os.path.basename(apl), A["um_py_novo"]["sha16"], A["modulos_novos"], inicio))
an = [{"tipo": "ANOTACAO", "rota_id": "umpy.v404.cadeia_de_selo_preparada_28out", "estatuto": "REAL", "olhou_dados": False, "titulo": titulo, "resultado": resultado,
       "artefatos": [apl, os.path.join(H, "CANDIDATO_v404.json"), os.path.join(H, "PRECONDICOES_v404.json"), comp, os.path.join(H, "rito_servidor_v404.log")],
       "proximo_passo": "esperar o RITO_RC no fim de rodada_v404_stdout.txt (~2 h); conferir_rito_v404.py; pos_rito/chain_pos_rito_v404.sh (0-14; 10a/10c com V404_AUTORIZACAO_OPERADOR, texto sem o nome do script do servico); registrar_mapa_v404.py; custodia G1.",
       "nota": "A revisao e' da gerencia, distinta do agente que construiu; nenhum terceiro revisou. Nada move o gate; NOT_FALSIFIED nunca e' CONFIRMED."}]
pj = os.path.join(H, "mapa_anotacao_instalada_rito_lancado_v404.json"); io.open(pj, "w", encoding="utf-8").write(json.dumps(an, ensure_ascii=False, indent=1))
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", pj, "--quem", "claude-c1 (gerência), 28/10"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("mapa rc", r.returncode, (r.stdout or r.stderr).strip()[-200:])
TIPO = os.environ.get("QUADRO_TIPO", "etapa")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", TIPO, "--unidade", "F4.1",
                    "--dados", json.dumps({"quando": hoje + " " + inicio, "etapa": "v404 instalada no Nos e rito lancado", "um_py_sha16": A["um_py_novo"]["sha16"], "modulos_novos": A["modulos_novos"], "p00": "TODAS PASSARAM", "memory_md": "%d linhas / %d B apos compactacao" % (pino["linhas"], pino["bytes"])}, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace"); print("quadro rc", r.returncode, (r.stdout or r.stderr).strip()[:160])
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return rr.returncode, (json.loads(rr.stdout) if rr.stdout.strip().startswith("{") else {"raw": (rr.stdout + rr.stderr)[:300]})
rc, g = sm({"operation": "get", "reference": REF}); rev = g["result"]["revision"]
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-v404-instalada-rito-lancado-28out",
            "changes": {"records": [{"id": "c1-v404-instalada-rito-lancado", "kind": "fact", "statute": "REAL", "sources": [S(apl), S(comp), S(pj)],
                                     "text": "28/10/2026 %s: v404 (um.py %s; pedras ProjecaoTransversalDaMeiaNat e Jo8v32) instalada no Nos com %d backups; rito lancado; p00 TODAS PASSARAM depois da compactacao do MEMORY.md pela regra dos dois arquivos (8 linhas integras no MEMORY_2.md; %d linhas / %d B; pino %s). Revisao da gerencia sobre a preparacao do agente; sem terceiro." % (inicio, A["um_py_novo"]["sha16"], A["n_backups"], pino["linhas"], pino["bytes"], pino["sha256"][:16])}],
                        "flow": {"phase": "v404_rito_em_curso__pos_rito_a_seguir", "next_action": "ao RITO_RC=0: conferir_rito_v404.py; chain_pos_rito_v404.sh (passos 0-14; B(n) com V404_AUTORIZACAO_OPERADOR); fechar; registrar_mapa; custodia G1; indice da memoria e Atlas. E0 segue pergunta ao operador; conjunto D nao se abre sem a palavra dele."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
