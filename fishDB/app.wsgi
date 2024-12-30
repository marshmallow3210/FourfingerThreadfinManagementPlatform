# 載入虛擬環境
activate_this = '/var/www/html/fishDB/fishenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# 載入 Flask 應用程式
from fishapp import app as application

