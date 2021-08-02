# -*- coding: utf-8 -*-
from discord.ext import commands
from datetime import datetime
import asyncio
import discord
import random
import os

from lib.Helpers import Helpers



# os adm
adm_discriminator = ['8954','1218']

# lista de canais onde o bot não pode enviar mensagens
black_list_channels = ['deposito-farm-maconhas']

intents = discord.Intents.default()
intents.members = True

# client = discord.Client()
client = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)

chat_path = os.path.abspath(os.getcwd())+'/Chat'


if not os.path.exists(f'{chat_path}'):
    os.mkdir(f'{chat_path}')


def get_token():
    try:
        token = open('token.txt', mode='r').read()
    except Exception:
        print('Não foi encontrado o token do bot, por favor insira o token')
        token = input('Digite o token: ')
        file = open('token.txt', mode='w')
        file.write(token)
        file.close()

    return token


def save_messages(message):
    try:
        server = message.guild.name
        channel = message.channel.name
    except Exception:
        server = 'private'
        channel = message.channel.recipient.name+'#'+message.channel.recipient.discriminator

    if not os.path.exists(f'{chat_path}/{server}/'):
        os.mkdir(f'{chat_path}/{server}/')

    time_log = f'{Helpers().fix_date(datetime.now().day)}/{Helpers().fix_date(datetime.now().month)}/{datetime.now().year} {str(Helpers().fix_date(datetime.now().hour))}:{str(Helpers().fix_date(datetime.now().minute))}'

    msg = f'{time_log} - {message.author.name}#{message.author.discriminator}: {message.content}\n'
    print(msg)

    file = open(f'{chat_path}/{server}/{channel}.txt', mode='a')
    file.write(msg)
    file.close()


@client.event
async def on_ready():
    print(f'Bot online: {client.user.name}!\n')


# Ao entrar no servidor
@client.event
async def on_member_join(member):
    channel = client.get_channel(856202101981446206) # Canal: Bem-vindo

    embed = discord.Embed(
        title = 'Bem vindo à Cidade Cinza!',
        description = f'Olá, {member.mention} Seja muito bem vindo ao discord da cidade!\nLeia as <#856296996968202251> para se manter atualizado\ne juntos manter um bom RP :smile:',
        colour = discord.Colour.green()
    )

    embed.set_footer(text='Wubba lubba dub dub!')
    embed.set_thumbnail(url=member.avatar_url)
    # embed.set_author(name=client.get_user(170752898462908416).display_name, icon_url=client.get_user(170752898462908416).avatar_url) # Sagos#8954

    mensagem = await channel.send(embed=embed)
    # await mensagem.delete()

    await asyncio.sleep(20)

    role = discord.utils.find(lambda r: r.id == 856243210737287190, member.guild.roles) # Aguardando WL
    await member.add_roles(role)



# Ao enviar mensagens
@client.event
async def on_message(message):
    # Se a mensagem veio de um bot, ignora
    if message.author.bot == True:
        return 

    try:
        server = message.guild.name
    except Exception:
        server = 'private'

    save_messages(message)

    # se a mensagem não foi no privado
    if server != 'private':
        # se a mensagem foi para o discord do Cidade Cinza
        if message.guild.id == 856128407313973278:

            # 1% de chance de reagir uma mensagem com joinha
            msg_id = [856309867593334805, 856128407313973281] # chat-novatos, chat-geral
            if random.randint(1,100) == 42 and message.channel.id in msg_id:
                await message.add_reaction('👍')

            # Responde o !ping com pong!
            msg = ['!ping']
            msg_id = [856309867593334805, 856128407313973281] # chat-novatos, chat-geral
            if message.content.lower() in msg and message.channel.id in msg_id:
                await message.channel.send(f'Pong!')


# Ao editar mensagens
@client.event
async def on_message_edit(before, after):
    # Se a mensagem veio de um bot, ignora
    if before.author.bot == True:
        return

    print(f'{before.author.display_name.capitalize()} editou uma mensagem')
    print(f'{before.content} > {after.content}\n')


# Ao adicionar reações
@client.event
async def on_reaction_add(reaction, user):
    if user.bot == True:
        return

    print(f'{user.display_name} reagiu uma mensagem com {reaction.emoji}\n')

    import ipdb; ipdb.set_trace()


# Ao remover reações
@client.event
async def on_reaction_remove(reaction, user):
    if user.bot == True:
        return

    print(f'{user.display_name} removeu a reação {reaction.emoji} de uma mensagem\n')


# client.run(get_token())

user_id = input(f'Digite seu ID: ')

try:
    user = Helpers.db_consult(None, f'SELECT id, whitelisted, banned FROM vrp_users WHERE id={user_id};')[0]
except Exception:
    user = None


if not user:
    print('Esse ID não existe')
elif user[2] == 1:
    print('Você foi banido da cidade')
else:
    if user[1] == 1:
        print('Esse ID já foi liberado')
    else:
        teste = Helpers.db_update(1, f'UPDATE vrp_users SET whitelisted=1 WHERE id={user[0]};')
        print('Seu ID foi liberado')