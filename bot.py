import random
import discord
from discord.ext import commands
from discord.ext.commands.core import check
import json
import time

client = commands.Bot(command_prefix=['+'],help_command=None,case_insensitive=True)

@client.command(pass_context=True,aliases=['hlp','info'])
async def help(ctx):
    em = discord.Embed(title='Command List',color=discord.Color.green())
    em.add_field(name='Currency Commands',value='`balance`,`inventory`,`deposit`,`withdraw`,`beg`,`search`,`shop`,`buy`,`hunt`,`fish`,`sell`,\n`gamble`,`share`,`moony`')
    em.set_footer(icon_url=ctx.author.avatar_url,text='Brought To You By Goldy!')
    await ctx.send(embed=em)
    return True

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown) and ctx.message.content == f"{client.command_prefix[0]}daily":
        test = '{:.0f}'.format(error.retry_after)
        hours = int(test) / 3600
        msg = f'You Already Claimed Your Daily Reward Today! Try Again In `{int(hours)}h`.'
        await ctx.send(msg)
        return True
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'The Used Command: `' + ctx.message.content + '` Is On Cooldown Currently. Try Again In `{:.0f}` Seconds'.format(error.retry_after)
        await ctx.send(msg)
        return True

async def open_inv(user):
    with open('inv.json','r') as file:
        users = json.load(file,)
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['rifle'] = 0
        users[str(user.id)]['rod'] = 0
        users[str(user.id)]['soccer'] = 0
        users[str(user.id)]['fish'] = 0
        users[str(user.id)]['boar'] = 0
        users[str(user.id)]['tropical'] = 0
        users[str(user.id)]['octopus'] = 0
        users[str(user.id)]['shrimp'] = 0
        users[str(user.id)]['frog'] = 0
        users[str(user.id)]['mouse'] = 0
        users[str(user.id)]['wolf'] = 0
        users[str(user.id)]['trophy'] = 0
    with open('inv.json','w') as file:
        json.dump(users,file)
    return True

async def open_account(user):
    with open('user.json','r') as file:
        users = json.load(file,)
    if str(user.id) in users:
        if int(users[str(user.id)]['wallet']) + 0 != users[str(user.id)]['wallet']:
            users[str(user.id)]['wallet'] -= 0.5
            with open('user.json','w') as file:
                json.dump(users,file) 
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0
    with open('user.json', 'w') as file:
        json.dump(users,file)
    return True

async def get_data():
    with open('user.json','r') as file:
        users = json.load(file,)
    return users

async def get_inv_data():
    with open('inv.json','r') as file:
        users = json.load(file,)
    return users

@client.event
async def on_ready():
    print("Online!")

@client.command(pass_context=True,aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_data()

    wallet = users[str(user.id)]['wallet']
    bank = users[str(user.id)]['bank']

    em = discord.Embed(title=f"{ctx.author.name}'s Balance",color=discord.Color.green())
    em.add_field(name='Wallet: ',value=wallet,inline=False)
    em.add_field(name='Bank',value=bank,inline=False)
    await ctx.send(embed=em)

@client.command(pass_context=True)
@commands.cooldown(1,60*60*24,commands.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_data()
    users[str(user.id)]['wallet'] += 10000
    with open('user.json','w') as file:
        json.dump(users,file)
    await ctx.send(f"Here Are Your Daily `10,000 Coins`, {ctx.author.name}!")
    return True

@client.command(pass_context=True,aliases=['dep','depo'])
async def deposit(ctx,amt=0):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_data()
    if amt == 0:
        await ctx.send("Type In How Much You Would Like To Deposit!")
        return False
    elif amt > users[str(user.id)]['wallet']:
        await ctx.send(f"Hey! You Cannot Deposit That Much! You Do Not Have `{amt}` Coins In Your Wallet! You Only Have `"  + users[str(user.id)]['wallet'] + '` Coins.')
        return False
    elif amt < 0:
        await ctx.send(f"Hey You Cannot Deposit `{amt}` Coins! That's A Negative Number.")
        return False
    else:
        users[str(user.id)]['bank'] += amt
        users[str(user.id)]['wallet'] -= amt
        with open('user.json','w') as file:
            json.dump(users,file)
        await ctx.send(f"Succesfully Deposited `{amt}` In Your Bank Account!")
        return True

@client.command(pass_context=True,aliases=['wh','with','draw'])
async def withdraw(ctx,amt=0):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_data()
    if amt == 0:
        await ctx.send("Type In How Much You Would Like To Deposit!")
        return False
    elif amt > users[str(user.id)]['bank']:
        await ctx.send(f"Hey! You Cannot Deposit That Much! You Do Not Have `{amt}` Coins In Your Bank Account! You Only Have `{users[str(user.id)]['bank']}` Coins.")
        return False
    else:
        users[str(user.id)]['wallet'] += amt
        users[str(user.id)]['bank'] -= amt
        with open('user.json','w') as file:
            json.dump(users,file)
        await ctx.send(f"Succesfully Withdrawn `{amt}` From Your Bank Account!")
        return True

@client.command(pass_context=True)
@commands.cooldown(1,35,commands.BucketType.user)
async def moony(ctx):
    nr = random.randint(1,5)
    await open_account(ctx.author)
    user = ctx.author
    users = await get_data()
    if nr == 1:
        em = discord.Embed(title='Moony Says',color=discord.Color.red())
        em.set_thumbnail(url='https://w7.pngwing.com/pngs/702/870/png-transparent-emoji-running-top-speed-need-for-racing-moon-information-emoji-english-face-text.png')
        em.add_field(name='No Coins',value='I Cannot Bless You With Any Coins At This Time... Visit Me Later...',inline=False)
        await ctx.send(embed=em)
        return False
    elif nr == 2:
        em = discord.Embed(title='Moony Says',color=discord.Color.green())
        em.set_thumbnail(url='https://w7.pngwing.com/pngs/729/376/png-transparent-emoji-black-moon-emoticon-scarry-purple-face-head.png')
        amt = random.randint(50,150)
        em.add_field(name='A Few Coins',value=f'Here... Have These `{amt}` Coins. Visit Me Later...',inline=False)
        await ctx.send(embed=em)
        users[str(user.id)]['wallet'] += amt
        with open('user.json','w') as file:
            json.dump(users,file)
        return True
    elif nr == 3:
        em = discord.Embed(title='Moony Says',color=discord.Color.green())
        em.set_thumbnail(url='https://e7.pngegg.com/pngimages/808/718/png-clipart-yellow-emoji-illustration-emoji-full-moon-whatsapp-chatbot-emoji-face-head.png')
        amt = random.randint(750,1550)
        em.add_field(name='I\'m Feeling Good',value=f'I\'m In A Good Mood... Have These `{amt}` Coins. Visit Me Later...',inline=False)
        await ctx.send(embed=em)
        users[str(user.id)]['wallet'] += amt
        with open('user.json','w') as file:
            json.dump(users,file)
        return True
    elif nr == 4:
        em = discord.Embed(title='Moony Says',color=discord.Color.red())
        em.set_thumbnail(url='https://w7.pngwing.com/pngs/954/339/png-transparent-black-moon-emoji-new-moon-lunar-phase-moon-face-head-sticker.png')
        amt = random.randint(300,550)
        em.add_field(name='Something Odd',value=f'My Body Is Acting Weird... Have These `{amt}` Coins And Come Back Later...',inline=False)
        await ctx.send(embed=em)
        users[str(user.id)]['wallet'] += amt
        with open('user.json','w') as file:
            json.dump(users,file)
        return True
    elif nr == 5:
        em = discord.Embed(title='Where Is Moony?',color=discord.Color.purple())
        em.add_field(name='No Moony',value='Moony Is Nowhere To Be Found...',inline=False)
        await ctx.send(embed=em)
        return False

@client.command(pass_context=True,aliases=['share'])
async def give(ctx,amt=0,member: discord.Member=''):
    if amt <= 0 and member != '':
        await ctx.send("You Cannot Share Nothing! Try A Larger Sum.")
        return False
    elif amt >= 1 and member != '':
        await open_account(ctx.author)
        await open_account(member)
        user = ctx.author
        wallet = await get_data()
        if wallet[str(user.id)]['wallet'] < amt:
            await ctx.send(f"You Don't Have {amt} Coins In Your Wallet! Try A Lower Sum.")
            return False
        else:
            wallet[str(user.id)]['wallet'] -= amt
            wallet[str(member.id)]['wallet'] += amt
            with open('user.json','w') as file:
                json.dump(wallet,file)
            await ctx.send(f"Succesfully Shared `{amt}` Of Your Coins With `{member.display_name}`!")
            time.sleep(1)
            await ctx.send(f"Your Current Wallet: `{wallet[str(user.id)]['wallet']}` Coins  \n`{member.display_name}`'s Current Wallet: `{wallet[str(member.id)]['wallet']}`.")
            return True
    elif amt >= 1 and member == '':
        await ctx.send(f"Who Do You Want To Share {amt} With?")
        return False
    else:
        await ctx.send("What Do You Want To Share And With Who?")
        return False

@client.command(pass_context=True,aliases=['inv'])
async def inventory(ctx,page=1):
    await open_inv(ctx.author)
    users = await get_inv_data()
    user = ctx.author
    nr = 0
    em = discord.Embed(title=f"{ctx.author.name}'s Inventory",color=discord.Color.purple())
    if users[str(user.id)]['rifle'] != 0:
        em.add_field(name=':gun: Rifle(s): ',value=f"`{users[str(user.id)]['rifle']}`")
        nr += 1
    if users[str(user.id)]['rod'] != 0:
        em.add_field(name=':fishing_pole_and_fish: Fishing Rod(s): ',value=f"`{users[str(user.id)]['rod']}`")
        nr += 1
    if users[str(user.id)]['soccer'] != 0:
        em.add_field(name=':soccer: Soccer Ball(s): ',value=f"`{users[str(user.id)]['soccer']}`")
        nr += 1
    if users[str(user.id)]['frog'] != 0:
        em.add_field(name=':frog: Frog(s): ',value=f"`{users[str(user.id)]['frog']}`")
        nr += 1
    if users[str(user.id)]['wolf'] != 0:
        em.add_field(name=':wolf: Wolves: ',value=f"`{users[str(user.id)]['wolf']}`")
        nr += 1
    if users[str(user.id)]['mouse'] != 0:
        em.add_field(name=':mouse: Mice: ',value=f"`{users[str(user.id)]['mouse']}`")
        nr += 1
    if users[str(user.id)]['boar'] != 0:
        em.add_field(name=':boar: Boar(s) ',value=f"`{users[str(user.id)]['boar']}`")
        nr += 1
    if users[str(user.id)]['fish'] != 0:
        em.add_field(name=':fish: Fish ',value=f"`{users[str(user.id)]['fish']}`")
        nr += 1
    if users[str(user.id)]['tropical'] != 0:
        em.add_field(name=':tropical_fish: Tropical Fish ',value=f"`{users[str(user.id)]['tropical']}`")
        nr += 1
    if users[str(user.id)]['shrimp'] != 0:
        em.add_field(name=':shrimp: Shrimp(s) ',value=f"`{users[str(user.id)]['shrimp']}`")
        nr += 1
    if users[str(user.id)]['octopus'] != 0:
        em.add_field(name=':octopus: Octopus(es) ',value=f"`{users[str(user.id)]['octopus']}`")
    if users[str(user.id)]['trophy'] != 0:
        em.add_field(name=':trophy: Trophy(ies) ',value=f"`{users[str(user.id)]['Trophy']}`")
        nr += 1
    if nr == 0:
        em.add_field(name='Items: ',value='You Have No Items In Your Inventory!')
    await ctx.send(embed=em)

nlist = ['Steve','Bob','An Elephant','Larry','A Dog','Your Imaginary Friend','A Random Kid','Lars']
@client.command(pass_context=True)
@commands.cooldown(1,25,commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_data()
    nr = random.randint(30,650)
    if nr > 59:
        em = discord.Embed(title=f"{ctx.author.name} Went Begging!",color=discord.Color.green())
        em.add_field(name=random.choice(nlist),value=f"Have These `{nr}` Coins!")
        await ctx.send(embed=em)
        users[str(user.id)]['wallet'] += nr
        with open('user.json','w') as file:
            json.dump(users,file)
        return True
    else:
        em = discord.Embed(title=f"{ctx.author.name} Went Begging!",color=discord.Color.red())
        em.add_field(name=random.choice(nlist),value='No Coins For You!')
        await ctx.send(embed=em)
        return False

places = ['bakery','closet','factory','purse','pizzeria','pockets','attic','wardrobe']
@client.command(pass_context=True)
@commands.cooldown(1,25,commands.BucketType.user)
async def search(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_data()
    choice1 = random.randint(0,7)
    choice2 = random.randint(0,7)
    if choice1 == choice2:
        choice2 += 1
    em = discord.Embed(title='Where Do You Want To Go Searching',color=discord.Color.green())
    em.add_field(name='1.',value=f'`{places[choice1]}`',inline=False)
    em.add_field(name='2.',value=f'`{places[choice2]}`',inline=False)
    await ctx.send(embed=em)
    msg = await client.wait_for('message',check=check)
    if (msg.content).casefold() == places[choice1]:
        p = places[choice1]
        if p == 'bakery':
            nr = random.randint(300,650)
            await ctx.send(f"You Scatter Through The Bakery And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'closet':
            nr = random.randint(450,750)
            await ctx.send(f"You Search The Closet And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'factory':
            nr = random.randint(700,930)
            await ctx.send(f"You Look Around The Factory And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'purse':
            nr = random.randint(250,550)
            await ctx.send(f"You Desperately Search A Random Purse And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'pizzeria':
            nr = random.randint(300,650)
            await ctx.send(f"You Scatter Through The Pizzeria And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'pockets':
            nr = random.randint(150,390)
            await ctx.send(f"You Search Your Pockets And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'attic':
            nr = random.randint(800,1250)
            await ctx.send(f"You Search Through Your Old Attic And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'wardrobe':
            nr = random.randint(425,830)
            await ctx.send(f"You Investigate The Wardrobe And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
    elif (msg.content).casefold() == places[choice2]:
        p = places[choice2]
        if p == 'bakery':
            nr = random.randint(300,650)
            await ctx.send(f"You Scatter Through The Bakery And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'closet':
            nr = random.randint(450,750)
            await ctx.send(f"You Search The Closet And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'factory':
            nr = random.randint(700,930)
            await ctx.send(f"You Look Around The Factory And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'purse':
            nr = random.randint(250,550)
            await ctx.send(f"You Desperately Search A Random Purse And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'pizzeria':
            nr = random.randint(300,650)
            await ctx.send(f"You Scatter Through The Pizzeria And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'pockets':
            nr = random.randint(150,390)
            await ctx.send(f"You Search Your Pockets And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'attic':
            nr = random.randint(800,1250)
            await ctx.send(f"You Search Through Your Old Attic And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif p == 'wardrobe':
            nr = random.randint(425,830)
            await ctx.send(f"You Investigate The Wardrobe And You Find `{nr}` Coins!")
            users[str(user.id)]['wallet'] += nr
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
    else:
        await ctx.send("That Place Isn't Listed There, Yo!")
        return False
    

@client.command(pass_context=True)
@commands.cooldown(1,20,commands.BucketType.user)
async def play(ctx):
    await open_inv(ctx.author)
    await open_account(ctx.author)
    user = ctx.author
    users = await get_data()
    inv = await get_inv_data()
    if inv[str(user.id)]['soccer'] == 0:
        await ctx.send("You Don't Have A Soccer Ball To Play With! Go Buy One At The Item Shop!")
        return False
    else:
        nr = random.randint(300,675)
        await ctx.send(f"You Played With You Soccer Ball And You Found {nr} Coins!")
        users[str(user.id)]['wallet'] += nr
        with open('user.json','w') as file:
            json.dump(users,file)
        return True

pmax = 1
@client.command(pass_context=True,aliases=['itemshop'])
async def shop(ctx,page=1):
    em = discord.Embed(title='Item Shop',color=discord.Color.blue())
    if page == 1:
        em.add_field(name=':gun: `Rifle` ',value='10,000 Coins',inline=False)
        em.add_field(name=':fishing_pole_and_fish: `Fishing Rod` ',value='10,000 Coins',inline=False)
        em.add_field(name=':soccer: `Soccer Ball` ',value='5,000 Coins',inline=False)
        em.add_field(name=':trophy: `Golden Trophy` ',value='100,000 Coins',inline=False)
        em.set_footer(text=f"Page {page} Of {pmax}")
        await ctx.send(embed=em)
        return True
    else:
        await ctx.send(f"The Item Shop Only Has `{pmax}` Page(s)!")
        return False

@client.command(pass_context=True)
async def buy(ctx,item='',amt=1):
    if item == '':
        await ctx.send(f"Type In The Item That You Want To Buy. TIP: Type '{client.command_prefix[0]}shop' To See The Full List Of Items!")
        return False
    elif item.casefold() == 'rifle' or item.casefold() == 'gun':
        await open_account(ctx.author)
        await open_inv(ctx.author)
        user = ctx.author
        users = await get_data()
        inv = await get_inv_data()
        if users[str(user.id)]['wallet'] >= amt * 10000:
            users[str(user.id)]['wallet'] -= amt * 10000
            inv[str(user.id)]['rifle'] += amt
            with open('user.json','w') as file:
                json.dump(users,file)
            with open('inv.json','w') as file:
                json.dump(inv,file)
            await ctx.send(f"Succesuflly Purchased `{amt} Rifle`!")
            return True
        else:
            need = (amt * 10000) - users[str(user.id)]['wallet']
            await ctx.send(f"Insufficient Funds! You Need `{need}` More Coins To Purchase This Item!")
            return False
    elif item.casefold() == 'rod' or item.casefold() == 'fishing':
        await open_account(ctx.author)
        await open_inv(ctx.author)
        user = ctx.author
        users = await get_data()
        inv = await get_inv_data()
        if users[str(user.id)]['wallet'] >= amt * 10000:
            users[str(user.id)]['wallet'] -= amt * 10000
            inv[str(user.id)]['rod'] += amt
            with open('user.json','w') as file:
                json.dump(users,file)
            with open('inv.json','w') as file:
                json.dump(inv,file)
            await ctx.send(f"Succesfully Purchased `{amt} Fishing Rod`!")
            return True
        else:
            need = (amt * 10000) - users[str(user.id)]['wallet']
            await ctx.send(f"Insufficient Funds! You Need `{need}` More Coins To Purchase This Item!")
            return False
    elif item.casefold() == 'soccer':
        await open_account(ctx.author)
        await open_inv(ctx.author)
        user = ctx.author
        users = await get_data()
        inv = await get_inv_data()
        if users[str(user.id)]['wallet'] >= amt * 5000:
            users[str(user.id)]['wallet'] -= amt * 5000
            inv[str(user.id)]['soccer'] += amt
            with open('user.json','w') as file:
                json.dump(users,file)
            with open('inv.json','w') as file:
                json.dump(inv,file)
            await ctx.send(f"Succesfully Purchased `{amt} Soccer Ball`!")
            return True
        else:
            need = (amt * 5000) - users[str(user.id)]['wallet']
            await ctx.send(f"Insufficient Funds! You Need `{need} More Coins To Purchase This Item`!")
            return False
    elif item.casefold() == 'trophy' or item.casefold() == 'golden':
        await open_account(ctx.author)
        await open_inv(ctx.author)
        user = ctx.author
        users = await get_data()
        inv = await get_inv_data()
        if users[str(user.id)]['wallet'] >= amt * 100000:
            users[str(user.id)]['wallet'] -= amt * 100000
            inv[str(user.id)]['soccer'] += amt
            with open('user.json','w') as file:
                json.dump(users,file)
            with open('inv.json','w') as file:
                json.dump(inv,file)
            await ctx.send(f"Succesfully Purchased `{amt} Soccer Ball`!")
            return True
        else:
            need = (amt * 5000) - users[str(user.id)]['wallet']
            await ctx.send(f"Insufficient Funds! You Need `{need} More Coins To Purchase This Item`!")
            return False
    else:
        await ctx.send(f"Hey! That Item Does Not Exist On The Item Shop! TIP: Type '{client.command_prefix[0]}shop page_number' To See The Full List Of Items!")
        return False

@client.command(pass_context=True)
@commands.cooldown(1,25,commands.BucketType.user)
async def gamble(ctx,bet=0):
    if bet <= 49 or bet >= 501:
        await ctx.send("You Need To Type In A Bet From 50 To 500 Coins To Enter The Gamble!")
        return False
    elif bet >= 50 and bet <= 500:
        await open_account(ctx.author)
        user = ctx.author
        users = await get_data()
        nr_bot = random.randint(1,10)
        nr_user = random.randint(1,10)
        if nr_bot > nr_user:
            em = discord.Embed(title=f"{ctx.author.name} Went Gambling",color=discord.Color.red())
            em.add_field(name='My Number',value=f'`{nr_bot}`',inline=False)
            em.add_field(name='Your Number',value=f'`{nr_user}`',inline=False)
            em.set_footer(text='You Lost The Bet')
            await ctx.send(embed=em)
            users[str(user.id)]['wallet'] -= bet
            with open('user.json','w') as file:
                json.dump(users,file)
            return True
        elif nr_bot == nr_user:
            em = discord.Embed(title=f"{ctx.author.name} Went Gambling",color=discord.Color.orange())
            em.add_field(name='My Number',value=f'`{nr_bot}`',inline=False)
            em.add_field(name='Your Number',value=f'`{nr_user}`',inline=False)
            em.set_footer(text='It\'s A Tie! You Don\'t Lose Anything')
            await ctx.send(embed=em)
            return True
        elif nr_bot < nr_user:
            percent = random.randint(55,125)
            em = discord.Embed(title=f"{ctx.author.name} Went Gambling",color=discord.Color.green())
            em.add_field(name='My Number',value=f'`{nr_bot}`',inline=False)
            em.add_field(name='Your Number',value=f'`{nr_user}`',inline=False)
            em.set_footer(text=f'You Win The Bet With A Win Of {percent}%!')
            await ctx.send(embed=em)
            users[str(user.id)]['wallet'] += ((percent/100) * bet)
            with open('user.json','w') as file:
                json.dump(users,file)
            return True

captures = ['frog','mouse','wolf','boar']
@client.command(pass_context=True)
@commands.cooldown(1,35,commands.BucketType.user)
async def hunt(ctx):
    nr = random.randint(1,5)
    await open_inv(ctx.author)
    user = ctx.author
    users = await get_inv_data()
    if users[str(user.id)]['rifle'] < 1:
        await ctx.send('You Do Not Own A Rifle! Go And Buy One From The Item Shop!')
        return False
    if nr == 1:
        em = discord.Embed(title='You Went Hunting :gun:',color=discord.Color.orange())
        em.add_field(name='Hunting Status ',value='You Didn\'t Hunt Down Anyhting!',inline=False)
        await ctx.send(embed=em)
        return False
    elif nr == 2:
        cap = captures[0]
    elif nr == 3:
        cap = captures[1]
    elif nr == 4:
        cap = captures[2]
    elif nr == 5:
        cap = captures[3]
    em = discord.Embed(title='You Went Hunting :gun:',color=discord.Color.green())
    em.add_field(name='Hunting Status ',value=f"You Hunted Down A `{cap}` :{cap}:!",inline=False)
    await ctx.send(embed=em)
    users[str(user.id)][f'{cap}'] += 1
    with open('inv.json','w') as file:
        json.dump(users,file)
    return True

fishe = ['fish','shrimp','octopus']
@client.command(pass_context=True)
@commands.cooldown(1,35,commands.BucketType.user)
async def fish(ctx):
    nr = random.randint(1,5)
    await open_inv(ctx.author)
    user = ctx.author
    users = await get_inv_data()
    if users[str(user.id)]['rod'] < 1:
        await ctx.send('You Do Not Own A Fishing Rod! Go And Buy One From The Item Shop!')
        return False
    if nr == 1:
        em = discord.Embed(title='You Went Fishing :fishing_pole_and_fish:',color=discord.Color.orange())
        em.add_field(name='Fishing Status ',value='You Didn\'t Catch Anyhting!',inline=False)
        await ctx.send(embed=em)
        return False
    elif nr == 2:
        cap = fishe[0]
    elif nr == 3:
        cap = fishe[1]
    elif nr == 4:
        cap = fishe[2]
    elif nr == 5:
        em = discord.Embed(title='You Went Fishing :fishing_pole_and_fish:',color=discord.Color.green())
        em.add_field(name='Fishing Status ',value="You Caught A `Tropical Fish` :tropical_fish:!",inline=False)
        await ctx.send(embed=em)
        users[str(user.id)]['tropical'] += 1
        with open('inv.json','w') as file:
            json.dump(users,file)
        return True
    em = discord.Embed(title='You Went Fishing :fishing_pole_and_fish:',color=discord.Color.green())
    em.add_field(name='Fishing Status ',value=f"You Caught A `{cap}` :{cap}:!",inline=False)
    await ctx.send(embed=em)
    users[str(user.id)][f'{cap}'] += 1
    with open('inv.json','w') as file:
        json.dump(users,file)
    return True

@client.command(pass_context=True)
@commands.cooldown(1,3,commands.BucketType.user)
async def sell(ctx,item='',amt=1):
    await open_inv(ctx.author)
    user = ctx.author
    users = await get_inv_data()
    await open_account(ctx.author)
    wallet = await get_data()
    if item == '':
        await ctx.send("What Do You Want To Sell?")
        return False
    elif item.casefold() == 'frog':
        sell = 825
        if users[str(user.id)]['frog'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['frog'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['frog']} Frog(s)!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Frog(s) For `{price}` Coins!')
            users[str(user.id)]['frog'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    elif item.casefold() == 'mouse':
        sell = 650
        if users[str(user.id)]['mouse'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['mouse'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['mouse']} Mice!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Mice For `{price}` Coins!')
            users[str(user.id)]['mouse'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    elif item.casefold() == 'wolf':
        sell = 1050
        if users[str(user.id)]['wolf'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['wolf'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['wolf']} Wolves!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Wolves For `{price}` Coins!')
            users[str(user.id)]['wolf'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    elif item.casefold() == 'boar':
        sell = 1325
        if users[str(user.id)]['boar'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['boar'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['boar']} Boar(s)!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Boar(s) For `{price}` Coins!')
            users[str(user.id)]['boar'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    elif item.casefold == 'soccer':
        sell = 2000
        if users[str(user.id)]['soccer'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['Soccer'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['soccer']} Soccer Ball(s)!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Soccer Ball(s) For `{price}` Coins!')
            users[str(user.id)]['soccer'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    elif item.casefold() == 'rifle' or item.casefold() == 'gun':
        sell = 3500
        if users[str(user.id)]['rifle'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['rifle'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['rifle']} Rfile(s)!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Rifle(s) For `{price}` Coins!')
            users[str(user.id)]['rifle'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    elif item.casefold() == 'fishing' or item.casefold() == 'rod':
        sell = 3500
        if users[str(user.id)]['rod'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['rod'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['rod']} Fishing Rod(s)!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Fishing Rod(s) For `{price}` Coins!')
            users[str(user.id)]['rod'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    elif item.casefold() == 'fish':
        sell = 650
        if users[str(user.id)]['fish'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['fish'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['fish']} Fish!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Fish For `{price}` Coins!')
            users[str(user.id)]['fish'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    elif item.casefold() == 'tropical':
        sell = 925
        if users[str(user.id)]['tropical'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['tropical'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['tropical']} Tropical Fish!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Tropical Fish For `{price}` Coins!')
            users[str(user.id)]['tropical'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    elif item.casefold() == 'shrimp':
        sell = 500
        if users[str(user.id)]['shrimp'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['shrimp'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['shrimp']} Shrimp(s)!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Shrimp(s) For `{price}` Coins!')
            users[str(user.id)]['shrimp'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    elif item.casefold() == 'octopus' or item.casefold == 'octo':
        sell = 1350
        if users[str(user.id)]['octopus'] == 0:
            await ctx.send("You Do Not Own This Item!")
            return False
        elif users[str(user.id)]['octopus'] < amt:
            await ctx.send(f"You Only Have {users[str(user.id)]['octopus']} Octopus(es)!")
            return False
        else:
            price = amt * sell
            await ctx.send(f'Succesfully Sold `{amt}` Octopus(es) For `{price}` Coins!')
            users[str(user.id)]['octopus'] -= amt
            wallet[str(user.id)]['wallet'] += price
            with open('user.json','w') as file:
                json.dump(wallet,file)
            with open('inv.json','w') as file:
                json.dump(users,file)
            return True
    else:
        await ctx.send("Hey! This Item Does Not Exist! Can't Sell What Can't Be Obtained.")
        return False


client.run('ODU0NjYwMDgzMzMzMjAxOTcw.YMnKOg.dout0CgAnOHwyxzr18xX6suPwDo')