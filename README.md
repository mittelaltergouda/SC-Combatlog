# SC-CombatLog

## License
The use of this tool is subject to the terms of the license described in the [LICENSE.txt](./LICENSE.txt) file.

## Introduction
SC-CombatLog ist ein Tool zur Analyse und Auswertung von Kampflogs in Star Citizen. Es bietet Funktionen wie Kill-Zählung, Statistik-Tracking und Leaderboard-Anzeige. Das Tool ist besonders nützlich für Spieler, die ihre Performance überwachen oder detaillierte Berichte über ihre Aktivitäten erstellen möchten.

## Privacy
**Wichtig**: Alle Nutzerdaten werden ausschließlich lokal auf deinem Computer gespeichert und niemals an externe Server übertragen. SC-CombatLog respektiert deine Privatsphäre und funktioniert auch ohne Internetverbindung (außer für optionale Update-Prüfungen).

## Requirements
Um SC-CombatLog zu nutzen, benötigst du entweder:
- The pre-compiled .exe file or installer from the latest release
- OR
- **Python 3.12** or higher and the following Python libraries:
  - `tkinter`
  - `logging`
  - `sqlite3`
  - `watchdog`
  - `tkcalendar` (optional, for date selection)

## Installation
1. **Installer Version (recommended)**:
   - Lade die aktuelle Version des Installers (`SC-CombatLog-Setup-x.x.x.exe`) von der [Releases-Seite](https://github.com/YourRepo/SC-CombatLog/releases) herunter.
   - Run the installer and follow the on-screen instructions.
   - A shortcut will be created on the desktop and in the start menu.

2. **Portable Version**:
   - Lade das ZIP-Archiv (`SC-CombatLog-x.x.x.zip`) von der [Releases-Seite](https://github.com/YourRepo/SC-CombatLog/releases) herunter.
   - Extract the archive to any location.
   - Starte die Anwendung durch Doppelklick auf `sc-combatlog.exe`.

3. **Source Code Version**:
   - Make sure Python 3.12 or higher is installed on your system. You can download Python from [python.org](https://www.python.org/).
   - Install the required libraries with the following command:
     ```bash
     pip install watchdog tkcalendar
     ```
   - Clone or download the repository.
   - Führe die Datei `y_start_sc_combatlog.bat` aus oder starte das Programm direkt über die Kommandozeile:
     ```bash
     python sc_combatlog_tk.py
     ```

## Starting the Program
1. **Installed Version**:
   - Click on the desktop shortcut or find the application in the start menu.

2. **Portable Version**:
   - Navigate to the directory where you extracted the program.
   - Doppelklicke auf die Datei `sc-combatlog.exe`.

3. **Source Code Version**:
   - Führe die Datei `y_start_sc_combatlog.bat` aus.
   - Alternatively, you can start the program directly from the command line:
     ```bash
     python sc_combatlog_tk.py
     ```

## Features
- **Kill and Death Tracking**:
  - Track your kills and deaths in Star Citizen.
  - View leaderboards with the best players.

- **Statistics and Reports**:
  - Create detailed reports about your activities.
  - Filter data by date and other criteria.

- **Live Log Processing**:
  - The tool monitors your Star Citizen logs in real-time and updates statistics automatically.

## Notes
- **Configuration File**:
  - The `config.txt` file contains user-specific settings such as player name and logging options.
  - This file is created automatically if it does not exist.

- **Database**:
  - All data is stored in a SQLite database located in the `databases/` folder.
  - **Privacy**: Your data is stored exclusively locally and never transmitted to external servers.

- **Logs**:
  - Error and activity logs are saved in the `Logs/` folder.

- **Automatic Updates**:
  - The application can check for updates when an internet connection is available.
  - The update must be manually confirmed and no data is transmitted without your consent.

## Support
If you have questions or issues, please contact the developer or consult the documentation.