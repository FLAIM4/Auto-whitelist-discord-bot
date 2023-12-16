import disnake
from disnake.ext import commands
from disnake import TextInputStyle
import time
import sqlite3


class Modal(commands.Cog, disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        self.con = sqlite3.connect('data.db')

        components = [
            disnake.ui.TextInput(
                label="Введите имя из игры",
                placeholder=None,
                custom_id="name",
                style=TextInputStyle.short,
                max_length=16,
            ),
            disnake.ui.TextInput(
                label="Введите свой возраст",
                placeholder=None,
                custom_id="age",
                style=TextInputStyle.short,
                max_length=2,
            ),
            disnake.ui.TextInput(
                label="Согласны ли вы соблюдать правила?",
                placeholder=None,
                custom_id="rule",
                style=TextInputStyle.short,
                max_length=3,
            ),
            disnake.ui.TextInput(
                label="Как вы попали к нам?",
                placeholder=None,
                custom_id="id1",
                style=TextInputStyle.paragraph,
            ),
        ] 

        super().__init__(title="Процесс заполнения заявки", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        Modal.human = inter.author.id
        Modal.name = inter.text_values.get("name")
        Modal.age = inter.text_values.get("age")
        Modal.rule = inter.text_values.get("rule")
        Modal.id1 = inter.text_values.get("id1")

        role = inter.guild.get_role(1164894879646765067)
        await inter.author.add_roles(role)

        
        embed = disnake.Embed(
            title="__Заявка была отправлена!__",
            description=f"Ваша заявка была отправлена на проверку. Это может занять около 5 минут до нескольких суток.\n \n__Заполненная заявка:__\n \n```Имя: {Modal.name}\nВозраст: {Modal.age}\nСогласны ли вы с правилами: {Modal.rule}\nКак вы попали на сервер: {Modal.id1}```",
            color=0x2b2d31
        )
        embed.set_thumbnail(url=inter.author.avatar.url)
        embed2 = disnake.Embed(
            title=None,
            description=None,
            color=0x2b2d31
        )
        embed2.set_image(url="https://media.discordapp.net/attachments/1071030207726755882/1168632679177146388/Frame_10_2.png?ex=655278fe&is=654003fe&hm=7de5be1279a9f38fcb7ec25c0462d17ca1a88dc67042959db09205b775b19d2c&=&width=960&height=319")
        embed1 = disnake.Embed(
            description=f"Пользователь, идентифицируемый как <@{inter.author.id}>, находится в \nсостоянии ожидания подтвержденияего заявки на вступление на \nсервер [BLACK HOLE](https://discord.gg/Pbev9CHB).\n \n__Заполненная заявка:__\n \n```Имя: {Modal.name}\nВозраст: {Modal.age}\nСогласны ли вы с правилами: {Modal.rule}\nКак вы попали на сервер: {Modal.id1}```",
            color=0x2b2d31
        )

        channel = self.bot.get_channel(1159919164559999007)

        message = await channel.send(embeds=[embed2,embed1], components=[
            disnake.ui.Button(
                label="Принять",
                custom_id="bt2",
                style=disnake.ButtonStyle.success,
            ),
            disnake.ui.Button(
                label="Отклонить",
                custom_id="bt3",
                style=disnake.ButtonStyle.secondary,
            )
        ])
        message_id = message.id
        user = inter.author.id
        cur = self.con.cursor()
        cur.execute("""INSERT INTO USER(message_id, name, id_user, age, rule , id1) VALUES (?, ?, ?,?, ?, ?)""",(message_id, Modal.name, user , Modal.age, Modal.rule, Modal.id1))
        self.con.commit()

        await inter.send(embed=embed, ephemeral=True)