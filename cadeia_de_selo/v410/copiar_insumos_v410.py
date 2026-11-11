# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] as fontes da v410: a pedra IALD2 (embutida e fonte normalizada), a saida do lean, a candidata e o registro anterior, o BUNDLE, o KH; as nove falas de 06/11 (de uma, o trecho que fica e o arquivo inteiro so' por sha256: D65); congela a lista das falas
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] as ONZE falas (06, 07 e 09/11; de duas so' o trecho); o congelado de 06/11 e os insumos derivados da pedra antiga foram a backup (.bak_20261109_114113_secao6) para serem regerados da pedra com a secao 6
"""copiar_insumos_v410.py -- copia de BYTES, para a pasta DURAVEL v410\\insumos, das fontes que os registros da v410 pinam por sha256: a pedra normalizada EMBUTIDA (v410\\pedra -> insumos\\IALD2_embutida.lean), a fonte normalizada com #print axioms
(ja' em insumos\\IALD2.lean), a saida do lean, a candidata de origem (work\\pedras_candidatas_06nov\\IALD2.lean) e a LeitorDoCodigoR1 (registro anterior), o BUNDLE_v410.json, a medida do Audit (KH_N1_v410.json) e as falas do operador de 06, 07 e 09/11/2026
(na da D65 e na ordem de 09/11, so' o TRECHO QUE FICA e' copiado, com nome neutro, porque o nome de origem resume a parte que fica fora; o arquivo inteiro entra so' por sha256 e NAO e' copiado para insumos\\, que a custodia publica).
CONGELA a lista das falas (VERBATIM_CONGELADO_v410.json; lista de trabalho da cadeia, nao pinada como fonte: traz os caminhos de origem). Grava MANIFESTO_INSUMOS_v410.json (sha256, origem). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta.
Roda DEPOIS do pos_build_kernel_v410.py (que gera kernel\\KH_N1_v410.json). Molde: copiar_insumos_v409.py.
uso: python -I -B -X utf8 copiar_insumos_v410.py"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
import registros_hms13_v410 as RF  # noqa: E402   (D80: a excecao declarada ao veto da pasta do Kimi: os seis artefatos documentais HMS/13, por sha256)
sha = lambda b: hashlib.sha256(b).hexdigest()
# a lista das falas: congelada na PRIMEIRA execucao (as quinze do DESENHO_v410 §3 e dos AO LADO de 06 e 09/11; os congelados de 06/11 (nove) e das 11:41 de 09/11 (onze) foram a backup quando a gerencia refez o DESENHO); depois, lida (fala que chegar depois fica fora, dita em fora_do_desenho)
CONG = os.path.join(HERE, "VERBATIM_CONGELADO_v410.json")
if not os.path.exists(CONG):
    arqs = list(DL.VERBATIM_ORIGEM_V410)
    reg = [{"arquivo": p_, "sha256": sha(open(p_, "rb").read()), "bytes": os.path.getsize(p_), "autor": "operador"} for p_ in arqs]
    c = {"contrato": "VERBATIM_CONGELADO_v410", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "n": len(arqs), "arquivos": arqs, "registro": reg, "fora_do_desenho": dict(DL.VERBATIM_FORA_DO_DESENHO_V410),
         "nota": "as %d falas (06 a 10/11/2026) que esta versao embute (as oito do DESENHO_v410 §3, a do AO LADO de 06/11, as duas do AO LADO da retomada de 09/11, as duas do AO LADO das decisoes de 09/11, a da E30 e a da D76; as da escala, do Clay e das ratificacoes de 09/11; as de 10/11 dos ADENDOS 2, 3, 5, 6 e 7, D94, D96, D100, D101, D108, D109, D113 e D116 a D123); de %d, so' o trecho e' embutido e citado (D65; a ordem de 09/11; as tres copias de 08/11; a leitura do 5 sigma; a ratificacao dos nomes da secao 7, D117); lista de trabalho da cadeia (NAO pinada como fonte: traz os caminhos de origem)" % (len(arqs), len(DL.VERBATIM_SO_O_TRECHO))}
    b = json.dumps(c, ensure_ascii=False, indent=1).encode("utf-8")
    open(CONG + ".tmp", "wb").write(b); assert os.path.getsize(CONG + ".tmp") == len(b); os.replace(CONG + ".tmp", CONG)
    print("VERBATIM_CONGELADO_v410.json: %d falas congeladas" % len(arqs))
import importlib  # noqa: E402
DL = importlib.reload(DL)                                       # (relido com a lista congelada)
import registros_v410 as RG  # noqa: E402
INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens")
os.makedirs(CUN, exist_ok=True)
man = {}


def grava(destino, b, origem):
    if os.path.exists(destino):
        assert open(destino, "rb").read() == b, ("o insumo ja existe e DIFERE da origem: nao sobrescrevo", destino)
    else:
        open(destino + ".tmp", "wb").write(b); assert os.path.getsize(destino + ".tmp") == len(b); os.replace(destino + ".tmp", destino)
    assert open(destino, "rb").read() == b
    return {"origem": origem, "sha256": sha(b), "bytes": len(b)}


def copia(destino, origem):
    return grava(destino, open(origem, "rb").read(), origem)


# a pedra que carrega a ancora principal: a fonte tem o sha16 do recibo dos nomes; a copia v410\pedra == o bundle == o sandbox
tf = DL.testemunha_fonte()
for p in DL.PEDRAS_V410:
    b = open(p["src"], "rb").read()
    assert sha(b) == DL.BUNDLE_POR_REL[p["rel"]]["sha256"] == sha(open(os.path.join(DL.SANDBOX, *p["rel"].split("/")), "rb").read()), ("a pedra em v410\\pedra difere do bundle ou do sandbox", p["name"])
    assert sha(open(p["origem"], "rb").read()) == p["sha256_origem"], ("a fonte normalizada em insumos\\ difere do que o bundle pinou", p["name"])
_VED = os.path.normcase(os.path.normpath(DL.H0DN_PASTA_VEDADA))   # (AVISO da gerencia, 09/11) a entrega do Kimi NAO e' copiada nem pinada: nenhuma origem cai sob kimi\ -- EXCECAO D80 (ordem do operador, ratificada por sha256): SOMENTE os seis artefatos documentais HMS/13 (RF.ORIGENS_HMS13), por sha256 conferido no HANDOFF e na ORDEM do Kimi imediatamente antes (RF.pinos_hms13)
_PIN_HMS13, _, _ = RF.pinos_hms13(); _EXC = {os.path.normcase(os.path.normpath(o_)): n_ for n_, o_ in RF.ORIGENS_HMS13}
assert len(_EXC) == 6 and all(n_.startswith("hms13_") for n_ in _EXC.values()) and all(p_.startswith(_VED) for p_ in _EXC), "a excecao D80 nao e' exatamente os seis artefatos documentais sob a pasta do Kimi"
for nome, orig in RG.ORIGENS:
    _o = os.path.normcase(os.path.normpath(orig))
    if _o.startswith(_VED):
        assert _EXC.get(_o) == nome, ("VEDADO: origem sob a entrega do Kimi fora da excecao D80 (a v410 pre-registra e nao abre)", orig)
        _pn = [k_ for k_, v_ in _PIN_HMS13.items() if os.path.normcase(os.path.normpath(v_["path"])) == _o]; assert len(_pn) == 1, ("D80: artefato HMS/13 sem pino do HANDOFF/ORDEM", orig)
        assert sha(open(orig, "rb").read()) == _PIN_HMS13[_pn[0]]["sha256"], ("D80 (fail-closed): o artefato HMS/13 em disco nao tem o sha256 do HANDOFF/ORDEM", orig)
    man[nome] = copia(os.path.join(INS, nome), orig)
man["_pasta_vedada_nao_copiada"] = {"origem": DL.H0DN_PASTA_VEDADA, "sha256": None, "bytes": 0, "nota": "a entrega do Kimi (vetor observado, covariancia) nao entra na v410: nenhuma origem sob esta pasta fora da excecao D80 (assert acima)", "excecao_d80": sorted(_EXC.values())}
man["_pasta_vedada_excecoes_d80"] = {"origem": DL.HMS13_DIR, "sha256": None, "bytes": 0, "nota": "D80: os seis artefatos documentais HMS/13 (mapa, manifesto, validacao, levantamento, HANDOFF, ORDEM) copiados como insumos\\hms13_* por sha256 conferido no HANDOFF e na ORDEM; nada mais da pasta", "excecoes": sorted(_EXC.values()), "pinos": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"]} for k_, v_ in _PIN_HMS13.items()}}
assert man["IALD2.lean"]["sha256"][:16] == DL.TESTEMUNHA["sha16_da_ordem"] == tf["sha256_origem"][:16]
for p in DL.PEDRAS_V410:
    assert man["%s_embutida.lean" % p["name"]]["sha256"] == DL.BUNDLE_POR_REL[p["rel"]]["sha256"]
for v in DL.verbatins410(CUN):   # os prefixos de sha256 da ORDEM da gerencia (as falas-chave) sao conferidos dentro de DL.verbatins410
    if v.get("so_o_trecho"):
        assert sha(open(v["fonte_original"], "rb").read()) == v["sha256_arquivo_inteiro"]
        man["cunhagens/" + os.path.basename(v["arquivo"])] = grava(v["arquivo"], v["text"].encode("utf-8"), "%s (sha256 do arquivo inteiro %s; %s)" % (v["nome_publico"], v["sha256_arquivo_inteiro"], v["so_o_trecho"]))
    else:
        man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
# D65: nada copiado para insumos\ traz a parte que fica fora (nem o nome do arquivo de origem que a resume)
for n_ in os.listdir(CUN):
    assert "solucao_definitiva" not in n_.lower(), ("D65: nome de arquivo em insumos\\cunhagens resume a parte que fica fora", n_)
    if n_.startswith(tuple(v_[:16] for v_ in [DL.VERBATIM_PREFIXOS_DA_ORDEM_V410[DL.N_SOLUCAO]])):
        assert not any(x_.lower() in open(os.path.join(CUN, n_), encoding="utf-8").read().lower() for x_ in DL.FORA_D65), ("D65: o trecho copiado traz o que fica fora", n_)
b_man = json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8")
open(os.path.join(HERE, "MANIFESTO_INSUMOS_v410.json.tmp"), "wb").write(b_man)
os.replace(os.path.join(HERE, "MANIFESTO_INSUMOS_v410.json.tmp"), os.path.join(HERE, "MANIFESTO_INSUMOS_v410.json"))
print("insumos copiados/conferidos:", len(man), "| total", sum(v["bytes"] for v in man.values()), "B | IALD2 (fonte):", tf["sha256_origem"][:16])
