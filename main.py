import os
open("out.txt", "w").write("reload")
while True:
    try:
      if open("out.txt", "r").read() == "reload":
        open("out.txt", "w").write("none")
        os.system("bot.py")
      if open("out.txt", "r").read() == "shutdown":
        open("out.txt", "w").write("none")
        exit()
    except FileNotFoundError:
      open("out.txt", "w").write("reload")