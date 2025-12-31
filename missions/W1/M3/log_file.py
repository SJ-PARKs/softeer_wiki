from datetime import datetime

LOG_FILE = "etl_project_log.txt"

def log_message(message):
    current_time = datetime.now().strftime("%Y-%B-%d-%H-%M-%S")
    log_entry = f"{current_time}, {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry)