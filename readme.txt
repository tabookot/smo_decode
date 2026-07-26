========================================================================
 ScanMyOpel log decoder | Расшифровщик логов ScanMyOpel (.smo в .txt)
========================================================================
(English version below from line 130)

Совместимо с "ScanMyOpel 1.1.36". Если не работает - все претензии к электроовцам!
Для работы скриптов требуется установленный Python 3.6 или выше.

------------------------------------------------------------------------
 КОРОТКО (QUICK START)
------------------------------------------------------------------------
1. Подключить совместимый OBD2 к телефону.
2. В приложении ScanMyOpel:
   - Левое меню -> Установки -> выбрать протокол и свой OBD2.
   - Выбрать год, модель, КП -> подключиться.
   - Левое меню:
     * Поставить галку "включить" для начала записи лога.
     * Делать с авто всё, что хочется проверить.
     * В конце выключить галку.
     * Нажать Send Logs - переправить архив на компьютер.
3. На компьютере:
   - Скачать скрипты (с GitHub или в виде ZIP-архива).
   - Из zip архива (присланного с телефона) достать файлы 
     ScanMyOpel_Logging_Global__[дата_время].smo и положить их рядом со скриптами.
   - Доступны два варианта скриптов:
     smo_decode - простой декодер в txt, просто сырая расшифровка.
     smo_decode_plus - убирает мусор, строит псевдо-табличку и текстовые графики.
   - Файлы .py - сами скрипты, файлы .bat - для запуска под Windows двойным кликом.


------------------------------------------------------------------------
 КАК СКАЧАТЬ СКРИПТЫ С GITHUB
------------------------------------------------------------------------
1. Зайдите на страницу проекта: https://github.com/tabookot/smo_decode
2. Найдите зеленую кнопку "<> Code" и нажмите на неё.
3. В появившемся меню выберите "Download ZIP".
4. Скачается архив. Распакуйте его в любую папку на компьютере.
5. Внутри распакованной папки будут лежать нужные файлы .py и .bat.
   (Если у вас установлен Git, используйте команду: 
    git clone https://github.com/tabookot/smo_decode.git)


------------------------------------------------------------------------
 ПОДРОБНАЯ ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ
------------------------------------------------------------------------
Скрипт smo_decode_plus читает закрытые файлы логов приложения ScanMyOpel (*.smo),
расшифровывает их, очищает от служебного мусора, объединяет повторяющиеся
циклы опроса в единую таблицу и строит текстовые графики (спарклайны)
для цифровых параметров.

1. ТРЕБОВАНИЯ К СИСТЕМЕ
- ОС: Windows, macOS или Linux.
- Python: версия 3.6 или выше.
- Дополнительные библиотеки: НЕ ТРЕБУЮТСЯ.

2. УСТАНОВКА PYTHON

>>> ДЛЯ WINDOWS:
1. Зайдите на официальный сайт: https://www.python.org/downloads/
2. Скачайте последнюю версию Python 3.
3. Запустите скачанный установщик.
4. ВАЖНО: В самом низу окна установщика ОБЯЗАТЕЛЬНО поставьте галочку
   "Add python.exe to PATH" (Добавить Python в PATH).
5. Нажмите "Install Now" и дождитесь окончания установки.

>>> ДЛЯ macOS:
1. Откройте приложение "Терминал".
2. Если у вас установлен пакетный менеджер Homebrew, выполните команду:
   brew install python
3. Если Homebrew нет, скачайте установщик с https://www.python.org/downloads/

>>> ДЛЯ LINUX (Ubuntu/Debian):
   sudo apt update
   sudo apt install python3

>>> ДЛЯ LINUX (Fedora/RHEL):
   sudo dnf install python3

3. ПОДГОТОВКА ФАЙЛОВ
1. Распакуйте скачанный архив со скриптами в удобную папку (например, OpelLogs).
2. Скопируйте файлы логов из приложения ScanMyOpel (файлы .smo) в эту же папку,
   рядом со скриптами.

4. ЗАПУСК СКРИПТА
Откройте Терминал (в Windows - "Командная строка" или "PowerShell") и укажите путь к папке.

--- Способ А: Расшифровать сразу ВСЕ файлы .smo в папке ---
(Скрипт автоматически найдет все файлы .smo рядом с собой)

1. В терминале перейдите в папку со скриптом командой cd:
   Windows:  cd %USERPROFILE%\Desktop\OpelLogs
   macOS:    cd ~/Desktop/OpelLogs
   Linux:    cd ~/Desktop/OpelLogs

2. Запустите скрипт:
   Windows:  python smo_decode_plus.py
   macOS:    python3 smo_decode_plus.py
   Linux:    python3 smo_decode_plus.py

--- Способ Б: Расшифровать только ОДИН конкретный файл ---

1. В терминале перейдите в папку со скриптом (см. выше пункт 1).
2. Запустите скрипт, указав имя файла:
   Windows:  python smo_decode_plus.py my_log.smo
   macOS:    python3 smo_decode_plus.py my_log.smo
   Linux:    python3 smo_decode_plus.py my_log.smo

5. ГДЕ ИСКАТЬ РЕЗУЛЬТАТ?
После успешного выполнения скрипта в той же папке появятся новые текстовые
файлы с таким же именем, но с расширением .txt. Откройте их в любом редакторе.
СОВЕТ: Для удобного просмотра таблиц используйте редакторы с моноширинным
шрифтом (Notepad++, VS Code) и отключите перенос строк.

6. ВОЗМОЖНЫЕ ПРОБЛЕМЫ
- Ошибка: "python: команда не найдена" или "python is not recognized"
  Решение: Вы не поставили галочку "Add to PATH" при установке Python (на Windows).
           Либо используйте команду python3 вместо python.

- Ошибка: "FileNotFoundError"
  Решение: Вы пытаетесь запустить скрипт не из той папки, где лежат файлы .smo,
           либо неверно указали имя файла.

ВНИМАНИЕ ПО ПОВОДУ СОДЕРЖИМОГО ЛОГОВ:
Если в логе приложения ScanMyOpel были записаны только "сырые" данные
(строки вида "80 F1 18 22 61 01...") без текстовых названий параметров,
скрипт обработает такой лог, но раздел "Живые данные" будет пустым.


========================================================================
 SCANMYOPEL LOG DECODER
========================================================================

Compatible with "ScanMyOpel 1.1.36". If it doesn't work - direct all 
complaints to the electric sheep!
The scripts require Python 3.6 or higher to be installed.


------------------------------------------------------------------------
 QUICK START
------------------------------------------------------------------------
1. Connect a compatible OBD2 to your phone.
2. In the ScanMyOpel app:
   - Left menu -> Settings -> select protocol and your OBD2.
   - Select year, model, transmission -> connect.
   - Left menu:
     * Check the "enable" box to start recording the log.
     * Do whatever you want to test on the car.
     * Uncheck the box at the end.
     * Click Send Logs - send the archive to your computer.
3. On your computer:
   - Download the scripts (from GitHub or as a ZIP archive).
   - Extract the files ScanMyOpel_Logging_Global__[date_time].smo from 
     the .zip archive (sent from the phone) and place them next to the scripts.
   - Two script options are available:
     smo_decode - a simple decoder to txt, just raw decoding.
     smo_decode_plus - removes garbage, builds a pseudo-table and text 
       graphs (sparklines).
   - .py files are the scripts themselves, .bat files are for launching 
     on Windows with a double-click.


------------------------------------------------------------------------
 HOW TO DOWNLOAD THE SCRIPTS FROM GITHUB
------------------------------------------------------------------------
1. Go to the project page: https://github.com/tabookot/smo_decode
2. Find the green "<> Code" button and click it.
3. In the menu that appears, select "Download ZIP".
4. The archive will be downloaded. Extract it to any folder on your computer.
5. Inside the extracted folder, you will find the required .py and .bat files.
   (If you have Git installed, use the command: 
    git clone https://github.com/tabookot/smo_decode.git)


------------------------------------------------------------------------
 DETAILED INSTRUCTIONS FOR USE
------------------------------------------------------------------------
The smo_decode_plus script reads the closed log files of the ScanMyOpel 
application (*.smo), decodes them, cleans them from service garbage, 
combines repeated polling cycles into a single table, and builds text 
graphs (sparklines) for digital parameters.

1. SYSTEM REQUIREMENTS
- OS: Windows, macOS, or Linux.
- Python: version 3.6 or higher.
- Additional libraries: NOT REQUIRED.

2. INSTALLING PYTHON

>>> FOR WINDOWS:
1. Go to the official website: https://www.python.org/downloads/
2. Download the latest version of Python 3.
3. Run the downloaded installer.
4. IMPORTANT: At the bottom of the installer window, MAKE SURE to check 
   the box "Add python.exe to PATH".
5. Click "Install Now" and wait for the installation to finish.

>>> FOR macOS:
1. Open the "Terminal" app.
2. If you have the Homebrew package manager installed, run the command:
   brew install python
3. If you don't have Homebrew, download the installer from 
   https://www.python.org/downloads/

>>> FOR LINUX (Ubuntu/Debian):
   sudo apt update
   sudo apt install python3

>>> FOR LINUX (Fedora/RHEL):
   sudo dnf install python3

3. PREPARING THE FILES
1. Extract the downloaded archive with scripts to a convenient folder 
   (e.g., OpelLogs).
2. Copy the log files from the ScanMyOpel app (files with the .smo 
   extension) to the same folder, next to the scripts.

4. RUNNING THE SCRIPT
Open a Terminal (in Windows - "Command Prompt" or "PowerShell") and 
specify the path to your folder.

--- Method A: Decode ALL .smo files in the folder at once ---
(The script will automatically find all .smo files next to itself)

1. In the terminal, navigate to the folder with the script using the cd command:
   Windows:  cd %USERPROFILE%\Desktop\OpelLogs
   macOS:    cd ~/Desktop/OpelLogs
   Linux:    cd ~/Desktop/OpelLogs

2. Run the script:
   Windows:  python smo_decode_plus.py
   macOS:    python3 smo_decode_plus.py
   Linux:    python3 smo_decode_plus.py

--- Method B: Decode only ONE specific file ---

1. In the terminal, navigate to the folder with the script (see step 1 above).
2. Run the script, specifying the file name:
   Windows:  python smo_decode_plus.py my_log.smo
   macOS:    python3 smo_decode_plus.py my_log.smo
   Linux:    python3 smo_decode_plus.py my_log.smo

5. WHERE TO FIND THE RESULT?
After the script successfully executes, new text files with the same name 
but with a .txt extension will appear in the same folder. Open them in any 
text editor.
TIP: For convenient viewing of tables without distorting the columns, open 
the file in editors with a monospaced font (Notepad++, VS Code) and turn 
off word wrapping.

6. POSSIBLE ISSUES
- Error: "python: command not found" or "python is not recognized"
  Solution: You didn't check the "Add to PATH" box during Python 
            installation (on Windows). Alternatively, use the python3 
            command instead of python.

- Error: "FileNotFoundError"
  Solution: You are trying to run the script from the wrong folder where 
            the .smo files are located, or you specified the file name 
            incorrectly.

NOTE REGARDING LOG CONTENTS:
If the ScanMyOpel app log recorded only "raw" data (lines like 
"80 F1 18 22 61 01...") without text parameter names, the script will 
process such a log, but the "Live data" section will be empty.
