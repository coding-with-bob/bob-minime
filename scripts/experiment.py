#!/usr/bin/env python3
"""Controlled Bob MiniMe rehearsals and evidence capture over local Omnigent."""
import argparse
import json
import shutil
import subprocess
import time
import urllib.parse
import uuid
from pathlib import Path

from runtime import (ROOT, COMMUNICATION_TOOLS, NATIVE_UI_LABELS, archive_bundle,
                     communication_config, launch_args, multipart_bundle, request, save)


def start(args):
    request(args.server, 'GET', '/health')
    hosts = request(args.server, 'GET', '/v1/hosts')['hosts']
    ready = [h for h in hosts if h['status'] == 'online'
             and h.get('configured_harnesses', {}).get('codex-native') is True
             and h.get('configured_harnesses', {}).get(args.harness) is True]
    if len(ready) != 1:
        raise RuntimeError(f'Expected one online Codex-native host, found {len(ready)}')
    run_id = time.strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:6]
    run_dir = ROOT / '.runs' / run_id
    workspace = run_dir / 'workspace'
    workspace.mkdir(parents=True)
    (workspace / '.minime').mkdir()
    if args.approve_communication:
        (workspace / '.codex').mkdir()
        (workspace / '.codex/config.toml').write_text(communication_config())
    shutil.copy(ROOT / 'CONTRACT.md', workspace / 'CONTRACT.md')
    fixture = Path(args.fixture).resolve() if args.fixture else ROOT / 'fixtures/workflow.md'
    shutil.copy(fixture, workspace / 'OWNER_TASK.md')
    (workspace / 'AGENTS.md').write_text(
        '# Disposable Bob MiniMe trial\n\n'
        'Read OWNER_TASK.md. Use Python standard library only. Files and commits\n'
        'are English. Work only here. No network, external data, remotes, global\n'
        'settings, or other sessions. Do not modify OWNER_TASK.md or CONTRACT.md.\n'
        'Commit implementation and project review/status documents; .minime/ is\n'
        'ignored relay evidence, not the canonical completion record.\n')
    (workspace / '.gitignore').write_text('.minime/\n__pycache__/\n*.pyc\n')
    subprocess.run(['git', 'init', '-b', 'main', str(workspace)], check=True, capture_output=True)
    subprocess.run(['git', '-C', str(workspace), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(workspace), 'commit', '-m', 'chore: seed synthetic trial'],
                   check=True, capture_output=True)
    record = {'run_id': run_id, 'server': args.server, 'workspace': str(workspace),
              'host_id': ready[0]['host_id'], 'agent_name': 'bob-minime-trial-' + run_id,
              'fixture': str(fixture), 'started_at': time.time(), 'session_ids': [],
              'communication_preapproved': args.approve_communication,
              'root_harness': args.harness}
    record_path = run_dir / 'run.json'
    save(record_path, record)
    archive = archive_bundle(record['agent_name'], args.harness)
    (run_dir / 'bundle.tar.gz').write_bytes(archive)
    body, content_type = multipart_bundle(archive, {
        'title': 'Bob MiniMe trial ' + run_id,
        'host_id': ready[0]['host_id'], 'workspace': str(workspace),
        'terminal_launch_args': launch_args(args.harness, args.approve_communication),
        'labels': {'minime_run': run_id, **NATIVE_UI_LABELS},
    })
    session = request(args.server, 'POST', '/v1/sessions', body, content_type)
    record['root_id'] = session.get('id') or session['session_id']
    record['session_ids'].append(record['root_id'])
    save(record_path, record)
    snapshot = request(args.server, 'GET', f"/v1/sessions/{record['root_id']}?include_items=false")
    record['agent_id'] = snapshot['agent_id']
    save(record_path, record)
    ack = request(args.server, 'POST', f"/v1/sessions/{record['root_id']}/events", {
        'type': 'message', 'data': {'role': 'user', 'content': [
            {'type': 'input_text', 'text':
             'Run the task in OWNER_TASK.md under CONTRACT.md. This is an authorized '
             'local synthetic trial. Use the configured native agents and existing '
             'authentication. Complete the bounded task, preserving any real '
             'uncertainties. Do not alter the task to make the trial pass.'}]}})
    record['start_ack'] = ack
    save(record_path, record)
    print(json.dumps({'run': str(record_path), 'root_id': record['root_id'],
                      'workspace': str(workspace),
                      'url': args.server + '/c/' + record['root_id']}, indent=2))


def list_owned(record):
    result, after = [], None
    while True:
        query = {'agent_name': record['agent_name'], 'kind': 'any', 'visibility': 'all',
                 'include_archived': 'true', 'limit': 100}
        if after:
            query['after'] = after
        page = request(record['server'], 'GET', '/v1/sessions?' + urllib.parse.urlencode(query))
        for session in page['data']:
            if session.get('agent_name') != record['agent_name']:
                raise RuntimeError('Session listing returned a foreign agent; refusing to act')
            if (session['id'] == record['root_id']
                    or session.get('parent_session_id') == record['root_id']):
                result.append(session)
        if not page.get('has_more'):
            break
        after = page.get('last_id')
        if not after:
            raise RuntimeError('Paginated session response has no cursor')
    return result


def operate(args):
    path = Path(args.run).resolve()
    record = json.loads(path.read_text())
    sessions = list_owned(record)
    for session in sessions:
        if session['id'] not in record['session_ids']:
            record['session_ids'].append(session['id'])
    save(path, record)
    if args.command == 'stop':
        # Stop children before the root; never target an unverified external ID.
        sessions.sort(key=lambda s: s['id'] == record['root_id'])
        for session in sessions:
            request(record['server'], 'POST', f"/v1/sessions/{session['id']}/events",
                    {'type': 'stop_session', 'data': {}})
            request(record['server'], 'PATCH', f"/v1/sessions/{session['id']}",
                    {'archived': True})
        record['stop_requested_at'] = time.time()
        save(path, record)
    if args.command == 'capture':
        dest = path.parent / 'snapshots'
        dest.mkdir(exist_ok=True)
        for session in sessions:
            snapshot = request(record['server'], 'GET',
                               f"/v1/sessions/{session['id']}?include_items=true&include_usage=true")
            save(dest / (session['id'] + '.json'), snapshot)
        print('Captured', len(sessions), 'sessions in', dest)
    print(json.dumps([{'id': s['id'], 'title': s.get('title'), 'status': s.get('status'),
                       'archived': s.get('archived'),
                       'parent': s.get('parent_session_id')}
                      for s in sessions], indent=2, ensure_ascii=False))
    if args.command == 'stop':
        print('Stop and archive requested. Runtime teardown is asynchronous; verify snapshots.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    launch = sub.add_parser('start')
    launch.add_argument('--server', default='http://127.0.0.1:6767')
    launch.add_argument('--fixture')
    launch.add_argument('--harness', choices=['codex-native'], default='codex-native')
    launch.add_argument('--approve-communication', action='store_true',
                        help='Use only with owner authorization: preapprove four session tools')
    for name in ('status', 'capture', 'stop'):
        sub.add_parser(name).add_argument('run')
    args = parser.parse_args()
    start(args) if args.command == 'start' else operate(args)


if __name__ == '__main__':
    main()
