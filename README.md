# 💣 Multilingual Minesweeper

A modern, feature-rich Minesweeper game built with Python and PyQt5. It supports **28 languages** out of the box, automatic high-DPI scaling for Retina displays, and includes helpful assistance tools for beginners and advanced players alike.

---

## 🖥️ Supported Platforms & Downloads

Go to the **Releases** page to download the ready-to-run packages for your system:

* 🪟 **Windows (7 - 11):** Download `Minesweeper.7z` (Extract and run the `.exe`).
* 🍏 **macOS (Intel only):** Download `Minesweeper.dmg` (Drag & Drop installation. *Note: Built for Intel Macs*).
* 🐧 **Linux:** Download `Minesweeper.tar.gz` (Standalone binary package).

---

## 🎮 How to Play

### Objective
Your goal is to uncover all grid cells that do not contain mines. Mark suspected mines with flags until only safe cells remain.

### Controls & Core Rules
* **Left-Click:** Uncover a cell. The very first click generates the minefield and is **always 100% safe**.
* **Right-Click (or Middle-Click):** Mark a cell with a flag / remove a flag.
* **Numbers:** Uncovered cells show numbers indicating how many mines are located within the 8 adjacent neighboring cells.
* **Empty Cells (0):** Clicking an empty cell automatically reveals all connected empty and numbered neighboring cells (Flood-Fill effect).

### UI Features & Tools
* **New Game:** Instantly restarts the game with the chosen settings.
* **Safe Move:** An automatic helper function. It analyzes the board to safely reveal a hidden cell or place a guaranteed flag. Use it whenever you are stuck!
* **Time:** The timer starts automatically with your first click and tracks your elapsed play time.
* **Mine Counter:** Displays the total number of mines minus the number of flags currently placed.

### Victory & Defeat
* **🏆 Victory:** You win the game when every single non-mine cell on the board has been uncovered.
* **💥 Defeat:** If you reveal a cell containing a mine, the game ends immediately and all remaining mine locations are revealed.

---

## 💡 Quick Tips & Strategies

1. **Start Big:** Begin near the corners or in the center to increase your chances of opening up a large, safe starting area.
2. **Use the "Safe Move" Helper:** Don't gamble! Use the build-in logical solver helper before making risky guesses.
3. **Analyze Number Patterns:** If the number of unrevealed neighbors equals the number on a cell, all those neighbors are definitely mines. If a cell's number is already satisfied by flags, all other hidden neighbors are safe to click.
4. **Think Logically:** Minesweeper is a game of logic. Take your time, analyze the layout, and use the Safe Move function instead of guessing blindly.

---

## 🌍 Supported Languages (28)
The game UI and messages automatically save your choices and fully support:
English, Deutsch, Français, Español, Italiano, Русский, Українська, Polski, Nederlands, Português, Čeština, Dansk, Suomi, Magyar, Norsk, Svenska, Română, Български, Ελληνικά, Slovenčina, Slovenščina, Српски, Hrvatski, Eesti, Latviešu, Lietuvių, Malti, Gaeilge.

---

**Good luck, have fun, and enjoy playing!** 🚀
