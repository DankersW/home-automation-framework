# todo: create an event to read from mongodb
# todo: mongo, fetch digital_twin docement
# todo: define digital_twin document (status, location, technology, batterie level)
# todo: setup basic skelethon

"""
Flow:
    init
        download digital twin from db
        create local digital-twin struct with status zero-d
        create device_status_poll_timer with callback

    device_status_poll_timer_cb
        send out status_request msg to all units
        wait for x minutes to getter responses
        plublish digital-twin status to db
        zero twin struct
        start timer

    start
        listen for messages, on message update digital twin wih status to active

"""
