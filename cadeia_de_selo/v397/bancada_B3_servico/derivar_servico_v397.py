# -*- coding: utf-8 -*-
"""derivar_servico_v397.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os tres scripts de servico do B(n) da v397 a partir dos da v396 (v396\\bancada_B3_servico\\):
evento_c1_b3_v396.py -> evento_c1_b3_v397.py, recibo_parada_v396.py -> recibo_parada_v397.py, recibo_religamento_v396.py -> recibo_religamento_v397.py.
1) mapa mecanico das versoes, numa passada so (as referencias v396 viram v397 e as v395 viram v396; rel395 vira rel396; a variavel de ambiente V396_AUTORIZACAO_OPERADOR vira V397_AUTORIZACAO_OPERADOR);
2) regras nomeadas, cada uma com a contagem exata (o script aborta se a regra nao casar o numero esperado de vezes). Os padroes estao escritos como o texto fica DEPOIS do mapa. Dois tipos:
   - INVARIANTE (confere que o texto mapeado traz a regra semantica da v396 subindo uma versao; nao altera nada):
       * passo simples, SEM salto: a Bancada de producao pina a v396 e o Nos passa a v397; o veredito esperado do aplicar e' REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO,
         com n = a geracao do manifesto anterior + 1, e SEM o trecho __SALTO_;
       * evento: o hash esperado do um.py NAO e digitado: e' lido em tempo de execucao de v397\\ESPERADOS_v397.json (campo candidato_sha16), com assert e mensagem clara se o arquivo ainda nao existe
         (ele so' nasce com gerar_esperados_v397, antes do rito); nenhum hash literal no script;
       * parada: a data do ultimo religamento (v396) e' LIDA do RECIBO_RELIGAMENTO_v396.json real (nao fica data digitada), e a nota nao afirma que o servico ja estava fora do ar;
       * parada e religamento: nao se presume autorizacao: o script exige V397_AUTORIZACAO_OPERADOR no ambiente e a grava no recibo; a frase «por autorizacao geral do operador» nao existe;
   - SUBSTITUICAO (uma so', no religamento): alem de calcular n a partir do manifesto anterior do proprio recibo do B(n) da v397 (como no molde), o script cruza esse n com a geracao que o recibo do B(n) da
     v396 (RECIBO_SINCRONIZACAO_v396_*.json, manifesto_novo.deployment_id) deixou na Bancada: «n = geracao do manifesto anterior (lida do recibo do B(n) da v396) + 1»; assert com mensagem clara;
3) ast.parse de cada saida (so' compila, nao executa); diff unificado e relatorio JSON com sha256 de entrada e de saida; e a CONFERENCIA, so' por leitura, do que os scripts v396 previam contra o que o
   rito REAL de 22/10 gravou (RECIBO_PARADA_v396.json, RECIBO_RELIGAMENTO_v396.json, recibo do B(n) da v396): chaves, ordem, passos, PID, datas, hashes, ordem dos atos.
Escreve so' em v397\\bancada_B3_servico\\ (arquivos novos; nao sobrescreve; tudo ou nada: calcula e confere as tres saidas antes de gravar a primeira). Le v395\\ e v396\\ e o esboco pinado (so' leitura).
uso: python -I -B -X utf8 derivar_servico_v397.py"""
import sys

sys.dont_write_bytecode = True
import ast
import datetime
import difflib
import glob
import hashlib
import json
import os
import re

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
CS = os.path.dirname(V)
V6 = os.path.join(CS, "v396")
V6S = os.path.join(V6, "bancada_B3_servico")
V5S = os.path.join(CS, "v395", "bancada_B3_servico")
MAPA = {"v396": "v397", "v395": "v396", "rel395": "rel396", "V396_AUTORIZACAO_OPERADOR": "V397_AUTORIZACAO_OPERADOR"}
RE_MAPA = re.compile(r"V396_AUTORIZACAO_OPERADOR|v396|v395|rel395")
INV, SUB = "invariante", "substituicao"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def lj(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def mapear(t):
    return RE_MAPA.sub(lambda m: MAPA[m.group(0)], t)


# a linha do molde que calcula n; a SUBSTITUICAO acrescenta, logo depois dela, o cruzamento com o B(n) da v396
N_ESP_LINHA = 'n_esp = int(b["manifesto_anterior"]["deployment_id"].split("-")[0][1:]) + 1   # B<n>: a geracao do manifesto anterior + 1\n'
CRUZA_BLOCO = N_ESP_LINHA + (
    'rb_ant = sorted(glob.glob(os.path.join(D, "..", "..", "v396", "bancada_B3", "RECIBO_SINCRONIZACAO_v396_*.json")))\n'
    'assert len(rb_ant) == 1, rb_ant\n'
    'ger_ant = int(json.load(open(rb_ant[0], encoding="utf-8"))["manifesto_novo"]["deployment_id"].split("-")[0][1:])   # a geracao que o B(n) da v396 deixou na Bancada\n'
    'assert n_esp == ger_ant + 1, ("o manifesto anterior do B(n) da v397 nao e o que o B(n) da v396 deixou na Bancada", n_esp, ger_ant)\n')
AUT_AUTOR = '"autor": "claude-c1 (gerencia)", "autorizacao_do_operador": AUT}'
AUT_EXIGIDA = 'assert AUT, "defina V397_AUTORIZACAO_OPERADOR com a ordem do operador que cobre este ato (data e texto): o script nao presume autorizacao"'

# (nome da regra, tipo, padrao [regex, sobre o texto JA MAPEADO], texto novo (so' SUB), vezes esperadas)
REGRAS = {
    "evento_c1_b3_v396.py": [
        ("docstring_passo_simples_sem_salto", INV, re.escape("(passo simples v396 -> v397, sem salto)"), None, 1),
        ("versao_nova_no_evento", INV, re.escape('dados = {"versao": "v397", "acao": "sincronizacao"'), None, 1),
        ("unidade_herdada_do_molde", INV, re.escape('"unidade": "F0.6"'), None, 1),
        ("esperados_da_v397_lido_em_execucao", INV, re.escape('ESP = os.path.join(D, "..", "ESPERADOS_v397.json")'), None, 1),
        ("assert_se_esperados_ainda_nao_existe", INV, r'assert os\.path\.isfile\(ESP\), "ESPERADOS_v397\.json nao existe ainda \(e gerado antes do rito, por gerar_esperados_v397\)', None, 1),
        ("candidato_lido_do_arquivo", INV, re.escape('CAND16 = json.load(open(ESP, encoding="utf-8"))["candidato_sha16"]'), None, 1),
        ("um_py_do_nos_conferido_contra_o_candidato", INV,
         re.escape('assert dados["um_py"].startswith(CAND16), ("o um.py do Nos nao e o candidato de ESPERADOS_v397.json", dados["um_py"][:16], CAND16)'), None, 1),
        ("nenhum_hash_literal_no_script", INV, r'"[0-9a-f]{16,64}"', None, 0),
    ],
    "recibo_parada_v396.py": [
        ("docstring_no_molde_da_anterior", INV, re.escape('"""10-bis-a da v397: recibo da parada do servico da Bancada Um (porta 18777), no molde do recibo_parada_v396.py."""'), None, 1),
        ("autorizacao_do_operador_no_ambiente", INV, r"V397_AUTORIZACAO_OPERADOR", None, 2),
        ("autorizacao_exigida", INV, re.escape(AUT_EXIGIDA), None, 1),
        ("recibo_de_religamento_anterior_lido_da_v396", INV,
         re.escape('rel396 = json.load(open(os.path.join(D, "..", "..", "v396", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v396.json"), encoding="utf-8"))'), None, 1),
        ("pid_estado_com_a_data_do_religamento_da_v396", INV,
         re.escape('"pid_estado": "ultimo PID conhecido do servico (religamento da v396, %s/%s); o processo ja nao existe" % (rel396["hora_recibo"][8:10], rel396["hora_recibo"][5:7]),'), None, 1),
        ("nota_cita_o_religamento_da_v396", INV, r"foi religado no passo %s da v396 \(PID %s\)", None, 1),
        ("nota_nao_afirma_servico_fora_do_ar", INV, r"ja estava fora do ar", None, 0),
        ("autor_com_a_autorizacao_do_ambiente", INV, re.escape(AUT_AUTOR), None, 1),
        ("sem_autorizacao_geral_presumida", INV, r"por autorizacao geral do operador", None, 0),
        ("recibo_da_parada_v397", INV, re.escape('"RECIBO_PARADA_v397.json"'), None, 1),
    ],
    "recibo_religamento_v396.py": [
        ("docstring_no_molde_da_anterior", INV, re.escape('"""10-ter da v397: recibo do religamento do servico da Bancada Um, no molde do recibo_religamento_v396.py + completar_recibos.py.'), None, 1),
        ("autorizacao_do_operador_no_ambiente", INV, r"V397_AUTORIZACAO_OPERADOR", None, 2),
        ("autorizacao_exigida", INV, re.escape(AUT_EXIGIDA), None, 1),
        ("recibo_do_B_n_da_v397_lido", INV, re.escape('glob.glob(os.path.join(D, "..", "bancada_B3", "RECIBO_SINCRONIZACAO_v397_*.json"))'), None, 1),
        ("veredito_do_aplicar_REPINADA_Bn", INV,
         re.escape('assert b["veredito"].startswith("REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % n_esp), b["veredito"]'), None, 1),
        ("veredito_sem_salto", INV, re.escape('assert "__SALTO_" not in b["veredito"], b["veredito"]   # passo simples: a Bancada pinava a v396 e o Nos passou a v397'), None, 1),
        ("versao_servida_v397", INV, re.escape('assert c.get("canonical_version") == "v397", c.get("canonical_version")'), None, 1),
        ("autor_com_a_autorizacao_do_ambiente", INV, re.escape(AUT_AUTOR), None, 1),
        ("sem_autorizacao_geral_presumida", INV, r"por autorizacao geral do operador", None, 0),
        ("recibo_de_religamento_v397", INV, re.escape('"RECIBO_RELIGAMENTO_v397.json"'), None, 1),
        ("n_confere_com_o_B_n_da_v396", SUB, r"^" + re.escape(N_ESP_LINHA), CRUZA_BLOCO, 1),
    ],
}


def derivar(nome):
    with open(os.path.join(V6S, nome), "rb") as fh:
        bruto = fh.read()
    texto = bruto.decode("utf-8")
    assert "\r" not in texto, "a fonte tem CR: nao e' o formato esperado"
    t = mapear(texto)
    aplicadas = []
    for rnome, tipo, padrao, novo, n_esp in REGRAS[nome]:
        rx = re.compile(padrao, re.M | re.S)
        achados = rx.findall(t)
        assert len(achados) == n_esp, ("a regra %s casou %d vez(es), esperado %d" % (rnome, len(achados), n_esp), nome)
        if tipo == SUB:
            t, k = rx.subn(lambda m, novo=novo: novo, t)
            assert k == n_esp
        aplicadas.append({"regra": rnome, "tipo": tipo, "casou": len(achados), "esperado": n_esp})
    ast.parse(t)      # so' compila; nada e' executado
    restos = {k: len(re.findall(k, t)) for k in ("393", "394", "395", "V396_", "v398")}
    assert not any(restos.values()), ("restou referencia a versao fora do mapa", nome, restos)
    return bruto, t, aplicadas, restos


def chaves_e_constantes(texto, var):
    """(chaves na ordem, {chave: valor constante}) do dict literal atribuido a `var` (ast); (None, None) se nao houver."""
    for no in ast.walk(ast.parse(texto)):
        if isinstance(no, ast.Assign) and isinstance(no.value, ast.Dict) and any(isinstance(t, ast.Name) and t.id == var for t in no.targets):
            chaves = [k.value for k in no.value.keys if isinstance(k, ast.Constant)]
            consts = {k.value: v.value for k, v in zip(no.value.keys, no.value.values) if isinstance(k, ast.Constant) and isinstance(v, ast.Constant)}
            return chaves, consts
    return None, None


def chaves_evento_do_esboco(esb):
    for no in ast.walk(ast.parse(open(esb, encoding="utf-8").read())):
        if isinstance(no, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CHAVES_EVENTO" for t in no.targets):
            return sorted(e.value for e in no.value.args[0].elts)
    return None


def geracao(deployment_id):
    return int(str(deployment_id).split("-")[0][1:])      # B<n>-...


def conferir_rito_real():
    """O que os scripts v396 previam, contra o que o rito REAL de 22/10 gravou. So leitura; nada e' executado."""
    checks = []

    def chk(nome, ok, observado, esperado):
        checks.append({"nome": nome, "ok": bool(ok), "observado": observado, "esperado": esperado})

    fontes = {n: open(os.path.join(V6S, n), encoding="utf-8").read() for n in REGRAS}
    bn_p = sorted(glob.glob(os.path.join(V6, "bancada_B3", "RECIBO_SINCRONIZACAO_v396_*.json")))
    assert len(bn_p) == 1, bn_p
    bn_raw = open(bn_p[0], "rb").read()
    bn = json.loads(bn_raw.decode("utf-8"))
    p_par, p_rel, p_r394 = (os.path.join(V6S, "RECIBO_PARADA_v396.json"), os.path.join(V6S, "RECIBO_RELIGAMENTO_v396.json"), os.path.join(V5S, "RECIBO_RELIGAMENTO_v395.json"))
    rp, rr, r394 = lj(p_par), lj(p_rel), lj(p_r394)
    esp5 = lj(os.path.join(V6, "ESPERADOS_v396.json"))
    pinos = lj(os.path.join(V6, "PINOS_BN_v396.json"))
    esb, esb_sha = pinos["esboco_R3_5"]["path"], pinos["esboco_R3_5"]["sha256"]
    assert sha(open(esb, "rb").read()) == esb_sha, "o esboco R3.5 em disco nao e o pinado"

    k_par, c_par = chaves_e_constantes(fontes["recibo_parada_v396.py"], "rec")
    k_rel, c_rel = chaves_e_constantes(fontes["recibo_religamento_v396.py"], "rec")
    k_ev, _c_ev = chaves_e_constantes(fontes["evento_c1_b3_v396.py"], "dados")
    k_esb = chaves_evento_do_esboco(esb)
    chk("parada: chaves do script v396 (ordem) = chaves do recibo real", k_par == list(rp.keys()), [k_par, list(rp.keys())], "listas iguais")
    chk("religamento: chaves do script v396 (ordem) = chaves do recibo real", k_rel == list(rr.keys()), [k_rel, list(rr.keys())], "listas iguais")
    chk("evento: chaves do script v396 dentro do conjunto fechado CHAVES_EVENTO do esboco pinado", k_ev is not None and k_esb is not None and set(k_ev) <= set(k_esb), [k_ev, k_esb], "subconjunto")
    chk("parada: passo do script = passo do recibo real", c_par.get("passo") == rp.get("passo"), [c_par.get("passo"), rp.get("passo")], "iguais")
    chk("religamento: passo do script = passo do recibo real", c_rel.get("passo") == rr.get("passo"), [c_rel.get("passo"), rr.get("passo")], "iguais")
    chk("parada: o PID gravado e' o do religamento anterior (v395)", rp["pid"] == r394["pid"], [rp["pid"], r394["pid"]], "iguais")
    dm394 = "%s/%s" % (r394["hora_recibo"][8:10], r394["hora_recibo"][5:7])
    chk("parada: o pid_estado traz a data (DD/MM) do religamento anterior, lida do recibo dele", dm394 in rp["pid_estado"], [dm394, rp["pid_estado"]], "data contida")
    chk("parada: a nota cita o passo e o PID do religamento anterior", str(r394["passo"]) in rp["nota"] and str(r394["pid"]) in rp["nota"], [r394["passo"], r394["pid"]], "ambos contidos")
    chk("parada: porta fechada e zero processos vivos", rp["porta_fechada"] is True and rp["processos_um_bancada_vivos"] == 0, [rp["porta_fechada"], rp["processos_um_bancada_vivos"]], "True e 0")
    chk("parada: autorizacao do operador gravada (nao vazia)", bool(str(rp.get("autorizacao_do_operador") or "").strip()), len(str(rp.get("autorizacao_do_operador") or "")), "> 0")
    chk("religamento: autorizacao do operador gravada (nao vazia)", bool(str(rr.get("autorizacao_do_operador") or "").strip()), len(str(rr.get("autorizacao_do_operador") or "")), "> 0")
    man_novo = bn["aplicacao"]["pos_conferencia"]["canonical_manifest_sha256"]
    chk("religamento: versao servida = v396", rr["versao_servida"] == "v396" and rr["identidade"]["canonical_version"] == "v396", [rr["versao_servida"], rr["identidade"]["canonical_version"]], "v396 e v396")
    chk("religamento: manifesto servido = o do aplicar (pos_conferencia) = identidade", rr["manifesto_sha256"] == man_novo == rr["identidade"]["canonical_manifest_sha256"],
        [rr["manifesto_sha256"][:16], man_novo[:16], rr["identidade"]["canonical_manifest_sha256"][:16]], "tres iguais")
    chk("religamento: o recibo cita o recibo do B(n) pelo sha256 lido na hora", rr["recibo_do_10_bis"]["sha256"] == sha(bn_raw) and os.path.samefile(rr["recibo_do_10_bis"]["path"], bn_p[0]),
        [rr["recibo_do_10_bis"]["sha256"][:16], sha(bn_raw)[:16]], "iguais")
    chk("religamento: um.py servido comeca por ESPERADOS_v396.candidato_sha16", rr["identidade"]["um_py_sha256"].startswith(esp5["candidato_sha16"]), [rr["identidade"]["um_py_sha256"][:16], esp5["candidato_sha16"]], "prefixo")
    chk("religamento: o deployment servido = o manifesto_novo do B(n)", rr["identidade"]["deployment_id"] == bn["manifesto_novo"]["deployment_id"], [rr["identidade"]["deployment_id"], bn["manifesto_novo"]["deployment_id"]], "iguais")
    n_real = geracao(bn["manifesto_anterior"]["deployment_id"]) + 1
    chk("B(n) real: veredito segue a regra do passo simples (REPINADA_B<n> com n = anterior + 1, sem __SALTO_)",
        bn["veredito"].startswith("REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % n_real) and "__SALTO_" not in bn["veredito"], [bn["veredito"], n_real], "prefixo e sem salto")
    t_par = datetime.datetime.fromisoformat(rp["hora_recibo"])
    t_ev = datetime.datetime.fromisoformat(bn["evento_c1"]["quando"])
    t_rel = datetime.datetime.fromisoformat(rr["hora_recibo"])
    chk("ordem dos atos: recibo de parada <= evento c1 <= recibo de religamento", t_par <= t_ev <= t_rel, [rp["hora_recibo"], bn["evento_c1"]["quando"], rr["hora_recibo"]], "ordem crescente")
    chk("evento real: verificado pela cadeia de hash do quadro", bn["evento_c1"].get("verificado") is True and bn["evento_c1"].get("fonte_e_o_quadro") is True,
        [bn["evento_c1"].get("verificado"), bn["evento_c1"].get("fonte_e_o_quadro")], "True e True")
    ger_deixada = geracao(bn["manifesto_novo"]["deployment_id"])
    esperado = {
        "geracao_que_o_B_n_da_v396_deixou_na_Bancada": ger_deixada,
        "n_esperado_no_B_n_da_v397": ger_deixada + 1,
        "veredito_esperado_do_aplicar_da_v397": "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % (ger_deixada + 1),
        "sem_salto": "a Bancada pinava a v396 e o Nos passa a v397",
        "ultimo_religamento_lido": {"path": p_rel, "sha256": sha(open(p_rel, "rb").read()), "pid": rr["pid"], "passo": rr["passo"], "hora_recibo": rr["hora_recibo"]},
        "pid_estado_previsto_no_recibo_de_parada": "ultimo PID conhecido do servico (religamento da v396, %s/%s); o processo ja nao existe" % (rr["hora_recibo"][8:10], rr["hora_recibo"][5:7]),
        "variavel_de_ambiente_exigida_na_parada_e_no_religamento": "V397_AUTORIZACAO_OPERADOR",
        "arquivo_que_o_evento_le_em_execucao": {"path": os.path.join(V, "ESPERADOS_v397.json"), "existe_agora": os.path.isfile(os.path.join(V, "ESPERADOS_v397.json")),
                                                  "campo": "candidato_sha16", "gerado_por": "gerar_esperados_v397.py, antes do rito"},
        "recibo_do_B_n_da_v397_que_o_religamento_espera": os.path.join(V, "bancada_B3", "RECIBO_SINCRONIZACAO_v397_*.json"),
    }
    return {"recibos_reais_lidos": {"parada": {"path": p_par, "sha256": sha(open(p_par, "rb").read())}, "religamento": {"path": p_rel, "sha256": sha(open(p_rel, "rb").read())},
                                    "religamento_anterior_v395": {"path": p_r394, "sha256": sha(open(p_r394, "rb").read())}, "B_n_v396": {"path": bn_p[0], "sha256": sha(bn_raw)}},
            "esboco_pinado": {"path": esb, "sha256": esb_sha},
            "condicoes": checks, "n_condicoes": len(checks), "n_condicoes_ok": sum(1 for c in checks if c["ok"]),
            "algo_que_os_scripts_v396_nao_previam": [c["nome"] for c in checks if not c["ok"]]}, esperado


def main():
    me = os.path.abspath(__file__)
    rel = {"contrato": "DERIVACAO_SERVICO_v397", "script": {"path": me, "sha256": sha(open(me, "rb").read())},
           "fonte_dir": V6S, "saida_dir": HERE, "mapa_de_versoes": MAPA, "executado": False, "arquivos": []}
    prontos = []
    for nome in REGRAS:
        bruto, novo, aplicadas, restos = derivar(nome)
        destino = RE_MAPA.sub(lambda m: MAPA[m.group(0)], nome)
        dp = os.path.join(HERE, destino)
        if os.path.exists(dp):
            raise SystemExit("ja existe, nao sobrescrevo: " + dp)
        prontos.append((nome, destino, dp, bruto, novo, aplicadas, restos))
    conf, esperado = conferir_rito_real()
    difp = os.path.join(HERE, "DIFF_SERVICO_v396_v397.diff")
    rp = os.path.join(HERE, "DERIVACAO_SERVICO_v397.json")
    for p in (difp, rp):
        if os.path.exists(p):
            raise SystemExit("ja existe, nao sobrescrevo: " + p)
    diffs = []
    for nome, destino, dp, bruto, novo, aplicadas, restos in prontos:       # so' aqui comeca a gravar: as tres saidas ja passaram em todas as regras
        dados = novo.encode("utf-8")
        with open(dp + ".tmp", "wb") as fh:
            fh.write(dados)
        if os.path.getsize(dp + ".tmp") != len(dados):
            raise SystemExit("tamanho do temporario nao confere: " + dp)
        os.replace(dp + ".tmp", dp)
        ast.parse(open(dp, encoding="utf-8").read())
        diffs.append("".join(difflib.unified_diff(bruto.decode("utf-8").splitlines(True), novo.splitlines(True),
                                                   fromfile="v396/bancada_B3_servico/" + nome, tofile="v397/bancada_B3_servico/" + destino)))
        rel["arquivos"].append({"fonte": {"path": os.path.join(V6S, nome), "bytes": len(bruto), "sha256": sha(bruto)}, "saida": {"path": dp, "bytes": len(dados), "sha256": sha(dados)},
                                "regras_aplicadas": aplicadas, "ast_parse": "ok", "referencias_residuais_fora_do_mapa": restos})
    alldiff = "\n".join(diffs)
    with open(difp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(alldiff)
    rel["diff_unificado"] = {"path": difp, "sha256": sha(open(difp, "rb").read())}
    rel["conferencia_com_o_rito_real_da_v396"] = conf
    rel["expectativa_do_B_n_da_v397"] = esperado
    rel["escopo"] = "so leitura de v395\\ e v396\\; escreve so' em v397\\bancada_B3_servico\\; os tres scripts derivados NAO foram executados; NOT_FALSIFIED nao e creditacao; o gate nao se move"
    with open(rp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({a["saida"]["path"]: {"sha16": a["saida"]["sha256"][:16], "bytes": a["saida"]["bytes"], "regras": len(a["regras_aplicadas"])} for a in rel["arquivos"]}, ensure_ascii=False, indent=1))
    print("conferencia com o rito real:", "%d/%d" % (conf["n_condicoes_ok"], conf["n_condicoes"]), "nao previstos:", conf["algo_que_os_scripts_v396_nao_previam"])
    print("B(n) da v397 esperado:", esperado["veredito_esperado_do_aplicar_da_v397"])
    print("DERIVACAO:", rp, sha(open(rp, "rb").read())[:16])
    print("DIFF:", difp, rel["diff_unificado"]["sha256"][:16])


if __name__ == "__main__":
    main()
