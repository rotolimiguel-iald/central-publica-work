from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'TRANSFERENCIA_DELTA_PARA_E5_080_20260910'
OUT.mkdir(exist_ok=False)
sources = [
 ROOT / 'GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md',
 ROOT / 'REVISAO_GERACAO_WEYL_080_20260910_044142_861011/PARECER_GERACAO_NATURAL_WEYL_E4_080.md',
 ROOT / 'LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md',
 ROOT / 'RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md',
 ROOT / 'FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md']

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

before = [pin(path) for path in sources]
note = r'''# Transferência da liberdade de levantamento para o primeiro diferencial em E5

10/09/2026. [DERIVED — prova algébrica escrita; depende da geração E4 da080 no alcance fixado]. Sem CAS, Lean ou execução/importação de um.py. Nenhum arquivo anterior alterado.

**Resultado:** no complexo métrico natural da referência espaço-forma fixada da080,

\[
\boxed{\delta(\mathcal K)=\operatorname{im}\bigl(d_1:H^3(\mathcal A_5,s_0)\longrightarrow H^4(\mathcal A_6,s_0)\bigr).}
\tag{1}
\]

Portanto a pergunta079 sobre outra classe que preserve o líder cúbico é precisamente

\[
\boxed{-[A_6]\in\operatorname{im}d_1|_{E=5}?}
\tag{2}
\]

O lema identifica o mapa a calcular. Não calcula sua imagem, não afirma que todo seu domínio seja finito e não estabelece o cancelamento ou uma obstrução universal.

## 1. Objetos e hipóteses

Seja A_E o espaço de zeroformas de valência E, com ordem finita de jatos por elemento e os coeficientes da [nota de geração080](<C:/IALD/Central de Patentes/Chatgpt/GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md>). Fixam-se dimensão quatro, orientação, referência espaço-forma com K>0, κ não nulo e matéria constante já projetada ao complexo métrico com seus escalares herdados. Não se acrescentam tensores espectadores nem se varia K num anel universal restrito.

O BRST formal s=s0+s1+s2+... tem ghost1, com sj aumentando a valência em j; s²=0. A completação é por valência, não uma permissão de jatos infinitos dentro de um coeficiente. Defina F^n=∏_(E≥n)A_E e C_N=A/F^(N+1). Então F^n é estável por s e

\[
0\longrightarrow (\mathcal A_6,s_0)\longrightarrow (C_6,s)\longrightarrow(C_5,s)\longrightarrow0
\tag{3}
\]

é uma sequência exata de complexos. As projeções de cochains são sobrejetivas por truncamento; nenhuma afirmação sobre sobrejetividade de cohomologias é usada.

Ponha

\[
\mathcal K=\ker\{H^3(C_5,s)\to H^3(C_3,s)\}.
\tag{4}
\]

δ:H³(C5)→H⁴(A6,s0) é a conexão de (3): levanta-se um ciclo a C6, aplica-se s e toma-se a classe da componente E6. A troca do levantamento acrescenta uma fronteira s0, portanto δ está bem definida.

Usamos o resultado080 já submetido à [revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_GERACAO_WEYL_080_20260910_044142_861011/PARECER_GERACAO_NATURAL_WEYL_E4_080.md>):

\[
\ker\{d_1:H^3(\mathcal A_4,s_0)\to H^4(\mathcal A_5,s_0)\}=0.
\tag{5}
\]

O operador d1 é induzido por s1. A identidade s0s1+s1s0=0, extraída de s² na primeira diferença de valência, garante que ele leva ciclos a ciclos e fronteiras a fronteiras. O sinal na última afirmação é s1s0v=−s0s1v.

## 2. Toda classe de K admite representante fechado que começa em E5

Seja [b]∈K. A imagem de b em C3 é uma fronteira. Escolha uma primitiva a em C3 e um levantamento finito em C5; substitua b por b−sa. A nova classe é a mesma e suas componentes até E3 são zero. Ela se escreve b4+b5. Essa escolha não precisa ser canônica nem uma seção linear uniforme: basta a primitiva da classe em exame. Naturalidade e ordem finita estão na própria definição de fronteira no complexo usado.

As componentes E4 e E5 de s(b4+b5)=0 em C5 são

\[
s_0b_4=0,\qquad s_0b_5+s_1b_4=0.
\tag{6}
\]

A segunda dá d1[b4]=0. Por (5), b4=s0v4 para algum v4 natural de ghost2 e valência quatro. Subtraindo sv4 em C5 obtém-se somente

\[
\widetilde b_5=b_5-s_1v_4,
\qquad
s_0\widetilde b_5=s_0b_5+s_1s_0v_4=-s_1b_4+s_1b_4=0.
\tag{7}
\]

O termo s2v4 pertence a E6 e desaparece apenas no truncamento C5. Ele NÃO foi declarado zero nem descartado numa equação de C6. A conexão δ não depende da escolha de levantamento; ao trabalhar em C6, essa mudança reaparece como a correspondente correção de E6.

## 3. A aplicação sobrejetiva e a identidade das imagens

Um ciclo z5 de s0 determina um ciclo em C5: todos os sjz5 com j≥1 ficam acima da valência máxima desse truncamento. Uma fronteira z5=s0v5 é também sv5 em C5. Assim a inclusão define

\[
q:H^3(\mathcal A_5,s_0)\longrightarrow H^3(C_5,s),\quad [z_5]\mapsto[z_5].
\tag{8}
\]

Sua imagem está em K, pois z5 projeta a zero em C3. O §2 prova que todo elemento de K vem de algum [z5]; logo im q=K. Não se afirmou que q seja injetiva: fronteiras que envolvem ordens inferiores podem identificar classes distintas de A5.

Levante z5 a C6 sem acrescentar componente E6. Como s0z5=0,

\[
\delta q[z_5]=[(sz_5)_6]=[s_1z_5]=d_1[z_5].
\tag{9}
\]

De im q=K e (9) segue (1). Não é preciso conhecer ker q ou escolher uma cisão de q. Se q[z5]=0, a mesma identidade automaticamente implica d1[z5]=0; isso não equivale a uma descrição completa de ker d1.

## 4. Necessidade e suficiência exatas para ESTE passo C5→C6

Seja T≤5 a classe particular da [nota078](<C:/IALD/Central de Patentes/Chatgpt/RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md>). Seu resíduo r6=(sT≤5)_6 satisfaz [r6]=[A6], não nulo no teste. Qualquer outra classe com a mesma imagem em H³(C3) difere de [T≤5] por K. Pela sequência exata (3), essa classe prolonga a C6 se e somente se sua imagem por δ é zero. Usando (1), isso equivale a (2).

Em representantes, caso exista z5 com s0z5=0 e [s1z5]=−[A6], há uma zeroforma finita a6 tal que

\[
r_6+s_1z_5=s_0a_6.
\]

Então

\[
T_{\le5}+z_5-a_6
\tag{10}
\]

é fechado em C6. Esse é um certificado CONDICIONAL de construção, com sinal explícito. Reciprocamente, qualquer prolongamento com o mesmo líder fornece a classe z5 pelo §2 e satisfaz (2).

Essa equivalência é apenas para o próximo truncamento e na categoria fixada. Mesmo um resultado positivo em (2) não provaria prolongamento a todas as valências, convergência, QME, admissibilidade causal ou uma teoria quântica completa.

## 5. O detector ímpar é compatível com a passagem ao quociente

O [funcional079](<C:/IALD/Central de Patentes/Chatgpt/FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md>) satisfaz Lk(s0a6)=0 e Lk(A6)=−4k/z0. Portanto descende a uma aplicação linear ℓk:H⁴(A6,s0)→Rher e

\[
\ell_k\circ d_1:H^3(\mathcal A_5,s_0)\to R_{\rm her}
\tag{11}
\]

é bem definida. Se z5 muda por s0v5, s1z5 muda por −s0s1v5 e o valor de (11) permanece igual. Logo não se depende de um representante particular para testar a condição necessária

\[
(\ell_k\circ d_1)[z_5]=+4k/z_0.
\tag{12}
\]

Toda z5 tem espécies h²C³ e h*C⁴, com jatos. A079 anula a contribuição direta da segunda espécie em (11), mesmo sem fechamento isolado. Entretanto a primeira ainda precisa ser s0-fechada em conjunto com a segunda. Esta nota não elimina antifields de todas as classes, não classifica H³(A5) e não declara (12) suficiente para (2).

## 6. Pendência precisa

O próximo trabalho é calcular a imagem de d1 em E5 no mesmo domínio, ou construir um funcional que anule TODA essa imagem e permaneça não nulo sobre [A6]. Mostrar (12) apenas para alguns candidatos, enumerar até uma ordem escolhida ou trocar o anel não resolveria essa obrigação. A investigação081 de representantes quadráticos fica separada desta entrega080.

Este lema usa somente truncamentos finitos de valência e a redução080 demonstrada. Não supõe Mittag-Leffler, não intercambia limite inverso e cohomologia, não usa testes de natureza e não altera o gate. O objetivo de reconstrução geral pelos mesmos dados selecionados e de setor quântico interagente continua aberto.
'''
note_pin = emit(OUT / 'IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md', note.encode('utf-8'))
after = [pin(path) for path in sources]
assert before == after
manifest = {'created_utc': datetime.now(timezone.utc).isoformat(),
 'status': 'WRITTEN_ALGEBRAIC_PROOF_AWAITING_INDEPENDENT_REVIEW',
 'sources_before': before, 'sources_after': after, 'all_sources_unchanged': before == after,
 'note': note_pin, 'writer': pin(Path(__file__)), 'new_cas_controls': 0, 'new_lean_compilations': 0,
 'originals_written': False, 'um_executed_or_imported': False,
 'scope': 'Equality delta(K)=image(d1 at E5), conditioned on the fixed-category E4 injectivity. No determination of that image.'}
manifest_pin = emit(OUT / 'MANIFESTO_TRANSFERENCIA_080.json',
 (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'note': note_pin, 'manifest': manifest_pin}, ensure_ascii=True))
