import os.path

# обращает прайс в csv файле в обратном порядке, чтобы когда при загрузке в торговую систему он будет ей обращен - порядок стал бы таким каким был на сайте поставщика
def reverse_csv_price(lc_source_file_name:str):
    if not(os.path.exists(lc_source_file_name)):
        return
    source_file = open(lc_source_file_name, mode='r', encoding='cp1251')
    lines = source_file.read().splitlines()
    source_file.close()
    inverted_file = open(lc_source_file_name+'_reversed.csv', mode='w', encoding='cp1251')
    inverted_file.writelines(lines[0] + '\n')
    for i in reversed(lines[1:len(lines)]):
        inverted_file.write(i + '\n')
    inverted_file.close()

def delete_from_string_between_substrings(lc_source: str, lc_from: str, lc_to: str):    # удаляет подстроку из строки ограниченную начальной и конечной подстрокой
    l = lc_source.find(lc_from)
    r = lc_source.find(lc_to)
    if l > -1 and r > -1: return lc_source[:l] + lc_source[r + 1:-1]
    else: return lc_source

def file_to_str(file_path:str):         # считывает текстовый файл в строку
    with open(file_path, "r", encoding="utf-8") as myfile:
        data = ' '.join(myfile.readlines())
    myfile.close()
    return data


def prepare_for_csv_non_list (pc_value):     # подготовка к записи в csv, списки преобразуются к строке с разделителями пробелами
    if type(pc_value) =="<class 'str'>":
        return prepare_str(pc_value)
    else:       #if type(pc_value) == "<class 'list'>"
        lc = ''
        for i in pc_value:
            lc = lc + ' ' + prepare_str(i)
        return lc.strip()
    return pc_value


def prepare_for_csv_list(pc_value):     # подготовка к записи в csv, списки преобразуются в список с разделителями точка с запятой и экранируются кавычками
    if type(pc_value) == "<class 'str'>":
        return prepare_str(pc_value)
    else: #if type(pc_value) == "<class 'list'>"
        lc = ''
        ln_counter = 0
        for i in pc_value:
            ln_counter=ln_counter+1
            if ln_counter != 1: lc_comma = ';'
            else: lc_comma = ''
            lc = lc + lc_comma + prepare_str(i)
        return '"'+lc.strip()+'"'

def prepare_str(pc_value:str):  #удаляет из будущего параметра CSV недопустимые символы
    #print(pc_value)
    #print(type(pc_value))
    if pc_value != None:
        return pc_value.replace('"', '').replace(';', ' ').replace('\n', ' ').replace('\t', ' ')
        #if type(pc_value)==str: return pc_value.replace('"', '').replace(';', ' ').replace('\n', ' ').replace('\t', ' ')
        #if type(pc_value)==list:
        #    for element in pc_value:
        #        print('       ', element, type(element))
        #        exit()
    else: return ''

def sx(source_string='', left_split='', right_split='', index=1):
    # print(source_string + ' '+left_split + ' '+ right_split)
    # print(index)
    # star_position = 0
    # print('')
    # print(source_string.count(left_split))
    if source_string.count(
            left_split) < index:  # если требуется вхождение с большим номером чем имеется в исходной строке
        return ""
    lc_str = source_string
    for i in range(0, index):  # range(1,source_string.count(left_split)):
        lc_str = lc_str[lc_str.find(left_split) + len(left_split):len(lc_str)]
        # print(lc_str)
    # print(lc_str[0:lc_str.find(right_split)])
    return lc_str[0:lc_str.find(right_split)]

def is_price_have_link(price_path:str, price_link:str): #возвращает истину, если ссылка на сайт поставшика уже присустствует в прайсе
        lb_result = False
        try:
            price_file = open(price_path, mode='r', encoding='cp1251')
            lc_str = price_file.read()
            price_file.close()
            lb_result = True if lc_str.count(price_link)>0 else False
        except: lb_result = False
        return lb_result



class Price:
    def __init__(self, file_name:str):
        self.file_name = file_name
        if os.path.isfile(file_name):
            self.good = []
            self.goods = []
        else:
            self.good = []
            self.goods = []
            self.goods.append(['ID товара', 'наименование', 'описание', 'цена', 'орг %', 'ccылка на товар на сайте поставщика', 'ссылки на Фото', 'размер'])



    def add_good(self, id, name, descr, price, procent, link_on_site, link_on_pictures, size):
        self.goods.append([id, name, descr, price, procent, link_on_site, link_on_pictures, size])

    def write_to_csv(self, file_name):
        if os.path.isfile(file_name):
            #self.goods.pop(0) # удаляем заголовок списка, если будем дополнять существующий прайс
            file = open(file_name, mode='a', encoding='cp1251')
        else:
            file = open(file_name, mode='w', encoding='cp1251')

        for gd in self.goods:
            lc_str = ''
            for col in gd:
                if col != None:
                    lc_str = lc_str + col + ';'
                else:
                    lc_str = lc_str + ';'
            lc_str = (lc_str+'|').replace(';|', '').replace('|', '') + '\n'
            if not is_price_have_link(file_name, lc_str):
                file.write(lc_str)
        file.close()
        self.goods.clear()


