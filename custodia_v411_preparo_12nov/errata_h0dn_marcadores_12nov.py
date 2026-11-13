# -*- coding: utf-8 -*-
"""O H0DN × BG1 ABERTO na G1 (12/11/2026, claude-site-custodia; de acordo da gerência c1, 12/11/2026): edição por bytes de três arquivos.
  - textos.py (CRLF): a NOTA do ledger vem do marcador NOTA_EN_vNNN; o molde de ENTROU/ARCO não serve; F67 e números em todo texto da perna 1;
  - primordial.py (LF): lê o registro h0dn_bg1_vNNN aberto e os marcadores README_* do handoff, conferidos (forma, F67, números, cabeça);
  - readme_pinado.py (LF): o painel do H0DN no topo, a Fase 9 V2 em uma linha EN e uma PT, o painel inteiro dela em REGISTRO_FASE9_V2.md
    (gerado e pinado), as trocas do b_status, do b_ritos e do parágrafo da parte P = nP.
Sem registro aberto no core, todo texto sai byte a byte como antes (as funções originais ficam intactas). Backup de bytes antes de tocar;
gravação por temporário; compilação conferida; o arquivo tem de crescer."""
import os, time

G1 = r"C:\IALD\Central de Patentes\tools\custodia_g1"
STAMP = time.strftime("%Y%m%d_%H%M%S")
AO_LADO = "AO LADO (12/11/2026, claude-site-custodia; de acordo da gerencia c1)"

TEXTOS = [
    ("from .util import Parar\n",
     "from .util import Parar\nfrom . import h0dn   # " + AO_LADO + ": o teste H0DN x BG1 aberto\n"),
    ("    for ident in MARCADORES_OPCIONAIS:\n",
     "    # " + AO_LADO + ": com um h0dn_bg1_vNNN aberto no core selado, a NOTA (E04) e os blocos do\n"
     "    # README (E08) so vem do handoff (o molde diria que beta_TGL na natureza a 5 sigma e o passo aberto); sem o marcador, bloqueia mesmo com --aceitar-molde.\n"
     "    ab, extras = None, ()\n"
     "    if pend_ids is None or {\"E04\", \"E08\"} & set(pend_ids):\n"
     "        try:\n"
     "            ab = h0dn.registro_aberto(_core_da_versao(ctx))\n"
     "        except Exception as e:  # noqa: BLE001\n"
     "            out[\"bloqueios\"].append(\"o core selado nao se leu para saber se o H0DN foi aberto: %s\" % e)\n"
     "    if ab:\n"
     "        out[\"h0dn_aberto\"] = ab[0]\n"
     "        extras = h0dn.TODOS\n"
     "        if pend_ids is None or \"E04\" in pend_ids:\n"
     "            precisa.add(h0dn.MARCADOR_NOTA)\n"
     "        if pend_ids is None or \"E08\" in pend_ids:\n"
     "            precisa |= set(h0dn.MARCADORES_README)\n"
     "    for ident in MARCADORES_OPCIONAIS + extras:\n"),
    ("    out[\"bloqueia\"] = bool((out[\"faltam\"] and not ctx.aceitar_molde) or (out[\"bloqueios\"] and precisa))\n",
     "    faltam_h0dn = [k for k in out[\"faltam\"] if k.rsplit(\"_\", 1)[0] in h0dn.TODOS]\n"
     "    out[\"bloqueia\"] = bool((out[\"faltam\"] and not ctx.aceitar_molde) or faltam_h0dn or (out[\"bloqueios\"] and precisa))\n"),
    ("    core = _core_da_versao(ctx)\n",
     "    core = _core_da_versao(ctx)\n"
     "    ab = h0dn.registro_aberto(core)          # " + AO_LADO + ": o H0DN aberto (None: nada muda)\n"
     "    Vh = None\n"
     "    if ab:\n"
     "        try:\n"
     "            Vh = h0dn.valores(ab[1])\n"
     "        except ValueError as e:\n"
     "            raise Parar(str(e))\n"),
    ("    T.nota_en = Item(nota, \"molde-factual\")\n",
     "    T.nota_en = Item(nota, \"molde-factual\")\n"
     "    if ab:   # " + AO_LADO + ": a NOTA vem do handoff (o molde diria «waits for 5 sigma»); sem marcador, PARA\n"
     "        mk_nota = _marcador(ctx, h0dn.MARCADOR_NOTA)\n"
     "        if not mk_nota:\n"
     "            raise Parar(\"o H0DN foi aberto (%s no core selado): a NOTA do molde diria que beta_TGL espera 5 sigma; o handoff precisa trazer \"\n"
     "                        \"<!-- INICIO_%s_%s --> (nem --aceitar-molde)\" % (ab[0], h0dn.MARCADOR_NOTA, v))\n"
     "        T.nota_en = Item(mk_nota, \"handoff:%s_%s\" % (h0dn.MARCADOR_NOTA, v))\n"),
    ("    # --- LEDGER ---\n",
     "    if ab:   # " + AO_LADO + ": o molde do «what entered» e do arco diz que o painel do Teste da Unica Palavra «stays at the top»\n"
     "        velhos = [k for k in T.molde_usado if k.rsplit(\"_\", 1)[0] in (\"ENTROU_EN\", \"ARCO_EN\", \"ARCO_PT\")]\n"
     "        if velhos:\n"
     "            raise Parar(\"o H0DN foi aberto (%s): o molde factual ficou velho; o handoff precisa trazer %s (nem --aceitar-molde)\" % (ab[0], \", \".join(velhos)))\n"
     "    # --- LEDGER ---\n"),
    ("        T.violacoes += portao(bloco, T.conhecidos, rotulo=\"handoff:\" + ident)\n",
     "        T.violacoes += portao(bloco, T.conhecidos, rotulo=\"handoff:\" + ident)\n"
     "    if ab:   # " + AO_LADO + ": F67, numeros, cabeca e sigma contra o registro do H0DN em todo texto desta perna\n"
     "        for rot, txt in ([(\"TXT\", T.txt_en.texto), (\"ERR\", T.err_en.texto), (\"NOTA\", T.nota_en.texto), (\"ARCO_EN\", T.arco_en.texto),\n"
     "                          (\"ARCO_PT\", T.arco_pt.texto), (\"COMMIT\", T.commit_espelho.texto)] + [(\"handoff:\" + i, b) for i, b in T.paragrafos]):\n"
     "            T.violacoes += h0dn.conferir_bloco(txt, Vh, rot)\n"),
]

PRIMORDIAL = [
    ("    from custodia_g1.caminhos import Caminhos  # type: ignore\nelse:\n    from .caminhos import Caminhos\n",
     "    from custodia_g1.caminhos import Caminhos  # type: ignore\n    from custodia_g1 import h0dn as H0DN  # type: ignore\n"
     "else:\n    from .caminhos import Caminhos\n    from . import h0dn as H0DN\n"),
    ("        c.derivar(\"mudou.paragrafo_pronto_titulo\", None, \"handoff\", \"nenhum marcador PARAGRAFO_*_\" + versao, \"regex\")\n",
     "        c.derivar(\"mudou.paragrafo_pronto_titulo\", None, \"handoff\", \"nenhum marcador PARAGRAFO_*_\" + versao, \"regex\")\n"
     "    # --- " + AO_LADO + ": o teste H0DN x BG1 ABERTO. Com um h0dn_bg1_vNNN de\n"
     "    # opened_once = true no core selado, os blocos do README que diziam que beta_TGL na natureza a 5 sigma e o passo aberto saem do handoff\n"
     "    # (marcadores README_*), conferidos contra o registro (forma, F67, numeros, cabeca); sem o marcador, PARA. Sem registro aberto, nada muda.\n"
     "    ab = H0DN.registro_aberto(c.dados[\"core\"])\n"
     "    c.derivar(\"h0dn.aberto\", bool(ab), \"core\", \"um h0dn_bg1_vNNN com opened_once = true\", \"busca\")\n"
     "    if ab:\n"
     "        nome_h, reg_h = ab\n"
     "        try:\n"
     "            Vh = H0DN.valores(reg_h)\n"
     "        except ValueError as e:\n"
     "            raise Falha(str(e))\n"
     "        c.derivar(\"h0dn.registro\", nome_h, \"core\", \"o h0dn_bg1_vNNN aberto mais novo\", \"busca\")\n"
     "        for k in (\"z_null\", \"z_tgl\", \"D\", \"p_unilateral\", \"ramo\", \"outcome\", \"t\", \"modelo\"):\n"
     "            c.pegar(\"h0dn.primario.\" + k, \"core\", nome_h + \"/values/primario/\" + k)\n"
     "        for k in (\"z_null\", \"z_tgl\", \"D\", \"ramo\", \"outcome\", \"t\", \"modelo\"):\n"
     "            c.pegar(\"h0dn.cefeidas_livres.\" + k, \"core\", nome_h + \"/values/cefeidas_livres/\" + k)\n"
     "        c.pegar(\"h0dn.cabeca\", \"core\", nome_h + \"/cabeca_do_teste\")\n"
     "        c.pegar(\"h0dn.outcome\", \"core\", nome_h + \"/outcome\")\n"
     "        faltam_h = [\"INICIO_%s_%s\" % (mk, versao) for mk in H0DN.MARCADORES_README if \"%s_%s\" % (mk, versao) not in marc]\n"
     "        if faltam_h:\n"
     "            raise Falha(\"o H0DN foi aberto (%s): o handoff nao traz %s (os blocos do README nao se inventam; o molde do 5 sigma ficou velho)\" % (nome_h, \", \".join(faltam_h)))\n"
     "        ids_h = {\"README_PAINEL_H0DN\": \"painel\", \"README_FASE9_V2\": \"fase9_v2\", \"README_PRIMORDIAL_5SIGMA\": \"primordial_5sigma\",\n"
     "                 \"README_STATUS_5SIGMA\": \"status_5sigma\", \"README_H0DN\": \"paragrafo\", \"README_RITOS\": \"ritos\"}\n"
     "        for mk in H0DN.MARCADORES_README:\n"
     "            txt = marc[\"%s_%s\" % (mk, versao)].strip(\"\\n\")\n"
     "            forma = []\n"
     "            if \"{{\" in txt or \"PORTAS:\" in txt:\n"
     "                forma.append(\"traz «{{» ou o marcador das portas\")\n"
     "            if mk in (\"README_PRIMORDIAL_5SIGMA\", \"README_H0DN\") and \"\\n\" in txt:\n"
     "                forma.append(\"tem de ser uma linha so (entra dentro de uma linha do README)\")\n"
     "            if mk == \"README_H0DN\" and \"*\" in txt:\n"
     "                forma.append(\"nao pode trazer «*» (entra dentro do italico da parte P = nP)\")\n"
     "            if mk == \"README_STATUS_5SIGMA\" and re.search(r\"\\n\\s*\\n\", txt):\n"
     "                forma.append(\"nao pode ter linha em branco (entra dentro do paragrafo do estado)\")\n"
     "            if mk == \"README_RITOS\" and not all(ln.startswith(\"|\") and ln.rstrip().endswith(\"|\") for ln in txt.split(\"\\n\")):\n"
     "                forma.append(\"cada linha tem de ser uma linha de tabela markdown («| … |»)\")\n"
     "            if mk == \"README_FASE9_V2\" and \"REGISTRO_FASE9_V2.md\" not in txt:\n"
     "                forma.append(\"nao aponta para REGISTRO_FASE9_V2.md (onde o painel inteiro da Fase 9 V2 fica)\")\n"
     "            viol = forma + H0DN.conferir_bloco(txt, Vh, mk, painel=(mk == \"README_PAINEL_H0DN\"))\n"
     "            if viol:\n"
     "                raise Falha(\"o marcador %s_%s nao passa: %s\" % (mk, versao, \" | \".join(viol[:6])))\n"
     "            c.derivar(\"h0dn.readme.\" + ids_h[mk], txt, \"handoff\", \"marcador INICIO_%s_%s\" % (mk, versao), \"marcador\")\n"),
]

README = [
    ("BLOCOS = {\"primordial\": b_primordial, \"hubble_pt\": b_hubble_pt, \"status\": b_status, \"apoios\": b_apoios, \"ritos\": b_ritos, \"selo\": b_selo,\n"
     "          \"proveniencia\": b_proveniencia, \"mudou\": b_mudou}\n",
     "# ================================================================================================= o H0DN x BG1 ABERTO\n"
     "# " + AO_LADO + ". Com h0dn.aberto = true no PRIMORDIAL (um h0dn_bg1_vNNN de opened_once = true no\n"
     "# core selado), os blocos que diziam que beta_TGL na natureza a 5 sigma e o passo aberto saem dos marcadores do handoff (lidos e conferidos\n"
     "# pelo primordial.py): o painel do H0DN sobe ao topo; o da Fase 9 V2 vira uma linha EN e uma PT (README_FASE9_V2) e desce VERBATIM, com a\n"
     "# frase do autor de 02/11, para REGISTRO_FASE9_V2.md (gerado e pinado aqui: nada se perde, so muda de lugar); a linha da Fase 9 V2 na tabela\n"
     "# dos ritos da lugar a README_RITOS; o paragrafo do H0DN da parte P = nP, a README_H0DN. Sem o registro aberto, todo byte sai como antes:\n"
     "# as funcoes originais ficam intactas acima e o BLOCOS original fica abaixo, como registro.\n"
     "#   BLOCOS = {\"primordial\": b_primordial, \"hubble_pt\": b_hubble_pt, \"status\": b_status, \"apoios\": b_apoios, \"ritos\": b_ritos, \"selo\": b_selo,\n"
     "#             \"proveniencia\": b_proveniencia, \"mudou\": b_mudou}\n"
     "H0DN_FRASE_VELHA_P_IGUAL_NP = (\"O teste H0DN \u00d7 BG1: pr\u00e9-registrado; nenhum dado observado lido; n\u00e3o foi aberto: o certificado de poder foi recusado \"\n"
     "                               \"(declarado pelo executor, lido pela ger\u00eancia), teste sem poder preditivo discriminante n\u00e3o se abre, e a abertura \u00e9 de vers\u00e3o futura.\")\n"
     "REGISTRO_FASE9_V2 = \"REGISTRO_FASE9_V2.md\"\n"
     "_ANCORA_HUBBLE = \"`\\n>\\n> **Hubble-ratio test**\"\n"
     "\n\n"
     "def h0dn_aberto(C):\n"
     "    return (C.itens.get(\"h0dn.aberto\") or {}).get(\"valor\") is True\n"
     "\n\n"
     "def _trocar(s, velho, novo, rotulo):\n"
     "    n = s.count(velho)\n"
     "    if n != 1:\n"
     "        raise Falha(\"H0DN aberto: o trecho a trocar em %s aparece %d vez(es), nao 1: %r\" % (rotulo, n, velho[:70]))\n"
     "    return s.replace(velho, novo)\n"
     "\n\n"
     "def b_primordial_h0dn(C):\n"
     "    s = b_primordial(C)\n"
     "    if not h0dn_aberto(C):\n"
     "        return s\n"
     "    if s.count(_ANCORA_HUBBLE) != 1:\n"
     "        raise Falha(\"H0DN aberto: a ancora do painel da Fase 9 V2 nao esta uma vez no b_primordial\")\n"
     "    i = s.index(_ANCORA_HUBBLE)\n"
     "    return s[:i + 2] + \"\\n\" + C.v(\"h0dn.readme.painel\") + \"\\n\\n\" + C.v(\"h0dn.readme.fase9_v2\") + \"\\n\\n> \" + C.v(\"h0dn.readme.primordial_5sigma\") + \"\\n\"\n"
     "\n\n"
     "def b_hubble_pt_h0dn(C):\n"
     "    return \"\" if h0dn_aberto(C) else b_hubble_pt(C)\n"
     "\n\n"
     "def b_status_h0dn(C):\n"
     "    s = b_status(C)\n"
     "    if not h0dn_aberto(C):\n"
     "        return s\n"
     "    d = C.v(\"hubble.degrau_creditacao_sigma\")\n"
     "    velho = (\"What nature decides is not proved: the decisive open factor is **\\u03b2_TGL in nature at \\u2265 %d\\u03c3**. *Provada, como validade, em tr\\u00eas apoios; \"\n"
     "             \"ainda n\\u00e3o creditada; o fator decisivo aberto \\u00e9 \\u03b2_TGL na natureza a %d\\u03c3.*\" % (d, d))\n"
     "    return _trocar(s, velho, C.v(\"h0dn.readme.status_5sigma\"), \"b_status\")\n"
     "\n\n"
     "def b_ritos_h0dn(C):\n"
     "    s = b_ritos(C)\n"
     "    if not h0dn_aberto(C):\n"
     "        return s\n"
     "    velho = \"| Hubble ratio, Phase 9 V2 | `NOT_FALSIFIED_POWERED` (the panel at the top) | \\u03b2 in nature at %d\\u03c3: the step was not reached |\\n\" % C.v(\"hubble.degrau_creditacao_sigma\")\n"
     "    return _trocar(s, velho, C.v(\"h0dn.readme.ritos\").strip(\"\\n\") + \"\\n\", \"b_ritos\")\n"
     "\n\n"
     "def b_h0dn_paragrafo(C):\n"
     "    return C.v(\"h0dn.readme.paragrafo\")\n"
     "\n\n"
     "def registro_fase9_v2(C):\n"
     "    \"\"\"O painel inteiro da Fase 9 V2 e a frase do autor de 02/11, como estiveram no topo do README (as MESMAS funcoes, os MESMOS itens do PRIMORDIAL).\"\"\"\n"
     "    s = b_primordial(C)\n"
     "    if s.count(_ANCORA_HUBBLE) != 1:\n"
     "        raise Falha(\"H0DN aberto: a ancora do painel da Fase 9 V2 nao esta uma vez no b_primordial\")\n"
     "    hub = \"> **Hubble-ratio test**\" + s[s.index(_ANCORA_HUBBLE) + len(_ANCORA_HUBBLE):]\n"
     "    return (\"# Record \\u00b7 registro: the Phase 9 V2 panel (Hubble ratio, opened once on %s)\\n\\n\"\n"
     "            \"<!-- PINADO por tools/custodia_g1/readme_pinado.py \\u00b7 fonte PRIMORDIAL.json sha16 %s \\u00b7 pino PINO_README.json \\u00b7 n\\u00e3o editar \\u00e0 m\\u00e3o -->\\n\\n\"\n"
     "            \"*This panel stood at the top of the README until the custody of %s, when the H0DN \\u00d7 BG1 test, opened once (registry `%s`), took the top; \"\n"
     "            \"it moved here verbatim, from the same generator and the same PRIMORDIAL items. It stays true about that test.*\\n\\n\"\n"
     "            % (C.v(\"hubble.data_abertura\"), C.prim_sha16, C.v(\"selo.versao\"), C.v(\"h0dn.registro\")) + hub + \"\\n\" + b_hubble_pt(C))\n"
     "\n\n"
     "BLOCOS = {\"primordial\": b_primordial_h0dn, \"hubble_pt\": b_hubble_pt_h0dn, \"status\": b_status_h0dn, \"apoios\": b_apoios, \"ritos\": b_ritos_h0dn, \"selo\": b_selo,\n"
     "          \"proveniencia\": b_proveniencia, \"mudou\": b_mudou, \"h0dn_paragrafo\": b_h0dn_paragrafo}\n"),
    ("            render_texto(C, arq.read_text(encoding=\"utf-8\"), partes_dir, portas, segs, \"parte:\" + nome[6:], nivel + 1)\n",
     "            txt_parte = arq.read_text(encoding=\"utf-8\")\n"
     "            if h0dn_aberto(C) and nome[6:] == \"p_igual_np\":   # " + AO_LADO + ": o paragrafo do H0DN vem do handoff, como bloco gerado\n"
     "                txt_parte = _trocar(txt_parte, H0DN_FRASE_VELHA_P_IGUAL_NP, \"{{bloco:h0dn_paragrafo}}\", \"parte p_igual_np\")\n"
     "            render_texto(C, txt_parte, partes_dir, portas, segs, \"parte:\" + nome[6:], nivel + 1)\n"),
    ("    pino = montar_pino(C, b, prim_bytes, a.template, a.partes, a.nome, portas, a.nos, Path(__file__).resolve().parent)\n",
     "    pino = montar_pino(C, b, prim_bytes, a.template, a.partes, a.nome, portas, a.nos, Path(__file__).resolve().parent)\n"
     "    if h0dn_aberto(C):   # " + AO_LADO + ": o painel inteiro da Fase 9 V2, ao lado, pinado\n"
     "        reg_txt = registro_fase9_v2(C)\n"
     "        viol_h = textos.portao(_neutraliza(reg_txt), conhecidos_de(prim_bytes.decode(\"utf-8\")) | {C.prim_sha16}, rotulo=REGISTRO_FASE9_V2) + regra_444(reg_txt, C.P)\n"
     "        for id_ in (\"painel\", \"fase9_v2\", \"primordial_5sigma\", \"status_5sigma\", \"paragrafo\", \"ritos\"):\n"
     "            t_ = C.v(\"h0dn.readme.\" + id_)\n"
     "            viol_h += textos.portao(_neutraliza(t_), conhecidos_de(prim_bytes.decode(\"utf-8\")), rotulo=\"h0dn.readme.\" + id_) + regra_444(t_, C.P)\n"
     "        if viol_h:\n"
     "            raise Falha(\"H0DN aberto: o portao de textos ou a regra do 4,44 recusam: %s\" % \" | \".join(viol_h[:6]))\n"
     "        rb_ = reg_txt.encode(\"utf-8\")\n"
     "        est_r = escrever_bytes(saida / REGISTRO_FASE9_V2, rb_, \"REGISTRO\")\n"
     "        pino[\"registro_fase9_v2\"] = {\"arquivo\": REGISTRO_FASE9_V2, \"bytes\": len(rb_), \"sha256\": sha256b(rb_)}\n"
     "        print(\"%s: %d bytes, sha16 %s [%s]\" % (REGISTRO_FASE9_V2, len(rb_), sha256b(rb_)[:16], est_r))\n"),
    ("    g = Path(__file__).resolve().parent\n    for nome in (\"readme_pinado.py\", \"primordial.py\"):\n",
     "    if h0dn_aberto(C):   # " + AO_LADO + ": o registro da Fase 9 V2 confere com o gerador e com o pino\n"
     "        rp_ = readme_p.parent / REGISTRO_FASE9_V2\n"
     "        try:\n"
     "            esperado_ = registro_fase9_v2(C).encode(\"utf-8\")\n"
     "            if not rp_.is_file() or rp_.read_bytes() != esperado_:\n"
     "                erros.append(\"%s ausente ou diferente do regenerado\" % REGISTRO_FASE9_V2)\n"
     "            elif (pino.get(\"registro_fase9_v2\") or {}).get(\"sha256\") != sha256b(esperado_):\n"
     "                erros.append(\"%s nao e o do pino\" % REGISTRO_FASE9_V2)\n"
     "        except SystemExit as e:\n"
     "            erros.append(str(e))\n"
     "    g = Path(__file__).resolve().parent\n    for nome in (\"readme_pinado.py\", \"primordial.py\"):\n"),
]


def aplicar(nome, eds, crlf):
    P = os.path.join(G1, nome)
    b = open(P, "rb").read()
    n_crlf = b.count(b"\r\n")
    assert (n_crlf > 0) == crlf, "fim de linha inesperado em %s (CRLF %d)" % (nome, n_crlf)
    conv = (lambda s: s.replace("\n", "\r\n").encode("utf-8")) if crlf else (lambda s: s.encode("utf-8"))
    pares = [(conv(a), conv(d)) for a, d in eds]
    for a, _ in pares:
        assert b.count(a) == 1, "o trecho mudou em %s - PARAR: %r" % (nome, a[:90])
    bak = P + ".bak_%s_h0dn_aberto" % STAMP
    open(bak, "wb").write(b)
    assert open(bak, "rb").read() == b
    novo = b
    for a, d in pares:
        novo = novo.replace(a, d)
    compile(novo.decode("utf-8"), P, "exec")
    if crlf:
        assert novo.count(b"\n") == novo.count(b"\r\n"), "fim de linha misturado em %s" % nome
    else:
        assert novo.count(b"\r\n") == 0, "CRLF entrou em %s" % nome
    t = P + ".tmp_errata"
    open(t, "wb").write(novo)
    assert os.path.getsize(t) == len(novo) > len(b)
    os.replace(t, P)
    print("ok:", nome, len(b), "->", len(novo), "| backup", os.path.basename(bak))


aplicar("textos.py", TEXTOS, True)
aplicar("primordial.py", PRIMORDIAL, False)
aplicar("readme_pinado.py", README, False)
