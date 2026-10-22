# -*- coding: utf-8 -*-
"""Os README dos três repositórios públicos da Central (22/10/2026) — central-publica (núcleo), central-publica-work e
central-publica-bancada —, com o vínculo patentário (lido dos dockets por vinculo_patentario.py), os vínculos cruzados ao the_boundary, ao
modo interativo do site e ao um.acom, o critério público e a nota de direitos. Números lidos do selo e dos índices.
Uso: <python do backend> gerar_readmes_publicos.py <raiz_dos_preparos>"""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
from vinculo_patentario import ler_vinculos  # noqa: E402

RAIZ = Path(sys.argv[1])
# o pino que vale no README público é o do selo PUBLICADO no the_boundary (HEAD), não o do Nós: o Nós pode estar uma versão à frente da
# custódia (22/10/2026: Nós em v396, espelho em v395 — o README diria v396 para um espelho que não a tem)
import subprocess  # noqa: E402
_r = subprocess.run(["git", "-C", r"C:\IALD\Artigo\the_boundary", "show", "HEAD:Um (absoluto) — Grande Atrator/um_absoluto_selo.json"],
                    capture_output=True)
assert _r.returncode == 0, ("selo do espelho ilegível — PARAR", _r.stderr[-300:])
selo = json.loads(_r.stdout.decode("utf-8"))
PIN, VER = selo["sha256"]["um.py"], selo.get("um_version")
info = json.loads(Path(r"C:\IALD\Site\tgl\v3.0_bancada\central_publica\acom\um_acom_info.json").read_text(encoding="utf-8"))
SITE = "https://teoriadagravitacaoluminodinamica.com"
GH = "https://github.com/rotolimiguel-iald"
REPOS = {"central-publica": "o núcleo: as 16 patentes (código, execuções, selos), a Fronteira Teórica, o cofre e o kernel, o cockpit",
         "central-publica-work": "a bancada de trabalho: as custódias, os ritos, as cadeias de selo, o app e a IALD nativa",
         "central-publica-bancada": "a bancada do ChatGPT: os projetos Lean, as entregas e o túnel de pesquisa"}
vs = ler_vinculos()
linhas = ["| pedido no INPI | título | depósito | PCT (OMPI) | data do PCT |", "|---|---|---|---|---|"]
for v in vs:
    linhas.append("| **%s** | %s | %s | %s | %s |" % (v["pedido_inpi"], (v["titulo"] or "").rstrip("."), v["deposito"] or "—", v["pct"] or "—", v["pct_data"] or "—"))
# quem deposita e quem inventa: LIDO dos formulários de depósito do INPI e dos recibos do ePCT (vinculo_patentario.py), nunca digitado —
# ERRATA AO LADO (22/10/2026): a 1ª versão deste gerador escrevia «Titular: IALD Ltda.»; os 16 formulários dizem pessoa física
_deps = sorted({(v["depositante"], v["tipo_de_pessoa"]) for v in vs})
_invs = sorted({v["inventor"] for v in vs if v["inventor"]})
_reqs = sorted({v["pct_requerente"] for v in vs if v["pct_requerente"]})
QUEM = "depositante (lido dos formulários de depósito no INPI): %s; inventor: %s%s" % (
    "; ".join("%s, %s" % (n, t.lower()) for n, t in _deps), "; ".join(_invs),
    ("; requerente nos PCT (como a OMPI o escreve): %s" % "; ".join(_reqs)) if _reqs else "")
adic = [(v["pedido_inpi"], a) for v in vs for a in v["processos_adicionais"]]
TAB = "\n".join(linhas)
if adic:
    TAB += "\n\nProcessos adicionais: " + "; ".join("**%s** (%s, de %s; %s)" % (a["processo"], a["papel"], v, a["deposito"] or "—") for v, a in adic) + "."
COMUM = """
## O critério público

Por ordem do operador, **todo o código e todo resultado** estão publicados. Ficam fora só:
- **dados pessoais** (a regra do operador: «segredo são dados pessoais, somente») — trocados à vista por «[dado pessoal removido]» no
  texto (CPF, RG, telefone, e-mail pessoal, endereço, CEP, data de nascimento); PDFs, compactados e documentos que os trazem e não se
  podem mascarar ficam fora (o texto técnico dos pedidos segue nas partes separadas: relatório, reivindicações, resumo, desenhos);
- **credenciais e estado de execução** (senhas, tokens, chaves; perfis de navegador, login, sessões, segredos): todo arquivo que os contém
  fica fora;
- **as notas operacionais do operador** (prazos, protocolo do PCT, leituras do monitor, pendências, prompts compilados): ficam na Central dele;
- **obras de terceiros** (PDFs de artigos e livros consultados, pacotes de software de terceiros): ficam fora — baixar da fonte;
- arquivos acima do limite do GitHub e caches binários deriváveis: só no índice.

Os marcadores internos da casa (nomes de módulos, o protocolo de colapso, desclassificado pelo operador em 28/09/2026) **não** são motivo
de exclusão: não há segredo industrial a proteger.

`INDICE_PUBLICO.json` dá o sha256 de cada arquivo publicado; `EXCLUSOES_PUBLICAS.json`, a contagem do que ficou fora e o motivo.

## Direitos

Como no [the_boundary](https://github.com/rotolimiguel-iald/the_boundary#license): publicado como **source-available**, para
reprodutibilidade e verificação científica — o código pode ser **lido, executado e verificado**. Os dispositivos são objeto de **pedidos de
patente** depositados (tabela no núcleo; {QUEM}): a reprodução comercial depende de autorização do depositante. A reprodução científica
e simulada da teoria é livre — uma teoria científica não é patenteável.

## A régua

PROVADA = validade (o kernel prova a implicação); CONFIRMADA = creditação (ato de terceiros, recusada à máquina); `NOT_FALSIFIED` nunca é
`CONFIRMED`; β = α·√e, nunca literal. Pedido de patente depositado não é patente concedida.
""".replace("{QUEM}", QUEM)
LINKS = """
| onde | o quê |
|---|---|
| [%s/central/](%s/central/) | **o modo interativo da Central**, só de visualização: o cockpit do operador em retrato (patentes, código, execuções, Fronteira, TGL) |
| [%s/central/um.acom](%s/central/um.acom) | **o um.acom**: a Central inteira colapsada pelo dispositivo ACOM (%d arquivos; sha256 `%s`); chave universal pública `%s`; abrir no descompactador público da IALD |
| [%s/the_boundary](%s/the_boundary) | **a teoria**: o `um.py` %s (`%s`), os artigos, o kernel Lean — o espelho canônico |
| [%s/central-publica](%s/central-publica) · [work](%s/central-publica-work) · [bancada](%s/central-publica-bancada) | os três repositórios desta Central |
""" % (SITE, SITE, SITE, SITE, info["n_arquivos"], info["sha256"][:16], info["chave_publica"], GH, GH, VER, PIN[:16], GH, GH, GH, GH)
SO = set(sys.argv[2:])   # (opcional) só estes repositórios — o README de um repositório já publicado não se regrava por tabela
for repo, desc in REPOS.items():
    if SO and repo not in SO:
        continue
    d = RAIZ / repo
    if not d.is_dir():
        print("sem preparo:", repo); continue
    idx = json.loads((d / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))
    corpo = ["# %s — a Central de Patentes da IALD, aberta" % repo, "",
             "Este repositório é **%s**. A Central foi aberta ao público por ordem do operador, Luiz Antonio Rotoli Miguel (IALD Ltda., CNPJ "
             "62.757.606/0001-23), em 22/10/2026. %d arquivos publicados; selo da teoria: `um.py` %s `%s`." % (desc, idx["n_arquivos"], VER, PIN[:16]),
             "", LINKS.strip(), ""]
    if repo == "central-publica":
        corpo += ["## O vínculo patentário", "",
                  "Os dispositivos da Central são objeto de **pedidos de patente depositados** no INPI (Brasil) e no PCT (OMPI) — pedidos, não "
                  "patentes concedidas. " + QUEM[0].upper() + QUEM[1:] + ".", "", TAB, "",
                  "Cada pasta `patents/<pedido>_<dispositivo>/` traz o runner (`runner/one_<dispositivo>.py`), o código FINAL autocontido "
                  "(`<dispositivo>_FINAL.py`), as execuções (`results/`) e os selos (`seals/`); o texto técnico de cada pedido (relatório, "
                  "reivindicações, resumo, desenhos) está em `Patentes/`.", ""]
    corpo.append(COMUM.strip())
    (d / "README.md").write_text("\n".join(corpo) + "\n", encoding="utf-8")
    if repo == "central-publica":
        (d / "PATENTES.md").write_text("# O vínculo patentário da Central\n\n" + TAB + "\n\nPedidos de patente depositados (não concedidos). "
                                       + QUEM[0].upper() + QUEM[1:] + ".\n", encoding="utf-8")
        (d / "vinculo_patentario.json").write_text(json.dumps([{k: v[k] for k in v if k != "dir"} for v in vs], ensure_ascii=False, indent=1),
                                                   encoding="utf-8")
    print("README:", repo, (d / "README.md").stat().st_size, "bytes")
