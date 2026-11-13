# -*- coding: utf-8 -*-
# [AO LADO, 12/11/2026 tarde, D174] a primeira frase do ARCO curta (o b_mudou da G1 a leva ao README); o item (iii) e a regra do teto ditos como a G1 os aplica
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411-posrito] REESCRITO para a v411 (o corpo da v410, com IALD2, AEscala, HMS/13 e os blocos README_FRENTE/README_O_QUE_SAI, fica no .bak): os sete textos da prosa da custodia sao os da v411 (o teste H0DN x BG1 aberto; nenhum modulo novo), e os textos que a abertura torna obrigatorios (NOTA_EN, os seis README_*, os onze ESTATUTO_*, mais README_H0DN_EN e X_TEXTO) vem de blocos_custodia_v411.py; as notas da cadeia (D133, D135) entram no fim.
"""textos_custodia_handoff_v411.py -- (gerencia c1, pelo claude-construtor-v411-posrito, 12/11/2026) o S6d do orquestrador da v411: ENCADEADO depois da chain 14, anexa ao HANDOFF_v411_CUSTODIA.md do Nos:
  (1) os sete marcadores da prosa da custodia (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT): sem eles a G1 usaria o molde factual, que diria que o painel do Teste da Unica
      Palavra «stays at the top» e que beta_TGL espera 5 sigma (a G1 PARA nesses casos: errata da custodia de 12/11);
  (2) a secao «README: o que fica evidente» (v411) e, sob marcadores, os textos que a abertura torna obrigatorios (blocos_custodia_v411.secao_handoff: a NOTA inteira, os seis do README, os onze do estatuto e
      os dois extras), MONTADOS do core selado e da formula (TOPO_RATIFICADO_v411.json:formula_curta, quando existir; senao a PROPOSTA da gerencia, dita);
  (3) as notas da cadeia: a contagem esperada de arquivos da pasta da cadeia, os contratos de registro fora da escada (D135), a excecao estreita da P18 (so' na cadeia), a pasta sem .tmp (D133).
Antes de anexar: cada texto passa na guarda de frases da v411 (guarda_frases_v411.violacoes), no portao do G1 (custodia_g1.textos.portao), nas regras de forma do ARCO e do COMMIT e, os da abertura, nas MESMAS
conferencias da custodia (custodia_g1.h0dn.conferir_bloco: F67, numeros, cabeca, sigma; regra do 4,44; forma de cada marcador); o acrescimo inteiro passa outra vez. Anexa com backup de BYTES, temporario, conferencia
de que cresceu; re-le pelo parser do G1 (custodia_g1.nos.ler_handoff) e exige cada corpo igual ao escrito; grava RECIBO_TEXTOS_CUSTODIA_HANDOFF_v411.json. Falha = rc 1 e NADA anexado.
Ensaio: V411_NOS_DIR (o Nos: le core, selo, diario e o HANDOFF e escreve SO' o HANDOFF), V411_PKG_DIR (onde estao ESPERADOS_v411.json e a revisao) e V411_RECIBO_DIR (onde vai o recibo); sem elas, os da casa.
Toda citacao « » e' fala do operador copiada do arquivo; frase da gerencia vai entre “ ”."""
import ast
import datetime
import hashlib
import json
import os
import re
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG_REAL = HERE.parent
CEN = Path(r"C:\IALD\Central de Patentes")
V = "v411"
sys.path.insert(0, str(CEN / "tools")); sys.path.insert(0, str(PKG_REAL)); sys.path.insert(0, str(HERE))
from custodia_g1 import textos as TX, nos as NOSMOD, h0dn as H0DN  # noqa: E402
import guarda_frases_v411 as GF  # noqa: E402
import delta_v411 as DL  # noqa: E402
import blocos_custodia_v411 as BC  # noqa: E402

MARCADORES_PROSA = tuple(TX.MARCADORES_OPCIONAIS)   # os sete da G1 (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT)
MARCADORES_ABERTURA = tuple(BC.MARCADORES_CUSTODIA) + tuple(BC.MARCADORES_EXTRAS)
SECAO_README = "**README: o que fica evidente (v411)**"
NOME_RECIBO = "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v411.json"
DEPOIS_DO_HANDOFF = ("pos_rito/" + NOME_RECIBO, "ORDEM_HANDOFF_CUSTODIA_v411.md", "orquestrador/RELATORIO_POS_TREINO_v411.md", "orquestrador/RELATORIO_POS_TREINO_v411.json")   # o que a cadeia ainda grava DEPOIS deste passo


def s16b(b):
    return hashlib.sha256(b).hexdigest()[:16]


def _nao_decide_en():
    """a lista EN do que o teste nao decide: o literal `_V411_NAO_DECIDE_EN` do quadro que vai embutido no um.py (quadro_v411.py da pasta da cadeia), lido por ast; nunca redigitado aqui."""
    arv = ast.parse((PKG_REAL / "quadro_v411.py").read_text(encoding="utf-8"))
    for no in arv.body:
        if isinstance(no, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_V411_NAO_DECIDE_EN" for t in no.targets):
            v = ast.literal_eval(no.value)
            assert isinstance(v, list) and all(isinstance(x, str) for x in v) and v
            return v
    raise ValueError("quadro_v411.py nao traz _V411_NAO_DECIDE_EN")


def compor(core, selo, esp, diario, rev, pkg):
    """os textos (lista de (ident, texto)), a secao do README e o relatorio; nada escrito. Levanta AssertionError/ValueError se um numero nao confere."""
    R = core[DL.FECHO_REGISTRO]
    assert R.get("all_verified") is True and R.get("opened_once") is True and (R.get("mechanics") or {}).get("passed") is True, "o registro %s nao selou (ou nao foi aberto)" % DL.FECHO_REGISTRO
    assert (R.get("mechanics") or {}).get("n_checks") == DL.N_CHECKS_FECHO, "o registro nao tem as %d checagens do DESENHO" % DL.N_CHECKS_FECHO
    vno = (esp.get("vereditos_novos_v411") or {}).get(DL.FECHO_REGISTRO)
    assert vno is None or vno == R["verdict"], "o veredito do registro != o de ESPERADOS_v411.json"
    pin = selo["sha256"]["um.py"][:16]
    assert selo.get("um_version") == V and pin == esp.get("candidato_sha16"), "o selo do Nos nao e' o da v411 ou o pino != o candidato de ESPERADOS"
    mc = NOSMOD.RE_CAB.search(diario[max(0, diario.find("**%s SELADA" % V) - 80):])
    assert mc and mc.group("v") == V and mc.group("pin") == pin, "o cabecalho «%s SELADA» do diario nao foi lido" % V
    esc_a, esc_b, k = int(mc.group("a")), int(mc.group("b")), mc.group("k")
    lad = core.get("external_ladder") or {}
    assert esc_b == lad.get("n_theorems_clean") == lad.get("n_theorems_expected"), "a escada do diario != a do core"
    assert k in ("nenhum", "0"), "a v411 nao tem modulo novo, e o diario diz %r" % k
    KH = core.get("kh_n1_cobertura_" + V) or {}; CU = core.get("cunhagens_" + V) or {}
    kc, kt = (KH.get("lido") or {}).get("constantes_cobertas"), (KH.get("lido") or {}).get("teoremas_cobertos")
    assert isinstance(kc, int) and isinstance(kt, int), "kh_n1_cobertura_%s sem constantes/teoremas cobertos" % V
    nfal = len(CU.get("verbatim") or {})
    assert nfal == DL.N_FALAS_V411, "cunhagens_%s traz %d falas, o DESENHO pede %d" % (V, nfal, DL.N_FALAS_V411)
    ctx = BC.contexto_do_core(core)
    B, rel = BC.montar(core, ctx)
    _tj, _fonte, Nn, _est, P, A = BC.pecas(core)   # (aditivo 4) os pedacos da frase de estado RATIFICADA (TOPO_RATIFICADO_v411.json), os mesmos dos textos da abertura
    en = dict(P["en"], retro=P["en"]["retro_minusc"], estatuto=P["en"]["estatuto_minusc"]); pt = dict(P["pt"], retro=P["pt"]["retro_minusc"], estatuto=P["pt"]["estatuto_minusc"])
    pa = dict(A["pt_ascii"], retro=A["pt_ascii"]["retro_minusc"], estatuto=A["pt_ascii"]["estatuto_minusc"])
    quem_credita_en = en["estatuto"].split(": ", 1)[1]   # “creditation belongs to the observer who rereads” (a redacao em ingles do arquivo ratificado; a palavra do operador, em portugues, e' a da fala citada por bytes)
    nd_en = _nao_decide_en()
    rev_en = " The independent review of the package (Sonnet, another model family) approved this candidate before the seal." if rev else " The independent review of the package (Sonnet, D69) is a distinct act and is not claimed here."
    rev_c = " Revisao de terceiro (Sonnet) aprovada." if rev else " A revisao de terceiro (Sonnet, D69) e ato distinto."
    TEXTOS = [
        ("TITULO_EN", DL.TITULO_SECAO_EN),
        ("ENTROU_EN", "%s: no new kernel module (the kernel of v410, byte for byte; ladder %d -> %d, nothing outside the trio); one registry with function, `%s` (%d checks, all verified), which recomputes in the rite, "
                      "from embedded bytes pinned by sha256, the result of the one opening of the pre-registered test: %s: %s; %s; %s; %s; `cunhagens_%s`: %d inscriptions by sha256; kh_n1 %d constants / %d theorems; "
                      "certified by the sha256 the program reads of itself (%s)." % (DL.TITULO_SECAO_EN, esc_a, esc_b, DL.FECHO_REGISTRO, DL.N_CHECKS_FECHO, en["abertura"], en["dois_z"], en["cefeidas"], en["retro"],
                                                                                      en["estatuto"], V, nfal, kc, kt, pin)),
        ("KERNEL_LEITURA_EN", "the kernel proves the terms (kernel validity, not creditation) and this version adds none: the ladder stays %d/%d and Python proves no theorem. The registry `%s` confers, in each rite, the "
                              "arithmetic of the opening: the pinned code of the pre-registration runs from the embedded bytes and its result is compared with the result recorded at the opening (numbers at 1e-9; branch, "
                              "outcome and head by equality of text), and the order of the acts is read from the receipts (the public push of the pre-registration before the opening). The head of the verdict (09/11) and the "
                              "amendment (11/11) are the operator’s INPUT; the published error model is the collaboration’s." % (esc_b, esc_b, DL.FECHO_REGISTRO)),
        ("ABERTOS_EN", "Stays open what the test does not decide: %s (%s); %s; the twelve candidate stones of 11/11 and the stone of the observer and of the scale wait for the operator’s names (a later version)."
                       % ("; ".join(nd_en), quem_credita_en, en["rever"])),
        ("ARCO_EN", "The custody of v411 (complete round): the decisive test, H0DN × BG1, opened once. It is the local/background Hubble ratio, opened on %s after the public pre-registration and recomputed in the rite "
                    "from embedded bytes (registry %s, %d checks). %s: %s; %s; %s; %s. No new kernel module (ladder %d/%d); the gate does not move." % (Nn["data_en"], DL.FECHO_REGISTRO, DL.N_CHECKS_FECHO, _cap(en["abertura"]),
                                                                                                                                                     en["dois_z"], en["cefeidas"], en["retro"], en["estatuto_curto"], esc_b, esc_b)),
        ("ARCO_PT", "A custódia da v411 (rodada completa): o teste decisivo, H0DN × BG1, aberto uma vez. É a razão de Hubble local/fundo, aberta em %s depois do pré-registro público e recalculada no rito a partir "
                    "dos bytes embutidos (registro %s, %d checagens). %s: %s; %s; %s; %s. Nenhum módulo novo no kernel (escada %d/%d); o gate não se move." % (Nn["data_pt"], DL.FECHO_REGISTRO, DL.N_CHECKS_FECHO, _cap(pt["abertura"]),
                                                                                                                                              pt["dois_z"], pt["cefeidas"], pt["retro"], pt["estatuto_curto"], esc_b, esc_b)),
        ("COMMIT", "v411: o teste decisivo H0DN x BG1, aberto uma vez em %s depois do pre-registro publico e recalculado no rito dos bytes embutidos (registro %s, %d checagens): %s: %s; %s; %s; %s. Nenhum modulo novo "
                   "no kernel (escada %d/%d); o gate nao se move.%s" % (Nn["data_pt"], DL.FECHO_REGISTRO, DL.N_CHECKS_FECHO, pa["abertura"], pa["dois_z"], pa["cefeidas"], pa["retro"], pa["estatuto"], esc_b, esc_b, rev_c)),
    ]
    TEXTOS[1] = (TEXTOS[1][0], TEXTOS[1][1] + rev_en)
    readme = (SECAO_README + " (DESENHO_v411 5.3; a ordem do operador de 12/11/2026, D170 [INPUT]: o resultado no README e no topo do resumo do artigo). O que muda no README do espelho vem SÓ dos marcadores abaixo, "
              "conferidos pela G1 contra o registro `%s`: (i) o painel do topo com o resultado, EN e PT (`README_PAINEL_H0DN`), logo depois da linha do selo, e a linha de registro da Fase 9 V2 logo depois dele "
              "(`README_FASE9_V2`; o painel inteiro dela e a frase do autor de 02/11 descem verbatim para `%s`); (ii) a linha do topo que dizia que β na natureza a 5σ é o passo aberto (`README_PRIMORDIAL_5SIGMA`) e a "
              "frase do estado (`README_STATUS_5SIGMA`); (iii) as duas linhas do H0DN na parte do Clay (`README_H0DN`, PT, e `README_H0DN_EN`, EN), apontadores para o painel e para a leitura inteira; (iv) as duas linhas da tabela dos "
              "ritos (`README_RITOS`); (v) o bloco do Clay (`p_igual_np.md`) fica como está, com a faixa de versões `v408–%s`. Os geradores do espelho recebem os onze `ESTATUTO_*`, cada um no lugar do trecho do 5σ "
              "da sua chave. O README inteiro fica em até 40.960 B, medido pelo renderizador da custódia; se não couber, a cadeia PARA (nada é cortado em silêncio)." % (DL.FECHO_REGISTRO, BC.REGISTRO_FASE9_V2_MD, V))
    return TEXTOS, readme, B, rel, {"pin": pin, "escada": [esc_a, esc_b], "kh": [kc, kt], "falas": nfal, "n_checks": DL.N_CHECKS_FECHO}


def _cap(s):
    return BC._cap(s)


def notas_da_cadeia(pkg, reg):
    """as notas que o handoff leva sobre a pasta da cadeia (D133, D135, decisao (c) da gerencia): .tmp removidos antes, a contagem esperada, os contratos fora da escada, a excecao da P18."""
    tmp = sorted(p for p in Path(pkg).rglob("*.tmp") if p.is_file())
    for p in tmp:
        p.unlink()
    assert not [p for p in Path(pkg).rglob("*.tmp") if p.is_file()], "sobrou .tmp na pasta da cadeia"
    agora = sorted(str(p.relative_to(pkg)).replace(os.sep, "/") for p in Path(pkg).rglob("*") if p.is_file())
    vem = [x for x in DEPOIS_DO_HANDOFF if x not in agora]
    contr = sorted(set(DL.CONTRATOS_DE_REGISTRO_FORA_DA_ESCADA) | set(reg.get("contratos_de_registro_fora_da_escada") or []))
    texto = ("**Notas da cadeia para a custódia (v411; D133, D135, decisão (c) da gerência de 12/11):** (1) a pasta `work\\cadeia_de_selo\\%s` não tem `.tmp` (%d removido(s) neste passo, antes do handoff%s); "
             "(2) a contagem esperada de arquivos da pasta (recursiva), medida neste passo: %d, mais %d que a cadeia grava depois deste passo (%s), %d no total ao fim do orquestrador; (3) contratos de REGISTRO novos, fora "
             "da escada de teoremas: %s (não são contrato com `expected_ladder`); (4) a exceção estreita da P18 para a cabeça EXATA do teste (`_v411_p18_sem_cabeca`, uma função só, usada por todos os conferidores) fica "
             "só na cadeia: a G1 não tem a regra R1 que a exige (a custódia mediu), e nenhum texto deste handoff precisa dela."
             % (V, len(tmp), (": " + ", ".join(str(p.relative_to(pkg)) for p in tmp)) if tmp else "", len(agora), len(vem), ", ".join("`%s`" % x for x in vem) or "nenhum", len(agora) + len(vem),
                ", ".join("`%s`" % c for c in contr)))
    return texto, {"tmp_removidos": [str(p) for p in tmp], "arquivos_agora": len(agora), "depois_do_handoff": vem, "esperado_ao_fim": len(agora) + len(vem), "contratos_fora_da_escada": contr}


def guardas_dos_textos(textos, conhecidos, core=None):
    """as guardas de cada texto: a guarda de frases da v411, o portao do G1, a forma (ARCO/COMMIT, D59, D65, o 4,44 so' com a regra dele) e, sobre os textos da abertura, as conferencias da custodia (blocos_custodia_v411.conferir)."""
    out, falhas = {}, []
    abert = {i: t for i, t in textos if i in MARCADORES_ABERTURA}
    conf = BC.conferir(abert, core, conhecidos=conhecidos) if (abert and core is not None) else {}
    for ident, t in textos:
        v1 = [list(x) for x in GF.violacoes(t)]
        v2 = TX.portao(t, conhecidos, rotulo=ident)
        v3 = []
        if ident in ("ARCO_EN", "ARCO_PT") and ("'" in t or "<" in t or "\\" in t or "\n" in t):
            v3.append("%s: aspa simples, «<», barra invertida ou quebra de linha" % ident)
        if ident == "COMMIT" and any(ord(ch) > 127 for ch in t):
            v3.append("COMMIT: caractere fora do ASCII")
        if ident not in ("NOTA_EN", "README_FASE9_V2") and re.search(r"(?<![0-9,.])4[,.]44(?![0-9])", t):
            v3.append("%s: traz o 4,44 fora da NOTA e da linha da Fase 9 V2 (a regra do 4,44)" % ident)
        if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", t) or (re.search(r"(?i)kimi", t) and not re.search(r"(?i)h0dn", t)):
            v3.append("%s: D59: traz o que fica fora dos textos" % ident)
        if any(x.lower() in t.lower() for x in DL.FORA_D65):
            v3.append("%s: D65: traz o que a fala do nome do algoritmo deixa fora" % ident)
        if ident in ("ENTROU_EN", "ARCO_EN", "ARCO_PT", "COMMIT") or ident in MARCADORES_ABERTURA:
            v3 += ["%s: %s" % (ident, x) for x in H0DN.f67(t)] if ident not in conf else []
            if core is not None and ident not in conf:   # a F67 estrita (o numero do primario sempre com as quatro obrigacoes) tambem na prosa da custodia
                v3 += ["%s: %s" % (ident, x) for x in BC._f67_estrita(t, H0DN.valores(core[DL.FECHO_REGISTRO]))]
        v4 = list(conf.get(ident, []))
        out[ident] = {"guarda_frases_v411": v1, "portao_g1": v2, "forma": v3, "custodia_h0dn": v4, "n_bytes": len(t.encode("utf-8"))}
        if v1 or v2 or v3 or v4:
            falhas.append((ident, v1[:3], v2[:3], v3[:3], v4[:3]))
    return out, falhas


def main(nos=None, pkg=None, recibo_dir=None):
    nos = Path(nos or os.environ.get("V411_NOS_DIR") or r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
    pkg = Path(pkg or os.environ.get("V411_PKG_DIR") or PKG_REAL)
    recibo_dir = Path(recibo_dir or os.environ.get("V411_RECIBO_DIR") or HERE)
    assert recibo_dir.is_dir() or not recibo_dir.exists(), "o lugar do recibo nao e' pasta"
    recibo_dir.mkdir(parents=True, exist_ok=True)   # (antes de tocar o handoff: o recibo nunca pode faltar depois do acrescimo)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    core = json.loads((nos / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
    selo = json.loads((nos / "um_absoluto_selo.json").read_text(encoding="utf-8"))
    assert selo["sha256"]["um.py"][:16] == s16b((nos / "um.py").read_bytes()), "o um.py do Nos nao e' o do selo"
    esp = json.loads((pkg / "ESPERADOS_v411.json").read_text(encoding="utf-8"))
    diario = (nos / "MEMORIA_DA_LINHAGEM.md").read_text(encoding="utf-8", errors="replace")
    revp = pkg / "revisao_terceiro" / "REVISAO_TERCEIRO_v411.json"
    rev = None
    if revp.exists():
        rev = json.loads(revp.read_text(encoding="utf-8"))
        assert rev.get("aprovada") is True and rev.get("candidato_sha16") == selo["sha256"]["um.py"][:16], "a revisao de terceiro existe mas nao aprova este pino: PARO"
    TEXTOS, readme, B, rel, nums = compor(core, selo, esp, diario, rev, pkg)
    notas, notas_info = notas_da_cadeia(pkg, core[DL.FECHO_REGISTRO])
    hpath = nos / ("HANDOFF_%s_CUSTODIA.md" % V)
    hb = hpath.read_bytes(); ht = hb.decode("utf-8")
    assert b"\r\n" not in hb, "o handoff e' CRLF: ajustar o acrescimo"
    todos = list(TEXTOS) + [(k, B[k]) for k in MARCADORES_ABERTURA]
    for ident, _ in todos:
        assert ("INICIO_%s_%s" % (ident, V)) not in ht, "o marcador %s ja existe no handoff" % ident
    conh = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", ht)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", ht)) | {nums["pin"], rel["fonte"]["sha256"]}   # (o sha256 do arquivo ratificado, lido nesta rodada)
    guardas, falhas = guardas_dos_textos(todos + [("README_EVIDENTE", readme), ("NOTAS_DA_CADEIA", notas)], conh, core)
    if falhas:
        for f in falhas:
            print("REPROVADO:", f)
        return 1
    cab = ("\n\n**Textos da custódia (gerência c1, 12/11/2026; substituem o molde factual da G1; números lidos do core selado, do selo e do diário por `pos_rito\\textos_custodia_handoff_%s.py` e conferidos antes de "
           "anexar: a guarda de frases da v411, o portão da G1 e, nos textos da abertura do H0DN × BG1, as mesmas conferências da custódia; nenhum módulo novo; validade no kernel não é creditação):**\n" % V)
    marc = lambda i, t: "\n<!-- INICIO_%s_%s -->\n%s\n<!-- FIM_%s_%s -->\n" % (i, V, t, i, V)
    acresc = cab + "".join(marc(i, t) for i, t in TEXTOS) + "\n" + readme + "\n\n" + BC.secao_handoff(B, rel, V) + "\n" + notas + "\n"
    vac = [list(x) for x in GF.violacoes(acresc)] + TX.portao(acresc, conh, rotulo="acrescimo")
    assert not vac, "o acrescimo inteiro nao passa nas guardas: %r" % (vac[:3],)
    novo = hb.rstrip(b"\n") + acresc.encode("utf-8")
    assert novo.startswith(hb.rstrip(b"\n")) and len(novo) > len(hb) + 3000, "o acrescimo nao cresceu como esperado"
    # o recibo e' MONTADO antes de tocar o handoff (um erro aqui nao deixa handoff sem recibo); so' o sha16 de depois e a releitura entram depois
    rec = {"quando": datetime.datetime.now().isoformat(timespec="seconds"), "quem": "gerencia c1 (orquestrador da v411, S6d)", "handoff": str(hpath), "sha16_antes": s16b(hb), "sha16_depois": s16b(novo),
           "numeros_lidos": nums, "revisao_terceiro": ({"aprovada": rev["aprovada"], "candidato_sha16": rev["candidato_sha16"]} if rev else "ausente: os textos dizem que e' ato distinto"),
           "formula": {"origem": rel["formula_origem"], "proposta": rel["proposta"], "ratificada": rel["ratificada"], "fonte": rel["fonte"], "p2_rotulo": rel["p2_rotulo"], "p2_registro_selado": rel["p2_registro_selado"],
                       "painel_inteiro": rel["painel_inteiro"], "decisao_d174": rel["decisao_d174"]},
           "marcadores": [i for i, _ in todos], "textos": dict(todos), "readme_evidente": readme, "notas_da_cadeia": notas, "notas_info": notas_info, "guardas": guardas,
           "estatuto": "REAL (numeros lidos do core selado, do selo e do diario); o texto e' o RATIFICADO pelo operador (TOPO_RATIFICADO_v411.json), cortado em oracoes inteiras para cada lugar; os conectivos sao da gerencia c1, em nome proprio; NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move"}
    json.dumps(rec, ensure_ascii=False)
    bak = hpath.with_name(hpath.name + ".bak_" + ts); open(bak, "xb").write(hb); assert bak.read_bytes() == hb
    tmp = hpath.with_name(hpath.name + ".tmp_" + ts); open(tmp, "xb").write(novo); assert tmp.stat().st_size == len(novo)
    os.replace(tmp, hpath); assert hpath.read_bytes() == novo
    print("handoff: %d -> %d bytes; sha16 %s -> %s; backup %s" % (len(hb), len(novo), s16b(hb), s16b(novo), bak.name))
    h = NOSMOD.ler_handoff(types.SimpleNamespace(NOS=nos, CEN=CEN), V)
    faltam = [i for i, _ in todos if ("%s_%s" % (i, V)) not in h.corpos]
    assert h is not None and not faltam and not h.problemas, ("o parser do G1 nao leu os corpos", faltam, h.problemas)
    for i, t in todos:
        assert h.corpos["%s_%s" % (i, V)].strip("\n") == t, "o corpo lido difere do escrito: " + i
    rec.update(backup=str(bak), parser_g1={"corpos": sorted(h.corpos), "problemas": h.problemas})
    rp = recibo_dir / NOME_RECIBO
    rb = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
    open(str(rp) + ".tmp", "wb").write(rb); os.replace(str(rp) + ".tmp", rp)
    print("parser do G1: %d corpos lidos, 0 problemas; recibo %s" % (len(todos), rp))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
