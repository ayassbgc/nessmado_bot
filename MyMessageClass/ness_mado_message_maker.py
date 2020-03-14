# スクリプト名：ness_mado_message_maker.py
# バージョン：3.1
# 作成日：2019/03/xx
# 最終更新日：2019/05/13
# 作成者：(へっへ)
# スクリプト概要：
# ｜任意のメッセージに対して、何かしらの返信をするお遊び用の機能群。
# ｜motherシリーズやネス窓にゆかりのある名言（迷言）の返事がくる。
#
# 使い方
# ｜ここにある内容を見て、それに習って書く。パパとママを見ればそれで良い。
# ｜作ったら、nessmado_function.pyに使い方を見て、必要な情報を入れる。
# ｜そこまでできたら使えるようになってる。以上。

from MyMessageClass.message_maker import MessageMaker
import random


"""更新履歴
    2019/03/xx ver 3.1?覚えてない。
    オブジェクト指向に沿ってクラス化。
"""


class NessMadoMessageMaker(MessageMaker):
    pass


class PapaMessageMaker(MessageMaker):
    """パパのメッセージを作成するクラス"""

    def __init__(self):
        super(PapaMessageMaker, self).__init__()
        self.keyword = '/パパ'
        self.reply = 'ママに似てがんばり屋だなあ。無理するなよ。'


class MamaMessageMaker(MessageMaker):
    """ママのメッセージを作成するクラス"""

    # ★__init__でごちゃごちゃ書いている理由
    # 関数の名前の観点からmakeMessageメンバ関数をオーバーライドすべきでは？と思うが、
    # 本クラス群では現状で__init__で一通り作ってしまった方が運用しやすい
    # (=ここのクラス群は__init__さえいじれば他は変えなくて良い）ので、この方針で進める。
    def __init__(self):
        super(MamaMessageMaker, self).__init__()
        self.keyword = '/ママ'
        self.l_reply = []
        self.l_reply.append('「おかえり、ネス。\n')
        self.l_reply.append('    何も言わなくてもいいの。ママはわかってるつもりよ。\n')
        self.l_reply.append('    ずいぶん疲れてるようだし、ハンバーグを食べておやすみ。チュッ！」')
        for i in range(len(self.l_reply)):
            self.reply += self.l_reply[i]


class ObasanMessageMaker(MessageMaker):
    """おばさんのメッセージを作成するクラス"""

    def __init__(self):
        super(ObasanMessageMaker, self).__init__()
        self.keyword = '/おばさん'
        self.reply = ' ◆キイイー！　こうるさい ハエだよ！　しんで じごくへいけ！！'


class FlyingmanMessageMaker(MessageMaker):
    """フライングマンのメッセージを作成するクラス"""

    def __init__(self):
        super(FlyingmanMessageMaker, self).__init__()
        self.keyword = '/フライングマン'
        self.reply = ' わたしは あなたの ゆうき。あなたに ついてゆきます。…なまえ? フライングマンとでも いっておきましょうか。'


class DoseisanMessageMaker(MessageMaker):
    """どせいさんのメッセージを作成するクラス"""

    def __init__(self):
        super(DoseisanMessageMaker, self).__init__()
        self.keyword = '/どせいさん'
        self.reply = ' なにかむずかしいことをかんがえよう。これからのぼくは。'


class EscargotMessageMaker(MessageMaker):
    """エスカルゴ運送のメッセージを作成するクラス"""

    def __init__(self):
        super(EscargotMessageMaker, self).__init__()
        self.keyword = '/エスカルゴ'
        self.reply = ' エスカルゴ運送でーす！お預かり料金は１８ドルです。お金持ってますよね？'


class FsannMessageMaker(MessageMaker):
    """Fsannのメッセージを作成するクラス"""

    def __init__(self):
        super(FsannMessageMaker, self).__init__()
        self.keyword = '/Fsann'
        self.reply = ' 神に感謝'


class NessOugiMessageMaker(MessageMaker):
    def __init__(self):
        super(NessOugiMessageMaker, self).__init__()
        self.keyword = '/ネス奥義'
        # 参考：ネス奥義公式サイトおよびTwitterネス奥義アカウント
        # 2020/3/12時点で83種類。最近のは取りこぼしあるかも。
        self.l_nessougi = ['殺', '朧', '命', '雫', '薊',
                           '芥', '閃', '雷雲', '不知火', '早咲きの薔薇',
                           'クロスPKファイアー', 'チェイスPKファイアー', 'エイリアンPKファイアー（旧名 アブソードPKファイアー、くつした）', 'PKファイアージャンプ', '裏PKファイアージャンプ',
                           '焔・ホームラン', '食い逃げ', '完全に停止したハニワは吸収できる。知らなかったのか？', 'スタッカート', '背中で語る',
                           '雀の涙', 'たびゴマフラッシュ', '阿修羅飯綱落ち', 'Infinity ∞ Sign', 'Uroboros Exhale',
                           'Final Dive', 'Ishtar Drive', 'Eclipse End', 'Fate Reload', 'Orion Imagine',
                           '銀河鉄道YAMANOTE', 'とうごうアタック', 'PKサヨナラ', 'パイク・オブ・アブソリュート', '椿',
                           'おもてなし', '少年院ヘッドバッド（旧名 βストライク）', '河童の川流れ', 'オイルパニック', '無拍子',
                           'ヘル・アンド・ヘヴン', 'ノアの方舟', 'リリパットステップ', '裏シャトル', '崖の上のポニョ',
                           'お天道様は見ておるぞ', 'だるまさんがころんだ', 'かなまる', 'かなまる改', 'かなまる隼',
                           'かなまるファントム', 'Final Time', 'EarthBound', 'クロノス・サンダー', 'エフランエンディカルバースト（略称 FEB）',
                           'ファイナルうんちバズーカ', 'うめきレインボー', '逆さ富士描き', 'ディヴァイン・ブラスト', 'とどかぬ翼',
                           'はんげきのサイコシールド', '朱赤の盾', '太陽の牢獄', '切断（旧名 トロコンクエスト）', 'PKカケヒキ',
                           '闇', '場外ファウル', 'チェックザアンサー', '一本釣り', 'フォーリングPKフラッシュ',
                           'ハッケヨ～イ・ノコッタノコッタ', '今日も陽は落ちる', '鯖折り', 'ボンバーマン参戦', '太陽心酔',
                           'アヤメ返し', '滝登り', '忍', '108マシンガン', 'ネス使い',
                           'タイタニック','野原しんのすけ','PKジェットコースター衝撃映像',
                           ]
        self.reply = random.choice(self.l_nessougi)
