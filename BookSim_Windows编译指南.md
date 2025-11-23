# BookSim Windows 编译指南

## 🎯 问题分析

当前编译错误：
```
injection.cpp:37:10: fatal error: nlohmann/json.hpp: No such file or directory
```

**根本原因**: BookSim需要nlohmann/json库，但Windows环境下默认没有安装。

## 🔧 解决方案

### 方案一：使用vcpkg（推荐）

#### 步骤1: 安装vcpkg
```bash
# 克隆vcpkg到某个目录（比如D:\vcpkg）
git clone https://github.com/Microsoft/vcpkg.git D:\vcpkg
cd D:\vcpkg

# 运行bootstrap脚本
.\bootstrap-vcpkg.bat

# 将vcpkg添加到系统环境变量
.\vcpkg integrate install
```

#### 步骤2: 安装nlohmann/json
```bash
# 在vcpkg目录下
.\vcpkg install nlohmann-json
```

#### 步骤3: 修改BookSim的Makefile
创建Windows友好的Makefile：

```makefile
# BookSim Windows Makefile
CC = g++
CXX = g++

# 基本编译选项
CPPFLAGS = -Wall -I. -Iarbiters -Iallocators -Irouters -Inetworks -Ipower
CPPFLAGS += -O3 -g -std=c++11

# 添加vcpkg的include路径
VCPKG_INCLUDE = -I"D:\vcpkg\installed\x64-windows\include"
CPPFLAGS += $(VCPKG_INCLUDE)

# 源文件
CPP_SRCS = $(wildcard *.cpp) $(wildcard */*.cpp)
CPP_OBJS = $(CPP_SRCS:.cpp=.o)

# 目标程序
PROG = booksim.exe

# 默认目标
all: $(PROG)

# 编译规则
%.o: %.cpp
	$(CXX) $(CPPFLAGS) -c $< -o $@

# 链接目标
$(PROG): $(OBJS)
	$(CXX) $(OBJS) -o $(PROG)

# 清理
clean:
	del /Q *.o */*.o $(PROG)

.PHONY: all clean
```

#### 步骤4: 编译
```bash
cd booksim2/src
# 使用上面的Makefile（保存为Makefile.windows）
make -f Makefile.windows
```

### 方案二：手动下载nlohmann/json

#### 步骤1: 下载nlohmann/json
```bash
# 创建include目录
mkdir -p booksim2/src/include

# 下载nlohmann/json单头文件版本
curl -o booksim2/src/include/json.hpp https://raw.githubusercontent.com/nlohmann/json/develop/single_include/nlohmann/json.hpp
```

或者直接从GitHub下载：
1. 访问 https://github.com/nlohmann/json
2. 下载单头文件版本
3. 将 `json.hpp` 放到 `booksim2/src/include/` 目录

#### 步骤2: 修改Makefile
```makefile
# 在现有Makefile的CPPFLAGS中添加
CPPFLAGS += -I./include
```

#### 步骤3: 编译
```bash
cd booksim2/src
make
```

### 方案三：使用Visual Studio

#### 步骤1: 安装Visual Studio
确保安装了"C++桌面开发"工作负载。

#### 步骤2: 创建项目
1. 打开Visual Studio
2. 创建"空项目"
3. 将booksim2/src目录下所有.cpp和.hpp文件添加到项目中

#### 步骤3: 配置项目属性
```
配置属性 -> C/C++ -> 常规 -> 附加包含目录:
添加: $(ProjectDir)include
```

#### 步骤4: 添加nlohmann/json
将json.hpp文件添加到项目的include目录中。

#### 步骤5: 编译
右键项目 -> 生成

### 方案四：使用Chocolatey

#### 步骤1: 安装Chocolatey
```powershell
# 以管理员身份运行PowerShell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

#### 步骤2: 安装依赖
```bash
choco install nlohmann-json
choco install make
```

#### 步骤3: 编译
```bash
cd booksim2/src
make
```

## 🚀 快速解决方案（推荐新手）

如果你想要最简单的方法，我推荐**方案二**：

```bash
# 1. 下载单头文件版本
curl -o booksim2/src/json.hpp https://raw.githubusercontent.com/nlohmann/json/develop/single_include/nlohmann/json.hpp

# 2. 简单修改编译（在booksim2/src目录下）
sed -i 's|#include <nlohmann/json.hpp>|#include "json.hpp"|' injection.cpp

# 3. 编译
make
```

## 🔍 验证编译成功

编译成功后，你应该能看到：
```bash
booksim.exe  # 或 booksim（Linux格式）
```

然后在RapidChiplet中测试：
```bash
cd ../../
python rapidchiplet.py -df inputs/designs/design_example_experiment.json -rf test_with_booksim -bs
```

## 🛠️ 常见问题解决

### 问题1: Make命令不存在
**解决方案**: 安装MinGW或使用Chocolatey安装make
```bash
choco install make
```

### 问题2: g++编译器未找到
**解决方案**: 安装MinGW或Visual Studio
```bash
choco install mingw
```

### 问题3: 路径包含空格
**解决方案**: 使用引号包围路径或使用8.3格式路径

### 问题4: 权限问题
**解决方案**: 以管理员身份运行命令提示符

## 💡 推荐配置

对于你的使用场景，我推荐：

1. **快速开始**: 使用方案二（手动下载json.hpp）
2. **长期使用**: 使用方案一（vcpkg）
3. **Windows集成**: 使用方案三（Visual Studio）

选择任何一种方案都能成功编译BookSim，然后你就可以在RapidChiplet中使用精确的BookSim仿真了！

## 🎯 完成后的验证

编译成功后，运行这个命令验证：
```bash
cd booksim2/src
./booksim.exe  # 测试BookSim是否工作
cd ../../
python rapidchiplet.py -df inputs/designs/design_example_experiment.json -rf verification_test -bs
```

如果成功，你就能看到BookSim的详细仿真结果了！