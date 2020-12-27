# On the spot test task

### Small project description ###

Для решения задачи обходов виртуальных машин я использовал графы и обход по графу в глубину.
В системе 2 сервиса, которые при перезагрузке теряют состояние. Так же они являются singletone.
LogService - Хранит только среднее время выполнения и количество выполненных запросов на сервер. Используется в LogMiddleware
VmAttackService - При старте получает список vm и firewall_rules по которым и строит графы. 
Каждая виртуальная машина - это вершина, каждое правило - это грань.


### Setup project ###
There is no database or other side services/integrations, so you will need python3 and virtualenv

- Clone repository

`$ git clone git@github.com:F4ever/on-the-spot.git`

- Goto project folder

`$ cd on-the-spot`

- Create virtual env and run

`$ pip install -r requirements.txt`

- Profit

### Run service ###

- Run server command

`vm_file` argument is required. 

`$ python manage.py runserver --vm_file path/to/json/file.json`

You can use presaved fixtures to run server from project root folder

`$ python manage.py runserver --vm_file core/tests/fixtures/input-0.json`

### Server API ###

There are only 2 endpoints

`GET /api/v1/stats/` - Returns count of requests made from server start, average request time and vm count.

Response schema: 

```
{
    vm_count: int,  
    request_count: int,
    average_request_time: float
}
```

`GET /api/v1/attack/?vm_id=vm_xxx` - Returns ids list of vulnerable vm.

Gets `vm_id` param - machine id of vm that attacker got access to. 

Response schema: 

```
[
    "vm_xxx", "vm_xxx"
]
```

### Tests ###

You can run tests via:

`$ python manage.py test`
