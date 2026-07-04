import LibPhysics.Shape
import LibPhysics.RigidBody
import LibPhysics.Collision

class Scene:
    def __init__(self):
        self.Shapes = []
        self.RigidBodies = []
    def __del__(self):
        pass
    
    def Update(self, deltaSec):
        for rb in self.RigidBodies:
            rb.ApplyGravity(deltaSec)

        Contacts = []
        # BroadPhase
        # NarrowPhase
        Len = len(self.RigidBodies)
        for i in range(Len):
            for j in range(i + 1, Len):
                rbA = self.RigidBodies[i]
                rbB = self.RigidBodies[j]
                if rbA.Mass_Inverse == 0.0 and rbB.Mass_Inverse == 0.0:
                    continue

                ct = LibPhysics.Collision.Contact()
                if LibPhysics.Collision.ConservativeAdvance(rbA, rbB, deltaSec, ct):
                    if ct.TimeOfImpact == 0.0:
                        # Manifold.append(ct)
                        None
                    else:
                        Contacts.append(ct)

        Contacts.sort(key = lambda rhs: rhs.TimeOfImpact, reverse = False)
        
        if len(Contacts):
            print(len(Contacts))

        # SolveConstraints

        # TOI 毎にタイムスライスしてシミュレーションを進める
        accTime = 0.0
        for i in Contacts:
            # 次の衝突まで進める
            delta = i.TimeOfImpact - accTime
            for rb in self.RigidBodies:
                rb.Update(delta)

            # 衝突による力積の適用
            #ApplyImpulse(i)
            
            accTime += delta

        # 残りのシミュレーションを進める
        delta = deltaSec - accTime
        if 0.0 < delta:
            for rb in self.RigidBodies:
                rb.Update(delta)
