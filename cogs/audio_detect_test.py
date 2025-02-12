import discord
from discord import app_commands
from discord.ext import commands, voice_recv

import globals


class AudioDetectSink(voice_recv.AudioSink):
    def __init__(self):
        super().__init__()
    
    def wants_opus(self) -> bool:
        return False
    
    def write(self, user: discord.User, data: voice_recv.VoiceData):
        pass
    
    def cleanup(self):
        pass

    @voice_recv.AudioSink.listener()
    def on_voice_member_speaking_start(self, member: discord.Member):
        print(f"{member.name} {member.display_name} {member.global_name} <{member.id}> has started speaking.")
    
    @voice_recv.AudioSink.listener()
    def on_voice_member_speaking_stop(self, member: discord.Member):
        print(f"{member.name} {member.display_name} {member.global_name} <{member.id}> has stopped speaking.")



class AudioDetectTest(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_channels: dict[int, voice_recv.VoiceRecvClient] = {}
        
    @app_commands.command()
    async def connect(self, interaction: discord.Interaction):
        channel = interaction.user.voice.channel
        guild_id = interaction.guild_id
        voice_client = await channel.connect(cls=voice_recv.VoiceRecvClient)
        voice_client.listen(AudioDetectSink())
        self.voice_channels[guild_id] = voice_client
    
    @connect.error
    async def connect_error(cls, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        description = ""
    
        if isinstance(error, discord.ClientException):
            description = f"Bot is already on the voice channel."
        else:
            description = "You must be in a voice channel to use this command."

        if description:
            embed = discord.Embed(
                title=globals.ERROR_TITLE,
                description=description,
                color=globals.ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, delete_after=globals.DELETE_AFTER)

    @app_commands.command()
    async def disconnect(self, interaction: discord.Interaction):
        # TODO
        guild_id = interaction.guild_id
        voice_client = self.voice_channels.get(guild_id)
        
        if voice_client:
            voice_client.stop()
            for voice_protocol in self.bot.voice_clients:
                print(voice_protocol)
    
    @disconnect.error
    async def disconnect_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(AudioDetectTest(bot))