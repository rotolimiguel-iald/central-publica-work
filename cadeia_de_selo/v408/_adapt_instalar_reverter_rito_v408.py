# -*- coding: utf-8 -*-
"""_adapt_instalar_reverter_rito_v408.py -- adapta a v408 (04/11/2026, claude-construtor-v408, a servico da gerencia c1) os scripts do ATO (nunca executados na preparacao) e a conferencia deles:
instalar_v408.py, reverter_v408.py, rito_v408.sh e conferir_instalar_rito_v408.py. O que muda e' o CONTEUDO dito: o bundle de 4 modulos (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP; nomes do operador de 04/11),
o registro tetelestai_terminal_v408, as 41 ancoras, as 12 falas de 04/11, as decisoes D48 a D54 e as erratas E21 a E23, nenhuma chave antiga muda; as pedras anteriores ganham os 9 modulos da v407 (lidos de v407/kernel_modulos_novos_v407.json);
os tempos do rito sao LIDOS de kernel/construir_marcas.txt e kernel/POS_BUILD_v408.json (nunca digitados). Os invariantes do instalador (recibo pre_selo, Bancada pina v407, raiz/Audit da v407, lista lida do JSON) nao mudam.
Trocas de contagem EXATA; backup de bytes; a marca so' sai do arquivo adaptado. Escrito pela ferramenta Write."""
import ast, datetime, json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); V407 = os.path.join(os.path.dirname(HERE), "v407")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
_nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v408.json"), encoding="utf-8"))["novos"]
assert [x.split("/")[-1][:-5] for x in _nov] == ["TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP"], _nov
_nov7 = json.load(open(os.path.join(V407, "kernel_modulos_novos_v407.json"), encoding="utf-8"))["novos"]
MODS7 = [x.split("/")[-1][:-5] for x in _nov7]
assert len(MODS7) == 9 and MODS7[0] == "PsionCanto" and MODS7[1] == "Par" and all(x.startswith("TGLExt/") and x.count("/") == 1 for x in _nov7), MODS7
_mk = open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read()
_mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", _mk, re.M)}
BUILD_S = _mm["epoch_build_fim"] - _mm["epoch_inicio"]; AUDIT_S = _mm["epoch_audit_fim"] - _mm["epoch_build_fim"]; assert BUILD_S > 0 and AUDIT_S > 0
_pb = json.load(open(os.path.join(HERE, "kernel", "POS_BUILD_v408.json"), encoding="utf-8"))
assert _pb["duracao_build_s"] == BUILD_S and _pb["duracao_audit_s"] == AUDIT_S, (_pb["duracao_build_s"], BUILD_S, _pb["duracao_audit_s"], AUDIT_S)
_soma = _pb.get("build_modulos_s_soma"); _mx = _pb.get("build_modulos_s_max")
_mx_txt = ("%s s" % _mx) if isinstance(_mx, (int, float)) else json.dumps(_mx, ensure_ascii=False)
MARCA_RX = re.compile(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n")


class Arq:
    def __init__(self, rel):
        self.p = os.path.join(HERE, rel); self.rel = rel
        self.raw = open(self.p, "rb").read()
        open(self.p + ".bak_" + TS + "_adapt", "wb").write(self.raw)
        self.t = self.raw.decode("utf-8"); self.crlf = "\r\n" in self.t
        if self.crlf:
            self.t = self.t.replace("\r\n", "\n")

    def sub(self, old, new, n=1):
        assert self.t.count(old) == n, (self.rel, old[:100], self.t.count(old), n); self.t = self.t.replace(old, new)

    def sub_linha(self, prefixo, nova):
        """troca a UNICA linha que comeca por `prefixo` pela linha `nova` inteira"""
        rx = re.compile("(?m)^" + re.escape(prefixo) + "[^\n]*$"); assert len(rx.findall(self.t)) == 1, (self.rel, prefixo[:80], len(rx.findall(self.t)))
        self.t = rx.sub(lambda m_: nova, self.t, count=1)

    def tira_marca(self):
        assert len(MARCA_RX.findall(self.t)) == 1, (self.rel, "marca"); self.t = MARCA_RX.sub("", self.t, count=1)

    def grava(self):
        assert "[A ADAPTAR" not in self.t, self.rel
        t = self.t.replace("\n", "\r\n") if self.crlf else self.t
        if self.rel.endswith(".py"):
            ast.parse(t)
        open(self.p, "wb").write(t.encode("utf-8"))
        if self.rel.endswith(".sh"):
            r = subprocess.run(["sh", "-n", self.p], capture_output=True, text=True); assert r.returncode == 0, (self.rel, r.stderr[:300])
        print("ok", self.rel, len(self.raw), "->", len(t.encode("utf-8")))


# ======================================================================================= instalar_v408.py
a = Arq("instalar_v408.py"); a.tira_marca()
a.sub("(ato da gerencia c1; adaptado em 03/11/2026 para o BUNDLE PEQUENO de nove modulos em TGLExt/, NAO executado na preparacao)",
      "(ato da gerencia c1; adaptado em 04/11/2026 por claude-construtor-v408 para o BUNDLE PEQUENO de quatro modulos em TGLExt/ [TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP], NAO executado na preparacao)")
a.sub("a v408 so' ACRESCENTA nove imports na raiz e nao muda o Audit;", "a v408 so' ACRESCENTA quatro imports na raiz e nao muda o Audit;")
a.sub("(a v408 traz 9 modulos novos de kernel em TGLExt/ [PsionCanto, Par e as sete pedras de 02/11, todos de nome ratificado pelo operador; nenhum da bancada do ChatGPT];",
      "(a v408 traz 4 modulos novos de kernel em TGLExt/ [TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, com os nomes dados pelo operador em 04/11/2026; nenhum da bancada do ChatGPT];")
a.sub_linha("# v408: (a) as pedras anteriores (",
            "# v408: (a) as pedras anteriores (o criterio binario, a rede de Fock, o tempo, Psibit, TestemunhaEstatica, Token, Sonico, AfinacaoDasCordas, FalsidadeDaInercia, PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional, Caminho, Vida, VerdadeAdendo, ProjecaoTransversalDaMeiaNat, Jo8v32, as OITO da v405: PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler e PontoZeroDoPsion, e os 9 modulos da v407: %s) e o bundle do fecho da v406 (301 modulos em TGLExt/F1Fecho394, com a candidata CanonicalFullTGLWitnessR1) JA estao no kernel do Nos (a base instalada e' a v407 selada); (b) os 4 modulos novos da v408 (em TGLExt/, nao em F1Fecho394) NAO estao la ainda." % ", ".join(MODS7))
a.sub('"DiscoDeEuler", "PontoZeroDoPsion")\n', '"DiscoDeEuler", "PontoZeroDoPsion",\n                      %s)   # (os 9 da v407, lidos de v407/kernel_modulos_novos_v407.json pelo adaptador)\n' % ", ".join('"%s"' % m for m in MODS7))
a.sub('"as pedras anteriores (v394 a v407, as oito da v405 e o bundle do fecho da v407 inclusive) nao estao no kernel do Nos -- nao instalo"',
      '"as pedras anteriores (v394 a v407, as oito da v405, os 9 modulos da v407 e o bundle do fecho da v406 inclusive) nao estao no kernel do Nos -- nao instalo"')
a.sub('("a lista dos modulos novos nao e\' a do ESPERADOS (o bundle de nove modulos em TGLExt/)", _N)', '("a lista dos modulos novos nao e\' a do ESPERADOS (o bundle de quatro modulos em TGLExt/)", _N)')
a.grava()
# ======================================================================================= reverter_v408.py
a = Arq("reverter_v408.py"); a.tira_marca()
a.sub("(ato da gerencia c1; usar so' se o rito falhar; adaptado em 03/11/2026 para o BUNDLE PEQUENO de nove modulos em TGLExt/, NAO executado na preparacao)",
      "(ato da gerencia c1; usar so' se o rito falhar; adaptado em 04/11/2026 por claude-construtor-v408 para o BUNDLE PEQUENO de quatro modulos em TGLExt/, NAO executado na preparacao)")
a.sub("e poe os 9 modulos novos de kernel da v408 (PsionCanto, Par e as sete pedras de 02/11, em TGLExt/: a lista que o instalador gravou;",
      "e poe os 4 modulos novos de kernel da v408 (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, em TGLExt/: a lista que o instalador gravou;")
a.sub('("a lista dos modulos novos da v408 difere de ESPERADOS.bundle_sha256 (o bundle de nove modulos em TGLExt/)", len(_lista))', '("a lista dos modulos novos da v408 difere de ESPERADOS.bundle_sha256 (o bundle de quatro modulos em TGLExt/)", len(_lista))')
a.grava()
# ======================================================================================= rito_v408.sh
a = Arq("rito_v408.sh"); a.tira_marca()
a.sub_linha("# O RITO v408 (ato da gerencia c1, adaptado em 03/11/2026; o psion, o canto e o par):",
            "# O RITO v408 (ato da gerencia c1, adaptado em 04/11/2026 por claude-construtor-v408; Tetelestai e' o terminal): roda o um.py v408 instalado no Nos -- 4 modulos novos de kernel em TGLExt/ (o BUNDLE PEQUENO: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, com os nomes dados pelo operador em 04/11/2026; a lista e' lida de kernel_modulos_novos_v408.json e conferida contra ESPERADOS.bundle_sha256) materializados a partir do corpo embutido, kernel e Audit")
a.sub_linha("# construidos pelo proprio um.py (a raiz TGLExt.lean ganha nove imports;",
            "# construidos pelo proprio um.py (a raiz TGLExt.lean ganha quatro imports; o Audit nao muda), o registro com FUNCAO tetelestai_terminal_v408 (chamado no main logo depois do bloco do psion_canto_v407 e dos registros por spec da v407; le as 41 ancoras do axiom_report do rito, as quatro fontes embutidas por sha256, as 12 falas de 04/11 por sha256 [nas duas de autor misto, so' o paragrafo do operador e' citado] e a escada; NENHUMA chave antiga muda: a chave do lema (v407) segue LIDA do kernel; os vereditos de testemunha_estatica_v396, psibit_v395, rede_fock_v394, fechamento_v406 e psion_canto_v407 nao mudam de prefixo; o gate e a funcao do neutrino nao mudam; o numero da massa nao muda), os registros por spec novos do core v408 (cunhagens_v408, com as 12 falas de 04/11, os nomes das pedras, a regra «provar ou podar», as decisoes D48 a D54 e as erratas E21 a E23; kh_n1_cobertura_v408) e os registros da v399 a v407 RECRIADOS (incluidos o psion_canto_v407, com a escada do contrato subida para a da v408, e os specs cunhagens_v407 [com a errata E21 AO LADO] e kh_n1_cobertura_v407, este ultimo com pisos no lugar de igualdades; o fechamento_v406 e os specs da v406 seguem como na v407), o SIDECAR um_absoluto_selo_acom.json (depois da ultima escrita do selo). O QUADRO do Teste da Unica Palavra segue no topo. Nada aqui move o gate; validade no kernel nao e' creditacao; NOT_FALSIFIED nunca e' confirmacao.")
a.sub_linha("# O PILAR QUANTICO NAO roda de novo:",
            "# O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (a mesma da v407; o motor continuo no pilar NAO entra na v408: as decisoes D38/D45 das cadeias anteriores seguem, nenhuma decisao da v408 [D48 a D54] as muda); TGL_RITE_CHECKPOINT DESLIGADO; nenhum dado novo e' aberto (o teste (d) do ramo B segue so' por citacao do pre-registro V1.1, D44 herdada). Molde: o rito da v407 (herdeiro do rito_v399.sh com as afericoes dele), trocados os nomes, o pacote (a propria pasta da cadeia v408) e a")
a.sub_linha("# TEMPO ESPERADO (v408,",
            "# TEMPO ESPERADO (v408, parametro lido de kernel/construir_marcas.txt e kernel/POS_BUILD_v408.json, MEDIDO em 04/11/2026 no sandbox k408c): o `lake build` dos 4 modulos novos a frio (a v407 selada ja' esta' compilada em .lake/build; muda a raiz TGLExt; o Audit nao muda) = %d s e 1 Audit = %d s (a soma dos tempos por modulo e' %s s, o maximo de um modulo %s); o rito faz 3 passagens de build + Audit no Nos, cuja arvore compilada e' a da v407: a PRIMEIRA compila os 4 a frio (a ordem de grandeza e' a medida do sandbox, %d s + %d s) e as outras duas passagens so' reconferem (build ja' pronto + Audit de %d s) [estimativa da gerencia, nao medida: o tempo total do rito sai das marcas rito_horarios_v408.txt]. O timeout do lake build DENTRO do um.py (candidato) tem de caber nisso: conferir no candidato antes de rodar." % (BUILD_S, AUDIT_S, _soma, _mx_txt, BUILD_S, AUDIT_S, AUDIT_S))
for velho in ("psion, o canto e o par", "PsionCanto", "76 ancoras", "nove imports", "D41 a D47", "E18 a E20", "03/11/2026", "k407c"):
    assert velho not in a.t, ("rotulo velho ficou no rito", velho)
a.grava()
# ======================================================================================= conferir_instalar_rito_v408.py
a = Arq("conferir_instalar_rito_v408.py"); a.tira_marca()
a.sub("(derivados dos da v407, adaptados em 03/11/2026 ao BUNDLE PEQUENO de nove modulos em TGLExt/, com as licoes da v407)", "(derivados dos da v407, adaptados em 04/11/2026 ao BUNDLE PEQUENO de quatro modulos em TGLExt/, com as licoes da v407)")
a.sub("os nove modulos em TGLExt/ e nao mais em TGLExt/F1Fecho394/...)", "os quatro modulos em TGLExt/, nao em TGLExt/F1Fecho394/...; as pedras anteriores incluem os 9 modulos da v407)")
a.sub("_DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D6.DECISOES), key=lambda k_: int(k_[1:]))   # as decisoes que a v408 acrescenta (D41..D47), lidas de DL",
      "_DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D7.DECISOES), key=lambda k_: int(k_[1:]))   # as decisoes que a v408 acrescenta (D48..D54), lidas de DL (a diferenca contra o delta da v407, nao contra o da v406)\nassert _DEC_NOVAS and _DEC_NOVAS[0] == \"D48\" and _DEC_NOVAS[-1] == \"D54\", _DEC_NOVAS")
a.sub("_ERR_NOVAS = [e_.split(\" --\")[0] for e_ in DL.ERRATAS_V408]   # as erratas da v408 (E18..E20), lidas de DL", "_ERR_NOVAS = [e_.split(\" --\")[0] for e_ in DL.ERRATAS_V408]   # as erratas da v408 (E21..E23), lidas de DL\nassert _ERR_NOVAS == [\"E21\", \"E22\", \"E23\"], _ERR_NOVAS")
# instalar: marcas novas (as pedras da v408 e da v407 no texto) e rotulos velhos que viram erro
a.sub("\"FalsidadeDaInercia\", \"PonteDaEscalaDual\", \"QuedaSemGeometria\", \"EsperancaCondicional\", \"ProjecaoTransversalDaMeiaNat\", \"Jo8v32\", \"tgl_kernel_proof_manifest.json\", '\"version\") == \"v407\"'],",
      "\"FalsidadeDaInercia\", \"PonteDaEscalaDual\", \"QuedaSemGeometria\", \"EsperancaCondicional\", \"ProjecaoTransversalDaMeiaNat\", \"Jo8v32\", \"tgl_kernel_proof_manifest.json\", '\"version\") == \"v407\"',\n                              \"TetelestaiTerminal\", \"PIgualNP\", \"PsionCanto\", \"OIgual\", \"quatro imports\", \"os 9 modulos da v407\", \"bundle do fecho da v406\"],")
a.sub("'x_.startswith(\"TGLExt/F1Fecho394/\")', \"== 301\", \"o bundle de 301\", \"301 modulos novos\", \"pilar_anterior_v405\", \"[A ADAPTAR v408]\"])",
      "'x_.startswith(\"TGLExt/F1Fecho394/\")', \"== 301\", \"o bundle de 301\", \"301 modulos novos\", \"pilar_anterior_v405\", \"[A ADAPTAR v408]\", \"nove imports\", \"nove modulos\", \"PsionCanto, Par e as sete pedras de 02/11, todos de nome ratificado\", \"bundle do fecho da v407\", \"03/11/2026\"])")
a.sub("\"pedras_sha256\", \"quarentena_pedras_\", 'x_.startswith(\"TGLExt/F1Fecho394/\")', \"== 301\", \"o bundle de 301\", \"301 modulos novos\", \"[A ADAPTAR v408]\"])",
      "\"pedras_sha256\", \"quarentena_pedras_\", 'x_.startswith(\"TGLExt/F1Fecho394/\")', \"== 301\", \"o bundle de 301\", \"301 modulos novos\", \"[A ADAPTAR v408]\", \"nove modulos\", \"PsionCanto, Par e as sete pedras de 02/11\", \"03/11/2026\"])")
# rito: os marcadores do conteudo v408 (e os velhos da v407 viram erro)
a.sub("\"psion_canto_v407\", \"PsionCanto\", \"the_psion_is_the_corner_on_both_faces\", \"linked_to_the_corner_by_a_lemma\", \"cunhagens_v407\", \"kh_n1_cobertura_v407\", \"fechamento_v406\", \"D44\",",
      "\"tetelestai_terminal_v408\", \"TetelestaiTerminal\", \"TempoIgualMoeda\", \"PontoDeContradicao\", \"PIgualNP\", \"cunhagens_v408\", \"kh_n1_cobertura_v408\", \"psion_canto_v407\", \"cunhagens_v407\", \"kh_n1_cobertura_v407\", \"fechamento_v406\", \"E21\", \"D38/D45\", \"NENHUMA chave antiga muda\", \"12 falas de 04/11\", \"carimbar_stdout_v408.py\",")
a.sub("[\"rodada_v407_stdout\", \".rito_v407.pid\", \"rito_v407\", \"TGLExt/Testemunho, nome PROVISORIO\", \"do Codex, ORDEM 025\", \"OS OITO registros com FUNCAO\", \"8 modulos novos de kernel\", \"301 modulos novos\", \"TGLExt/F1Fecho394\", \"CanonicalFullTGLWitnessR1\", \"dois imports\", \"k407c\", \"1736 s\", \"2016 s\", \"15986 s\", \"[A ADAPTAR v408]\"])",
      "[\"rodada_v407_stdout\", \".rito_v407.pid\", \"rito_v407\", \"TGLExt/Testemunho, nome PROVISORIO\", \"do Codex, ORDEM 025\", \"OS OITO registros com FUNCAO\", \"8 modulos novos de kernel\", \"301 modulos novos\", \"TGLExt/F1Fecho394\", \"CanonicalFullTGLWitnessR1\", \"dois imports\", \"k407c\", \"1736 s\", \"2016 s\", \"15986 s\", \"[A ADAPTAR v408]\",\n                              \"9 modulos novos de kernel em TGLExt/\", \"nove imports\", \"76 ancoras\", \"PsionCanto e Par, da gerencia c1\", \"the_psion_is_the_corner_on_both_faces\", \"D41 a D47\", \"E18 a E20\", \"o psion, o canto e o par\", \"carimbar_stdout_v407.py\", \"03/11/2026\"])")
a.sub('("lista_que_nao_e_lista", {"novos": "TGLExt/PsionCanto.lean"})', '("lista_que_nao_e_lista", {"novos": "TGLExt/TetelestaiTerminal.lean"})')
a.grava()
print("tempos: build", BUILD_S, "audit", AUDIT_S, "| soma por modulo", _soma, "| max", _mx_txt, "| 9 da v407:", MODS7)
