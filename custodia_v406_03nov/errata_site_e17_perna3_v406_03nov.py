# -*- coding: utf-8 -*-
"""03/11/2026 06:3x, gerencia c1: na retomada do S7 (orquestrador 05:51), a G1 parou em E17 (subida do site em ensaio): «o ensaio 20261103_051202_dryrun cobre o alvo
mas difere FORA do conjunto esperado (L10): central/RELATORIO_RETRATO_PUBLICO.json, central/api/fronteira.json, central/api/iald/status.json, central/api/patents/.../code.json...».
O que aconteceu: a perna 1 (E16-E19, o site) subiu as 02:49-03:11; DEPOIS a perna 3 (C18, a Central publica) rodou o encadeador ate' o ensaio (rodada 20261103_031336,
posterior ao commit da Central 42f3b0c9 das 03:12) e regenerou 82 arquivos de central/ dentro de v3.0; a subida da perna 3 (052210) foi revertida pelo Range do hospedeiro
(licao 49). Na retomada, o alvo da perna 1 corrente e' o DISCO INTEIRO de v3.0 (`_alvo`), logo E16 viu «manifesto velho frente ao disco: 82 mudados» e regenerou
manifesto_v406.json, e E17 achou um ensaio que cobre o alvo (o dry-run da perna 3) mas com diferencas que o ESPERADOS da perna 1 nao conhece: central/ e' da perna 3.
A regra L10 («o ensaio so' pode diferir no que ESTA custodia escreveu; nunca publicar meio-trabalho de outra sessao») esta' certa; o que faltava e' que a perna 3 da MESMA
custodia tambem escreve em v3.0 (central/, llms.txt, sitemap.xml, linhas-de-pesquisa.html...), e isso so' aparece na perna 1 quando C18 falha depois de E18 e a G1 e' retomada.
Conserto AO LADO em tools/custodia_g1/site.py: `fora_do_esperado(difs, ctx=None)` mantem o original (em comentario e como primeira passada) e, so' quando ha' diferencas
fora do conjunto da perna 1, a versao e' corrente e EXISTE a rodada da perna 3 completa ate' o ensaio para esta versao (publica._rodada_completa_ate_o_ensaio: ok, passos
ate' subir_ensaio com rc 0, posterior ao commit da custodia, com o manifesto do carimbo), desconta tambem o ESPERADOS_PERNA3 de publica.py (o mesmo conjunto que o C18 ja'
aplica ao ensaio da perna 3). Sem a rodada da perna 3, nada muda: meio-trabalho de outra sessao segue barrado. Os dois chamadores (_ja_e17 e _ap_e17) passam ctx; a marca
APLICADO de E17 diz quando o conjunto da perna 3 entrou. Aplicado por patches.aplicar_em_arquivo (backup de BYTES, py_compile, os.replace); conferido por
`custodiar.py planejar --seco` (so' leitura) depois. Nada toca o ar, o um.py, o selo, o cofre ou o gate. Escrito pelo Write."""
import json, sys
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes"); SITE = CEN / "tools" / "custodia_g1" / "site.py"
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import patches  # noqa: E402

O1 = ("def fora_do_esperado(difs):\n"
      "    return [(p, e) for p, e in difs if not any(rx.match(p) for rx in ESPERADOS)]\n")
N1 = ("def _perna3_pronta_ate_o_ensaio(ctx):\n"
      "    \"\"\"[AO LADO, 03/11/2026, gerência c1, custódia v406] (carimbo, manifesto) da rodada da perna 3 (Central pública, C18) completa até o ensaio, posterior ao commit\n"
      "    da custódia e com o manifesto do carimbo — ou None. Memo em ctx. Só se consulta quando o ensaio da perna 1 difere fora do seu conjunto.\"\"\"\n"
      "    if \"perna3_pronta\" not in ctx._memo:\n"
      "        from . import publica\n"
      "        try:\n"
      "            passos = [n for n in publica._passos_do_encadeador(ctx) if n not in publica.FORA_DA_CHAMADA]\n"
      "            ate = passos[: passos.index(\"subir_ensaio\") + 1] if \"subir_ensaio\" in passos else None\n"
      "            ctx._memo[\"perna3_pronta\"] = publica._rodada_completa_ate_o_ensaio(ctx, ate) if ate else None\n"
      "        except Exception:  # noqa: BLE001 — sem a rodada da perna 3, a regra original vale inteira\n"
      "            ctx._memo[\"perna3_pronta\"] = None\n"
      "    return ctx._memo[\"perna3_pronta\"]\n"
      "\n"
      "\n"
      "def fora_do_esperado(difs, ctx=None):\n"
      "    # ERRATA AO LADO (03/11/2026, gerência c1, custódia v406): o original (abaixo, intacto) só conhecia o conjunto da perna 1:\n"
      "    #     def fora_do_esperado(difs):\n"
      "    #         return [(p, e) for p, e in difs if not any(rx.match(p) for rx in ESPERADOS)]\n"
      "    # Na retomada da v406 (C18 falhou DEPOIS de E18: o hospedeiro não honrou o Range, lição 49), a perna 3 da MESMA custódia já tinha regenerado 82 arquivos de\n"
      "    # central/ dentro de v3.0 (rodada 20261103_031336, posterior ao commit da Central), e E17 bloqueou o site por «meio-trabalho de outra sessão». Não era de outra\n"
      "    # sessão: era a perna 3 desta custódia. Leitura vigente: com ctx, versão corrente e a rodada da perna 3 completa até o ensaio para esta versão, desconta-se TAMBÉM\n"
      "    # o ESPERADOS_PERNA3 de publica.py (o mesmo conjunto que C18 aplica ao ensaio da perna 3). Sem essa rodada, nada muda: L10 segue inteira.\n"
      "    fora = [(p, e) for p, e in difs if not any(rx.match(p) for rx in ESPERADOS)]\n"
      "    if fora and ctx is not None and ctx.corrente and _perna3_pronta_ate_o_ensaio(ctx) is not None:\n"
      "        from .publica import ESPERADOS_PERNA3\n"
      "        p3 = [re.compile(x) for x in ESPERADOS_PERNA3]\n"
      "        fora = [(p, e) for p, e in fora if not any(rx.match(p) for rx in p3)]\n"
      "    return fora\n"
      "\n"
      "\n"
      "def _sufixo_perna3(ctx):\n"
      "    \"\"\"[AO LADO, 03/11/2026] a frase da marca quando o conjunto da perna 3 entrou na conta — ou vazio.\"\"\"\n"
      "    r = ctx._memo.get(\"perna3_pronta\") if hasattr(ctx, \"_memo\") else None\n"
      "    return (\" [+ o conjunto da perna 3, pela rodada %s do encadeador até o ensaio; ao lado, 03/11/2026]\" % r[0]) if r else \"\"\n")
O2 = ("        fora = fora_do_esperado(difs)\n"
      "        if fora and ctx.corrente:\n")
N2 = ("        fora = fora_do_esperado(difs, ctx)  # [AO LADO, 03/11/2026] com ctx: o conjunto da perna 3 entra se a rodada dela até o ensaio existir\n"
      "        if fora and ctx.corrente:\n")
O3 = ("        return aplicado(\"ensaio %s cobre o alvo (%s): %d arquivos, sha16 de cada um igual; %d diferenças com o ar, todas no conjunto esperado\" % (p.name, desc, len(alvo), len(difs)))\n")
N3 = ("        return aplicado(\"ensaio %s cobre o alvo (%s): %d arquivos, sha16 de cada um igual; %d diferenças com o ar, todas no conjunto esperado%s\" % (p.name, desc, len(alvo), len(difs), _sufixo_perna3(ctx)))\n")
O4 = ("    fora = fora_do_esperado(difs)\n"
      "    if fora:\n"
      "        raise Parar(\"o ensaio da subida difere FORA do conjunto esperado desta custódia (publicaria meio-trabalho de outra sessão — L10)\", [\"%s: %s\" % x for x in fora[:20]])\n"
      "    return {\"relatorio\": ens[-1].name, \"diferencas_esperadas\": len(difs)}\n")
N4 = ("    fora = fora_do_esperado(difs, ctx)  # [AO LADO, 03/11/2026] idem _ja_e17\n"
      "    if fora:\n"
      "        raise Parar(\"o ensaio da subida difere FORA do conjunto esperado desta custódia (publicaria meio-trabalho de outra sessão — L10)\", [\"%s: %s\" % x for x in fora[:20]])\n"
      "    return {\"relatorio\": ens[-1].name, \"diferencas_esperadas\": len(difs), \"conjunto\": (\"perna 1 + perna 3\" if _sufixo_perna3(ctx) else \"perna 1\")}\n")
PARES = [(O1, N1, "1 fora_do_esperado(difs, ctx) + _perna3_pronta_ate_o_ensaio + _sufixo_perna3 (ao lado)"), (O2, N2, "2 _ja_e17 passa ctx"),
         (O3, N3, "3 marca de E17 diz quando a perna 3 entrou"), (O4, N4, "4 _ap_e17 passa ctx e registra o conjunto")]


def f(s):
    assert "ERRATA AO LADO (03/11/2026, gerência c1, custódia v406): o original (abaixo, intacto) só conhecia o conjunto da perna 1" not in s, "a errata ja esta' no site.py"
    for o, _, nome in PARES:
        assert s.count(o) == 1, "trecho original nao esta' UMA vez (%d): %s" % (s.count(o), nome)
    for o, n, _ in PARES:
        s = s.replace(o, n)
    return s, [p[2] for p in PARES]


r = patches.aplicar_em_arquivo(SITE, f, "v406_errata_e17_perna3")
print("patch:", json.dumps(r, ensure_ascii=False)); assert r["estado"] == "aplicado"
# importa o pacote depois do patch (sintaxe e nomes): fail-closed
import importlib  # noqa: E402
m = importlib.import_module("custodia_g1.site"); assert callable(m.fora_do_esperado) and callable(m._perna3_pronta_ate_o_ensaio)
print("OK: custodia_g1.site importa com a errata ao lado; conferir com `custodiar.py planejar --seco`")
