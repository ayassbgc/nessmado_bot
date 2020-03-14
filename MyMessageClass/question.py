# スクリプト名：nessmado_function.py
# バージョン：5.0
# 作成日：2019/03/xx
# 最終更新日：2019/07/19
# 作成者：(へっへ)
# スクリプト概要：
# ｜キャラ対策チャンネル（大元）に「質問」から始まるメッセージを投稿すると、
# ｜各キャラ別の対策チャンネルに文言をコピーした上で、
# ｜大元のキャラ対策チャンネルと雑談チャンネルに周知メッセージを送る。
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
# ｜・そこまでしてもらえれば、あとはNMconfig.iniにキャラ対策チャンネルのIDを書き込み、
# ｜  nessmado_basicで本クラスのimportとFunctionGeneratorクラスのgenerateFunctionInstanceメソッドの
# ｜  コメントアウトを外せば使えます。

"""更新履歴
    2019/03/xx ver 3.1
    新規作成
    2019/07/19 ver 5.0
    makeMessageをasync/awaitに仕様変更
"""


# discordAPIモジュール
from discord import message
from discord import client
from discord import channel

# 自作モジュール
from MyMessageClass.message_maker import MessageMaker
from nessmado_discord_manager import ChannelManager


class QuestionMessageMaker(MessageMaker):
    def __init__(self):
        super(QuestionMessageMaker, self).__init__()
        self.keyword = '質問'
        self.l_reply = []
        self.output_replies = []
        self.message_pattern = 0
        self.be_character_name = False
        self.ch_manager = ChannelManager()
        self.keychannel = self.ch_manager.CHARACTER_TAISAKU_ID

    async def _makeMessage(self, message, client, channel=None) -> str:
        # 長い関数なので構成を文章で説明
        # ｜_makeMessageでは全部で3パターンに分けてメッセージを作成する。
        # ｜パターン1：正常な場合。スクリプト概要に記載された処理が走る。
        # ｜パターン2：メッセージが「質問」から始まっていない場合。ちゃんと書いてほしい旨のメッセージを作成する。
        # ｜パターン3：質問から始められているが、キャラ名がキチンとかけていない場合。
        # ｜         キャラ名ちゃんと書いてねって旨のメッセージが作成される。
        asyncio_result = None

        # パターン1：質問が適切な場合
        if self.message_pattern == 0:
            # 1-1：キャラ対策チャンネルと雑談チャンネルに質問が着たことを周知するためのメッセージの作成
            self.l_reply.append(f'{channel.mention}  で質問がきたよ')
            for i in range(len(self.l_reply)):
                self.reply += self.l_reply[i]
            self.output_replies.append(
                [client.get_channel(self.ch_manager.CHARACTER_TAISAKU_ID), self.reply])
            self.output_replies.append(
                [client.get_channel(self.ch_manager.ZATSUDAN_CHANNEL_ID), self.reply])

            # 1-2：対象キャラのキャラ対策ページ用のメッセージを作成するにあたり、変数をクリア。
            self.l_reply.clear()
            self.reply = ""

            # 1-3：質問が着たキャラのキャラ対策チャンネルに質問内容をコピペするためのメッセージを作成。
            self.l_reply.append(f'{message.author.mention} からの質問\n')
            self.l_reply.append(message.content)
            for tmp_reply in self.l_reply:
                self.reply += tmp_reply
            self.output_replies.append(
                [client.get_channel(channel.id), self.reply])

        # パターン2：メッセージが「質問」から始まっていない場合。
        if self.message_pattern == -1:
            self.l_reply.append(f'{message.author.mention} エラー！\n')
            self.l_reply.append('「質問です。○○（キャラ名）について〜」の形で書いてね。')
            for i in range(len(self.l_reply)):
                self.reply += self.l_reply[i]
            self.output_replies.append(
                [client.get_channel(self.ch_manager.CHARACTER_TAISAKU_ID), self.reply])

        # パターン3：質問から始められているが、キャラ名がキチンとかけていない場合
        if self.message_pattern == -2:
            self.l_reply.append(f'{message.author.mention} エラー！\n')
            self.l_reply.append('何のキャラの質問か分からないよ\n')
            self.l_reply.append('「質問です。○○（キャラ名）について〜」の形で書いてね。')
            for i in range(len(self.l_reply)):
                self.reply += self.l_reply[i]
            self.output_replies.append(
                [client.get_channel(self.ch_manager.CHARACTER_TAISAKU_ID), self.reply])

        for reply_channel, reply_content in self.output_replies:
            #print("message.channel:" + str(message.channel))
            asyncio_result = await reply_channel.send(reply_content)
        return asyncio_result

    async def executeFunction(self, message, client) -> str:
        asyncio_result = None
        # 「質問」から始まってなかったら -1 パターンのメッセージを作成
        if not message.content.startswith(self.keyword):
            self.message_pattern = -1
            asyncio_result = await self._makeMessage(message, client)
            return asyncio_result

        # TO:DO ここ関数化すべき。何のためにこれを書いてるのかがぱっと見でわからん。
        if not message.channel.id == self.keychannel:
            return None

        # 全てのチャンネルについてfor文を回し、質問の内容に該当するキャラがいないか調べる。
        for character_ch in client.get_all_channels():
            # 以下if文について：
            # ひたすらにメッセージに記載されているキャラ名とチャンネル名の一致の有無を確認する。
            # チャンネル名称（＝キャラ名）がメッセージ内に含まれてたら、該当するキャラでの質問があった場合のメッセージ作成を実施する。

            # ★各キャラ窓へ①
            # 以下if文の条件にあるcharacter_ch.nameがチャンネル名称です。
            # client.get_all_channels()を使用していることからキャラ対策以外のチャンネル名も
            # 取得してきてしまうので、キャラ対策以外のチャンネルで「キャラクター名称を含むチャンネル名」が
            # 存在する場合『もし「_対」の文言が含まれていたら』といったような条件付けも必要だと思います。
            # print(character_ch.name)
            if self.ch_manager.judgeNameContained(client, character_ch.name, message.content) \
                    and self.ch_manager.judgeFuzzyCharacterName(character_ch.name, message.content):
                self.be_character_name = True
                asyncio_result = await self._makeMessage(message, client, character_ch)
                return asyncio_result

        # 対策したいキャラが見つからなかったら -2 パターンのメッセージを作成
        if not self.be_character_name:
            self.message_pattern = -2
        asyncio_result = await self._makeMessage(message, client)
        return asyncio_result

    def checkTriggers(self, message) -> bool:
        if self._checkKeyword(message) or self._checkChannelMessageWritten(message):
            return True
        return False
