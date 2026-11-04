# -*- coding: utf-8 -*-
"""adaptar_pos_rito_v407.py -- auxiliares da ADAPTACAO ao conteudo da v407 (O PSION, O CANTO E O PAR: bundle PEQUENO de 9 modulos em TGLExt/, o registro com funcao psion_canto_v407 e os registros por spec cunhagens_v407 e kh_n1_cobertura_v407;
a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma passa de literal False a leitura True) dos scripts do pos_rito que a subida mecanica de rotulo (_bump_copia_v407.py) so' tinha rotulado a partir da v406.
Molde: adaptar_pos_rito_v406.py (que fez o mesmo da v405 para a v406). Cada edicao e' uma troca EXATA com contagem conferida (assert): se o texto de partida nao for o esperado, PARA e nada e' gravado naquele arquivo.
Backup de BYTES (.bak_<data>_adapt) antes de gravar; CRLF respeitado; temporario -> conferir tamanho -> substituir. Idempotente por arquivo: se a marca de preparacao ja' nao existe, o arquivo e' pulado.
Os blocos novos de cada arquivo moram em _adapt_<arquivo>_v407.py (este modulo traz so' os auxiliares). Nada e' executado contra o real; so' texto."""
import ast, datetime, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sha = lambda b: hashlib.sha256(b).hexdigest()
MARCA = "# [A ADAPTAR v407]"
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
NOTA_ADAPT = "# [ADAPTADO v407, 03/11/2026] sobre a subida mecanica de rotulo da v406 FINAL (_bump_copia_v407.py) por adaptar_pos_rito_v407.py: o conteudo e' o da v407 (O PSION, O CANTO E O PAR: bundle de 9 modulos, o registro com funcao psion_canto_v407, o fechamento_v406 HERDADO e recriado, a chave do lema lida do kernel); a gerencia revisa antes do rito (nao e' versao selada)."


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


def entre_linhas(txt, ini, fim, novo):
    """troca as LINHAS inteiras desde a que contem `ini` (unica) ate' a que antecede a que contem `fim` (unica); `novo` deve terminar em quebra de linha."""
    assert txt.count(ini) == 1 and txt.count(fim) == 1, ("ancora nao unica", ini[:60], txt.count(ini), fim[:60], txt.count(fim))
    i = txt.rfind("\n", 0, txt.index(ini)) + 1
    j = txt.rfind("\n", 0, txt.index(fim)) + 1
    assert i < j, ("ancoras fora de ordem", ini[:60], fim[:60])
    assert novo.endswith("\n")
    return txt[:i] + novo + txt[j:]


def tira_cabecalho(txt):
    """retira a marca `# [A ADAPTAR v407]` e a linha velha `# [ADAPTADO v407, 02/11/2026]` (resto da subida mecanica sobre a nota da v406) e poe a linha de adaptacao logo depois do coding/shebang."""
    ls = txt.split("\n")
    out = []
    achou = False
    for l in ls:
        if l.startswith(MARCA) or l.startswith("# [ADAPTADO v407, 02/11/2026]"):
            achou = achou or l.startswith(MARCA)
            continue
        out.append(l)
    assert achou, "marca de adaptacao nao achada"
    k = 0
    if out[0].startswith("#!"):
        k = 2 if (len(out) > 1 and out[1].startswith("# -*- coding")) else 1
    elif out[0].startswith("# -*- coding"):
        k = 1
    out.insert(k, NOTA_ADAPT)
    return "\n".join(out)


def pula(nome, txt):
    if MARCA not in txt:
        print("  JA ADAPTADO (sem a marca):", nome)
        return True
    return False
