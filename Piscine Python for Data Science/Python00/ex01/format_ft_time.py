import time
import datetime
import locale

locale.setlocale(locale.LC_ALL, '')

date = time.time()
date_entier = int(date)
date_decimal = date - date_entier

date_format = locale.format_string("%d", date_entier, grouping=True)
date_format += "{:.9f}".format(date_decimal)[1:]

print("Seconds since January 1, 1970:", date_format, "or",
      '{:.2e}'.format(date), "in scientific notation\n",
      datetime.datetime.fromtimestamp(time.time()).strftime('%b %d %Y'))
