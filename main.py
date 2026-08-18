import random
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
from googletrans import Translator


# ==========================================
# ENGLISH VOICE CHALLENGE
# ==========================================

print(" _____ _   _  ____ _      ___ ____  _   _ ")
print("| ____| \ | |/ ___| |    |_ _/ ___|| | | |")
print("|  _| |  \| | |  _| |     | |\___ \| |_| |")
print("| |___| |\  | |_| | |___  | | ___) |  _  |")
print("|_____|_| \_|\____|_____|___|____/|_| |_|")
print()
print("          VOICE CHALLENGE")
print()
print("Di la traduccion de la palabra en INGLES.")
print("Tienes maximo 3 errores.")
print("Intenta conseguir la mayor puntuacion!")
print()


# ==========================================
# NIVELES DE DIFICULTAD
# ==========================================

words_by_level = {
    "facil": [
        "gato",
        "perro",
        "manzana",
        "leche",
        "sol"
    ],

    "medio": [
        "banano",
        "escuela",
        "amigo",
        "ventana",
        "amarillo"
    ],

    "dificil": [
        "tecnologia",
        "universidad",
        "informacion",
        "pronunciacion",
        "imaginacion"
    ]
}


# ==========================================
# SELECCIONAR NIVEL
# ==========================================

print("Selecciona tu nivel:")
print("1. Facil")
print("2. Medio")
print("3. Dificil")

opcion = input("Escribe 1, 2 o 3: ")

if opcion == "1":
    nivel = "facil"
elif opcion == "2":
    nivel = "medio"
elif opcion == "3":
    nivel = "dificil"
else:
    print("Opcion no valida. Se seleccionara Facil.")
    nivel = "facil"

print()
print("NIVEL SELECCIONADO:", nivel.upper())
print()


# ==========================================
# VARIABLES DEL JUEGO
# ==========================================

score = 0
errors = 0
streak = 0

translator = Translator()
recognizer = sr.Recognizer()


# ==========================================
# BUCLE PRINCIPAL DEL JUEGO
# ==========================================

while errors < 3:

    # Seleccionar una palabra aleatoria
    spanish_word = random.choice(words_by_level[nivel])

    print("-" * 45)
    print("PALABRA:", spanish_word.upper())
    print("Di su traduccion en INGLES")
    print("-" * 45)

    input("Presiona ENTER para comenzar a grabar...")

    # ======================================
    # GRABAR VOZ
    # ======================================

    print()
    print("Grabando... Habla ahora!")

    seconds = 4
    sample_rate = 44100

    recording = sd.rec(
        int(seconds * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    # Guardar la grabacion como PCM WAV
    write("voz.wav", sample_rate, recording)

    print("Grabacion terminada.")


    # ======================================
    # RECONOCIMIENTO DE VOZ
    # ======================================

    try:

        with sr.AudioFile("voz.wav") as source:
            audio = recognizer.record(source)

        recognized = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        # Convertir a minusculas
        recognized = recognized.lower().strip()

        print("Dijiste:", recognized)

    except sr.UnknownValueError:

        print("No pude entender tu voz.")

        errors += 1
        streak = 0

        print("Errores:", errors, "/ 3")
        continue

    except sr.RequestError:

        print("No se pudo conectar con el reconocimiento de voz.")
        print("Revisa tu conexion a Internet.")
        break

    except Exception as error:

        print("Ocurrio un error con el audio:")
        print(error)

        errors += 1
        streak = 0

        print("Errores:", errors, "/ 3")
        continue


    # ======================================
    # TRADUCIR LA PALABRA
    # ======================================

    try:

        translation = translator.translate(
            spanish_word,
            src="es",
            dest="en"
        )

        # Convertir la traduccion a minusculas
        correct_answer = translation.text.lower().strip()

        print("Traduccion correcta:", correct_answer)

    except Exception as error:

        print("No se pudo realizar la traduccion.")
        print(error)
        break


    # ======================================
    # COMPARAR RESPUESTAS
    # ======================================

    if recognized == correct_answer:

        score += 1
        streak += 1

        print()
        print("CORRECTO!")
        print("+1 PUNTO")
        print("Racha:", streak)

        if streak >= 3:
            print("SUPER RACHA!")

    else:

        errors += 1
        streak = 0

        print()
        print("INCORRECTO")
        print("La respuesta correcta era:", correct_answer)
        print("Errores:", errors, "/ 3")


    # ======================================
    # MOSTRAR MARCADOR
    # ======================================

    print()
    print("PUNTUACION:", score)
    print("ERRORES:", errors)
    print()


# ==========================================
# FIN DEL JUEGO
# ==========================================

print()
print("=" * 45)
print("             GAME OVER")
print("=" * 45)

print("PUNTUACION FINAL:", score)
print("ERRORES:", errors)

if score >= 5:
    print("EXCELENTE! ERES UNA MAQUINA DEL INGLES!")
elif score >= 3:
    print("MUY BIEN! SIGUE PRACTICANDO!")
else:
    print("BUEN INTENTO! PUEDES MEJORAR!")

print()
print("Gracias por jugar ENGLISH VOICE CHALLENGE")
print("=" * 45)
