from pathlib import Path
S=Path(__file__).parent/'stage'
def edit(name,old,new,count=1):
 p=S/name;t=p.read_text(encoding='utf-8');assert t.count(old)==count,(name,old[:80],t.count(old));p.write_text(t.replace(old,new),encoding='utf-8')
edit('iald_app_spend.py','    def settle(self, measured):', '''    def discard_undispatched(self):
        """Only for a locally rejected request whose transport never started."""
        with self._lock:
            if self.pending is not None:
                self.guard.settle(self.pending['key'],amount=0)
                self.pending=None

    def settle(self, measured):''')
edit('iald_app_providers.py',"                if authorize is not None:authorize()\n                response = (http_post or requests.post)", "                if authorize is not None:\n                    try:authorize()\n                    except Exception:\n                        record['calls'][-1]['status']='not_dispatched'\n                        if spending is not None:spending.discard_undispatched()\n                        raise\n                response = (http_post or requests.post)")
s='iald_web_server.py'
edit(s,"    dispatch_check = dispatch_check or _dispatch_guard(user,motor,False)\n    try:dispatch_check()\n    except PermissionError:return _sse_aviso('Acesso ou consentimento revogado.','motor_indisponivel')\n    claude =", "    dispatch_check = dispatch_check or _dispatch_guard(user,motor,False)\n    claude =")
edit(s,'    soltar = []           # o que devolver no fim:',"    try:dispatch_check()\n    except PermissionError:return _sse_aviso('Acesso ou consentimento revogado.','motor_indisponivel')\n    soltar = []           # o que devolver no fim:")
edit(s,"    if any(iald_motores.consentiu(registro,key) for key in providers):return router_consent\n    for key", "    if any(iald_motores.consentiu(registro,key) for key in providers):return router_consent\n    if _nativa_automatica_pronta() and MODERACAO_LIGADA:\n        return _consentimento_do_motor(registro,'openai')\n    for key")
edit(s,"                                          verificar_payload=lambda _:dispatch_check(), task_control=", "                                          verificar_payload=lambda _:_check_reserved_dispatch(dispatch_check,conta), task_control=")
edit(s,"                            def fazer():\n                                dispatch_check()", "                            def fazer():\n                                _check_reserved_dispatch(dispatch_check,conta)")
edit(s,"                    conta.iniciar_chamada(payload)\n                    response, decision = post_guarded", "                    conta.iniciar_chamada(payload)\n                    _check_reserved_dispatch(dispatch_check,conta)\n                    response, decision = post_guarded")
helper='''def _check_reserved_dispatch(check,account):
    try:check()
    except Exception:
        # This check is strictly before the transport. Never use it to erase
        # a hold after a request has started or an upstream result is uncertain.
        account.descartar_ultima_chamada()
        raise


'''
edit(s,'def _dispatch_guard(user,executor,automatic):',helper+'def _dispatch_guard(user,executor,automatic):')
print('Final review corrections staged')
