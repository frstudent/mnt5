# Домашнее задание к занятию "10.04. ELK"

<!--
## Дополнительные ссылки

При выполнении задания пользуйтесь вспомогательными ресурсами:

- [поднимаем elk в докер](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html)
- [поднимаем elk в докер с filebeat и докер логами](https://www.sarulabs.com/post/5/2019-08-12/sending-docker-logs-to-elasticsearch-and-kibana-with-filebeat.html)
- [конфигурируем logstash](https://www.elastic.co/guide/en/logstash/current/configuration.html)
- [плагины filter для logstash](https://www.elastic.co/guide/en/logstash/current/filter-plugins.html)
- [конфигурируем filebeat](https://www.elastic.co/guide/en/beats/libbeat/5.3/config-file-format.html)
- [привязываем индексы из elastic в kibana](https://www.elastic.co/guide/en/kibana/current/index-patterns.html)
- [как просматривать логи в kibana](https://www.elastic.co/guide/en/kibana/current/discover.html)
- [решение ошибки increase vm.max_map_count elasticsearch](https://stackoverflow.com/questions/42889241/how-to-increase-vm-max-map-count)

В процессе выполнения задания могут возникнуть также не указанные тут проблемы в зависимости от системы.

Используйте output stdout filebeat/kibana и api elasticsearch для изучения корня проблемы и ее устранения.

## Задание повышенной сложности

Не используйте директорию [help](./help) при выполнении домашнего задания.

-->

## Задание 1

Поднятие сервиса даже при использовании docker-compose оказалось задачей с сюпризом.
- elasticsearch(hot и warm ноды)
- logstash
- kibana
- filebeat

В условии задания было сказано подождать 5 минут, но поднятая инфраструктура столь долго не жила.
Поиск по логам указал на источник проблемы:
<pre>
es-hot              | ERROR: [1] bootstrap checks failed
es-hot              | [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
es-hot              | ERROR: Elasticsearch did not exit normally - check the logs at /usr/share/elasticsearch/logs/es-docker-cluster.log
e</pre>

Соответственно, контейнер kibana не мог синхронизироваться с elastic нодой со всемы вытекающими последствиями. Решение нашлось быстро и оно показано ниже:

```bash
sysctl -w vm.max_map_count=262144
```

Следующая проблема возникла с filebeat
<pre>
filebeat            | Exiting: error loading config file: config file ("filebeat.yml") must be owned by the user identifier (uid=0) or root
filebeat exited with code 1
</pre>

Эта проблема решилась крайне просто:
```bash
sudo chown root filebeat.yml
```

Следующая проблема с filebeat
<pre>
filebeat            | {"level":"info","timestamp":"2021-10-20T11:32:58.284Z","caller":"pipeline/output.go:93","message":"Attempting to reconnect to backoff(async(tcp://logstash:5046)) with 11 reconnect attempt(s)"}
filebeat            | {"level":"warn","timestamp":"2021-10-20T11:33:00.900Z","caller":"transport/tcp.go:53","message":"DNS lookup failure \"logstash\": lookup logstash on 127.0.0.11:53: no such host"}
</pre>

Причина найдена - из контейнера filebeat хост logstash не пингуется. При это logstash пингуется из контейнера kibana. Проблема решается добавлением в docker-compose.yml в параметры контейнра filebeat: 
```yaml
    networks:
      - elastic
 ```
 Упс. Это лишь решает проблему сети, но в логах теперь другая ошибка:
 <pre>
 filebeat            | {"level":"error","timestamp":"2021-10-20T12:05:43.868Z","caller":"pipeline/output.go:100","message":"Failed to connect to backoff(async(tcp://logstash:5046)): dial tcp 172.19.0.4:5046: connect: connection refused"}
</pre>
 
 При этом фрагмент лога logstash
 <pre>
logstash            | [2021-10-20T12:25:49,496][INFO ][org.logstash.beats.Server] Starting server on port: 5044
 </pre>

Ага. Похоже что он слушает на порту 5044 вместо 5046.
И тут я пошёл по неправильному пути - поднял API на порту 5046 и получил следующую ошибку протокола. Теперь стало понятно что надо было изменять порт в конфигурации filebeat.yml, а не в logstash.yml. После смены порта filebeat заработал.

> Logstash следует сконфигурировать для приёма по tcp json сообщений.  
> Filebeat следует сконфигурировать для отправки логов docker вашей системы в logstash.  

Пришлось это сделать чтобы запустить.

> В директории [help](./help) находится манифест docker-compose и конфигурации filebeat/logstash для быстрого 
выполнения данного задания.

Было бы удивительно, если бы достаточно было его запустить. 

Результатом выполнения данного задания должны быть:
- скриншот `docker ps` через 5 минут после старта всех контейнеров (их должно быть 5)
- скриншот интерфейса kibana
- docker-compose манифест (если вы не использовали директорию help)
- ваши yml конфигурации для стека (если вы не использовали директорию help)

## Задание 2

Перейдите в меню [создания index-patterns  в kibana](http://localhost:5601/app/management/kibana/indexPatterns/create)
и создайте несколько index-patterns из имеющихся.

Перейдите в меню просмотра логов в kibana (Discover) и самостоятельно изучите как отображаются логи и как производить 
поиск по логам.

В манифесте директории help также приведенно dummy приложение, которое генерирует рандомные события в stdout контейнера.
Данные логи должны порождать индекс logstash-* в elasticsearch. Если данного индекса нет - воспользуйтесь советами 
и источниками из раздела "Дополнительные ссылки" данного ДЗ.
 
---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---

 
