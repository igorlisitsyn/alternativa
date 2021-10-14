# -*- coding: UTF-8 -*-


from PIL import Image
from PIL.ExifTags import TAGS
from pymediainfo import MediaInfo
from geopy import GoogleV3
import os
import json
import argparse
import sys


NAME_PATH = "C:/Users/051LisitsynIV/PycharmProjects/alternativa/IMG_2558.JPEG"
#NAME_PATH = "C:/Users/051LisitsynIV/PycharmProjects/alternativa/enimal.jpg"
APY_KEY = ""


def parce_file(name):
    image = Image.open(name)

    try:
        for (k,v) in image._getexif().items():
            print(TAGS.get(k),v)
    except AttributeError:
        print("Нет атрибутов")


def real_path(): # преобразовываем windows путь, к реальному пути
    real = input("Вводим путь к файлам :")
    return real.replace("\\", "/")

def create_Parce(): # обработчик аргумента переданный в командной строке
    parser = argparse.ArgumentParser()
    try:
        parser.add_argument('-p', '--path', help = 'в качестве параметра нужно ввести путь к файлам')
        path_name = parser.parse_args(sys.argv[1:])
        path = path_name.path
        if '\\' in path:
            return path.replace("\\", "/")
        else:
            print("Укажите правильный путь")
            return None
    except TypeError:
        print('должен быть передан параметр (-h для подсказки)')


def read_dir(dir): # составляем список имен директории и входящих в неё файлов
    dir_file_names = []
    for root, dir, files in os.walk(dir):
        dir_file_names.append(root)
        for file in files:
            dir_file_names.append(file)

    return dir_file_names


def parsing_direction(file): # определяем направления парсинга в зависимости от расширения
    dir = file[0]
    new_name = ""
    for name in file[1:]:
        file_name = os.path.join(dir, name)
        if name.split('.')[1].lower() != 'mp4' and name.split('.')[1].lower() != 'mov':
            exif = Image.open(file_name)._getexif()
            data_time = get_field(exif, 'DateTime')
            gps_info = get_field(exif, 'GPSInfo')
            coordinate = gps_coordinat(gps_info)
            if data_time != None:       # формируем первую часть имени на основании даты съемки
                new_name = new_data_name(data_time)
                #print(new_name)

            if coordinate != None:
                new_name = new_name + "_" + get_goole_coordinate(coordinate, APY_KEY)
                #print(new_name)
        else:
            media_info = MediaInfo.parse(file_name, output="JSON")
            js = json.loads(media_info)
            data = js['media']['track'][0]['Encoded_Date'] # получаем ответ "UTC xxxx-xx-xx xx:xx:xx"
            no_uts = data.find(" ")
            data = data[no_uts + 1:] #              преобразовываем "UTC xxxx-xx-xx xx:xx:xx" в "xxxx-xx-xx xx:xx:xx"
            new_name = new_data_name(data)
            #print(new_name)

        new_file_name = os.path.join(dir,new_name)
        rename_file(file_name, new_file_name)    # переписываем файл с новым именем


def rename_file(old_name, new_name):
    os.rename(old_name,new_name)




def get_goole_coordinate(coordinate, APY_KEY): # получаем наименование точки на карте по координатам
    latitude = coordinate[0]
    longitude = coordinate[1]
    point_name = GoogleV3(api_key=APY_KEY).reverse((latitude, longitude))
    point_name = str(point_name)
    name_pars = point_name.split(",")
    try:
        name = name_pars[0].replace(" ","_") + "_" + name_pars[1].replace(" ","_") + "_" + name_pars[1].replace(" ","_")
    except:
        # не кривые координаты
        name = ""
    return name

def new_data_name(date): #
    new_name = date.split()
    if "-" in new_name[0]:
        new_file_name_data = str(new_name[0]).replace("-", "_") + "_" + str(new_name[1])
    else:
        new_file_name_data = str(new_name[0]).replace(":", "_") + "_" + str(new_name[1])
    return new_file_name_data



def get_field(exif, field):
    """
    :param exif: - объект из картинки содержащий информацию о метаданных
    :param field: - поля поиска (DateTime,  GPSInfo)
    :return: для 1-го возврат строки вида "2021:08:07 10:37:52"
             для 2-го возврат словаря вида "{1: 'N', 2: (53.0, 4.0, 8.55), 3: 'E', 4: (158.0, 36.0, 42.43), 5: b'\x00',
             6: 163.9537468626748, 12: 'K', 13: 0.0, 16: 'T', 17: 280.56999226604796, 23: 'T',
             24: 280.56999226604796, 31: 65.0}"
    """
    try:
        for (k,v) in exif.items():
            if TAGS.get(k) == field:
                return v
    except AttributeError:
        return None


def gps_coordinat(gps):
    try:
        part_of_the_world_1 = gps[1]
        part_of_the_world_2 = gps[3]
        coor = gps[2]

        gps_latitude = float(coor[0]) + float(coor[1]) / 60 + float(coor[2]) /3600
        if part_of_the_world_1 == 'S':
            gps_latitude = -gps_latitude

        coor = gps[4]
        gps_longitude = float(coor[0]) + float(coor[1]) / 60 + float(coor[2]) / 3600

        if part_of_the_world_2 == 'W':
            gps_longitude = -gps_longitude

        return (gps_latitude,gps_longitude)
    except:
        return None


if __name__ == '__main__':
    """
    скрипт предназначен для просмотра каталога 
    содержащего фотографии сохраненые с телефона (фотоаппарата)
    |
    | запуск через командную строку : python parse_file_pillow.py -p disk:\xxxxx\xxxx\....
    |
    | -h помощь
    """

    #!dir = real_path() # запуск через IDE
    dir = create_Parce()
    ff = read_dir(dir)
    parsing_direction(ff)