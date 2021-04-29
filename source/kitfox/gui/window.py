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
#import mathutils
from mathutils import *
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from ..math.vecmath import *


vertices = (
    (100, 100), (300, 100),
    (100, 200), (300, 200))

indices = (
    (0, 1, 2), (2, 1, 3))

shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
#batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)

batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices})

#----------------------------------

class Label:
    def __init__(self):
        self.position = Vector((0, 0))
        self.size = Vector((100, 100))
        self.title = ""

#----------------------------------

class TextInput:
    def __init__(self):
        self.position = Vector((0, 0))
        self.size = Vector((100, 100))
        self.title = ""

#----------------------------------

class Panel:
    def __init__(self):
        self.position = Vector((0, 0))

#----------------------------------

class FoldoutPanel(Panel):
    def __init__(self):
        self.position = Vector((0, 0))

#----------------------------------

class Window:
    def __init__(self):
        self.position = Vector((0, 0))
        self.size = Vector((100, 100))
        self.title = ""
        self.titleHeight = 20
        self.background_color = Vector((.5, .5, .5, 1))
        
        self.dragging = False
        
    def mouse_click(self, context, event):
        return {'consumed': False}
        pass
        
    def mouse_move(self, context, event):
        return {'consumed': False}
        pass
        
    def draw(self, context):
        region = context.region
        #rv3d = context.region_data
        region.width
        region.x
        
        shader.bind()
#        shader.uniform_float("color", (0, 0.5, 0.5, 1.0))
        shader.uniform_float("color", self.background_color)
        batch.draw(shader)
        
        #context.
        
    def handle_event(self, context, event):
        
        if event.type == 'LEFTMOUSE':
            return self.mouse_click(context, event)
        
        elif event.type == 'MOUSEMOVE':
            return self.mouse_move(context, event)
            
        
        
#        return {'CONSUMED'}
        return {'consumed': False}
        
        