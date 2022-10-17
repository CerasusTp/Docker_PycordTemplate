import discord
from discord.ui import InputText, Modal, View
import os
from dotenv import load_dotenv

# 環境変数読込
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")
GUILD_ID = [os.environ.get("DeveloperGUILD_ID")]

bot = discord.Bot(debug_guilds = GUILD_ID)

@bot.event
async def on_ready():
    print(f"[info]{bot.user} 起動完了")

# モーダルウィンドウ
class TestModal(Modal):
    def __init__(self) -> None:
        super().__init__(title = "モーダルウィンドウ テスト")
        self.add_item(InputText(label="Short"))
        self.add_item(InputText(style=discord.InputTextStyle.long, label='Long', required=False))
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Short:{self.children[0].value}\nLong:{self.children[1].value}')

# 選択メニュー
class TestSelect(View):
    @discord.ui.select(
        options = [
            discord.SelectOption(label = "Morning", emoji = "☀️", description = "朝"),
            discord.SelectOption(label = "AfterNoon", emoji = "🕛", description = "昼"),
            discord.SelectOption(label = "Night", emoji = "🌙", description = "夜")
        ])
    
    async def callback(self, select, interaction: discord.Interaction):
        GREETING = {'Morning':'おはよう！', 'AfterNoon':'こんにちは！', 'Night':'こんばんは！'}
        select.disabled = True
        await interaction.response.edit_message(view = self)
        await interaction.followup.send(f'{GREETING[select.values[0]]}')

# スラッシュコマンド
@bot.slash_command(description = "スラッシュコマンド テスト")
async def test(ctx):
    await ctx.interaction.response.send_message(f'{str(ctx.interaction.user)[:-5]}さん こんにちは！！')

@bot.slash_command(description = "モーダルウィンドウ 呼び出し")
async def modal(ctx):
    modal = TestModal()
    await ctx.interaction.response.send_modal(modal)

@bot.slash_command(description = "選択メニュー 呼び出し")
async def hello(ctx):
    view = TestSelect()
    await ctx.interaction.response.send_message("時間帯を選んでね！", view = view)

# Embedメッセージ
@bot.slash_command(description = "Embedメッセージ テスト")
async def embedtest(ctx):
    embed = discord.Embed(title = 'タイトル', description = 'タイトル説明', color = 0xa2d7dd)
    embed.add_field(name = 'サブタイトル1', value = '内容')
    embed.add_field(name = 'サブタイトル2', value = '内容')
    embed.set_footer(text = 'フッター')
    await ctx.interaction.response.send_message(embed = embed)

bot.run(TOKEN)