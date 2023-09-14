# Future Steps:
# 1) The lattice can't just be the phermone values, also need to have ant objects literally present on lattice (I think)
# 2) Implementing multiple ant objects using some sort of tracking list?
# 3) Make the ant motion not uniformly random - this should be easy with using random.choice - update NO
# 4) Make a BASIC display using matplotlib - maybe black squares for ants and then other colors for phermones
# 5) Make into a loop
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
        self.dir = np.random.choice([0, 45, 90, 135, 180, 225, 270, 315])
    
    # Move an ant
    def move(self):
        # Deposit at current position
        self.lattice.deposit(self.pos)

        # Ant is alive
        ant_alive = True
        # Get x and y coordinates
        x = self.pos[0]
        y = self.pos[1]

        # Declare new position
        (x_new, y_new) = (x, y)

        # # If on a trail
        # if self.lattice.phermones[x][y] > 0:
        # Check if current direction is on trail
        (x_front, y_front) = translate(self.dir, x, y)

        if check_bounds(x_front, y_front):
            self.lattice.kill(self)
            return

        if self.lattice.phermones[x_front][y_front] > 0:
            (x_new, y_new) = (x_front, y_front)
        
        # # Using Vedaant's intepretation of forking algorithm
        # # Ignore all forks except immediate left and right
        # # (Carrie's interpretation was including non-immediate forks too)
        # Check right and left forks
        else:
            # Check right fork
            dir_right = rotate(self.dir, 0, 1)
            (x_right, y_right) = translate(dir_right, x, y)

            # Check left fork
            dir_left = rotate(self.dir, 0, 1)
            (x_left, y_left) = translate(dir_left, x, y)

            # Kill ant if out of bounds
            if check_bounds(x_right, y_right):
                self.lattice.kill(self)
                return

            if check_bounds(x_left, y_left):
                self.lattice.kill(self)
                return
                
            # If forks are of equal concentration (or there are no forks)
            if self.lattice.phermones[x_right][y_right] \
                == self.lattice.phermones[x_left][y_left]:
                # Choose angle (number of 45 degree turns) with turning kernel
                turn = np.random.choice(5, p = [0.581, 0.36, 0.047, 0.008, 0.004])
                # Choose turning left or right
                side = np.random.choice(2)
                # Rotate the ant
                self.dir = rotate(self.dir, side, turn)
                # Get next position based on the new direction of heading
                (x_new, y_new) = translate(self.dir, x, y)
            
            # If right is stronger than left
            elif self.lattice.phermones[x_right][y_right] \
                > self.lattice.phermones[x_left][y_left]:
                # Choose right fork
                (x_new, y_new) = (x_right, y_right)

            else:
                # Choose left fork
                (x_new, y_new) = (x_left, y_left)
       
        # Kill ant if out of bounds
        if check_bounds(x_new, y_new):
            self.lattice.kill(self)
            return

        # If not, move to new spot
        self.pos = (x_new, y_new)

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
        my_ant = Ant(self, id, (127, 127))
        self.active_ants.append(my_ant)

    # Kill a specified ant
    def kill(self, ant):
        self.active_ants.remove(ant)
        
    # Display lattice
    def show(self):
        ax.clear()
        ax.imshow(self.phermones, cmap = "gray_r")  # Use 'gray' colormap for grayscale images
        ax.axis('off')  # Turn off axis labels and ticks
        plt.pause(0.001)

def translate(dir, x, y):
    # Change position depending on turning angle
    if dir == 0:
        x += 1
    elif dir == 45:
        x += 1
        y += 1
    elif dir == 90:
        y += 1
    elif dir == 135:
        x -= 1
        y += 1
    elif dir == 180:
        x -= 1
    elif dir == 225:
        x -= 1
        y -= 1
    elif dir == 270:
        y -= 1
    else:
        x += 1
        y -= 1
    
    return (x, y)


def rotate(dir, side, turn):
    # Turning right
    if side == 0:
        dir -= 45*turn
        # Keep within 0 to 360
        if dir < 0:
            dir += 360
    # Turning left
    else:
        dir += 45*turn
        # Keep within 0 to 360
        if dir > 360:
            dir -= 360
    
    return dir

def check_bounds(x_new, y_new):
    # Kill ant if out of bounds
    return x_new > 255 or x_new < 0 or y_new > 255 or y_new < 0


# Create an empty lattice
my_lattice = Lattice()

# Display lattice
fig, ax = plt.subplots()
my_lattice.show()

# Create an ant
ant_0 = Ant(my_lattice, 0, (123, 127))

# Simulation master loop
for i in range(4000):
    my_lattice.add_ant(i)

    for ant in my_lattice.active_ants:
        ant.move()

    # print(len(my_lattice.active_ants))
    # Evaporate phermones
    my_lattice.evap()
    # Display lattice
    my_lattice.show()