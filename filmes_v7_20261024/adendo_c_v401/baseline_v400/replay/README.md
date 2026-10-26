# Replay numérico V7 — integração

`startReplay(container, options)` em `../web/replay-panel.mjs` monta um botão independente. Importar/montar não carrega dados nem runtime. O clique inicia um worker Python; `destroy()` cancela e remove o painel. `replay-demo.html` é a página de teste isolada. Não há alteração em player, cenas ou fundo.

```js
import {startReplay} from './replay-panel.mjs';
const replay = startReplay(document.querySelector('#replay'), {onResult: result => console.log(result.status)});
// replay.destroy() ao desmontar a página.
```

Na raiz delivery_v7, com Python + NumPy locais:
```powershell
C:\Python314\python.exe -B replay/build_replay.py --source source/um.py --hud data/hud.json
C:\Python314\python.exe -B replay/test_replay.py
C:\Python314\python.exe -B replay/vendor_pyodide.py
C:\Python314\python.exe -m http.server 8000 --bind 127.0.0.1
```
Abra `http://127.0.0.1:8000/web/replay-demo.html`. Servir via localhost ou HTTPS (Web Crypto), com MIME WASM. Sem CDN em execução: somente arquivos do mesmo servidor. Para ensaio headless, execute `node replay/test_browser.cjs`, definindo `PLAYWRIGHT_MODULE` e, se necessário, `CHROMIUM_EXECUTABLE` para instalações existentes. Nada se instala globalmente.

O builder exige programa/core coerentes com o selo e identidade do HUD. Extrai bytes verbatim por AST, com linhas e offsets no manifesto. `um_nucleo_filme.py` contém dez funções principais (as oito do exportador, J e Powers), auxiliares e imports; `um_scalar_excerpt.py` conserva o bloco escalar indentado. O harness separado envolve esse bloco em `if True:`; não altera seus bytes. Nem browser nem builder importam o um.py completo. Flags de kernel não entram como resultados calculados: funções recebem dicionários vazios e só folhas numéricas selecionadas saem para a comparação. Textos/veredictos históricos não são renderizados.

34 âncoras são recalculadas contra o core selado, 27 também contra o HUD: 61 comparações. Os demais campos do HUD são explicitamente documentais, incluindo Einstein, gate, contagens formais e teste de natureza. Não se alega reproduzir os 64 checks do exportador ou executar Lean. Tolerâncias absolutas constam no manifesto; a da cadeia Powers é menor que o valor esperado para impedir que zero passe. A matemática citada é do kernel sob hipóteses; o replay mede sombras numéricas.

O painel verifica o manifesto pelo pin de `replay-trust.mjs`, depois recorte, escalares, runner, âncoras, HUD e worker; o worker verifica runtime e dependência. Alterar recorte/HUD ou faltar runtime resulta em NOT_SEALED. O pin do um.py é conferido no build e mostrado integralmente: o navegador não baixa os 38 MB do programa. Isso é integridade vinculada à entrega confiável, não assinatura contra alteração conjunta do servidor e dos pins. Após mudar fontes/HUD, reexecutar o builder e publicar junto o novo `replay-trust.mjs`.

Pyodide 0.27.7 + NumPy 2.0.2: 16.910.221 bytes no subconjunto, sem SciPy. `vendor_pyodide.py --download` repõe bytes oficiais somente se coincidirem com os hashes medidos. Referências: [distribuição](https://pyodide.org/en/0.27.7/usage/downloading-and-deploying.html), [worker](https://pyodide.org/en/0.27.7/usage/webworker.html). Tempos e resíduos medidos ficam em TEST_OFFLINE.json e TEST_BROWSER.json; não são benchmark mobile. A falha inicial de localização do Chromium foi preservada separadamente.

Integração e submissão/review_pending pertencem ao coordenador. O requisito C não modifica missão, Atlas, Nós, site ou espelho.

O controle adicional de WASM ausente expôs espera no carregador; o worker passou a verificar todos os arquivos antes de iniciar. O negativo está em TEST_BROWSER_R2_RUNTIME_MISSING_FAILURE.json; a correção passa no recibo final. Preserve web/, replay/ e data/ como diretórios irmãos na integração. A licença oficial distribuída está em PYODIDE_LICENSE.txt (NumPy inclui suas licenças no wheel).
