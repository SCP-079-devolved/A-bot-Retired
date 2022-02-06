import random
import discord 
from discord.ext import commands
from asyncio import sleep
import os
import requests
import json
import typing
import aiohttp
from config import config

cfg = config


intents = discord.Intents.default()
intents.members=True
client = discord.Client()
client = commands.Bot(command_prefix=cfg.BOT_PREFIX)
badwords = ['']
link = ['http://', 'https://', '.com']



@client.event
async def on_ready():
    print(client.user.name,"is currently online")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="A bot shutting down for good. "), status = discord.status.Idle )


@client.command()
async def goodbye(ctx):
    channel = "861840031002263572"
    await ctx.send("Abot went down... \n bc SCP-079 Devolved Is raising!")

#class MyPaginator(buttons.Paginator):

#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#
#    @buttons.button(emoji='\u23FA')
#    async def record_button(self, ctx, member):
#        await ctx.send('This button sends a silly message! But could be programmed to do much more.')
#
#    @buttons.button(emoji='my_custom_emoji:1234567890')
#    async def silly_button(self, ctx, member):
#        await ctx.send('Beep boop...')

#@client.command()
#async def ooo(ctx):
#    pagey = MyPaginator(title='Silly Paginator', colour=0xc67862, embed=True, timeout=90, use_defaults=True,
#                        entries=[1, 2, 3], length=1, format='**')
#
#    await pagey.start(ctx)

@client.event
async def on_message(message):
   for i in badwords: # Go through the list of bad words;
      if i in message.content:
         await message.delete()
         await message.channel.send(f"{message.author.mention} Don't use that word!")
         client.dispatch('profanity', message, i)
         return # So that it doesn't try to delete the message again, which will cause an error.
   await client.process_commands(message)

@client.event
async def on_profanity(message, word):
   channel = client.get_channel(840846352077422602)
   embed = discord.Embed(title="Bad word Alert!",description=f"{message.author.name} just said ||{word}||", color=discord.Color.blurple()) # Let's make an embed!
   await channel.send(embed=embed)
   await client.process_commands(message)

#@client.event
#async def on_message(message):
#  if "owo" in message.content:
#    await message.channel.send("OWO")
#  await client.process_commands(message)

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send("You can type `!help` for more info")
    await client.process_commands(message)


#@client.event
#async def on_message_delete(message):
#    channel=client.get_channel(840846352077422602)
#    embed=discord.Embed(title="{} deleted a message".format(message.member.name), 
#    description="woooo", color="Blue")
#    embed.add_field(name= message.content ,value="This is the message that he has deleted", inline=True)
#    await channel.send(embed=embed)





class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return '{0.author} slapped {1} because *{2}*'.format(ctx, to_slap, argument)

@client.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)
    #print('{0.author} slapped me because {2}'.format(ctx, reason))

@client.command()
@commands.has_any_role('Mod', 'Head Mod', 'Server Manager', 'Dev', 'Head Dev')
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'User {member} has been Kicked')
  channel = client.get_channel(835708482471723078)
  await channel.send(f"<@{ctx.author.id}> Has Kicked {member} because {reason}")

@client.command()
@commands.has_any_role('Mod', 'Head Mod', 'Server Manager', 'Dev', 'Head Dev')
async def ban(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'User {member} has been Banned')
  channel = client.get_channel(835708482471723078)
  await channel.send(f"<@{ctx.author.id}> Has Kicked {member} because {reason}")

@client.command()
@commands.has_any_role('Mod', 'Head Mod', 'Server Manager', 'Dev', 'Head Dev')
async def announce_p(ctx, role: discord.Role, *, message):
  channel = client.get_channel(835708482471723078)
  clientProfilePicture = ctx.author.avatar_url
  await ctx.send("Announcement sent to #announcements")
  embed=discord.Embed(title=f"Announcement from: {ctx.author.display_name}", description=f"{message}")
  embed.set_thumbnail(url=clientProfilePicture)
  embed.set_footer(text="V: 3.1.0")
  await channel.send(embed=embed)
  await channel.send(f"{ctx.author.display_name} Also pinged this role: {role.mention}")

@client.command()
@commands.has_any_role('Mod', 'Head Mod', 'Server Manager', 'Dev', 'Head Dev')
async def announce_i(ctx, image, *, message):
  channel = client.get_channel(835708482471723078)
  piv = image
  await ctx.send("Announcement sent to #announcements")
  embed=discord.Embed(title=f"Announcement from: {ctx.author.display_name}", description=f"{message}")
  embed.set_thumbnail(url=piv)
  embed.set_footer(text="V: 3.1.0")
  await channel.send(embed=embed)

@client.command()
@commands.has_any_role('Mod', 'Head Mod', 'Server Manager', 'Dev', 'Head Dev')
async def announce(ctx, *, message):
  channel = client.get_channel(835708482471723078)
  clientProfilePicture = ctx.author.avatar_url
  await ctx.send("Announcement sent to #announcements")
  embed=discord.Embed(title=f"Announcement from: {ctx.author.display_name}", description=f"{message}")
  embed.set_thumbnail(url=clientProfilePicture)
  embed.set_footer(text="V: 3.1.0")
  await channel.send(embed=embed)

@client.command()
@commands.has_any_role('Mod', 'Head Mod', 'Server Manager', 'Dev', 'Head Dev')
async def shutdown(ctx, password, reason):
    if password == "852":
      channel = client.get_channel(835708482471723078)
      #await channel.send(f"<@{ctx.author.id}> shutted down bot because {reason}")
      await ctx.send("Shutting Down")
      await ctx.bot.logout()
    else:
      await ctx.send("Password was wrong")

@client.command()
async def pm(ctx, user: discord.Member = None, *, message = None):
  if user is None:
    await ctx.send("Well, who you sending this to?!")
  if user is not None:
    if message is None:
      await ctx.send("What is the message you are sending?")
    if message is not None:
      myembed = discord.Embed()
      myembed.add_field(name=f"{ctx.author} sent you:", value=f"{message}")
      myembed.set_footer(text="If this message is inappropriate plese contact a server admin")
      await user.send(embed=myembed)
      await ctx.send(f"I've sent your message to {user}")

@client.command()
async def rickroll(ctx, user: discord.Member = None):
  if user is None:
    await ctx.send("Well, who you sending this to?!")
  if user is not None:
      myembed = discord.Embed()
      myembed.add_field(name=f"{ctx.author} wanted to Rick Roll you", value=" YOU MUST LISTEN TILL END")
      myembed.set_footer(text="hahahaha")
      await user.send(embed=myembed)
      await user.send ("https://youtu.be/dQw4w9WgXcQ")
      await ctx.send(f"I've rick rolled {user} hahaha")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

        
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

@client.command()
async def connect(ctx):
    user=ctx.message.author
    voicech = ctx.author.voice.channel
    if voicech != None:
        vc= await voicech.connect()
    else:
        await ctx.send(f'{user} is not in a channel.')

@client.event
async def on_message_join(member):
    channel = client.get_channel(835708187016560661)
    embed=discord.Embed(title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!") # F-Strings!
    embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!
    await channel.send(embed=embed)

@client.command()
async def test(ctx):
    if "Ken" in [i.name.lower() for i in ctx.author.roles]:
        await ctx.send(f"<@{ctx.author.id}> woooooooooooo")
    else:
        await ctx.send(f"<@{ctx.author.id}> u dont have perms to use this command")




#@comands.has_any_role('Bot Developer', 'Ken', 'King Carnoval')

@client.command()
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()

   embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.set_footer(text=factjson['fact'])
   await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    ping = int(round(client.latency, 3) * 1000)
    await ctx.send(f"<@{ctx.author.id}>, the ping is {ping} ms.")

@client.command()
async def current_v(ctx):
  embed=discord.Embed(title="What is new!", description="*Hey*, checking what is new in this version? here are details: \n New command that will do something, It's moderation command and important so i wont say anything about it", color=0xf51919)
  embed.set_thumbnail(url="https://i.imgur.com/kDVpgmF.png")
  embed.add_field(name="What will come!", value="No idea! \n  **Any Idea? Dm me!**", inline=False)
  embed.set_footer(text="V: 3.1.0")
  await ctx.send(embed=embed)

client.remove_command('help')

@client.command()
async def help(ctx):
    async with ctx.typing():
        # do expensive stuff here
        await sleep(2)
        embed=discord.Embed(title="Help", description="*Please note that the bot is under construction* \n \n 1. `!slap [reason]`: with this you can slap bot with reason! \n 2. `!dog`: get a random pic of dogs! \n 3. `!ping`: check the ping, easy \n 4. `!inspire`: get a random quote! \n 5. `!mod_help [PASSWORD]`: help command for mods *Note: Mods know what is password and if they tell you you can't even use it, (yeah good codes)* \n \n   ***END OF LIST OF COMMANDS***     \n \n ***Created By Carnoval15*** \n ***With help of zbot***", color=0x9219f5)
        embed.set_author(name="A bot", icon_url="https://i.imgur.com/kDVpgmF.png")
        embed.add_field(name = 'Commands:', value=('!slap [REASON], !dog, !ping, !inspire, !mod_help (MOD ONLY)'))
        embed.add_field(name ='Made By:', value=('**Carnoval15** and **Zbot**'))
        embed.set_thumbnail(url="https://i.imgur.com/kDVpgmF.png")
        embed.set_footer(text="V: 3.1.0")
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role('Mod', 'Head Mod', 'Server Manager', 'Dev', 'Head Dev')
async def mod_help(ctx, password):
  if password == "321":
    embed=discord.Embed(title="Mod Help", description="*Mod's commands:* \n 1.`!ban [user mention] <reason>`: This will ban the user you have mentioned \n 2.`!kick [user mention <reason>`: This will kick the use you have mentioned with reason \n 3.`!announce [Message you want to announce in #announcements]`: This will make bot to announce what you say Directly to #announcements channel \n 4.`!announce_p [Role you want to ping] [announcement]`: This will also ping role you wish to get notification on the announcement \n 5.`!announce_i [image link] [what you want to announce]`: This will announce anything with image (NOTE:you need to paste image URL) \n 6.`!pm [user mention] [your message]`: This will send a dm with your message to user you want \n 7.`!clear [number of messages]`: Easy clears number of messages you tell to the bot \n \n Keep in mind that bot will announce every action, (Ban & Kick) you have made into #anouncements", color=0x5900ff)
    embed.set_thumbnail(url="https://i.imgur.com/kDVpgmF.png")
    embed.set_footer(text="V: 3.1.0")
    await ctx.send(embed=embed)
    await sleep(2)
    await ctx.message.delete

  else:
    await ctx.send("PASSWORD ENTERED WRONG TRY AGAIN")
      
#@client.command()
#async def test(ctx, *, arg):
#    await ctx.send(arg)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

# token stuff
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
