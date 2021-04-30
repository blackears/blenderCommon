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

from .graphics import *

#----------------------------------

class Rectangle2D:
    def __init__(self, x = 0, y = 0, width = 0, height = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def contains(self, x, y):
        return x >= self.x and x < self.x + self.width and y >= self.y and y < self.y + self.height
        
    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.width) + ", " + str(self.height)


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

class Layout:

    def __init__(self):
        pass
        
    def layout_components(self, bounds):
        pass

    def draw(self, ctx):
        pass

#----------------------------------

class LayoutAxis(Enum):
    X = 1
    Y = 2

#----------------------------------

class AlignX(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

#----------------------------------

class AlignY(Enum):
    TOP = 1
    CENTER = 2
    BOTTOM = 3

#----------------------------------

class ExpansionType(Enum):
    EXPAND = 1
    PREFERRED = 2
#    MIN = 3
#    MAX = 4


#----------------------------------


class LayoutBox(Layout):
    class Info:
        def __init__(self):
            self.span = 0
        

    def __init__(self, axis = Axis.X):
        super().__init__()
        
        self.axis = axis
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)

    def calc_minimum_size(self):
        span_x = 0
        span_y = 0
        
        for child in self.children:
            child = self.children[i]
            size = child.calc_minimum_size()
            
            if self.axis == Axis.X:
                span_x += size.width
                span_y = max(span_y, size.height)
            else:
                span_x = max(span_x, size.width)
                span_y += size.height
                
        return Vector((span_x, span_y))

    def calc_preferred_size(self):
        span_x = 0
        span_y = 0
        
        for child in self.children:
            child = self.children[i]
            size = child.calc_preferred_size()
            
            if self.axis == Axis.X:
                span_x += size.width
                span_y = max(span_y, size.height)
            else:
                span_x = max(span_x, size.width)
                span_y += size.height
                
        return Vector((span_x, span_y))


    def calc_maximum_size(self):
        span_x = 0
        span_y = 0
        
        for child in self.children:
            child = self.children[i]
            size = child.calc_maximum_size()
            
            if self.axis == Axis.X:
                span_x += size.width
                span_y = max(span_y, size.height)
            else:
                span_x = max(span_x, size.width)
                span_y += size.height
                
        return Vector((span_x, span_y))

    
    def layout_components(self, bounds):
        local_span = bounds.width if self.axis == Axis.X else bounds.height
    
        infoList = []
        total_span = 0
        
        
        #Allocate min sizes first
#        print("calc min")
        for i in range(len(self.children)):
            child = self.children[i]
            size = child.calc_minimum_size()
            
            info = self.Info()
            infoList.append(info)
            info.span = size.x if self.axis == Axis.X else size.y
            total_span += info.span

#            print("child %d: span %d" % (i, info.span))

        #Expand to preferred sizes if there is room
#        print("calc pref")
        for i in range(len(self.children)):
            if total_span < local_span:
                child = self.children[i]
                size = child.calc_preferred_size()
                pref_span = size.x if self.axis == Axis.X else size.y
                span_remaining = local_span - total_span
                
#                print("span_remaining " + str(span_remaining))
#                print("pref_span " + str(pref_span))
                
                info = infoList[i]
#                print("info.span " + str(info.span))
                span_to_add = min(span_remaining, pref_span - info.span)
                info.span += span_to_add
                total_span += span_to_add

#                print("child %d: span %d" % (i, info.span))
                    
        #If there is space left, expand children with expand set
#        print("calc max")
        for i in range(len(self.children)):
            if total_span < local_span:
                child = self.children[i]
                if (self.axis == Axis.X and child.expansion_type_x == ExpansionType.EXPAND) or (self.axis == Axis.Y and child.expansion_type_y == ExpansionType.EXPAND):
                    size = child.calc_maximum_size()
                    max_span = size.x if self.axis == Axis.X else size.y
                    
                    expand_to = min(max_span, local_span - total_span)
                    
                    info = infoList[i]
                    span_to_add = expand_to - info.span
                    info.span += span_to_add
                    total_span += span_to_add

#                print("child %d: span %d" % (i, info.span))
                    
        #Apply sizes
        cursor_offset = 0
        for i in range(len(self.children)):
            child = self.children[i]
            info = infoList[i]
            
            if self.axis == Axis.X:
                child.position.x = cursor_offset
                child.position.y = 0
                child.size.x = info.span
                child.size.y = bounds.height
            else:
                child.position.x = 0
                child.position.y = cursor_offset
                child.size.x = bounds.width
                child.size.y = info.span
                
            cursor_offset += info.span

    def draw(self, ctx):
        for child in self.children:
            child.draw(ctx)
            
#----------------------------------

class Panel:
    def __init__(self):
        self.background_color = Vector((.5, .5, .5, 1))
        self.font_color = Vector((1, 1, 1, 1))
        self.font_dpi = 20
        self.font_size = 60
        self.font_id = 0
        
        self.margin = None
        self.padding = None
        self.layout = None
        self.size = Vector((0, 0))
        self.maximum_size = Vector((sys.maxsize, sys.maxsize))
        self.minimum_size = Vector((0, 0))
        self.preferred_size = Vector((0, 0))
        self.expansion_type_x = ExpansionType.PREFERRED
        self.expansion_type_y = ExpansionType.PREFERRED
        
        self.position = Vector((0, 0))
        
    def bounds(self):
        return Rectangle2D(self.position.x, self.position.y, self.size.x, self.size.y)
        
    def calc_minimum_size(self):
        if self.layout != None:
            layout_size = self.layout.calc_minimum_size()
            retSize = Vector((max(layout_size.x, self.minimum_size.x), max(layout_size.y, self.minimum_size.y)))
            
        else:    
            return self.minimum_size
    
    def calc_preferred_size(self):
        if self.layout != None:
            layout_size = self.layout.calc_preferred_size()
            retSize = Vector((max(layout_size.x, self.preferred_size.x), max(layout_size.y, self.preferred_size.y)))
            
        else:    
            return self.preferred_size
    
    def calc_maximum_size(self):
        if self.layout != None:
            layout_size = self.layout.calc_maximum_size()
            retSize = Vector((max(layout_size.x, self.maximum_size.x), max(layout_size.y, self.maximum_size.y)))
            
        else:    
            return self.maximum_size

    def draw(self, ctx):
        ctx.push_transform()
        ctx.translate(self.position.x, self.position.y)
        
        self.draw_component(ctx)
        
        ctx.pop_transform()

    def draw_component(self, ctx):
        pass

#----------------------------------

class Label(Panel):
    def __init__(self, text = "label"):
        super().__init__()
        
        self.position = Vector((0, 0))
        self.size = Vector((100, 100))
        self.text = text
#        self.margin = Inset2D(2, 2, 2, 2)
#        self.margin = Vector((2, 2, 2, 2))
        self.padding = Vector((2, 2, 2, 2))
        
        self.align_x = AlignX.LEFT
        self.align_y = AlignY.TOP
        
    def calc_preferred_size(self):
        blf.size(self.font_id, self.font_size, self.font_dpi)
        text_w, text_h = blf.dimensions(self.font_id, self.text)
        
        w = text_w
        h = text_h
        if self.padding != None:
            w += self.padding[0] + self.padding[2]
            h += self.padding[1] + self.padding[3]
        
        return Vector((w, h))

    def draw_component(self, ctx):
#        print("drawing panel")
    
        blf.size(self.font_id, self.font_size, self.font_dpi)
        text_w, text_h = blf.dimensions(self.font_id, self.text)
        
        bounds = self.bounds()

#        print("bounds " + str(bounds))
        
        if self.align_x == AlignX.LEFT:
            off_x = 0
        elif self.align_x == AlignX.CENTER:
            off_x = (bounds.width - text_w) / 2
        else:
            off_x = bounds.width - text_w

        if self.align_y == AlignY.TOP:
            off_y = 0
        elif self.align_y == AlignY.CENTER:
            off_y = (bounds.height - text_h) / 2
        else:
            off_y = bounds.height - text_h
        
        x = bounds.x + off_x
        y = bounds.y + off_y + text_h
        
        if self.padding != None:
            x += self.padding[0]
            y += self.padding[1]
            
        
        ctx.draw_text(self.text, x, y)


#----------------------------------

class TextInput(Panel):
    def __init__(self):
        self.position = Vector((0, 0))
        self.size = Vector((100, 100))
        self.title = ""

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
        self.main_panel = Panel()
        self.layout.add_child(self.main_panel)
        self.main_panel.expansion_type_x = ExpansionType.EXPAND
        self.main_panel.expansion_type_y = ExpansionType.EXPAND
        
        self.layout.layout_components(self.bounds())
        
        self.set_title("")
#        print("title panel " + str(self.title_panel.bounds()))
#        print("main panel " + str(self.main_panel.bounds()))

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
        
        