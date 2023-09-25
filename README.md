# Project 1: Ants!

### Author: Vedaant Kuchhal

## Aim
The aim of this project is to simulate ant trail patterns using agent-based modelling.

## Background
 This is scientifically relevant since agent-based simulations have proved to be quite useful in explaining complex behaviors in social organisms that have otherwise limited capacity to self-organize.

 This project is based off the model presented by Watmough and Edelstein-Keshet in *Modelling the Formation of Trail Networks by Foraging Ants* [[1]](#1). As might be evident from this project's name, the success of this implementation will be benchmarked by its similarity to the trail diagrams and variable relationships noted in the aforementioned paper.

 ## Code Overview
 ### Pre-requisites
 This project is written entirely in [Python](https://www.python.org/), and two libraries outside of base Python 2.0 or higher are required to run the code in this repository. These are:

  - `numpy`
  - `matplotlib`

  Both can be installed appropriately (depending on operating system, other configurations) if not already present. See directions [here](https://docs.python.org/3/installing/index.html) if needed.

  ### Files
  There are three main code files in this repository:

  1. `main.py`: Runtime loop and parameters
  2. `lattice.py`: Lattice class to manage the overall space in which the ants move
  3. `ant.py`: Ant class to represent and manage behaviors of an ant

  ### Running
  To run the code, run `main.py` in your appropriate Python environment (e.g.- entering `python main.py` in a shell).

  In a nutshell, the `main.py` file imports `lattice.py` and creates an instance of the Lattice class. 
  
  `lattice.py` itself imports `ant.py` and creates many instances of Ant classes. These 'ants' then populate the 'lattice'. Each ant follows a very simple set of rules, but when thousands of these ants interact over time through depositing phermones as they move, we see complex trails being formed.

  ## Results
  My implementation closely matched the results that the authors of the paper reached!

Figure 3(b) from paper    |  My figure (same parameters)
:-------------------------:|:-------------------------:
  ![](.img/paper_trails.png) | ![](.img/my_trails.png)


  As you can see, the implementation and my figure had a similar shape. My figure looks messier with more light trails (and I'll include appropriate further discussion on that in the [Discussion](#discussion) section), but that could partly be because of difference in visual scaling. Additionally, the resultant mean trail strength (F/L ratio) for this figure from the paper was 14, and, with the same parameters, I got an average value of 15.6!

  Importantly, all the trends from modifying parameters described in the paper were replicated by my implementation:
  
  1)  **Decreasing fidelity decreased the strength of trails** - When fidelity was reduced gradually from 0.9 to 0.6, the mean strength of trails, measured by ratio of following to lost ants, reduced dramatically from around 4.2 to 0.9.

  2) **Reducing deposition rate increased rapid formation of strong trails** - When the rate was decreased form 8 to 4, dominant trails formed more quickly and stayed as they were, whereas at a higher rate no trail was able to clearly dominate. The ratio of followers to lost ants decreased as expected since there were much fewer weak trails.

  3) **Narrowing the turning kernel decreased the tortuosity of trails** - When the turning kernel was changed to bias forward movement, the trails were significantly more straight - going from a complex web to an "X" shape with few bends.

  4) **Increasing the concentration of antennae saturating decreased number of strong trails** - This is tricky since I don't think I implemented this parameter as specified in the paper. I discuss this further in the [next section](#differences-in-method), but essentially I interpreted it as the maximum phermone concentration allowed on the lattice. When this was increased, there was a more complex web of weak trails as opposed fewer, stronger trails.

  I did not implement the second version of the Forking Algorithm mentioned in the paper, both due to time constraints and low relevance ascribed by the authors to its results.

  ## Discussion
  ### Differences (in method)
  To begin the discussion, I want to highlight the key differences between my implementation and that of the paper:

  1) Determining the saturation concentration proved to be very puzzling. The paper didn't mention its value for the figures I benchmarked for, and it is very likely that I didn't use it in the same way that the authors used it in their model. They spoke about ants not being able to distinguish between separated trails beyond a saturated phermone level, whereas I used it as the ceiling value for deposited phermone level. The one place they did mention it (Figure 6 in the paper), my results didn't match the figure at all. Either way, not knowing the value for this added uncertainty to my implementation being a good replication.

  2) The forking algorithm (and adjacent implenentation of fidelity) too was confusion and open to interpretation. My interpretation was using fidelity as a weighted "coin flip". In other words:

        1) If no trail near, keep exploring
        2) If trail near, choose whether to follow depending on a variable that is weighted by the probability value ascribed to fidelity. 
        3) If following trail, the forking algorithm is implemented in 4. and 5.
        4) Continue to any trail **directly** ahead, *no matter how weak*
        5) If nothing ahead, check the four squares to left and right and turn appropriately, weighted by angle and phermone concentration.

  3) The final difference likely had to do with display. The figures in the paper appeared to display ants on top of trails. Zooming into the graphs it looked like while the phermones were displayed on a greyscale, the mass of ants on an established trail defined it further. My implementation was only limited to displaying phermone concentrations where the maximum concentration was the darkest, which explained differences such as, for example, not being able to see exploring (lost) ants in my implementation which had weak trails.

  ### Differences (in results)
  Perhaps due to any of the above factors and more, my implementation's results were different in two major ways:
  
  1) All my figures (except for those with narrow turning kernels) had lots of dark clustering around the center, whereas almost all of the paper's figures, regardless of parameter, had a pretty clear "X" shape at the center.
  2) I couldn't model the single trail behavior that a few figures in the paper showed. This was the single, long, winding trail that occurred during low deposition rates. While I had stronger trails overall for lower deposition, there was never a single, winding one.

  ### Next Steps
  I feel like I came reasonably close enough to the figures I was planning to use as a benchmark. Instead of trying to perfect the match, I think more appropriate next steps would involve further research into ant behavior and trails. This could inform more appropriate implementations of things like the forking algorithm, deposition and evaporation, saturation, and much more. To gain more accuracy to real-world benchmarks, it would probably make more sense to display the ants on a lattice as well instead of just the otherwise invisible phermones. And lastly, I think it could be interesting to research into modelling more complex behavior, such as possibilities for how ants communicate and form trails when they find a food source.

  ## Conclusion
  On the whole, I could successfully replicate trail forming behavior demonstrated by Watmough and Edelstein-Keshet in their paper, with the privilege of significantly more computing power and higher-level language. While there are some differences in approach and results, the current code provides a good starting point for further, more nuanced modelling.


## References
<a id="1">[1]</a> Watmough, J., & Edelstein-Keshet, L. (1995). Modelling the formation of trail networks by foraging ants. Journal of Theoretical Biology, 176(3), 357-371.
___
If you made it all the way to the end, thank you for reading!!