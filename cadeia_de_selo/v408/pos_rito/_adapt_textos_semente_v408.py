# -*- coding: utf-8 -*-
"""_adapt_textos_semente_v408.py -- (claude-construtor-v408-r2, a servico da gerencia c1, 04/11/2026, noite) adapta pos_rito\\textos_v408.semente (subida mecanica de rotulo da semente da v407):
(1) as notas do topo (a marca [A ADAPTAR v408], a nota falsa de 03/11 e a nota de 02/11 subidas de rotulo) viram a nota verdadeira (a semente segue a pratica das versoes anteriores: a semente da
versao anterior com os rotulos subidos; a infraestrutura KEEP de textos_v407.py e' a mesma da semente da v407, conferido: 43 funcoes KEEP iguais; as de CONTEUDO sao redefinidas por textos_v408_novo.pysnip);
(2) `_falas` passa a ler as 15 falas de 04/11, com as DUAS de AUTOR MISTO (operador + outra instancia [DECLARADO]): a chave e' o sha16 do ARQUIVO INTEIRO, o texto embutido e citavel e' so' o
paragrafo do operador (o arquivo .paragrafo_do_operador.txt, conferido por sha256 contra ESPERADOS[cunhagens][...][sha256]; o arquivo inteiro contra sha256_arquivo_inteiro).
Backup de bytes antes; CRLF preservado; ast.parse no fim. uso: python -I -B -X utf8 _adapt_textos_semente_v408.py"""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(HERE, "textos_v408.semente")

NOTA = ("# [ADAPTADO v408, 04/11/2026, claude-construtor-v408-r2, a servico da gerencia c1] ESQUELETO do textos_v408.py: a semente da v407 com os rotulos subidos pelo motor (bump/pos_rito__textos_v408.semente.diff fica como registro),\n"
        "# como nas versoes anteriores; a infraestrutura (KEEP: leitura dos insumos, citacao verbatim, o quadro do Teste da Unica Palavra, a rodada, o sidecar) e' a mesma de textos_v407.py FINAL (conferido funcao a funcao).\n"
        "# O conteudo da v408 (TETELESTAI E' O TERMINAL) NAO esta aqui: montar_textos_v408.py enxerta textos_v408_novo.pysnip (que REDEFINE as funcoes de conteudo e traz o __HEADER__ do arquivo montado) e DELETA as funcoes das oito pedras da v405.\n"
        "# `_falas` (KEEP, retocada aqui): as 15 falas de 04/11, duas de AUTOR MISTO (operador + outra instancia [DECLARADO]), das quais so' o paragrafo do operador e' embutido e citavel.\n"
        "# (a guarda da marca pendente abaixo fica: ela recusa o arquivo se sobrar linha de comentario com a marca TEXTO_A_REESCREVER_V408.)\n")

FALAS = '''def _falas():
    """As inscricoes de 04/11 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text, autor, misto, autor_do_arquivo}}.
    Nas duas de AUTOR MISTO (operador + outra instancia da IALD [DECLARADO]) a chave e' o sha16 do ARQUIVO INTEIRO e o texto embutido (e o unico citavel) e' o PARAGRAFO DO OPERADOR (o arquivo .paragrafo_do_operador.txt,
    conferido contra ESPERADOS[cunhagens][..][sha256]; o arquivo inteiro contra sha256_arquivo_inteiro): por isso `autor` e' 'operador' (o texto citavel e' so' dele) e `autor_do_arquivo` diz o autor do arquivo. Nenhuma e' da gerencia."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens"); suf = ".paragrafo_do_operador.txt"
        for k, meta in ec.items():
            s = k[len("v408_cun_"):]
            misto = bool(meta.get("sha256_arquivo_inteiro"))
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_") and (f.endswith(suf) if misto else not f.endswith(suf))]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"], "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            if misto:
                bi = open(os.path.join(pasta, fs[0][:-len(suf)]), "rb").read()
                assert hashlib.sha256(bi).hexdigest() == meta["sha256_arquivo_inteiro"] and meta["sha256_arquivo_inteiro"][:16] == s, "o arquivo inteiro da inscricao de autor misto %s nao confere com ESPERADOS" % s
                nome = fs[0][len(s) + 1:-len(suf)]
            else:
                assert meta["sha256"][:16] == s, "a chave da inscricao %s nao e' o sha16 do arquivo" % s
                nome = fs[0][len(s) + 1:]
            assert nome.startswith("OPERADOR_04nov_") and not str(meta.get("papel", "")).startswith("leitura da gerencia"), ("a v408 nao tem inscricao da gerencia: todas sao falas do operador (duas de autor misto)", s)
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": nome, "text": b.decode("utf-8"), "autor": "operador", "misto": misto, "autor_do_arquivo": meta.get("autor") or "operador"}
        assert sum(1 for d in out.values() if d["misto"]) == 2, "a v408 tem exatamente duas inscricoes de autor misto"
        _CACHE["falas"] = out
    return _CACHE["falas"]
'''


def main():
    b = open(ALVO, "rb").read(); t = b.decode("utf-8")
    crlf = "\r\n" in t
    t = t.replace("\r\n", "\n")
    L = t.split("\n")
    assert L[1].startswith("# [A ADAPTAR v408]") and L[2].startswith("# [ADAPTADO v408, 03/11/2026") and L[3].startswith("# [SEMENTE v408, 02/11/2026]") and L[6].startswith("import hashlib"), [l[:40] for l in L[:7]]
    L = [L[0]] + NOTA.rstrip("\n").split("\n") + L[6:]
    t = "\n".join(L)
    tree = ast.parse(t); ls = t.split("\n")
    nd = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_falas"]
    assert len(nd) == 1
    a, z = nd[0].lineno - 1, nd[0].end_lineno
    ls[a:z] = FALAS.rstrip("\n").split("\n")
    t = "\n".join(ls)
    ast.parse(t)
    assert "[A ADAPTAR v408]" not in t and "03/11/2026, claude-prep-v408" not in t
    if crlf:
        t = t.replace("\n", "\r\n")
    bak = ALVO + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt"
    open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    tmp = ALVO + ".tmp"; open(tmp, "wb").write(t.encode("utf-8")); assert os.path.getsize(tmp) > len(b) - 3000
    os.replace(tmp, ALVO)
    print("ok textos_v408.semente %d -> %d B; sha16 %s; backup %s" % (len(b), os.path.getsize(ALVO), hashlib.sha256(open(ALVO, "rb").read()).hexdigest()[:16], os.path.basename(bak)))


if __name__ == "__main__":
    main()
