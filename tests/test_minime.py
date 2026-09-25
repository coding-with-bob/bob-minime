"""Check that normal startup remains a conversation, not a trial kickoff."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location('minime', SCRIPTS / 'minime.py')
minime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(minime)


class ConversationStartupTests(unittest.TestCase):
    def test_empty_start_has_no_task_no_git_repository_and_main_terminal_ui(self):
        calls = []

        def api(server, method, path, data=None, content_type=None):
            calls.append((method, path))
            if path == '/health':
                return {}
            if path == '/v1/hosts':
                return {'hosts': [{'host_id': 'local', 'status': 'online',
                                  'configured_harnesses': {'codex-native': True}}]}
            if method == 'POST' and path == '/v1/sessions':
                return {'id': 'new-session'}
            self.fail(f'Unexpected request: {method} {path}')

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'CONTRACT.md').write_text('Conversation contract\n')
            with (patch.object(minime, 'ROOT', root),
                  patch.object(minime, 'request', side_effect=api),
                  patch.object(minime, 'archive_bundle', return_value=b'bundle'),
                  patch.object(minime, 'multipart_bundle', return_value=(b'upload', 'multipart')) as upload,
                  patch('builtins.print')):
                record = minime.start(approve_communication=True)

            workspace = Path(record['workspace'])
            self.assertFalse((workspace / 'OWNER_TASK.md').exists())
            self.assertFalse((workspace / '.git').exists())
            self.assertEqual(list((workspace / '.minime').iterdir()), [])
            self.assertEqual((workspace / 'CONTRACT.md').read_text(), 'Conversation contract\n')
            metadata = upload.call_args.args[1]
            self.assertEqual(metadata['workspace'], str(workspace))
            self.assertEqual(metadata['labels']['omnigent.ui'], 'terminal')
            self.assertEqual(metadata['labels']['omnigent.wrapper'], 'codex-native-ui')
            self.assertEqual(calls, [('GET', '/health'), ('GET', '/v1/hosts'),
                                     ('POST', '/v1/sessions')])
            stored = json.loads((workspace.parent / 'session.json').read_text())
            self.assertEqual(stored['root_id'], 'new-session')
            import tomllib
            config = tomllib.loads((workspace / '.codex/config.toml').read_text())
            self.assertEqual(set(config['mcp_servers']['omnigent']['tools']), {
                'sys_session_send', 'sys_read_inbox', 'sys_session_get_history', 'sys_session_close'})

    def test_no_ready_host_creates_no_local_workspace_or_session(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (patch.object(minime, 'ROOT', root),
                  patch.object(minime, 'request', side_effect=[{}, {'hosts': []}]) as api):
                with self.assertRaisesRegex(RuntimeError, 'Expected one online'):
                    minime.start()
            self.assertEqual(list(root.iterdir()), [])
            self.assertEqual([call.args[1] for call in api.call_args_list], ['GET', 'GET'])


if __name__ == '__main__':
    unittest.main()
