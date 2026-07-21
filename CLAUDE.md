# CLAUDE.md - Graphify System Rules

## Graphify 必須ルール

**すべての作業開始前に、以下のファイルを必ず読み込むこと：**

1. `.graphify/memory/claude-memory.md` — Claude 永久記憶
2. `.graphify/bots/claude-bot.md` — Claude BOT 共有情報
3. `.graphify/bots/codex-bot.md` — Codex BOT 共有情報（Codex の状態確認）

**作業完了後に、以下を必ず更新すること：**

1. `.graphify/memory/claude-memory.md` に作業結果を追記
2. `.graphify/bots/claude-bot.md` に Codex への伝達事項を追記

## 役割

- **Claude**: 設計、指示、監査、検証、緊急時作業
- **Codex**: 作業実行、検証、緊急時指示

## ファイル構成

```
.graphify/
├── config/
│   └── system.md          # システム設定
├── memory/
│   ├── claude-memory.md   # Claude 永久記憶
│   └── codex-memory.md    # Codex 永久記憶
└── bots/
    ├── claude-bot.md      # Claude BOT（Codex との共有）
    └── codex-bot.md       # Codex BOT（Claude との共有）
```

## 記憶ファイル更新ルール

- 既存内容は**絶対に削除しない**（追記のみ）
- 日付を必ず付与する
- テーブル形式のログは行を追加する形で更新する
