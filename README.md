### 操作指南

    设置执行权限（Mac需要）
    chmod 755 ffmpeg/ffmpeg

    运行测试
    python main.py

[video_tool.log](..%2F..%2FDesktop%2Fffmpeg%2Fvideo_tool%2Flogs%2Fvideo_tool.log) Windows打包命令:
~~~shell
    pyinstaller --onefile --windowed --add-data="config;config" --add-data="ffmpeg;ffmpeg" --name=main_win .\main.py
~~~
Mac打包命令(产生的main_mac.app可以删除，不需要):
~~~shell
    pyinstaller --onefile --windowed --add-data="config:config/" --add-data="ffmpeg:ffmpeg/" --hidden-import=configparser --name=main_mac main.py
~~~

#### 4.常见问题处理
###### Q1: 出现 Permission denied 错误
~~~shell
    # Mac/Linux
    chmod 755 ffmpeg/ffmpeg
~~~

    # Windows
    右键exe文件 → 属性 → 解除锁定

###### Q2: Mac 上安装 Homebrew（brew）和 ffmpeg
~~~shell
    /bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
~~~
    
~~~shell
    # M1/M2 (Apple Silicon) 用户
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
    eval "$(/opt/homebrew/bin/brew shellenv)"
~~~

~~~shell
    # Intel 用户：
    echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc
    eval "$(/usr/local/bin/brew shellenv)"
~~~

~~~shell
    brew uninstall ffmpeg
    brew install ffmpeg
    brew --version
~~~

###### Q3: 在Mac中执行，如果出现ffmpeg隐私问题，解决办法：

    检查ffmpeg是否还在video_tool/ffmpeg/mac/ffmpeg下，没有就再复制一个ffmpeg进去。
    
    进入“系统设置”->"隐私安全"->在“安全性”下的“允许一下来源的应用程序”中选择“App Store与已知开发者”->然后再次执行；
    
    再次执行会在 “系统设置”->"隐私安全"->在“安全性”下的“允许一下来源的应用程序”中选择“App Store与已知开发者”的下面，有一个“仍然打开ffmpeg”->点击"允许仍然打开",此时等待终端窗口一会，执行日志会在终端窗口中展示;
    
    如果还不行，就重复上面的步骤。

### 目录结构
    your_project/
        .
        ├── README.md
        ├── config
        │   └── config.ini
        ├── ffmpeg
        │    ├── mac
        │    │   └── ffmpeg(进入该目录设置权限，终端执行：chmod +x ffmpeg)
        │    └── win
        │        └── ffmpeg.exe
        ├── input
        │   ├── 1.mp4
        │   ├── 2.mp4
        │   └── 放置要处理的视频文件
        ├── logs
        │   └── video_tool.log
        ├── main.py
        └─main_win.exe （Windows系统主程序，点击执行）
        └─main_mac （Mac系统主程序，点击执行）
        └── output
            └── 输出处理后的视频文件