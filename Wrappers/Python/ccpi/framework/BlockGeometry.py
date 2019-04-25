from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy
from numbers import Number
import functools
from ccpi.framework import BlockDataContainer
#from ccpi.optimisation.operators import Operator, LinearOperator
 
class BlockGeometry(object):
    '''Class to hold Geometry as column vector'''
    #__array_priority__ = 1
    def __init__(self, *args, **kwargs):
        ''''''
        self.geometries = args
        self.index = 0

        shape = (len(args),1)
        self.shape = shape

        n_elements = functools.reduce(lambda x,y: x*y, shape, 1)
        if len(args) != n_elements:
            raise ValueError(
                    'Dimension and size do not match: expected {} got {}'
                    .format(n_elements, len(args)))
                      
            
    def get_item(self, index):
        '''returns the Geometry in the BlockGeometry located at position index'''
        return self.geometries[index]            

    def allocate(self, value=0, dimension_labels=None, **kwargs):
        
        symmetry = kwargs.get('symmetry',False)        
        containers = [geom.allocate(value) for geom in self.geometries]
        
        if symmetry == True:
                        
            # for 2x2       
            # [ ig11, ig12\
            #   ig21, ig22]
            
            # Row-wise Order
            
            if len(containers)==4:
                containers[1]=containers[2]
            
            # for 3x3  
            # [ ig11, ig12, ig13\
            #   ig21, ig22, ig23\
            #   ig31, ig32, ig33]            
                      
            elif len(containers)==9:
                containers[1]=containers[3]
                containers[2]=containers[6]
                containers[5]=containers[7]
            
            # for 4x4  
            # [ ig11, ig12, ig13, ig14\
            #   ig21, ig22, ig23, ig24\
            #   ig31, ig32, ig33, ig34
            #   ig41, ig42, ig43, ig44]   
            
            elif len(containers) == 16:
                containers[1]=containers[4]
                containers[2]=containers[8]
                containers[3]=containers[12]
                containers[6]=containers[9]
                containers[7]=containers[10]
                containers[11]=containers[15]
                
                
                
        
        return BlockDataContainer(*containers)
    
    
         