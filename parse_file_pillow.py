# -*- coding: UTF-8 -*-


from PIL import Image
from PIL.ExifTags import TAGS
import os


NAME_PATH = "C:/Users/051LisitsynIV/PycharmProjects/alternativa/IMG_2693.JPG"
#NAME_PATH = "C:/Users/051LisitsynIV/PycharmProjects/alternativa/enimal.jpg"

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

def read_dir(dir): # составляем список имен директории и входящих в неё файлов
    dir_file_names = []
    for root, dir, files in os.walk(dir):
        dir_file_names.append(root)
        for file in files:
            dir_file_names.append(file)

    return dir_file_names


def parsing_direction(file): # определяем направления парсинга в зависимости от расширения
    dir = file[0]
    for name in file[1:]:
        file_name = os.path.join(dir, name)
        if name.split('.')[1].lower() != 'mp4' and name.split('.')[1].lower() != 'mov':
            exif = Image.open(file_name)._getexif()
            data_time = get_field(exif, 'DateTime')
            gps_info = get_field(exif, 'GPSInfo')
            coordinate = gps_coordinat(gps_info)
            if data_time != None:       # формируем первую часть имени на основании даты съемки
                new_name = new_data_name(data_time)
                print(new_name)

            if coordinate != None:
                pass


def new_data_name(date): #
    new_name = date.split()
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
    #parce_file(NAME_PATH)
    #exif = Image.open(NAME_PATH)._getexif()
    #data_time = get_field(exif,'DateTime')
    #gps_info = get_field(exif,'GPSInfo')
    #print(get_field(exif,'GPSInfo'))
    #print(data_time)
    #print(gps_info)
    #print(gps_coordinat(gps_info))
    dir = real_path()
    ff = read_dir(dir)
    parsing_direction(ff)