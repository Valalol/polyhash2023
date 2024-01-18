import os
import math

def visualize_grid(size: tuple, warehouses_dict, orders_dict):
    from PIL import Image
    
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
    from PIL import Image
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



def coverage_map(size: tuple, warehouses_dict, orders_dict):
    import matplotlib.pyplot as plt
    
    radius = 40
    warehouses_x = [i[1] for i in warehouses_dict.keys()]
    warehouses_y = [i[0] for i in warehouses_dict.keys()]
    orders_x = [i[1] for i in orders_dict.keys()]
    orders_y = [i[0] for i in orders_dict.keys()]
    
    fig, ax = plt.subplots()
    
    plt.scatter(warehouses_x, warehouses_y, s=50, c='#ffb000', marker='o', alpha=0.7)
    for i in range(len(warehouses_x)):
        ax.add_patch(plt.Circle((warehouses_x[i], warehouses_y[i]), radius, color='#37ff00', alpha=0.2))
    
    
    colors = ["#d42708" for _ in range(len(orders_x))]
    covered = 0
    for i in range(len(orders_x)):
        for j in range(len(warehouses_x)):
            if math.sqrt((orders_x[i] - warehouses_x[j])**2 + (orders_y[i] - warehouses_y[j])**2) < radius:
                colors[i] = "#34a0ff"
                covered += 1
                break
    
    print(f"Orders covered: {covered}/{len(orders_x)} ({covered/len(orders_x)*100}%)")
    
    plt.scatter(orders_x, orders_y, s=20, c=colors, marker='o', alpha=0.7)
    
    
    plt.xlim(-50, size[1]+50)
    plt.ylim(-50, size[0]+50)
    plt.gca().set_aspect('equal')
    plt.show()



def simple_summary(rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict, warehouses_list, orders_list, tick, score):
    text = f"The grid is {rows} rows by {columns} columns. ({rows*columns} cells)\n"
    text += f"There are {drone_count} drones available each with a maximum load of {max_load}.\n"
    text += f"The deadline is {deadline} turns.\n"
    text += f"There are {len(products_weight)} different product types.\n"
    text += f"Their weights ranges from {min(products_weight)} to {max(products_weight)} with an average of {round(sum(products_weight)/len(products_weight), 2)}.\n"
    text += f"There are {len(warehouses_list)} warehouses.\n"
    text += f"There are {len(orders_list)} orders with an average of {round(sum([len(order.items) for order in orders_list])/len(orders_list), 2)} items per order.\n"
    print(text)