import pymysql
pymysql.version_info = (1, 4, 3, "final", 0) # Ensure Bootstrap v5 compatibility
pymysql.install_as_MySQLdb()