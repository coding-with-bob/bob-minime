"""Shared local Omnigent transport and bundle helpers."""
import io
import json
import re
import tarfile
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNICATION_TOOLS = ('sys_session_send', 'sys_read_inbox',
                       'sys_session_get_history', 'sys_session_close')
NATIVE_UI_LABELS = {'omnigent.ui': 'terminal', 'omnigent.wrapper': 'codex-native-ui'}


def launch_args(harness='codex-native', approve_communication=False):
    if harness == 'claude-native':
        return (['--allowedTools', ','.join('mcp__omnigent__' + tool
                                          for tool in COMMUNICATION_TOOLS)]
                if approve_communication else [])
    return ['--ask-for-approval', 'never', '--sandbox', 'workspace-write']


def communication_config():
    return '\n'.join(f'[mcp_servers.omnigent.tools.{tool}]\napproval_mode = "approve"\n'
                     for tool in COMMUNICATION_TOOLS)


def request(server, method, path, data=None, content_type='application/json'):
    if urllib.parse.urlparse(server).hostname not in ('127.0.0.1', 'localhost', '::1'):
        raise ValueError('MiniMe only targets a local Omnigent server')
    if data is not None and not isinstance(data, bytes):
        data = json.dumps(data).encode()
    req = urllib.request.Request(server + path, data=data, method=method,
                                 headers={'Content-Type': content_type})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            body = response.read()
            return json.loads(body) if body else None
    except urllib.error.HTTPError as error:
        raise RuntimeError(f'{method} {path}: HTTP {error.code}: '
                           f'{error.read().decode()[:2000]}') from error


def save(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temp.replace(path)


def archive_bundle(name, harness='codex-native'):
    if harness != 'codex-native':
        raise ValueError('The pinned Astra/Sol bundle requires codex-native')
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode='w:gz') as archive:
        for source in sorted((ROOT / 'bundle').rglob('*')):
            if not source.is_file():
                continue
            relative = source.relative_to(ROOT / 'bundle')
            data = source.read_bytes()
            if str(relative) == 'config.yaml':
                data = re.sub(rb'(?m)^name: .*$', f'name: {name}'.encode(), data, count=1)
            info = tarfile.TarInfo(str(relative))
            info.size, info.mode = len(data), 0o644
            archive.addfile(info, io.BytesIO(data))
    return output.getvalue()


def multipart_bundle(data, metadata):
    boundary = 'minime-' + uuid.uuid4().hex
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="metadata"\r\n\r\n'
            + json.dumps(metadata) + '\r\n').encode()
    body += (f'--{boundary}\r\nContent-Disposition: form-data; name="bundle"; '
            'filename="agent.tar.gz"\r\nContent-Type: application/gzip\r\n\r\n').encode()
    body += data + f'\r\n--{boundary}--\r\n'.encode()
    return body, f'multipart/form-data; boundary={boundary}'

