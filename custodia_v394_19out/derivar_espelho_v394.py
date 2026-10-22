# -*- coding: utf-8 -*-
"""Deriva custodia_v394_espelho.py (custódia conjunta v393+v394 no espelho) do custodia_v392_espelho.py. Cada troca conferida por contagem."""
from pathlib import Path

T = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools")
s = (T / "custodia_v392_espelho.py").read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (a[:100], c, n)
    s = s.replace(a, b)


rep('r"""CUSTÓDIA v392 (13/10/2026; handoff v392, pin da 3ª tentativa; molde v391)',
    'r"""CUSTÓDIA CONJUNTA v393+v394 (19/10/2026; handoffs v393 e v394; a v393 nunca foi custodiada no espelho; molde v392): backup = v392; '
    'stdouts até a v394; + as FONTES PINADAS que o motor de registros relê por caminho absoluto (fontes_pinadas/, com mapa); + os diffs da '
    'v394; + os recibos do B(n) da Bancada. Do molde v392: CUSTÓDIA v392 (13/10/2026; handoff v392, pin da 3ª tentativa; molde v391)')
rep('REL = BANC / "revisoes" / "custodia_v392_espelho.json"', 'REL = BANC / "revisoes" / "custodia_v394_espelho.json"')
rep('VERSAO = "v392"', 'VERSAO = "v394"')
rep('STDOUTS = ("v383", "v384", "v385", "v386", "v387", "v388", "v389", "v390", "v391", "v392")',
    'STDOUTS = ("v383", "v384", "v385", "v386", "v387", "v388", "v389", "v390", "v391", "v392", "v393", "v394")')
rep('bk364 = sorted(BK.glob("um_v391_*"))   # (nome da variável herdado do molde; é o backup da v391)',
    'bk364 = sorted(BK.glob("um_v392_*"))   # (nome da variável herdado do molde; é o backup da v392)')
rep('assert bm["conferido_contra_origem"] is True and bm["versao"] == "v391", "BACKUP DA v391 NÃO CONFERE — PARAR"',
    'assert bm["conferido_contra_origem"] is True and bm["versao"] == "v392", "BACKUP DA v392 NÃO CONFERE — PARAR"')
rep('    sementes = []   # v392: uma versão só, nenhuma semente', '    sementes = []   # v394: conjunta v393+v394, sem sementes (a v393 entra pelo stdout e pelas fontes)')

# os blocos novos, depois dos diffs da v392
ancora = '''        pares.append((a_, ESP / "diferencas_v392" / nome, "DIFF"))
'''
novo = ancora + '''    # v394 (custódia conjunta v393+v394): os dois diffs da cadeia da v394 (a v393 não gerou diffs: o passo 11 da cadeia dela não rodou —
    # handoff v393; dito em nao_levados)
    for nome in ("DIFF_v393_v394.diff", "DIFF_KERNEL_v394.txt"):
        a_, b_ = CK / "v394" / nome, CK / "v394_kernel" / nome
        assert a_.is_file() and b_.is_file() and sha(a_) == sha(b_), "v394: %s diverge entre v394 e v394_kernel — PARAR" % nome
        pares.append((a_, ESP / "diferencas_v394" / nome, "DIFF"))
    # v394: as FONTES PINADAS. O motor de registros (v392, estendido pela v393 e pela v394) relê cada fonte pelo caminho ABSOLUTO desta
    # máquina e confere sha256 e bytes; sem elas, uma reprodução pública dá NOT_SEALED_THIS_RUN (handoff v394). Vão ao espelho em
    # fontes_pinadas/<caminho depois de C:\\IALD\\>, com o mapa (chave, dicionário, caminho exigido, sha256, bytes). Só entra o arquivo
    # cujo sha256 bate com o pino do um.py; o que não bate fica fora e dito.
    import ast as _ast
    _arv = _ast.parse((NOS / "um.py").read_text(encoding="utf-8"))
    _dic = {}
    for _n in _arv.body:
        if isinstance(_n, _ast.Assign) and len(_n.targets) == 1 and isinstance(_n.targets[0], _ast.Name) and _n.targets[0].id in (
                "_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2"):
            _dic[_n.targets[0].id] = _ast.literal_eval(_n.value)
    assert set(_dic) == {"_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2"}, sorted(_dic)
    FONTES_MAPA = []
    _vistos = set()
    for _nd, _d in sorted(_dic.items()):
        for _k, _v in sorted(_d.items()):
            _orig = (_v or {}).get("arquivo") if isinstance(_v, dict) else None
            if not _orig:
                continue
            _p = Path(_orig)
            _ent = {"dicionario": _nd, "chave": _k, "caminho_exigido_pelo_um_py": _orig, "sha256": _v.get("sha256"), "bytes": _v.get("bytes")}
            _rel = str(_p).replace("/", "\\\\")
            _pref = "C:\\\\IALD\\\\"
            assert _rel.upper().startswith(_pref.upper()), "fonte fora de C:\\\\IALD — PARAR: %s" % _orig
            _rel = Path(*Path(_rel[len(_pref):].replace("\\\\", "/")).parts)
            _dst = ESP / "fontes_pinadas" / _rel
            if not _p.is_file():
                _ent.update({"publicado": False, "motivo": "AUSENTE na casa"})
            elif _v.get("sha256") and sha(_p) != _v["sha256"]:
                _ent.update({"publicado": False, "motivo": "o arquivo da casa NÃO bate com o pino do um.py (errata da gerência ao lado; não se publica outro byte)"})
            else:
                _ent.update({"publicado": True, "caminho_no_espelho": str(_dst.relative_to(TB)).replace("\\\\", "/")})
                if str(_dst) not in _vistos:
                    _vistos.add(str(_dst))
                    pares.append((_p, _dst, "FONTE_TUNEL" if "\\\\Chatgpt\\\\" in str(_p) else "FONTE"))
            FONTES_MAPA.append(_ent)
    # v394: os recibos do B(n) da Bancada Um (aplicação, parada e religamento do serviço), localizados por sha256 do handoff
    _BS = Path(r"C:/IALD/Bancada_Um/estado/sincronizacao")
    _rec = {}
    for _p in sorted(_BS.rglob("*")):
        if _p.is_file() and ".bak_" not in _p.name:
            _h = sha(_p, 16)
            if _h in ("635577a30a836cc2", "c73822c96408a48c", "15041e927551dfa0"):
                _rec[_h] = _p
    assert set(_rec) == {"635577a30a836cc2", "c73822c96408a48c", "15041e927551dfa0"}, ("recibos do B(n) da v394 não achados por sha256 — PARAR", sorted(_rec))
    for _h, _p in sorted(_rec.items()):
        pares.append((_p, ESP / "recibos_bancada_v394" / _p.name, "RECIBO"))
'''
rep(ancora, novo)

# a varredura: o que vem do túnel (TUNEL e FONTE_TUNEL) pode ser barrado sem parar; o resto, para
rep('    criticos = [b for b in barrados if b["tipo"] != "TUNEL"]', '    criticos = [b for b in barrados if b["tipo"] not in ("TUNEL", "FONTE_TUNEL")]')
# o mapa das fontes, gravado depois da cópia
rep('    assert sha(ESP / "um.py", 16) == pin\n',
    '    assert sha(ESP / "um.py", 16) == pin\n'
    '    for _e in FONTES_MAPA:\n'
    '        if _e.get("publicado") and any(str(src) == _e["caminho_exigido_pelo_um_py"] or src == Path(_e["caminho_exigido_pelo_um_py"]) for src in barr):\n'
    '            _e.update({"publicado": False, "motivo": "barrado pela varredura de material privado (termo-guarda)", "caminho_no_espelho": None})\n'
    '    (ESP / "fontes_pinadas").mkdir(parents=True, exist_ok=True)\n'
    '    _mp = ESP / "fontes_pinadas" / "MAPA_FONTES_PINADAS.json"\n'
    '    _tmp = _mp.with_name(_mp.name + ".tmp_custodia")\n'
    '    _tmp.write_text(json.dumps({"gerado_em": datetime.now().isoformat(timespec="seconds"), "um_py_pin": selo["sha256"]["um.py"],\n'
    '        "leia": "O um.py relê cada fonte pelo caminho absoluto em caminho_exigido_pelo_um_py e confere sha256 e bytes; para reproduzir os "\n'
    '                "registros (v392–v394) em outra máquina, copie cada arquivo de caminho_no_espelho para esse caminho. Sem isso o registro "\n'
    '                "diz NOT_SEALED_THIS_RUN (fail-closed), por desenho.",\n'
    '        "n_fontes": len(FONTES_MAPA), "n_publicadas": sum(1 for _e in FONTES_MAPA if _e.get("publicado")), "fontes": FONTES_MAPA},\n'
    '        ensure_ascii=False, indent=1), encoding="utf-8")\n'
    '    _tmp.replace(_mp)\n'
    '    R["fontes_pinadas"] = {"n": len(FONTES_MAPA), "publicadas": sum(1 for _e in FONTES_MAPA if _e.get("publicado")),\n'
    '                           "fora": [(_e["chave"], _e["motivo"]) for _e in FONTES_MAPA if not _e.get("publicado")]}\n')
# o que não se leva (acréscimo)
rep('        "one_input.txt": "difere do espelho só no fim de linha (CRLF na casa); fica o do espelho",\n',
    '        "one_input.txt": "difere do espelho só no fim de linha (CRLF na casa); fica o do espelho",\n'
    '        "HANDOFF_v393_CUSTODIA.md e HANDOFF_v394_CUSTODIA.md": "documentos de trabalho; ficam no Nós e no cofre da Central (um_unificado_v394)",\n'
    '        "diffs da v393": "não existem: o passo 11 da cadeia da v393 (manifesto de arquivo, diffs) não rodou — handoff v393, dito",\n'
    '        "um.py da v393": "só o stdout da v393 vai ao espelho; o selo vigente é a v394 (o um.py da v393 fica no cofre e no backup)",\n'
    '        "work/cadeia_de_selo/v393_kernel e v394_kernel/pedras": "os 193 módulos novos chegam ao espelho pela cópia do kernel (tgl_kernel), conferidos arquivo a arquivo contra o manifesto",\n')
(T / "custodia_v394_espelho.py").write_text(s, encoding="utf-8")
print("ok custodia_v394_espelho.py", len(s))
