import os
import subprocess
from time import sleep

if __name__ == "__main__":
    try:
        # os.system("del db\\* /Q")
        subprocess.run(["del", "db\\*", "/Q"], shell=True, check=True)
        subprocess.run(["del", "source_documents\\*", "/Q"], shell=True, check=True)
        sleep(5)
        # subprocess.run(["py", "backend.py"], check=True)
        os.system("py backend.py")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the backend script: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
