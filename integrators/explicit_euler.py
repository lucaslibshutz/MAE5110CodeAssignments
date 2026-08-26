import numpy as np

# Define an explicit euler integrator that takes dynamics in and outputs the next step

def step(
    state,
    time,
    dynamics,
    timestep,
    params
):
    return state + timestep * dynamics(time, state, params)
