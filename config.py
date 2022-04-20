class ConfigFile:
    def __init__(self, filename: str) -> None:
        from configparser import ConfigParser

        # edge cases
        if not type(filename) == str:
            raise TypeError('config filename must be a string')
        
        config_file = ConfigParser()
        config_file.read(filename)
        # if file is found and is not empty
        self.data = config_file if len(config_file) > 1 else None

        try:
            # other config data will go here
            self.database_credentials = dict(config_file['DATABASE_CREDENTIALS'])
        except KeyError:
            self.database_credentials = None
            raise Exception('config file is missing database credentials')





