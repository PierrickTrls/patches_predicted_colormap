# patches_predicted_colormap

# Description

Extraction of .png colormap based on classifier predictions.

# Usage

Export your patches positions and predictions associated with export_probability_slide.py

command : <br/><pre><code>python export_probability_slide.py --picklefolder path/to/your/pickle/directory </code></pre>

NB : please ensure your pickle directory contains 1 pickle file for each slide, and each pickle file is built as follows :

{ <br/>
IdPatch1 : {'x' : x0 coordinate , 'y' : y0 coordinate , 'feature' : float between 0 and 1 }<br/>
IdPatch2 : {'x' : x0 coordinate , 'y' : y0 coordinate , 'feature' : float between 0 and 1 }<br/>
...<br/>
IdPatchN : {'x' : x0 coordinate , 'y' : y0 coordinate , 'feature' : float between 0 and 1 }<br/> 
}

Create color map using : <br/>

command : <br/><pre><code>python produce_probability_slide.py --slidefolder path/to/your/slide/folder --outputfolder path/to/some/output/folder --jsonfolder path/to/json/previously/extracted --delta some_reduction_factor(optionnal) </code></pre>
