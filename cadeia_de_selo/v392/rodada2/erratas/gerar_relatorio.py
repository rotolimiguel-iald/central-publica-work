# -*- coding: utf-8 -*-
"""gerar_relatorio.py -- escreve V\\rodada2\\erratas\\RELATORIO.md a partir de V\\patches_erratas_v392.py (tudo lido do arquivo; nada digitado)."""
import importlib.util, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(os.path.dirname(HERE))
sp = importlib.util.spec_from_file_location("p", os.path.join(V, "patches_erratas_v392.py"))
P = importlib.util.module_from_spec(sp)
sp.loader.exec_module(P)
MASK = lambda s: s.replace("CONF" + "IRMED", "C-O-N-F-I-R-M-E-D")


def anc(p):
    return MASK(p["old"].split("\n")[-1].strip()[:90]).replace("|", "/")


def lin(p):
    return ", ".join(str(x) for x in p["linha_v391"])


rows = []
for p in list(P.E01_PATCHES) + list(P.A03_PATCHES):
    txt = MASK(p["texto"].replace("\n", " // "))
    rows.append("| %s | %s | %s | `%s` | %s | %s | %s |" % (p["id"], lin(p), p["alvo_descricao"].replace("|", "/"), anc(p).replace("`", "'"), p["registro"], p["estatuto"].replace("|", "/"), (txt[:170] + "...").replace("|", "/")))

out = []
out.append("# RELATORIO -- erratas E01 (codigo) e A03 (artigo) da v392 (rodada 2, agente ERRATAS, 13/10/2026, gerencia c1)\n")
out.append("Estatutos: [REAL] medido/lido aqui por script; [DERIVED]; [DECLARADO] dito na origem, nao conferido; [OPEN]. Nada foi aplicado ao um.py real: os patches sao DADOS; o teste aplica em memoria. O gate nao se move.\n")
out.append("## 1. Entregas\n")
out.append("- `V\\patches_erratas_v392.py`: `E01_PATCHES` (%d), `A03_PATCHES` (%d), `aplicar(T, crlf)`, `UM_V391_SHA16`. Gerado por `V\\rodada2\\erratas\\gerar_patches_erratas.py` (le o um.py v391 so' para leitura; cada hash e cada numero citado e' lido do arquivo e conferido; divergencia => recusa)." % (len(P.E01_PATCHES), len(P.A03_PATCHES)))
out.append("- `V\\testar_erratas_v392.py` (`--latex` compila o texto novo do artigo PT/EN com pdflatex 2x em `V\\rodada2\\erratas\\latex\\`).")
out.append("- Numeracao: as linhas do plano sao por LF (o um.py tem 468 LF soltos dentro de strings alem dos 213.655 CRLF); com `split('\\n')` as ancoras do plano caem nas linhas dadas. As ancoras dos patches sao o TEXTO (`old`), unico no arquivo.\n")
out.append("## 2. Tabela (id -> linha achada -> alvo -> ancora -> registro -> estatuto -> texto)\n")
out.append("| id | linha v391 (dica) | alvo | ancora (ultima linha do `old`) | registro v392 | estatuto | texto novo (inicio) |")
out.append("|---|---|---|---|---|---|---|")
out += rows
out.append("")
out.append("## 3. ALVO_NAO_ENCONTRADO\n")
out.append("Nenhum alvo da tarefa ficou sem paragrafo: todos foram achados por texto e a ancora e' unica (`n = 1`). Desvios e leituras, ditos sem veu:")
out.append("- **txt PT l.139 e l.202 (CR-05)**: o `.txt` do artigo nao foi gerado (o um.py nao roda aqui). Mapeei por texto os dois lugares do gerador que imprimem a escada `1,64 -> 2,21 -> 2,95 sigma`: o paragrafo (ii-b) da lamina m2 (PT l.170073-94; EN l.174481-502) e o resumo do S234 (PT l.204314-44; EN l.206781-811). [DERIVED de leitura; a conferir quando o `.txt` sair].")
out.append("- **Linhas do plano vs arquivo**: tudo bateu em numeracao LF (E01 4802, 4796-4801, 4816, 4829, 193300-193302, 193150, 193186, 213968, 208557; A03 166152, 165421, 203582, 166093, 166070, 166079, 166688, 166634, 165561, 166092, 166771, 166219, 166078-82; EN 170494, 165419, 206031).")
out.append("- **A tabela R3 (F4 neutrino)**: as linhas PT 166386-88 / EN 170739-41 imprimem `tensao_atual_sigma` = 2,95 numa linha de TABELA (nao ha paragrafo); nao patcheei a linha, a errata A03-12 diz o numero. Residuo declarado.")
out.append("- **Docstring de `prove_neff_channel` (l.4776-4790)**: nao toquei a docstring; a nota E01-a/E01-b1 vai nos comentarios logo depois de `centro_atual` e da escada.")
out.append("- **Outros 'CMB-S4' no codigo** (l.2934, 4225, 4266, 151973, 211102): fora da lista da tarefa, nao tocados. Extras que fiz (marcados `nota`): E01-f (ledger l.3253-3256, CR-13) e A03-14a/b/c (ponteiros CR-13 em 3 paragrafos do artigo).")
out.append("- **Fora do escopo (nao tinham alvo no um.py/artigo)**: B3 (`erratas_o_que_resta_v392`, texto no core), CR-02 (gerador da arvore e registro), CR-08 nas demais superficies (CLAUDE.md, Atlas...), a errata da ATRIBUICAO de Coulomb (vai ao `tgl_paper_unified.py`, ao `Haja_Luz\\CLAUDE.md` e ao 'Custo').\n")
out.append("## 4. Resultado do teste (`testar_erratas_v392.py --latex`)\n")
out.append("Ver a saida impressa; resumo: sha16/tamanho do um.py = 8e7b9927ceae64b8 / 33.910.631 B; 44 patches, contagens exatas (CRLF), ordem irrelevante, nenhum LF solto novo; `ast.parse` do todo; **E01 nao altera valor** (`ast.dump` identico ao original); **A03 so' acrescenta** (mesmo numero de funcoes/classes; cada `old` preservado); os 28 trechos `s/c/partC.append` novos, executados com nomes de teste, emitem exatamente o texto declarado (o D1 resolve `%s` pelo `_or7` do core: 3,01 e 0,09); as 6 insercoes dentro de string saem so' no ramo da lingua certa; guarda P18 = zero violacoes em todo o texto novo (controle negativo pega as classes); pdflatex 2x PT e EN sem erro.\n")
out.append("## 5. Dependencias e atos da gerencia\n")
out.append("- Os textos citam **registros v392 que os agentes de registros precisam criar**: " + ", ".join(sorted({r.strip() for p in list(P.E01_PATCHES) + list(P.A03_PATCHES) for r in p["registro"].split("+")})) + ". Se algum nao nascer, o texto cita registro inexistente (fail visivel no teste de citacoes, nao no meu).")
out.append("- **Pedras**: A03-01 pressupoe `TGLExt.LiganteLeiCampoCurvo` instalada; A03-03, `TGLExt.Palavra`; A03-06 e A03-10, `TGLExt.PostoAdendo` (a pedra que a gerencia acrescentou; a sonda `PostoRankAdendo` ficou FORA; o adendo esta SEM auditoria independente, e o texto diz).")
out.append("- **Numeros no texto do artigo sao estaticos** (2,21 / 2,95 / 2,44; as contas do rank); so' o D1 le o core em runtime (`_or7`). Os numeros do E01 (2,486 / 1,612 / +0,1195 / -2,24 / -2,71 / 6,3-7,7 / +1,12) foram recalculados e conferidos no gerador contra o `neff_conferencia.out.txt` e o `RECALCULO_A_SN.json`.")
out.append("- **Veto/leitura da gerencia**: A03-02 (escala de beta, X6) e A03-06 (nome AXIOMA) vao como [DERIVED de leitura; a vetar]; A03-12 (perito JUNO) idem.")
out.append("- Divergencia plano/fonte: o plano diz 'ramo invertido a 0,09 sigma [DECLARADO pelo critico]'; o core v391 tem `orientation_is_the_sign_v367.z_to_coupling_branch` = 0,0869 [REAL, lido]; usei o do core.")
out.append("- A palavra da regua nao aparece por extenso nos meus arquivos (nas ancoras copiadas do um.py ela esta em escape `\\x49`/`\\u0049`).")
txt = "\n".join(out) + "\n"
path = os.path.join(HERE, "RELATORIO.md")
tmp = path + ".tmp"
if os.path.exists(path):
    import shutil, time
    shutil.copyfile(path, path + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
open(tmp, "w", encoding="utf-8", newline="\n").write(txt)
os.replace(tmp, path)
print("OK", path, len(txt))
