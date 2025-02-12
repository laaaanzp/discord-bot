import discord
from discord import app_commands
from discord.ext import commands

import globals


class SyncCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, *, target: str = "locally"):
        guild = None if target == "globally" else ctx.guild
        self.bot.tree.clear_commands(guild=guild)
        self.bot.tree.copy_global_to(guild=guild)
        fmt = await self.bot.tree.sync(guild=guild)
        count = len(fmt)
        s = "s" if count > 1 else ""

        await ctx.send(
            f"Synced {len(fmt)} command{s} {'globally' if guild == None else 'locally'}.",
            delete_after=globals.DELETE_AFTER
        )
    
    @commands.command()
    @commands.is_owner()
    async def clear(self, ctx: commands.Context, *, target: str = "locally"):
        guild = None if target == "globally" else ctx.guild
        self.bot.tree.clear_commands(guild=guild)
        _ = await self.bot.tree.sync(guild=guild)

        await ctx.send(
            f"Command(s) cleared {'globally' if guild == None else 'locally'}.",
            delete_after=globals.DELETE_AFTER
        )
    
    @sync.error
    @clear.error
    async def error(cls, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(SyncCog(bot))
        