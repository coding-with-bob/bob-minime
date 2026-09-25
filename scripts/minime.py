#!/usr/bin/env python3
"""Open a conversation-first MiniMe session on the local Omnigent host."""
import argparse
import json
import shutil
import time
import uuid

from runtime import (ROOT, NATIVE_UI_LABELS, archive_bundle, communication_config,
                        launch_args, multipart_bundle, request, save)


def start(server='http://127.0.0.1:6767', approve_communication=False, title='MiniMe'):
    request(server, 'GET', '/health')
    hosts = request(server, 'GET', '/v1/hosts')['hosts']
    ready = [host for host in hosts if host['status'] == 'online'
             and host.get('configured_harnesses', {}).get('codex-native') is True]
    if len(ready) != 1:
        raise RuntimeError(f'Expected one online Codex-native host, found {len(ready)}')

    session_key = time.strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:6]
    directory = ROOT / '.sessions' / session_key
    workspace = directory / 'workspace'
    workspace.mkdir(parents=True)
    (workspace / '.minime').mkdir()
    shutil.copy(ROOT / 'CONTRACT.md', workspace / 'CONTRACT.md')
    (workspace / 'AGENTS.md').write_text(
        '# MiniMe coordination workspace\n\n'
        'Read CONTRACT.md. Start with conversation; no project task is assigned yet.\n'
        'The owner chooses the project during the conversation. Store coordination\n'
        'notes in .minime/ here. Give children the exact agreed project and handoff\n'
        'paths, and have them use that project for commands and repo instructions.\n'
        'Do not treat this directory as the implementation repository.\n'
        'Files and handoffs are English; talk with the owner in Hungarian.\n')
    if approve_communication:
        (workspace / '.codex').mkdir()
        (workspace / '.codex/config.toml').write_text(communication_config())

    record = {'session_key': session_key, 'server': server,
              'workspace': str(workspace), 'host_id': ready[0]['host_id'],
              'agent_name': 'minime', 'communication_preapproved': approve_communication}
    save(directory / 'session.json', record)
    body, content_type = multipart_bundle(archive_bundle('minime'), {
        'title': title, 'host_id': ready[0]['host_id'], 'workspace': str(workspace),
        'terminal_launch_args': launch_args('codex-native', approve_communication),
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
    parser.add_argument('--server', default='http://127.0.0.1:6767')
    parser.add_argument('--title', default='MiniMe')
    parser.add_argument('--approve-communication', action='store_true',
                        help='Preapprove only the four owner-authorized communication tools')
    args = parser.parse_args()
    start(args.server, args.approve_communication, args.title)


if __name__ == '__main__':
    main()
