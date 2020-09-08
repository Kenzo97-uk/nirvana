import discord
import asyncio
from discord.ext import commands


def setup(bot):
    bot.add_cog(Verificator(bot))


class Verificator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        agreeing_role = discord.utils.get(member.guild.roles, name='Agreeing')
        task = asyncio.create_task(self.verify_member(member), name=f'verify_{member.id}')
        await member.add_roles(agreeing_role, reason='JOINING')

    async def verify_member(self, member):
        await asyncio.sleep(300)
        verification_channel = discord.utils.get(member.guild.text_channels, name='verify')
        member_role = discord.utils.get(member.guild.roles, name='Участник')
        agreeing_role = discord.utils.get(member.guild.roles, name='Agreeing')
        await verification_channel.set_permissions(member, send_messages=True, reason='VERIFICATION')
        def check(message):
            return message.channel == verification_channel and message.content == f'{self.bot.command_prefix}agree'
        msg = await self.bot.wait_for('message', check=check)
        await msg.delete()
        await member.remove_roles(agreeing_role, reason='Succesful Verification')
        await member.add_roles(member_role, reason='Succesful Verification')
        await verification_channel.set_permissions(member, overwrite=None)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        for task in asyncio.all_tasks():
            if task.get_name() == f'verify_{member.id}':
                task.cancel()



