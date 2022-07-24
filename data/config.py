DISTRICT_ALL_MEAN = [34.7779522, 32.0754307]
DISTRICT_ALL_COV = [[8.52817924e-05, 5.15982983e-05],
                    [5.15982983e-05, 1.44299236e-04]]

DISTRICT_3_MEAN = [34.77571312, 32.08268047]
DISTRICT_3_COV = [[2.10406225e-05, 1.16698654e-05],
                  [1.16698654e-05, 6.05453333e-05]]

DISTRICT_4_MEAN = [34.79019377, 32.08767867]
DISTRICT_4_COV = [[3.13454192e-05, 6.13334709e-07],
                  [6.13334709e-07, 4.20103657e-05]]

DISTRICT_5_MEAN = [34.7718902, 32.0670179]
DISTRICT_5_COV = [[2.87629113e-05, 8.33559110e-06],
                  [8.33559110e-06, 4.43653987e-05]]

DISTRICT_6_MEAN = [34.78304742, 32.0688201]
DISTRICT_6_COV = [[2.72357171e-05, -3.96142950e-06],
                  [-3.96142950e-06, 2.82419607e-05]]

district_probabilities = {3: [DISTRICT_3_MEAN, DISTRICT_3_COV],
                          4: [DISTRICT_4_MEAN, DISTRICT_4_COV],
                          5: [DISTRICT_5_MEAN, DISTRICT_5_COV],
                          6: [DISTRICT_6_MEAN, DISTRICT_6_COV]}

# residential
DISTRICT_RES_PROB_VEC = [0.35, 0.35, 0.2, 0.1]
# industrial
DISTRICT_IND_PROB_VEC = [0.25, 0.25, 0.25, 0.25]
# commercial
DISTRICT_COM_PROB_VEC = [0.35, 0.10, 0.45, 0.10]

zone_type_probabilities = {1: DISTRICT_RES_PROB_VEC,
                           2: DISTRICT_IND_PROB_VEC,
                           3: DISTRICT_COM_PROB_VEC}

MORNING_HOUR_MEAN = 8
AFTERNOON_HOUR_MEAN = 16
EVENING_HOUR_MEAN = 20

HOUR_VARIANCE = 1.3

MORNING_HOUR_RIDES_PROB = [0.6, 0.15, 0.1, 0.15]
AFTERNOON_HOUR_RIDES_PROB = [0.25, 0.5, 0.1, 0.15]
EVENING_HOUR_RIDES_PROB = [0.15, 0.15, 0.6, 0.1]

day_parts_hours_prob = {1: (MORNING_HOUR_MEAN, HOUR_VARIANCE),
                        2: (AFTERNOON_HOUR_MEAN, HOUR_VARIANCE),
                        3: (EVENING_HOUR_MEAN, HOUR_VARIANCE)}

day_part_rides_prob = {1: [0.6, 0.15, 0.1, 0.15],
                       2: [0.25, 0.5, 0.1, 0.15],
                       3: [0.15, 0.15, 0.6, 0.1]}

ride_type_to_zones = {1: (1, 2), 2: (2, 1), 3: (1, 3), 4: (3, 1)}

MIN_LONGITUDE = 34.756515
MAX_LONGITUDE = 34.819521

MIN_LATITUDE = 32.056657
MAX_LATITUDE = 32.102753

