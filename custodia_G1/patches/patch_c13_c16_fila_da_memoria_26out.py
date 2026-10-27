# -*- coding: utf-8 -*-
"""G1 obedece à FILA DA MEMÓRIA (26/10/2026, ordem do operador; regra em memory\\fila\\README.md; item 6 do
work\\memoria_inteligente_26out\\ROTEIRO_MEMORIA_INTELIGENTE_26out.md): só a gerência c1 escreve MEMORY.md, MEMORY_2.md e os
arquivos-tópico do diretório da memória. C13 e C16, rodados pela sessão do site, passam a DEPOSITAR (memoria.py depositar --quem
claude-site) o que antes acrescentavam; o «já aplicado» aceita o depósito (ou a promoção, que leva a sentinela ao tópico).
O DIARIO_DO_SITE.md e o Atlas (fora do diretório da memória) seguem como estavam. Trocas contadas; backup de bytes; py_compile."""
import os
import py_compile
import time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\memorias.py")
raw = P.read_bytes()
assert raw.count(b"\r\n") == raw.count(b"\n")                       # o arquivo é todo CRLF: casa-se em LF e grava-se em CRLF
s = raw.decode("utf-8").replace("\r\n", "\n")

pares = [
    # 0. a nota no topo
    ('Backup de BYTES antes de tocar (regra de 22/08/2026); correção AO LADO, nunca por cima; MEMORY.md < 24 KB (alarme a 90%, parada a 98%)."""',
     'Backup de BYTES antes de tocar (regra de 22/08/2026); correção AO LADO, nunca por cima; MEMORY.md < 24 KB (alarme a 90%, parada a 98%).\n\n'
     '  L23 a FILA DA MEMÓRIA (26/10/2026, ordem do operador; memory\\\\fila\\\\README.md): só a gerência c1 escreve MEMORY.md, MEMORY_2.md e os\n'
     '      arquivos-tópico do diretório da memória. C13/C16 DEPOSITAM (memoria.py depositar --quem claude-site), uma vez por sentinela; o\n'
     '      «já aplicado» aceita o depósito ou a promoção (que leva a sentinela ao tópico). DIARIO_DO_SITE.md e o Atlas seguem como estavam."""'),
    # 1. os ajudantes da fila, depois de sent()
    ('def sent(ctx, bloco):\n    return "<!-- custodia:%s:%s -->" % (ctx.versao, bloco)\n',
     'def sent(ctx, bloco):\n    return "<!-- custodia:%s:%s -->" % (ctx.versao, bloco)\n\n\n'
     '# =================================================================== a FILA DA MEMÓRIA (L23)\n'
     'QUEM_FILA = "claude-site"\n\n\n'
     'def _na_memoria(ctx, p):\n'
     '    """O arquivo mora no diretório da memória (onde só a gerência c1 escreve)?"""\n'
     '    return os.path.normcase(str(Path(p).parent)) == os.path.normcase(str(ctx.c.MEM))\n\n\n'
     'def _depositos_com(ctx, sentinela):\n'
     '    d = ctx.c.MEM / "fila" / "depositos" / QUEM_FILA\n'
     '    return [x for x in sorted(d.glob("*.md")) if sentinela in util.ler_texto(x, "replace")] if d.is_dir() else []\n\n\n'
     'def depositar(ctx, alvo, texto, sentinela, bloco):\n'
     '    """Deposita UMA vez na fila (a sentinela vai no corpo): já depositado, ou já promovido (a sentinela no tópico), nada faz."""\n'
     '    if _depositos_com(ctx, sentinela):\n'
     '        return {"estado": "ja_depositado"}\n'
     '    t = ctx.c.MEM / alvo\n'
     '    if alvo.endswith(".md") and t.is_file() and sentinela in util.ler_texto(t, "replace"):\n'
     '        return {"estado": "ja_aplicado"}\n'
     '    slug = re.sub(r"[^a-z0-9_-]+", "-", ("custodia_%s_%s" % (ctx.versao, bloco)).lower()).strip("-")[:64]\n'
     '    arq = ctx.W / "fila_da_memoria" / (slug + ".md")\n'
     '    arq.parent.mkdir(parents=True, exist_ok=True)\n'
     '    util.escrever_atomico(arq, (texto.strip("\\n") + "\\n" + sentinela + "\\n").encode("utf-8"), backup=True)\n'
     '    r = util.rodar([str(ctx.c.PYTHON), "-X", "utf8", str(ctx.c.MEM / "fila" / "memoria.py"), "depositar", "--quem", QUEM_FILA, "--tipo", "project",\n'
     '                    "--estatuto", "REAL", "--alvo", alvo, "--fonte", str(ctx.handoff.caminho), "--texto-arquivo", str(arq), "--slug", slug])\n'
     '    if r["rc"] != 0:\n'
     '        raise Parar("memoria.py depositar recusou o depósito para %s" % alvo, r["saida"].strip().splitlines()[-4:])\n'
     '    return {"estado": "depositado"}\n\n\n'
     'def registrar_memoria(ctx, nome, texto, bloco):\n'
     '    """Uma superfície do diretório da memória: deposita para a gerência (o tópico que ainda não existe vai como novo:<slug>)."""\n'
     '    p = ctx.c.memoria(nome)\n'
     '    alvo = nome if p.is_file() else "novo:" + nome[:-3]\n'
     '    return depositar(ctx, alvo, texto, sent(ctx, bloco), bloco)\n'),
    # 2. _ja_c13: a superfície vale registrada no tópico OU depositada
    ('    for nome, p, bloco in _superficies_c13(ctx):\n'
     '        if not p.is_file():\n'
     '            faltam.append("%s ausente" % nome)\n',
     '    for nome, p, bloco in _superficies_c13(ctx):\n'
     '        if _na_memoria(ctx, p) and _depositos_com(ctx, sent(ctx, bloco)):\n'
     '            continue                                           # depositada na fila: a promoção é da gerência c1 (L23)\n'
     '        if not p.is_file():\n'
     '            faltam.append("%s ausente" % nome)\n'),
    ('    elif not ok:\n        faltam.append("linha do MEMORY.md ainda sem CUSTODIADO/PUBLICADA")\n'
     '    return aplicado("Atlas, as 6 memórias/diários (%s) e a linha do MEMORY.md" % ", ".join(n for n, _, _ in _superficies_c13(ctx))[:150]) if not faltam else falta("faltam: " + "; ".join(faltam))\n',
     '    elif not ok and not _depositos_com(ctx, sent(ctx, "indice:custodiado")):\n        faltam.append("linha do MEMORY.md ainda sem CUSTODIADO/PUBLICADA (nem a troca depositada na fila)")\n'
     '    return aplicado(("Atlas, as 6 memórias/diários (%s) e a linha do MEMORY.md" % ", ".join(n for n, _, _ in _superficies_c13(ctx)))[:150] + "; as do diretório da memória pela fila (L23)") if not faltam else falta("faltam: " + "; ".join(faltam))\n'),
    # 3. _pre_c13: o handoff de memória ausente vai como novo:
    ('            ctx.aviso("%s não existe: será criado do molde, marcado DECLARADO" % rot)\n',
     '            ctx.aviso("%s não existe: vai à fila como novo:%s (a gerência c1 cria o tópico)" % (rot, rot[:-3]))\n'),
    # 4. a troca da linha do índice vira PROPOSTA depositada
    ('def montar_rota(ctx, estado):\n',
     'def propor_linha_memory(ctx, marcas_ja, rotulo, extra, bloco):\n'
     '    """A troca da linha «- [HANDOFF vN » do índice, DEPOSITADA para a gerência c1 (L23): a antiga e a nova, verbatim; trocar e mover a antiga ao\n'
     '    MEMORY_2.md (regra dos dois arquivos) é ato da gerência."""\n'
     '    p = ctx.c.memoria("MEMORY.md")\n'
     '    antiga, ok = _memory_ja(ctx, marcas_ja)\n'
     '    if antiga is None:\n'
     '        raise Parar("a linha «- [HANDOFF %s » não existe no MEMORY.md" % ctx.versao)\n'
     '    if ok:\n'
     '        return {"estado": "ja_aplicado"}\n'
     '    nova = _linha_nova_memory(ctx, antiga, rotulo, extra)\n'
     '    tam = len(util.ler_bytes(p)) - len(antiga.encode("utf-8")) + len(nova.encode("utf-8"))\n'
     '    nota = ""\n'
     '    if tam > 0.90 * TETO_MEMORY:\n'
     '        nota = " Medido: com a troca, o MEMORY.md iria a %d B (%.0f%% do teto de 24 KB)." % (tam, 100.0 * tam / TETO_MEMORY)\n'
     '        ctx.aviso("a troca depositada levaria o MEMORY.md a %.0f%% do teto de 24 KB" % (100.0 * tam / TETO_MEMORY))\n'
     '    texto = ("Troca proposta da linha do índice da custódia %s (%s). Ato da gerência: substituir a linha ANTIGA pela NOVA e levar a antiga, VERBATIM, "\n'
     '             "ao MEMORY_2.md (regra dos dois arquivos).%s\\n\\nANTIGA:\\n%s\\n\\nNOVA:\\n%s" % (ctx.versao, rotulo, nota, antiga, nova))\n'
     '    return depositar(ctx, "MEMORY.md (linha de indice)", texto, sent(ctx, "indice:" + bloco), "indice_" + bloco)\n\n\n'
     'def montar_rota(ctx, estado):\n'),
    # 5. _ap_c13: as quatro memórias de sessão, o handoff e a linha do índice
    ('    saidas["site-sessao-estado"] = ap(c.memoria("site-sessao-estado.md"), "## %s \\u2014 %s no ar\\n\\n%s" % (when, v, estado), sent(ctx, "site_sessao_estado"))\n',
     '    saidas["site-sessao-estado"] = registrar_memoria(ctx, "site-sessao-estado.md", "## %s \\u2014 %s no ar\\n\\n%s" % (when, v, estado), "site_sessao_estado")\n'),
    ('    saidas["tgl-fronteira-teorica"] = ap(c.memoria("tgl-fronteira-teorica.md"),\n',
     '    saidas["tgl-fronteira-teorica"] = registrar_memoria(ctx, "tgl-fronteira-teorica.md",\n'),
    ('                                                  Fa["registro"]["pt"], Fa["registro"]["anterior"], Fa["anterior"], len(Fa["registro"]["mudados"]), Fa["kernel"]["formais"], Fa["kernel"]["declaracoes"]),\n'
     '        sent(ctx, "fronteira_teorica"))\n',
     '                                                  Fa["registro"]["pt"], Fa["registro"]["anterior"], Fa["anterior"], len(Fa["registro"]["mudados"]), Fa["kernel"]["formais"], Fa["kernel"]["declaracoes"]),\n'
     '        "fronteira_teorica")\n'),
    ('    saidas["central-de-patentes-estado"] = ap(c.memoria("central-de-patentes-estado.md"), "## %s \\u2014 custódia %s\\n\\n%s" % (when, v, estado), sent(ctx, "central_estado"))\n'
     '    saidas["dispositivos-formula-completa"] = ap(c.memoria("dispositivos-formula-completa.md"),\n',
     '    saidas["central-de-patentes-estado"] = registrar_memoria(ctx, "central-de-patentes-estado.md", "## %s \\u2014 custódia %s\\n\\n%s" % (when, v, estado), "central_estado")\n'
     '    saidas["dispositivos-formula-completa"] = registrar_memoria(ctx, "dispositivos-formula-completa.md",\n'),
    ('        "regerados. Nada muda número de dispositivo." % (when, v, v, ", ".join(Fa["registros_novos"]), Fa["escada"]["texto"], fv["n_disp"], fv["n_dev"], fv["final"] if fv["final"] else fv["n_dev"]),\n'
     '        sent(ctx, "dispositivos"))\n',
     '        "regerados. Nada muda número de dispositivo." % (when, v, v, ", ".join(Fa["registros_novos"]), Fa["escada"]["texto"], fv["n_disp"], fv["n_dev"], fv["final"] if fv["final"] else fv["n_dev"]),\n'
     '        "dispositivos")\n'),
    ('    h = c.memoria("handoff-%s-custodia.md" % v)\n'
     '    if not h.is_file():\n'
     '        util.escrever_atomico(h, ("---\\nname: HANDOFF %s \\u2014 custódia (criado por G1, DECLARADO)\\ndescription: memória da custódia de %s; criada do molde porque a gerência c1 não a emitiu\\n---\\n\\n"\n'
     '                                  "Handoff: `Nós\\\\HANDOFF_%s_CUSTODIA.md` (sha16 `%s`). [DECLARADO] criado por G1.\\n" % (v, v, v, ctx.handoff.sha16_arquivo)).encode("utf-8"), backup=False)\n'
     '    saidas["handoff-memoria"] = ap(h, "## %s \\u2014 CUSTODIADO pela sessão %s da Central\\n\\n%s" % (when, ctx.sessao, estado), sent(ctx, "handoff_custodiado"))\n',
     '    h = c.memoria("handoff-%s-custodia.md" % v)\n'
     '    molde = "" if h.is_file() else ("Handoff: `Nós\\\\HANDOFF_%s_CUSTODIA.md` (sha16 `%s`); o tópico ainda não existe: a gerência c1 o cria.\\n\\n" % (v, ctx.handoff.sha16_arquivo))\n'
     '    saidas["handoff-memoria"] = registrar_memoria(ctx, "handoff-%s-custodia.md" % v, "%s## %s \\u2014 CUSTODIADO pela sessão %s da Central\\n\\n%s" % (molde, when, ctx.sessao, estado), "handoff_custodiado")\n'),
    ('    saidas["MEMORY.md"] = trocar_linha_memory(ctx, ("CUSTODIADO", "PUBLICADA"), "CUSTODIADO",\n',
     '    saidas["MEMORY.md"] = propor_linha_memory(ctx, ("CUSTODIADO", "PUBLICADA"), "CUSTODIADO",\n'),
    ('                                              "the_boundary `%s`; Central: cofre %s, runner v%d, %d/%d, FINAL, ledger %s" % (fv["esp"], v, fv["runner_n"], fv["n_disp"], fv["n_dev"], fv["ledger"].get("erros")), "custodiado")\n'
     '    if os.path.getsize(c.memoria("MEMORY.md")) >= TETO_MEMORY:\n'
     '        raise Parar("MEMORY.md passou de 24 KB")\n',
     '                                              "the_boundary `%s`; Central: cofre %s, runner v%d, %d/%d, FINAL, ledger %s" % (fv["esp"], v, fv["runner_n"], fv["n_disp"], fv["n_dev"], fv["ledger"].get("erros")), "custodiado")\n'),
    ('    return Passo("C13", 4, "registro: diário do site, memórias, Atlas, MEMORY.md (a rota é de C16)", _ja_c13, aplicar=_ap_c13, pre=_pre_c13, fase="B",\n'
     '                 escreve="DIARIO_DO_SITE.md, memórias da sessão, TGL_ATLAS.md (só acréscimo), MEMORY.md/MEMORY_2.md")\n',
     '    return Passo("C13", 4, "registro: diário do site, Atlas; memórias e linha do MEMORY.md pela fila da memória (a rota é de C16)", _ja_c13, aplicar=_ap_c13, pre=_pre_c13, fase="B",\n'
     '                 escreve="DIARIO_DO_SITE.md, TGL_ATLAS.md (só acréscimo), depósitos em memory\\\\fila\\\\depositos\\\\claude-site (memórias da sessão e a troca da linha do MEMORY.md)")\n'),
    # 6. C16
    ('    lin, ok = _memory_ja(ctx, ("PUBLICADA",))\n'
     '    if lin is None:\n'
     '        return falta("linha do handoff %s ausente no MEMORY.md" % ctx.versao)\n'
     '    h = ctx.c.memoria("handoff-%s-custodia.md" % ctx.versao)\n'
     '    tem = h.is_file() and "PUBLICADA (pós-push)" in util.ler_texto(h, "replace")\n',
     '    lin, ok = _memory_ja(ctx, ("PUBLICADA",))\n'
     '    if lin is None:\n'
     '        return falta("linha do handoff %s ausente no MEMORY.md" % ctx.versao)\n'
     '    ok = ok or bool(_depositos_com(ctx, sent(ctx, "indice:publicada")))\n'
     '    h = ctx.c.memoria("handoff-%s-custodia.md" % ctx.versao)\n'
     '    tem = (h.is_file() and "PUBLICADA (pós-push)" in util.ler_texto(h, "replace")) or bool(_depositos_com(ctx, sent(ctx, "publicada_handoff")))\n'),
    ('        return aplicado("MEMORY.md e handoff-%s-custodia.md dizem PUBLICADA; rota custodia.%s registrada" % (ctx.versao, ctx.versao))\n',
     '        return aplicado("MEMORY.md e handoff-%s-custodia.md dizem PUBLICADA (ou a fila da memória o tem para a gerência); rota custodia.%s registrada" % (ctx.versao, ctx.versao))\n'),
    ('    s["handoff"] = ap(c.memoria("handoff-%s-custodia.md" % v), "## %s \\u2014 PUBLICADA (pós-push)\\n\\n%s" % (when, txt), sent(ctx, "publicada_handoff"))\n'
     '    s["central-estado"] = ap(c.memoria("central-de-patentes-estado.md"), "## %s \\u2014 custódia %s publicada\\n\\n%s" % (when, v, txt), sent(ctx, "publicada_central"))\n',
     '    s["handoff"] = registrar_memoria(ctx, "handoff-%s-custodia.md" % v, "## %s \\u2014 PUBLICADA (pós-push)\\n\\n%s" % (when, txt), "publicada_handoff")\n'
     '    s["central-estado"] = registrar_memoria(ctx, "central-de-patentes-estado.md", "## %s \\u2014 custódia %s publicada\\n\\n%s" % (when, v, txt), "publicada_central")\n'),
    ('    s["MEMORY.md"] = trocar_linha_memory(ctx, ("PUBLICADA",), "PUBLICADA",',
     '    s["MEMORY.md"] = propor_linha_memory(ctx, ("PUBLICADA",), "PUBLICADA",'),
    ('                 escreve="memórias da sessão, DIARIO_DO_SITE.md, MEMORY.md (o Atlas não se toca depois do push), mapa de rotas (só-acréscimo)")\n',
     '                 escreve="DIARIO_DO_SITE.md, depósitos na fila da memória (memórias da sessão e a troca da linha do MEMORY.md; o Atlas não se toca depois do push), mapa de rotas (só-acréscimo)")\n'),
]
for a, b in pares:
    n = s.count(a)
    assert n == 1, (a[:90], n)
    s = s.replace(a, b)
assert "ap(c.memoria(" not in s and "ap(h," not in s, "sobrou escrita direta no diretório da memória"
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp")
t.write_bytes(s.replace("\n", "\r\n").encode("utf-8"))
py_compile.compile(str(t), doraise=True)
os.replace(t, P)
print("ok", len(raw), "->", P.stat().st_size)
