# Anonymize the whole slide image

## The code does run on python version 2.6 and 2.7
----------------------------------------------------------------

###  1. Setting up Anaconda Environment
----------------------------------------------------------------

Commands:<br>
* a. conda create --name py2 python=2.7 <br>
* b. activate py2<br>
* c. conda install nb_conda<br>

For more information refer [Anaconda page of managing environments](https://docs.anaconda.com/anaconda/user-guide/tasks/switch-environment/).<br>

If the environment was activated successfully, you should see (py2- name used here) at the beggining of the command prompt. This will set the kernel as your default kernel when running the code.<br>

----------------------------------------------------------------

###  2. Installing Openslide library and also Openslide binaries files for Windows<br>
----------------------------------------------------------------

OpenSlide is C libraries; as a result, they have to be installed separately from the conda environment, which contains all of the python dependencies.<br>

The Windows Binaries for OpenSlide can be found at 'openslide.org/download/'. Download the appropriate binaries for your system (either 32-bit or 64-bit) and unzip the file.<br>

**Steps:**<br>
* a. Copy the .dll files in ../bin/ to .../Anaconda/envs/py2/Library/bin/.<br>
* b. Copy the .h files to .../Anaconda/envs/py2/include/.<br>
* c. Finally, copy the .lib file to .../Anaconda/envs/py2/libs/.<br>

Note- py2 is the name of the environment.<br>
OpenSlide has now been installed.<br>

Installing Openslide Python library<br>
conda install -c cdeepakroy openslide-python<br>
For more information refer [Anaconda page of openslide](https://anaconda.org/cdeepakroy/openslide-python).<br>

----------------------------------------------------------------
###  3. Running the code
----------------------------------------------------------------

If you are on the environment created which was just created, go the the path to that environment and then:<br>
***python anonymize-slide.py 'path for the whole slide image'***<br>
Example: python anonymize-slide.py abc.svs<br>
where abc.svs is the filename for the whole slide image and is present in the same path. If not on the same path, we need to mention the path along with the name.<br>

If the whole folder has to be anonymize with a specific format, then:<br>
__anonymize-slide.py *.svs__<br>
This will delete all the labels from the whole slide image<br>

