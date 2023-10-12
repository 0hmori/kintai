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