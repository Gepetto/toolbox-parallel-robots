from example_parallel_robots.loader_tools import completeRobotLoader
from toolbox_parallel_robots.slider_generation import createSlidersInterface
import pinocchio as pin
model,constraint_models,actuation_model,visual_model,collision_model = completeRobotLoader("battobot", freeflyer=True)
mot_ids_q = actuation_model.mot_ids_q

from toolbox_parallel_robots.mounting import closedLoopMountProximal
# entraxe = (dmodel.jointPlacements[2].translation[1])
entraxe=0.125
Lcontact_frame =[]
for idframe,f in enumerate(model.frames):

    if f.name == "foot_right":
        placement=pin.SE3.Identity()
        placement.translation[1]=entraxe
        Lcontact_frame.append([f,placement.copy()])
    if f.name == "foot_left":
        placement=pin.SE3.Identity()
        placement.translation[1]=-entraxe
        Lcontact_frame.append([f,placement.copy()])


torso_placement=pin.SE3.Identity()
torso_placement.translation[2]=0.55
id_torso=model.getFrameId("torso")
Lcontact_frame.append([model.frames[id_torso],torso_placement])
constraint_model=[]
q_prec=pin.neutral(model)
q_prec[:3]=[0,0,0.55]
for f1,placement in Lcontact_frame[:2]:
    constraint_model.append(pin.RigidConstraintModel(pin.ContactType.CONTACT_6D,model,f1.parentJoint,f1.placement,0,placement,pin.ReferenceFrame.LOCAL))

data=model.createData()
cdata=[c.createData() for c in constraint_model]
cdatas=[c.createData() for c in constraint_models]
q0 = closedLoopMountProximal(model,data,constraint_models+constraint_model,cdatas+cdata)

constraint_model=[]
q_prec=pin.neutral(model)
q_prec[:3]=[0,0,0.55]
for f1,placement in Lcontact_frame[:]:
    constraint_model.append(pin.RigidConstraintModel(pin.ContactType.CONTACT_6D,model,f1.parentJoint,f1.placement,0,placement,pin.ReferenceFrame.LOCAL))


data=model.createData()
cdata=[c.createData() for c in constraint_model]
cdatas=[c.createData() for c in constraint_models]

q0 = closedLoopMountProximal(model,data,constraint_models+constraint_model,cdatas+cdata,q_prec=q0)


# import example_robot_data as erd
# robot = erd.load("solo12")
# model, visual_model, collision_model = robot.model, robot.visual_model, robot.collision_model
# constraint_models = []
# mot_ids_q = [model.getJointId(joint_name) for joint_name in ["FL_HAA", "FL_HFE", "FL_KFE", "FR_HAA", "FR_HFE", "FR_KFE", "HL_HAA", "HL_HFE", "HL_KFE", "HR_HAA", "HR_HFE", "HR_KFE"]]
# * Create the visualizer
import pinocchio as pin
from pinocchio.visualize import MeshcatVisualizer
import meshcat
viz = MeshcatVisualizer(model, collision_model, visual_model)
viz.viewer = meshcat.Visualizer(zmq_url="tcp://127.0.0.1:6000")
viz.clean()
viz.loadViewerModel(rootNodeName="universe")
viz.display(q0)
createSlidersInterface(model, constraint_models, visual_model, mot_ids_q, viz,q0=q0)
