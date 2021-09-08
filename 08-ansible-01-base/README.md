# Домашнее задание к занятию "08.01 Введение в Ansible"

## Подготовка к выполнению
1. Установите ansible версии 2.10 или выше.
2. Создайте свой собственный публичный репозиторий на github с произвольным именем.
3. Скачайте [playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.

## Основная часть
1. Попробуйте запустить playbook на окружении из `test.yml`, зафиксируйте какое значение имеет факт `some_fact` для указанного хоста при выполнении playbook'a.

<pre>
devops@frcloud2:~/ansible/mnt-homeworks/08-ansible-01-base/playbook$ ansible-playbook site.yml -i inventory/test.yml
PLAY [Print os facts] ***********************************************************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************************************
ok: [localhost]

TASK [Print OS] *****************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "Debian"
}

TASK [Print fact] ***************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": 12
}

PLAY RECAP **********************************************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

</pre>

3. Найдите файл с переменными (group_vars) в котором задаётся найденное в первом пункте значение и поменяйте его на 'all default fact'.

```bash
cat ~/ansible/mnt-homeworks/08-ansible-01-base/playbook/group_vars/all/examp.yml
some_fact: "All default fact"
```

5. Воспользуйтесь подготовленным (используется `docker`) или создайте собственное окружение для проведения дальнейших испытаний.

Инструмент ansible новый, посему логично создать докер контейнер с его же помощью, заодно и понять как работает.
Пришлось не на шутку повозиться с конфигурированием python3.8, собирать его из исходников, разбираться с pip3. 
```yaml
---
- hosts: all
  gather_facts: true
  become: true
  vars:
    create_containers: 1
    default_container_name: docker
    default_container_image: ubuntu
    default_container_command: sleep 1d

  tasks:
    - name: Install aptitude using apt
      apt: name=aptitude state=latest update_cache=yes force_apt_get=yes

    - name: Install required system packages
      apt: name={{ item }} state=latest update_cache=yes
      loop: [ 'apt-transport-https', 'ca-certificates', 'curl', 'software-properties-common', 'python3-pip', 'virtualenv', 'python3-setuptools']

    - name: Add Docker GPG apt Key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present

    - name: Add Docker Repository
      apt_repository:
        repo: deb https://download.docker.com/linux/ubuntu xenial stable
        state: present

    - name: Update apt and install docker-ce
      apt: update_cache=yes name=docker-ce state=latest

    - name: Install Docker Module for Python
      pip:
        name: docker

    - name: Pull default Docker image
      docker_image:
        name: "{{ default_container_image }}"
        source: pull

    - name: Create default containers
      docker_container:
        name: "{{ default_container_name }}{{ item }}"
        image: "{{ default_container_image }}"
        command: "{{ default_container_command }}"
        state: present
      with_sequence: count={{ create_containers }}
```

Эта конфигурация отработала, докер контейнер создался. 

6. Проведите запуск playbook на окружении из `prod.yml`. Зафиксируйте полученные значения `some_fact` для каждого из `managed host`.

В этом месте возникла засада. ansible никак не хотел работать с контейнером. Все мои старания приводили к следующей ошибке:
<pre>
fatal: [ubuntu]: UNREACHABLE! => {"changed": false, "msg": "Failed to create temporary directory.In some cases, you may have been able
to authenticate and did not have permissions on the target directory. Consider changing the remote tmp path in ansible.cfg to a path rooted
in \"/tmp\", for more error information use -vvv. Failed command was: ( umask 77 && mkdir -p \"` echo ~/.ansible/tmp `\"&& mkdir \"` 
echo ~/.ansible/tmp/ansible-tmp-1631041588.6787155-42532-255989698407141 `\" && echo ansible-tmp-1631041588.6787155-42532-255989698407141=\"` 
echo ~/.ansible/tmp/ansible-tmp-1631041588.6787155-42532-255989698407141 `\" ), exited with result 1", "unreachable": true}
</pre>
При этом импользование ключа -vvv не помогло решить проблему.

Поскольку срок выполнения задания поджимает, пришлось использовать реальный хост. Для этого был добавлен файл inventort/fr.yml с описанием реального хоста. А для выполнения задания был добавлен файл group_vars/frhosts/examp.yml со переменной some_fact.

Результат выполнения кооманды 
ansible-playbook site.yml -i inventory/fr.yml
<pre>

PLAY [Print os facts] *************************************************************************************************************

TASK [Gathering Facts] ************************************************************************************************************
ok: [frc1]

TASK [Print OS] *******************************************************************************************************************
ok: [frc1] => {
    "msg": "Debian"
}

TASK [Print fact] *****************************************************************************************************************
ok: [frc1] => {
    "msg": "This fact was added for real host"
}

PLAY RECAP ************************************************************************************************************************
frc1
</pre>

8. Добавьте факты в `group_vars` каждой из групп хостов так, чтобы для `some_fact` получились следующие значения: для `deb` - 'deb default fact', для `el` - 'el default fact'.
9.  Повторите запуск playbook на окружении `prod.yml`. Убедитесь, что выдаются корректные значения для всех хостов.
10. При помощи `ansible-vault` зашифруйте факты в `group_vars/deb` и `group_vars/el` с паролем `netology`.

```bash
ansible-vault encrypt group_vars/deb/examp.yml
cat group_vars/deb/examp.yml
$ANSIBLE_VAULT;1.1;AES256
36313364393733663231313765333737626230623664356233363739393730333263323466316137
3632376131366135353435303030316638613732346532620a396635306363393336663062613930
34376239353633316434373631326134653030346664623462363138326461313466383030323039
3135643631383665640a613234373939663031626336616362626232633835366433316239396462
39393631636264383339363738306131343365386663373231643836366539353932
```
11. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь в работоспособности.

```
ansible-playbook site.yml -i inventory/fr.yml --ask-vault-pass
```

12. Посмотрите при помощи `ansible-doc` список плагинов для подключения. Выберите подходящий для работы на `control node`.

```ansible-dock -l``` покажет спискок всех модулей.
Подходящий модуль для работы на `control node` это модуль debug. Для работы с докером потребуются плагины из группы community.docker

13. В `prod.yml` добавьте новую группу хостов с именем  `local`, в ней разместите localhost с необходимым типом подключения.
14. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь что факты `some_fact` для каждого из хостов определены из верных `group_vars`.

<pre>
$ ansible-playbook site.yml -i inventory/fr.yml --ask-vault-pass
Vault password:

PLAY [Print os facts] ***********************************************************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************************************
ok: [frc1]
ok: [localhost]

TASK [Print OS] *****************************************************************************************************************************************************************************
ok: [frc1] => {
    "msg": "Debian"
}
ok: [localhost] => {
    "msg": "Debian"
}

TASK [Print fact] ***************************************************************************************************************************************************************************
ok: [frc1] => {
    "msg": "This fact was added for real host"
}
ok: [localhost] => {
    "msg": "All default fact"
}

PLAY RECAP **********************************************************************************************************************************************************************************
frc1                       : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

</pre>

15. Заполните `README.md` ответами на вопросы. Сделайте `git push` в ветку `master`. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым `playbook` и заполненным `README.md`.

Изначально я клонировал репозиторий, но затем заметил что это привело к тому, что любой желающий может увидеть мои ответы. Не то, чтобы мне было жалко, но не хочется вводить в заблуждение других студентов в случае неправильного ответа. Поэтому пришлось удалять клонированный репозторий и пересоздавать заново как положено.

<!--
## Необязательная часть

1. При помощи `ansible-vault` расшифруйте все зашифрованные файлы с переменными.
2. Зашифруйте отдельное значение `PaSSw0rd` для переменной `some_fact` паролем `netology`. Добавьте полученное значение в `group_vars/all/exmp.yml`.
3. Запустите `playbook`, убедитесь, что для нужных хостов применился новый `fact`.
4. Добавьте новую группу хостов `fedora`, самостоятельно придумайте для неё переменную. В качестве образа можно использовать [этот](https://hub.docker.com/r/pycontribs/fedora).
5. Напишите скрипт на bash: автоматизируйте поднятие необходимых контейнеров, запуск ansible-playbook и остановку контейнеров.
6. Все изменения должны быть зафиксированы и отправлены в вашей личный репозиторий.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---

-->
