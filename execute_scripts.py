import os
import subprocess


def run(file):
    output_name = file.replace('.robot', '.xml')
    log_name = file.replace('.robot', '.html')
    report_name = file.replace('.robot', '_report.html')
    subprocess.run(f"robot --timestampoutputs --outputdir reports --output {output_name} --log {log_name} --report {report_name} scripts/{file}", shell=True)


def fetch_scripts_to_run():
    files = []
    for file in os.listdir('scripts'):
        if file.endswith('.robot'):
            files.append(file)
    files.sort()
    for file in files:
        run(file)


fetch_scripts_to_run()
