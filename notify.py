"""
このモジュールは、LINE Notify APIを使用してメッセージを送信するための機能を提供します。

クラス:
- LINENotifyBot: LINE Notify APIを利用してメッセージを送信するためのクラス。

使い方:
- `LINENotifyBot`クラスのインスタンスを生成し、必要なアクセストークンを引数として渡します。
- `send`メソッドを使用して、LINEにメッセージを送信します。
"""

import requests
import logging


class LINENotifyBot:
    """
    LINE Notify APIを利用してメッセージを送信するためのクラスです。

    Attributes:
        API_URL (str): LINE Notify APIのエンドポイントURL。
        headers (dict): 認証情報を含むHTTPヘッダー。

    Methods:
        send: LINEにメッセージを送信します。
    """

    API_URL = "https://notify-api.line.me/api/notify"

    def __init__(self, access_token):
        """
        LINENotifyBotクラスのコンストラクタです。

        Args:
            access_token (str): LINE Notify APIのアクセストークン。
        """
        self.headers = {'Authorization': 'Bearer ' + access_token}

    def send(self, message):
        """
        指定されたメッセージをLINEに送信します。

        Args:
            message (str): LINEに送信するメッセージ。

        Returns:
            bool: メッセージの送信が成功した場合はTrue、それ以外はFalse。

        Raises:
            requests.RequestException: HTTPリクエスト中にエラーが発生した場合。
        """
        message = '\n' + message
        payload = {'message': message}

        try:
            response = requests.post(
                self.API_URL, headers=self.headers, data=payload)
            if response.status_code == 200:
                logging.info("Message sent successfully.")
                return True
            else:
                logging.error(
                    f"Failed to send message: {response.status_code} {response.text}")
                return False
        except requests.RequestException as e:
            logging.error(f"Error sending message: {e}")
            return False
