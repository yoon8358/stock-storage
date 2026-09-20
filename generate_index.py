#!/usr/bin/env python3
"""
stock-storage INDEX.md 생성기
저장소 루트에서 실행: python3 generate_index.py
모든 파일을 폴더별로 정리해 GitHub blob/raw 링크를 INDEX.md에 기록한다.
"""
import os
import subprocess
from datetime import datetime, timezone
from urllib.parse import quote

REPO = "yoon8358/stock-storage"
BRANCH = "main"
OUT = "INDEX.md"
SKIP_DIRS = {".git", ".github", "__pycache__", "node_modules"}
SKIP_FILES = {OUT, "generate_index.py"}


def list_files():
    """git 추적 파일 우선, 실패하면 파일시스템 스캔."""
    try:
        # NUL 구분으로 한글, 공백, 줄바꿈이 있는 파일명도 그대로 읽는다.
        out = subprocess.check_output(
            ["git", "ls-files", "-z"], stderr=subprocess.DEVNULL
        )
        files = [f for f in os.fsdecode(out).split("\0") if f]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for root, dirs, names in os.walk("."):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for n in names:
                path = os.path.relpath(os.path.join(root, n), ".")
                files.append(path.replace(os.sep, "/"))
    files = [
        f for f in files
        if not any(part in SKIP_DIRS for part in f.split("/")[:-1])
        and os.path.basename(f) not in SKIP_FILES
        and os.path.isfile(f)
    ]
    return sorted(files)


def blob(path):
    return f"https://github.com/{REPO}/blob/{quote(BRANCH, safe='')}/{quote(path, safe='/')}"


def raw(path):
    return f"https://raw.githubusercontent.com/{REPO}/{quote(BRANCH, safe='')}/{quote(path, safe='/')}"


def label(path):
    """파일명 안의 Markdown 대괄호와 줄바꿈을 표시용으로 이스케이프한다."""
    return (path.replace("\\", "\\\\")
                .replace("[", "\\[").replace("]", "\\]")
                .replace("\r", "&#13;").replace("\n", "&#10;"))


def main():
    files = list_files()
    by_dir = {}
    for f in files:
        d = os.path.dirname(f) or "(root)"
        by_dir.setdefault(d, []).append(f)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# INDEX",
        "",
        f"자동 생성: {now}  ",
        f"총 {len(files)}개 파일. AI/도구는 이 파일의 링크를 따라 개별 파일을 읽는다.",
        "",
    ]
    for d in sorted(by_dir):
        lines.append(f"## {label(d)}")
        lines.append("")
        for f in by_dir[d]:
            try:
                size = os.path.getsize(f)
            except OSError:
                size = 0
            lines.append(f"- [{label(f)}]({blob(f)}) · [raw]({raw(f)}) · {size:,} B")
        lines.append("")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("\n".join(lines))
    print(f"{OUT} 생성 완료 ({len(files)} files)")


if __name__ == "__main__":
    main()
