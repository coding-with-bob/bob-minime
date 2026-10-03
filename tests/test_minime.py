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
    def test_project_start_preserves_project_and_keeps_coordination_private(self):
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
            project = root / 'project with spaces'
            project.mkdir()
            (project / 'AGENTS.md').write_text('Project-owned rules\n')
            (project / '.codex').mkdir()
            (project / '.codex/config.toml').write_text('model = "project-choice"\n')
            before = {str(p.relative_to(project)): p.read_bytes()
                      for p in project.rglob('*') if p.is_file()}
            with (patch.object(minime, 'ROOT', root),
                  patch.object(minime, 'request', side_effect=api),
                  patch.object(minime, 'archive_bundle', return_value=b'bundle') as bundle,
                  patch.object(minime, 'multipart_bundle', return_value=(b'upload', 'multipart')) as upload,
                  patch('builtins.print')):
                record = minime.start(project, approve_communication=True)

            workspace = Path(record['workspace'])
            self.assertEqual(workspace, project.resolve())
            self.assertEqual(before, {str(p.relative_to(project)): p.read_bytes()
                                     for p in project.rglob('*') if p.is_file()})
            self.assertFalse((project / '.minime').exists())
            coordination = Path(record['coordination'])
            self.assertEqual(list(coordination.iterdir()), [])
            self.assertEqual((coordination.parent / 'CONTRACT.md').read_text(),
                             'Conversation contract\n')
            self.assertEqual(coordination.parent.stat().st_mode & 0o777, 0o700)
            context = bundle.call_args.kwargs['prompt_context']
            self.assertIn(str(coordination), context)
            metadata = upload.call_args.args[1]
            self.assertEqual(metadata['workspace'], str(workspace))
            self.assertEqual(metadata['labels']['omnigent.ui'], 'terminal')
            args = metadata['terminal_launch_args']
            self.assertEqual(args[args.index('--sandbox') + 1], 'danger-full-access')
            self.assertNotIn('--add-dir', args)
            approvals = [args[i+1] for i, arg in enumerate(args) if arg == '-c' and args[i+1].startswith('mcp_servers.')]
            self.assertEqual(set(approvals), {
                f'mcp_servers.omnigent.tools.{tool}.approval_mode="approve"'
                for tool in ('sys_session_send', 'sys_read_inbox',
                             'sys_session_get_history', 'sys_session_close')})
            self.assertEqual(calls, [('GET', '/health'), ('GET', '/v1/hosts'),
                                     ('POST', '/v1/sessions')])
            stored = json.loads((coordination.parent / 'session.json').read_text())
            self.assertEqual(stored['root_id'], 'new-session')

    def test_invalid_project_fails_before_network_or_session_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file = root / 'not-a-directory'
            file.write_text('keep')
            with patch.object(minime, 'request') as api:
                with self.assertRaises(FileNotFoundError):
                    minime.start(root / 'missing')
                with self.assertRaisesRegex(ValueError, 'existing directory'):
                    minime.start(file)
                api.assert_not_called()

    def test_bundle_context_is_root_only_and_keeps_declared_children(self):
        import io
        import tarfile
        import runtime
        context = 'Coordination directory: "/private/run with spaces/.minime"\n'
        with tarfile.open(fileobj=io.BytesIO(runtime.archive_bundle(
                'bob-minime', prompt_context=context)), mode='r:gz') as archive:
            root_prompt = archive.extractfile('config.yaml').read().decode()
            self.assertIn('  ' + context, root_prompt)
            for role in ('architect', 'developer'):
                path = f'agents/{role}/config.yaml'
                self.assertEqual(archive.extractfile(path).read(),
                                 (runtime.ROOT / 'bundle' / path).read_bytes())

    def test_no_ready_host_creates_no_local_workspace_or_session(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (patch.object(minime, 'ROOT', root),
                  patch.object(minime, 'request', side_effect=[{}, {'hosts': []}]) as api):
                with self.assertRaisesRegex(RuntimeError, 'Expected one online'):
                    minime.start(root)
            self.assertEqual(list(root.iterdir()), [])
            self.assertEqual([call.args[1] for call in api.call_args_list], ['GET', 'GET'])


if __name__ == '__main__':
    unittest.main()
