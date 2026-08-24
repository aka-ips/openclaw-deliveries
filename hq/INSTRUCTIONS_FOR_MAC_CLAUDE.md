# Mac側Claudeへの指示文（ボスがそのまま貼り付けて使う）

以下のブロックを Mac mini の Claude Code セッションにそのまま貼り付けてください。

---

openclaw-deliveries リポジトリの `claude/uq-tool-issues-39kov5` ブランチにある
`hq/SPEC_FIXES_v1.1.md` と `hq/hq_backup.sh` を取得して、HQツールの改修を進めてください。

手順:
1. `git clone -b claude/uq-tool-issues-39kov5 https://github.com/aka-ips/openclaw-deliveries /tmp/hq-fixes` で取得
2. `SPEC_FIXES_v1.1.md` を読み、F1（文書整合）と F4（バックアップ常設）を先に適用
   - F4 では GitHub にプライベートリポジトリ hq-backup を作ってから
     `hq_backup.sh setup <リポジトリURL>` を実行。公開リポジトリは絶対に使わない
3. F2・F3・F5 は 2026-08-24 に私（ボス）が承認語「①YES」で承認済み
   （SPEC_FIXES_v1.1.md の承認記録参照）。承認カードの起票は不要、そのまま適用してよい
4. 各修正は検証担当（反対側のBOT）の独立再検査を通してから確定する
5. 完了報告は4行カードで

---

## 出先からの確認方法（ボス向けメモ）

- **同じセッションを出先で見る:** Mac の Claude Code セッション内で `/rc` を打っておくと、
  スマホの Claude アプリ（Codeタブ）や claude.ai/code から同じセッションに合流できる
- **正本・状態の閲覧:** F4 適用後は、スマホの GitHub アプリで hq-backup リポジトリを
  開けば最新の charter.md や状態ファイルが読める
- **承認:** 従来どおり Telegram の4行カードに番号＋承認語（①YES など）で返信
