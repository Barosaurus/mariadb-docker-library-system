

# Bibliotheksverwaltungssystem mit MariaDB & Docker

Dieses Repository enthält ein containerisiertes Bibliotheksverwaltungssystem auf Basis von FastAPI und MariaDB. Die folgenden Schritte zeigen, wie Sie das Projekt von Grund auf starten und testen können.

---

## 1. Vorbereitung: Docker bereinigen

Um sicherzustellen, dass Sie mit einer sauberen Basis starten, führen Sie bitte folgende Befehle aus:

```bash
# (Optional, aber empfohlen) Alte Docker-Container, Images und Builder entfernen
docker compose down --volumes --remove-orphans
docker builder prune --all --force
docker image prune --all --force
docker volume prune --force
```

---

## 2. Projekt herunterladen

```bash
git clone https://github.com/Barosaurus/mariadb-docker-library-system.git
cd mariadb-docker-library-system
```

---

## 3. Projekt starten / Projekt beenden

```bash
#Programm starten
docker compose up --build
```

```bash
#Programm beenden
docker compose down
```

---

## 4. API testen & nutzen

Öffnen Sie die Swagger-UI im Browser:
[http://localhost:8000/docs](http://localhost:8000/docs)

**Beispiele für API-Requests:**

### Books (Bücher)
```bash
# Alle Bücher abrufen
curl -L "http://localhost:8000/api/books"

# Nach Autor suchen
curl -L "http://localhost:8000/api/books?author=Douglas%20Adams"

# Nach Kategorie filtern
curl -L "http://localhost:8000/api/books?category=Informatik"

# Buch hinzufügen
curl -L -X POST "http://localhost:8000/api/books" \
  -H "Content-Type: application/json" \
  -d '{"isbn":"9783161484100","title":"Beispielbuch","author":"Max Autor","category":"Technik","publication_year":2023,"total_copies":2,"available_copies":2}'
```

### Users (Benutzer)
```bash
# Alle Benutzer abrufen
curl -L "http://localhost:8000/api/users"

# Benutzer anlegen (user_number ist Pflichtfeld)
curl -L -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{"user_number":"STU999","first_name":"Jan","last_name":"Schlappen","email":"jan@uni.de","phone":"122333","status":"active"}'

# Einzelnen Benutzer abrufen
curl -L "http://localhost:8000/api/users/1"
```

### Loans (Ausleihen)
```bash
# Alle Ausleihen anzeigen
curl -L "http://localhost:8000/api/loans"

# Buch ausleihen (Fälligkeitsdatum in YYYY-MM-DD Format)
curl -L -X POST "http://localhost:8000/api/loans" \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"book_id":1,"due_date":"2025-09-02"}'

# Buch zurückgeben (loan_id durch tatsächliche ID ersetzen)
curl -L -X PUT "http://localhost:8000/api/loans/1/return"
```

### Health Check
```bash
# System-Status prüfen
curl -L "http://localhost:8000/health"
```

**Die interaktive API-Dokumentation mit "Try it out"-Funktionalität ist in der Swagger-UI unter http://localhost:8000/docs verfügbar.**

---

## 5. Funktionen des Systems

### Bücherverwaltung
- **CRUD-Operationen**: Bücher erstellen, anzeigen, bearbeiten und löschen
- **Suchfunktionen**: Filter nach ISBN, Titel, Autor oder Kategorie
- **Bestandsverwaltung**: Automatische Verwaltung verfügbarer und ausgeliehener Exemplare

### Benutzerverwaltung
- **Benutzerregistrierung**: Neue Nutzer mit eindeutiger Benutzernummer anlegen
- **Status-Management**: Benutzer können aktiv, inaktiv oder gesperrt sein
- **Kontaktdaten**: E-Mail und Telefonnummer werden validiert

### Ausleihsystem
- **Buch ausleihen**: Automatische Reduzierung verfügbarer Exemplare
- **Rückgabe**: Rückgabedatum wird gesetzt, Exemplare wieder verfügbar
- **Überfällige Ausleihen**: Automatische Erkennung basierend auf Fälligkeitsdatum
- **Verlauf**: Vollständige Nachverfolgung aller Ausleihvorgänge

### Zusätzliche Features
- **Health Check**: System- und Datenbankstatus prüfen
- **Swagger-UI**: Interaktive API-Dokumentation
- **Validation**: Automatische Eingabevalidierung und Fehlerbehandlung

---

## 6. Wichtige Hinweise

- Die Datenbank wird beim ersten Start automatisch mit Beispieldaten gefüllt
- Änderungen am Code erfordern einen Neustart mit `docker compose up --build`
- Die API unterstützt sowohl die Swagger-UI als auch direkte curl-Befehle
- Alle Datumsangaben erfolgen im Format YYYY-MM-DD
- E-Mail-Adressen und ISBN werden automatisch validiert

---

## 7. Systemzugang

### API-Endpunkte
- **Swagger-UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

### Datenbank-Zugang
- **phpMyAdmin**: http://localhost:8080
- **Direkte Verbindung**: localhost:3306

- Keine lokale Datenbankinstallation nötig
- Reproduzierbare Umgebung für Entwicklung und Tests
- Einfaches Deployment

## Datenbank-Zugangsdaten

- Nutzer: `library_user`
- Passwort: `library_pass123`
- Datenbank: `library_system`

---
