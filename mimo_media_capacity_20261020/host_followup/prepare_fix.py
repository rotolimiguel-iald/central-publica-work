"""Minimal diagnostic correction; preserve policy admission and science."""
import hashlib,json,difflib,ast
from pathlib import Path
HERE=Path(__file__).resolve().parent
LIVE=Path('C:/IALD/projetos_pyhton/IALD')
p=LIVE/'iald_web_server.py';raw=p.read_bytes();before=raw.decode();source=before.replace('\r\n','\n')
old="    except (MediaError,MediaBudgetError):\n        return _sse_aviso(private_media_host.PUBLIC_BUDGET_REFUSAL,'anexo_excede_contexto')"
new="""    except MediaBudgetError as exc:
        # Whitelisted local diagnosis only; never echo arbitrary exception data.
        if str(exc)=='Uncertain media policy; no automatic quality substitution':
            return _sse_aviso('O seletor não atingiu a confiança mínima para a política de mídia. Núcleo, histórico e anexo foram preservados. O seletor pode ter sido consultado; o anexo não foi enviado ao modelo executor. Nenhum reenvio automático.', 'politica_midia_incerta')
        return _sse_aviso('Anexo excede o contexto, bytes ou orçamento disponíveis; núcleo e histórico preservados. O seletor pode ter sido consultado; nada foi enviado ao modelo executor.', 'anexo_excede_contexto')
    except MediaError:
        return _sse_aviso('Não foi possível validar o anexo ou sua admissão; núcleo e histórico preservados. O seletor pode ter sido consultado; nada foi enviado ao modelo executor.', 'anexo_validacao_recusada')"""
assert source.count(old)==2
source=source.replace(old,new);ast.parse(source)
staged=source.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode()
(HERE/'iald_web_server.py').write_bytes(staged)
(HERE/'diagnostic.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),staged.decode().splitlines(True),fromfile='runtime/iald_web_server.py',tofile='staging/iald_web_server.py')),encoding='utf-8')
(HERE/'FIX_BASELINE.json').write_text(json.dumps(dict(source=str(p),sha256=hashlib.sha256(raw).hexdigest(),staged_sha256=hashlib.sha256(staged).hexdigest(),threshold_changed=False,policy_retry=False,scope='Diagnostic/UI correction only;0.68 decision still refuses under unchanged0.70 gate.'),indent=2),encoding='utf-8')
