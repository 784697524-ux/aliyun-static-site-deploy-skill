#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", "site", "output", "outputs"}
BIG_FILE_LIMIT = 80 * 1024 * 1024


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    env = os.environ.copy()
    env["GIT_LFS_SKIP_SMUDGE"] = "1"
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    return proc.returncode, proc.stdout.strip()


def git_cmd(args: list[str], cwd: Path) -> tuple[int, str]:
    base = [
        "git",
        "-c",
        "filter.lfs.required=false",
        "-c",
        "filter.lfs.process=",
        "-c",
        "filter.lfs.smudge=cat",
        "-c",
        "filter.lfs.clean=cat",
    ]
    return run(base + args, cwd)


def iter_files(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        cur = Path(current)
        for name in files:
            yield cur / name


def has_build_script(package_json: Path) -> bool:
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except Exception:
        return False
    return isinstance(data.get("scripts"), dict) and "build" in data["scripts"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether a frontend project is ready for Aliyun static deployment.")
    parser.add_argument("--project", default=".", help="Project root.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when required items are missing.")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    if not root.exists():
        print(f"ERROR: project does not exist: {root}")
        return 2

    index_html = root / "index.html"
    package_json = root / "package.json"
    if index_html.exists():
        info.append("found index.html")
    elif package_json.exists() and has_build_script(package_json):
        info.append("found package.json build script")
    else:
        errors.append("no index.html and no package.json build script")

    workflow_dir = root / ".github" / "workflows"
    generated_workflow = workflow_dir / "deploy-aliyun-static-site.yml"
    existing_aliyun_workflows = []
    if workflow_dir.exists():
        for workflow in sorted(workflow_dir.glob("*.y*ml")):
            try:
                body = workflow.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if "ALIYUN_" in body or "ossutil" in body.lower():
                existing_aliyun_workflows.append(workflow.relative_to(root))

    if generated_workflow.exists():
        info.append("found .github/workflows/deploy-aliyun-static-site.yml")
    elif existing_aliyun_workflows:
        info.append("found existing Aliyun workflow: " + ", ".join(str(p) for p in existing_aliyun_workflows))
    elif args.strict:
        errors.append("deployment workflow is missing")
    else:
        warnings.append("deployment workflow not generated yet")

    code, out = git_cmd(["rev-parse", "--is-inside-work-tree"], root)
    if code == 0 and out.strip() == "true":
        info.append("inside a git repository")
        code, remote = git_cmd(["remote", "get-url", "origin"], root)
        if code == 0 and remote:
            info.append(f"git remote origin: {remote}")
        elif args.strict:
            errors.append("git remote origin is not configured")
        else:
            warnings.append("git remote origin is not configured")
        code, status = git_cmd(["status", "--short"], root)
        if code == 0:
            changed = [line for line in status.splitlines() if line.strip()]
            if changed:
                warnings.append(f"git has {len(changed)} changed/untracked paths")
            else:
                info.append("git working tree appears clean")
        else:
            warnings.append(f"git status failed: {status}")
    elif args.strict:
        errors.append("not inside a git repository")
    else:
        warnings.append("not inside a git repository")

    large_files = []
    local_videos = []
    for path in iter_files(root):
        try:
            size = path.stat().st_size
        except OSError:
            continue
        rel = path.relative_to(root)
        if size >= BIG_FILE_LIMIT:
            large_files.append((str(rel), size))
        if path.suffix.lower() in {".mp4", ".mov", ".m4v", ".avi"}:
            local_videos.append((str(rel), size))

    if large_files:
        warnings.append("large files may exceed GitHub limits: " + ", ".join(f"{p} ({s // 1024 // 1024}MB)" for p, s in large_files[:8]))
    if local_videos:
        warnings.append("local video files found; prefer remote OSS video URLs or Git LFS: " + ", ".join(p for p, _ in local_videos[:8]))

    print("Aliyun static site deployment readiness")
    print(f"Project: {root}")
    for item in info:
        print(f"OK: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    for item in errors:
        print(f"ERROR: {item}")

    if errors and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
