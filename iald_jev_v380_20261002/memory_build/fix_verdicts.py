from pathlib import Path
B=Path(__file__).resolve().parent
p=B/'haiku_codec.py';s=p.read_text(encoding='utf-8')
a="r'statute|status|estatuto|scope|escopo|hypothes|hip[oó]tes|not_claimed|not_said'"
b="r'statute|status|estatuto|scope|escopo|hypothes|hip[oó]tes|not_claimed|not_said|verdict|veredit'"
assert s.count(a)==2;s=s.replace(a,b);t=p.with_suffix('.tmp');t.write_bytes(s.encode());t.replace(p)
p=B/'test_local_stage.py';s=p.read_text(encoding='utf-8')
a="        self.assertEqual(len(receipt['topic_json_roundtrips']),362)"
b="""        json_topics={row['topic'] for row in receipt['topic_json_roundtrips']}
        def bodies(text):
            return {block.split('\\n',1)[0]:block.split('\\n',1)[1] for block in text.split(codec.MARKER)[0].split('\\n### ')[1:] if block.split('\\n',1)[0] in self.source['core']}
        old=bodies(original);new=bodies(fitted)
        for name in set(old)-json_topics:
            restored=new[name]
            for long,short in fit.ALIASES.items():restored=restored.replace(short,long)
            self.assertEqual(restored,old[name],name)
        self.assertEqual(len(json_topics)+len(set(old)-json_topics),362)"""
assert a in s;s=s.replace(a,b)
a="            for location,value in fields.items():self.assertTrue(codec.is_represented(location,value,seen),location)"
b=a+"""
            if name=='bancada_fases_5_6_7_v380':
                for suffix in ('/fase6/veredito_principal','/emenda_v4/vereditos_todos','/emenda_v5/vereditos_todos_DEC'):
                    location=pointer+suffix
                    self.assertTrue(codec.is_represented(location,codec.resolve(self.source,location),seen),location)"""
s=s.replace(a,b);t=p.with_suffix('.tmp');t.write_bytes(s.encode());t.replace(p)
print('Verdict containers kept whole; explicit three-path regression added')