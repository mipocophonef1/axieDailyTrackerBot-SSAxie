import yaml
import discord
from ssaxie import *

client = discord.Client()

ronin_prefix = "0x"
command_prefix = "$"

with open('secrets.yaml') as f:
    accounts = yaml.safe_load(f)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content == "$commands":
        await message.channel.send("```*** SSAxie Bot Commands ***\n\n$daily <discordName>```")

    for user in accounts['scholars']:
        if user in message.content.lower():
            private_key = accounts["scholars"][user]["private_key"]
            address = accounts['scholars'][user]['ronin_address'].replace("ronin:", ronin_prefix)
            ronin_mp_address = address.replace("0x", "ronin:")
            access_token = get_access_token(address, private_key)

            claimable_slp = get_unclaimed_slp(address)
            profile = get_profile(address)

            energy_stats = get_remaining_energy(address, access_token)
            daily = get_daily_mission(address, access_token)

            check_in = daily['items'][0]['missions'][0]
            adv = daily['items'][0]['missions'][1]
            arena = daily['items'][0]['missions'][2]

            if message.content.startswith(f"{command_prefix}daily"):
                if check_in['is_completed']:
                    done_check_in = "Completed"
                else:
                    done_check_in = "Not Yet Completed"

                # Title
                embed = discord.Embed(title=f"Daily Stats", color=0xb200ff)

                # First Row
                embed.add_field(name="Dashboard Link: ", value=f"[{profile['name']}](https://marketplace.axieinfinity.com/profile/{ronin_mp_address}/axie)", inline=False)

                # Second Row
                embed.add_field(name=":student: Scholar Name", value=f"{profile['name']}", inline=True)
                embed.add_field(name=":calendar_spiral: Last Claim", value=f"{profile['last_claim']}", inline=True)
                embed.add_field(name=":calendar_spiral: Next Claim", value=f"{profile['next_claim']}", inline=True)

                # Third Row
                embed.add_field(name="<:slp:903258151007174717>  Lifetime SLP", value=f"{profile['lifetime_slp']}", inline=True)
                embed.add_field(name="<:slp:903258151007174717>  In-game SLP", value=f"{profile['in_game_slp']}", inline=True)
                embed.add_field(name="<:slp:903258151007174717> Claimable", value=f"{claimable_slp}", inline=True)

                # Fourth Row
                embed.add_field(name=":crossed_swords: Arena MMR", value=f"{profile['mmr']}", inline=True)
                embed.add_field(name=":trophy: Arena Rank", value=f"{profile['rank']}", inline=True)
                embed.add_field(name="<:lightning:903284219302797372> Energy Left", value=f"{energy_stats['player_stat']['remaining_energy']}", inline=True)

                # Fifth Row
                embed.add_field(name=":clipboard: Daily: Check In", value=f"{done_check_in}", inline=True)
                embed.add_field(name=":orangutan: Daily: PvE", value=f"{adv['progress']}/{adv['total']}", inline=True)
                embed.add_field(name=":dagger: Daily: PvP", value=f"{arena['progress']}/{arena['total']}", inline=True)

                # Sixth Row (BLANK)
                embed.add_field(name="\u2800", value="\u2800", inline=False)

                # Footer
                embed.set_footer(text=f"Requested by: {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)

client.run(accounts["discord_token"])