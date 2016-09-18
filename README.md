Spatially Explicit Pesticide Model: 
=======================
How Corn Pesticides Impact Foraging Honeybees
-------------------------

#How to Run Locally:
* Clone repo to a local folder
* Navigate to your local copy via your terminal
* Create two subfolders: `landscapes` and `exposures` (this is where csv data is written to)
* Run `python create_landscapes_spread_pesticides.py` (this generates fields and exposure drift)
  * This script generates forageable landscapes based on 0, 12.5, 25, 50, 75, and 100% weedy non-corn fields
  * `.npy` and `.csv` files are saved to `landscapes` subdirectory where forageable points are in `field#landscape*` and drift visualization is in `field#exposures*`
    * `#` is the landscape number; `*` is the percent weediness
* Run `python send_bees.py` (this script collects iterations of pesticide exposures on bees)
  * 10 groups of 100 bees are sent to 10 different scouted points
  * When each bee is sent they arrive at a point within a zone of constant radius surrounding the original point
  * Each bee then traverses across adjacent patches
  * Each patch adds to each bee's exposure level
  * `.csv` files are saved to `exposures` under the filename of `field_#_bee_exposures_*`
    * `#` is landscape number; `*` is weediness percentage
* If you wish to visualize any of the results run `python plot_script.py`

#Model Considerations
Below is a list of default constants set in `create_landscapes_spread_pesticides` and `send_bees` that impact the model:
* FIELD_LENGTH
  * Length of landscape area
  * DEFAULT: 4000 x 4000 m^2
* HIVE_CENTER_X = FIELD_LENGTH/2
* HIVE_CENTER_Y = FIELD_LENGTH/2
* NUM_FIELDS
  * Total number of fields within each landscape
  * DEFAULT: 15
* MARGIN_WIDTH
  * Space between fields where foraging occurs
  * MUST BE AN EVEN NUMBER
  * DEFAULT: 100 m
* FORAGE_RADIUS
  * Radius for the circular zone surrounding each of the 10 scouted foraging sites
  * DEFAULT: 25 m
* NUM_ITERATIONS
  * Number of iterations performed for each foraging group
  * This parameter has a strong influence on run time
  * DEFAULT: 1
