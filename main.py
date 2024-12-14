from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pynput import keyboard

# Получаем устройство микрофона
devices = AudioUtilities.GetMicrophone()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Флаг для отслеживания состояния микрофона
mic_muted = True
hot_key = keyboard.Key.home


# Функция для включения/выключения микрофона
def mute_mic(mute: bool):
    volume.SetMute(mute, None)
    if mute:
        print("Микрофон выключен")
    else:
        print("Микрофон включен")


# Обработчики событий клавиатуры
def on_press(key):
    global mic_muted
    try:
        if key == hot_key:
            if mic_muted:
                mute_mic(False)
                mic_muted = False
    except AttributeError:
        pass


def on_release(key):
    global mic_muted
    if key == hot_key:
        if not mic_muted:
            mute_mic(True)
            mic_muted = True


# Основная логика работы с клавишами
def start_ptt():
    # Изначально выключаем микрофон
    mute_mic(True)

    # Прослушиваем нажатие клавиш
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    print("Запущен режим Push-to-Talk. Нажмите выбранную клавишу, чтобы говорить.")
    start_ptt()
