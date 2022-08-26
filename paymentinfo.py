
def get_fare_amount(user_category, distance_travelled):
    actual_fare_amount = int(fare_calculator(distance_travelled))
    if str(user_category).lower() == "others" or str(user_category).lower() == "other":
        return actual_fare_amount
    else:
        return(actual_fare_amount-actual_fare_amount*0.45)


def fare_calculator(distance_travelled):
    if distance_travelled < 5:
        return 25
    elif distance_travelled < 10:
        return 30
    elif distance_travelled < 20:
        return 35
    else:
        return 40

