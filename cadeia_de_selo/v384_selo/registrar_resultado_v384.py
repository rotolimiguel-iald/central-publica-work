# -*- coding: utf-8 -*-
"""O RESULTADO da v384 para o MAPA DE ROTAS (molde: registrar_resultado_v383.py), tudo LIDO da rodada (leitura_v384.ler). Por padrao NAO registra: monta o
JSON (registro_mapa_v384.json), PRE-VALIDA cada registro pela propria regua do mapa (rotas._valida, so leitura: estatuto da casa, guarda da palavra
proibida, artefatos existentes com o sha256 calculado pela ferramenta) e imprime o comando que a GERENCIA roda:
    python C:\\IALD\\MAPA_DE_ROTAS\\rotas.py registrar <json> --quem "<IA / sessao>"
Com --registrar (so com o Nos REAL; ato da gerencia), chama rotas.registrar. Com o Nos SINTETICO: o JSON vai a ensaio_saidas, marcado SINTETICO, e --registrar e' recusado.
Registros: (1) ROTA quantica.pilar_v384_rodada_completa (o pilar calculado na rodada completa: veredito, numeros, negativos honestos, custodia);
(2) ANOTACAO na quantica.pilar_v384_cadeia_ate_o_rito (a cadeia ate o selo fechou: conferidor, superficies); (3) ANOTACAO na
quantica.pilar_v384_rascunhos_b_reduzido_e_a (o V1 ratificado foi o lido pelo rito, por hash)."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import ambiente_v384 as A
import leitura_v384, textos_v384 as T
import rotas
AMB = A.ambiente()
V, PROB = leitura_v384.ler()
if PROB:
    print("REGISTRO RECUSADO:", PROB); sys.exit(2)
X = T._x(V)
ROTA_ID = "quantica.pilar_v384_rodada_completa"
# a guarda de idempotencia do molde (registrar_resultado_v383.py:13-14; 5o achado da revisao de 04/10): a rota ja existe -> nada gravado, rc 0
if any(r.get("rota_id") == ROTA_ID and r.get("tipo") == "ROTA" for r in rotas._le()):
    print("mapa: a rota %s ja existe; nada gravado (os registros desta rodada ja entraram)" % ROTA_ID); sys.exit(0)
NOS = V["nos"]; S = " [SINTETICO -- ENSAIO DA CADEIA; NAO REGISTRAR]" if AMB["sint"] else ""
RD = os.path.join(NOS, V["qp_run_dir"]) if not os.path.isabs(V["qp_run_dir"]) else V["qp_run_dir"]
art = [os.path.join(NOS, f) for f in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "rodada_v384_stdout.txt", "um_absoluto_pilar_quantico.json")]
art += [os.path.join(RD, f) for f in ("result.json", "result_partial.json", "details.jsonl", "cpuref.json") if os.path.exists(os.path.join(RD, f))]
if V["qp_classe"] != "RAMO_9" and os.path.exists(os.path.join(RD, "worker_stdout.txt")):
    art.append(os.path.join(RD, "worker_stdout.txt"))   # fora do ramo 9, o registro do trabalhador e' a prova do que houve
if V["qp_classe"] == "RAMO_9":
    _deu = ("T2: atrator unico em %s de %s pontos (ambiguos %s, degenerados %s), NAME_IN_CORE %s/%s, FOLDS_WINDOW %s/%s; T1: %s injecoes, %s; T3: %s controles falharam como exigido; "
            "T4: %s instancias, %s violacoes de identidade, unico em %s; D128: %s; CPU: %s comparados, %s discordancias (maior diferenca %s); motor %s; %s min; resultado %s = arquivo no Nos = hash no selo %s"
            % (V["t2_unique"], V["t2_points"], V["t2_amb"], V["t2_deg"], V["t2_name"], V["t2_configs"], V["t2_folds"], V["t2_configs"], V["t1_inj"], X["t1_frase"], V["t3_ctl"],
               V["t4_n"], V["t4_viol"], V["t4_u"], V["d128_txt"], V["cpu_cmp"], V["cpu_dis"], V["cpu_maxdiff"], V["eng"], V["qp_min"], V["qp_res16"], V["qp_selo16"]))
else:
    _deu = "computacao nao concluida: %s; lancamento: %s; custodia: %s" % (V["qp_classe_txt"], V["qp_lanc_txt"], V["qp_custodia_txt"])
art += [A.PR_JSON, A.PR_MD, os.path.join(AMB["conf_dir"], "conferencia_rito_v384.json")]
res = [dict(tipo="ROTA", rota_id="quantica.pilar_v384_rodada_completa", dominio="DEPHASING", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo=("v384 SELADA%s: o pilar quantico na GPU calculado na rodada completa [COMPUTED: calculo do sistema da teoria, nao medicao] -- o sistema aberto H_LD + "
                    "cinco saltos de Lindblad em paralelo com o kernel e os ritos, sob o pre-registro %s (especificacao %s) ratificado pelo operador (%s); classe: %s; gate intocado"
                    % (S, V["pr_id"], V["pr_spec16"], V["pr_escolha"], X["qp_classe_curta"])),
            pergunta="o sistema aberto da teoria, calculado sob o V1 congelado, da o ramo 9 da arvore (atrator unico, instrumento cego, controles que falham, identidades, CPU)? com que negativos honestos?",
            dados=["nenhum dado da natureza: calculo do sistema da teoria na GPU (%s), com a referencia independente na CPU" % V["qp_gpu"],
                   "o pre-registro %s (JSON %s / MD %s por sha256; %s evidencias)" % (V["pr_id"], V["pr_json16"], V["pr_md16"], V["pr_ev"])],
            metodo=("o trabalhador embutido no um.py v384 (%s), lancado depois da inscricao do Um; o rito espera, confere o sha256, REDERIVA o veredito pela mesma arvore e registra "
                    "no core, no selo (ao lado do gate) e no artigo; conferidor do pacote (copia byte a byte); a cadeia do selo" % V["pr_worker16"]),
            resultado=("um.py %s (%s B) sobre a v383 %s; %s; rodada %s; conferidor %s (%s / %s); %s; %s; gate %s (%s/18) inalterado; por termo %s"
                       % (V["s16"], X["umb_fmt"], V["base16"], V["teor"], V["selo_ts"], X["conf_res"], V["conf_dm"], V["conf_np"], _deu, V["qp_cache"], V["qg"], V["n18"], V["hvals"])),
            veredito=V["qp_v"],
            nao_refazer=("o V1 congelado nao muda: mudanca no trabalhador ou na especificacao e' um V1.x com nova ratificacao; repetir a rodada sob o MESMO V1 congelado e' decisao do operador; "
                         "o pilar e' calculo [COMPUTED], nao medicao, e nao move o gate; "
                         "a hierarquia das dobras e' matematica; o T1 testa o instrumento; as identidades so falham se o motor errar; negativos honestos desta rodada: %s" % V["qp_negativos"]),
            proximo_passo=("custodia/espelho pela sessao do site (ato dela; commit/push do operador), com a v383 agora ou junto (decisao do operador); o que espelhar do pre-registro e das "
                           "evidencias (decisao do operador)"),
            onde="Nos\\um.py v384: quantum_pillar_start_v384 / quantum_pillar_finish_v384 / _qp_summary; pasta da rodada: %s; Nos\\um_absoluto_pilar_quantico.json" % V["qp_run_dir"],
            artefatos=art, refs=["quantica.pilar_v384_cadeia_ate_o_rito", "quantica.pilar_v384_rascunhos_b_reduzido_e_a", "quantica.pilar_v384_conferencia_do_congelamento",
                                 "quantica.cinco_operadores_lindblad_matrizes", "quantica.dobras_c3_hierarquia_e_matematica", "memory v384-pilar-quantico-gpu-02out"]),
       dict(tipo="ANOTACAO", rota_id="quantica.pilar_v384_cadeia_ate_o_rito", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo="o rito v384 rodou%s: %s, rc %s, %s; conferidor %s (%s / %s); a cadeia do selo (linhagem, desenho, Atlas, indice, arvore) por leitura_v384/textos_v384" % (S, V["teor"], V["rc"], V["selftest"], X["conf_res"], V["conf_dm"], V["conf_np"]),
            nota="servidor do modelo nativo depois do rito (do log do lancador): %s; o marcador do pacote: %s" % (V["servidor"], V["marcador_txt"]),
            artefatos=[os.path.join(NOS, "rodada_v384_stdout.txt")], refs=["quantica.pilar_v384_rodada_completa"]),
       dict(tipo="ANOTACAO", rota_id="quantica.pilar_v384_rascunhos_b_reduzido_e_a", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo="o V1 ratificado (%s) foi o lido pelo rito v384%s: JSON %s e MD %s em disco = os do candidato (on_disk_matches), especificacao %s embutida e conferida pelo hash" % (V["pr_escolha"], S, V["pr_json16"], V["pr_md16"], V["pr_spec16"]),
            artefatos=[A.PR_JSON, A.PR_MD], refs=["quantica.pilar_v384_rodada_completa"])]
if AMB["sint"]:
    for r in res:
        r["nota"] = (r.get("nota", "") + " | SINTETICO: ensaio da cadeia com o Nos sintetico; NAO registrar").strip(" |")
# pre-validacao pela regua do mapa (so leitura)
regs = rotas._le(); ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}; seqs = {r["seq"] for r in regs}
ok = []
for r in res:
    vv = rotas._valida(dict(r), set(ids), seqs)
    ok.append((r["tipo"], r["rota_id"], len(vv.get("artefatos") or [])))
    if r["tipo"] == "ROTA":
        ids.add(r["rota_id"])
out_dir = AMB["saidas"]; os.makedirs(out_dir, exist_ok=True)
out = A.pode_escrever(os.path.join(out_dir, "registro_mapa_v384.json"), AMB)
open(out + ".tmp", "wb").write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8")); os.replace(out + ".tmp", out)
print("pre-validado pela regua do mapa:", ok)
print("JSON para o mapa%s: %s" % (S, out))
if "--registrar" in sys.argv:
    if AMB["sint"]:
        print("RECUSO --registrar com o Nos SINTETICO"); sys.exit(2)
    o = rotas.registrar(res, "claude-code/central-de-patentes (gerencia) sessao 6da8f00d")
    print(json.dumps({k: o[k] for k in o if k != "registros"}, ensure_ascii=False)[:500])
else:
    print('a gerencia registra: python C:\\IALD\\MAPA_DE_ROTAS\\rotas.py registrar "%s" --quem "claude-code/central-de-patentes (gerencia) sessao 6da8f00d"%s' % (out, "   <- NAO (SINTETICO)" if AMB["sint"] else ""))
