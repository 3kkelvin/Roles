import interactions
import os
import aiofiles
ALLOWED_PARTY = ["海外", "台灣", "美加"]
ATABLE_ROLES = ["国务大臣（管理员）"]

class Roles(interactions.Extension):
    roles_base: interactions.SlashCommand = interactions.SlashCommand(
        name="roles",
        description="command about roles"
    )
    at_group: interactions.SlashCommand = roles_base.group(
        name="at",
        description="command about @"
    )

    at_group.subcommand("party", sub_cmd_description="To @party")
    @interactions.slash_option(#選擇身分組
        name="party",
        description="Choose a party to @",
        required=True,
        opt_type=interactions.OptionType.ROLE  
    )
    async def at_party(self, ctx: interactions.SlashContext, role: interactions.Role):
        await ctx.send(f"{role.mention}")# @黨派身分組
    @interactions.autocomplete("party")#自動補全，限制選項
    async def autocomplete_party(self, ctx: interactions.AutocompleteContext):
        await ctx.send(choices=[{"name": i, "value": i} for i in ALLOWED_PARTY])

    at_group.subcommand("manager", sub_cmd_description="To @manager")
    @interactions.slash_option(#選擇身分組
        name="manager",
        description="Choose a manager to @",
        required=True,
        opt_type=interactions.OptionType.ROLE  
    )
    async def at_manager(self, ctx: interactions.SlashContext, role: interactions.Role):
        await ctx.send(f"{role.mention}")# @黨派身分組
    @interactions.autocomplete("manager")#自動補全，限制選項
    async def autocomplete_manager(self, ctx: interactions.AutocompleteContext):
        await ctx.send(choices=[{"name": i, "value": i} for i in ATABLE_ROLES])

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
