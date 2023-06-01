Cloner le depot dans vos roles
==============================

cd roles
git clone https://github.com/pvalois/check_oc.git

Inventory
=========
[bastions]
bastion-4.9
bastion-4.7
...

Playbook
=========

- name: Install check-oc script on bastion
  hosts:
    - bastions

  tasks:

    - name: import role
      include_role:
        name: check_oc
~                        
