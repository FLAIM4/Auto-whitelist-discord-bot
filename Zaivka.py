import disnake
import cog.Modals as Modals
from mcrcon import MCRcon
from disnake.ext import commands
from disnake import TextInputStyle
import time , sqlite3

class Oservere(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.con = sqlite3.connect('data.db')


    def add_persistent_view(self):
        persistent_views = disnake.ui.View()
        self.bot.add_view(persistent_views)
        self.bot.add_view(Modals.Modal(self.bot), message_id=1164942526571098243)  # Замените message_id на свой


    @commands.command()
    @commands.has_role(1159018783931895821)
    async def server(self, inter: disnake.ApplicationCommandInteraction):
        # Картинка (О сервере) 
        embed1 = disnake.Embed(
            color=0x2b2d31
        )


        # Картинка (О сервере) 
        embed1.set_image(
            url="https://media.discordapp.net/attachments/1071030207726755882/1168624023358410962/Frame_10_1.png?ex=655270ef&is=653ffbef&hm=829a5481f2080555a1a183e59870a154d75acd70fb778cbc49346935255e83d6&=&width=960&height=319"
        )


        # Текст под которые под картинкой (о сервере)
        embed2 = disnake.Embed(
            description="Мы рады видеть вас на сервере [BLACK HOLE](https://discord.gg/Pbev9CHB)! Надеемся вам\nпонравится то, что мы делаем, а пока мы расскажем как попасть\nна приватный сервер.\n \nЧтобы играть на сервере, вам необходимо отправить заявку.\nНажмите кнопку \"Оставить заявку\" ниже, чтобы сделать это.",
            color=0x2b2d31
        )



        # Вы водит Embeds и кнопку 
        await inter.send(
            embeds=[embed1, embed2],
            components=[
                # Кнопка с хорактеристиками
                disnake.ui.Button(
                    label="Оставить заявку",
                    style=disnake.ButtonStyle.secondary,
                    custom_id="bt1",
                    emoji="openlinksvgrepocom1:1164218702909165650"
                )
            ]
        )


    async def add_to_whitelist(self, name):
        host = "ip"
        port = "порт"
        password = "пороль"
        mcr = MCRcon(host, password, port , timeout=60)
        mcr.connect()
        resp = mcr.command(f"easywl add {name}")
        print(resp)
        mcr.disconnect()

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "bt1":
            await inter.response.send_modal(Modals.Modal(self.bot))
        elif inter.component.custom_id == "bt2":
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            message_id = inter.message.id
            cur.execute('SELECT * FROM user WHERE message_id = ?', (message_id,))
            row = cur.fetchone()
            message1 = row[0]
            name = row[1]
            user = row[2]
            age = row[3]
            rule = row[4]
            id1 = row[5]
            print(message_id)

            if message_id == message1:
                await self.add_to_whitelist(name)

            guild = inter.guild
            member = guild.get_member(user)
            role = guild.get_role(1164894879646765067)

            await member.remove_roles(role)

            role = inter.guild.get_role(1161908642484858890)
            await member.add_roles(role)

            message_id = inter.message.id
            message = await inter.channel.fetch_message(message_id)
            await message.delete()

            embed = disnake.Embed(
                        description=f"Вы успешно добавили пользователя по имени <@{user}>\n \n__Заполненная заявка:__\n \n```Имя: {name}\nВозраст: {age}\nСогласны ли вы с правилами: {rule}\nКак вы попали на сервер: {id1}```",
                        color=0x2b2d31
            )

            await inter.send(embed=embed)

            embed1 = disnake.Embed(
                        description=f"Ваша заявка была __принята__\n \n__Заполненная заявка:__\n \n```Имя: {name}\nВозраст: {age}\nСогласны ли вы с правилами: {rule}\nКак вы попали на сервер: {id1}```",
                        color=0x2b2d31
            )

            channel = self.bot.get_channel(1159919319032013013)
            await channel.send(f"<@{user}>", embed=embed1)

        elif inter.component.custom_id == "bt3":
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            message_id = inter.message.id
            cur.execute('SELECT * FROM user WHERE message_id = ?', (message_id,))
            row = cur.fetchone()
            name = row[1]
            user = row[2]
            age = row[3]
            rule = row[4]
            id1 = row[5]
            print(message_id)

            message = await inter.channel.fetch_message(message_id)
            await message.delete()

            embed = disnake.Embed(
                        description=f"Вы успешно отклонили заявку пользователя по имени <@{user}>\n \n__Заполненная заявка:__\n \n```Имя: {name}\nВозраст: {age}\nСогласны ли вы с правилами: {rule}\nКак вы попали на сервер: {id1}```",
                        color=0x2b2d31
            )

            await inter.send(embed=embed)

            embed1 = disnake.Embed(
                        description=f"Ваша заявка была __отклонена__\n \n__Заполненная заявка:__\n \n```Имя: {name}\nВозраст: {age}\nСогласны ли вы с правилами: {rule}\nКак вы попали на сервер: {id1}```",
                        color=0x2b2d31
            )

            channel = self.bot.get_channel(1159919319032013013)

            await channel.send(f"<@{user}>", embed=embed1)

            guild = inter.guild
            member = guild.get_member(user)
            role = guild.get_role(1164894879646765067)

            await member.remove_roles(role)




def setup(bot):
    bot.add_cog(Oservere(bot))