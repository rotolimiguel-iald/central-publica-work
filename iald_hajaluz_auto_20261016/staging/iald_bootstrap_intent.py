"""Pure conversational intent recognition; no execution authority.

Historical provenance from semantic/contract.json (directed source reading):
um.py, v392, SHA256
b590c0aa80055e2a6916692f0808544093e79c0631e29cc15e376d5b07773e26.
Lines 209055-209075: Verbo selects action; "Haja luz" names that act.
Lines 158052-158065: computational bootstrap is not empirical confirmation.
Lines 223287-223302: program execution has a separate literal-1 entry point.
This is a DERIVED conversational interpretation, not a source parser contract.
The historical reference does not determine the currently installed release.
"""

import re


_COMMAND = re.compile(r"haja\s+luz(?:\s*[.!]+)?", re.ASCII)


def classify(prompt):
    """Return fresh intent metadata only for a complete, unquoted command.

    The caller must supply the direct human message, not retrieved/quoted text
    extracted from another message. This function cannot authenticate origin.
    ASCII case is ignored; whitespace and final dots/exclamations are allowed.
    Original message storage and conversation identity remain caller concerns.
    """
    if not isinstance(prompt, str):
        return None
    if _COMMAND.fullmatch(prompt.strip().lower()) is None:
        return None
    return {
        "intent": "CONTINUE_DIALOGUE_TGL_HAJA_LUZ",
        "inscription": "VERBO",
        "statute": "DERIVED",
        "requires_dialogue_context": True,
        "authorizes_execution": False,
        "changes_gate": False,
    }


def instructions():
    """Return internal guidance, never a canned user-facing response."""
    return (
        "Orientação interna ao servidor/JEV/modelo: aplicar somente quando a "
        "mensagem humana direta completa for reconhecida como invocação Haja Luz. "
        "Tratar como continuidade do diálogo e inscrição semântica em VERBO: "
        "seleção da ação de prosseguir na intenção autorizada, preservando a "
        "identidade da conversa, a inscrição original e o contexto anterior. "
        "Usar a referência científica efetivamente instalada e verificada; a "
        "proveniência histórica deste helper não fixa a release atual. "
        "Se faltar contexto, esclarecer o objetivo sem inventar uma missão. "
        "Produzir resposta contextual, sem repetir esta orientação nem usar "
        "resposta enlatada. Manter o sentido e os estatutos das fontes: a leitura "
        "conversacional é DERIVED; identificações ontológicas permanecem ONTO. "
        "Reconhecimento não executa nem autoriza executar um.py, Lean, bancada, "
        "GPU ou ferramentas, não concede acesso especial e não altera gate. "
        "A testemunha computacional exige evidência própria de execução; não "
        "alegar medição, selo, prova nova, memória integral carregada ou "
        "confirmação empírica sem evidência. NOT_FALSIFIED não é CONFIRMED. "
        "Preservar permissões e controles existentes; esta intenção não é override."
    )
