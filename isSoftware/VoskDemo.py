# fr"C:\Users\16616\Desktop\vosk\vosk-model-small-cn-0.22" # 替换为你的模型路径

import os
import pyperclip
import vosk

# 下载并解压 Vosk 模型
# 你可以从 https://alphacephei.com/vosk/models 下载中文模型
# 获取用户桌面的路径
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
model_path = desktop_path+fr"\vosk\vosk-model-small-cn-0.22"  # 替换为模型路径

model = vosk.Model(model_path)

# 创建一个 recognizer
recognizer = vosk.KaldiRecognizer(model, 16000)

# 使用麦克风作为音频源
import pyaudio

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("请说话...")

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()

        # 检查 result 是否为空
        if result:
        # 复制文本到剪贴板
         pyperclip.copy(result)
         print(result)
    # else:
        # partial_result = recognizer.PartialResult()
        # print(partial_result)