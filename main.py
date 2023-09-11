# Future Steps:
# 1) Add a "phermone leaving" function
# 2) The lattice can't just be the phermone values, also need to have ant objects literally present on lattice (I think)
# 2a) Implementing multiple ant objects using some sort of tracking list?
# 3) Make the ant motion not uniformly random - this should be easy with using random.choice
# 4) Make a BASIC display using matplotlib - maybe black squares for ants and then other colors for phermones
# 5) Make into a loop
# 6) If time, encode things like phermone evaporation (link to intensity of colors in lattice)
# 7) Review code with Carrie what's going on
# 8) Next step is probably ant trail following and scaling up model to working by midterm review (maybe?)
# 9) If more time, maybe see if you can "display" ants? Would definitely need pygame for this

# Import libraries
import numpy as np
import matplotlib.pyplot as plt

# Ant
class Ant:
    # Initialize an ant, assigning it the lattice it is on, the ID, and its starting position
    def __init__(self, lattice, id, pos):
        self.id = id
        self.pos = pos
        self.lattice = lattice
        self.dir = 0
    
    # Move an ant
    def move(self):
        # Deposit at current position
        self.lattice.deposit(self.pos)

        # Get x and y coordinates
        x = self.pos[0]
        y = self.pos[1]

        # Choose angle (number of 45 degree turns) with turning kernel
        turn = np.random.choice(5, p = [0.581, 0.36, 0.047, 0.008, 0.004])
        # Choose turning left or right
        side = np.random.choice(2)

        # Turning right
        if side == 0:
            self.dir -= 45*turn
            # Keep within 0 to 360
            if self.dir < 0:
                self.dir += 360
        # Turning left
        else:
            self.dir += 45*turn
            # Keep within 0 to 360
            if self.dir > 360:
                self.dir -= 360

        # Change position depending on turning angle
        if self.dir == 0:
            x += 1
        elif self.dir == 45:
            x += 1
            y += 1
        elif self.dir == 90:
            y += 1
        elif self.dir == 135:
            x -= 1
            y += 1
        elif self.dir == 180:
            x -= 1
        elif self.dir == 225:
            x -= 1
            y -= 1
        elif self.dir == 270:
            y -= 1
        else:
            x += 1
            y -= 1
        
        # Kill ant if out of bounds
        if x > 255 or x < 0 or y > 255 or y < 0:
            self.lattice.kill(self)
        # If not, move to new spot
        else:
            self.pos = (x, y)

# Lattice on which Ants move
class Lattice:
    # Initialize Phermone deposition tracker
    def __init__(self):
        self.phermones = np.zeros((256, 256))
        self.active_ants = []
    
    # Deposit phermone at specified location
    def deposit(self, pos):
        x = pos[0]
        y = pos[1]
        self.phermones[x][y] = 8

    # Phermone evaporation
    def evap(self):
        self.phermones[self.phermones > 0] -= 1

    # Add a new ant with specified ID to the lattice
    def add_ant(self, id):
        my_ant = Ant(self, id, (0, 127))
        self.active_ants.append(my_ant)

    # Kill a specified ant
    def kill(self, ant):
        self.active_ants.remove(ant)
        
    # Display lattice
    def show(self):
        ax.clear()
        ax.imshow(self.phermones, cmap = "gray_r")  # Use 'gray' colormap for grayscale images
        ax.axis('off')  # Turn off axis labels and ticks
        plt.pause(0.01)
        # plt.show() 

# Create an empty lattice
my_lattice = Lattice()

# Display lattice
fig, ax = plt.subplots()
my_lattice.show()

# Create an ant
ant_0 = Ant(my_lattice, 0, (123, 127))

# Simulation master loop
for i in range(500):
    if i % 50 == 0:
        my_lattice.add_ant(i)

    for ant in my_lattice.active_ants:
        ant.move()

    # Evaporate phermones
    my_lattice.evap()
    # Display lattice
    my_lattice.show()