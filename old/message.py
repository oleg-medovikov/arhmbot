import time 

def get_hello_start():
    temp = int(time.strftime("%H"))
    return {
         0   <= temp   < 6  :  'Доброй ночи, ',
         6   <= temp   < 11 :  'Доброе утро, ',
         11  <= temp   < 16 :  'Добрый день, ',
         16  <= temp   < 22 :  'Добрый вечер, ',
         22  <= temp   < 24 :  'Доброй ночи, '
    }[True]



MESS_disclaimer = 'Вы попали в адаптацию настольной игры "Ужас Аркхэма". Помните, что в этом городе чужаков не любят, и если и не пошлют, то нагрубить могут вполне. Вы согласны стойко вытерпеть пренебрежительное отношение горожан? (16+)'

MESS_hello_nologin = get_hello_start() + 'искатель приключений!\n\tДо тебя дошли слухи, что в городе Аркхеме творится нечто загадочное? Глупые сказки пьяных рыбаков будоражут фантазию настолько, что это стоит потраченного времени? Ты очень странный человек, раз решил провести свой отпуск в этом задрипанном городишке. Твои планы туманны, а действия вызывают подозрения. А мы не любим подозрительных личностей. Мы будем следить за тобой. А то вдруг, ты отважишься бросить вызов Древнему Ужасу?'


MESS_anketa_first = 'Так как вы впервые прибыли в наш город, заполните небольшую анкету о себе. Желательно, ознакомьтесь с правилами поведения в городе. Это повысит ваши шансы.'

MESS_hello_login = get_hello_start() + 'искатель приключений!\n\tПри взгляде на Вас я испытываю лёгкое чувство дежавю. Возможно, Вы уже посещали наш прекрасный город Аркхэм? Тем не менее, вам стоит зарегистрироваться ещё раз.'

MESS_anketa_second = 'Чистый бланк лежит перед вами. Так же не забывайте о возможности ознакомиться с правилами поведения в городе. Это повысит ваши шансы.'

