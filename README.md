

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

## 3. Projekt starten

```bash
docker compose up --build
```

---

## 4. API testen & nutzen

Öffnen Sie die Swagger-UI im Browser:
[http://localhost:8000/docs](http://localhost:8000/docs)

**Beispiele für API-Requests:**
```bash
# Alle Bücher abrufen
curl -X GET "http://localhost:8000/api/books"

# Nach Autor suchen
curl -X GET "http://localhost:8000/api/books?author=Douglas%20Adams"

# Benutzer anlegen
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Max","last_name":"Mustermann","email":"max@uni.de","phone":"123456","membership_status":"active"}'
```

---

## Hinweise

- Die Datenbank wird beim ersten Start automatisch mit Beispieldaten gefüllt.
- Änderungen am Code erfordern ggf. einen Neustart mit `docker compose up --build`.
- Die API ist über Swagger-UI und per curl nutzbar.

---

Viel Erfolg beim Arbeiten mit dem System!

- Keine lokale Datenbankinstallation nötig
- Reproduzierbare Umgebung für Entwicklung und Tests
- Einfaches Deployment

## Datenbank-Zugangsdaten

- Nutzer: `library_user`
- Passwort: `library_pass123`
- Datenbank: `library_system`

---
