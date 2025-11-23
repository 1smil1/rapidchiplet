# generate_inputs.py 文件总结

## 功能概述
`generate_inputs.py` 是 RapidChiplet 框架的核心输入文件生成器，能够根据一组参数自动生成大部分所需的输入文件，大大简化了设计配置过程。

## 主要功能

### 自动文件生成
**自动生成的文件**：
- `chiplets`: 芯片配置文件
- `design`: 主设计文件
- `placement`: 布局配置文件
- `routing_table`: 路由表文件
- `topology`: 拓扑配置文件
- `traffic_by_unit`: 按单元的流量配置
- `traffic_by_chiplet`: 按芯片的流量配置

**基于现有文件修改的文件**：
- `booksim_config`: BookSim配置文件

**需要手动编写的文件**：
- `technologies`: 工艺技术文件
- `packaging`: 封装配置文件

### 核心生成函数
- **`generate_inputs()`**: 主要的输入生成函数
- 接受参数集合和设计名称
- 可选择是否写入文件（`do_write`参数）

### 拓扑到布局的映射
- 自动将拓扑类型映射到对应的布局类型
- 支持的拓扑-布局映射关系
- 自动选择合适的PHY布局配置

### 规模参数处理
支持不同的规模参数格式：
- **网格布局**: `<rows>x<cols>` 格式（如 "4x4"）
- **六边形布局**: `<radius>` 格式（如 "3"）

### PHY布局自适应
- 根据拓扑类型自动调整PHY布局
- 特殊处理某些拓扑（如flattened_butterfly）的PHY配置
- 支持动态PHY数量计算

## 集成的生成模块
调用多个专门的生成模块：
- `generate_chiplet`: 芯片配置生成
- `generate_placement`: 布局生成
- `generate_topology`: 拓扑生成
- `generate_routing`: 路由表生成
- `generate_traffic`: 流量模式生成
- `inputs.trace_to_traffic`: 轨迹转换

## 输入参数
主要参数包括：
- `use_memory`: 是否使用内存芯片
- `topology`: 网络拓扑类型
- `grid_scale`/`hex_scale`: 网格规模
- 各种芯片和系统参数

## 输出组织
- 生成的文件按照标准目录结构组织
- 文件命名基于设计名称
- 保持与现有文件格式的一致性

## 使用场景
- 批量设计生成
- 设计空间探索
- 标准化配置创建
- 自动化测试和验证

## 特点
- 高度自动化，减少手动配置工作
- 灵活的参数系统
- 模块化设计，易于扩展
- 完整的文件生成流程