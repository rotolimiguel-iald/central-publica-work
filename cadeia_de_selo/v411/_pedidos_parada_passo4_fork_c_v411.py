# -*- coding: utf-8 -*-
"""_pedidos_parada_passo4_fork_c_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) ACRESCENTA (so' acrescimo; backup de BYTES
antes; temporario -> conferir -> substituir) em PEDIDOS_ENTRE_FRENTES_v411.md: (1) a parada do fim_de_cadeia no passo 4 (a derivacao do pos-rito, da
outra frente) e a lista exata dos pinos velhos em pos_rito\\ (arquivo e linha, lidos por grep as 14h45, ANTES do conserto que a gerencia assumiu;
este script NAO le pos_rito\\: a gerencia mandou nao ler enquanto o agente dela trabalha la'); (2) AO LADO do item 7 da resposta anterior: o residuo
das citacoes nao existe mais; (3) os tres portoes do relatorio que nenhuma rodada limpa da cadeia passa, com as linhas (lidas aqui por script do
p00, do relatorio e da cadeia). As listas e o token saem do delta. uso: python -B -X utf8 _pedidos_parada_passo4_fork_c_v411.py"""
import datetime, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
P = os.path.join(HERE, "PEDIDOS_ENTRE_FRENTES_v411.md")
MARCA = "<!-- fork_c_parada_passo4_12nov -->"
b = open(P, "rb").read(); t = b.decode("utf-8")
assert MARCA not in t, "a nota da parada ja' esta' no arquivo (so' acrescimo: nao repetir)"
assert "<!-- fork_c_respostas_mlh_12nov -->" in t, "a resposta anterior do fork C nao esta' no arquivo"


def linha(arq_, trecho_):
    """o numero da UNICA linha de arq_ (da pasta da cadeia, fora de pos_rito) que traz trecho_"""
    ls_ = [i_ + 1 for i_, l_ in enumerate(open(os.path.join(HERE, arq_), encoding="utf-8").read().split("\n")) if trecho_ in l_]
    assert len(ls_) == 1, (arq_, trecho_, ls_)
    return ls_[0]


L_PEND = linha("p00_precondicoes_v411.py", 'pend("a folga do MEMORY.md')
L_P00 = linha("gerar_relatorio_v411.py", '    "p00": bool(')
L_CAD = linha("gerar_relatorio_v411.py", '    "cadeia_limpa_ate_o_relatorio": bool(')
L_VF = linha("gerar_relatorio_v411.py", '    "varredura_fock_omega": bool(')
_cad = open(os.path.join(HERE, "cadeia_v411.sh"), encoding="utf-8").read()
assert "varredura_fock_omega" not in _cad, "a cadeia ja' tem o passo da varredura: reler antes de escrever"
PASSOS_P00 = re.findall(r"^passo (\d\d_p00\w*)", _cad, re.M); assert PASSOS_P00 == ["14_p00", "17_p00_final"], PASSOS_P00
CIT = json.load(open(DL.saida("conferir_citacoes_v411.json"), encoding="utf-8"))
assert CIT.get("ok") is True and CIT.get("ok_do_um_py") is True and CIT.get("ok_do_pos_rito") is True and not CIT.get("nao_verbatim_do_pos_rito"), "as citacoes nao estao limpas nos dois escopos: nao escrever que estao"
PRE = json.load(open(DL.saida("PRECONDICOES_v411.json"), encoding="utf-8"))
_dec = sorted(DL.DECISOES_V411, key=lambda k_: int(k_[1:]))
L = []
L.append("\n\n## (claude-construtor-v411, fork C, %s) o fim_de_cadeia parou no passo 4; os pinos velhos em pos_rito\\; tres portoes do relatorio %s\n" % (datetime.datetime.now().strftime("%d/%m/%Y %Hh%M"), MARCA))
L.append("1. **A frente pos-rito (a gerencia assumiu o conserto; a lista vai inteira, para um conserto so').** O `fim_de_cadeia_v411.sh` das 14h37 passou os passos 1 a 3 (o B20 pre-selo; o servico estatico e o controle negativo dele) e PAROU no passo 4: "
         "`pos_rito\\gerar_derivacao_pos_rito_v411.py` levanta a mensagem “o delta nao e' o da v411 (um registro com funcao; D159 a D170)”. Os passos 4 a 7 (a derivacao, o harness dos textos, a previa do X e o harness do fechar) NAO rodaram. "
         "Os pinos velhos EXECUTAVEIS, lidos por grep as 14h45 (antes do conserto; os numeros de linha sao dessa leitura):")
L.append("   - `gerar_derivacao_pos_rito_v411.py`, linhas 16 (o conjunto das seis decisoes D159, D162, D167, D168, D169 e D170 comparado com `DL.DECISOES_V411`) e 17 (`DL.N_FALAS_V411 == len(DL.FALAS_V411) == 9`);")
L.append("   - `leitura_v411.py`, linha 247 (o mesmo conjunto de seis, em `decisoes_ok_`);")
L.append("   - `textos_v411.py`, linhas 149 (`len(out) == DL_.N_FALAS_V411 == 9`) e 243 (o conjunto de seis);")
L.append("   - `textos_v411_novo.pysnip`, linhas 130 e 184 (o par do `textos_v411.py`);")
L.append("   - `registrar_mapa_v411.py`, linha 282 (`DEC = \"D159 a D170\"`: o texto do registro do Mapa diria a faixa velha);")
L.append("   - `teste_textos_sem_candidato_v411.py`, linha 254 (`Vc[\"n\"] == 9` e `Vc[\"n_decisoes\"] == 6`).")
L.append("   O conserto (pedido do principal): ler `DL.N_FALAS_V411` (hoje %d), `DL.DECISOES_V411` (hoje %d: %s) e `DL.DECISOES_TOKEN_V411` (`%s`), sem digitar o numero de falas nem o fim da faixa. "
         "Mencoes so' de TEXTO (“nove falas”, “D159 a D170”) seguem em comentarios e mensagens de `harness_textos_ensaio_v411.py` (1172, 2170), `harness_fechar_sandbox_v411.py` (1120), `leitura_v411.py` (3, 22, 238, 1037), `registrar_mapa_v411.py` (267, 334), `textos_v411.py` (706) e `textos_v411_novo.pysnip` (448)."
         % (DL.N_FALAS_V411, len(DL.DECISOES_V411), ", ".join(_dec), DL.DECISOES_TOKEN_V411))
L.append("2. **AO LADO do item 7 da resposta anterior do fork C (as citacoes).** O residuo nao existe mais: as aspas da linha 82 de `pos_rito\\textos_custodia_handoff_v411.py` foram trocadas pela gerencia as 14h39; `conferir_citacoes_v411.py --candidato` da' rc 0 "
         "(os dois escopos limpos; o JSON lido agora: `ok` %s, `ok_do_um_py` %s, `ok_do_pos_rito` %s). O `PRONTO_PARA_O_POS_RITO.json` foi regravado com esse estado em `citacoes`; o que o ensaio a seco mediu na hora dele (rc 2) fica ao lado, em `citacoes_no_ensaio_a_seco`."
         % (CIT.get("ok"), CIT.get("ok_do_um_py"), CIT.get("ok_do_pos_rito")))
L.append("3. **Ao principal e a gerencia (o relatorio exige, antes, o que e' ato da gerencia).** Como estao escritos, tres portoes do `gerar_relatorio_v411.py` nao passam em NENHUMA rodada limpa da `cadeia_v411.sh`, e por isso `pronta` nao chega a true: "
         "(a) `p00` (linha %d) exige o veredito “TODAS PASSARAM”, e o `p00_precondicoes_v411.py` tem na linha %d um pendente INCONDICIONAL (a folga do MEMORY.md e o pino do MEMORY.md): nenhum ato o apaga (o p00 de agora: %s); "
         "(b) `cadeia_limpa_ate_o_relatorio` (linha %d) exige todo `rc=0` no `cadeia_v411_out.txt`, e os passos %s devolvem rc 3 enquanto houver pendente (a cadeia aceita o 3; o portao nao); "
         "(c) `varredura_fock_omega` (linha %d) exige `VARREDURA_FOCK_OMEGA_v411.json`, que nenhum passo da `cadeia_v411.sh` grava (a varredura corre por fora; le os textos rendidos pelo harness dos textos, as fontes de `pos_rito\\`, o relatorio e o plano). "
         "O fork C NAO tocou o p00, o relatorio nem a cadeia (nao sao dele): a decisao e' do principal e da gerencia. Enquanto nao houver decisao, o fork C roda a varredura por fora (depois do harness dos textos, quando a gerencia liberar `pos_rito\\`) e diz no relatorio o que os portoes (a) e (b) deixam em falta."
         % (L_P00, L_PEND, PRE.get("veredito"), L_CAD, " e ".join(PASSOS_P00), L_VF))
add = "\n".join(L) + "\n"
nb = (t.rstrip("\n") + add).encode("utf-8")
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc2"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) and nb.startswith(t.rstrip("\n").encode("utf-8")); os.replace(P + ".tmp", P)
print("acrescentado:", len(b), "->", len(nb), "| linhas lidas:", {"p00_pend": L_PEND, "rel_p00": L_P00, "rel_cadeia": L_CAD, "rel_varredura": L_VF})
