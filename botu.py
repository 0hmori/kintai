# ボツにしたやつ


# kintai.pyにて
def edit():
    # 修正するために一番下の行を0:00で上書きしたが、再度出勤すると一番下に行が追加されてしまう
    worksheet = auth()
    df1 = pd.DataFrame(worksheet.get_all_records())

    # timestamp = datetime.now(JST)

    # punch_out = timestamp.strftime("%H:%M")
    # print(punch_out)

    df1.iloc[-1, 2] = "00:00"
    df1.iloc[-1, 1] = "00:00"

    worksheet.update([df1.columns.values.tolist()] + df1.values.tolist())

    print("修正登録完了しました。入力し直してください")

# edit() #動作確認はOK！最終行が0:00になる


class LINE_Notify:
    def __init__(self):
        # LINE_Notify_APIのURL
        self.API_url = "https://notify-api.line.me/api/notify"
        self.access_token = ""
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


def rimind_punch_out():
    Today = datetime.datetime.today()
    # print(Today)

    weekday_number = Today.weekday()
    week_list = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
    # print(Today, weekday_number, week_list[weekday_number])

    if weekday_number == 0:
        message = "退勤時間になりました！退勤登録をお願いします。月曜日、おつかれさまでした"

    elif weekday_number == 1:
        message = "退勤時間になりました！退勤登録をお願いします。火曜日、おつかれさまでした"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    elif weekday_number == 2:
        message = "退勤時間になりました！退勤登録をお願いします。水曜日、おつかれさまでした"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    elif weekday_number == 3:
        message = "退勤時間になりました！退勤登録をお願いします。木曜日、おつかれさまでした"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    elif weekday_number == 4:
        message = "退勤時間になりました！退勤登録をお願いします。金曜日、おつかれさまでした"  # 動作確認用。動作OK！print(rimind_punch_in())ではこのメッセージのみ出せた

    else:
        pass

    return message  # week_list[weekday_number]を入れないでみた
    # print(message)  # week_list[weekday_number]を入れないと上のリストにエラー。でも出力はできる。


# print(rimind_punch_out())  # 動作確認OK


if __name__ == "__main__":
    schedule.every().monday.at("17:30").do(rimind_punch_out)
    schedule.every().tuesday.at("17:30").do(rimind_punch_out)
    schedule.every().wednesday.at("17:30").do(rimind_punch_out)
    schedule.every().thursday.at("06:16").do(rimind_punch_out)
    schedule.every().friday.at("17:30").do(rimind_punch_out)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)