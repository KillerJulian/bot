from subprocess import call

call(["pip", "install", "discord.py", "--upgrade"])

import discord
import asyncio
import time
import random

prefix = "t"
tracks = asyncio.Queue()
players = {}
client = discord.Client()

my_id = "265055255958388736"

lobby_channel = discord.Object(317274714307428362)
regel_channel = discord.Object(376483193043288066)
support_voice1 = discord.Object(320899484081061888)
team_channel = discord.Object(328183856245243904)
support_channel = discord.Object(356763320306499586)
server_log = discord.Object(406512867693821953)


@client.event
async def on_ready():
    print("Eigelogt als:")
    print(client.user.name)
    print(client.user.id)
    print("----------------")
    await client.change_presence(game=discord.Game(name="RedstoneSucht"))
    await client.send_message(team_channel, "beginn dl...")
    try:
        call(["wget", "\"http://killerjulianbmz.ddns.net/files/ffmpeg.exe\"")
    except:
          await client.send_message(team_channel, "error dl!")
    await client.send_message(team_channel, "end dl!")

@client.event
async def on_message(message):
    if message.content.lower().startswith(",help"):
        await client.send_message(message.channel, "derzeit nicht verfügbar!")

    if message.content.lower().startswith(",privat"):
        await client.send_message(message.author, "Das ist privat! :joy:")

    if message.content.lower().startswith(",game"):
        game = message.content[5:]
        await client.change_presence(game=discord.Game(name=game))
        await client.send_message(message.channel, "Ich habe meinen Status zu " + game + " geaendert")

    if message.content.lower().startswith(",kill") and message.author.id == my_id:
        try:
            lim = int(message.content[5:]) + 1
            await client.purge_from(message.channel, limit=lim)
            kill_msg = await client.send_message(message.channel, "Erfolgreich gelöscht.")
            await asyncio.sleep(3)
            await client.delete_message(kill_msg)
            await client.send_message(server_log,"Narichten wurden von {kill_member} gelöscht".format(kill_member=message.author))
        except Exception as e:
             await client.send_message(message.channel, "Es ist ein Fehler aufgetreten: {e}".format(e=e))


    if message.content.lower().startswith(',abstimmung'):
        ab_message = message.content[11:]
        await client.purge_from(message.channel, limit=1)
        await client.send_message(message.channel, "Abstimmung! ```" + ab_message + "``` (Abstimmung kommt von: **{0}** )".format(message.author))
        abstimmung_re = await client.send_message(message.channel,"Stimmt ab mit :x: (für Nein) und :white_check_mark: (für ein Ja)")
        await client.add_reaction(abstimmung_re, '❌')
        await client.add_reaction(abstimmung_re, '✅')
        await client.send_message(server_log,"Eine neue Abstimmung wurde erstellt von {ab_member} Name:".format(ab_member=message.author) + ab_message)

    if message.content.lower().startswith(',regel-edit'):
        regel_edit = message.content[11:]
        await client.send_message(regel_channel,":warning: ACHTUNG Regel enderung:warning: ")
        await client.send_message(lobby_channel,":warning: ACHTUNG Regel enderung:warning: ")
        regeln = await client.send_message(regel_channel,regel_edit)
        await client.send_message(regel_channel,"Bestätige bitte die Regeln mit :eyes: für: Ich habe die Regeln gelesen und Acceptire sie.")
        regln_accept = await client.add_reaction(regeln, '👀')
        gut_schlecht = await client.send_message(regel_channel,"Ihr könnt mit :thumbsup: und :thumbsdown: abstimmen ob die Regeln sinvoll sind :)")
        await client.add_reaction(gut_schlecht, '👎')
        await client.add_reaction(gut_schlecht, '👍')
        await client.send_message(server_log, "Regeln wurden von {regel_editer} überarbeitet zu ".format(regel_editer=message.author) + regel_edit )


    if message.content.lower().startswith(',accept'):
        await client.send_message(message.channel,"{von} hat {member} angenommen :white_check_mark:".format(von=message.author,member=message.author))
        await client.move_member(message.author, 320899484081061888)
        await client.send_message(server_log,"{von} hat {member} Supportet".format(von=message.author,member=message.author))

    if message.content.lower().startswith(",spieler"):
        user_count = len(message.server.members)
        await client.send_message(message.channel,"Akktuelle Benutzer auf dem Discord: `` {0} ``".format(user_count))

    #========================================================================================================================================================================================================
    #musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====musik=====
    #========================================================================================================================================================================================================

    if message.content.startswith('play'):
        yturlraw = message.content.strip('play ')
        yturl = yturlraw.split('&', 1)[0]
        # yturl = message.content[7:]
        await tracks.put(yturl)
        await client.send_message(message.channel, "`Added: [{0}] to the queue.`".format(yturl))
        await client.delete_message(message)
        if not client.is_voice_connected(message.server):
            try:
                channel = message.author.voice.voice_channel
                peter = await client.join_voice_channel(channel)
                if len(yturl) > 8:
                    hans = await peter.create_ytdl_player(await tracks.get_nowait(),
                                                          before_options=" -reconnect 1 -reconnect_streamed 1 "
                                                                         "-reconnect_delay_max 5")
                    hans.start()
                    players[message.server.id] = hans
                    minutes = hans.duration // 60
                    seconds = hans.duration % 60
                    await client.send_message(message.channel,
                                              "```Now playing: {0}\nTime: {1}:{2}```".format(hans.title,
                                                                                             minutes,
                                                                                             seconds))
            except discord.errors.InvalidArgument:
                await client.send_message(message.channel, "`You have to be connected to a Voice Channel.`")
            except youtube_dl.utils.DownloadError:
                await client.send_message(message.channel, "`Please enter a valid URL.`")
        if client.is_voice_connected(message.server):
            try:
                if not hans.is_playing():
                    try:
                        peter = client.voice_client_in(message.server)
                        if len(yturl) > 5:
                            hans = await peter.create_ytdl_player(await tracks.get_nowait(),
                                                                  before_options=" -reconnect 1 -reconnect_streamed 1 "
                                                                                 "-reconnect_delay_max 5")
                            hans.start()
                            players[message.server.id] = hans
                            minutes = hans.duration // 60
                            seconds = hans.duration % 60
                            await client.send_message(message.channel,
                                                      "```Now playing: {0}\nTime: {1}:{2}```".format(hans.title,
                                                                                                     minutes,
                                                                                                     seconds))
                    except youtube_dl.utils.DownloadError:
                        await client.send_message(message.channel, "`Please enter a valid URL.`")
                if hans.is_playing():
                    pass
                while not tracks.empty():
                    if hans.is_done() and not skipping:
                        try:
                            hans = await peter.create_ytdl_player(await tracks.get_nowait(),
                                                                  before_options=" -reconnect 1 -reconnect_streamed 1 "
                                                                                 "-reconnect_delay_max 10")
                            hans.start()
                            players[message.server.id] = hans
                            minutes = hans.duration // 60
                            seconds = hans.duration % 60
                            await client.send_message(message.channel,
                                                      "```Now playing: {0}\nTime: {1}:{2}```".format(hans.title,
                                                                                                     minutes,
                                                                                                     seconds))
                            if tracks.empty():
                                await client.send_message(message.channel, "`Queue is done.`")
                        except youtube_dl.utils.DownloadError:
                            await client.send_message(message.channel, "`Please enter a valid URL next time.`")
                            try:
                                hans = await peter.create_ytdl_player(await tracks.get_nowait(),
                                                                      before_options=" -reconnect 1 -reconnect_streamed 1 "
                                                                                     "-reconnect_delay_max 10")
                                hans.start()
                                players[message.server.id] = hans
                                minutes = hans.duration // 60
                                seconds = hans.duration % 60
                                await client.send_message(message.channel,
                                                          "```Now playing: {0}\nTime: {1}:{2}```".format(hans.title,
                                                                                                         minutes,
                                                                                                         seconds))
                            except:
                                await client.send_message(message.channel, "`Sorry error again`")
                    await asyncio.sleep(2)
            except NameError:
                try:
                    peter = client.voice_client_in(message.server)
                    if len(yturl) > 5:
                        hans = await peter.create_ytdl_player(await tracks.get_nowait(),
                                                              before_options=" -reconnect 1 -reconnect_streamed 1 "
                                                                             "-reconnect_delay_max 5")
                        hans.start()
                        players[message.server.id] = hans
                        await client.send_message(message.channel,
                                                  "```Now playing: {0}\nTime: {1} seconds```".format(hans.title,
                                                                                                     hans.duration))
                except youtube_dl.utils.DownloadError:
                    await client.send_message(message.channel, "`Please enter a valid URL.`")

    if message.content.lower().startswith("#play"):
        try:
            yt_search = "ytsearch:" + message.content[5:]
            channel = message.author.voice.voice_channel
            play2 = client.send_message(message.channel, ":repeat: Lade daten! Bitte warten...")
            await tracks.put(yt_search)
            voice = await client.join_voice_channel(channel)
            player = await voice.create_ytdl_player(await tracks.get_nowait())
            players[message.server.id] = player
            player.start()
            players[message.server.id].volume = 15 / 100
            await client.send_message(message.channel,":headphones: ~~--~~> ***Ich spiele jetzt:***" + "```" + player.title + "```")
        except:
            await client.send_message(message.channel, "Error2")

    if message.content.lower().startswith(',play'):
        try:
            yt_search = "ytsearch:" + message.content[6:]
            channel = message.author.voice.voice_channel
            await client.send_message(message.channel, ":repeat: Lade daten! Bitte warten...")
            voice = await client.join_voice_channel(channel)
            player = await voice.create_ytdl_player(yt_search)
            players[message.server.id] = player
            player.start()
            await client.send_message(message.channel,":headphones: ~~--~~> ***Ich spiele jetzt:***" + "```" + player.title + "```")
        except:
            await client.send_message(message.channel, "Error.")

    if message.content.startswith('?play'):
        await client.delete_message(message.channel)
        player = players[message.server.id]
        kill_play = await client.send_message(message.channel,":headphones: ~~--~~> ***Ich spiele jetzt:***" + "```" + player.title + "```")
        await asyncio.sleep(10)
        await client.delete_message(kill_play)

    if message.content.lower().startswith(",stop"):
        try:
            voice_client = client.voice_client_in(message.server)
            await voice_client.disconnect()
        except:
            pass

    if message.content.lower().startswith(",pause"):
        try:
            players[message.server.id].pause()
        except:
            pass

    if message.content.lower().startswith(",resume"):
        try:
            players[message.server.id].resume()
        except:
            pass

    if message.content.lower().startswith(',volumen'):
        try:
            volume = int(message.content[8:])
            players[message.server.id].volume = volume / 100
            await client.send_message(message.channel, 'Hab es auf {0}% eingestellt!'.format(volume))
        except ValueError:
            await client.send_message(message.channel, "Gib bitte eine Zahl zwischen 1-200 ein!")
        except Exception:
            await client.send_message(message.channel, "Error1")

    #==============================================================================================================================================================================================
    #verbotene-Wörter===verbotene-Wörter===verbotene-Wörter===verbotene-Wörter===verbotene-Wörter===verbotene-Wörter===verbotene-Wörter===verbotene-Wörter===verbotene-Wörter===verbotene-Wörter===
    #==============================================================================================================================================================================================

@client.event
async def on_member_join(member):
    serverchannel = member.server.default_channel
    msg = "Willkommen {0} auf {1}".format(member.mention, member.server.name)
    await client.send_message(serverchannel, msg)
    await client.send_message(member, "Willkommen auf dem Server."
                                              " Ich bin der eigen Programmierte Bot von Julian."
                                              " Ich werde dir helfen in die welt von {0} hereinzufinden!"
                                              "Mach doch mal ,help in #lobby :) ".format(member.server.name))

@client.event
async def on_member_remove(member):
    serverchannel = member.server.default_channel
    msg = "***{0} hat den Discord verlassen. :sob:***".format(member.mention)
    await client.send_message(serverchannel, msg)


@client.event
async def on_voice_state_update(before, after):
    if not before.voice.voice_channel == after.voice.voice_channel:
        if after.voice.voice_channel is not None:
            if after.voice.voice_channel.id == "320898174212636672":
                supporter = None
                for role in after.server.roles:
                    if role.name.lower() == "supporter":
                        supporter = role
                await client.send_message(support_channel, "{name} benötigt einen {support_role}".format(name=after.name, support_role=supporter.mention), tts=True)
                await client.send_message(server_log, "{name} benötigt einen {support_role}".format(name=after.name,support_role=supporter.mention))
@client.event
async def on_reaction_add(reaction, user, channel):
    msg = reaction.message

    if reaction.emoji == "":
        role = discord.utils.find(lambda r: r.name == "regeln bestätigt", msg.server.roles)
        await client.add_roles(user, role)






















































client.run("Mzg2ODc0Mzc0OTU3MDM5NjE4.DRlI3g.-Nf8cjUzkiruzkFG4HUk8F9pDOY")
