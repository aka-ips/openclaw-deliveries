# Claude 永久記憶ファイル

> このファイルは Claude が作業開始前に必ず確認する永久記憶です。
> 既存内容は削除せず、追記で更新してください。

---

## 関連ファイル

- システム設定: [[system]]
- BOT 共有: [[claude-bot]]
- Codex 記憶: [[codex-memory]] / BOT: [[codex-bot]]
- マカロニ: [[macaroni-memory]] / [[macaroni-bot]]
- ケン: [[ken-memory]] / [[ken-bot]]
- レクス: [[rex-memory]] / [[rex-bot]]
- エリク: [[erik-memory]] / [[erik-bot]]
- ブレイク: [[blake-memory]] / [[blake-bot]]

## 基本情報

- **役割**: 設計・監査・検証・緊急時作業
- **システム**: Graphify（マルチエージェント協調システム）
- **リポジトリ**: aka-ips/openclaw-deliveries

## 作業ルール

1. 作業開始前にこのファイルと [[claude-bot]] を必ず読む
2. Codex への指示は [[codex-bot]] に記載する
3. 作業完了後はこのファイルを更新し、成果を記録する
4. Codex の成果物は [[codex-bot]] で確認する

## プロジェクト知識

<!-- プロジェクト固有の知識・決定事項をここに追記 -->

- [2026-07-21] Graphify システム初期構築完了
- [2026-07-21] BOT エージェント5名追加: マカロニ、ケン、レクス、エリク、ブレイク

## 監査ログ

<!-- 監査結果を日付付きで追記 -->

| 日付 | 対象 | 結果 | メモ |
|------|------|------|------|
| 2026-07-21 | Graphify 初期構築 | OK | システムファイル一式作成 |
| 2026-07-21 | BOT エージェント追加 | OK | マカロニ/ケン/レクス/エリク/ブレイクの記憶・BOT ファイル作成 |
| 2026-07-22 | Graphify 構築完了確認 | OK | 全ファイル構築・プッシュ完了、ユーザーにダウンロード方法を案内済 |
| 2026-07-22 | MacBook ダウンロード確認 | OK | ユーザーが MacBook にクローン・チェックアウト完了を確認 |
| 2026-07-22 | Obsidian リンク構造追加 | OK | 全ファイルに [[wikilink]] を追加、グラフビュー対応 |

## 指示履歴

<!-- Codex への指示内容を追記 -->

| 日付 | 指示内容 | ステータス |
|------|---------|-----------|
| 2026-07-21 | Graphify 初期環境セットアップ | 完了 |

## 学習・メモ

<!-- 作業を通じて得た知見を追記 -->

- Graphify は `.graphify/` ディレクトリに全設定・記憶を格納する
- 全 7 エージェント構成: Claude, Codex, マカロニ, ケン, レクス, エリク, ブレイク
- [2026-07-22] 構築済ファイルはブランチ `claude/code-work-od3ic7` にプッシュ済
- [2026-07-22] MacBook へのダウンロードは `git clone` → `git checkout claude/code-work-od3ic7`
- [2026-07-22] `.graphify/` はドットフォルダのため Finder では `Cmd+Shift+.` で表示切替が必要
- [2026-07-22] Obsidian で閲覧可能（Vault = `openclaw-deliveries` フォルダを指定）
- [2026-07-22] Obsidian リンク構造: 全15ファイルに [[wikilink]] 追加済、system.md に Mermaid 関係図追加
- [2026-07-22] MacBook 反映手順: `git pull origin claude/code-work-od3ic7` → Obsidian で Vault を開く
- [2026-07-22] Graphify はアプリ不要の Markdown ベースシステム。Obsidian/Typora/VS Code 等で閲覧可能
