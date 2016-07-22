import json

import aiohttp

import discord
import discord.ext.commands as commands
import scarecrow.cogs.utils as utils


def setup(bot):
    bot.add_cog(Misc(bot))


class Misc:
    """Miscellaneous commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def agarify(self, *, content):
        """Agarifies a string."""
        await self.bot.say(utils.agarify(content))

    @agarify.command()
    async def user(self, *, user: discord.Member=None):
        """Agarifies a user's name."""
        name = user.nick if user.nick is not None else user.name
        await self.bot.say(utils.agarify(name, True))

    @commands.command(aliases=['meow'])
    async def cat(self):
        """Meow !"""
        with aiohttp.ClientSession(loop=self.bot.loop) as session:
            resp = await session.get('http://random.cat/meow')
            data = json.loads(await resp.text())
            await self.bot.say(data['file'])

    @commands.command()
    async def insult(self):
        """Poke the bear."""
        await self.bot.say(utils.random_line('data/insults.txt'))

    @commands.command()
    async def weebnames(self, wanted_gender=None):
        """Looking for a name for your new waifu ?

        A prefered gender can be specified between f(emale), m(ale), x(mixed).
        """
        content = ''
        for i in range(1, 10):
            # Get a random name satisfying the wanted gender and kick the '\n' out
            def predicate(line):
                return line[0] == wanted_gender
            line = utils.random_line('data/weeb_names.txt', predicate if wanted_gender else None)
            gender, name, remark = line[:-1].split('|')

            content += '[{}] {} {}\n'.format(gender, name, '({})'.format(remark) if remark else '')

        await self.bot.say_block(content)
