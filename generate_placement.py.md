# generate_placement.py 文件总结

## 功能概述
`generate_placement.py` 是专门用于生成芯片布局配置的模块，支持多种标准布局模式，确保芯片在封装上的正确定位。

## 主要功能

### 支持的布局模式

#### 1. 网格布局（Grid Placement）
- **函数**: `generate_grid_placement()`
- **参数**:
  - `rows`: 行数
  - `cols`: 列数
  - `chiplet_spacing`: 芯片间距
- **布局特点**: 规则的矩形网格排列

#### 2. 六边形布局（Hexagonal Placement）
- **函数**: `generate_hexagonal_placement()`
- **参数**:
  - `radius`: 六边形网格半径
  - `chiplet_spacing`: 芯片间距
- **布局特点**: 六边形紧密排列，提高空间利用率

### 布局生成算法

#### 网格布局算法
- 计算每个芯片的X、Y坐标
- X坐标：`col * (芯片宽度 + 间距)`
- Y坐标：`row * (芯片高度 + 间距)`
- 支持边界芯片的特殊配置（如内存芯片）

#### 六边形布局算法
- 基于HexaMesh论文的六边形排列方法
- 计算每行的芯片数量和起始位置
- 行间偏移计算以实现六边形排列
- 支持可变半径的六边形网格

### 内存支持
- 自动检测是否使用内存芯片（`use_memory`参数）
- 边界芯片可配置为内存芯片
- 中心芯片保持为计算芯片
- 内存芯片命名：`<chiplet_name>_memory`

### 输出格式
生成的布局配置包含：
```json
{
  "chiplets": [
    {
      "position": {"x": x, "y": y},
      "rotation": 0,
      "name": "chiplet_name"
    }
  ],
  "interposer_routers": []
}
```

## 布局注册系统
- 使用字典 `placement_generation_functions` 管理布局函数
- 支持动态添加新的布局类型
- 标准化的函数接口

## 输入参数
通用参数：
- `chiplet`: 芯片配置对象
- `chiplet_name`: 芯片名称
- `use_memory`: 是否使用内存芯片

特定布局参数：
- 网格布局：`rows`, `cols`, `chiplet_spacing`
- 六边形布局：`radius`, `chiplet_spacing`

## 使用场景
- 标准化芯片布局生成
- 不同拓扑结构的布局配置
- 大规模芯片阵列设计
- 封装空间优化

## 特点
- 支持多种标准布局模式
- 自动化的坐标计算
- 灵活的内存芯片配置
- 易于扩展新的布局算法
- 标准化的输出格式