# Ansible Collection - netology.frstudent

Коллекция состоит из одного модуля fr_student.py, который создаёт файл на удалённом хосте с именем и содержимым, 
передаваемыех в параметрах модулю.

Пример использования модуля playbool.yml

```yaml
---
- name: test frstudent module
  gather_facts: false
  hosts: localhost
  tasks:
  - name: run my new module
    netology.frstudent.fr_module:
      path: "/home/devops/ansible/src/like_pass"
      context: "Oppps, I meamd contetn but use context. Again"
      overwrite: False
    register: output
  - name: Show output
    debug:
      msg: "{{ output }}"
```

Тестовый запуск
```bash
$ ansible-galaxy collection install netology-frstudent-1.0.0.tar.gz --force
$ ansible-playbook playbook.yml
```
