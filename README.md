Cloner le depot dans vos roles
==============================
```
cd roles
git clone https://github.com/pvalois/check_oc.git
```

Editer dans files/ les scripts python, pour ajouter les liens des webhooks mattermost.

Inventory
=========
```
[bastions:children]
HorsProd
Prod

[HorsProd]
bastion-4.9

[Prod]
bastion-4.7
```

Variables
=========
créer dans les group_vars les fichiers Prod.yaml et HorsProd.yaml dans lequel vous positionnerez l'url de webhook:

```
mattermost_webhook="..."
```

Playbook
=========
```
- name: Install check-oc script on bastion
  hosts:
    - bastions

  tasks:

    - name: import role
      include_role:
        name: check_oc
```                        
