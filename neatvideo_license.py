import getpass
import os
import platform


class NeatVideoFloatingLicense(object):
    def __init__(self, license_server, port):
        """This script will check if a license file is set on Windows,
        and if not, create the file so the user won't have to set it up.

        This will also allow Neat Video to run on render farms."""

        # Only run this script on Windows
        if platform.system() == "Windows":
            user_name = getpass.getuser()
            license_path = os.path.join(
                "C:",
                "users",
                user_name,
                "AppData",
                "Roaming",
                "NeatVideo5 OFX 64",
                "RLM",
                "neatclient.lic",
            )

            # Fix for Windows
            license_path = license_path.replace(os.sep, "/")

            # If file is not validated, create license file
            if not self.__check_license(license_path, license_server, port):
                self.__generate_license_file(
                    license_path, license_server, port
                )

    def __check_license(self, license_path, license_server, port):
        """Checks if license is existing and is correct

        Args:
            license_path (str): path to file for license file
            license_server (str): floating license server
            port (int): server port

        Returns:
            bool: If True, license exists, if false, license doesn't exist
        """

        # If license file exist, check if file is valid
        if os.path.isfile(license_path):
            license_file = open(license_path, "r", encoding="utf-8")
            license_information = license_file.read()

            # Check if license server is existing in file
            if license_server in license_information:
                # Check if port is existing in file
                if str(port) in license_information:

                    # If everything exists, file is valid
                    self.__logger("License exists")
                    return True

        # If file is not correct or doesn't exist, return invalidated
        self.__logger("License doesn't exist")
        return False

    def __generate_license_file(self, license_path, license_server, port):
        """Creates license file using specified parameters

        Args:
            license_path (str): path to file for license file
            license_server (str): floating license server
            port (int): server port
        """
        # First make sure we got all the directories
        # necessary to create the file

        self.__logger("Creating license file")

        # Get folder for license file to create and check
        license_folder = os.path.dirname(license_path)

        # If folder doesn't exist, create every folder
        if not os.path.isdir(license_folder):
            self.__logger("Directory created")
            os.makedirs(license_folder)

        try:
            # Create license file
            license_file = open(license_path, "w", encoding="utf-8")
            license_file.write(
                "SERVER %s ANY %s" % (license_server, str(port))
            )
            license_file.close()
            self.__logger("License file created")

        # If any exception occured, throw error
        except Exception as exception:
            self.__logger(str(exception))

    @staticmethod
    def __logger(log):
        """Logger with correct formatting for printing

        Args:
            log (str): message to print to logger
        """

        # Logging message formatting
        log = "[NeatVideo] %s" % log
        print(log)
