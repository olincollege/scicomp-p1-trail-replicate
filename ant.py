import numpy as np


class Ant:
    """
        Represents an ant, and handles ant motion

        Params:
            id: Positive integer representing unique ID for ant
            pos: Tuple of two integers representing grid coordinates of ant
            lattice: Instance of Lattice object which Ant is part of
            fidelity: Float for probability of ant losing trail (from lattice)
            probs: List of floats for turning kernel while exploring (from  lattice)
            dir: Integer for direction of heading of ant
            lost: Boolean that represents if the ant is lost (not following trail)
            dir_mapping: Dictionary that maps directions to the position increments
        """
    def __init__(self, lattice, id, pos):
        """
        Initializes an ant in the lattice
        """
        self.id = id
        self.pos = pos
        self.lattice = lattice
        self.fidelity = self.lattice.fidelity
        self.probs = self.lattice.probs
        self.dir = np.random.choice([45, 135, 225, 315])
        self.lost = True
        self.dir_mapping = {0:(1, 0), 45:(1, 1), 90:(0, 1), 135:(-1, 1), 
                            180:(-1, 0), 225:(-1, -1), 270:(0, -1), 315:(1, -1)}


    def move(self):
        """
        Move an ant to new location based on surrounding phermone values

        Main function of the Ant object. Deposits phermone, kills out of bound
        ant, explores if no trails, implements fidelity, handles trail 
        following and weighted turning.
        """
        # Assume ant is following trail (since explore sets lost to True)
        self.lost = False

        # Deposit at current position
        self.lattice.deposit(self.pos)

        # Kill ant if out of bound
        if self.outside_bounds():
            self.lattice.kill(self)
            return

        # If no trails nearby, explore
        if np.sum(self.sense()) == 0:
            self.pos = self.explore()
            return

        # Fidelity check: if ant loses trail, switch to exploring
        if not self.stay():
            self.pos = self.explore()
            return

        # Is following a trail, check surrounding phermones
        surround = self.sense()

        # If trail directly ahead, move forward
        if surround[0] > 0:
            # Move forward
            self.pos = self.translate(self.dir)
            return

        # If surrounding trails have same phermone concentrations, move as if exploring
        if (surround[1] == surround[4]) and (surround[2] == surround[5]):
            self.pos = self.explore()
            return

        # Weighted turning:

        # Calculate probabilities weighted by phermone from turning kernel
        surround_weighted = surround * np.array([0, *self.probs[1:3]] * 2)
        # Normalize probabilities
        surround_norm = surround_weighted / np.sum(surround_weighted)

        # Pick a direction based on kernel
        turn = np.random.choice(6, p = surround_norm)

        # Turning right
        if turn < 3:
            self.dir = self.rotate(0, turn)
        # Turning left
        else:
            self.dir = self.rotate(1, turn - 3)

        # Move to new position
        self.pos = self.translate(self.dir)
        return


    def stay(self):
        """
        Return boolean depending on set fidelity
        """
        return np.random.rand() < self.fidelity


    def explore(self):
        """
        Provides new location of an exploring ant

        Returns:
            Tuple with two elements containing coordinates of new position
        """
        # Categorize ant as lost
        self.lost = True
        # Choose angle (number of 45 degree turns) with turning kernel
        turn = np.random.choice(5, p = self.probs)
        # Choose turning left or right
        side = np.random.choice(2)
        # Rotate the ant
        self.dir = self.rotate(side, turn)
        # Get next position based on the new direction of heading
        return self.translate(self.dir)
    

    def sense(self):
        """
        Checks the grid points around an ant for phermones

        Returns:
            List of integers containing the phermone values in surrounding
            5 squares (directly ahead square is repeated)
        """
        # Build map of surrounding phermones
        surround = []
        # Left and right
        for side in range(2):
            # 0, 45, or 90 degrees left or right
            for turn in range(3):
                # Pseudo move the ant to the next spot
                next_dir = self.rotate(side, turn)
                (x_next, y_next) = self.translate(next_dir)
                # Append phermone concentration
                surround.append(self.lattice.phermones[x_next][y_next])
        
        # Return array with phermone concentrations around ant
        return np.array(surround)
    

    def translate(self, dir):
        """
        Moves ant with specified direction to new coordinates

        Args:
            dir: Positive integer with heading of the ant in degrees
        
        Returns:
            Tuple of two integers with new coordinates of ant
        """
        # Get current position coordinates
        x = self.pos[0]
        y = self.pos[1]
        
        # Get value increments based on direction
        (x_i, y_i) = self.dir_mapping[dir]
        
        # Return next position
        return (x + x_i, y + y_i)
    

    def rotate(self, side, turn):
        """
        Rotate an ant as specified

        Args:
            side: integer that is 0 for right, 1 for left
            turn: amount in degrees to turn from current direction
        
        Returns:
            Integer with new direction of heading of ant
        """
        dir = self.dir

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
            if dir >= 360:
                dir -= 360
        
        return dir
    
    
    def outside_bounds(self):
        """
        Return if ant is out of bounds of lattice

        Returns:
            Boolean if ant is out of bounds
        """
        # Get x and y coordinates
        x = self.pos[0]
        y = self.pos[1]

        # Return if out of bounds
        return x > 254 or x < 1 or y > 254 or y < 1