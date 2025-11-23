# BookSim2 在 MSYS2 UCRT64 编译记录

本文记录我在 MSYS2 UCRT64 环境下成功编译 BookSim2 的完整过程、关键问题与修复点，便于复现与排查。

## 结果
- 可执行文件：`booksim2/src/booksim.exe`
- 编译环境：MSYS2 UCRT64（`/ucrt64/bin/g++ (Rev8) 15.2.0`，`flex`，`bison`）

## 关键问题与修复
1) 依赖缺失：`nlohmann/json.hpp`
- 现象：`injection.cpp`/`traffic.cpp`/`trafficmanager.cpp` 报 `fatal error: nlohmann/json.hpp: No such file or directory`
- 解决：安装 UCRT64 版本的头文件库
  - 命令：`pacman -Sy --noconfirm mingw-w64-ucrt-x86_64-nlohmann-json`

2) 工具链混用导致链接不稳定
- 现象：最初环境混入了非 MSYS2 的 `g++`（如 Strawberry 工具链），出现 `undefined reference` 等异常
- 解决：强制使用 UCRT64 工具链并固定 PATH
  - 变量：`MSYSTEM=UCRT64`，`PATH=/ucrt64/bin:/usr/bin:$PATH`
  - 构建参数：`CC=/ucrt64/bin/gcc CXX=/ucrt64/bin/g++`

3) bison/flex 生成物按 C 编译但包含 C++ 内容
- 现象：`y.tab.c` 包含 `<cstdlib>` 等 C++ 头，用 C 编译器会报错；同时与 C++ 侧符号链接名不匹配导致链接失败
- 修复：将 lex/yacc 生成物用 C++ 编译器编译，并统一 C 语言链接名
  - 修改 `booksim2/src/Makefile`
    - `$(LEX_OBJS)` 规则：改为 `$(CXX) $(CPPFLAGS) -x c++ -c $< -o $@`
    - `$(YACC_OBJS)` 规则：改为 `$(CXX) $(CPPFLAGS) -x c++ -c $< -o $@`
  - 修改 `booksim2/src/config.l`
    - 为 `config_error`/`config_input`/`yyerror` 增加 `extern "C"` 原型声明，确保与 bison 调用约定一致
    - `config_error` 原型使用 `const char*`（与头文件一致）
  - 修改 `booksim2/src/config_utils.cpp`
    - `extern "C" void config_error(const char* msg, int lineno)`：与声明一致，供 lex 调用

## 复现步骤
以下命令在 PowerShell 中调用 MSYS2 Bash（UCRT64 环境）执行：

```powershell
& 'C:\msys64\usr\bin\bash.exe' -lc "^
  set -e; ^
  export MSYSTEM=UCRT64; ^
  export PATH=/ucrt64/bin:/usr/bin:$PATH; ^
  pacman -Sy --noconfirm mingw-w64-ucrt-x86_64-nlohmann-json; ^
  cd /d/python_prj/rapidchiplet/rapidchiplet/booksim2/src; ^
  make clean; ^
  make -j$(nproc) V=1 CC=/ucrt64/bin/gcc CXX=/ucrt64/bin/g++
"
```

完成后，产物位于：`booksim2/src/booksim.exe`。

## 验证
- 查看产物：`ls -la booksim2/src/booksim*`
- 运行帮助（如有）：`./booksim.exe` 或搭配示例配置运行。

## 变更文件一览（已提交到工作区）
- `booksim2/src/Makefile`
  - 将 `lex.yy.c` 与 `y.tab.c` 的编译规则统一为使用 C++ 编译器并显式 `-x c++`
- `booksim2/src/config.l`
  - 为 `config_error`/`config_input`/`yyerror` 增加 `extern "C"` 声明；`config_error` 原型使用 `const char*`
- `booksim2/src/config_utils.cpp`
  - 定义 `extern "C" void config_error(const char* msg, int lineno)`，与头文件/lex 一致

## 备注
- 若希望通过 vcpkg 获取 `nlohmann-json`，也可采用 vcpkg 方案，但在 MSYS2 UCRT64 下直接 pacman 安装更简洁。

