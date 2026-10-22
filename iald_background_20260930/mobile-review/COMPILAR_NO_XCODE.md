# Compilar o IALD no Xcode e instalar no iPhone

> Escrito em 12/09/2026, para o operador. Tudo que dava para ajustar a partir do
> Windows **já está ajustado** — este guia cobre só o que exige o Mac.

---

## O que já está pronto no projeto (não precisa mexer)

Conferido no `project.pbxproj` desta máquina:

| ajuste | valor |
|---|---|
| Bundle Identifier | `br.ia.IALD` — o mesmo do app 6760655636 |
| Team | `48DLBH89QY` |
| Assinatura | `Automatic` |
| Entitlements | `App/App.entitlements`, com `com.apple.developer.applesignin: ("Default")` |
| Versão | **4.1** |
| Build | **11** — a loja já tem a 4.0(10), e o número tem de subir |
| iOS mínimo | 15.0 (o seu iPhone 17 está muito acima) |
| Interface | embarcada em `ios/App/App/public`, com sha256 conferido |

---

## Caminho A — direto do seu Mac para o seu iPhone 17

É o caminho mais curto para **ver o app rodando**. Não envolve a App Store.

### 1. Levar a pasta para o Mac

Copie a pasta inteira `C:\IALD\projetos_pyhton\IALD\iald-app` para o Mac
(pendrive, rede ou nuvem). O que importa: `ios/`, `www/`, `node_modules/`,
`package.json` e `capacitor.config.json`.

### 2. Abrir

No Mac, abra **`ios/App/App.xcodeproj`** (duplo clique).

⚠ **Não procure `App.xcworkspace` nem `Podfile`: eles não existem de propósito.**
O Capacitor 8 usa Swift Package Manager em vez de CocoaPods — foi isso que
permitiu gerar o projeto no Windows. Na primeira abertura o Xcode vai baixar os
pacotes sozinho ("Resolving Package Graph"); espere terminar.

### 3. Conferir a assinatura

Clique no projeto **App** (topo da coluna esquerda) → alvo **App** → aba
**Signing & Capabilities**:

- **Automatically manage signing**: marcado
- **Team**: deve aparecer o seu (`48DLBH89QY`). Se aparecer vazio, escolha-o na
  lista. Se a lista estiver vazia: Xcode → Settings → Accounts → **+** → Apple ID.
- **Sign in with Apple**: deve aparecer como capability já listada. Se **não**
  aparecer, clique **+ Capability** e adicione — o arquivo de entitlements já
  está lá, é só o Xcode reconhecê-lo.

### 4. Rodar no iPhone 17

1. Ligue o iPhone no Mac por cabo e desbloqueie-o.
2. Na barra de cima do Xcode, onde diz o destino, escolha **o seu iPhone**.
3. **⌘R**.
4. Na primeira vez o iPhone recusa: **Ajustes → Geral → VPN e Gerenciamento de
   Dispositivo → Apple Development: (sua conta) → Confiar**. Depois rode de novo.

### 5. O que você deve ver

- A tela azul do portão, com o botão preto **"Entrar com a Apple"**.
- Ao tocar: o diálogo nativo da Apple.
- Depois: o chat.

⚠ **Sem o servidor pronto, a entrada falha** — e falha dizendo o motivo na tela.
Antes de testar, confirme os dois itens da seção "Antes de testar", mais abaixo.

---

## Caminho B — Xcode Cloud (compilar pela internet)

Serve para gerar a build que vai à App Store sem depender do Xcode local antigo.

⚠ **Exigência que hoje NÃO está satisfeita: o Xcode Cloud só compila a partir de
um repositório git** (GitHub, GitLab ou Bitbucket) ligado ao App Store Connect.
O `iald-app` não está em repositório nenhum — `git ls-files` sob `IALD/` devolve
**zero arquivos**.

Para usar este caminho seria preciso, antes:

1. Criar um repositório **privado** só para o `iald-app`.
2. ⚠ **Não subir junto**: `node_modules/`, `_backups_*/`, os `.bak_*`, e nada de
   `C:\IALD\projetos_pyhton\IALD\` fora da pasta do app — ali estão `.env`,
   `iald_users.json` e chaves. O `.gitignore` da pasta-mãe protege o servidor,
   mas um repositório novo começa sem proteção nenhuma.
3. No App Store Connect → aba **Xcode Cloud** → conectar o repositório e criar um
   workflow apontando para `ios/App/App.xcodeproj`, esquema **App**.

Se quiser seguir por aqui, me diga: eu preparo o `.gitignore` do repositório novo
e a lista exata do que entra.

---

## Antes de testar a entrada (senão o botão falha com razão)

Estes dois itens são do servidor, não do app:

1. **Criar o `.env`** — já criado em `C:\IALD\projetos_pyhton\IALD\.env` com
   `IALD_APPLE_BUNDLE_ID=br.ia.IALD`. ✅
2. **Reiniciar o web server.** O processo em execução ainda roda o código anterior
   a 11/09: sem reiniciar, não existem nem `/api/apple-signin`, nem a verificação
   do token, nem o CORS. Sem isso o portão vai dizer que o servidor recusou — e
   estará dizendo a verdade.
3. O túnel `demo.iald.ia.br` precisa estar no ar enquanto você testa no iPhone,
   porque o app fala com esse endereço, não com `localhost`.

---

## Se der errado

| sintoma | causa provável |
|---|---|
| "Signing for App requires a development team" | Team não escolhido na aba Signing |
| O botão da Apple não aparece / capability ausente | adicionar **+ Capability → Sign in with Apple** |
| Erro de pacote na abertura | espere o "Resolving Package Graph" terminar; depois File → Packages → Resolve |
| Portão diz "o servidor recusou a entrada" | falta reiniciar o web server, ou o `.env` não foi lido |
| Portão diz "não foi possível falar com o servidor" | túnel fora do ar |
| Avisos do plugin `apple-sign-in` | ele é declarado para Capacitor 7 e usamos o 8; **é aqui que se descobre se atrapalha** — me mande o texto do erro |

---

## O que ainda não foi provado

**Nada disto rodou num iPhone.** O projeto foi gerado e ajustado a partir do
Windows, a interface está embarcada com hash conferido, e o Android compila —
mas o fluxo nativo da Apple nunca foi executado. Escrito e empacotado não é o
mesmo que funcionando, e este guia existe para transformar um no outro.
