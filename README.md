# An interactive scatterplot tool for genomic analysis

## Prepare input file

The input file is a TSV file (i.e., tab-delimited file) with 5+ columns. The first three columns are chromosome name, start, and end position of a region. The rest columns represent average signals of different data. For example, the first 7 rows of an sample data looks at this:

```
chrom   start   stop    H1_4xAP3_DAMID_25kb_hg38_combined       H1_4xAP3_DAMID_25kb_hg38_rep1
chr5    200000  300000  0.17783526703715324     0.12051905319094658
chr5    300000  400000  -0.11982538551092148    -0.004135941155254841
chr5    400000  500000  -0.03748955391347408    -0.271945983171463
chr5    500000  600000  0.4752919003367424      -0.15632009133696556
chr5    600000  700000  -0.06437647342681885    -0.6367996484041214
chr5    700000  800000  0.270381648093462       -0.15118619240820408
```

Notably, the first row must be the header, showing the name of each column.

To create the input file, you can either write a custom script or use some public tools. For example, the deepTools provides a convenient program called multiBigwigSummary that can create the input file from some bigWig files. Please read their [https://deeptools.readthedocs.io/en/develop/content/tools/multiBigwigSummary.html](documentation) for details.

## Use the tool
You can access the tool at [http://genome-dev.compbio.cs.cmu.edu:8050](http://genome-dev.compbio.cs.cmu.edu:8050). Several pre-computed input files are available to use. You can use the dropdown menu to select annotation file you want to use. You can also upload your input file to explore customized data. To host the tool in your server, please clone this repo and modify the host name at the end of the app.py file. The tool is built using [dash](https://dash.plotly.com/installation) and [dash-extensions](https://pypi.org/project/dash-extensions/).

After you install the dash and dash_extensions, start the server by typing 'python app.py'. The server should be up at <hostname>:8050.
```
  pip install dash==1.17.0
  pip install dash-extensions
  python app.py
```
 
The tool currently only supports python3 due to the dependency of dash-extensions. 

## About
This tool is created by Yang Zhang. 
