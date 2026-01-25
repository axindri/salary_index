from enum import StrEnum


class City(StrEnum):
    moscow = "moscow"
    saint_petersburg = "saint_petersburg"
    novosibirsk = "novosibirsk"
    yekaterinburg = "yekaterinburg"
    kazan = "kazan"
    samara = "samara"
    omsk = "omsk"
    krasnoyarsk = "krasnoyarsk"
    vladivostok = "vladivostok"
    irkutsk = "irkutsk"
    barnaul = "barnaul"


DOMCLICK_CITY_MAP = [
    {"city": City.moscow, "district_name": "moskva", "city_name": "moskva"},
    {"city": City.saint_petersburg, "district_name": "sankt-peterburg", "city_name": "sankt-peterburg"},
    {"city": City.novosibirsk, "district_name": "novosibirskaya-oblast", "city_name": "novosibirsk"},
    {"city": City.yekaterinburg, "district_name": "sverdlovskaya-oblast", "city_name": "ekaterinburg"},
    {"city": City.kazan, "district_name": "respublika-tatarstan", "city_name": "kazan"},
    {"city": City.samara, "district_name": "samarskaya-oblast", "city_name": "samara"},
    {"city": City.omsk, "district_name": "omskaya-oblast", "city_name": "omsk"},
    {"city": City.krasnoyarsk, "district_name": "krasnoyarskiy-kray", "city_name": "krasnoyarsk"},
    {"city": City.vladivostok, "district_name": "primorskiy-kray", "city_name": "vladivostok"},
    {"city": City.irkutsk, "district_name": "irkutskaya-oblast", "city_name": "irkutsk"},
    {"city": City.barnaul, "district_name": "altayskiy-kray", "city_name": "barnaul"},
]


COOL_GROUPS: dict[float, str] = {
    0.0: "awful",
    0.3: "very bad",
    0.5: "bad",
    0.7: "below average",
    0.85: "normal",
    1.0: "good",
    1.2: "very good",
    1.5: "excellent",
    2.0: "great",
    3.0: "perfect",
}
