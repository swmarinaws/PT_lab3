"""
1) Придумать «простую» и «сложную» (более эффективную по скорости и с меньшим числом коллизий) хэш-функции вычисления хэша ключевого поля своего класса.

2) Добавить поле со значением хэша в класс, изменить конструкторы и методы соответствующим образом.

3) Построить хэш таблицу на основе значения хэша и написать функцию поиска элемента в массиве объектов с использованием хэш-таблицы, реализовать один из методов разрешения коллизий.

4) Провести эксперименты с исследованием зависимости времени поиска от размерности массива для обоих хэш-функций, построить графики.

5) Сравнить результаты с результатами времени поиска, полученными в предыдущей работе.

6) Исследовать зависимость числа коллизий для каждой хэш-функции от размерности массива, построить график.

Массив данных о преподавателях: ФИО преподавателя, факультет, ученое звание, ученая степень (сравнение по  полям - ФИО, факультет, степень, звание)
"""

import random
from russian_names import RussianNames
import pandas as pd
import timeit

list_faculties = ['Биологический', 'Богословский','Географический', 'Геологический', 'Журналистики', 'Информационный', 'Исторический', 'Кибернетики', 'Математический', 'Механический', 'Политологический', 'Психологический', 'Радиотехнический', 'Социологический', 'Управления', 'Физический', 'Филологический', 'Философский', 'Химический', 'Художественно-графический', 'Экономический', 'Юридический']
list_ranks = ['Доцент', 'Профессор']
list_degrees = ['Кандидат наук', 'Доктор наук']
sizes = [100, 250, 500, 1000, 5000, 10000, 100000]

"""Время поиска"""
time_difficulty, time_simple = [], []

def generate(n):
    """Генерирование n данных"""
    final_dict = {}
    names, surnames, patronymics, faculties, ranks, degrees = [], [], [], [], [], []
    for i in range(n):
        full_name = RussianNames().get_person().split()
        names.append(full_name[0])
        patronymics.append(full_name[1])
        surnames.append(full_name[2])
        faculties.append(random.choice(list_faculties))
        ranks.append(random.choice(list_ranks))
        degrees.append(random.choice(list_degrees))

    final_dict['Фамилия'] = surnames
    final_dict['Имя'] = names
    final_dict['Отчество'] = patronymics
    final_dict['Факультет'] = faculties
    final_dict['Учёная степень'] = ranks
    final_dict['Учёное звание'] = degrees
    return final_dict

def quick_sort(l, fst, lst):
    """Быстрая сортировка"""
    if fst >= lst: return

    i, j = fst, lst
    pivot = l[fst + (lst - fst) // 2]

    while i <= j:
        while l[i] < pivot: i += 1
        while l[j] > pivot: j -= 1
        if i <= j:
            l[i], l[j] = l[j], l[i]
            i += 1
            j -= 1

    quick_sort(l, fst, j)
    quick_sort(l, i, lst)

def linear_search(l, key):
    """Прямой поиск"""
    for i in range(len(l)):
        if l[i] == key:
            return i
    return -1

def binary_search(l, start, end, key):
    """Бинарный поиск"""
    if start > end: return -1

    middle = start + (end - start) // 2

    if l[middle] == key:
        return middle
    elif l[middle] > key:
        return binary_search(l, start, middle - 1, key)
    return binary_search(l, middle + 1, end, key)

def calculate_hash(value):
    """Сложная хэш-функция"""
    prime = 31  # простое число для вычисления хэша
    hash_value = 0
    for char in value:
        hash_value = (hash_value * prime + ord(char))  # суммируем коды символов с учетом предыдущего значения
    return hash_value

def calculate_hash_simple(value):
    """Простая хэш-функция"""
    hash_value = 0
    for char in value:
        hash_value += ord(char)  # суммируем коды символов с учетом предыдущего значения
    return hash_value

class Teacher:
    """Класс для описания объекта преподавателя"""
    """Объект включает в себя: фамилию, имя, отчество, факультет, учёное звание, учёную степень"""
    def __init__(self, surname, name, patronymic, faculty, rank, degree):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.faculty = faculty
        self.rank = rank
        self.degree = degree
        self.hash = calculate_hash(surname)  #вычисляем хэш для поля surname
        self.hash_simple = calculate_hash_simple(surname) #вычисляем хэш для поля surname

    def __gt__(self, other):
        """Перегрузка оператора >"""
        if self.faculty != other.faculty:
            return self.faculty > other.faculty
        if self.surname != other.surname:
            return self.surname > other.surname
        if self.name != other.name:
            return self.name > other.name
        if self.patronymic != other.patronymic:
            return self.patronymic > other.patronymic
        if self.degree != other.degree:
            return self.degree > other.degree
        return self.rank > other.rank

    def __lt__(self, other):
        """Перегрузка оператора <"""
        if self.faculty != other.faculty:
            return self.faculty < other.faculty
        if self.surname != other.surname:
            return self.surname < other.surname
        if self.name != other.name:
            return self.name < other.name
        if self.patronymic != other.patronymic:
            return self.patronymic < other.patronymic
        if self.degree != other.degree:
            return self.degree < other.degree
        return self.rank < other.rank

    def __ge__(self, other):
        """Перегрузка оператора >="""
        if self.faculty != other.faculty:
            return self.faculty >= other.faculty
        if self.surname != other.surname:
            return self.surname >= other.surname
        if self.name != other.name:
            return self.name >= other.name
        if self.patronymic != other.patronymic:
            return self.patronymic >= other.patronymic
        if self.degree != other.degree:
            return self.degree >= other.degree
        return self.rank >= other.rank

    def __le__(self, other):
        """Перегрузка оператора <="""
        if self.faculty != other.faculty:
            return self.faculty <= other.faculty
        if self.surname != other.surname:
            return self.surname <= other.surname
        if self.name != other.name:
            return self.name <= other.name
        if self.patronymic != other.patronymic:
            return self.patronymic <= other.patronymic
        if self.degree != other.degree:
            return self.degree <= other.degree
        return self.rank <= other.rank

"""Запись сгенерированных данных в файл MS Excel"""
# with pd.ExcelWriter("./sets.xlsx") as writer:
#     for i in sizes:
#         pd.DataFrame(generate(i)).to_excel(writer, sheet_name=f"{i}", index=False)

"""Считывание входных данных из файла MS Excel и запись в словарь"""
teachers = {}
for i in sizes:
    temp = pd.read_excel('./sets.xlsx', sheet_name=f"{i}").to_dict('records')
    teachers[i] = [Teacher(t['Фамилия'], t['Имя'], t['Отчество'], t['Факультет'], t['Учёная степень'], t['Учёное звание']) for t in temp]

collisions_all = []
collisions_simple_all = []
for i in sizes:
    #faculties = [k.faculty for k in teachers[i]]
    collisions = 0
    collisions_simple = 0
    table = {}
    table_simple = {}
    """Создание хэш-таблицы методом цепочек"""
    for j in range(i):
        hash_value_simple = teachers[i][j].hash_simple
        hash_value = teachers[i][j].hash

        #добавление в сложную хэш-таблицу
        if hash_value not in table:
            table[hash_value] = [teachers[i][j]]
        else:
            for k in table[hash_value]:
                if teachers[i][j].surname == k.surname:
                    break
            else:
                collisions += 1
            table[hash_value].append(teachers[i][j])

        #добавление в простую хэш-таблицу
        if hash_value_simple not in table_simple:
            table_simple[hash_value_simple] = [teachers[i][j]]
        else:
            for k in table_simple[hash_value_simple]:
                if teachers[i][j].surname == k.surname:
                    break
            else:
                collisions_simple += 1
            table_simple[hash_value_simple].append(teachers[i][j])

    collisions_all.append(collisions)
    collisions_simple_all.append(collisions_simple)

    """Поиск в хэш таблице"""
    key = teachers[i][random.randint(0, i - 1)].surname

    #Поиск в сложной
    starttime = timeit.default_timer()
    hash_value = calculate_hash(key)  # Вычисляем хэш ключа для поиска
    if hash_value in table:
        items = table[hash_value]
        for item in items:
            if item.surname == key:
                print(item)
                break
    else:
        print("None")
    end = timeit.default_timer() - starttime
    time_difficulty.append(end)

    #Поиск в простой
    starttime = timeit.default_timer()
    hash_value_simple = calculate_hash_simple(key)  # Вычисляем хэш ключа для поиска
    if hash_value_simple in table_simple:
        items = table_simple[hash_value_simple]
        for item in items:
            if item.surname == key:
                print(item)
                break
    else:
        print("None")
    end = timeit.default_timer() - starttime
    time_simple.append(end)

print(collisions_simple_all)
print(f'time_simple = {time_simple}')
print(collisions_all)
print(f'time_difficulty = {time_difficulty}')
