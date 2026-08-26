import numpy as np
import matplotlib.pyplot as plt

from models import pendulum as model
from integrators import rk4 as integrator

# Basic simulation of the pendulum

params = {
    "gravity": 9.81,  # gravity m/s^2)
    "length": 1,  # rod length (m)
    "mass": 0.2,  # point mass at end of rod (kg)
    "damping_coeff": 0.0,  # damping coefficient (kg*m^2/s)
}


# some set-up
initial_state = np.array([np.pi / 4, 0.0])

# sweep timesteps to check stability

start_exp = -5
end_exp = -1
num_exp = abs(end_exp - start_exp)

timestep_keys = np.linspace(start_exp,end_exp,num_exp,dtype=int)

timestep_vals = np.logspace(start_exp, end_exp, num=num_exp)

time_trajs = {}
state_trajs = {}

for timestep, timestep_key in zip(timestep_vals,timestep_keys):

    sim_time = 5.0

    n_timesteps = int(sim_time / timestep) + 1
    time_traj = np.arange(n_timesteps) * timestep
    state_traj = np.zeros((2, n_timesteps))
    state_traj[:, 0] = initial_state

    # simulation loop
    for step, t in enumerate(time_traj[:-1]):
        # state_traj[:, step + 1] = state_traj[:, step] + timestep * model.dynamics(
            # t, state_traj[:, step], params
        # )
        state_traj[:, step + 1] = integrator.step(
            state_traj[:, step],
            t,
            model.dynamics,
            timestep,
            params
        )

    time_trajs[str(timestep_key)] = time_traj
    state_trajs[str(timestep_key)] = state_traj


# sanity check the energies: since there is no actuation, and no damping, total energy should stay
# constant. If we turn on the damping coefficient, it should slowly bleed out energy until it comes to
# a stand-still.

# for sweeping timesteps, we want to find the maximum \Delta t for which the total energy is a constant.


total_energies = {}
for timestep_key in timestep_keys:
    kinetic_energy, potential_energy = model.calculate_energy(state_trajs[str(timestep_key)], params)

    total_energy = kinetic_energy + potential_energy

    total_energies[str(timestep_key)] = total_energy


eps = 1e-3
min_samples = 10

def energy_drift(e_arr: np.ndarray):
    return np.max(np.abs(e_arr - e_arr[0])) / np.abs(e_arr[0])

passing = [
    int(key)
    for key, tE in total_energies.items()
    if tE.size >= min_samples and energy_drift(tE) < eps
]

max_dt = max(passing, default=None)

best_timestep = str(max_dt)

print(f"Best DT value: 1e{max_dt}, Relative Drift: {energy_drift(total_energies[best_timestep]):.3e} J")


kinetic_energy, potential_energy = model.calculate_energy(state_trajs[best_timestep], params)

plt.figure()
plt.plot(time_trajs[best_timestep], potential_energy, label="Potential energy")
plt.plot(time_trajs[best_timestep], kinetic_energy, label="Kinetic energy")
plt.plot(time_trajs[best_timestep], potential_energy + kinetic_energy, label="Total energy")
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")
plt.title(f"Pendulum energy for timestep 1e{best_timestep}")
plt.legend()
plt.tight_layout()
plt.show()

# TODO: make a phase portrait plot

theta, theta_dot = state_trajs[best_timestep]

plt.figure()
plt.plot(theta, theta_dot, lw=0.8)
plt.plot(theta[0], theta_dot[0], "o", label="start")
plt.xlabel(r"$\theta$ (rad)")
plt.ylabel(r"$\dot{\theta}$ (rad/s)")
plt.title(rf"Phase portrait, $\Delta t = 10^{{{best_timestep}}}$")
plt.axhline(0, lw=0.5, color="0.7")
plt.legend()
plt.tight_layout()
plt.show()
