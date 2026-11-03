# -*- coding: utf-8 -*-
"""adaptar_pos_rito_v406.py -- ADAPTA ao conteudo da v406 (O FECHAMENTO: bundle de 301 modulos, UM registro com funcao fechamento_v406, as quatro chaves de testemunha lidas do kernel) os scripts do pos_rito que o motor
(derivar_encanamento_v406.py, lote F) so' tinha subido de rotulo a partir da v405 FINAL. Molde: adaptar_pos_rito_v405.py (que fez o mesmo da v404 para a v405). Cada edicao e' uma troca EXATA com contagem conferida (assert): se o texto de partida nao for o esperado, PARA e nada e' gravado
naquele arquivo. Backup de BYTES (.bak_<data>_adapt) antes de gravar; CRLF respeitado; temporario -> conferir tamanho -> substituir. Idempotente por arquivo: se o cabecalho de preparacao ja' nao existe, o arquivo e' pulado.
Os blocos novos de cada arquivo moram em _adapt_<arquivo>_v406.py (este modulo traz so' os auxiliares). Nada e' executado contra o real; so' texto.
Edicoes POSTERIORES aos adaptadores (feitas direto nos arquivos quando o ensaio apontou o defeito; os adaptadores espelham so' parte): leitura (estrutura de fe[anchors], regex da linha [v405], erratas dos specs recriados, ressalvas no topo do registro), textos_v406_novo.pysnip (clausula do 4,44 em _decisoes, cabecalho da linhagem para o regex da custodia G1, forma dos modulos TGLExt.F1Fecho394), harness_textos (veredito final, citacoes de 02/11, hex nas mutacoes), pedras_sha256 -> bundle_sha256 (a chave do ESPERADOS_v406).
uso: python -I -B -X utf8 adaptar_pos_rito_v406.py <leitura|superficies|registrar_mapa|chain|outros|harness_fechar|harness_textos|todos>   (superficies cobre tambem o fechar; outros cobre b3_recibo, gerar_derivacao, gerar_x_custodia e o conferir da bateria)"""
import ast, datetime, hashlib, importlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sha = lambda b: hashlib.sha256(b).hexdigest()
CAB_PREP = "[PREPARACAO v406"
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
NOTA_ADAPT = "# [ADAPTADO v406, 02/11/2026] sobre a subida mecanica da v405 FINAL (derivar_encanamento_v406.py, lote F) por adaptar_pos_rito_v406.py: o conteudo e' o da v406 (O FECHAMENTO: bundle de 301 modulos, UM registro com funcao fechamento_v406, quatro chaves de testemunha lidas do kernel); a gerencia revisa antes do rito (nao e' versao selada)."


def le(nome):
    raw = open(os.path.join(HERE, nome), "rb").read()
    return raw.decode("utf-8").replace("\r\n", "\n"), (b"\r\n" in raw), raw


def grava(nome, txt, crlf, raw_antigo):
    p = os.path.join(HERE, nome)
    if nome.endswith(".py"):
        ast.parse(txt)
    out = txt.replace("\n", "\r\n") if crlf else txt
    b = out.encode("utf-8")
    open(p + ".bak_" + STAMP + "_adapt", "wb").write(raw_antigo)
    tmp = p + ".tmp"
    open(tmp, "wb").write(b)
    assert os.path.getsize(tmp) > 0.5 * len(raw_antigo), ("o arquivo adaptado encolheu demais", nome, os.path.getsize(tmp), len(raw_antigo))
    os.replace(tmp, p)
    print("  gravado %s: %d B -> %d B (backup .bak_%s_adapt)" % (nome, len(raw_antigo), len(b), STAMP))


def sub(txt, velho, novo, n=1):
    c = txt.count(velho)
    assert c == n, ("troca nao casou", velho[:90], "esperado", n, "achou", c)
    return txt.replace(velho, novo)


def entre(txt, ini, fim, novo):
    """troca o trecho que comeca em `ini` (inclusive) e termina ANTES de `fim` (que fica); ambos unicos e na ordem."""
    assert txt.count(ini) == 1 and txt.count(fim) == 1, ("ancora nao unica", ini[:70], txt.count(ini), fim[:70], txt.count(fim))
    i = txt.index(ini)
    j = txt.index(fim)
    assert i < j, ("ancoras fora de ordem", ini[:60], fim[:60])
    return txt[:i] + novo + txt[j:]


def tira_cabecalho(txt):
    """retira as linhas do cabecalho de preparacao ([PREPARACAO v406 -- ESTADO], a de 'NAO e' versao selada' e a [A ADAPTAR v406]) e poe a linha de adaptacao logo depois do coding/shebang."""
    ls = txt.split("\n")
    out = []
    achou = False
    for l in ls:
        if l.startswith("# " + CAB_PREP) or l.startswith("# NAO e' versao selada: a gerencia revisa antes do rito.") or l.startswith("# [A ADAPTAR v406]"):
            achou = True
            continue
        out.append(l)
    assert achou, "cabecalho de preparacao nao achado"
    k = 0
    if out[0].startswith("#!"):
        k = 2 if (len(out) > 1 and out[1].startswith("# -*- coding")) else 1
    elif out[0].startswith("# -*- coding"):
        k = 1
    out.insert(k, NOTA_ADAPT)
    return "\n".join(out)


def pula(nome, txt):
    if CAB_PREP not in txt and "# [A ADAPTAR v406]" not in txt:
        print("  JA ADAPTADO (sem o cabecalho de preparacao):", nome)
        return True
    return False


def main(alvos):
    for a in alvos:
        m = importlib.import_module("_adapt_%s_v406" % a)
        print("== %s" % a)
        m.rodar(sys.modules[__name__])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    arg = sys.argv[1:] or ["todos"]
    todos = ["leitura", "superficies", "registrar_mapa", "chain", "outros", "harness_fechar", "harness_textos"]
    main(todos if arg == ["todos"] else arg)
