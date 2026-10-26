# -*- coding: utf-8 -*-
r"""Liga o central_extra ao montar e a cadeia (24/10/2026, sessao a7; ordem da gerencia: «a forma menos invasiva»).
Dois arquivos, trocas CONTADAS (cada trecho antigo tem de aparecer exatamente uma vez, senao nada e gravado), backup de BYTES
(<arquivo>.bak_<carimbo> na mesma pasta), temporario -> confere -> substitui:
  montar_central_no_site.py          4a fonte (central_extra), o assert das chaves e o filtro do que nao sobe ao site
  atualizar_central_publica.py       passo `central_extra` (grupo site) ANTES de `montar`
Uso: patch_central_extra_na_cadeia.py [--seco]"""
import os, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
CARIMBO = time.strftime("%Y%m%d_%H%M%S")
SECO = "--seco" in sys.argv

MONTAR = [
    # docstring
    ("o um.acom público e os seus dados (acom/). Cópia de bytes conferida por sha256.",
     "o um.acom público e os seus dados (acom/) e os contratos do organismo (central_extra/). Cópia de bytes conferida por sha256."),
    # a 4a fonte
    ('FONTES = [Path(r"C:\\IALD\\Central de Patentes\\frontend\\dist_publica"),',
     '# (24/10/2026) 4a fonte: central_extra — os contratos que a gerência deve ao Kimi (organismo/: a página dele + o quadro saneado + as custódias;\n'
     '# pensamentos/), gerados por gerar_central_extra.py no passo `central_extra`, que roda ANTES deste. O arcos.json e o MANIFESTO_CENTRAL_EXTRA.json\n'
     '# FICAM FORA do site até a gerência decidir onde publicá-los (mesma lista do gerador); *.bak_* e *.tmp também não sobem.\n'
     'EXTRA = Path(r"C:\\IALD\\Site\\tgl\\v3.0_bancada\\central_extra")\n'
     'EXTRA_NAO_PUBLICA = {"arcos.json", "MANIFESTO_CENTRAL_EXTRA.json"}\n'
     'FONTES = [Path(r"C:\\IALD\\Central de Patentes\\frontend\\dist_publica"),'),
    ('          Path(r"C:\\IALD\\Site\\tgl\\v3.0_bancada\\central_publica\\acom")]',
     '          Path(r"C:\\IALD\\Site\\tgl\\v3.0_bancada\\central_publica\\acom"),\n'
     '          EXTRA]'),
    # as chaves
    ('assert (FONTES[0] / "index.html").is_file() and (FONTES[1] / "api" / "_mapa.json").is_file() and (FONTES[2] / "um.acom").is_file()\n',
     'assert (FONTES[0] / "index.html").is_file() and (FONTES[1] / "api" / "_mapa.json").is_file() and (FONTES[2] / "um.acom").is_file()\n'
     'assert all((EXTRA / x).is_file() for x in ("organismo/index.html", "organismo/ESTADO_DO_ORGANISMO.json", "organismo/custodias.json",\n'
     '                                           "pensamentos/pensamentos.json")), "central_extra incompleto — rodar o passo central_extra (gerar_central_extra.py) antes do montar — PARAR"\n'),
    # o filtro
    ('        rel = p.relative_to(base)\n',
     '        rel = p.relative_to(base)\n'
     '        if base == EXTRA and (rel.as_posix() in EXTRA_NAO_PUBLICA or ".bak_" in p.name or p.name.endswith(".tmp")):\n'
     '            continue\n'),
]
ATUALIZAR = [
    ("-> vínculo -> montagem ->", "-> vínculo -> central_extra -> montagem ->"),
    ('add("montar", "site", [str(W / "montar_central_no_site.py")])\n',
     'add("central_extra", "site", [str(W / "gerar_central_extra.py")])   # (24/10/2026) os contratos do organismo, pensamentos e custódias, ANTES do montar que os copia\n'
     'add("montar", "site", [str(W / "montar_central_no_site.py")])\n'),
]


def aplicar(nome, trocas):
    p = W / nome
    raw = p.read_bytes()
    s = raw.decode("utf-8")
    for i, (velho, novo) in enumerate(trocas, 1):
        n = s.count(velho)
        if n != 1:
            raise SystemExit("PARADO: %s, troca %d: o trecho antigo aparece %d vez(es) (esperado 1) — nada foi gravado" % (nome, i, n))
        s = s.replace(velho, novo, 1)
    novo_bytes = s.encode("utf-8")
    if SECO:
        print("%s: %d trocas conferidas (seco); %d -> %d bytes" % (nome, len(trocas), len(raw), len(novo_bytes)))
        return
    bak = p.with_name(p.name + ".bak_" + CARIMBO)
    bak.write_bytes(raw)
    assert bak.read_bytes() == raw, "backup de %s nao confere" % nome
    t = p.with_name(p.name + ".tmp_central_extra")
    t.write_bytes(novo_bytes)
    assert t.stat().st_size == len(novo_bytes) > len(raw), "temporario de %s nao confere" % nome
    compile(t.read_text(encoding="utf-8"), nome, "exec")        # sintaxe valida antes de substituir
    os.replace(t, p)
    assert p.read_bytes() == novo_bytes
    print("%s: %d trocas; %d -> %d bytes; backup %s" % (nome, len(trocas), len(raw), len(novo_bytes), bak.name))


aplicar("montar_central_no_site.py", MONTAR)
aplicar("atualizar_central_publica.py", ATUALIZAR)
