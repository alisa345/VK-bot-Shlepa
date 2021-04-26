# -*- coding: utf-8 -*-
import json
import os
import random
from random import randint
from urllib.request import urlopen

import requests
import vk_api
from PIL import Image
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from nim import Nim

COUNTRIES = ['Мавритания', 'Монтсеррат', 'Мальта', 'Маврикий', 'Мальдивы', 'Малави', 'Мексика', 'Малайзия', 'Мозамбик',
             'Намибия', 'Новая Каледония', 'Нигер', 'Остров Норфолк', 'Нигерия', 'Никарагуа', 'Нидерланды', 'Норвегия',
             'Непал', 'Науру', 'Ниуэ', 'Новая Зеландия', 'Оман', 'Панама', 'Перу', 'Французская Полинезия',
             'Папуа-Новая Гвинея', 'Филиппины', 'Пакистан', 'Польша', 'Сент-Пьер и Микелон', 'Питкерн', 'Пуэрто-Рико',
             'Палестина', 'Португалия', 'Палау', 'Парагвай', 'Катар', 'Реюньон', 'Румыния', 'Сербия', 'Россия',
             'Руанда', 'Саудовская Аравия', 'Соломоновы острова', 'Сейшелы', 'Судан', 'Швеция', 'Сингапур', 'Словения',
             'Украина', 'Чад']

NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

first_kb = [["а", "б", "в"], ["г", "д", "е"], ["ж", "з", "и"], ["й", "к", "л"]]
two_kb = [["м", "н", "о"], ["п", "р", "с"], ["т", "у", "ф"], ["х", "ц", "ч"]]
three_kb = [["ш", "щ", "ъ"], ["ь", "э", "ю"], ["я"]]

quest_flag = 'Флаг чьей страны изображен?'
quest_text = 'Викторина состоит из 10 вопросов.\nНапишите "СТОП", чтобы закончить.'

token = ''  # токен сообщества
id_group = 0  # id сообщества

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, id_group)


def next_keyboard(kb_nm, symbol, ev):
    if kb_nm == 1:
        keyboard = keyboard_gallows1
    elif kb_nm == 2:
        keyboard = keyboard_gallows2
    else:
        keyboard = keyboard_gallows3
    if symbol == '>' and kb_nm < 3:
        kb_nm += 1
        if kb_nm == 2:
            write_message(ev.obj.message['from_id'], "Клавиатура обновлена", keyboard_gallows2)
        else:
            write_message(ev.obj.message['from_id'], "Клавиатура обновлена", keyboard_gallows3)
    elif symbol == '<' and kb_nm > 1:
        kb_nm -= 1
        if kb_nm == 2:
            write_message(ev.obj.message['from_id'], "Клавиатура обновлена", keyboard_gallows2)
        else:
            write_message(ev.obj.message['from_id'], "Клавиатура обновлена", keyboard_gallows1)
    else:
        write_message(ev.obj.message['from_id'], "Не удалось обновить клавиатуру", keyboard)
    return kb_nm


# создание клавиатур с буквами
def generate_keyboard(kb):
    num = 4
    if kb == keyboard_gallows3:
        num = 3
    for i in range(num):
        for j in range(3):
            if kb == keyboard_gallows1:
                kb.add_button(first_kb[i][j], color=VkKeyboardColor.SECONDARY)
            elif kb == keyboard_gallows2:
                kb.add_button(two_kb[i][j], color=VkKeyboardColor.SECONDARY)
            else:
                if (i != 2) or (i == 2 and j == 0):
                    kb.add_button(three_kb[i][j], color=VkKeyboardColor.SECONDARY)
        kb.add_line()
    kb.add_button('<', color=VkKeyboardColor.PRIMARY)
    kb.add_button('СТОП', color=VkKeyboardColor.NEGATIVE)
    kb.add_button('>', color=VkKeyboardColor.PRIMARY)


def upgrade_keyboard():
    generate_keyboard(keyboard_gallows1)
    generate_keyboard(keyboard_gallows2)
    generate_keyboard(keyboard_gallows3)


# основная клавиатура
keyboard_main = VkKeyboard(one_time=True)
keyboard_main.add_button('Что? Где? Когда?', color=VkKeyboardColor.PRIMARY)
keyboard_main.add_button('Викторина по флагам', color=VkKeyboardColor.PRIMARY)
keyboard_main.add_line()
keyboard_main.add_button('Анекдоты', color=VkKeyboardColor.PRIMARY)
keyboard_main.add_button('Виселица', color=VkKeyboardColor.PRIMARY)
keyboard_main.add_line()
keyboard_main.add_button('Быки и коровы', color=VkKeyboardColor.PRIMARY)
keyboard_main.add_button('Случайная картинка', color=VkKeyboardColor.PRIMARY)
keyboard_main.add_line()
keyboard_main.add_button('Ним', color=VkKeyboardColor.PRIMARY)

# клавиатура для чгк и викторины
keyboard_question = VkKeyboard(one_time=True)
keyboard_question.add_button('Ответ', color=VkKeyboardColor.POSITIVE)
keyboard_question.add_button('Дальше', color=VkKeyboardColor.SECONDARY)
keyboard_question.add_button('СТОП', color=VkKeyboardColor.NEGATIVE)

# клавиатура с буквами для виселицы
keyboard_gallows1 = VkKeyboard(one_time=True)
keyboard_gallows2 = VkKeyboard(one_time=True)
keyboard_gallows3 = VkKeyboard(one_time=True)

# клавиатура для быков и коров
keyboard_bulls_cows = VkKeyboard(one_time=True)
keyboard_bulls_cows.add_button('Новая игра', color=VkKeyboardColor.POSITIVE)
keyboard_bulls_cows.add_button('СТОП', color=VkKeyboardColor.NEGATIVE)

# клавиатура для нима
keyboard_nim = VkKeyboard(one_time=True)
keyboard_nim.add_button('СТОП', color=VkKeyboardColor.NEGATIVE)

upgrade_keyboard()


def write_message(user_id, msg_txt, keybrd=keyboard_main, attachment=False):
    if attachment is False:
        vk.messages.send(
            user_id=user_id,
            keyboard=keybrd.get_keyboard(),
            message=msg_txt,
            random_id=random.randint(0, 2 ** 64))
    else:
        vk.messages.send(
            user_id=user_id,
            keyboard=keybrd.get_keyboard(),
            attachment=attachment,
            message=msg_txt,
            random_id=random.randint(0, 2 ** 64)
        )


# проверка для быков и коров
def repeat_letter(line):
    for el in line:
        if line.count(el) > 1:
            return False
    return True


# рандомное слово для виселицы
def random_word():
    with open('data/words.json', encoding="utf8") as file:
        data = json.load(file)

    theme, theme_list = random.choice(list(data.items()))
    word = random.choice(theme_list)
    return theme, word


# рандомная картинка
def random_pic():
    url = 'https://picsum.photos/960/720'
    image = Image.open(urlopen(url))
    image.save('data/img/random_pic.png')
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages('data/img/random_pic.png')
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = 'photo' + str(owner_id) + '_' + str(photo_id) + '_' + str(access_key)
    os.remove("data/img/random_pic.png")
    return attachment


# создание вариантов для викторины
def variants_to_line(var_list):
    line = ''
    for i in range(len(var_list)):
        line += str(i + 1) + ') ' + COUNTRIES[var_list[i]] + '\n'
    return line


# рандомная шутка
def get_joke():
    response = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=1')
    joke = response.text.replace('\r', '').split('{"content":"')[1][:-3]
    return joke


# виселица
def gallows(word, letter, wrd_list):
    change = False
    if letter in word:
        change = True
        for i in range(len(word)):
            if word[i] == letter:
                wrd_list[i] = letter
    return change, wrd_list


# быки и коровы
def bulls_and_cows(user_num, right_num):
    win = False
    bulls, cows = 0, 0
    for i in range(4):
        if int(user_num[i]) == right_num[i]:
            bulls += 1
        elif int(user_num[i]) in right_num:
            cows += 1
    if bulls == 0:
        line = '0 быков, '
    elif bulls == 1:
        line = '1 бык, '
    else:
        line = str(bulls) + ' быка, '
        if bulls == 4:
            win = True
    if cows == 0:
        line += '0 коров'
    elif cows == 1:
        line += '1 корова'
    else:
        line += str(cows) + ' коровы'
    return line, win


# викторина флагов
def country_quiz(count_list):
    country = 'line'
    while country not in count_list:
        country = random.choice(COUNTRIES)
    count_id = COUNTRIES.index(country)
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages('data/img/' + str(count_id) + '.png')
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = 'photo' + str(owner_id) + '_' + str(photo_id) + '_' + str(access_key)
    answer_options = [count_id]
    while len(answer_options) != 4:
        elem = random.randint(0, 50)
        if elem not in answer_options:
            answer_options.append(elem)
    random.shuffle(answer_options)
    return count_id, answer_options, attachment


# чгк
def what_where_when():
    www_list = []
    url = 'https://db.chgk.info/random/types1/1675321037'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all('div', class_='random-results')
    for item in results:
        txt = item.text.split('\n')
        for elem in txt:
            if elem != '' and elem != '...':
                www_list.append(elem)
    www_list = www_list[1:]
    question, answer, comment = '', '', ''
    quest, comm = True, False
    for elem in www_list:
        if 'Вопрос 1:' in elem:
            question += elem[9:] + ' '
            quest = True
        elif 'Ответ:' in elem:
            answer = elem[6:]
            quest = False
            continue
        elif quest:
            question += elem + ' '
            continue
        if 'Комментарий:' in elem:
            comment = elem[12:]
            comm = True
        elif quest is False and comm is False:
            break
        elif comm and 'Источник' not in elem:
            comment += ' ' + elem
        else:
            comm = False
    return question.strip(' '), answer.strip(' ').rstrip('.'), comment.strip(' ')


def main():
    www = False
    quiz = False
    gallows_flag = False
    bulls_cows = False
    nim_flag = False

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            request = event.obj.message['text'].lower()
            if www:
                if request == 'ответ':
                    write_message(event.obj.message['from_id'], answer, keyboard_question)
                    if comm:
                        write_message(event.obj.message['from_id'], comm, keyboard_question)
                    quest, answer, comm = what_where_when()
                    write_message(event.obj.message['from_id'], quest, keyboard_question)
                elif request == 'дальше':
                    quest, answer, comm = what_where_when()
                    write_message(event.obj.message['from_id'], quest, keyboard_question)
                elif request == 'стоп':
                    write_message(event.obj.message['from_id'], "Что дальше?")
                    www = False
                else:
                    if request == answer.lower():
                        write_message(event.obj.message['from_id'], 'Правильный ответ!', keyboard_question)
                        quest, answer, comm = what_where_when()
                        write_message(event.obj.message['from_id'], quest, keyboard_question)
                    else:
                        write_message(event.obj.message['from_id'], 'Что-то не то.\nНапишите "СТОП", чтобы закончить.',
                                      keyboard_question)
            elif quiz:
                if request == 'ответ':
                    write_message(event.obj.message['from_id'], COUNTRIES[answer_cnt_id], keyboard_question)
                elif request == 'дальше':
                    pass
                elif request == 'стоп':
                    write_message(event.obj.message['from_id'], "Что дальше?")
                    quiz = False
                    continue
                else:
                    if request == COUNTRIES[answer_cnt_id].lower() or request == str(variants.index(answer_cnt_id) + 1):
                        write_message(event.obj.message['from_id'], 'Правильный ответ!', keyboard_question)
                        correct_answers += 1
                    else:
                        write_message(event.obj.message['from_id'],
                                      'Неправильный ответ\nОтвет: ' + COUNTRIES[answer_cnt_id], keyboard_question)
                if counter < 10:
                    count_list.remove(COUNTRIES[answer_cnt_id])
                    answer_cnt_id, variants, attachment = country_quiz(count_list)
                    write_message(event.obj.message['from_id'], quest_flag, keyboard_question, attachment)
                    write_message(event.obj.message['from_id'], variants_to_line(variants), keyboard_question)
                    counter += 1
                else:
                    quiz = False
                    ln = "Результаты викторины: " + str(correct_answers) + "/10"
                    write_message(event.obj.message['from_id'], ln + '\nЧто дальше?')
            elif gallows_flag:
                if request == 'стоп':
                    write_message(event.obj.message['from_id'], "Что дальше?")
                    gallows_flag = False
                    continue
                elif request == '<' or request == '>':
                    kb_num = next_keyboard(kb_num, request, event)
                else:
                    result, word_list = gallows(word_gallows, request, word_list)
                    if result:
                        write_message(event.obj.message['from_id'], "Эта буква есть в слове!", keyboard_gallows1)
                        line = 'Тема: ' + theme + '\nСлово: ' + ' '.join(word_list) + '\nЖизней: ' + '<3 ' * lives
                        write_message(event.obj.message['from_id'], line, keyboard_gallows1)
                        kb_num = 1
                    else:
                        write_message(event.obj.message['from_id'], "Буквы нет в слове!", keyboard_gallows1)
                        lives -= 1
                        line = 'Тема: ' + theme + '\nСлово: ' + ' '.join(word_list) + '\nЖизней: ' + '<3 ' * lives
                        write_message(event.obj.message['from_id'], line, keyboard_gallows1)
                        kb_num = 1
                    if '_' not in word_list:
                        write_message(event.obj.message['from_id'], "Вы победили!")
                        gallows_flag = False
                    if lives == 0:
                        write_message(event.obj.message['from_id'], "Вы проиграли!")
                        gallows_flag = False
            elif bulls_cows:
                if request == 'стоп':
                    write_message(event.obj.message['from_id'], "Что дальше?")
                    bulls_cows = False
                    continue
                elif request == 'новая игра':
                    moves = 0
                    nm_cows_bulls = NUMBERS[:]
                    random.shuffle(nm_cows_bulls)
                    nm_cows_bulls = nm_cows_bulls[:4]
                    write_message(event.obj.message['from_id'], "Найди число, задуманное шлёпой", keyboard_bulls_cows)
                else:
                    if request.isdigit() and len(request) == 4 and repeat_letter(request):
                        pass
                    elif request.isdigit() is False or len(request) != 4:
                        write_message(event.obj.message['from_id'], 'Ход - четырехзначное число', keyboard_bulls_cows)
                        continue
                    elif repeat_letter(request) is False:
                        write_message(event.obj.message['from_id'], 'Цифры не должны повторяться', keyboard_bulls_cows)
                        continue
                    line, win = bulls_and_cows(list(request), nm_cows_bulls)
                    write_message(event.obj.message['from_id'], line, keyboard_bulls_cows)
                    moves += 1
                    if win:
                        write_message(event.obj.message['from_id'], 'Мууу! Победа!\nХодов: ' + str(moves))
                        bulls_cows = False
            elif nim_flag:
                if request == 'стоп':
                    write_message(event.obj.message['from_id'], "Что дальше?")
                    nim_flag = False
                    continue
                elif num_stones:
                    if request == '1' or request == '2' or request == '3':
                        nm_stones = request
                        write_message(event.obj.message['from_id'], 'Введите кол-во забираемых камней', keyboard_nim)
                        num_stones = False
                    else:
                        write_message(event.obj.message['from_id'], 'Введите номер кучи', keyboard_nim)
                else:
                    play_mv = request
                    if play_mv.isdigit() is False:
                        write_message(event.obj.message['from_id'], 'Введите кол-во забираемых камней', keyboard_nim)
                        continue
                    if ((nm_stones == '1' and int(play_mv) <= nim_play.get_stones1()) or
                        (nm_stones == '2' and int(play_mv) <= nim_play.get_stones2()) or
                        (nm_stones == '3' and int(play_mv) <= nim_play.get_stones3())) and int(play_mv) > 0:
                        pass
                    else:
                        write_message(event.obj.message['from_id'], 'Введите кол-во забираемых камней', keyboard_nim)
                        continue
                    end, ln1, ln2 = nim_play.play(int(nm_stones), int(play_mv))
                    write_message(event.obj.message['from_id'], ln1, keyboard_nim)
                    write_message(event.obj.message['from_id'], ln2, keyboard_nim)
                    if end:
                        write_message(event.obj.message['from_id'], 'ЧЕЛОВЕК ПОБЕДИЛ!')
                        nim_flag = False
                        continue
                    end, ln1, ln2 = nim_play.play()
                    write_message(event.obj.message['from_id'], ln1, keyboard_nim)
                    write_message(event.obj.message['from_id'], ln2, keyboard_nim)
                    if end:
                        write_message(event.obj.message['from_id'], 'ШЛЁПА ПОБЕДИЛ!')
                        nim_flag = False
                        continue
                    num_stones = True
                    write_message(event.obj.message['from_id'], 'Введите номер кучи', keyboard_nim)
            else:
                if request == 'привет':
                    write_message(event.obj.message['from_id'], "Привет!")
                elif request == 'пока':
                    write_message(event.obj.message['from_id'], "До встречи")
                elif request == 'анекдоты':
                    write_message(event.obj.message['from_id'], get_joke())
                elif request == 'случайная картинка':
                    write_message(event.obj.message['from_id'], "Держи", keyboard_main, random_pic())
                elif request == 'ним':
                    st1, st2, st3 = randint(5, 20), randint(5, 20), randint(5, 20)
                    nim_play = Nim(st1, st2, st3)
                    ln = 'Кол-во камней в первой куче: ' + str(st1) + '\nКол-во камней во второй куче: ' + str(st2) \
                         + '\nКол-во камней в третьей куче: ' + str(st3)
                    write_message(event.obj.message['from_id'], ln, keyboard_nim)
                    end, ln1, ln2 = nim_play.play()
                    write_message(event.obj.message['from_id'], ln1, keyboard_nim)
                    write_message(event.obj.message['from_id'], ln2, keyboard_nim)
                    nim_flag, num_stones = True, True
                    write_message(event.obj.message['from_id'], 'Введите номер кучи', keyboard_nim)
                    nm_stones, play_mv = 0, 0
                elif request == 'быки и коровы':
                    moves = 0
                    nm_cows_bulls = NUMBERS[:]
                    random.shuffle(nm_cows_bulls)
                    nm_cows_bulls = nm_cows_bulls[:4]
                    write_message(event.obj.message['from_id'], "Найди число, задуманное шлёпой", keyboard_bulls_cows)
                    bulls_cows = True
                elif request == 'виселица':
                    theme, word_gallows = random_word()
                    word_list = ['_'] * len(word_gallows)
                    lives = 10
                    line = 'Тема: ' + theme + '\nСлово: ' + ' '.join(word_list) + '\nЖизней: ' + '<3 ' * lives
                    kb_num = 1
                    write_message(event.obj.message['from_id'], line, keyboard_gallows1)
                    gallows_flag = True
                elif request == 'что? где? когда?' or request == 'чгк':
                    www = True
                    quest, answer, comm = what_where_when()
                    write_message(event.obj.message['from_id'], quest, keyboard_question)
                elif request == 'викторина по флагам':
                    quiz = True
                    count_list = COUNTRIES[:]
                    counter, correct_answers = 1, 0
                    answer_cnt_id, variants, attachment = country_quiz(count_list)
                    write_message(event.obj.message['from_id'], quest_text, keyboard_question)
                    write_message(event.obj.message['from_id'], quest_flag, keyboard_question, attachment)
                    write_message(event.obj.message['from_id'], variants_to_line(variants), keyboard_question)
                else:
                    write_message(event.obj.message['from_id'], "Сложно! Я же просто кот")


if __name__ == '__main__':
    main()
