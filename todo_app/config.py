class Configuration:
    def __init__(self, db_user, db_pass, db_host, db_port, db_name, secret_key):
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.secret = secret_key
