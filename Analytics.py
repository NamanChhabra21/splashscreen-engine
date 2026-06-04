# Required Modules
import requests

# Pre-Installed Modules
import platform
import datetime
import json
import uuid
from pathlib import Path
import os
from typing import Any


# Firebase Database URL
DATABASE_URL = "https://splashscreenanalytics-default-rtdb.europe-west1.firebasedatabase.app"


class Analyse:

    def __init__(self):

        # ------- MAKING FRAMEWORK FOLDER ----------

        # Getting File Path for Windows
        if platform.system() == "Windows":

            local_appdata = os.getenv("LOCALAPPDATA")
            if not local_appdata:
                # Unable to find app data, so don't break the framework and stop analytics
                self.success = False
                return
            self.APP_DIR = Path(local_appdata) / "SplashScreenEngine"


        # Getting File Path for Linux / macOS
        else:
            self.APP_DIR = Path.home() / ".SplashScreenEngine"

        self.success = True # File Path Created

        # Create Folder
        self.APP_DIR.mkdir(exist_ok=True)


        # JSON File Path
        self.DATA_FILE = self.APP_DIR / "SplashData.json"

        # Default Data Structure
        self.DATA: dict[str,Any] = {

            # Unique User ID
            "user_id": str(uuid.uuid4()),

            # OS type
            "OS": platform.system(),

            # Error Logs
            "errors": {},

            # Functions Used
            "functions_used": {},

            # Last Usage Time
            "last_usage": None,

            # Program running time (seconds)
            "runtime": None,

            # Total Runtime of module usage till it was installed
            "total_runtime": 0.0
        }


        # Other required variables
        self.start_time = None


        self.file_exists()
        self.start()


    # Checks if file exists and openable
    def file_exists(self):

        # Return if path not created
        if not self.success:
            return

        try :
            # Create JSON File if not exists
            if not self.DATA_FILE.exists():

                # Create JSON File
                with open(self.DATA_FILE, "w") as f:
                    json.dump(self.DATA, f, indent=4)

            # Save JSON File as dictionary in `DATA` variable if exists
            else:

                with open(self.DATA_FILE, "r") as f:
                    self.DATA = json.load(f)

        # If unable to create/read file
        except Exception as e:
            self.DATA["errors"][self.DATA["user_id"]] = str(e)
            self.success = False

    # Start Analyzing Data
    def start(self):

        # Return if path not created
        if not self.success:
            return

        self.start_time = datetime.datetime.now()

    # Store which functions used and store usage time
    def append_function(self,func_name):

        # Return if path not created
        if not self.success:
            return

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        self.DATA["functions_used"][current_time] = func_name

    # Store Errors
    def add_error(self,error):

        # Return if path not created
        if not self.success:
            return

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        self.DATA["errors"][current_time] = str(error)

    # save all the data at the end
    def save(self):

        if self.start_time is None:
            return

        # Return if path not created
        if not self.success:
            return

        current_time = datetime.datetime.now()
        runtime = (current_time - self.start_time).total_seconds()
        total_runtime = float(self.DATA["total_runtime"]) + float(runtime)
        current_time = current_time.strftime("%Y-%m-%d_%H-%M-%S-%f")

        self.DATA["total_runtime"] = total_runtime
        self.DATA["runtime"] = runtime
        self.DATA["last_usage"] = current_time


        try:
            response = requests.post(

                f"{DATABASE_URL}/analytics.json",

                json=self.DATA,

                timeout=3
            )
            response.raise_for_status()

        except Exception as e:
            self.add_error(e)


        # Save Everything in the json file
        try:
            with open(self.DATA_FILE, "w") as f:
                json.dump(self.DATA, f, indent=4)
        except Exception as e:
            self.add_error(e)


