# スクリプト名：ness_skill.py
# バージョン：5.0
# 作成日：2019/10/14
# 最終更新日：2019/10/14
# 作成者：(へっへ)
# スクリプト概要：
# ｜Nessskillクラス
# ｜「/脱初心者」「/初心者」「/中級者」「/上級者」と任意のページで打つと
# ｜議題・相談1（仮）内のメッセージでその文字で始まっているメッセージのログをまとめて出力する
# ｜
# ｜★キャラ窓の方へ
# ｜一時的に作っただけのクラスなので使えなくて良いです。参考までに載せます。
"""更新履歴
    2019/10/14 ver 5.0
    新規作成。
"""

import asyncio

# discordAPIモジュール
from discord import message
from discord import client
from discord import channel

# 自作モジュール
from MyMessageClass.message_maker import MessageMaker
from nessmado_discord_manager import ChannelManager


class NessSkill(MessageMaker):
    def __init__(self):
        self.keyword = '/ネススキル'
        self.HIS_MSG_LMT = 500  # ログのヒストリカル取得index数。今後使う機能用。
        self.ch_manager = ChannelManager()
        self.skill_ch_id = self.ch_manager.NESS_SKILL_CHANNEL_ID

    async def _makeMessage(self, client, message) -> str:
        asyncit_result = None
        nessskill_messages = []  # ここに実力毎のメッセージの内容が格納される。
        skill_ch = client.get_channel(self.skill_ch_id)
        historical_messages = await skill_ch.history(limit=self.HIS_MSG_LMT).flatten()

        # 各メッセージについて、リアクション情報を取得
        for history_message in historical_messages:
            if history_message.content.startswith('脱初心者'):
                nessskill_messages.append(history_message.content)
        for history_message in historical_messages:
            if history_message.content.startswith('初心者'):
                nessskill_messages.append(history_message.content)
        for history_message in historical_messages:
            if history_message.content.startswith('中級者'):
                nessskill_messages.append(history_message.content)
        for history_message in historical_messages:
            if history_message.content.startswith('上級者'):
                nessskill_messages.append(history_message.content)

        str_ness_skills = ""
        str_ness_skills = '\n'.join(nessskill_messages)

        # fav_messagesをスタンプ多い順に並べ替える
        self.reply = str("【ネス使い実力別スキル表】")
        await message.channel.send(self.reply)
        asyncit_result = await message.channel.send(str_ness_skills)
        return asyncit_result

    async def executeFunction(self, message, client) -> str:
        asyncit_result = await self._makeMessage(client, message)
        return asyncit_result
