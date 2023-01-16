import math


def make_pagination_range(
    page_range,
    qtd_paginas,
    current_page
):
    middle_range = math.ceil(qtd_paginas/2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    return page_range[start_range:stop_range]