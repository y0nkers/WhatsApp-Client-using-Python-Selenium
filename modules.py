from dependencies import *


# Отправляем сообщение message с помощью driver
def send_message(driver, message):
    # Выбираем поле ввода для отправки сообщения
    text_box = driver.find_element(By.XPATH, '//*[@id="main"]//footer//div[contains(@contenteditable, "true")]')
    text_box.click()
    action = ActionChains(driver)  # Выполняем ввод с клавиатуры и нажатия клавиш
    action.send_keys(message).send_keys(Keys.ENTER).perform()
    print("Сообщение отправлено!")


# Запускаем планировщик, который проверяет чат на наличие новых сообщений
def start_getting_messages(driver):
    incoming_scheduler.enter(config['get_message_interval'], 1, getting_messages, (driver, incoming_scheduler))
    incoming_scheduler.run()


# Получаем новые сообщения
def getting_messages(driver, scheduler):
    global last_printed_message
    curr_thread_name = get_receiver_name(driver)
    try:
        # Получаем все сообщения
        all_messages = driver.find_elements(By.XPATH, '//*[@id="main"]//div[contains(@class, "message")]')
        # Проверяем, есть ли хотя бы 1 сообщение в чате
        if len(all_messages) >= 1:
            last_message_outgoing = is_outgoing_message(all_messages[-1])
            last_message_sender, last_message_text = get_message_meta_info(all_messages[-1])
            is_messages_exist = True
        else:
            is_messages_exist = False
    except Exception as e:
        print(e)
        is_messages_exist = False

    if is_messages_exist:
        if not last_message_outgoing:  # Если последнее сообщение было ВХОДЯЩИМ
            if last_printed_message == last_message_sender + last_message_text:  # Если последнее соообщение уже напечатано
                pass
            else:  # Иначе выводим новые сообщения
                print_from = 0
                for i, curr_msg in reversed(list(enumerate(all_messages))):  # Идём от последнего сообщения к 1-ому
                    current_message_outgoing = is_outgoing_message(curr_msg)
                    current_message_sender, current_message_text = get_message_meta_info(curr_msg)

                    # Если текущее сообщение исходящее или если найдено последнее напечатанное сообщение
                    if current_message_outgoing or last_printed_message == current_message_sender + current_message_text:
                        # Прерываем цикл, начинаем печатать сообщения с i-го индекса
                        print_from = i
                        break
                # Выводим все сообщения от последнего напечатанного до самого нового
                for i in range(print_from + 1, len(all_messages)):
                    message_sender, message_text = get_message_meta_info(all_messages[i])
                    last_printed_message = message_sender + message_text
                    # playsound('message.mp3') # Play sound when receive message
                    if message_sender != "" and message_text != "":
                        print('\nНовое сообщение!\nВремя получения: ' + message_sender[1:message_sender.find(']')]
                              + '\nОтправитель: ' + message_sender[message_sender.find(']') + 2:len(message_sender) - 2]
                              + '\nТекст сообщения: ' + message_text + '\n')
                    else:
                        print("\nСобеседник отправил вложение. Перейдите в приложение, чтобы посмотреть его.\n")

    # Повторно запускаем планировщик на получение сообщений.
    incoming_scheduler.enter(config['get_message_interval'], 1, getting_messages, (driver, scheduler,))


def is_outgoing_message(webdriver_element):  # Проверка на то, является ли сообщение исходящим.
    for _class in webdriver_element.get_attribute('class').split():
        if _class == "message-out":
            return True
    return False


# Получаем с помощью webdriver отправителя и текст сообщения.
def get_message_meta_info(webdriver_element):
    # Проверка на не-текстовое сообщение
    try:
        message = webdriver_element.find_element(By.XPATH, './/div[contains(@class, "copyable-text")]')
        message_sender = message.get_attribute('data-pre-plain-text')
        message_text = message.find_elements(By.XPATH, './/span[contains(@class, "selectable-text")]')[-1].text
    except IndexError:
        message_text = ""
    except Exception:
        message_sender = ""
        message_text = ""

    return message_sender, message_text


# Выбираем, кому будем отправлять сообщения.
def choose_receiver(driver, receiver=None):
    if receiver:  # Если передано имя получателя
        send_to = receiver
    else:
        send_to = ' '.join(sys.argv[1:])  # Если не было передано имя, то это вызов из консоли
    input_box = driver.find_element(By.XPATH,  # Находим элемент "Поиск по имени"
                                    '//*[@id="side"]//div[contains(@class,"copyable-text selectable-text")]')
    input_box.clear()  # Очищаем ввод
    input_box.click()  # Нажимаем на поле ввода
    input_box.send_keys(send_to)  # Пишем в поле имя получателя
    input_box.send_keys(Keys.RETURN)  # Нажимаем клавишу enter, переходим к диалогу с получателем
    get_receiver_name(driver)  # Выводим имя получателя


# Вывод в консоль имя пользователя, которому будем отправлять сообщение.
def get_receiver_name(driver):
    global receiver_name
    current_receiver_name = driver.find_element(By.XPATH,
                                                '//*[@id="main"]/header//span[contains(@dir, "auto")]').text
    if current_receiver_name != receiver_name:
        receiver_name = current_receiver_name
        print("Текущий собеседник: ", current_receiver_name)
    return current_receiver_name


def send_smiley(driver, smile):
    text_box = driver.find_element(By.XPATH, '//*[@id="main"]//footer//div[contains(@contenteditable, "true")]')
    text_box.click()
    action = ActionChains(driver)  # Выполняем ввод с клавиатуры и нажатия клавиш
    for i in range(len(smile)):
        for j in range(len(smile[i])):
            action.send_keys(smile[i][j])
        action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER)
    action.send_keys(Keys.ENTER).perform()
    print("Отправлен смайлик!")


def send_file(driver, filepath):
    # Находим кнопку прикрепления вложения и нажимаем на неё
    attachment_box = driver.find_element_by_xpath('//div[@title = "Прикрепить"]')
    attachment_box.click()
    # Находим кнопку прикрепления документа и нажимаем на неё
    file_box = driver.find_element_by_xpath('//input[@accept="*"]')
    file_box.send_keys(filepath)
    time.sleep(2)
    # Находим кнопку отправки и нажимаем на неё
    send_button = driver.find_element_by_xpath('//span[@data-icon="send"]')  # Для светлого режима send-light
    send_button.click()
    print("Файл отправлен!")


def send_media(driver, filepath):
    # Находим кнопку прикрепления вложения и нажимаем на неё
    attachment_box = driver.find_element_by_xpath('//div[@title = "Прикрепить"]')
    attachment_box.click()
    # Находим кнопку прикрепления фото/видео файла и нажимаем на неё
    image_box = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    image_box.send_keys(filepath)
    time.sleep(2)
    # Находим кнопку отправки и нажимаем на неё
    send_button = driver.find_element_by_xpath('//span[@data-icon="send"]')  # Для светлого режима send-light
    send_button.click()
    print("Файл отправлен!")


def send_emoji(driver, emoji):
    emoji_box = driver.find_element_by_xpath('//span[@data-icon="smiley"]')
    emoji_box.click()

    search_box = driver.find_element_by_xpath('//input[@title="Поиск смайла"]')
    search_box.send_keys(emoji)
    search_box.send_keys(Keys.ENTER)

    send_button = driver.find_element_by_xpath('//span[@data-icon="send"]')
    send_button.click()
    print("Эмодзи " + emoji + " отправлен!")


def send_contact(driver, contact):
    attachment_box = driver.find_element_by_xpath('//div[@title = "Прикрепить"]')
    attachment_box.click()

    contact_box = driver.find_element_by_xpath('//span[@data-icon="attach-contact"]')
    contact_box.click()

    input_box = driver.find_element_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
    input_box.click()
    input_box.send_keys(contact)

    contact_box = driver.find_element_by_xpath(f'//span[@title="{contact}"]')
    contact_box.click()
    time.sleep(0.5)

    send_button = driver.find_element_by_xpath('//span[@data-icon="send"]')
    send_button.click()
    send_button = driver.find_element_by_xpath('//span[@data-icon="send"]')
    send_button.click()
    print("Контакт " + contact + " отправлен!")


def send_voice(driver):
    voice_box = driver.find_element_by_xpath('//span[@data-icon="ptt"]')
    voice_box.click()
    print("Началась запись голосового сообщения.\nВведите stop, чтобы отменить отправку голосового сообщения.")
    print("Для отправки голосового сообщения введите send.")
    user_input = input("Ваш выбор: ")
    while user_input != "stop" and user_input != "send":
        user_input = input("Неправильный ввод. Повторите попытку: ")
    if user_input == "send":
        input_box = driver.find_element_by_xpath('//button[@aria-label="Отправить"]')
        input_box.click()
        print("Голосовое сообщение отправлено!\n")
    else:
        print("Прекращение отправки голосового сообщения.\n")
        input_box = driver.find_element_by_xpath('//button[@aria-label="Отменить"]')
        input_box.click()


def is_stopsending(value):
    if value == 1:
        print("Вы не можете отправлять сообщения. Введите stopsending, чтобы включить отправку сообщений.")
        return 1
    return 0
