"""Unit contracts only: synthetic tool content/counts, no provider or credentials."""
from copy import deepcopy
import hashlib
import json
import unittest
from unittest.mock import Mock
from claude_tool_budget import fit_latest_tool_results, ToolResultsDoNotFit

def serialized(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True)

class FitContracts(unittest.TestCase):
    def setUp(self):
        self.content=json.dumps({'path':'TGLExt/Fixture.lean','source_sha256':hashlib.sha256(b'fixture source').hexdigest(),
            'status':'READ_NOT_COMPILED','negative':'NOT_CONFIRMED','start_line':10,'next_line':90,
            'text':'\n'.join('lemma fixture_'+str(i) for i in range(80))})
        self.payload={'model':'claude-haiku-4-5-20251001','max_completion_tokens':4096,'tool_choice':'auto',
            'tools':[{'name':'immutable fixture tool'}], 'messages':[
                {'role':'developer','content':'IMMUTABLE PREFIX'},
                {'role':'user','content':'KEEP QUESTION'},
                {'role':'assistant','tool_calls':[{'id':'old','function':{'name':'read','arguments':'{}'}}]},
                {'role':'tool','tool_call_id':'old','content':'OLD BATCH KEEP'},
                {'role':'assistant','content':'KEEP OWN TEXT','tool_calls':[{'id':'new','function':{'name':'read','arguments':'{"path":"TGLExt/Fixture.lean"}'}}]},
                {'role':'tool','tool_call_id':'new','content':self.content}]}

    def counter(self,p):
        return 190000 if 'PARTIAL_TOOL_RESULT' in p['messages'][-1]['content'] else 196000

    def test_payload_prefix_history_assistant_args_and_tools_unchanged(self):
        before=serialized(self.payload);result=fit_latest_tool_results(self.payload,self.counter,200000)
        self.assertEqual(serialized(self.payload),before)
        self.assertEqual(serialized(result['messages'][:-1]),serialized(self.payload['messages'][:-1]))
        self.assertEqual(serialized(result['tools']),serialized(self.payload['tools']))
        self.assertEqual(result['messages'][-1]['tool_call_id'],'new')
        self.assertEqual(result['tool_choice'],'none')

    def test_provenance_negatives_hash_status_and_resume_are_explicit(self):
        result=fit_latest_tool_results(self.payload,self.counter,200000)
        item=json.loads(result['messages'][-1]['content'])
        self.assertEqual(item['original_result_sha256'],hashlib.sha256(self.content.encode()).hexdigest())
        self.assertEqual(item['original_metadata']['negative'],'NOT_CONFIRMED')
        self.assertEqual(item['original_metadata']['status'],'READ_NOT_COMPILED')
        self.assertEqual(item['original_metadata']['next_line'],90)
        self.assertEqual(item['excerpt_resume']['start_line'],50)
        self.assertEqual(len(item['excerpt']['text'].splitlines()),40)
        self.assertEqual(item['context_status'],'PARTIAL_TOOL_RESULT')

    def test_counter_failure_propagates_before_send(self):
        send=Mock();count=Mock(side_effect=RuntimeError('synthetic counter failure'))
        with self.assertRaises(RuntimeError):send(fit_latest_tool_results(self.payload,count,200000))
        send.assert_not_called()

    def test_no_round_fits_fail_closed_with_bounded_counts(self):
        send=Mock();count=Mock(return_value=199000);before=serialized(self.payload)
        with self.assertRaises(ToolResultsDoNotFit):send(fit_latest_tool_results(self.payload,count,200000))
        self.assertEqual(count.call_count,6);send.assert_not_called()
        self.assertEqual(before,serialized(self.payload))

    def test_old_batch_never_modified_when_tail_is_user(self):
        self.payload['messages'].append({'role':'user','content':'NEW QUESTION'})
        count=Mock();before=serialized(self.payload)
        self.assertIs(fit_latest_tool_results(self.payload,count,200000),self.payload)
        count.assert_not_called();self.assertEqual(before,serialized(self.payload))

    def test_mismatched_tool_ids_refused(self):
        self.payload['messages'][-1]['tool_call_id']='unrelated'
        with self.assertRaises(ToolResultsDoNotFit):fit_latest_tool_results(self.payload,self.counter,200000)

    def test_little_room_forces_final_without_changing_results(self):
        count=Mock(return_value=194705)
        result=fit_latest_tool_results(self.payload,count,200000)
        self.assertEqual(result['tool_choice'],'none')
        self.assertEqual(serialized(result['messages']),serialized(self.payload['messages']))
        self.assertEqual(count.call_count,2)

if __name__=='__main__':unittest.main()
