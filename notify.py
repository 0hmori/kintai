import requests
import schedule
import datetime
import locale
import time


def send_line_notify(notification_message):
    # LINEに通知する
    line_notify_token = "lZGbtwZUGrxRQy3Df8vdRgdwwby8u9FuofvfwGE8qod"
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {line_notify_token}"}
    data = {"message": "\n" + notification_message}
    requests.post(line_notify_api, headers=headers, data=data)


if __name__ == "__main__":
    send_line_notify("LiNEに通知する")

# 上と下のやり方がある


class LINE_Notify:
    def __init__(self):
        # LINE_Notify_APIのURL
        self.API_url = "https://notify-api.line.me/api/notify"
        self.access_token = "lZGbtwZUGrxRQy3Df8vdRgdwwby8u9FuofvfwGE8qod"
        self.__headers = {"Authorization": "Bearer " + self.access_token}

    # メッセージだけを送信するための関数
    def Sent_Message(self, message):
        payload = {"message": message}
        requests.post(
            self.API_url,
            headers=self.__headers,
            params=payload,
        )


# if __name__ == "__main__":
#    LINE_Notify = LINE_Notify()
#    LINE_Notify.Sent_Message("テストメッセージだよ！！")
# エラーが出るけど実行できる


locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
Today = datetime.datetime.now()
week_num = Today.weekday()
w_list = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]

# print(Today,  week_num,  w_list[week_num]) 実行OK


def rimind_punch_in():
    if week_num == 0:
        message = "おはようございます！今日は月曜日です。出勤登録をお願いします"
    elif week_num == 1:
        message = "おはようございます！今日は火曜日です。出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた
    elif week_num == 2:
        message = "おはようございます！今日は水曜日です。出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた
    elif week_num == 3:
        message = "おはようございます！今日は木曜日です。出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた
    elif week_num == 4:
        message = "おはようございます！今日は金曜日です。出勤登録をお願いします"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた
    else:
        pass

    # print(w_list[week_num], message) 実行OK
    return message  # なんで赤波線が出るのか…


if __name__ == "__main__":
    schedule.every().monday.at("08:30").do(rimind_punch_in)
    schedule.every().tuesday.at("08:30").do(rimind_punch_in)
    schedule.every().wednesday.at("08:30").do(rimind_punch_in)
    schedule.every().thursday.at("07:30").do(rimind_punch_in)
    schedule.every().friday.at("08:30").do(rimind_punch_in)

    while True:
        schedule.run_pending()
        time.sleep(1)