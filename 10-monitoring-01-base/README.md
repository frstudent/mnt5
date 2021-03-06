# Домашнее задание к занятию "10.01. Зачем и что нужно мониторить"

## Обязательные задания

> 1. Вас пригласили настроить мониторинг на проект. На онбординге вам рассказали, что проект представляет из себя 
платформу для вычислений с выдачей текстовых отчетов, которые сохраняются на диск. Взаимодействие с платформой 
осуществляется по протоколу http. Также вам отметили, что вычисления загружают ЦПУ. Какой минимальный набор метрик вы
выведите в мониторинг и почему?

Прежде всего выберу метрику загрузки процессора из /proc/loadavg и /proc/stat, поскольку из условия задачи требуются вычисления. По-хорошему бы надо смотреть загрузку не только CPU, но и FPU, но беглый поиск в Интернете не дал информацию о статусе FPU в Linux. Надеюсь, по условию задачи загрузку FPU можно не мониторить. Если же да, то можно и ядро запатчить при большой необходимости.

Так же в условии задачи не указано, какие именно вычисления. Например, если считаются большие матрицы, тогда будет полезна информация из /proc/vmstat и /proc/meminfo в динамике отслеживая изменение параметров. Какие конкретно параметры отслеживать - сейчас не скажу. Однако, в некоторых случаях может потребоваться непосредственная информация о процессе, а не всей системы в целом. Думаю что некоторые поля из /proc/[pid]/stat будут весьма полезны.

Вычислительный процесс сохраняет данные на диск. Соответственно, необходимо следить за количеством доступой памяти и inodes.

> 2. Менеджер продукта посмотрев на ваши метрики сказал, что ему непонятно что такое RAM/inodes/CPUla. Также он сказал, 
что хочет понимать, насколько мы выполняем свои обязанности перед клиентами и какое качество обслуживания. Что вы 
можете ему предложить?

Прежде всего предложу переименовать RAM/inodes/CPUl в "Загрузка памяти", "Свободное место на диске", "Загрузка процессора". 

Касательно inodes, они показывают только количество созданных/свободных дескрипторов для создания файлов. Посему предложу alert на исчерпание inodes или свободного дискового пространства.

Далее, предложу мониторить бизнес-логику, например, соотношение количества корректных HTTP ответов и HTTP ответов, сигнализиоующих об ошибках.

Так же не будет лишним мониторинг загрузки сети.

> 3. Вашей DevOps команде в этом году не выделили финансирование на построение системы сбора логов. Разработчики в свою 
очередь хотят видеть все ошибки, которые выдают их приложения. Какое решение вы можете предпринять в этой ситуации, 
чтобы разработчики получали ошибки приложения?

`cat /var/log/appname.log | less` - скупой платит дважды.

Как вариант, на машине одного из разработчиков можно в докер контейнере развернуть развернуть и настроить Prometheus и собирать логи/метрики по своей инициативе.

И, возможно, самый лучший вариант - написать докладную записку на имя генерального директора с описание проблемы и поясненением насколько важен мониторинг продукта, объяснениеи, какие имидживые потери и потерю прибыли может понести компания в случае сбоев в ПО/железе и насколько система мониторинга позволяет предотвращать инцинденты. Уверен, при таком раскладе деньги на дополнительный сервер у руководства найдутся.

> 4. Вы, как опытный SRE, сделали мониторинг, куда вывели отображения выполнения SLA=99% по http кодам ответов. 
Вычисляете этот параметр по следующей формуле: summ_2xx_requests/summ_all_requests. Данный параметр не поднимается выше 
70%, но при этом в вашей системе нет кодов ответа 5xx и 4xx. Где у вас ошибка?

Я пока не опытный SRE, а только учусь. Очевидно, что остальные 30% это коды ответов 1xx и 2xx. Причин, по которым возвращаются эти коды, может быть несколько. Произвожу анализ логов и нахожу причины ошибок. Скорее всего добавляю коды 1xx в формулу. Коды ошибок 3xx анализирую - есть вероятность что разработчики фронтенда намудрили. Если переходы ожидаемые, то добавляю коды ошибок в 3xx в формулу. Причём, код 304 вообще не сочту за ошибку и сразу добавлю в формулу. (Надеюсь, в следующих лекциях узнаю как это реализовать)

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Поскольку задание необязательное, то я оставлю его на будущее. Увы, форс-мажор на работе, которая меня направила на курсы devops Нетологии.
Чтобы запускать скрипт сбора метрики, достаточно выполнить ```$ crontab -e```
И с помощью вышеприведённой команды добавить следующую строку в  crontab файл  

<pre>
* * * * * /usr/local/bin/python3 /home/devops/get_metrics.py
</pre>

В результате каждую минуту будет запускаться скрипт, собирающий метрики.

<!--
Вы устроились на работу в стартап. На данный момент у вас нет возможности развернуть полноценную систему 
мониторинга, и вы решили самостоятельно написать простой python3-скрипт для сбора основных метрик сервера. Вы, как 
опытный системный-администратор, знаете, что системная информация сервера лежит в директории `/proc`. 
Также, вы знаете, что в системе Linux есть  планировщик задач cron, который может запускать задачи по расписанию.

Суммировав все, вы спроектировали приложение, которое:
- является python3 скриптом
- собирает метрики из папки `/proc`
- складывает метрики в файл 'YY-MM-DD-awesome-monitoring.log' в директорию /var/log 
(YY - год, MM - месяц, DD - день)
- каждый сбор метрик складывается в виде json-строки, в виде:
  + timestamp (временная метка, int, unixtimestamp)
  + metric_1 (метрика 1)
  + metric_2 (метрика 2)
  
     ...
     
  + metric_N (метрика N)
  
- сбор метрик происходит каждую 1 минуту по cron-расписанию

Для успешного выполнения задания нужно привести:

а) работающий код python3-скрипта,

б) конфигурацию cron-расписания,

в) пример верно сформированного 'YY-MM-DD-awesome-monitoring.log', имеющий не менее 5 записей,

P.S.: количество собираемых метрик должно быть не менее 4-х.
P.P.S.: по желанию можно себя не ограничивать только сбором метрик из `/proc`.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

--->
