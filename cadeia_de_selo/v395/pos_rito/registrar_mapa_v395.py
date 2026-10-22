# -*- coding: utf-8 -*-
"""registrar_mapa_v395.py -- MONTA (nao registra) o registro da v395 no mapa de rotas e imprime o comando (molde: registrar_mapa_v394.py). Rodar DEPOIS do fechar (handoff gravado).
A v395 traz UMA rota nova, umpy.v395.psibit_na_fractalizacao_do_um (o modulo de kernel Psibit, o registro psibit_v395 chamado na fractalizacao do Um e as quatro falas de 21/10), mais DUAS ANOTACOES nas rotas que esperavam
por ela (a pedra candidata, kernel.psibit_v395_candidata_21out, e a pedra irma da v394, kernel.criterio_binario_de_parada.ponto_fixo_v394_d19), cada afirmacao testada contra o core/selo lidos por script (o registro existe?
selou? o que NAO fechou fica dito).
Fail-closed: o selo tem de ser a v395; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir.
SAIDA: pos_rito\\registro_mapa_v395.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real."""
import glob, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v395 as L
import textos_v395 as T
from guarda_p18_v395 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V395"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v395 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v395.psibit_na_fractalizacao_do_um"
ANOTADAS = ("kernel.psibit_v395_candidata_21out", "kernel.criterio_binario_de_parada.ponto_fixo_v394_d19")
REFS = ("umpy.v394.fock_tempo_e_cunhagens", "infra.bancada_um.sincronizacao_vnnn", "ontologia.um_posto_dimensao_do_nome_07out")


def ids_do_livro():
    """As rotas do livro do mapa (so' leitura)."""
    ids = set()
    for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("tipo") == "ROTA":
            ids.add(d.get("rota_id"))
    return ids


def sim(cond, fechado, aberto):
    return fechado if cond else aberto


def montar(V, core, selo, ids, arts):
    """Monta os registros (a ROTA nova e as ANOTACOES), cada afirmacao testada contra o core/selo; devolve a lista; recusa (assert) se algo nao conferir. Nao escreve nada."""
    assert selo.get("um_version") == "v395", "o selo nao e a v395"
    S = V["s16"]; d = T._d(V); ps = V["psibit"]; kf = core.get("kernel_formalization") or {}
    assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
    for r in ANOTADAS + REFS:
        assert r in ids, "a rota %s nao existe no mapa (anotada ou citada em refs)" % r

    def selou(k):
        return (core.get(k) or {}).get("all_verified") is True

    def anot(rota_id, titulo, resultado, proximo, refs=None, nota=None, estatuto="REAL"):
        a = {"tipo": "ANOTACAO", "rota_id": rota_id, "estatuto": estatuto, "olhou_dados": False, "titulo": titulo, "resultado": resultado, "proximo_passo": proximo, "refs": [NOVA] + (refs or [])}
        if nota:
            a["nota"] = nota
        return a
    c_ps = selou("psibit_v395") and selou("cunhagens_v395") and (ps.get("conditional") or {}).get("inhabitant_exhibited") is False
    v = ps["values"]
    T3 = []
    T3.append(anot(ANOTADAS[0], "v395 SELADA %s: a pedra Psibit (a candidata desta rota) %s" % (S, sim(c_ps, "entra no selo e o registro psibit_v395 selou", "NAO selou no rito")),
                   "psibit_v395 selou=%s (%s); a pedra TGLExt.Psibit esta no kernel do rito (%d modulo, %d bandeiras novas True, escada %s -> %s, dentro do trio); a conjuncao incondicional psibit_is_the_mode_of_the_reader (bandeira %s) e a face do psion, CONDICIONAL "
                   "(bandeira %s; nenhum habitante do certificado de Fock da luz exibido); a mecanica da orbita do Um pela matriz-S em theta_M foi CALCULADA neste rito (%d checagens) e concorda com os termos do kernel (paridade %+d, codigo (%+d, %+d)); "
                   "as %d falas de 21/10 estao embutidas por sha256 (cunhagens_v395 selou=%s). Bijecao de CONJUNTOS sobre o livro de codigos, nao isomorfismo de espacos de Hilbert; o colapso perde exatamente a paridade (um bit); a entropia so' vale ln 2 nos pesos iguais; "
                   "psibit = psion = modo do leitor e' leitura do operador [INPUT/ONTO]." % (selou("psibit_v395"), V["reg395"]["psibit_v395"]["verdict"], V["n_pedras"], d["n_f"], V["escada_antes"], d["depois"], d["unc"], d["cond"], ps["n_checks"], v["parity"], v["code_word"], v["code_verb"],
                                                                                         d["n_cun"], selou("cunhagens_v395")),
                   sim(c_ps, "decisao do operador [LEGAL] sobre a divergencia da tabela da patente ACOM Mirror (qual leitura da paridade e canonica); habitar o certificado de Fock da luz, se o operador quiser fechar a face do psion; auditoria independente do candidato e da cadeia "
                             "(quem construiu nao aprova).", "segue aberto: integrar o que falta numa proxima versao.")))
    c_bin = kf.get("ext_bin394_0001") is True and selou("criterio_binario_de_parada_v394")
    T3.append(anot(ANOTADAS[1], "v395 SELADA %s: a pedra da v394 de nome provisorio (TheBinaryReadingAtTheFixedPoint) %s" % (S, sim(c_bin, "fica como registro e e' citada pela conjuncao do psibit; a bandeira dela segue True", "NAO segue selada no rito")),
                   "a bandeira ext_bin394_0001 segue True no kernel do rito e criterio_binario_de_parada_v394 segue selado; a conjuncao psibit_is_the_mode_of_the_reader (v395) cita a pedra; o nome «ponto fixo» para os pesos iguais segue sendo leitura do operador [ONTO] "
                   "(a fala de 21/10 o usa de novo); o que o colapso e a conjugacao pela matriz-S fixam e' (1/2) I [REAL] (half_identity_is_a_fixed_point); a analogia com o qubit vale nos pesos, nao na entropia.",
                   sim(c_bin, "o nome definitivo da pedra da v394 segue decisao do operador (o nome provisorio fica como registro).", "segue aberto: integrar o que falta numa proxima versao."), refs=[ANOTADAS[0]]))
    for a in T3:
        assert a["rota_id"] in ids, "a rota %s nao existe no mapa" % a["rota_id"]
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v395 SELADA %s: o modo psionico (psibit) na fractalizacao do Um — %d modulo (Psibit), o registro psibit_v395 e %d falas de 21/10 por sha256; escada %s -> %s; o gate nao se move" % (S, V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"]),
            "pergunta": "o candidato v395 selou com o modulo Psibit, o registro psibit_v395 chamado na fractalizacao do Um (a mecanica da orbita do Um pela matriz-S calculada no rito e confrontada com o kernel do proprio rito) e as quatro falas de 21/10 embutidas por sha256, "
                        "sem mudar nenhum veredito fora da troca dita?",
            "dados": ["nenhum dado observado: a mecanica da orbita do Um pela matriz-S em theta_M (beta = alfa CODATA 2018 x sqrt(e) em runtime) e o kernel do rito"],
            "metodo": "ensaio a seco do candidato; um lake build e um Audit no sandbox; rito completo; conferidor (deve mudar / nao pode mudar); leitura da rodada; superficies com a regra da linhagem completa; elo B(n) da Bancada (passo simples, sem salto; recibos)",
            "resultado": "%s | %s | %s | conferidor %s e %s | %d vereditos fora da troca dita mudaram (exigido 0)" % (V["reg395"]["psibit_v395"]["verdict"], V["reg395"]["cunhagens_v395"]["verdict"], V["reg395"]["kh_n1_cobertura_v395"]["verdict"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"]),
            "defeito": "a bijecao e' de CONJUNTOS sobre o livro de codigos da orbita do Um pela matriz-S (nao isomorfismo de espacos de Hilbert, nao toda a mecanica quantica); a face do psion e' CONDICIONAL a um certificado de Fock da luz que o kernel nao habita; "
                       "psibit = psion = modo do leitor e o nome «ponto fixo» sao leituras do operador [INPUT/ONTO], sem lema que ligue o psion ao codigo; a entropia so' vale ln 2 nos pesos iguais; o calculo e' numerico e confere os teoremas, nao os prova; "
                       "a tabela da patente ACOM Mirror diverge de si mesma e a pedra segue o produto sign L x sign dL [LEGAL, decisao do operador]; o dado de alfa tem dois nomes no um.py (SEALED_CODATA_ALPHA e ALPHA_FINE_CODATA_2018) e o beta do core difere de alfa x sqrt(e) em %s relativo "
                       "(o registro compara a %s); o registro kh_n1_cobertura_v394 e os tres contratos da v394 foram corrigidos ao lado (pisos e escada), porque a v395 quebra as igualdades que eles cobravam; a revisao independente do candidato e da cadeia nao esta afirmada" % (
                           T._pe(ps["beta_core_rel_diff"]), T._pg(T._limiar_beta())),
            "nao_refazer": "a integracao do modulo Psibit e a escada %s -> %s estao medidas; a pedra foi recompilada no sandbox e examinada (duas rodadas, a segunda a aprovou); repetir so' com kernel novo" % (V["escada_antes"], d["depois"]),
            "proximo_passo": "decisao do operador [LEGAL] sobre a tabela da patente; o elo B(n) da Bancada Um (palavra do operador); custodia pela sessao do site; commit/push (operador); revisao independente do candidato e da cadeia (quem construiu nao aprova)",
            "onde": PK, "artefatos": arts, "refs": sorted(a["rota_id"] for a in T3) + [r for r in REFS],
            "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move"}
    for r in ROTA["refs"]:
        assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
    REG = [ROTA] + T3
    bad = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
    return REG


def gravar(p, b):
    """backup de BYTES se existir e mudar; temporario -> conferir tamanho -> substituir."""
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m395"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m395"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v395_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v395_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(PK, "ESPERADOS_v395.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v395.json"),
            os.path.join(PK, "DIFF_KERNEL_v395.txt"), os.path.join(PK, "DIFF_v394_v395.diff"), os.path.join(NOS, "HANDOFF_v395_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v395.json"),
            os.path.join(PK, "insumos", "Psibit.lean")] + b3[-1:]
    arts = [a for a in arts if os.path.exists(a)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v395.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v395"
    print("registro MONTADO (NAO registrado): %d registro(s) -> %s" % (len(REG), J))
    print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
