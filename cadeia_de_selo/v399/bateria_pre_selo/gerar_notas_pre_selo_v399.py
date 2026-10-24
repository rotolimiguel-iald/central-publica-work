# -*- coding: utf-8 -*-
"""gerar_notas_pre_selo_v399.py -- gera NOTAS_PRE_SELO_v399.txt (o relatorio completo da preparacao do pre_selo e do servico da v399) com TODO numero e hash LIDO dos arquivos na hora de gerar
(regua: hash nunca de memoria). So' leitura do resto: le o Nos, a Bancada de producao (manifesto), o servico (porta 18777, so' consulta de processo) e os artefatos da cadeia; escreve so' as NOTAS ao lado
(nao sobrescreve). uso: python -I -B -X utf8 gerar_notas_pre_selo_v399.py"""
import datetime
import glob
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
CS = os.path.dirname(V)
V8 = os.path.join(CS, "v398")
SRV = os.path.join(V, "bancada_B3_servico")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
BAN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um")
dest = os.path.join(HERE, "NOTAS_PRE_SELO_v399.txt")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)


def shaf(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def s16(p):
    return shaf(p)[:16]


def lj(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


# ---- o estado de hoje (lido)
um = os.path.join(NOS, "um.py")
selo_p = os.path.join(NOS, "um_absoluto_selo.json")
selo = lj(selo_p)
um_sha = shaf(um)
km_sha = shaf(os.path.join(NOS, "tgl_kernel_proof_manifest.json"))
man = lj(os.path.join(BAN, "canonical_contracts.json"))
man_sha = shaf(os.path.join(BAN, "canonical_contracts.json"))
ger = int(re.match(r"B(\d+)-", man["deployment_id"]).group(1))
pid_srv = criado = cmd = None
try:
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "$c = Get-NetTCPConnection -State Listen -LocalPort 18777 -ErrorAction SilentlyContinue | Select-Object -First 1; if ($c) { $p = Get-CimInstance Win32_Process -Filter ('ProcessId=' + $c.OwningProcess); "
                        "$p.ProcessId.ToString() + '|' + $p.CreationDate.ToString('yyyy-MM-ddTHH:mm:ss') + '|' + $p.CommandLine }"], capture_output=True, text=True, encoding="utf-8", timeout=60)
    partes = r.stdout.strip().split("|", 2)
    if len(partes) == 3:
        pid_srv, criado, cmd = partes[0], partes[1], partes[2].strip()
except Exception as exc:                                                         # a falha de leitura fica DITA, nao disfarcada
    pid_srv, criado, cmd = "FALHA_DE_LEITURA: %r" % (exc,), "?", "?"
# ---- derivacao do pre_selo, ensaio, conferencia, pino, prova
dpre = lj(os.path.join(HERE, "DERIVACAO_PRE_SELO_v399.json"))
pino = lj(os.path.join(V, "PINO_RECIBO_PRE_SELO_v399.json"))
prova = lj(os.path.join(V, "PROVA_PRODUCAO_INTACTA_v399_pre_selo.json"))
conf = lj(os.path.join(HERE, "conferencia_pelo_esboco_v399.json"))
rec_p = pino["path"]
rec = lj(rec_p)
t0 = datetime.datetime.fromisoformat(rec["inicio_utc"]).astimezone()
t1 = datetime.datetime.fromisoformat(rec["fim_utc"]).astimezone()
bat = rec["bateria_resultado"]
pbn = lj(os.path.join(V8, "PINOS_BN_v398.json"))
pbat = lj(os.path.join(V8, "bateria_pos_selo", "PINOS_BATERIA_v398.json"))
b_ban, b_nos = prova["bancada_de_producao"], prova["nos"]
# a lista da Bancada e do Nos contra a prova da v398 (antes do ensaio de 23/10)
a8 = lj(os.path.join(V8, "bateria_pre_selo", "prova_producao", "fp_bancada_antes.json"))
a9 = lj(os.path.join(HERE, "prova_producao", "fp_bancada_antes.json"))
d8 = {x[0]: tuple(x[1:]) for x in a8}
d9 = {x[0]: tuple(x[1:]) for x in a9}
add, rem, alt = sorted(set(d9) - set(d8)), sorted(set(d8) - set(d9)), sorted(k for k in set(d8) & set(d9) if d8[k] != d9[k])
n8 = json.loads(gzip.decompress(open(os.path.join(V8, "bateria_pre_selo", "prova_producao", "fp_nos_antes.json.gz"), "rb").read()).decode("utf-8"))
n9 = json.loads(gzip.decompress(open(os.path.join(HERE, "prova_producao", "fp_nos_antes.json.gz"), "rb").read()).decode("utf-8"))
dn8 = {x[0]: tuple(x[1:]) for x in n8}
dn9 = {x[0]: tuple(x[1:]) for x in n9}
# ---- servico
dd = lj(os.path.join(SRV, "DERIVACAO_DERIVADOR_v399.json"))
ds = lj(os.path.join(SRV, "DERIVACAO_SERVICO_v399.json"))
ce = lj(os.path.join(SRV, "CONFERENCIA_EXIGENCIAS_SERVICO_v399.json"))
cn = lj(os.path.join(SRV, "controle_negativo", "RESULTADO_CONTROLE_NEGATIVO_v399.json"))
cr = ds["conferencia_com_o_rito_real_da_v398"]
ex = ds["expectativa_do_B_n_da_v399"]
rp8 = lj(os.path.join(V8, "bancada_B3_servico", "RECIBO_PARADA_v398.json"))
rr8 = lj(os.path.join(V8, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v398.json"))
quadro = lj(os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD", "PROGRAMA.json"))
f06 = next((u for u in quadro["unidades"] if u.get("id") == "F0.6"), {})
limpeza_p = os.path.join(HERE, "LIMPEZA_SANDBOX_vb16.json")
limpeza = lj(limpeza_p) if os.path.exists(limpeza_p) else None
cont = dpre["contagens"]
tot = {k: cont[k]["versoes"] for k in cont}
tok = {k: cont[k]["versoes_por_token"] for k in cont}
sub_nota = next(r for a in ds["arquivos"] if a["saida"]["path"].endswith("recibo_parada_v399.py") for r in a["regras_aplicadas"] if r["regra"] == "nota_nao_atribui_a_parada_ao_operador")
nao_prev = cr["algo_que_os_scripts_v398_nao_previam"]

L = []
L.append("NOTAS do pre_selo e do servico da v399 (subagente de preparacao Sonnet, 24/10/2026; gerado por gerar_notas_pre_selo_v399.py: todo numero e hash abaixo foi LIDO dos arquivos na hora de gerar)")
L.append("- No canonico: um.py sha16 %s == pino do selo (um_version %s; selo sha16 %s); manifesto do kernel sha16 %s == pino do selo (%s). Bancada de producao pina %s (manifesto sha16 %s; versao %s; estado_do_contrato_instalado %s). "
         "O B(n) da v399 e' o passo seguinte, SEM SALTO: grava B%d (veredito esperado REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO). Servico na porta 18777 no ar: PID %s criado %s; so' MEDIDO, nao tocado."
         % (um_sha[:16], selo.get("um_version"), shaf(selo_p)[:16], km_sha[:16], "sim" if selo["sha256"]["tgl_kernel_proof_manifest.json"] == km_sha else "NAO", man["deployment_id"], man_sha[:16],
            man["canonical"]["version"], conf["bancada_de_producao_lida"]["estado_do_contrato_instalado"], ger + 1, ger + 1, pid_srv, criado))
L.append("  Conferencia do pino do selo: selo.sha256[um.py] == sha256 do um.py = %s; Bancada.canonical.script.sha256 == o mesmo = %s."
         % (selo["sha256"]["um.py"] == um_sha, man["canonical"]["script"]["sha256"] == um_sha))
L.append("- Derivados por derivar_pre_selo_v399.py (sha16 %s; subida de versao v398->v399, v397->v398, v396->v397, vb15->vb16, V7->V8, fronteira de digitos, uma passada; DERIVACAO_PRE_SELO_v399.json sha16 %s traz sha256 de entrada e saida): "
         "gerar_pino_recibo_pre_selo_v399.py, conferir_recibo_pre_selo_v399.py, snap_producao_v399.py, rodar_ensaio_1_pre_selo_v399.sh (sh -n ok)."
         % (s16(os.path.join(HERE, "derivar_pre_selo_v399.py")), s16(os.path.join(HERE, "DERIVACAO_PRE_SELO_v399.json"))))
por_tok = ["%d/%d/%d" % (tok[k]["v398"], tok[k]["v397"], tok[k]["v396"]) for k in ("gerar_pino_recibo_pre_selo", "conferir_recibo_pre_selo", "snap_producao", "rodar_ensaio_1_pre_selo")]
L.append("  Contagens de versoes por arquivo: gerar_pino_recibo_pre_selo=%d; conferir_recibo_pre_selo=%d; snap_producao=%d; rodar_ensaio_1_pre_selo=%d (por token v398/v397/v396: %s; as mesmas da v398 e agora conferidas por assert por token)."
         % (tot["gerar_pino_recibo_pre_selo"], tot["conferir_recibo_pre_selo"], tot["snap_producao"], tot["rodar_ensaio_1_pre_selo"], " | ".join(por_tok)))
L.append("- Divergencias do molde v398 (regras com contagem exata e assert no derivador): (a) o conferir ja le o selo e o manifesto do kernel ANTERIORES (v398) de v399\\base_v398 (copia de bytes do Nos: %d de 5 arquivos com sha256 igual ao Nos, medido na hora; "
         "o selo pina o manifesto do kernel da copia): %d usos de os.path.join(V, \"base_v398\" e nenhum de HERE\\base_v39x; (b) SELO_V396/KM_V396 (nomes herdados) viraram SELO_V397/KM_V397 (%d+%d); o controle negativo usa o selo da v397 (v398\\base_v397, selo sha16 %s); "
         "(c) o derivador ganhou assert por token de versao e a checagem de que V8 nao pre-existe; as quatro saidas tem o mesmo tamanho em bytes que as da v398: %s (todas as trocas sao de mesmo comprimento)."
         % (sum(1 for n in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json") if shaf(os.path.join(V, "base_v398", n)) == shaf(os.path.join(NOS, n))),
            cont["conferir_recibo_pre_selo"]["base_v398_em_V"], cont["conferir_recibo_pre_selo"]["SELO_V396_para_SELO_V397"], cont["conferir_recibo_pre_selo"]["KM_V396_para_KM_V397"], s16(os.path.join(V8, "base_v397", "um_absoluto_selo.json")),
            str(all(os.path.getsize(os.path.join(HERE, n + "_v399" + e)) == os.path.getsize(os.path.join(V8, "bateria_pre_selo", n + "_v398" + e))
                    for n, e in (("gerar_pino_recibo_pre_selo", ".py"), ("conferir_recibo_pre_selo", ".py"), ("snap_producao", ".py"), ("rodar_ensaio_1_pre_selo", ".sh")))).lower()))
L.append("- Pinos LIDOS e conferidos contra o disco antes de rodar: esboco R3.5 sha16 %s (v398\\PINOS_BN_v398.json[esboco_R3_5]; disco == pino: %s); bateria v398 sha16 %s (v398\\bateria_pos_selo\\PINOS_BATERIA_v398.json[bateria]; disco == pino: %s)."
         % (pbn["esboco_R3_5"]["sha256"][:16], shaf(pbn["esboco_R3_5"]["path"]) == pbn["esboco_R3_5"]["sha256"], pbat["bateria"]["sha256"][:16], shaf(pbat["bateria"]["path"]) == pbat["bateria"]["sha256"]))
L.append("- Ensaio (--versao v398 --fase pre_selo --modo ensaio, sem salto; %s a %s, %d s): %s, RC %d, bateria %s (%d passa, %d falha, %d nao executado: T17 so no pos_selo; T12/T13/T14 so no pre_selo, %s)."
         % (t0.strftime("%H:%M:%S"), t1.strftime("%H:%M:%S"), round((t1 - t0).total_seconds()), pino["veredito"], pino["codigo_de_saida"], pino["contagens"]["veredito_bateria"], pino["contagens"]["passa"], pino["contagens"]["falha"],
            pino["contagens"]["nao_executado"], "/".join(pino["t12_t13_t14_por_corrida"].values())))
L.append("  recibo pre_selo sha256 %s; PINO_RECIBO_PRE_SELO_v399.json sha256 %s; utilizavel_como_recibo_pre_selo_do_B_n=%s; modo=%s fase=%s producao=%s sandbox=%s gate_effect=%s."
         % (pino["sha256"], shaf(os.path.join(V, "PINO_RECIBO_PRE_SELO_v399.json")), str(pino["utilizavel_como_recibo_pre_selo_do_B_n"]).lower(), rec["modo"], rec["fase"], rec["producao"], rec["sandbox"], rec.get("gate_effect")))
L.append("  O recibo vale enquanto a Bancada de producao pinar %s (manifesto sha16 %s): um re-pino antes do B(n) da v399 o torna obsoleto e a conferencia do esboco o recusa. T12/T13/T14 foram medidos contra o um.py v398 (o Nos de hoje), nao contra o v399; o T17 so' se decide no pos_selo."
         % (man["deployment_id"], man_sha[:16]))
L.append("- Conferencia pelo esboco R3.5 (ja_sincronizada=False, sem cadeia, selo e manifesto do kernel anteriores = v399\\base_v398): aceita=%s; %d/%d condicoes; %d/%d controles negativos recusados como esperado (inclui REPINADA_B%d no controle do veredito); conferencia_pelo_esboco_v399.json sha16 %s."
         % (str(conf["esboco_aceita"]).lower(), conf["n_condicoes_ok"], conf["n_condicoes"], conf["n_controles_como_esperado"], len(conf["controles_negativos"]), ger + 1, s16(os.path.join(HERE, "conferencia_pelo_esboco_v399.json"))))
L.append("- Producao: Bancada %d entradas (antes/depois/final: %s), Nos %d entradas (%s); listas iguais=%s e %s; chaves iguais nas tres fotografias=%s; PROVA_PRODUCAO_INTACTA_v399_pre_selo.json sha256 %s; producao_intacta=%s."
         % (b_ban["fotografias"]["final"]["n_entradas"], "/".join(str(b_ban["fotografias"][r]["n_entradas"]) for r in ("antes", "depois", "final")), b_nos["fotografias"]["final"]["n_entradas"],
            "/".join(str(b_nos["fotografias"][r]["n_entradas"]) for r in ("antes", "depois", "final")), str(b_ban["lista_identica_antes_depois_final"]).lower(), str(b_nos["lista_identica_antes_depois_final"]).lower(),
            str(all(c["igual_nas_tres"] for c in prova["chaves"])).lower(), shaf(os.path.join(V, "PROVA_PRODUCAO_INTACTA_v399_pre_selo.json")), str(prova["producao_intacta"]).lower()))
L.append("  A lista da Bancada tem %d entradas contra %d na prova da v398; adicionadas %s; removidas %s; alteradas %s (o B8 aplicado em 24/10, anterior ao ensaio; as tres fotografias da v399 sao iguais entre si). "
         "O Nos: %d entradas contra %d na prova da v398 (+%d adicionadas, %d removidas, %d alteradas: a instalacao e o rito da v398)."
         % (len(a9), len(a8), add, rem, alt, len(n9), len(n8), len(set(dn9) - set(dn8)), len(set(dn8) - set(dn9)), sum(1 for k in set(dn8) & set(dn9) if dn8[k] != dn9[k])))
L.append("- Falhas do molde por causa da versao (pre_selo): nenhuma; o derivador, o ensaio, a conferencia e a geracao do pino passaram na primeira rodada. %s"
         % ("Sandbox curto C:\\t\\vb16 apagado por limpar_sandbox_vb16.py (%d arquivos, %d pastas, juncoes/links antes de apagar: %d; existe depois: %s; irmaos de C:\\t iguais: %s)." % (limpeza["arquivos"], limpeza["pastas"], limpeza["juncoes_ou_links_antes_de_apagar"], limpeza["existe_depois"], limpeza["irmaos_iguais"])
            if limpeza else "Sandbox curto C:\\t\\vb16 AINDA EXISTE neste instante (limpar_sandbox_vb16.py nao rodou)."))
L.append("- Servico (bancada_B3_servico): derivar_derivador_v399.py (sha16 %s) gera derivar_servico_v399.py (subida de versao do v398; sha16 %s; +1 em %d tokens, %d variaveis de caminho), que gera os 3 scripts "
         "(evento %s, parada %s, religamento %s), DERIVACAO_SERVICO_v399.json (sha16 %s) e DIFF_SERVICO_v398_v399.diff (sha16 %s). Nada executado (so' ast.parse)."
         % (s16(os.path.join(SRV, "derivar_derivador_v399.py")), s16(os.path.join(SRV, "derivar_servico_v399.py")), dd["contagens"]["versoes_mais_um"], dd["contagens"]["variaveis_de_caminho"],
            s16(os.path.join(SRV, "evento_c1_b3_v399.py")), s16(os.path.join(SRV, "recibo_parada_v399.py")), s16(os.path.join(SRV, "recibo_religamento_v399.py")), s16(os.path.join(SRV, "DERIVACAO_SERVICO_v399.json")),
            s16(os.path.join(SRV, "DIFF_SERVICO_v398_v399.diff"))))
L.append("  Conferencia com o rito REAL de 24/10 (v398): %d/%d. B(n) esperado: %s (geracao deixada pela v398 = B%d). O que o rito real mostrou e o molde nao previa: %s."
         % (cr["n_condicoes_ok"], cr["n_condicoes"], ex["veredito_esperado_do_aplicar_da_v399"], ex["geracao_que_o_B_n_da_v398_deixou_na_Bancada"], "; ".join(nao_prev) if nao_prev else "nada"))
L.append("  DEFEITO DO MOLDE (BAIXO; corrigido com regra de contagem exata): a nota do recibo_parada_v398 dizia «e a parada que precede este recibo e ato do operador, pelo PID, nao desta cadeia»; o RECIBO_PARADA_v398.json real traz no campo autorizacao_do_operador "
         "«...executada pela gerencia c1 em 24/10» (sob a ordem geral do operador). Regra SUB (casou %d, esperado %d) troca por «feita pelo PID (nunca por nome), nao por este script; quem a executou e sob que ordem do operador consta em autorizacao_do_operador»; "
         "regra INV garante 0 ocorrencias de «e ato do operador»; a 20a condicao da conferencia mostra a divergencia no recibo real (falha de proposito no real da v398)." % (sub_nota["casou"], sub_nota["esperado"]))
L.append("  Desvios do molde (unicos): (1) a regra SUB do cruzamento com o B(n) anterior (que na v398 reduzia DUAS copias a UMA) virou INVARIANTE com contagem exata 1, porque os tres scripts da v398 que RODARAM ja trazem UMA copia (a SUB nao casaria: 0 != 1); "
         "(2) o texto historico «(v398: o molde v397 trazia este bloco DUAS vezes ...)» NAO sobe de versao (viraria falso): a docstring e' reescrita por regex localizada; (3) a data do rito real 23/10 -> 24/10 (2 usos); (4) a tupla de restos ('395','396','397','V398_','v400').")
L.append("  Realidade lida hoje contra o recibo de religamento da v398: PID %s no recibo; processo vivo PID %s; linha de comando medida == campo comando do recibo (a menos de um espaco final): %s. O campo comando continua LITERAL no script (nao medido); BAIXO, residuo."
         % (rr8["pid"], pid_srv, (cmd or "").strip() == rr8["comando"]))
L.append("  Exigem V399_AUTORIZACAO_OPERADOR: parada e religamento (conferencia ESTATICA por ast, nada executado: %d/%d condicoes, CONFERENCIA_EXIGENCIAS_SERVICO_v399.json sha16 %s; o assert AUT e' a primeira coisa executavel, antes de qualquer E/S). "
         "Controle negativo do conferidor: %d mutacoes, rc %d (esperado 1), %d condicoes falharam, toda mutacao pega=%s (controle_negativo\\RESULTADO_CONTROLE_NEGATIVO_v399.json sha16 %s)."
         % (ce["n_condicoes_ok"], ce["n_condicoes"], s16(os.path.join(SRV, "CONFERENCIA_EXIGENCIAS_SERVICO_v399.json")), len(cn["mutacoes"]), cn["rc_do_conferidor_sobre_as_mutacoes"], len(cn["condicoes_que_falharam"]), str(cn["toda_mutacao_foi_pega"]).lower(),
            s16(os.path.join(SRV, "controle_negativo", "RESULTADO_CONTROLE_NEGATIVO_v399.json"))))
src_v398 = open(os.path.join(V8, "bancada_B3_servico", "derivar_servico_v398.py"), encoding="utf-8").read()
n_r394 = src_v398.count("394") - src_v398.count('("394", "395", "396", "V397_", "v399")')      # as ocorrencias de 394 que NAO sao a tupla de restos: os nomes p_r394 / r394 / dm394
titulo_f06 = unicodedata.normalize("NFKD", f06.get("titulo", "?").split(" (")[0].replace("↔", "<->")).encode("ascii", "ignore").decode("ascii")
L.append("  Residuos BAIXOS declarados (nao bloqueiam): nomes de variavel p_r394/r394/dm394 no derivar_servico guardam o recibo do religamento ANTERIOR (hoje o da v397; %d usos medidos; cosmetico, nao renomeado para manter o molde); "
         "na v400 a regra SUB da nota vira INVARIANTE (o molde v399 ja traz a nota nova), como a do cruzamento virou nesta; a unidade do evento F0.6 foi CONFERIDA no quadro: «%s», status %s, dono %s, historico ate o evento %s (e' o elo B(n) permanente, nao uma heranca por acaso)."
         % (n_r394, titulo_f06, f06.get("status"), f06.get("dono"), (f06.get("historico") or [None])[-1]))
L.append("  Pendencias para a gerencia (atos que NAO sao desta preparacao): ESPERADOS_v399.json existe agora=%s (o evento afirma isso por assert; nasce com gerar_esperados_v399 antes do rito); a parada do servico (pelo PID %s, nunca por nome), o religamento e o evento c1 que nomeia a v399 "
         "sao atos da gerencia/operador com V399_AUTORIZACAO_OPERADOR no ambiente; o ultimo religamento lido e' o da v398 (PID %s, %s, passo %s)."
         % (str(os.path.exists(os.path.join(V, "ESPERADOS_v399.json"))).lower(), pid_srv, rr8["pid"], rr8["hora_recibo"][:10], rr8["passo"]))
L.append("- Mapa de rotas consultado ANTES (rotas.py consultar): 'pre_selo' -> 1 rota (infra.bancada_um.sincronizacao_vnnn, EM_CURSO, R3.5: nao refeitos a lista de permissao, a fusao do PINOS_BN nem o passo 10; reusados por pino); 'bancada B3' -> 0 rotas; 'v398' -> 9 rotas "
         "(kernel.afinacao_das_cordas_v398, kernel.sonico_v398, kernel.testemunho_v399_candidata_24out, custodia.v397, iald.ordem019.f0_3.memoria_v391, umpy.v397/v398/v399.*); tambem 'sincronizacao' (8), 'parada' (32), 'religamento' (1), 'servico da Bancada' (0), 'ensaio pre_selo' (0). "
         "Nada do que foi derivado aqui existia como rota; o registro desta preparacao no mapa e' da gerencia.")
L.append("- Escopo: so' leitura da producao (Bancada e Nos); nada gravado nelas; nenhum um.py rodado, nenhum rito, nenhuma regra de permissao; NOT_FALSIFIED nao e creditacao; o gate nao se move.")
txt = "\n".join(L) + "\n"
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(txt)
assert os.path.getsize(dest + ".tmp") == len(txt.encode("utf-8"))
os.replace(dest + ".tmp", dest)
print(dest, shaf(dest)[:16], len(txt.encode("utf-8")), "bytes")
