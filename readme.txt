========================================================================
 ScanMyOpel log decoder | Расшифровщик логов ScanMyOpel (.smo в .txt)
========================================================================
(English version below from line 190)

Совместимо с ScanMyOpel (https://scanmyopel.com) 1.1.36.
Если не работает — все претензии к электроовцам! ;-)
Авторский коллектив — GPT 5.5, GLM 5.2 и Kimi K3.

Для работы скриптов требуется установленный Python 3.6 или выше.

----------------------------------------------------------------
 🚀 КОРОТКО (QUICK START)
----------------------------------------------------------------

1. Подключить совместимый OBD2 к телефону.
2. В приложении ScanMyOpel:
   - Левое меню ➔ Установки ➔ выбрать протокол и свой OBD2.
   - Выбрать год, модель, КП ➔ подключиться.
   - Левое меню:
     - Поставить галку "включить" для начала записи лога.
     - Делать с авто всё, что хочется проверить.
     - В конце выключить галку.
     - Нажать Send Logs — переправить архив на компьютер.
3. На компьютере:
   - Скачать скрипты с этого сайта (см. инструкцию ниже).
   - Из .zip архива (присланного с телефона) достать файлы 
     ScanMyOpel_Logging_Global__[дата_время].smo и положить их 
     рядом со скриптами.
   - Доступны два варианта скриптов:
     - smo_decode 0.1.4 — простой декодер в .txt, просто сырая 
       расшифровка.
     - smo_decode_plus 0.2.13 — убирает мусор, строит таблицы и 
       графики. Поддерживает вывод в .txt (спарклайны) и .xlsx 
       (Excel с цветными графиками).
   - Файлы .py — сами скрипты, файлы .bat — для запуска под 
     Windows двойным кликом.

----------------------------------------------------------------
 ⬇️ КАК СКАЧАТЬ СКРИПТЫ
----------------------------------------------------------------

Так как это открытое хранилище кода, скачать программу можно 
двумя способами:

Способ 1: Скачать ZIP-архив (Самый простой, для всех)
1. На главной странице проекта (нажмите на логотип GitHub в 
   левом верхнем углу, чтобы перейти в корень репозитория).
2. Найдите зеленую кнопку <> Code и нажмите на неё.
3. В появившемся меню выберите Download ZIP.
4. Скачается архив smo_decode-main.zip. Распакуйте его в любую 
   папку на компьютере (например, на Рабочий стол).
5. Внутри распакованной папки будут лежать нужные файлы .py и .bat.

Способ 2: Через Git (Для продвинутых пользователей)
Если у вас установлен Git, выполните в терминале:
   git clone https://github.com/tabookot/smo_decode.git

----------------------------------------------------------------
 📖 ПОДРОБНАЯ ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ
----------------------------------------------------------------

Скрипт smo_decode_plus читает закрытые файлы логов приложения 
ScanMyOpel (https://scanmyopel.com) (*.smo), расшифровывает их, 
очищает от служебного мусора и объединяет повторяющиеся циклы 
опроса в единую таблицу.

Доступны два формата вывода (задается ключами --txt или --xlsx):
- Текстовый (.txt): строит псевдо-таблицы и текстовые графики 
  (спарклайны) для цифровых параметров.
- Excel (.xlsx): формирует транспонированную таблицу Live Data и 
  строит наглядные графики.

1. Требования к системе
- ОС: Windows, macOS или Linux.
- Python: версия 3.6 или выше.
- Дополнительные библиотеки: Для базового .txt вывода НЕ 
  ТРЕБУЮТСЯ. Для генерации Excel-отчетов (.xlsx) нужен модуль 
  openpyxl (скрипт предложит установить его автоматически при 
  первом запуске с ключом --xlsx).

2. Установка Python

Для Windows:
1. Зайдите на официальный сайт: https://www.python.org/downloads/
2. Скачайте последнюю версию Python 3 (кнопка "Download Python 3.x.x").
3. Запустите скачанный установщик.
4. ВАЖНО: В самом низу окна установщика ОБЯЗАТЕЛЬНО поставьте 
   галочку "Add python.exe to PATH".
5. Нажмите "Install Now" и дождитесь окончания установки.

Для macOS:
1. Откройте приложение "Терминал" (Command + Пробел ➔ Терминал).
2. Если у вас установлен пакетный менеджер Homebrew (рекомендуется), 
   выполните команду:
   brew install python
3. Если Homebrew нет, скачайте установщик с 
   https://www.python.org/downloads/ и установите как обычную программу.

Для Linux (Ubuntu/Debian):
   sudo apt update
   sudo apt install python3

Для Linux (Fedora/RHEL):
   sudo dnf install python3

3. Подготовка файлов
1. Если вы скачали ZIP-архив (см. раздел "Как скачать"), распакуйте 
   его в удобную папку (например, OpelLogs на Рабочем столе).
2. Скопируйте файлы логов из приложения ScanMyOpel (файлы с 
   расширением .smo) и положите их в эту же папку, рядом со 
   скриптами smo_decode_plus.py и smo_decode.py.

4. Запуск скрипта

Вам нужно открыть Терминал (в Windows — "Командная строка" или 
"PowerShell", в macOS/Linux — "Терминал") и указать путь к вашей 
папке.

Способ А: Расшифровать сразу ВСЕ файлы .smo в папке
(Скрипт автоматически найдет все файлы .smo рядом с собой)

1. В терминале перейдите в папку со скриптом командой cd:
   cd %USERPROFILE%\Desktop\OpelLogs
2. Запустите скрипт:

   Windows (простой текстовый вывод):
   python smo_decode_plus.py

   Windows (вывод в Excel с графиками):
   python smo_decode_plus.py --xlsx

   macOS / Linux (простой текстовый вывод на русском):
   python3 smo_decode_plus.py -l ru

Способ Б: Расшифровать только ОДИН конкретный файл

1. В терминале перейдите в папку со скриптом (см. выше пункт 1).
2. Запустите скрипт, указав имя файла:

   Windows:
   python smo_decode_plus.py my_log.smo

   macOS / Linux:
   python3 smo_decode_plus.py my_log.smo

СОВЕТ: Вы также можете добавить ключ -l ru или -l en, чтобы 
выбрать язык заголовков в отчете (по умолчанию en).

5. Где искать результат?

После успешного выполнения скрипта в той же папке появятся новые 
файлы отчетов с таким же именем, но с расширением .txt (по 
умолчанию) или .xlsx (если запускали с ключом --xlsx).

Например, если вы обработали файл log_2023.smo, рядом появится 
файл log_2023.txt или log_2023.xlsx. Откройте его в любом 
текстовом редакторе ("Блокнот", Notepad++) или в Microsoft Excel / 
LibreOffice Calc.

СОВЕТ: Для удобного просмотра текстовых таблиц без искажения 
колонок открывайте файл в редакторах с моноширинным шрифтом 
(например, Notepad++, VS Code или стандартный Блокнот) и включите 
отображение без переноса строк.

6. Возможные проблемы

Ошибка: python: команда не найдена или python is not recognized
Решение: Вы не поставили галочку "Add to PATH" при установке 
Python (на Windows). Либо используйте команду python3 вместо python.

Ошибка: FileNotFoundError
Решение: Вы пытаетесь запустить скрипт не из той папки, где лежат 
файлы .smo, либо неверно указали имя файла.

Ошибка: Ошибка установки openpyxl при запуске с --xlsx
Решение: Убедитесь, что у вас есть доступ к интернету, или 
установите библиотеку вручную командой:
   pip install openpyxl

ВНИМАНИЕ ПО ПОВОДУ СОДЕРЖИМОГО ЛОГОВ:
Если в логе приложения ScanMyOpel были записаны только "сырые" 
данные (строки вида 80 F1 18 22 61 01...) без текстовых названий 
параметров, скрипт обработает такой лог, но раздел "Живые данные" 
будет пустым, так как приложению не удалось записать имена параметров.



================================================================
 SCANMYOPEL LOG DECODER
================================================================

Compatible with ScanMyOpel (https://scanmyopel.com) 1.1.36.
If it doesn't work, blame the electric sheep! ;-)
Authors' collective — GPT 5.5, GLM 5.2, and Kimi K3.

The scripts require Python 3.6 or higher to be installed.

----------------------------------------------------------------
 🚀 QUICK START
----------------------------------------------------------------

1. Connect a compatible OBD2 adapter to your phone.
2. In the ScanMyOpel app:
   - Left menu ➔ Settings ➔ select protocol and your OBD2.
   - Select year, model, transmission ➔ connect.
   - Left menu:
     - Check the "enable" box to start logging.
     - Do whatever you want to test on the car.
     - Uncheck the box at the end.
     - Press Send Logs — send the archive to your computer.
3. On the computer:
   - Download the scripts from this repository (see instructions below).
   - Extract the ScanMyOpel_Logging_Global__[date_time].smo files 
     from the .zip archive (sent from the phone) and place them 
     next to the scripts.
   - Two script options are available:
     - smo_decode 0.1.4 — a simple decoder to .txt, just raw decoding.
     - smo_decode_plus 0.2.13 — removes garbage, builds tables and 
       graphs. Supports output to .txt (sparklines) and .xlsx (Excel 
       with colored charts).
   - .py files are the scripts themselves, .bat files are for 
     running on Windows via double-click.

----------------------------------------------------------------
 ⬇️ HOW TO DOWNLOAD THE SCRIPTS
----------------------------------------------------------------

Since this is an open code repository, you can download the program 
in two ways:

Method 1: Download ZIP archive (Easiest, for everyone)
1. On the main project page (click the GitHub logo in the top left 
   corner to go to the repository root).
2. Find the green <> Code button and click it.
3. In the appearing menu, select Download ZIP.
4. The smo_decode-main.zip archive will be downloaded. Extract it 
   to any folder on your computer (e.g., Desktop).
5. Inside the extracted folder, you will find the required .py and 
   .bat files.

Method 2: Via Git (For advanced users)
If you have Git installed, run in the terminal:
   git clone https://github.com/tabookot/smo_decode.git

----------------------------------------------------------------
 📖 DETAILED USAGE INSTRUCTIONS
----------------------------------------------------------------

The smo_decode_plus script reads the proprietary log files of the 
ScanMyOpel (https://scanmyopel.com) app (*.smo), decodes them, 
cleans them from service garbage, and combines repeated polling 
cycles into a single table.

Two output formats are available (set by --txt or --xlsx keys):
- Text (.txt): builds pseudo-tables and text graphs (sparklines) 
  for numeric parameters.
- Excel (.xlsx): generates a transposed Live Data table and builds 
  visual charts.

1. System Requirements
- OS: Windows, macOS, or Linux.
- Python: version 3.6 or higher.
- Additional libraries: NOT REQUIRED for basic .txt output. To 
  generate Excel reports (.xlsx), the openpyxl module is needed 
  (the script will offer to install it automatically on the first 
  run with the --xlsx key).

2. Python Installation

For Windows:
1. Go to the official website: https://www.python.org/downloads/
2. Download the latest version of Python 3 ("Download Python 3.x.x" button).
3. Run the downloaded installer.
4. IMPORTANT: At the bottom of the installer window, make sure to 
   check the "Add python.exe to PATH" box.
5. Click "Install Now" and wait for the installation to finish.

For macOS:
1. Open the "Terminal" app (Command + Space ➔ Terminal).
2. If you have the Homebrew package manager installed (recommended), 
   run the command:
   brew install python
3. If you don't have Homebrew, download the installer from 
   https://www.python.org/downloads/ and install it as a regular 
   application.

For Linux (Ubuntu/Debian):
   sudo apt update
   sudo apt install python3

For Linux (Fedora/RHEL):
   sudo dnf install python3

3. File Preparation
1. If you downloaded the ZIP archive (see "How to download" section), 
   extract it to a convenient folder (e.g., OpelLogs on your Desktop).
2. Copy the log files from the ScanMyOpel app (files with the .smo 
   extension) and place them in the same folder, next to the 
   smo_decode_plus.py and smo_decode.py scripts.

4. Running the Script

You need to open a Terminal (in Windows — "Command Prompt" or 
"PowerShell", in macOS/Linux — "Terminal") and navigate to your folder.

Method A: Decode ALL .smo files in the folder at once
(The script will automatically find all .smo files next to itself)

1. In the terminal, navigate to the folder with the script using 
   the cd command:
   cd %USERPROFILE%\Desktop\OpelLogs
2. Run the script:

   Windows (simple text output):
   python smo_decode_plus.py

   Windows (Excel output with charts):
   python smo_decode_plus.py --xlsx

   macOS / Linux (simple text output in Russian):
   python3 smo_decode_plus.py -l ru

Method B: Decode only ONE specific file

1. In the terminal, navigate to the folder with the script (see 
   step 1 above).
2. Run the script, specifying the file name:

   Windows:
   python smo_decode_plus.py my_log.smo

   macOS / Linux:
   python3 smo_decode_plus.py my_log.smo

TIP: You can also add the -l ru or -l en key to select the language 
of the headers in the report (defaults to en).

5. Where to find the result?

After successful execution of the script, new report files with 
the same name but with a .txt extension (by default) or .xlsx (if 
run with the --xlsx key) will appear in the same folder.

For example, if you processed the log_2023.smo file, a log_2023.txt 
or log_2023.xlsx file will appear next to it. Open it in any text 
editor ("Notepad", Notepad++) or in Microsoft Excel / LibreOffice Calc.

TIP: For convenient viewing of text tables without column distortion, 
open the file in editors with a monospaced font (e.g., Notepad++, 
VS Code, or standard Notepad) and disable word wrap.

6. Possible Issues

Error: python: command not found or python is not recognized
Solution: You didn't check the "Add to PATH" box during Python 
installation (on Windows). Alternatively, use the python3 command 
instead of python.

Error: FileNotFoundError
Solution: You are trying to run the script from the wrong folder 
where the .smo files are not located, or you specified the file 
name incorrectly.

Error: openpyxl installation error when running with --xlsx
Solution: Make sure you have internet access, or install the 
library manually with the command:
   pip install openpyxl

NOTE ON LOG CONTENTS:
If the ScanMyOpel app log only recorded "raw" data (lines like 
80 F1 18 22 61 01...) without text parameter names, the script 
will process such a log, but the "Live Data" section will be empty 
because the app failed to record the parameter names.
```