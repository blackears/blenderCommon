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
    (0, 0), (1, 0),
    (1, 1), (0, 1))

# vertices = (
    # (100, 100), (300, 100),
    # (100, 200), (300, 200))

# indices = (
    # (0, 1, 2), (2, 1, 3))

shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
#batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)

batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices})
#batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coordsSquare})

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
        self.position = Vector((100, 40))
        self.size = Vector((100, 100))
        self.title = "Untitled"
        self.titleHeight = 20
        self.background_color = Vector((.5, .5, .5, 1))
        self.font_color = Vector((1, 1, 1, 1))
        self.font_dpi = 20
        self.font_size = 60
        
        self.dragging = False
        
    def mouse_click(self, context, event):
        return {'consumed': False}
        pass
        
    def mouse_move(self, context, event):
        return {'consumed': False}
        pass
      
    def coords_to_screen_matrix(self, context):
        region = context.region
        #rv3d = context.region_data

        mT = Matrix.Translation((0, region.height, 0))
        mS = Matrix.Diagonal((1, -1, 1, 1))
        return mT @ mS
        
    # def draw_string(self, context, string, pos):
        # c2s = self.coords_to_screen_matrix(context)
        
        
        
    def draw(self, context):
        bgl.glDisable(bgl.GL_DEPTH_TEST)
    
        mToScreen = self.coords_to_screen_matrix(context)
        
        
        #self.draw_string(self.title, 
        # region = context.region
        # #rv3d = context.region_data

        # mT = Matrix.Translation((0, region.height, 0))
        # mS = Matrix.Diagonal((1, -1, 1, 1))
        # mToScreen = mT @ mS


        #Background
        mT = Matrix.Translation(self.position.to_3d())
        mS = Matrix.Diagonal(self.size.to_4d())
        
        m = mToScreen @ mT @ mS
        
#        print("window mtx " + str(m))
        
        gpu.matrix.push()
        
        gpu.matrix.multiply_matrix(m)

        
        shader.bind()
#        shader.uniform_float("color", (0, 0.5, 0.5, 1.0))
        shader.uniform_float("color", self.background_color)
        batch.draw(shader)
        
        gpu.matrix.pop()

        #Text
        font_id = 0  # default font
        blf.color(font_id, self.font_color.x, self.font_color.y, self.font_color.z, self.font_color.w)
        blf.size(font_id, self.font_size, self.font_dpi)
        text_w, text_h = blf.dimensions(font_id, self.title)
        
        
        width = self.size.x
        text_x = self.position.x + (width - text_w) / 2
        text_y = self.position.y + text_h
        
        screenPos = mToScreen @ Vector((text_x, text_y, 0, 1))
        
        blf.position(font_id, screenPos.x, screenPos.y, 2)
        blf.draw(font_id, self.title)

        
    def handle_event(self, context, event):
        
        if event.type == 'LEFTMOUSE':
            return self.mouse_click(context, event)
        
        elif event.type == 'MOUSEMOVE':
            return self.mouse_move(context, event)
            
        
        
#        return {'CONSUMED'}
        return {'consumed': False}
        
        