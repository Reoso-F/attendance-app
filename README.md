# 出席確認アプリ

## 概要
欠席・欠課管理のためのWebアプリケーションです。Flask + SQLite による軽量構成で、ローカルPC上で動作します。

## 特徴
- 日付ごとの出席・欠席状況の表示
- 欠席理由・書類提出の管理
- SQLiteでのローカルデータ管理

## 動作環境
- Python 3.9+
- Flask 2.x

## セットアップ手順

```bash
git clone https://github.com/Reoso-F/attendance-app.git
cd attendance_app
pip install -r requirements.txt
sqlite3 db.sqlite3 < schema.sql
python app.py