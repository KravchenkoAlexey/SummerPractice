import requests

COOKIES = {
    'yasosu_session': 'f35bbafd7aad7d5d88ad2761e409ae4d',
}

YASOSU__BASE_URL: str = 'https://api.yaso.su/v1/records'


def yasosu__paste(content: str) -> str:
    json_data = {
        'content': content,
        'codeLanguage': 'auto',
        'captcha': '03AFcWeA4xpfpFXgb-zHL0LAuriuYAYWYmhdl818MmB50dFstlKB-9_ilqiQfffupMcZCSN8W5c3T5IuH4e4_lpuksTM08eikYYNbZUddoCtgiPJ8t83_t4L8gaOXYvlP5ay4JpdV8i3S8qMNKFmhCQglxuxNVIYSd_Ay00I3GkxgqbND6UThwwRPYizAEOPVekDF9kuAXrq-Hb6Pbpl7Eun6KGe8TKY0mwSeMbx08LPffdq5jGhcawV1wRr7-ExVcJjboUG3SaouWM9wGpZnSoH_Rzlq_sgcXDCv6CEsDX80jrgRkttpbjHySFD297oeUBrVxdGC446_Q2CzCKC6kC0d7Np7sXoggItWI4JjLXtadxaWMXaeHkmmUYPTKUaMQ47jmTBOKLhB1JMohN3Xuv5zn-UBQKUh4liwPBdR1dt1klnoE9OR2XbZZF33viTran4P0M42qpNCorjjzmhQWv6sh3BUojOMTz_s19lavpWA1vLYzT0Z18ZWQ-J7DuC-hNAkMi_B5gqdNj2S0yWwkE8qHaF_H96yp45Sv06w-5QbfWIKh9nxRCHnr4q4Iis5peAK9pkcZDhX5rIdPtr1P5_nQfm2kj3pOMROSkpO5ceOBr6Nqidfqi18loRGlndYsz3z-byQMeJsaEggDqLW1NV8558DKl2plxw',
        'expirationTime': -1,
    }
    return "https://yaso.su/" + requests.post(YASOSU__BASE_URL, cookies=COOKIES, json=json_data).json()['url']
