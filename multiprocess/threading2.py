import threading, time, queue, random


def worker(data, result):
    # цикл, пока в очереди есть задания
    while not data.empty():
        # получаем задание из очереди с данными
        task = data.get()
        # для приличия, умножим хотя бы на 2
        res = task * 2
        # результаты будем возвращать как кортеж,
        # в котором будет (результат и ID_потока)
        result.put((res, threading.get_ident()))
        # имитируем нагрузку
        t_sleep = random.uniform(0.5, 2)
        time.sleep(t_sleep)
        # говорим очереди с данными 'data',
        # что задание выполнено
        data.task_done()


# заполняем очередь заданиями для потоков
# пускай это будет простой список чисел,
# которые потоки будут возвращать
data = queue.Queue()
for i in range(10, 20):
    data.put(i)

# очередь с возвращаемыми
# результатами работы потоков
result = queue.Queue()

# создаем и запускаем потоки
for _ in range(3):
    # имена потоков будут одинаковыми, что бы можно
    # было их отличить от основного потока программы
    thread = threading.Thread(name='worker',
                              target=worker,
                              args=(data, result,))
    thread.start()

# получаем результаты работы потоков в реальном
# времени в основном потоке программы.
t_start = time.time()
# цикл, пока жив хоть один поток 'worker'
while any(th.is_alive()
          for th in threading.enumerate()
          if th.name == 'worker'):

    # !Внимание! очередь с результатами при
    # работе потоков с разной нагрузкой,
    # на короткие промежутки может быть пустой,
    # к тому же мы сразу извлекаем результаты
    if not result.empty():
        res, id_thread = result.get()
        # прошедшее время с момента запуска потоков
        tm = round(time.time() - t_start, 2)
        print(f'ThID-{id_thread}: результат {res}, время: {tm}')