# Тестовое задание Workmate
Нужно написать скрипт для обработки csv-файла.  
Скрипт читает файлы с данными о подготовке студентов к экзаменам (см. примеры ниже) и формирует отчеты. Нужно сформировать один отчет в котором будет медианная сумма трат на кофе по каждому студенту за весь период сессии. Отчёт включает в себя список студентов и медиану трат (по колонке coffee spent), отчёт сортируются по убыванию трат. Название файлов (может быть несколько) и название отчета передается в виде параметров --files и --report (в нашем случае это median-coffee). Отчёт формируется по всем переданных файлам, а не по каждому отдельно.  
Чтобы сфокусироваться на функционале формирования отчёта и не отвлекаться на рутинные задачи (обработку параметров скрипта, чтения файлов и вывод), можно использовать стандартную библиотеку argparse и csv, для расчета медианы statistics, а для отображения в консоли tabulate.  
    
## Примеры запусков
**Пример запуска скрипта для формирования `median-coffee` отчета.**  
`main.py --files example_files\math.csv example_files/physics.csv`  
![median-coffee example](https://sun9-69.userapi.com/s/v1/ig2/0RvgdzlC0OEenyZqe7N0u8fjXrkNioob-pwLZS6oAdWDIJp0w-ZWmTK0lN42SFOz35v5mBnp3CqdA41GyyZlthSF.jpg?quality=95&as=32x37,48x56,72x83,108x125,160x185,240x278,360x417,480x556,540x625,640x741,652x755&from=bu&cs=652x0)  
*Флаг `--report median-coffee` является дефолтным и не требует прямого указания*  
    
**Пример запуска скрипта для формирования `sleep-hours` отчета.**  
`main.py --files example_files\math.csv example_files/physics.csv --report sleep-hours`  
![slepp-hours](https://sun9-68.userapi.com/s/v1/ig2/rBguLp0KvFxGVjxI5_nL0w5mMeY_ALYxMgqE7C-xKgAZSnTqayuvfmUJmkpPBquAYucdNXPTLKwSsE-TUff-D7vl.jpg?quality=95&as=32x37,48x56,72x83,108x125,160x185,240x278,360x417,480x556,540x625,640x741,652x755&from=bu&cs=652x0)
