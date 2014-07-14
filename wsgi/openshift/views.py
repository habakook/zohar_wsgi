# -*- coding: utf-8 -*-
from django.shortcuts import render
import os
import re
import io
import sys
import unicodedata


ALEPHBET = u'[אבגדהוזחטיכךלמםנןסעפףצץקרשתﭏ]'

def index(request):
    debug = []
    debug2= []
    found_verses = []
    count = 0
    filter = request.GET.get('filter')
    value = request.GET.get('criteria', '').strip()
    title_lib1 = request.GET.get('title_lib1', '')
    title_lib2 = request.GET.get('title_lib2', '')
    lib = request.GET.get('library', '')
    book=''
    docs=1
    
    if lib != '':
        main_lib = True if lib=='lib1' else False 
    
    #remove BOM
    if title_lib1.startswith(u'\ufeff'):
        title_lib1 = title_lib1[1:]
    
    if value != '':
        found_verses = search(value, main_lib, filter)
        count = len(found_verses)
    elif title_lib1 != '':
        docs = list_of_resources(True)
        debug, book = get_book(docs,title_lib1)
    elif title_lib2 != '':
        docs = list_of_resources(False)
        debug, book = get_book(docs,title_lib2)
    
    context = {'found_verses':found_verses, 'count':count, 'value':value, 'master_map':MASTER_MAP, 'book':book, 'debug':debug, 'debug2':debug2}
    return render(request, 'zohar/main.html', context)

def get_book(docs,title):
    debug = []
    book=[]
    pattern = re.compile(ALEPHBET, re.UNICODE)
    title = unicodedata.normalize('NFC', title)
    for doc in docs:
        with io.open(doc, 'r', encoding='utf-8-sig') as doc:
            
            for line in doc:
                if title != line.strip():
                    break
                else:
                    
                    modified_title = '<h2 id="title">{0}</h2>'.format(title.encode('utf-8-sig'))
                    book.append(modified_title)
                    
                    for l in doc:
                        
                        found = pattern.search(l)
                        if found:
                            l = pattern.sub('<span xml:lang="he" lang="he" class="ezra">'+'\g<0>'+'</span>',l)
                        book.append(l)
    
    return debug, book

def search(words, main_lib, filter):
    verse_list = []
    key_words = []
    
    docs = list_of_resources(main_lib)
    which_lib = 'title_lib1' if main_lib else 'title_lib2'
    
    if filter == 'filter_1':
        key_words.append(words)
    else:
        key_words = words.split()
    
    if len(key_words)==1:
        pattern = set_pattern(key_words[0], filter)
    
    for doc in docs:
        with io.open(doc, 'r', encoding='utf-8-sig') as doc:
            
            get_title = True
            for line in doc:
                if get_title:
                    title = line
                    get_title = False
                    #ind = which_book(title)
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
                    verse_list.append('<a href="/zohar/?'+which_lib+'='+title+'"><b>'+title+'</b></a></br>'+line)
    
    return verse_list

def which_book(title):
    i = 0
    for book in RESOURCES_2:
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

def list_of_resources(main_lib=True):
    res = []
    
    if main_lib:
        docs_dir = os.path.join(os.path.dirname(__file__),'lib1')
    else:
        docs_dir = os.path.join(os.path.dirname(__file__),'lib2')
    
    for doc in os.listdir(docs_dir):
        if not doc.startswith('.'):
            res.append(os.path.join(docs_dir,doc))
    
    return res

MASTER_MAP = [('בְּרֵאשִׁית',	'Берешит', ['Зоhар Брейшит I','Зоhар Брейшит II'],['Зоhар Брейшит I','Зоhар Брейшит II','Зоhар Брейшит III']),
              ('נֹחַ	', 'Ноах', ['Зоhар Ноах'],['Зоhар Ноах']),
              ('לֶךְ-לְךָ	', 'Лех Леха', ['Зоhар Лех Леха'],['Зоhар Лех Леха']),
              ('וַיֵּרָא	', 'Ва-Иера', ['Зоhар Ва-йера'],['Зоhар Ва-йера']),
              ('חַיֵּי שָׂרָה	', 'Хайей Сара', ['Зоhар Хайей Сара'],['Зоhар Хайей Сара']),
              ('תּוֹלְדֹת	', 'Толдот', ['Зоhар Толдот'],['Зоhар Толдот']),
              ('וַיֵּצֵא	', 'Ва-Иеце', ['Зоhар Ва-йеце'],['Зоhар Ваеце']),
              ('וַיִּשְׁלַח	', 'Ва-Йишлах', ['Зоhар Ва-йишлах'],['Зоhар Ваишлах']),
              ('וַיֵּשֶׁב	', 'Ва-Иешев', ['﻿Зоhар Ва-йешев'],['Зоhар Вейшев']),
              ('מִקֵּץ	', 'Ми-Кец', ['Зоhар Ми-кец'],['Зоhар Микец']),
              ('וַיִּגַּשׁ	', 'Ва-Йиггаш', [],['Зоhар Ваигаш']),
              ('וַיְחִי	', 'Ва-Иехи', [],['Зоhар Ваехи I','Зоhар Ваехи II','Зоhар Ваехи III']),
              ('שְׁמוֹת	', 'Шмот', [],['Зоhар Шемот']),
              ('וָאֵרָא	', 'Ва-Эра', [],['Зоhар Ва-Эра']),
              ('בֹּא	', 'Бо', [],['Зоhар Бо']),
              ('בְּשַׁלַּח	', 'Бе-Шаллах', [],['Зоhар Бешалах']),
              ('יִתְרוֹ	', 'Итро', [],['Зоhар Итро I','Зоhар Итро II','Зоhар Итро III']),
              ('מִשְׁפָּטִים	', 'Мишпатим', [],['Зоhар Мишпатим I','Зоhар Мишпатим II']),
              ('תְּרוּמָה	', 'Трума', [],['Зоhар Трума I','Зоhар Трума II']),
              ('תְּצַוֶּה	', 'Тецавве', [],['Зоhар Тецаве']),
              ('כִּי תִשָּׂא	', 'Ки Тисса', [],['Зоhар Ки Тиса']),
              ('וַיַּקְהֵל	', 'Ва-Якхел', [],['Зоhар Ваикаэль']),
              ('פְּקוּדֵי	', 'Пкудей', [],['Зоhар Пкудей']),
              ('וַיִּקְרָא	', 'Ва-Йикра', [],['Зоhар Ваикра']),
              ('צַו	', 'Цав', [],['Зоhар Цав I','Зоhар Цав II']),
              ('שְׁמִינִי	', 'Шмини', [],['Зоhар Шмини']),
              ('תַּזְרִיעַ	 ', 'Тазриа', [],['Зоhар Тазриа']),
              ('מְצֹרָע	', 'Мецора', [],[ 'Зоhар Мецора']),
              ('אַחֲרֵי מוֹת	', 'Ахарей Мот', [],[]),
              ('קְדֹשִׁים	', 'Кдошим', [],[]),
              ('אֱמֹר	', 'Эмор', [],[]),
              ('בְּהַר	', 'Бе-Хар', [],['Зоhар Беhар']),
              ('בְּחֻקֹּתַי	', 'Бе-Хукотай', [],['Зоhар Бехукотай']),
              ('בְּמִדְבַּר	', 'Бе-Мидбар', [],['Зоhар Бемидбар']),
              ('נָשֹׂא	', 'Насо', [],[]),
              ('בְּהַעֲלֹתְךָ	 ', 'Бе-Хаалотха', [],['Зоhар Беhаалотеха']),
              ('שְׁלַח-לְךָ	 ', 'Шлах Леха', [],[]),
              ('קֹרַח	', 'Корах', [],['Зоhар Корах']),
              ('חֻקַּת	', 'Хукат', [],['Зоhар Хукат']),
              ('בָּלָק	', 'Балак', [],[]),
              ('פִּינְחָס	', 'Пинхас', [],[]),
              ('מַטּוֹת	', 'Матот', [],[]),
              ('מַסְעֵי	', 'Масей', [],[]),
              ('דְּבָרִים	', 'Дварим', [],[]),
              ('וָאֶתְחַנַּן	', 'Ва-Этханан', [],[]),
              ('עֵקֶב	', 'Экев', [],['Зоhар Экев']),
              ('רְאֵה	', 'Реэ', [],[]),
              ('שֹׁפְטִים	', 'Шофтим', [],['Зоhар Шофтим']),
              ('כִּי תֵצֵא	', 'Ки Теце', [],[]),
              ('כִּי תָבוֹא	', 'Ки Таво', [],[]),
              ('נִצָּבִים	', 'Ниццавим', [],[]),
              ('וַיֵּלֶך	', 'Ва-Иелех', [],[]),
              ('הַאֲזִינוּ	', 'Хаазину', [],[]),
              ('וְזֹאת הַבְּרָכָה	', 'Ве-Зот ха-браха', [],[])]

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


RESOURCES_2 = ['Зоhар Корах',
               'Зоhар Акдамат I',
               'Зоhар Акдамат II',
               'Зоhар Беhаалотеха',
               'Зоhар Беhар',
               'Зоhар Бемидбар',
               'Зоhар Бехукотай',
               'Зоhар Бешалах',
               'Зоhар Бо',
               'Зоhар Брейшит I',
               'Зоhар Брейшит II',
               'Зоhар Брейшит III',
               'Зоhар Ва-йера',
               'Зоhар Ваехи I',
               'Зоhар Ваехи II',
               'Зоhар Ваехи III',
               'Зоhар Ваеце',
               'Зоhар Ваигаш',
               'Зоhар Ваикаэль',
               'Зоhар Ваикра',
               'Зоhар Ваишлах',
               'Зоhар Вейшев',
               'Зоhар Ки Тиса',
               'Зоhар Корах',
               'Зоhар Лех Леха',
               'Зоhар Мецора',
               'Зоhар Микец',
               'Зоhар Мишпатим I',
               'Зоhар Мишпатим II',
               'Зоhар Ноах',
               'Зоhар Пкудей',
               'Зоhар Тазриа',
               'Зоhар Тецаве',
               'Зоhар Толдот',
               'Зоhар Трума I',
               'Зоhар Трума II',
               'Зоhар Хайей Сара',
               'Зоhар Хукат',
               'Зоhар Цав I',
               'Зоhар Цав II',
               'Зоhар Шемот',
               'Зоhар Шмини',
               'Зоhар Шофтим',
               'Зоhар Экев']
"""
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
"""