# -*- coding: utf-8 -*-
"""derivar_servico_v395.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os tres scripts de servico do B(n) da v395 a partir dos da v394 (v394\\bancada_B3_servico\\):
evento_c1_b3_v394.py -> evento_c1_b3_v395.py, recibo_parada_v394.py -> recibo_parada_v395.py, recibo_religamento_v394.py -> recibo_religamento_v395.py.
1) mapa mecanico das versoes, numa passada so (as referencias v394 viram v395 e as v392 viram v394; rel392 vira rel394);
2) edicoes SEMANTICAS nomeadas, cada uma com a contagem exata (o script aborta se a regra nao casar o numero esperado de vezes). Os padroes estao escritos como o texto fica DEPOIS do mapa:
   - evento: o hash esperado do um.py NAO e digitado: e' lido em tempo de execucao de v395\\ESPERADOS_v395.json (campo candidato_sha16), com assert e mensagem clara se o arquivo ainda nao existe;
   - evento, parada e religamento: o passo da v395 NAO e' salto (a Bancada de producao pina a v394 e o Nos passa a v395): o veredito esperado do aplicar e' REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO,
     com n = a geracao do manifesto anterior (lida do recibo do B(n)) + 1, e SEM o trecho __SALTO_ (no esboco R3.5 o veredito_base e' REPINADA_B<n> e o __SALTO_ so' entra quando o recibo pre_selo declara salto);
   - parada: a data do ultimo religamento e' lida do recibo da v394 (nao fica a data de 13/10 da v392), e a nota nao afirma que o servico ja estava fora do ar (isso valia para a v394);
   - parada e religamento: a frase «por autorizacao geral do operador (13/10 e 19/10)» NAO e' copiada (nao se presume autorizacao para a v395): o script exige V395_AUTORIZACAO_OPERADOR no ambiente e a grava no recibo;
3) ast.parse de cada saida (so' compila, nao executa); diff unificado e relatorio JSON com sha256 de entrada e de saida.
Escreve so' em v395\\bancada_B3_servico\\ (arquivos novos; nao sobrescreve). uso: python -I -B -X utf8 derivar_servico_v395.py"""
import sys

sys.dont_write_bytecode = True
import ast
import difflib
import hashlib
import json
import os
import re

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
V4S = os.path.join(os.path.dirname(V), "v394", "bancada_B3_servico")
MAPA = {"v392": "v394", "v394": "v395", "rel392": "rel394"}
RE_MAPA = re.compile(r"v392|v394|rel392")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def mapear(t):
    return RE_MAPA.sub(lambda m: MAPA[m.group(0)], t)


D_LINHA = "D = os.path.dirname(os.path.abspath(__file__))\n"
# nao se presume autorizacao para a v395: o ato cita a ordem do operador no ambiente
AUT_BLOCO = ('AUT = os.environ.get("V395_AUTORIZACAO_OPERADOR", "").strip()\n'
             'assert AUT, "defina V395_AUTORIZACAO_OPERADOR com a ordem do operador que cobre este ato (data e texto): o script nao presume autorizacao"\n')
# o veredito esperado do aplicar SEM salto: a geracao n = a do manifesto anterior (lida do recibo do B(n)) + 1
VEREDITO_BLOCO = ('n_esp = int(b["manifesto_anterior"]["deployment_id"].split("-")[0][1:]) + 1   # B<n>: a geracao do manifesto anterior + 1\n'
                  'assert b["veredito"].startswith("REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % n_esp), b["veredito"]\n'
                  'assert "__SALTO_" not in b["veredito"], b["veredito"]   # passo simples: a Bancada pinava a v394 e o Nos passou a v395\n')
# o hash esperado do um.py: lido de ESPERADOS_v395.json em tempo de execucao
ESPERADOS_BLOCO = ('D = os.path.dirname(os.path.abspath(__file__))\n'
                   'ESP = os.path.join(D, "..", "ESPERADOS_v395.json")\n'
                   'assert os.path.isfile(ESP), "ESPERADOS_v395.json nao existe ainda (e gerado antes do rito, por gerar_esperados_v395): sem ele o um.py do Nos nao tem com que ser conferido; nada foi anotado no quadro"\n'
                   'CAND16 = json.load(open(ESP, encoding="utf-8"))["candidato_sha16"]\n'
                   'assert len(CAND16) >= 16, CAND16\n'
                   'assert dados["um_py"].startswith(CAND16), ("o um.py do Nos nao e o candidato de ESPERADOS_v395.json", dados["um_py"][:16], CAND16)\n')
PARADA_PID_ESTADO = '"pid_estado": "ultimo PID conhecido do servico (religamento da v394, %s/%s); o processo ja nao existe" % (rel394["hora_recibo"][8:10], rel394["hora_recibo"][5:7]),\n'
PARADA_NOTA = ('"nota": ("nenhum processo um_bancada.py vivo e a porta 18777 fechada, conferidos por este script no momento do recibo; o script nao para nada: o servico foi religado no passo %s da v394 (PID %s), "\n'
               '                "e a parada que precede este recibo e ato do operador, pelo PID, nao desta cadeia" % (rel394.get("passo"), pid_ultimo)),\n')
AUTOR_NOVO = '"autor": "claude-c1 (gerencia)", "autorizacao_do_operador": AUT}'
RE_AUTOR = r'"autor": "claude-c1 \(gerencia\), por autorizacao geral do operador \(\d\d/\d\d e \d\d/\d\d\)"\}'

# (nome da regra, padrao [regex, sobre o texto JA MAPEADO], texto novo, vezes esperadas)
REGRAS = {
    "evento_c1_b3_v394.py": [
        ("docstring_sem_salto", re.escape("(salto v394 -> v395)"), "(passo simples v394 -> v395, sem salto)", 1),
        ("import_os", r"^import json\nimport subprocess\n", "import json\nimport os\nimport subprocess\n", 1),
        ("hash_esperado_lido_de_ESPERADOS", r'^assert dados\["um_py"\]\.startswith\("[0-9a-f]{16}"\), dados\["um_py"\]\[:16\]\n', ESPERADOS_BLOCO, 1),
    ],
    "recibo_parada_v394.py": [
        ("autorizacao_no_ambiente", r"^" + re.escape(D_LINHA), D_LINHA + AUT_BLOCO, 1),
        ("pid_estado_com_a_data_do_religamento_da_v394", r'"pid_estado": "ultimo PID conhecido do servico \(religamento da v394, \d\d/\d\d\); o processo ja nao existe",\n', PARADA_PID_ESTADO, 1),
        ("nota_nao_afirma_servico_fora_do_ar", r'"nota": "o servico ja estava fora do ar antes da v395 .*?por esta cadeia",\n', PARADA_NOTA, 1),
        ("autor_sem_autorizacao_presumida", RE_AUTOR, AUTOR_NOVO, 1),
    ],
    "recibo_religamento_v394.py": [
        ("autorizacao_no_ambiente", r"^" + re.escape(D_LINHA), D_LINHA + AUT_BLOCO, 1),
        ("veredito_do_aplicar_sem_salto", r'^assert b\["veredito"\]\.startswith\("REPINADA_B\d+__SALTO_v\d+_v\d+__APLICADA"\), b\["veredito"\]\n', VEREDITO_BLOCO, 1),
        ("autor_sem_autorizacao_presumida", RE_AUTOR, AUTOR_NOVO, 1),
    ],
}


def derivar(nome):
    bruto = open(os.path.join(V4S, nome), "rb").read()
    texto = bruto.decode("utf-8")
    assert "\r" not in texto, "a fonte tem CR: nao e' o formato esperado"
    t = mapear(texto)
    aplicadas = []
    for rnome, padrao, novo, n_esp in REGRAS[nome]:
        rx = re.compile(padrao, re.M | re.S)
        achados = rx.findall(t)
        assert len(achados) == n_esp, ("a regra %s casou %d vez(es), esperado %d" % (rnome, len(achados), n_esp), nome)
        t, k = rx.subn(lambda m, novo=novo: novo, t)
        assert k == n_esp
        aplicadas.append({"regra": rnome, "casou": k})
    ast.parse(t)      # so' compila; nada e' executado
    restam_392 = re.findall(r"392", t)
    return bruto, t, aplicadas, restam_392


def main():
    rel = {"contrato": "DERIVACAO_SERVICO_v395", "script": {"path": os.path.abspath(__file__), "sha256": sha(open(os.path.abspath(__file__), "rb").read())},
           "fonte_dir": V4S, "saida_dir": HERE, "mapa_de_versoes": MAPA, "executado": False, "arquivos": []}
    diffs = []
    for nome in REGRAS:
        bruto, novo, aplicadas, restam_392 = derivar(nome)
        assert not restam_392, ("restou referencia a 392", nome)
        destino = nome.replace("v394", "v395")
        dp = os.path.join(HERE, destino)
        if os.path.exists(dp):
            raise SystemExit("ja existe, nao sobrescrevo: " + dp)
        dados = novo.encode("utf-8")
        with open(dp + ".tmp", "wb") as fh:
            fh.write(dados)
        if os.path.getsize(dp + ".tmp") != len(dados):
            raise SystemExit("tamanho do temporario nao confere: " + dp)
        os.replace(dp + ".tmp", dp)
        ast.parse(open(dp, encoding="utf-8").read())
        diffs.append("".join(difflib.unified_diff(bruto.decode("utf-8").splitlines(True), novo.splitlines(True),
                                                   fromfile="v394/bancada_B3_servico/" + nome, tofile="v395/bancada_B3_servico/" + destino)))
        rel["arquivos"].append({"fonte": {"path": os.path.join(V4S, nome), "bytes": len(bruto), "sha256": sha(bruto)}, "saida": {"path": dp, "bytes": len(dados), "sha256": sha(dados)},
                                "regras_aplicadas": aplicadas, "ast_parse": "ok", "referencias_a_392_que_restam": 0})
    difp = os.path.join(HERE, "DIFF_SERVICO_v394_v395.diff")
    rp = os.path.join(HERE, "DERIVACAO_SERVICO_v395.json")
    for p in (difp, rp):
        if os.path.exists(p):
            raise SystemExit("ja existe, nao sobrescrevo: " + p)
    alldiff = "\n".join(diffs)
    with open(difp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(alldiff)
    rel["diff_unificado"] = {"path": difp, "sha256": sha(open(difp, "rb").read())}
    with open(rp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({a["saida"]["path"]: {"sha16": a["saida"]["sha256"][:16], "regras": [x["regra"] for x in a["regras_aplicadas"]]} for a in rel["arquivos"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
