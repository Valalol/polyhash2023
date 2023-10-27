from PIL import Image
import os

def visualize_grid(size: tuple, warehouses_dict, orders_dict):
    img = Image.new('RGB', size, color = 'white')
    pixels = img.load()
    
    for warehouse_location in warehouses_dict.keys():
        pixels[warehouse_location] = (255,215,0)
    
    for order_location in orders_dict.keys():
        pixels[order_location] = (34,160,255)
    
    img = img.resize((size[0]*10, size[1]*10))
    
    if not os.path.exists('output/'):
        os.makedirs('output/')
    img.save(r'output/visualizer.png')


def heatmap(size: tuple, warehouses_dict, orders_dict):
    dot_size = 5
    grid = [[0 for i in range(size[1])] for j in range(size[0])]
    for warehouse_location in warehouses_dict.keys():
        for i in range(warehouse_location[0]-dot_size, warehouse_location[0]+dot_size):
            for j in range(warehouse_location[1]-dot_size, warehouse_location[1]+dot_size):
                if i >= 0 and i < size[0] and j >= 0 and j < size[1]:
                    grid[i][j] += 1
    
    for order_location in orders_dict.keys():
        for i in range(order_location[0]-dot_size, order_location[0]+dot_size):
            for j in range(order_location[1]-dot_size, order_location[1]+dot_size):
                if i >= 0 and i < size[0] and j >= 0 and j < size[1]:
                    grid[i][j] += 1
    
    max = 0
    for i in range(size[0]):
        for j in range(size[1]):
            if grid[i][j] > max:
                max = grid[i][j]
    
    img = Image.new('RGB', size, color = 'white')
    pixels = img.load()
    for i in range(size[0]):
        for j in range(size[1]):
            if grid[i][j] > 0:
                pixels[i,j] = (255,int(226*(1-grid[i][j]/max)),0)
    
    img = img.resize((size[0]*10, size[1]*10))
    
    if not os.path.exists('output/'):
        os.makedirs('output/')
    img.save(r'output/heatmap.png')