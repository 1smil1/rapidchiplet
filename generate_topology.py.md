# generate_topology.py 文件总结

## 功能概述
`generate_topology.py` 是网络拓扑生成模块，支持多种标准网络拓扑结构，为芯片间互连网络提供不同的连接配置。

## 主要功能

### 支持的拓扑类型

#### 1. Mesh拓扑
- **函数**: `generate_mesh_topology()`
- **适用布局**: 仅适用于网格布局
- **特点**: 2D网格连接，边界节点连接数较少
- **PHY映射**: 使用标准4个PHY（东、南、西、北）

#### 2. Torus拓扑
- **函数**: `generate_torus_topology()`
- **适用布局**: 仅适用于网格布局
- **特点**: 环形连接，所有节点连接数相同
- **优势**: 更好的网络容错性和负载均衡

#### 3. Flattened Butterfly拓扑
- **函数**: `generate_flattened_butterfly_topology()`
- **适用布局**: 网格布局
- **特点**: 高连通性，长距离直接连接
- **复杂度**: 需要更多PHY资源

#### 4. Tree拓扑
- **函数**: `generate_tree_topology()`
- **适用布局**: 多种布局
- **特点**: 分层结构，根节点易成为瓶颈

#### 5. Hexagonal Mesh拓扑
- **函数**: `generate_hexagonal_mesh_topology()`
- **适用布局**: 六边形布局
- **特点**: 六边形网格，更自然的连接模式

### 拓扑生成算法

#### Mesh/Torus算法
- 基于行优先的芯片ID编号
- 水平连接：使用PHY 0和2
- 垂直连接：使用PHY 1和3
- 支持边界回环（Torus）或边界截断（Mesh）

#### 复杂拓扑处理
- 自适应PHY数量计算
- 动态连接配置
- 跨行/跨列的长距离连接

### 拓扑映射表
定义了拓扑与相关配置的映射关系：
```python
topology_to_placement = {
    "mesh": "grid",
    "torus": "grid",
    "flattened_butterfly": "grid",
    "tree": "tree",
    "hexagonal_mesh": "hexagonal"
}

topology_to_phy_placement = {
    "mesh": "4PHY_Edge",
    "torus": "4PHY_Edge",
    "flattened_butterfly": "xPHY_yPHY",  # 动态计算
    "tree": "4PHY_Edge",
    "hexagonal_mesh": "6PHY_HM"
}
```

### 链路配置
每个链路包含：
- `ep1`, `ep2`: 两个端点配置
- `color`: 可视化颜色
- 端点类型：chiplet 或 interposer_router
- 芯片内部PHY ID映射

### 命令行接口
```bash
python3 generate_topology.py -df <design_file> -tf <topology_file> -t <topology_type>
```

## 输入参数
- **通用参数**: 行数、列数、半径等
- **拓扑特定参数**: 不同拓扑的特殊要求
- **PHY配置**: 自动或手动PHY数量配置

## 输出格式
生成的拓扑文件包含：
- 链路列表及其端点配置
- 可视化颜色信息
- PHY连接映射

## 使用场景
- 不同网络性能比较
- 拓扑设计空间探索
- 应用需求匹配
- 成本性能权衡分析

## 技术特点
- 支持多种标准拓扑
- 自动PHY配置
- 灵活的布局适配
- 标准化的输出格式
- 可视化支持

## 依赖关系
- **内部模块**: `global_config.py`
- **布局系统**: 与 `generate_placement.py` 紧密集成