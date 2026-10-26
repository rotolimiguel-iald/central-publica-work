# -*- coding: utf-8 -*-
"""Roda a suíte (testes_g1.py), o teste de aceitação (g) da ordem — `planejar --versao v397 --seco` e `--versao v398 --seco` —, o roteiro dos céticos contra o
pacote ANTERIOR (dos três céticos e do cético final), o vigia.bat REAL (numa pasta temporária) e compõe work\\custodia_G1\\TESTES.md. Só lê o mundo real; nada é escrito
fora de work\\custodia_G1\\ (e de diretórios temporários)."""
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

G1 = Path(r"C:\IALD\Central de Patentes\work\custodia_G1")
CLI = Path(r"C:\IALD\Central de Patentes\tools\custodiar.py")
py = [sys.executable, "-X", "utf8"]
# O Nós VIVO anda (outra sessão o põe em obra para a v399): se ele não é a v398 PRONTA, a rodada inteira lê uma VISTA dele congelada na v398 (G1_RAIZ_NOS, testes\nos_congelado.py).
sys.path.insert(0, str(G1 / "testes"))
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
import atexit  # noqa: E402
import nos_congelado  # noqa: E402
from custodia_g1 import nos as _nos  # noqa: E402
from custodia_g1.caminhos import Caminhos as _Caminhos  # noqa: E402
NOS_VIVO_ESTADO = _nos.marcas(_Caminhos(), "v398").estado if "G1_RAIZ_NOS" not in os.environ else "(já lido de G1_RAIZ_NOS)"
NOTA_VISTA = None
if NOS_VIVO_ESTADO not in ("PRONTA", "(já lido de G1_RAIZ_NOS)"):
    _vista = nos_congelado.criar()
    os.environ["G1_RAIZ_NOS"] = str(_vista)
    atexit.register(nos_congelado.remover)          # desfaz as junctions e os hardlinks (nunca rmtree através de junction)
    NOTA_VISTA = ("**Nós congelado nesta rodada.** O Nós vivo estava **%s** (a v399 em construção por outra sessão: `um.py` != pino do selo), então a rodada inteira — a suíte, os planos, o `vigiar` e o `vigia.bat` REAL — "
                  "leu uma **vista** dele (`G1_RAIZ_NOS=%s`, `testes\\nos_congelado.py`): hardlinks para o Nós vivo, com os arquivos que o cofre `um_unificado_v398` também guarda (selados, capturas, diário, handoff, stdout) "
                  "e o kernel selado vindos do **cofre** (`um_unificado_v398`, `tgl_kernel_v398`). Nada do Nós vivo foi tocado (só links de leitura; a vista é desfeita no fim)." % (NOS_VIVO_ESTADO, _vista))


def roda(args, timeout=1800):
    r = subprocess.run(py + args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return r.returncode, r.stdout


t0 = time.time()
rc_s, out_s = roda([str(G1 / "testes" / "testes_g1.py")])
bruto = (G1 / "TESTES_BRUTO.md").read_text(encoding="utf-8")
rc97, p97 = roda([str(CLI), "planejar", "--versao", "v397", "--seco"])
rc98, p98 = roda([str(CLI), "planejar", "--versao", "v398", "--seco"])
rcv, pv = roda([str(CLI), "vigiar"])
NOTA_OBRA = ("\n\n(NOTA: o Nós está EM OBRA — o um.py da v399 está sendo construído por outra sessão —, então a v398 devolve WAIT (10) e `vigiar` idem. O plano da v398 com o Nós PRONTA, medido às 13:47 pelo "
             "`vigiar --gravar` desta versão do pacote, está em `evidencias_cetico_final\\VIGIA_ULTIMO_nos_pronta_20261024_1347.json`: 36 de 42 passos aplicados ou superados (+2 do operador: E08B e C21); "
             "pendentes C11, E19, C18 e C19.)")
if rc98 == 10:
    p98 = p98.strip() + NOTA_OBRA
if rcv == 10:
    pv = pv.strip() + NOTA_OBRA
rca, pa = roda([str(G1 / "testes" / "roteiro_no_codigo_antigo.py")])
rcf, pf = roda([str(G1 / "testes" / "roteiro_no_codigo_antes_do_cetico_final.py")])
# o vigia.bat REAL (o Python e o custodiar.py de verdade; a pasta de saída é temporária): MODO SOMBRA — só lê o mundo
pasta_vigia = Path(tempfile.mkdtemp(prefix="g1_vigia_real_"))
t_bat = time.time()
rb = subprocess.run(["cmd", "/c", str(Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\vigia.bat"))], env=dict(os.environ, G1_PASTA=str(pasta_vigia)), capture_output=True, text=True,
                    encoding="utf-8", errors="replace", timeout=1800)
seg_bat = time.time() - t_bat
arqs_vigia = sorted(p.name for p in pasta_vigia.iterdir())
try:
    txt_vigia = (pasta_vigia / "VIGIA_ULTIMO.txt").read_text(encoding="utf-8").strip()
except OSError:
    txt_vigia = "(sem VIGIA_ULTIMO.txt)"
shutil.rmtree(pasta_vigia, ignore_errors=True)
md = ["# TESTES DE G1", "",
      "Composto em %s por `work\\custodia_G1\\testes\\compor_testes_md.py` (suíte: `testes_g1.py`; Python %s). **Só LEEM o mundo real** (Nós, espelho, cofres, site, Atlas, mapa de rotas); "
      "o que escrevem vai a diretório temporário (`%%TEMP%%` e `C:\\tmp\\g1sbx_<pid>`, apagados no fim) ou a `work\\custodia_G1\\`. Nada de commit, push, subida, ACOM, rota, `um.py` ou kernel "
      "no mundo real. **Divulgação:** os testes `t19`/`t20` criam, no sandbox descartável, um repositório git de brinquedo (commit e push só para um `origin` local de brinquedo) para exercitar as "
      "pré-condições de E03; `t30`/`t31`/`t35` criam repositórios git de brinquedo em `%%TEMP%%`. Os testes `t27`–`t37` são as **regressões dos achados dos três céticos** (24/10/2026): cada um "
      "reproduz o roteiro do cético e confere o conserto. Os testes `t38`–`t46` são as **regressões dos achados do cético final** (24/10/2026, 3 MEDIA e 3 BAIXA, mais o auditor L04 que não via o "
      "llms.txt e o index.md e o `GIT_OPTIONAL_LOCKS` do vigia): `t39` cria um repositório git de brinquedo com `origin` local (commit e push só para ele), `t41` roda o `vigia.bat` de verdade com um `custodiar.py` de brinquedo "
      "e `t43`/`t44` usam diretórios temporários. **O Nós vivo anda:** nove testes antigos (`t01`, `t04`, `t17`, `t18`, `t19`, `t20`, `t25`, `t32`, `t33`) leem o Nós vivo e foram aprovados com a v398 PRONTA; quando outra "
      "sessão o põe em obra (um.py != pino do selo: a v399 em construção) eles ficam **PULADOS, com o motivo dito** (nem aprovação nem falha de código). A rodada completa com o Nós PRONTA (13:55–14:00, t01–t45: "
      "**45/45**) está guardada em `evidencias_cetico_final\\SUITE_45de45_nos_pronta_20261024_1400.txt`; a de 14:32, **46/46** com o Nós congelado (vista), em `SUITE_46de46_nos_congelado_vista_20261024_1432.txt`; a anterior às mudanças, `--rapido`, em `BASELINE_antes_das_mudancas_rapido_20261024_1336.txt`." % (
          time.strftime("%d/%m/%Y %H:%M:%S"), sys.version.split()[0]), "",
      *([NOTA_VISTA, ""] if NOTA_VISTA else []),
      "## 1. Teste de aceitação (g) da ordem", "",
      "### `custodiar.py planejar --versao v397 --seco`  → código de saída **%d** (5 = nada a fazer por G1, com as decisões do operador do handoff abertas; 0 só se não houvesse nenhuma)" % rc97, "", "```", p97.strip(), "```", "",
      "### `custodiar.py planejar --versao v398 --seco`  → código de saída **%d** (a outra sessão custodia a v398 agora: o plano lista só o que ainda falta; 20 = um passo BLOQUEADO)" % rc98, "", "```", p98.strip(), "```", "",
      "### `custodiar.py vigiar`  → código de saída **%d**" % rcv, "", "```", pv.strip(), "```", "",
      "### `vigia.bat` REAL (MODO SOMBRA; o Python e o `custodiar.py` de verdade; `G1_PASTA` = pasta temporária, apagada) → código de saída **%d** em %.0f s" % (rb.returncode, seg_bat), "",
      "Arquivos que o vigia deixou na pasta: %s. `VIGIA_ULTIMO.txt`:" % ", ".join("`%s`" % a for a in arqs_vigia), "", "```", txt_vigia, "```",
      "(o código de saída é o do `vigiar`: %s)" % "0 custodiada · 1 pendente · 5 custodiada com decisões do operador abertas · 10 em obra · 20 incompleta/bloqueada · 30 falha de leitura/escrita · 40 divergência · 99 sem Python/CLI", "",
      "## 2. A suíte (`testes_g1.py`; código de saída %d)" % rc_s, ""]
md += bruto.split("\n", 2)[2].strip().splitlines()
md += ["", "## 3. Os roteiros dos céticos contra o pacote ANTERIOR às correções (`roteiro_no_codigo_antigo.py`; código de saída %d)" % rca, "",
       "O pacote de antes (os módulos `*.antes` guardados em `originais_antes_dos_ceticos\\`, sem `recibos.py`) montado em diretório temporário e posto a ler os mesmos cenários de brinquedo "
       "(`t27`, `t29`, `t30`): o defeito aparece nele e some no pacote atual. `util.py.antes` foi **reconstruído** desfazendo as três trocas de hoje (o `util.py` foi editado antes da cópia de segurança).", "",
       "```", pa.strip(), "```", "",
       "## 3b. Os roteiros do cético final contra o pacote ANTERIOR a esta rodada (`roteiro_no_codigo_antes_do_cetico_final.py`; código de saída %d)" % rcf, "",
       "O pacote de antes (os módulos `*.antes` de `originais_antes_do_cetico_final\\`: site, central, espelho, quadro, publica, caminhos, motor, util) montado em diretório temporário e posto a ler os "
       "mesmos cenários de brinquedo (`t38`, `t39`, `t43`, `t44`, `t45`): os seis defeitos aparecem nele e somem no pacote atual (cada linha termina com «o certo»). O 6º usa a mensagem do commit da "
       "v398 com os dados reais (somente leitura). `publica.py.antes` foi **reconstruído** desfazendo a única troca (o backup foi esquecido antes de editar; o tamanho 6.452 é o que o patch imprimiu).", "",
       "```", pf.strip(), "```", "",
       "## 4. O que os testes NÃO provam (dito, não calado)", "",
       "- Os passos que **chamam os geradores fixos no espelho real** (`E05` gerar_estado_atual, `E06`/`E08` gerar_portas + gerar_readme_frente + o laço até o ponto fixo, `E09` verificar_portas/guarda_do_selo, `E13`–`E16`, `E19`) e os que **rodam coisa pesada na Central** "
       "(`C7` runner ×2, `C9` 16 dispositivos, `C10` build, `C12` ledger) só foram verificados por **leitura do código, marcas contra o estado real e gates em fixtures**; não foram executados (a v398 está em custódia por outra sessão e não existe versão nova para custodiar). "
       "`C11` (os 16 FINAL) foi exercido só com FINAL de brinquedo (`t29`).",
       "- Não executados por regra da ordem: commit/push (`E10`,`E11`,`C14`), subida (`E18`, `C18`), ACOM (`C2`, `C17*`), `E12` (rede), `C19`/`C20` ao vivo (rodam o quadro e esperam serviços): o **gancho que remede o quadro velho** foi testado com um `remedir` de brinquedo (`t28`), nunca rodando `estado_do_organismo.py` no mundo real. Seus **gates** (conjunto esperado da subida, lista de permissão, portão de texto, trava, `--publicar`) estão testados.",
       "- `C5` em escala real (≈35 min, 474 mil arquivos) não foi rodado; a lógica (base = último snapshot conferido, delta por sha-256, exclusões, divergência, instante do selo) foi exercida em sandbox.",
       "- `E03` sandbox usa um **espelho de brinquedo** (a v397 guardada pelo passo zero) e uma guarda privada **sintética**: o arquivo de marcadores privados da casa NÃO foi lido (regra da ordem); a leitura real roda só em `executar`.",
       "- O laço `E08` (ponto fixo em ≤4 passadas) e o auditor foram escritos a partir da leitura dos geradores e do estado medido; **a convergência em 2–3 passadas é hipótese** até a primeira execução viva (a ESPEC L23 diz o mesmo).",
       "- O **registro das subidas** (E18) diz o que o ar TEM pelo que as subidas verificadas levaram; não consulta o ar. Quem muda o ar por fora do `subir_site.py` (painel, FTP manual) não aparece: o ensaio (E17, HTTP) e o quadro (`Site (ar)`) é que veem o ar.",
       "- `SUPERADO_REL` é honestidade, não prova: nas versões históricas a ferramenta não tem como provar o que a versão seguinte sobrescreveu; ela o diz em vez de fingir (ver o plano de v397).",
       "- **Nós congelado e asserções relaxadas (24/10/2026):** quando o Nós vivo não é a v398 PRONTA (a v399 em construção), esta composição roda TUDO numa **vista** dele (`testes\\nos_congelado.py`, `G1_RAIZ_NOS`): hardlinks para os arquivos do Nós vivo, com os que o cofre `um_unificado_v398` também guarda (selados, capturas, diário, handoff, stdout) e o kernel selado tomados do **cofre** — é a v398 como foi selada, não o Nós de hoje; a vista é desfeita no fim e nada do Nós vivo é tocado. Três asserções do mundo vivo foram **relaxadas** por deriva de outras sessões, sem tirar a forma: `t04` não conta arquivo do túnel criado DEPOIS da cópia desta custódia (ORDEM_022), `t18` aceita `E03` entre os pendentes da v398 e `t25` conta «pelo menos 27» passos do encadeador da Central pública (que ganhou `central_extra`).",
       "- **Do fechamento dos achados do cético final:** (1) o commit da Central com pathspec foi exercido em repositório de brinquedo (com `origin` local) — nunca no `.git` da Central real, e `C14` segue sem rodar "
       "ao vivo; (2) «nada a subir» foi exercido com relatórios fabricados no formato exato que `subir_site.py` grava (título e tabela lidos do código dele); nenhuma subida foi feita; (3) o `vigia.bat` rodou "
       "de verdade, mas a **tarefa agendada do Windows não está instalada** (é da gerência, junto com a decisão L17) e o `executar` NÃO é chamado por ele; (4) `C21` só confere o `iald_nucleo_fixo.json`: não "
       "roda o pipeline do app, não instala e não reinicia o serviço; (5) o R1 relido no fim de `C18` foi exercido com o encadeador e o leitor substituídos — a Central pública não subiu; (6) o hash de "
       "**amostra** do backup (E01) não pega um byte trocado, de mesmo tamanho, num arquivo que não esteja na amostra de 48 (a lista e os tamanhos de todos os arquivos, o selo de dentro e os selados são conferidos).", ""]
(G1 / "TESTES.md").write_text("\n".join(md), encoding="utf-8")
try:
    (G1 / "TESTES_BRUTO.md").unlink()
except OSError:
    pass
print("TESTES.md composto em %.0f s | suíte rc %d | v397 rc %d | v398 rc %d | vigiar rc %d | roteiro antigo rc %d" % (time.time() - t0, rc_s, rc97, rc98, rcv, rca))
