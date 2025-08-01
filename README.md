# mariadb-docker-library-system

Datenbanken Hausarbeit: Developing Applications with MariaDB & Containers via Docker (mit Bibliotheksverwaltungssystem als PoC)

## Features

- Bücherverwaltung (CRUD, Suche nach ISBN, Titel, Autor, Kategorie)
- Benutzerverwaltung (CRUD, Suche nach Name, E-Mail, Status)
- Ausleihmanagement (Buch ausleihen, zurückgeben)
- Moderne API mit FastAPI und MariaDB
- Vollständig containerisiert mit Docker Compose

## Schnellstart

```bash
# Projekt clonen
git clone https://github.com/Barosaurus/mariadb-docker-library-system.git
cd mariadb-docker-library-system

# Docker-Container starten
docker-compose up --build
```

## API testen

Swagger-UI: [http://localhost:8000/docs](http://localhost:8000/docs)

**Beispiele:**
```bash
# Alle Bücher abrufen
curl -X GET "http://localhost:8000/api/books"

# Nach Autor suchen
curl -X GET "http://localhost:8000/api/books?author=Douglas%20Adams"

# Benutzer anlegen
curl -X POST "http://localhost:8000/api/users" -H "Content-Type: application/json" -d '{"first_name":"Max","last_name":"Mustermann","email":"max@uni.de"}'
```

## Vorteile von Containern

- Keine lokale Datenbankinstallation nötig
- Reproduzierbare Umgebung für Entwicklung und Tests
- Einfaches Deployment

## Datenbank-Zugangsdaten

- Nutzer: `library_user`
- Passwort: `library_pass123`
- Datenbank: `library_system`

---

**Viel Erfolg bei deiner Hausarbeit!**