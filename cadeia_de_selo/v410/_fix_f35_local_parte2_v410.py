# -*- coding: utf-8 -*-
"""_fix_f35_local_parte2_v410.py -- ACHADO do pre-teste do ensaio (09/11, noite): o filtro da F35 herdada (a palavra do Clay dita resolvida) caia para o TEXTO INTEIRO quando ele trazia, em qualquer ponto, a forma da D83/D84; com isso oito frases secas
(a TGL dita resolvendo o problema do milenio, e variantes) PASSAVAM quando plantadas num texto que tinha a forma canonica noutro ponto. Conserto na causa: a F35 so' cai quando o PROPRIO trecho (com os 40 caracteres seguintes) traz a forma da D83/D84 e o texto traz a creditacao;
a frase seca noutro ponto continua reprovada. A guarda_frases_v410 ganha o controle. Tambem: o ensaio conta DOIS contratos novos com expected_ladder (iald2 e a_escala). Backup de BYTES; temporario -> conferir tamanho -> substituir; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S"); BS = chr(92)


def aplicar(nome, trocas):
    p = os.path.join(HERE, nome); b0 = open(p, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
    for a, b in trocas:
        c = t.count(a); assert c == 1, (nome, c, a[:140]); t = t.replace(a, b)
    nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8"); ast.parse(nb)
    open(p + ".bak_" + TS + "_pre_f35_local", "wb").write(b0)
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    print(nome, len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16])


S = BS + "s"
aplicar("runtime_v410.py", [
    ('    out_ = [v_ for v_ in _v409_guarda_frases(txt_) if not ((v_[0].startswith("F37_") or v_[0].startswith("F34_")) and q_rel_ and q_fora_)',
     '    _FORMA83_ = r"no' + S + '+sentido' + S + '+do' + S + '+operador|in' + S + '+the' + S + "+operator'?s" + S + '+sense|tal' + S + '+qual' + S + '+apresentad[oa]' + S + '+pela' + S + '+TGL|as' + S + '+presented' + S + '+by' + S + '+(?:the' + S + '+)?TGL"\n'
     '    _s1_ = s_.replace("' + BS + 'n", " ")\n'
     '\n'
     '    def _f35_local_(tr_):   # (a F35 herdada so\' cai quando o PROPRIO trecho, com os 40 caracteres seguintes, traz a forma da D83/D84; uma frase seca noutro ponto do texto continua reprovada)\n'
     '        i_ = _s1_.find(tr_)\n'
     '        return bool(_re.search(_FORMA83_, (_s1_[i_:i_ + len(tr_) + 40] if i_ >= 0 else tr_), _re.I))\n'
     '\n'
     '    out_ = [v_ for v_ in _v409_guarda_frases(txt_) if not ((v_[0].startswith("F37_") or v_[0].startswith("F34_")) and q_rel_ and q_fora_)'),
    ('and not (v_[0].startswith("F35_") and q_d83_)]', 'and not (v_[0].startswith("F35_") and q_d83_ and _f35_local_(v_[1]))]'),
])
aplicar("guarda_frases_v410.py", [
    ('                            "forma_obrigatoria_d81_passa": not G(DL.FRASE_D81_PT) and not G(DL.FRASE_D81_EN),\n',
     '                            "forma_obrigatoria_d81_passa": not G(DL.FRASE_D81_PT) and not G(DL.FRASE_D81_EN),\n'
     '                            "clay_seco_junto_da_forma_canonica_reprova": bool(G(DL.FRASE_D83_OBRIGATORIA_PT + ". Outra coisa: a TGL resolve o problema do milênio.")) and bool(G(DL.FRASE_CLAY_CANONICA_PT + " E mais: o problema do milênio está resolvido.")) and bool(G(DL.FRASE_D83_OBRIGATORIA_EN + ". Besides: the millennium problem is solved."))\n'
     '                                                                         and not G(DL.FRASE_D83_OBRIGATORIA_PT) and not G(DL.FRASE_D83_OBRIGATORIA_EN) and not G(DL.FRASE_CLAY_CANONICA_PT) and not G(DL.FRASE_CLAY_CANONICA_EN),   # (achado do pre-teste do ensaio, 09/11: a F35 so\' cai no PROPRIO trecho que traz a forma da D83/D84)\n'),
])
aplicar("ensaio_a_seco_v410.py", [
    ('_n_esc_cand == _n_esc_base + 1 and not re.search(', '_n_esc_cand == _n_esc_base + 2 and not re.search('),
])
