# -*- coding: utf-8 -*-
"""gerar_notas_pre_selo_v401.py -- gera NOTAS_PRE_SELO_v401.txt (relatorio da preparacao do pre_selo e do servico da v401) com TODO numero e hash LIDO dos arquivos na hora de gerar (regua: hash nunca de memoria).
So' leitura (o Nos, o manifesto da Bancada, a porta 18777 por consulta de rede); escreve so' as NOTAS ao lado (nao sobrescreve). uso: python -I -B -X utf8 gerar_notas_pre_selo_v401.py"""
import hashlib
import json
import os
import re
import socket
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
CS = os.path.dirname(V)
SRV = os.path.join(V, "bancada_B3_servico")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
BAN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um")
dest = os.path.join(HERE, "NOTAS_PRE_SELO_v401.txt")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)


def shaf(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def s16(p):
    return shaf(p)[:16]


def lj(p):
    return json.load(open(p, encoding="utf-8"))


selo = lj(os.path.join(NOS, "um_absoluto_selo.json"))
man = lj(os.path.join(BAN, "canonical_contracts.json"))
um_sha = shaf(os.path.join(NOS, "um.py"))
km_sha = shaf(os.path.join(NOS, "tgl_kernel_proof_manifest.json"))
s = socket.socket()
s.settimeout(1.5)
porta = s.connect_ex(("127.0.0.1", 18777)) == 0
s.close()
rel_v400 = lj(os.path.join(CS, "v400", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v400.json"))
dpre = lj(os.path.join(HERE, "DERIVACAO_PRE_SELO_v401.json"))
pino_p = os.path.join(V, "PINO_RECIBO_PRE_SELO_v401.json")
prova_p = os.path.join(V, "PROVA_PRODUCAO_INTACTA_v401_pre_selo.json")
pino = lj(pino_p)
prova = lj(prova_p)
conf_p = os.path.join(HERE, "conferencia_pelo_esboco_v401.json")
conf = lj(conf_p)
rec = lj(pino["path"])
bat = rec["bateria_resultado"]
limp = lj(os.path.join(HERE, "LIMPEZA_SANDBOX_vb18.json"))
pbn = lj(os.path.join(CS, "v400", "PINOS_BN_v400.json"))
pbat = lj(os.path.join(CS, "v400", "bateria_pos_selo", "PINOS_BATERIA_v400.json"))
esb_ok = shaf(pbn["esboco_R3_5"]["path"]) == pbn["esboco_R3_5"]["sha256"]
bat_ok = shaf(pbat["bateria"]["path"]) == pbat["bateria"]["sha256"]
dsv = lj(os.path.join(SRV, "DERIVACAO_SERVICO_v401.json"))
csv_p = os.path.join(SRV, "CONFERENCIA_EXIGENCIAS_SERVICO_v401.json")
csv = lj(csv_p)
cn_p = os.path.join(SRV, "controle_negativo", "RESULTADO_CONTROLE_NEGATIVO_v401.json")
cn = lj(cn_p)
b_ban, b_nos = prova["bancada_de_producao"], prova["nos"]
ger = int(re.match(r"B(\d+)-", man["deployment_id"]).group(1))
cont_pre = {k: v["versoes_por_token"] for k, v in ((a, b) for a, b in dpre["contagens"].items())}
t = []
w = t.append
w("NOTAS do pre_selo e do servico da v401 (subagente de preparacao Sonnet, 25/10/2026; gerado por gerar_notas_pre_selo_v401.py: todo numero e hash abaixo foi LIDO dos arquivos na hora de gerar)")
w("- No canonico: um.py sha16 %s == pino do selo (um_version %s; selo sha16 %s); manifesto do kernel sha16 %s == pino do selo (%s). Bancada de producao pina %s (manifesto sha16 %s; versao %s; estado_do_contrato_instalado %s). O B(n) da v401 e' o passo seguinte, SEM SALTO: grava B%d (veredito esperado REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO). Porta 18777 no ar: %s (so' consulta de rede; ultimo religamento lido: v400, PID %s, %s; nada tocado)."
  % (um_sha[:16], selo.get("um_version"), s16(os.path.join(NOS, "um_absoluto_selo.json")), km_sha[:16], "sim" if selo["sha256"]["tgl_kernel_proof_manifest.json"] == km_sha else "NAO",
     man["deployment_id"], s16(os.path.join(BAN, "canonical_contracts.json")), pino["bancada_pina"]["version"], pino["bancada_pina"]["estado_do_contrato_instalado"], ger + 1, ger + 1, porta, rel_v400["pid"], rel_v400["hora_recibo"][:19]))
w("  Conferencia do pino do selo: selo.sha256[um.py] == sha256 do um.py = %s." % (selo["sha256"]["um.py"] == um_sha))
w("- TAREFA 1 (pre_selo): derivados por derivar_pre_selo_v401.py (sha16 %s; DERIVACAO_PRE_SELO_v401.json sha16 %s; fonte = v399\\bateria_pre_selo, os scripts que geraram um recibo NOVO; subida simultanea v399->v401, v398->v400, v397->v399, vb16->vb18, V8->V10, SELO_V397/KM_V397->SELO_V399/KM_V399; contagem exata por token e por arquivo, assert). Saidas: gerar_pino_recibo_pre_selo_v401.py, conferir_recibo_pre_selo_v401.py, snap_producao_v401.py, rodar_ensaio_1_pre_selo_v401.sh, limpar_sandbox_vb18.py."
  % (dpre["script"]["sha256"][:16], s16(os.path.join(HERE, "DERIVACAO_PRE_SELO_v401.json"))))
for k, v in dpre["contagens"].items():
    w("    %s: versoes por token %s; vb16->vb18 %s; V8->V10 %s" % (k, v["versoes_por_token"], v["vb16_para_vb18"], v["V8_para_V10"]))
w("  Pinos LIDOS de v400\\PINOS_BN_v400.json[esboco_R3_5] (esboco sha16 %s; disco == pino: %s) e v400\\bateria_pos_selo\\PINOS_BATERIA_v400.json[bateria] (bateria sha16 %s; disco == pino: %s); o lancador os le e confere de novo antes de rodar."
  % (pbn["esboco_R3_5"]["sha256"][:16], esb_ok, pbat["bateria"]["sha256"][:16], bat_ok))
w("  Ensaio (--versao v400 --fase pre_selo --modo ensaio, sem --cadeia-de-selos nem --recibo-pre-selo; %s a %s UTC): %s, RC %s, bateria %s (%d passa, %d falha, %d nao executado: T17 so' no pos_selo; T12/T13/T14 so' no pre_selo, %s)."
  % (rec["inicio_utc"][11:19], rec["fim_utc"][11:19], rec["veredito"], pino["codigo_de_saida"], bat["veredito"], bat["passa"], bat["falha"], bat["nao_executado"], "/".join(pino["t12_t13_t14_por_corrida"].values())))
w("  Recibo pre_selo: %s; sha256 %s. PINO_RECIBO_PRE_SELO_v401.json (GERADO NOVO, contrato %s) sha256 %s; utilizavel_como_recibo_pre_selo_do_B_n=%s; modo=%s fase=%s producao=%s sandbox=%s gate_effect=%s."
  % (os.path.basename(pino["path"]), pino["sha256"], pino["contrato"], shaf(pino_p), pino["utilizavel_como_recibo_pre_selo_do_B_n"], rec["modo"], rec["fase"], rec.get("producao"), rec.get("sandbox"), rec.get("gate_effect")))
w("  O recibo vale enquanto a Bancada de producao pinar %s (manifesto sha256 %s...): um re-pino antes do B(n) da v401 o torna obsoleto e a conferencia do esboco o recusa. T12/T13/T14 foram medidos contra o um.py v400 (o Nos de hoje), nao contra o v401; o T17 so' se decide no pos_selo."
  % (pino["valido_enquanto"]["bancada_pina"]["deployment_id"], pino["valido_enquanto"]["bancada_pina"]["manifesto_sha256"][:16]))
w("  Conferencia pelo proprio esboco R3.5 (ja_sincronizada=False, sem cadeia, selo e manifesto anteriores = v401\\base_v400: selo sha16 %s, manifesto sha16 %s): aceita=%s; %d/%d condicoes; %d/%d controles negativos recusados como esperado; conferencia_pelo_esboco_v401.json sha16 %s."
  % (conf["selo_anterior"]["sha256"][:16], conf["kernel_manifesto_anterior"]["sha256"][:16], conf["esboco_aceita"], conf["n_condicoes_ok"], conf["n_condicoes"], conf["n_controles_como_esperado"], len(conf["controles_negativos"]), s16(conf_p)))
w("  Producao: Bancada %d entradas (antes/depois/final: %d/%d/%d), Nos %d (%d/%d/%d); listas iguais=%s e %s; chaves iguais nas tres fotografias=%s; arquivos .pyc/__pycache__ na Bancada (ja existentes, iguais nas tres): %s; PROVA_PRODUCAO_INTACTA_v401_pre_selo.json sha256 %s; producao_intacta=%s."
  % (b_ban["fotografias"]["final"]["n_entradas"], b_ban["fotografias"]["antes"]["n_entradas"], b_ban["fotografias"]["depois"]["n_entradas"], b_ban["fotografias"]["final"]["n_entradas"],
     b_nos["fotografias"]["final"]["n_entradas"], b_nos["fotografias"]["antes"]["n_entradas"], b_nos["fotografias"]["depois"]["n_entradas"], b_nos["fotografias"]["final"]["n_entradas"],
     b_ban["lista_identica_antes_depois_final"], b_nos["lista_identica_antes_depois_final"], all(c["igual_nas_tres"] for c in prova["chaves"]), prova["arquivos_pyc_ou_pycache_na_bancada"], shaf(prova_p), prova["producao_intacta"]))
w("  Sandbox curto %s apagado por limpar_sandbox_vb18.py (%d arquivos, %d pastas, juncoes/links antes de apagar: %d; existe depois: %s; irmaos de C:\\t iguais: %s). A pasta temporaria do controle negativo do servico recriou C:\\t\\vb18 vazia depois (a pasta interna sumiu ao sair do with) e foi removida com rmdir (so' se vazia)."
  % (limp["alvo"], limp["arquivos"], limp["pastas"], limp["juncoes_ou_links_antes_de_apagar"], limp["existe_depois"], limp["irmaos_iguais"]))
w("- TAREFA 2 (servico da Bancada, v401 = v400 com 400->401 e 398->400, uma passada; NADA executado: nem parada, nem religamento, nem evento; porta 18777 nao tocada): derivar_servico_v401.py (sha16 %s) gerou os arquivos abaixo (sha16): %s."
  % (dsv["script"]["sha256"][:16], ", ".join("%s %s" % (k, v["sha256"][:16]) for k, v in dsv["arquivos"].items())))
w("  A Bancada deixou a geracao B%d (B(n) da v400, RECIBO_SINCRONIZACAO_v400_*.json: manifesto_novo.deployment_id); o recibo_religamento_v401 assere n_esp == geracao anterior + 1 = B%d e veredito REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lendo o recibo do B(n) da v400 (nada digitado)." % (ger, ger + 1, ger + 1))
w("  A parada le o PID do ultimo religamento em v400\\bancada_B3_servico\\RECIBO_RELIGAMENTO_v400.json (PID %s)." % rel_v400["pid"])
w("  Exigem V401_AUTORIZACAO_OPERADOR: parada e religamento (assert AUT e' a primeira coisa executavel, antes de qualquer E/S). Conferidor ESTATICO (ast + texto): %d/%d condicoes, CONFERENCIA_EXIGENCIAS_SERVICO_v401.json sha16 %s. Controle negativo de 3 mutacoes: rc %s (esperado 1), %d condicoes falharam, toda mutacao pega=%s (RESULTADO_CONTROLE_NEGATIVO_v401.json sha16 %s)."
  % (csv["n_condicoes_ok"], csv["n_condicoes"], s16(csv_p), cn["rc_do_conferidor_sobre_as_mutacoes"], len(cn["condicoes_que_falharam"]), cn["toda_mutacao_foi_pega"], s16(cn_p)))
w("  Desvio do molde v400: a condicao do ESPERADOS no conferidor vale nos DOIS estados (ESPERADOS_v401.json ausente: o evento aborta no isfile; presente com o um.py do Nos diferente do candidato: aborta no assert do candidato); depois do rito, com o um.py do Nos igual ao candidato, essa condicao PASSA a falhar de proposito (o evento deixaria de abortar). O controle negativo, que a v400 nao teve, vem do da v399, com a pasta temporaria dentro de C:\\t\\vb18.")
w("- Pendencias para a gerencia (atos que NAO sao desta preparacao): ESPERADOS_v401.json existe agora=%s (nasce com gerar_esperados_v401 antes do rito); a parada do servico (pelo PID, nunca por nome), o religamento e o evento c1 que nomeia a v401 sao atos da gerencia/operador com V401_AUTORIZACAO_OPERADOR no ambiente." % os.path.exists(os.path.join(V, "ESPERADOS_v401.json")))
w("- Mapa de rotas consultado ANTES (rotas.py consultar): 'pre_selo' -> 3 rotas (umpy.v399/v400.cadeia_de_selo_preparada_24out, infra.bancada_um.sincronizacao_vnnn: reusados por pino o esboco R3.5, a lista de permissao e a fusao do PINOS_BN; o salto do R3.4 NAO se refaz, esta' medido impossivel; o passo da v401 e' simples v400 -> v401); 'sincronizacao' -> 11 rotas. Nada do que foi derivado aqui existia como rota; o registro desta preparacao no mapa e' da gerencia.")
w("- Escopo: so' leitura da producao (Bancada e Nos); nada gravado nelas; nenhum um.py rodado, nenhum rito, nenhuma regra de permissao; NOT_FALSIFIED nao e creditacao; o gate nao se move.")
txt = "\n".join(t) + "\n"
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(txt)
assert os.path.getsize(dest + ".tmp") == len(txt.encode("utf-8"))
os.replace(dest + ".tmp", dest)
print(dest, shaf(dest)[:16], len(txt))
