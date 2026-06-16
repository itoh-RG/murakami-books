# 村上春樹 文庫本管理アプリ

Pythonista 3 for iOS で動く、村上春樹の文庫本管理アプリです。

## 機能

- 文庫本40冊の一覧（長編小説・短篇集・エッセイ）
- **カテゴリフィルター**：長編小説 / 短篇集 / エッセイ
- **ステータスフィルター**：読了 / 未読 / 所持 / 未所持
- 読了・所持のトグル管理
- ★5段階評価
- 感想・メモの記入
- 読了・所持冊数のサマリー表示
- データは `~/Documents/murakami_data.json` に自動保存

## 使い方

1. [Pythonista 3](https://omz-software.com/pythonista/) を iPhone にインストール
2. `murakami_books.py` を Pythonista の Documents フォルダにコピー
3. Pythonista で開き、実行ボタン（▶︎）をタップ

## ファイル構成

```
murakami_books.py   ← アプリ本体（これ1つだけ必要）
```

## データ管理

データは JSON で保存されます。バックアップしたい場合は `murakami_data.json` をコピーしてください。このファイルは `.gitignore` に含まれているためリポジトリには含まれません。
