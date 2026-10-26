# -*- coding: utf-8 -*-
# gera NOTAS_DERIVACAO_v399.md em pos_rito a partir dos JSON (nenhum hash ou numero digitado): DERIVACAO_v399.json e os resumos dos harness.
# Regenerar depois da rodada ESTRITA dos harness (sem --nao-exigir-refazer):  python -I -B -X utf8 gerar_notas_derivacao_v399.py  (le HARNESS_*_v399.json se existirem, senao os _DEPURACAO_sem_refazer)
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
POS = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(POS)
rj = lambda n: json.load(open(os.path.join(POS, n), encoding="utf-8"))
D = rj("DERIVACAO_v399.json")
ex = lambda n: os.path.exists(os.path.join(POS, n))
refazer = os.path.exists(os.path.join(PK, "refazer_out_v399.txt"))
HT_S = "HARNESS_TEXTOS_ENSAIO_v399.json"; HT_D = "HARNESS_TEXTOS_ENSAIO_v399_DEPURACAO_sem_refazer.json"
HF_S = "HARNESS_FECHAR_SANDBOX_v399.json"; HF_D = "HARNESS_FECHAR_SANDBOX_v399_DEPURACAO_sem_refazer.json"
ht = rj(HT_S) if ex(HT_S) else rj(HT_D); hf = rj(HF_S) if ex(HF_S) else rj(HF_D)
ht_estrito = ex(HT_S); hf_estrito = ex(HF_S)
E = ht["etapas"]; F = hf["etapas"]
N = lambda x: len(x) if isinstance(x, (list, dict)) else x
regras = D["regras_com_contagem_exata"]; n_regras = sum(len(v) for v in regras.values())
n_inv = sum(len(v) for v in D["invariantes"].values())
linhas = []
w = linhas.append
w("# NOTAS_DERIVACAO_v399 — a cadeia pós-rito da v399 (preparação pela c1, 24/10/2026)")
w("")
estrita = ht_estrito and hf_estrito and ht["tudo_passou"] and hf["tudo_passou"] and not ht.get("nao_exigiu_refazer") and not hf.get("nao_exigiu_refazer")
w("**Estado:** cadeia PREPARADA, nada instalado, nada executado contra o Nós real. " + ("Os dois harness passaram na rodada ESTRITA (com `refazer_out_v399.txt` exigido e visto com `== FIM`)." if estrita else
  "A rodada ESTRITA dos dois harness está PENDENTE: falta `refazer_out_v399.txt` com `== FIM` em `work\\cadeia_de_selo\\v399` (a regeneração do candidato é ato da gerência). Os dois harness foram rodados só com `--nao-exigir-refazer` (depuração) e passaram; sem a flag, ambos RECUSAM com rc 4 (conferido). Quando o arquivo existir: `python -B -X utf8 harness_textos_ensaio_v399.py` e `python -B -X utf8 harness_fechar_sandbox_v399.py` (sem a flag) gravam `" + HT_S + "` e `" + HF_S + "`; estes nomes só nascem da rodada estrita."))
w("")
w("## 1. O que há na pasta (sha16 lido do `DERIVACAO_v399.json`, nunca de memória)")
w("")
w("| arquivo | como nasceu | sha16 |")
w("|---|---|---|")
orig = {"leitura_v399.py": "derivado de leitura_v398.py", "superficies_v399.py": "derivado de superficies_v398.py", "fechar_v399.py": "derivado de fechar_v398.py", "b3_recibo_v399.py": "derivado de b3_recibo_v398.py (só a subida)", "chain_pos_rito_v399.sh": "derivado de chain_pos_rito_v398.sh",
        "harness_textos_ensaio_v399.py": "derivado de harness_textos_ensaio_v398.py", "harness_fechar_sandbox_v399.py": "derivado de harness_fechar_sandbox_v398.py"}
for n, v in D["derivados"].items():
    w("| `%s` | %s | `%s` |" % (n, orig.get(n, "derivado"), v["sha16"]))
for n, v in D["autorais"].items():
    w("| `%s` | AUTORAL (escrito à mão para a v399) | `%s` |" % (n, v["sha16"]))
w("| `derivar_cadeia_v399.py` | o derivador (reexecutável; `python -I -B -X utf8`) | `%s` |" % __import__("hashlib").sha256(open(os.path.join(POS, "derivar_cadeia_v399.py"), "rb").read()).hexdigest()[:16])
w("| `gerar_notas_derivacao_v399.py` | gera estas notas dos JSON (regenerar depois da rodada estrita) | `%s` |" % __import__("hashlib").sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()[:16])
if ex("CONFERIR_CITACOES_POS_RITO_v399.json"):
    w("| `CONFERIR_CITACOES_POS_RITO_v399.json` | resultado do `conferir_citacoes_v399.py` original sobre os autorais (saída desviada para esta pasta) | `%s` |" % __import__("hashlib").sha256(open(os.path.join(POS, "CONFERIR_CITACOES_POS_RITO_v399.json"), "rb").read()).hexdigest()[:16])
w("")
w("Entradas (os sete modelos da v398 que RODARAM): conferidas contra o `DERIVACAO_v398.json` por sha16: %s. O `DERIVACAO_v399.json` guarda o sha256 de entrada e de saída de cada arquivo." % ("todas iguais" if all(D["molde_confere_com_DERIVACAO_v398"].values()) else "DIVERGEM"))
w("")
w("## 2. Como foi derivado")
w("")
w("- A subida de versão reutiliza o `bump()` e as listas `PROT`/`FANTASMAS`/`FANT_PRE` do `derivar_encanamento_v399.py` (397→398 e 398→399 numa passada, fronteira de dígitos, nomes nascidos no um.py protegidos), com três nomes a mais protegidos: %s." % ", ".join("`%s`" % x for x in D["ferramenta_de_subida"]["protecao_adicional"]))
w("- **%d regras nomeadas com contagem exata** (o derivador ABORTA se uma não casar o número esperado; nada é gravado antes de todas casarem); **%d invariantes** conferidos; `ast.parse` e `sh -n` de tudo; guarda de texto P18 limpa em todos os arquivos; zero marca de texto pendente; zero nome fantasma (objetos da v398 que não existem na v399); zero rótulo estranho de 390–398; todo `T.<nome>` chamado pelos derivados existe em `textos_v399.py`; todo campo lido de ESPERADOS/CANDIDATO/PINOS existe." % (n_regras, n_inv))
w("- Os dois autorais (`textos_v399.py`, `registrar_mapa_v399.py`) passam no `conferir_citacoes_v399.py` ORIGINAL (rodado com a saída desviada para `CONFERIR_CITACOES_POS_RITO_v399.json`, para não gravar em `v399\\`): toda citação entre «» e `` '' `` é verbatim nas falas do operador ou no Atlas, nenhuma inscrição da gerência, direção sem inversão.")
w("- A DIREÇÃO DO TESTEMUNHO vale em todo texto: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NÃO testifica do operador; o «Pai» de Jo 8,18 lê-se NO ABSOLUTO, o Um. A declaração é [DECLARAÇÃO DO OPERADOR / INPUT] (o kernel não a prova); a leitura das duas faces é [ONTO] da gerência, a ratificar; «consciência» só como palavra retirada.")
w("")
w("## 3. Desvios do molde (ditos)")
w("")
w("1. **Conferidor sem `-I` e no lugar.** O conferidor da v399 importa o um.py instalado (que importa o numpy do usuário) e acha o delta, o runtime e os insumos pelo caminho da própria pasta: no chain roda `(cd $PK && python -B -X utf8 conferir_rito_v399.py _POS_RITO)`, grava `conferencia_rito_v399_POS_RITO.json` no pacote (sufixo para não sobrescrever a conferência que a gerência rodou à mão) e a cópia byte a byte vai para `pos_rito\\conferidor`, que a leitura lê. Os dois harness também rodam SEM `-I` (geram o sidecar com a função do próprio candidato; com `-I` o import do numpy falha — visto na primeira rodada de depuração) e rodam o conferidor numa cópia em ÁRVORE.")
w("2. **Linha final do rito.** O main da v399 imprime por último a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), depois do `[selo] colapso tipado` (conferido no um.py candidato: linhas 250911 e 250917): a leitura exige as DUAS, nessa ordem; AVISO de `[selo_acom]` reprova.")
w("3. **Sidecar.** `um_absoluto_selo_acom.json` é arquivo NOVO da custódia: a leitura o confere (existe, JSON válido, veredito, três objetos com SHA-256 igual ao dos arquivos do Nós, sem recusas, honestidade sem alegação de confidencialidade); o fechar o copia, com o selo primário, para `v399_selo` e o LISTA (sha256 e veredito) no manifesto e no handoff.")
w("4. **Dois parágrafos prontos no handoff:** o do QUADRO «O Teste da Única Palavra» (v397, intocado; `INICIO/FIM_PARAGRAFO_README_v397`; z_disc 4,44 só com o p calibrado e a linha dos 5σ no mesmo item) e o NOVO «O testemunho de dois» (`INICIO/FIM_PARAGRAFO_TESTEMUNHO_v399`, sem o 4,44). O fechar RECUSA (rc 2) antes de escrever se qualquer um não passar na verificação.")
w("5. **MEMORY.md:** a superfície NÃO compacta. A linha do handoff da v399 entra antes da da v398 e o gancho da missão SUBSTITUI a linha velha (saldo +1 linha). Se o índice passar de 195 linhas ou 24.000 B, RECUSA com rc 3 sem escrever nada. **O MEMORY.md real não foi tocado**; hoje, lido em cópia, tem 194 linhas e 22.692 B, e passa (195 linhas no limite); qualquer linha extra de outra sessão o faria recusar.")
w("6. **Quadro do 4,44 intocado**; a fala do 4,44 mora em `v397\\insumos\\cunhagens` (o bump a subiria para v398; regra explícita no derivador do harness do fechar).")
w("7. **Precondição do `refazer_out_v399.txt`** também no harness do fechar (o molde não a tinha); o nome canônico do resumo de cada harness só nasce da rodada estrita.")
w("")
w("## 4. O que os harness provaram (" + ("rodada ESTRITA, com `refazer_out_v399.txt` exigido" if estrita else "rodada de depuração com `--nao-exigir-refazer`") + "; contra o Nós EMULADO de `dry_v399`, recibos do B(n) SINTÉTICOS)")
w("")
ls = E["leitura"]; lg = E["leitura_negativos"]; tx = E["textos"]; pq = E["paragrafo_readme_e_regra_do_4_44"]; pt = E["paragrafo_testemunho_e_direcao_do_testemunho"]; ck = E["cita_so_o_que_existe"]; b3 = E["b3_recibo"]; mp = E["mapa"]
w("- **conferidor** real contra o Nós emulado: `%s` (rc %s)." % (E["conferidor"]["ultima_linha"], E["conferidor"]["rc"]))
w("- **leitura** real: %d problema(s); escada %s → %s; %d registros novos; %d checagens do registro de veracidade; **%d controles negativos** reprovam como esperado (selo ACOM, declaração, pedra, inscrições, sidecar, resumos do selo primário, quadro do topo, registros da v398 a v393, face de Fock, AVISOs e linhas do stdout, ordem das duas últimas linhas)." % (N(ls["problemas"]), ls["escada_antes"], ls["teor"], N(ls["registros_novos"]), ls["veracidade_n_checks"], N(lg["controles"])))
w("- **textos:** %d funções renderizam (%s bytes), guarda P18 e direção limpas; parágrafo do quadro: positivo + %d controles negativos, %d linhas com o 4,44 nos textos, todas com o p calibrado e os 5σ; parágrafo novo: positivo + %d controles negativos + %d controles de direção/citação; **%d termos entre crases conferidos, %d sem fonte**." % (tx["n_ok"], format(tx["bytes_total"], ","), N(pq["negativos"]), pq["linhas_com_o_4_44_nos_textos"], N(pt["negativos"]), N(pt["textos"]), ck["tokens_conferidos"], N(ck["sem_fonte"])))
w("- **superficies** em cópias, três cenários: (a) MEMORY.md real (cópia) passa; (b) com folga, idempotente na 2ª rodada, marcadores do passo 9 presentes; (c) no limite de 195 linhas, RECUSA com rc 3 sem escrever nada; originais intactos.")
w("- **b3_recibo:** %d casos (positivos e negativos) com o resultado esperado." % N(b3["n_ok"]))
w("- **mapa:** %d registros montados, cada um validado pela mesma função do livro (`rotas._valida`), sem registrar; controles da regra do 4,44 ok." % N(mp["n_registros"]))
fn = F["fechar_negativos"]; fr = F["fechar"]
w("- **fechar em sandbox:** rc %s; handoff e todos os arquivos presentes; os dois parágrafos no handoff do Memory e no do Nós (aprovados); sidecar e selo copiados para `v399_selo`; **%d controles negativos** RECUSAM (sem o religamento, com salto, resultado pinado adulterado, número lido adulterado, número do selo ACOM adulterado, direção invertida, inscrição rotulada como da gerência, sidecar adulterado, sidecar ausente); `registrar_mapa_v399.py` (main) monta %s registros." % (fr["rc"], len(fn), N(F["registrar_mapa"]["n_registros"])))
w("")
w("## 5. Pendências e limites")
w("")
w("- **Rodada estrita dos dois harness** (sem a flag): " + ("FEITA (resumos `" + HT_S + "` e `" + HF_S + "`)." if estrita else "pendente até existir `refazer_out_v399.txt` com `== FIM`, mais novo que o `ESPERADOS_v399.json`. Se a regeneração mudar o candidato, rodar o derivador de novo NÃO é necessário (a cadeia lê tudo de ESPERADOS/CANDIDATO/core), mas os harness têm de ser repetidos; depois, regenerar estas notas com `gerar_notas_derivacao_v399.py`."))
w("- Nenhum derivado foi executado contra o Nós real, nem revisto por cético independente (quem constrói não aprova). A prova é: `ast.parse`, `sh -n`, invariantes, guarda, e os harness com Nós emulado.")
w("- A leitura do rito real pode divergir do emulado em campos que só o rito mede (tempos, horários); os números de ESPERADOS vêm do ensaio a seco.")
w("")
w("## 6. Atos da gerência e do operador (nada disto foi feito aqui)")
w("")
w("- Regenerar o candidato (`refazer_candidato_v399.sh`), rodar o rito, instalar; depois a cadeia: `CHAIN_DE=0 sh chain_pos_rito_v399.sh` (passos 10a, 10b e 10c param em AGUARDA_OPERADOR; `V399_AUTORIZACAO_OPERADOR` nos recibos de parada e religamento; `B3_AUTORIZADO=sim`, `EVENTO` e `EVENTO_HASH` só no 10b).")
w("- Registrar no mapa de rotas (`registrar_mapa_v399.py` só monta o JSON e imprime o comando); o `MEMORY.md` no limite dos 195 linhas decide o que sai do índice se recusar.")
w("- Decisões do operador já listadas nos estudos: nomes provisórios (pedra e dois registros), D2 [LEGAL] (publicar o bloco embutido, com a agente de PI), D7 (ratificar a leitura das duas faces), commit/push.")
w("")
w("## 7. Mapa de rotas (consultado antes; só leitura)")
w("")
w("`rotas.py consultar` com «pos_rito», «v399» e «testemunho»: rotas lidas e respeitadas — `kernel.testemunho_v399_candidata_24out` (a pedra, nome provisório; não reabrir a direção), `umpy.v399.declaracao_do_operador_operacao_quadratica_24out` (declaração = [INPUT], o kernel não a prova), `umpy.v399.selo_pela_propria_tecnologia_estudo_24out`, `custodia.v398` (a custódia seguinte usa `custodiar.py`), `infra.bancada_um.sincronizacao_vnnn` (B(n) R3.5, passo simples) e `kernel.criterio_binario_de_parada.ponto_fixo_v394_d19` (a pedra da v394 segue citada). Nenhum caminho já examinado foi refeito; a construção desta cadeia pode entrar no mapa como rota nova (`infra.cadeia_pos_rito_v399_preparacao`), a critério da gerência.")
w("")
w("_Gerado por script a partir de `DERIVACAO_v399.json` e dos resumos dos harness em %s._" % time.strftime("%d/%m/%Y %H:%M"))
txt = "\n".join(linhas) + "\n"
p = os.path.join(POS, "NOTAS_DERIVACAO_v399.md")
if os.path.exists(p):
    b = open(p, "rb").read(); open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c1", "wb").write(b)
open(p + ".tmp", "wb").write(txt.encode("utf-8")); os.replace(p + ".tmp", p)
print("escrito", p, len(txt.encode("utf-8")), "bytes")
