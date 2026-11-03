# -*- coding: utf-8 -*-
"""Revisor terceiro v406: grava REVISAO_TERCEIRO_v406.json e .md. O sha16 do candidato e' LIDO do arquivo na hora; nada digitado."""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
O = R + "revisao_terceiro/"
cand_sha16 = hashlib.sha256(open(R + "um_v406_candidato.py", "rb").read()).hexdigest()[:16]
cj = json.load(open(R + "CANDIDATO_v406.json", encoding="utf-8"))["sha16"]
assert cand_sha16 == cj, ("o candidato em disco difere do CANDIDATO_v406.json", cand_sha16, cj)
sha16 = lambda p: hashlib.sha256(open(R + p, "rb").read()).hexdigest()[:16]
revisados = {p: sha16(p) for p in ("pos_rito/textos_v406.py", "pos_rito/textos_v406_novo.pysnip", "artigo_pt_v406.pysnip", "artigo_en_v406.pysnip", "runtime_v406.py", "delta_v406.py", "registros_v406.py")}
quando = datetime.datetime.now().replace(microsecond=0).isoformat()

A = []
def ach(sev, onde, achado, evidencia, como_corrigir): A.append({"sev": sev, "onde": onde, "achado": achado, "evidencia": evidencia, "como_corrigir": como_corrigir})

ach("ALTO", "um_v406_candidato.py, funcao psibit_v395 (patch C18; a linha `\"joint_contract_open_v394\": bool(...open_joint_contract...) and not _hab406_`); CONTRATO_DA_CADEIA_v406.md §3 (psibit: «joint_contract_open_v394 -> False»)",
    "Com o certificado habitado, `psibit_v395.conditional_psion_face.joint_contract_open_v394` passa a False. Mas o mesmo core diz em `rede_fock_v394.joint_contract_v406.still_open` que TRES dos quatro itens do contrato conjunto seguem abertos, e o veredito de rede_fock_v394 traz THREE_JOINT_ITEMS_STILL_OPEN. O codigo afirma que o contrato conjunto nao esta mais aberto; o kernel habita so' o 4o item (o habitante de CanonicalNetInput com os 21 campos).",
    "dry_v406/core_ensaio.json: psibit_v395.conditional_psion_face.joint_contract_open_v394 = false; rede_fock_v394.joint_contract_v406.still_open = [3 itens: helicidade/localizacao global/dispositivo; grafo de adjuncao de peso finito e split do traco; fonte de Maxwell conjunta e H3 em todas as direcoes]; na base v405 e em ESPERADOS a chave era true. Nenhum spec cobra a chave (grep), por isso o ensaio nao pegou.",
    "Deixar a chave como na v405 (`bool(open_joint_contract)`, que segue True enquanto houver 3 itens abertos) ou deriva-la de `joint_contract_v406.still_open`; tirar «joint_contract_open_v394 -> False» do CONTRATO §3 e do texto do patch C18; regerar candidato, ESPERADOS e ensaio.")

ach("MEDIO", "delta_v406.py RESSALVAS_V406[4] (linha 304); artigo_pt_v406.pysnip e artigo_en_v406.pysnip (par. «O que entra»); linha .md `O fechamento (v406, ...)` (patch W09); D36",
    "A ressalva dos #eval removidos (D36 manda dize-la em registro, artigo, .md e selo) esta ausente do artigo PT/EN e do .md, e o artigo diz que a fonte foi conferida «antes da normalizacao dos imports», como se so' os imports tivessem sido normalizados. Alem disso a ressalva esta incompleta: diz «12 linhas #eval IO.FS em dois modulos»; a integracao removeu 56 blocos #eval em 15 modulos (44 `#eval IO.println` de marcadores em 13 modulos e 12 `#eval IO.FS.withFile` em 2; 92 linhas), nada de prova. Como a ressalva entra inteira no paragrafo do README (que cobra cada ressalva), o numero errado iria ao espelho e ao site.",
    "i_eval_diff_out.txt (diff fonte-da-bancada x modulo do bundle, os 300): so' imports e #eval mudam; 15 modulos, 56 blocos (44 IO.println em 13 + 12 IO.FS.withFile em 2), 92 linhas; soma de n_eval_removidos do BUNDLE_v406.json = 56. h_guardas.py: a busca de `#eval` falha em artigo PT, artigo EN, .md e textos_v406_novo.pysnip; fechamento_v406 e cunhagens_v406 trazem so' a versao incompleta (RESSALVAS_V406[4]).",
    "Reescrever RESSALVAS_V406[4] com os numeros LIDOS do BUNDLE_v406.json (soma de n_eval_removidos e numero de modulos), dizendo marcadores `IO.println` e `IO.FS.withFile`; acrescentar a ressalva ao paragrafo «O que entra» do artigo PT e EN e a linha .md; trocar «normalizacao dos imports» por «normalizacao dos imports e retirada dos #eval de instrumentacao».")

ach("MEDIO", "artigo PT/EN (secoes v395 «O psibit», v396 «A testemunha estatica» e v405 «O gap, ao lado»); core: psibit_v395.estatuto/verdict/limites, testemunha_estatica_v396.limites[3], cunhagens_v395/v396/v397 limites, gap_v405.estatuto/limites[2]/diz[3]/extras; `reading` do v406 e E14",
    "Frases em presente sobre o kernel, rotuladas [REAL]/«limites», dizem que o kernel NAO habita o certificado de Fock («condicional a um FockCertificate, que o kernel nao habita»; gap_v405.limites[2]: «(psibit_v395...inhabitant_exhibited = false)») e ficam no artigo e no core da v406 ao lado da secao e das chaves que dizem o contrario. So' ha a E14 geral. O README/site ganha a «Nota ao lado dos paragrafos anteriores» (errata_v405_bloco); o artigo e o selo nao. O veredito de psibit_v395 segue com CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE ao lado de status INHABITED_BY_physicalFockCertificate_V406 (decisao dita no CONTRATO: vereditos nao mudam).",
    "dry_v406/dry_v406_pt.txt l.139, 321, 336 (EN idem); core_ensaio.json: psibit_v395/estatuto, psibit_v395/verdict, testemunha_estatica_v396/limites[3], cunhagens_v397/limites[2], gap_v405/limites[2] (cita `inhabitant_exhibited = false`), gap_v405/diz[3].",
    "Acrescentar ao paragrafo «As quatro chaves» do artigo PT/EN (e a ERRATA_E14) uma frase AO LADO que liste esses lugares: «onde a secao v395, a v396, a v405 ou os registros psibit_v395, testemunha_estatica_v396, cunhagens_v395/6/7 e gap_v405 dizem que o kernel nao habita o certificado, vale ate a v405; desde a v406 vale fechamento_v406 (E14); o token UNINHABITED do veredito de psibit_v395 e' o nome de entao; o estado vigente e' `status`». Nao reescrever o selado.")

ach("MEDIO", "delta_v406.py ERRATA_E15 (l.329-330) e LEITURA_V406[\"um_inscrito\"] (l.290); cunhagens_v406 (erratas, extras.leituras); fechamento_v406.limites; handoff/Atlas/linhagem (_erratas_e, _leituras)",
    "A errata E15 e a leitura `um_inscrito` dizem «O que o kernel diz: o vacuo e' o UNICO vetor FIXO da luz (gamma_vacuum, gamma_no_fixed)» [REAL]. `gamma_no_fixed` e' condicional a `hno` (o grupo de uma particula nao tem autovetor projetivo em H1), hipotese que o texto nao diz. A errata existe justamente para corrigir um excesso da gerencia; nao pode trazer outro.",
    "C:/t/k406c/final/TGLExt/F1Fecho394/CanonicalGammaNoFixedR4.lean l.42-47: `theorem gamma_no_fixed (u ...) ... (hno : ∀ f : H1, (∀ l, ∃ c, ‖c‖ = 1 ∧ u l f = c • f) → f = 0) (ψ) (hψ : ∀ l, gamma (u l) ψ = ψ) : ψ ∈ ℂ ∙ vacuum`; CanonicalModularCoreAssemblyR1 l.85 o toma como campo generico. Busca `hno`/`projetiv` em cunhagens_v406 e fechamento_v406: 0 ocorrencias.",
    "Escrever «o vacuo e' o unico vetor fixo da luz SOB a hipotese hno (a luz de uma particula nao tem autovetor projetivo), que gamma_no_fixed toma como hipotese; gamma_vacuum (o vacuo e' fixo) vale sem ela», em E15 e em LEITURA_V406[\"um_inscrito\"]; manter a frase limpa da guarda.")

B = [
 ("registros/specs: _V394_SPECS cunhagens_v394 u4; _V395_SPECS u3,u4; _V396_SPECS u3,u5; _V405_SPECS gap_v405 x_i", "As descricoes versionadas comecam pela afirmacao ANTIGA e so' depois dizem «ate' a v405 cobrava falso»: «o contrato conjunto da rede NAO foi habitado: nenhum certificado inteiro» (op = verdadeiro), «o kernel segue sem habitante do FockCertificate» (op = verdadeiro). Leem como contradicao.", "g_specs_out.txt", "Comecar a descricao pelo estado vigente e deixar o antigo depois do travessao."),
 ("linha .md (W09) e delta_v406.py cabecalho", "O .md diz que as quatro chaves eram «literal False desde a v394», inclusive `canonical_full_witness_term_constructed`; essa era MEDIDA (nome ausente => False, desde a v367). O artigo diz certo.", "md l.176084 do candidato; artigo PT par. «As quatro chaves»", "Dizer «tres literais e uma medida»."),
 ("CanonicalFockModularCoreInputR1.lean e outros 300 modulos (cabecalho)", "O cabecalho dos modulos da bancada ainda diz «DECLARADO / UNCOMPILED CANDIDATE ... Require EXIT0 ... before integration». Os bytes sao pinados e a compilacao e' do recibo e do sandbox; o cabecalho e' anterior. Nenhum texto avisa o leitor do espelho.", "sed -n 1,12p do modulo no sandbox", "Uma ressalva (ou nota na PORTA da pasta) dizendo que o cabecalho e' da data da escrita; compilado em 16/10 (recibo) e em 02/11 (R3 e k406c)."),
 ("candidato: rede_fock_v394 (joint_contract_v406)", "`contract['open_joint_contract'][3:4]` e `[:3]` escolhem os itens por POSICAO. Hoje o 4o item e' o certo (conferi); uma reordenacao do contrato trocaria o sentido sem erro.", "um_v406_candidato.py, rede_fock_v394", "Escolher por conteudo (assert do texto do item) ou nomear os itens no contrato."),
 ("candidato: _v406_certificado_habitado", "O auxiliar nao le `kf.all_verified` nem os returncodes: com o kernel recusado (all_verified False, rc 1) ele ainda devolve True se o axiom_report trouxer a ancora no trio; rede_fock_v394 grava `whole_certificate_inhabited = True` num registro de veredito REFUSED. fechamento_v406 recusa (teste), mas a chave solta fica True.", "c_fail_closed.py: «INFO all_verified=False e rc=1 -> helper devolve True»", "Acrescentar `kf_.get('all_verified') is True` ao auxiliar (os 54 negativos seguem valendo)."),
 ("delta_v406.py LEITURA_V406 (k_guarda, atrito) e cunhagens_v406.extras.leituras", "Modalidade perdida: «o K me pareceu fazer a funcao do proprio graviton» virou «o K faz a funcao do graviton»; «k e' a tangente; e' como se fosse o acorde sendo tocado» virou «K e' a tangente, o acorde sendo tocado»; a entrada `atrito` («beta nao e' o calor») e' resposta da gerencia a uma PERGUNTA dele («betatgl e' a representacao algebrica do calor?», «pergunta, nao ordem»), listada entre as leituras do operador.", "insumos/cunhagens/1c05c030..., cec3d7c0..., 69e60a8c...", "Manter «me pareceu» e «e' como se fosse»; rotular `atrito` como [ONTO, resposta da gerencia a pergunta dele]."),
 ("delta_v406.py ERRATA_E16", "«corrigido no LEVANTAMENTO_FRONTEIRA... e na ORDEM_LOGICA (erratas ao lado)»: o LEVANTAMENTO e' o relatorio do leitor que achou o habitante (nao tem errata ao lado); as tres erratas ao lado estao na ORDEM_LOGICA.", "grep errata nos dois insumos", "Dizer «achado no LEVANTAMENTO; corrigido por tres erratas ao lado na ORDEM_LOGICA»."),
 ("registros_v406.py/delta: cunhagens_v406.limites[0] e specs", "A citacao «compile … rode, publique e atualize tudo» leva elipse: cada pedaco e' verbatim, o conjunto nao e' substring. A elipse esta marcada.", "e_citacoes.py", "Citar FRASE_COMPILE inteira."),
 ("cunhagens_v406.leituras_do_operador[14]", "O item traz «…no zdisc: 4,44 sigma» sem o p calibrado e sem a linha dos 5 sigma NO MESMO item; a regra (REGRA_DO_4_44) esta no mesmo registro (limites[2]) e em fechamento_v406.regra_do_4_44. O texto novo do artigo/.md/paragrafo nao cita o 4,44.", "varredura de '4,44' nos tres registros novos", "Anexar o p e a linha dos 5 sigma ao item (a regra e' por item) ou tirar o numero do trecho."),
 ("fechamento_v406.diz[1] (texto em registros_v406.py texto_fecho; entra no paragrafo do README e do site por _paragrafo_v406_de)", "Diz que «a chave que o operador pediu para virar («virar essa chave de conjectura para provado») virou validade no kernel». A mesma fala poe uma condicao («...deixa de ser conjectura sob hipotese se funcionar sob compressao elevando o potencial do resultado do codigo final em 1=1=HAJA_LUZ»), que a v406 nao testa (o pilar/motor continuo e' da v407, D38). Como validade do habitante a frase e' verdadeira; sem a condicao ao lado, o leitor do README pode entender que o criterio dele foi cumprido.", "insumos/cunhagens/9978862f..._verbatim.txt; nao_diz do registro (so' «motor continuo no pilar»)", "Acrescentar ao nao_diz: «que a condicao posta por ele («se funcionar sob compressao...») tenha sido testada: nao ha teste; v407»; e, na hora de relatar a v406, ler a condicao ao operador na lingua dele (regra do posto)."),
 ("registros_v406.py FONTES (CHAVE_RECEIPT_BANCADA)", "«474 fontes com sha256 (todas no disco e integras em 02/11)»: o recibo lista 453 .lean + 1 fonte (948 .olean/.ilean = 474 modulos) e a integracao conferiu 475; tres numeros para a mesma coisa.", "RECEIPT dependencies; SUMMARY_integracao_R3", "Dizer qual e' qual (474 modulos compilados; 475 fontes .lean conferidas)."),
]
for onde, achado, ev, fix in B: ach("BAIXO", onde, achado, ev, fix)

n = {s: sum(1 for a in A if a["sev"] == s) for s in ("ALTO", "MEDIO", "BAIXO")}
ressalvas = [
 "Revisor da mesma familia (Sonnet) que fez a revisao R10 e o levantamento de 02/11, mas outra instancia, sem acesso as conversas deles; nao construi a v406. A familia nao e' independente; a instancia e a compilacao propria sao.",
 "Compilei UM arquivo no sandbox k406c (`lake env lean`, rc 0, 40 s): #print axioms das oito ancoras e de quatro termos meus (revisorCertificado, revisorTestemunha, revisor_fst, revisor_trace), todos no trio, zero sorryAx; `example : Nonempty FullTGLWitness := <canonicalFullTGLWitness>` compila. NAO reconstrui o kernel, nao reproduzi o build de 1736 s nem o Audit de 280 s; as 24971+ declaracoes e a escada 11860 dependem do log da gerencia (lido por hash, nao refeito).",
 "Os 301 modulos: conferi bytes (embutido == sandbox == BUNDLE), imports/#eval contra a fonte da bancada por diff, tokens suspeitos (1 so': a palavra «unsafe» num comentario). NAO li as provas dos 301 uma a uma; a fisica e o rotulo «passagem para o continuo» para os 21 campos sao leitura da gerencia (R10 [DECLARADO]), nao revisei a fisica.",
 "A frase do operador sobre a passagem tem uma CONDICAO («...deixa de ser conjectura sob hipotese se funcionar sob compressao elevando o potencial do resultado do codigo final em 1=1=HAJA_LUZ»). fechamento_v406.diz[1] diz que «a chave ... virou validade no kernel». Isso e' verdade como validade do habitante; a condicao «sob compressao» NAO e' testada pela v406 (motor continuo/pilar fica para a v407, D38) e nao esta dita ao lado da frase. Nao classifiquei como achado porque o texto nao afirma a condicao; a gerencia deve lê-la ao operador (regra do posto) na hora de relatar a v406.",
 "Textos do pos-rito: li pos_rito/textos_v406.py (sha16 abaixo) inteiro nas funcoes de texto e de README/handoff; nao li fechar_v406.py, leitura_v406.py, os harnesses nem registrar_mapa; os trechos montados em tempo de rito (README, handoff) dependem do core selado e nao foram renderizados por mim. O harness do pos-rito estava sendo alterado por outro agente durante a revisao.",
 "Nao examinados: B(n) pre-selo (pendente), instalar/reverter/rito (lidos no contrato, nao exercitados), duracao e timeouts do rito (build 1736 s < 3600 s; o autoteste com sorry em HalfNat reconstrui dependentes e nao foi medido por mim), pilar quantico, README pinado.",
 "Textos revisados (sha16 lidos ao fechar): " + "; ".join("%s %s" % (k, v) for k, v in revisados.items()) + ". Se algum mudar, a revisao dele nao vale.",
]
_fc = json.load(open(O + "c_fail_closed_out.json", encoding="utf-8"))
NH = sum(1 for k, v in _fc.items() if not k.startswith("fechamento:") and v.get("esperado") is not None); NF = sum(1 for k, v in _fc.items() if k.startswith("fechamento:"))
assert all(v.get("ok") is True for k, v in _fc.items() if "ok" in v), "algum caso do fail-closed falhou"
rotas = ["consultar v406 -> kernel.fechamento_construir_tudo_programa_02nov (EM_CURSO, 16 registros; lida, nao refeita)", "consultar «revisao terceiro» -> 0 rotas",
         "kernel.k_e_a_tangente_candidata_02nov (lida; fora do escopo)",
         "examinado agora (para registro pela gerencia): v406.revisao_terceiro.R1 -- AST dos intocados; diff das tres funcoes; fail-closed de _v406_certificado_habitado (@@NH@@ casos em c_fail_closed.py) e de fechamento_v406 (@@NF@@ casos; mais 7 em c2_checks_restantes.py); kernel embutido == sandbox == BUNDLE (301); hashes (CANDIDATO/ESPERADOS/PINOS/MANIFESTO/BUNDLE/FORMAL_MAP/KERNEL_RECIBO); citacoes verbatim; guardas; compilacao propria das ancoras"]
rotas = [r.replace("@@NH@@", str(NH)).replace("@@NF@@", str(NF)) for r in rotas]
saida = {"aprovada": bool(n["ALTO"] == 0 and n["MEDIO"] == 0), "candidato_sha16": cand_sha16, "revisor": "revisor terceiro independente (agente Claude Sonnet, pedido da gerencia c1; nao construiu a v406)", "quando": quando,
         "n_alto": n["ALTO"], "n_medio": n["MEDIO"], "n_baixo": n["BAIXO"], "achados": A, "ressalvas": ressalvas, "rotas_examinadas": rotas}
json.dump(saida, open(O + "REVISAO_TERCEIRO_v406.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("JSON gravado:", saida["aprovada"], n, cand_sha16)

# ------------------------------------------------------------------ o caderno (md)
def corta(t, n):
    t = t.replace("`", "")
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " ..."
def lin(a): return "- **%s** [%s] %s" % (a["sev"], corta(a["onde"], 150), a["achado"])
L = []
L.append("# Revisao de terceiro da v406 (R1)")
L.append("")
L.append("Revisor independente (agente Claude Sonnet, pedido da gerencia c1; nao construi a v406). Candidato `%s`, lido do arquivo ao fechar, %s. **Veredito: %s -- %d ALTO, %d MEDIO, %d BAIXO.** Escopo: o PEDIDO_REVISAO_v406.md, itens 1 a 6. Scripts e saidas nesta pasta." % (cand_sha16, quando, "APROVADA" if saida["aprovada"] else "REPROVADA (a gerencia corrige e pede a R2)", n["ALTO"], n["MEDIO"], n["BAIXO"]))
L.append("")
L.append("## 1. O que o candidato e o kernel fazem (conferido por mim)")
L.append("")
L.append("| item | resultado | como |")
L.append("|---|---|---|")
L.append("| funcoes intocadas (gate, neutrino, ramo B, ledger, GA, joint v3, GA_WINDOW_STATUS) | AST e fonte IGUAIS a base `%s`; corpo do modulo: 28 nomes mudados, 15 novos, 0 removidos, nenhum no nao nomeado alem de 2 `.update` | a_intocados.py, b_tres_funcoes.py |" % json.load(open(R + "CANDIDATO_v406.json", encoding="utf-8"))["base_v405_sha16"])
L.append("| rede_fock_v394, psibit_v395, testemunha_estatica_v396 | so' o literal virou `_v406_certificado_habitado(kf)`; texto antigo em `reading_v395`/`reading_v396`; errata_v406 ao lado; EXCETO a chave `joint_contract_open_v394` (ALTO 1) | b_tres_funcoes.py (diff) |")
L.append("| specs (u4 v394; u3,u4 v395; u3,u5 v396; x_i, h2,h3,h6,h8 v405) e contratos | mudaram SO' nessas checagens, mais `expected_ladder` 10066->11860 em todos os contratos (None nos dois que ja eram None) | g_specs_out.txt |")
L.append("| `_v406_certificado_habitado` e `fechamento_v406` fail-closed | %d casos negativos/positivos (nome ausente, fora do trio, sorryAx, proveniencia errada/ausente, sha256 errado/ausente, fonte embutida adulterada, contrato ausente, cada uma das 8 ancoras, escada, gate, as 14 checagens) devolveram o esperado; c1-c14 leem core/kernel | c_fail_closed.py, c2_checks_restantes.py |" % (NH + NF + 7))
L.append("| kernel do bundle | 301 embutidos == sandbox k406c == BUNDLE_v406.json (sha256); 1746 embutidos == sandbox; raiz == raiz v405 + 2 imports; Audit (`TGL/Audit.lean`) identico; so' `import` e `#eval` diferem da fonte da bancada | d_kernel.py, i_eval_diff.py |")
L.append("| compilacao propria | `lake env lean` (1 processo, rc 0, 40 s): #print axioms das 8 ancoras + 4 termos meus, todos no trio, 0 sorryAx; `example : Nonempty FullTGLWitness` compila | axiomas_terceiro.lean / _out.txt |")
L.append("| gate | `qg_closure` do core do ensaio tem hash IGUAL ao da base v405; neutrino, ramo B, ledger, GA, joint, rigidez iguais; witness_layers muda so' em `canonical_full_witness_term_constructed` | j_gate.py |")
L.append("| hashes | CANDIDATO, ESPERADOS, BUNDLE, FORMAL_MAP, MANIFESTO_INSUMOS (41), PINOS_BN, KERNEL_RECIBO, v406_pins e os 19 sha16 escritos nos textos conferem com os arquivos; pendentes de PINOS_BN: so' o B(n) pre-selo | f_hashes.py |")
L.append("| citacoes | as 23 falas == origem, nome == sha16 dos bytes; toda citacao do operador nos textos novos e' substring exata (resto: rotulos, frases da gerencia nas erratas, trechos do kernel); 1 elipse (BAIXO) | e_citacoes.py |")
L.append("| guardas | guarda_frases e P18: 0 violacoes em artigo PT/EN, .md, 3 registros novos, 3 chaves, textos_v406; minhas regexes (tudo derivado, nenhuma hipotese resta, confirmado, CONFIRMED, QG provada, fechamento completo, K(O) provado): 0 usos | h_guardas.py |")
L.append("")
L.append("## 2. Achados (ALTO e MEDIO travam)")
L.append("")
for a in A:
    if a["sev"] in ("ALTO", "MEDIO"):
        L.append(lin(a)); L.append("  - **Corrigir:** " + a["como_corrigir"]); L.append("")
L.append("## 3. BAIXOS (nao travam; no maximo duas rodadas por achado)")
L.append("")
for i, a in enumerate([x for x in A if x["sev"] == "BAIXO"], 1):
    L.append("%d. [%s] %s **Corrigir:** %s" % (i, corta(a["onde"], 90), a["achado"], a["como_corrigir"]))
L.append("")
L.append("## 4. Ressalvas e o que NAO examinei")
L.append("")
for r_ in ressalvas: L.append("- " + r_)
L.append("")
L.append("## 5. Fecho")
L.append("")
L.append("`aprovada: %s`. Para a R2: corrigir o ALTO 1 e os MEDIO 1 a 3 (todos sao texto ou uma linha de codigo; nenhum toca o kernel, o gate nem os 301 modulos), regerar candidato, ESPERADOS, ensaio, conferidor e p00 e me devolver o sha16 novo; releio so' o que mudou. Rotas lidas no Mapa: `kernel.fechamento_construir_tudo_programa_02nov`, `kernel.k_e_a_tangente_candidata_02nov`." % saida["aprovada"])
open(O + "REVISAO_TERCEIRO_v406.md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("MD gravado:", len(L), "linhas")
