# スクリプト名：match.py
# バージョン：5.0
# 作成日：2019/07/21
# 最終更新日：2019/10/14
# 作成者：(へっへ)
# スクリプト概要：
# ｜AnnounceMatchクラス
# ｜対戦募集チャンネルで「対戦募集」から始まるメッセージを入力すると
# ｜雑談チャンネルに対戦募集の周知をする
# ｜
# ｜★キャラ窓の方へ
# ｜NMconfig.iniに対戦募集用のチャンネルIDと、対戦募集用の役職IDを書き込めば使えます。
# ｜使う場合はnessmado_basicで本クラスのimportとFunctionGeneratorクラスのgenerateFunctionInstanceメソッドの
# ｜コメントアウトを外してください。
"""更新履歴
    2019/07/21 ver 5.0
    新規作成。
    2019/10/14 ver 5.1
    sterved_matchingを最新のロールIDに修正。
"""


# discordAPIモジュール
from discord import message
from discord import client
from discord import channel

# 自作モジュール
from MyMessageClass.message_maker import MessageMaker
from nessmado_discord_manager import ChannelManager


class AnnounceMatchMessageMaker(MessageMaker):
    def __init__(self):
        super(AnnounceMatchMessageMaker, self).__init__()
        self.keyword = '対戦募集'
        self.output_replies = []
        self.message_pattern = 0
        self.ch_manager = ChannelManager()
        self.keychannel = self.ch_manager.MATCH_CHANNEL_ID
        print(type(self.keychannel))
        self.starved_matching = self.ch_manager.STARVED_MATCHING

    async def _makeMessage(self, message, client, channel=None) -> str:
        asyncio_result = None
        if self.message_pattern == -1:
            return asyncio_result
        if self.message_pattern == 0:
            self.reply = f'{message.author.mention} さんが対戦募集を開始しました。 {self.starved_matching}\n \
                参加したい方はこちらから→{message.channel.mention}  \n'
        self.output_replies.append(
            [client.get_channel(self.ch_manager.ZATSUDAN_CHANNEL_ID), self.reply])
        for reply_channel, reply_content in self.output_replies:
            asyncio_result = await reply_channel.send(reply_content)
        return asyncio_result

    async def executeFunction(self, message, client) -> str:
        asyncio_result = None
        # 「対戦募集」から始まってなかったら -1 パターンのメッセージを作成
        if not message.content.startswith(self.keyword):
            self.message_pattern = -1
            asyncio_result = await self._makeMessage(message, client)
            return asyncio_result
        # 対戦募集チャンネル「以外」でのメッセージはスルーする。
        if message.channel.id == self.keychannel:
            asyncio_result = await self._makeMessage(message, client)
        return asyncio_result

    def checkTriggers(self, message) -> bool:
        if self._checkKeyword(message) or self._checkChannelMessageWritten(message):
            return True
        return False