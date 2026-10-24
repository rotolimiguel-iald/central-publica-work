"""Builds registro_mapa_anotacao_kimi.json (draft for the spine; the gerencia registers it) and validates it OFFLINE with the
spine's own validator (rotas._valida). Nothing is written to the spine."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUD = ROOT / "AUDITORIA_KIMI_TURBINA.md"
S = HERE / "saidas"

nota_principal = (
    "PARA KIMI+OPERADOR: aferição cética de 23/10 (subagente Claude Sonnet 5.5 por ordem da gerência c1; a gerência registra em nome próprio). "
    "Tudo [REAL] abaixo foi reproduzido por script em cópia isolada (evidencias/run_all.py); o que veio de Kimi/Codex sem reprodução é [DECLARADO].\n\n"
    "A (turbina: descida, parada, ranking) — ASSINA a aritmética: sobre o prefixo do livro de 1284 registros (3.427.185 B) saem exatamente 254 rotas, "
    "c3=823, c2=31.319, c1=767.724, pins 052e71f9/558296fc/3c791151, economia 95,49 %, fator 22,2×. CONTESTA a leitura: (1) a «deriva de gabarito 12/36» é falso negativo de formato "
    "— as 12 divergências são as 12 perguntas «Quais artefatos…», cuja resposta congelada (lista JSON) é comparada por substring contra um dicionário serializado; "
    "os 51 caminhos congelados coincidem 51/51 com o `artefatos` vivo; concordância real 36/36, deriva medida 0 (ERRATA ao lado da 1286, no mesmo arquivo); "
    "(2) `hit_c2` é `dict.get(rota_id do gabarito)`, não grep; só vale porque as 36 perguntas contêm o id literal; (3) «dobrar o acervo sobe uma oitava» contradiz o modelo de custo: "
    "|c2| é 90 % do custo e cresce linear, o fator satura em ~24,5×. FALTA: pré-registro do critério de parada e do ranking (o Kimi não registrou; o Codex pré-registrou outra política em 21/10 10:17, "
    "sem estatuto/recência/centralidade como pesos; a qualidade de recuperação não foi medida; o `rank_nodes` instalado conta palavras vazias e ignora estatuto — contraexemplo em saidas/05).\n\n"
    "B (benchmark seq 1288) — CONTESTA: não assinar o v1 e não rodar o pacote e662b198. Braço B recebe o c1 do alvo por oráculo (36/36; resposta verbatim no contexto 24/24); "
    "o gabarito vivo não tem chave para as 12 perguntas de artefatos; H2 (densidade >5×) vale sempre que B tenha >23 % das afirmações suportadas de A (razão de tokens 14,9–23,4×) e o limiar foi fixado 13 min depois do fator 22,2× (seq 1286); "
    "H3 compara braço instruído com não instruído; H4 usa ids zz.inexistente; a ROTA 1288 não tem artefatos pinados; a regra de decisão não fixa procedimento inferencial (n=36). "
    "ASSINA o adendo v2 do Codex (ADENDO_BENCHMARK_V2.md, sha 0862cd56) como base, com 5 acréscimos: chave de artefatos por conjunto, controles e corpus temáticos sem id, função de veredito pinada no livro antes das respostas, H2/H3 com unidades verificadas e ablação do cabeçalho, respondedor e teto de bytes no manifesto.\n\n"
    "C (cabeçalho e dobra) — cabeçalho v1: CONTESTA (146/255 rotas têm tipo≠ROTA e 123/255 título diferente na dobra: «EXATAMENTE o que a casa escreveu» é falso; «REAL>DERIVED>OPEN» faz escala de peso de rótulo autodeclarado; «a borda do acervo é o dado» vira falso negativo com recuperação parcial; pins de 16 hex). "
    "«v2» do Kimi: FALTA (só existe a constante v1); v2 do Codex (HEADER_V2.txt): ASSINA, ressalva: citar source_id e conferir o SHA-256 por script, não pedir o hash ao modelo. "
    "Dobra do Kimi (57bf9be7): CONTESTA — aceitava pacote acima do teto agregado (28.028 chars contra 12.000; 911.379 B contra 909.312; 36.855 B contra 36.000; 0 fontes) e o teste dele não soma a reserva; o segundo portão (attach) recusa os mesmos casos; "
    "os jobs e1ce17ac, 9dd45d6a e 90528e45 seguem awaiting_dispatch. Produção atual f95ed18e (Codex, 21/10 10:35): ASSINA. NÃO BLOQUEANTE: todo pacote dobrado traz o aviso no prompt e folded/fold_layers/fold_notice no recibo; nenhum consumidor trata índice+trechos como memória completa. "
    "As 3 falhas de test_canonical_memory/test_request_controls são pré-existentes (mesmos 3 testes, mesma causa, em 5 configurações; coordination 6/6 e transport 7/7 idênticos), mas nenhum teste do repositório cobre a dobra.\n\n"
    "D (manutenção de 21/10 e esta resposta) — título F9.9: bytes ASSINA (uma linha, −2 B, 122 unidades iguais); processo CONTESTA (PROGRAMA.json é «só pelo iald.py», sem evento; ordem das 09:40 sem verbatim); "
    "reindexação do Nós Vivo: ASSINA (backups 093151 e 094237 conferem, integrity ok, números = seq 1289). FALTA o verbatim das ordens de 19:11 e 09:40. "
    "Extras: 1302 FALTA (o livro da Bancada não tem a observação: 103 linhas, última 01/10); 1301 ASSINA (CONJECTURE, regra de morte simétrica); 1303 ASSINA os bloqueios 2 e 3 e CONTESTA o 1.º.\n\n"
    "Decisões que cabem ao operador: estatuto como peso no ranking (recomendação: não); dobra INDEX_ONLY em missão científica (permitir com aviso ou recusar); ratificar ou não as edições do Kimi em Chatgpt\\ e PROGRAMA.json."
)
assert "CONFIRM" not in nota_principal.upper().replace("NOT_FALSIFIED", "")

registros = [
    {
        "tipo": "ANOTACAO",
        "rota_id": "infra.benchmark_turbina",
        "titulo": "Aferição cética de 23/10 do pacote Kimi (turbina): descida grep-c3, benchmark v1, cabeçalho e dobra do envelope; veredito por item A–D",
        "metodo": "Cópia isolada do código do orquestrador (sem state, sem segredos; memória selada sintética; sem CLIs de provedor, proxy morto); 5 configurações × 4 módulos de teste; "
                  "reprodução de 12 casos do envelope; segundo portão (attach); teste do próprio Kimi rodado contra 3 variantes; re-medição da descida sobre o prefixo exato do livro; análise do pacote do benchmark; "
                  "leitura de quadro, Nós Vivo, livro da Bancada e fila em modo só leitura.",
        "resultado": "A: aritmética da descida reproduz bit a bit (95,49 %; 22,2×); a deriva de gabarito 12/36 não existe (36/36). B: pacote v1 aprovável por construção (oráculo; chave ausente em 12/36; H2 aritmética de tamanhos). "
                     "C: dobra do Kimi aceitava envelope acima do teto (falso sucesso em prepare()), superada pela f95ed18e (verificada); aviso legível em todo pacote dobrado. D: bytes do título e da reindexação conferem; processo do título fora do iald.py.",
        "veredito": "A_ASSINA_ARITMETICA_CONTESTA_LEITURA_FALTA_PREREGISTRO__B_CONTESTA_V1_ASSINA_ADENDO_V2_DO_CODEX__C_DOBRA_DO_KIMI_SUPERADA_PRODUCAO_ASSINADA_NAO_BLOQUEANTE__D_BYTES_ASSINA_PROCESSO_CONTESTA",
        "estatuto": "REAL",
        "status": "EXAMINADA_COM_DEFEITO",
        "olhou_dados": True,
        "defeito": "Limites da aferição: memória selada sintética (não a real); nenhuma fila real nem provedor; χ² da Bancada (1302) não reproduzido; prompt da VOZ não revisado. "
                   "Residuais da produção: reserva ≥1 destrava a dobra; sem teste do repositório para a dobra; fontes do Nós Vivo entregues como prefixo de 2.400 chars sem marcador no texto.",
        "nao_refazer": "Não rodar o pacote do benchmark v1 (sha e662b198…). Não refazer a reprodução da descida e do envelope: evidencias/run_all.py refaz tudo em ~2 min.",
        "proximo_passo": "Kimi: ERRATAs ao lado da 1286 e da 1294; benchmark v2 sobre o adendo do Codex + 5 acréscimos; corrigir a frase do livro da Bancada; pinar o verbatim das ordens de 19:11 e 09:40. "
                         "Gerência: integrar os 19 testes do Codex à suíte; marcador textual de prefixo no Nós Vivo. Operador: as 3 decisões da nota.",
        "onde": "work/auditoria_kimi_turbina_23out/AUDITORIA_KIMI_TURBINA.md; evidencias/run_all.py",
        "artefatos": [str(AUD), str(S / "02_fold_tabela.txt"), str(S / "04_teste_do_kimi_contra_as_tres_variantes.txt"),
                      str(S / "07_deriva_de_gabarito_refutada.txt"), str(S / "08_pacote_do_benchmark.txt"), str(HERE / "sha256_dos_artefatos.json")],
        "refs": ["infra.grep_acom_camadas", "infra.envelope_modo_dobrado", "infra.bancada_um_modo_uso_kimi",
                 "infra.vigilia_fila_claude_gate_acom", "d7.kilonova_fronteira_aguda"],
        "nota": nota_principal,
    },
    {
        "tipo": "ERRATA",
        "rota_id": "infra.grep_acom_camadas",
        "corrige": 1286,
        "titulo": "ERRATA ao lado da 1286 (23/10): a «deriva de gabarito 12/36» é falso negativo de formato; concordância real gabarito × livro 36/36",
        "resultado": "Sobre o prefixo do livro usado (1284 registros, 3.427.185 B): as 12 divergências são as 12 perguntas «Quais artefatos a rota X registra (caminhos)?»; a resposta congelada é uma lista JSON de caminhos "
                     "e o teste `resposta[:60] in json.dumps(registro)` compara essa lista com um dicionário serializado, então nunca passa. Conferindo como conjuntos: 12/12 listas = `artefatos[].caminho` vivos "
                     "(2,5,2,1,16,2,1,4,12,2,3,1 = 51/51 caminhos), também em todo o histórico das rotas; as 24 respostas de texto passam 24/24. Deriva medida: 0. "
                     "A aritmética da seq 1286 (95,49 %; 22,2×; pins; custo 34.647) reproduz exatamente. `hit_c2` é consulta por rota_id do gabarito (36/36 por id literal na pergunta).",
        "veredito": "DERIVA_DE_GABARITO_REFUTADA__12_DIVERGENCIAS_SAO_AS_12_PERGUNTAS_DE_ARTEFATOS__51_DE_51_CAMINHOS_COINCIDEM__CONCORDANCIA_36_DE_36",
        "estatuto": "REAL",
        "olhou_dados": True,
        "defeito": "A lição «gabarito sobre memória viva envelhece em horas» não vem desta medição. O `gabarito_vivo` do benchmark herda o erro: não tem chave `artefatos`.",
        "artefatos": [str(S / "06_descida_prefixo_do_livro.txt"), str(S / "07_deriva_de_gabarito_refutada.txt")],
        "nota": "PARA KIMI+OPERADOR: correção ao lado (a 1286 não se altera). O recall de entidade nomeada não era 0,6667; era 36/36 e trivial por id literal. O recall temático segue não medido.",
    },
    {
        "tipo": "ERRATA",
        "rota_id": "infra.envelope_modo_dobrado",
        "corrige": 1294,
        "titulo": "ERRATA ao lado da 1294 (23/10): a dobra do Kimi aceitava pacote acima do teto agregado (falso sucesso); superada pela versão f95ed18e de 21/10 10:35",
        "resultado": "Reproduzido em cópia isolada: com a versão 57bf9be7, prepare() aceita o caso bloqueado (28.028 chars contra teto 12.000; 22.969 contra 20.000), maximum (911.379 B contra 909.312), "
                     "deepseek_maximum (649.235 contra 647.168), pedido multibyte sem reserva (36.055 e 36.855 B contra 36.000) e lista de fontes vazia; o teste do Kimi (3/3) não soma a reserva (7.364 B reproduzido). "
                     "O segundo portão (attach) recusa os mesmos casos; os jobs e1ce17ac, 9dd45d6a e 90528e45 seguem awaiting_dispatch; a dobra nunca foi exercida em produção (0 recibos folded). "
                     "A produção atual (f95ed18e, Codex) recusa todos esses casos. As falhas de test_canonical_memory (1F+1E) e test_request_controls (1E) são pré-existentes.",
        "veredito": "DOBRA_57BF9BE7_SUPERADA_PELA_F95ED18E__FALSO_SUCESSO_EM_PREPARE__NAO_BLOQUEANTE__AVISO_LEGIVEL_EM_TODO_PACOTE_DOBRADO",
        "estatuto": "REAL",
        "olhou_dados": True,
        "defeito": "Residuais na produção atual: qualquer reserva ≥1 destrava a dobra; a invariante «pelo menos um trecho» foi derrogada (INDEX_ONLY); nenhum teste do repositório cobre a dobra.",
        "artefatos": [str(S / "02_fold_tabela.txt"), str(S / "03_attach_kimi.txt"), str(S / "04_teste_do_kimi_contra_as_tres_variantes.txt")],
        "nota": "PARA KIMI+OPERADOR: a frase «foi esse bloqueio que segurou o teu briefing» não se sustenta; a 1304 já havia recuado. Correção ao lado; a 1294 não se altera.",
    },
]

out = ROOT / "registro_mapa_anotacao_kimi.json"
out.write_text(json.dumps(registros, ensure_ascii=False, indent=1), encoding="utf-8")

# offline validation with the spine's own validator (reads the ledger; writes nothing)
spec = importlib.util.spec_from_file_location("rotas_mod", r"C:\IALD\MAPA_DE_ROTAS\rotas.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
regs = m._le()
ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}
seqs = {r["seq"] for r in regs}
for r in registros:
    v = m._valida(r, ids, seqs)
    print("VALIDO:", r["tipo"], r["rota_id"], "| campos:", sorted(v)[:6], "...", "| chars nota:", len(r.get("nota", "")))
print("escrito:", out, out.stat().st_size, "bytes")
