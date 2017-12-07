import lingua, time

aethred = lingua.Brain('aethred.xml')
aethred.is_running = True
aethred.start()

while not aethred.get_brain():
    time.sleep(5)

print(aethred.get_brain().get_response('test'))

aethred.stop_running()
