from pathlib import Path
from datetime import datetime
B=Path(__file__).resolve().parent;p=B/'test_provider_budget_context.py';raw=p.read_bytes();s=raw.decode()
s=s.replace('import iald_kernel,iald_core_indexado,iald_fontes_publicas,iald_task_session,iald_task_artifacts','import iald_kernel,iald_core_indexado,iald_fontes_publicas,iald_task_session,iald_task_artifacts,iald_motores\nfrom claude_haiku_messages import assemble as assemble_haiku')
s=s.replace("tree=ast.parse(SERVER.read_bytes())", "SERVER_RAW=SERVER.read_bytes()\ntree=ast.parse(SERVER_RAW)\nROUTING_INSTRUCTION='DIRETIVA_SINTETICA_JEV: preserve hipóteses e estatutos; responda sem task_scope.'\n\ndef routing_note(name,variable,scope=None):\n    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)\n    expected=ast.parse(f\"if routing_instruction and task_scope is None: {variable} += '\\\\n'+routing_instruction\").body[0]\n    nodes=[n for n in ast.walk(function) if isinstance(n,ast.If) and ast.dump(n,include_attributes=False)==ast.dump(expected,include_attributes=False)]\n    assert len(nodes)==1\n    ns={variable:'BASE_SERVICE_NOTE', 'routing_instruction':ROUTING_INSTRUCTION,'task_scope':scope}\n    exec(compile(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[]),'actual_routing_note','exec'),ns)\n    return ns[variable]\n")
s=s.replace("cls.messages=providers.wire_messages([{'role':'user','content':'Teste sintético de orçamento e contexto.'}],cls.prefix)", "cls.note=routing_note('_chat_avaliacao','note')\n        cls.messages=providers.wire_messages([{'role':'user','content':'Teste sintético de orçamento e contexto.'}],cls.prefix,cls.note)")
s=s.replace("self.assertEqual(body['messages'][0]['content'],self.prefix)", "self.assertEqual(body['messages'][0]['content'],self.prefix+'\\n\\n'+self.note)\n            self.assertIn(ROUTING_INSTRUCTION,body['messages'][0]['content'])\n            without=copy.deepcopy(body);without['messages'][0]['content']=without['messages'][0]['content'].replace('\\n'+ROUTING_INSTRUCTION,'')\n            baseline_bound=providers.check_window(without,spec['output'])\n            self.assertGreater(bound,baseline_bound)")
s=s.replace("'cold_hold_usd_reference':expected,'window':providers.WINDOW,'tools':len(body['tools'])", "'cold_hold_usd_reference':expected,'window':providers.WINDOW,'tools':len(body['tools']),\n                'routing_instruction_included':True,'directive_extra_json_bytes':bound-baseline_bound")
s=s.replace("'retrieval_fixture_characters':24000,'window':providers.WINDOW", "'retrieval_fixture_characters':24000,'routing_instruction_included':ROUTING_INSTRUCTION in prompt,'window':providers.WINDOW")
s=s.replace("def count(payload):counter_calls.append(payload);return self.snapshot.reference_input", "def count(payload):\n            self.assertIn(ROUTING_INSTRUCTION,payload['messages'][0]['content'])\n            counter_calls.append(payload);return self.snapshot.reference_input+37  # Synthetic counter delta; no new native measurement.")
s=s.replace("payload={'model':HAIKU.model,'messages':self.messages,'max_completion_tokens':4096}", "assembled,_=assemble_haiku(iald_motores,[{'role':'user','content':'Teste sintético.'}],self.prefix,HAIKU.model,[],routing_note('_chat_externo','instrucao'))\n        self.assertTrue(assembled[0]['content'].startswith(self.prefix))\n        payload={'model':HAIKU.model,'messages':assembled,'max_completion_tokens':4096}")
s=s.replace("math.ceil(self.snapshot.reference_input*budget.RESERVATION_MARGIN)", "math.ceil((self.snapshot.reference_input+37)*budget.RESERVATION_MARGIN)")
s=s.replace("'cold_hold_usd_reference_default_5m_rates':expected,", "'synthetic_directive_delta_tokens':37,'cold_hold_usd_synthetic_counter_default_5m_rates':expected,")
start=s.index('    def test_07_staged_spend_routes_not_relaxed(self):')
stop=s.index("\nif __name__=='__main__':",start)
s=s[:start]+'''    def test_07_only_reviewed_directive_changes_keep_downstream_guards(self):
        old=ast.parse((R/'iald_web_server.py').read_bytes())
        for name,variable in (('_chat_avaliacao','note'),('_chat_externo','instrucao')):
            left=next(n for n in old.body if isinstance(n,ast.FunctionDef) and n.name==name)
            original=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
            right=copy.deepcopy(original)
            positions=[i for i,arg in enumerate(right.args.kwonlyargs) if arg.arg=='routing_instruction']
            self.assertEqual(len(positions),1);position=positions[0]
            self.assertIsInstance(right.args.kw_defaults[position],ast.Constant)
            self.assertIsNone(right.args.kw_defaults[position].value)
            del right.args.kwonlyargs[position];del right.args.kw_defaults[position]
            expected=ast.parse(f"if routing_instruction and task_scope is None: {variable} += '\\\\n'+routing_instruction").body[0]
            class RemoveReviewedDirective(ast.NodeTransformer):
                removed=0
                def visit_If(self,node):
                    if ast.dump(node,include_attributes=False)==ast.dump(expected,include_attributes=False):
                        self.removed+=1;return None
                    return self.generic_visit(node)
            remover=RemoveReviewedDirective();right=remover.visit(right)
            self.assertEqual(remover.removed,1)
            self.assertEqual(ast.dump(left,include_attributes=False),ast.dump(right,include_attributes=False),name)
            self.assertEqual(routing_note(name,variable),'BASE_SERVICE_NOTE\\n'+ROUTING_INSTRUCTION)
            self.assertEqual(routing_note(name,variable,scope=object()),'BASE_SERVICE_NOTE')
        messages=[{'role':'user','content':'Teste sintético de montagem.'}]
        for provider,model in (('OpenAI','gpt-5.6-luna'),('Anthropic','claude-sonnet-5-5')):
            assembled,_=iald_motores.montar_mensagens(messages,self.prefix,model,[],1000000,4096,
                routing_note('_chat_externo','instrucao'),provedor=provider)
            self.assertTrue(assembled[0]['content'].startswith(self.prefix))
            self.assertEqual(assembled[0]['content'].count(ROUTING_INSTRUCTION),1)
        METRICS['routing_directive']={'only_diff':'keyword routing_instruction=None plus one guarded append before message assembly in each function',
            'functions':['_chat_avaliacao','_chat_externo'],'scope_none_inserts':True,'existing_scope_does_not_duplicate':True,
            'all_other_function_ast_unchanged':True,'openai_sonnet_haiku_real_message_assemblers_keep_directive':True}
''' +s[stop:]
s=s.replace("    report={'status'", "    assert SERVER.read_bytes()==SERVER_RAW,'Server changed during review'\n    report={'status'")
s=s.replace("[Path(__file__),SERVER,W/", "[Path(__file__),SERVER,R/'iald_web_server.py',W/")
backup=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'));backup.write_bytes(raw);assert backup.read_bytes()==raw
compile(s,str(p),'exec');temp=p.with_suffix('.tmp');temp.write_bytes(s.encode());assert temp.read_bytes()==s.encode();temp.replace(p)
print('Updated seven existing regressions; no runtime changes')