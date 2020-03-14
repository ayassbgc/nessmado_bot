# スクリプト名：bot.py
# バージョン：5.0
# 作成日：2019/03/xx
# 最終更新日：2019/07/19
# 作成者：(へっへ)
# はじめに：
# ｜ネス窓をdiscort運用するにあたり、窓の運用が快適になるような機能群を用意する。
# ｜機能群を用意するに当たり、可読性、新規機能追加の容易さの観点から
# ｜オブジェクト指向をベースにプログラムを組むこととする。
# ｜ただし、私も勉強の途中であることから、変な書き方になってるところがいっぱいあります。すまん。
# ｜
#
# スクリプト概要：
# ｜メイン関数があるスクリプト。サーバーで起動する際は本スクリプトを起動させる。
"""更新履歴（目を通す必要はない）
    2019/03/11 ver 3.0
    キャラ対策用チャンネルの管理bot開発
     - キャラ対策チャンネルへの質問の振り分け機能
     - mother2ネタのメッセージ送信機能
    2019/05/01 Ver 2.0
    オブジェクト指向に沿ってリファクタリング実施。
     - 今後の課題：質問クラスが死んでるので気が向いたらきれいにする。
    2019/05/13 Ver 3.0, 3.1
    質問チャンネルおよびそれに関わる部分の修正
     - メッセージの文言だけをトリガーにしていたが、メッセージがどのチャンネルに投稿されたのかについてもトリガーに追加。
       これにより質問クラスのフローかなりマシになった。
    2019/07/06 Ver 4.0
    discord.py のバージョンを0.16.12 → 1.2.3へ変更。
    これにあたり以下を修正。
    ・send_message周りを更新
    ・チャンネルIDの型がstrからintへ変更。
    2019/07/18 ver 5.0
    対策クラスの作成にて、コルーチンを使用するAPIの使用方法を学習し、その結果
    自作クラスにてasync/await使用する方法がわかった。
    そのために、
    ・自作クラスからbot.pyに作成したメッセージとそれを記載するチャンネルを送り、
    ・それをbot.pyにてsendにて記載する
    という処理をわざわざbot.pyでする必要がなくなる（＝自作クラス内ですればよい）。
    なので、上記2点を実行するための処理を削除。自作クラスに処理を記載。
"""
import discord  # インストールした discord.py

# 自作モジュール
import nessmado_basic
import NMconfig


client = discord.Client()  # 接続に使用するオブジェクト
nmconfig = NMconfig.NMConfig()

# ------------------------------------------------------
# ここからdiscordAPIの実行
# ------------------------------------------------------
# 起動時に通知してくれる処理
@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message):

    func_executer = nessmado_basic.FunctionExecuter(message, client)
    await func_executer.startFunction()
    print("処理終了")

# botの接続と起動
# （tokenにはbotアカウントのアクセストークンを入れてください）
client.run(nmconfig.TOKEN)

# -------------------ここでメイン終わり---------------------


# ------------------------------------------------------
# ここから落書き
# ------------------------------------------------------
'''
       # ユーザーリスト表示
        # リプライする場合message.contentにユーザーIDを含む
        if message.content.startswith('<@hogehoge> ユーザーリスト'):
            reply = f'{message.author.mention} ユーザーリストね〜' # 返信文の作成
            await client.send_message(message.channel, reply) # 返信を送る

            member_list = [
                member.display_name for member in client.get_all_members()]
            reply = member_list
        '''

'''
        # チャンネルリスト表示
        if message.content.startswith('<@hogehoge> チャンネルリスト'):
            reply = f'{message.author.mention} チャンネルリストね〜' # 返信文の作成
            await client.send_message(message.channel, reply) # 返信を送る

            channel_list = [str(channel)
                                for channel in client.get_all_channels()]
            reply = channel_list
        else :
            reply = f'{message.author.mention} はあい' # 返信文の作成
        await client.send_message(message.channel, reply) # 返信を送る
        '''

"""チャンネルをバーっと作るプログラム。今はいらない。
if message.content.startswith('!!!!!!!!!!mkch'):
        csv_file = open('all_chara.csv', 'r', newline='')
        reader = csv.reader(csv_file)
        for row in reader:
            for cell in row:
                channel_name = cell
                await client.create_channel(message.server, channel_name, type=discord.ChannelType.text)
                await client.send_message(message.channel, f'{channel_name} チャンネルを作成しました')

"""
