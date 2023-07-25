import speech_recognition as sr

def ouvir_e_escrever():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Diga algo...")
        recognizer.adjust_for_ambient_noise(source)  # Ajusta o nível de ruído ambiente
        audio = recognizer.listen(source)

    try:
        print("Reconhecendo...")
        texto = recognizer.recognize_google(audio, language="pt-BR")  # Reconhece a fala em Português do Brasil
        print("Você disse: ", texto)
    except sr.UnknownValueError:
        print("Não foi possível entender o que você disse.")
    except sr.RequestError as e:
        print(f"Não foi possível acessar o serviço de reconhecimento de voz; {e}")

if __name__ == "__main__":
    ouvir_e_escrever()
