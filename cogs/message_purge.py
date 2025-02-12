import discord
from discord import app_commands
from discord.ext import commands

import globals


def permission_list_to_str(permissions: list[str]) -> str:
    """Converts permissions list to a string representation.

    Sample: 
        ["Administrator"] => "`Administrator`"
        ["Manage Nicknames", "Attach Files"] => "`Manage Nicknames` and `Attach Files`"
        ["Kick Members", "Ban Members", "Add Reactions"] => "`Kick Members`, `Ban Members` and `Add Reactions`"

    Args:
        permissions (list[str]): _List of permissions string._

    Returns:
        str: _Formatted string of permission list._
    """
    
    permissions_str = ""

    match permissions:
        case [a]:       # 1 permission
            permissions_str = a
        case [_, _]:    # 2 permissions
            permissions_str = "` and `".join(permissions)
        case _:         # More than 2 permissions
            permissions_str = "`, `".join(permissions[:-1]) + "` and `" + permissions[-1]

    return f"`{permissions_str}"


class MessagePurgeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Deletes the last n messages")
    @app_commands.describe(limit="How many messages to delete. (Range of 5-100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def delete(self, interaction: discord.Interaction, limit: int):
        limit = min(limit, 100)
        deleted_messages = await interaction.channel.purge(limit=limit)
        count = len(deleted_messages)
        s = "s" if count > 1 else ""

        await interaction.response.send_message(
            f"Deleted {count} message{s}.", 
            delete_after=globals.DELETE_AFTER
        )
    
    @delete.error
    async def delete_error(cls, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        description = ""

        if isinstance(error, app_commands.BotMissingPermissions):
            missing_permissions_str = permission_list_to_str(error.missing_permissions)
            s = "" if len(error.missing_permissions) == 1 else "s"
            description=f"Bot requires {missing_permissions_str} permission{s} to perform this action."

        elif isinstance(error, app_commands.MissingPermissions):
            missing_permissions_str = permission_list_to_str(error.missing_permissions)
            s = "" if len(error.missing_permissions) == 1 else "s"
            description=f"You need {missing_permissions_str} permission{s} to perform this action.",


        if description:
            embed = discord.Embed(
                title=globals.ERROR_TITLE,
                description=description,
                color=globals.ERROR_COLOR
            )

            await interaction.response.send_message(embed=embed, delete_after=globals.DELETE_AFTER)

    
async def setup(bot: commands.Bot):
    await bot.add_cog(MessagePurgeCog(bot))
