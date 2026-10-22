# -*- coding: utf-8 -*-
"""editar_p00.py -- DELTA 19/10: edita p00_precondicoes_v394.py (backup de bytes ja' feito): candidato novo, sandbox k394d, kernel_d19, contagens LIDAS das listas (nada de 189/1421/46 digitado), e checagens novas (o candidato
anterior 4022ad521dc7293d segue intacto como registro; a pedra do delta; o h8; a simulacao da arvore do Nos; o exame dos pontos; os scripts novos). Cada troca tem assert de unicidade."""
import ast, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "p00_precondicoes_v394.py")
t = open(P, "rb").read().decode("utf-8")
assert "\r" not in t
n_edits = 0


def sub(old, new, count=1):
    global t, n_edits
    assert t.count(old) == count, ("troca", old[:100], t.count(old), count)
    t = t.replace(old, new); n_edits += 1


sub('HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote"))\nfrom carregar_embutido import carregar  # noqa: E402\n',
    'HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)\nfrom carregar_embutido import carregar  # noqa: E402\nimport delta19_v394 as DL  # noqa: E402   (DELTA 19/10: geracao d19)\n')
sub('KS = os.path.join(C, "t", "k394", "final"); KA = os.path.join(C, "t", "k394", "arvore")', 'KS = DL.SANDBOX; KA = DL.ARVORE; KDIR = os.path.join(HERE, DL.KERNEL_DIR)')
sub('cand = os.path.join(HERE, "um_v394_candidato.py"); cb = rd(cand)\n',
    'cand = os.path.join(HERE, DL.CANDIDATO); cb = rd(cand)\n'
    'chk("o candidato em exame (%s) segue INTACTO como registro, em arquivo proprio, e difere do novo" % DL.CANDIDATO_ANTERIOR_SHA16, sha(rd(os.path.join(HERE, "um_v394_candidato.py")))[:16] == DL.CANDIDATO_ANTERIOR_SHA16 and sha(cb)[:16] != DL.CANDIDATO_ANTERIOR_SHA16)\n')
sub('and len(E1) == 1421, len(E1))', 'and len(E1) == CM["formal_files_n"], len(E1))')
sub('chk("o kernel embutido do candidato == o sandbox construido (189 novos, raiz, Audit e os demais, byte a byte)"', 'chk("o kernel embutido do candidato == o sandbox construido (os modulos novos, raiz, Audit e os demais, byte a byte)"')
sub('chk("nenhum dos 189 modulos novos esta no kernel do Nos; as 3 pedras da v393 estao"', 'chk("nenhum dos modulos novos (%d, com a pedra do delta) esta no kernel do Nos; as 3 pedras da v393 estao" % len(nov)')
sub('pb = json.load(open(os.path.join(HERE, "kernel", "POS_BUILD_v394.json"), encoding="utf-8"))', 'pb = json.load(open(os.path.join(KDIR, "POS_BUILD_v394.json"), encoding="utf-8"))')
sub('chk("pos-build do kernel VERDE (rc 0, zero sorry, trio, .olean Lean 4.31.0, 189 compilados) e a arvore so-fontes existe", pb["ok"] is True and pb["jobs_built_novos"] == 189 and os.path.isdir(KA),',
    'chk("pos-build do kernel VERDE (rc 0, zero sorry, trio, .olean Lean 4.31.0, todos os modulos novos COMPILADOS a frio) e a arvore so-fontes existe", pb["ok"] is True and pb["jobs_built_novos"] == len(nov) and os.path.isdir(KA),')
sub('KR = json.load(open(os.path.join(HERE, "kernel", "KERNEL_RECIBO_v394.json"), encoding="utf-8"))', 'KR = json.load(open(os.path.join(KDIR, "KERNEL_RECIBO_v394.json"), encoding="utf-8"))')
sub('os.path.isdir(KR["arvore"]) and len(KR["pedras"]) == 189)', 'os.path.isdir(KR["arvore"]) and len(KR["pedras"]) == len(nov))')
sub('or k == "KH_N1_v394.json") for k, v in MI.items()), len(MI))', 'or k == DL.KH_N1_INSUMO) for k, v in MI.items()), len(MI))')
sub('chk("as 46 cunhagens: arquivo duravel', 'chk("as cunhagens (as 46 anteriores e as 2 de 19/10): arquivo duravel')
sub('and len(cd["itens"]) == 46, len(cd["itens"]))', 'and len(cd["itens"]) == cd["n"] == len(ESP["cunhagens"]), len(cd["itens"]))')
sub('for f in ("instalar_v394.py", "reverter_v394.py", "refazer_arvore_v394_pos_selo.py", "conferir_rito_v394.py", "gerar_candidato_v394.py", "ensaio_a_seco_v394.py"):',
    '''chk("a pedra do delta: a fonte autoral == a copia duravel pinada (insumos) == a EMBUTIDA no candidato == a do sandbox", sha(rd(DL.STONE_SRC)) == sha(rd(os.path.join(HERE, "insumos", DL.STONE_INSUMO))) == sha(E1[DL.STONE_REL].encode("utf-8")) == sha(rd(os.path.join(KS, *DL.STONE_REL.split("/")))) and sha(rd(DL.STONE_SRC))[:16] == ESP["pedra_do_delta"]["sha16"], ESP["pedra_do_delta"])
chk("o hash formal que o RITO vai gerar (a arvore do Nos depois do rito) tem %d entradas, com os residuais %s; o pino h8 do candidato bate" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]), len(ESP["h8_residuais_do_nos"]) + CM["formal_files_n"] == ESP["h8_entradas"] and all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in ESP["h8_residuais_do_nos"]), ESP["h8_entradas"])
sim = json.load(open(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % CM["sha16"]), encoding="utf-8"))
chk("simular_arvore_do_nos DESTE candidato: o kh_n1_cobertura_v394 sela na arvore simulada do Nos e o hash formal tem %d entradas" % ESP["h8_entradas"], sim["candidato_sha16"] == CM["sha16"] and sim["formal_files_n_no_rito_real"] == ESP["h8_entradas"] and sim["kh_n1_cobertura_v394"]["all_verified"] is True and sim["kf_all_verified"] is True, sim["formal_files_n_no_rito_real"])
exm = json.load(open(os.path.join(HERE, "EXAME_PONTOS_%s.json" % CM["sha16"]), encoding="utf-8"))
chk("exame_pontos_v394 DESTE candidato: nenhum ponto de chamada real da falso", exm["sha256"] == CM["sha256"] and exm.get("algum_falso") == [], exm.get("algum_falso"))
for f in ("delta19_v394.py", "preparar_kernel_v394.py", "pos_build_kernel_v394.py", "registros_v394.py", "montar_cunhagens_delta19_v394.py", "copiar_insumos_v394.py", "diff_e_pinos_v394.py", "gerar_esperados_v394.py", "derivar_instalar_rito_v394.py", "simular_arvore_do_nos.py", "exame_pontos_v394.py"):
    try:
        ast.parse(open(os.path.join(HERE, f), encoding="utf-8").read()); s_ = True
    except SyntaxError:
        s_ = False
    chk("ast.parse de %s" % f, s_)
for f in ("instalar_v394.py", "reverter_v394.py", "refazer_arvore_v394_pos_selo.py", "conferir_rito_v394.py", "gerar_candidato_v394.py", "ensaio_a_seco_v394.py"):''')
sub('for f in ("rito_v394.sh", "refazer_sandbox_v394.sh", "refazer_sandbox_v394_pos_selo.sh", os.path.join("pos_rito", "chain_pos_rito_v394.sh")):',
    'for f in ("rito_v394.sh", "refazer_sandbox_v394.sh", "refazer_sandbox_v394_pos_selo.sh", "construir_kernel_v394.sh", os.path.join("pos_rito", "chain_pos_rito_v394.sh")):')
ast.parse(t)
open(P + ".tmp", "wb").write(t.encode("utf-8")); os.replace(P + ".tmp", P)
print("p00_precondicoes_v394.py: %d trocas; ast.parse ok" % n_edits)
