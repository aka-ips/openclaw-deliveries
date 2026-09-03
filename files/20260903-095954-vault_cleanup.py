#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian Vault クリーンアップツール

Vaultヘルスチェックで検出された肥大化（特に 10_raw フォルダ）を
安全に調査・整理するためのスクリプト。

使い方:
    # 1) まず分析だけ実行（何も削除しない）
    python3 vault_cleanup.py analyze

    # 2) 削除候補を確認（拡張子・サイズ・経過日数で絞り込み）
    python3 vault_cleanup.py candidates --older-than 90 --min-size 1M

    # 3) 実際にゴミ箱へ移動（dry-runがデフォルト、--apply で実行）
    python3 vault_cleanup.py clean --older-than 90 --min-size 1M --apply

    # 重複ファイル検出（ハッシュベース、時間がかかるので大きめのファイルのみ）
    python3 vault_cleanup.py dupes --min-size 1M

    # 別Vaultパスを使う場合
    python3 vault_cleanup.py analyze --vault ~/path/to/other-vault
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_VAULT = Path(
    os.path.expanduser(
        "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/obsidian-vault"
    )
)

# 分析から除外するディレクトリ（Obsidian内部/git等）
EXCLUDE_DIRS = {".git", ".obsidian", ".trash", ".DS_Store", "node_modules"}

# 削除しても比較的安全な拡張子（キャッシュ・一時ファイル・大容量メディア候補）
SAFE_EXT_HINT = {
    ".tmp", ".bak", ".log", ".cache",
    ".mov", ".mp4", ".m4v", ".webm",   # 動画：大容量になりがち
    ".zip", ".tar", ".gz", ".7z",       # アーカイブ
    ".dmg", ".iso",
}

SIZE_UNITS = {"B": 1, "K": 1024, "M": 1024**2, "G": 1024**3, "T": 1024**4}


# ----------------------------- ユーティリティ -----------------------------

def parse_size(s: str) -> int:
    s = s.strip().upper()
    if not s:
        return 0
    if s[-1] in SIZE_UNITS:
        return int(float(s[:-1]) * SIZE_UNITS[s[-1]])
    return int(s)


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}" if unit != "B" else f"{n}B"
        n /= 1024
    return f"{n:.1f}PB"


@dataclass
class FileEntry:
    path: Path
    size: int
    mtime: float

    @property
    def age_days(self) -> float:
        import time
        return (time.time() - self.mtime) / 86400

    @property
    def ext(self) -> str:
        return self.path.suffix.lower()


def iter_files(root: Path) -> Iterable[FileEntry]:
    """Vault配下の全ファイルを走査（EXCLUDE_DIRSは除外）"""
    for dirpath, dirnames, filenames in os.walk(root):
        # in-place で除外
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            if name.startswith("."):
                # ドットファイルはスキップ（.DS_Store 等）
                continue
            p = Path(dirpath) / name
            try:
                st = p.stat()
            except (FileNotFoundError, PermissionError):
                continue
            yield FileEntry(path=p, size=st.st_size, mtime=st.st_mtime)


# ----------------------------- コマンド：analyze -----------------------------

def cmd_analyze(args: argparse.Namespace) -> int:
    vault = args.vault
    if not vault.exists():
        print(f"❌ Vaultが見つかりません: {vault}", file=sys.stderr)
        return 2

    total_files = 0
    total_bytes = 0
    per_top = defaultdict(lambda: [0, 0])   # top_dir -> [count, bytes]
    per_ext = defaultdict(lambda: [0, 0])
    largest: list[FileEntry] = []

    for fe in iter_files(vault):
        total_files += 1
        total_bytes += fe.size

        rel = fe.path.relative_to(vault)
        top = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        per_top[top][0] += 1
        per_top[top][1] += fe.size

        per_ext[fe.ext or "(no-ext)"][0] += 1
        per_ext[fe.ext or "(no-ext)"][1] += fe.size

        # 上位N件を保持
        largest.append(fe)
        if len(largest) > 200:
            largest.sort(key=lambda x: x.size, reverse=True)
            largest = largest[:100]

    largest.sort(key=lambda x: x.size, reverse=True)

    print(f"📊 Vault分析: {vault}")
    print(f"   総ファイル数: {total_files:,}")
    print(f"   総サイズ:     {human(total_bytes)} ({total_bytes:,} bytes)")

    print("\n▼ トップディレクトリ別（サイズ降順）")
    for top, (c, b) in sorted(per_top.items(), key=lambda kv: kv[1][1], reverse=True):
        pct = (b / total_bytes * 100) if total_bytes else 0
        print(f"   {top:20s}  {c:6d} files  {human(b):>10s}  ({pct:5.1f}%)")

    print("\n▼ 拡張子別 TOP15（サイズ降順）")
    for ext, (c, b) in sorted(per_ext.items(), key=lambda kv: kv[1][1], reverse=True)[:15]:
        print(f"   {ext:12s}  {c:6d} files  {human(b):>10s}")

    print(f"\n▼ 最大ファイル TOP{min(args.top, len(largest))}")
    for fe in largest[: args.top]:
        rel = fe.path.relative_to(vault)
        print(f"   {human(fe.size):>10s}  age={fe.age_days:5.0f}d  {rel}")

    return 0


# ----------------------------- コマンド：candidates -----------------------------

def _filter_candidates(vault: Path, args: argparse.Namespace) -> list[FileEntry]:
    min_size = parse_size(args.min_size) if args.min_size else 0
    older = args.older_than
    exts = set(e.lower() if e.startswith(".") else "." + e.lower()
               for e in args.ext) if args.ext else None
    subdir = (vault / args.subdir) if args.subdir else vault

    out: list[FileEntry] = []
    for fe in iter_files(subdir):
        if fe.size < min_size:
            continue
        if older is not None and fe.age_days < older:
            continue
        if exts is not None and fe.ext not in exts:
            continue
        out.append(fe)
    out.sort(key=lambda x: x.size, reverse=True)
    return out


def cmd_candidates(args: argparse.Namespace) -> int:
    vault = args.vault
    if not vault.exists():
        print(f"❌ Vaultが見つかりません: {vault}", file=sys.stderr)
        return 2

    cands = _filter_candidates(vault, args)
    total = sum(fe.size for fe in cands)

    print(f"🔍 削除候補: {len(cands)} files / {human(total)}")
    print(f"   条件: subdir={args.subdir or '(vault全体)'} "
          f"older-than={args.older_than}d min-size={args.min_size or '0'} "
          f"ext={args.ext or 'ALL'}")
    print()
    for fe in cands[: args.limit]:
        rel = fe.path.relative_to(vault)
        hint = " ⚠️" if fe.ext in SAFE_EXT_HINT else ""
        print(f"   {human(fe.size):>10s}  age={fe.age_days:5.0f}d  {rel}{hint}")

    if len(cands) > args.limit:
        print(f"   ...他 {len(cands) - args.limit} 件（--limit で拡張）")

    return 0


# ----------------------------- コマンド：clean -----------------------------

def _move_to_trash(path: Path) -> bool:
    """macOSのゴミ箱へ移動（osascript経由、失敗したらFalse）"""
    try:
        subprocess.run(
            [
                "osascript", "-e",
                f'tell application "Finder" to delete POSIX file "{path}"',
            ],
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def cmd_clean(args: argparse.Namespace) -> int:
    vault = args.vault
    if not vault.exists():
        print(f"❌ Vaultが見つかりません: {vault}", file=sys.stderr)
        return 2

    cands = _filter_candidates(vault, args)
    total = sum(fe.size for fe in cands)

    mode = "🗑️  実行" if args.apply else "🧪 dry-run"
    print(f"{mode}: {len(cands)} files / {human(total)} を対象")
    print(f"   条件: subdir={args.subdir or '(vault全体)'} "
          f"older-than={args.older_than}d min-size={args.min_size or '0'} "
          f"ext={args.ext or 'ALL'}")

    if not cands:
        print("対象なし。終了。")
        return 0

    if not args.apply:
        print("\n（先頭30件を表示）")
        for fe in cands[:30]:
            print(f"   would delete: {human(fe.size):>10s}  {fe.path.relative_to(vault)}")
        print("\n👉 --apply を付けて実行するとゴミ箱へ移動します。")
        return 0

    # --apply: 実行
    if not args.yes:
        ans = input(f"\n本当に {len(cands)} 件 / {human(total)} をゴミ箱へ移動しますか？ [y/N]: ")
        if ans.strip().lower() != "y":
            print("中止しました。")
            return 1

    ok = 0
    ng = 0
    for fe in cands:
        if _move_to_trash(fe.path):
            ok += 1
        else:
            ng += 1
            print(f"   ⚠️ 失敗: {fe.path}", file=sys.stderr)
    print(f"\n完了: OK={ok} / NG={ng}")
    return 0 if ng == 0 else 1


# ----------------------------- コマンド：dupes -----------------------------

def _hash_file(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def cmd_dupes(args: argparse.Namespace) -> int:
    vault = args.vault
    if not vault.exists():
        print(f"❌ Vaultが見つかりません: {vault}", file=sys.stderr)
        return 2

    min_size = parse_size(args.min_size) if args.min_size else 0

    # まずサイズでグルーピング（サイズが違うなら中身も違う）
    by_size: dict[int, list[FileEntry]] = defaultdict(list)
    for fe in iter_files(vault):
        if fe.size >= min_size:
            by_size[fe.size].append(fe)

    dupe_groups: list[list[FileEntry]] = []
    for size, entries in by_size.items():
        if len(entries) < 2:
            continue
        # サイズ一致だけハッシュ計算
        by_hash: dict[str, list[FileEntry]] = defaultdict(list)
        for fe in entries:
            try:
                by_hash[_hash_file(fe.path)].append(fe)
            except (OSError, PermissionError):
                continue
        for group in by_hash.values():
            if len(group) >= 2:
                dupe_groups.append(group)

    dupe_groups.sort(key=lambda g: g[0].size * (len(g) - 1), reverse=True)

    total_waste = sum(g[0].size * (len(g) - 1) for g in dupe_groups)
    print(f"🧬 重複グループ: {len(dupe_groups)} 個 / 節約可能 {human(total_waste)}")
    print(f"   条件: min-size={args.min_size or '0'}\n")

    for g in dupe_groups[: args.limit]:
        waste = g[0].size * (len(g) - 1)
        print(f"[{len(g)}件 x {human(g[0].size)}  → 節約 {human(waste)}]")
        for fe in g:
            print(f"   {fe.path.relative_to(vault)}")
        print()
    return 0


# ----------------------------- CLI -----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Obsidian Vault クリーンアップツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--vault", type=lambda x: Path(os.path.expanduser(x)),
                   default=DEFAULT_VAULT, help=f"Vaultパス（既定: {DEFAULT_VAULT}）")

    sub = p.add_subparsers(dest="cmd", required=True)

    p_an = sub.add_parser("analyze", help="Vault全体のサイズ内訳を表示")
    p_an.add_argument("--top", type=int, default=30, help="最大ファイル表示件数")
    p_an.set_defaults(func=cmd_analyze)

    def add_filter_args(sp):
        sp.add_argument("--subdir", default=None,
                        help="対象サブディレクトリ（例: 10_raw）")
        sp.add_argument("--older-than", type=int, default=None,
                        help="この日数より古いファイルのみ")
        sp.add_argument("--min-size", type=str, default=None,
                        help="最小サイズ（例: 1M, 500K）")
        sp.add_argument("--ext", nargs="*", default=None,
                        help="対象拡張子（例: --ext mov mp4 zip）")

    p_ca = sub.add_parser("candidates", help="削除候補を一覧表示")
    add_filter_args(p_ca)
    p_ca.add_argument("--limit", type=int, default=100)
    p_ca.set_defaults(func=cmd_candidates)

    p_cl = sub.add_parser("clean", help="ゴミ箱へ移動（既定はdry-run）")
    add_filter_args(p_cl)
    p_cl.add_argument("--apply", action="store_true", help="実際に実行")
    p_cl.add_argument("--yes", action="store_true", help="確認プロンプトを省略")
    p_cl.set_defaults(func=cmd_clean)

    p_du = sub.add_parser("dupes", help="重複ファイル検出")
    p_du.add_argument("--min-size", type=str, default="1M")
    p_du.add_argument("--limit", type=int, default=30)
    p_du.set_defaults(func=cmd_dupes)

    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
