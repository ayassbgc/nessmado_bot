# スクリプト名：nessmado_function.py
# バージョン：5.0
# 作成日：2019/03/xx
# 最終更新日：2019/07/31
# 作成者：(へっへ)
# スクリプト概要：
# ｜ネス窓の機能群を使用するにあたり、それらのインターフェースとなるクラス群が記載されているスクリプト。
# ｜メッセージを受信したら、メッセージの内容を読み取り、必要に応じた機能クラスを使用する。
# ｜
# ｜備考
# ｜現在は「受信したメッセージに対して何かしらのリアクションを返す」という機能のみだが、
# ｜今後はトリガーをスタンプとした機能なども作成していく予定。
#
# 以下開発者用
# 新機能実装方法：
# ｜新機能を開発したら
# ｜    ①新しいクラスを本スクリプトファイルにimportする
# ｜    ②新しいクラスを本スクリプトファイルに記載の
# ｜      FunctionGeneratorクラスのgenerateFunctionInstanceメソッドに追加する。
# ｜①②のやり方はここにある既存のものを参考にして追加すること。
#
# 注意点：
# ｜メッセージを受信し、それが該当するメッセージかどうかの判別にMessageMakerクラスを使用している。
# ｜新機能を開発する場合は、インターフェースとしてMessageMakerを継承したクラスを作成し、
# ｜その継承したクラスから新機能を実行させること。
"""更新履歴
    2019/03/xx ver 3.0?覚えてない。
    オブジェクト指向に沿ってクラス化。
    2019/07/31 Ver 5.0
    asyncioに完全に沿わせるためにサブジェネレータをasync文に書き直してAwaitableにした
    （使い方あってるのか？これ）
"""

# discortAPI
from discord import message
from discord import client

# ネス窓の共通クラス
from nessmado_discord_manager import ChannelManager

# 機能クラス
# 新しいクラスを作ったらここでimportする
from MyMessageClass.ness_mado_message_maker import PapaMessageMaker
from MyMessageClass.ness_mado_message_maker import MamaMessageMaker
from MyMessageClass.ness_mado_message_maker import ObasanMessageMaker
from MyMessageClass.ness_mado_message_maker import FlyingmanMessageMaker
from MyMessageClass.ness_mado_message_maker import DoseisanMessageMaker
from MyMessageClass.ness_mado_message_maker import EscargotMessageMaker
from MyMessageClass.ness_mado_message_maker import FsannMessageMaker
from MyMessageClass.ness_mado_message_maker import NessOugiMessageMaker
#from MyMessageClass.question import QuestionMessageMaker
#from MyMessageClass.taisaku import TaisakuMessageMaker
#from MyMessageClass.match import AnnounceMatchMessageMaker
#from MyMessageClass.ness_skill import NessSkill


class FunctionExecuter:
    """FunctionExecuter
        discordで使用する機能クラスを実行するクラス
        FunctionSelecter関数を内包し、これを使って使用する機能を選択する。
        ▼本クラスの使い方
        ・bot.pyにインスタンスを生成
        ・startFunctionで実行。
    """

    def __init__(self, message, client):
        self.message = message
        self.client = client
        self.ch_manager = ChannelManager()
        self.func_selecter = FunctionSelecter(message, client)
        self.function_instance = None

    async def startFunction(self) -> str:
        if self.checkMessageFromRobot():
            return None
        self.function_instance = self.func_selecter.selectFunctionClass()
        if self.function_instance:
            asynciot_result = await self.function_instance.executeFunction(
                self.message, self.client)
            return asynciot_result
        return None

    def checkMessageFromRobot(self):
        if self.message.author.id == self.client.user.id:
            return True
        return False


class FunctionSelecter:
    """FunctionSelecter
        messageを読み取り、実行すべき機能を選択する。
        FunctionExecuterクラスのメンバオブジェクトとして使用する。
    """

    def __init__(self, message, client):
        self.message = message
        self.client = client

    def selectFunctionClass(self) -> 'class':
        func_generator = FunctionGenerator()
        for f_instance in func_generator.generateFunctionInstance():
            if f_instance.checkTriggers(self.message):
                return f_instance
        return None


class FunctionGenerator:
    """FunctionGenerator
        使用する機能クラス群を生成するクラス。
        使用する候補のクラスを全て保持するとメモリ負荷がやばくなるかもしれないので、
        クラスの生成手法にはジェネレーターを採用。
        使用したいクラスをFunctionSelecterに逐一生成し、渡すことでメモリ負担を減らす。
        （この考慮が必要かどうかを測ったりはしていない）
    """

    def __init__(self):
        pass

    # 新しいクラスを作ったらここでインスタンスを渡す。
    def generateFunctionInstance(self):
        yield PapaMessageMaker()
        yield ObasanMessageMaker()
        yield MamaMessageMaker()
        yield FlyingmanMessageMaker()
        yield DoseisanMessageMaker()
        yield EscargotMessageMaker()
        yield FsannMessageMaker()
        yield NessOugiMessageMaker()
#        yield QuestionMessageMaker()
#        yield TaisakuMessageMaker()
#        yield AnnounceMatchMessageMaker()
#        yield NessSkill()
