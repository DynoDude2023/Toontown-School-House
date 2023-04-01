import random

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.toon import InventoryBase


class DistributedObstacleBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedObstacleBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.cameraDamage = [8, 12, 15]
        self.chopperDamage = [15, 20, 25]

    def setOuch(self, penalty):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        self.notify.debug('setOuch %s' % penalty)
        if av and penalty > 0:
            av.takeDamage(penalty)
            if av.getHp() <= 0:
                av.inventory.zeroInv()
                av.d_setInventory(av.inventory.makeNetString())

    def zapToon(self, x, y, z, h, p, r, attackCode, timestamp):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return
        toon = self.air.doId2do.get(avId)
        if toon:
            self.d_showZapToon(avId, x, y, z, h, p, r, attackCode, timestamp)
            damage = 15
            if damage == None:
                self.notify.warning('No damage listed for attack code %s' % attackCode)
                damage = 5
            damage *= 1.0
            self.damageToon(toon, damage)
        return

    def d_showZapToon(self, avId, x, y, z, h, p, r, attackCode, timestamp):
        self.sendUpdate('showZapToon', [avId,
                                        x,
                                        y,
                                        z,
                                        h,
                                        p,
                                        r,
                                        attackCode,
                                        timestamp])

    def damageToon(self, toon, deduction):
        toon.takeDamage(deduction)
        if toon.getHp() <= 0:
            empty = InventoryBase.InventoryBase(toon)
            toon.b_setInventory(empty.makeNetString())

    def trapFire(self, isChopper):
        avId = self.air.getAvatarIdFromSender()
        toon = self.air.doId2do.get(avId)
        if toon:
            if isChopper == True:
                toon.takeDamage(random.choice(self.chopperDamage))
            else:
                toon.takeDamage(random.choice(self.cameraDamage))

    def d_showObstacle(self):
        self.sendUpdate('showObstacle')

    def d_setPos(self, x, y, z):
        self.sendUpdate('setPos', [x, y, z])

    def d_setHpr(self, h, p, r):
        self.sendUpdate('setHpr', [h, p, r])

    def d_setPosHpr(self, x, y, z, h, p, r):
        self.sendUpdate('setPosHpr', [x, y, z, h, p, r])

    def d_setScale(self, sx, sy=None, sz=None):
        if not sy:
            sy = sx

        if not sz:
            sz = sx

        self.sendUpdate('setScale', [sx, sy, sz])
