# Wa BGM 公開前チェック 是正指示書

- 対象動画: 穏やかな渓流を眺める2時間｜新緑・森・小川のせせらぎ｜リラックス環境音｜Wa BGM ✨ Japanese Nature Sounds for Deep Sleep | 森の渓流
- video id: `yOp1Y-J8LnU`
- チェック結果: **WARN**（PASS=5 / WARN=6 / FAIL=0）
- レポート受領日: 2026-08-28
- 本書の位置づけ: WARN 6件の是正内容をまとめた作業指示書。公開前に YouTube Studio 側で下記を反映のこと。

---

## ⚠️ #1 タイトル長 89 文字（86–100 の警告帯：Latin 系言語で表示崩れの可能性）

末尾の「| 森の渓流」は冒頭の「渓流」と重複しており、削除しても検索キーワードを失わない。

**修正案（82 文字、警告帯を回避）:**

```
穏やかな渓流を眺める2時間｜新緑・森・小川のせせらぎ｜リラックス環境音｜Wa BGM ✨ Japanese Nature Sounds for Deep Sleep
```

- 削除部分: 末尾 ` | 森の渓流`（7 文字）
- 「Wa BGM」ブランド名・主要キーワード（渓流 / 新緑 / 森 / せせらぎ / 環境音 / Deep Sleep）はすべて維持。

## ⚠️ #3 説明文に hanagasa CTA URL が欠落

説明文の CTA ブロック（チャンネル登録導線の直後）に、チャンネル標準の 花笠（hanagasa）CTA URL を挿入すること。URL はチャンネル運用ドキュメントの最新版を正とする（本リポジトリには URL 原本がないため、ここでは転記しない）。

挿入位置の目安:

```
🌸 花笠はこちら → <hanagasa CTA URL>
```

挿入後、ハッシュタグ数が 15 以下のままであることを再確認（現在 12、#5 は PASS のため余裕あり）。

## ⚠️ #7 公開時刻 12:00 JST（規定外）

公開予約時刻がチャンネル規定から外れている。YouTube Studio の公開スケジュールを、チャンネル規定の公開時刻（運用ドキュメント記載の標準時刻）に変更すること。リラックス／睡眠系の同チャンネル動画と同一の時刻に揃える。

## ⚠️ #9 ローカライズ不足 1/8（de / en / es / fr / ko / pt / zh が未設定）

以下の訳文を YouTube Studio →「字幕」→「タイトルと説明」に登録する。説明文は各言語とも「訳文 1 行＋日本語原文の主要ブロック＋CTA」を基本とし、下記はタイトルと説明リード文。

### en (English)
- Title: `Calm Mountain Stream for 2 Hours | Fresh Green Forest & Babbling Brook | Relaxing Nature Sounds | Wa BGM`
- Description lead: `Relax and fall asleep to the gentle sounds of a Japanese mountain stream, surrounded by fresh green forest. Wa BGM – Japanese nature sounds for deep sleep, study, and relaxation.`

### de (Deutsch)
- Title: `Ruhiger Gebirgsbach – 2 Stunden | Frischer grüner Wald & plätschernder Bach | Naturgeräusche | Wa BGM`
- Description lead: `Entspannen und einschlafen mit den sanften Klängen eines japanischen Gebirgsbachs im frischen grünen Wald. Wa BGM – japanische Naturklänge für tiefen Schlaf und Entspannung.`

### es (Español)
- Title: `Arroyo de montaña tranquilo, 2 horas | Bosque verde y agua que fluye | Sonidos de la naturaleza | Wa BGM`
- Description lead: `Relájate y duerme con el suave sonido de un arroyo de montaña japonés rodeado de bosque verde. Wa BGM: sonidos de la naturaleza de Japón para dormir profundamente y relajarse.`

### fr (Français)
- Title: `Ruisseau de montagne paisible, 2 h | Forêt verdoyante et eau qui coule | Sons de la nature | Wa BGM`
- Description lead: `Détendez-vous et endormez-vous au doux murmure d'un ruisseau de montagne japonais entouré de verdure. Wa BGM : sons de la nature du Japon pour un sommeil profond et la relaxation.`

### ko (한국어)
- Title: `잔잔한 계곡 물소리 2시간 | 신록의 숲과 시냇물 소리 | 릴렉스 자연 소리 | Wa BGM`
- Description lead: `신록의 숲에 둘러싸인 일본 계곡의 잔잔한 물소리와 함께 휴식하고 잠들어 보세요. Wa BGM – 깊은 수면과 휴식을 위한 일본의 자연 소리.`

### pt (Português)
- Title: `Riacho de montanha tranquilo, 2 horas | Floresta verde e água corrente | Sons da natureza | Wa BGM`
- Description lead: `Relaxe e adormeça com o som suave de um riacho de montanha japonês cercado por floresta verde. Wa BGM – sons da natureza do Japão para sono profundo e relaxamento.`

### zh (中文)
- Title: `平静溪流2小时｜新绿森林与潺潺流水｜放松自然环境音｜Wa BGM`
- Description lead: `在新绿森林环绕的日本山间溪流声中放松身心、安然入睡。Wa BGM——助您深度睡眠与放松的日本自然之声。`

※ 各タイトルは 100 文字以内であることを確認済み。各言語の説明文にも「Wa BGM」表記を必ず含める（チェック #2 対応の言語版）。

## ⚠️ #10 チャプター／コンセプト自動生成 OFF → 人間目視確認

自動生成が OFF のため、公開前に以下を目視確認すること。

- [ ] 説明文内のチャプター（タイムスタンプ）が動画内容と一致しているか
- [ ] チャプターを付けない方針の動画であれば、その方針どおりであることを確認

## ⚠️ #11 コメントモデレーション「強」 → 人間目視確認

- [ ] モデレーション「強」がこの動画で意図した設定かを確認（チャンネル標準と異なる場合は標準へ戻す）
- [ ] 保留コメントの確認運用が回ることを確認

---

## 対応サマリ

| # | 項目 | 対応 |
|---|------|------|
| 1 | タイトル長 89 | 末尾「| 森の渓流」を削除 → 82 文字 |
| 3 | hanagasa CTA 欠落 | CTA ブロックを説明文へ挿入 |
| 7 | 公開時刻 12:00 JST | チャンネル規定時刻へ再スケジュール |
| 9 | ローカライズ 1/8 | 上記 7 言語の訳文を登録 |
| 10 | チャプター自動生成 OFF | 公開前に人間目視確認 |
| 11 | コメントモデレーション強 | 設定意図を人間目視確認 |

反映後に `wabgm-pre-publish` チェックを再実行し、#1 / #3 / #7 / #9 が PASS になることを確認すること（#10 / #11 は目視確認で完了）。
