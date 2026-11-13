# -*- coding: utf-8 -*-
"""_pedidos_harnesses_fork_c_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) ACRESCENTA (so' acrescimo; backup de BYTES antes;
temporario -> conferir -> substituir) em PEDIDOS_ENTRE_FRENTES_v411.md o que a segunda rodada do fim_de_cadeia (14h51, depois do conserto das listas
em pos_rito\\) e a rodada de DEPURACAO dos dois harnesses (--nao-exigir-refazer, 14h56 a 15h01) mostraram: (A) a precondicao do refazer_out_v411.txt,
que nenhuma rodada real satisfaz como a cadeia esta' escrita; (B) as tres expectativas da leitura que o core e o selo do candidato nao cumprem, com o
MEDIDO de cada uma; (C) o que derruba o harness do fechar; (D) o que passou; (E) o que mudou no conferidor depois disso. Os numeros saem dos JSONs de
depuracao e do core/selo do falso Nos, lidos aqui por script; os numeros de linha de pos_rito\\ sao os lidos por grep entre 14h56 e 15h05 (o fork C
NAO editou pos_rito\\). uso: python -B -X utf8 _pedidos_harnesses_fork_c_v411.py"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
J = lambda p_: json.load(open(p_, encoding="utf-8"))
s16 = lambda p_: hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16]
P = os.path.join(HERE, "PEDIDOS_ENTRE_FRENTES_v411.md")
MARCA = "<!-- fork_c_harnesses_depuracao_12nov -->"
b = open(P, "rb").read(); t = b.decode("utf-8")
assert MARCA not in t, "a nota ja' esta' no arquivo (so' acrescimo: nao repetir)"
HT_P = os.path.join(HERE, "pos_rito", "HARNESS_TEXTOS_ENSAIO_v411_DEPURACAO_sem_refazer.json"); HF_P = os.path.join(HERE, "pos_rito", "HARNESS_FECHAR_SANDBOX_v411_DEPURACAO_sem_refazer.json")
HT = J(HT_P); HF = J(HF_P)
assert HT.get("nao_exigiu_refazer") is True and HF.get("nao_exigiu_refazer") is True and HT.get("tudo_passou") is False and HF.get("tudo_passou") is False
core = J(os.path.join(DL.FALSO_NOS_DIR, "um_absoluto.json"))["core"]; selo = J(os.path.join(DL.FALSO_NOS_DIR, "um_absoluto_selo.json")); base = J(os.path.join(HERE, "base_v410", "um_absoluto.json"))["core"]
cand16 = s16(DL.CANDIDATO_ARQ)
# (B1) o resumo do registro no selo
ks = sorted(selo.get(DL.FECHO_REGISTRO) or {}); assert "p2_ao_lado_da_v387" in ks
# (B2) a forma de cada verbatim do core e os autores nos extras
cu = core[DL.CUNHAGENS_REGISTRO]; vb = cu.get("verbatim") or {}; kv = sorted({k_ for v_ in vb.values() for k_ in v_}); au = (cu.get("extras") or {}).get("autores") or {}
assert "autor" not in kv and len(au) == len(vb) == DL.N_FALAS_V411 and set(au.values()) == {"operador"}
kv10 = sorted({k_ for v_ in (base["cunhagens_v410"].get("verbatim") or {}).values() for k_ in v_}); assert kv10 == kv
# (B3) as erratas dos kh herdados: o core do candidato contra o core da v410 selada
n = lambda c_, k_: len((c_.get(k_) or {}).get("erratas") or [])
e9, e9b, e10, e10b = n(core, "kh_n1_cobertura_v409"), n(base, "kh_n1_cobertura_v409"), n(core, "kh_n1_cobertura_v410"), n(base, "kh_n1_cobertura_v410")
assert e9 == e9b and e10 == e10b + 1 and str(core["kh_n1_cobertura_v410"]["erratas"][-1].get("assinatura")) == DL.ASSINA
_pt = [str(p_) for p_ in HT.get("problemas") or []]; _pf = [str(p_) for p_ in HF.get("problemas") or []]
n_leit = sum(1 for p_ in _pt if p_.startswith("leitura: ")); n_casc = sum(1 for p_ in _pt if "a leitura da rodada nao confirma o registro" in p_)
n_nao_rec = sum(1 for p_ in _pf if "nao recusou como esperado" in p_)
fila = ((HF.get("etapas") or {}).get("fila_da_memoria"))
L = []
L.append("\n\n## (claude-construtor-v411, fork C, %s) a segunda rodada do fim_de_cadeia e a DEPURACAO dos dois harnesses: o que para a cadeia real em pos_rito\\ e na cadeia %s\n" % (datetime.datetime.now().strftime("%d/%m/%Y %Hh%M"), MARCA))
L.append("Candidato `%s`. O `fim_de_cadeia_v411.sh` das 14h51 passou as etapas 1 a 4 (o B20 pre-selo; o servico estatico e o controle negativo dele; a derivacao do pos-rito, agora rc 0) e PAROU na etapa 5: o harness dos textos RECUSA com rc 4, “falta refazer_out_v411.txt no pacote”. "
         "Para colher as linhas PROBLEMA sem editar nada, o fork C rodou os dois harnesses no modo de depuracao deles (`--nao-exigir-refazer`; os resumos, que o proprio harness grava, sao `pos_rito\\HARNESS_TEXTOS_ENSAIO_v411_DEPURACAO_sem_refazer.json` e `pos_rito\\HARNESS_FECHAR_SANDBOX_v411_DEPURACAO_sem_refazer.json`; "
         "os consoles ficam fora de work, em `C:\\t\\k411c\\saidas_forkc_20261112\\`). Esses resumos NAO valem para o relatorio. O fork C NAO editou `pos_rito\\`." % cand16)
L.append("")
L.append("A. **Ao principal e a gerencia: a precondicao do `refazer_out_v411.txt` nao e' satisfeita por NENHUMA rodada real, como a cadeia esta' escrita.** Fora do ensaio, os dois harnesses exigem `refazer_out_v411.txt` no pacote, com `== FIM` e mais novo que o `ESPERADOS_v411.json` "
         "(`harness_textos_ensaio_v411.py`, linhas 142 a 149; `harness_fechar_sandbox_v411.py`, linhas 711 a 718). A `cadeia_v411.sh` nao grava esse arquivo; o `refazer_candidato_v411.sh` (que so' chama a cadeia) cria o arquivo no INICIO e so' escreve `== FIM` DEPOIS que a cadeia inteira termina com rc 0, "
         "mas os harnesses rodam DENTRO da cadeia (o passo 15): na hora deles o arquivo nao tem `== FIM` e e' mais antigo que o ESPERADOS (regravado no passo 08). Na v410 o refazer terminava no p00 e os harnesses vinham depois, em outro script. "
         "Dois consertos possiveis, um so' basta: (i) na cadeia (do principal): logo depois do passo 14 (o p00, onde o refazer da v410 terminava), gravar `refazer_out_v411.txt` com a saida da cadeia ate' ali e a linha `== FIM`; (ii) nos harnesses (da frente pos-rito): aceitar como prova o `cadeia_v411_out.txt` da rodada (os passos 05 a 14 com o rc aceito, mais novo que o ESPERADOS). O fork C nao tocou nenhum dos dois.")
L.append("B. **A frente pos-rito (leitura_v411.py): tres expectativas que o core e o selo do candidato NAO cumprem; as tres estao na leitura.** O harness dos textos em depuracao: o conferidor contra o Nos emulado deu TUDO BATE; a leitura deu %d problemas, e %d dos %d problemas do harness sao cascata deles (“a leitura da rodada nao confirma o registro”)."
         % (n_leit, n_casc, len(_pt)))
L.append("   1. `H0_SELO_CHAVES` (linha 54; a igualdade de conjuntos na linha 197) tem 12 chaves; o resumo do `%s` no selo tem %d: a mais, `p2_ao_lado_da_v387` (o aditivo do P2, de 12/11, no registro e no selo; o conferidor e os ESPERADOS ja' o leem). Medido no selo do falso Nos: %s."
         % (DL.FECHO_REGISTRO, len(ks), ", ".join("`%s`" % k_ for k_ in ks)))
L.append("   2. `todas_op_` (linha 243) exige `autor == 'operador'` em CADA `verbatim[k]` do core; o core nao traz essa chave em nenhum (as chaves de cada verbatim: %s; a mesma forma da v410 selada). A autoria esta' em `extras.autores` (%d entradas, todas `operador`) e nos ESPERADOS (`cunhagens`), onde a leitura da v410 a lia (`leitura_v410.py`, linha 1122)."
         % (", ".join("`%s`" % k_ for k_ in kv), len(au)))
L.append("   3. `kh9_ok_` (linha 1049) espera em `kh_n1_cobertura_v409` UMA errata a mais que na v410 selada, assinada pela v411. Medido: `kh_n1_cobertura_v409` tem %d erratas no candidato e %d na v410 selada (iguais); a errata nova dos pisos, assinada `%s`, esta' em `kh_n1_cobertura_v410` (%d contra %d). "
         "O bloco da v409 tem de ser o das erratas IGUAIS as da v410 selada (como os da v408 e da v406), e o do “mais uma” e' o da v410." % (e9, e9b, DL.ASSINA, e10, e10b))
L.append("C. **A frente pos-rito (harness_fechar_sandbox_v411.py): o que o derruba, alem da leitura.** %d problemas. (1) O conferidor dentro do SANDBOX cai com FileNotFoundError em `...\\fechar_sandbox\\work\\cadeia_de_selo\\v409\\acom_conferencias_v409.py`, que o `v410\\acom_conferencias_v410.py` (linha 14) carrega por caminho: "
         "a lista das pastas irmas do sandbox (linha 815) nao traz a `v409`. (2) O `fechar_v411.py` do sandbox sai com rc 2 pelos tres problemas da leitura do item B; %d controles ficam como “nao recusou como esperado” (cascata provavel; so' se sabe depois dos consertos; um deles, o da porta do paragrafo novo com o K adulterado, saiu com rc 0: olhar esse)."
         % (len(_pf), n_nao_rec))
L.append("D. **O que passou na depuracao.** A previa do X sobre o Nos emulado (rc 0). No harness do fechar: a fila da memoria (`fila_da_memoria`: %s; os controles negativos da fila e das superficies recusaram como esperado; a prova do diretorio REAL de memoria antes e depois: inalterado) e os seis casos do `b3_recibo`. "
         "A varredura do Fock/Omega sobre o que a depuracao rendeu: 187 arquivos, 2 achados historicos, 0 novos (o JSON dessa rodada ficou fora de work; a varredura oficial corre depois do harness oficial)." % fila)
L.append("E. **Uma observacao e o que mudou no conferidor.** O campo `veredito` do harness dos textos diz “TUDO PASSOU: ...” mesmo com %d problemas (a frase e' incondicional, linha 2168, como na v410); o rc e `tudo_passou` dizem a verdade, e o relatorio le `tudo_passou`. "
         "Depois da depuracao o fork C tirou do `conferir_rito_v411.py` as duas dependencias de arquivo que tinha posto nele hoje: a guarda dos trechos herdados usa a funcao SELADA `_v410_guarda_frases` que a `guarda_frases_v411.py` ja' carrega do um.py da v410 (nenhum arquivo da pasta v410), e a conferencia do topo (condicao 3(a)) mora dentro do conferidor "
         "(`_topo_com_resultado_v411`; o `topo_com_resultado_v411.py` virou um carregador para o ensaio a seco). A lista de arquivos do sandbox do harness NAO precisa mudar por causa do conferidor." % len(_pt))
add = "\n".join(L) + "\n"
nb = (t.rstrip("\n") + add).encode("utf-8")
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc3"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) and nb.startswith(t.rstrip("\n").encode("utf-8")); os.replace(P + ".tmp", P)
print("acrescentado:", len(b), "->", len(nb), "| leitura:", n_leit, "| cascata:", n_casc, "de", len(_pt), "| fechar:", len(_pf), "| nao recusou:", n_nao_rec, "| fila:", fila)
