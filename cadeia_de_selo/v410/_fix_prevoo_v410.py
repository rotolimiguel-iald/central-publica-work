# -*- coding: utf-8 -*-
"""_fix_prevoo_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410): os achados do PRE-VOO do gerador e as pendencias do agente dos textos que sao do construtor:
(1) runtime_v410.py: a linha de marca da guarda do H0DN citava as frases proibidas (F53/F53b pegavam a propria marca); o regex F51 trazia «observad…confirmad» a menos de 60 caracteres (a R4 da P18 selada o le como texto): sai «confirmad|confirmed» da F51;
(2) runtime_h0dn_v410.py: n_pinos_freeze nos values; o rotulo da rota Kimi entre “ ” (nao e' fala do operador); (3) registros_h0dn_v410.py e os snippets do H0DN: o mesmo rotulo entre “ ”; os pinos ditos com o FREEZE e os embutidos fora dele;
(4) registros_v410.py: o dict da errata E30 no spec cunhagens_v410 (entre a E29 e a dos pisos; a leitura e o mapa exigem [E29, E30] + pisos); (5) delta_v410.py: «CONFIRMADA» em caixa baixa na D76 (o portao do G1 so' aceita a maiuscula na formula da regua);
(6) pos_rito/chain_pos_rito_v410.sh: REGS ganha h0dn_bg1_v410. Backup de bytes; trocas exatas com contagem; fim de linha de cada arquivo; ast.parse nos .py."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(nome, trocas, parse="py"):
    P = os.path.join(HERE, nome); b0 = open(P, "rb").read()
    nl = "\r\n" if b0.count(b"\r\n") else "\n"
    bk = P + ".bak_" + TS + "_prevoo"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for v, n, k in trocas:
        v2, n2 = (v.replace("\n", nl), n.replace("\n", nl)) if nl == "\r\n" else (v, n)
        c = t.count(v2); assert c == k, (nome, c, v[:110]); t = t.replace(v2, n2)
    nb = t.encode("utf-8")
    if parse == "py":
        ast.parse(nb)
    elif parse == "snip":
        ast.parse(b"def _f(core, verdict, data_path, s):\n" + nb)
    assert nb.count(b"\r\n") == b0.count(b"\r\n") + (0 if nl == "\n" else sum(n.count("\n") - v.count("\n") for v, n, _ in trocas) * 0), "fim de linha preservado"
    tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
    print(nome, len(b0), "->", len(nb), hashlib.sha256(nb).hexdigest()[:16], "| trocas", len(trocas))


# (1) runtime_v410.py
troca("runtime_v410.py", [
    ("# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_d72_guarda_v410.py: a guarda do H0DN (D72): F53 (5 sigma atingido; o teste deu), F53b (H0DN detectado/confirmado no trecho), F53c (tokens de veredito do H0DN), F54 (obrigacao: onde H0DN aparecer, pré-registrado; nenhum dado observado lido)\n",
     "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_d72_guarda_v410.py: a guarda do teste da razao de Hubble (D72): F53 (o cinco-sigma dito alcancado; o teste dito como dado), F53b (a deteccao ou a confirmacao ditas no mesmo trecho do teste), F53c (os tokens de veredito do teste), F54 (a obrigacao: onde o nome do teste aparecer, pré-registrado; nenhum dado observado lido)\n", 1),
    (r"(?:observad|medid|detectad|vist|confirmad|observed|measured|detected|seen|confirmed)", r"(?:observad|medid|detectad|vist|observed|measured|detected|seen)", 1),
])
# (2) runtime_h0dn_v410.py
troca("runtime_h0dn_v410.py", [
    ('        {"id": "c10", "descricao": "a rota Kimi «coerencia espectro x fotometria» consta como NOT_TESTABLE (eta = 1; Mapa seq %s): nao e\' o teste" % rk_.get("mapa_seq"), "ok": bool(c10_ok_)},',
     '        {"id": "c10", "descricao": "a rota Kimi “coerencia espectro x fotometria” consta como NOT_TESTABLE (eta = 1; Mapa seq %s): nao e\' o teste" % rk_.get("mapa_seq"), "ok": bool(c10_ok_)},', 1),
    ('"cauda_nula_freeze": float(freeze_["null_alpha"]), "pinos": pinos_, "n_pinos": len(pinos_),',
     '"cauda_nula_freeze": float(freeze_["null_alpha"]), "pinos": pinos_, "n_pinos": len(pinos_), "n_pinos_freeze": c_["n_pinos_freeze"], "n_embutidos": len(c_["insumos"]),', 1),
])
# (3) registros_h0dn_v410.py e os snippets do H0DN
troca("registros_h0dn_v410.py", [
    ('"A rota Kimi «coerencia espectro x fotometria» consta como NOT_TESTABLE (eta = 1): não é o teste.', '"A rota Kimi “coerencia espectro x fotometria” consta como NOT_TESTABLE (eta = 1): não é o teste.', 1),
    ('"a rota Kimi «coerencia espectro x fotometria» e\' NOT_TESTABLE (eta = 1; nao e\' o teste);', '"a rota Kimi “coerencia espectro x fotometria” e\' NOT_TESTABLE (eta = 1; nao e\' o teste);', 1),
    ('"que a rota «coerencia espectro x fotometria» seja o teste: e\' NOT_TESTABLE (eta = 1)",', '"que a rota “coerencia espectro x fotometria” seja o teste: e\' NOT_TESTABLE (eta = 1)",', 1),
])
troca("artigo_pt_h0dn_v410.pysnip", [
    ("A rota «coerência espectro $\\times$ fotometria» consta como NOT\\_TESTABLE ($\\eta=1$): não é o teste. ", "A rota “coerência espectro $\\times$ fotometria” consta como NOT\\_TESTABLE ($\\eta=1$): não é o teste. ", 1),
    ("(\\texttt{FREEZE\\_R2}, \" + str(_vh410.get(\"n_pinos\") if isinstance(_vh410.get(\"n_pinos\"), int) else \"n/d\") + r\" pinos conferidos neste rito, os embutidos por sha256 e os só em disco se presentes). \"",
     "(\\texttt{FREEZE\\_R2}: \" + str(_vh410.get(\"n_pinos_freeze\") if isinstance(_vh410.get(\"n_pinos_freeze\"), int) else \"n/d\") + r\" pinos; \" + str(_vh410.get(\"n_pinos\") if isinstance(_vh410.get(\"n_pinos\"), int) else \"n/d\") + r\" conferidos neste rito, com o próprio \\texttt{FREEZE\\_R2} e a entrega; os embutidos por sha256, os só em disco se presentes). \"", 1),
], parse="snip")
troca("artigo_en_h0dn_v410.pysnip", [
    ("The route «spectrum $\\times$ photometry coherence» stands as NOT\\_TESTABLE ($\\eta=1$): it is not the test. ", "The route “spectrum $\\times$ photometry coherence” stands as NOT\\_TESTABLE ($\\eta=1$): it is not the test. ", 1),
    ("(\\texttt{FREEZE\\_R2}, \" + str(_vh410.get(\"n_pinos\") if isinstance(_vh410.get(\"n_pinos\"), int) else \"n/a\") + r\" pins checked in this rite, the embedded ones by sha256 and the on-disk ones if present). \"",
     "(\\texttt{FREEZE\\_R2}: \" + str(_vh410.get(\"n_pinos_freeze\") if isinstance(_vh410.get(\"n_pinos_freeze\"), int) else \"n/a\") + r\" pins; \" + str(_vh410.get(\"n_pinos\") if isinstance(_vh410.get(\"n_pinos\"), int) else \"n/a\") + r\" checked in this rite, with \\texttt{FREEZE\\_R2} itself and the delivery; the embedded ones by sha256, the on-disk ones if present). \"", 1),
], parse="snip")
# (4) registros_v410.py: a errata E30 no spec cunhagens_v410
troca("registros_v410.py", [
    ('             "lacuna_de_fidelidade": "a gerencia disse leitura o que o kernel ja\' tinha como termo; o operador corrigiu; o Nome finito e o projetor de Bell tem o traco igual ao posto (o_signo_do_nome; o_signo_do_par)", "estatuto": "[REAL: o_signo_do_nome e o_signo_do_par no kernel do rito]", "assinatura": ASSINA},\n'
     '            _errata_pisos_v409(cov_base)],\n',
     '             "lacuna_de_fidelidade": "a gerencia disse leitura o que o kernel ja\' tinha como termo; o operador corrigiu; o Nome finito e o projetor de Bell tem o traco igual ao posto (o_signo_do_nome; o_signo_do_par)", "estatuto": "[REAL: o_signo_do_nome e o_signo_do_par no kernel do rito]", "assinatura": ASSINA},\n'
     '            {"ao_lado_de": "a D72 (o AO LADO de 09/11 do DESENHO) e a funcao de veredito do registro h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido)", "dizia": "que o ramo z_null >= 5 e |z_tgl| <= 1,96 da funcao de veredito levava na cabeca a palavra popperiana do livro de cobrancas.", "agora": DL.ERRATA_E30,\n'
     '             "lacuna_de_fidelidade": "a gerencia repetiu a palavra do livro de cobrancas onde o operador pede a LEITURA do 5 sigma (beta_TGL provado na natureza (validade, não creditação) a n sigma; D76); a palavra do livro vai no campo outcome", "estatuto": "[INPUT: a correcao do operador de 09/11; REAL: a funcao de veredito congelada, testada em vetores deterministicos]", "assinatura": ASSINA},\n'
     '            _errata_pisos_v409(cov_base)],\n', 1),
])
# (5) delta_v410.py: a caixa baixa na D76
troca("delta_v410.py", [
    ("PROVADO = validade; CONFIRMADA = creditacao (o juizo de fora, que o um.py nao da), que segue recusada;", "PROVADO = validade; confirmada = creditacao (o juizo de fora, que o um.py nao da), que segue recusada;", 1),
])
# (6) o chain: REGS com o segundo registro com funcao
troca("pos_rito/chain_pos_rito_v410.sh", [
    ('REGS="iald2_v410 cunhagens_v410 kh_n1_cobertura_v410"\n', 'REGS="iald2_v410 h0dn_bg1_v410 cunhagens_v410 kh_n1_cobertura_v410"   # (09/11, D72: o segundo registro com funcao)\n', 1),
], parse="sh")
