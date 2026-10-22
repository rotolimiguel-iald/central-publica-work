# -*- coding: utf-8 -*-
"""editar_resultado_d19c.py -- DELTA 19/10 (rodada d19c): ajusta gerar_resultado.py para o estado FINAL: cabecalho (pos_rito so' foi tocada em textos_v394.py), a nova secao 0.1 (as quatro ordens), a clausula «teoremas limpos»,
as secoes 7 e 8 (agora vem de resultado_d19c.py) e os comandos de «como refazer». Backup de BYTES antes (.bak_<STAMP>_c1d19c), ancoras unicas, temporario -> conferir -> substituir, idempotente."""
import hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(HERE, "gerar_resultado.py")
BS = chr(92)
raw = open(ALVO, "rb").read(); s = raw.decode("utf-8")
if "resultado_d19c" in s:
    print("JA APLICADO (idempotente): gerar_resultado.py"); sys.exit(0)


def uma(a, b):
    global s
    assert s.count(a) == 1, ("ancora nao unica", a[:90], s.count(a))
    s = s.replace(a, b)


# (1) cabecalho
uma("escopo ampliado em duas ordens (a integração final da v394).", "escopo ampliado em duas ordens (a integração final da v394) e uma rodada final (d19c: a seção 0.1).")
uma("`pos_rito" + BS * 2 + "` não foi tocada (o aviso do coordenador foi cumprido: `derivar_cadeia_v394.py` NÃO rodou).",
    "`pos_rito" + BS * 2 + "` só foi tocada na rodada final e só em `textos_v394.py` (a proposta aprovada e a frase de errata, por ordem expressa, com backup de bytes; `derivar_cadeia_v394.py` NÃO rodou).")
# (2) o contexto e as secoes novas
uma('sim_r = SIM["kh_n1_cobertura_v394"]; ver = EXM["verify"]\n',
    'sim_r = SIM["kh_n1_cobertura_v394"]; ver = EXM["verify"]\n'
    'import glob\n'
    'sys.path.insert(0, HERE)\n'
    'import resultado_d19c as RD  # noqa: E402\n'
    'HA, HD = J(HERE, "HARNESS_TEXTOS_ENSAIO_ANTES_original.json"), J(HERE, "HARNESS_TEXTOS_ENSAIO_DEPOIS_aplicado.json")\n'
    'al_ = {e_["arquivo"]: e_ for e_ in ALT["alterados"]}\n'
    'inter_ = sorted(glob.glob(os.path.join(V, "um_v394_candidato_d19.py.bak_*_c1d19c"))); assert len(inter_) == 1, inter_\n'
    'C_ = {"OLD": OLD, "S16": S16, "CM": CM, "ESP": ESP, "ENS": ENS, "SIM": SIM, "EXM": EXM, "CN": CN, "PRE": PRE, "POS": J(HERE, "conferencia_POSITIVO_FALSO_NOS.json"), "SOMA": SOMA, "HA": HA, "HD": HD, "bg": bg,\n'
    '      "dv": KH["delta_vs_v393"], "nao_thm": KH["delta_vs_v393"]["decl"] - KH["delta_vs_v393"]["thm"], "tx": al_["pos_rito/textos_v394.py"], "ap_": al_["artigo_pt_v394.pysnip"], "ae": al_["artigo_en_v394.pysnip"], "es_": al_["ESTADO_V394.md"],\n'
    '      "ERR": DL.ERRATA_TEOREMAS_PT, "INTER": hashlib.sha256(open(inter_[0], "rb").read()).hexdigest()[:16], "INTER_BAK": os.path.basename(inter_[0]),\n'
    '      "erro_antes": (HA["etapas"]["_d"].get("erro") or "").split(": ", 1)[-1], "ntexto": sum(1 for k_ in HD["etapas"] if k_ != "leitura"),\n'
    '      "com_errata": [k_ for k_, e_ in HD["etapas"].items() if isinstance(e_, dict) and e_.get("tem_errata_teoremas")]}\n')
uma('a("## 1. A pedra candidata (nome provisório: o operador nomeia) [REAL a conjunção; ONTO a leitura]")',
    'for l_ in RD.secao_0_1(C_):\n    a(l_)\na("## 1. A pedra candidata (nome provisório: o operador nomeia) [REAL a conjunção; ONTO a leitura]")')
# (3) a clausula «teoremas limpos» da secao 3
uma("**NÃO mudei**: a frase «teoremas limpos» (15 ocorrências; 7 «clean theorems») no artigo e no stdout do rito (`teoremas limpos: N/M`, l.242868 do candidato), porque `pos_rito" + BS * 2 + "leitura_v394.py` PARSEIA essa linha por regex e a errata de 13/10 (`estatuto_da_prova_ressalva_v392`) já diz o que o número conta; é decisão da gerência.",
    "**Mantive** a frase «teoremas limpos» como REGISTRO DE MÁQUINA no artigo e no stdout do rito (`teoremas limpos: N/M`), porque `pos_rito" + BS * 2 + "leitura_v394.py` PARSEIA essa linha por regex (decisão da gerência de 19/10: manter o token e acrescentar a errata ao lado; ver a seção 0.1, item 2).")
# (4) as secoes 7 e 8 passam a vir do modulo novo
i0, i1 = s.index('a("## 7. Os textos do pós-rito'), s.index('a("## 9. Arquivos alterados')
assert s.count('a("## 7. Os textos do pós-rito') == 1 and s.count('a("## 9. Arquivos alterados') == 1 and i0 < i1
s = s[:i0] + "for l_ in RD.secao_7_8(C_):\n    a(l_)\n" + s[i1:]
# (5) como refazer
uma("Scripts de edição do delta (já aplicados, falham se repetidos): `delta_19out" + BS * 2 + "editar_*.py`, `aplicar_bloco.py`.",
    "Scripts de edição do delta (já aplicados, falham se repetidos): `delta_19out" + BS * 2 + "editar_*.py`, `aplicar_bloco.py`. Rodada final (d19c), nesta ordem: `aplicar_pos_rito_d19c.py`, `editar_delta19_errata_d19c.py`, `editar_artigo_errata_d19c.py` (antes do `gerar_candidato`); depois do ensaio e de `teste_conferidor_positivo.py` (que monta o Nós falso): `harness_textos_ensaio.py` (e `--textos` com o ORIGINAL para ver a recusa), `emular_soma_textos.py`, `tabela_arquivos_alterados.py`, `gerar_adendo_estado_d19.py`, `gerar_resultado.py`, `gerar_registro_mapa.py`.")
stamp = time.strftime("%Y%m%d_%H%M%S"); bak = ALVO + ".bak_%s_c1d19c" % stamp
assert not os.path.exists(bak)
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
tmp = ALVO + ".tmp_c1d19c"; open(tmp, "wb").write(s.encode("utf-8")); assert os.path.getsize(tmp) > 0
os.replace(tmp, ALVO); compile(open(ALVO, encoding="utf-8").read(), ALVO, "exec")
print("OK: %s %d B -> %d B (sha16 %s -> %s); backup %s" % (os.path.basename(ALVO), len(raw), os.path.getsize(ALVO), hashlib.sha256(raw).hexdigest()[:16], hashlib.sha256(open(ALVO, "rb").read()).hexdigest()[:16], os.path.basename(bak)))
