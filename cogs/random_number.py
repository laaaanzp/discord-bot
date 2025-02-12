import random
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

# Default values for generate command
DEFAULT_MIN = 1
DEFAULT_MAX = 10


class RandomNumberCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Generates random number")
    @app_commands.describe(
        min=f"Minimum Range. (Defaults of {DEFAULT_MIN})",
        max=f"Maximum Range. (Defaults of {DEFAULT_MAX})"
    )
    async def generate(
        self, 
        interaction: discord.Interaction, 
        min: Optional[int] = DEFAULT_MIN, 
        max: Optional[int] = DEFAULT_MAX
    ):
        # If min was provided and is equal to max and default min value, that 
        # means that min was provided and max was not provided, making them 
        # have the same value. We should set the min value to 0
        if min == max == DEFAULT_MIN:
            min = 0

        # Swap min with max if min is bigger than max
        if min > max:
            min, max = max, min

        rand = random.randint(min, max)
        await interaction.response.send_message(f"Random Number: {rand}")


async def setup(bot: commands.Bot):
    await bot.add_cog(RandomNumberCog(bot))
        