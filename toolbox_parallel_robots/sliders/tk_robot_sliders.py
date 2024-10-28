import tkinter as tk
import numpy as np
import pinocchio as pin
from functools import partial
from toolbox_parallel_robots.mounting import closedLoopMountProximal
class SlidersFrame:
    """
    Create a tk.Frame and add sliders corresponding to robot joints.
    Return the tk.Frame, that must be added to the container.
    """
    NROW = 6  # Number of sliders per row

    def __init__(self, model, mot_ids_q, q0, viz,constraint_models):
        """
        motors is a list of joint names that must be highlighted in blue
        """
        self.rmodel = model
        self.mot_ids_q = mot_ids_q
        self.viz = viz
        self.q0 = q0.copy()
        self.slider_vars = []

        self.auto_refresh = True
        self.active_constraint_models = []
        self.rdata= model.createData()
        self.cmodel=constraint_models
        self.cdata=[c.createData() for c in constraint_models]
        self.old_q=q0

    def reset(self):
        self.setConfiguration(self.q0)
        self.viz.display(self.q0)

    def setConfiguration(self, qref):
        dq_ref = pin.difference(self.rmodel, self.q0, qref)
        for i, s in enumerate(self.slider_vars):
            s.set(dq_ref[i])

    def getConfiguration(self):
        values = [var.get() for var in self.slider_vars]
        dq = np.array(values)
        nq = pin.integrate(self.rmodel, self.q0, dq)
        if len(self.cmodel)==[]:
            q=nq.copy()
        else:
        ##closedlooprespect
            local_constraint=[]
            for id_joint,joint in enumerate(self.rmodel.joints):
                if joint.nq == 1:
                    id_dq=joint.idx_v
                    if abs(dq[id_dq]) > 1e-3 :
                        id_joint_parent=self.rmodel.parents[id_joint]
                        rotate=pin.SE3.Identity()
                        rotate.rotation = pin.utils.rotate('z',dq[id_dq])
                        joint_placement=self.rmodel.jointPlacements[id_joint] * rotate
                        constraint=pin.RigidConstraintModel(pin.ContactType.CONTACT_6D,self.rmodel,id_joint_parent,joint_placement,id_joint,pin.SE3.Identity(),pin.ReferenceFrame.LOCAL)
                        local_constraint.append(constraint)

            local_constraint_data=[c.createData() for c in local_constraint]
            q = closedLoopMountProximal(self.rmodel,self.rdata,self.cmodel+local_constraint,self.cdata+local_constraint_data,q_prec=self.old_q)

            q[:7]=nq[:7]
        self.old_q=q
        return q

    def display(self):
        q = self.getConfiguration()
        self.viz.display(q)
    
    def on_slider_move(self, iq, e):
        if self.auto_refresh:
            self.display()

    def createSlider(self, tkParent):
        # Frame pour les sliders
        frame = tk.Frame(tkParent)

        # Création des sliders verticaux
        iq = 0
        for j, name in enumerate(self.rmodel.names):
            if j == 0:
                continue
            for iv in range(self.rmodel.joints[j].nv):
                
                var = tk.DoubleVar(value=0)
                self.slider_vars.append(var)

                if self.rmodel.joints[j].idx_q in self.mot_ids_q:
                    slider_frame = tk.Frame(
                        frame,
                        highlightbackground=("blue" if self.rmodel.joints[j].idx_q in self.mot_ids_q
                            else "black"),
                        highlightthickness=1,
                    )
                    row = iq // self.NROW
                    slider_frame.grid(
                        row=row * 1, column=iq - self.NROW * row, padx=0, pady=0
                    )
                    name_i = name if self.rmodel.joints[j].nv == 1 else name + f"{iv}"
                    slider_label = tk.Label(slider_frame, text=name_i)
                    slider_label.pack(side=tk.BOTTOM)
                    slider = tk.Scale(
                        slider_frame,
                        variable=var,
                        orient=tk.HORIZONTAL,
                        from_=-3.0,
                        to=3.0,
                        resolution=0.01,
                        command=partial(self.on_slider_move, iq),
                    )  # When sliders are moved, call this function
                    slider.pack(side=tk.BOTTOM)
                    iq += 1
            frame.pack(side=tk.TOP)
        return frame

