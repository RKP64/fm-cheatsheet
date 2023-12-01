# -*- coding: utf-8 -*-

import requests
import time
import math
import signal

def is_ok(url: str) -> bool:
    """
    Returns True if the provided URL responds with a 2XX when fetched via
    a HTTP GET request.
    """
    try:
        resp = requests.get(url)
    except:
        return False
    return True if math.floor(resp.status_code / 100) == 2 else False

def scan():
    """
    Broadcasts the availability of the proxy's HTTP server once the app is ready for traffic.

    This script exists solely to ease confusion locally, as both Streamlit logs tells the
    user about the ports they're bound to (even though they're inaccessible).
    """

    print("")
    print("⚓️ Ahoy!")
    print("")
    print(
        "Your application is starting and will be available at " +
        "http://localhost:8080 when it's ready."
    )
    print("")

    # If someone tries to cancel the `docker-compose up` invocation, docker
    # will send a SIGTERM to the program. We need to handle this and set a
    # value that allows the loop to be broken.
    term = False
    def handle_interrupt(signal_number, stack_frame):
        global term
        term = True
    signal.signal(signal.SIGTERM, handle_interrupt)

    last_check = time.perf_counter()
    is_app_live = False
    while (is_app_live != True):
        if term is True:
            break
        # We don't use `time.sleep()`, as that'd prevent us from being able
        # to break the loop quickly in the event of a SIGTERM.
        now = time.perf_counter()
        if (now - last_check >= 5):
            last_check = now
            if not is_app_live:
                is_app_live = is_ok("http://app:8000")
    if is_app_live:
        print("")
        print("✨ Your local environment is ready:")
        print("")
        print("     http://localhost:8080")
        print("")
        print("⛵️ Smooth sailing!")
        print("")

if __name__ == "__main__":
    scan()
