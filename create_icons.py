from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple icon with the specified size"""
    
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    

    for y in range(size):
       
        r = int(102 + (118 - 102) * y / size)
        g = int(126 + (126 - 126) * y / size)
        b = int(234 + (234 - 234) * y / size)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    center = size // 2
    radius = size // 4
   
    nodes = [
        (center - radius//2, center - radius),
        (center + radius//2, center - radius),
        (center - radius, center),
        (center + radius, center),
        (center - radius//2, center + radius),
        (center + radius//2, center + radius),
    ]
  
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes[i+1:], i+1):
            draw.line([node1, node2], fill=(255, 255, 255, 100), width=2)
 
    for node in nodes:
        draw.ellipse([node[0]-4, node[1]-4, node[0]+4, node[1]+4], 
                    fill=(255, 255, 255, 200))
    
    
    img.save(filename, 'PNG')
    print(f"Created {filename}")

def main():
    """Create all required icon sizes"""
    icons = [
        (16, 'icon16.png'),
        (48, 'icon48.png'),
        (128, 'icon128.png')
    ]
    
    for size, filename in icons:
        create_icon(size, filename)

if __name__ == '__main__':
    main() 