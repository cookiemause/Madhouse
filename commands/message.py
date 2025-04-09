import discord
from discord.ext import commands
from discord import ui


class ChannelSelect(discord.ui.ChannelSelect):

    def __init__(self, parent_view):
        super().__init__(placeholder="Wähle einen Channel",
                         min_values=1,
                         max_values=1,
                         channel_types=[discord.ChannelType.text])
        self._parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(self.values[0].id)
        self._parent_view.channel = channel
        await interaction.response.send_modal(
            MessageModal(self._parent_view.bot, channel))


class MessageModal(ui.Modal, title="Schreibe deine Nachricht hier"):
    titel = ui.TextInput(label="Titel", style=discord.TextStyle.short)
    message = ui.TextInput(label="Deine Nachricht",
                           style=discord.TextStyle.paragraph)

    def __init__(self, bot, channel):
        super().__init__()
        self.bot = bot
        self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title=str(self.titel),
                                  description=str(self.message),
                                  color=discord.Color.blue())
            await self.channel.send(embed=embed)
            await interaction.response.send_message(
                f"✅ Nachricht in {self.channel.mention} gesendet!",
                ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                "⚠ Ich habe keine Berechtigung, in diesen Kanal zu schreiben!",
                ephemeral=True)


class ChannelButton(discord.ui.Button):

    def __init__(self, channel):
        super().__init__(label=channel.name,
                         style=discord.ButtonStyle.secondary,
                         custom_id=f"channel_{channel.id}")
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Channel: {self.channel.name}\nID: {self.channel.id}",
            ephemeral=True)


class ChannelView(discord.ui.View):

    def __init__(self, channels):
        super().__init__()
        for channel in channels:
            self.add_item(ChannelButton(channel))


class Message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @commands.hybrid_command(
        name="nachricht",
        description="Öffnet ein Formular für deine Mitteilung")
    async def nachricht(self, ctx):
        if not ctx.interaction:
            await ctx.send(
                "⚠ Dieser Befehl funktioniert nur als Slash-Befehl!",
                delete_after=5)
            return

        class MessageView(discord.ui.View):

            def __init__(self, bot):
                super().__init__()
                self.bot = bot
                self.channel = None
                self.add_item(ChannelSelect(self))

            @discord.ui.button(label="Weiter",
                               style=discord.ButtonStyle.primary)
            async def button_callback(self, interaction, button):
                if not self.channel:
                    await interaction.response.send_message(
                        "❌ Bitte wähle zuerst einen Channel!", ephemeral=True)
                    return

                modal = MessageModal(self.bot, self.channel)
                await interaction.response.send_modal(modal)

        await ctx.send("Wähle einen Channel:",
                       view=MessageView(self.bot),
                       ephemeral=True)


async def setup(bot):
    await bot.add_cog(Message(bot))
