from app import kekaLoginLogout
import schedule
import time

schedule.every().day.at("20:45").do(kekaLoginLogout, False)
schedule.every().day.at("09:15").do(kekaLoginLogout, True)

while True:
     schedule.run_pending()
     time.sleep(1)