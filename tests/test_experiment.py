"""Protect the launcher's scope on a shared Omnigent server."""
import importlib.util
import json
import tempfile
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

SPEC = importlib.util.spec_from_file_location(
    'experiment', Path(__file__).resolve().parents[1] / 'scripts/experiment.py')
experiment = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(experiment)


class ScopeTests(unittest.TestCase):
    def setUp(self):
        self.record = {'server': 'http://127.0.0.1:6767', 'agent_id': 'own-agent', 'agent_name': 'own-name',
                       'root_id': 'own-root', 'session_ids': ['own-root']}

    def test_other_roots_of_same_bundle_are_excluded_across_pages(self):
        pages = [
            {'data': [{'id': 'own-root', 'agent_id': 'own-agent', 'agent_name': 'own-name'},
                      {'id': 'foreign-root', 'agent_id': 'own-agent', 'agent_name': 'own-name',
                       'parent_session_id': 'foreign-root'}],
             'has_more': True, 'last_id': 'cursor'},
            {'data': [{'id': 'own-child', 'agent_id': 'distinct-child-agent', 'agent_name': 'own-name',
                       'parent_session_id': 'own-root'}], 'has_more': False},
        ]
        with patch.object(experiment, 'request', side_effect=pages) as call:
            self.assertEqual([x['id'] for x in experiment.list_owned(self.record)],
                             ['own-root', 'own-child'])
            self.assertIn('after=cursor', call.call_args.args[2])

    def test_foreign_agent_response_fails_before_any_stop(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'run.json'
            path.write_text(json.dumps(self.record))
            args = type('Args', (), {'run': str(path), 'command': 'stop'})()
            with patch.object(experiment, 'request', return_value={
                    'data': [{'id': 'foreign', 'agent_id': 'other', 'agent_name': 'foreign'}]}) as call:
                with self.assertRaisesRegex(RuntimeError, 'foreign agent'):
                    experiment.operate(args)
                self.assertEqual([c.args[1] for c in call.call_args_list], ['GET'])

    def test_stop_archives_only_owned_children_before_root(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'run.json'
            path.write_text(json.dumps(self.record))
            args = type('Args', (), {'run': str(path), 'command': 'stop'})()
            calls = []

            def api(server, method, endpoint, data=None):
                calls.append((method, endpoint, data))
                if method == 'GET':
                    return {'data': [
                        {'id': 'own-root', 'agent_id': 'own-agent', 'agent_name': 'own-name'},
                        {'id': 'own-child', 'agent_id': 'distinct-child-agent', 'agent_name': 'own-name',
                         'parent_session_id': 'own-root'},
                        {'id': 'unrelated', 'agent_id': 'own-agent', 'agent_name': 'own-name',
                         'parent_session_id': 'unrelated'},
                    ]}
                return {}

            with patch.object(experiment, 'request', side_effect=api), patch('builtins.print'):
                experiment.operate(args)
            writes = calls[1:]
            self.assertEqual(writes, [
                ('POST', '/v1/sessions/own-child/events', {'type': 'stop_session', 'data': {}}),
                ('PATCH', '/v1/sessions/own-child', {'archived': True}),
                ('POST', '/v1/sessions/own-root/events', {'type': 'stop_session', 'data': {}}),
                ('PATCH', '/v1/sessions/own-root', {'archived': True}),
            ])

    def test_remote_server_is_rejected_before_network(self):
        with patch('urllib.request.urlopen') as network:
            with self.assertRaises(ValueError):
                experiment.request('https://example.com', 'POST', '/v1/sessions', {})
            network.assert_not_called()

    def test_permission_config_contains_only_authorized_tools(self):
        import tomllib
        config = tomllib.loads(experiment.communication_config())
        self.assertEqual(config, {'mcp_servers': {'omnigent': {'tools': {
            name: {'approval_mode': 'approve'} for name in (
                'sys_session_send', 'sys_read_inbox',
                'sys_session_get_history', 'sys_session_close')
        }}}})
        self.assertEqual(experiment.launch_args('codex-native'),
                         ['--ask-for-approval', 'never', '--sandbox', 'workspace-write'])


if __name__ == '__main__':
    unittest.main()
