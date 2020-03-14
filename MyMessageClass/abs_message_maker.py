# スクリプト名：abs_message_maker.py
# バージョン：6.0
# 作成日：2020/03/10
# 最終更新日：-
# 作成者：(へっへ)
# スクリプト概要：
# ｜インターフェースを使ってみたかったから抽象クラスを実装。
# ｜MessageMakerが子クラスとなる。
"""更新履歴
    2020/03/10 ver 6.0
    新規作成
    
"""

from abc import ABCMeta
from abc import ABCMeta, abstractmethod

from discord import message
from discord import client


class AbsMessageMaker(metaclass=ABCMeta):
    """メッセージを作成するMessageMakerクラスの抽象クラス"""

    @abstractmethod
    def executeFunction(self):
        pass

    @abstractmethod
    def _makeMessage(self):
        pass
