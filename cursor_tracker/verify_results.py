def compare_results(prediction_path_json:str,actual_path_txt:str):
    '''
    take in two paths containing json data of model detection and actual results
    - prints 
        TP (correct model detection), FP (incorrect model detection) and 
        FN (cursor not detected by model). TN is always 0 as all frames have a cursor.
        accuracy (TP+TN/total) and precision (TP/TP+FP)
    - returns a dataframe with actual versus predicted data
    '''

    import pandas as pd
    import json

    # read the prediction json file
    with open(prediction_path_json, 'r') as f:
        prediction = json.load(f)
    
    # read the actual txt file
    with open(actual_path_txt, 'r') as f:
        actual = f.readlines()

    # extract time, and bounding box x1, y1, x2, y2 from the prediction
    prediction_time_bbox_raw = [(dct['timestamp'], tuple(dct['bbox'])) for dct in prediction]
    # extract time, and x,y from the actual data
    actual_time_coord_raw = [(line.split(',')[0], [int(line.split(',')[1]), int(line.split(',')[2])]) for line in actual]
    
    # convert the list to a dataframe with columns timestamp, coord, x, y
    df = pd.DataFrame(actual_time_coord_raw, columns=['timestamp', 'coord'])
    df[['actual_x', 'actual_y']] = pd.DataFrame(df['coord'].tolist(), index=df.index)
    df['timestamp'] = df['timestamp'].astype('int64')

    df_prediction = pd.read_json(json.dumps(prediction))
    df_prediction[['pred_x1', 'pred_y1', 'pred_x2', 'pred_y2']] = pd.DataFrame(df_prediction['bbox'].tolist(), index=df_prediction.index)

    df = pd.merge(df, df_prediction, on='timestamp', how='left')
    df.drop(columns=['coord', 'coordinates', 'bbox', 'coord_x', 'coord_y'], inplace=True)

    # Get stats
    TP, FP = 0, 0
    FN = df.loc[df['class_label'].isnull()].shape[0] # number of rows
    filtered_df = df.loc[df['class_label'].notnull()].reset_index(drop=True)
    
    filtered_df['within_box'] = filtered_df.apply(lambda row: row['pred_x1'] <= row['actual_x'] <= row['pred_x2'] and row['pred_y1'] <= row['actual_y'] <= row['pred_y2'], axis=1)
    TP = filtered_df.loc[filtered_df['within_box'] == True].shape[0]
    FP = filtered_df.loc[filtered_df['within_box'] == False].shape[0]

    print(f"TP: {TP}, FP: {FP}, FN: {FN}")
    print(f"accuracy: {round((TP+FN)/(TP+FP+FN), 2)}, precision: {round(TP/(TP+FP), 2)}")

    return df