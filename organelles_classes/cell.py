import numpy as np

class Cell:
    def __init__(self, cell_id=-1, pixel_coordinates=[]):
        self.center = [0,0]
        self.cell_id = cell_id
        self.pixel_coord = pixel_coordinates
        self.morphometry = {'area': 0, 'min_diam': 0, 'max_diam': 0, 'nucleus': None, 'intensities': None}

    def set_center(self, center):
        self.center = center
        
    def set_area(self, area):
        """
        Set the area of the cell.
        """
        self.morphometry['area'] = area

    def set_min_diameter(self, min_diameter):
        """
        Set the minimum diameter of the cell.
        """
        self.morphometry['min_diam'] = min_diameter

    def set_max_diameter(self, max_diameter):
        """
        Set the maximum diameter of the cell.
        """
        self.morphometry['max_diam'] = max_diameter

    def set_nucleus(self, nucleus):
        """
        Set the nucleus object.
        """
        self.morphometry['nucleus'] = nucleus

    def set_intensities(self, intensities):
        """
        Set the intensities object.
        """
        self.morphometry['intensities'] = intensities

    def calculate_morphometrics(self):    
        # Calculate the center coordinate
        center = np.mean(self.pixel_coord, axis=1)
        self.set_center(center)
    
        # Calculate the distances of each point from the center
        distances = np.linalg.norm(np.array(self.pixel_coord).T - np.array(center), axis=1)

        # Calculate the minimum and maximum diameters
        min_diameter = 2 * np.min(distances)
        max_diameter = 2 * np.max(distances)
        self.set_min_diameter(min_diameter) 
        self.set_max_diameter(max_diameter)
        
        # Calculate the area
        self.set_area(np.pi * (max_diameter / 2) * (min_diameter / 2))

    def calculate_intensity_metrics(self, im_stack):
        # get stat through each im stack
        stats =[]
        for i in range(len(im_stack)):
            intensities = im_stack[i][self.pixel_coord]
            stats.append([np.mean(intensities), np.std(intensities)])
        self.set_intensities(stats)
        

