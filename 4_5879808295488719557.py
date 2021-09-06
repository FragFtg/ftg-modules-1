#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging
import io

from telethon import types, functions
from telethon.tl.types import User, Channel
from telethon.errors import MessageIdInvalidError, UserNotParticipantError

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class BlockNonDiscussionMod(loader.Module):
    """Block Comments For Non Discussion Members"""
    strings = {"name": "Block Non Discussion",
               "trigger": (", zum Kommentieren tritt bitte dem Chat bei.")}

    def __init__(self):
        self._ratelimit = []

    async def watcher(self, message):

        watchedchat = 1287869945
        chat = await message.get_chat()

        if not chat.id == watchedchat or message.is_private:
            return 
        user = await message.get_sender()
        entity = await message.client.get_entity(user.id)
        
        if not isinstance(entity, User):
            if entity.has_link:
                return
        usertag = "<a href=tg://user?id=" + str(user.id) + ">" + user.first_name + "</a>"
        try:
            permissions = await message.client.get_permissions(chat.id, user.id)
            return
        except UserNotParticipantError:
            await message.delete()
            replymsg = await utils.answer(message, usertag + self.strings("trigger", message))
            await asyncio.sleep(60)
            for x in replymsg:
                await x.delete()
                return
        except ValueError:
            return
        except AttributeError:
            return