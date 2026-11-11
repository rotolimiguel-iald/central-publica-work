# -*- coding: utf-8 -*-
"""_r5ag_01_congelado_v410.py -- R5 (D100 e D101; ADENDOS 5 e 6): a lista congelada das falas passa de 26 a 28 (as duas de 10/11: a clausula do Tetelestai e o «confirmo tudo»). Backup de BYTES do congelado anterior ao lado; o novo e' gravado por temporario
com a MESMA estrutura que copiar_insumos_v410.py grava (contrato, quando, n, arquivos, registro com sha256 e bytes LIDOS de cada arquivo, fora_do_desenho, nota); a lista `arquivos` e' a anterior mais as duas falas, em ordem de nome (como o glob);
`fora_do_desenho` e' CARREGADO do congelado anterior (as tres falas de 10/11 que chegaram depois ficam fora e ditas a parte em VERBATIM_CHEGARAM_DEPOIS_V410, como hoje). Nada digitado: os hashes sao lidos dos arquivos."""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE))
CUN = os.path.join(WK, "cunhagens_13out")
NOVAS = ["OPERADOR_10nov_a_clausula_do_tetelestai_esta_no_acom_mirror_um_menos_beta_beta_e_o_operador_modular_verbatim.txt",
         "OPERADOR_10nov_confirmo_tudo_nomeio_e_o_numero_corrige_o_nome_como_zero_modular_verbatim.txt"]
CONG = os.path.join(HERE, "VERBATIM_CONGELADO_v410.json")
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(CONG, "rb").read(); c0 = json.loads(b0.decode("utf-8"))
assert c0["n"] == len(c0["arquivos"]) == len(c0["registro"]) == 26, ("o congelado nao e' o de 26 falas", c0["n"])
bak = CONG + ".bak_%s_26_falas_antes_r5_agente" % ts
open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
sha = lambda b: hashlib.sha256(b).hexdigest()
novos = [os.path.join(CUN, n_) for n_ in NOVAS]
assert all(os.path.exists(p_) for p_ in novos) and not (set(novos) & set(c0["arquivos"]))
arqs = sorted(list(c0["arquivos"]) + novos, key=lambda p_: os.path.basename(p_))
assert [p_ for p_ in c0["arquivos"]] == sorted(c0["arquivos"], key=lambda p_: os.path.basename(p_)), "a lista anterior nao estava em ordem de nome"
reg = [{"arquivo": p_, "sha256": sha(open(p_, "rb").read()), "bytes": os.path.getsize(p_), "autor": "operador"} for p_ in arqs]
n_so_trecho = 4   # lido abaixo do delta; aqui so' conferido contra a nota anterior
assert "de 4, so' o trecho" in c0["nota"]
nota = ("as %d falas (06 a 10/11/2026) que esta versao embute (as oito do DESENHO_v410 §3, a do AO LADO de 06/11, as duas do AO LADO da retomada de 09/11, as duas do AO LADO das decisoes de 09/11, a da E30 e a da D76; as da escala, do Clay e das ratificacoes de 09/11; "
        "as cinco de 10/11 dos ADENDOS 2, 3, 5 e 6, D94, D96, D100 e D101); de %d, so' o trecho e' embutido e citado (D65; a ordem de 09/11; as tres copias de 08/11; a leitura do 5 sigma); lista de trabalho da cadeia (NAO pinada como fonte: traz os caminhos de origem)" % (len(arqs), n_so_trecho))
c = {"contrato": "VERBATIM_CONGELADO_v410", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "n": len(arqs), "arquivos": arqs, "registro": reg, "fora_do_desenho": dict(c0.get("fora_do_desenho") or {}), "nota": nota}
b = json.dumps(c, ensure_ascii=False, indent=1).encode("utf-8")
open(CONG + ".tmp", "wb").write(b); assert os.path.getsize(CONG + ".tmp") == len(b); os.replace(CONG + ".tmp", CONG)
c1 = json.loads(open(CONG, "rb").read().decode("utf-8"))
assert c1["n"] == len(c1["arquivos"]) == len(c1["registro"]) == 28 and all(os.path.exists(p_) for p_ in c1["arquivos"]) and len(set(c1["arquivos"])) == 28
print("VERBATIM_CONGELADO_v410.json: 26 -> 28 falas | backup", os.path.basename(bak), "| sha16", sha(b)[:16], "| fora_do_desenho:", list(c1["fora_do_desenho"]))
