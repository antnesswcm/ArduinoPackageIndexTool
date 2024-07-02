## Arduino Package Index Tool

### 简介
该工具用于从外部JSON文件读取Arduino包索引URL，用户可以选择预定义的URL或输入自定义URL来获取所需的JSON数据，并从中选择版本和host类型，最后获取相应的下载链接。工具还会在程序结束前打印一些关于Arduino默认存放路径的提示信息。
该工具不能帮你解决网络环境导致的下载问题，仅仅帮你将开发板管理JSON内容中的下载链接快速罗列出来。
最后，你应该手动下载并放到指定目录中，然后在arduinoIDE中安装开发板。

### 特性
- 从外部文件读取URL列表
- 用户选择预定义URL或输入自定义URL
- 显示可用版本信息并让用户选择
- 显示可用host类型并让用户选择
- 获取并打印选择版本和host类型的下载链接
- 打印Arduino默认存放路径提示信息

### 依赖
- `requests`: 用于发送HTTP请求
- `json`: 用于解析JSON数据
- `os`: 用于获取环境变量和操作系统路径

### 安装
1. 克隆或下载该仓库。
2. 确保Python环境中安装了`requests`库。可以使用以下命令安装：
    ```bash
    pip install requests
    ```
3. 在项目目录中创建并编辑`packageIndexUrl.json`文件，内容示例如下：
    ```json
    {
        "esp8266": "http://arduino.esp8266.com/stable/package_esp8266com_index.json",
        "stm32": "https://dl.espressif.com/dl/package_esp32_index.json",
        "STM32": "https://dan.drown.org/stm32duino/package_STM32duino_index.json",
        "m5stack": "https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/arduino/package_m5stack_index.json"
    }
    ```

### 使用方法
1. 运行主程序：
    ```bash
    python main.py
    ```
2. 按照提示选择预定义URL或输入自定义URL。
3. 选择版本和host类型，程序将会输出相应的下载链接。
4. 程序结束前会打印Arduino默认存放路径的提示信息。

### 目录结构
```plaintext
ArduinoPackageIndexTool/
│
├── packageIndexUrl.json
├── main.py
└── README.md
```

### 示例输出
```
可用的URL列表:
    1. esp8266: http://arduino.esp8266.com/stable/package_esp8266com_index.json
    2. stm32: https://dl.espressif.com/dl/package_esp32_index.json
    3. STM32: https://dan.drown.org/stm32duino/package_STM32duino_index.json
    4. m5stack: https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/arduino/package_m5stack_index.json
    5. 输入自定义URL
请选择URL (默认: 1): 

可用版本:
1.  3.0.0         4.  2.7.4         7.  2.6.2         
2.  2.9.1         5.  2.7.2         8.  2.6.1         
3.  2.8.0         6.  2.6.3         9.  2.6.0         
10. 2.5.2        
请选择版本 (默认: 3.0.0): 

可用 host 类型:
    1. x86_64-mingw32
    2. x86_64-pc-linux-gnu
    3. i686-mingw32
请选择 host 类型(1-3): 

版本 3.0.0 的 x86_64-mingw32 依赖如下:
============================================================
esp8266
xtensa-lx106-elf-gcc
...
============================================================
https://github.com/esp8266/Arduino/releases/download/....
https://github.com/earlephilhower/esp-quick-toolchain/releases/download/....
...
============================================================

=====================
Tips: 下面是Arduino默认的存放路径
C:\Users\xxxx\AppData\Local\Arduino15\
C:\Users\xxxx\AppData\Local\Arduino15\staging\packages
=====================
```

### 许可证
该项目遵循MIT许可证。详情请参阅LICENSE文件。
