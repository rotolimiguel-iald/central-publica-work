from pathlib import Path
import json,hashlib,ast
W=Path(__file__).parent;R=Path(r"C:\IALD\projetos_pyhton\IALD")
s=W/"server_stage";s.mkdir(exist_ok=True)
original=(R/"iald_web_server.py").read_bytes();text=original.decode("utf-8");sep="\r\n" if "\r\n" in text else "\n"
def replace(old,new,count=1):
 global text
 old=old.replace("\n",sep);new=new.replace("\n",sep)
 assert text.count(old)==count,(old[:100],text.count(old),count)
 text=text.replace(old,new)
helper="""def _mimo_media_limits(registro, user, automatic=False):
    # Capability display never grants permission or transmits attachments.
    eligible = app_providers.allowed(registro, user, 'mimo')
    if automatic:
        eligible = eligible and app_router.allowed(registro,user)
    authorized = eligible and iald_motores.consentiu(registro,'mimo')
    limits = app_router.limits() if automatic else app_providers.limits('mimo',media_authorized=authorized)
    if eligible:
        from iald_mimo_multimodal import media_capabilities
        capabilities = media_capabilities()
        # Local attachment selection is allowed before consent; transmission
        # below still requires the current per-provider versioned acceptance.
        limits.update(imagens=True, audio=capabilities['audio'],
                      video=capabilities['video'], media_capabilities=capabilities)
    else:
        limits.update(imagens=False,audio=False,video=False)
    return limits


"""
replace('def _consentimento_automatico(registro,user):',helper+'def _consentimento_automatico(registro,user):')
replace("        app_providers.wire_messages(client,'routing_validation')", """        media = app_providers.request_media(client)
        has_media = bool(media['kinds'])
        if has_media:
            if not app_providers.allowed(registro,user,'mimo'):
                return _sse_aviso('MiMo não autorizado para estes anexos. Nada foi enviado.','recurso_indisponivel')
            media_consent = _consentimento_do_motor(registro,'mimo')
            if not media_consent['dado']:
                return _sse_aviso('Leia e aceite o aviso do MiMo para enviar estes anexos.','consentimento_ia',
                    dict(versao=media_consent['versao'],provedor=media_consent['provedor'],detalhe=media_consent['texto']))
        app_providers.wire_messages(client,'routing_validation',provider='mimo' if has_media else None,
            images_authorized=has_media,media_authorized=has_media)""")
replace("""        chosen,receipt=app_router.choose(client[-1]['content'],candidates,operator_context=operator_context,
            model_ids={key:candidate_models[key] for key in candidates if key in candidate_models})""", """        routing_prompt = media['prompt'] or ('Analise o anexo enviado.' if has_media else '')
        chosen,receipt=app_router.choose(routing_prompt,candidates,operator_context=operator_context,
            model_ids={key:candidate_models[key] for key in candidates if key in candidate_models},
            multimodal=has_media,media=media,media_integrated=has_media)""")
replace(r"        messages = app_providers.wire_messages(client, prefix, note + ('\nUSER CONTEXT:\n'+profile if profile else ''))", r"""        messages = app_providers.wire_messages(client, prefix, note + ('\nUSER CONTEXT:\n'+profile if profile else ''),
            provider=motor,images_authorized=(motor=='mimo' and consent['dado']),
            media_authorized=(motor=='mimo' and consent['dado']))""")
replace("            decision = iald_motores.moderar_textos([profile]+[m['content'] for m in messages[1:]],", r"""            # Moderate textual parts only; inline media stays with the consented MiMo executor.
            moderation_text = [m['content'] if isinstance(m['content'],str) else '\n'.join(
                part['text'] for part in m['content'] if part.get('type')=='text') for m in messages[1:]]
            decision = iald_motores.moderar_textos([profile]+moderation_text,""")
replace("memory_sha256=memoria_info.get('context_sha256'))", "memory_sha256=memoria_info.get('context_sha256'),messages=req_json.get('messages'))")
replace("resposta.response = APP_EVALUATION.observe(resposta.response, modelo)", "resposta.response = APP_EVALUATION.observe(resposta.response, modelo, messages=(request.get_json(silent=True) or {}).get('messages'))")
replace("limites=app_router.limits(),", "limites=_mimo_media_limits(registro,username,automatic=True),")
replace("limites=app_providers.limits(motor), consentimento=", "limites=(_mimo_media_limits(registro,username) if motor=='mimo' else app_providers.limits(motor)), consentimento=")
ast.parse(text)
(s/'iald_web_server.py').write_bytes(text.encode())
(s/'server_baseline.json').write_bytes(json.dumps(dict(destination=str(R/'iald_web_server.py'),baseline=hashlib.sha256(original).hexdigest(),source=str(s/'iald_web_server.py')),indent=2).encode())
print('SERVER_STAGED')
