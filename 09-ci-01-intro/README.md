# Домашнее задание к занятию "09.01 Жизненный цикл ПО"

## Kanban workwlow

![Screenshot0](./KanbanBorard.png)

<!--
1. Получить бесплатную [JIRA](https://www.atlassian.com/ru/software/jira/free)
2. Настроить её для своей "команды разработки"
3. Создать доски kanban и scrum
-->
![Screenshot1](./scrum_softwarelifecyle_2021-10-06_01.07pm.png)

## Настройка Jira

- Схема Workflow разработки - [NetlogyDefaultWorkflow](./NetlogyDefaultWorkflow.xml) 
- Схема  Workflow исправления ошибок - [NetlogyBugfixesWorkflow](./NetlogyBugfixesWorkflow.xml) 

## Список Issues

- Экспорт Issues после проведения задач в Jira  [workflow](./SearchRequest.xml)

<!--
В рамках основной части необходимо создать собственные workflow для двух типов задач: bug и остальные типы задач. Задачи типа bug должны проходить следующий жизненный цикл:
1. Open -> On reproduce
2. On reproduce <-> Open, Done reproduce
3. Done reproduce -> On fix
4. On fix <-> On reproduce, Done fix
5. Done fix -> On test
6. On test <-> On fix, Done
7. Done <-> Closed, Open

Остальные задачи должны проходить по упрощённому workflow:
1. Open -> On develop
2. On develop <-> Open, Done develop
3. Done develop -> On test
4. On test <-> On develop, Done
5. Done <-> Closed, Open

Создать задачу с типом bug, попытаться провести его по всему workflow до Done. Создать задачу с типом epic, к ней привязать несколько задач с типом task, провести их по всему workflow до Done. При проведении обеих задач по статусам использовать kanban. Вернуть задачи в статус Open.
Перейти в scrum, запланировать новый спринт, состоящий из задач эпика и одного бага, стартовать спринт, провести задачи до состояния Closed. Закрыть спринт.
-->




---
