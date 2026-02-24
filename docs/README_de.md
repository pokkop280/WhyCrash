# 🚀 WhyCrash
**WhyCrash** ist ein vollautomatischer KI-Assistent zur Fehlerbehandlung in Python. Wenn Ihr Code abstürzt, fängt WhyCrash den Fehler ab, analysiert ihn mithilfe von neuronalen Netzen (OpenRouter + Minimax), sammelt den Kontext aus Ihren lokalen Projektdateien und liefert die Ursache zusammen mit einer **AUTOMATISCHEN CODE-KORREKTUR**.

Ist Ihr Code abgestürzt? Die KI erklärt, warum, und ersetzt die defekte Datei automatisch durch die korrigierte (wenn Sie es erlauben).

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Versions](https://img.shields.io/badge/python-3.8%2B-blue)

## ✨ Hauptfunktionen
- 🧠 **Intelligente Traceback-Analyse**: Versteht nicht nur die Zeile mit dem Fehler, sondern sammelt auch importierte lokale Projektdateien.
- 🛠️ **Auto-Korrektur**: Schlägt eine fertige Lösung vor und kann die Ziel-Python-Dateien selbst umschreiben.
- 🎯 **Präzise Kontrolle**: Sie entscheiden, wo Fehler abgefangen werden sollen: im gesamten Projekt, in einer einzelnen Funktion oder in einem bestimmten Codeblock.
- 🎨 **Schöne Benutzeroberfläche**: Verwendet die `rich`-Bibliothek für ansprechende Fenster und Terminalformatierungen.

---

## 📦 Installation

```bash
pip install WhyCrash
```
> *(Erfordert `requests`, `rich` und `questionary` — sie werden automatisch installiert)*

---

## 🛠️ Verwendung

Sie haben 4 Möglichkeiten zu steuern, welche Fehler WhyCrash abfangen soll. Wählen Sie die Variante, die am besten passt!

### 1. Globales Abfangen (am einfachsten)
Wenn Sie möchten, dass **jeder** unbehandelte Fehler in Ihrem Programm von der KI analysiert wird:

```python
import WhyCrash

# Fehlererfassung für das gesamte Skript aktivieren
WhyCrash.debug()

# Wenn der Code unten abstürzt, kommt WhyCrash zur Rettung!
print(1 / 0)
```

### 2. Dynamisches Ein-/Ausschalten (start & end)
Wenn Sie einen großen Codeblock haben und die intelligente Analyse kurz davor einschalten und danach ausschalten möchten:

```python
import WhyCrash

# ... normaler Code ohne WhyCrash ...

WhyCrash.start_debug()  # Interceptor einschalten

a = "text"
b = int(a)  # <-- Dieser Fehler geht an die KI!

WhyCrash.end_debug()    # Interceptor ausschalten (Rückkehr zum Standardverhalten)
```

### 3. Dekorator für bestimmte Funktionen `@catch_errors`
Wenn Sie nur die Zuverlässigkeit einer bestimmten Funktion überprüfen möchten, können Sie sie in einen Dekorator einwickeln. Wenn die Funktion abstürzt, wird WhyCrash ausgelöst, während Systemfehler außerhalb davon unberührt bleiben.

```python
from WhyCrash import catch_errors

@catch_errors
def my_danger_function():
    # Wenn es hier bricht — wird WhyCrash ausgelöst
    file = open("no_exist.txt", "r")

def normal_function():
    # Und wenn es hier bricht — Standard-Python-Traceback
    pass

my_danger_function()
```

### 4. Kontextmanager `with catch_block()`
Für maximale Kontrolle, wenn Sie einen Fehler in genau 2 spezifischen Codezeilen erwarten:

```python
from WhyCrash import catch_block

print("Arbeit beginnt...")
text = "100"

with catch_block():
    # Only code inside this block is monitored
    number = int(text)
    result = number / 0  # Dies löst einen Fehler aus, der an WhyCrash gesendet wird!

print("Dieser Code wird nicht ausgeführt, wenn oben ein Fehler aufgetreten ist.")
```

---

## 🛑 Wie ignoriere ich Fehler?
WhyCrash analysiert nur **unbehandelte** (unhandled) Ausnahmen. Wenn Sie möchten, dass ein Fehler in Ihrem Code **nicht** zu WhyCrash gelangt und das Skript weiterläuft, verwenden Sie einfach einen normalen `try...except`-Block:

```python
import WhyCrash
WhyCrash.debug()

try:
    int("letter")
except ValueError:
    print("Fehler abgefangen, erreicht WhyCrash nicht. Weiter geht's!")
```

## ⚙️ Unter der Haube
- **OpenRouter & Minimax** — Verantwortlich für die Codeanalyse, das "Reasoning" und das Generieren von Korrekturdateien.
- **Traceback Walking** — Das Skript verfolgt automatisch die Fehlerkette, findet alle betroffenen `.py`-Dateien, liest sie und sendet sie als Kontext an die KI.
- **Rich** — Schöne Konsolen-Benutzeroberfläche (Farben, Panels, Markdown-Formatierung).

---

Mit ❤️ gemacht, um die Nerven der Entwickler zu schonen!

---
🌍 **Sprachen:** [English](../README.md) | [Русский](README_ru.md)
