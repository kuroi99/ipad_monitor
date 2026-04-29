# iPad整備品 在庫監視ツール

Appleの認定整備済製品ページを定期的に監視し、指定したiPadが入荷した際にメールで通知するツールです。

## 機能

- 30分ごとに自動チェック
- 対象商品が入荷した際にメール通知
- 一度通知した商品は重複通知しない

## 必要な環境

- Python 3.12.0
- Mac（音声通知にafplayを使用）

## インストール

```bash
pip install -r requirements.txt
```

## 環境変数の設定

`.env`ファイルをプロジェクトフォルダに作成してください：
## 使い方

```bash
python3 main.py
```

## 監視対象の変更

`main.py`の以下の部分を編集してください：

```python
TARGET_KEYWORDS = ["iPad Air", "iPad Pro"]
SUB_KEYWORD = "第3世代"
```

## 注意事項

- `.env`ファイルは絶対にGitHubに上げないでください
- Googleアプリパスワードの取得には2段階認証の設定が必要です