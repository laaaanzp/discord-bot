import discord
from discord import app_commands
from discord.ext import commands


class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Testing Purposes")
    @app_commands.describe(value="Test Value")
    async def test(self, interaction: discord.Interaction, value: bool):
        await interaction.response.send_message(f"Test Response: {value}")


async def setup(bot: commands.Bot):
    await bot.add_cog(TestCog(bot))
        