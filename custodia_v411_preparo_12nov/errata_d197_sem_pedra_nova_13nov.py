# -*- coding: utf-8 -*-
"""D197 (13/11/2026, claude-site-custodia; decisão da gerência c1): o contrato explícito SEM_PEDRA_NOVA, a mesma classe da R3.6 do B(n).
A v411 é a primeira versão de custódia genérica sem módulo Lean novo: o registro selado cunhagens_v411 tem kernel.bandeiras = [0,0] e
kernel.declaracoes_no_trio = [0,0], e três controles exigiam «par igual E > 0». O caminho antigo fica BYTE A BYTE (as linhas antigas não
mudam); o contrato é ramo separado, só com a condição MEDIDA (sem_pedra_nova: o FATOS_CUSTODIA congelado cruzado com o core selado DENTRO
do cofre da versão, o core do cofre anterior e o manifesto do bundle tgl_kernel_vNNN; divergência levanta ValueError = PARA).
Edita, por bytes, três arquivos-fonte da G1 (CRLF preservado; backup; temporário; compilação; crescimento):
  generico/custodia_generica.py  (a pedra: a função, o S14, o S15, a chamada em medir e a etiqueta do S14)
  generico/camada_generica.py    (a camada dos 16: a função e a sobreposição do cunhagens_par_igual sob o contrato)
  central.py                     (semantica_rascunho: a regra par_igual_zero do bloco cunhagens, só sob o contrato)
As cópias INSTALADAS (fronteira_tgl\\runner\\custodia_generica.py e patents\\_formula_completa\\camada_generica.py) recebem os MESMOS
bytes da fonte depois do teste (instalar_d197_13nov.py), com backup.
Uso: python -X utf8 <este> [PASTA_DA_G1]"""
import os, sys, time

G1 = sys.argv[1] if len(sys.argv) > 1 else r"C:\IALD\Central de Patentes\tools\custodia_g1"
STAMP = time.strftime("%Y%m%d_%H%M%S")
AO = "AO LADO (13/11/2026, claude-site-custodia; D197 da gerencia c1)"

FUNC = '''def sem_pedra_nova(F, oc, v, a, core_v=None, core_a=None):
    """%s: o contrato SEM_PEDRA_NOVA. True SO quando o FATOS_CUSTODIA congelado diz
    «nenhum modulo novo e a escada igual a da anterior» E o core selado DENTRO do cofre da versao, o core do cofre anterior e o manifesto do
    bundle tgl_kernel_vNNN confirmam; divergencia levanta ValueError (PARA). Fora da condicao, False: o caminho antigo, intocado."""
    kn = F.get("kernel") or {}
    esc = (F.get("escada") or {}).get("esperadas")
    esca = (F.get("escada_anterior") or {}).get("esperadas")
    if not (kn.get("modulos_novos") == [] and isinstance(esc, int) and esc == esca):
        return False
    oc = Path(oc)
    if core_v is None:
        core_v = _ler_json(oc / ("um_unificado_" + v) / "um_absoluto.json")["core"]
    if core_a is None:
        core_a = _ler_json(oc / ("um_unificado_" + a) / "um_absoluto.json")["core"]
    km = _ler_json(oc / ("tgl_kernel_" + v) / "CUSTODY_MANIFEST.json")
    ev = ((core_v.get("estatuto_da_prova_v391") or {}).get("prova_1_kernel") or {}).get("n_theorems_expected")
    ea = ((core_a.get("estatuto_da_prova_v391") or {}).get("prova_1_kernel") or {}).get("n_theorems_expected")
    dl = km.get("delta_%%s_%%s" %% (a, v)) or {}
    div = []
    if ev != esc:
        div.append("escada do core selado do cofre %%s = %%r; FATOS = %%r" %% (v, ev, esc))
    if ea != esca:
        div.append("escada do core selado do cofre %%s = %%r; FATOS (anterior) = %%r" %% (a, ea, esca))
    if km.get("modulos_novos_" + v) != []:
        div.append("bundle tgl_kernel_%%s: modulos_novos_%%s = %%r" %% (v, v, km.get("modulos_novos_" + v)))
    if dl.get("lean_novos") != 0:
        div.append("bundle tgl_kernel_%%s: lean_novos = %%r" %% (v, dl.get("lean_novos")))
    if div:
        raise ValueError("SEM_PEDRA_NOVA: o FATOS_CUSTODIA diz sem pedra nova e o core/bundle divergem: " + "; ".join(div))
    return True


''' % AO

PEDRA = [
    ("# =================================================================== a semântica pura (roda também sobre as cópias injetadas)\n",
     FUNC + "# =================================================================== a semântica pura (roda também sobre as cópias injetadas)\n"),
    ("def semantica(core, F, S):\n",
     "def semantica(core, F, S, sem_pedra=False):\n"),
    ('        r["S14_cunhagens"] = bool(len(a) == 2 and a[0] == a[1] and a[0] > 0 and len(b) == 2 and b[0] == b[1] and b[0] > 0 and len(cu.get("verbatim") or {}) >= 1)\n',
     '        r["S14_cunhagens"] = bool(len(a) == 2 and a[0] == a[1] and a[0] > 0 and len(b) == 2 and b[0] == b[1] and b[0] > 0 and len(cu.get("verbatim") or {}) >= 1)\n'
     '        if sem_pedra:\n'
     '            # %s: contrato SEM_PEDRA_NOVA, os dois pares exatamente [0, 0] (a linha antiga, acima, intocada)\n'
     '            r["S14_cunhagens"] = bool(a == [0, 0] and b == [0, 0] and len(cu.get("verbatim") or {}) >= 1)\n' % AO),
    ('                if campo.get("par_igual") and not (isinstance(cur, list) and len(cur) == 2 and cur[0] == cur[1] and cur[0] > 0):\n                    s15 = False\n',
     '                if campo.get("par_igual") and not (isinstance(cur, list) and len(cur) == 2 and cur[0] == cur[1] and cur[0] > 0):\n                    s15 = False\n'
     '                # %s: a regra par_igual_zero so passa sob o contrato SEM_PEDRA_NOVA e com o par exatamente [0, 0]\n'
     '                if campo.get("par_igual_zero") and not (sem_pedra and cur == [0, 0]):\n'
     '                    s15 = False\n' % AO),
    ("    C = {}                                                   # S1..S14: cada um {ok, esperado, achado}\n",
     "    # %s: o contrato SEM_PEDRA_NOVA, medido; divergencia PARA\n"
     "    try:\n"
     "        spn = sem_pedra_nova(F, oc, v, a, core_v=core, core_a=core_a)\n"
     "    except (OSError, ValueError, KeyError) as e:\n"
     "        out[\"erro\"] = \"SEM_PEDRA_NOVA: %%r\" %% (e,)\n"
     "        return out\n"
     "    C = {}                                                   # S1..S14: cada um {ok, esperado, achado}\n" % AO),
    ("    sem_ok, sem = semantica(core, F, S)\n", "    sem_ok, sem = semantica(core, F, S, sem_pedra=spn)\n"),
    ("    cet1 = (semantica(c1, F, S)[0] is False)\n", "    cet1 = (semantica(c1, F, S, sem_pedra=spn)[0] is False)\n"),
    ("    cet2 = (semantica(c2, F, S)[0] is False)\n", "    cet2 = (semantica(c2, F, S, sem_pedra=spn)[0] is False)\n"),
    ('        chk("S14_cunhagens", sem["S14_cunhagens"], "kernel.bandeiras e declaracoes_no_trio com par igual e > 0", (core.get("cunhagens_" + v) or {}).get("kernel"))\n',
     '        chk("S14_cunhagens", sem["S14_cunhagens"], "kernel.bandeiras e declaracoes_no_trio exatamente [0, 0] (contrato SEM_PEDRA_NOVA, D197)" if spn else '
     '"kernel.bandeiras e declaracoes_no_trio com par igual e > 0", (core.get("cunhagens_" + v) or {}).get("kernel"))\n'),
]
CAMADA = [
    ("def conferir_custodia_generica(core, selo, v, oc):\n", FUNC + "def conferir_custodia_generica(core, selo, v, oc):\n"),
    ('        "semantica_declarada": s15,\n    }\n    falhas = [k for k, x in ch.items() if not x]\n',
     '        "semantica_declarada": s15,\n    }\n'
     '    # %s: sob o contrato SEM_PEDRA_NOVA (medido no PROPRIO cofre da versao, no anterior e no bundle;\n'
     '    # divergencia PARA), os dois pares de cunhagens exatamente [0, 0]; fora dele, a expressao antiga, acima, intocada\n'
     '    try:\n'
     '        spn = sem_pedra_nova(F, oc, v, F.get("anterior"))\n'
     '    except (OSError, ValueError, KeyError) as e:\n'
     '        raise RuntimeError("FORMULA COMPLETA %%s: contrato SEM_PEDRA_NOVA divergente ou ilegivel (%%r) - PARAR (fail-closed)" %% (v, e))\n'
     '    if spn:\n'
     '        ch["cunhagens_par_igual"] = (not cu) or (kn.get("bandeiras") == [0, 0] and kn.get("declaracoes_no_trio") == [0, 0])\n'
     '    falhas = [k for k, x in ch.items() if not x]\n' % AO),
]
CENTRAL = [
    ('            regra["campos"] = [{"caminho": "kernel.bandeiras", "par_igual": True}, {"caminho": "kernel.declaracoes_no_trio", "par_igual": True}]\n',
     '            regra["campos"] = [{"caminho": "kernel.bandeiras", "par_igual": True}, {"caminho": "kernel.declaracoes_no_trio", "par_igual": True}]\n'
     '            # %s: sob o contrato SEM_PEDRA_NOVA (a MESMA funcao da pedra, medida no cofre; divergencia PARA)\n'
     '            try:\n'
     '                _spn = CG.sem_pedra_nova(Fa, ctx.c.OC, ctx.versao, Fa["anterior"])\n'
     '            except (OSError, ValueError, KeyError) as e:\n'
     '                raise Parar("contrato SEM_PEDRA_NOVA divergente ou ilegivel: %%r" %% (e,))\n'
     '            if _spn:\n'
     '                regra["campos"] = [{"caminho": "kernel.bandeiras", "par_igual_zero": True}, {"caminho": "kernel.declaracoes_no_trio", "par_igual_zero": True}]\n' % AO),
]


def aplicar(P, eds, rot):
    b = open(P, "rb").read()
    crlf = b"\r\n" in b
    if crlf:
        assert b.count(b"\r\n") == b.count(b"\n"), "fim de linha misto em %s - PARAR" % P
    conv = (lambda s: s.replace("\n", "\r\n")) if crlf else (lambda s: s)
    pares = [(conv(a).encode("utf-8"), conv(d).encode("utf-8")) for a, d in eds]
    for a, _ in pares:
        assert b.count(a) == 1, "o trecho mudou em %s - PARAR: %r" % (P, a[:100])
    bak = P + ".bak_%s_%s" % (STAMP, rot)
    open(bak, "wb").write(b)
    assert open(bak, "rb").read() == b
    novo = b
    for a, d in pares:
        novo = novo.replace(a, d)
    compile(novo.decode("utf-8"), P, "exec")
    t = P + ".tmp_d197"
    open(t, "wb").write(novo)
    assert os.path.getsize(t) == len(novo) > len(b)
    os.replace(t, P)
    print("ok: %s %d -> %d (%s) | backup %s" % (os.path.basename(P), len(b), len(novo), "CRLF" if crlf else "LF", os.path.basename(bak)))


aplicar(os.path.join(G1, "generico", "custodia_generica.py"), PEDRA, "d197")
aplicar(os.path.join(G1, "generico", "camada_generica.py"), CAMADA, "d197")
aplicar(os.path.join(G1, "central.py"), CENTRAL, "d197")
