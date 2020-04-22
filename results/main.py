import json
import math
import plotly.graph_objects as go
import plotly.express as px
from textwrap import wrap
import random
import operator

# Rectangle class

class Rectangle():
	    def __init__(self, h, w):
	        self.height = h
	        self.width  = w
	
	    def rectangle_area(self):
	        return self.height*self.width
	
# set
set = {
      

  'ExampleSetE': [[1, 27], [9, 21], [14, 2], [20, 29], [4, 22], [10, 26], [12, 1]]  
    }


# iterate through set t0 get amount of rectangles, total area and sort rectangles according to height
def iterate ():
    global area_rectangles
    global amount_rectangles
    global h
    global w
    global order
    for i in set:
        a = (set[i]) 
        area_rectangles = 0
        amount_rectangles = 0
        order = []
        for x in a:
            if x[0] < x[1]:
                w =x[0]
                h = x[1]
            else:
                w =x[1]
                h = x[0]

            newRectangle = Rectangle(h, w)
            area = newRectangle.rectangle_area()
            amount_rectangles = amount_rectangles + 1
            area_rectangles = area_rectangles + area
            order.append([h,w,area])    
        order.sort(key = operator.itemgetter(0), reverse=True)
    
# Random color for each rectangle
def color():
    global rgb
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    rgb = f"rgb{(r,g,b)}"
    return rgb      




# array of all 
global points
global result
points = [[0,0,0,0]]
result = []

# Calculation of x0 , y0, x1, y1 and all previous rectangles
def calculate(i, index):

    height, width, area = i
    prev = points[-1]
    prev_x1 = prev[2]

    # Rectangles 1 - 4
    if index < 4: 
        x0 = prev_x1
        y0= 0
        x1= prev_x1 + width
        y1= height
        max_x0 = max(map(lambda x:x[2], points))
        max_y0 = max(map(lambda x:x[3], points))
        points.append([x0,y0,x1,y1])
        
    # Fifth rectangle
    elif index == 4:
        zero= points[0]
        first = points[1]
        second = points[2]
        third = points[3]
        fourth = points[4]
        max_x0 = max(map(lambda x:x[2], points))
        max_y0 = max(map(lambda x:x[3], points))

        x0 = zero[3]
        y0= first[3] 
        x1= zero[3]+height
        y1= first[3]+ width
        points.append([x0,y0,x1,y1])

    # Sixth rectangle
    elif index == 5:
        first = points[1]
        second = points[2]
        third = points[3]
        fourth = points[4]
        fifth = points[5]
        max_x0 = max(map(lambda x:x[2], points))
        max_y0 = max(map(lambda x:x[3], points))
     
        x0 = second[2] if second[2] > fifth[2] else fifth[2]
        y0= third[3]  
        x1= second[2]+height if second[2] > fifth[2] else fifth[2]+height
        y1= third[3]+ width

        points.append([x0,y0,x1,y1])
    
    # Seventh rectangle
    elif index == 6:
        first = points[1]
        second = points[2]
        third = points[3]
        fourth = points[4]
        fifth = points[5]
        sixth = points[6]

        max_x0 = max(map(lambda x:x[2], points))
        max_y0 = max(map(lambda x:x[3], points))
       
        x0 = third[2] if third[2] > sixth[2] else sixth[2]
        y0= fourth[3] 
        x1= third[2]+height if third[2] > sixth[2] else sixth[2]+height
        y1= fourth[3]+ width

        points.append([x0,y0,x1,y1])

# Calculations for result
        req_area = max_x0 * max_y0 
        
        bounding_perimeter = 2*(max_x0 + max_y0)
        bounding_perimeter = round(bounding_perimeter,2)
        missing_space = req_area - area_rectangles
    
        missing_space= round(missing_space, 2)
        total_area = area_rectangles + missing_space
        total_area=round(total_area, 2)
        perc_missing_space = missing_space/total_area
        perc_missing_space= round(perc_missing_space, 2)
        ratio_perimeter_area = bounding_perimeter/total_area
        ratio_perimeter_area= round(ratio_perimeter_area, 2)
        result.extend([bounding_perimeter, missing_space, total_area, perc_missing_space, ratio_perimeter_area])
       
    return x0,y0,x1,y1  
   
iterate()
color()


fig = go.Figure(layout_title_text=f"{set.popitem()[0]}")


# VISUALIZATION


for index, i in enumerate(order, start=0): 
          a,b,c,d = calculate(i,index)  
          fig.add_shape(
            # filled Rectangle
                type="rect",
                x0= a,
                y0= b,
                x1= c,
                y1= d,
                line=dict(
                    color="White",
                    width=1,
                ),
                fillcolor = color(),
                

            )

# Add rectangle number
count = 0   
for i in points[1:]:  
    count +=1 
    fig.add_trace(go.Scatter(
        x=[i[0], i[2]],
        y=[i[1], i[3]],
        text=[f"{count}"],
        mode="text",
        textfont = dict(
            color="black",
            size=16,
            family ="Arial",
        )
    ))      

# Set axes properties as well as show results

fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    xaxis_title = f"1) {result[0]}"
                    f" 2) {result[1]}" 
                    f" 3) {result[2]}"
                    f" 4) {result[3]}"
                    f" 5) {result[4]}",
  
  
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=0,
      
    ),
    paper_bgcolor="LightSteelBlue",

)           

fig.update_shapes(dict(opacity = 1,xref='x', yref='y', layer="below"))
fig.show()


