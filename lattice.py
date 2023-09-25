import numpy as np
import matplotlib.pyplot as plt
from ant import Ant


class Lattice:
    """
    Represents the lattice on which ants move

    Params:
        phermones: Two dimensional NumPy array of positive integers containing
            phermone values. 256 by 256 points
        active_ants: List of active ants
        dep: Integer representing amount of phermone deposited per time step per ant
        sat: Integer representing max phermone value allowed 
            i.e. concentration at which antennae saturate
        fidelity: Float for probability of ant losing a trail
        probs: List of floats for turning kernel while exploring
    """
    def __init__(self, deposition_rate, saturation, fidelity, probs):
        """
        Initialize a lattice, and plot first grid
        """
        # Initialize Phermone deposition tracker
        self.phermones = np.zeros((256, 256))
        # List of active ants
        self.active_ants = []
        # Deposition rate
        self.dep = deposition_rate
        # Concentration at which antennae saturate
        self.sat = saturation
        # Probability of ant losing a trail
        self.fidelity = fidelity
        # Turning kernel while exploring
        self.probs = probs

        # Display lattice
        _, self.ax = plt.subplots()
        self.show()
    

    def deposit(self, pos):
        """
        Deposit phermone at specified location
        """
        x = pos[0]
        y = pos[1]
        # Ensure that phermone doesn't exceed saturation
        self.phermones[x][y] = min(self.phermones[x][y] + self.dep, self.sat)

    
    def evap(self):
        """
        Phermone evaporation
        """
        # Ensure that phermones levels don't fall below 0
        self.phermones[self.phermones > 0] -= 1

    
    def add_ant(self, id):
        """
        Add a new ant with specified ID to the lattice

        Args:
            id: integer distinguishing a unique ant
        """
        # Start in center
        my_ant = Ant(self, id, (127, 127))
        # Add to list of active ants
        self.active_ants.append(my_ant)

    
    def kill(self, ant):
        """
        Kill a specified ant

        Args:
            Instance of Ant object to be killed
        """
        # Remove from list of active ants
        self.active_ants.remove(ant)
        
    
    def show(self):
        """
        Plot and display updated lattice
        """
        # Clear previous plot
        self.ax.clear()
        # Show phermones as a colormap
        self.ax.imshow(self.phermones, cmap="gray_r")
        # Turn off axis labels and ticks
        self.ax.axis('off')  
        # Pause briefly
        plt.pause(0.001)


    def calculate_strength(self):
        """
        Calculate the ratio of follower to lost ants

        Returns:
            Positive float of ratio of follower to lost ants
        """
        # Calculate number of lost ants
        n_lost = len([ant for ant in self.active_ants if ant.lost])
        # Subtract from all active ants to find following ants
        n_following = len(self.active_ants) - n_lost

        # Prevent division by zero error by having at least one lost ant
        if n_lost == 0:
            return n_following
        
        # Return ration of following to lost (measure of trail strength)
        return n_following / n_lost