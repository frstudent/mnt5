# Домашнее задание к занятию "10.03. Grafana"

### Задание 1
Скриншот веб-интерфейса grafana со списком подключенных Datasource.

![GrafanaDataSources](./GrafanaDataSources.png)


## Задание 2
Создана Dashboard и в ней созданы следующие Panels:  
- Утилизация CPU для nodeexporter (в процентах, 100-idle)
```
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

- CPULA 1/5/15
```
avg(node_load1{instance="$node",job="$job"}) /  count(count(node_cpu_seconds_total{instance="$node",job="$job"}) by (cpu)) * 100

avg(node_load5{instance="$node",job="$job"}) /  count(count(node_cpu_seconds_total{instance="$node",job="$job"}) by (cpu)) * 100

avg(node_load15{instance="$node",job="$job"}) /  count(count(node_cpu_seconds_total{instance="$node",job="$job"}) by (cpu)) * 100
```

- Количество свободной оперативной памяти
```
avg by (instance) (rate(node_memory_MemFree_bytes[1h]))
```

- Количество места на файловой системе
```
irate(node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"}[30m])/(1024*1024)

100 - ((node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"} * 100) / node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"})
```

![Task2](./Task2.png)

## Задание 3
Итоговая дашборд на предыдущем скриншоте, на следующем скриншоте показан Alert для случая, когда загрузка процессора поднимается до 75%. Alert протестирован и он послал два сообщения в Discord - при прервышении нагрузки было послано сообщение Alert и сообщение OK когда нагрузка упала ниже 75%. 

![Task3](./Task3.png)


## Задание 4
Сохранённый Dashboard - [NetologyDashboard.json](./NetologyDashboard.json)

---
