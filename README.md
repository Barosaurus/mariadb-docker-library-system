# 📚 Bibliotheksverwaltungssystem mit FastAPI, MariaDB & Docker

Dieses Repository enthält ein containerisiertes Bibliotheksverwaltungssystem zur Verwaltung von Büchern, Benutzern und Ausleihen. Das Projekt dient als Proof-of-Concept (PoC) für moderne Softwareentwicklung mit Datenbanken und Containern.

---

## 1. Vorbereitung: Docker bereinigen

Um mit einer sauberen Umgebung zu starten und eventuelle Konflikte mit alten Containern, Images oder Volumes zu vermeiden, empfehlen wir folgende Befehle auszuführen:

```bash
# (Optional, aber empfohlen) Alte Docker-Container, Images und Builder entfernen
docker compose down --volumes --remove-orphans
docker builder prune --all --force
docker image prune --all --force
docker volume prune --force
```

Damit wird sichergestellt, dass das Projekt auf einem „frischen“ Stand startet und alle Komponenten neu aufgebaut werden.

---

## 2. Projekt klonen

```bash
git clone https://github.com/Barosaurus/mariadb-docker-library-system.git
cd mariadb-docker-library-system
```

---

## 3. .env Datei konfigurieren

Im Ordner `backend/` wird eine Datei `.env` mit den Datenbank-Zugangsdaten benötigt:

**Pfad:**  
```
backend/.env
```

**Beispiel-Inhalt:**  
```env
DATABASE_URL=mysql+pymysql://library_user:library_pass123@mariadb:3306/library_system
```

Wir nutzen die `.env`-Datei, um die Zugangsdaten zentral und einfach verwaltbar zu halten. In der Praxis würden diese Daten natürlich nicht unverschlüsselt oder öffentlich in einer README stehen – für den PoC und die Nachvollziehbarkeit ist das hier aber bewusst so gewählt.

---

## 4. Container starten & stoppen

```bash
# Container und Abhängigkeiten bauen und starten
docker compose up --build

# Container stoppen
docker compose down
```

*Bei Code-Änderungen: `docker compose up --build` neu ausführen.*

---

## 5. API-Dokumentation & Test

- Swagger-UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/health](http://localhost:8000/health)
- Direktzugriff: [http://localhost:8000/](http://localhost:8000/)

---

## 🧪 Beispiel-API-Requests

**Bücher**
```bash
# Alle Bücher abrufen
curl -X GET "http://localhost:8000/api/books/"

# Buch anlegen
curl -X POST "http://localhost:8000/api/books/" \
  -H "Content-Type: application/json" \
  -d '{"isbn":"9783161484100","title":"Beispielbuch","author":"Max Autor","category":"Technik","publication_year":2023,"total_copies":2,"available_copies":2}'
```

**Benutzer**
```bash
# Alle Benutzer abrufen
curl -X GET "http://localhost:8000/api/users/"

# Benutzer anlegen (user_number ist Pflicht)
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{"user_number":"STU999","first_name":"Jan","last_name":"Schlappen","email":"jan@uni.de","phone":"122333","status":"active"}'
```

**Ausleihe**
```bash
# Buch ausleihen
curl -X POST "http://localhost:8000/api/loans/" \
  -H "Content-Type: application/json" \
  -d '{"user_number":"STU003","book_isbn":"9783161484100","due_date":"2025-09-02"}'

# Buch zurückgeben
curl -X PUT "http://localhost:8000/api/loans/1/return/"
```

**System-Status**
```bash
curl -X GET "http://localhost:8000/health"
```

---

## 🏷️ Funktionen im Überblick

- **Bücherverwaltung:** 
  - Hinzufügen, Anzeigen, Bearbeiten und Löschen von Büchern (CRUD)
  - Verwaltung von verfügbaren und ausgeliehenen Exemplaren
  - Such- und Filtermöglichkeiten (z.B. nach Autor, Kategorie, ISBN)
- **Benutzerverwaltung:** 
  - Hinzufügen, Bearbeiten und Löschen von Nutzern
  - Nutzerinformationen wie Name, E-Mail, Telefonnummer und Status werden gespeichert
  - Eingaben werden auf grundlegende Gültigkeit geprüft (z.B. E-Mail-Syntax)
- **Ausleihsystem:** 
  - Erfassen von Ausleihen und Rückgaben
  - Beim Ausleihen wird die Anzahl verfügbarer Exemplare automatisch reduziert, bei Rückgabe wieder erhöht
  - Ausleihen können nach Fälligkeitsdatum gefiltert werden; überfällige Ausleihen werden angezeigt, jedoch erfolgt keine automatische Benachrichtigung oder Sanktion
- **Fehlerbehandlung:** 
  - Sinnvolle Fehlermeldungen bei ungültigen oder fehlenden Eingaben (z.B. Pflichtfelder, Datumsformat, nicht vorhandene Entitäten)
- **API-Dokumentation:** 
  - Interaktive Dokumentation und Testmöglichkeit durch Swagger-UI
- **Health Check:** 
  - Überprüfung des System- und Datenbankstatus
- **Initialbefüllung:** 
  - Die Datenbank wird beim ersten Start automatisch mit Beispieldaten befüllt

---

## 🗄️ Datenbankzugriff

- **phpMyAdmin:** [http://localhost:8080](http://localhost:8080)
- **Direkte Verbindung:** `localhost:3306`  
  z.B. mit Tools wie DBeaver, HeidiSQL oder MySQL Workbench

---

## ⚠️ Hinweise

- Datumsangaben verwenden das Format `YYYY-MM-DD`
- Bei Benutzer-E-Mails und ISBN erfolgt eine grundlegende Syntaxprüfung, jedoch keine tiefergehende Validierung
- Änderungen am Code erfordern einen Neustart des Containers
- Die Umgebung ist vollständig reproduzierbar und benötigt keine lokale Datenbankinstallation

---

## 🗝️ Standard-Datenbank-Zugangsdaten

- **Benutzer:** `library_user`
- **Passwort:** `library_pass123`
- **Datenbank:** `library_system`

---

**Das System bietet eine moderne, containerisierte Lösung für die Verwaltung von Bibliotheksdaten mit Fokus auf Erweiterbarkeit und Praxisnähe.**