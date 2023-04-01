from direct.distributed.ClockDelta import *
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from panda3d.core import *

from toontown.distributed import DelayDelete
from toontown.toonbase import ToontownGlobals


class DistributedObstacleBase(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedObstacleBase')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.activeIntervals = {}
        self.toonSphere = None

    def delete(self):
        self.cleanupIntervals()
        self.disableLocalToonSimpleCollisions()
        DistributedObject.delete(self)

    def b_setOuch(self, penalty, anim=None):
        self.notify.debug('b_setOuch %s' % penalty)
        av = base.localAvatar
        if not av.isStunned:
            self.d_setOuch(penalty)
            self.setOuch(penalty, anim)

    def d_setOuch(self, penalty):
        self.sendUpdate('setOuch', [penalty])

    def setOuch(self, penalty, anim=None):
        if anim == 'Squish':
            if base.cr.playGame.getPlace():
                base.cr.playGame.getPlace().fsm.request('squished')
        elif anim == 'Fall':
            if base.cr.playGame.getPlace():
                base.cr.playGame.getPlace().fsm.request('fallDown')
        av = base.localAvatar
        av.stunToon()
        av.playDialogueForString('!')

    def touchedGavel(self, gavel, entry):
        self.notify.debug('touchedGavel')
        attackCodeStr = entry.getIntoNodePath().getNetTag('attackCode')
        if attackCodeStr == '':
            self.notify.warning('Node %s has no attackCode tag.' % repr(entry.getIntoNodePath()))
            return
        attackCode = int(attackCodeStr)
        into = entry.getIntoNodePath()
        self.zapLocalToon(attackCode, into)

    def touchedGavelHandle(self, gavel, entry):
        attackCodeStr = entry.getIntoNodePath().getNetTag('attackCode')
        if attackCodeStr == '':
            self.notify.warning('Node %s has no attackCode tag.' % repr(entry.getIntoNodePath()))
            return
        attackCode = int(attackCodeStr)
        into = entry.getIntoNodePath()
        self.zapLocalToon(attackCode, into)

    def zapLocalToon(self, attackCode, origin=None):
        if localAvatar.ghostMode or localAvatar.isStunned:
            return
        messenger.send('interrupt-pie')
        place = self.cr.playGame.getPlace()
        currentState = None
        if place:
            currentState = place.fsm.getCurrentState().getName()
        if currentState != 'walk' and currentState != 'finalBattle' and currentState != 'crane':
            return
        toon = localAvatar
        fling = 1
        shake = 0
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            fling = 0
            shake = 1
        if fling:
            if origin == None:
                origin = self
            camera.wrtReparentTo(render)
            toon.headsUp(origin)
            camera.wrtReparentTo(toon)
        pos = toon.getPos()
        hpr = toon.getHpr()
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('zapToon', [pos[0],
                                    pos[1],
                                    pos[2],
                                    hpr[0] % 360.0,
                                    hpr[1],
                                    hpr[2],
                                    attackCode,
                                    timestamp])
        self.doZapToon(toon, fling=fling, shake=shake)
        return

    def showZapToon(self, toonId, x, y, z, h, p, r, attackCode, timestamp):
        if toonId == localAvatar.doId:
            return
        ts = globalClockDelta.localElapsedTime(timestamp)
        pos = Point3(x, y, z)
        hpr = VBase3(h, p, r)
        fling = 1
        toon = self.cr.doId2do.get(toonId)
        if toon:
            if attackCode == ToontownGlobals.BossCogAreaAttack:
                pos = None
                hpr = None
                fling = 0
            else:
                ts -= toon.smoother.getDelay()
            self.doZapToon(toon, pos=pos, hpr=hpr, ts=ts, fling=fling)
        return

    def doZapToon(self, toon, pos=None, hpr=None, ts=0, fling=1, shake=1):
        zapName = toon.uniqueName('zap')
        self.clearInterval(zapName)
        zapTrack = Sequence(name=zapName)
        if toon == localAvatar:
            self.toOuchMode()
            messenger.send('interrupt-pie')
            self.enableLocalToonSimpleCollisions()
        else:
            zapTrack.append(Func(toon.stopSmooth))

        def getSlideToPos(toon=toon):
            return render.getRelativePoint(toon, Point3(0, -5, 0))

        if pos != None and hpr != None:
            (zapTrack.append(Func(toon.setPosHpr, pos, hpr)),)
        toonTrack = Parallel()
        if shake and toon == localAvatar:
            toonTrack.append(
                Sequence(Func(camera.setZ, camera, 1), Wait(0.15), Func(camera.setZ, camera, -2), Wait(0.15),
                         Func(camera.setZ, camera, 1)))
        if fling:
            toonTrack += [ActorInterval(toon, 'slip-backward'), toon.posInterval(0.5, getSlideToPos, fluid=1)]
        else:
            toonTrack += [ActorInterval(toon, 'slip-forward')]
        zapTrack.append(toonTrack)
        if toon == localAvatar:
            zapTrack.append(Func(self.disableLocalToonSimpleCollisions))
            currentState = self.state
            if currentState == 'BattleThree':
                zapTrack.append(Func(self.toFinalBattleMode))
            elif hasattr(self, 'chairs'):
                zapTrack.append(Func(self.toFinalBattleMode))
            else:
                zapTrack.append(Func(self.toWalkMode))
        else:
            zapTrack.append(Func(toon.startSmooth))
        if ts > 0:
            startTime = ts
        else:
            zapTrack = Sequence(Wait(-ts), zapTrack)
            startTime = 0
        zapTrack.append(Func(self.clearInterval, zapName))
        zapTrack.delayDelete = DelayDelete.DelayDelete(toon, 'DistributedObstacleBase.doZapToon')
        zapTrack.start(startTime)
        self.storeInterval(zapTrack, zapName)
        return

    def storeInterval(self, interval, name):
        if name in self.activeIntervals:
            ival = self.activeIntervals[name]
            if hasattr(ival, 'delayDelete') or hasattr(ival, 'delayDeletes'):
                self.clearInterval(name, finish=1)
        self.activeIntervals[name] = interval

    def cleanupIntervals(self):
        for interval in self.activeIntervals.values():
            interval.finish()
            DelayDelete.cleanupDelayDeletes(interval)

        self.activeIntervals = {}

    def clearInterval(self, name, finish=1):
        if self.activeIntervals.has_key(name):
            ival = self.activeIntervals[name]
            if finish:
                ival.finish()
            else:
                ival.pause()
            if self.activeIntervals.has_key(name):
                DelayDelete.cleanupDelayDeletes(ival)
                del self.activeIntervals[name]
        else:
            self.notify.debug('interval: %s already cleared' % name)

    def toOuchMode(self):
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                place.setState('ouch')

    def toWalkMode(self):
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                place.setState('walk')

    def enableLocalToonSimpleCollisions(self):
        if not self.toonSphere:
            sphere = CollisionSphere(0, 0, 1, 1)
            sphere.setRespectEffectiveNormal(0)
            sphereNode = CollisionNode('SimpleCollisions')
            sphereNode.setFromCollideMask(ToontownGlobals.WallBitmask | ToontownGlobals.FloorBitmask)
            sphereNode.setIntoCollideMask(BitMask32.allOff())
            sphereNode.addSolid(sphere)
            self.toonSphere = NodePath(sphereNode)
            self.toonSphereHandler = CollisionHandlerPusher()
            self.toonSphereHandler.addCollider(self.toonSphere, localAvatar)
        self.toonSphere.reparentTo(localAvatar)
        base.cTrav.addCollider(self.toonSphere, self.toonSphereHandler)

    def disableLocalToonSimpleCollisions(self):
        if self.toonSphere:
            base.cTrav.removeCollider(self.toonSphere)
            self.toonSphere.detachNode()

    def showObstacle(self):
        if hasattr(self, 'reparentTo'):
            self.reparentTo(render)
