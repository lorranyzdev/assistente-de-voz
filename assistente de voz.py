import speech_recognition as sr
import pyttsx3
import subprocess
import os
import time
from pathlib import Path
import webbrowser


TEXT_TO_SPEECH_RATE = 187
TEXT_TO_SPEECH_VOLUME = 1.0
MIC_ADJUSTMENT_DURATION = 2
MIC_TIMEOUT = 20           
MIC_PHRASE_LIMIT = 30      

# Inicializa o mecanismo de texto para fala com as configurações definidas
def init_text_to_speech():
    engine = pyttsx3.init()
    engine.setProperty('rate', TEXT_TO_SPEECH_RATE)
    engine.setProperty('volume', TEXT_TO_SPEECH_VOLUME)
    return engine

# Fala o texto usando o mecanismo de voz e imprime no terminal
def speak(text, engine):
    print(f"Assistente: {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)

# Escuta a entrada do microfone e tenta reconhecer o que foi dito
def listen_command(recognizer, source):
    """Ouve e reconhece comandos de voz."""
    print("Aguardando a sua fala...")
    try:
        audio = recognizer.listen(source, timeout=MIC_TIMEOUT, phrase_time_limit=MIC_PHRASE_LIMIT)
        print("Reconhecendo o que você disse...")
        command = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {command}")
        return command.lower()
    except sr.WaitTimeoutError:
        speak("Você não falou nada. Tente novamente.", engine)
    except sr.UnknownValueError:
        speak("Desculpe, não consegui entender o que você disse.", engine)
    except sr.RequestError as e:
        speak(f"Erro ao se conectar ao serviço de reconhecimento de voz: {e}", engine)
    except Exception as e:
        speak(f"Ocorreu um erro inesperado: {e}", engine)
    return ""

# Procura o caminho do executável do aplicativo com base em seu nome
def find_executable(app_name):
    paths = {
        "spotify": [
            os.path.expanduser(r"~\AppData\Roaming\Spotify\Spotify.exe"),
            r"C:\Program Files\Spotify\Spotify.exe"
        ],
        "whatsapp": [
            os.path.expanduser(r"~\AppData\Local\WhatsApp\WhatsApp.exe"),
            r"C:\Program Files\WhatsApp\WhatsApp.exe"
        ],
        "valorant": [
            r"C:\Riot Games\VALORANT\live\ShooterGame\Binaries\Win64\VALORANT-Win64-Shipping.exe",
            os.path.expanduser(r"~\AppData\Local\Riot Games\VALORANT\live\ShooterGame\Binaries\Win64\VALORANT-Win64-Shipping.exe")
        ],
        "undertale": [
            r"C:\Program Files (x86)\Steam\steamapps\common\Undertale\Undertale.exe",
            r"C:\Program Files\Steam\steamapps\common\Undertale\Undertale.exe",
            os.path.expanduser(r"~\AppData\Local\Undertale\Undertale.exe")
        ]
    }
    
    for path in paths.get(app_name.lower(), []):
        if os.path.exists(path):
            return path
    return None

# Tenta abrir o Spotify via caminho local ou protocolo URI
def open_spotify(engine):
    path = find_executable("spotify")
    if path:
        try:
            subprocess.Popen(path)
            speak("Abrindo o Spotify.", engine)
        except Exception as e:
            speak(f"Erro ao abrir o Spotify: {e}", engine)
    else:
        try:
            subprocess.run(['start', 'spotify:'], shell=True)
            speak("Abrindo o Spotify.", engine)
        except Exception as e:
            speak(f"Spotify não encontrado ou erro ao abrir: {e}", engine)

# Tenta abrir o WhatsApp via caminho local ou protocolo URI
def open_whatsapp(engine):
    path = find_executable("whatsapp")
    if path:
        try:
            subprocess.Popen(path)
            speak("Abrindo o WhatsApp.", engine)
        except Exception as e:
            speak(f"Erro ao abrir o WhatsApp: {e}", engine)
    else:
        try:
            subprocess.run(['start', 'whatsapp:'], shell=True)
            speak("Abrindo o WhatsApp.", engine)
        except Exception as e:
            speak(f"WhatsApp não encontrado ou erro ao abrir: {e}", engine)

# Abre o Bloco de Notas (Notepad)
def open_notepad(engine):
    try:
        subprocess.run(['notepad'], shell=True)
        speak("Abrindo o Bloco de Notas.", engine)
    except Exception as e:
        speak(f"Erro ao abrir o Bloco de Notas: {e}", engine)

# Abre a Calculadora do Windows
def open_calculator(engine):
    try:
        subprocess.run(['calc'], shell=True)
        speak("Abrindo a Calculadora.", engine)
    except Exception as e:
        try:
            subprocess.run(['start', 'calculator:'], shell=True)
            speak("Abrindo a Calculadora (versão Microsoft Store).", engine)
        except Exception as e2:
            speak(f"Erro ao abrir a Calculadora: {e2}", engine)

# Tenta abrir o jogo Valorant usando o cliente da Riot ou diretamente
def open_valorant(engine):
    path = find_executable("valorant")
    if path:
        try:
            riot_client = r"C:\Riot Games\Riot Client\RiotClientServices.exe"
            if os.path.exists(riot_client):
                subprocess.Popen([riot_client, "--launch-product=valorant", "--launch-patchline=live"])
                speak("Abrindo o Valorant.", engine)
            else:
                subprocess.Popen([path])
                speak("Abrindo o Valorant diretamente.", engine)
        except Exception as e:
            speak(f"Erro ao abrir o Valorant: {e}", engine)
    else:
        speak("Valorant não encontrado.", engine)

# Tenta abrir o jogo Undertale
def open_undertale(engine):
    path = find_executable("undertale")
    if path:
        try:
            subprocess.Popen(path)
            speak("Abrindo o Undertale.", engine)
        except Exception as e:
            speak(f"Erro ao abrir o Undertale: {e}", engine)
    else:
        speak("Undertale não encontrado.", engine)

# Abre o YouTube no navegador padrão
def open_youtube(engine):
    try:
        webbrowser.open("https://www.youtube.com")
        speak("Abrindo o YouTube.", engine)
    except Exception as e:
        speak(f"Erro ao abrir o YouTube: {e}", engine)

# Abre o Google no navegador padrão
def open_google(engine):
    try:
        webbrowser.open("https://www.google.com")
        speak("Abrindo o Google.", engine)
    except Exception as e:
        speak(f"Erro ao abrir o Google: {e}", engine)

# Abre o LinkedIn no navegador padrão
def open_linkedin(engine):
    try:
        webbrowser.open("https://www.linkedin.com")
        speak("Abrindo o Linkedin.", engine)
    except Exception as e:
        speak(f"Erro ao abrir o Linkedin: {e}", engine)

# Função principal que executa o assistente de voz
def run_assistant():
    global engine
    engine = init_text_to_speech()
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print(f"Ajustando ruído ambiente... Aguarde {MIC_ADJUSTMENT_DURATION} segundos.")
        recognizer.adjust_for_ambient_noise(source, duration=MIC_ADJUSTMENT_DURATION)
        recognizer.dynamic_energy_threshold = True

        speak("Oii, sou sua assistente de voz (ꈍᴗꈍ)♡", engine)

        while True:
            command = listen_command(recognizer, source)
            if not command:
                continue

            print(f">> Comando reconhecido: {command}")

            if "spotify" in command:
                open_spotify(engine)
            elif "whatsapp" in command:
                open_whatsapp(engine)
            elif "bloco de notas" in command or "notepad" in command:
                open_notepad(engine)
            elif "calculadora" in command:
                open_calculator(engine)
            elif "valorant" in command:
                open_valorant(engine)
            elif "undertale" in command:
                open_undertale(engine)
            elif "youtube" in command:
                open_youtube(engine)
            elif "google" in command:
                open_google(engine)
            elif "linkedin" in command or "linked in" in command:
                open_linkedin(engine)
            elif "sair" in command or "encerrar" in command:
                speak("Encerrando. Até mais!", engine)
                print("Tchauzinho <3")
                break
            else:
                speak("Comando não reconhecido. Tente novamente.", engine)

# Ponto de entrada do programa. Inicia o assistente e trata erros.
if __name__ == "__main__":
    try:
        run_assistant()
    except KeyboardInterrupt:
        print("\n>> Assistente encerrado pelo usuário.")


