# Code to help you upload tree data to [fruitmap.org](https://www.fruitmap.org/)

[Fruitmap.org](https://www.fruitmap.org/) is a beautiful project but its [tree-mapping interface](https://www.fruitmap.org/fruit/pridat) is a bit broken an tedious to use.

It may also be the case that, like me, you mark the trees you find (+ various useful notes on them) in a maps app such as [Mapy.cz](https://en.mapy.cz). For instance, you might have a map point named `pear (very juicy, ripened around August 10th, '22)` along with some geo coordinates. And you might have tens or hundreds of such records!

The question is: How do you upload your data to fruitmap.org easily, whether you store it in Mapy.cz or elsewhere. This repository aims to help with that.

## How to use this repository

The 2 main steps are:
1. Converting your data into a unified format which uses the exact same forms of fruit tree names that fruitmap.org uses.
1. Entering the converted data into fruitmap.org.

### Converting data into a fruitmap.org-friendly format

Currently, this step is automated only for those who have trees stored in Mapy.cz under names/descriptions in Slovak. In general, though, the aim is merely to end up with a JSON file of this form:
```json
[
	{
		"name": "Dula", // fruit tree name exactly as it appears on fruitmap.org 
		"lat": 48.324143,
		"lon": 17.481637
	},
	...
]
```
Mapy.cz users can follow these steps:
1. Make sure you:
	- have this repository downloaded on your PC,
	- are able to run Python scripts on your PC,
	- have [`pip` installed](https://pip.pypa.io/en/stable/installation/),
	- have installed the pip packages listed in `requirements.txt` (e.g. by running `pip install -r requirements.txt`).
1. Assuming all of your trees are stored in Mapy.cz as points in a folder of yours, on a desktop, navigate to that folder and export the contents as GPX -- click the 3 dots above your folder's name and choose `Export` (no need to change any of the export options).
1. Place the downloaded file into the downloaded repository.
1. In a console/terminal/command line, navigate to the downloaded repository, e.g. with a command like `cd ~/Downloads/fruitmap-scripts` on MacOS/Linux.
1. Run the script that converts your downloaded GPX data into a fruitmap.org-friendly JSON format (replace `export.gpx` with your GPX file's name):
	```shell
	python gpx_wpt_to_json.py --input_file=export.gpx --output_file=data.json
	```
	_Note that the script tries to match the names of your points from Mapy.cz to the exact Slovak tree names used by fruitmap.org. If your Mapy.cz data doesn't use Slovak, the conversion process is likely to be unusable for you. (Though, adding support for English isn't too difficult!) You should still be able to use the 2nd step, though (entering data on fruitmap.org)._
1. Inspect the output of the previous command to see if the program matched your Mapy.cz point names to the correct fruitmap.org tree names. The program also excludes trees not currently supported by fruitmap.org, but it might not always work as expected and deserves a manual inspection. If something about the output looks incorrect, try to fix this by rewriting stuff in your exported GPX data and then running the above command again.
1. That's it, you should now have a one-line `data.json` file that looks something like the JSON example below.

### Bulk-entering data on fruitmap.org

Given that you've created a JSON file like in the above example (doesn't matter how you created it!), you should be ready to take that file and upload its contents on fruitmap.org in a few clicks.

1. Copy all your JSON data and paste it in the dedicated place in `tree_uploader.js`. For this, it helps to have the JSON data condensed into one line like this (the output of `gpx_wpt_to_json.py` should already be in such format):
	```json
	[{"name": "Dula", "lat": 48.324143, "lon": 17.481637}, ...]
	```
1. Go to [fruitmap.org](https://www.fruitmap.org/), sign in and go to the tree-mapping interface at [fruitmap.org/fruit/pridat](https://www.fruitmap.org/fruit/pridat).
1. Make sure you have Slovak as the selected language (this is important for the code to work!).
1. Select the `Zaznačiť pomocou mapy` (`Mark on the map`) option.
1. Open the developer panel in your browser (usually by pressing F12) and navigate to the Console tab.
1. Paste the entire contents of `tree_uploader.js` (including your data you had included in the file previously) in the console.
1. Hit Enter. This should run the pasted code. Ideally, no error messages appear in the console, only some informative messages from the pasted code.
	_Note that no markers will be shown on the map but your tree data should now be silently transferred to the page with the map._ **Do not add any trees manually while also adding some with the code. Save your manually added trees, then refresh and add trees with the code. Similarly, don't paste/run the code multiple times. If you need to do it, first, refresh the page.**
1. Hit `Uložiť` (`Save`) to actually save all the transferred data. To check that the data has indeed been uploaded successfully, head over to the overview of your trees at [fruitmap.org/moj-ucet](https://www.fruitmap.org/moj-ucet) and check that the new trees are there. If they're not, either try to figure it out yourself or contact me :-)