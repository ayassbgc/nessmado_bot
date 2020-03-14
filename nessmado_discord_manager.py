# スクリプト名：nessmado_function.py
# バージョン：5.01
# 作成日：2019/03/xx
# 最終更新日：2019/10/14
# 作成者：(へっへ)
# スクリプト概要：
# ｜キャラ対策チャンネル（大元）に「質問」から始まるメッセージを投稿すると、
# ｜各キャラ別の対策チャンネルに文言をコピーした上で、
# ｜大元のキャラ対策チャンネルと雑談チャンネルに周知メッセージを送る。
"""更新履歴
    2019/03/xx ver 3.0?覚えてない。
    オブジェクト指向に沿ってクラス化。
    2019/07/31 Ver 5.0
    勇者追加。
    2019/10/14 Ver 5.1
    バンカズ追加。
    NESS_SKILLクラス考慮。
"""


# discordAPIモジュール
from discord import message
from discord import client
from discord import channel

# 自作モジュール
from NMconfig import NMConfig


class ChannelManager:
    def __init__(self):
        self.nmconfig = NMConfig()
        self.TOKEN = ""
        self.ZATSUDAN_CHANNEL_ID = ""
        self.CHARACTER_TAISAKU_ID = ""  # 「対策」は英語で"counterplan"って言うらしいが分かりにくいので
        self.MATCH_CHANNEL_ID = ""
        self.TAISAKU_STAMP = ""
        self.NESS_SKILL_CHANNEL_ID = ""
        self.STARVED_MATCHING = ""
        self.MYCHARACTER = ""

        self.inputConfig()

    def inputConfig(self):
        self.TOKEN = self.nmconfig.TOKEN
        self.ZATSUDAN_CHANNEL_ID = self.nmconfig.ZATSUDAN_CHANNEL_ID
        self.CHARACTER_TAISAKU_ID = self.nmconfig.CHARACTER_TAISAKU_ID
        self.MATCH_CHANNEL_ID = self.nmconfig.MATCH_CHANNEL_ID
        self.TAISAKU_STAMP = self.nmconfig.TAISAKU_STAMP
        self.NESS_SKILL_CHANNEL_ID = self.nmconfig.NESS_SKILL_CHANNEL_ID
        self.STARVED_MATCHING = self.nmconfig.STARVED_MATCHING
        self.MYCHARACTER = self.nmconfig.MYCHARACTER

    def judgeNameContained(self, client, ch_name, content) -> bool:
        """
        キャラクター名について、包括してしまっている名前はいい感じに振り分けしてくれる処理。
        TO:DO本当はさ、もっとスッキリ書けることなんてわかってるんだよ。でもさ、メンドかったんだよ。許してくれな。
        """
        if ch_name == 'マリオ':
            if ('ドクター' in content) or ('Dr' in content) or ('dr' in content):
                return False
        elif ch_name == 'ファルコ':
            if 'ファルコン' in content:
                return False
        elif ch_name == 'クッパ':
            if ('ジュニア' in content) or ('Jr' in content) or ('jr' in content):
                return False
        elif ch_name == 'ピット':
            if ('ブラック' in content):
                return False
        elif ch_name == self.MYCHARACTER:
            if self._judgeMyCharacterNameContained(client, ch_name, content):
                return False
        return True

    def _judgeMyCharacterNameContained(self, client, ch_name, content) -> bool:
        all_channels = client.get_all_channels()
        for channel in all_channels:
            if channel.name == ch_name:
                continue
            elif (channel.name in content):
                return True
        return False

    def judgeFuzzyCharacterName(self, ch_name: str, content: str):
        """
        質問対象のキャラに対して、質問が投下されるべきチャンネルがどれなのかを
        メッセージのキャラ名とキャラクター毎の対策チャンネル名を見比べることで判別している。
        ただ、窓民が質問メッセージを書く際に、キャラクターの名前が微妙にチャンネル名と違っちゃう場合が
        出てくることが予測される。その名前の差分を力ずくで補完してくれる関数がこいつである。
        TO:DO 本当はさ、もっとスッキリ書けることなんてわかってるんだよ。でもさ、メンドかったんだよ。許してくれな。
        """

        # ★各キャラ窓へ③
        # ｜ch_nameがチャンネル名称からキャラ名を抽出したものです。
        # ｜各キャラ窓のサーバーに適用させる場合、
        # ｜1. if ch_name == 〜の行のキャラ名をチャンネル名称のキャラ名に合わせる
        # ｜2. ネス窓ではポケトレは１つのチャンネルで対応しているので、これを分ける
        # ｜   （分けるに当たり、他の関数も変えるといったことは不要なはずです）
        # ｜3. ネス窓ではMiiファイター用の対策チャンネルを作成していないので、これを作る
        #     （作るに当たり、他の関数も変えるといったことは不要なはずです）
        if ch_name in content:
            return True
        if ch_name == "ドクマリ":
            if ('ドクター' in content) or ('Dr' in content) or ('dr' in content) or ('医者' in content):
                return True
        if ch_name == "ロゼッタ＆チコ":
            if ('ロゼチコ' in content) or ('ロゼッタ' in content):
                return True
        if ch_name == "クッパjr":
            if ('ジュニア' in content) or ('Jr' in content) or ('jr' in content):
                return True
        if ch_name == "パックンフラワー":
            if ('パックン' in content) or ('花' in content):
                return True
        if ch_name == "ドンキーコング":
            if ('DK' in content) or ('D.K.' in content) or ('D.K' in content) or ('ドンキー' in content) or ('ゴリラ' in content):
                return True
        if ch_name == "ディディーコング":
            if ('DD' in content) or ('D.D.' in content) or ('D.D' in content) or ('ディディー' in content) or ('猿' in content):
                return True
        if ch_name == "キングクルール":
            if ('クルール' in content) or ('鰐' in content) or ('ワニ' in content):
                return True
        if ch_name == "ガノンドロフ":
            if ('ガノン' in content) or ('おじさん' in content):
                return True
        if ch_name == "ヤングリンク":
            if ('ヤンリン' in content) or ('こどもリンク' in content) or ('子どもリンク' in content) or ('子供リンク' in content):
                return True
        if ch_name == "トゥーンリンク":
            if ('トリン' in content):
                return True
        if ch_name == "ダークサムス":
            if ('ダムス' in content):
                return True
        if ch_name == "ゼロスーツサムス":
            if ('ダムス' in content) or ('ゼロサム' in content) or ('ZSS' in content) or ('ゼロスーツ・サムス' in content):
                return True
        if ch_name == "ピチュー":
            if ('ピチュカス' in content):
                return True
        if ch_name == "ミュウツー":
            if ('M2' in content) or ('m2' in content):
                return True
        if ch_name == "ポケモントレーナー":
            if ('ポケモン・トレーナー' in content) or ('ポケトレ' in content) or ('ゼニガメ' in content) \
                    or ('フシギソウ' in content) or ('リザードン' in content) or ('リザ' in content):
                return True
        if ch_name == "ゲッコウガ":
            if ('蛙' in content):
                return True
        if ch_name == "メタナイト":
            if ('メタ' in content):
                return True
        if ch_name == "デデデ":
            if ('デデデ大王' in content):
                return True
        if ch_name == "フォックス":
            if ('狐' in content):
                return True
        if ch_name == "ブラックピット":
            if ('ブラック・ピット' in content) or ('ブラピ' in content):
                return True
        if ch_name == "むらびと":
            if ('ムラビト' in content) or ('村人' in content):
                return True
        if ch_name == "アイスクライマー":
            if ('アイス・クライマー' in content) or ('アイクラ' in content):
                return True
        if ch_name == "インクリング":
            if ('スプラゥーン' in content) or ('インリン' in content) or ('イカちゃん' in content) \
                    or ('いかちゃん' in content) or ('烏賊' in content) or ('イカ' in content):
                return True
        if ch_name == "キャプテン・ファルコン":
            if ('ファルコン' in content) or ('キャプテンファルコン' in content) or ('CF' in content) \
                    or ('C.F' in content) or ('cf' in content) or ('c.f' in content):
                return True
        if ch_name == "ダックハント":
            if ('ダック・ハント' in content) or ('犬' in content):
                return True
        if ch_name == "ピクミン＆オリマー":
            if ('ピクミン&オリマー' in content) or ('ピクオリ' in content) or ('ピクミン' in content) or ('オリマー' in content):
                return True
        if ch_name == "リトル・マック":
            if ('リトルマック' in content) or ('マック' in content) or ('トルマク' in content):
                return True
        if ch_name == "ロボット":
            if ('ロボ' in content):
                return True
        if ch_name == "mrゲーム＆ウォッチ":
            if ('ゲムヲ' in content) or ('ゲムオ' in content) or ('ミスター' in content) \
                    or ('ゲーム&ウォッチ' in content) or ('ゲーム&ウォッチ' in content):
                return True
        if ch_name == "wii-fitトレーナー":
            if ('フィットレ' in content) or ('Wii Fit' in content) or ('wii fit' in content) \
                    or ('Wii fit' in content) or ('wii Fit' in content) or ('Wii-Fit' in content) or ('wii-fit' in content) \
                    or ('Wii-fit' in content) or ('wii-Fit' in content)or ('wii-Fit' in content) \
                    or ('tトレーナー' in content)or ('Tトレーナー' in content) or ('t トレーナー' in content)or ('T トレーナー' in content):
                return True
        if ch_name == "パックマン":
            if ('金玉' in content):
                return True
        if ch_name == "ベヨネッタ":
            if ('ベヨ' in content):
                return True
        if ch_name == "ロックマン":
            if ('ロック' in content) or ('岩男' in content):
                return True
        if ch_name == "ジョーカー":
            if ('ペルソナ' in content):
                return True
        if ch_name == "格闘mii":
            if ('格闘Mii' in content) or ('格闘MII' in content):
                return True
        if ch_name == "剣術mii":
            if ('剣術Mii' in content) or ('剣術MII' in content):
                return True
        if ch_name == "射撃mii":
            if ('射撃Mii' in content) or ('射撃MII' in content) or ('シャゲミ' in content):
                return True
        if ch_name == "勇者":
            if ('HERO' in content) or ('hero' in content) or ('Hero' in content) \
                    or ('HELO' in content) or ('helo' in content) or ('Helo' in content) \
                    or ('ゆうしゃ' in content) or ('ユウシャ' in content) or ('ゆーしゃ' in content) \
                    or ('ユーシャ' in content) or ('ひーろー' in content) or ('ヒーロー' in content) \
                    or ('よしひこ' in content) or ('ヨシヒコ' in content):
                return True
        if ch_name == "バンジョー＆カズーイ":
            if ('バンジョー&カズーイ' in content) or ('バンジョーとカズーイ' in content) or ('バンカズ' in content) \
                    or ('バンジョー' in content) or ('カズーイ' in content):
                return True
        if ch_name == "ベレスト":
            if ('ベレス' in content) or ('ベレト' in content):
                return True

        return False
