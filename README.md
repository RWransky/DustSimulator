Spatially Explicit Pesticide Model: 
=======================
How Corn Pesticides Impact Foraging Honeybees
-------------------------

#How to Run Locally:
* Clone repo to a local folder
* Navigate to your local copy via your terminal
* Create two subfolders: `landscapes` and `exposures` (this is where csv data is written to)
* Run `python create_landscapes.py` 
  * This script generates fields saved as non-forageable corn points and forageable points
  * `.npy` and `.csv` files are saved to `landscapes` subdirectory where forageable points are in `flowers#_percent%` and non-forageable corn is in `corn#_percent%`
    * `#` is the landscape number, `%` is percent weediness of corn fields
* Run `python send_bees.py` (this script collects iterations of pesticide exposures on bees)
  * 10 groups of 100 bees are sent to 10 different scouted points
  * When each bee is sent they arrive at a point within a zone of constant radius surrounding the original point
  * Each bee then traverses across adjacent patches
  * Each patch adds to each bee's exposure level
  * `.csv` files are saved to `exposures` under the filename of `field_#_bee_exposures_%`
    * `#` is landscape number, `%` is percent weediness of corn fields
* If you wish to visualize any of the results run `python plot_script.py`

#Model Considerations
Below is a list of default constants set in `create_landscapes_spread_pesticides`, `create_landscapes`, and `send_bees` that impact the model:
* FIELD_LENGTH
  * Length of landscape area
  * DEFAULT: 4000 x 4000 m^2
* HIVE_CENTER_X = FIELD_LENGTH/2
* HIVE_CENTER_Y = FIELD_LENGTH/2
* NUM_FIELDS
  * Total number of fields within each landscape
  * DEFAULT: 25
* MARGIN_WIDTH
  * Space between fields where foraging occurs
  * MUST BE AN EVEN NUMBER
  * DEFAULT: 10 m
* FORAGE_RADIUS
  * Radius for the circular zone surrounding each of the 10 scouted foraging sites
  * DEFAULT: 250 m
* NUM_ITERATIONS
  * Number of iterations performed for each foraging group
  * This parameter has a strong influence on run time
  * DEFAULT: 1
