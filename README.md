# Association Rules Problem

I won't restate the problem here, assuming you don't want other candidates searching.

To run, it's as simple as navigating to the directory with the script and running:

`python gen_assoc_rules.py`

The output will go to out/out.
It has been tested using Python 2.7 and 3.6

## Additional options
If you want, you can specify some additional options:
-s, --sigma: give it a different sigma [default = 4]
-d, --datafile: supply a different data file [default = data/retail_25k.dat]
-o, --outfile: supply a different output file [default = out/out]
