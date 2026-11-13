# -*- coding: utf-8 -*-
"""_fork_b_lib_v411.py -- (claude-construtor-v411, retomada, fork B, 12/11/2026) a ferramenta UNICA com que o fork B aplica as adaptacoes de verdade da v411 aos scripts do seu escopo (bateria_pre_selo, bancada_B3_servico,
fim_de_cadeia, gerar_relatorio, guardas_estaticas_bancada, depositar_construtor, varredura_fock_omega, cadeia_parte2, _marca_adaptado, fechar_preparacao, acom_inscrever_prep). Para cada arquivo: backup de BYTES
<arquivo>.bak_<ts>_forkb na mesma pasta; cada ancora tem de ocorrer EXATAMENTE uma vez; o fim de linha do arquivo e' respeitado; a linha da marca de copia mecanica e' trocada pela de ADAPTADO; ast.parse (.py) ou
sh -n (.sh) no texto novo; escrita por .tmp, conferida pelo tamanho, e so' entao substitui. Nao executa os scripts. A marca e' montada por concatenacao (este arquivo nao a traz literal)."""
import ast, datetime, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
MARCA = "# [A ADAPTAR v" + "411]"
ROT = "# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] "
# a subida mecanica escreveu nas notas herdadas que o fork B do construtor da v411 reconferiu o arquivo em 06/11 (falso: o rotulo subiu); o registro certo, ao lado:
HIST = [("e em 06/11/2026 pelo fork B do claude-construtor-v411, com os rotulos subidos)", "e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos; na v411, adaptado em 12/11/2026 pelo fork B do claude-construtor-v411, retomada)"),
        ("reconferida pelo fork B do claude-construtor-v410 e em 06/11/2026 pelo fork B do claude-construtor-v411, com os rotulos subidos)", "reconferida pelo fork B do claude-construtor-v410 em 06/11/2026, com os rotulos subidos; na v411, adaptado em 12/11/2026 pelo fork B do claude-construtor-v411, retomada)")]


def linha(rel, prefixo):
    """a linha EXATA (forma LF) do arquivo que comeca com prefixo (uma so'), para servir de ancora."""
    p = os.path.join(HERE, *rel.replace("\\", "/").split("/"))
    ls = [l for l in open(p, "rb").read().decode("utf-8").replace("\r\n", "\n").split("\n") if l.startswith(prefixo)]
    assert len(ls) == 1, (rel, prefixo, len(ls))
    return ls[0]


def substituir_inteiro(rel, fonte_nova):
    """REESCRITA (varrida, nao remendada): o arquivo rel passa a ser o texto de fonte_nova (um rascunho ja' escrito); backup de BYTES antes; a marca nao pode ficar; ast.parse / sh -n; por .tmp."""
    p = os.path.join(HERE, *rel.replace("\\", "/").split("/"))
    b = open(p, "rb").read(); t = open(fonte_nova, "rb").read().decode("utf-8")
    assert MARCA not in t and "\r" not in t
    if rel.endswith(".py"):
        ast.parse(t)
    novo = t.encode("utf-8")
    if rel.endswith(".sh"):
        tmp_sh = p + ".tmp"
        open(tmp_sh, "wb").write(novo)
        r = subprocess.run(["sh", "-n", tmp_sh], capture_output=True, text=True)
        os.remove(tmp_sh)
        assert r.returncode == 0, ("sh -n reprovou", rel, r.stderr[:400])
    bak = p + ".bak_" + TS + "_forkb"
    open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p)
    print("ok (reescrito) %-52s %7d -> %7d B | backup %s" % (rel, len(b), len(novo), os.path.basename(bak)))


def aplicar(rel, pares, motivo, extra_check=None, so_comentario_hist=True):
    """rel: caminho relativo a v411; pares: [(antigo, novo)] (cada antigo EXATAMENTE uma vez, em forma LF); motivo: o texto da linha ADAPTADO."""
    p = os.path.join(HERE, *rel.replace("\\", "/").split("/"))
    b = open(p, "rb").read(); t = b.decode("utf-8")
    crlf = "\r\n" in t
    if crlf:
        assert "\n" not in t.replace("\r\n", ""), ("fim de linha misto", rel)
        t = t.replace("\r\n", "\n")
    ln = t.split("\n")
    im = [i for i, l in enumerate(ln) if l.startswith(MARCA)]
    assert len(im) == 1, ("a marca de copia mecanica nao esta' uma vez", rel, len(im))
    ln[im[0]] = ROT + motivo
    t = "\n".join(ln)
    for a_, n_ in pares:
        c_ = t.count(a_)
        assert c_ == 1, ("ancora nao unica", rel, a_[:120], c_)
        t = t.replace(a_, n_)
    for a_, n_ in HIST:
        t = t.replace(a_, n_)
    assert MARCA not in t
    if extra_check:
        extra_check(t)
    if rel.endswith(".py"):
        ast.parse(t)
    novo = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
    if rel.endswith(".sh"):
        tmp_sh = p + ".tmp"
        open(tmp_sh, "wb").write(novo)
        r = subprocess.run(["sh", "-n", tmp_sh], capture_output=True, text=True)
        os.remove(tmp_sh)
        assert r.returncode == 0, ("sh -n reprovou", rel, r.stderr[:400])
    bak = p + ".bak_" + TS + "_forkb"
    open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p)
    print("ok %-62s %7d -> %7d B | backup %s" % (rel, len(b), len(novo), os.path.basename(bak)))
    return t
