''' Calculates how long a driver must wait at a red or yellow light
    until the green phase starts again.'''

def time_until_green(light, current_time):
    time = (current_time - light.offset) % light.cycle_duration

    if (time<light.green_duration):
        return 0.0
    elif (time<light.green_duration + light.yellow_duration):
        return light.cycle_duration - time
    else:
        return light.cycle_duration - time