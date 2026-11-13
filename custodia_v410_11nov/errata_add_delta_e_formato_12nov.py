# -*- coding: utf-8 -*-
"""Duas erratas ao lado na esteira pública, antes da cadeia da v411 (12/11/2026, claude-site-custodia; de acordo da gerência c1, 12/11):
1. atualizar_repo_publico.py: o add só do que difere do HEAD. O add do índice inteiro (560.887 caminhos) ficou 3.917 s sem escrever o
   index.lock na publicação do pré-registro do H0DN (medido pela c1) e é o passo das 14.322 s do C18 da v410; o add do delta levou 1 s.
2. mesclar_incremento.py: o arquivo já publicado cujo sha256 de agora (na origem e no preparo) é igual ao do índice não sai quando o único
   motivo da exclusão é o formato («binário de cache ou outro formato»). Sem isso, a v411 tiraria do topo do work o vetor e o estimador S0
   do pré-registro (mtime depois do DESDE). Qualquer outra exclusão (guarda, credencial, dado pessoal) continua tirando.
Os dois arquivos são CRLF: edição por bytes, backup de bytes antes, gravação por temporário, compilação conferida."""
import os, time

W = r"C:\IALD\Central de Patentes\work\central_publica_22out"
STAMP = time.strftime("%Y%m%d_%H%M%S")
EDICOES = {
    "atualizar_repo_publico.py": [(
        b'lista.write_bytes(b"\\0".join(x.encode("utf-8") for x in sorted(quer)))\r\n'
        b'g("add", "-f", "--pathspec-from-file=" + str(lista), "--pathspec-file-nul")\r\n',
        b'# AO LADO (12/11/2026, claude-site-custodia; de acordo da gerencia c1): o add vai so com o que difere do HEAD, nao com o indice inteiro.\r\n'
        b'# O add de sorted(quer) (560.887 caminhos no work) ficou 3.917 s sem escrever o index.lock na publicacao do pre-registro do H0DN e e o\r\n'
        b'# passo das 14.322 s do C18 da v410; o do delta levou 1 s. O stage e o mesmo: entram os caminhos do indice que o git nao rastreia\r\n'
        b'# (o -f fica: o .gitignore copiado da origem nao barra o curado) e os rastreados que o status mostra mudados. Antes:\r\n'
        b'#   lista.write_bytes(b"\\0".join(x.encode("utf-8") for x in sorted(quer))); g("add", "-f", "--pathspec-from-file=" + str(lista), ...)\r\n'
        b'_tok = g("status", "--porcelain", "-z", "--untracked-files=all").stdout.split("\\0")\r\n'
        b'_mud, _i = set(), 0\r\n'
        b'while _i < len(_tok):\r\n'
        b'    _e = _tok[_i]; _i += 1\r\n'
        b'    if len(_e) > 3:\r\n'
        b'        _mud.add(_e[3:])\r\n'
        b'        if _e[0] in "RC":\r\n'
        b'            _i += 1   # com -z, o nome de origem de um rename vem no token seguinte, sem o prefixo XY\r\n'
        b'_dif = sorted((quer - tem) | (_mud & quer))\r\n'
        b'lista.write_bytes(b"\\0".join(x.encode("utf-8") for x in _dif))\r\n'
        b'if _dif:\r\n'
        b'    g("add", "-f", "--pathspec-from-file=" + str(lista), "--pathspec-file-nul")\r\n')],
    "mesclar_incremento.py": [(
        b'# 2) o que a rodada excluiu: se estava publicado, sai\r\n',
        b'# AO LADO (12/11/2026, claude-site-custodia; de acordo da gerencia c1): o ja publicado que a rodada exclui SO pelo formato nao sai se os\r\n'
        b'# bytes de agora (na origem e no preparo) tem o sha256 do indice. Sem isso, a v411 tiraria do topo do work o vetor e o estimador S0 do\r\n'
        b'# pre-registro do H0DN (os .npz publicados fora da cadeia em 12/11, commit 769fcb26). Guarda, credencial e dado pessoal seguem tirando.\r\n'
        b'SO_FORMATO = "bin\xc3\xa1rio de cache ou outro formato"\r\n'
        b'\r\n'
        b'\r\n'
        b'def mesmos_bytes(rel):\r\n'
        b'    s = por[rel]["sha256"]\r\n'
        b'    for base in (SRC, D):\r\n'
        b'        p = longo(base, rel)\r\n'
        b'        if not os.path.isfile(p):\r\n'
        b'            return False\r\n'
        b'        with open(p, "rb") as fh:\r\n'
        b'            if hashlib.sha256(fh.read()).hexdigest() != s:\r\n'
        b'                return False\r\n'
        b'    return True\r\n'
        b'\r\n'
        b'\r\n'
        b'# 2) o que a rodada excluiu: se estava publicado, sai\r\n'), (
        b'        if rel in por:\r\n'
        b'            tirar(rel, motivo); cont["saiu (a esteira agora exclui)"] += 1\r\n',
        b'        if rel in por:\r\n'
        b'            if motivo.startswith(SO_FORMATO) and mesmos_bytes(rel):\r\n'
        b'                cont["mantido (j\xc3\xa1 publicado com os mesmos bytes; s\xc3\xb3 o formato)"] += 1; continue\r\n'
        b'            tirar(rel, motivo); cont["saiu (a esteira agora exclui)"] += 1\r\n')],
}
# AO LADO (12/11/2026, a mesma sessão): os dois arquivos são LF (medido em Python: CRLF 0; a contagem do grep -c $'\r$' do Git Bash
# enganou). Os trechos acima, escritos em CRLF, são normalizados para LF; o script parou no primeiro assert, antes de gravar qualquer byte.
EDICOES = {n: [(a.replace(b"\r\n", b"\n"), d.replace(b"\r\n", b"\n")) for a, d in eds] for n, eds in EDICOES.items()}
for nome, eds in EDICOES.items():
    P = os.path.join(W, nome)
    b = open(P, "rb").read()
    for antes, _d in eds:
        assert b.count(antes) == 1, "o trecho mudou em %s — PARAR: %r" % (nome, antes[:80])
    bak = P + ".bak_%s_add_delta_e_formato" % STAMP
    open(bak, "wb").write(b)
    assert open(bak, "rb").read() == b
    novo = b
    for antes, depois in eds:
        novo = novo.replace(antes, depois)
    compile(novo.decode("utf-8"), P, "exec")
    assert novo.count(b"\r\n") == 0, "fim de linha misturado em %s" % nome
    t = P + ".tmp_errata"
    open(t, "wb").write(novo)
    assert os.path.getsize(t) == len(novo) > len(b)
    os.replace(t, P)
    print("ok:", nome, len(b), "->", len(novo), "| backup", os.path.basename(bak))
