# Toolbox Parallel Robots
This repository includes usefull functions for working with robots with rigid bilateral contacts.

This was originally designed for working with closed kinematic loop by considering open loop models extended with contact constraints.
This package provides a convention to describe actuation of such robots and is the base of another package providing example models of parallel robots.

## Installation
Installation instuctions are to be added.

## Run examples

## Contents
* ActuationModel and ActuationData - *class for containing usefull information about the robot actuation (essentially which joints are actuated)*
* Actuation utils - *utility functions to manipulate actuated and free joints configuration (e.g. recreate robot configuration from separated actuated and free joint configuration, extract actuated joints configuration from complete state...)*
* Closures - *Functions to determine closed configurations based on open configuration and fixed serial joints*
* Constraints - *Functions to compute contact constraint violation for 6D and 3D contacts*
* Forward Kinematics
* Inverse Dynamics
* Inverse Kinematics
* Freeze Joints - *Fixes some joints and recreate the Acutation and Constraints models*
* Jacobian - *Computes closed-loop jacobians*
* Mounting - *Computes a mounted condiguration based on the contact constraints (internal and with the environment)
* Projection - *Projects configuration to the closest closed-loop configuration*

## :copyright: Credits

### :writing_hand: Written by

- [Ludovic De Matteis](https://ludovicdematteis.github.io/), LAAS-CNRS :fr:
- Virgile Batto, LAAS-CNRS :fr:

### :construction_worker: With contributions from