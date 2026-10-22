# -*- coding: utf-8 -*-
"""Adversarial and realistic inputs for the D4 content scanner (R2, review finding 2). ~1 MB each."""
import json

B = chr(92)


def listing(n):
    paths = [B.join(['C:', 'IALD', 'projetos_pyhton', 'IALD', 'files', 'arquivo_%05d.txt' % i]) for i in range(n)]
    return json.dumps({'tool': 'listdir', 'result': paths}, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def inputs(size=1_000_000):
    def rep(unit):
        return unit * max(1, size // len(unit))
    cases = {
        # review A, E7 / E7b
        'E7_drive_letters': rep('a:/'),
        'E7_drive_path_deep': 'c:/' + rep('pasta/') + 'x',
        'E7_words_colon': rep('ab:/cd '),
        'E7b_listing_json_16000': listing(16000),
        # review B, F
        'F_many_drive_prefixes': rep('c:' + B + 'a'),
        'F_deep_path': 'c:' + rep(B + 'ab'),
        'F_slashes': rep('/a'),
        # every rule, near-miss families
        'key_pem_hyphen_words': rep('a-'),
        'key_pem_hyphen_runs': rep('-' * 1000 + '.ke'),
        'openai_short_runs': rep('sk-abc '),
        'openai_chain': rep('sk-'),
        'google_near': rep('AIza-'),
        'github_near': rep('ghp_x '),
        'slack_near': rep('xoxb-1 '),
        'bearer_near': rep('bearer abc '),
        'bearer_spaces': 'bearer' + ' ' * size,
        'dotenv_near': rep(' .env.a/'),
        'dotenv_chain': rep('/.env'),
        'unc_chain': rep(B + B + 'srv' + B),
        'percent_chain': rep('%5c%2f'),
        'escritori_near': rep('/escritori'),
        'accents': rep('é/'),
        'plain_text': rep('texto comum da memoria '),
    }
    return cases
