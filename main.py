import interactions
from . import internal_t
import os
import aiofiles
from interactions.api.events import MessageCreate
from interactions import Task, IntervalTrigger

class Roles(interactions.Extension):
    module_base: interactions.SlashCommand = interactions.SlashCommand(
        name="roles",
        description="command about roles"
    )
    #機器人代@
    @module_base.subcommand("at", sub_cmd_description="Send a mention to the selected role")
    @interactions.slash_option(#選擇身分組
        name="role",
        description="Choose a role to @",
        required=True,
        opt_type=interactions.OptionType.ROLE  
    )
    async def at_role(self, ctx: interactions.SlashContext, role: interactions.Role):
        await ctx.send(f"{role.mention}")# @那個身分組
    #列出某人身上的身分組
    @module_base.subcommand("list", sub_cmd_description="List all roles of the user or another user")
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
