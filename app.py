import os
from flask import Flask, render_template, request, jsonify
import subprocess
import validators

app = Flask(__name__)

@app.route('/ferramentas_web')
def ferramentas_web():
    return render_template('ferramentas_web.html')

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para theHarvester (corrigida)
@app.route('/theharvester', methods=['GET', 'POST'])
def theharvester():
    if request.method == 'POST':
        domain = request.form['domain']
        try:
            command = ["theHarvester", "-d", domain, "-b", "all"]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return render_template('theharvester_result.html', result=result.stdout)
        except subprocess.CalledProcessError as e:
            return render_template('theharvester_result.html', result=f"Erro: {e.stderr}")
    return render_template('theharvester_form.html')

# Rota para Sherlock
@app.route('/sherlock', methods=['GET', 'POST'])
def sherlock():
    if request.method == 'POST':
        username = request.form['username']
        try:
            command = ["sherlock", username]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return render_template('sherlock_result.html', result=result.stdout)
        except subprocess.CalledProcessError as e:
            return render_template('sherlock_result.html', result=f"Erro: {e.stderr}")
    return render_template('sherlock_form.html')

# Rota para PhoneInfoga
@app.route('/phoneinfoga', methods=['GET', 'POST'])
def phoneinfoga():
    if request.method == 'POST':
        number = request.form['number']
        try:
            if os.path.exists('/home/kali/osint_tool/phoneinfoga'):
                command = ["/home/kali/osint_tool/phoneinfoga", "scan", "-n", number]
            else:
                command = ["phoneinfoga", "scan", "-n", number]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return render_template('phoneinfoga_result.html', result=result.stdout)
        except subprocess.CalledProcessError as e:
            return render_template('phoneinfoga_result.html', result=f"Erro: {e.stderr}")
    return render_template('phoneinfoga_form.html')

# Rota para Nmap
@app.route('/nmap', methods=['GET', 'POST'])
def nmap():
    if request.method == 'POST':
        target = request.form['target'].strip()
        options = request.form.get('options', '')
        try:
            if not target:
                return render_template('nmap_result.html', result="Erro: Alvo não fornecido.", target="", options="")
            if not (validators.ipv4(target) or validators.domain(target)):
                return render_template('nmap_result.html', result="Erro: Alvo inválido. Insira um IP ou domínio válido.", target=target, options=options)
            command = ["nmap"]
            if options:
                command.extend(options.split())
            command.extend(["-sV", "-A", target])
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output = result.stdout
        except subprocess.CalledProcessError as e:
            output = f"Erro ao executar Nmap: {e.stderr}"
        except Exception as e:
            output = f"Erro inesperado: {str(e)}"
        return render_template('nmap_result.html', result=output, target=target, options=options)
    return render_template('nmap_form.html')

# Rota para opções do Nmap
@app.route('/nmap/options', methods=['GET'])
def nmap_options():
    nmap_options = {
        "Escaneamento Básico": [
            "-sV: Detecta versões de serviços",
            "-A: Escaneamento agressivo (OS, versão, scripts, traceroute)",
            "-p <portas>: Especifica portas (ex.: -p 80,443 ou -p 1-1000)"
        ],
        "Escaneamento de Vulnerabilidades": [
            "--script vuln: Verifica vulnerabilidades comuns",
            "--script http-vuln-cveYYYY-NNNN: Verifica vulnerabilidades específicas (substitua YYYY-NNNN por uma CVE)",
            "--script ssl-heartbleed: Verifica vulnerabilidade Heartbleed",
            "--script http-enum: Enumera diretórios e arquivos web"
        ],
        "Performance": [
            "-T4: Aumenta a velocidade do escaneamento (moderado)",
            "-T5: Aumenta ainda mais a velocidade (rápido, mas menos preciso)"
        ],
        "Outros": [
            "-O: Detecta sistema operacional",
            "-sU: Escaneia portas UDP",
            "--host-timeout <tempo>: Limita o tempo por host (ex.: --host-timeout 30s)"
        ]
    }
    return jsonify(nmap_options)

# Rota para Whois
@app.route('/whois', methods=['GET', 'POST'])
def whois():
    if request.method == 'POST':
        target = request.form['target']
        try:
            command = ["whois", target]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return render_template('whois_result.html', result=result.stdout)
        except subprocess.CalledProcessError as e:
            return render_template('whois_result.html', result=f"Erro: {e.stderr}")
    return render_template('whois_form.html')

# Rota para ExifTool
@app.route('/exiftool', methods=['GET', 'POST'])
def exiftool():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('exiftool_form.html', error="Nenhum arquivo enviado.")
        file = request.files['file']
        if file.filename == '':
            return render_template('exiftool_form.html', error="Nenhum arquivo selecionado.")
        if file and file.filename:
            filepath = os.path.join('/tmp', file.filename)
            file.save(filepath)
            try:
                command = ["exiftool", filepath]
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                os.remove(filepath)
                return render_template('exiftool_result.html', result=result.stdout)
            except subprocess.CalledProcessError as e:
                os.remove(filepath)
                return render_template('exiftool_result.html', result=f"Erro: {e.stderr}")
    return render_template('exiftool_form.html')

# Rota para Shodan (versão limitada com myip, info e version)
@app.route('/shodan', methods=['GET', 'POST'])
def shodan_search():
    if request.method == 'POST':
        try:
            output = ""
            # Obter o IP público
            myip_command = ["shodan", "myip"]
            myip_result = subprocess.run(myip_command, capture_output=True, text=True, check=True)
            output += f"Seu IP público: {myip_result.stdout.strip()}\n"

            # Obter informações da conta
            info_command = ["shodan", "info"]
            info_result = subprocess.run(info_command, capture_output=True, text=True, check=True)
            output += f"Informações da conta:\n{info_result.stdout}"

            # Obter versão do CLI
            version_command = ["shodan", "version"]
            version_result = subprocess.run(version_command, capture_output=True, text=True, check=True)
            output += f"Versão do Shodan CLI: {version_result.stdout.strip()}"

            return render_template('shodan_result.html', result=output)
        except subprocess.CalledProcessError as e:
            return render_template('shodan_result.html', result=f"Erro: {e.stderr}")
    return render_template('shodan_form.html')

@app.route('/reconng', methods=['GET', 'POST'])
def reconng():
    if request.method == 'POST':
        domain = request.form['domain']
        try:
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp_file.write(f"workspaces create temp_{domain.replace('.', '_')}\n")
            temp_file.write(f"modules load recon/domains-hosts/brute_hosts\n")
            temp_file.write(f"options set SOURCE {domain}\n")
            temp_file.write("run\n")
            temp_file.write("show hosts\n")
            temp_file.write("exit\n")
            temp_file_name = temp_file.name
            temp_file.close()

            command = ["recon-ng", "-r", temp_file_name]
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            # Filtrar apenas a tabela 'show hosts'
            output = result.stdout
            start_marker = "show hosts\n"
            end_marker = "[recon-ng][temp_"
            if start_marker in output:
                start_idx = output.index(start_marker) + len(start_marker)
                end_idx = output.index(end_marker, start_idx) if end_marker in output[start_idx:] else len(output)
                filtered_result = output[start_idx:end_idx].strip()
            else:
                filtered_result = "Nenhum resultado encontrado."

            return render_template('reconng_result.html', result=filtered_result)
        except subprocess.CalledProcessError as e:
            return render_template('reconng_result.html', result=f"Erro durante execução:\n{e.stderr}")
        finally:
            if 'temp_file_name' in locals():
                os.remove(temp_file_name)
    return render_template('reconng_form.html')

if __name__ == '__main__':
    app.run(debug=True)
