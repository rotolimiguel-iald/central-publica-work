# -*- coding: utf-8 -*-
"""_fix_s6d_e_aviso_harness_parte2_v410.py -- (1) orquestrador\\pos_treino_v410.py, S6d: a checagem da D59 sobre o handoff seguia a regra da v409 (o nome do executor vetado em qualquer texto) e reprovaria o handoff REAL da v410, que nomeia o executor so' no contexto do H0DN (D72, D77(g));
passa a seguir a MESMA regra de pos_rito\\registrar_mapa_v410.d59_viola (o que a D59 deixa fora segue vetado em qualquer texto; o nome do executor so' onde ha' H0DN). Achado do agente de depuracao do harness (09/11, noite), conferido no arquivo (l.435).
(2) gerar_relatorio_v410.py: um terceiro aviso, DITO, sobre a primeira rodada dos harnesses do pos-rito e os consertos (sha16 antes -> depois lidos dos backups de bytes e dos arquivos; a contagem dos controles lida da saida do harness).
Backup de BYTES; temporario -> conferir tamanho -> substituir; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S"); BS = chr(92)


def aplicar(rel, trocas, sufixo):
    p = os.path.join(HERE, rel); b0 = open(p, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
    for a, b in trocas:
        c = t.count(a); assert c == 1, (rel, c, a[:140]); t = t.replace(a, b)
    nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8"); ast.parse(nb)
    open(p + ".bak_" + TS + "_" + sufixo, "wb").write(b0)
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    print(rel, len(b0), "->", len(nb), "| sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16])


aplicar(os.path.join("orquestrador", "pos_treino_v410.py"), [
    ('            if re.search(r"(?i)kimi|mil[eê]nio|millennium|navier|lindão", ht):\n',
     '            if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", ht) or (re.search(r"(?i)kimi", ht) and not re.search(r"(?i)h0dn", ht)):   # (09/11, D72 e D77(g): a mesma regra de pos_rito' + BS + BS + 'registrar_mapa_v410.d59_viola -- o nome do executor so\' no contexto do H0DN; o resto do que a D59 deixa fora segue vetado em qualquer texto)\n'),
], "pre_d59_s6d")
aplicar("gerar_relatorio_v410.py", [
    ('if _apont_gf:\n',
     '_arqs_h90 = ("pos_rito/textos_v410.py", "pos_rito/leitura_v410.py", "pos_rito/harness_textos_ensaio_v410.py", "pos_rito/harness_fechar_sandbox_v410.py", "pos_rito/registrar_mapa_v410.py", "orquestrador/pos_treino_v410.py")\n'
     '\n'
     '\n'
     'def _antes_depois_h90(rel_):\n'
     '    bk_ = sorted(_glob90.glob(P(rel_ + ".bak_20261109_2*")))   # (os backups de bytes desta noite, das 20h em diante: o mais antigo e\' o estado de ANTES da primeira rodada dos harnesses)\n'
     '    return "%s %s -> %s" % (rel_, (hashlib.sha256(open(bk_[0], "rb").read()).hexdigest()[:16] if bk_ else "backup ausente"), (h16(rel_) if os.path.exists(P(rel_)) else "ausente"))\n'
     '\n'
     '\n'
     '_ht90 = open(P("pos_rito/harness_textos_out_v410.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("pos_rito/harness_textos_out_v410.txt")) else ""\n'
     'AVISOS.append("os harnesses do pos-rito NUNCA tinham rodado na v410; a primeira rodada do harness dos textos (20:55) caiu e os defeitos foram corrigidos na causa, todos fora do candidato (ele nao mudou): (a) os textos do pos-rito liam o quadro_v397 da pasta da v409 pela ordem do sys.path (e, por ele, o delta da v409): agora o quadro e\' carregado pelo caminho do pacote; "\n'
     '              "(b) tres controles negativos eram mutacoes nulas (o rotulo errado da linha do stdout da v408, em dois; a forma canonica do Clay tirada so\' de um campo, em um) e um quarto trocava uma frase que o paragrafo nao tem; (c) a errata E31 renderizada com o rotulo na mesma linha fazia a regra F37b da guarda cortar o qualificador (o trecho e\' cortado em 200 caracteres): o rotulo foi para linha propria, e a fragilidade da guarda fica DITA para a versao seguinte (a guarda esta\' embutida no candidato e nao foi tocada); "\n'
     '              "(d) a linha das ressalvas do teste da razao de Hubble ganhou a clausula-padrao da regra da ordem do quadro; (e) a checagem da D59 no harness e no S6d do orquestrador seguia a regra da v409 e reprovaria o handoff por nomear o executor da ORDEM do teste: passou a seguir a D77(g), a mesma regra de registrar_mapa_v410.d59_viola; (f) o harness do fechar ganhou a pasta irma da v408, o campo pasta_vedada traduzido para o sandbox e a copia do conferidor nas variantes; a checagem da forma do Clay em registrar_mapa passou a ser por campo e trecho. "\n'
     '              "Rodada final: harness dos textos com %d controles negativos reprovados como esperado e %d que nao reprovaram; harness do fechar rc 0. Arquivos (sha16 antes -> depois): %s"\n'
     '              % (_ht90.count("REPROVOU como esperado") - _ht90.count("NAO REPROVOU como esperado"), _ht90.count("NAO REPROVOU como esperado"), "; ".join(_antes_depois_h90(r_) for r_ in _arqs_h90)))\n'
     'if _apont_gf:\n'),
], "pre_aviso_harness")
