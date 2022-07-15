import discord, os, shutil as sh, sys
from colorama import init
init()
from colorama import Fore, Back, Style
try:
    BotVersion = 2.3
    client = discord.Client()

    send_target = ""
    author = ""

    @client.event
    async def on_ready():
      print(Back.GREEN+f'Я подключился как {client.user}\nНа версии {BotVersion}')
      if not os.path.exists("savefiles/perm.txt"):
        if not os.path.exists("savefiles"):
          os.mkdir("savefiles")
        open("savefiles/perm.txt", "w").write("669188250568753154\n")
        print(Back.YELLOW+f"WARNING:\nЯ не нашел родных директорий и файлов,\nпо-этому я инициализировался в директории\n{os.getcwd()}\n")
        
    @client.event
    async def on_message(message):
      global send_target, author
      if message.author == client.user:
          return
      mes = message.content.split(" ")
      
      if not os.path.exists("savefiles/perm.txt"):
        if not os.path.exists("savefiles"):
          os.mkdir("savefiles")
        open("savefiles/perm.txt", "w").write("669188250568753154\n")
        print(Back.YELLOW+f"WARNING:\nЯ не нашел родных директорий и файлов,\nпо-этому я инициализировался в директории\n{os.getcwd()}\n")

      if send_target == "" and author == "":
        admin = False
        owner = False
        for i in open("savefiles/perm.txt", "r").read().split("\n"):
          if str(message.author.id) == i:
            admin = True
          if str(message.author.id) == "669188250568753154":
            owner = True

        if mes[0] == "perm":
          if admin or owner:
            if mes[1] == "del":
              idex =False
              perms = ""
              for i in open("savefiles/perm.txt", "r").read().split("\n"):
                if mes[2] == i:
                  idex = True
                else:
                  perms += f"{i}\n"
              
              if idex:
                await message.channel.send(f"Удалил {mes[2]} из спика админов")
                open("savefiles/perm.txt", "w").write(perms)
              else:
                await message.channel.send(f"Не нашел {mes[2]} в списке админов")
            if mes[1] == "add":
              if len(mes[2]) == 18:
                try:
                  int(mes[2])
                  open("savefiles/perm.txt", "a").write(mes[2]+"\n")
                  await message.channel.send(f"Добавил {mes[2]} в список админов")
                except:
                  await message.channel.send("Вы не правильно указали ID пользователя, он должен состоять только из цифр")
              else:
                await message.channel.send("Вы не правильно указали ID пользователя, он должен иметь длинну 18 символов")
            if mes[1] == "list":
              await message.channel.send(open("savefiles/perm.txt", "r").read())
          else:
            await message.channel.send("У вас нет прав на выполнение этой команды")
          #/perm (add/del) (userid) / perm list: Команда для управления административными правами пользователей, использующих бота (необходимы права администратора)#/
        if mes[0] == "getid":
          await message.channel.send(message.author.id)
          #/getid: Выдает ваш id#/
        if mes[0] == "remove":
          if admin or owner:
            try:
              for i in range(len(mes)):
                if i > 0:
                  os.remove("savefiles/"+mes[i])
                  await message.channel.send(f"Удалил файл savefiles/{mes[i]}")
            except FileNotFoundError:
              await message.channel.send(f"Я не нашел файл savefiles/{mes[1]}")
          else:
            await message.channel.send("У вас нет прав на выполнение этой команды")
          #/remove (filename): Команда для удаления файла из каталога файлов бота (необходимы права администратора)#/
        if mes[0] == "save":
          for attach in range(len(message.attachments)):
            try:
              await message.attachments[attach].save(f"savefiles/{mes[attach+1]}.{message.attachments[attach].filename.split('.')[1]}")
              await message.channel.send(f"Сохранил файл {attach+1} как {mes[attach+1]}.{message.attachments[attach].filename.split('.')[1]}")
            except IndexError:
              await message.channel.send("Укажи с каким именем мне сохранить этот файл: save yourname, или при сохранении в папку: save folder/yourname")
          #/save (filename): Команда для сохранения файла из сообщения в каталог файлов бота#/
        if mes[0] == "ls":
          ls = ""
          dmax = 0
          dirs = []
          files = []
          ls_count = 0
          if len(mes) > 1:
            try:
              for i in range(len(os.listdir("savefiles/"+mes[1]))):
                if "." in os.listdir("savefiles/"+mes[1])[i]:
                  files.append(os.listdir("savefiles/"+mes[1])[i])
                else:
                  dirs.append(os.listdir("savefiles/"+mes[1])[i])
              for i in range(len(dirs)):
                if i == 0:
                  dmax = len(dirs[i])
                else:
                  if len(dirs[i]) > dmax:
                    dmax = len(dirs[i])
              for i in dirs:
                ls_count += 1
                ls += i+" "*(dmax-len(i)+2)
                if ls_count == 3:
                  ls += "\n"
                  ls_count = 0
              if ls_count != 0:
                ls += "\n"
              ls_count = 0
              for i in range(len(files)):
                if i == 0:
                  dmax = len(files[i])
                else:
                  if len(files[i]) > dmax:
                    dmax = len(files[i])
              for i in files:
                ls_count += 1
                ls += i+" "*(dmax-len(i)+2)
                if ls_count == 3:
                  ls += "\n"
            except FileNotFoundError:
              await message.channel.send(f"Не нашел папку savefiles/{mes[1]}")
          else:
            try:
              for i in range(len(os.listdir("savefiles"))):
                if "." in os.listdir("savefiles")[i]:
                  files.append(os.listdir("savefiles")[i])
                else:
                  dirs.append(os.listdir("savefiles")[i])
              for i in range(len(dirs)):
                if i == 0:
                  dmax = len(dirs[i])
                else:
                  if len(dirs[i]) > dmax:
                    dmax = len(dirs[i])
              for i in dirs:
                ls_count += 1
                ls += i+" "*(dmax-len(i)+2)
                if ls_count == 3:
                  ls += "\n"
                  ls_count = 0
              if ls_count != 0:
                ls += "\n"
              ls_count = 0
              for i in range(len(files)):
                if i == 0:
                  dmax = len(files[i])
                else:
                  if len(files[i]) > dmax:
                    dmax = len(files[i])
              for i in files:
                ls_count += 1
                ls += i+" "*(dmax-len(i)+2)
                if ls_count == 3:
                  ls += "\n"
            except FileNotFoundError:
              await message.channel.send(f"Не нашел папку savefiles/{mes[1]}")
          try:
            await message.channel.send(ls)
          except discord.errors.HTTPException:
                await message.channel.send(f"Папка savefiles/{mes[1]} пустая")
          except UnboundLocalError:
            pass
          #/ls / ls (dirname): Команда для просмотра файлов в директории из каталога файлов бота#/
        if mes[0] == "open":
          try:
            await message.channel.send(file=discord.File("savefiles/"+mes[1]))
          except FileNotFoundError:
            await message.channel.send(f"Не нашел файл savefiles/{mes[1]}")
          #/open (filename): Команда, которая высылает файл из каталога файлов бота#/
        if mes[0] == "mkdir":
          try:
            os.mkdir(f"savefiles/{mes[1]}")
            await message.channel.send(f"создал папку savefiles/{mes[1]}")
          except FileExistsError:
            await message.channel.send(f"Папка {mes[1]} уже существует")
          #/mkdir (dirname): Команда для создания папки в каталоге файлов бота#/
        if mes[0] == "rmdir":
          if admin or owner:
            try:
              try:
                for i in os.listdir(f"savefiles/{mes[1]}"):
                  os.remove(f"savefiles/{mes[1]}/{i}")
              except:
                pass
              os.rmdir("savefiles/"+mes[1])
              await message.channel.send(f"удалил папку savefiles/{mes[1]}")
            except FileNotFoundError:
              await message.channel.send(f"Я не нашел файл savefiles/{mes[1]}")
          else:
            await message.channel.send("У вас нет прав на выполнение этой команды")
          #/rmdir (dirname): Команда для удаления папки из каталога файлов бота (необходимы права администратора)#/
        if mes[0] == "mktxt":
          txt = ""
          for i in range(len(mes)):
            if i > 1:
              txt += f"{mes[i]} "
          open("savefiles/"+mes[1]+".txt", "w").write(txt)
          await message.channel.send(f"Создал файл {mes[1]}.txt")
          #/mktxt (filename) (text): Команда для создания текстового файла в каталоге файлов бота#/
        if mes[0] == "rename":
          if admin or owner:
            try:
              os.rename("savefiles/"+mes[1], "savefiles/"+mes[2])
              await message.channel.send(f"Переименовал файл savefiles/{mes[1]} в savefiles/{mes[2]}")
            except FileNotFoundError:
              await message.channel.send(f"Я не нашел файла savefiles/{mes[1]}")
          else:
            await message.channel.send("У вас нет прав на выполнение этой команды")
          #/rename (file1) (file2): Команда для изменения имени файла в каталоге файлов бота (необходимы права администратора)#/
        if message.content == "savebot":
          if owner:
            sh.make_archive("DiscordBot", "zip", "savefiles")
            await message.channel.send(f"Сохраняю бота {BotVersion}")
            await message.channel.send(file=discord.File("DiscordBot.zip"))
            await message.channel.send(file=discord.File("main.py"))
          else:
            await message.channel.send("У вас нет прав на выполнение этой команды")
          #/savebot: Команда для того, чтобы бот выслал свой код и каталог файлов (необходимы права создателя)#/
        if message.content == "update":
          if owner:
            if len(message.attachments) == 1:
              for attach in message.attachments:
                await attach.save(f"bot.py")
              await message.channel.send("Загрузил обновленный код")
            else:
              await message.channel.send("Прекрепи 1 файл с кодом, который нужно загрузить")
          else:
            await message.channel.send("У вас нет прав на выполнение этой команды")
          #/update: Команда для обновления кода бота (необходимы права создателя)#/
        if message.content == "reload":
          if owner:
            open("out.txt", "w").write("reload")
            await message.channel.send("Перезагружаюсь...")
            await client.close()
          else:
            await message.channel.send("У вас нет прав на выполнение этой команды")
          #/reload: Команда для перезапуска бота, и загрузки необходимых обновлений (необходимы права создателя)#/
        if message.content == "help":
          helpmsg = f"Я Скайнет {BotVersion}, для взаимодействия со мной создатель составил список команд, смотри:\n-------------------\n"
          cmds = open("bot.py", "r", encoding="utf-8").read().split("#/")#/
          for i in range(len(cmds)):
            if i%2 != 0 and cmds[i] != '")':
              helpmsg += f"{cmds[i]}\n-------------------\n"
          await message.channel.send(helpmsg)
          #/help: Команда для вывода этого сообщения#/
        #/startcom (userid) / stopcom: Команды для общения с человеком через бота, он пишел личные сообщения в лс жертве (необходимы права администратора)#/
        
      else:
        if message.author == send_target:
          await author.send(message.content)
        if message.author == author:
          send_mes = ""
          for i in mes:
                send_mes += f"{i} "
          if send_mes != "stopcom":
            await send_target.send(send_mes)
        
      if mes[0] == "startcom":
        if len(mes) == 2:
          send_target = await client.fetch_user(int(mes[1]))
          author = message.author
          await message.channel.send(f"Начал общение с <@{send_target.id}>")
      if mes[0] == "stopcom":
        author = ""
        await message.channel.send(f"перестал писать <@{send_target.id}>")
        send_target = ""
    client.run("OTIyOTIxMDM2MjkzNDgwNTEw.GB3LvF.Lj_98Szac32ZFN2Q0x4V0DpXjUDG6yDkGzhjDM")
except Exception as ex:
    print(Back.RED+"ERROR"+str(ex))