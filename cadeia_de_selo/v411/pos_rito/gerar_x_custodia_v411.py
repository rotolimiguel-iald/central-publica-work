# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-sonnet-posrito-M-v411] REESCRITO: o texto CURTO da v411 no X diz o teste H0DN x BG1 com os DOIS numeros no mesmo texto (o primario contra o nulo e as Cefeidas livres), sob o modelo publicado, retrodicao e nao cego, validade nao creditacao; numeros LIDOS do core (consts_mapa_x_v411); montar_post() e' funcao pura (o teste a roda sem candidato)
"""gerar_x_custodia_v411.py -- RASCUNHO do texto CURTO da versao v411 no X (molde: o post da v410, escrito pela gerencia; este e' bem menor: o resultado do teste da razao de Hubble, o que ele nao decide, o kernel e o gate).
LE o Nos (selo e core) e escreve SO' pos_rito\\CUSTODIA_v411_RASCUNHO.txt; NAO escreve no tunel nem publica: copiar para X_VITRINE\\CUSTODIA_v411.txt e publicar e' ato da gerencia/do orquestrador (ORDEM de vitrine).
Todo numero e todo hash vem do selo e do core lidos agora (nada digitado); o texto passa na guarda P18, na guarda das frases da v411 (inclui a F67: os DOIS numeros no mesmo bloco, com sob o modelo de erros publicado, as Cefeidas livres com o numero,
validade nao creditacao, retrodicao e nao cego; EN: under the published error model, free Cepheids, validity not creditation, retrodiction, not blind), na regra da ordem (nao traz o 4,44), na D59 e na D65.
A funcao montar_post(core, selo, ESP, hoje) e' PURA (sem leitura de arquivo): devolve o texto ou levanta AssertionError (selo de outra versao; registro que nao selou; numero que falta no texto).
uso: python -I -B -X utf8 gerar_x_custodia_v411.py [--nos <pasta>] [--esp <ESPERADOS.json>] [--saida <arquivo>]   (padrao: o Nos real; antes do rito o selo e' o da v410 e o script RECUSA: o post so' nasce da v411 selada)"""
import datetime, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
from guarda_p18_v411 import violacoes  # noqa: E402
import delta_v411 as DL  # noqa: E402
import consts_mapa_x_v411 as C  # noqa: E402
NOS_REAL = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
LINK = "https://github.com/rotolimiguel-iald/the_boundary"


def montar_post(core, selo, ESP, hoje):
    """O texto curto do X, montado do core e do selo (FAIL-CLOSED)."""
    assert selo.get("um_version") == "v411" and str((selo.get("sha256") or {}).get("um.py", ""))[:16] == ESP["candidato_sha16"], "o selo do Nos nao e' o da v411 candidata: o post so' nasce da v411 selada"
    hd = core.get(DL.FECHO_REGISTRO) or {}
    F = C.fatos_h0dn(hd)
    assert hd.get("verdict") == (ESP.get("vereditos_novos_v411") or {}).get(DL.FECHO_REGISTRO), "o veredito do registro h0dn_bg1_v411 != o de ESPERADOS"
    for k_ in (DL.FECHO_REGISTRO, DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO) + tuple(DL.REGISTROS_FUNCAO_V410):
        assert (core.get(k_) or {}).get("all_verified") is True, "um registro da v411 (ou da v410, recriado) nao selou: o post nao diz isto (%s)" % k_
    el = core.get("external_ladder") or {}
    assert el.get("n_theorems_clean") == el.get("n_theorems_expected") == ESP["escada_v410_e_v411"][0] == ESP["escada_v410_e_v411"][1], "a escada nao e' a da v410 (a v411 nao tem modulo novo)"
    n_decl = len((core.get("kernel_formalization") or {}).get("axiom_report") or [])
    assert n_decl > 0, "o relatorio de axiomas do core esta' vazio"
    assert (hd.get("values") or {}).get("gate_verdict") == selo.get("qg_closure_verdict"), "o gate lido pelo registro != o do selo"
    a_ = F["atos"]; sha = selo["sha256"]["um.py"]
    nd = "; ".join(F["nao_decide"])
    r1, r2 = DL.RESSALVAS_ROTULOS_PT[0], DL.RESSALVAS_ROTULOS_PT[1]
    txt = f"""TGL · a v411 do programa terminal, custodiada em {hoje}

H0DN × BG1, recalculado a cada rito dos bytes embutidos e conferido contra o resultado da abertura: {C.moldura_pt(F)}. O teste não decide: {nd}.

O pré-registro era público antes da abertura (commit {a_['commit_do_pre_registro'][:12]}, push {a_['push_do_pre_registro_utc']}; abertura às {a_['inicio_da_abertura_utc']}; resultado no commit {a_['commit_do_resultado'][:12]}, push {a_['push_do_resultado_utc']}). As sete ressalvas estão no registro h0dn_bg1_v411; as duas primeiras: {r1}; {r2}.

Kernel: nenhum módulo novo (o da v410); escada {el['n_theorems_clean']}/{el['n_theorems_expected']}, {format(n_decl, ',').replace(',', '.')} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry; nenhuma chave antiga muda. P = nP segue como na v410: {DL.D10.FRASE_QUALIFICADOR_PT} (validade no kernel, não creditação). O sha256 do programa:
{sha}

EN · H0DN × BG1, recomputed at every rite from the embedded bytes and checked against the opening result: {C.moldura_en(F)}.

O código e o selo: {LINK}

O número corrige a frase, sempre. — IALD
"""
    # o texto TEM de trazer os dois numeros e os obrigatorios (a F67 le por bloco; aqui, o texto inteiro)
    for x_ in (F["zn_pt"], F["zk_pt"], F["cn_pt"], F["zn_en"], F["cn_en"], DL.OBRIG_MODELO_PT, DL.OBRIG_MODELO_EN, DL.OBRIG_VALIDADE_PT, DL.OBRIG_VALIDADE_EN, DL.OBRIG_RETRO_PT, DL.OBRIG_RETRO_EN, DL.OBRIG_NAO_CEGO_PT, DL.OBRIG_NAO_CEGO_EN, DL.OBRIG_CEFEIDAS_PT, DL.OBRIG_CEFEIDAS_EN):
        assert x_ in txt, "o post nao traz %r" % x_
    return txt


def conferir(txt_):
    """As guardas do post (a mesma funcao serve ao teste sem candidato): devolve a lista de problemas (vazia = passa)."""
    p_ = [("P18", x_) for x_ in violacoes(txt_)]
    import guarda_frases_v411 as GF  # noqa: E402
    p_ += [("guarda_frases_v411", x_) for x_ in GF.violacoes(txt_)]
    if "4,44" in txt_ or "z_disc" in txt_:
        p_.append(("regra_da_ordem", "o post nao traz o 4,44 (a regra da ordem e' do quadro)"))
    if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", txt_) or (re.search(r"(?i)kimi", txt_) and not re.search(r"(?i)h0dn", txt_)):   # (D59 com a excecao da D72/D77: o nome do executor so' em texto que trata do H0DN)
        p_.append(("D59", "o post traz o que fica fora dos textos"))
    p_ += [("D65", x_) for x_ in DL.FORA_D65 if x_.lower() in txt_.lower()]
    if any(t_ in txt_ for t_ in DL.TOKENS_PROIBIDOS_V411):
        p_.append(("token_proibido", "o post traz um token de veredito proibido"))
    return p_


def main(argv):
    nos = argv[argv.index("--nos") + 1] if "--nos" in argv else NOS_REAL
    esp_p = argv[argv.index("--esp") + 1] if "--esp" in argv else os.path.join(PK, "ESPERADOS_v411.json")
    out = argv[argv.index("--saida") + 1] if "--saida" in argv else os.path.join(HERE, "CUSTODIA_v411_RASCUNHO.txt")
    rj = lambda p: json.load(open(p, encoding="utf-8"))
    selo = rj(os.path.join(nos, "um_absoluto_selo.json")); core = rj(os.path.join(nos, "um_absoluto.json"))["core"]; ESP = rj(esp_p)
    if selo.get("um_version") != "v411" or str((selo.get("sha256") or {}).get("um.py", ""))[:16] != ESP["candidato_sha16"]:
        print("RECUSO: o selo do Nos nao e' o da v411 candidata (um_version %r): o post so' nasce da v411 selada" % selo.get("um_version")); return 2
    txt = montar_post(core, selo, ESP, datetime.datetime.now().strftime("%d/%m/%Y"))
    pr = conferir(txt)
    assert not pr, ("o post nao passou nas guardas", pr[:3])
    open(out, "w", encoding="utf-8", newline="\n").write(txt)
    print("rascunho do post:", out, len(txt.encode("utf-8")), "B (NAO publicado; copiar para X_VITRINE\\CUSTODIA_v411.txt e' ato da gerencia)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
