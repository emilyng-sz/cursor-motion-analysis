# Functions should largely be used in order to visualise tracker through plots and animations

def get_time_coord_raw(json_path:str):
    '''
    take in json_path:str and outputs time_coord_raw: List[Tuple[Int, Tuple[Int, Int]]] 
    '''
    import pandas as pd
    import json
    # read the json file
    with open(json_path, 'r') as f:
        data = json.load(f)
    # convert the json data to a dataframe
    df = pd.read_json(json.dumps(data))
    return list(zip(df['timestamp'], df['coordinates']))

def post_process_data(time_coord_raw, height, split = False, threshold=None): # can set default to threshold=2*FPS
    ''' 
    takes in time_coord_raw:List[Tuple[Int, Tuple[Int, Int]]] 
    - sorts all_data based on timestamp 
    - adjust height of data

    if split = True, splits all_data in different sections based on threshold:int
        - reccomended: 2* FPS
        - threshold should be minimally more than FPS

    returns a List[List[Tuple[Int, Tuple[Int, Int]]] 
    '''
    time_coord_raw.sort(key=lambda tup: tup[0]) # sort by timestamp
    time_coord_raw = list(map(lambda x: (x[0], (round(x[1][0], 2), round(height - x[1][1],2))), time_coord_raw)) # adjust height

    if split:
        def get_time(tup): 
            return tup[0]

        sections = []
        section = [time_coord_raw[0],] # add first element 
        for index in range(1,len(time_coord_raw)):
            if get_time(time_coord_raw[index-1]) + threshold < get_time(time_coord_raw[index]):
                sections.append(section)
                section = []

            section.append(time_coord_raw[index])
        sections.append(section)

        assert len(time_coord_raw) == sum(map(len, sections)) # check that each tuple in all_data is in sections 

        print(f"all_data split into {len(sections)} sections, each of {tuple(map(len, sections))} length")

        return sections
    else:
        return time_coord_raw

def group_coordinates(all_data, height, width, factor):
    ''' takes in all_data 
        and returns new_all_data, x and y as three separate lists '''
    return list(map(lambda tup: (tup[0], (tup[1][0]//factor, tup[1][1]//factor)), all_data)), height/factor, width/factor

def plot_2D(time_coord_data):
    ''' Visualise 2D trajectory as plot '''
    import matplotlib.pyplot as plt
    _, x_values, y_values = list(map(lambda x: x[0], time_coord_data)), \
           list(map(lambda x: x[1][0], time_coord_data)), \
           list(map(lambda x: x[1][1], time_coord_data))
    plt.scatter(x_values, y_values, color='blue', marker='o', alpha = 0.5)
    # Set axis labels and plot title
    plt.xlabel('X position')
    plt.ylabel('Y position')
    plt.title('Positions of cursor on screen')
    # Display the plot
    plt.grid(True)
    plt.show()

def plot_3D(time_coord_data):

    ''' plot 3D plot to show position over time'''
    import matplotlib.pyplot as plt
    timestamps, x_values, y_values = list(map(lambda x: x[0], time_coord_data)), \
           list(map(lambda x: x[1][0], time_coord_data)), \
           list(map(lambda x: x[1][1], time_coord_data))
    ax = plt.figure().add_subplot(projection='3d')

    ax.scatter(x_values, timestamps, y_values, label='Position of cursor over time')
    ## notice a scatter plot is used because there are missing timestamps in cursor detection

    ax.set_xlabel("X position")
    ax.set_ylabel("Time (ms)")
    ax.set_zlabel("Y position")
    ax.legend()

    plt.show()

def plot_3D_animation(time_coord_data, height, width, path):
    ''' Creates 3D plot with animation and SAVES to gif format '''
    from matplotlib import pyplot as plt
    import numpy as np
    from matplotlib import animation
    timestamps, x_values, y_values = list(map(lambda x: x[0], time_coord_data)), \
           list(map(lambda x: x[1][0], time_coord_data)), \
           list(map(lambda x: x[1][1], time_coord_data))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    def gen(N):
        '''return (x,y,z) in array format '''
        for i in range(N):
            yield np.array([x_values[i], timestamps[i], y_values[i]])

    def update(num, data, line):
        line.set_data(data[:2, :num])
        line.set_3d_properties(data[2, :num])

    N = len(x_values)
    data = np.array(list(gen(N))).T
    line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1])

    # Setting the axes properties
    ax.set_xlim3d([0, width])
    ax.set_xlabel('X Position')

    ax.set_ylim3d([0, timestamps[-1]])
    ax.set_ylabel('Time (ms)')

    ax.set_zlim3d([0, height])
    ax.set_zlabel('Y Position')

    ani = animation.FuncAnimation(fig, update, N, fargs=(data, line), interval=10000/N, blit=False)
    ani.save(path)
    plt.show()