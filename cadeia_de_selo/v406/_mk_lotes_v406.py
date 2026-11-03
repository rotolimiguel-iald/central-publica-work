# -*- coding: utf-8 -*-
"""_mk_lotes_v406.py -- gera os LOTES DE REGRAS derivar_encanamento_v406_regras*.py a partir dos lotes derivar_encanamento_v405_regras*.py (cadeia_de_selo/v405), pelo MESMO mapa mecanico do motor derivar_v406_motor
(origem "v405": 404 -> 405 e 405 -> 406; nomes que nasceram no um.py v405 ficam). So' le v405\\ e so' escreve em v406\\ (backup de BYTES .bak_<ts> se o destino existir e diferir). Nao executa nada derivado.
Por que existe: a receita (secao 5, passo 1) manda subir os lotes por arquivo; o mapa faz a parte mecanica (nomes dos scripts-fonte e destino, rotulos); o CONTEUDO das regras (padroes que so' casavam no texto da v404) NAO e' reescrito aqui:
o motor aborta, com a contagem, onde o padrao nao casa no texto da v405 -- isso e' a lista do que a gerencia tem de reescrever (ver DERIVACAO_v406_NOTAS.md e DERIVACAO_ENCANAMENTO_v406_POR_ENTRADA.json).
uso: python -I -B -X utf8 _mk_lotes_v406.py"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v406_motor as M  # noqa: E402
CH = os.path.dirname(HERE); V5 = os.path.join(CH, "v405")
sha = lambda b: hashlib.sha256(b).hexdigest()
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# correcoes que o mapa nao faz sozinho (contagem EXATA, asserida): o PAR de nomes do comparador (origem v404 x v405 na v405; origem v405 x v406 na v406) -- o v403 do nome de origem nao esta no mapa
POS = {"derivar_encanamento_v405_regrasE3_comparar.py": [("comparar_v403_v405.py", "comparar_v404_v405.py", 2)],
       # lote F: a nota de estado que a regra poe no topo de cada script do pos-rito e o regex que tira a nota ANTIGA. Sem esta correcao a regra "passa" (count=1 de re.sub nao falha quando nao acha) e o derivado fica com DUAS notas
       # (a da v405 subida + a nova), a nova AFIRMANDO uma adaptacao que na v406 ainda nao existe. A data da nota antiga (28/10 na subida v404 -> v405) passa a ser a da nota da v405 (01/11); a nota nova diz que e' so' subida mecanica.
       "derivar_encanamento_v405_regrasF_pos_rito.py": [
           ("# [PREPARACAO v406, 01/11/2026 -- ESTADO] derivado da v405 FINAL (derivar_encanamento_v406.py, lote F) e adaptado por adaptar_pos_rito_v406.py e textos_v406_novo.pysnip ao conteudo da v406; exercitado pelo harness_textos_ensaio_v406.py e pelo harness_fechar_sandbox_v406.py.",
            "# [PREPARACAO v406, 02/11/2026 -- ESTADO] SUBIDA MECANICA da v405 FINAL (derivar_encanamento_v406.py, lote F); AINDA NAO adaptada ao conteudo da v406 nem exercitada por harness: a gerencia adapta e ensaia.", 1),
           ("Ver RELATORIO_PREPARACAO_v406.md.", "Ver DERIVACAO_v406_NOTAS.md.", 1),
           ("28/10/2026 -- ESTADO", "01/11/2026 -- ESTADO", 2)]}
lotes = sorted(f for f in os.listdir(V5) if f.startswith("derivar_encanamento_v405_regras") and f.endswith(".py"))
assert len(lotes) == 12, ("numero de lotes diferente do esperado na v405", len(lotes), lotes)
rel = []
for f in lotes:
    raw = open(os.path.join(V5, f), "rb").read(); t = raw.decode("utf-8")
    t2 = M.bump(t, (), "v405")
    for old, new, n in POS.get(f, []):
        assert t2.count(old) == n, ("correcao posterior: contagem diferente", f, old, t2.count(old), n)
        t2 = t2.replace(old, new)
    nome = f.replace("_v405_", "_v406_"); assert nome != f
    novo = t2.encode("utf-8"); p = os.path.join(HERE, nome)
    estado = "gravado"
    if os.path.exists(p):
        atual = open(p, "rb").read()
        if atual == novo:
            estado = "igual"
        else:
            open(p + ".bak_" + TS, "wb").write(atual); estado = "gravado_com_backup"
    if estado.startswith("gravado"):
        open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p)
    rel.append({"origem": f, "origem_sha256": sha(raw), "destino": nome, "destino_sha256": sha(novo), "estado": estado, "correcoes_posteriores": [(o, n_, c) for o, n_, c in POS.get(f, [])]})
    print("%-60s %-18s %s" % (nome, estado, sha(novo)[:12]))
out = os.path.join(HERE, "DERIVACAO_LOTES_v406.json")
txt = json.dumps({"contrato": "DERIVACAO_LOTES_v406", "executado": False, "mapa": "origem v405: 404->405, 405->406 (motor derivar_v406_motor.bump)", "lotes": rel}, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(out):
    open(out + ".bak_" + TS, "wb").write(open(out, "rb").read())
open(out + ".tmp", "wb").write(txt); os.replace(out + ".tmp", out)
