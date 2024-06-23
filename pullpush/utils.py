#! /bin/python3
def progressBar(message: str, num, denom, size = 50):
    initial = message + "[{}] {: >3.1f}%"

    progressValue = int(num/denom * size)

    if progressValue > size:
        progressValue = size

    print('\r' + initial.format(((progressValue * "=") + ((size - progressValue) * " ")), num/denom * 100), end = '')

    if num/denom >= 1.0:
        print()

