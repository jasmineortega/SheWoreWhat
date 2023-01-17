===========
SheWoreWhat
===========

Sustainable fashion dashboard displaying personal wardrobe analytics to better inform future closet purchases in terms of cost-per-wear, color, and seasonal trends. Built with Python, Dash, and Altair. Hosted on Heroku. 

The Process
-----------
1. Log all items in closet (as a closet minimalis, this was not as tedious as you'd think)
2. Collect daily outfit data via Google Form (Jan 01 - Dec 31, 2023)

* Free software: MIT license

The Dashboard:
-------------
The dashboard itself is composed of four sections (*for now...*)
1. Wardrobe Analysis
  - Here, I took stock of the items that exist in my closet. What colors dominate my closet? How many of my items were purchased secondhand, new?
2. Most Worn Items of 2023
  - This is the interesting stuff -- which specific items in my closet were worn the most? A GitHub contribution-like heatmap in this section allows for the visualization of the top 10 most worn items over the calender year.
  - As 2023 is still ongoing, this section is updated weekly. 
3. Seasonal Trends
  - As the weather changes, so will the items that dominate the season.This section will most likely be completed post-humously per season. It's only January 17, 2023 at the time I'm writing this. Only 62 days left of winter!!
4. Cost-Per-Wear
  - Here, I calculated the price-per-wear for each item in my clost (where price is known). Which item was the most cost-efficient? Were the pricy items in my closet worth the money? This is a useful metric I can refer to when thinking about adding a new piece to my wardrobe. 
  - *Note:* Majority of items in my closet were purchased prior to 2023. Thus, cost-per-wear here is calculated only for the year 2023 for ease of comparasion. Most of the prices I've listed for items were verified by online reciepts or credit card statements. 

* TODO

Credits
-------
* Free software: MIT license
This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
