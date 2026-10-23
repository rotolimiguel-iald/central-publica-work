# -*- coding: utf-8 -*-
"""registrar_mapa_v396.py -- MONTA (nao registra) o registro da v396 no mapa de rotas e imprime o comando (molde: registrar_mapa_v395.py). Rodar DEPOIS do fechar (handoff gravado).
A v396 traz UMA rota nova, umpy.v396.testemunha_estatica_na_fractalizacao_do_um (o modulo de kernel TestemunhaEstatica, o registro testemunha_estatica_v396 chamado na fractalizacao do Um junto do psibit e as tres falas de 22/10),
mais DUAS ANOTACOES nas rotas que esperavam por ela (a pedra candidata, kernel.testemunha_estatica_v396_candidata_22out, e a rota do psibit da v395, umpy.v395.psibit_na_fractalizacao_do_um, cuja face de Fock a v396 declara fora da pedra
e deixa condicional), cada afirmacao testada contra o core/selo lidos por script (o registro existe? selou? o que NAO fechou fica dito).
Fail-closed: o selo tem de ser a v396; as rotas anotadas e as citadas em refs tem de existir no livro (so' leitura); a nova nao pode existir. A rota de preparo (umpy.v396.testemunha_estatica_preparo), se a gerencia a registrou, entra nas refs.
SAIDA: pos_rito\\registro_mapa_v396.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa).
A montagem vive na funcao montar(V, core, selo, ids, arts) (sem efeito colateral): o harness a roda contra o Nos emulado, e a cadeia a roda contra o Nos real."""
import glob, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v396 as L
import textos_v396 as T
from guarda_p18_v396 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V396"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v396 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
NOVA = "umpy.v396.testemunha_estatica_na_fractalizacao_do_um"
ANOTADAS = ("kernel.testemunha_estatica_v396_candidata_22out", "umpy.v395.psibit_na_fractalizacao_do_um")
REFS = ("infra.bancada_um.sincronizacao_vnnn", "kernel.v385_axioma_e_testemunha_falsa", "kernel.psibit_v395_candidata_21out", "kernel.criterio_binario_de_parada.ponto_fixo_v394_d19")
OPCIONAIS = ("umpy.v396.testemunha_estatica_preparo",)      # a rota de preparo da gerencia: entra nas refs so' se ja' estiver no livro


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
    assert selo.get("um_version") == "v396", "o selo nao e a v396"
    S = V["s16"]; d = T._d(V); ts = V["testemunha"]; kf = core.get("kernel_formalization") or {}; v = ts["values"]; pv = d["pv"]
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
    c_ts = selou("testemunha_estatica_v396") and selou("cunhagens_v396") and (ts.get("fock") or {}).get("inhabitant_exhibited") is False
    T3 = []
    T3.append(anot(ANOTADAS[0], "v396 SELADA %s: a pedra TestemunhaEstatica (a candidata desta rota) %s" % (S, sim(c_ts, "entra no selo e o registro testemunha_estatica_v396 selou", "NAO selou no rito")),
                   "testemunha_estatica_v396 selou=%s (%s); a pedra TGLExt.TestemunhaEstatica esta no kernel do rito (%d modulo, %d bandeiras novas True, escada %s -> %s, dentro do trio); a composicao incondicional the_psion_inhabits_the_static_witness (bandeira %s) esta no kernel do rito "
                   "e a face de Fock do psion segue CONDICIONAL, declarada em %s fora da pedra e sem habitante exibido; a mecanica foi CALCULADA neste rito (%d checagens, beta = alfa CODATA 2018 x sqrt(e) em runtime) e concorda com os termos: o par ecoa (P^2 = P, residuo %s), "
                   "o individuo (a reducao a um sitio, (1/2) I) nao ecoa, o fluxo construido fixa exatamente a reta do psion e a testemunha global e falsa, o colapso e idempotente e nao injetivo; as %d falas de 22/10 estao embutidas por sha256 (cunhagens_v396 selou=%s). "
                   "A ponte e CONSTRUIDA, nao derivada; o 1/2 e entropia linear (a de von Neumann e ln 2 = %s nat); psion como habitante da testemunha estatica, luz como eco de reconhecimento e colapso como eco da identidade reconhecida sao leituras do operador [INPUT/ONTO]." % (
                       selou("testemunha_estatica_v396"), V["reg396"]["testemunha_estatica_v396"]["verdict"], V["n_pedras"], d["n_f"], V["escada_antes"], d["depois"], d["unc"], d["fock_path"], ts["n_checks"], T._pe(v["pair_idempotence_residual"]),
                       d["n_cun"], selou("cunhagens_v396"), T._p(v["ln2"], 12)),
                   sim(c_ts, "o operador nomeia a pedra (nome provisorio); habitar o certificado de Fock da luz e ligar o psion do certificado ao canto, se o operador quiser fechar a face de Fock; auditoria independente do candidato e da cadeia (quem construiu nao aprova).",
                       "segue aberto: integrar o que falta numa proxima versao.")))
    c_ps = selou("psibit_v395") and selou("cunhagens_v395") and selou("kh_n1_cobertura_v395") and kf.get(d["fock_flag"]) is True
    T3.append(anot(ANOTADAS[1], "v396 SELADA %s: a testemunha estatica e' lida junto do psibit na fractalizacao do Um; %s" % (S, sim(c_ps, "os registros da v395 seguem selados e a face de Fock do psion segue condicional", "algum registro da v395 NAO segue selado ou a face de Fock mudou")),
                   "psibit_v395, cunhagens_v395 e kh_n1_cobertura_v395 seguem selados no rito da v396 (selou=%s); a escada nova entra como dado nos quatro contratos (expected_ladder) e kh_n1_cobertura_v395 virou piso (errata ao lado), sem mudar nenhum veredito; "
                   "a face de Fock do psion (TGLExt.Psibit.the_psion_face_of_the_psibit, bandeira %s True=%s) segue CONDICIONAL a um certificado de Fock da luz sem habitante exibido: o registro testemunha_estatica_v396 a declara em %s, fora da pedra, e nao a habita; "
                   "nenhum lema liga o psion do certificado ao psionCorner (dois objetos do kernel com o mesmo nome)." % (c_ps, d["fock_flag"], kf.get(d["fock_flag"]) is True, d["fock_path"]),
                   sim(c_ps, "habitar o certificado de Fock da luz e provar o elo psion C <-> psionCorner, se o operador quiser fechar a face; a decisao [LEGAL] herdada da v395 (tabela da patente) segue do operador.", "segue aberto: integrar o que falta numa proxima versao."), refs=[ANOTADAS[0]]))
    for a in T3:
        assert a["rota_id"] in ids, "a rota %s nao existe no mapa" % a["rota_id"]
    ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
            "titulo": "v396 SELADA %s: a testemunha estatica (o psion habita a fronteira) na fractalizacao do Um — %d modulo (TestemunhaEstatica, nome provisorio), o registro testemunha_estatica_v396 e %d falas de 22/10 por sha256; escada %s -> %s; o gate nao se move" % (
                S, V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"]),
            "pergunta": "o candidato v396 selou com o modulo TestemunhaEstatica, o registro testemunha_estatica_v396 chamado na fractalizacao do Um junto do psibit (a mecanica do canto do psion, da reducao a um sitio, do fluxo construido e do colapso, calculada no rito e confrontada com o kernel do proprio rito) "
                        "e as tres falas de 22/10 embutidas por sha256, sem mudar nenhum veredito fora da troca dita?",
            "dados": ["nenhum dado observado: a mecanica do canto do psion (projetor de Bell 4x4), da reducao a um sitio, do fluxo F_t = P + exp(-t beta g)(1 - P) e do colapso P y P (beta = alfa CODATA 2018 x sqrt(e) em runtime) e o kernel do rito"],
            "metodo": "ensaio a seco do candidato; um lake build e um Audit no sandbox; rito completo; conferidor (deve mudar / nao pode mudar); leitura da rodada; superficies com a regra da linhagem completa; elo B(n) da Bancada (passo simples, sem salto; recibos)",
            "resultado": "%s | %s | %s | conferidor %s e %s | %d vereditos fora da troca dita mudaram (exigido 0)" % (V["reg396"]["testemunha_estatica_v396"]["verdict"], V["reg396"]["cunhagens_v396"]["verdict"], V["reg396"]["kh_n1_cobertura_v396"]["verdict"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"]),
            "defeito": "a ponte e' CONSTRUIDA (o fluxo foi escolhido para ter o vetor de Bell como modo zero), nao derivada: nao mostra que o Nome da fronteira da TGL seja o vetor de Bell nem que psionFlow seja a dinamica da teoria (ressalva de tipo: vetor x projetor); "
                       "o 'individuo' que nao ecoa e' o par visto por um lado so; o 1/2 da reducao e' entropia linear e a de von Neumann e' ln 2; a face de Fock do psion segue CONDICIONAL a um certificado sem habitante exibido e nenhum lema liga psion C ao psionCorner; "
                       "psion como habitante da testemunha estatica, luz como eco de reconhecimento e colapso como eco da identidade reconhecida sao leituras do operador [INPUT/ONTO]; o calculo e' numerico e confere os teoremas, nao os prova; "
                       "a proveniencia atribui %d declaracoes a pedra e so' %d sao novas (TGLExt.diagFlow.eq_1 muda de modulo); o dado de alfa tem dois nomes no um.py (SEALED_CODATA_ALPHA e ALPHA_FINE_CODATA_2018) e o beta do core difere de alfa x sqrt(e) em %s relativo (o registro compara a %s); "
                       "o registro kh_n1_cobertura_v395 e os quatro contratos foram corrigidos ao lado (pisos e escada), porque a v396 quebra as igualdades que eles cobravam; o nome da pedra e' provisorio; nao e' teste (ordem do operador de 22/10: nada de teste armado); "
                       "a revisao independente do candidato e da cadeia nao esta afirmada" % (pv["mod"], pv["novas"], T._pe(ts["beta_core_rel_diff"]), T._pg(T._limiar_beta())),
            "nao_refazer": "a integracao do modulo TestemunhaEstatica e a escada %s -> %s estao medidas; a pedra foi recompilada no sandbox e examinada (PEDRA_APROVADA, tres BAIXAS aplicadas como texto); repetir so' com kernel novo" % (V["escada_antes"], d["depois"]),
            "proximo_passo": "o operador nomeia a pedra; o elo B(n) da Bancada Um (palavra do operador); custodia pela sessao do site; commit/push (operador); decisao [LEGAL] herdada da v395; revisao independente do candidato e da cadeia (quem construiu nao aprova)",
            "onde": PK, "artefatos": arts, "refs": sorted(a["rota_id"] for a in T3) + [r for r in REFS] + [r for r in OPCIONAIS if r in ids],
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
        bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m396"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_m396"; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def main():
    V, PROB = L.ler()
    if PROB:
        print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); return 2
    NOS = L.NOS
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v396_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v396_*.json")), key=os.path.getmtime)
    arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(PK, "ESPERADOS_v396.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v396.json"),
            os.path.join(PK, "DIFF_KERNEL_v396.txt"), os.path.join(PK, "DIFF_v395_v396.diff"), os.path.join(NOS, "HANDOFF_v396_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v396.json"),
            os.path.join(PK, "insumos", "TestemunhaEstatica.lean"), os.path.join(PK, "insumos", "EXAME_TESTEMUNHA.md")] + b3[-1:]
    arts = [a for a in arts if os.path.exists(a)]
    REG = montar(V, core, selo, ids_do_livro(), arts)
    J = os.path.join(HERE, "registro_mapa_v396.json")
    gravar(J, json.dumps(REG, ensure_ascii=False, indent=1).encode("utf-8"))
    quem = "claude-c1 (gerência), cadeia v396"
    print("registro MONTADO (NAO registrado): %d registro(s) -> %s" % (len(REG), J))
    print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
    print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
