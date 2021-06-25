from modules import *
from smiles import *
try:
    def main():
        global receiver_name
        global stopsending

        print('\nДобро пожаловать в WhatsApp клиент!\n ')
        # Используем директорию данных, чтобы сохранять cookie файлы сеанса и не авторизовываться при повторном запуске приложения.
        # Папка через время может стать большой. Это исправляется её удалением, но тогда нужно повторно авторизовываться.
        if not os.path.exists(config['chrome_data_directory']):  # Если папка не создана, то создаём её.
            os.makedirs(config['chrome_data_directory'])
        # Webdriver - драйвер для тестирования веб-приложений
        driver_options = webdriver.ChromeOptions()  # Подключаем методы ChromeOptions
        driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Отключаем вывод логов в консоль
        driver_options.add_argument("user-data-dir={0}".format(config['chrome_data_directory']))
        driver = webdriver.Chrome(config['path_to_chromedriver'],
                                  options=driver_options)  # Настраиваем webdriver для работы с Chrome
        driver.get(config['whatsapp_url'])  # Открываем WhatsApp в Chrome

        print("Пожалуйста, отсканируйте QR-код на появившейся странице в своём мобильном приложении WhatsApp"
              " и введите ok.\nЕсли сразу открылась страница WhatsApp, нажмите Enter.\n")
        while True:  # Просим пользователя сканировать QR-код, который появился при открытии страницы WhatsApp
            is_connected = input("QR-код отсканирован? Ok/No: ")
            if is_connected.lower() == 'ok' or is_connected == '':
                break

        if len(sys.argv) > 1:
            choose_receiver(driver)  # В качестве получателя указываем полученный аргумент при запуске
        else:
            receiver_input = input("\nВведите имя собеседника в WhatsApp: ")
            choose_receiver(driver, receiver_input)
        print("Для просмотра доступных команд введите help.")
        # Запускаем отдельный поток для получения входящих сообщений.
        get_message_thread = threading.Thread(target=start_getting_messages, args=(driver,))
        get_message_thread.start()

        while True:
            user_input = input().strip()
            if len(user_input) > 7 and 'sendto ' in user_input[:7]:
                choose_receiver(driver, receiver=user_input[7:])
            elif len(user_input) > 5 and 'send ' in user_input[:5]:
                if is_stopsending(stopsending) == 0:
                    send_message(driver, user_input[5:])
            elif user_input == 'stopsending':
                if stopsending == -1:
                    print("Прекращение отправки сообщений. Теперь вы только получаете входящие сообщения.")
                else:
                    print("Отправка сообщений вновь доступна.")
                stopsending *= -1
            elif user_input == "voice":
                send_voice(driver)
            elif user_input == "file":
                if is_stopsending(stopsending) == 0:
                    filepath = input("Введите путь до файла, который вы хотите отправить: ")
                    send_file(driver, filepath)
            elif user_input == "media":
                if is_stopsending(stopsending) == 0:
                    filepath = input("Введите путь до медиафайла, который вы хотите отправить: ")
                    send_media(driver, filepath)
            elif user_input == "emoji":
                if is_stopsending(stopsending) == 0:
                    emoji = input("Введите название эмодзи, который вы хотите отправить: ")
                    send_emoji(driver, emoji)
            elif user_input == "contact":
                if is_stopsending(stopsending) == 0:
                    contact = input("Введите имя контакта, который вы хотите отправить: ")
                    send_contact(driver, contact)
            elif user_input == "smile":
                if is_stopsending(stopsending) == 0:
                    seed()
                    random_smile = choice(smiles)
                    send_smiley(driver, random_smile)
            elif user_input == 'help':
                print("\nДоступные команды:\nsendto <name> - перейти к чату с указанным пользователем.\n"
                      "stopsending - включить/выключить отправку сообщений.\n"
                      "send <message> - отправка сообщения текущему собеседнику.\n"
                      "voice - отправка голосового сообщения текущему собеседнику.\n"
                      "file - отправка файла текущему собеседнику.\n"
                      "media - отправка медиафайла текущему собеседнику.\n"
                      "emoji - отправка эмодзи текущему собеседнику.\n"
                      "contact - отправка контакта текущему собеседнику.\n"
                      "smile - отправка смайлика текущему собеседнику.\n"
                      "exit - выход из программы.\n")
            elif user_input == 'exit':
                print('Закрывается WebDriver...')
                driver.quit()
                print('Закрывается программа...')
                quit()
            else:
                print("Неизвестная команда. Для просмотра доступных команд введите help.")

    if __name__ == '__main__':
        main()

except AssertionError as e:
    sys.exit(print("\nНе удаётся открыть URL-адрес WhatsApp.\n"))

except KeyboardInterrupt as e:
    sys.exit("\nНажмите Ctrl+C для выхода.\n")

except WebDriverException as e:
    sys.exit(print(e, "\nОшибка ChromeDriver.\n"
                      "Проверьте, совместима ли установленная версия ChromeDriver с установленной версией Chrome.\n"))
