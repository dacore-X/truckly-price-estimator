from app.internal.schema.delivery import Delivery

# Dataframe train data
# Количество км, Пеший, Газель, Легковой, Минивэн, Удлиненная газель, Ночь, Рабочее время, Раннее утро/поздний вечер, Наличие грузчика

# helper function for categorizing time
def __convert_time(hour: int):
    if 0 <= hour <= 5:  # Ночь
        return [1, 0, 0]
    elif 6 <= hour <= 10 or \
        20 <= hour <= 23:  # Раннее утро/поздний вечер
        return [0, 0, 1]
    elif 11 <= hour <= 19:  # Рабочее время
        return [0, 1, 0]


# helper function for getting dummy vector of delivery type
def __convert_type(type_id: int):
    arr = [0] * 5  # 5 - amount of delivery types
    arr[type_id - 1] = 1
    return arr


# converting input Delivery model into a vector for predicting price
def convert_vector(delivery: Delivery):
    vec = [delivery.distance]

    vec_type = __convert_type(delivery.type_id)
    vec.extend(vec_type)

    vec_time = __convert_time(delivery.time.hour)
    vec.extend(vec_time)

    vec.append(int(delivery.has_loader))

    return vec
