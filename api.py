import os
import sys
import argparse
from flask import Flask, request, jsonify, send_file

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 src 目录的绝对路径
src_dir = os.path.join(current_dir, 'src')
# 将 src 目录添加到 sys.path
sys.path.append(src_dir)

from src.f5_tts import F5TTS

app = Flask(__name__)

# 实例化 F5TTS 类
f5tts = F5TTS(hf_cache_dir = './hf_download')

# 设置保存生成音频和频谱图的临时目录
temp_dir = "temp_outputs"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

@app.route('/tts', methods=['GET','POST'])
def tts():
    data = request.json
    print(f"即将开始制作....")
    # 参考音频
    ref_text = data.get('prompt_text', '你好啊')
    # 参考音频
    ref_audio_path = data.get('ref_audio_path', '')
    # 要生成的音频
    gen_text = data.get('gen_text', '')
    # 导出的文件名
    output_file = data.get('output_file', '')
    # 语速
    speed_factor = data.get('speed_factor', 1)
    # 种子
    seed = data.get('seed', -1)
    print(f'导出目录{output_file}')

    # 调用 infer 方法生成音频和频谱图
    wav, sr, spect = f5tts.infer(
        ref_file=ref_audio_path,
        ref_text=ref_text,
        gen_text=gen_text,
        file_wave=output_file,
        speed=speed_factor,
        seed=seed  # 使用随机种子
    )

    print(f'制作成功')
    out = {
        "path": output_file,
        "success": 1
     }
    print(f'生成成功{out}')
    return jsonify(out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='F5-tts一句话克隆')
    parser.add_argument('--port', type=int, default=6020, help='输入端口号')
    args = parser.parse_args()
    port = args.port
    # 启动 Flask 应用到 6020 端口
    app.run(host='0.0.0.0', port=port)
    print(f'服务启动成功，端口号：{port}')