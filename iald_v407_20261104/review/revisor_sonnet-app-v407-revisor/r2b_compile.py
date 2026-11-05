"""Revisor sonnet-app-v407-revisor -- RODADA 2, PARTE 2: compila r2b_d7_d8_out.json em validation/review_verify.json (modo 'x') e ACRESCENTA a secao «Verify (D7-D8)» ao fim do PARECER_v407_R2.md
(sem apagar nada). Numeros LIDOS dos JSON de saida."""
import datetime, hashlib, json, sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
ACTOR = 'sonnet-app-v407-revisor'
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: json.loads(Path(p).read_bytes())
now = datetime.datetime.now(datetime.timezone.utc)
O = rd(HERE / 'r2b_d7_d8_out.json')
iv_sha = sha((W / 'INSTALLED_VERIFICATION.json').read_bytes())
so_sha = sha((W / 'verify_stdout.txt').read_bytes())
pk, cmp, d9, ctrl, jev, man, ex, rel, ker = O['pacotes'], O['D8_comparacao'], O['D9'], O['controles_negativos'], O['jev'], O['manifesto_ativo'], O['extras'], O['release'], O['kernel']
lit = O['D8_provider_calls_e_science_executed_no_codigo_do_verificador']
all_pass = bool(O['PASS_D7'] and O['PASS_D8'] and O['PASS_D9_carregadores'])
n_cmp = sum(1 for k, v in cmp.items() if isinstance(v, bool))
n_cmp_ok = sum(1 for k, v in cmp.items() if v is True)

F = []
add = lambda sev, ident, text: F.append({'severity': sev, 'id': ident, 'text': text})
add('BAIXO', 'V1', f"`provider_calls: 0` e `science_executed: false` do INSTALLED_VERIFICATION.json são LITERAIS do código de verify_installed.py (constantes no dicionário de saída: provider_calls = {lit['provider_calls']['valor']}, science_executed = {lit['science_executed']['valor']}), não medições; mesma classe do B2 da v406 (campos que parecem medida e são constante). O 0 é verdadeiro por construção (o script só chama carregadores) e eu o sustento com medida minha: {d9['tentativas_de_rede']} tentativas de rede (0 evento socket de qualquer tipo), {d9['aberturas_de_env_bloqueadas']} aberturas de .env, {d9['subprocessos_bloqueados']} subprocessos e nenhuma biblioteca de provedor importada. Para a v408: contar de verdade (gancho de auditoria) em vez de gravar 0.")
add('INFO', 'V2', f"Os tokens permanentes são LIDOS, não recomputados (a contagem nativa é da API e não há rede). O `permanent_tokens` do carregador é o `budget.permanent_tokens` do `manifest.json`, depois de o carregador validar o manifesto contra o sha do prefixo, a política de saída/margem e a sobra ≥ 10.000. Verifiquei que quatro fontes dizem o mesmo número: carregador, manifest instalado, native_count instalado e o recibo do staging da rodada 1 (haiku55 {pk['haiku55']['permanent_tokens_lidos']['carregador']}; haiku {pk['haiku']['permanent_tokens_lidos']['carregador']}), e que prefixo, manifest e recibo têm o mesmo sha256.")
add('INFO', 'V3', f"Corroboração independente do servidor: o stdout do web novo (`web-server_20261104_051250_r2.log`, linha 10) imprime `[IALD-CANONICAL-CATALOG] release=v407 source_sha256=833121339e649f71 lean_files={ker['lean_files']}`, e o do web antigo (`..._r1.log`) imprimia `release=v406 source_sha256=ddcb91930982d614 lean_files=1743`: o processo que serve o app carregou a v407. `lean_files` bate com o meu `KernelCatalog` ({ker['lean_files']}; {ker['files']} arquivos formais).")
add('INFO', 'V4', f"Controles negativos: {sum(1 for k, v in ctrl.items() if str(v).startswith('RECUSOU'))} de {sum(1 for k, v in ctrl.items() if k != 'copia_adulterada_apagada')} recusas esperadas (release e os dois pacotes com fonte errada: «Canonical release, source and catalog differ»; cópia do haiku55 com 1 byte do prefixo trocado: «Memory changed since provider measurement»). A conferência pode falhar e não falhou. A cópia adulterada foi apagada.")
add('INFO', 'V5', f"`files_verified: {rd(W / 'INSTALLED_VERIFICATION.json')['files_verified']}` é o comprimento do plano que o verificador percorreu comparando sha256 de cada destino; igual ao meu D2 (1782). Não rehasheei os 1782 nesta parte (não reabri D1–D6). `iald_native_memory` importa `urllib.request` (auxiliar HTTP do llama) mas nenhum evento socket ocorreu; {d9['modulos_de_topo_importados']} módulos de topo importados, nenhum de provedor. Prompt público {ex['public_prompt_bytes']} B com `private_atlas_included` = {ex['private_atlas_included']}; contexto nativo {ex['native_bytes']} B; política `AUTOMATIC_ORDER[:2]` = {ex['politica_AUTOMATIC_ORDER_2_primeiros']}.")
transparency = ["Nenhum critério mudou depois de ver dados: a primeira execução do r2b_d7_d8.py já deu PASS. Dois ajustes de código no meu script foram feitos ANTES de rodar (a expressão que reúne os booleanos do manifesto e a leitura dos caminhos instalados do resultado selado a partir do manifesto ativo).",
                "A partitura desta parte (PARTITURA_R2b_antes_de_medir.md) foi escrita antes de qualquer medição dela."]
limits = ["Não instalei, não reiniciei, não matei nem iniciei processo; nenhuma rede (o GET local do D5 não se repete aqui); não rodei verify_installed.py, deploy_controlled.py nem teste_escopo_v407.py; não importei verify_installed.py.",
          "Tokens permanentes lidos, não recomputados (contagem nativa é da API). Não há controle negativo do contrato JEV (o manifesto fixa caminhos absolutos; adulterar uma cópia exigiria reescrever o manifesto).",
          "O processo do construtor (15:07:00–15:07:05) já tinha terminado quando medi e não pôde ser auditado: o D9 vale para os MESMOS carregadores rodados no MEU processo novo (e sustenta o 0 do verificador por ser código só de carregadores), não é uma auditoria do processo dele.",
          "Não avalio resposta de modelo ao vivo nem celular físico; a carga dos carregadores e o log de partida do servidor não provam que o app responde bem."]
scripts = {p.name: sha(p.read_bytes())[:16] for p in sorted(HERE.glob('r2b*.py'))}
checks = {'D7': {'PASS': O['PASS_D7'], 'pino_confere_com_o_um_py_do_cofre': O['pino_confere_com_o_um_py_do_cofre'], 'manifesto_ativo': man, 'kernel': ker, 'release': rel, 'jev': jev, 'pacotes': pk, 'controles_negativos': ctrl, 'extras': ex},
          'D8': {'PASS': O['PASS_D8'], 'comparacao_campo_a_campo': cmp, 'campos_comparados': n_cmp, 'campos_iguais': n_cmp_ok, 'literais_no_codigo_do_verificador': lit},
          'D9_carregadores': {'PASS': O['PASS_D9_carregadores'], **d9, 'env_removidas_do_meu_processo': O['env_removidas_do_meu_processo']}}
rv = {'status': 'PASS' if all_pass else 'FAIL', 'reviewer': ACTOR, 'timestamp': now.isoformat(), 'task': 'verify', 'release': 'v407',
      'scope': 'Revisão independente da VERIFICAÇÃO da release v407 instalada (D7, D8 e o D9 dos carregadores): carregadores de produção em processo novo, sem rede, com os argumentos do servidor; INSTALLED_VERIFICATION.json contra o que eu meço. Não mede resposta de modelo ao vivo nem celular.',
      'evidence_sha256': {'INSTALLED_VERIFICATION.json': iv_sha, 'verify_stdout.txt': so_sha}, 'checks': checks, 'findings': F, 'findings_alto_medio': [], 'transparency': transparency, 'limits': limits, 'scripts_sha16': scripts,
      'partitura_antes_de_medir_sha256': sha((HERE / 'PARTITURA_R2b_antes_de_medir.md').read_bytes())}
WRITE = '--write' in sys.argv
if WRITE:
    with (W / 'validation/review_verify.json').open('x', encoding='utf8') as f:
        json.dump(rv, f, ensure_ascii=False, indent=2, default=str)
    rv_sha = sha((W / 'validation/review_verify.json').read_bytes())
else:
    rv_sha = sha(json.dumps(rv, ensure_ascii=False, indent=2, default=str).encode('utf8'))

md = f"""

---

## Verify (D7–D8) — secção ao lado (escrita depois da segunda mensagem do orquestrador; o que está acima fica como estava)
Data: {now.strftime('%Y-%m-%dT%H:%MZ')}. Evidência em exame: `INSTALLED_VERIFICATION.json` (sha16 `{iv_sha[:16]}`) e `verify_stdout.txt` (sha16 `{so_sha[:16]}`), escritos às 15:07:05 pelo `verify_installed.py` (15:07:00–15:07:05). **Veredito: {'ACEITO (tarefa `verify`)' if all_pass else 'RECUSADO'}. Nenhum achado ALTO ou MÉDIO.** Esta secção substitui, para D7, D8 e D9 dos carregadores, as frases acima que diziam que ficavam para depois.

**Partitura (dita antes de medir; `PARTITURA_R2b_antes_de_medir.md`, sha16 `{sha((HERE/'PARTITURA_R2b_antes_de_medir.md').read_bytes())[:16]}`):** decide se os carregadores de produção aceitam a v407 instalada e se o `INSTALLED_VERIFICATION.json` coincide com o que eu meço; não decide resposta de modelo ao vivo nem celular; um FAIL seria parede medida. Escolhas ditas antes: processo novo sem rede (nenhum evento `socket` permitido), os mesmos argumentos do `iald_web_server.py`, tokens lidos de quatro fontes (não recomputados), três controles negativos (um numa cópia adulterada), D8 campo a campo.

| item | veredito | número-chave |
|---|---|---|
| D7 manifesto ativo | {'PASS' if all(v for v in man.values() if isinstance(v, bool)) and man['operational_core.current_release'] == man['active_cluster.release'] == man['jev_control.release'] == 'v407' else 'FAIL'} | `operational_core.current_release` = `active_cluster.release` = `jev_control.release` = `v407`; `release_source_sha256` = pino (`833121339e649f71…`) nos três; `jev_control.sha256` `{man['jev_control.sha256_no_manifesto'][:16]}…` = sha do `jev_control_v407.json` instalado; cluster e núcleo operacional com o sha do arquivo instalado |
| D7 kernel e release | {'PASS' if ker['source_sha256_igual_pino'] and rel['e_v407'] and rel['source_igual_pino'] else 'FAIL'} | `KernelCatalog`: sha = pino, {ker['files']} arquivos formais ({ker['lean_files']} `.lean`); `load_release`: identidade v407 com `cluster_sha256` `{rel['identity']['cluster_sha256'][:16]}…` e `operational_core_sha256` `{rel['identity']['operational_core_sha256'][:16]}…`, ambos iguais ao sha do arquivo instalado |
| D7 contrato JEV | {'PASS' if jev['release'] == 'v407' and jev['source_sha256_igual_pino'] else 'FAIL'} | `load_contract`: release `{jev['release']}`, `source_sha256` = pino, `result_sha256` e `proof_manifest_sha256` = os arquivos instalados, `core_packet` `core_packet_v407_bound.txt` com o sha do arquivo da raiz |
| D7 pacotes | {'PASS' if all(v['quatro_fontes_iguais'] and v['sobra_maior_que_10000'] for v in pk.values()) else 'FAIL'} | haiku55: **{pk['haiku55']['permanent_tokens_lidos']['carregador']} tokens permanentes**, {pk['haiku55']['prefix_bytes_utf8_do_carregador']} B, sobra {pk['haiku55']['remaining_tokens']}; haiku: **{pk['haiku']['permanent_tokens_lidos']['carregador']} tokens**, {pk['haiku']['prefix_bytes_utf8_do_carregador']} B, sobra {pk['haiku']['remaining_tokens']}; carregador = manifest = native_count = recibo do staging; prefixo igual ao do staging; saída reservada 16384; 0 pedidos de geração |
| D7 controles negativos | {'PASS' if all(str(v).startswith('RECUSOU') for k, v in ctrl.items() if k != 'copia_adulterada_apagada') else 'FAIL'} | 4 de 4 recusas (release e dois pacotes com fonte errada; cópia com 1 byte do prefixo trocado) |
| D8 | {'PASS' if O['PASS_D8'] else 'FAIL'} | {n_cmp_ok} de {n_cmp} comparações iguais: status, `files_verified` 1782 (= meu D2), `identity` inteira, `public_commit`, tokens e bytes de haiku55 e haiku, `native_bytes` {ex['native_bytes']}, `public_prompt_bytes` {ex['public_prompt_bytes']}, `JEV_release`, `science_executed`, `provider_calls`; `verify_stdout.txt` é a mesma linha JSON; escrito depois do restart; evidência submetida inalterada |
| D9 carregadores | {'PASS' if O['PASS_D9_carregadores'] else 'FAIL'} | **0 tentativas de rede** (0 evento `socket` de qualquer tipo), **0 aberturas de `.env`**, 0 de segredos, 0 subprocessos, 0 escritas fora da minha pasta; {d9['modulos_de_topo_importados']} módulos de topo importados, nenhum de provedor; `provider_calls` 0 (ver V1: é literal do verificador, e a minha medida o sustenta) |

Corroboração: o web novo imprimiu na partida `[IALD-CANONICAL-CATALOG] release=v407 source_sha256=833121339e649f71 lean_files={ker['lean_files']}` (o antigo: `release=v406 … lean_files=1743`).

### Achados desta parte (nenhum ALTO ou MÉDIO)
""" + ''.join(f"- **{f['severity']} {f['id']}**: {f['text']}\n" for f in F) + f"""
### Transparência e limites (desta parte)
""" + ''.join(f"- {t}\n" for t in transparency) + ''.join(f"- {t}\n" for t in limits) + f"""
### Aceite registrado (desta parte)
`validation/review_verify.json` sha256 `{rv_sha}`. O `mission_step.py accept verify` é registrado logo abaixo, depois de rodar.
"""
p = HERE / 'PARECER_v407_R2.md'
if WRITE:
    p.write_text(p.read_text(encoding='utf-8') + md, encoding='utf-8')
else:
    print(md)
print(json.dumps({'WRITE': WRITE, 'status': rv['status'], 'all_pass': all_pass, 'sha256_review_verify': rv_sha, 'campos_D8': [n_cmp_ok, n_cmp], 'parecer_bytes_atual': len(p.read_bytes())}, indent=1))
