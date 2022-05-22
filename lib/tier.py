from discord.ext import commands as c
from asyncpgw import general
from db import *
tier = """tier(
    server bigint,
    member bigint,
    register timestamptz,
    update timestamptz,
    finish timestamptz,
    tier integer DEFAULT 0
)"""

__all__ = ["check_user_tier", "check_server_tier"]

async def check_user_tier(bot, member):
    "サブスク確認ティアを1~2の中から確認する"
    enable = Tier()
    if ((data := await enable.fetch_member(member.id))):
        return data["tier"]

    return 0


async def check_server_tier(bot, guild):
    "サブスク確認ティアを1~2の中から確認する"
    enable = Tier()
    if ((data := await enable.fetch_server(guild.id))):
        return data["tier"]

    return 0


"""
tier1: 1000

ミニサメ１～３
自動VC作成 5個まで
匿名アンケート
リアルタイムでプロフィールをキャッシュ(キャッシュしないとコマンドでプロフィールを表示できない。匿名告白なども。)
即時リマインド(定期的なリマインドは無料。誰かがメッセージを送信した後、即時リマインドするのは有料)

tier2: 2000

tier1の内容
ミニサメ4~6
自動VC サブカテゴリーにも作成できるように
裏2ショットの定期自動確認(誰も居ないVCの削除、権限の確認)
カテゴリー毎のカウンター(裏2ショットのやつは無料)
複数ロールの人数を一つのチャンネルに表示 例: 男: 10人,女: 10人


上記のやつ+

tie3: 300
永久ブロックリスト3重バックアップ
永久ブロックリスト11人以上追加可能(21人以上で+300,31人以上で+30と10人ずつ増える毎に+300円)

tier4: 100
1機能毎に+100円
"""