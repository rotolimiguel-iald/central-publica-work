def _v375_measure_trace_tracial_not_consumed():
    """MEDIDA desta rodada no kernel EMBUTIDO: toda ocorrencia de `X.trace_tracial` esta numa linha que DEFINE o mesmo campo de outro certificado
    em uma de DUAS formas exatas -- o repasse `trace_tracial := X.trace_tracial` (lightRealization, PhotonMassiveTransport) ou o transporte
    `trace_tracial := fun x y => by rw [X.trace_tracial]` (a renormalizacao `rescale` da v375, cuja 1a rodada do ensaio foi RECUSADA por esta medida
    ate a regra dizer isso; forma apertada por sugestao do aferidor: um consumidor disfarcado noutra forma nao passa) --, nunca um uso em prova. Qualquer outra ocorrencia (inclusive em
    comentario) = consumidor = ABERTO (fail-closed). `uses > 0` e exigido porque o
    repasse em lightRealization EXISTE (zero usos significaria que o arquivo embutido nao foi lido). A medida por texto nao ve campo aberto por
    `open`/`obtain`; o aferidor mediu no fecho em Lean (27/09): so repasse; ContinuousCoreData.trace_tracial com 0 usuarios."""
    import re as _re
    try:
        files = _EMBEDDED_KERNEL_FILES
    except NameError:
        return False, ["_EMBEDDED_KERNEL_FILES ausente"]
    uses, consumers = 0, []
    for rel, txt in files.items():
        if not rel.endswith(".lean"):
            continue
        for ln in txt.splitlines():
            # v394: an exact audit command reports dependencies, it is not a proof consumer.
            # Only a whole bare directive is excluded; comments/extra expressions still refuse.
            if _re.fullmatch(r"\s*#print\s+axioms\s+[\w.]+\.trace_tracial\s*", ln):
                continue
            for m in _re.finditer(r"\b[\w.]+\.trace_tracial\b", ln):
                uses += 1
                if not _re.match(r"^\s*trace_tracial\s*:=\s*(?:[\w.]+\.trace_tracial|fun x y => by rw \[[\w.]+\.trace_tracial\])\s*$", ln):
                    consumers.append("%s: %s" % (rel, ln.strip()[:120]))
    return (uses > 0 and not consumers), consumers