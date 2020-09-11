from os import stat
import aiohttp


async def verifyQmailUid(qq: int, uid: int) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://mcskin.littleservice.cn/api/verifyQmailUid',
                               params={'qq': qq, 'uid': uid}) as resp:
            statusCode = resp.status
    return statusCode
