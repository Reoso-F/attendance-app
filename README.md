# 出席確認アプリ　　"""作成中"""

## 🧩 概要
職業訓練校の出席管理をシンプルにWeb上で行うための内部向けアプリ。
Flask + SQLite を使って高速に開発。

機能

日付別の欠席情報表示

欠席理由や書類提出の管理

SQLiteによるデータ保存

欠席情報の編集・更新（/edit 機能）

## 🔧 技術スタック

- Python 3.12
- Flask
- SQLite
- HTML / CSS（テンプレートはJinja2）

## ✅ 現時点の進捗（2025-03-26）

- [x] Flask + SQLite の最小構成で立ち上げ完了
- [x] `/other-date` ページの基本レイアウトと機能実装完了
  - 日付で出欠情報を切り替えて表示
  - 教室ごとに縦割りレイアウト（内側に小テーブル）
  - 書類提出のチェックボックス（POSTで反映）
  - 編集・削除ボタンあり（削除は未実装）
- [x] CSSは `style.css` に整理済み
- [ ] 編集ページのUI未調整
- [ ] 削除機能未実装
- [ ] レスポンシブデザイン未対応（今後検討）

## 🔜 今後やること（メモ）

- 削除処理の実装（POST＋CSRF対策）
- 編集画面のブラッシュアップ
- テーブルデザインの最適化（可能ならBootstrapなしで）
- 編集履歴の記録 or ログ機能の追加

---

## 📝 備考

このアプリは学習・運用用途を兼ねており、軽量で明快な構成を優先しています。

## セットアップ手順

# リポジトリクローン
$ git clone https://github.com/your-username/attendance-app.git
$ cd attendance-app

# ライブラリインストール
$ pip install -r requirements.txt

# 初期DB作成
$ sqlite3 db.sqlite3 < schema.sql

# 起動
$ python app.py

# ファイル構成
attendance_app/
├── app.py              # Flaskアプリ本体
├── schema.sql          # DB初期スクリプト
├── db.sqlite3          # SQLite DB（初回はスクリプトで生成）
├── templates/          # HTMLテンプレート
│   └── index.html      # 欠席一覧画面
│   └── edit.html       # 欠席編集画面
├── static/             # CSS/JS
├── tests/              # テストコード
│   └── test_app.py     # 簡易テスト
├── README.md           # 説明文書
└── requirements.txt    # 必要ライブラリ
