import pyaudio
import numpy as np
from openwakeword.model import Model
from faster_whisper import WhisperModel

# Configuracion del audio
CHANNELS = 1
RATE = 16000
CHUNK = 1280  # ~80ms de audio

# Cargar el modelo que generaste (o uno por defecto para probar)
# Sustituye 'ede.onnx' por la ruta a tu archivo generado
model = Model(wakeword_models=["ED-E/models/wakeword/ede.onnx"], inference_framework="onnx")

audio = pyaudio.PyAudio()
mic_stream = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, 
                        input=True, frames_per_buffer=CHUNK)

print("tED-E is listening...")

try:
    while True:
        # Capturar audio del Netbot
        buf = mic_stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(buf, dtype=np.int16)
        
        # Prediccion
        prediction = model.predict(audio_data)
        
        # El umbral estondar es 0.5
        for mdl, score in prediction.items():
            if score > 0.6:  # Ajusta este valor según falsos positivos
                print(f"Word detected! Score: {score}")
                # Imprimimos lo escuchado anteriormente, que deberia ser la wakeword
                segments, info = model.transcribe(audio_np, beam_size=5)
                for segment in segments:
                    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
except KeyboardInterrupt:
    mic_stream.stop_stream()
    mic_stream.close()
    audio.terminate()
