# -*- coding: utf-8 -*-
"""publicar_readme_pinado_v406.py — PREPARA, no espelho `the_boundary`, a publicação do README pinado da v406. NÃO FAZ COMMIT NEM PUSH (a gerência faz).

O que faz, nesta ordem (fail-closed: qualquer passo que falhe PARA e lista os backups feitos até ali):
  0. precondições: espelho = repositório git LIMPO e sem nada em stage; candidato inteiro e coerente (readme_pinado.py --verificar --conferir-fontes sobre ele);
     o selo do espelho e do Nós são aqueles de que o candidato nasceu; as âncoras do remendo do gerar_portas.py estão lá (ou ele já foi remendado).
  1. backup de BYTES (`<arquivo>.bak_<carimbo>`, na mesma pasta) de README.md e de tools/gerar_portas.py; nenhum arquivo do espelho é gravado sem isso.
  2. copia o PRIMORDIAL.json, o template e as partes do candidato (tools/readme_pinado/...).
  3. remenda tools/gerar_portas.py (backup acima): descrições de PRIMORDIAL.json e PINO_README.json e as duas linhas do llms.txt; o PORTA.json da raiz já lista
     os arquivos da raiz por git ls-files, então os dois entram ao serem postos em stage.
  4. gera README.md e PINO_README.json do espelho com readme_pinado.py (e confere se o README é byte a byte o do candidato) e põe em stage SÓ os caminhos
     deste pacote (README.md, PRIMORDIAL.json, PINO_README.json, tools/readme_pinado/, tools/gerar_portas.py).
  5. o laço do E08 da G1 (gerar_secoes -> gerar_portas -> README <-> portas até o README parar de mudar -> read-brief / llms do site -> gerar_portas) até o PONTO FIXO,
     com `readme_pinado.py --gerar` no lugar de `gerar_readme_frente.py`. Depois de cada geração, só entram em stage: os caminhos do pacote, as portas (PORTA.md/json,
     TUNEL.json/md, llms.txt) e, se os geradores do site rodaram, read-brief.md e secoes/. Qualquer OUTRO caminho alterado PARA a execução antes de ir ao stage.
  6. confere: readme_pinado.py --verificar --conferir-fontes contra o espelho; as verificações do E09 (verificar_portas.py e guarda_do_selo.py, lidas como a G1 as lê);
     a auditoria L04 dos números citados (arquivo (N bytes)); imprime `git status --short` e `git diff --cached --stat`.

Uso:  python publicar_readme_pinado_v406.py --seco       (só as precondições e o plano; não grava nada)
      python publicar_readme_pinado_v406.py              (executa no espelho real)
      python publicar_readme_pinado_v406.py --espelho <clone> --ensaio    (ensaio num clone: os geradores do site, que têm o espelho real fixo no código, NÃO rodam)
      --sem-site   não roda os geradores do site (read-brief / llms / secoes do site): o read-brief.md do espelho citará o tamanho antigo do README e a auditoria L04 da G1 o apontará.
Os geradores do site (G1 E08) escrevem também no código-fonte local do site (Site\\tgl\\v3.0), com backup de bytes; não sobem nada ao ar."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

QUI = Path(__file__).resolve().parent
G1_TOOLS = Path(r"C:\IALD\Central de Patentes\tools")
sys.path.insert(0, str(G1_TOOLS))
from custodia_g1.caminhos import Caminhos  # noqa: E402

A3 = "Um (absoluto) \u2014 Grande Atrator"
PACOTE = ("README.md", "PRIMORDIAL.json", "PINO_README.json", "tools/gerar_portas.py")
PACOTE_DIR = ("tools/readme_pinado/",)
PORTAS_BASE = ("PORTA.md", "PORTA.json", "TUNEL.json", "TUNEL.md", "llms.txt")
SITE_TOCADOS = ("read-brief.md",)
SITE_DIRS = ("secoes/",)


class Parar(SystemExit):
    def __init__(self, msg, detalhes=()):
        super().__init__(2)
        print("\nPARADO: " + msg)
        for d in detalhes:
            print("   - " + str(d))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rodar(cmd, cwd, timeout=1800):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    return r.returncode, (r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace"))


class Pub:
    def __init__(self, a):
        self.cam = Caminhos()
        self.a = a
        self.tb = Path(a.espelho) if a.espelho else self.cam.TB
        self.real = self.tb.resolve() == self.cam.TB.resolve()
        self.cand = Path(a.candidato)
        self.py = str(self.cam.PYTHON)
        self.ts = time.strftime("%Y%m%d_%H%M%S")
        self.baks = []
        self.nos = Path(a.nos) if a.nos else self.cam.NOS
        self.site_gens = self.real and not a.sem_site and not a.ensaio
        self.rp = self.cam.CEN / "tools" / "custodia_g1" / "readme_pinado.py"
        self.pr = self.cam.CEN / "tools" / "custodia_g1" / "primordial.py"

    # ---------------------------------------------------------------- utilidades
    def git(self, *args, check=True):
        rc, out = rodar(["git", "-c", "core.quotepath=off", "-C", str(self.tb)] + list(args), self.tb)
        if check and rc != 0:
            self.falha("git %s falhou (rc %s)" % (" ".join(args), rc), out.strip().splitlines()[-6:])
        return out

    def falha(self, msg, det=()):
        det = list(det)
        if self.baks:
            det.append("backups de bytes feitos até aqui (restaure copiando de volta, se precisar desfazer): " + " | ".join(str(b) for b in self.baks))
        raise Parar(msg, det)

    def backup(self, p):
        p = Path(p)
        if not p.exists():
            return None
        b = p.read_bytes()
        bak = p.with_name(p.name + ".bak_" + self.ts)
        bak.write_bytes(b)
        if bak.read_bytes() != b:
            self.falha("backup de bytes não confere: " + str(bak))
        self.baks.append(bak)
        return bak

    def grava(self, p, b, rotulo):
        p = Path(p)
        if p.exists() and p.read_bytes() == b:
            print("  = %s (inalterado)" % rotulo)
            return
        if p.exists():
            self.backup(p)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(p.name + ".tmp")
        tmp.write_bytes(b)
        if tmp.stat().st_size != len(b):
            self.falha("gravação truncada: " + str(p))
        os.replace(tmp, p)
        print("  + %s (%d B)" % (rotulo, len(b)))

    def rp_args(self, readme_saida, saida, primordial, template, partes, portas_de):
        return [self.py, "-X", "utf8", str(self.rp), "--gerar", "--primordial", str(primordial), "--template", str(template), "--partes", str(partes),
                "--saida", str(saida), "--nome", readme_saida, "--portas-de", str(portas_de), "--espelho", str(self.tb), "--nos", str(self.nos)]

    # ---------------------------------------------------------------- 0. precondições
    def precondicoes(self):
        a, tb, cand = self.a, self.tb, self.cand
        falhas = []
        if not (tb / ".git").exists():
            falhas.append("o espelho não é um repositório git: " + str(tb))
        for n in ("README.candidato.md", "PRIMORDIAL.json", "PINO_README.json", "readme_template.md"):
            if not (cand / n).is_file():
                falhas.append("falta no candidato: " + n)
        if not list((cand / "readme_partes").glob("*.md")):
            falhas.append("candidato sem readme_partes/*.md")
        if a.ensaio and self.real:
            falhas.append("--ensaio não pode rodar no espelho real")
        if falhas:
            self.falha("precondições", falhas)
        st = self.git("status", "--porcelain", "-uall")
        if st.strip():
            falhas.append("o espelho não está limpo (commit ou guarde o que há antes): " + " ; ".join(st.strip().splitlines()[:5]))
        if self.git("diff", "--cached", "--name-only").strip():
            falhas.append("há arquivos em stage no espelho: " + self.git("diff", "--cached", "--name-only").strip().replace("\n", " ; ")[:200])
        pino = json.loads((cand / "PINO_README.json").read_text(encoding="utf-8"))
        if sha(cand / "README.candidato.md") != pino["readme"]["sha256"]:
            falhas.append("README.candidato.md não é o do PINO_README.json do candidato")
        sel_tb, sel_nos = sha(tb / A3 / "um_absoluto_selo.json"), sha(self.nos / "um_absoluto_selo.json")
        if not (sel_tb == sel_nos == pino["selo"]["sha256"]):
            falhas.append("o selo do espelho (%s), o do Nós (%s) e o de que o candidato nasceu (%s) não são o mesmo" % (sel_tb[:16], sel_nos[:16], pino["selo"]["sha256"][:16]))
        if sha(tb / A3 / "um.py") != pino["pin_um_py"]:
            falhas.append("o um.py do espelho não é o pin do candidato")
        gp = (tb / "tools" / "gerar_portas.py").read_text(encoding="utf-8")
        if "PRIMORDIAL.json" not in gp:
            for k, (ancora, _) in self.remendos(gp).items():
                if gp.count(ancora) != 1:
                    falhas.append("âncora do remendo do gerar_portas.py (%s) não casa exatamente uma vez (%d)" % (k, gp.count(ancora)))
        rt = (tb / "README.md").read_text(encoding="utf-8")
        if rt.count("<!-- PORTAS:INI -->") != 1 or rt.count("<!-- PORTAS:FIM -->") != 1:
            falhas.append("o README do espelho não tem exatamente um bloco de portas")
        if falhas:
            self.falha("precondições reprovadas", falhas)
        cmd = [self.py, "-X", "utf8", str(self.rp), "--verificar", "--conferir-fontes", "--primordial", str(cand / "PRIMORDIAL.json"), "--template", str(cand / "readme_template.md"),
               "--partes", str(cand / "readme_partes"), "--readme", str(cand / "README.candidato.md"), "--pino", str(cand / "PINO_README.json"), "--nos", str(self.nos), "--espelho", str(tb)]
        rc, out = rodar(cmd, tb)
        print("  candidato: " + (out.strip().splitlines() or ["(sem saída)"])[-1])
        if rc != 0:
            self.falha("o candidato não passa em readme_pinado.py --verificar --conferir-fontes", out.strip().splitlines()[-8:])
        # o bloco das portas de hoje produz o README do candidato?
        tmp = Path(os.environ.get("TEMP", ".")) / ("pub_readme_prova_" + self.ts)
        tmp.mkdir(parents=True, exist_ok=True)
        rc, out = rodar(self.rp_args("README.md", tmp, cand / "PRIMORDIAL.json", cand / "readme_template.md", cand / "readme_partes", tb / "README.md"), tb)
        igual = rc == 0 and sha(tmp / "README.md") == pino["readme"]["sha256"]
        print("  README gerado com o bloco das portas de hoje == README do candidato: %s" % ("sim" if igual else "NÃO (o bloco das portas mudou desde o candidato; o laço o refaz)"))
        for f in tmp.glob("*"):
            f.unlink()
        tmp.rmdir()
        return pino

    def remendos(self, gp):
        """(âncora exata, texto novo) do gerar_portas.py; a ordem e o texto são os únicos pontos de contato com aquele gerador."""
        d_llms = '    "llms.txt": "A porta de entrada para IA (convencao llmstxt.org): as URLs raw diretas de tudo que importa",\n'
        d_novo = (d_llms +
                  '    "PRIMORDIAL.json": "A FONTE UNICA das informacoes primordiais (README pinado e site): cada numero com a chave de origem, o arquivo e o sha256 da fonte -- '
                  'gerada por tools/custodia_g1/primordial.py, nunca a mao",\n'
                  '    "PINO_README.json": "O PINO do README: sha256 do README gerado, do PRIMORDIAL.json, do template, das partes e do selo de que nasceu -- o README so\' se edita pelo gerador",\n')
        l_readme = ('    T.append("- [README.md](%s): a PAGINA DE FRENTE (<= 40 KB, gerada por script): o selo, reproduzir, as portas, os tres artigos, a ordem de leitura, abstract, citar." '
                    '% registra(url_raw("README.md")))\n')
        l_novo = (l_readme +
                  '    T.append("- [PRIMORDIAL.json](%s): a FONTE UNICA das informacoes primordiais -- cada numero do README e do site com a chave de origem, o arquivo e o sha256 da fonte '
                  '(gerada por script)." % registra(url_raw("PRIMORDIAL.json")))\n'
                  '    T.append("- [PINO_README.json](%s): o PINO do README -- sha256 do README, do PRIMORDIAL.json, do template, das partes e do selo; o README so\' se edita pelo gerador." '
                  '% registra(url_raw("PINO_README.json")))\n')
        r_old = "(tools/gerar_readme_frente.py, 11/09/2026)"
        r_new = "(tools/custodia_g1/readme_pinado.py a partir de PRIMORDIAL.json, pinado por PINO_README.json; antes tools/gerar_readme_frente.py, 11/09/2026)"
        return {"descricoes": (d_llms, d_novo), "llms.txt": (l_readme, l_novo), "descricao do README": (r_old, r_new)}

    def snapshot_geradas(self):
        """Backup de BYTES, fora do repositório (the_boundary_BACKUPS\\readme_pinado_<carimbo>), de todo arquivo rastreado que os geradores podem reescrever."""
        rc, out = rodar(["git", "-c", "core.quotepath=off", "-C", str(self.tb), "ls-files", "-z"], self.tb)
        if rc != 0:
            self.falha("git ls-files falhou")
        alvo = self.cam.BK / ("readme_pinado_v406_" + self.ts + ("" if self.real else "_ENSAIO"))
        n = 0
        for rel in (x for x in out.split("\0") if x):
            base = rel.rsplit("/", 1)[-1]
            if base in PORTAS_BASE or rel in SITE_TOCADOS or any(rel.startswith(d) for d in SITE_DIRS):
                src = self.tb / rel
                if src.is_file():
                    dst = alvo / rel
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    b = src.read_bytes()
                    dst.write_bytes(b)
                    if dst.read_bytes() != b:
                        self.falha("backup de bytes não confere: " + str(dst))
                    n += 1
        self.baks.append(alvo)
        print("  snapshot de %d arquivos gerados (portas, TUNEL, llms.txt, read-brief, secoes) em %s" % (n, alvo))

    # ---------------------------------------------------------------- 3. remendo
    def remendar_gerar_portas(self):
        p = self.tb / "tools" / "gerar_portas.py"
        gp = p.read_text(encoding="utf-8")
        if "PRIMORDIAL.json" in gp:
            print("  = gerar_portas.py já remendado")
            return
        novo = gp
        for k, (old, new) in self.remendos(gp).items():
            if novo.count(old) != 1:
                self.falha("âncora do remendo (%s) não casa exatamente uma vez" % k)
            novo = novo.replace(old, new)
        try:
            compile(novo, str(p), "exec")
        except SyntaxError as e:
            self.falha("o gerar_portas.py remendado não compila: %s" % e)
        self.grava(p, novo.encode("utf-8"), "tools/gerar_portas.py (remendo: descrições e llms.txt)")

    # ---------------------------------------------------------------- git: stage só do permitido
    def permitido(self, caminho):
        c = caminho.replace("\\", "/")
        base = c.rsplit("/", 1)[-1]
        if c in PACOTE or any(c.startswith(d) for d in PACOTE_DIR):
            return True
        if base in PORTAS_BASE:
            return True
        if self.site_gens and (c in SITE_TOCADOS or any(c.startswith(d) for d in SITE_DIRS)):
            return True
        return False

    def stage_permitido(self):
        rc, out = rodar(["git", "-c", "core.quotepath=off", "-C", str(self.tb), "status", "--porcelain", "-z", "-uall"], self.tb)
        if rc != 0:
            self.falha("git status falhou")
        itens = [x for x in out.split("\0") if x]
        caminhos, i = [], 0
        while i < len(itens):
            x = itens[i]
            xy, p = x[:2], x[3:]
            if xy[0] in "RC":
                i += 1                    # o segundo caminho do renome
            caminhos.append((xy, p))
            i += 1
        fora = [p for xy, p in caminhos if not self.permitido(p)]
        if fora:
            self.falha("caminhos alterados FORA do pacote e das portas (nada foi posto em stage):", fora[:20])
        dentro = [p for xy, p in caminhos if self.permitido(p)]
        if dentro:
            self.git("add", "--", *dentro)
        return dentro

    # ---------------------------------------------------------------- 5. o laço do E08
    def assinatura(self):
        h = hashlib.sha256()
        itens = [self.tb / n for n in ("README.md", "PINO_README.json", "PRIMORDIAL.json", "ESTADO_ATUAL.md", "read-brief.md", "llms.txt", "TUNEL.json", "TUNEL.md", "PORTA.json", "PORTA.md")]
        itens += sorted((self.tb / "secoes").glob("*")) if (self.tb / "secoes").is_dir() else []
        if self.site_gens:
            itens += [self.cam.SITE / "read-brief.md", self.cam.SITE / "llms.txt"]
        for p in itens:
            if not p.is_file():
                continue
            t = p.read_text(encoding="utf-8", errors="replace")
            t = re.sub(r"\d{4}-\d\d-\d\d(T[\d:]+Z)?", "<D>", t)
            h.update(p.name.encode("utf-8") + b"\0" + t.encode("utf-8"))
        return h.hexdigest()[:16]

    def tool(self, onde, script, rotulo=None):
        rc, out = rodar([self.py, "-X", "utf8", "tools/" + script], onde)
        if rc != 0:
            self.falha("%s falhou (rc %s)" % (rotulo or script, rc), out.strip().splitlines()[-8:])
        return out

    def gerar_readme(self):
        rc, out = rodar(self.rp_args("README.md", self.tb, self.tb / "PRIMORDIAL.json", self.tb / "tools" / "readme_pinado" / "readme_template.md",
                                     self.tb / "tools" / "readme_pinado" / "readme_partes", self.tb / "README.md"), self.tb)
        if rc != 0:
            self.falha("readme_pinado.py --gerar falhou", out.strip().splitlines()[-8:])
        return out.strip().splitlines()[0] if out.strip() else ""

    def laco(self):
        banc = self.cam.BANC
        sig_ant, passadas = None, []
        for i in range(1, 5):
            if self.site_gens:
                self.tool(banc, "gerar_secoes.py")
            self.stage_permitido()
            self.tool(self.tb, "gerar_portas.py")
            for _ in range(3):
                antes = sha(self.tb / "README.md")
                print("  [%d] %s" % (i, self.gerar_readme()))
                self.stage_permitido()
                self.tool(self.tb, "gerar_portas.py")
                if sha(self.tb / "README.md") == antes:
                    break
            if self.site_gens:
                for g in ("gerar_read_brief.py", "gerar_llms_site.py", "gerar_head_camada_texto.py"):
                    self.tool(banc, g)
            self.stage_permitido()
            self.tool(self.tb, "gerar_portas.py", "gerar_portas.py (hash final)")
            self.stage_permitido()
            sig = self.assinatura()
            passadas.append(sig)
            print("  passada %d: assinatura %s" % (i, sig))
            if sig == sig_ant:
                return passadas
            sig_ant = sig
        self.falha("o laço não convergiu em 4 passadas (arquivos oscilam)", passadas)

    # ---------------------------------------------------------------- 6. conferências
    def l04(self):
        rx = re.compile(r"([A-Za-z0-9_./%-]+\.[A-Za-z0-9]{1,5})\)?\s*\(([0-9][0-9.,]*)\s*bytes\b")
        base = {"TB": self.tb, "SITE": self.cam.SITE}
        sup = [("TB", "read-brief.md"), ("TB", "llms.txt")] + ([("SITE", "read-brief.md"), ("SITE", "llms.txt")] if self.site_gens else [])
        div = []
        for raiz, nome in sup:
            p = base[raiz] / nome
            if not p.is_file():
                continue
            for m in rx.finditer(p.read_text(encoding="utf-8", errors="replace")):
                alvo = m.group(1).split("/secoes/")[-1] if "/secoes/" in m.group(1) else m.group(1).rsplit("/", 1)[-1]
                rel = ("secoes/" + alvo) if "/secoes/" in m.group(1) else alvo
                cit = int(re.sub(r"[.,]", "", m.group(2)))
                real = next((q.stat().st_size for q in (base["TB"] / rel, base["SITE"] / rel) if q.is_file()), None)
                if real is not None and real != cit:
                    div.append("%s:%s cita %s=%s, real %s" % (raiz, nome, rel, cit, real))
        return div

    def conferir(self):
        erros = []
        cmd = [self.py, "-X", "utf8", str(self.rp), "--verificar", "--conferir-fontes", "--primordial", str(self.tb / "PRIMORDIAL.json"),
               "--template", str(self.tb / "tools" / "readme_pinado" / "readme_template.md"), "--partes", str(self.tb / "tools" / "readme_pinado" / "readme_partes"),
               "--readme", str(self.tb / "README.md"), "--pino", str(self.tb / "PINO_README.json"), "--nos", str(self.nos), "--espelho", str(self.tb)]
        rc, out = rodar(cmd, self.tb)
        print("  readme_pinado --verificar --conferir-fontes: " + (out.strip().splitlines() or ["(sem saída)"])[-1])
        if rc != 0:
            erros.append("README PINADO reprovou: " + " | ".join(out.strip().splitlines()[-4:]))
        rc, out = rodar([self.py, "-X", "utf8", "tools/verificar_portas.py"], self.tb)
        ok = bool(re.search(r"ERROS\s*\.+\s*0\b", out)) and "TODAS AS PORTAS RESOLVEM" in out
        print("  verificar_portas.py: " + ("ERROS 0, TODAS AS PORTAS RESOLVEM" if ok else "REPROVOU"))
        if not ok:
            erros.append("verificar_portas.py: " + (out.strip().splitlines() or [""])[-1][:120])
        rc, out = rodar([self.py, "-X", "utf8", "tools/guarda_do_selo.py"], self.tb)
        ok = rc == 0 and bool(re.search(r"ERROS\s*\.+\s*0\b", out)) and "O QUE SE PUBLICA E O QUE O SELO DESCREVE" in out
        print("  guarda_do_selo.py: " + ("ERROS 0, O QUE SE PUBLICA E O QUE O SELO DESCREVE" if ok else "REPROVOU (rc %s)" % rc))
        if not ok:
            erros.append("guarda_do_selo.py reprovou (rc %s): %s" % (rc, " | ".join(out.strip().splitlines()[-3:])))
        d = self.l04()
        print("  números citados («arquivo (N bytes)»): %s" % ("0 defasados" if not d else "%d DEFASADOS" % len(d)))
        if d and self.site_gens:
            erros.append("números citados defasados (L04): " + " ; ".join(d[:4]))
        elif d:
            print("  AVISO (geradores do site não rodaram; a G1 o apontará no E08 até o read-brief ser regerado): " + " ; ".join(d[:3]))
        if (self.tb / "README.md").stat().st_size > 40960:
            erros.append("README acima do teto de 40.960 bytes")
        return erros

    # ---------------------------------------------------------------- roteiro
    def rodar(self):
        a, tb, cand = self.a, self.tb, self.cand
        print("espelho: %s%s | candidato: %s | python: %s" % (tb, "" if self.real else " (ENSAIO/clone)", cand, self.py))
        print("geradores do site (E08): %s" % ("SIM (escrevem também em Site\\tgl\\v3.0, com backup de bytes)" if self.site_gens else "NÃO"))
        print("\n[0] precondições")
        pino = self.precondicoes()
        print("    candidato: README %d B, sha16 %s; selo %s; pin %s" % ((cand / "README.candidato.md").stat().st_size, pino["readme"]["sha16"], pino["selo"]["sha256"][:16], pino["pin_um_py"][:16]))
        if a.seco:
            print("\n--seco: precondições OK; nada foi gravado. Plano: backup de README.md e gerar_portas.py; copiar PRIMORDIAL.json, template e partes; remendar gerar_portas.py; "
                  "gerar README.md e PINO_README.json; stage só do pacote; laço do E08 até o ponto fixo; conferir; imprimir status e stat. SEM commit e SEM push.")
            return 0
        print("\n[1] backups de bytes")
        for rel in ("README.md", "tools/gerar_portas.py"):
            b = self.backup(tb / rel)
            print("  backup: %s" % b)
        self.snapshot_geradas()
        print("\n[2] arquivos do pacote")
        self.grava(tb / "PRIMORDIAL.json", (cand / "PRIMORDIAL.json").read_bytes(), "PRIMORDIAL.json")
        self.grava(tb / "tools" / "readme_pinado" / "readme_template.md", (cand / "readme_template.md").read_bytes(), "tools/readme_pinado/readme_template.md")
        for p in sorted((cand / "readme_partes").glob("*.md")):
            self.grava(tb / "tools" / "readme_pinado" / "readme_partes" / p.name, p.read_bytes(), "tools/readme_pinado/readme_partes/" + p.name)
        print("\n[3] remendo do gerar_portas.py")
        self.remendar_gerar_portas()
        print("\n[4] README.md e PINO_README.json do espelho")
        print("  " + self.gerar_readme())
        igual = sha(tb / "README.md") == pino["readme"]["sha256"]
        print("  README do espelho == README do candidato: %s" % ("sim" if igual else "NÃO (o bloco das portas de hoje difere; o laço o refaz)"))
        self.stage_permitido()
        print("\n[5] laço README <-> portas até o ponto fixo")
        self.laco()
        print("\n[6] conferências")
        erros = self.conferir()
        print("\n--- git status --short")
        print(self.git("status", "--short", "-uall").rstrip() or "(vazio)")
        print("--- git diff --cached --stat")
        print(self.git("diff", "--cached", "--stat").rstrip() or "(vazio)")
        if erros:
            self.falha("as conferências reprovaram (nada foi commitado; o stage fica para a gerência decidir):", erros)
        print("\nPRONTO PARA A GERÊNCIA: tudo conferido e em stage. NÃO houve commit nem push. Backups de bytes: %s" % " | ".join(str(b) for b in self.baks))
        return 0


def main():
    ap = argparse.ArgumentParser(description="prepara (sem commit, sem push) a publicação do README pinado da v406 no espelho")
    ap.add_argument("--espelho", help="espelho (padrão: C:\\IALD\\Artigo\\the_boundary)")
    ap.add_argument("--candidato", default=str(QUI), help="pasta do candidato (padrão: a deste script)")
    ap.add_argument("--nos", help="pasta do Nós (padrão: a da casa)")
    ap.add_argument("--seco", action="store_true", help="só as precondições e o plano; não grava nada")
    ap.add_argument("--ensaio", action="store_true", help="espelho de ensaio (clone): não roda os geradores do site")
    ap.add_argument("--sem-site", action="store_true", help="não roda os geradores do site")
    a = ap.parse_args()
    return Pub(a).rodar()


if __name__ == "__main__":
    sys.exit(main())
