from matplotlib import pyplot as plt
from models import ball as model
import numpy as np
from integrators import rk4 as integrator 

"""
What we expect to see:

We want to see that the ball bounces and hits the ground, and loses
some of its energy on each bounce. The total energy should decrease on each bounce,
and only at the bounces, as there is no other energy loss mechanism in the model. 
"""

params = model.generate_params()

initial_state = np.array([0.5, 0.0]) # start at 0.5 m above ground, no velocity

sim_time = 5.0 # seconds
timestep = 1e-5

n_timesteps = int(sim_time / timestep) + 1
time_traj = np.arange(n_timesteps) * timestep
state_traj = np.zeros((2, n_timesteps)) # 2 by default for now, should make this generic
state_traj[:,0] = initial_state

# simulation loop as before
for step, t in enumerate(time_traj[:-1]):
    state_traj[:, step + 1] = integrator.step(
        state_traj[:, step],
        t,
        model.dynamics,
        timestep,
        params
    )

kinetic_energy, potential_energy = model.calculate_energy(state_traj, params)

plt.figure()
plt.plot(time_traj, potential_energy, label="Potential Energy")
plt.plot(time_traj, kinetic_energy, label="Kinetic Energy")
plt.plot(time_traj, kinetic_energy + potential_energy, label="Total Energy")
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(time_traj, state_traj[0, :], label="Position")
plt.plot(time_traj, state_traj[1, :], label="Velocity")
plt.xlabel("Time (s)")
plt.legend()
plt.tight_layout()
plt.show()
