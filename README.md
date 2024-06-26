# Welcome to the SegMine project!

This project contains the skeleton of a pipeline for cell profiling.
It aims to perform the bioimage analysis task proposed by Phenaros, description can be found here: https://github.com/pharmbio/SegMine/tree/main

The image segmentation was performed using online GPU access while the image analysis of the project was built on a Windows machine (8G RAM,Processor	11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz, 2803 Mhz, 4 Core(s), 8 Logical Processor(s )
To set up the environment: 
pip install -r requirements_segmine.txt 

## Below are the pipeline steps 

### 1. PrepareDataForCellpose.ipynb 
This notebook combines images acquired at 3 wavelengths into rgb (405, 488 and 730 nm). The resulting images_rgb folder was then uploaded on google drive to be accessed for the next step.

### 2. Run_cellpose.ipynb
This notebook tunes the parameters of the cyto3 model on a subset of images before running the model on the entire folder. Illustration of the segmentations are stored in data/seg_plots folder. The resulting segmentation masks were then downloaded and set in a folder parallel to the source images.
![Example result](Figures/ExampleOfSegmentation.png)

### 3. ExtractMorphoPerImage.ipynb 
This notebook harvest the cells for morphometry metrics. The median  is more robust to outliers than the mean. The median of the metrics were calculated at each well-site combo over all cells, and are stored in the file:
median_morphometry_per_site.csv 
Due to poor image quality 1 combo (well G06 site 2) was excluded from the rest of the study.

### 4. DataAnalysis.ipynb
This notebook combines informations from plate_metadata.csv with the morphometry metrics. As the plate description were providing multiple references of well-site combo an assumption was made to select arbitrarily and consistently the plate with the smallest barcode.
From the gathered data a t-SNE is performed. Combining this with the small variety of collected metrics collected, it can be expected that the resulting figure does not exhibit clusters (not even for the DMSO buffer). The results are illustrated with more plots in the data folder. 
The metrics used for this t-SNE are purely based on inividual cells number and shapes (area, min and max diameter). The intensity metrics were drafted but could not be harvested within the time constraint. Ideally in addition metrics to extract cells interactions (e.g. clustered or dispersed) could complete the research.  

![Example result](Figures/t-SNE-per_compound_type.png)
