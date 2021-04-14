import sendook
import pytest


def mock_sendook():
    sendook.GPIO = sendook.MockGPIO()
    sendook.GPIO.HIGH = 100
    sendook.GPIO.LOW = -100
    pinstates = []
    delays = []
    sendook.GPIO.output = lambda pin, state: pinstates.append([pin, state])
    sendook.sleep_finegrain = lambda delay: delays.append(delay)
    return pinstates, delays


def test_send_one():
    # mock
    pinstates, delays = mock_sendook()
    sendook.send_one(1000, 777)

    assert(pinstates == [[1000, 100], [1000, -100]])
    assert(delays == [777])


def test_main_expecthelp():
    import subprocess
    import sys
    with pytest.raises(subprocess.CalledProcessError) as callError:
        subprocess.check_output(
            str(sys.executable) + " sendook.py", shell=True)
        assert("usage: sendook.py" in str(callError.value))


def test_main_dryrun():
    import subprocess
    import sys
    import time
    start = time.time()

    stdout = subprocess.check_output(str(sys.executable) + " sendook.py "
                                     + "110011DOGGGYDOGSNOOPISITHEORISITANOTHERRANDOMCHARACTERLETSMAKETHISVERYVERYLONG1001 "
                                     + "-d True -g 999 -p 10000 -s 1000 -r 10", shell=True)
    end = time.time()
    assert("usage: sendook.py" not in str(stdout))
    assert("110011DOGGGYDOGSNOOPISITHEORISITANOTHERRANDOMCHARACTERLETSMAKETHISVERYVERYLONG1001" in str(stdout))
    duration = end - start
    # expected duration by signal length is 1 sec + minimal for program run
    assert(duration > 1)
    assert(duration < 4)


def test_main_dryrunverbose():
    import subprocess
    import sys
    import time
    start = time.time()

    stdout = subprocess.check_output(str(sys.executable) + " sendook.py "
                                     + "10001 "
                                     + "-d True -g 999 -p 10 -s 10 -r 1 -v True", shell=True)
    end = time.time()
    assert("usage: sendook.py" not in str(stdout))
    assert("1" in str(stdout))
    duration = end - start
    # expected duration by signal length is 0.01 sec + program run
    assert(duration < 2)
