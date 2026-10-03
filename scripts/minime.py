#!/usr/bin/env python3
"""Open a conversation-first Bob MiniMe session on the local Omnigent host."""
import argparse
import json
import shutil
import time
import uuid
from pathlib import Path

from runtime import (ROOT, NATIVE_UI_LABELS, archive_bundle,
                     launch_args, multipart_bundle, request, save)


def start(project, server='http://127.0.0.1:6767', approve_communication=False, title='Bob MiniMe'):
    workspace = Path(project).expanduser().resolve(strict=True)
    if not workspace.is_dir():
        raise ValueError(f'Project must be an existing directory: {workspace}')
    request(server, 'GET', '/health')
    hosts = request(server, 'GET', '/v1/hosts')['hosts']
    ready = [host for host in hosts if host['status'] == 'online'
             and host.get('configured_harnesses', {}).get('codex-native') is True]
    if len(ready) != 1:
        raise RuntimeError(f'Expected one online Codex-native host, found {len(ready)}')

    session_key = time.strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:6]
    directory = ROOT / '.sessions' / session_key
    directory.mkdir(parents=True, mode=0o700)
    coordination = directory / '.minime'
    coordination.mkdir()
    shutil.copy(ROOT / 'CONTRACT.md', directory / 'CONTRACT.md')
    prompt_context = (
        f'Read your coordination contract at {json.dumps(str(directory / "CONTRACT.md"))}.\n'
        f'Use {json.dumps(str(coordination))} for all private coordination notes,\n'
        'including state.md, events.jsonl and any handoffs.\n'
    )
    terminal_args = launch_args('codex-native', approve_communication,
                                sandbox='danger-full-access')

    record = {'session_key': session_key, 'server': server,
              'workspace': str(workspace), 'coordination': str(coordination), 'host_id': ready[0]['host_id'],
              'agent_name': 'bob-minime', 'communication_preapproved': approve_communication}
    save(directory / 'session.json', record)
    body, content_type = multipart_bundle(archive_bundle('bob-minime', prompt_context=prompt_context), {
        'title': title, 'host_id': ready[0]['host_id'], 'workspace': str(workspace),
        'terminal_launch_args': terminal_args,
        'labels': {**NATIVE_UI_LABELS, 'minime_session': session_key},
    })
    session = request(server, 'POST', '/v1/sessions', body, content_type)
    record['root_id'] = session.get('id') or session['session_id']
    record['url'] = server + '/c/' + record['root_id']
    save(directory / 'session.json', record)
    # Creating the session must not submit a task or start a child agent.
    print(json.dumps(record, indent=2))
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True,
                        help='Existing project directory (or worktree) used as the startup directory')
    parser.add_argument('--server', default='http://127.0.0.1:6767')
    parser.add_argument('--title', default='Bob MiniMe')
    parser.add_argument('--approve-communication', action='store_true',
                        help='Preapprove only the four owner-authorized communication tools')
    args = parser.parse_args()
    start(args.project, args.server, args.approve_communication, args.title)


if __name__ == '__main__':
    main()
