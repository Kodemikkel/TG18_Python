import pigpio
pi = pigpio.pi()
for g in range(0,32):
    print("GPIO {} is {}".format(g, pi.read(g)))
pi.stop()