def step(
    state,
    time,
    dynamics,
    timestep,
    params
):
    k1 = dynamics(time, state, params)
    k2 = dynamics(time + timestep/2, state + timestep/2 * k1, params)
    k3 = dynamics(time + timestep/2, state + timestep/2 * k2, params)
    k4 = dynamics(time + timestep, state + timestep * k3, params)
    return state + (timestep/6) * (k1 + 2*k2 + 2*k3 + k4)
