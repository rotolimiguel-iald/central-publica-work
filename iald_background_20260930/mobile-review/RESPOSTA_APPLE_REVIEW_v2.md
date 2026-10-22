# Resposta à App Review — submissão após a reprovação de 23/03/2026

> **Preparado em 11/09/2026.** Substitui o `RESPOSTA_APPLE_REVIEW.md` de 19/03,
> que respondeu bem às diretrizes 5.1.1(ii) e 2.1(b) mas não previu a 3.1.1.

---

## ⚠ LEIA ANTES DE ENVIAR — esta parte NÃO se cola no App Store Connect

**Esta carta descreve um build que ainda não existe.** Enviá-la antes de o app
novo estar compilado e submetido torna cada frase dela falsa, e a terceira
reprovação viria por credibilidade — que é bem pior que uma reprovação técnica.

**Só envie depois que TODAS estas condições forem verdade:**

| # | Condição | Estado em 12/09/2026 |
|---|---|---|
| 1 | O app não tem nenhuma tela de cadastro | ✅ **o app novo é outro projeto**: Capacitor, sem `InterestFormView` nem `PendingApprovalView`. Os arquivos de março continuam em `IOS_entregas_marco_2026/`, mas não são mais o que se compila |
| 2 | O app entra direto por Sign in with Apple (`/api/apple-signin`) | ✅ servidor testado (24/24 + verificação do `identityToken`) e **tela escrita e ligada** (plugin `@capacitor-community/apple-sign-in` 7.1.0, embarcada nas duas plataformas com sha conferido) — ⚠ **nunca executada num iPhone de verdade**: só um build no Xcode prova o fluxo nativo |
| 3 | O web server foi **reiniciado** (o processo em execução roda o código antigo) | ❌ ato do operador |
| 4 | O app declara `iald_surface: "app"` e não recebe `request_contract` | ✅ testado (21 → 20 ferramentas) |
| 5 | O prompt do app não tem tabela de preços | ✅ variante gerada e conferida (−138 caracteres) |
| 6 | O `Info.plist` não tem `NSMicrophoneUsageDescription` nem `NSSpeechRecognitionUsageDescription` | ✅ **medido no projeto novo**: o `Info.plist` não declara **chave de permissão alguma** — nem microfone, nem voz, nem câmera. A 5.1.1(ii) não tem como reincidir |
| 7 | Build novo enviado e selecionado no App Store Connect | ❌ — lembre que o próximo build precisa de número **maior que 10** |

**Estado do projeto iOS em 12/09/2026** (criado nesta máquina, Windows):
`ios/App/App.xcodeproj` existe, `PRODUCT_BUNDLE_IDENTIFIER = br.ia.IALD` nas duas
configurações, e a interface está embarcada em `ios/App/App/public` com sha256 idêntico
ao da fonte. O Capacitor 8 usa **Swift Package Manager**, não CocoaPods — por isso não há
`Podfile` nem `.xcworkspace`, e por isso o esqueleto pôde ser gerado fora do macOS.
Abrir `ios/App/App.xcodeproj` no Xcode (ou apontar o Xcode Cloud para ele) é o caminho.

**Também confirme no App Store Connect** (o PDF de 16/03 mostrava estes campos
em falta, e eles barram a submissão antes de qualquer revisor olhar): categoria
primária, classificação etária, URL da política de privacidade e **URL de
suporte** (este estava em vermelho).

### Fatos medidos no App Store Connect — 12/09/2026

Lidos da própria ficha da compilação. Não adivinhe nenhum destes de novo:

| campo | valor |
|---|---|
| ID do pacote (bundle ID) | **`br.ia.IALD`** — com `IALD` em maiúsculas |
| application-identifier | `48DLBH89QY.br.ia.IALD` |
| Team ID | `48DLBH89QY` |
| Versão / build | **4.0 (10)**, carregada em 19/03/2026 16:04, estado "Validado" |
| Sign in with Apple | `com.apple.developer.applesignin: ("Default")` — **já provisionado** |
| iOS mínimo | 17.0 · arm64 · iPhone e iPad |
| App Store Connect | app ID `6760655636` |

Três consequências:

1. **O próximo build precisa de número maior que 10** (ou uma versão nova).
2. **O projeto Capacitor declara `br.ia.iald.app`, que é outro identificador.**
   Para o iOS ele tem de ser `br.ia.IALD`; caso contrário o envio cria um
   aplicativo diferente em vez de atualizar o 6760655636. O Android está
   construído sob `br.ia.iald.app` e nada foi publicado lá, então alinhar é
   barato — mas é mudança de identidade e depende da palavra do operador.
3. A capability de Sign in with Apple **já existe** no App ID: não há trabalho
   no portal da Apple para habilitá-la.

**Como compilar:** o passo a passo está em `COMPILAR_NO_XCODE.md`, ao lado deste
arquivo. O projeto já vai com Team `48DLBH89QY`, entitlement de Sign in with Apple,
versão **4.1** e build **11** — só falta o Mac.

**Nas notas para o revisor (App Review Information), escreva:** que não é mais
necessária credencial de demonstração — basta o revisor tocar "Sign in with
Apple" e ele entra direto. E garanta que o túnel `demo.iald.ia.br` esteja no ar
durante todo o período de revisão, com o modelo carregado.

---

## ═══ COPIE DAQUI PARA BAIXO ═══

Hello,

Thank you for the detailed feedback. We have made structural changes to the app
rather than cosmetic ones. Below is a point-by-point response.

### Guideline 3.1.1 — Business — Payments — In-App Purchase

**We removed the account registration feature entirely.**

The app no longer contains any registration or application form. It no longer
asks for — and no longer stores — company name, job title, institution, or any
other business or organizational information. There is no application step, no
manual approval step, and no "waiting for approval" screen.

Authentication is now Sign in with Apple only, and it grants immediate access:
the user signs in and is taken directly into the app. Nothing is requested from
the user beyond the Apple ID itself.

In the same change we removed two other commercial surfaces that were present in
the previous build:

1. **In-chat contract request.** The assistant previously exposed a function
   that let a user register a formal request for a commercial license (company
   name, tax ID, legal representative, license type). That function is no longer
   available to the app.
2. **Pricing information.** The assistant's instructions previously contained
   our licensing rates. Those lines were removed from the instruction set used
   by the app, so the assistant cannot quote prices or commercial terms.

The app now contains no commercial offer, no price, no license selection, and no
way to initiate a business relationship. It is a free demonstration of the
technology.

### Guideline 2.1(b) — Information Needed

Our answers from the previous submission remain accurate, and we want to add one
correction about the review experience itself.

There are no paid features, no subscriptions, no in-app purchases, and no
external purchase mechanisms in the app. The app is free for everyone and
unlocks nothing that is paid. IALD LTDA's revenue comes from business-to-business
licensing of server technology, negotiated entirely outside the app through
direct contracts, and the app no longer references that business in any way.

**Correction regarding the previous review:** in the build reviewed on March 23,
access required manual approval by us, which means the reviewer could not
actually use the app after signing in. That was our mistake and it is now fixed —
access is immediate and unconditional. The reviewer can sign in with Apple and
use every feature of the app right away, with no credentials from us.

### Guideline 5.1.1(ii) — Legal — Privacy — Purpose Strings

All microphone and speech recognition functionality has been removed from the
app. The `NSMicrophoneUsageDescription` and `NSSpeechRecognitionUsageDescription`
keys have been removed from `Info.plist`. The app requests no protected resources
that require a purpose string for these capabilities.

### Note on the in-app usage meter

So the reviewer is not surprised by it: the app shows a screen labelled "usage
credits". This is an internal meter of how much the assistant has generated for
that user, computed from the number of tokens produced. It is not a currency and
is not represented as one:

- it cannot be purchased, sold, redeemed, transferred out of the app, or
  converted into money;
- it unlocks no feature, content, or capability whatsoever — the app behaves
  identically at any value;
- there is no mining, no blockchain, and no distributed ledger of any kind;
- the screen itself states, in the user's language, that the credits have no
  monetary value.

It exists to make the cost of computation visible to the user, which is the
subject our technology addresses.

### Summary of changes in this submission

- Removed the account registration form and all collection of business or
  organizational data
- Removed manual access approval; Sign in with Apple now grants immediate access
- Removed the in-chat commercial contract request function
- Removed licensing prices from the assistant's instructions
- Removed all microphone and speech recognition functionality and permissions
- No paid features, no in-app purchases, no subscriptions, no external purchase
  mechanisms
- Privacy policy linked from within the app

We appreciate the review team's time and are happy to provide any further detail.

IALD LTDA
