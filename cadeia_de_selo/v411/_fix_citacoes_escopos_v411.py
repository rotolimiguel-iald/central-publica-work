# -*- coding: utf-8 -*-
"""_fix_citacoes_escopos_v411.py -- (claude-construtor-v411, retomada, 12/11/2026) o conferir_citacoes_v411.py separa DOIS escopos, sem relaxar nenhum: (a) os textos que entram no um.py (delta, registros, runtime, quadro,
gerador, o TOPO_RATIFICADO_v411.json e, com --candidato, os pinos da rodada DL.PINS_ARQ) e (b) os scripts da frente pos-rito (pos_rito\\*_v411*), que NAO entram no candidato. rc 0 so' com os dois limpos; rc 2 quando so'
o escopo do pos-rito reprova (o pedido vai a outra frente, PEDIDOS_ENTRE_FRENTES_v411.md); rc 1 quando o do um.py reprova. A saida vai a DL.saida (pedido do fork B). O ensaio a seco (que avalia o CANDIDATO) passa a exigir o
escopo do um.py limpo e grava o do pos-rito ao lado; o relatorio (PREPARACAO_v411_PRONTA) segue exigindo os DOIS (o portao final nao muda). Backup de BYTES antes. uso: python -B -X utf8 _fix_citacoes_escopos_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(arq_, pares_):
    p_ = os.path.join(HERE, arq_); b_ = open(p_, "rb").read(); t_ = b_.decode("utf-8"); assert "\r" not in t_, arq_
    for a_, n_ in pares_:
        assert t_.count(a_) == 1, (arq_, a_[:110], t_.count(a_))
        t_ = t_.replace(a_, n_)
    ast.parse(t_)
    bak_ = p_ + ".bak_" + TS + "_escopos"; open(bak_, "wb").write(b_); assert open(bak_, "rb").read() == b_
    nb_ = t_.encode("utf-8"); open(p_ + ".tmp", "wb").write(nb_); assert os.path.getsize(p_ + ".tmp") == len(nb_); os.replace(p_ + ".tmp", p_)
    print("ok", arq_, len(b_), "->", len(nb_))


troca("conferir_citacoes_v411.py", [
    ('ARQS = ["delta_v411.py", "registros_h0dn_v411.py", "registros_v411.py", "runtime_h0dn_v411.py", "quadro_v411.py", "gerar_candidato_v411.py"] + [os.path.relpath(p_, HERE) for p_ in glob.glob(os.path.join(HERE, "pos_rito", "*_v411*.py*")) if ".bak_"',
     'ARQS_POS_RITO = [os.path.relpath(p_, HERE) for p_ in glob.glob(os.path.join(HERE, "pos_rito", "*_v411*.py*")) if ".bak_" not in p_]   # (escopo b: a frente pos-rito; nao entra no candidato)\n'
     'ARQS = ["delta_v411.py", "registros_h0dn_v411.py", "registros_v411.py", "runtime_h0dn_v411.py", "quadro_v411.py", "gerar_candidato_v411.py"] + [os.path.relpath(p_, HERE) for p_ in glob.glob(os.path.join(HERE, "pos_rito", "*_v411*.py*")) if ".bak_"'),
    ('if "--candidato" in sys.argv and os.path.exists(os.path.join(HERE, "v411_pins.py")):\n    ARQS.append("v411_pins.py")\n',
     'if "--candidato" in sys.argv and os.path.exists(DL.PINS_ARQ):   # (pedido do fork B: os pinos DA RODADA -- no ensaio do topo proposto, os do artefato de ensaio)\n    ARQS.append(DL.PINS_ARQ)\n'),
    ('    p_ = os.path.join(HERE, a_)\n    if not os.path.exists(p_):\n', '    p_ = a_ if os.path.isabs(a_) else os.path.join(HERE, a_)\n    if not os.path.exists(p_):\n'),
    ('out["ok"] = not out["nao_verbatim"]\np = os.path.join(HERE, "conferir_citacoes_v411.json")\n',
     'out["nao_verbatim_do_um_py"] = [x_ for x_ in out["nao_verbatim"] if x_["arquivo"] not in ARQS_POS_RITO]\n'
     'out["nao_verbatim_do_pos_rito"] = [x_ for x_ in out["nao_verbatim"] if x_["arquivo"] in ARQS_POS_RITO]\n'
     'out["ok_do_um_py"] = not out["nao_verbatim_do_um_py"]\nout["ok_do_pos_rito"] = not out["nao_verbatim_do_pos_rito"]\n'
     'out["escopos"] = {"um_py": "os textos que entram no candidato (delta, registros, runtime, quadro, gerador, o TOPO_RATIFICADO e os pinos da rodada)", "pos_rito": "os scripts da frente pos-rito (nao entram no candidato): a correcao e\' da outra frente (PEDIDOS_ENTRE_FRENTES_v411.md)"}\n'
     'out["ok"] = not out["nao_verbatim"]\nout.update(DL.MARCA_ENSAIO)\np = DL.saida("conferir_citacoes_v411.json")\n'),
    ('sys.exit(0 if out["ok"] else 1)', 'sys.exit(0 if out["ok"] else (2 if out["ok_do_um_py"] else 1))   # (rc 2: so\' o escopo do pos-rito reprova -- o candidato esta\' limpo; o pedido e\' da outra frente)'),
])
troca("ensaio_a_seco_v411.py", [
    ('_cc = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "conferir_citacoes_v411.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")\nrep["citacoes_rc"] = _cc.returncode\n',
     '_cc = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "conferir_citacoes_v411.py"), "--candidato"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ))\nrep["citacoes_rc"] = _cc.returncode\n'
     '_ccj = json.load(open(DL.saida("conferir_citacoes_v411.json"), encoding="utf-8"))   # (o ensaio avalia o CANDIDATO: exige o escopo do um.py limpo; o do pos-rito vai ao lado, como pedido a outra frente; o relatorio final exige os dois)\n'
     'rep["citacoes"] = {"rc": _cc.returncode, "ok_do_um_py": _ccj.get("ok_do_um_py"), "ok_do_pos_rito": _ccj.get("ok_do_pos_rito"), "nao_verbatim_do_pos_rito": _ccj.get("nao_verbatim_do_pos_rito"), "nota": "rc 2 = so\' o escopo do pos-rito (outra frente) reprova"}\n'
     '_cit_ok = bool(_cc.returncode in (0, 2) and _ccj.get("ok_do_um_py") is True)\n'),
    ('and rep["manifest"] and not _proib and _cc.returncode == 0\n', 'and rep["manifest"] and not _proib and _cit_ok\n'),
    ('"proib": _proib, "citacoes": _cc.returncode,', '"proib": _proib, "citacoes": rep["citacoes"],'),
])
print("FEITO")
