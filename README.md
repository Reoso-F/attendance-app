# 出席確認アプリ　　"""作成中"""

## 🧩 概要
出席管理をシンプルにWeb上で行うための内部向けアプリ。
Flask + SQLite を使って開発。

機能

- 日付別の欠席情報表示
- 欠席理由や書類提出の管理
- SQLiteによるデータ保存
- 欠席情報の編集・更新（/edit 機能）
- 書類未提出一覧、期間指定による欠席表示機能追加

## 🔧 技術スタック

- Python 3.12
- Flask
- SQLite
- HTML / CSS（テンプレートはJinja2）

## ✅ 現時点の進捗（2025-03-27）

- [x] Flask + SQLite の最小構成で立ち上げ完了
- [x] `/other-date` ページの基本レイアウトと機能実装完了
- [x] `/today` ページの表示と曜日表記対応
- [x] `/undelivered`（書類未提出一覧）ページ実装完了
- [x] `/range`（期間指定表示）ページ実装完了
- [x] `/edit` ページの編集処理機能完成
- [x] 各教室を縦割りで表示し、内部にサブテーブルを設置
- [x] 書類提出チェック機能とデータ反映処理
- [x] 編集・削除ボタンあり（/edit, /delete）
- [x] CSSは `style.css` に整理済み
- [x] 書類提出のチェック状態により別日画面への遷移を防止
- [ ] 編集ページのUI未調整
- [ ] レスポンシブデザイン未対応（今後検討）
- [ ] ログ出力（app.log）導入は保留中

## 🔜 今後やること（メモ）

- 編集画面のブラッシュアップ
- テーブルデザインの最適化（可能ならBootstrapなしで）
- 編集履歴の記録 or ログ機能の追加
- DBの整合性チェック強化（NULL値対策など）

---

## 📝 備考

このアプリは学習・運用用途を兼ねており、軽量で明快な構成を優先しています。

## セットアップ手順

```bash
# リポジトリクローン
$ git clone https://github.com/your-username/attendance-app.git
$ cd attendance-app

# ライブラリインストール
$ pip install -r requirements.txt

# 初期DB作成
$ sqlite3 db.sqlite3 < schema.sql

# 起動
$ python app.py
```

## ファイル構成

```
attendance_app/
├── app.py              # Flaskアプリ本体
├── schema.sql          # DB初期スクリプト
├── db.sqlite3          # SQLite DB（初回はスクリプトで生成）
├── templates/          # HTMLテンプレート
│   ├── write.html      # 書き込みページ
│   ├── today.html      # 本日の欠席・欠課
│   ├── other_date.html # 別日表示ページ
│   ├── undelivered.html# 書類未提出一覧
│   ├── range.html      # 指定期間の欠席表示
│   └── edit.html       # 欠席編集画面
├── static/             # CSS/JS
│   └── style.css       # 全体スタイル定義
├── tests/              # テストコード
│   └── test_app.py     # 簡易テスト
├── README.md           # 説明文書
└── requirements.txt    # 必要ライブラリ
```
