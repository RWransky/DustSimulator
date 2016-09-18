Spatially Explicit Pesticide Model: 
=======================
How Corn Pesticides Impact Foraging Honeybees
-------------------------

How to Run Locally:
* Clone repo to a local folder
* Create two subfolders: `landscapes` and `exposures` (this is where csv data is written to)
* Run `python create_landscapes_spread_pesticides.py` (this generates fields and exposure drift)
  * This script generates forageable landscapes based on 0, 12.5, 25, 50, 75, and 100% weedy non-corn fields
  * `.npy` and `.csv` files are saved to `landscapes` subdirectory where forageable points are in `field#landscape*` and drift visualization is in `field#exposures*`
    * `#` is the landscape number; `*` is the percent weediness
* Run `python send_bees.py` (this script collects iterations of pesticide exposures on bees)
* If you wish to visualize any of the results run `python plot_script.py`

