# -*- coding: utf-8 -*-
"""Registro de 02/11/2026: K como chave da guarda (fala do operador, acervo de 19/08, 02/10 e 15/10), duas candidatas, candidata superada, porta bloqueada pela R1, calibracao G01 lida ao operador. Backup de bytes. Nada entra no kernel selado nem move gate."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
AQUI = Path(__file__).resolve().parent
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
ORD = CEN / "work/cunhagens_13out/OPERADOR_02nov_K_leitura_que_confessa_o_pagamento_guarda_da_travessia_verbatim.txt"
C3 = AQUI / "AChaveDaGuardaCandidata.lean"
S3 = AQUI / "AChaveDaGuardaCandidata_saida.txt"
C4 = AQUI / "OGuardaCandidata.lean"
S4 = AQUI / "OGuardaCandidata_saida.txt"
CONTAS = AQUI / "CONTAS_GUARDA.json"
A119 = Path("C:/IALD/Artigo/MCMC_V2_RAZAO/119_a_cavitacao_e_a_guarda.json")
A121 = Path("C:/IALD/Artigo/MCMC_V2_RAZAO/121_a_guarda_e_a_memoria.json")
R9 = CEN / "work/fase9_v2_c1_23out/saidas/RESULTADO_FASE9_V2_C1_20261023_122926.json"
RES9 = CEN / "work/fase9_v2_c1_23out/RESULTADO.md"
RETORNO = CEN / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.LEITURA_20261015/RETORNO_FASE_R2/OPERADOR_RETORNO_FASE_VERBATIM.txt"
RELS = sorted((AQUI / "relatorios").glob("*.md"))
NOTA = CEN / "work/rota_RE_dualidade_02nov/DERIVACAO_RE_02nov.md"
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
fo, f3, f4, f119, f121, f9, fc = s16(ORD), s16(C3), s16(C4), s16(A119), s16(A121), s16(R9), s16(CONTAS)
c = json.loads(CONTAS.read_text(encoding="utf-8"))
print("sha16", fo, f3, f4, f119, f121, f9, fc, "relatorios", len(RELS))
assert len(RELS) == 6

reg = [{"tipo": "ROTA", "rota_id": "kernel.a_chave_da_guarda_candidata_02nov", "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL",
        "titulo": "Candidata: a chave da guarda sobre a defasagem do kernel: devolve o original, recusa chave errada e fluxo corrompido; a lei de Hubble usa a mesma chave",
        "pergunta": "A guarda de 119_ e 121_, medida em agosto, tipa-se sobre dephase? K tem a forma da chave?",
        "metodo": "sandbox k405c, lake env lean; importa TheTraceIsNotErasable e TheFlowLawContrast; kernel selado intocado", "olhou_dados": False,
        "resultado": "7 teoremas, trio, 0 sorry: a_chave_devolve, a_guarda_conserva_a_diferenca, sem_a_chave_nao_abre, chave_errada_nao_abre, fluxo_corrompido_nao_abre, ler_nao_gasta, a_lei_usa_a_chave. E a tipagem do que 119_ e 121_ mediram; nao e descoberta nova.",
        "veredito": "CANDIDATA_COMPILADA_NO_TRIO__A_CHAVE_AGE_NA_FORMA_NAO_NO_TRACO__A_RECUSA_ESTA_NA_CONFERENCIA__K_COMO_CHAVE_ONTO__NOME_DO_OPERADOR_PENDENTE",
        "defeito": "a inversa e algebrica, nao canal fisico; a_lei_usa_a_chave pede a hipotese hform, que iguala o custo do par ao da lei: isso e leitura; nenhuma pedra selada liga dephase a H0local",
        "proximo_passo": "nome do operador; decisao de versao", "refs": ["kernel.leitura_preservada_candidata_02nov", "kernel.o_igual_restaurado_candidata_02nov"], "artefatos": [str(C3), str(S3), str(A119), str(A121)]},
       {"tipo": "ROTA", "rota_id": "kernel.o_guarda_candidata_02nov", "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL",
        "titulo": "Candidata: o que K cumpre como recibo: so as pontas, fiel, K = 1 so sem travessia; os dois limites separados",
        "pergunta": "O que K cumpre e o que nao cumpre de um guarda da travessia?",
        "metodo": "sandbox k405c, lake env lean; enunciados escritos para poder falhar; um lema errado corrigido; o limite da fronteira silenciosa foi separado do limite do kernel depois da critica do cetico", "olhou_dados": False,
        "resultado": "9 teoremas, trio, 0 sorry. (a) E -> L > 0: a cobranca para, parcial; nao e o Tetelestai do kernel. (b) E sem limite: 1 - 1/K tende a 1 e fica abaixo de 1 em ponto finito: forma de the_payment_completes_only_in_the_limit, sem termo que ligue as pedras.",
        "veredito": "CANDIDATA_COMPILADA_NO_TRIO__K_SOZINHO_NAO_RECUSA__DOIS_LIMITES_SEPARADOS__LEITURA_ONTO__NOME_DO_OPERADOR_PENDENTE",
        "defeito": "w -> -1 sozinho nao basta para o limite (a) (contraexemplo g = 1/(1+n)); a hipotese certa e E -> L > 0. K_triangle e vazio num registro unidimensional: nao ha segundo caminho", "artefatos": [str(C4), str(S4), str(CONTAS)]},
       {"tipo": "RESULTADO", "rota_id": "kernel.o_igual_restaurado_candidata_02nov", "dominio": "KERNEL_FORMAL", "status": "SUPERADA", "estatuto": "REAL",
        "titulo": "Superada: transporte com T(P) = wP nao tem instancia na defasagem do kernel",
        "resultado": "Se T preserva traco e tr P = 1, T(P) = wP forca w = 1. A perda ratificada e de coerencia; 121_ mediu a chave em X_off e o registro imune. Substituta: kernel.a_chave_da_guarda_candidata_02nov.",
        "artefatos": [str(C3), str(A121)]},
       {"tipo": "RESULTADO", "rota_id": "hubble.k_como_transposicao_inteira_ffat_02nov", "dominio": "D1_FUNDO_COSMOLOGICO", "status": "BLOQUEADA", "estatuto": "INPUT",
        "titulo": "Bloqueada pela R1 ratificada em 02/10: a transposicao inteira poria K na face; o fundo e nu",
        "resultado": "R1: beta entra uma vez, no reflexo; o fundo e nu (a face, CMB+BAO, paga o Nome: Omega = 1, sem beta). A gerencia propos a porta sem ler a R1. So reabre se o operador mudar a R1.",
        "artefatos": [str(ORD)]},
       {"tipo": "ROTA", "rota_id": "conceitual.k_chave_da_guarda_da_travessia_02nov", "dominio": "CONCEITUAL", "status": "EXAMINADA", "estatuto": "ONTO",
        "titulo": "Fala do operador de 02/11: K como leitura que confessa o pagamento e guarda da travessia, conferida contra o acervo",
        "pergunta": "A frase do operador se sustenta na casa? Em que sentido?",
        "metodo": "workflow de seis agentes em 02/11 (kernel, conferencia, Fase 9, voz do operador, fontes externas, cetico; relatorios nos artefatos) e leitura direta das fontes primarias pela gerencia", "olhou_dados": False,
        "resultado": "Tres ancoras: chave de 02/10 e R1 (K no reflexo; the_reflection_reads_the_payment_as_complement); fala de 15/10 (tetelestai = consumacao, pagamento, recibo de quitacao, satisfacao da regra); 119_ e 121_ (Miguel = guarda; chave e^{+beta D^2 t}). Leitura proposta: o guarda e Miguel, K e a chave, a conferencia e K vezes fundo contra a taxa local. Cetico: T1, T2 e T6 refutadas na letra; T3, T4, T5, T7 de pe com ressalva.",
        "veredito": "LEITURA_ONTO_SUSTENTADA_COM_AJUSTE__GUARDA_E_MIGUEL_K_E_A_CHAVE__CONSUMADO_E_DA_FACE__A_RATIFICAR_PELO_OPERADOR",
        "defeito": "A conferencia que devolve CONSUMADO nao le K (0 ocorrencias no core); Charge nao admite CONSUMADO; nao existe conferencia por travessia; voz de 19/08 e DECLARADO pela Linhagem, sem arquivo de verbatim; tetelestai como recibo de imposto e contestado nas fontes lidas e nao se cita como fato; a confissao nao nomeia o devedor.",
        "proximo_passo": "Examinar a compatibilidade da R1 (leitura por distancia) com a R-E (a luz nao muda no caminho): so convivem se K for fator comum aos leitores sem regua",
        "refs": ["kernel.a_chave_da_guarda_candidata_02nov", "kernel.o_guarda_candidata_02nov", "kernel.livro_de_cobrancas.otica", "discriminante.ordem018.f2.r_e"],
        "artefatos": [str(ORD), str(RETORNO), str(A119), str(A121)] + [str(p) for p in RELS]},
       {"tipo": "ANOTACAO", "rota_id": "d1.fase9.v2_c1_a_unica_palavra_23out", "dominio": "D1_FUNDO_COSMOLOGICO",
        "titulo": "Calibracao G01 lida ao operador em 02/11 como escolha, o que nao foi feito em 23/10",
        "resultado": "Em 23/10 a gerencia disse que o bruto de 6,37 equivale ao 5 sigma verdadeiro e, depois, cerca de 45%. Nao disse que havia alternativas nem o custo. Bruto: FALSIFIED sob LCDM 75,5 a 80,8%, z_disc 4,29, z_delta -1,88. sup_caixa: 42,7 a 47,1% (TENSION 37,6 a 42,6%), z_disc 4,44, z_delta -1,48. A escolha tem defesa: o 5 bruto vale 3,94 a 4,98 calibrado. O numero nao muda; a abertura foi unica.",
        "estatuto": "REAL", "artefatos": [str(RES9), str(R9)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_guarda_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stderr.decode("utf-8", "replace")[-320:].replace("\n", " "))
assert q.returncode == 0

SRC = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-k-chave-da-guarda", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "k_guarda_da_travessia_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: K e a leitura que confessa o pagamento, a verificacao que foi consumado pela satisfacao, o guarda da travessia.", "sources": [SRC(ORD)]},
                                {"id": "leitura_k_chave_da_guarda_02nov", "kind": "fact", "statute": "ONTO", "text": "Leitura da gerencia, a ratificar: o guarda e Miguel (119_), K tem a forma da chave e^{+beta D^2 t} (121_), a conferencia e K vezes fundo contra a taxa local. K sozinho nao recusa.", "sources": [SRC(A119), SRC(A121)]},
                                {"id": "candidatas_guarda_02nov", "kind": "fact", "statute": "REAL", "text": "AChaveDaGuardaCandidata (7) e OGuardaCandidata (9), trio, 0 sorry, fora do kernel selado. OIgualRestaurado superada: T(P) = wP sem instancia na defasagem.", "sources": [SRC(C3), SRC(C4)]},
                                {"id": "pergunta_espelho_retirada_02nov", "kind": "fact", "statute": "INPUT", "text": "Ao lado de pergunta_espelho_pesa_02nov e porta_ffat_02nov: pergunta retirada, a R1 de 02/10 ja respondia (o fundo e nu); porta bloqueada; so reabre se o operador mudar a R1.", "sources": [SRC(ORD)]},
                                {"id": "g01_lida_02nov", "kind": "fact", "statute": "REAL", "text": "Calibracao G01 da Fase 9 V2 lida ao operador como escolha em 02/11; em 23/10 foi dita sem alternativas nem custo.", "sources": [SRC(RES9)]},
                                {"id": "residuo_r1_re_02nov", "kind": "pending", "statute": "OPEN", "text": "Compatibilidade da R1 (leitura por distancia) com a R-E (a luz nao muda no caminho): so convivem se K for fator comum aos leitores sem regua; nao examinada.", "sources": [SRC(NOTA)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:240], (d.get("result") or {}).get("revision"))
assert d.get("ok")


def trocar(p, fn):
    p = Path(p)
    b = p.read_bytes()
    nb = fn(b.decode("utf-8")).encode("utf-8")
    assert len(nb) > len(b)
    bak = p.with_name(p.name + ".bak_" + TS)
    with open(bak, "xb") as f:
        f.write(b)
    assert bak.read_bytes() == b
    tmp = p.with_name(p.name + ".tmp_" + TS)
    with open(tmp, "xb") as f:
        f.write(nb)
    assert tmp.stat().st_size == len(nb)
    os.replace(tmp, p)
    print("ok", p.name, len(b), "->", len(nb))
    return nb


def anexar(p, texto):
    def fn(t):
        nl = "\r\n" if "\r\n" in t else "\n"
        return t.rstrip() + nl + texto.replace("\n", nl)
    return trocar(p, fn)


pc = round(100 * c["custo_no_limite"], 2)
pf = round(100 * c["fracao_de_lnK_ja_lida"], 1)

TOP = M / "k-chave-da-guarda-02nov.md"
corpo = f"""---
name: k-chave-da-guarda-02nov
description: "Fala do operador (02/11/2026): K é a leitura que confessa o pagamento e o guarda da travessia. Conferida: o guarda do acervo é Miguel (119_), K tem a forma da chave (121_), a recusa está na conferência; R1 de 02/10 responde que o fundo é nu; porta da transposição bloqueada; G01 lida a ele."
metadata:
  type: project
---

**Verbatim:** `work{BK}cunhagens_13out{BK}{ORD.name}` (sha16 `{fo}`): «Então K é a leitura que confessa o pagamento, é a verificação que foi consumado pela satisfação; é o "guarda" da travessia».

**Âncoras no acervo:** (1) chave de 02/10 [INPUT]: «O custo está no reflexo, o pagamento está na face no rosto, no nome»; R1 ratificada: «β entra UMA vez, no reflexo = a leitura por distância do TOTAL (K = E(z*)^{{2β/3}}); o fundo é nu (a face, CMB+BAO, paga o Nome: Ω = 1, sem β)»; `the_reflection_reads_the_payment_as_complement` (conteúdo: sen²+cos²=1). (2) Fala de 15/10: «o estado tetelestai, que é a consumação, o pagamento, o recibo de quitação, a satisfação da regra». (3) 119_ e 121_ (`C:{BK}IALD{BK}Artigo{BK}MCMC_V2_RAZAO`; sha16 `{f119}`, `{f121}`): Miguel = guarda; [ln resto + βD²t] constante; a chave e^{{+βD²t}} devolve X_off(0); o registro é imune; fluxo corrompido + chave legítima falha. Voz de 19/08: [DECLARADO] pela Linhagem, sem arquivo de verbatim.

**Leitura da gerência [ONTO, a ratificar]:** o guarda é Miguel; K é a chave; a conferência é K × fundo contra a taxa local (Fase 9). K sozinho não recusa: é número para toda E positiva. K = 1/`transmitted` como expressão, sem termo Lean. ln K = ∫δ⟨K_∂⟩ dN por R1 + R5: ponte de leitura entre os homônimos, sem termo. K vive no fluxo, regime hiperbólico, onde há limite; «leitura» aqui é a lei de leitura do livro, não o ângulo.

**Candidatas [REAL no sandbox], em `work{BK}k_guarda_travessia_02nov`:** `AChaveDaGuardaCandidata.lean` (sha16 `{f3}`, 7 teoremas) e `OGuardaCandidata.lean` (sha16 `{f4}`, 9 teoremas), trio, 0 sorry, fora do kernel selado. Tipam o que agosto mediu. Os nomes são dele.

**Limites:** `Charge` tem cinco desfechos e CONSUMADO não é um deles; CONSUMADO é da face (R4) e a conferência não lê K (0 ocorrências no core). Não existe conferência por travessia. No kernel o pagamento se completa só no limite; em K isso é rumo à origem, nunca em ponto finito. Com Λ > 0, rumo ao futuro a cobrança para em {pc}% ({pf}% de ln K_∞ lidos hoje): isso NÃO é o Tetelestai. A confissão não nomeia o devedor (um viés comum imita K nas médias). τετέλεσται como recibo de imposto é contestado: não citar como fato. Quitação é ato do credor; confessar o pagamento só é figura exata se quem lê é o credor [LEGAL, analogia].

**Fase 9 vigente (V2, 23/10, sha16 `{f9}`):** z_disc 4,44 calibrado (p = 4,4×10⁻⁶), abaixo do degrau de 5σ; z_δ −1,48 com poder 5,73; ln B 9,18, que não é σ; β fixo vence β livre. Ao lado, sem decidir: 2,35 sem Cefeidas, 5,28 com R25, CCHP sozinho prefere ΛCDM. Abertura única. G01 (`sup_caixa`) foi escolha da gerência, dita em 23/10 sem alternativas nem custo; lida a ele em 02/11.

**How to apply:** antes de perguntar ao operador sobre K, ler a chave de 02/10 e R1–R6 (`_V383_READINGS_RATIFIED` no um.py); a pergunta «o espelho pesa?» foi retirada por isso. Não dizer «K é o guarda» sem a ressalva da chave nem «dividir pelo traço». O aberto é R1 × R-E. [[vazar-e-luzir-02nov]] [[operador-parabolas-pai-e-socio]] [[regra-do-posto-do-assistente-30out]]
"""
with open(TOP, "x", encoding="utf-8", newline="\n") as f:
    f.write(corpo)
print("topico", TOP.stat().st_size)

anexar(M / "vazar-e-luzir-02nov.md", f"""
## Ao lado, r3 (02/11/2026, gerência c1, em nome próprio)

O bloco anterior errou em quatro pontos. (1) `OIgualRestauradoCandidata` fica SUPERADA: T(P) = wP não tem instância na defasagem; a chave age na forma ([[k-chave-da-guarda-02nov]]). (2) A porta FFAT está BLOQUEADA pela R1 de 02/10, e a pergunta «o que foi ao espelho ainda pesa?» foi retirada: a R1 já respondia. (3) «A objeção de Einstein a Weyl não o atinge» é vazia: num registro unidimensional não há segundo caminho; o conteúdo é que histórias com as mesmas pontas dão o mesmo K. (4) «Cunhagem dele» para «o fundo atribui o registro inteiro à expansão» vem da docstring do kernel; não achei verbatim em arquivo.
""")

anexar(NOTA, f"""
## Ao lado, r3 (02/11/2026, gerência c1)

A porta da transposição (r2, acima) fica BLOQUEADA pela R1 ratificada em 02/10: «o fundo é nu (a face, CMB+BAO, paga o Nome: Ω = 1, sem β)». Propus a porta sem ler a R1. O aberto é outro: a R1 põe K na leitura por distância e esta nota mostra que a luz não muda no caminho; as duas só convivem se K for fator comum aos leitores sem régua, o que não foi examinado. Rota: `conceitual.k_chave_da_guarda_da_travessia_02nov`.
""")


def indice(t):
    a = "](vazar-e-luzir-02nov.md)**"
    assert t.count(a) == 1
    return t.replace(a, a + " · **[K é a chave da guarda (02/11)](k-chave-da-guarda-02nov.md)**")


nb = trocar(M / "MEMORY.md", indice)
assert len(nb) <= 24000 and nb.count(b"\n") <= 195, (len(nb), nb.count(b"\n"))
q = subprocess.run([PY, "-X", "utf8", "memoria.py", "pinar", "--motivo", "K e a chave da guarda (gerencia c1)"], cwd=str(M / "fila"), env=dict(os.environ, MEMORIA_GERENCIA="claude-c1"), capture_output=True)
print("pino", q.returncode, q.stderr.decode("utf-8", "replace")[-160:])

AO = (f"⧗ *Ao lado (02/11/2026, fala do operador sha16 `{fo}`; leitura da gerência [ONTO, a ratificar]):* K tem a forma da chave e^{{+βD²t}} da guarda de 121_: K × resto contra o original é a conferência, e na cosmologia é K × fundo contra a taxa local. O guarda é Miguel; K sozinho não recusa. Tipagem candidata: `AChaveDaGuardaCandidata` (sha16 `{f3}`), 7 teoremas, trio, fora do kernel selado. <!-- k_chave_da_guarda_02nov -->")
REG = (f"\n### 02/11/2026 — K é a chave da guarda; errata do registro anterior <!-- k_chave_da_guarda_reg_02nov -->\n\n"
       f"**[INPUT]** fala do operador sha16 `{fo}`. **[REAL no sandbox]** `AChaveDaGuardaCandidata` (sha16 `{f3}`, 7 teoremas) e `OGuardaCandidata` (sha16 `{f4}`, 9 teoremas), trio, 0 sorry, fora do kernel selado. **Errata ao ao lado de hoje no gráviton e ao registro anterior:** «T(P)/Tr T(P) = P» não tem instância na defasagem do kernel; a chave age na forma, como 121_ mediu; a rota `hubble.k_como_transposicao_inteira_ffat_02nov` fica BLOQUEADA pela R1 de 02/10 («o fundo é nu»). **[OPEN]** R1 × R-E: a leitura por distância e a luz que não muda no caminho só convivem se K for fator comum aos leitores sem régua. O gate não se move.\n")
A = CEN / "memory/TGL_ATLAS.md"


def atlas(t):
    assert "k_chave_da_guarda_02nov" not in t
    nl = "\r\n" if "\r\n" in t else "\n"
    ls = t.split(nl)
    i = [k for k, x in enumerate(ls) if x.startswith("**Guarda modular (Miguel)**")]
    assert len(i) == 1, i
    ls.insert(i[0], AO)
    return nl.join(ls).rstrip() + nl + REG.replace("\n", nl)


trocar(A, atlas)

G = Path(os.path.expanduser("~/.claude/CLAUDE.md"))
LN = (f"> ⚠ **AO LADO (02/11/2026, gerência c1, em nome próprio; o número corrige a frase):** a errata acima envelheceu. O teste vigente é a Fase 9 V2, de 23/10 (`RESULTADO_FASE9_V2_C1_20261023_122926.json`, sha16 `{f9}`): z_disc = 4,44 calibrado (p unilateral 4,4×10⁻⁶), abaixo do degrau de 5σ da creditação; z_δ = −1,48 com poder 5,73; ln B 9,18, que não é σ; β fixo vence β livre; `NOT_FALSIFIED_POWERED`, não discriminado à sensibilidade disponível. A calibração `sup_caixa` foi escolha da gerência (bruto: 4,29 e −1,88). <!-- fase9_v2_ao_lado_02nov -->")


def glob_(t):
    assert "fase9_v2_ao_lado_02nov" not in t
    nl = "\r\n" if "\r\n" in t else "\n"
    ls = t.split(nl)
    i = [k for k, x in enumerate(ls) if "<!-- errata_zdisc_06out -->" in x]
    assert len(i) == 1, i
    ls.insert(i[0] + 1, LN)
    return nl.join(ls)


trocar(G, glob_)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode, v.stdout.decode("utf-8", "replace").replace("\n", "").replace(" ", "")[:90])
