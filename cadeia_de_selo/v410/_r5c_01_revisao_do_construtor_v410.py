# -*- coding: utf-8 -*-
"""_r5c_01_revisao_do_construtor_v410.py -- a REVISAO DO CONSTRUTOR sobre a adaptacao da R5 feita pelo agente (10/11/2026), antes da cadeia oficial. Idempotente; backup de BYTES (<arquivo>.bak_<TS>_r5c); temporario + os.replace; ast.parse nos .py.

O que conserta (achados do construtor ao reler o texto do registro a_escala_v410 e os consumidores):
 (K1) a chave do registro `nomes_novos_a_ratificar` trazia os 24 nomes novos, 22 deles JA' ratificados (D101): o nome da chave mentia. Passa a `nomes_novos_da_pedra` (so' o campo do RECIBO dos nomes, que e' insumo, fica como esta').
 (K2) a chave `estatuto_dos_nomes_novos` dizia RATIFICADOS para a lista de 24, que inclui os 2 auxiliares pendentes: passa a `estatuto_dos_nomes_ratificados_d101` (o estatuto dos pendentes ja' mora em ratificacao_pendente).
 (T1) a juncao da frase da clausula com a clausula do limite nao tinha pontuacao («... nao da' beta <= 1/2 Z(s) = ...»): passa a «FRASE (CLAUSULA); RECONSTRUCAO», no registro, na D100, no handoff, nos textos do pos-rito e no X.
 (T2) a linha do .md anunciava a clausula de 1 - beta sem a clausula do limite logo depois da frase: entra.
 (T3) a errata E36 (o limiar de um pixel e' a decisao exata) ficava SOZINHA em duas folhas do registro, sem a clausula do limite (a mesma classe do MEDIO da R2): no nucleo do texto ela vem sempre com a clausula na mesma folha; a c8 passa a exigir isso (fail-closed).
 (T4) o estatuto do registro anunciava a clausula de 1 - beta («n oitavas mais uma constante») sem a clausula do limite na folha: entra; e a lista dos temas das falas do registro ganha as duas falas novas.
 (T5) frases que envelheceram com a c13 (que usa beta de RUNTIME): «nenhum numero de beta entra», «beta so' por nome», «o registro nem o usa» -> «beta nunca literal (so' por nome na pedra; na c13, pelo valor de runtime)».
 (T6) comentarios/docstrings/mensagens que ainda diziam «nomes novos a ratificar» (o texto da D99, registro historico, NAO muda).
"""
import ast, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
FORA = re.compile(r"\.bak|\.pre_|trabalho_r4|^_r1_|^_r2_|^_r\dag_|^_r5c_|^_fix_|^_adapt_|^um_v410_candidato\.py$|^v410_pins\.py$")


def ativos():
    out = []
    for d in (HERE, os.path.join(HERE, "pos_rito")):
        for n in sorted(os.listdir(d)):
            if n.endswith((".py", ".pysnip", ".sh")) and not FORA.search(n) and os.path.isfile(os.path.join(d, n)):
                out.append(os.path.join(d, n))
    return out


class Arq:
    def __init__(self, p):
        self.p = p; self.b0 = open(p, "rb").read(); self.t = self.b0.decode("utf-8"); self.log = []

    def tr(self, a, b, n=1, opcional=False):
        c = self.t.count(a)
        if c == 0 and b in self.t:
            self.log.append("ja' feito: " + a[:70]); return
        if opcional and c == 0:
            return
        assert c == n, (os.path.basename(self.p), "contagem", c, "esperado", n, a[:120])
        self.t = self.t.replace(a, b); self.log.append("trocado x%d: %s" % (c, a[:70]))

    def grava(self):
        b1 = self.t.encode("utf-8")
        if b1 == self.b0:
            return False
        if self.p.endswith(".py"):
            ast.parse(self.t)
        bak = self.p + ".bak_" + TS + "_r5c"
        if not os.path.exists(bak):   # (o mesmo arquivo pode ser tocado duas vezes na mesma rodada: o backup que vale e' o PRIMEIRO, o do estado de antes)
            open(bak, "wb").write(self.b0); assert open(bak, "rb").read() == self.b0
        tmp = self.p + ".tmp_r5c"; open(tmp, "wb").write(b1); assert os.path.getsize(tmp) == len(b1) > 0
        os.replace(tmp, self.p); assert open(self.p, "rb").read() == b1
        return True


mudados = []
# ---------------------------------------------------------------- K1/K2: as chaves do registro (todos os arquivos ativos)
RX_K1 = re.compile(r"nomes_novos_a_ratificar")
n_k1 = n_k2 = 0; pulados = []
for p in ativos():
    A = Arq(p); t = A.t; partes = []; pos = 0
    for m in RX_K1.finditer(t):
        antes = t[max(0, m.start() - 40):m.start()]
        if antes.endswith('_REC_AESC.get("') or antes.endswith('[1].get("') or antes.endswith("[1].get('"):   # o campo do RECIBO dos nomes (insumo): fica
            pulados.append((os.path.relpath(p, HERE), antes[-28:])); continue
        partes.append(t[pos:m.start()]); partes.append("nomes_novos_da_pedra"); pos = m.end(); n_k1 += 1
    partes.append(t[pos:]); t = "".join(partes)
    c2 = t.count("estatuto_dos_nomes_novos"); t = t.replace("estatuto_dos_nomes_novos", "estatuto_dos_nomes_ratificados_d101"); n_k2 += c2
    # (T6) a prosa «nomes novos a ratificar» (mensagens, comentarios), menos o texto historico da D99 no delta («ao de nomes novos a ratificar»)
    t = t.replace("nomes novos a ratificar (R3)", "nomes novos da pedra (R3, R4 e R5)")
    t = re.sub(r"(?<!ao de )nomes novos a ratificar", "nomes novos da pedra", t)
    t = t.replace("nomes NOVOS a ratificar (R3)", "nomes NOVOS da pedra (R3, R4 e R5): RATIFICADOS em 10/11 (D101), salvo os dois auxiliares da autoria, pendentes")
    A.t = t
    if A.grava():
        mudados.append(os.path.relpath(p, HERE))
print("K1: %d trocas de chave | K2: %d | campos do recibo deixados: %s" % (n_k1, n_k2, pulados))

# ---------------------------------------------------------------- runtime_aescala_v410.py
A = Arq(os.path.join(HERE, "runtime_aescala_v410.py"))
A.tr("Nada aqui e' teste com a natureza; o gate nao se move; beta so' por nome.", "Nada aqui e' teste com a natureza; o gate nao se move; beta nunca literal (so' por nome na pedra; na c13, pelo valor de runtime).")
A.tr("c12 beta so' por nome (nenhum literal na pedra), nenhuma chave antiga muda", "c12 beta nunca literal (so' por nome na pedra; no registro so' a c13 o usa, pelo valor de runtime), nenhuma chave antiga muda")
A.tr("# ---- c12 beta so' por nome; nada muda", "# ---- c12 beta nunca literal (so' por nome na pedra; no registro so' a c13 o usa, pelo valor de runtime); nada muda")
A.tr("\"descricao\": \"beta so' por nome (nenhum literal na pedra; o registro nem o usa); nenhuma chave antiga muda", "\"descricao\": \"beta nunca literal: so' por nome na pedra (nenhum literal nela); no registro so' a c13 o usa, pelo valor de runtime; nenhuma chave antiga muda")
A.tr("    n_anunciam_r5_ = sum(1 for cam_, x_ in folhas_ if anuncia_r5_(x_))",
     "    n_anunciam_r5_ = sum(1 for cam_, x_ in folhas_ if anuncia_r5_(x_))\n"
     "    # (revisao do construtor, R5) a errata E36 diz o limiar de um pixel como a decisao exata: no NUCLEO do texto (fora dos extras, que guardam a frase solta para os controles) ela vem sempre com a CLAUSULA do limite na MESMA folha\n"
     "    sem_e36_ = sorted(cam_ for cam_, x_ in folhas_ if not cam_.startswith(\".extras\") and ((e36_pt_ in x_ and clz_pt_ not in x_) or (e36_en_ in x_ and clz_en_ not in x_)))\n"
     "    n_e36_ = sum(1 for cam_, x_ in folhas_ if not cam_.startswith(\".extras\") and (e36_pt_ in x_ or e36_en_ in x_))")
A.tr("clausula_r5_ok_ = bool(n_anunciam_r5_ >= 3 and not sem_r5_ and ", "clausula_r5_ok_ = bool(n_anunciam_r5_ >= 3 and not sem_r5_ and n_e36_ >= 3 and not sem_e36_ and ")
A.tr("\"clausula_r5\": {\"n_folhas_que_anunciam\": n_anunciam_r5_, \"folhas_que_anunciam_sem_a_forma\": sem_r5_, ", "\"clausula_r5\": {\"n_folhas_que_anunciam\": n_anunciam_r5_, \"folhas_que_anunciam_sem_a_forma\": sem_r5_, \"n_folhas_do_nucleo_com_a_errata_e36\": n_e36_, \"folhas_com_a_errata_e36_sem_a_clausula\": sem_e36_, ")
A.tr("a errata e a citacao do dispositivo, esta so' com as ressalvas", "a errata E36, no nucleo do texto sempre com a clausula do limite na mesma folha, e a citacao do dispositivo, esta so' com as ressalvas")
if A.grava():
    mudados.append("runtime_aescala_v410.py")
print("runtime_aescala:", A.log)

# ---------------------------------------------------------------- registros_aescala_v410.py
A = Arq(os.path.join(HERE, "registros_aescala_v410.py"))
A.tr('ANUNCIO_PT = DL.FRASE_TETELESTAI_PT + " " + DL.CLAUSULA_Z_PT + " " + DL.FRASE_RECONSTROI_PT', 'ANUNCIO_PT = DL.FRASE_TETELESTAI_PT + " (" + DL.CLAUSULA_Z_PT + "); " + DL.FRASE_RECONSTROI_PT')
A.tr('ANUNCIO_EN = DL.FRASE_TETELESTAI_EN + " " + DL.CLAUSULA_Z_EN + " " + DL.FRASE_RECONSTROI_EN', 'ANUNCIO_EN = DL.FRASE_TETELESTAI_EN + " (" + DL.CLAUSULA_Z_EN + "); " + DL.FRASE_RECONSTROI_EN')
A.tr("o limiar de tempo em n oitavas mais uma constante que so' depende de beta; \" + NUMEROS_TET", "o limiar de tempo em n oitavas mais uma constante que so' depende de beta (\" + DL.CLAUSULA_Z_PT + \"); \" + NUMEROS_TET")
A.tr("a mentira lida como mentira e' verdade); as leituras dele; \" % n_fal", "a mentira lida como mentira e' verdade; a clausula do Tetelestai em 1 - beta; «É isso aí, confirmo tudo» e a regra do nome); as leituras dele; \" % n_fal")   # (o trecho entre aspas angulares e' verbatim da fala 28: DL.FRASE_CONFIRMO_TUDO; conferido por conferir_citacoes)
A.tr("nada aqui e' teste com a natureza, nada move o gate, nenhum numero de beta entra", "nada aqui e' teste com a natureza, nada move o gate; beta nunca literal (so' por nome na pedra; na c13 do registro, pelo valor de runtime)")
A.tr('+ ANUNCIO_PT + ". [INPUT/dicionario] " + DL.FRASE_E36_PT + ". [PILOTO][SIM] "', '+ ANUNCIO_PT + ". [REAL o limiar de um pixel; INPUT/dicionario a leitura do operador] " + DL.FRASE_E36_PT + ". [PILOTO][SIM] "')
A.tr('"[INPUT/dicionario] " + DL.FRASE_E36_PT,', '"[REAL o limiar de um pixel; INPUT/dicionario a leitura do operador] " + DL.FRASE_E36_PT + " (" + DL.CLAUSULA_Z_PT + ")",')
A.tr('PENDENTE, ANUNCIO_PT, DL.FRASE_E36_PT, DL.FRASE_DISPOSITIVO_PT, NUMEROS_TET,', 'PENDENTE, ANUNCIO_PT, DL.FRASE_E36_PT + " (" + DL.CLAUSULA_Z_PT + ")", DL.FRASE_DISPOSITIVO_PT, NUMEROS_TET,')
A.tr("nenhum dado novo; beta so' por nome\"]", "nenhum dado novo; beta nunca literal (so' por nome na pedra; na c13, pelo valor de runtime)\"]")
if A.grava():
    mudados.append("registros_aescala_v410.py")
print("registros_aescala:", A.log)

# ---------------------------------------------------------------- delta_v410.py (a D100)
A = Arq(os.path.join(HERE, "delta_v410.py"))
A.tr('+ FRASE_TETELESTAI_PT + " " + CLAUSULA_Z_PT + " "', '+ FRASE_TETELESTAI_PT + " (" + CLAUSULA_Z_PT + "); "')
if A.grava():
    mudados.append("delta_v410.py")
print("delta:", A.log)

# ---------------------------------------------------------------- gerar_candidato_v410.py (a linha do .md e o comentario da chamada)
A = Arq(os.path.join(HERE, "gerar_candidato_v410.py"))
A.tr("DL.FRASE_TETELESTAI_PT + '. ' + DL.FRASE_RECONSTROI_PT + '. [INPUT/dicionário] '", "DL.FRASE_TETELESTAI_PT + ' (' + DL.CLAUSULA_Z_PT + '); ' + DL.FRASE_RECONSTROI_PT + '. [REAL o limiar de um pixel; INPUT/dicionário a leitura do operador] '")
A.tr("nomes RATIFICADOS pelo operador em 09/11; nomes novos da pedra), LOGO DEPOIS", "nomes RATIFICADOS pelo operador em 09/11; nomes novos RATIFICADOS em 10/11, D101; dois auxiliares da autoria pendentes), LOGO DEPOIS")
if A.grava():
    mudados.append("gerar_candidato_v410.py")
print("gerar_candidato:", A.log)

# ---------------------------------------------------------------- pos_rito: handoff, textos e X (a juncao FRASE (CLAUSULA); RECONSTRUCAO)
for nome, pref in (("textos_custodia_handoff_v410.py", "DL."), ("textos_v410.py", "DL_.")):
    A = Arq(os.path.join(HERE, "pos_rito", nome))
    for lg in ("PT", "EN"):
        A.tr(pref + 'FRASE_TETELESTAI_' + lg + ' + ". " + ' + pref + 'CLAUSULA_Z_' + lg + ' + " " + ' + pref + 'FRASE_RECONSTROI_' + lg, pref + 'FRASE_TETELESTAI_' + lg + ' + " (" + ' + pref + 'CLAUSULA_Z_' + lg + ' + "); " + ' + pref + 'FRASE_RECONSTROI_' + lg, opcional=True)
    if A.grava():
        mudados.append("pos_rito/" + nome)
    print(nome + ":", A.log)
A = Arq(os.path.join(HERE, "pos_rito", "gerar_x_custodia_v410.py"))
A.tr("{DL.FRASE_TETELESTAI_PT.replace(chr(96), '')}. {DL.CLAUSULA_Z_PT} {DL.FRASE_E36_PT.replace(chr(96), '')}.", "{DL.FRASE_TETELESTAI_PT.replace(chr(96), '')} ({DL.CLAUSULA_Z_PT}); {DL.FRASE_E36_PT.replace(chr(96), '')}.")
if A.grava():
    mudados.append("pos_rito/gerar_x_custodia_v410.py")
print("gerar_x_custodia:", A.log)
print("ARQUIVOS MUDADOS (%d):" % len(sorted(set(mudados))), sorted(set(mudados)))
