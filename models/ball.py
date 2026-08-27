import numpy as np

def dynamics(t, state, params):
    gravity = params["gravity"]
    mass = params["mass"]
    ground_spring = params["ground_spring"]
    ground_damping = params["ground_damping"]

    height = state[0]
    velocity = state[1]


    #TODO: add if statement if height is at ground, and velocity < 0, add bounce up at that instant
    if height < 0:
        acceleration = -gravity - (ground_spring/mass * height) - (ground_damping/mass * velocity)
    else:
        acceleration = -gravity

    state_derivative = np.array([velocity, acceleration])
    return state_derivative



def generate_params():
    params = {
        "gravity": 9.81,  # gravity m/s^2)
        "mass": 1,  # point mass at end of rod (kg)
        "ground_spring": 1000,
        "ground_damping": 4.5,
    }
    return params


def calculate_energy(state, params):
    """Compute energies for a state ``(2,)`` or trajectory ``(2, N)``."""
    gravity = params["gravity"]
    mass = params["mass"]
    ground_spring = params["ground_spring"]

    height = state[0]
    velocity = state[1]

    kinetic_energy = 0.5 * mass * velocity**2
    gravitational_energy = mass * gravity * height
    # spring only acts when below 0, so this is why we use `np.minimum()`` here
    spring_energy = 0.5 * ground_spring * np.minimum(height, 0.0) ** 2

    return kinetic_energy, gravitational_energy + spring_energy
