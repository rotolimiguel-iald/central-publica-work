# -*- coding: utf-8 -*-
"""Registro FINAL da tarefa de 22/10/2026 (sessão a7 da Central; ordem do operador: «Encontre vulnerabilidades em php e as corrija. A
licença é como você falou mesmo, tudo certo. Atualize tudo com a nova versão do um.py»): a correção de PHP (site no ar e backup do
WordPress) e a Central pública na v396. Superfícies: memória nova (php-site-e-wordpress-22out.md) + linha no MEMORY.md; apêndices em
central-publica-22out.md, site-sessao-estado.md, MEMORY_2.md, DIARIO_DO_SITE.md e TGL_ATLAS.md (§X); rota no Mapa de Rotas. Números LIDOS
dos registros e do git; backup de BYTES antes de tocar; temporário -> confere -> substitui."""
import glob, json, os, subprocess, sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
CEN = r"C:\IALD\Central de Patentes"
WP = CEN + r"\work\php_e_v396_22out"
WC = CEN + r"\work\central_publica_22out"
W6 = CEN + r"\work\custodia_v396_22out"


def git(cwd, *a):
    return subprocess.run(["git", "-C", cwd] + list(a), capture_output=True, text=True).stdout.strip()


def tocar(p, f, pode_encolher=False):
    raw = open(p, "rb").read()
    open(p + ".bak_" + TS, "wb").write(raw)
    nl = "\r\n" if b"\r\n" in raw else "\n"
    novo = f(raw.decode("utf-8"), nl).encode("utf-8")
    tmp = p + ".tmp_" + TS
    open(tmp, "wb").write(novo)
    assert pode_encolher or os.path.getsize(tmp) > len(raw), p
    os.replace(tmp, p)
    print("ok", os.path.basename(p), len(raw), "->", os.path.getsize(p))


def ap(p, texto):
    tocar(p, lambda t, nl: t.rstrip("\r\n") + nl + nl + texto.strip("\n").replace("\n", nl) + nl)


reg = json.load(open(WP + r"\registro_htaccess_site.json", encoding="utf-8"))
assert reg["fase1"]["scripts_403_sem_php"] and reg["fase1"]["cabecalhos_ok"] and reg["teste_redirecionamento"]["ok"]
assert reg["fase2"]["https_llms"] == 200 and reg["multiext"]["x_php_txt"] == 403
HT16 = reg["multiext"]["sha16_depois"]
heads = {}
for r in ("central-publica", "central-publica-work", "central-publica-bancada"):
    d = r"C:\IALD\Central_publica" + "\\" + r
    h, o = git(d, "rev-parse", "--short=8", "HEAD"), git(d, "rev-parse", "--short=8", "origin/main")
    assert h == o, (r, h, o)
    heads[r] = (h, json.load(open(d + r"\INDICE_PUBLICO.json", encoding="utf-8"))["n_arquivos"])
info = json.load(open(r"C:\IALD\Site\tgl\v3.0_bancada\central_publica\acom\um_acom_info.json", encoding="utf-8"))
ACOM16 = info["sha256"][:16]
sub = sorted(glob.glob(r"C:\IALD\Site\tgl\v3.0_bancada\subidas\20261022_2*"), key=os.path.getmtime)
sub = [s for s in sub if not s.endswith("_dryrun")][-1]
assert "SUBIDA VERIFICADA" in open(os.path.join(sub, "RELATORIO.md"), encoding="utf-8").read(), sub
SUB = os.path.basename(sub)

PHP = ("PHP (22/10/2026, sessão a7, ordem do operador «Encontre vulnerabilidades em php e as corrija»): auditoria em workflow (5 frentes, "
       "cada uma com cético; 47 achados; `work/php_e_v396_22out/PLANO_CORRECAO_PHP.md`). NO AR: o servidor do site da TGL (estático, 0 "
       "arquivos PHP) entregava todo `*.php` ao PHP-FPM 8.3.0 (aviso da php.net de 21/10/2026: RCE sem autenticação, corrigida na "
       "8.3.36); corrigido no `.htaccess` do site em etapas com volta automática — todo pedido de script 403 no Apache sem X-Powered-By, "
       "http -> 301 https (teste prévio numa subpasta, apagada), HSTS em rampa (300 s), nosniff, X-Frame-Options, Referrer-Policy e "
       "Permissions-Policy; teste da auditoria: falhas 0 (linha de base 28); `.htaccess` local sha16 `%s` (backups .bak_ ao lado). "
       "BACKUP do WordPress (`C:\\Users\\rotol\\Wordpress Backup`): sem malware nem backdoor; Parte A aplicada (as 11 credenciais do "
       "wp-config.php fora de todos os arquivos; o nome do banco = usuário = $table_prefix mantido; DISALLOW_FILE_EDIT, FORCE_SSL_ADMIN, "
       "erros fora da tela; .htaccess v2; mu-plugin; 12 sobras com IP e caminho da conta removidas); a cópia ORIGINAL intacta ao lado "
       "(com as credenciais; ir cifrada ao cofre é decisão do operador). ACHADO NOVO: iald.ia.br (Cloudflare) também responde `/x.php` "
       "com PHP/8.3.0 — sem credencial aqui; passos em `IALD_IA_BR_mesma_exposicao.md`. PENDENTE DO OPERADOR: na hospedagem, desligar o PHP "
       "do domínio (ou >= 8.3.36, ou atestação escrita do backport); trocar a senha do SFTP/SSH e passar à chave; o banco MySQL antigo "
       "(exportar e apagar, ou trocar a senha); iald.ia.br. Sessão do site: HSTS de 31536000 depois de um dia com falhas 0 "
       "(`testar_site_estatico_v2.sh --hsts-longo`). Rotas 1345–1347." % HT16)
PUB = ("CENTRAL PÚBLICA NA v396 (22/10/2026, noite): rodada INCREMENTAL pela mesma esteira (construtores derivados por trocas contadas que "
       "pulam o já visto e não mudado; mescla que não devolve nada excluído antes; conferência independente do delta, que roda o próprio "
       "conferidor no que difere do HEAD): central-publica `%s` (%d arquivos no índice), central-publica-work `%s` (%d), "
       "central-publica-bancada `%s` (%d); README com o pino v396 e o um.acom novo `%s` (88/88 conferidos; 0 identificador de terceiro; 0 "
       "dado pessoal); /central/ do site com o retrato v396 (1280 leituras) — subida `%s` verificada. Correções da esteira: a regra "
       "«^varredura_» pegava resultados científicos (16 voltaram: rito9 varredura_n.csv, VARREDURA_FONTE, VARREDURA_PALAVRAS, "
       "varredura_nos); as listas ja_vistos_ e git_add/rm ficam fora; os gerados da raiz (README, PATENTES, vínculo) protegidos na mescla; "
       "a pasta da auditoria de PHP inteira fora do público. A licença (source-available, a redação do the_boundary) fica como está, por "
       "decisão do operador: «A licença é como você falou mesmo, tudo certo»." % (heads["central-publica"][0], heads["central-publica"][1],
                                                                      heads["central-publica-work"][0], heads["central-publica-work"][1],
                                                                      heads["central-publica-bancada"][0], heads["central-publica-bancada"][1],
                                                                      ACOM16, SUB))
SITE = ("Site: os dados literais do selo (nota «Current seal», título do fechamento, contagens) estavam na v392 desde a custódia v392 — as "
        "custódias v393+v394 e v395 não rodaram `tools/atualizar_dados_selo_site.py`; passaram à v396. REGRA PARA A PRÓXIMA CUSTÓDIA: "
        "rodar `atualizar_dados_selo_site.py` (primeiro com --conferir) depois de gerar_portas e antes de aplicar_selo. O `.htaccess` do site "
        "agora traz o bloco IALD-SEGURANCA-ESTATICO (o subir_site o envia sempre): não tirar; a fase 2 do HSTS (31536000) vem depois de um "
        "dia com falhas 0.")

nova_mem = os.path.join(MEM, "php-site-e-wordpress-22out.md")
assert not os.path.exists(nova_mem), nova_mem
corpo = ("---\nname: php-site-e-wordpress-22out\ndescription: \"PHP (22/10/2026): o site estático da TGL entregava *.php ao PHP-FPM 8.3.0 "
         "(RCE do aviso php.net de 21/10) — bloqueado no .htaccess, https 301, cabeçalhos; backup do WordPress saneado; iald.ia.br com a "
         "mesma exposição; atos de hospedagem pendentes do operador\"\nmetadata:\n  type: project\n---\n\n# PHP — o site da TGL e o backup "
         "do WordPress (22/10/2026)\n\n" + PHP + "\n\n**Why:** a exposição era no ar (o PHP-FPM 8.3.0 recebia o pedido mesmo sem arquivo PHP); "
         "o backup trazia credenciais de um banco remoto em claro.\n\n**How to apply:** o bloco IALD-SEGURANCA-ESTATICO do `.htaccess` do "
         "site não se tira em custódia nenhuma; nunca testar conexão com a credencial antiga do banco; o que é da hospedagem (PHP, senha do "
         "SFTP, banco antigo, iald.ia.br) é ato do operador; a fase 2 do HSTS só depois de um dia com falhas 0.\n\nRelacionado: "
         "[[central-publica-22out]] · [[regra-do-backup-imediato]] · [[escritorio-miguel]]\n")
tmp = nova_mem + ".tmp_" + TS
open(tmp, "w", encoding="utf-8", newline="\n").write(corpo)
assert os.path.getsize(tmp) > 1000
os.replace(tmp, nova_mem)
print("ok (nova)", os.path.basename(nova_mem), os.path.getsize(nova_mem))

ap(os.path.join(MEM, "central-publica-22out.md"), "## %s — a Central pública na v396; a licença fica como está\n\n%s" % (AGORA, PUB))
ap(os.path.join(MEM, "site-sessao-estado.md"), "## %s — PHP bloqueado no .htaccess; dados do selo trazidos da v392\n\n%s\n\n%s" % (AGORA, PHP, SITE))
ap(r"C:\IALD\Site\tgl\v3.0_bancada\DIARIO_DO_SITE.md", "## %s — o PHP do servidor bloqueado; a Central pública na v396 (sessão a7 da Central)\n\n%s\n\n%s\n\n%s" % (AGORA, PHP, SITE, PUB))
ap(os.path.join(MEM, "MEMORY_2.md"), "## %s — PHP corrigido e a Central pública na v396 (sessão a7)\n\n%s\n\n%s" % (AGORA, PHP, PUB))
ap(CEN + r"\memory\TGL_ATLAS.md", "[%s — §X append (re-ancorado ao selo v396 `0a4395a89eeebbb7`): A CENTRAL PÚBLICA NA v396 E O PHP DO SITE] %s %s" % (AGORA, PUB, PHP))
M = os.path.join(MEM, "MEMORY.md")
t = open(M, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in t else "\n"
anc = [l for l in t.split(nl) if l.startswith("- [A CENTRAL ABERTA (22/10)](central-publica-22out.md)")]
assert len(anc) == 1, anc
linha = ("- [PHP do site e backup do WordPress (22/10)](php-site-e-wordpress-22out.md) — **.htaccess bloqueia *.php (PHP-FPM 8.3.0); https 301; "
         "backup saneado; iald.ia.br e hospedagem pendentes do operador**")
tocar(M, lambda t_, nl_: t_.replace(anc[0], anc[0] + nl_ + linha, 1))
assert os.path.getsize(M) < 24 * 1024, os.path.getsize(M)

rota = {"tipo": "ROTA", "rota_id": "iald.central.publica.v396_incremental", "dominio": "CUSTODIA",
        "titulo": "A Central pública alcança a v396 por rodada incremental (mesma esteira, conferência do delta)",
        "pergunta": "Como levar uma versão nova aos três repositórios públicos, ao /central/ e ao um.acom sem reconstruir 420 mil arquivos e sem afrouxar a conferência?",
        "dados": ["a Central privada (git ls-files), work/ e Chatgpt/", "os três preparos em C:\\IALD\\Central_publica"],
        "metodo": "construir_*_incremental.py (derivados por derivar_incrementais.py: pulam o já visto não mudado desde 22/10 00:00) -> "
                  "mesclar_incremento.py (nada excluído volta; gerados da raiz protegidos; work/php_e_v396_22out fora inteira) -> "
                  "atualizar_pasta_no_preparo.py (a esteira) -> gerar_readmes_publicos.py + indexar_raiz.py -> conferir_delta.py (o próprio "
                  "conferidor no que difere do HEAD) -> atualizar_repo_publico.py (índice exato no git, push sem força, árvore remota = índice); "
                  "refazer_retrato_v396.py + gerar_um_acom_publico.py + conferir_um_acom_publico.py + vincular + montar + subir_site.",
        "resultado": PUB, "veredito": "CENTRAL_PUBLICA_V396__TRES_REPOSITORIOS_E_SITE__DELTA_APROVADO__ARVORE_REMOTA_IGUAL_AO_INDICE",
        "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
        "defeito": "A regra «^varredura_» do construtor da região pegava resultados científicos (corrigida: só os prefixos das listas locais). "
                   "O histórico público ainda guarda o que foi corrigido à frente na abertura (decisão do operador).",
        "nao_refazer": "Para a próxima versão: rodar_incremental.py (com o DESDE da última rodada), conferir_delta.py, atualizar_repo_publico.py.",
        "proximo_passo": "Na v397: trocar o DESDE de rodar_incremental.py para a hora desta rodada; o resto igual.",
        "onde": WC,
        "artefatos": [WC + r"\mesclar_incremento.py", WC + r"\conferir_delta.py", WC + r"\atualizar_repo_publico.py",
                      WC + r"\varredura_conferencia_delta_central-publica.json", r"C:\IALD\Site\tgl\v3.0_bancada\central_publica\acom\um_acom_info.json"],
        "refs": ["iald.central.abertura_publica_22out", "custodia.v396", "seguranca.php.site_e_backup_wordpress_22out"],
        "nota": "Sessão a7 da Central (Claude), 22/10/2026."}
for k, v in rota.items():
    if isinstance(v, str):
        assert "CONFIRM" not in v.upper(), k
rp = os.path.join(W6, "rota_central_publica_v396.json")
open(rp, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", rp, "--quem", "claude-central-a7 (Central pública v396)"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("rota:", r.returncode, (r.stdout or r.stderr).strip().splitlines()[-2:])
print("REGISTRO FINAL OK:", heads, ACOM16, SUB, HT16)
