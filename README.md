# LINE 通知機能付きリンクチェッカー

## 概要

このプロジェクトは、指定されたウェブサイトからリンクを抽出し、新しいリンクが見つかった場合に LINE を通じて通知を行う Python スクリプトです。<br>
GitHub Actions を使用して定期的に実行されることを想定しています。

## 機能

- 指定したウェブサイトから HTML を取得し、リンクを抽出します。
- 新しいリンクが前回のリンクと異なる場合、それらを CSV ファイルに保存し、LINE で通知します。
- 新しいリンクが見つからなかった場合、その旨をログに記録します。

## 使用技術

- Python 3
- BeautifulSoup
- requests
- LINE Notify API
- GitHub Actions

## アピールポイント

- **GitHub Actions の活用**: GitHub Actions を利用した CI/CD パイプラインにより、定期的かつ自動的にスクリプトを実行できるようになっています。
- **カスタマイズ可能**: 抽出するリンクのタイプや通知の内容は容易にカスタマイズ可能で、多様なウェブサイトに対応可能です。
- **多目的利用**: リンクの監視だけでなく、価格変動、ニュース更新など様々な用途に応じてカスタマイズ可能です。

## 必要条件

- Python 3
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [requests](https://docs.python-requests.org/en/latest/)

## セットアップ

**HTML 要素からどのリンクを取得するかは、アプリケーションによって異なります。<br>
extract_links 関数内の BeautifulSoup の使用方法を変更する必要があります。**<br>

1. リポジトリをクローンします。

```shell
git clone https://github.com/yourusername/your-repo-name.git<br>
```

2. ディレクトリの移動

```shell
cd your-repo-name
```

2. 必要な依存関係をインストールします。

```shell
pip install beautifulsoup4 requests
```

3. 環境変数`LINE_TOKEN`に LINE Notify のアクセストークンを設定します。

```shell
export LINE_TOKEN='your_line_notify_token'
```

4. `main.py`の`URL`変数をスクレイピングしたいウェブサイトの URL に設定します。

```shell
   URL = "your_want_to_scrape_site"
```

## GitHub Actions を使用した使用方法

1. GitHub リポジトリの Settings に移動し、Secrets を設定します。
2. `LINE_TOKEN`として LINE Notify のアクセストークンを追加します。
3. `.github/workflows`ディレクトリに GitHub Actions のワークフローファイルを作成します。

## 注意事項

- このスクリプトは、ウェブスクレイピングを行います。対象ウェブサイトの利用規約を確認し、適切な使用を心がけてください。
- LINE Notify のアクセストークンは安全に保管し、公開しないでください。
