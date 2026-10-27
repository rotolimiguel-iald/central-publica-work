# -*- coding: utf-8 -*-
"""gerar_notas_pre_selo_v402.py -- gera NOTAS_PRE_SELO_v402.txt (relatorio da preparacao do pre_selo e do servico da v402) com TODO numero e hash LIDO dos arquivos na hora de gerar (regua: hash nunca de memoria).
Analogo do gerar_notas_pre_selo_v401.py (escrito a mao, nao derivado por script: o texto das notas depende do que cada rodada fez). So' leitura (o Nos, o manifesto da Bancada, a porta 18777 por consulta de rede,
o horario do ultimo boot do PC por consulta ao WMI, o mapa de rotas por rotas.py consultar); escreve so' as NOTAS ao lado (nao sobrescreve). uso: python -I -B -X utf8 gerar_notas_pre_selo_v402.py"""
import hashlib
import importlib.util
import json
import os
import re
import socket
import subprocess
import sys
import time

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
CS = os.path.dirname(V)
SRV = os.path.join(V, "bancada_B3_servico")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
BAN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um")
dest = os.path.join(HERE, "NOTAS_PRE_SELO_v402.txt")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)


def shaf(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def s16(p):
    return shaf(p)[:16]


def lj(p):
    return json.load(open(p, encoding="utf-8"))


def consultar_mapa(tema):
    """rotas.py consultar (so' leitura do livro do mapa de rotas); devolve (n, [(rota_id, status)], n_registros, cabeca)"""
    r = subprocess.run([sys.executable, "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py"), "consultar", tema], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, (tema, r.returncode, r.stderr[-300:])
    j = json.loads(r.stdout)
    return j["n"], [(x["rota_id"], x["status"]) for x in j["rotas"]], j["n_registros"], j["cabeca"]


selo = lj(os.path.join(NOS, "um_absoluto_selo.json"))
man = lj(os.path.join(BAN, "canonical_contracts.json"))
um_sha = shaf(os.path.join(NOS, "um.py"))
km_sha = shaf(os.path.join(NOS, "tgl_kernel_proof_manifest.json"))
s = socket.socket()
s.settimeout(1.5)
porta = s.connect_ex(("127.0.0.1", 18777)) == 0
s.close()
boot = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToString('s')"], capture_output=True, text=True).stdout.strip()
rel_v401 = lj(os.path.join(CS, "v401", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v401.json"))
bn_v401 = lj(os.path.join(CS, "v401", "bancada_B3", [x for x in os.listdir(os.path.join(CS, "v401", "bancada_B3")) if re.fullmatch(r"RECIBO_SINCRONIZACAO_v401_\d{8}_\d{6}\.json", x)][0]))
dpre = lj(os.path.join(HERE, "DERIVACAO_PRE_SELO_v402.json"))
pino_p = os.path.join(V, "PINO_RECIBO_PRE_SELO_v402.json")
prova_p = os.path.join(V, "PROVA_PRODUCAO_INTACTA_v402_pre_selo.json")
pino = lj(pino_p)
prova = lj(prova_p)
conf_p = os.path.join(HERE, "conferencia_pelo_esboco_v402.json")
conf = lj(conf_p)
rec = lj(pino["path"])
bat = rec["bateria_resultado"]
limp = lj(os.path.join(HERE, "LIMPEZA_SANDBOX_vb19.json"))
pbn = lj(os.path.join(CS, "v401", "PINOS_BN_v401.json"))
pbat = lj(os.path.join(CS, "v401", "bateria_pos_selo", "PINOS_BATERIA_v401.json"))
esb_ok = shaf(pbn["esboco_R3_5"]["path"]) == pbn["esboco_R3_5"]["sha256"]
bat_ok = shaf(pbat["bateria"]["path"]) == pbat["bateria"]["sha256"]
dsv = lj(os.path.join(SRV, "DERIVACAO_SERVICO_v402.json"))
csv_p = os.path.join(SRV, "CONFERENCIA_EXIGENCIAS_SERVICO_v402.json")
csv = lj(csv_p)
cn_p = os.path.join(SRV, "controle_negativo", "RESULTADO_CONTROLE_NEGATIVO_v402.json")
cn = lj(cn_p)
b_ban, b_nos = prova["bancada_de_producao"], prova["nos"]
ger = int(re.match(r"B(\d+)-", man["deployment_id"]).group(1))
ger_ant = int(bn_v401["manifesto_novo"]["deployment_id"].split("-")[0][1:])      # a geracao que o B(n) da v401 deixou na Bancada
quando_antes = lj(os.path.join(HERE, "prova_producao", "chaves_antes.json"))["quando"]
quando_final = lj(os.path.join(HERE, "prova_producao", "chaves_final.json"))["quando"]
rotas = {tema: consultar_mapa(tema) for tema in ("pre_selo", "bateria")}
# reconferencia da producao AGORA (depois da limpeza do sandbox e de tudo que esta tarefa leu): a mesma varredura do snap_producao_v402.py (so' leitura), comparada com a fotografia FINAL da prova
_spec = importlib.util.spec_from_file_location("snap_producao_v402", os.path.join(HERE, "snap_producao_v402.py"))
SN = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SN)
_lb, _eb = SN.varrer(SN.BAN)
_ln, _en = SN.varrer(SN.NOS)
re_ban = (SN.sha_lista(_lb) == b_ban["fotografias"]["final"]["sha256_da_lista"] and not _eb, len(_lb))
re_nos = (SN.sha_lista(_ln) == b_nos["fotografias"]["final"]["sha256_da_lista"] and not _en, len(_ln))
sandboxes_antigos = sorted(x for x in os.listdir(os.path.join("C:" + os.sep, "t")) if re.fullmatch(r"vb\d+", x))
t = []
w = t.append
w("NOTAS do pre_selo e do servico da v402 (subagente de apoio Sonnet 5.5 da gerencia c1, %s; gerado por gerar_notas_pre_selo_v402.py: todo numero e hash abaixo foi LIDO dos arquivos na hora de gerar)" % time.strftime("%d/%m/%Y"))
w("- No canonico: um.py sha16 %s == pino do selo (um_version %s; selo sha16 %s); manifesto do kernel sha16 %s == pino do selo (%s). Bancada de producao pina %s (manifesto sha16 %s; versao %s; estado_do_contrato_instalado %s). O B(n) da v402 e' o passo seguinte, SEM SALTO: grava B%d (veredito esperado REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO). Porta 18777 no ar: %s (so' consulta de rede; ultimo religamento lido: v401, PID %s, %s; ultimo boot do PC lido do WMI: %s; nada tocado)."
  % (um_sha[:16], selo.get("um_version"), s16(os.path.join(NOS, "um_absoluto_selo.json")), km_sha[:16], "sim" if selo["sha256"]["tgl_kernel_proof_manifest.json"] == km_sha else "NAO",
     man["deployment_id"], s16(os.path.join(BAN, "canonical_contracts.json")), pino["bancada_pina"]["version"], pino["bancada_pina"]["estado_do_contrato_instalado"], ger + 1, ger + 1, porta, rel_v401["pid"], rel_v401["hora_recibo"][:19], boot))
w("  Conferencia do pino do selo: selo.sha256[um.py] == sha256 do um.py = %s. Geracao que o B(n) da v401 deixou na Bancada (manifesto_novo do RECIBO_SINCRONIZACAO_v401_*.json) = B%d; geracao pinada hoje = B%d; iguais = %s." % (selo["sha256"]["um.py"] == um_sha, ger_ant, ger, ger_ant == ger))
w("- TAREFA 1 (pre_selo): derivados por derivar_pre_selo_v402.py (sha16 %s; DERIVACAO_PRE_SELO_v402.json sha16 %s; fonte = v401\\bateria_pre_selo, os scripts que RODARAM de verdade em 25/10 e geraram um recibo NOVO; subida simultanea v401->v402, v400->v401, v399->v400, vb18->vb19, V10->V11, SELO_V399/KM_V399->SELO_V400/KM_V400; contagem exata por token e por arquivo, assert). Saidas: gerar_pino_recibo_pre_selo_v402.py, conferir_recibo_pre_selo_v402.py, snap_producao_v402.py, rodar_ensaio_1_pre_selo_v402.sh, limpar_sandbox_vb19.py; gerar_notas_pre_selo_v402.py (este) foi escrito a mao, analogo do v401; adendo_notas_reinicio_v401.py NAO foi replicado (ultimo boot do PC %s; primeira fotografia da producao %s; boot anterior a primeira fotografia, isto e, nenhum reinicio durante esta tarefa = %s)."
  % (dpre["script"]["sha256"][:16], s16(os.path.join(HERE, "DERIVACAO_PRE_SELO_v402.json")), boot, quando_antes[:19], boot < quando_antes[:19]))
for k, v in dpre["contagens"].items():
    w("    %s: versoes por token %s; vb18->vb19 %s; V10->V11 %s" % (k, v["versoes_por_token"], v["vb18_para_vb19"], v["V10_para_V11"]))
w("  Pinos LIDOS de v401\\PINOS_BN_v401.json[esboco_R3_5] (esboco sha16 %s; disco == pino: %s) e v401\\bateria_pos_selo\\PINOS_BATERIA_v401.json[bateria] (bateria sha16 %s; disco == pino: %s); o lancador os le e confere de novo antes de rodar."
  % (pbn["esboco_R3_5"]["sha256"][:16], esb_ok, pbat["bateria"]["sha256"][:16], bat_ok))
w("  Ensaio (--versao v401 --fase pre_selo --modo ensaio, sem --cadeia-de-selos nem --recibo-pre-selo; %s a %s UTC): %s, RC %s, bateria %s (%d passa, %d falha, %d nao executado: T17 so' no pos_selo; T12/T13/T14 so' no pre_selo, %s)."
  % (rec["inicio_utc"][11:19], rec["fim_utc"][11:19], rec["veredito"], pino["codigo_de_saida"], bat["veredito"], bat["passa"], bat["falha"], bat["nao_executado"], "/".join(pino["t12_t13_t14_por_corrida"].values())))
w("  Recibo pre_selo: %s; sha256 %s. PINO_RECIBO_PRE_SELO_v402.json (GERADO NOVO, contrato %s) sha256 %s; utilizavel_como_recibo_pre_selo_do_B_n=%s; modo=%s fase=%s producao=%s sandbox=%s gate_effect=%s."
  % (os.path.basename(pino["path"]), pino["sha256"], pino["contrato"], shaf(pino_p), pino["utilizavel_como_recibo_pre_selo_do_B_n"], rec["modo"], rec["fase"], rec.get("producao"), rec.get("sandbox"), rec.get("gate_effect")))
w("  O recibo vale enquanto a Bancada de producao pinar %s (manifesto sha256 %s...): um re-pino antes do B(n) da v402 o torna obsoleto e a conferencia do esboco o recusa. T12/T13/T14 foram medidos contra o um.py v401 (o Nos de hoje), nao contra o v402; o T17 so' se decide no pos_selo. Adendo de pino do T12 (lido do pino): o pre-registro do F1.ATRATOR, pinado ao um.py sha16 %s, foi repinado NA COPIA para o um.py medido (sha16 %s); a ratificacao do dono da F1.ATRATOR segue pendente [DECLARADO: RESULTADO_R3_5.md]."
  % (pino["valido_enquanto"]["bancada_pina"]["deployment_id"], pino["valido_enquanto"]["bancada_pina"]["manifesto_sha256"][:16], pino["adendo_de_pino_do_t12"]["antes"]["sha256"][:16], pino["adendo_de_pino_do_t12"]["depois"]["sha256"][:16]))
w("  Conferencia pelo proprio esboco R3.5 (ja_sincronizada=False, sem cadeia, selo e manifesto anteriores = v402\\base_v401: selo sha16 %s, manifesto sha16 %s): aceita=%s; %d/%d condicoes; %d/%d controles negativos recusados como esperado; conferencia_pelo_esboco_v402.json sha16 %s."
  % (conf["selo_anterior"]["sha256"][:16], conf["kernel_manifesto_anterior"]["sha256"][:16], conf["esboco_aceita"], conf["n_condicoes_ok"], conf["n_condicoes"], conf["n_controles_como_esperado"], len(conf["controles_negativos"]), s16(conf_p)))
w("  Producao: Bancada %d entradas (antes/depois/final: %d/%d/%d), Nos %d (%d/%d/%d); listas iguais=%s e %s; chaves iguais nas tres fotografias=%s; arquivos .pyc/__pycache__ na Bancada (ja existentes, iguais nas tres): %s; PROVA_PRODUCAO_INTACTA_v402_pre_selo.json sha256 %s; producao_intacta=%s."
  % (b_ban["fotografias"]["final"]["n_entradas"], b_ban["fotografias"]["antes"]["n_entradas"], b_ban["fotografias"]["depois"]["n_entradas"], b_ban["fotografias"]["final"]["n_entradas"],
     b_nos["fotografias"]["final"]["n_entradas"], b_nos["fotografias"]["antes"]["n_entradas"], b_nos["fotografias"]["depois"]["n_entradas"], b_nos["fotografias"]["final"]["n_entradas"],
     b_ban["lista_identica_antes_depois_final"], b_nos["lista_identica_antes_depois_final"], all(c["igual_nas_tres"] for c in prova["chaves"]), prova["arquivos_pyc_ou_pycache_na_bancada"], shaf(prova_p), prova["producao_intacta"]))
w("  Fotografias da producao: antes %s, final %s (horarios locais lidos de chaves_*.json). Sandbox curto %s apagado por limpar_sandbox_vb19.py (%d arquivos, %d pastas, juncoes/links antes de apagar: %d; existe depois: %s; irmaos de C:\\t iguais: %s). O controle negativo do servico rodou ANTES da limpeza (a pasta temporaria dele ficou dentro de C:\\t\\vb19 e sumiu ao sair do with), logo a limpeza apagou tudo de uma vez e nada recriou C:\\t\\vb19 depois: existe agora = %s."
  % (quando_antes[:19], quando_final[:19], limp["alvo"], limp["arquivos"], limp["pastas"], limp["juncoes_ou_links_antes_de_apagar"], limp["existe_depois"], limp["irmaos_iguais"], os.path.exists(limp["alvo"])))
w("  Reconferencia da producao ao gerar estas notas (depois da limpeza do sandbox e de tudo que esta tarefa leu; mesma varredura do snap_producao_v402.py): lista da Bancada igual a da fotografia final = %s (%d entradas); lista do Nos igual a da fotografia final = %s (%d entradas). Sandboxes curtos de cadeias anteriores que continuam em C:\\t, NAO tocados por esta tarefa: %s."
  % (re_ban[0], re_ban[1], re_nos[0], re_nos[1], ", ".join(sandboxes_antigos) or "nenhum"))
w("- TAREFA 2 (servico da Bancada, v402 = v401 com 401->402 e 400->401, uma passada; NADA executado: nem parada, nem religamento, nem evento; porta 18777 nao tocada): derivar_servico_v402.py (sha16 %s) gerou os arquivos abaixo (sha16): %s."
  % (dsv["script"]["sha256"][:16], ", ".join("%s %s" % (k, v["sha256"][:16]) for k, v in dsv["arquivos"].items())))
w("  A Bancada esta na geracao B%d (B(n) da v401, RECIBO_SINCRONIZACAO_v401_*.json: manifesto_novo.deployment_id); o recibo_religamento_v402 assere n_esp == geracao anterior + 1 = B%d e veredito REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lendo o recibo do B(n) da v402 (nada digitado)." % (ger_ant, ger_ant + 1, ger_ant + 1))
w("  A parada le o PID do ultimo religamento em v401\\bancada_B3_servico\\RECIBO_RELIGAMENTO_v401.json (PID %s) como 'ultimo PID conhecido'; ela ASSERE porta 18777 fechada e nenhum processo um_bancada.py vivo (quanto a porta, hoje ela esta %s: a condicao %s)." % (rel_v401["pid"], "no ar" if porta else "fechada", "ja' vale" if not porta else "ainda nao vale"))
w("  Exigem V402_AUTORIZACAO_OPERADOR: parada e religamento (assert AUT e' a primeira coisa executavel, antes de qualquer E/S). Conferidor ESTATICO (ast + texto): %d/%d condicoes, CONFERENCIA_EXIGENCIAS_SERVICO_v402.json sha16 %s. Controle negativo de 3 mutacoes: rc %s (esperado 1), %d condicoes falharam, toda mutacao pega=%s (RESULTADO_CONTROLE_NEGATIVO_v402.json sha16 %s)."
  % (csv["n_condicoes_ok"], csv["n_condicoes"], s16(csv_p), cn["rc_do_conferidor_sobre_as_mutacoes"], len(cn["condicoes_que_falharam"]), cn["toda_mutacao_foi_pega"], s16(cn_p)))
w("  Desvios do molde v401: nenhum alem do mapa de versoes (a condicao do ESPERADOS que vale nos DOIS estados e a pasta temporaria do controle negativo dentro do sandbox curto ja' vem do molde v401; a v401 derivou o controle negativo da v399, a v402 o deriva do proprio da v401).")
w("- Pendencias para a gerencia (atos que NAO sao desta preparacao): ESPERADOS_v402.json existe agora=%s (nasce com gerar_esperados_v402 antes do rito); a parada do servico (pelo PID, nunca por nome; hoje a porta 18777 esta %s), o religamento e o evento c1 que nomeia a v402 sao atos da gerencia/operador com V402_AUTORIZACAO_OPERADOR no ambiente."
  % (os.path.exists(os.path.join(V, "ESPERADOS_v402.json")), "no ar" if porta else "fechada"))
w("- Mapa de rotas consultado ANTES (rotas.py consultar) e de novo ao gerar estas notas: %s. Nada foi registrado no mapa por esta tarefa (o registro e' da gerencia); o passo da v402 e' simples v401 -> v402 e o recibo pre_selo foi GERADO NOVO em ensaio, como na v401."
  % "; ".join("'%s' -> %d rota(s) [%s] (livro: %d registros, cabeca %s)" % (tema, n, ", ".join("%s=%s" % x for x in ids), nreg, cab) for tema, (n, ids, nreg, cab) in rotas.items()))
w("- Escopo: so' leitura da producao (Bancada e Nos); nada gravado nelas; nenhum um.py rodado, nenhum rito, nenhuma regra de permissao; NOT_FALSIFIED nao e creditacao; o gate nao se move.")
txt = "\n".join(t) + "\n"
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(txt)
assert os.path.getsize(dest + ".tmp") == len(txt.encode("utf-8"))
os.replace(dest + ".tmp", dest)
print(dest, shaf(dest)[:16], len(txt))
