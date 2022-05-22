from discord import Member, PermissionOverwrite, Role

import db


class Permission:
    def __init__(self, member: Member):
        self.member = member

        self.perms = {}

        self.users = db.Users()
        self.dbroles = db.Role()

    async def fetch_info(self) -> db.models.UsersModels:
        return await self.users.fetch(self.member.id)

    async def sync_voice_perms(self):
        self.perms[self.member.id] = self.member.voice.channel.overwrites
        return self


class BackPerms(Permission):
    def __init__(self, member: Member):
        super().__init__(member)

    def set_everyone(self):
        self.perms[self.member.guild.default_role] = PermissionOverwrite(
            view_channel=False, connect=False
        )

    async def set_gender(self):
        user_info = await self.fetch_info()

        gsp_data = await self.dbroles.fetch(self.member.guild.id)

        boy = self.member.guild.get_role(gsp_data.boy)
        girl = self.member.guild.get_role(gsp_data.girl)

        gender_name = user_info.gender

        if gender_name == "boy":
            isomerism = girl
        else:
            isomerism = boy

        self.perms[isomerism] = PermissionOverwrite(view_channel=True)

    async def set_bot(self):
        gsp_data = await self.dbroles.fetch(self.member.guild.id)

        for bot_role_id in gsp_data.bot:
            bot_role = self.member.guild.get_role(bot_role_id)
            self.permns[bot_role] = PermissionOverwrite(view_channel=True, connect=True)

    def set_creater(self):
        self.perms[self.member] = PermissionOverwrite(view_channel=True, connect=True)

    def set_custom(self, target: Member | Role, **kwargs):
        self.perms[target] = PermissionOverwrite(**kwargs)

    def set_vc_open_room_perms(self):
        self.set_everyone()
        self.set_creater()
        self.set_gender()
        self.set_bot()

        """
        member: {
            everyone: view_channel:=False, connect=True
            creater: view_channel=True, connect=True
            isomerism: view_channel=True
            bot: view_channel=True, connect=True
        }
        
        """

    def items(self):
        return self.perms.items()
