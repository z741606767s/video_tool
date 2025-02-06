1.设置配置
    [Paths]
    # 输入视频目录
    input_dir = ./input
    # 输出目录
    output_dir = ./output
    # 是否覆盖已有文件,用小写 ✅
    overwrite = false

    [Region]
    # （重点）马赛克位置左上角X坐标
    x = 0
    # （重点）马赛克位置左上角Y坐标
    y = 0
    # （重点）马赛克区域宽度
    width = 400
    # （重点）马赛克区域高度
    height = 80

    [Processing]
    # 模糊处理参数
    # （重点，设置模糊度）kernel必须为奇数，sigma为高斯标准差（0表示自动计算）
    blur_kernel = 35
    blur_sigma = 35
    # 是否移除音频
    remove_audio = false

    [Formats]
    # 支持的视频类型
    supported = .mp4, .avi, .mov, .mkv, .flv, .webm, .ts

2.放置要处理的视频
   在input文件夹中放置要处理的视频文件。
   默认支持的视频类型：.mp4, .avi, .mov, .mkv, .flv, .webm, .ts

3.点击main.exe执行主程序
   点击执行后会产生video_tool.log日志文件，记录详细执行过程信息。
   中间会有多次弹出终端面板，请勿关闭，程序执行结束后会自动关闭。

4.处理过后的视频会输出到output文件夹下

5.在Mac中执行，如果出现ffmpeg隐私问题，解决办法：
  检查ffmpeg是否还在video_tool/ffmpeg/mac/ffmpeg下，没有就再复制一个ffmpeg进去。
  进入“系统设置”->"隐私安全"->在“安全性”下的“允许一下来源的应用程序”中选择“App Store与已知开发者”->然后再次执行；
  再次执行会在 “系统设置”->"隐私安全"->在“安全性”下的“允许一下来源的应用程序”中选择“App Store与已知开发者”的下面，有一个“仍然打开ffmpeg”->点击"允许仍然打开",此时等待终端窗口一会，执行日志会在终端窗口中展示;
  如果还不行，就重复上面的步骤。
   
6.检查目录结构是否一致：
    根目录
    ├─config
    │  └─settings.ini（配置文件）
    ├─ffmpeg
    │  ├─mac
    │  │	├─ffmpeg (进入该目录设置权限，终端执行：chmod +x ffmpeg)
    │  │	└─ffprobe (进入该目录设置权限，终端执行：chmod +x ffprobe)
    │  └─win
    │	├─ffmpeg.exe
    │	├─ffplay.exe
    │	└─ffprobe.exe
    ├─input
    │  └─（需要处理的视频文件）
    └─output
    │  └─（输出处理过后的视频文件）
    └─main_win.exe （Windows系统主程序，点击执行）
    └─main_mac （Mac系统主程序，点击执行）
    └─video_tool.log （执行日志，程序执行时会自动生成）
    └─openh264-1.8.0-win64.dll （可选，部分Windows系统，在执行时报错或被处理视频文件与处理后视频结果文件大小相差太大时，把该文件复制到C:\Windows\System32文件夹下面）
