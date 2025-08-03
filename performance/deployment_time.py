import subprocess
import time

start = time.time()
# Docker starten
process = subprocess.Popen(
    ["docker", "compose", "up", "--build"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)
for line in process.stdout:
    print(line.decode(), end="")
process.wait()
end = time.time()

duration = end - start
print(f"\nDeployment-Dauer: {duration:.2f} Sekunden")

# Messwert abspeichern im Vergleich zu Startzeitpunkt
with open("performance/deployment_result.txt", "w") as f:
    f.write(f"Deployment-Dauer: {duration:.2f} Sekunden\n")