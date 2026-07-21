# Graphify System Configuration

## システム概要

Graphify は 7つのAIエージェントが協調して作業を行うマルチエージェントシステムです。

## 役割分担

### Claude（設計・監査担当）
- **指示**: 作業方針の策定、タスク設計、Codex への作業指示
- **監査**: Codex の成果物レビュー、品質チェック
- **検証**: 出力の正確性・整合性の最終検証
- **緊急時作業**: Codex が対応不能な場合の直接作業

### Codex（実行・作業担当）
- **作業**: 実装、コード記述、ファイル操作の実行
- **検証**: 自身の成果物のセルフチェック
- **緊急時指示**: Claude が応答不能な場合の自律判断

### マカロニ（BOT エージェント）
- **作業**: タスク実行・検証
- **連携**: Claude / Codex からの指示に基づき作業

### ケン（BOT エージェント）
- **作業**: タスク実行・検証
- **連携**: Claude / Codex からの指示に基づき作業

### レクス（BOT エージェント）
- **作業**: タスク実行・検証
- **連携**: Claude / Codex からの指示に基づき作業

### エリク（BOT エージェント）
- **作業**: タスク実行・検証
- **連携**: Claude / Codex からの指示に基づき作業

### ブレイク（BOT エージェント）
- **作業**: タスク実行・検証
- **連携**: Claude / Codex からの指示に基づき作業

## 作業フロー

```
1. Claude が記憶ファイルを確認 → 作業方針決定
2. Claude が Codex に指示を発行
3. Codex が自身の記憶ファイルを確認 → 作業実行
4. Codex が成果物を BOT 記憶ファイルに記録
5. Claude が成果物を監査・検証
6. Claude が結果を記憶ファイルに記録
```

## 記憶ファイル構成

| ファイル | 用途 |
|---------|------|
| `memory/claude-memory.md` | Claude 専用永久記憶 |
| `memory/codex-memory.md` | Codex 専用永久記憶 |
| `bots/claude-bot.md` | Claude BOT 状態・共有情報 |
| `bots/codex-bot.md` | Codex BOT 状態・共有情報 |
| `memory/macaroni-memory.md` | マカロニ専用永久記憶 |
| `memory/ken-memory.md` | ケン専用永久記憶 |
| `memory/rex-memory.md` | レクス専用永久記憶 |
| `memory/erik-memory.md` | エリク専用永久記憶 |
| `memory/blake-memory.md` | ブレイク専用永久記憶 |
| `bots/macaroni-bot.md` | マカロニ BOT 状態・共有情報 |
| `bots/ken-bot.md` | ケン BOT 状態・共有情報 |
| `bots/rex-bot.md` | レクス BOT 状態・共有情報 |
| `bots/erik-bot.md` | エリク BOT 状態・共有情報 |
| `bots/blake-bot.md` | ブレイク BOT 状態・共有情報 |

## 必須ルール

1. **作業前確認**: 各エージェントは作業開始前に自身の記憶ファイルと BOT ファイルを必ず読み込む
2. **作業後記録**: 作業完了後は記憶ファイルと BOT ファイルを必ず更新する
3. **情報共有**: 相手エージェントに伝えるべき情報は BOT ファイルに記載する
4. **履歴保持**: 記憶ファイルの既存内容は削除せず、追記で更新する
