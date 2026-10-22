"""Host task/media partitions for new ledger records; no payload retention.

Media counts cover all user/assistant content actually sent, including history.
Text-only followups to old attachments therefore remain media-bearing requests.
Counts are a partition, not a workload/quality benchmark. Unknown shapes refuse
classification; provider attachment validation and consent remain separate.
"""
import re
import iald_task_policy as task_policy

VERSION = 'resolved_history_media_cost_v4_20261020'
KINDS = ('image', 'audio', 'video')
PARTS = {'image_url':'image', 'input_audio':'audio', 'video_url':'video'}


def partition(media=None, *, multimodal=False):
    """Accept request_media's host summary; never store URLs or encoded bytes."""
    if type(multimodal) is not bool:
        raise ValueError('Host-owned multimodal flag required')
    if media is None:
        # Legacy bool remains supported but cannot establish exact media counts.
        return None if multimodal else dict.fromkeys(KINDS, 0)
    if type(media) is not dict or type(media.get('counts')) is not dict:
        raise ValueError('Host media summary required')
    counts = media['counts']
    if set(counts) != set(KINDS) or any(type(n) is not int or n < 0 for n in counts.values()):
        raise ValueError('Invalid host media counts')
    kinds = media.get('kinds')
    if (type(kinds) is not list or any(type(k) is not str for k in kinds) or len(set(kinds)) != len(kinds)
            or set(kinds) != {k for k in KINDS if counts[k]}):
        raise ValueError('Inconsistent host media kinds/counts')
    return {k:counts[k] for k in KINDS}


def category(text, counts):
    # Mixed input uses the richest media task; the full counts still partition it.
    if counts is None:return 'image_analysis'  # Legacy image flag; no comparison.
    for kind in ('video', 'audio', 'image'):
        if counts[kind]:return kind+'_analysis'
    return task_policy.classify(text)


def summarize(messages):
    """Same media scope as request_media: all user/assistant message parts."""
    if type(messages) is not list:raise ValueError('Message list required')
    counts = dict.fromkeys(KINDS, 0)
    prompt = None
    for message in messages:
        if type(message) is not dict:raise ValueError('Invalid message')
        if message.get('role') not in ('user', 'assistant'):continue
        content = message.get('content')
        if type(content) is str:text = content
        elif type(content) is list:
            texts = []
            for part in content:
                if type(part) is not dict:raise ValueError('Invalid part')
                kind = part.get('type')
                if kind == 'text':
                    if type(part.get('text')) is not str:raise ValueError('Invalid text')
                    texts.append(part['text'])
                elif kind in ('iald_media','iald_media_ref'):
                    if part.get('kind') not in KINDS:raise ValueError('Invalid typed media kind')
                    counts[part['kind']] += 1
                elif kind in PARTS:
                    field = 'data' if kind == 'input_audio' else 'url'
                    obj = part.get(kind)
                    if type(obj) is not dict or type(obj.get(field)) is not str:
                        raise ValueError('Invalid media reference')
                    counts[PARTS[kind]] += 1
                else:raise ValueError('Unsupported message part')
            text = '\n'.join(texts)
        else:raise ValueError('Unsupported message content')
        if message['role'] == 'user':
            prompt = re.sub(r'\[ARQUIVO:[^\n]*\][\s\S]*?\[FIM\]', '', text).strip()
    if prompt is None:raise ValueError('Missing current user')
    return prompt, counts


def stamp(record, messages, *, media_plan=None):
    if type(record) is not dict:raise ValueError('Transport record required')
    try:
        text, counts = summarize(messages)
        if not text and not any(counts.values()):raise ValueError('Empty current user')
    except (ValueError, TypeError):
        record.update(task=None, task_source='unclassified_message_shape',
                      modality_class=None, modality_counts=None)
        return record
    record.update(task=category(text, counts), task_source=VERSION,
                  task_classification='host_lexical_not_quality',
                  modality_class='+'.join(k for k in KINDS if counts[k]) or 'text',
                  modality_counts=counts)
    if any(counts.values()):
        record['efficiency_comparison']='excluded_until_duration_resolution_frame_classes_are_controlled'
        if media_plan is not None:
            import iald_media_budget
            view=iald_media_budget.routing_options({'selected':media_plan})['selected']
            record['media_cost_profile']=view
    return record
