# スクリプト名：nessmado_function.py
# バージョン：5.0
# 作成日：2019/07/19
# 最終更新日：2019/07/19
# 作成者：(へっへ)
# スクリプト概要：
# ｜キャラ対策チャンネル（大元）に「/対策 [キャラ名]」から始まるメッセージを投稿すると、
# ｜各キャラ別の対策チャンネルで対策スタンプが押されたメッセージを取得し（過去500件分のメッセージから抽出）、
# ｜/対策 が書かれたチャンネルに票数でソートした順にメッセージを記載する。
# ｜
# ｜★キャラ窓の方へ
# ｜これを使う場合、nessmado_discord_manager.pyをちゃんとイジる必要があります。
# ｜具体的には、各チャンネル名を完全一致で取得してるので、例えば
# ｜・「No.1_マリオ」のようにキャラ名以外にもチャンネル名にNo.1_とか付けてる場合は
# ｜  上手いことをそれを外す処理を加える必要があります。正規表現を使うと良いと思います。
# ｜・そうじゃなく、キャラ名だけのチャンネル名になっている場合は
# ｜  例えばMr.Game&Watchなど（アルファベット？カタカナ？半角？全角？）と微妙に異なる場合が
# ｜  あるはずなので、そのへんの埋め合わせが必要です。
# ｜  窓側のチャンネル名を変更してもらうか、スクリプト記載内容を修正してもらうか。
# ｜・そこまでしてもらえれば、あとはNMconfig.iniにキャラ対策チャンネルのIDおよび作成した対策スタンプのIDを書き込み、
# ｜  nessmado_basicで本クラスのimportとFunctionGeneratorクラスのgenerateFunctionInstanceメソッドの
# ｜  コメントアウトを外せば使えます。
"""更新履歴
    2019/07/19 ver 5.0
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


class TaisakuMessageMaker(MessageMaker):
    def __init__(self):
        super(TaisakuMessageMaker, self).__init__()
        self.keyword = '/対策'
        self.HIS_MSG_LMT = 500  # ログのヒストリカル取得index数。今後使う機能用。
        self.be_character_name = False
        self.ch_manager = ChannelManager()

    async def _makeMessage(self, client, message, character_ch) -> str:
        asyncit_result = None
        fav_messages_and_counts = []  # ここに対策スタンプついてるメッセージの対策スタンプの数, メッセージの内容が格納される。
        historical_messages = await character_ch.history(limit=self.HIS_MSG_LMT).flatten()

        # 各メッセージについて、リアクション情報を取得
        for history_message in historical_messages:
            for reaction in history_message.reactions:
                # リアクションが対象の絵文字だったら、fav_messagesリストにメッセージの内容とスタンプの数を格納
                if str(reaction.emoji) == self.ch_manager.TAISAKU_STAMP:
                    fav_messages_and_counts.append(
                        [reaction.count, history_message.content])
        # fav_messagesをスタンプ多い順に並べ替える
        fav_messages_and_counts.sort(reverse=True)
        self.reply = str("【" + character_ch.name + "対策】")
        await message.channel.send(self.reply)
        for fav_count, fav_content in fav_messages_and_counts:
            asyncit_result = await message.channel.send("・" + fav_content + "、" + str(fav_count)+"票")
        return asyncit_result

    async def executeFunction(self, message, client) -> str:
        # await history()をbot.pyに直書きしている現在は、チャンネルと特定し、そのチャンネルを_makeMessageに渡すだけの関数。
        character_ch = self.specifyCharacter(message, client)
        if character_ch == None:
            return await message.channel.send("キャラ名が正しく入力されてません。\n「/対策 ○○(キャラ名)」で入力してください。")
        asyncit_result = await self._makeMessage(client, message, character_ch)
        return asyncit_result

    def specifyCharacter(self, message, client):
        # 全てのチャンネルについてfor文を回し、対策情報を取得したいキャラを特定する。
        # 処理として対象キャラのチャンネルでログを取得するためcharacter_chって変数名にしている。
        for character_ch in client.get_all_channels():
            # 以下if文について：
            # ひたすらにメッセージに記載されているキャラ名とチャンネル名の一致の有無を確認する。
            # チャンネル名称（＝キャラ名）がメッセージ内に含まれてたら、該当するキャラでの質問があった場合のメッセージ作成を実施する。
            if self.ch_manager.judgeNameContained(client, character_ch.name, message.content) \
                    and self.ch_manager.judgeFuzzyCharacterName(character_ch.name, message.content):
                self.be_character_name = True
                return character_ch
