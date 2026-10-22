# -*- coding: utf-8 -*-
"""R2.1: implantacao_lib.py (9_R2_1) — nova tentativa em PermissionError, recibos pendentes, reinício pendente."""
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'implantacao_lib.py'
s = P.read_bytes().decode('utf-8')
assert '\r' not in s


def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:80], s.count(old))
    s = s.replace(old, new)


sub('''"""Biblioteca comum de implantar.py / reverter.py (conserto ACOM 12/10; R2 de 13/10). Só stdlib.''',
    '''"""Biblioteca comum de implantar.py / reverter.py (conserto ACOM 12/10; R2 e R2.1 de 13/10). Só stdlib.''')

sub('''    fora do job object do shell que rodou a ferramenta). Sem tarefa, o reinício usa Win32_Process.Create (WMI),
    também fora do job.
"""''', '''    fora do job object do shell que rodou a ferramenta). Sem tarefa, o reinício usa Win32_Process.Create (WMI),
    também fora do job.

R2.1 (revisão independente R2 de 13/10, achados K2, K3, K4, K6 e passo 8):
  * K6 — toda troca (os.replace) e remoção de tempário tem nova tentativa curta e LIMITADA em PermissionError
    (WinError 5/32: um leitor — antivírus, indexador, um operador abrindo o recibo — segura o arquivo sem
    FILE_SHARE_DELETE). Os recibos esperam até 30 s; os demais arquivos até 10 s. Depois, a falha sobe como antes.
  * K2 — recibos com carimbo (nunca sobrescritos) e `recibos_pendentes`: a implantação real anterior que mudou algo
    e não tem RECIBO_REVERSAO REVERTIDA correspondente bloqueia uma nova implantação (e indica o recibo a reverter).
  * passo 8 — `ReinicioPendente`: o comando de início foi aceito e há processo do app vivo, mas a saúde não chegou no
    prazo. Não é falha da implantação; o recibo diz «aguardando reinício» e manda conferir, não reverter.
  * `estado_real` — o recibo descreve a tarefa e os processos LIDOS, nunca presumidos.
"""''')

sub('''class ImplantacaoError(RuntimeError):
    pass
''', '''class ImplantacaoError(RuntimeError):
    pass


class ReinicioPendente(ImplantacaoError):
    """R2.1 (passo 8): o início foi aceito e há processo do app vivo, mas a saúde não chegou no prazo."""


RETRY_ARQUIVO_S = 10.0     # R2.1: espera máxima de uma troca de arquivo de código/backup
RETRY_RECIBO_S = 30.0      # R2.1: espera máxima de uma troca de recibo (um leitor pode segurá-lo por segundos)


def com_nova_tentativa(fn, *args, limite_s=RETRY_ARQUIVO_S, registro=None):
    """R2.1 (K6): chama fn(*args); em PermissionError (WinError 5 acesso negado / 32 violação de compartilhamento)
    espera 20 ms, dobrando até 500 ms, por no máximo `limite_s` segundos; depois a exceção sobe (falha visível).
    `registro` (lista), se dado, recebe uma linha por nova tentativa."""
    t0 = time.monotonic()
    espera = 0.02
    while True:
        try:
            return fn(*args)
        except PermissionError as exc:
            if time.monotonic() - t0 >= limite_s:
                raise
            if registro is not None and len(registro) < 50:
                registro.append({'op': getattr(fn, '__name__', str(fn)), 'erro': repr(exc)[:160],
                                 'apos_s': round(time.monotonic() - t0, 3)})
            time.sleep(espera)
            espera = min(espera * 2, 0.5)
''')

sub('''def write_bytes_atomic(dst, data):
    """tempário -> fsync -> conferência de bytes -> os.replace. Nunca open(dst, 'w') direto.

    R2: se a troca falhar (alvo somente-leitura, travado, sem permissão), o tempário — criado aqui e que nunca
    virou o arquivo — é removido e a exceção sobe com o nome do alvo; o alvo fica como estava.
    """
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + '.tmp_' + stamp())
    try:
        with open(tmp, 'xb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        if tmp.read_bytes() != data:
            raise ImplantacaoError('tempário divergente: %s' % dst)
        os.replace(tmp, dst)
    except BaseException:
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass
        raise
''', '''def write_bytes_atomic(dst, data, limite_s=RETRY_ARQUIVO_S):
    """tempário -> fsync -> conferência de bytes -> os.replace. Nunca open(dst, 'w') direto.

    R2: se a troca falhar (alvo somente-leitura, travado, sem permissão), o tempário — criado aqui e que nunca
    virou o arquivo — é removido e a exceção sobe com o nome do alvo; o alvo fica como estava.
    R2.1 (K6): a troca e a remoção do tempário têm nova tentativa curta e limitada em PermissionError.
    """
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + '.tmp_' + stamp())
    try:
        with open(tmp, 'xb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        if tmp.read_bytes() != data:
            raise ImplantacaoError('tempário divergente: %s' % dst)
        com_nova_tentativa(os.replace, tmp, dst, limite_s=limite_s)
    except BaseException:
        try:
            if tmp.exists():
                com_nova_tentativa(os.remove, tmp, limite_s=min(limite_s, 5.0))
        except OSError:
            pass
        raise
''')

sub('''    digest = h.hexdigest()
    if sha256_file(tmp) != digest:
        os.replace(tmp, dst.with_name(dst.name + '.mismatch'))
        raise ImplantacaoError('cópia divergente: %s' % dst)
    os.replace(tmp, dst)
    return {'path': str(dst), 'bytes': dst.stat().st_size, 'sha256': digest}''',
    '''    digest = h.hexdigest()
    if sha256_file(tmp) != digest:
        com_nova_tentativa(os.replace, tmp, dst.with_name(dst.name + '.mismatch'))
        raise ImplantacaoError('cópia divergente: %s' % dst)
    com_nova_tentativa(os.replace, tmp, dst)          # R2.1 (K6)
    return {'path': str(dst), 'bytes': dst.stat().st_size, 'sha256': digest}''')

sub('''    dest = path.with_name(path.name + '.' + sufixo + '_' + stamp())
    os.replace(path, dest)
    return dest''', '''    dest = path.with_name(path.name + '.' + sufixo + '_' + stamp())
    com_nova_tentativa(os.replace, path, dest)        # R2.1 (K6)
    return dest''')

sub('''def write_json_atomic(path, payload):
    write_bytes_atomic(path, (json.dumps(payload, ensure_ascii=False, indent=1, default=str) + '\\n').encode('utf-8'))
''', '''def write_json_atomic(path, payload, limite_s=RETRY_RECIBO_S):
    """Recibos e comandos: R2.1 (K6) — um leitor que segura o recibo por segundos não aborta mais a ferramenta."""
    write_bytes_atomic(path, (json.dumps(payload, ensure_ascii=False, indent=1, default=str) + '\\n').encode('utf-8'),
                       limite_s=limite_s)


def ler_json_com_nova_tentativa(path, limite_s=RETRY_RECIBO_S):
    return com_nova_tentativa(lambda: json.loads(Path(path).read_text(encoding='utf-8')), limite_s=limite_s)


# ============================================================================ R2.1: recibos pendentes (K2)
STATUS_REVERTIDO = ('REVERTIDA', 'REVERTIDA_AGUARDANDO_REINICIO')


def _impl_precisa_reverter(rec):
    """Uma implantação REAL precisa de reversão salvo se nada mudou: recusada, ou falhou sem mudança iniciada.
    EM_CURSO (morta no meio) e CONCLUIDA* precisam (estado desconhecido ou implantado)."""
    st = str(rec.get('status') or '')
    if st.startswith('RECUSADA'):
        return False
    if st.startswith('FALHOU_EM_') and not rec.get('mudancas_iniciadas'):
        return False
    return True


def recibos_pendentes(dirs):
    """R2.1 (K2): lista as implantações REAIS (não dry-run) que mudaram algo (ou cujo estado é desconhecido) e não
    têm RECIBO_REVERSAO real com status REVERTIDA* que as cite (por carimbo ou caminho). Recibo ilegível conta como
    pendente (fail-closed). Lê só JSON de recibo; nunca escreve."""
    impls, revertidos_stamp, revertidos_path, ilegiveis = [], set(), set(), []
    for d in dirs:
        d = Path(d)
        if not d.is_dir():
            continue
        for p in sorted(d.glob('RECIBO_REVERSAO*.json')):
            try:
                r = ler_json_com_nova_tentativa(p, limite_s=5.0)
            except (OSError, ValueError):
                continue                      # uma reversão ilegível não prova reversão
            if r.get('dry_run') or r.get('status') not in STATUS_REVERTIDO:
                continue
            if r.get('recibo_implantacao_stamp'):
                revertidos_stamp.add(r['recibo_implantacao_stamp'])
            if r.get('recibo_implantacao'):
                revertidos_path.add(os.path.normcase(os.path.abspath(r['recibo_implantacao'])))
        for p in sorted(d.glob('RECIBO_IMPLANTACAO*.json')):
            try:
                rec = ler_json_com_nova_tentativa(p, limite_s=5.0)
            except (OSError, ValueError) as exc:
                ilegiveis.append({'recibo': str(p), 'erro': repr(exc)[:200]})
                continue
            if rec.get('dry_run') or not _impl_precisa_reverter(rec):
                continue
            if rec.get('stamp') in revertidos_stamp or os.path.normcase(os.path.abspath(p)) in revertidos_path:
                continue
            impls.append({'recibo': str(p), 'stamp': rec.get('stamp'), 'status': rec.get('status'),
                          'mudancas_iniciadas': rec.get('mudancas_iniciadas'), 'iniciado_em': rec.get('iniciado_em')})
    return {'pendentes': impls, 'ilegiveis': ilegiveis}


def estado_real(backend):
    """R2.1: a tarefa e os processos LIDOS agora (o recibo nunca presume o estado). Erros de leitura são registrados."""
    if backend is None:
        return {'gerido': False}
    out = {'lido_em': now_iso()}
    try:
        t = backend.tarefa_ler()
        out['tarefa'] = {k: t.get(k) for k in ('existe', 'nome', 'estado', 'habilitada')}
    except Exception as exc:  # noqa: BLE001 - registrado
        out['tarefa_erro'] = repr(exc)[:300]
    try:
        p = backend.listar()
        out['processos'] = {'supervisores': len(p['supervisores']), 'web': len(p['web']), 'escutando': len(p['listen'])}
    except Exception as exc:  # noqa: BLE001
        out['processos_erro'] = repr(exc)[:300]
    return out
''')

# ProcessosSim._escrever_tarefa: a lib já tenta de novo; o laço do simulador fica (inofensivo)

# iniciar_app_gerido: distinguir «aguardando reinício» de «falha» (passo 8)
sub('''        time.sleep(1.0)
    reg.update({'ok': False, 'ultimo': ultimo})
    salvar()
    raise ImplantacaoError('o app não ficou saudável (1 supervisor + 1 web + saúde) em %ds' % esperar_s)
''', '''        time.sleep(1.0)
    reg.update({'ok': False, 'ultimo': ultimo})
    salvar()
    # R2.1 (passo 8): o comando de início FOI aceito (senão teria levantado acima). Se há processo do app vivo,
    # é um reinício lento, não uma falha da implantação: quem chama decide (nunca mandar reverter por isso).
    vivos = bool(ultimo) and (ultimo['procs']['supervisores'] or ultimo['procs']['web'])
    if vivos:
        reg['aguardando_reinicio'] = True
        salvar()
        raise ReinicioPendente('o início foi aceito e há processo do app vivo, mas a saúde (1 supervisor + 1 web + '
                               '/login) não chegou em %ds' % esperar_s)
    raise ImplantacaoError('o app não ficou saudável (1 supervisor + 1 web + saúde) em %ds' % esperar_s)
''')

# restaurar_tarefa: se e só se ESTA execução desabilitou (K3)
sub('''def restaurar_tarefa(backend, tarefa_antes, reg, salvar):
    """Só a TAREFA: reabilita se estava habilitada antes (usado quando nada mudou e o reinício falha)."""
    if tarefa_antes and tarefa_antes.get('existe') and tarefa_antes.get('habilitada'):
        if not backend.tarefa_ler().get('habilitada'):
            reg['tarefa_reabilitada'] = backend.tarefa_habilitar()
            salvar()
''', '''def restaurar_tarefa(backend, desabilitada_por_esta_execucao, reg, salvar):
    """Só a TAREFA. R2.1 (K3): reabilita SE E SÓ SE foi esta execução que a desabilitou (registrado no recibo como
    `tarefa_desabilitada_por_esta_execucao`); uma tarefa que o operador desabilitou nunca é reabilitada aqui.
    Devolve True se a tarefa ficou habilitada por esta chamada (ou já estava), False se nada foi feito."""
    if not desabilitada_por_esta_execucao:
        reg['tarefa_reabilitada'] = {'nota': 'não reabilitada: esta execução não a desabilitou'}
        salvar()
        return False
    if backend.tarefa_ler().get('habilitada'):
        reg['tarefa_reabilitada'] = {'nota': 'já estava habilitada'}
        salvar()
        return True
    reg['tarefa_reabilitada'] = backend.tarefa_habilitar()
    salvar()
    depois = backend.tarefa_ler()
    reg['tarefa_depois_de_reabilitar'] = {k: depois.get(k) for k in ('estado', 'habilitada')}
    salvar()
    if not depois.get('habilitada'):
        raise ImplantacaoError('Enable-ScheduledTask não deixou a tarefa habilitada')
    return True
''')

P.write_bytes(s.encode('utf-8'))
print('ok', P.stat().st_size)
