import speech_recognition as sr
import pyttsx3
import subprocess
import os
import time
from pathlib import Path 


TEXT_TO_SPEECH_RATE = 187
TEXT_TO_SPEECH_VOLUME = 1.0
MIC_ADJUSTMENT_DURATION = 2
MIC_TIMEOUT = 10
MIC_PHRASE_LIMIT = 15

def init_text_to_speech():
    """Inicializa o motor de text-to-speech."""
    engine = pyttsx3.init()
    engine.setProperty('rate', TEXT_TO_SPEECH_RATE)
    engine.setProperty('volume', TEXT_TO_SPEECH_VOLUME)
    return engine


def speak(text, engine):
    """Fala o texto fornecido e imprime no console."""
    print(f"Assistente: {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)  

def listen_command(recognizer, source):
    """Ouve e reconhece comandos de voz."""
    print("O que você deseja?")
    try:
        audio = recognizer.listen(source, timeout=MIC_TIMEOUT, phrase_time_limit=MIC_PHRASE_LIMIT)
        command = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {command}")
        return command.lower()
    except sr.WaitTimeoutError:
        speak("Nenhum comando detectado. Tente novamente.", engine)
    except sr.UnknownValueError:
        speak("Não entendi o que você disse.", engine)
    except sr.RequestError as e:
        speak(f"Erro de conexão: {e}", engine)
    return ""


def find_executable(app_name):
    """Localiza o executável de um aplicativo."""
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

def open_spotify(engine):
    """Abre o Spotify."""
    path = find_executable("spotify")
    if path:
        try:
            subprocess.Popen(path)
            speak("Abrindo o Spotify.", engine)
        except Exception as e:
            speak(f"Erro ao abrir o Spotify (versão desktop): {e}", engine)
    else:
        try:
            subprocess.run(['start', 'spotify:'], shell=True)
            speak("Abrindo o Spotify", engine)
        except Exception as e:
            speak(f"Spotify não encontrado ou erro ao abrir: {e}. Verifique se está instalado.", engine)

def open_whatsapp(engine):
    """Abre o WhatsApp."""
    path = find_executable("whatsapp")
    if path:
        try:
            subprocess.Popen(path)
            speak("Abrindo o WhatsApp.", engine)
        except Exception as e:
            speak(f"Erro ao abrir o WhatsApp (versão desktop): {e}", engine)
    else:
        try:
            subprocess.run(['start', 'whatsapp:'], shell=True)
            speak("Abrindo o WhatsApp", engine)
        except Exception as e:
            speak(f"WhatsApp não encontrado ou erro ao abrir: {e}. Verifique se está instalado.", engine)

def open_notepad(engine):
    """Abre o Bloco de Notas."""
    try:
        subprocess.run(['notepad'], shell=True)
        speak("Abrindo o Bloco de Notas.", engine)
    except Exception as e:
        speak(f"Erro ao abrir o Bloco de Notas: {e}", engine)

def open_calculator(engine):
    """Abre a Calculadora."""
    try:
        subprocess.run(['calc'], shell=True)
        speak("Abrindo a Calculadora.", engine)
    except Exception as e:
        try:
            subprocess.run(['start', 'calculator:'], shell=True)
            speak("Abrindo a Calculadora (versão Microsoft Store).", engine)
        except Exception as e2:
            speak(f"Erro ao abrir a Calculadora: {e2}. Verifique se está instalado.", engine)

def open_valorant(engine):
    """Abre o Valorant."""

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
            speak(f"Erro ao abrir o Valorant: {str(e)}", engine)
    else:
        
        possible_paths = [
            Path(r"C:\Riot Games\VALORANT\live\VALORANT.exe"),
            Path(r"C:\Program Files\Riot Games\VALORANT\live\VALORANT.exe")
        ]
        
        for valorant_path in possible_paths:
            if valorant_path.exists():
                try:
                    subprocess.Popen([str(valorant_path)])
                    speak("Abrindo o Valorant a partir do caminho padrão.", engine)
                    return
                except Exception as e:
                    speak(f"Erro ao abrir o Valorant: {str(e)}", engine)
                    return
        
        speak("Valorant não encontrado. Verifique se está instalado e o caminho está correto.", engine)

def open_undertale(engine):
    """Abre o jogo Undertale."""
    
    path = find_executable("undertale")
    if path:
        try:
            subprocess.Popen(path)
            speak("Abrindo o Undertale.", engine)
        except Exception as e:
            speak(f"Erro ao abrir o Undertale: {str(e)}", engine)
    else:
        speak("Undertale não encontrado. Verifique se está instalado e o caminho está correto.", engine)


def run_assistant():
    """Executa o assistente de voz."""
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
            elif "sair" in command or "encerrar" in command:
                speak("Encerrando. Até mais!", engine)
                break
            else:
                speak("Comando não reconhecido. Tente novamente.", engine)

if __name__ == "__main__":
    try:
        run_assistant()
    except KeyboardInterrupt:
        print("\nAssistente encerrado pelo usuário.")
    except Exception as e:
        print(f"Erro inesperado: {e}")