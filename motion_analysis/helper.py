# define helper functions for motion_analysis purposes

def analyse_motion(time_coord_data, factor, loop_duration=500, stationary_duration=3000, underline_duration=2000):
    '''
    Parameters: 
    time_coord_data: list of tuples of (time, (x, y)) coordinates
    factor: factor to round the coordinates to
    loop_duration: minimum duration for a loop to be considered (default 0.5s)
    stationary_duration: minimum duration for a stationary point to be considered (default 3s)
    underline_duration: minimum duration for an underline to be considered (default 2s)

    Returns: all_info with time_coord_data (list of dictionaries with information about loops, stationary points, and underlines)
    '''

    # loop variables
    window = []
    loop = []
    indx = 0

    # stationary variables
    stationary = []

    # underline variables
    underline = []

    previous_coords = None

    for time, coord in time_coord_data:
        
        # ----- check for loops ----- #
        #print("Start of new sliding window / loop")
        window.append(time_coord_data[indx])
        for time_inner, coord_inner in time_coord_data[indx+1:]:
            window.append((time_inner, coord_inner))
            if window[-1][0] - window[0][0] > loop_duration: # default minimum 0.5s for anything meaningful
                if is_clockwise_or_counterclockwise(list(map(lambda x: x[1], window))) and \
                    (round_to_factor(window[-1][1][0], factor) == round_to_factor(window[0][1][0], factor)) and \
                    (round_to_factor(window[-1][1][1], factor) == round_to_factor(window[0][1][1], factor)):  # checks if loop is closed
                    
                    if loop and loop[-1][0] <= window[0][0] <= loop[-1][1]:
                        # compare end window timing with end timing of latest loop
                        if window[-1][0] > loop[-1][1]: 
                            loop[-1][1] = window[-1][0]
                    else:
                        loop.append([window[0][0], window[-1][0], 'loop']) # adds the start and end time of the loop
        window.clear()
        indx += 1

        # ----- check for stationary points ----- #
        coord_factored =  (round_to_factor(coord[0], factor), round_to_factor(coord[1],factor))
        if previous_coords is None:
            current_stationary = [time, time] # start time, end time
        elif coord_factored == previous_coords:
            current_stationary[1] = time # modify and set end time
        else:
            # default minimum 3s to indicate stationary
            if current_stationary[1] - current_stationary[0] > stationary_duration:
                stationary.append(current_stationary+['stationary'])
            # start new check
            current_stationary = [time, time] 
        

        # ----- check for underline (horizontal) points ----- #
        if previous_coords is None:
            current_underline = [time, time, coord, coord] # start time, end time, start position(unfactored), end position(unfactored)
        elif coord_factored[1] == previous_coords[1] and coord_factored[0] != previous_coords[0]: # check same y value AND different x value
            current_underline[1] = time # modify and set end time
            current_underline[3] = coord # modify and set end coord
        else:
            # default minimum 2s to indicate underline OR consider: min distance for underline
            if current_underline[1] - current_underline[0] >= underline_duration: 
                underline.append([current_underline[0], current_underline[1], 'underline'])
            # start new check
            current_underline = [time, time, coord, coord]
        
        previous_coords = coord_factored

    all_info = loop + stationary + underline

    return get_all_info(all_info, time_coord_data)


def round_to_factor(number, factor):
    '''
    Given a number and a factor, round the number to the nearest multiple of the factor
    To discretise the coordinates to a specific factor for reasonable comparison
    '''
    return ((number + factor // 2) // factor ) * factor

def orientation(p, q, r):
    '''
    Given three points p, q, and r in the specific order, 
    calculate the cross product of the vectors (p,q) and (q,r) 
    to determine the orientation of the points.

    Parameters: p, q, r are tuples of (x, y) coordinates
    Returns: 0 if collinear, 1 if clockwise, -1 if counterclockwise
    '''
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else -1  # Clockwise or Counterclockwise

def is_clockwise_or_counterclockwise(polygon):
    ''' 
    Given a list of points, check if the points form either a clockwise or counterclockwise loop.

    Parameters: polygon is a list of tuples of (x, y) coordinates
    Returns: True if the points form a clockwise or counterclockwise loop, False otherwise
    Note that the points only need to be 80% in the same direction to be considered a loop
    '''
    n = len(polygon)
    if n < 5:
        return False  # A polygon must have at least 5 points
    
    orientation_sum = 0
    for i in range(n):
        orientation_sum += orientation(polygon[i], polygon[(i + 1) % n], polygon[(i + 2) % n])

    return int(0.8*n) <= abs(orientation_sum)


# --- functions for collating analysis results --- #

def get_all_info(all_info, time_coord_data):
    all_info_dct = [] # key value pairs of start_time: info
    for info in all_info:
        all_info_dct.append(get_info(info[0], info[1], info[2], time_coord_data))
    return all_info_dct

def get_info(start_time, end_time, type, time_coord_data):
    '''
    takes in a start and end time and returns a dictionary with information stored, depending on type

    Parameters:
    start_time: start time of the motion type 
    end_time: end time of the motion type
    type: type of motion ("loop", "stationary", "underline")
    time_coord_data: list of tuples of (time, (x, y)) coordinates for the entire duration

    Note that start_time and end_time must be within the range of times in time_coord_data 

    Returns: dictionary with information about all motion types during the video
    '''
    info = {}
    info['start_time'] = start_time
    info['end_time'] = end_time
    info['type'] = type
    coord_data = list(map(lambda x: x[1], filter(lambda tup: tup[0] >= start_time and tup[0] <= end_time, time_coord_data)))

    if type == 'loop':
        info['start_pos'] = coord_data[0]
        info['end_pos'] = coord_data[-1]
        bbox = get_bounding_box(coord_data)
        info['bounding_box'] = bbox
        info['center'] = ((bbox['max_x'] - bbox['min_x'])//2, (bbox['max_y'] - bbox['min_y'])//2)
    
    if type == 'stationary':
        info['pos'] = (sum(map(lambda x: x[0], coord_data))//len(coord_data), sum(map(lambda x: x[1], coord_data))//len(coord_data))
    
    if type == 'underline':
        info['start_pos'] = coord_data[0]
        info['end_pos'] = coord_data[-1]
        info['max_distance'] = round(max(coord_data, key=lambda p: p[0])[0] - min(coord_data, key=lambda p: p[0])[0])
        
    return info

def get_bounding_box(points):
    '''
    takes in a list of coordinates and returns a dictionary with the bounding box
    '''
    min_x = min(points, key=lambda p: p[0])[0]
    max_x = max(points, key=lambda p: p[0])[0]
    min_y = min(points, key=lambda p: p[1])[1]
    max_y = max(points, key=lambda p: p[1])[1]

    bounding_box = {
        'min_x': min_x,
        'max_x': max_x,
        'min_y': min_y,
        'max_y': max_y
    }

    return bounding_box