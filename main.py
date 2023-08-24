import subprocess
import threading
import keyboard

# 1つ目のPythonファイルを実行する関数
def execute_first_program():
    subprocess.run(["python", "play_snd1.py"])

# 2つ目のPythonファイルを実行する関数
def execute_second_program():
    subprocess.run(["python", "play_jdc1.py"])

# キーボードのイベントを監視するスレッド
def key_listener():
    keyboard.wait("a")  # キーボードのキーを指定
    execute_second_program()

# 1つ目のPythonファイルを実行
execute_first_program()

# キーボードのイベントを監視するスレッドを開始
thread = threading.Thread(target=key_listener)
thread.start()

# 1つ目のPythonファイルの実行が終了するまで待機
thread.join()

print("プログラムが終了しました")
