def get_basket_id(product_id: int) -> str:
    short_id = product_id // 100000

    if 0 <= short_id <= 143:
        basket = "01"
    elif 144 <= short_id <= 287:
        basket = "02"
    elif 288 <= short_id <= 431:
        basket = "03"
    elif 432 <= short_id <= 719:
        basket = "04"
    elif 720 <= short_id <= 1007:
        basket = "05"
    elif 1008 <= short_id <= 1061:
        basket = "06"
    elif 1062 <= short_id <= 1115:
        basket = "07"
    elif 1116 <= short_id <= 1169:
        basket = "08"
    elif 1170 <= short_id <= 1313:
        basket = "09"
    elif 1314 <= short_id <= 1601:
        basket = "10"
    elif 1602 <= short_id <= 1655:
        basket = "11"
    elif 1656 <= short_id <= 1919:
        basket = "12"
    else:
        basket = "13"

    return basket
