# PlaFi
PlaFi (**pl**otter **a**nd **fi**tter) is an application that allows to quickly plot and fit some data. Tt has been
designed to be used during data taking sessions, in order to have a quick display of simple data, and to confirm or not 
a certain behaviour.

## Installation
The application can be installed by cloning the repository [plafi](https://github.com/giggi22/plafi) and using pip:
```
git clone https://github.com/giggi22/plafi
pip install --editable plafi
```

## Usage
When installed, PlaFi can be called from command line using `plafi <subcommand>`. A help message will appear by typing
`plafi -h`. Here are the main commands:

### Plot
In order to plot some data, the command 
```
plafi plot <path_to_file>
```
can be used. The file must be of type _.txt_, _.xlsx_ or _.csv_ (with ';' as separator). Every column will be plotted as
function of the first one. <br/> In case of **headings** in the file, follow the next instruction.


In order to select a specific column to plot, the command 
```
plafi plot -v
```
can be used. It will ask the user for the path, the number of rows to skip (can be used to skip the headings), the 
columns to use for the plotting and the axis labels.

#### Example
Here there is an example of the `plot` option:
```
plafi plot <path_to_plafi>/examples/example1.xlsx
```
The output will be:
![](examples/example1_out1.png?raw=true)


