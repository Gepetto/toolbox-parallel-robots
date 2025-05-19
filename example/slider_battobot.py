from example_parallel_robots.loader_tools import completeRobotLoader
from toolbox_parallel_robots.slider_generation import createSlidersInterface
import pinocchio as pin
from toolbox_parallel_robots.mounting import closedLoopMountProximal


model, constraint_models, actuation_model, visual_model, collision_model = (
    completeRobotLoader("digit_2legs", freeflyer=True)
)
mot_ids_q = actuation_model.mot_ids_q


data = model.createData()
cdata = [c.createData() for c in constraint_model]
cdatas = [c.createData() for c in constraint_models]
q0 = closedLoopMountProximal(
    model, data, constraint_models + constraint_model, cdatas + cdata
)

constraint_model = []
q_prec = pin.neutral(model)
q_prec[:3] = [0, 0, 0.55]
for f1, placement in Lcontact_frame[:]:
    constraint_model.append(
        pin.RigidConstraintModel(
            pin.ContactType.CONTACT_6D,
            model,
            f1.parentJoint,
            f1.placement,
            0,
            placement,
            pin.ReferenceFrame.LOCAL,
        )
    )


data = model.createData()
cdata = [c.createData() for c in constraint_model]
cdatas = [c.createData() for c in constraint_models]

q0 = closedLoopMountProximal(
    model, data, constraint_models + constraint_model, cdatas + cdata, q_prec=q0
)


import pinocchio as pin
from pinocchio.visualize import MeshcatVisualizer
import meshcat

viz = MeshcatVisualizer(model, collision_model, visual_model)
viz.viewer = meshcat.Visualizer(zmq_url="tcp://127.0.0.1:6000")
viz.clean()
viz.loadViewerModel(rootNodeName="universe")
viz.display(q0)
createSlidersInterface(model, constraint_models, visual_model, mot_ids_q, viz, q0=q0)
