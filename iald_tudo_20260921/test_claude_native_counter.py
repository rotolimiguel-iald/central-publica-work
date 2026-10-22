"""Preservation tests at the native count boundary; no API calls."""
from types import SimpleNamespace
import copy
import unittest
from claude_native_counter import native_count_parameters, count_native_request

class CounterTests(unittest.TestCase):
    def setUp(self):
        self.request = {'model':'claude-sonnet-5','max_tokens':4096,
          'metadata':{'user_id':'synthetic-test-id'},
          'system':[{'type':'text','text':'kernel','cache_control':{'type':'ephemeral','ttl':'5m'}}],
          'messages':[{'role':'user','content':'question'},
            {'role':'assistant','content':[{'type':'thinking','thinking':'synthetic thought','signature':'synthetic-signature'},
              {'type':'tool_use','id':'tool1','name':'fetch_tgl','input':{'id':'public'}}]},
            {'role':'user','content':[{'type':'tool_result','tool_use_id':'tool1','content':'evidence'}]}],
          'tools':[{'name':'fetch_tgl','description':'Public source','input_schema':{'type':'object'},'eager_input_streaming':True}],
          'tool_choice':{'type':'auto'},'thinking':{'type':'adaptive'},
          'output_config':{'effort':'high'},'cache_control':{'type':'ephemeral'}}

    def test_all_prompt_blocks_and_signatures_survive(self):
        before = copy.deepcopy(self.request)
        params = native_count_parameters(self.request)
        for field in ('model','messages','system','thinking','tool_choice','output_config','cache_control'):
            self.assertEqual(params[field], self.request[field])
        self.assertEqual(params['tools'][0]['input_schema'], {'type':'object'})
        self.assertNotIn('eager_input_streaming', params['tools'][0])
        self.assertNotIn('metadata', params)
        self.assertNotIn('max_tokens', params)
        self.assertEqual(self.request, before)

    def test_unknown_field_is_not_silently_omitted(self):
        self.request['new_prompt_feature'] = 'unmeasured data'
        with self.assertRaises(ValueError):
            native_count_parameters(self.request)

    def test_provider_count_returned_without_estimation(self):
        captured = []
        def counter(**kwargs):
            captured.append(kwargs)
            return SimpleNamespace(input_tokens=182432)
        client = SimpleNamespace(messages=SimpleNamespace(count_tokens=counter))
        self.assertEqual(count_native_request(client,self.request),182432)
        self.assertEqual(captured[0]['messages'],self.request['messages'])

    def test_missing_or_invalid_count_is_error(self):
        for value in (None,True,0,'182432'):
            client = SimpleNamespace(messages=SimpleNamespace(count_tokens=lambda **kwargs:{'input_tokens':value}))
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    count_native_request(client,self.request)

    def test_sdk_failure_propagates_without_fallback(self):
        def fail(**kwargs):
            raise TimeoutError('synthetic timeout')
        client = SimpleNamespace(messages=SimpleNamespace(count_tokens=fail))
        with self.assertRaises(TimeoutError):
            count_native_request(client,self.request)

if __name__ == '__main__':
    unittest.main()
