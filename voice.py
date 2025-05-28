import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr

from googletrans import Translator
import random


# Создаем нашу запись

duration = 5  # секунды записи
sample_rate = 44100
osh = 0

# Словарь

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}


print('Добро пожаловать в игру "Говори правильно"!')
print('Выбери уровень сложности: easy / medium / hard: ')
level = input('>>> ').strip().lower()

if level == 'easy':
    rand = random.choice(words_by_level["easy"])
    print(f'Ваше слово для перевода: {rand}')
elif level == 'medium':
    rand = random.choice(words_by_level["medium"])
    print(f'Ваше слово для перевода: {rand}')
elif level == 'hard':
    rand = random.choice(words_by_level["hard"])
    print(f'Ваше слово для перевода: {rand}')


print("Говори...")
recording = sd.rec(
  int(duration * sample_rate), # длительность записи в сэмплах
  samplerate=sample_rate,      # частота дискретизации
  channels=1,                  # 1 — это моно
  dtype="int16")               # формат аудиоданных
sd.wait()  # ждём завершения записи


wav.write("output.wav", sample_rate, recording)
print("✅ Запись завершена, теперь распознаём...")


# Распознаем нашу запись

recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="en-US").lower()
        print("Ты сказал:", text)

        translator = Translator()
        translated = translator.translate(rand, dest = 'en')  # здесь 'en' — это английский

        print(f'Правильный перевод: {translated.text}')

        # Проверка 
        if text == translated.text:
            print('Правильно!')
        else:
            print('Неправильно!')

    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("❌ Не удалось распознать речь.")
    except sr.RequestError as e:             # - если нет интернета или API недоступен
        print(f"⚠ Ошибка сервиса: {e}")




