"""
-*- coding: utf-8 -*-
Ludovic DE MATTEIS - May 2023

Create a Tkinter interface to move some joints in the robots while satisfying the desired closed loop constraints

"""

import tkinter as tk
import pinocchio as pin
from toolbox_parallel_robots.tk_robot_sliders import SlidersFrame
from toolbox_parallel_robots.tk_sliders_manager import SlidersManager

# * Interface to activate or deactivate constraints on the robot


def createSlidersInterface(
    model, constraint_models, visual_model, mot_ids_q, viz, q0=None
):
    """
    Create a Tkinter interface to move some joints in the robots while satisfying the desired closed loop constraints
    """
    if q0 is None:
        q0 = pin.neutral(model)

    # # * Adding constraints
    # addXYZAxisToConstraints(model, visual_model, constraint_models, scale=scale)

    # # * Add frames to all joints
    # addXYZAxisToJoints(model, visual_model, scale=scale)

    # * Create data
    data = model.createData()
    constraint_datas = [cm.createData() for cm in constraint_models]
    # * Set a scale factor to handle too small and too big robots
    scale = 1

    # replaceGeomByXYZAxis(visual_model, viz, scale=scale)
    # viz.display(q0)

    # * Create the interface
    root = tk.Tk()
    root.bind("<Escape>", lambda ev: root.destroy())
    root.title("Simple Robot Sliders")
    sliders_frame = SlidersFrame(model, mot_ids_q, q0, viz, constraint_models)
    # Creating sliders, main projection functions are called when the sliders are moved
    sliders_frame.createSlider(root)

    managerWindow = tk.Toplevel()
    managerWindow.bind("<Escape>", lambda ev: root.destroy())

    sliders_manager = SlidersManager(sliders_frame, constraint_models)
    sliders_manager.createButtons(managerWindow)

    root.mainloop()
