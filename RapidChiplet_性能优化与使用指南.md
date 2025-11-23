# RapidChiplet 性能优化与使用指南

## 概述

RapidChiplet是一个用于设计和评估基于chiplet的系统的框架，专注于片上网络(NoC)性能分析。它结合了高级设计空间探索和使用BookSim2的周期精确仿真，并支持通过Netrace进行真实网络trace分析。

## RapidChiplet为什么"快速"？

### 1. 分析模型 vs 周期精确仿真

RapidChiplet使用数学分析模型而非逐个数据包的仿真：

- **延迟计算**（rapidchiplet.py:292-375）：基于路由表、链路距离和流量模式进行数学路径遍历
- **吞吐量计算**（rapidchiplet.py:377-458）：使用排队理论进行数学计算
- **功耗面积分析**：使用数学公式而非仿真测量

### 2. 多层缓存机制

- **输入文件缓存**（helpers.py:67-72）：避免重复文件I/O操作
- **中间结果缓存**（helpers.py:75-78）：缓存链路长度、延迟、带宽等计算结果
- **按需计算**：只计算需要的指标，避免不必要的计算

### 3. 简化的建模方法

- **恒定链路延迟模型**：使用可配置的延迟模型而非信号传播仿真
- **避免复杂的路由器微架构细节**：不建模VC分配、交换分配、缓冲区管理
- **降低仿真粒度**：操作周期级别而非数据包级别

### 4. 高效的图处理和路由

- **预计算路由表**：使用Dijkstra算法等预计算路由
- **批量处理**：将流量模式作为矩阵处理而非单个数据包
- **统计聚合**：同时计算所有流量流的平均值、最小值、最大值

### 5. 可配置的精度权衡

- **可选仿真**：BookSim仿真仅在明确要求时运行
- **分析精度**：用户可选择快速分析结果或较慢的周期精确仿真

## 核心区别对比

| 特性 | RapidChiplet | 传统BookSim2 |
|------|-------------|--------------|
| **分析方法** | 数学分析模型 | 周期精确仿真 |
| **计算粒度** | 周期级别 | 数据包级别 |
| **路由器建模** | 简化模型 | 详细微架构 |
| **缓存机制** | 多层缓存 | 基本缓存 |
| **设计空间探索** | 快速迭代 | 计算密集 |
| **使用场景** | 早期设计探索 | 详细验证 |

---

## RapidChiplet 输入系统详解

### 输入文件架构

RapidChiplet使用模块化输入系统，设计通过`inputs/`目录中的JSON文件指定：

```
inputs/
├── designs/          # 主设计文件，引用所有其他输入
├── chiplets/         # 单个chiplet规格（尺寸、功耗、PHY配置）
├── placements/       # chiplet和中介层路由器的物理布局
├── topologies/       # 网络连接定义
├── routing_tables/   # 不同算法的预计算路由表
├── technologies/     # 工艺技术参数
├── packagings/       # 封装和中介层规格
├── traffic_by_*/     # 流量模式（按chiplet或按unit）
├── traces/           # RapidChiplet格式的真实网络trace
└── booksim_configs/  # BookSim配置文件
```

### 1. 设计文件 (Design Files)

**文件位置**: `inputs/designs/`
**示例**: `design_example_experiment.json`

```json
{
    "design_name": "example_experiment",
    "technologies": "inputs/technologies/example_technologies.json",
    "chiplets": "inputs/chiplets/chiplets_example_experiment.json",
    "placement": "inputs/placements/placement_example_experiment.json",
    "topology": "inputs/topologies/topology_example_experiment.json",
    "packaging": "inputs/packagings/example_packaging.json",
    "routing_table": "inputs/routing_tables/routing_table_example_experiment.json",
    "traffic_by_unit": "inputs/traffic_by_unit/traffic_example_experiment.json",
    "traffic_by_chiplet": "inputs/traffic_by_chiplet/traffic_example_experiment.json",
    "trace": "none",
    "booksim_config": "inputs/booksim_configs/booksim_config_example_experiment.json"
}
```

**参数说明**：
- `design_name`: 设计名称标识符
- 其他字段：指向具体输入文件的路径
- `trace`: 可选，真实网络trace文件（"none"表示使用合成流量）

### 2. Chiplet规格文件 (Chiplet Specifications)

**文件位置**: `inputs/chiplets/`
**示例**: `chiplets_example_experiment.json`

```json
{
    "example_experiment": {
        "dimensions": {
            "x": 8.79772697916911,
            "y": 8.79772697916911
        },
        "type": "compute",
        "phys": [
            {
                "x": 0.6441986432926979,
                "y": 4.398863489584555,
                "fraction_bump_area": 0.25
            }
            // ... 更多PHY配置
        ],
        "fraction_power_bumps": 0.5,
        "technology": "tech_1",
        "power": 20.5,
        "relay": true,
        "internal_latency": 3,
        "unit_count": 8
    }
}
```

**参数说明**：
- `dimensions`: chiplet物理尺寸（mm）
- `type`: chiplet类型（compute/memory/io）
- `phys`: PHY（物理层）接口配置数组
  - `x`, `y`: PHY在chiplet上的相对位置
  - `fraction_bump_area`: PHY占用的凸点面积比例
- `fraction_power_bumps`: 用于电源的凸点比例
- `technology`: 使用的工艺技术
- `power`: 功耗（W）
- `relay`: 是否可作为中继节点
- `internal_latency`: 内部路由器延迟（周期）
- `unit_count`: 内部计算单元数量

### 3. 布局文件 (Placement Files)

**文件位置**: `inputs/placements/`
**示例**: `placement_example_experiment.json`

```json
{
    "chiplets": [
        {
            "position": {
                "x": 0.0,
                "y": 0.0
            },
            "rotation": 0,
            "name": "example_experiment"
        }
        // ... 更多chiplet布局
    ],
    "interposer_routers": []
}
```

**参数说明**：
- `chiplets`: chiplet布局数组
  - `position`: 在中介层上的绝对位置（mm）
  - `rotation`: 旋转角度（度）
  - `name`: 引用的chiplet规格名称
- `interposer_routers`: 中介层路由器布局（可选）

### 4. 拓扑文件 (Topology Files)

**文件位置**: `inputs/topologies/`
**示例**: `topology_example_experiment.json`

```json
[
    {
        "ep1": {
            "type": "chiplet",
            "outer_id": 0,
            "inner_id": 2
        },
        "ep2": {
            "type": "chiplet",
            "outer_id": 1,
            "inner_id": 0
        },
        "color": "#000099"
    }
    // ... 更多链路定义
]
```

**参数说明**：
- `ep1`, `ep2`: 链路的两个端点
  - `type`: 端点类型（chiplet/irouter）
  - `outer_id`: chiplet或路由器的ID
  - `inner_id`: PHY接口ID
- `color`: 可视化颜色（可选）

### 5. 工艺技术文件 (Technology Files)

**文件位置**: `inputs/technologies/`
**示例**: `example_technologies.json`

```json
{
    "tech_1": {
        "phy_latency": 12,
        "wafer_radius": 101.6,
        "wafer_cost": 500,
        "defect_density": 0.005
    },
    "tech_2": {
        "phy_latency": 12,
        "wafer_radius": 101.6,
        "wafer_cost": 750,
        "defect_density": 0.01
    }
}
```

**参数说明**：
- `phy_latency`: PHY延迟（周期）
- `wafer_radius`: 晶圆半径（mm）
- `wafer_cost`: 晶圆成本（美元）
- `defect_density`: 缺陷密度

### 6. 封装文件 (Packaging Files)

**文件位置**: `inputs/packagings/`
**示例**: `example_packaging.json`

```json
{
    "link_routing": "manhattan",
    "link_latency_type": "function",
    "link_latency": "lambda x : 0.25 * x",
    "link_power_type": "constant",
    "link_power": 1,
    "packaging_yield": 0.9,
    "bump_pitch": 0.05,
    "non_data_wires": 12,
    "is_active": true,
    "latency_irouter": 5,
    "power_irouter": 0.25,
    "has_interposer": true,
    "interposer_technology": "tech_3"
}
```

**参数说明**：
- `link_routing`: 链路布线类型（manhattan/euclidean）
- `link_latency_type`: 链路延迟类型（constant/function）
- `link_latency`: 延迟函数或常数
- `link_power_type`: 链路功耗类型（constant/function）
- `link_power`: 功耗函数或常数
- `packaging_yield`: 封装良率
- `bump_pitch`: 凸点间距（mm）
- `non_data_wires`: 非数据线数量
- `is_active`: 是否为有源中介层
- `latency_irouter`: 中介层路由器延迟
- `power_irouter`: 中介层路由器功耗
- `has_interposer`: 是否有中介层
- `interposer_technology`: 中介层工艺技术

### 7. 流量文件 (Traffic Files)

**文件位置**: `inputs/traffic_by_unit/` 或 `inputs/traffic_by_chiplet/`

**按单元的流量** (`traffic_by_unit/traffic_example_experiment.json`):
```json
{
    "__tuple__:[\"__tuple__:[0, 0]\", \"__tuple__:[1, 0]\"]": 0.008333333333333333,
    "__tuple__:[\"__tuple__:[0, 0]\", \"__tuple__:[1, 1]\"]": 0.008333333333333333
    // ... 更多流量矩阵条目
}
```

**按chiplet的流量** (`traffic_by_chiplet/traffic_example_experiment.json`):
```json
{
    "0": {
        "1": 0.06666666666666667,
        "2": 0.06666666666666667
        // ... 目标chiplet
    }
    // ... 源chiplet
}
```

### 8. 路由表文件 (Routing Table Files)

**文件位置**: `inputs/routing_tables/`
**示例**: `routing_table_example_experiment.json`

```json
{
    "type": "routing_table",
    "routes": {
        "chiplet_0": {
            "chiplet_1": [
                ["chiplet_0", "chiplet_1"]
                // ... 路由路径
            ]
        }
        // ... 更多路由条目
    }
}
```

### 9. BookSim配置文件 (BookSim Config Files)

**文件位置**: `inputs/booksim_configs/`
**示例**: `booksim_config_example_experiment.json`

```json
{
    "mode": "traffic",
    "ignore_cycles": 0,
    "precision": 0.001,
    "saturation_factor": 5,
    "num_vcs": 4,
    "vc_buf_size": 16,
    "warmup_periods": 1,
    "sim_count": 1,
    "hold_switch_for_packet": 0,
    "packet_size": 1,
    "vc_allocator": "separable_input_first",
    "sw_allocator": "separable_input_first",
    "alloc_iters": 1,
    "sample_period": 5300,
    "wait_for_tail_credit": 0,
    "priority": "none",
    "injection_rate_uses_flits": 1,
    "deadlock_warn_timeout": 1024
}
```

**参数说明**：
- `mode`: 仿真模式（traffic/trace）
- `precision`: 结果精度
- `saturation_factor`: 饱和因子
- `num_vcs`: 虚通道数量
- `vc_buf_size`: 虚通道缓冲区大小
- `warmup_periods`: 预热周期数
- `sim_count`: 仿真次数
- `packet_size`: 数据包大小
- `vc_allocator`: 虚通道分配器类型
- `sw_allocator`: 交换分配器类型

---

## 输入参数总结

### 必须手动创建的文件

1. **工艺技术文件** (`technologies/`) - 定义工艺参数
2. **封装文件** (`packagings/`) - 定义封装和中介层参数

### 可以使用生成工具的文件

1. **Chiplet规格** - 使用 `generate_chiplet.py`
2. **布局** - 使用 `generate_placement.py`
3. **拓扑** - 使用 `generate_topology.py`
4. **路由表** - 使用 `generate_routing.py`
5. **流量** - 使用 `generate_traffic.py`
6. **完整设计** - 使用 `generate_inputs.py`

### 默认值可用的参数

- 大多数几何参数（尺寸、位置）可以根据拓扑自动计算
- 流量模式可以使用预定义模式（随机均匀、转置等）
- 路由算法可以选择预实现算法（SPLIF、SPTMR）

### 需要用户自定义的参数

- 工艺技术参数（必须根据实际工艺定义）
- 功耗和性能目标
- 特定的应用流量模式
- 设计约束（尺寸、成本等）

---

## 输入生成工具使用方法

### 1. 完整设计生成 (`generate_inputs.py`)

```bash
# 参数定义
params = {
    "technologies_file": "inputs/technologies/example_technologies.json",
    "topology": "mesh",  # 或其他拓扑类型
    "grid_scale": "4x4",  # 网格尺寸
    "use_memory": False,  # 是否使用内存chiplet
    "chiplet_size": 10.0,  # chiplet尺寸 (mm)
    # ... 其他参数
}

# 生成输入文件
python generate_inputs.py --params params.json --design_name my_design
```

### 2. 单独文件生成

**生成路由表**：
```bash
python generate_routing.py -df inputs/designs/design_file.json -rtf routing_table.json -ra splif
```

**生成流量模式**：
```bash
python generate_traffic.py -df inputs/designs/design_file.json -tf traffic.json -tp random_uniform -par "{'injection_rate': 0.1}"
```

**生成拓扑**：
```bash
python generate_topology.py -df inputs/designs/design_file.json -tof topology.json -tn mesh
```

### 3. 支持的拓扑类型

- `mesh`: 网格拓扑
- `torus`: 环形拓扑
- `flattened_butterfly`: 扁平蝶形拓扑
- `hypercube`: 超立方体拓扑
- `kite_*`: 风筝拓扑变体
- `sparse_hamming_graph_*`: 稀疏汉明图

### 4. 支持的流量模式

- `random_uniform`: 随机均匀流量
- `transpose`: 转置流量
- `bit_complement`: 位补码流量
- `bit_rotation`: 位旋转流量
- `neighbor`: 邻居流量

### 5. 支持的路由算法

- `splif`: 最短路径最低ID优先（SPLIF）
- `sptmr`: 最短路径转向模型随机（SPTMR）

---

## 使用示例

### 1. 基本分析

```bash
# 分析设计的基本指标
python rapidchiplet.py -df inputs/designs/my_design.json -rf results.json -as -ps -ls -c

# 包含延迟和吞吐量分析
python rapidchiplet.py -df inputs/designs/my_design.json -rf results.json -as -ps -ls -c -l -t
```

### 2. BookSim仿真

```bash
# 运行周期精确仿真
python rapidchiplet.py -df inputs/designs/my_design.json -rf results.json -bs
```

### 3. 设计空间探索

```bash
# 运行自动化设计空间探索
python run_experiment.py -e experiments/experiment_file.json
```

### 4. 可视化

```bash
# 可视化完整芯片设计
python visualizer.py -df inputs/designs/my_design.json

# 创建性能图表
python create_plots.py -rf results.json -pt latency_vs_load
```

---

## 参数配置建议

### 1. 初学者配置

- 使用默认的示例文件作为起点
- 从简单的2x2或4x4网格开始
- 使用随机均匀流量模式
- 启用分析模式（不运行BookSim）

### 2. 高级用户配置

- 自定义工艺技术参数
- 设计特定的chiplet类型
- 实现自定义流量模式
- 运行完整的BookSim仿真

### 3. 性能优化配置

- 使用缓存结果避免重复计算
- 选择合适的分析精度级别
- 根据需要启用/禁用特定指标
- 使用并行处理进行大规模设计空间探索

---

## 常见问题解答

### Q: 如何选择合适的拓扑？
A: 根据应用需求选择：
- `mesh`: 适合通用计算，简单易实现
- `torus`: 适合高带宽需求
- `flattened_butterfly`: 适合低延迟需求
- `hypercube`: 适合大规模系统

### Q: 如何设置流量模式？
A: 根据应用特征：
- `random_uniform`: 通用基准测试
- `transpose`: 矩阵运算应用
- `neighbor`: 局部通信应用
- 自定义: 真实应用trace

### Q: 何时需要BookSim仿真？
A: 当需要：
- 周期精确的性能分析
- 详细的微架构研究
- 验证分析模型结果
- 研究特定的工作负载特性

### Q: 如何提高仿真速度？
A: 方法包括：
- 使用分析模型而非BookSim仿真
- 减少仿真参数精度
- 使用更简单的拓扑和流量模式
- 启用缓存机制

---

这个指南涵盖了RapidChiplet的核心性能特点、详细的输入系统说明以及实际使用方法。通过理解这些内容，用户可以有效地使用RapidChiplet进行chiplet系统的设计和分析。