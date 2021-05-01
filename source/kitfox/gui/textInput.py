# This file is part of the Kitfox Blender Common distribution (https://github.com/blackears/blenderCommon).
# Copyright (c) 2021 Mark McKay
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import bpy
import sys
#import mathutils
from mathutils import *
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from ..math.vecmath import *

from enum import Enum

from .graphics import DrawContext2D
from .layout import *
from .panel import *
from .label import *

#----------------------------------

class TextInput(Label):
    def __init__(self, text = "label"):
        super().__init__(text)

        self.set_background_color(Vector((.7, .7, .7, 1)))
        self.set_border_radius(4)
        self.set_align_x(AlignX.RIGHT)

    # def handle_event(self, context, event):
        # panel_pos = self.get_screen_position()
        # click_pos = event.
    
        # if event.value == "PRESS":
            # print ("TextInput press")
            
        # return False

    def mouse_pressed(self, event):
        print ("TextINput pressed")
        print("event.pos" + str(event.pos))
        print("event.screen_pos" + str(event.screen_pos))
        return True
        
    def mouse_released(self, event):
        print ("TextINput released")
        print("event.pos" + str(event.pos))
        print("event.screen_pos" + str(event.screen_pos))
        return True
        
    def mouse_moved(self, event):
        return True


