# MySQL Index maintenance

## Introduction


## Usage

```shell
(venv) PS D:\my_projects\python_projects\IndexSweeper> python .\main.py  --mysql 192.168.124.66:3306,192.168.124.66:3307 --user dba --password 123456Aa

options:
  -h, --help            show this help message and exit

unused_index:
  --auto-check AUTO_CHECK
                        provide just one host and port to get all nodes in the group
  --mysql MYSQL         host1:port1[,host2:port2] ...
  --user USER
  --password PASSWORD
  --output OUTPUT       execl file name

```

* return the common unused index in given hosts
```shell
python .\main.py  --mysql localhost:3306,localhost:3307 --user dba --password 123456Aa
```

* return the unused index by give one of the hosts- not implemented
```shell
```
