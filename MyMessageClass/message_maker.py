# スクリプト名：message_maker.py
# バージョン：5.0
# 作成日：2019/03/xx
# 最終更新日：2019/07/31
# 作成者：(へっへ)
# スクリプト概要：
# ｜新機能を開発するにあたり、基底とするクラス。
# ｜基本的にここに記載されているメンバ関数をいじる。
# ｜ただし、メッセージを出力させるだけといった簡単な機能の場合は__init__くらいしかいじらなくてもよい。
"""更新履歴
    2019/03/xx ver 3.1?覚えてない。
    オブジェクト指向に沿ってクラス化。
    2019/07/31 Ver 5.0
    asyncioに完全に沿わせるためにサブジェネレータをasync文に書き直してAwaitableにした
    （言葉の使い方あってるのか？これ）
    2020/03/10 ABCモジュール実装
"""

from discord import message
from discord import client
from MyMessageClass.abs_message_maker import AbsMessageMaker


class MessageMaker(AbsMessageMaker):
    """メッセージを作成する基底クラス
        absMessageMakerから直接いろんなMessageMakerに飛ばないのは
        オーバーライドさせたかったから。
        ness_mado_message_maker.pyを見てもらうとわかるが、
        このクラスを継承すれば変数に値を入れるだけでbotが反応するようにしてある。
    """

    def __init__(self):
        # -----------------------------------------------------------
        #  __init()__
        # -----------------------------------------------------------
        # ｜役割
        # ｜・変数の設定、代入をする。botの動作を試すだけなら、作成したクラスの__init()__の値をいじれば動きます。
        # ｜  ness_mado_message_maker.pyを参考に作ってもらえれば良いと思います。
        # ｜
        # -----------------------------------------------------------
        #  変数について
        # -----------------------------------------------------------
        # ｜keyword   : string型。ここに入れた文字から始まるメッセージが投稿されたらreplyに入る文字が返される。
        # ｜            基本的には文字の頭に「/」とか「|」とか付けて普通の会話で反応しないようにするのが良い。
        # ｜keychannel: int型。オプションみたいなもの。keywordから始まるメッセージについて、
        # ｜            「このチャンネルで投稿されたら」という条件を加えたい場合にkeychannelに値を代入する。
        # ｜            keychannelには対象としたいチャンネルのチャンネルIDを入れる。
        # ｜            keychannelの値はNMconfig.pyとNMconfig.iniをいじって入れた方が後々楽だけどどっちでもよい。
        # ｜reply     : string型。botが返すメッセージを入れる。
        # -----------------------------------------------------------
        self.keyword = ''
        self.keychannel = 0
        self.reply = ''

    async def executeFunction(self, message, clinet) -> str:
        # -----------------------------------------------------------
        #  executeFunction()
        # -----------------------------------------------------------
        # ｜役割
        # ｜・この次に書かれてる_makeMessage()メソッドを実行すること
        # ｜・その他諸々の処理（追加条件など）を加えたい場合にここに記述する。
        # ｜  question.pyやtaisaku.pyなどを見てもらえばと思います。
        # -----------------------------------------------------------
        asyncio_result = await self._makeMessage(message)
        return asyncio_result

    async def _makeMessage(self, message) -> str:
        # -----------------------------------------------------------
        #  _makeMessage()
        # -----------------------------------------------------------
        # ｜役割
        # ｜・この次に書かれてる_makeMessage()メソッドを実行すること
        # ｜・その他諸々の処理（追加条件など）を加えたい場合にここに記述する。
        # ｜  question.pyやtaisaku.pyなどを見てもらえばと思います。
        # -----------------------------------------------------------
        asyncio_result = await message.channel.send(self.reply)
        return asyncio_result

    def checkTriggers(self, message) -> bool:
        # -----------------------------------------------------------
        #  checkTriggers()
        # -----------------------------------------------------------
        # ｜役割
        # ｜・メッセージがkeywordから始まっているかをチェックする_checkKeyword()メソッドを返します。
        # ｜・それ以外にも特定のチャンネルからのメッセージかを判断する_checkChannelMessageWritten()メソッドを
        # ｜  条件に加えたい場合は、継承先の小クラス側でオーバーライドさせます。これについては
        # ｜  question.pyやtaisaku.pyなどを見てもらえばと思います。
        # -----------------------------------------------------------
        return self._checkKeyword(message)

    def _checkKeyword(self, message) -> bool:
        if message.content.startswith(self.keyword):
            return True
        return False

    def _checkChannelMessageWritten(self, message) -> bool:
        if message.channel.id == self.keychannel:
            return True
        return False
