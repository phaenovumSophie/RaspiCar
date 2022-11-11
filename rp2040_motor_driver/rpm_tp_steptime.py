factor = 150000 # 60 secs per minute * 1000000 us per s / 400 steps per round

def rpm_to_steptime(rpm):
    steptime = int(factor / rpm)
    return steptime

def steptime_to_rpm(steptime):
    rpm = int(factor / steptime)
    return rpm

def inc_rpm(rpm, delta):
    steptime1 = factor/rpm
    return
    return step_delta

print("{:5s} {:8s}".format("rpm", "steptime"))
for rpm in range(20, 200, 20):
    steptime = rpm_to_steptime(rpm)
    print("{:5d} {:8d} {:5d}".format(rpm, steptime, steptime_to_rpm(steptime)))
    
    