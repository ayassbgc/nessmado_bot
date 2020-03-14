# スクリプト名：NMconfig.py
# バージョン：5.0
# 作成日：2019/03/xx
# 最終更新日：2019/07/19
# 作成者：(へっへ)
# スクリプト概要：
# ｜classの説明に記載したため省略。
"""更新履歴
    2019/03/xx ver 3.1
    新規作成
    2019/07/19 ver 5.0
    対策スタンプメンバーを追加。
    2020/03/10 ver 6.0
    設定ファイル（NMconfig.ini）からもろもろ読み取ることにした。
    設定ファイルをいじればコードを知らなくても楽に値を変更できる。
    https://docs.python.org/ja/3/library/configparser.html
"""

import configparser


class NMConfig:
    """NMConfigクラス
    NessMadoConfigの略。
    Singleton（分からない場合はググる）のつもりで書いたクラス。
    Tokenとかその他諸々の環境による差分はここで吸収する。
    """

    def __init__(self):
        self.CONFIG_FILE_NAME = 'NMconfig.ini'
        self.S_DEFAULT = 'DEFAULT'
        self.S_MASTER_MODE = 'MASTER'
        self.S_TEST_MODE = 'TEST'

        self.config = configparser.ConfigParser()
        self.config.read(self.CONFIG_FILE_NAME)
        # -----------------------------------------------------------
        # 設定１：本番環境と試験環境の設定
        # -----------------------------------------------------------
        # ｜普通はどうかわからないがテストの環境と本番の環境を用意している場合は、
        # ｜このbe_testmodeの値を変更することでconfig的な設定を変えることができる。
        # ｜これにより変更する値はこのクラスで一括管理すると楽。
        # -----------------------------------------------------------
        # True:検証用、False:本番用
        self.be_testmode = self.config[self.S_DEFAULT].getboolean('BE_TEST')

        # -----------------------------------------------------------
        # 設定２：変数の設定
        # -----------------------------------------------------------
        # ｜サーバーごとにプライベートに変わってくるID等は一括で管理。
        # ｜ここの値を外部に公開するとサーバーを乗っ取られてしまうので
        # ｜そんなことはしてはいけない。
        # -----------------------------------------------------------
        self.TOKEN = ""
        self.ZATSUDAN_CHANNEL_ID = ""
        self.CHARACTER_TAISAKU_ID = ""  # 対策が英語だと"counterplan"って言うらしいが分かりにくいので
        self.MATCH_CHANNEL_ID = ""
        self.TAISAKU_STAMP = ""
        self.NESS_SKILL_CHANNEL_ID = ""
        self.STARVED_MATCHING = ""
        self.MYCHARACTER = ""

        if self.be_testmode:
            # テストサーバー用
            self._setConfig(self.S_TEST_MODE)
        else:
            # ネス窓本番
            self._setConfig(self.S_MASTER_MODE)

    def _setConfig(self, mode: str):
        self.TOKEN = self.config[mode].get('TOKEN')
        self.ZATSUDAN_CHANNEL_ID = self.config[mode].getint(
            'ZATSUDAN_CHANNEL_ID')
        self.CHARACTER_TAISAKU_ID = self.config[mode].getint(
            'CHARACTER_TAISAKU_ID')
        self.MATCH_CHANNEL_ID = self.config[mode].getint(
            'MATCH_CHANNEL_ID')
        self.TAISAKU_STAMP = self.config[mode].get('TAISAKU_STAMP')
        self.NESS_SKILL_CHANNEL_ID = self.config[mode].getint(
            'NESS_SKILL_CHANNEL_ID')  # 議論・相談1のチャンネル
        self.STARVED_MATCHING = self.config[mode].get(
            'STARVED_MATCHING')
