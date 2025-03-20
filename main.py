import interactions
import os
import aiofiles
PARTY_REQUIRE_ROLE_ID = 1200043628899356702 #選民
PARTY_ROLE_IDS = {
    "大舞台反对派联盟": 1344339893106774129,
    "大舞台活动党": 1344347203400896533,  
    "自由社會大舞台改革聯盟": 1344477869342195722   
}
#ATABLE_ROLES = ["国务大臣（管理员）"]

class Roles(interactions.Extension):
    roles_base: interactions.SlashCommand = interactions.SlashCommand(
        name="roles",
        description="command about roles"
    )
    at_group: interactions.SlashCommand = roles_base.group(
        name="at",
        description="command about @"
    )

    @at_group.subcommand("party", sub_cmd_description="To @party")
    @interactions.slash_option(#選擇身分組  
        name="party",
        description="Choose a party to @",
        required=True,
        opt_type=interactions.OptionType.STRING,
        autocomplete=True  
    )
    async def at_party(self, ctx: interactions.SlashContext, party: str):
        role_id = PARTY_ROLE_IDS.get(party)#根據選擇的名稱取得 ID
        if not role_id:
            await ctx.send("無效的選擇，請重新嘗試。")
            return
        role = ctx.guild.get_role(role_id)#透過 ID 取得角色物件
        if not role:
            await ctx.send("找不到該身分組，請找技術公務員。")
            return
        if role_id not in [r.id for r in ctx.author.roles]:#檢查是否符合身分
            await ctx.send("你不在該黨派中，無法 @ 該身分組。")
            return
        await ctx.send(f"{role.mention}") 
    @at_party.autocomplete("party")  
    async def autocomplete_party(self, ctx: interactions.AutocompleteContext):
        await ctx.send(choices=[{"name": i, "value": i} for i in PARTY_ROLE_IDS.keys()])

    '''@at_group.subcommand("manager", sub_cmd_description="To @manager")
    @interactions.slash_option(#選擇身分組
        name="manager",
        description="Choose a manager to @",
        required=True,
        opt_type=interactions.OptionType.ROLE, 
        autocomplete=True 
    )
    async def at_manager(self, ctx: interactions.SlashContext, role: interactions.Role):
        await ctx.send(f"{role.mention}")# @黨派身分組
    @at_manager.autocomplete("manager")#自動補全，限制選項
    async def autocomplete_manager(self, ctx: interactions.AutocompleteContext):
        await ctx.send(choices=[{"name": i, "value": i} for i in ATABLE_ROLES])'''

    #手動檢查所有用戶的身分組 (管理員可執行)
    @roles_base.subcommand("partycheck", sub_cmd_description="check all member's party roles")
    async def partycheck(self, ctx: interactions.SlashContext):
        guild = ctx.guild
        member_count = 0
        removed_count = 0
        role_objects = {role.id: role for role in guild.roles}#建立伺服器內role跟roleID的字典

        for member in guild.members:
            require_role = PARTY_REQUIRE_ROLE_ID in [role.id for role in member.roles]
            party_roles = [role_objects[role_id] for role_id in [role.id for role in member.roles] if role_id in PARTY_ROLE_IDS.values()]
            member_count += 1
            if not require_role and party_roles:
                for role in party_roles:
                    await member.remove_roles([role])
                # await ctx.send(f"party_roles: {party_roles}")
                removed_count += 1

        await ctx.send(f"已檢查{member_count}位用戶，共移除 {removed_count} 位成員的黨派身分組。")
'''
    #機器人代@
    @at_group.subcommand("roles", sub_cmd_description="Send a mention to the selected role")
    @interactions.slash_option(#選擇身分組
        name="role",
        description="Choose a role to @",
        required=True,
        opt_type=interactions.OptionType.ROLE  
    )
    async def at_role(self, ctx: interactions.SlashContext, role: interactions.Role):
        await ctx.send(f"{role.mention}")# @那個身分組
    #列出某人身上的身分組
    @roles_base.subcommand("list", sub_cmd_description="List all roles of the user or another user")
    @interactions.slash_option(# 可選項 某個人
        name="user",
        description="Select a user to list roles (optional)",
        required=False,  
        opt_type=interactions.OptionType.USER  
    )
    async def list_roles(self, ctx: interactions.SlashContext, user: interactions.User = None):
        if user is None:# 如果沒有選成員，列出自己的身分組
            roles = ctx.author.roles
        else:
            member = ctx.guild.get_member(user.id)  #獲取該成員在伺服器中的資料
            if member is None:
                await ctx.send("User not found in this server.")
                return
            roles = member.roles
        # 過濾掉 @everyone 
        role_names = [role.name for role in roles if role.name != "@everyone"]
        if role_names:
            await ctx.send(f"Roles: {', '.join(role_names)}")
        else:
            await ctx.send("This user does not have any roles apart from @everyone.")
'''