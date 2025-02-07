import configparser
import os
import subprocess
import logging
import platform
import sys

# 确保 logs 目录存在
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 设置日志文件路径
log_file = os.path.join(log_dir, "video_tool.log")

# 配置日志
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
logging.info("日志系统初始化完成，日志文件路径: %s", log_file)


def get_base_path():
    """获取程序运行的根目录，无论是开发环境还是 PyInstaller 打包环境"""
    return os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(
        os.path.abspath(__file__))


# **获取 base 目录**
BASE_DIR = get_base_path()

# **修正 config.ini 的路径**
CONFIG_DIR = os.path.join(BASE_DIR, "config")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.ini")

# **确保 config 目录存在**
os.makedirs(CONFIG_DIR, exist_ok=True)

# **加载配置文件**
config = configparser.ConfigParser()
if os.path.exists(CONFIG_PATH):
    config.read(CONFIG_PATH, encoding="utf-8")
else:
    logging.error(f"❌ 配置文件未找到: {CONFIG_PATH}")
    raise FileNotFoundError(f"❌ 配置文件未找到: {CONFIG_PATH}")

# **加载配置文件**
config = configparser.ConfigParser()
if os.path.exists(CONFIG_PATH):
    config.read(CONFIG_PATH, encoding="utf-8")
else:
    logging.error(f"❌ 配置文件未找到: {CONFIG_PATH}")
    raise FileNotFoundError(f"❌ 配置文件未找到: {CONFIG_PATH}")

# 解析输入、输出目录，并修正路径
INPUT_DIR = os.path.join(BASE_DIR, config.get("Paths", "input_dir"))
OUTPUT_DIR = os.path.join(BASE_DIR, config.get("Paths", "output_dir"))
OVERWRITE = config.getboolean("Paths", "overwrite")

# **确保路径存在**
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.info(f"✅ 配置文件路径: {CONFIG_PATH}")
logging.info(f"✅ 输入目录: {INPUT_DIR}")
logging.info(f"✅ 输出目录: {OUTPUT_DIR}")

# 解析马赛克区域
X, Y = config.getint("Region", "x"), config.getint("Region", "y")
W, H = config.getint("Region", "width"), config.getint("Region", "height")

# 解析处理参数
BLUR_KERNEL = config.getint("Processing", "blur_kernel")
BLUR_SIGMA = config.getint("Processing", "blur_sigma")
REMOVE_AUDIO = config.getboolean("Processing", "remove_audio")

# 解析支持格式
SUPPORTED_FORMATS = tuple(config.get("Formats", "supported").replace(" ", "").split(","))


def get_ffmpeg_path():
    """根据操作系统自动选择 FFmpeg 路径，并确保 FFmpeg 存在"""
    # 1️⃣ 适配 PyInstaller 运行环境
    if getattr(sys, 'frozen', False):
        base_dir = os.path.join(os.path.dirname(sys.executable), "ffmpeg")
    else:
        # 2️⃣ 开发环境，获取 main_mac.py 所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(script_dir, "ffmpeg")

        # 3️⃣ 兼容 `main_mac.py` 在 `project_root/ffmpeg/` 的情况
        if not os.path.exists(base_dir):
            base_dir = os.path.join(script_dir, "..", "ffmpeg")

    # 4️⃣ 选择 FFmpeg 路径
    system = platform.system()

    if system == "Windows":
        ffmpeg_path = os.path.join(base_dir, "win", "ffmpeg.exe")
    elif system == "Darwin":  # macOS
        ffmpeg_path = os.path.join(base_dir, "mac", "ffmpeg")
    elif system == "Linux":
        ffmpeg_path = os.path.join(base_dir, "linux", "ffmpeg")
    else:
        logging.error(f"❌ 不支持的操作系统: {system}")
        raise RuntimeError(f"❌ 不支持的操作系统: {system}")

    # 确保动态库路径正确
    if system == "Darwin":
        ffmpeg_lib_path = os.path.join(base_dir, "mac")  # FFmpeg 相关动态库目录
        os.environ["DYLD_LIBRARY_PATH"] = f"{ffmpeg_lib_path}:{os.environ.get('DYLD_LIBRARY_PATH', '')}"

    # 确保 FFmpeg 可执行文件存在
    if not os.path.isfile(ffmpeg_path):
        logging.error(f"❌ FFmpeg 未找到: {ffmpeg_path}\n请确保 FFmpeg 已安装或放置在正确目录中。")
        raise FileNotFoundError(f"❌ FFmpeg 未找到: {ffmpeg_path}\n请确保 FFmpeg 已安装或放置在正确目录中。")

    # 确保 FFmpeg 可执行
    if not os.access(ffmpeg_path, os.X_OK):
        logging.info(f"⚠️ {ffmpeg_path} 可能不可执行，尝试自动修复权限...")
        try:
            os.chmod(ffmpeg_path, 0o755)  # 赋予执行权限
        except PermissionError:
            logging.error(f"❌ 无法修改 {ffmpeg_path} 的执行权限，请手动修复")
            raise PermissionError(f"❌ 无法修改 {ffmpeg_path} 的执行权限，请手动修复")

    return ffmpeg_path


# 获取 FFmpeg 路径
FFMPEG_PATH = get_ffmpeg_path()
logging.info(f"✅ 使用 FFmpeg: {FFMPEG_PATH}")

# **强制指定 FFmpeg 给 imageio**
os.environ["IMAGEIO_FFMPEG_EXE"] = FFMPEG_PATH
logging.info(f"📌 设置环境变量 IMAGEIO_FFMPEG_EXE = {FFMPEG_PATH}")


def add_mosaic_and_compress(input_video, output_video, fast_mode=True):
    """
    使用 FFmpeg 给指定区域添加马赛克，并对视频进行最大程度的压缩。
    """
    logging.info(f"开始处理视频: {input_video}")
    codec = "libx264" if fast_mode else "libx265"
    preset = "ultrafast" if fast_mode else "fast"
    crf = "30" if fast_mode else "28"

    audio_option = [] if REMOVE_AUDIO else ["-c:a", "aac", "-b:a", "64k"]
    map_audio = [] if REMOVE_AUDIO else ["-map", "0:a?"]

    command = [
        FFMPEG_PATH,
        "-loglevel", "error",  # 只记录错误
        "-i", input_video,
        "-filter_complex",
        f"[0:v]crop={W}:{H}:{X}:{Y},boxblur={BLUR_KERNEL}:{BLUR_SIGMA}[blurred];[0:v][blurred]overlay={X}:{Y}[out]",
        "-map", "[out]",
        *map_audio,
        "-c:v", codec,
        "-preset", preset,
        "-crf", str(crf),
        *audio_option,
        "-threads", "4",
        "-y", output_video
    ]

    try:
        subprocess.run(command, check=True)
        logging.info(f"✅ 处理完成: {output_video}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ 处理失败: {input_video}, 错误: {e}")


def process_all_videos():
    """ 批量处理 input 目录下的所有支持格式的视频 """
    logging.info("开始批量处理视频...")
    video_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(SUPPORTED_FORMATS)]

    if not video_files:
        logging.warning("⚠️ 没有找到支持的视频文件。")
        return

    logging.info(f"🔄 发现 {len(video_files)} 个视频，开始处理...")

    for filename in video_files:
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        if not OVERWRITE and os.path.exists(output_path):
            logging.info(f"⚠️ 跳过已存在的视频: {filename}")
            continue

        logging.info(f"🎬 处理视频: {filename} -> {output_path}")
        add_mosaic_and_compress(input_path, output_path)

    logging.info("🎉 所有视频处理完成！")


if __name__ == '__main__':
    process_all_videos()
