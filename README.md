# 出席確認アプリ

## 🧩 概要
出席管理をシンプルにWeb上で行うための内部向けアプリ。  
Flask + SQLite を使って開発中。

### 主な機能
- 日付別の欠席情報表示
- 欠席理由や書類提出の管理
- 欠席情報の編集・削除
- 書類未提出者の自動抽出
- 指定期間での検索表示
- SQLiteによるデータ保存

---

## 🔧 技術スタック

- Python 3.12
- Flask（Blueprint構成にリファクタリング済）
- SQLite3
- HTML / CSS（テンプレートはJinja2）

---

## ✅ 現時点の進捗（2025-03-28）

- [x] Flask + SQLite の最小構成で立ち上げ完了
- [x] `/other-date` ページの基本レイアウトと機能実装完了
- [x] 教室ごとの縦割りレイアウト（内側に小テーブル）
- [x] 書類提出のチェックボックス（POSTで反映）
- [x] 編集・削除機能つき
- [x] `today`, `undelivered`, `range` ページ完成
- [x] テスト環境（pytest）整備
- [x] Blueprint を導入し `views/` ディレクトリに分割
- [x] DB層を `models/db.py` に切り出し
- [x] 初歩的なユニットテスト導入（`tests/`）
- [ ] テスト未網羅の機能あり（順次追加中）
- [ ] レスポンシブデザイン未対応

---

✨ 主な更新内容（2025/03/31）
	•	views/ディレクトリ内の各ルートをBlueprintごとにモジュールへ分離。
	•	toggle_submitted.py を新規作成し、POST処理のロジックを分離。
	•	URLエンドポイントの命名を明示的に変更し、url_forの解決エラーを修正。
	•	app.py を create_app() ベースに整理。
	•	不要となった attendance.py を廃止。
	•	ルーティングに依存するテストの準備環境を整理中。

---

## 🔜 今後のTODO（メモ）

- ページ間遷移時のUX改善
- エラーハンドリングの整理（特にDB操作）
- テストカバレッジの向上
- ログ機能の活用整備
- 編集画面のデザイン調整

---

## 🧪 テストについて

`pytest` を導入。以下の内容をテスト中：

- DB接続・初期化
- `/` ページ（write）POST処理の動作確認
- URL生成（`url_for`）が正しく動くか
- 将来的には `/edit`, `/toggle-submitted` などもカバー予定

---

## 📁 ファイル構成（リファクタリング後）
attendance_app/
├── app.py                  # アプリ起動用エントリポイント
├── models/
│   └── db.py               # DB接続と初期化処理
├── views/
│   ├── __init__.py         # Blueprintの一括登録
│   ├── write.py            # 登録ページ
│   ├── today.py            # 本日ページ
│   ├── other_date.py       # 任意日ページ
│   ├── undelivered.py      # 書類未提出者一覧
│   ├── edit.py             # 出席情報の編集
│   ├── range_view.py       # 期間指定閲覧
│   ├── delete.py           # レコード削除(生徒の登録じゃないよ)
│   └── toggle_submitted.py # 書類提出済みフラグのトグル
├── templates/
│   └── *.html              # 各テンプレート
├── static/
│   └── style.css             # 全体CSS
├── tests/                    # テストディレクトリ（pytest）
│   ├── test_app.py
│   ├── test_db.py
│   └── test_write.py
├── schema.sql              # DB初期化用SQL
├── db.sqlite3                # SQLite DB（初回はスクリプトで生成）
├── tests/                  # Pytest用のテストコード群
└── README.md               # このファイル
└── requirements.txt          # ライブラリ一覧
---

## 🚀 セットアップ手順

```bash
# リポジトリクローン
$ git clone https://github.com/your-username/attendance-app.git
$ cd attendance-app

# ライブラリインストール
$ pip install -r requirements.txt

# DB初期化（スキーマ反映）
$ sqlite3 db.sqlite3 < schema.sql

# アプリ起動
$ python app.py

⸻

📝 備考

このアプリは学習用・実用兼用として開発中です。
簡潔さ・軽さ・保守性を優先しており、依存パッケージも最小限に抑えています。