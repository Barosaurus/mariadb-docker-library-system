import subprocess
import time

CONTAINER_NAMES = [
    "mariadb-docker-library-system-backend-1",
    "mariadb-docker-library-system-mariadb-1",
    "mariadb-docker-library-system-phpmyadmin-1"
]

def get_stats(container):
    result = subprocess.run([
        "docker", "stats", container, "--no-stream", "--format",
        "{{.Name}},{{.CPUPerc}},{{.MemUsage}}"
    ], capture_output=True, text=True)
    return result.stdout.strip()

# Kurze Pause, um sicherzustellen, dass die Container stabil laufen
print("Warte 10 Sekunden, damit sich die Container stabilisieren...")
time.sleep(10)

stats = []
for name in CONTAINER_NAMES:
    stat = get_stats(name)
    print(stat)
    stats.append(stat)

# Ergebnis als CSV
with open("performance/resource_result.csv", "w") as f_csv:
    f_csv.write("Container,CPU (%),RAM\n")
    for line in stats:
        f_csv.write(line + "\n")

# Ergebnis als TXT 
with open("performance/resource_result.txt", "w") as f_txt:
    f_txt.write("Ressourcenverbrauch je Container:\n")
    for line in stats:
        try:
            parts = line.split(",")
            f_txt.write(f"Container: {parts[0]}, CPU: {parts[1]}, RAM: {parts[2]}\n")
        except Exception:
            f_txt.write(f"{line}\n")

print("\nRAM/CPU-Messwerte in performance/resource_result.csv und performance/resource_result.txt gespeichert.")