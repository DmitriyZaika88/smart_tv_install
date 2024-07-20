import os
import subprocess
from pathlib import Path
import sys
import time


# to do переделать циклы на повторные установки


success_message_lg = "Success"  # сообщение об успешной установке на lg, которое потом ищу в консоли
success_message_tizen = "successfully"  # сообщение об успешной установке на tizen, которое потом ищу в консоли
failed_message = "no connected target"  # выводится, если не установленно sdb соединение с tizen
tizenInstall = r"C:\\tizen-studio\\tools\\ide\\bin\\tizen.bat"  # путь до tizen, который записываем в path при установке
aresInstall = r"C:\\webOS_TV_SDK\\CLI\bin\\ares-install.cmd"  # пусть до ares install, который записываем в path при установке
# пути до установщиков
pathToLgApp = r"C:\\tricolorTv\\tricolortv-master\\buildWebos\\com.app.tricolortv.com_1.8.0_all.ipk"  # путь до нашего приложения lg
pathToTizenApp = r"C:\\tricolorTv\\tricolortv-master\\buildTizen\\sliz.wgt"  # путь до нашего приложения tizen(уже подписанного). Обязательно на русском
sdb = r"C:\tizen-studio\tools\sdb.exe" #путь до sdb
max_counter = 2
# success_message = "Success"
lg_tv_names = ("webos2", "webos3.5", "webos6") # тут записываю lg телевизоры так, как они называются в cli , подробнее о подключении https://conf.gs-labs.tv/pages/viewpage.action?pageId=166616747
tizen_tv_names = "UE43N5500" # имя телевизора tizen
aresLaunch = r"C:\\webOS_TV_SDK\\CLI\bin\\ares-launch.cmd"


# цикл установки на lg, перебирает все телевизоры из lg_tv_names и на каждый пытается установить приложение с выводом результатов в консоль, по три попытки на телевизор
for lg_tv in lg_tv_names:
    counter = 0
    while True:
        if counter <= max_counter:
            console_output = subprocess.run([aresInstall, '--device', lg_tv, pathToLgApp], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).stdout.decode('utf-8')
            if success_message_lg in console_output:
                print('успешно установлено на ' + lg_tv)
                break
            else:
                print(f'пробую еще раз установить на ' + lg_tv + '. попытка #' + str(counter + 1))
                counter += 1
                time.sleep(5)
        else:
            print('провал при установке на ' + lg_tv )
            break


for lg_tv in lg_tv_names:
    counter = 0
    while True:
        if counter <= max_counter:
            console_output = subprocess.run([aresLaunch, '--device', lg_tv, "com.app.tricolortv.com"], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).stdout.decode('utf-8')
            if "Launched application" in console_output:
                print('успешно запущено на ' + lg_tv)
                break
            else:
                print('провал при запуске на ' + lg_tv )
                break

# создание подписанного приложения. ОБЯЗАТЕЛЬНО ЛАТИНИЦЕЙ <name></name>
tizen_package = "package"
tizen_certificate = "sam2020t5300" # существующий сертификат
tizen_build_path = r"C:\\tricolorTv\\tricolortv-master\\buildTizen\\"
profiles_path = r":\\Users\\dmitriy.zaika\\tizen-studio-data\\vscode-tizentv\\resource\\profiles"


# на данный момент работает только команда cli
tizen_package_with_certificate = "tizen package -t wgt -s sam2020t5300 -- C:\\tricolorTv\\tricolortv-master\\buildTizen"
cli_push = subprocess.call(tizen_package_with_certificate, shell = True)

# пока не понял как прокинуть аргумент с наименованием сертификата (bash его не видит)
""" tv_tizen = subprocess.run([tizenInstall, tizen_package, '-t', 'wgt', '-s', tizen_certificate, tizen_build_path]) """


# установка приложения на Tizen
while True:
    counter = 0
    tv_tizen = subprocess.run([tizenInstall, 'install', '-n', pathToTizenApp, '-t', tizen_tv_names, '--', ' .'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE).stdout.decode('utf-8')
    if success_message_tizen in tv_tizen:
        print('успешно установленно на ' + tizen_tv_names)
        break
    elif counter == max_counter:
        print('провал при установке на ' + tizen_tv_names)
        exit
    elif failed_message in tv_tizen:
        print("телевизор не подключен, подключаюсь")
        subprocess.run(['sdb', 'connect', '192.168.88.254'])
        counter += 1
    else:
        print(f'пробую еще раз установить на ' + tizen_tv_names + "попытка #" + str(counter + 1))
        counter += 1
        time.sleep(5)


tizen_run = "run"
tizen_device_ip = "192.168.88.254:26101"
tizen_application_name = "sbrS3Deqed.multiscreen"

# запуск приложения на Tizen (Tizen run -s 192.168.88.253:26101 -p sbrS3Deqed.multiscreen работает через консоль) 

""" command = "Tizen run -s 192.168.88.254:26101 -p sbrS3Deqed.multiscreen"
res = subprocess.call(command, shell = True) """


for tv_tizen in tizen_tv_names:
    counter = 0
    if counter <= max_counter:
        console_output = tv_tizen = subprocess.run([tizenInstall, tizen_run, '-s', tizen_device_ip, "-p", tizen_application_name], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).stdout.decode('utf-8')
        if "successfully launched" in console_output:
            print ('Приложение запущено на ' + tizen_tv_names)
            break
        else: 
            print('Не удалось запустить на ' + tizen_tv_names + " попытка #" + str(counter + 1))
            counter += 1
            break
        


