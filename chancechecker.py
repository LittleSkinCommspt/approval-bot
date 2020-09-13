from typing import Dict
import pickle
import os.path

# settings
chanceCacheFilename = 'chances.cache'
chanceType = Dict[str, int]
chanceThreshold: int = 3

# check whether cache file was exist, if not, create it
if not os.path.exists(chanceCacheFilename):
    with open(chanceCacheFilename, 'wb') as f:
        pickle.dump(dict(), f)

class Chance(object):
    chance: chanceType
    def __enter__(self):
        with open(chanceCacheFilename, 'rb') as f:
            self.chance = pickle.load(f)
            return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(chanceCacheFilename, 'wb') as f:
            pickle.dump(self.chance, f)

class chanceChecker(object):
    '''机会检查器'''
    qq: str
    chance: chanceType

    def __init__(self, qqnum: int) -> None:
        self.qq = str(qqnum)

    def addOnce(self) -> None:
        '''增加一次使用'''
        with Chance() as c:
            if not self.qq in c.chance:  # 不存在则创建
                c.chance[self.qq] = 0
            c.chance[self.qq] += 1
    
    def remove(self) -> None:
        '''删除使用次数'''
        with Chance() as c:
            if self.qq in c.chance:
                del c.chance[self.qq]

    def hasChance(self) -> bool:
        '''是否有机会，有机会返回 `True`'''
        with Chance() as c:
            return c.chance[self.qq] < chanceThreshold if self.qq in c.chance else True
