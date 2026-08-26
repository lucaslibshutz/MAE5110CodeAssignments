import numpy as np

def dynamics(t, state, params):
    gravity = params["gravity"]
    mass = params["mass"]
    radius = params["radius"]
    coeff_rest = params["coeff_of_restitution"]

    height = state[0]
    velocity = state[1]


    #TODO: add if statement if height is at ground, and velocity < 0, add bounce up at that instant
    acceleration = -gravity

    state_derivative = np.array([velocity, acceleration])

    raise NotImplementedError


def generate_params():
    params = {
        "gravity": 9.81,  # gravity m/s^2)
        "radius": 1,  # ball radius (m)
        "mass": 1,  # point mass at end of rod (kg)
        "coeff_of_restitution": 0.1,  # damping coefficient (kg*m^2/s)
    }
    return params


def calculate_energy(state, params):
    """Compute energies for a state ``(2,)`` or trajectory ``(2, N)``."""
    gravity = params["gravity"]
    mass = params["mass"]

    height = state[0]
    velocity = state[1]

    kinetic_energy = 0.5 * mass * velocity**2
    potential_energy = mass * gravity * height

    return kinetic_energy, potential_energy
