from sklearn.preprocessing import MinMaxScaler


def calculate_remaining_features(i,json_data):
    row = {
        'id'                     : i,
        ' Flow Duration'         : json_data['Flow Duration']['statistics']['sum'],
        'Bwd Packet Length Max'  : json_data['Bwd Packet Length']['statistics']['max'],
        ' Bwd Packet Length Min' : json_data['Bwd Packet Length']['statistics']['min'],
        ' Bwd Packet Length Mean': json_data['Bwd Packet Length']['statistics']['average'],
        ' Bwd Packet Length Std' : json_data['Bwd Packet Length']['statistics']['std'],

        ' Flow IAT Std'          : json_data['Flow IAT']['statistics']['std'],
        ' Flow IAT Max'          : json_data['Flow IAT']['statistics']['max'],

        'Fwd IAT Total'          : json_data['Fwd IAT']['statistics']['sum'],
        ' Fwd IAT Std'           : json_data['Fwd IAT']['statistics']['std'],
        ' Fwd IAT Max'           : json_data['Fwd IAT']['statistics']['max'],

        ' Min Packet Length'     : json_data['Packet Length']['statistics']['min'],
        ' Max Packet Length'     : json_data['Packet Length']['statistics']['max'],
        ' Packet Length Mean'    : json_data['Packet Length']['statistics']['average'],
        ' Packet Length Std'     : json_data['Packet Length']['statistics']['std'],
        ' Packet Length Variance': json_data['Packet Length']['statistics']['std']**2,

        ' Average Packet Size'   : json_data['Packet Size']['statistics']['average'],
        ' Avg Bwd Segment Size'  : json_data['Bwd Segment Size']['statistics']['average'],
        'Idle Mean'              : json_data['Idle']['statistics']['average'],
        ' Idle Max'              : json_data['Idle']['statistics']['max'],
        ' Idle Min'              : json_data['Idle']['statistics']['min']
        }
    return row
    

def preprocess_data(features):
    scaler = MinMaxScaler()
    features = scaler.fit_transform(features)
    return features