<div align="center">
  <h1 align="center">Material Verwaltungstool</h1>

  <p align="center">
    Einfach und unkompliziert sein Material verwalten
    <br />
    <a href="https://github.com/SingSang25/HE21-ATL-Material-Lager"><strong>Zu GitHub »</strong></a>
  </p>
</div>

## Über das Projekt

Mit diesem Projekt soll man:

- Verwaltung der Lagerbestände:
  - Das Tool sollte in der Lage sein, den aktuellen Bestand an Materialien im Lager zu verfolgen. Es sollte Informationen wie Artikelnummern, Beschreibungen, Mengen und Verfügbarkeit enthalten.
- Lagerplatzverwaltung:
  - Es sollte eine Funktion zur Unterstützung der physischen Lagerplatzverwaltung vorhanden sein. Dazu gehört die Zuordnung von Materialien zu bestimmten Lagerplätzen, um eine leichte Auffindbarkeit und effiziente Lagerung zu gewährleisten.
- Rückverfolgbarkeit und Historie:
  - Das System sollte die Möglichkeit bieten, den Weg des Materials zu verfolgen, einschliesslich Informationen über Ein- und Ausgänge. Auf diese Weise kann eine vollständige Rückverfolgbarkeit gewährleistet werden.

## Erstellt mit

- [![fastapi][fastapi]][fastapi-url]
- [![sqlalchemy][sqlalchemy]][sqlalchemy-url]

## Wie startet, testet und nutzt

### Installation

Du musst Poetry installieren, um die verwendeten Bibliotheken zu Installieren. [Anleitung zum Poetry installieren][poetry-url]

Nach dem Poetry installiert ist, machst du ein `git clone` des Projektes.

```bash
git clone https://github.com/SingSang25/HE21-ATL-Material-Lager.git
```

Um nun die Bibliotheken zu Installieren mit Poetry fürst du folgenden Befehl im Terminal aus.

```bash
poetry install
```

#### Optional

Nun wäre die Installation abgeschlossen.

Jedoch kann man unter he21_atl_material_lager.config eine .env Datei erstellen, welche Default Parameter enthalten für die Autentifikation.

Dabei kann man folgende Parameter setzen:

- SECRET_KEY -> Der schlüssel für die Verifikation des Tokens
- ALGORITHM -> Der Algorithmus für die Autentifikation (Achte darauf das nicht alle Algorithmen unterstützt werden. Es wurde [python-jose][jwt] verwendet)
- ACCESS_TOKEN_EXPIRE_MINUTES -> Die Zeit in Minuten, wie lange ein Token gültig ist

Hier ein Beispiel, dies sind die Default Parameter welche im Programm hinterlegt sind:

```bash
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### Starten der API

Wenn die Installation abgeschlossen ist, kannst du die API mit folgendem Befehl starten.

```bash
poetry run uvicorn he21_atl_material_lager.main:app --reload
```

Um die API wieder zu beenden kannst du `CTRL + C` im Terminal drücken.

### Testen der API

Dazu hat es die Tests, welche man ausführen kann, unter dem Ordner Tests.

Dazu kannst du folgenden Code im Terminal ausführen.

```bash
poetry run pytest
```

### Benutzen der API

Wenn die API gestartet ist, kannst du die API unter folgender URL erreichen. [http://127.0.0.1:8000/docs#/][api-url]

Um nun die API verwenden zu können muss man sich zuerst einloggen (Oben Rechts beim "Authorize"). Dazu hat es einen Default User, welcher in der DB erstellt wird, wenn die API gestartet wird.

```bash
User mit Admin Rechten:
Username: admin
Passwort: admin

User ohne Admin Rechte:
Username: user
Passwort: user
```

Falls du den Default User nicht verwenden möchtest, kannst du dich auch selber registrieren. Dazu musst du auf den Button "POST /users/" klicken und dann auf "Try it out" und dann die Daten eingeben. Danach kannst du dich mit dem User einloggen.

**Achtung:** Wenn du ein User erstellt ist der default wert beim disabled true! Du musst dies auf false setzen, damit du dich mit dem User einloggen kannst. Dies zellt auch für die Admin rechte. Wenn du ein User erstellst, ist der default wert beim admin true! Du musst dies auf fals setzen, damit du keine Admin rechte hast.

## Komponenten

This is an example of how to list things you need to use the software and how to install them.

- npm

  ```sh
  npm install npm@latest -g
  ```

## Überlegungen

### Item

| Typ | Route | Beschreibung |
| :--- | :--- | :--- |
| PATCH | /items/{item_id}/ | Item ändern |
| GET | /items/{item_id}/ | Item anzeigen |
| DELETE | /items/{item_id}/ | Item löschen |
| POST | /items/ | Item erstellen |
| GET | /items/ | Alle Items anzeigen |
| GET | /items/{item_id}/logs/ | Alle Logs von einem Item anzeigen |

### Log

| Typ | Route | Beschreibung |
| :--- | :--- | :--- |
| GET | /logs/ | Alle Logs anzeigen |
| GET | /logs/{log_id}/ | Log anzeigen |
| GET | /logs/type/{log_type}/ | Alle Logs von einem Typ anzeigen |
| GET | /logs/created/{created_by}/ | Alle Logs von einem User anzeigen |

### User

| Typ | Route | Beschreibung |
| :--- | :--- | :--- |
| GET | /users/{user_id}/logs/ | Alle Logs von einem User anzeigen |
| GET | /users/ | Alle User anzeigen |
| POST | /users/ | User erstellen |
| GET | /users/me/ | User anzeigen |
| DELETE | /users/me/ | User löschen |
| PATCH | /users/me/ | User ändern |
| GET | /users/{user_id}/ | User anzeigen |
| PATCH | /users/{user_id}/ | User ändern |
| DELETE | /users/{user_id}/ | User löschen |

### Tocken

| Typ | Route | Beschreibung |
| :--- | :--- | :--- |
| POST | /login/access-token/ | Token erstellen |

## Ändern bzw. verbessern wenn genügend Zeit

- Grafische Benutzeroberfläche:
  - Ich hätte eine Benutzeroberfläche erstellt, die die API verwendet. Ich hatte jedoch keine Zeit, dies zu lernen.
- Mehr und genauere Tests:
  - Einige Tests sind nicht so genau, wie sie sein sollten. Allerdings habe ich nicht die Zeit gefunden, dies zu ändern. Besonders die Logs hätten besser getestet werden sollen. In den Tests hatt es mehrfachen Code den ich verbessern hätte können.
- Routen der Logs:
  - Ich hätte diese drei routen zusammengefasst oder Optimiert /logs/{log_id}/, /logs/type/{log_type}/ und /logs/created/{created_by}/ zu einer Route.
- Login mit scopes oder http Basic Auth:
  - Ich habe ein Login implementiert. Allerdings hatte ich nicht die Zeit die Advanced Version zu implementieren. Ich hätte dies mit scopes oder http Basic Auth gemacht.
- Material Lager:
  - Ich habe nur einen String für den Standort verwendet, bei den Items. Ich würde dies mit einer genaueren Auflistung machen. z.B. Standort, Regal, Fach, Ebene.
- Sicherungen bei der Eingabe im Backend, die ich jetzt im Frontend gelöst hätte.
  - z.B. Beim Ändern des Status verfügbar muss ein Benutzer angegeben werden muss.
- Dokumente, Metadaten:
  - Ich wollte die Schnittstellen besser dokumentieren, direkt in der API. Wie in diesem Tutorial beschrieben: [https://fastapi.tiangolo.com/tutorial/metadata/][fastapi-metadata].
- Material löschen:
  - Wenn man das Material löscht, wird es direkt aus der DB entfernt. Ich würde das so ändern, dass sie den Status gelöscht bekommen und dies erst nach 30 Tagen automatisch passiert. Dies würde die Möglichkeit bieten das Material wieder herzustellen.
- Beim erstellen der DB:
  - Akutell löse ich beim Start der API den lifespan aus um zu Prüfen ob die Default User berieits in der DB sind, jedoch kann ich dies nicht in einem Test realisieren. Ich müsste dies anders lösen, evtl. kann man dies anders lösen. Da ich zwingend User bruache (Um einen User zu erstellen ist ein User Notwendig um einen User zu habe welcher Admin rechte hat) Aktuell kann man dies nur manuell prüfen.
- Passwort sicherheit:
  - Ich hätte noch hinzugefügt, dass man ein Passwort mit mindestens 8 Zeichen, Grossbuchstaben, Kleinbuchstaben und Zahlen erstellen muss und das man diese Regeln auch bearbeiten kann.

## Kontakt

Jan Zeugin - <jan.zeugin@hf-ict.info>

Project Link: [https://github.com/SingSang25/HE21-ATL-Material-Lager][GitHub-Link]

<!-- MARKDOWN LINKS & IMAGES -->

[github-link]: https://github.com/SingSang25/HE21-ATL-Material-Lager
[fastapi]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white
[fastapi-url]: https://fastapi.tiangolo.com/
[sqlalchemy]: https://www.sqlalchemy.org/img/sqla_logo.png
[sqlalchemy-url]: https://www.sqlalchemy.org/
[fastapi-metadata]: https://fastapi.tiangolo.com/tutorial/metadata/
[poetry-url]: https://python-poetry.org/docs/#installation
[api-url]: http://127.0.0.1:8000/docs#/
[jwt]: https://jwt.io/libraries?language=Python
