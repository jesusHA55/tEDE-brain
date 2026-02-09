import threading
import pygame
from brain import tEDE_Brain
from voices import speak
from face import tEDE_Face

def logic_loop(brain, face):
    """
    Este hilo gestiona la interaccion con Ollama y la voz.
    Se ejecuta en paralelo para que la cara no se detenga.
    """
    print(">>> tED-E Sistema Operativo Iniciado <<<")
    print("Escribe tu mensaje en la terminal (o 'salir' para cerrar)")

    while face.running:
        # El input() bloquea este hilo, pero NO el hilo principal de Pygame
        u_input = input("\n[Usuario]: ")
        
        if u_input.lower() in ["salir", "exit", "quit"]:
            face.running = False
            break
        
        # 1. Cambiamos la cara a modo 'pensando' mientras Ollama procesa
        face.update_emotion("THINKING")
        
        # 2. Consultamos al cerebro
        texto, emocion = brain.ask(u_input)
        
        # 3. Mostramos logs y actualizamos cara/voz
        print(f"[tED-E]: {texto} // {emocion}")
        face.update_emotion(emocion)
        speak(texto)

def main():
    # Inicializacion de modulos
    brain = tEDE_Brain()
    face = tEDE_Face()
    
    # Lanzamos el hilo de logica como 'daemon' para que se cierre con el programa
    t = threading.Thread(target=logic_loop, args=(brain, face), daemon=True)
    t.start()

    # BUCLE PRINCIPAL (Visual)
    # Pygame DEBE correr en el hilo principal
    try:
        while face.running:
            # Gestionar eventos de ventana (cerrar con la X o ESC)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    face.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        face.running = False
            
            # Dibujar el siguiente frame de la animacion actual
            # Nota: face.draw() ya contiene el clock.tick(5)
            face.draw()
            
    except KeyboardInterrupt:
        print("\nApagando tED-E...")
    finally:
        face.quit()

if __name__ == "__main__":
    main()
