
## 菲姐点名器


--------------

### 介绍
这是一款使用Python实现的简易班级点名程序。

#### GUI
GUI文件是由Parth Jadhav的Tkinter Designer生成的。

> 仓库: [https://github.com/ParthJadhav/Tkinter-Designer](https://github.com/ParthJadhav/Tkinter-Designer)
##### 示例
![示例图片](https://raw.githubusercontent.com/b84955189/lottery_game/master/doc/img/example.png)
#### 第三方模块
##### openpyxl
一个关于读写Excel文件的Python库。

>  文档：[https://openpyxl.readthedocs.io/](https://openpyxl.readthedocs.io/)


### 打包
#### EXE打包
本项目的EXE可执行文件使用[PyInstaller](https://pyinstaller.org)第三方库进行打包。本项目路径中提供了 示例打包配置文件。您可以通过将其放在自己的项目根目录来使用和打包程序。

**pack-config-template.spec**
```
···
···
···
a = Analysis(['main.py',
'func\\CommonTools.py',
'func\\ExcelFunc.py',
'gui\\gui.py',
'venv\\Lib\\site-packages\\openpyxl\\__init__.py'
],
···
···
···

exe = EXE(pyz,
···
···
···
          name='菲姐点名器v1.0',
          debug=False,
          icon='./assets/icon128.ico',
          bootloader_ignore_signals=False,
···
···
···
```
**执行打包**
```
pyinstaller -w pack-config-template.spec
```
#### 安装包打包
本项目的EXE可执行文件使用[Inno Setup Compiler](https://jrsoftware.org/isinfo.php)工具进行打包。打包脚本文件已提交至本仓库。
### 联系
 - **作者**： Jason   
 - **邮箱**： lking@lking.icu
 - **博客**： [www.lking.icu](https://www.lking.icu)
 - **CSDN**： [https://blog.csdn.net/weixin_43670802](https://blog.csdn.net/weixin_43670802)
