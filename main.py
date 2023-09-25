# Import lattice
from lattice import Lattice

# Parameters
RUNTIME = 1500
FIDELITY = 0.98
KERNEL = [0.581, 0.36, 0.047, 0.008, 0.004]
DEPOSITION_RATE = 6
SATURATION = 6

# Create an empty lattice
my_lattice = Lattice(DEPOSITION_RATE, SATURATION, FIDELITY, KERNEL)

# Simulation master loop
for i in range(RUNTIME):
    # Print tracker
    if i % 100 == 0:
        print(round(i/RUNTIME * 100, 1), "percent completed")

    # Add ant at every iteration
    my_lattice.add_ant(i)

    # Move all active ants
    for ant in my_lattice.active_ants:
        ant.move()

    # Evaporate phermones
    my_lattice.evap()
    # Display lattice
    my_lattice.show()

# Print trail strength
print("Trail strength (F/L)", round(my_lattice.calculate_strength(), 2))