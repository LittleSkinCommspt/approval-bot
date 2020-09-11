import asyncio
import os
import re

from graia.application import GraiaMiraiApplication, Session
from graia.application.entry import MemberJoinRequestEvent, MessageChain, Plain
from graia.broadcast import Broadcast

from chancechecker import chanceChecker
from verifyuid import verifyQmailUid

# Application & BCC 初始化
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(broadcast=bcc,
                            connect_info=Session(
                                host=os.environ['graia-host'],
                                authKey=os.environ['graia-authkey'],
                                account=int(os.environ['graia-account']),
                                websocket=True),
                            enable_chat_log=False
                            )


class qqGroup(object):
    '''QQ 群号'''
    main = 586146922  # 主用户群
    cafe = 651672723  # 咖啡馆
    admins = 985317265  # 运营组


workInGroups = [qqGroup.main, qqGroup.cafe]  # 在这些群内工作


@bcc.receiver(MemberJoinRequestEvent)
async def command_test(app: GraiaMiraiApplication, event: MemberJoinRequestEvent):
    app.logger.info(f'{event.supplicant} 试图加入 {event.groupName}')
    # 判断是否为指定群组
    currentGroup = event.groupId
    if currentGroup in workInGroups:
        _userQq = event.supplicant
        c = chanceChecker(_userQq)
        if not c.hasChance:
            await event.reject('由于未正确填写 UID，你的入群机会已经耗尽')
            return
        # 是否已在其他群中
        otherGroups = workInGroups
        otherGroups.remove(currentGroup)
        inOtherGroups: bool = False
        for g in otherGroups:
            if await app.getMember(group=g, member_id=_userQq):
                inOtherGroups = True
        if inOtherGroups:
            c.remove()
            await event.accept()
            return
        # 验证 QQ 与 UID
        _requestMessage = event.message.strip()  # 除去首尾空格
        _answer = re.search(r'答案：(.*)', _requestMessage)  # 正则匹配 UID
        _uid = _answer.group(1)  # 取出 UID
        print(_uid)
        if not _answer:
            return
        if _uid.isdigit:  # UID 中只填写了数字（有效）
            _status = await verifyQmailUid(_userQq, _uid)  # 验证
            if _status == 200:  # 成功
                c.remove()
                await event.accept()
            elif _status == 403:  # 手动操作
                await app.sendGroupMessage(
                    qqGroup.admins,
                    MessageChain.create(
                        [Plain(f'{_userQq} 试图加入 {event.groupName}，UID 为 {_uid}')])
                )
            elif _status == 404:  # 找不到 UID
                c.addOnce()
                await event.reject(f'UID 不正确')
        else:
            c.addOnce()
            await event.reject('UID 应为纯数字')


if __name__ == '__main__':
    app.launch_blocking()
