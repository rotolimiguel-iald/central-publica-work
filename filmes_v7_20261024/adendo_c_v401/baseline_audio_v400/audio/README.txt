ORDEM 022 / requisito D / codex-video-audio
Estado: preparação local, candidata à revisão do coordenador. ZERO envio TTS nesta entrega.
Não executar narrate.js ou interactive_v5/narrate_v5.cjs: reutilizamos seu motor msedge-tts,
formato Edge, vozes e montagem FFmpeg, preservando os arquivos anteriores.

ENTRADAS (todas em delivery_v7):
data/hud.json: items[{id,value}], extra{...}, seal_version, seal_pin, seal_timestamp.
Duplicação items/extra só é aceita se os valores forem iguais. Nunca ler/renderizar verdict,
console, textos históricos ou registros completos. Decimais são formatados a partir do HUD.
data/film1.json: {total_seconds:144,scenes:[{start,duration,end?,key?},...]} — 9 cenas; referência provisória16s cada.
data/film2.json: {duration:240,chapters:[{start,duration,end?,key?},...]} — 10 capítulos; referência provisória24s cada.
A associação de templates às cenas/capítulos é POSICIONAL; source_key preserva a chave original.
A ordem semântica precisa ser conferida pelo coordenador antes de executar o plano.
Os arquivos de filme não são alterados. O builder não importa nem executa um.py.

CAMPOS HUD UTILIZADOS:
omega_I, half, S_boundary, beta, theta_M, pol, id_true, ray_count,
proof_ladder_clean, proof_ladder_total, formal_count, declaration_count,
flags, flags_computed, flags_literal, z_disc, p_disc, z_delta, threshold_sigma.
Metadados do selo são incluídos no plano; a versão e o pin permanecem no HUD.
seal_pin e seal_timestamp ficam para o cartão do renderer, sem pronunciar hashes.
A relação z_disc<threshold_sigma é conferida; mudança exige revisar a prosa.
z_disc/p_disc/threshold_sigma ficam na MESMA cue; o renderer deve mantê-los no MESMO quadro.
H₁/H₂/H₃ são identificadores de hipóteses, não valores medidos.
Fórmulas de solda, J, Clausius e spin são explicadas em prosa e remetem ao HUD visual.
A Pêntada é implicação sob hipóteses; contagens não substituem validação dos teoremas.
Os títulos EN são propostas, não aceite do operador.

COMANDOS (C:\Python314\python.exe -B -X utf8):
audio/build_narration.py self-test
audio/build_narration.py plan
audio/build_narration.py build
audio/build_narration.py build --tts --approved-plan-sha256 HASH_EXATO_DO_PLANO
--root permite caminho explícito para delivery_v7; --node e --ffmpeg aceitam executáveis locais.
plan imprime o texto final em quatro idiomas e seus pinos, sem escrita e sem rede.
build sem --tts gera apenas timelines/legendas planejadas, marcadas PLANNED_NO_AUDIO.
O coordenador revisa plan e aprova seu hash antes da chamada com --tts. O hash inclui
HUD, templates, builder e ambos os filmes; alteração de bytes invalida o aceite antigo.
O parâmetro é um controle operacional local, não autenticação de identidade humana.
Somente textos finais EN/PT-BR são enviados ao motor Edge, nunca fontes completas.
Dependências reutilizadas: ../node_modules/msedge-tts e @ffmpeg-installer/ffmpeg.
Não há instalação automática de dependências nem seleção de outro provedor.

SAÍDAS DA EXECUÇÃO FUTURA PELO COORDENADOR:
data/film1_narration_timeline.json; data/film2_narration_timeline.json.
subs/filmeN/{en,pt-BR,fr,zh-Hans}.vtt; subs/filmeN/chapters.vtt.
subs/filmeN/sync-en/*.vtt e sync-pt-BR/*.vtt: as quatro traduções para cada trilha.
Padrão: en/fr/zh-Hans acompanham EN; pt-BR acompanha PT-BR.
audio/filmN/{en,pt-BR}.wav e .m4a; audio/NARRATION_BUILD.json.
Entrega proposta: duas trilhas separadas por filme; o coordenador multiplexa ou produz
MP4 por idioma. Este builder não escreve os vídeos.
As legendas futuras têm tempo exato de cada enunciado TTS, não alinhamento por palavra.
Sem TTS os tempos são proporcionais ao texto e não representam voz já medida.
A narração começa após0,3s; reserva0,3s no final. Sem sobreposição, música ou atempo.
Fala longa recusa: revisar texto ou contrato de cena e obter novo aceite, sem cortar a voz.
Loudnorm em duas passagens para−16 LUFS; WAV e AAC medidos novamente, tolerância±1 LUFS.
A existência do código não prova a loudness nem a duração de uma voz ainda não sintetizada.

IDEMPOTÊNCIA:
audio/cache/{sha256(voz,texto,rate,formato)}.json/.mp3/.wav.
Intenção exclusiva e fsync ANTES de criar transporte; timeout/erro => uncertain.
intent/uncertain/arquivo órfão/pino divergente bloqueiam, sem retry e sem fallback.
Cache completed é reutilizado somente após hash; não apagar recibos para repetir.
Resultado incerto exige reconciliação humana documentada. Áudio recebido e custodiado
pode ser reutilizado após falha local de mixagem. Um BUILDING residual é execução incompleta.
Não executar builds concorrentes no mesmo destino.
Esta preparação não move review_pending, não submete nem aceita o requisito D.

REVISÃO R2 — NARRAÇÃO EXPLICATIVA
ONTO/INPUT breves na abertura; alcance/natureza no fim. Transporte, garganta e spin
explicam as mudanças visuais. Capítulo9: H1 traço/gap, H2 coframe/Lorentz,
H3 horizonte/Clausius, composição da Pêntada; escada falada uma vez.
formal_count/declaration_count/proof_ladder_total ficam apenas no HUD, fora da fala
e das legendas que a acompanham. Stdout V7-C continua sob o renderer do coordenador.
formats.beta=.3f e theta_M=.1f: arredondamento da fala e das legendas correspondentes.
O HUD original permanece intacto. Todos os valores são derivados dos campos reais.
Tempos são os dos JSON do coordenador;144/240 são provisórios. Durações positivas,
continuidade e totais coerentes são exigidos; capítulos ampliados, inclusive36s,
são aceitos sem acelerar a voz. Se scenes e chapters coexistem, atualizar AMBOS.
speech_budget em cada segmento estima130–165unidades faladas/min, com expansão
numérica heurística e margens; NÃO é duração medida de Edge nem comando de velocidade.
O pino muda quando dados, tempos, builder ou templates mudam. A trava é operacional
do coordenador; a autorização de Edge já está no escopo. Nesta revisão somente
build PLANNED sem rede; síntese só após a entrega do plano final revisado.

REPARO DE DIAGNÓSTICO — TENTATIVA INICIAL INCERTA
O primeiro recibo conserva ValueError, sem stderr histórico, MP3 ou request_id.
Reprodução offline do código anterior alcançou a barreira de rede bloqueada.
Isso não permite concluir que a tentativa histórica falhou antes da conexão.
A unidade incerta permanece intocada; não apagar, renomear ou trocar sua chave.
O reparo registra fases em cache/*.transport.jsonl com fsync, incluindo o request_id
real antes de ws.send; stderr/returncode e eventual áudio recebido ficam custodiados
em *.diagnostic.json / *.received.mp3. Esses arquivos não autorizam retry.
Os eventos distinguem intenção de conexão, metadados prontos, intenção de envio,
enfileiramento local e retorno de áudio; enfileiramento não é aceite remoto.
O plano aprovado anterior continua preservado no recibo. Como o builder mudou,
o hash técnico derivado muda; não executar o novo plano enquanto a unidade anterior
estiver incerta. Não houve envio remoto nesta investigação.

RETOMADA EXPLÍCITA AUTORIZADA — SUPORTE PREPARADO, RESPOSTA HUMANA PENDENTE
CLI: build --tts --approved-plan-sha256 HASH --retry-authorization ARQUIVO
O coordenador cria ARQUIVO somente após receber a resposta humana autêntica.
Nenhum arquivo de autorização real foi criado por esta preparação.
Contrato JSON:
schema: iald.edge.retry-authorization.v1
decision: APPROVED; human_response_received: true
destination: Microsoft Edge TTS
uncertain_key: chave SHA256 exata da unidade antiga
new_attempt_id: UUID novo, canônico, fixo para retomadas desta tentativa
voice / text_sha256: os mesmos do recibo incerto e da fala pública do plano
original_receipt_sha256: SHA256 dos bytes do JSON antigo, sem modificar esse JSON
approved_plan_sha256: hash do plano com o builder atual
human_response_source: {path: caminho da resposta humana, sha256: SHA256 dos bytes}
O documento operacional não autentica sozinho um humano: origem e decisão reais
cabem ao coordenador. PENDING/ausência de resposta/hash rompido recusam antes de rede.
A autorização vale para UMA chave; outras unidades incertas continuam bloqueadas.
Nova tentativa em audio/cache/attempts/CHAVE/UUID/CHAVE.{json,mp3,wav}.
O original fica intacto e seu MP3 continua ausente; nenhum rename ou reabertura.
Um vínculo exclusivo authorization_SHA_DA_RESPOSTA.json fixa a evidência ao UUID.
A mesma evidência não permite trocar UUID para repetir uma tentativa incerta.
Completed é reutilizado por hash nessa pasta; intent/uncertain voltam a recusar.
Novo áudio recebido não muda o estatuto histórico da tentativa anterior.
Sem fallback, sem retry automático, sem execução de rede durante esta preparação.
Não reaproveitar exemplos sintéticos dos testes como autorização.


COMPATIBILIDADE EDGE v399 (somente preparo offline)
Cliente base msedge-tts 2.0.7 preservado. Adapter em memoria no builder usa GEC v2 do upstream edge-tts, com destino speech.platform.bing.com e vozes originais. Sem reconnect automatico. Nao e SDK oficial Microsoft; fontes oficiais dos projetos comunitarios. Nenhuma fala de teste transmitida.
Fonte: https://raw.githubusercontent.com/rany2/edge-tts/master/src/edge_tts/drm.py
SHA256: b29c37e2a0c11284adb2a1ffc04f0f231e1ba2d921494a912797218b05d64c4a
Mudanca local: somente extracao das funcoes/constantes puras e timestamp runtime local. Vetor upstream 2026-10-13T10:40:00Z verificado offline.
PR: https://github.com/rany2/edge-tts/pull/492
Licenca do trecho upstream (LGPLv3) segue integralmente; fonte legivel incluida no builder:
The MIT license is used for 'src/edge_tts/srt_composer.py' only. All
remaining files are licensed under the LGPLv3.

-----------------------------------------------------------------------

The MIT License

Copyright (c) 2014-2023 Christopher Down
Copyright (c) 2025- rany <[dado pessoal removido]>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

-----------------------------------------------------------------------

                   GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.


  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

  0. Additional Definitions.

  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

       0) Convey the Minimal Corresponding Source under the terms of this
       License, and the Corresponding Application Code in a form
       suitable for, and under terms that permit, the user to
       recombine or relink the Application with a modified version of
       the Linked Version to produce a modified Combined Work, in the
       manner specified by section 6 of the GNU GPL for conveying
       Corresponding Source.

       1) Use a suitable shared library mechanism for linking with the
       Library.  A suitable mechanism is one that (a) uses at run time
       a copy of the Library already present on the user's computer
       system, and (b) will operate properly with a modified version
       of the Library that is interface-compatible with the Linked
       Version.

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.


BOUNDED RETRY / CACHE ONLY
Reconstrucao sem rede ou arquivo de aprovacao: build --cache-only --node "C:\Program Files\nodejs\node.exe". Reutiliza caches completos por hash voz/texto inclusive filhos de tentativas; ausencias ficam pendentes.
Execucao autorizada: build --tts --approved-plan-sha256 <SHA> --bounded-retry-authorization <arquivo humano>. Ate duas novas tentativas por fala falha, persistidas em slots exclusivos; retomada nao renova limite. Sucessos sao reutilizados, pendentes nao impedem coleta das demais falas.
Autorizacoes, cache, recibos e logs sao privados operacionais: nao incluir no manifesto/publicacao dos filmes.


CONTRATO FINAL DO RECIBO PARA MAKE
O campo tts registra o modo de execucao, nao a existencia de audio nem uma contagem de chamadas. --cache-only termina COMPLETED/tts=false com audio real AUDIO_MEASURED; --tts pode reutilizar tudo sem enviar.
Aceitar somente COMPLETED, pending vazio, tts_inflight=false, reports dos dois filmes AUDIO_MEASURED e timelines AUDIO_MEASURED ligadas ao mesmo plan_sha256 vigente. Verificar WAV via loudness[idioma].sha256, AAC via loudness[idioma].aac.sha256, duracao total_seconds e LUFS em after.input_i/aac.measurement.input_i. PLANNED_NO_AUDIO e loudness vazio nao sao audio medido.
A chave de cache vincula voz/texto/rate/formato; validar state=completed, text_sha256 e audio_sha256. Resolver filhos de attempts/bounded sem exigir aprovacao para reutilizacao. Teste sem subprocessos/aprovacoes:60 unidades,51 raiz+9 filhas. Reconstrucao cache-only anterior manteve todos os recibos de cache identicos. Evidencia em AUDIO_PREPARATION.json/final_receipt_contract.
