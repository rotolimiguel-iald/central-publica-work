"""Staging helpers; caller retains existing auth, CSRF, generation and job guards.

Not installed or wired to Flask. No cache, base, dispatch or network operation.
"""
import chat_wire_codec as wire

def session_capabilities(original):
    return {**original,'transport':wire.capabilities()}

def decode_before_submit(raw,parsed,authenticated_scope,has_new_audio_video):
    if not isinstance(parsed,dict) or 'iald_transport' not in parsed:
        return parsed # Existing legacy admission remains exactly in caller.
    _,payload=wire.decode_request(raw,authenticated_scope)
    # Existing before_request media policy cannot inspect compressed messages.
    wire.need(not has_new_audio_video(payload),'new_audio_video_blocked',415)
    return payload

def encode_existing_page(raw,authenticated_scope,job_id,after,opt_in):
    if opt_in!=wire.QUERY:return raw
    return wire.page_candidate(raw,authenticated_scope,
        dict(kind='page',job_id=job_id,after=after))
