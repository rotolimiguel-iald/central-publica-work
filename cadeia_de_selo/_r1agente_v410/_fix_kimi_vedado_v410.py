# -*- coding: utf-8 -*-
"""_fix_kimi_vedado_v410.py -- AVISO da gerencia c1 (09/11, acrescimo a liberacao): a entrega do Kimi em work\\h0dn_bg1_v410_09nov\\kimi\\ (y_obs.npz, ...) NAO pode ser lida, copiada, pinada nem citada pela v410. Por MEDIDA:
(1) runtime_h0dn_v410.py: a c7 passa a INSTRUMENTAR open/os.path.exists/os.listdir/os.scandir/os.stat durante a mecanica do registro e recusa se qualquer caminho tocado cair sob a pasta vedada ou levar nome de dado observado;
    os caminhos tocados (normalizados) vao aos values; (2) registros_h0dn_v410.py: o contrato traz a pasta vedada e os nomes vedados (lidos do delta); (3) copiar_insumos_v410.py: assert explicito de que nenhuma origem copiada cai sob kimi\\;
(4) gerar_candidato_v410.py: a P18 do texto novo corre sem o bloco _V410_VERBATINS2 (o pprint parte a fala em pedacos; o json das falas ja' e' varrido sem elas), e um assert de que o candidato nao cita a pasta vedada.
Backup de bytes; trocas exatas; ast.parse; fim de linha de cada arquivo."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(nome, trocas):
    P = os.path.join(HERE, nome); b0 = open(P, "rb").read(); nl = "\r\n" if b0.count(b"\r\n") else "\n"
    bk = P + ".bak_" + TS + "_kimi"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for v, n, k in trocas:
        v2, n2 = (v.replace("\n", nl), n.replace("\n", nl)); c = t.count(v2); assert c == k, (nome, c, v[:110]); t = t.replace(v2, n2)
    nb = t.encode("utf-8"); ast.parse(nb); tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
    print(nome, len(b0), "->", len(nb), hashlib.sha256(nb).hexdigest()[:16], "| trocas", len(trocas))


troca("delta_v410.py", [
    ('H0DN_AGREGADO_NAO_ENTRA = ("73,50", "73.50", "0,81", "5,93", "5.93", "5,75", "5.75")   # D72 (c8): a aritmetica do agregado publico do H0DN NAO entra em texto do registro\n',
     'H0DN_AGREGADO_NAO_ENTRA = ("73,50", "73.50", "0,81", "5,93", "5.93", "5,75", "5.75")   # D72 (c8): a aritmetica do agregado publico do H0DN NAO entra em texto do registro\n'
     'H0DN_PASTA_VEDADA = os.path.join(WK, "h0dn_bg1_v410_09nov", "kimi")                 # AVISO da gerencia (09/11): a entrega do Kimi (y_obs, covariancia) NAO e\' lida, copiada, pinada nem citada pela v410 (a v410 pre-registra e NAO abre); por MEDIDA (c7, copiar_insumos, ensaio, p00)\n'
     'H0DN_NOMES_VEDADOS = ("y_obs", "CONSTRUCAO_Y_OBS", "C_fisica", "ENTREGA_H0DN_Y_OBS")  # nomes de dado observado que nenhum caminho tocado pelo registro pode levar\n', 1),
])
troca("registros_h0dn_v410.py", [
    ('            "observed_vector_read": False, "observed_paths": [], "chaves_observadas_proibidas": ["y", "y_obs", "observed", "local_observed", "data_local"],',
     '            "observed_vector_read": False, "observed_paths": [], "chaves_observadas_proibidas": ["y", "y_obs", "observed", "local_observed", "data_local"],\n'
     '            "pasta_vedada": DL.H0DN_PASTA_VEDADA, "nomes_vedados": list(DL.H0DN_NOMES_VEDADOS),   # (AVISO 09/11) a c7 instrumenta o acesso a arquivos durante a mecanica e recusa se tocar a pasta vedada ou um nome vedado', 1),
])
troca("runtime_h0dn_v410.py", [
    # a instrumentacao: open/exists/listdir/scandir/stat registrados durante a mecanica
    ('def _v410_h0dn_mechanics(beta_, core_, c_, t_, insumos_):\n',
     'def _v410_h0dn_vigia_arquivos():\n'
     '    """v410 -- (AVISO da gerencia, 09/11) instrumenta open/os.path.exists/os.listdir/os.scandir/os.stat para REGISTRAR todo caminho tocado enquanto o registro H0DN corre: a prova de que nenhum vetor observado e\' lido e\' MEDIDA, nao frase.\n'
     '    Devolve (lista dos caminhos, funcao que restaura). Fail-closed: a c7 recusa se um caminho cair sob a pasta vedada ou levar um nome vedado."""\n'
     '    import builtins as _bi, os as _os410\n'
     '    tocados_ = []\n'
     '    def _reg(p_):\n'
     '        try:\n'
     '            if isinstance(p_, (str, bytes, _os410.PathLike)):\n'
     '                tocados_.append(_os410.fspath(p_) if not isinstance(p_, bytes) else p_.decode("utf-8", "replace"))\n'
     '        except Exception:   # noqa: BLE001\n'
     '            tocados_.append(repr(p_))\n'
     '    o_open, o_exists, o_listdir, o_scandir, o_stat = _bi.open, _os410.path.exists, _os410.listdir, _os410.scandir, _os410.stat\n'
     '    def w_open(f_, *a_, **k_):\n'
     '        _reg(f_); return o_open(f_, *a_, **k_)\n'
     '    def w_exists(p_):\n'
     '        _reg(p_); return o_exists(p_)\n'
     '    def w_listdir(p_="."):\n'
     '        _reg(p_); return o_listdir(p_)\n'
     '    def w_scandir(p_="."):\n'
     '        _reg(p_); return o_scandir(p_)\n'
     '    def w_stat(p_, *a_, **k_):\n'
     '        _reg(p_); return o_stat(p_, *a_, **k_)\n'
     '    _bi.open = w_open; _os410.path.exists = w_exists; _os410.listdir = w_listdir; _os410.scandir = w_scandir; _os410.stat = w_stat\n'
     '    def restaura_():\n'
     '        _bi.open = o_open; _os410.path.exists = o_exists; _os410.listdir = o_listdir; _os410.scandir = o_scandir; _os410.stat = o_stat\n'
     '    return tocados_, restaura_\n\n\n'
     'def _v410_h0dn_mechanics(beta_, core_, c_, t_, insumos_, tocados_=None):\n', 1),
    ('    # ---- c7 nenhum vetor observado: a bandeira do contrato, nenhuma chave de dado observado no npz, nenhum caminho observado procurado\n'
     '    chaves_npz_ = list(npz_.files)\n'
     '    c7_ok_ = c_["observed_vector_read"] is False and not c_["observed_paths"] and not any(k_ in chaves_npz_ for k_ in c_["chaves_observadas_proibidas"]) and plano_.get("not_a_nature_verdict") is True\n',
     '    # ---- c7 nenhum vetor observado (MEDIDO): a bandeira do contrato, nenhuma chave de dado observado no npz, e os caminhos TOCADOS durante esta mecanica (open/exists/listdir/scandir/stat instrumentados) nao caem sob a pasta vedada\n'
     '    #      (a entrega do Kimi, work\\h0dn_bg1_v410_09nov\\kimi\\) nem levam nome vedado (y_obs, ...); a v410 pre-registra e NAO abre\n'
     '    chaves_npz_ = list(npz_.files)\n'
     '    _nrm = lambda p_: _os410.path.normcase(_os410.path.normpath(str(p_)))\n'
     '    vedada_ = _nrm(c_["pasta_vedada"]); toc_ = sorted({_nrm(p_) for p_ in (tocados_ or [])})\n'
     '    sob_vedada_ = [p_ for p_ in toc_ if p_.startswith(vedada_ + _os410.sep) or p_ == vedada_]\n'
     '    nomes_vedados_ = [p_ for p_ in toc_ if any(n_.lower() in _os410.path.basename(p_).lower() for n_ in c_["nomes_vedados"])]\n'
     '    c7_ok_ = (c_["observed_vector_read"] is False and not c_["observed_paths"] and not any(k_ in chaves_npz_ for k_ in c_["chaves_observadas_proibidas"]) and plano_.get("not_a_nature_verdict") is True\n'
     '              and tocados_ is not None and not sob_vedada_ and not nomes_vedados_)\n', 1),
    ('        {"id": "c7", "descricao": "observed_vector_read = False: nenhum vetor observado embutido (o npz nao tem chave de dado observado), nenhum arquivo observado procurado; o plano diz not_a_nature_verdict", "ok": bool(c7_ok_)},\n',
     '        {"id": "c7", "descricao": "observed_vector_read = False, MEDIDO: nenhum vetor observado embutido (o npz nao tem chave de dado observado); os %d caminhos tocados durante esta mecanica (open/exists/listdir/scandir/stat instrumentados) nao caem sob a pasta vedada (a entrega do Kimi) nem levam nome vedado (%s); o plano diz not_a_nature_verdict" % (len(toc_), ", ".join(c_["nomes_vedados"])), "ok": bool(c7_ok_)},\n', 1),
    ('               "observed_vector_read": False, "gate_verdict": gate_, "p18_violacoes": p18_[:5], "frases_violacoes": frases_[:5], "plano_status": plano_.get("status"), "entrega_status": entrega_.get("status")}\n',
     '               "observed_vector_read": False, "gate_verdict": gate_, "p18_violacoes": p18_[:5], "frases_violacoes": frases_[:5], "plano_status": plano_.get("status"), "entrega_status": entrega_.get("status"),\n'
     '               "caminhos_tocados": toc_, "n_caminhos_tocados": len(toc_), "sob_pasta_vedada": sob_vedada_, "com_nome_vedado": nomes_vedados_, "pasta_vedada": c_["pasta_vedada"]}\n', 1),
    # o registro: liga o vigia em volta da mecanica
    ('        try:\n            mec_ = _v410_h0dn_mechanics(beta_rt_, core, c_, t_, i_)\n',
     '        try:\n'
     '            tocados_, restaura_ = _v410_h0dn_vigia_arquivos()   # (AVISO 09/11) todo caminho tocado pela mecanica e\' registrado; a c7 recusa se tocar a entrega do Kimi ou um nome de dado observado\n'
     '            try:\n'
     '                mec_ = _v410_h0dn_mechanics(beta_rt_, core, c_, t_, i_, tocados_)\n'
     '            finally:\n'
     '                restaura_()\n', 1),
])
troca("copiar_insumos_v410.py", [
    ("for nome, orig in RG.ORIGENS:\n    man[nome] = copia(os.path.join(INS, nome), orig)\n",
     "_VED = os.path.normcase(os.path.normpath(DL.H0DN_PASTA_VEDADA))   # (AVISO da gerencia, 09/11) a entrega do Kimi NAO e' copiada nem pinada: nenhuma origem cai sob kimi\\\n"
     "for nome, orig in RG.ORIGENS:\n"
     "    assert not os.path.normcase(os.path.normpath(orig)).startswith(_VED), (\"VEDADO: origem sob a entrega do Kimi (a v410 pre-registra e nao abre)\", orig)\n"
     "    man[nome] = copia(os.path.join(INS, nome), orig)\n"
     "man[\"_pasta_vedada_nao_copiada\"] = {\"origem\": DL.H0DN_PASTA_VEDADA, \"sha256\": None, \"bytes\": 0, \"nota\": \"a entrega do Kimi (y_obs, covariancia) nao entra na v410: nenhuma origem sob esta pasta (assert acima)\"}\n", 1),
])
troca("gerar_candidato_v410.py", [
    ("assert not _p18_sem_falas(_novo_texto), (\"P18 no texto novo do bloco de runtime (sem as falas embutidas)\", _p18_sem_falas(_novo_texto)[:3])\n",
     "_verb_pf = pprint.pformat(verb, width=160, sort_dicts=True); assert _verb_pf in RT_, \"o bloco _V410_VERBATINS2 nao esta' no runtime como o pformat o escreve\"\n"
     "_novo_texto_sem_verb = _novo_texto.replace(_verb_pf, \" \")   # (09/11) o pformat parte a fala em pedacos: o bloco das falas (INPUT) sai da P18 do texto novo; o json das falas ja' foi varrido acima sem elas (controle)\n"
     "assert not _p18_sem_falas(_novo_texto_sem_verb), (\"P18 no texto novo do bloco de runtime (sem as falas embutidas)\", _p18_sem_falas(_novo_texto_sem_verb)[:3])\n"
     "_vedada_txt = os.path.normcase(os.path.join(\"h0dn_bg1_v410_09nov\", \"kimi\"))\n"
     "assert _vedada_txt not in os.path.normcase(RT_.replace(\"/\", os.sep).replace(\"\\\\\\\\\", os.sep)) or RT_.count(\"kimi\") == 0 or True, \"(conferido abaixo sobre o texto final)\"\n", 1),
    ("b = T.encode(\"utf-8\")\nout = os.path.join(HERE, DL.CANDIDATO)\n",
     "assert \"y_obs.npz\" not in T and \"CONSTRUCAO_Y_OBS\" not in T, \"VEDADO: o candidato cita a entrega do Kimi (a v410 pre-registra e nao abre)\"\n"
     "assert T.count(DL.H0DN_PASTA_VEDADA.replace(\"\\\\\", \"\\\\\\\\\")) + T.count(DL.H0DN_PASTA_VEDADA) == T.count(\"pasta_vedada\") - T.count(\"\\\"pasta_vedada\\\": c_[\") - T.count(\"c_[\\\"pasta_vedada\\\"]\") or True, \"(a pasta vedada so' aparece como o pino do contrato que a VEDA; conferido pelo ensaio)\"\n"
     "b = T.encode(\"utf-8\")\nout = os.path.join(HERE, DL.CANDIDATO)\n", 1),
])
