import main as repo
import requests
import configparser

config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini")


class VkRequest:
    def __init__(self, token_list, version='5.131'):
        self.token = token_list[0]
        self.id = token_list[1]
        self.version = version
        self.start_params = {'access_token': self.token, 'v': self.version}
        self.json, self.export_dict = self._sort_info()

    def _get_photo_info(self):
        url = "https://api.vk.com/method/photos.get"
        params = {'owner_id': self.id,
                  'album_id': 'profile_id',
                  'photo_sizes': 1,
                  'extended': 1,
                  'rev': 1
                  }
        photo_info = requests.get(url, params={**self.start_params, **params}).json()
        return photo_info

    def _get_logs_only(self):
        photo_count, photo_items = self._get_photo_info()
        result = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            url_download, picture_size = repo.find_max_dpi(photo_items[i]['sizes'])
            time_warp = repo.time_convert(photo_items[i]['date'])
            new_value = result.get(likes_count, [])
            new_value.append({'likes_count': likes_count,
                              'add_name': time_warp,
                              'url_picture': url_download,
                              'size': picture_size})
            result[likes_count] = new_value
        return result

    def _sort_info(self):
        json_list = []
        sorted_dict = {}
        picture_dict = self._get_logs_only()
        counter = 0
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{value["likes_count"]}.jpeg'
                else:
                    file_name = f'{value["likes_count"]} {value["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': value["size"]})
                if value["likes_count"] == 0:
                    sorted_dict[file_name] = picture_dict[elem][counter]['url_picture']
                    counter += 1
                else:
                    sorted_dict[file_name] = picture_dict[elem][0]['url_picture']
        return json_list, sorted_dict


if __name__ == '__main__':
    tokenVK = config["VKTOKEN"]
    my_VK = VkRequest(tokenVK)
    my = my_VK._get_photo_info()
    print(my)
