# booksim_wrapper.py 文件总结

## 功能概述
`booksim_wrapper.py` 是 RapidChiplet 框架与 BookSim2 周期精确仿真器之间的接口模块。它负责将 RapidChiplet 的设计配置转换为 BookSim2 可以理解的格式，并管理仿真过程。

## 主要功能

### 1. BookSim 配置文件导出
- **`export_booksim_config()`**: 将 RapidChiplet 的设计参数转换为 BookSim2 配置文件
- 处理路由器延迟计算（自动计算平均延迟或使用手动指定值）
- 配置网络拓扑、路由表、流量模式等参数

### 2. 拓扑文件导出
- **`export_topology()`**: 将 RapidChiplet 的网络拓扑转换为 BookSim2 的 anynet 格式
- 支持多种拓扑类型：mesh、torus、tree 等
- 处理芯片间和芯片内部网络连接

### 3. 路由表导出
- **`export_routing_table()`**: 将路由表转换为 BookSim2 可用的 JSON 格式
- 支持不同路由算法（SPLIF、SPTMR）
- 处理路由表的数据编码转换

### 4. 流量模式导出
- **`export_traffic()`**: 导出合成流量模式到 BookSim2
- **`export_trace()`**: 导出真实网络轨迹到 BookSim2
- 支持多种流量模式：随机均匀、转置、置换、热点等

### 5. 仿真执行和管理
- **`run_booksim()`**: 执行 BookSim2 仿真
- **`run_booksim_sweep()`**: 执行多个负载点的批量仿真
- 处理仿真结果收集和错误处理

## 技术特点

### 参数映射
- 自动计算 BookSim2 所需的时序参数
- 处理 RapidChiplet 和 BookSim2 之间的单位转换
- 提供参数不一致时的警告信息

### 文件管理
- 自动生成 BookSim2 所需的所有配置文件
- 使用运行标识符管理多个仿真
- 在 `booksim2/src/rc_*` 目录下创建专用文件

### 仿真控制
- 支持注入率扫描以获得性能曲线
- 处理不同仿真模式（合成流量 vs 真实轨迹）
- 提供仿真超时和错误处理

## 使用场景
- 需要周期精确性能分析时
- 验证 RapidChiplet 快速分析结果的准确性
- 研究不同网络配置下的详细性能特征
- 生成学术论文中的性能对比数据

## 依赖关系
- **依赖**: `helpers.py`（工具函数）
- **外部依赖**: BookSim2 可执行文件
- **输入**: RapidChiplet 设计配置文件
- **输出**: BookSim2 仿真结果