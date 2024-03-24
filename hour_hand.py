__author__ = "Tamzin Hadasa Kelly"
__email__ = "coding@tamz.in"
__version__ = "0.0.0"

import datetime as dt

from discord import Intents, Message
from discord.ext.commands import Bot, Context

import config


intents = Intents.default()
intents.message_content = True
bot = Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    bot.TIME_CHANNEL = bot.get_channel(config.TIME_CHANNEL_ID)
    bot.TOWNSFOLK_ROLE = bot.TIME_CHANNEL.guild.get_role(config.TOWNSFOLK_ID)


class FormatError(Exception):
    pass


def to_dt(time_str: str) -> dt.datetime:
    try:
        time_dt = dt.datetime.strptime(time_str, "%Y%m%d%H%M")
    except ValueError as e:
        raise FormatError("Timestamp must be formatted as YYYYMMDDhhmm.") from e
    if time_dt.minute % 30:
        raise FormatError("Timestamp end in `00` or `30`.")
    return time_dt


@bot.command()
async def poll(ctx: Context, time: to_dt, flexibility: int | float = 0.5):
    if flexibility:
        later_bound = time + dt.timedelta(hours=flexibility)
        when = (f"starting between <t:{int(time.timestamp())}:F> and "
                f"<t:{int(later_bound.timestamp())}:t>")
    else:
        when = f"at <t:{time.timestamp}:F>"
    msg: Message = await bot.TIME_CHANNEL.send(
        f"{bot.TOWNSFOLK_ROLE.mention}: {ctx.author.mention} would like to play " +
        when +
        ". React with all clock emojis that you could start at (EASTERN TIME), or react"
        " with :no_entry: if you cannot do any time or :question: if you are unsure."
    )
    for i in range(int(flexibility * 2 + 1)):
        emoji = chr(int('1F550', 16) + (time.hour - 1 + i // 2) % 12 + (12 if i % 2 else 0))
        await msg.add_reaction(emoji)


bot.run(config.TOKEN)