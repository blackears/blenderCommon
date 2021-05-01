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
#import sys
#import mathutils
from mathutils import *
#import bgl
#import blf
#import gpu
#from gpu_extras.batch import batch_for_shader
#from ..math.vecmath import *

from enum import Enum

# from .graphics import DrawContext2D
# from .layout import *

#----------------------------------

class MouseButton(Enum):
    UNKNOWN = 0
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3

#----------------------------------

class MouseButtonEvent:
    def __init__(self, mouse_button = MouseButton.LEFT, pos = Vector((0, 0)), screen_pos = Vector((0, 0))):
        self.mouse_button = mouse_button
        self.pos = pos.copy()
        self.screen_pos = screen_pos.copy()
        
    def copy(self):
        return MouseButtonEvent(self.mouse_button, self.pos, self.screen_pos)

    def __str__(self):
        return "bn:" + str(self.mouse_button) + " pos:" + str(self.pos) + " scrn_pos:" + str(self.screen_pos) + " " 
        
#----------------------------------

class KeyEvent:
    def __init__(self, key = "A", shift = False, ctrl = False, alt = False):
        self.key = key
        self.shift = shift
        self.ctrl = ctrl
        self.alt = alt
        
    def copy(self):
        return KeyEvent(self.key, self.shift, self.ctrl, self.alt)
        
        
        
        
        
        
        
        