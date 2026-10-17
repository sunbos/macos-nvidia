#!/usr/bin/env python3
"""Verify selected source patches in a disposable directory; never build or install.

Supply an extracted, unmodified original source tree. Only explicitly listed
files are read from that tree. The supplied tree is never changed.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import tempfile

ARCHIVES = (
    'nvrm-nvaccel-headless', 'nvmtl-observer',
    'air-translator-nested-switch', 'nvk-mesa',
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative_path(value):
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or '\\' in value:
        raise ValueError('unsafe manifest path')
    return Path(*path.parts)


def verify(component, base):
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'manifests' / (component + '.json')).read_text())
    patch = root / relative_path(manifest['patch'])
    if digest(patch.read_bytes()) != manifest['patch_sha256']:
        raise ValueError('patch hash mismatch')
    with tempfile.TemporaryDirectory(prefix='gpu-source-archive-') as temp:
        output = Path(temp)
        for record in manifest['files']:
            relative = relative_path(record['path'])
            source = base / relative
            if source.is_symlink() or not source.resolve().is_relative_to(base.resolve()):
                raise ValueError('source symlink or path escape: ' + record['path'])
            if record['base_sha256'] is None:
                if source.exists():
                    raise ValueError('new file already exists in base: ' + record['path'])
                continue
            if not source.is_file():
                raise ValueError('missing base file: ' + record['path'])
            data = source.read_bytes()
            if digest(data) != record['base_sha256']:
                raise ValueError('wrong base content: ' + record['path'])
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            target.chmod(source.stat().st_mode & 0o777)
        for arguments in (['--check'], []):
            result = subprocess.run(
                ['git', 'apply', *arguments, str(patch)], cwd=output,
                capture_output=True, text=True,
            )
            if result.returncode:
                raise ValueError('git apply failed: ' + result.stderr.strip())
        for record in manifest['files']:
            target = output / relative_path(record['path'])
            if not target.is_file() or target.is_symlink():
                raise ValueError('missing output file: ' + record['path'])
            if digest(target.read_bytes()) != record['source_sha256']:
                raise ValueError('output content mismatch: ' + record['path'])
    return {
        'component': component,
        'base_commit': manifest['base']['commit'],
        'patch_sha256': manifest['patch_sha256'],
        'git_apply_check_exit_code': 0,
        'git_apply_exit_code': 0,
        'verified_source_files': len(manifest['files']),
        'output_hash_mismatches': [],
        'scope': 'Offline source validation only; no build, GPU or installation.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--component', choices=ARCHIVES, required=True)
    parser.add_argument('--base', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify(args.component, args.base)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, 'Verification failed: ' + str(error) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
