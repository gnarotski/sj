from panda3d.core import PandaNode, Loader, NodePath, CollisionNode, CollisionSphere, CollisionInvSphere, CollisionCapsule, Vec3
class PlacedObject(PandaNode):
	def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str):
		self.model: NodePath = loader.loadModel(modelPath)
		if not isinstance(self.model, NodePath):
			raise(AssertionError(modelPath+" is not a proper modelPath"))
		self.model.reparentTo(parentNode)
		self.model.setName(nodeName)
class CollidableObject(PlacedObject):
	def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str):
		super(CollidableObject,self).__init__(loader, modelPath, parentNode, nodeName)
		self.collisionNode=self.model.attachNewNode(CollisionNode(nodeName+'_cNode'))
class InverseSphereCollideObject(CollidableObject):
	def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,colPositionVec:Vec3, colRadius):
		super(InverseSphereCollideObject,self).__init__(loader, modelPath, parentNode, nodeName)
		self.collisionNode.node().addSolid(CollisionInvSphere(colPositionVec, colRadius))
		self.collisionNode.show()
class CapsuleCollideObject(CollidableObject):
	def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,ax:float,ay:float,az:float,bx:float,by:float,bz:float,r:float):
		super(CapsuleCollideObject,self).__init__(loader, modelPath, parentNode, nodeName)
		self.collisionNode.node().addSolid(CollisionCapsule(ax,ay,az,bx,by,bz,r))
		self.collisionNode.reparentTo(base.render)
		self.collisionNode.show()
class SphereCollideObject(CollidableObject):
	def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,colPositionVec:Vec3, colRadius):
		super(SphereCollideObject,self).__init__(loader, modelPath, parentNode, nodeName)
		self.collisionNode.node().addSolid(CollisionSphere(colPositionVec, colRadius))
		self.collisionNode.reparentTo(base.render)
		self.collisionNode.show()