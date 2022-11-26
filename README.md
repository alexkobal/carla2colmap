# carla2colmap
## Result generation
To generate results use the [result_generation.py](https://github.com/alexkobal/carla2colmap/blob/master/result_generation.py) script.

Change the output folder:
```python
gen_path = '/home/your_project_path' # TODO: change to a new project location (root directory)
```
Add/remove input folder paths in the following line:
```python
input_paths = [ # TODO: add correct input paths
...
]
```
Change the folder where the images are stored within the export folder:
```python
os.environ['IN_IMG_FOLDER'] = 'masked_rgb' # TODO: change if needed
```
Then run the script. After the script is done, reconstruction results should be available in the gen_path you specified.
Note that some additional python packages might be required.
