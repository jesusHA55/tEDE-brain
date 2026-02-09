import subprocess
import os

# Configura aqui tus rutas locales
BASE_DIR = "/home/tede/tEDEOS/voices"
PIPER_EXE = os.path.join(BASE_DIR, "piper", "piper")
PIPER_MODEL = os.path.join(BASE_DIR, "en_US-danny-low.onnx")

def speak(text):
    if not text:
        return
        
    clean_text = text.replace('"', '').replace('\n', ' ')
    print(clean_text)
    
    # Verificacion de que el modelo NO sea un HTML (por si acaso)
    if os.path.getsize(PIPER_MODEL) < 1000000: # Un modelo real pesa MBs
        print("[VOICE ERROR]: El archivo del modelo es demasiado pequeno. Es un HTML?")
        return

    # Comando optimizado para PipeWire
    # Usamos pw-play en lugar de aplay
    command = f'echo "{clean_text}" | {PIPER_EXE} --model {PIPER_MODEL} --output_raw | pw-play --rate 22050 --format s16 --channels 1 --raw -'
    
    try:
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error lanzando voz: {e}")
