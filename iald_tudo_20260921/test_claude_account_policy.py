import unittest
from claude_account_policy import available_models, authorize_model
from claude_profiles import HAIKU, SONNET


class AccountPolicyTests(unittest.TestCase):
    def test_guest_and_blocked_accounts_cannot_get_either_model(self):
        self.assertEqual(available_models(username='', account_approved=True,
            haiku_ready=True, sonnet_ready=True), ())
        self.assertEqual(available_models(username='luiz', account_approved=False,
            haiku_ready=True, sonnet_ready=True), ())

    def test_public_user_has_no_sonnet_even_when_both_ready(self):
        policy = dict(username='testador', account_approved=True,
                      haiku_ready=True, sonnet_ready=True)
        self.assertEqual(available_models(**policy), (HAIKU.model,))
        with self.assertRaises(PermissionError):
            authorize_model(SONNET.model, **policy)

    def test_only_luiz_has_internal_sonnet(self):
        policy = dict(username='luiz', account_approved=True, sonnet_ready=True)
        self.assertEqual(authorize_model(SONNET.model, **policy), SONNET.model)
        self.assertEqual(available_models(username='outro_admin',
            account_approved=True, sonnet_ready=True), ())

    def test_missing_readiness_never_exposes_undeployed_haiku(self):
        with self.assertRaises(PermissionError):
            authorize_model(HAIKU.model, username='luiz', account_approved=True)

    def test_alias_resolves_but_unknown_model_is_rejected(self):
        policy = dict(username='testador', account_approved=True, haiku_ready=True)
        self.assertEqual(authorize_model('claude-haiku-4-5', **policy), HAIKU.model)
        with self.assertRaises(ValueError):
            authorize_model('claude-unreviewed', **policy)

    def test_string_flags_cannot_enable_access(self):
        with self.assertRaises(ValueError):
            available_models(username='testador', account_approved='true', haiku_ready=True)


if __name__ == '__main__':
    unittest.main()
