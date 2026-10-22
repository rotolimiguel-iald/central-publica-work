"""Derive explicit V6 builder/verifier from the reviewed V5 implementation."""
from pathlib import Path
W=Path(__file__).resolve().parent
builder=(W/'integrate_topic_v5.py').read_text(encoding='utf-8')
builder=builder.replace("haiku_reviewed_topics_v4_20260922_134657_144992.md", "haiku_reviewed_topics_v5_20260922_140931_709157.md")
builder=builder.replace('topic_v5_positive23_20260922_140741_509336.json','topic_v6_review_20260922_141358_247824.json')
builder=builder.replace('topic_compaction_v5','topic_compaction_v6').replace('haiku_reviewed_topics_v5_', 'haiku_reviewed_topics_v6_')
# Restore the parent filename after replacing the output prefix.
builder=builder.replace('haiku_reviewed_topics_v6_20260922_140931_709157.md','haiku_reviewed_topics_v5_20260922_140931_709157.md')
verifier=(W/'verify_topic_v5_draft.py').read_text(encoding='utf-8')
verifier=verifier.replace("get('topic_compaction_v4')", "get('topic_compaction_v5')")
verifier=verifier.replace("W/'topic_capsules_v5'", "W/'topic_capsules_v6'").replace('TOPIC_V5_VERIFIED','TOPIC_V6_VERIFIED')
for name,text in [('integrate_topic_v6.py',builder),('verify_topic_v6_draft.py',verifier)]:
    with (W/name).open('x',encoding='utf-8')as f:f.write(text)
