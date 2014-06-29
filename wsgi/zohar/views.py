# -*- coding: utf-8 -*-
from django.shortcuts import render
import os
import re
import io
import sys

RESOURCES = ['Сефер Ецира',
            'Бахир',
            '﻿Зоhар hакдама',
            'Зоhар Брейшит I',
            'Зоhар Брейшит II',
            'Зоhар Ноах',
            'Зоhар Лех Леха',
            'Зоhар Ва-йера',
            'Зоhар Хайей Сара',
            'Зоhар Толдот',
            'Зоhар Ва-йеце',
            'Зоhар Ва-йишлах',
            '﻿Зоhар Ва-йешев',
            'Зоhар Ми-кец']

ALEPHBET = u'[אבגדהוזחטיכךלמםנןסעפףצץקרשתﭏ]'

def index(request):
    debug = []
    found_verses = []
    count = 0
    filter = request.GET.get('filter')
    value = request.GET.get('criteria', '').strip()
    
    if value != '':
        found_verses = search(value, filter)
        count = len(found_verses)
    
    context = {'what': RESOURCES, 'found_verses': found_verses, 'count': count, 'value': value}
    return render(request, 'zohar/main.html', context)


def book(request, book_number):
    debug = 0
    debug2 = []
    book = []
    title = RESOURCES[int(book_number)-1]
    
    docs = list_of_resources()
    pattern = re.compile(ALEPHBET, re.UNICODE)
    
    for doc in docs:
        with io.open(os.path.join(os.path.dirname(__file__),'res','{0}').format(doc), 'r', encoding='utf-8-sig') as doc:  
            
            for line in doc:
                if title.decode('utf-8-sig') != line.strip():
                    break
                else:
                    modified_title = '<h2 id="title">{0}</h2>'.format(title)
                    book.append(modified_title)
                    
                    for l in doc:
                        found = pattern.search(l)
                        if found:
                            l = pattern.sub('<span xml:lang="he" lang="he" class="ezra">'+'\g<0>'+'</span>',l)
                        book.append(l)
    
    context = {'book':book, 'debug':debug, 'debug2':debug2}
    return render(request, 'zohar/book.html', context)


def search(words, filter):
    verse_list = []
    key_words = []
    
    if filter == 'filter_1':
        key_words.append(words)
    else:
        key_words = words.split()
    
    docs = list_of_resources()
    
    if len(key_words)==1:
        pattern = set_pattern(key_words[0], filter)
    
    for doc in docs:
        with io.open(os.path.join(os.path.dirname(__file__),'res','{0}').format(doc), 'r', encoding='utf-8-sig') as doc:
            
            get_title = True
            for line in doc:
                if get_title:
                    title = line
                    get_title = False
                    ind = which_book(title)
                    continue
                
                if len(key_words)>1:
                    for word in key_words:
                        pattern = set_pattern(word, filter)
                        found = pattern.search(line)
                        if not found and filter != 'filter_2':
                            break
                        elif found and filter == 'filter_2':
                            break
                else:
                    found = pattern.search(line)
                
                if found:
                    for word in key_words:
                        pattern = set_pattern(word, filter)
                        line = pattern.sub('<span class="highlightme">'+'\g<0>'+'</span>',line)
                    verse_list.append('<a href="/zohar/'+ind+'"><b>'+title+'</b></a></br>'+line)
    
    return verse_list

def which_book(title):
    i = 0
    for book in RESOURCES:
        i += 1
        if book.decode('utf-8-sig') == title.strip():
            return str(i)

def set_pattern(key, filter):
    if filter == 'filter_1' or filter == 'filter_2':
        pattern = re.compile(key, re.I|re.UNICODE)
    elif filter == 'filter_3':
        pattern = re.compile(key, re.UNICODE)
    elif filter == 'filter_4':
        pattern = re.compile(ur'\b{0}\b'.format(key), re.I|re.UNICODE)
    else:
        pattern = re.compile(key, re.I|re.UNICODE)
    return pattern


def list_of_resources():
    res = []
    docs_dir = os.path.join(os.path.dirname(__file__),'res')
    for doc in os.listdir(docs_dir):
        if not doc.startswith('.'):
            res.append(doc)
    return res