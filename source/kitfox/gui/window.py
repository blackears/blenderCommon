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

# class Inset2D:
    # def __init__(self, left = 0, top = 0, right = 0, bottom = 0):
        # self.left = left
        # self.top = top
        # self.right = right
        # self.bottom = bottom
        
    # def __str__(self):
        # return str(self.left) + ", " + str(self.top) + ", " + str(self.right) + ", " + str(self.bottom)
    





#----------------------------------

class TextInput(Label):
    def __init__(self, text = "label"):
        super().__init__(text)

#----------------------------------

class FoldoutPanel(Panel):
    def __init__(self):
        super().__init__()
        self.position = Vector((0, 0))

#----------------------------------

class Window:
    def __init__(self):
        self.position = Vector((100, 40))
        self.size = Vector((400, 400))
#        self.__title = "Untitled"
#        self.titleHeight = 20
        self.background_color = Vector((.5, .5, .5, 1))
        self.font_color = Vector((1, 1, 1, 1))
        self.font_dpi = 20
        self.font_size = 60
        
        self.dragging = False
        
        self.layout = LayoutBox(Axis.Y)
        
        self.title_panel = Label("foo")
        self.layout.add_child(self.title_panel)
        self.title_panel.set_font_size(60)
        
        self.main_panel = Panel()
        self.layout.add_child(self.main_panel)
        self.main_panel.expansion_type_x = ExpansionType.EXPAND
        self.main_panel.expansion_type_y = ExpansionType.EXPAND
        
        
        self.set_title("")
#        print("title panel " + str(self.title_panel.bounds()))
#        print("main panel " + str(self.main_panel.bounds()))

        self.layout.layout_components(self.bounds())

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title
        self.title_panel.text = title

    def get_main_panel(self):
        return self.main_panel
        
    def bounds(self):
        return Rectangle2D(self.position.x, self.position.y, self.size.x, self.size.y)
            
    def mouse_click(self, context, event):
        c2s = self.coords_to_screen_matrix(context)
        s2c = c2s.inverted()
        mouse_pos = s2c @ Vector((event.mouse_region_x, event.mouse_region_y, 0, 1))

        # print ("event.mouse_region_x " + str(event.mouse_region_x))
        # print ("event.mouse_region_y " + str(event.mouse_region_y))
        # print ("mouse_pos " + str(mouse_pos))
        
        bounds = self.bounds()
        
        # print ("bounds " + str(bounds))
        
        if bounds.contains(mouse_pos.x, mouse_pos.y):
            if event.value == "PRESS":
                self.dragging = True
                self.mouse_down_pos = mouse_pos
                self.start_position = self.position.copy()
            else:
                self.dragging = False
            return {'consumed': True}
    
        return {'consumed': False}
        
    def mouse_move(self, context, event):
        c2s = self.coords_to_screen_matrix(context)
        s2c = c2s.inverted()
        mouse_pos = s2c @ Vector((event.mouse_region_x, event.mouse_region_y, 0, 1))
        
        
        if self.dragging:
            offset = mouse_pos - self.mouse_down_pos
    
            self.position = self.start_position + offset.to_2d()
            return {'consumed': True}
            
        return {'consumed': False}
      
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
        
        ctx = DrawContext2D(context)
        
    
        # c2s = self.coords_to_screen_matrix(context)
        
        ctx.translate(self.position.x, self.position.y)
        ctx.color = self.background_color.copy()
#        ctx.fill_rectangle(0, 0, self.size.x, self.size.y)
        ctx.fill_round_rectangle(0, 0, self.size.x, self.size.y, 10)

        # #Text
        # font_id = 0  # default font
        # blf.size(font_id, self.font_size, self.font_dpi)
        # text_w, text_h = blf.dimensions(font_id, self.title)
        
        
        # width = self.size.x
        # text_x = self.position.x + (width - text_w) / 2
        # text_y = self.position.y + text_h

        # ctx.draw_text(self.title, text_x, text_y)


        #Draw panel components
        self.layout.draw(ctx)

        
    def handle_event(self, context, event):
        
        if event.type == 'LEFTMOUSE':
            return self.mouse_click(context, event)
        
        elif event.type == 'MOUSEMOVE':
            return self.mouse_move(context, event)
            
        
        
#        return {'CONSUMED'}
        return {'consumed': False}
        
        