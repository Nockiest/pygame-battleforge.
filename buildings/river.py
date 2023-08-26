import pygame
import random
from .structure import Structure
from config import *
from utils.utils import *
 

class River(Structure):
    def __init__(self,startpoint, endpoint, control_points  ):

        super().__init__(startpoint[0], startpoint[1], size = 5, color=RIVER_BLUE)
        self.points = [] 
        self.control_points = control_points 
        self.convergence_point = None
        # self.chunks = []
        self.num_segments = 10
        self.startpoint = startpoint
        self.endpoint = endpoint
        

    def generate_chunks(self, rivers):
        for i in range(self.num_segments + 1):
            t = i / self.num_segments
            point = calculate_bezier_curve(t, self.startpoint, self.endpoint,self.control_points[0], self.endpoint) # měl bych využít oba control pointy
            rounded_point = (round(point[0]), round(point[1]))
            intersects = False  # Initialize the intersection flag as False
            self.points.append(rounded_point)


            for existing_river in  rivers:
                for j in range(len(existing_river.points) - 1):
                    intersection = do_lines_intersect(self.points[len(self.points) - 2], rounded_point, existing_river.points[j], existing_river.points[j+1])
                    # print(intersection, existing[j], existing[j+1] )
                    if intersection:
                        intersects = True  # Set the intersection flag to True
                        # print(intersection)
                        convergence_point = existing_river.points[j+1]  # Store the intersection point
                        self.convergence_point = convergence_point
                        break  # Break the inner loop once an intersection is found


                if intersects:  # If an intersection is found, break the outer loop
                    break


            if intersects:  # If an intersection is found, break the loop and do not add the river
                break


        if self.convergence_point  != None:
            self.points[-1] = self.convergence_point   # Replace the last point with the intersection point

  