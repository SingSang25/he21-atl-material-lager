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

**Achtung:**

Wenn du ein User erstellt ist der default wert beim disabled true! Du musst dies auf false setzen, damit du dich mit dem User einloggen kannst. Dies zellt auch für die Admin rechte. Wenn du ein User erstellst, ist der default wert beim admin true! Du musst dies auf fals setzen, damit du keine Admin rechte hast.

Des weiteren muss man aufpassen wenn man einen Patch macht darf beim Letzten Wert **kein** Komma sein. Dies führt zu einem Fehler in der API.

## Schnitstellen

### Item

| Typ    | Route                  | Beschreibung                      | Admin Rechte benötigt |
| :----- | :--------------------- | :-------------------------------- | :-------------------- |
| GET    | /items/                | Alle Items anzeigen               | Nein                  |
| POST   | /items/                | Item erstellen                    | Ja                    |
| GET    | /items/{item_id}/      | Ein Item anzeigen                 | Nein                  |
| PATCH  | /items/{item_id}/      | Item ändern                       | Nein                  |
| DELETE | /items/{item_id}/      | Item löschen                      | Ja                    |
| GET    | /items/{item_id}/logs/ | Alle Logs von einem Item anzeigen | Nein                  |

### Log

| Typ | Route                       | Beschreibung                      | Admin Rechte benötigt |
| :-- | :-------------------------- | :-------------------------------- | :-------------------- |
| GET | /logs/                      | Alle Logs anzeigen                | Nein                  |
| GET | /logs/{log_id}/             | Ein Log anzeigen                  | Nein                  |
| GET | /logs/type/{log_type}/      | Alle Logs von einem Typ anzeigen  | Nein                  |
| GET | /logs/created/{created_by}/ | Alle Logs von einem User anzeigen | Nein                  |

### User

| Typ    | Route                  | Beschreibung                      | Admin Rechte benötigt |
| :----- | :--------------------- | :-------------------------------- | :-------------------- |
| GET    | /users/                | Alle User anzeigen                | Nein                  |
| POST   | /users/                | User erstellen                    | Ja                    |
| GET    | /users/me/             | Eingelogter User anzeigen         | Nein                  |
| PATCH  | /users/me/             | Eingelogter User ändern           | Nein                  |
| DELETE | /users/me/             | Eingelogter User löschen          | Nein                  |
| GET    | /users/{user_id}/      | Ein User anzeigen                 | Nein                  |
| PATCH  | /users/{user_id}/      | Ein User ändern                   | Ja                    |
| DELETE | /users/{user_id}/      | Ein User löschen                  | Ja                    |
| GET    | /users/{user_id}/logs/ | Alle Logs von einem User anzeigen | Nein                  |

### Tocken

| Typ  | Route                | Beschreibung    | Admin Rechte benötigt |
| :--- | :------------------- | :-------------- | :-------------------- |
| POST | /login/access-token/ | Token erstellen | Nein                  |

### Überlegungen

Die Endpunbkte haben zwei verschiedene Berechtigunen. (Admin und User, sieh in den Tabellen oben welche sie verwenden können).

**User**

Alle User Endpunkte sind zum verwalten der User gedacht.

Jeder hat die Möglichkeit seinen User zu bearbeiten (Ja, auch die Adminrechte).

Jeder Admin kann alle User Bearbeiten und löschen so wie neue User erstellen. Dabei kann jeder User alle User aufrufgen, damit er diese dannach bei den Items zuweisen kann.

**Items**

Nur Admins können neue Items erstellen, oder auch die Items löschen.

Jedoch kann jeder User die Items aufrufen und bearbeiten, damit er diese anderen oder sich selbst zuweisen kann.

**Logs**

Jeder kann die Logs aufrufen und keiner kann die Logs beraeiten oder löschen.

Dies dient der nachverfolgbarkeit, damit man sieht wer was gemacht hat.

### Logs Lesen

Die Logs sind nicht selbsterklärend, deswegen hier ein kurzer beschrieb was sie bedeuten.

| Parameter  | Datentyp | Beschreibung                                                                                                                                                                    |
| :--------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| id         | String   | Die ID des Logs, dies sist eine uuid4, welche selbstständig generiert wird                                                                                                      |
| datum      | DateTime | Das Datum, wann der eintrag gemacht wurde                                                                                                                                       |
| log        | String   | Der Inhalt was gemacht wurde bei diesem eintrag **Es stehen keine User oder Items hier, nur z.B. User created**                                                                 |
| type       | String   | Der Typ des Logs, es gibt drei verschiedene Typen (item, user, system) Damit siehr man welchen Endpunkt verwendet wurde. Bei System sind es automatismen welche diese erstellen |
| created_by | String   | Die ID des Users, welcher diesen eingelogt war und diesen eintrag gemacht hat                                                                                                   |
| user_id    | String   | Die ID des Users, welcher betroffen ist. **Dies zeigt an, falls ein User betroffen welchen es war, z.B. Neuer User erstellt**                                                   |
| item_id    | String   | Die ID des Items, welcher betroffen ist. **Dies zeigt an, falls ein Item betroffen welches es war, z.B. Neues Item erstellt**                                                   |

## Ändern bzw. verbessern wenn genügend Zeit

- Grafische Benutzeroberfläche:
  - Ich hätte eine Benutzeroberfläche erstellt, die die API verwendet. Ich hatte jedoch keine Zeit, dies noch zu lernen, bzw. die Zeit dies Umzusetzen.
- Mehr und genauere Tests:
  - Einige Tests sind nicht so genau, wie sie sein sollten. Besonders die Logs hätten besser getestet werden sollen. In den Tests hatt es mehrfachen Code den ich verbessern hätte können.
- Routen der Logs:
  - Ich hätte diese drei routen zusammengefasst oder Optimiert /logs/{log_id}/, /logs/type/{log_type}/ und /logs/created/{created_by}/ zu einer Route. Dazu sind sie nicht so gut erstellt wie die Items oder User Routen.
  - Weiter würde ich den Inhalt der Logs Optimieren, mit exakterem Inhalt.
- Login mit scopes oder http Basic Auth:
  - Ich habe ein Login implementiert. Allerdings hatte ich nicht die Zeit die Advanced Version zu implementieren. Ich hätte dies mit scopes oder http Basic Auth gemacht.
- Material Lager:
  - Ich habe nur einen String für den Standort verwendet, bei den Items. Ich würde dies mit einer genaueren Auflistung machen. z.B. Standort, Regal, Fach, Ebene.
- Sicherungen bei der Eingabe:
  - Ich sollte einige eingaben im Backend abfangen, die ich jetzt im Frontend gelöst hätte. z.B. Beim Ändern des Status verfügbar muss ein Benutzer angegeben werden muss.
- Dokumente, Metadaten:
  - Ich wollte die Schnittstellen besser dokumentieren, direkt in der API. Wie in diesem Tutorial beschrieben: [https://fastapi.tiangolo.com/tutorial/metadata/][fastapi-metadata].
- Material / User löschen:
  - Wenn man das Material / User löscht, wird es direkt aus der DB entfernt. Ich würde das so ändern, dass sie den Status gelöscht bekommen und dies erst nach 30 Tagen automatisch passiert. Dies würde die Möglichkeit bieten das Material wieder herzustellen.
- Sicherheit:
  - Ich hätte noch hinzugefügt, dass man ein Passwort mit mindestens 8 Zeichen, Grossbuchstaben, Kleinbuchstaben und Zahlen erstellen muss und das man diese Regeln auch bearbeiten kann.
  - Aktuell kann sich selbst von ein nicht Admin zu einem Admin machen. (;
- Patch der Items
  - Aktuell kann jeder die alles an den Items verändern, dies müsste man einschrenken.
- Mehrere Lager:
  - Ich hätte die Möglichkeit geschaffen, mehrere Lager zu erstellen. Die Enzelne User haben und einzelne Items.
- Endpunkt Item sich selber zuweisen:
  - Einen Endpunkt, welcher dazu verwendet werden kann sich selber ein Item zuweisen.

# ATL 2

## Erstellen des Dockers

1. Erstelle ein Dockerfile, welches die API in einen Docker Container packt.

Dies kannst du mit folgendem Code machen.

```bash
docker init
```

Dannach muss man das Docker File anpassen:

```dockerfile
ARG PYTHON_VERSION=3.11.1

FROM python:${PYTHON_VERSION}-slim as build
WORKDIR /temp
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without test

FROM python:${PYTHON_VERSION}-slim
WORKDIR /app
COPY --from=build /temp/requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt
COPY ./he21_atl_material_lager/ /app/he21_atl_material_lager
CMD uvicorn he21_atl_material_lager.main:app --reload --proxy-headers --host 0.0.0.0 --port 8000
EXPOSE 8000
```

Gehen wir nun die einzelnen Schritte durch.

```dockerfile
ARG PYTHON_VERSION=3.11.1
```

Diese Zeile Definiert eine Variable, welche wir später verwenden können.

```dockerfile
FROM python:${PYTHON_VERSION}-slim as build
WORKDIR /temp
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without test
```

Hier wird ein neuer Container erstellt, welcher als Basis Python verwendet. Dieser Container wird als build bezeichnet. Danach wird das Arbeitsverzeichnis auf /temp gesetzt. Danach werden die Dateien pyproject.toml und poetry.lock in das Arbeitsverzeichnis kopiert. Danach wird poetry installiert und die requirements.txt erstellt.

Die requirements.txt wird erstellt, damit wir diese im nächsten Schritt verwenden können.

```dockerfile
FROM python:${PYTHON_VERSION}-slim
WORKDIR /app
COPY --from=build /temp/requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt
COPY ./he21_atl_material_lager/ /app/he21_atl_material_lager
CMD uvicorn he21_atl_material_lager.main:app --reload --proxy-headers --host 0.0.0.0 --port 8000
EXPOSE 8000
```

Hier wird ein neuer Container erstellt. Dieser Kontainer Protuktiv eingesetzt wird. Danach wird das Arbeitsverzeichnis auf /app gesetzt. Danach wird die requirements.txt in das Arbeitsverzeichnis vom build kopiert. Danach wird die requirements.txt installiert und danach das txt gelöscht.

Danach wird der Ordner he21_atl_material_lager in das Arbeitsverzeichnis kopiert. Danach wird der Befehl uvicorn ausgeführt, welcher die API startet. Am ende wird der Port 8000 freigegeben.

2. Nun kann man mit folgendem Befehl ein Docker Image.

```bash
docker build -t he21-atl-material-lager .
```

3. Nun haben wir ein Docker Image erstellt, welches wir nun starten können.

```bash
docker run -d -p 8000:8000 he21-atl-material-lager
```

![docker-run]

P.S. Bei meinem Geschäftslaptop ist der Port 8000 Blockiert von einer anderen Software. Deswegen habe ich den Port 8001 verwendet.

## Einrichten der Cloud

### Google Cloud

1. Verbinde dein GitHub Repository mit der Google Cloud.

1.1. Gehe auf die Google Cloud Platform und erstelle ein neues Projekt.

1.2. Gehe auf den Cloud Build und verbinde dein GitHub Repository.

![cloud-build-verknüpfen]

1.3. Ich habe dazu die Funktion "Cloud Build-GitHub-Anwendung" verwendet

2. Erstelle die Triggers für den Cloud Build.

Dazu habe ich einen Trigger erstellt, welcher bei jedem Push auf den Master Branch ein Build startet.

![cloud-trigger]

3. Zu guter letzt habe ich noch die einstellung vorgenommen, dass der Cloud Builder auf die Cloud Run zugreifen kann.

![settings-create]

### cloudbuild.yaml

1. Erstelle eine cloudbuild.yaml Datei, welche die API in einen Docker Container packt.

```yaml
steps:
  - name: python:3.11-slim
    entrypoint: bash
    args:
      - "-c"
      - pip install poetry && poetry install && poetry run pytest

  - name: "gcr.io/cloud-builders/docker"
    args: ["build", "-t", "gcr.io/$PROJECT_ID/$REPO_NAME:$COMMIT_SHA", "."]

  - name: "gcr.io/cloud-builders/docker"
    args: ["push", "gcr.io/$PROJECT_ID/$REPO_NAME:$COMMIT_SHA"]

  - name: "gcr.io/cloud-builders/gcloud"
    args:
      [
        "run",
        "deploy",
        "he21-atl-jan-zeugin",
        "--image",
        "gcr.io/$PROJECT_ID/$REPO_NAME:$COMMIT_SHA",
        "--min-instances",
        "0",
        "--max-instances",
        "1",
        "--region",
        "europe-west1",
        "--allow-unauthenticated",
        "--port",
        "8000",
      ]
```

Gehen wir nun die einzelnen Schritte durch.

```yaml
steps:
  - name: python:3.11-slim
    entrypoint: bash
    args:
      - "-c"
      - pip install poetry && poetry install && poetry run pytest
```

In diesem Schritt wird ein neuer Container mit Python als Basis erstellt. Der Container wird so konfiguriert, dass das Poetry-Paketverwaltungstool installiert wird. Anschliessend werden die erforderlichen Abhängigkeiten installiert und die Tests mit Poetry ausgeführt.

```yaml
- name: "gcr.io/cloud-builders/docker"
  args: ["build", "-t", "gcr.io/$PROJECT_ID/$REPO_NAME:$COMMIT_SHA", "."]
```

Im zweiten Schritt wird der Docker-Container erstellt. Der Container wird mit einem eindeutigen Tag versehen, das aus den Umgebungsvariablen:

- $PROJECT_ID -> Die ID des Projektes in der Google Cloud
- $REPO_NAME -> Der Name des GitHub-Repositorys
- $COMMIT_SHA -> Der SHA des Commits

```yaml
- name: "gcr.io/cloud-builders/docker"
  args: ["push", "gcr.io/$PROJECT_ID/$REPO_NAME:$COMMIT_SHA"]
```

Nach dem erfolgreichen Erstellen des Docker-Containers wird dieser in den Google Cloud Container Registry hochgeladen. Dieser Schritt stellt sicher, dass das erstellte Image für den späteren Einsatz in der Google Cloud verfügbar ist.

```yaml
- name: "gcr.io/cloud-builders/gcloud"
  args:
    [
      "run",
      "deploy",
      "he21-atl-jan-zeugin",
      "--image",
      "gcr.io/$PROJECT_ID/$REPO_NAME:$COMMIT_SHA",
      "--min-instances",
      "0",
      "--max-instances",
      "1",
      "--region",
      "europe-west1",
      "--allow-unauthenticated",
      "--port",
      "8000",
    ]
```

Der letzte Schritt beinhaltet das Bereitstellen des erstellten Containers in Google Cloud Run.
Mit folgenden Parametern, damit nicht zu viele Instanzen erstellt werden und die API unter dem Port 8000 erreichbar ist:

- --min-instances 0
- --max-instances 1
- --region europe-west1
- --allow-unauthenticated
- --port 8000

### Cloud Link

Die API ist nun unter folgendem Link erreichbar: [https://he21-atl-jan-zeugin-ihvnn4wuqq-ew.a.run.app/docs][api-url]

## Probleme

Ein Problem war, dass ich folgende Fehlermeldung erhielt:

```bash
The name must use only lowercase alphanumeric characters and dashes, cannot begin or end with a dash, and cannot be longer than 63 characters.
```

Ich habe das Problem gelöst, indem ich den Namen des GitHub-Repositorys geändert habe (HE21-ATL-Material-Lager -> he21-atl-material-lager), dabei muste ich die verknüpfung zu Google Cloud erneut herstellen.

![fehler-cloud-zwei-git]

## Fehler (Mit absicht)

Um nun einen Fehler zu provozieren habe ich bei meinen Tests einen Fehler eingebaut.

```bash
def test_fehler():
assert 1 == 2
```

Nun habe ich ein git push gemacht und der Build ist fehlgeschlagen.

![fehler-cloud-build]

## Kontakt

Jan Zeugin - <jan.zeugin@hf-ict.info>

Project Link: [https://github.com/SingSang25/HE21-ATL-Material-Lager][GitHub-Link]

<!-- MARKDOWN LINKS -->

[github-link]: https://github.com/SingSang25/HE21-ATL-Material-Lager
[fastapi]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white
[fastapi-url]: https://fastapi.tiangolo.com/
[sqlalchemy]: https://www.sqlalchemy.org/img/sqla_logo.png
[sqlalchemy-url]: https://www.sqlalchemy.org/
[fastapi-metadata]: https://fastapi.tiangolo.com/tutorial/metadata/
[poetry-url]: https://python-poetry.org/docs/#installation
[api-url]: http://127.0.0.1:8000/docs#/
[jwt]: https://jwt.io/libraries?language=Python

<!-- IMAGES -->

[fehler-cloud-build]: https://github.com/SingSang25/he21-atl-material-lager/blob/main/images/Fehler.png
[fehler-cloud-zwei-git]: https://github.com/SingSang25/he21-atl-material-lager/blob/main/images/ZweiGitHubVerknüpfungen.png
[docker-run]: https://github.com/SingSang25/he21-atl-material-lager/blob/main/images/docker-run.png
[cloud-build-verknüpfen]: https://github.com/SingSang25/he21-atl-material-lager/blob/main/images/cloud-build-verknüpfen.png
[cloud-trigger]: https://github.com/SingSang25/he21-atl-material-lager/blob/main/images/cloud-trigger.png
[settings-create]: https://github.com/SingSang25/he21-atl-material-lager/blob/main/images/settings-create.png
