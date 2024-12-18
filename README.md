**Dasha Helper** - бот, который контролирует наличие пользователя в чате по указанному списку: удаляет из группы, если отсутствует его имя в списке, и уведомляет, если пользователя из списка в группе нет.

**Функционал бота:**
1.  По команде **/commands** бот выводит список возможных команд, исполняемых им.
2.  По команде **/add_chat** (отправляется из чата) бот добавляет текущий чат и его пользователей в базу данных, печатает id чата в ответ (chat_id).
3.  По команде **/valid** {usernames} бот получает на вход список юзернеймов пользователей и добавляет их в список валидных (разрешенных) пользователей для текущего чата.
4.  По команде **/not_valid** {usernames} бот получает на вход список юзернеймов пользователей и удаляет их из списка валидных пользователей (если они в нем есть).
5.  По команде **/new** {usernames} бот меняет старый список валидных пользователей на указанный новый.
6.  По команде **/call_dasha** бот удаляет всех пользователей из чата, которые не содержатся в валидном списке и не являются при этом администраторами\владельцами чата. Для      выполнения этой функции бот должен обладать правами администратора в группе.
7.  По команде **/check** бот выводит список пользователей, которые находятся в валидном списке, но отсутствуют в чате.

**Инструкция по использованию:**

1.  Для управления уже существующей группой бота нужно добавить в нее, затем взаимодействие с ним осуществляется либо через сам чат, либо через личные сообщения.
2.  Добавлять и изменять список валидных пользователей может только пользователь с правами администратора в указанной группе.
3.  При обращении к боту, он предлагает список контролируемых групп (название + id), из которого пользователь выбирает, с какой группой он хочет взаимодействовать. Далее бот     предлагает список команд из функционала.

**Видеоотчет: https://disk.yandex.ru/i/eWyRygmRMrJpaw**

**Распределение ролей в проекте:**

Антипова Юлия (tg @antip_ula): описание функций, реализация функций, создание бота, мотиватор, написание тестов.

Михайлова Екатерина (tg @yaseledka): описание функций, создание базы данных, создание бота, генератор идей, реализация функций.
