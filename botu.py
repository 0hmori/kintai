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
