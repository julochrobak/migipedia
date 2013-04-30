migipedia
=========

Small example of using Migipedia database on mingle.io to look up a category for specific products. 
It matches every product form the input with all items in the "migipedia" database with a fuzzy string match provided by mingle.io.

The lookup_categories.py script prints out the response on the stdout. The purse is solely to explain the integration 
with mingle.io service.

Usage:

1. get a CSV file with Migros products (provided for the cumulus clients, see more on https://github.com/cstuder/cumulizer/tree/master/_sampledata)
2. run the script:
    
        cat input.csv | python lookup_categories.py


example mingle.io query matching product "ERDBEEREN CH":
  
    [ a.category, a.product, fuzzy(upper(a.product), upper("ERDBEEREN CH")) | 
      a <- migipedia, 
      fuzzy(upper(a.product), upper("ERDBEEREN CH")) > 0.40 && a.lang == "de" ]
      
The query calculates fuzzy match of the "ERDBEEREN CH" string with every german name of the product in the "migipedia" database
and only returns the records which match with at least 0.4 match.

