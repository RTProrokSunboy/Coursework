import datetime
import json
import configparser
import VkScript
import YandexScript

config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini")


def find_max_dpi(dict_in_search):
    max_dpi = 0
    need_elem = 0
    for j in range(len(dict_in_search)):
        file_dpi = dict_in_search[j].get('width') * dict_in_search[j].get('height')
        if file_dpi > max_dpi:
            max_dpi = file_dpi
            need_elem = j
    return dict_in_search[need_elem].get('url'), dict_in_search[need_elem].get('type')


def time_convert(time_unix):
    time_bc = datetime.datetime.fromtimestamp(time_unix)
    str_time = time_bc.strftime('%Y-%m-%d time %H-%M-%S')
    return str_time


if __name__ == '__main__':
    tokenVK = config["VKTOKEN"]
    tokenVK = [str(item) for item in tokenVK]
    tokenYandex = config["YaTOKEN"]["OAuthtoken"]

    my_VK = VkScript.VkRequest(tokenVK)

    with open('my_VK_photo.json', 'w') as outfile:
        json.dump(my_VK.json, outfile)

    my_yandex = YandexScript.Yandex('VK photo copies', tokenYandex, 5)
    my_yandex.create_copy(my_VK.export_dict)
