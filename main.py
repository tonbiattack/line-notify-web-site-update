"""
このスクリプトは、特定のウェブサイトからリンクを取得し、新しいリンクが見つかった場合にそれをLINE通知するために使用されます。

設定:
- URL: スクレイピングするウェブサイトのURL。
- ACCESS_TOKEN: LINE通知を送信するためのアクセストークン。
- CSV_FILE: 以前に取得したリンクを保存するCSVファイルの名前。
- LOG_FILE: ログを記録するファイルの名前。

関数:
- fetch_html(url): 指定されたURLからHTMLコンテンツを取得します。
- extract_links(html): HTMLコンテンツからリンクを抽出します。
- read_old_links(file_name): CSVファイルから以前に保存されたリンクを読み込みます。
- write_new_links(file_name, links): 新しく取得したリンクをCSVファイルに書き込みます。
- notify_new_links(bot, new_links, old_links): 新しく追加されたリンクがあれば、それをLINEで通知します。

メインプログラム:
- ウェブサイトからHTMLを取得し、リンクを抽出します。
- 新しいリンクが前回のリンクと異なる場合、それらをCSVファイルに保存し、LINEで通知します。
- 新しいリンクが見つからなかった場合、その旨をログに記録します。
"""

import os
import sys
import csv
import urllib.request
import logging
from bs4 import BeautifulSoup
from notify import LINENotifyBot

# 設定
URL = "your_want_to_scrape_site"
ACCESS_TOKEN = os.getenv('LINE_TOKEN')
CSV_FILE = 'links.csv'
LOG_FILE = 'log.log'

# ログの設定
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(levelname)s : %(asctime)s : %(message)s')


def fetch_html(url):
    """
    指定されたURLからHTMLコンテンツを取得します。

    Args:
        url (str): 取得するHTMLのURL。

    Returns:
        str: 取得したHTMLコンテンツ。

    Raises:
        Exception: URLの取得に失敗した場合。
    """
    try:
        with urllib.request.urlopen(url) as response:
            logging.info('HTTP STATUS CODE: ' + str(response.getcode()))
            return response.read()
    except Exception as e:
        logging.error(f"Error fetching URL {url}: {e}")
        sys.exit(1)


def extract_links(html):
    """
    HTMLコンテンツからリンクを抽出します。

    Args:
        html (str): 抽出するリンクが含まれるHTMLコンテンツ。

    Returns:
        list of str: 抽出されたリンクのリスト。
    """
    soup = BeautifulSoup(html, "html.parser")
    return [tag.get('href') for tag in soup.find_all(class_="line2")]


def read_old_links(file_name):
    """
    CSVファイルから以前に保存されたリンクを読み込みます。

    Args:
        file_name (str): 読み込むCSVファイルの名前。

    Returns:
        set of str: ファイルから読み込まれたリンクのセット。
    """
    try:
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                return set(row)
    except FileNotFoundError:
        logging.info('No previous links file found. Creating new one.')
    return set()


def write_new_links(file_name, links):
    """
    新しく取得したリンクをCSVファイルに書き込みます。

    Args:
        file_name (str): 書き込むCSVファイルの名前。
        links (list of str): 書き込むリンクのリスト。

    Raises:
        Exception: ファイルの書き込みに失敗した場合。
    """
    try:
        with open(file_name, 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerow(links)
    except Exception as e:
        logging.error(f"Failed to write csv file: {e}")
        sys.exit(1)


def notify_new_links(bot, new_links, old_links):
    """
    新しく追加されたリンクがあれば、それをLINEで通知します。

    Args:
        bot (LINENotifyBot): 通知を行うためのLINENotifyBotインスタンス。
        new_links (set of str): 新しく追加されたリンクのセット。
        old_links (set of str): 前回取得されたリンクのセット。
    """
    added = new_links - old_links
    for link in added:
        bot.send(link)


def main():
    """
    メインプログラムです。ウェブサイトからHTMLを取得し、リンクを抽出して処理します。
    """
    bot = LINENotifyBot(ACCESS_TOKEN)
    logging.info('START')

    html = fetch_html(URL)
    new_links = set(extract_links(html))
    old_links = read_old_links(CSV_FILE)

    if new_links != old_links:
        write_new_links(CSV_FILE, new_links)
        notify_new_links(bot, new_links, old_links)
        logging.info('New links found and notified.')
    else:
        logging.info('No new links found.')


if __name__ == "__main__":
    main()
