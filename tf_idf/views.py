import docx
import re
from django.shortcuts import render, redirect
import uuid
from tf_idf.forms import LoadFileForm
import random


def get_tf_idf(arr: list[str]) -> list:
    """
    Преобразовываем список из слов в список из словаря из уникальных слов (unic_words), tf и random_idf.
    Так как в задании непонятно значение понятия 'коллекция', взято случайное значение от 0,01 до 1
    """

    try:
        total_words = len(arr)
        unic_words = dict.fromkeys(arr)
        result = list()
        for word in unic_words:
            tf = arr.count(word) / total_words
            random_idf = random.randint(1, 100) / 100
            result.append(dict(name=word, tf=tf, idf=random_idf))
        return result
    except Exception as ex:
        print(ex)


def get_name(name):
    """Получаем полное имя для сохранения. Используем uuid для уникальности"""

    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())
    return f"{name}_{suffix}{ext}"


def handle_uploaded_file(f, name):
    """Открываем и сохраняем файл по частям"""

    with open(f"uploaded_files/{name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def good_func(name):
    """Открываем файл, читаем содержимое и сохраняем слова в список, убирая все лишнее"""

    # Получаем формат файла, ниже обрататываем .txt и .doc
    ext = name[name.rindex('.'):]
    try:
        if ext == '.txt':
            with open(f"uploaded_files/{name}", "r", encoding='utf-8') as file:
                text = file.read().replace('\n', ' ').lower()
                reg = re.compile('[^a-zA-Zа-яА-Я ]')
                return list(filter(lambda x: x.isalpha(), reg.sub('', text).split(' ')))
        elif ext in ['.docx', '.doc']:
            doc = docx.Document(f"uploaded_files/{name}")
            text_list = []
            for paragraph in doc.paragraphs:
                text_list.append(paragraph.text.lower())
            clear_text = re.sub(r'[^\w\s]', '', ' '.join(text_list))
            return list(filter(lambda x: x.isalpha(), clear_text.split(' ')))
        else:
            raise 'Программа работает только с форматами .txt, .docx, .doc'
    except Exception as ex:
        print(ex)


def load_file(request):
    if request.method == 'POST':
        form = LoadFileForm(request.POST, request.FILES)
        if form.is_valid():
            name = get_name(form.cleaned_data['file'].name)
            handle_uploaded_file(form.cleaned_data['file'], name)
            return redirect('show_words', name)
    else:
        form = LoadFileForm()
    return render(request, 'tf_idf/load_file.html', context={'form': form})


def show_words(request, name):
    list_words = good_func(name)
    result = get_tf_idf(list_words)
    sorted_result = sorted(result, key=lambda x: x['idf'])
    return render(request, 'tf_idf/show_words.html', context={'result': sorted_result})
