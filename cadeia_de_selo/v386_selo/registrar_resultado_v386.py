# -*- coding: utf-8 -*-
"""O RESULTADO da v386 para o MAPA DE ROTAS (molde: registrar_resultado_v385.py), tudo LIDO da rodada (leitura_v386.ler). Por padrao NAO registra: monta o
JSON (registro_mapa_v386.json), PRE-VALIDA cada registro pela propria regua do mapa (rotas._valida, so leitura: estatuto da casa, guarda da palavra
proibida, artefatos existentes com o sha256 calculado pela ferramenta) e imprime o comando que a GERENCIA roda:
    python C:\\IALD\\MAPA_DE_ROTAS\\rotas.py registrar <json> --quem "<IA / sessao>"
Com --registrar (so com o Nos REAL; ato da gerencia), chama rotas.registrar. Com o Nos SINTETICO: o JSON vai a ensaio_saidas, marcado SINTETICO, e --registrar e' recusado.
Registros (v386): (1) RESULTADO na rota kernel.v386_tipagem_do_verbo (registrada EM_CURSO em 05/10: a pedra selou; rota examinada nao se refaz);
(2) ROTA ringdown.ramo_b_preregistro_v386 (o V1 lido por hash; nada aberto; [INPUT]); (3) ANOTACAO na kernel.livro_de_cobrancas.otica (a errata ao lado
de R6; F2b); (4) ANOTACAO na quantica.pilar_v385_reprodutibilidade (o pilar reaproveitado na v386; a reprodutibilidade v385 NOT_COMPARED, dito);
(5) ANOTACAO na ringdown.dephasing (o ramo B reaberto por pre-registro; o 221 e a PE so-220 ficam para a v387)."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import ambiente_v386 as A
import leitura_v386, textos_v386 as T
import rotas
AMB = A.ambiente()
V, PROB = leitura_v386.ler()
if PROB:
    print("REGISTRO RECUSADO:", PROB); sys.exit(2)
X = T._x(V)
ROTA_VERBO = "kernel.v386_tipagem_do_verbo"; ROTA_B = "ringdown.ramo_b_preregistro_v386"
regs0 = rotas._le()
if any(r.get("rota_id") == ROTA_B and r.get("tipo") == "ROTA" for r in regs0):
    print("mapa: a rota %s ja existe; nada gravado (os registros desta rodada ja entraram)" % ROTA_B); sys.exit(0)
if not any(r.get("rota_id") == ROTA_VERBO and r.get("tipo") == "ROTA" for r in regs0):
    print("mapa: a rota %s (registrada em 05/10) NAO existe -- o RESULTADO do Verbo exigiria uma ROTA antes; conferir o mapa" % ROTA_VERBO); sys.exit(2)
NOS = V["nos"]; S = " [SINTETICO -- ENSAIO DA CADEIA; NAO REGISTRAR]" if AMB["sint"] else ""
RD = V["qp_run_dir"] if os.path.isabs(V["qp_run_dir"]) else os.path.join(NOS, V["qp_run_dir"])
art_k = [os.path.join(NOS, f) for f in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "rodada_v386_stdout.txt")]
art_k += [os.path.join(NOS, "tgl_kernel", "TGLExt", "TheVerbSelectsTheAction.lean"), os.path.join(NOS, "tgl_kernel", "TGLExt.lean"),
          os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"), os.path.join(AMB["conf_dir"], "conferencia_rito_v386.json"), A.OP_FILES["verbo_20261005_1653"], A.OP_FILES["respostas_20261005_1829"]]
V1F = [os.path.join(A.PRDIR_B, f) for f in ("PREREGISTRO_RAMO_B_RINGDOWN_V1.json", "PREREGISTRO_RAMO_B_RINGDOWN_V1.md", "V1_RAMO_B_HASHES.json")]
art_b = [os.path.join(NOS, f) for f in ("um_absoluto_selo.json", "um_absoluto.json", "rodada_v386_stdout.txt")] + V1F + [A.OP_FILES["ramo_b_decision_20261005_1711"],
         os.path.join(A.DAT, "ramo_b", "ESPEC_RUNTIME_RAMO_B_v386_ERRATA.json")]
art_p = [os.path.join(NOS, "um_absoluto_pilar_quantico.json"), os.path.join(NOS, "rodada_v386_stdout.txt")] + [os.path.join(RD, f) for f in ("result.json", "details.jsonl", "cpuref.json") if os.path.exists(os.path.join(RD, f))]
_r = lambda n: leitura_v386.render_op((V.get("op") or {}).get(n))
res = [dict(tipo="RESULTADO", rota_id=ROTA_VERBO, status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo=("v386 SELADA%s: o Verbo seleciona [KERNEL: a pedra TheVerbSelectsTheAction (%s decl.) + %s termos do regime angular fiados na escada; as leituras do operador "
                    "INPUT/ONTO] -- o Nome e' o posto (projecao de posto 1); a leitura e' um peso (Born); a ordem importa (triade su(2) escalada por c = beta_TGL [INPUT]); verdade e "
                    "custo duas faces; o tempo lido duas vezes; luz e gravidade indissociaveis; gate intocado" % (S, V["vb_n_pedra"], V["vb_n_ang"])),
            resultado=("um.py %s (%s B) sobre a v385 %s; %s; escada %s -> %s; o Verbo %s (pedra %s, angular %s); token lido do kernel = pino: %s; verbatins por sha256: %s; "
                       "conferidor %s (%s / %s / %s); gate %s (%s/18) inalterado; por termo %s" % (V["s16"], X["umb_fmt"], V["base16"], V["teor"], V["esc_v385"], V["esc"], V["vb_ok"], V["vb_vrb"],
                                                                                                V["vb_ang"], V["vb_token_ok"], V["vb_verbatim_ok"], X["conf_res"], V["conf_dm"], V["conf_np"], V["conf_md"], V["qg"], V["n18"], V["hvals"])),
            veredito=V["vb_v"],
            metodo=("pedra nova TGLExt/TheVerbSelectsTheAction.lean (sha16 %s; %s B; construida no sandbox %s) + 17 termos ext_ang_ no #print axioms; rito completo; conferidor do "
                    "pacote (copia byte a byte); o token lido da def verbTypingStoneName (embutido e materializado)" % (V["vb_pedra16"], V["vb_pedra_bytes"], V["vb_build"])),
            nao_refazer=("o que a pedra prova esta nos nomes dos termos (post/select; reading_post_is_born; two_posts_that_do_not_commute; triad_*; axis_posts_do_not_commute; "
                         "truth_and_cost_are_two_faces; time_read_twice_confirms_the_post; light_and_gravity_are_inseparable); o que NAO esta tipado: %s; c = beta_TGL e' [INPUT], "
                         "nunca literal (o operador escreveu alpha^2: citacao, correcao ao lado); provado nao e' confirmado" % V["vb_not_typed"][:900]),
            proximo_passo="custodia conjunta v383 + v384 + v385 + v386 pela sessao do site (decisao do operador de 05/10); commit/push do operador",
            onde="Nos\\um.py v386: the_verb_v386; Nos\\tgl_kernel\\TGLExt\\TheVerbSelectsTheAction.lean; selo the_verb_v386 / the_verb_reading_v386 / verb_typing_stone_name_v386",
            artefatos=art_k, refs=["kernel.livro_de_cobrancas.otica", ROTA_B, "memory verbo-selecao-da-acao-05out"]),
       dict(tipo="ROTA", rota_id=ROTA_B, dominio="RINGDOWN", status="EXAMINADA", estatuto="INPUT", olhou_dados=False,
            titulo=("v386 SELADA%s: o ramo B do ringdown REABERTO POR PRE-REGISTRO -- o V1 %s LIDO POR HASH pelo rito (JSON %s, MD %s, spec %s); OUTRA LEI (%s; k = %s; M = %s), "
                    "canal proprio F2b; so o conjunto D (%s de O4) testa, cego; A/B/C calibracao NOT_BLIND; NADA ABERTO; veredito do V1 %s; gate intocado"
                    % (S, V["rb_id"], V["rb_json16"], V["rb_md16"], V["rb_spec16"], V["rb_forma"], V["rb_k"], V["rb_M"], V["rb_nD"], V["rb_vered_v1"])),
            pergunta="a constante de acoplamento (beta) emerge da relacao do tempo emparelhado a gravidade sobre c^3 (tau* = k.G.M_f/c^3), lida no ringdown do conjunto D, cego? (pergunta do operador, 05/10)",
            dados=["nenhum dado aberto nesta versao: o V1 por hash; os valores centrais NOT_BLIND transcritos do registro selado v385 (A/C): %s" % V["rb_central_txt"],
                   "o conjunto D: %s elegiveis de O4; %s sem pendencia de qualidade; %s com data-quality hold" % (V["rb_nD"], V["rb_D_sem_hold"], V["rb_D_hold"])],
            metodo=("ramo_b_preregistration_v386: os 6 arquivos do V1 por sha256 e bytes; spec_sha256 recomputado do JSON canonico; cada entrada de V1_RAMO_B_HASHES.json contra o "
                    "disco; beta do V1 x beta do rito a 1e-9 relativo (medido: %s abs / %s rel); %s pinos numericos transcritos (nunca recalculados); sanidade k(chi=0) = 8pi e "
                    "beta = alpha.sqrt(e) em runtime" % (V["rb_abs"], V["rb_rel"], V["rb_pins_n"])),
            resultado=("V1 lido por hash: %s; F2b %s (%s); beta ok %s; pinos %s/%s; erratas ao lado: %d; vereditos permitidos na ordem: %s; proibidos: %s"
                       % (V["rb_disk_txt"], V["rb_F2b"], V["rb_qual"], V["rb_beta_ok"], V["rb_pins_iguais"], V["rb_pins_n"], V["rb_erratas_n"], V["rb_vereditos_ordem"], V["rb_vereditos_proibidos"])),
            veredito=V["rb_v"],
            nao_refazer=("o V1 e' congelado por hash: qualquer mudanca e' um V1.x com nova ratificacao; as erratas ao lado (agroa; compressoes da gerencia; chave da errata; 1e-9 relativo; "
                         "a citacao do manuscrito) ficam no registro; o 221 e' diagnostico (posteriores no tar.gz, nao extraidos); NOT_FALSIFIED nunca e' confirmacao"),
            proximo_passo="v387: o estagio cego do conjunto D (sigma_i, poder antes de abrir), as injecoes, a PE so-220 na casa e a abertura de D pela MESMA funcao de veredito, por hash; a errata da ESPEC a ratificar ao lado",
            onde="Nos\\um.py v386: ramo_b_preregistration_v386; C:\\IALD\\Bancada_Um\\investigacao\\preregistro_ramo_b_05out (espelho proposto: preregistro_ramo_b_v386)",
            nota="decidido por delegacao do operador (%s); a decisao do ramo B: %s" % (_r("delegacao"), _r("ramo_b")),
            artefatos=art_b, refs=["ringdown.dephasing", "kernel.livro_de_cobrancas.otica", ROTA_VERBO]),
       dict(tipo="ANOTACAO", rota_id="kernel.livro_de_cobrancas.otica", status="EXAMINADA", estatuto="INPUT", olhou_dados=False,
            titulo=("v386%s: a ERRATA AO LADO de R6 selou (%s): de ENCERRADO para REABERTO POR PRE-REGISTRO (decisao do operador %s, verbatim por sha256); o livro v383 INTACTO (%s "
                    "cobrancas); F2b nasce ao lado (%s); F2 e R2 intocados" % (S, V["le_v"][:60], V["le_dec_quando"], V["le_n"], V["le_f2b_token"])),
            nota="R6 (v383) lia: %s | regra: %s" % (V["le_r6_v383"][:400], V["le_rule"][:300]),
            artefatos=[os.path.join(NOS, "um_absoluto.json"), A.OP_FILES["ramo_b_decision_20261005_1711"]], refs=[ROTA_B]),
       dict(tipo="ANOTACAO", rota_id="quantica.pilar_v385_reprodutibilidade", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
            titulo="na v386%s o pilar NAO e' objeto da versao: %s (%s); a reprodutibilidade v385 nesta rodada: %s (%s)" % (S, X["qr_curtissima"], V["qr_v"][:100], V["rp_v"][:80], V["rp_txt"]),
            nota="servidor do modelo nativo depois do rito: %s; o marcador do pacote v386: %s" % (V["servidor"], V["marcador_txt"]),
            artefatos=art_p, refs=[ROTA_VERBO]),
       dict(tipo="ANOTACAO", rota_id="ringdown.dephasing", status="EXAMINADA_COM_DEFEITO", estatuto="INPUT", olhou_dados=False,
            titulo="v386%s: o ramo B (tau* = k.G.M_f/c^3) entrou por PRE-REGISTRO (ver %s); nada aberto; o 221 do GW250114 segue no tar.gz (diagnostico); a PE so-220 do conjunto D fica para a v387" % (S, ROTA_B),
            artefatos=V1F, refs=[ROTA_B])]
if AMB["sint"]:
    for r in res:
        r["nota"] = (r.get("nota", "") + " | SINTETICO: ensaio da cadeia com o Nos sintetico; NAO registrar").strip(" |")
# pre-validacao pela regua do mapa (so leitura)
ids = {r["rota_id"] for r in regs0 if r["tipo"] == "ROTA"}; seqs = {r["seq"] for r in regs0}
ok = []
for r in res:
    vv = rotas._valida(dict(r), set(ids), seqs)
    ok.append((r["tipo"], r["rota_id"], len(vv.get("artefatos") or [])))
    if r["tipo"] == "ROTA":
        ids.add(r["rota_id"])
out_dir = AMB["saidas"]; os.makedirs(out_dir, exist_ok=True)
out = A.pode_escrever(os.path.join(out_dir, "registro_mapa_v386.json"), AMB)
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
