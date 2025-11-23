# RapidChiplet多Chiplet通信延迟和能耗分析指南

## 需求分析

你的需求场景：
- **同时通信**: chiplet1 → chiplet3 (数据量x)，chiplet2 → chiplet4 (数据量y)
- **目标指标**: 通信延迟 + 能耗
- **考虑因素**: hops数 + 拥塞
- **核心问题**: 如何实现？需要什么输入？调用什么函数？

## 答案：完全可以实现！

RapidChiplet专门设计用于分析这种场景。让我逐步引导你：

## 第一步：理解RapidChiplet的分析能力

### ✅ 支持的功能
- **并发通信**: 支持多个chiplet同时通信
- **延迟分析**: 端到端延迟计算，考虑hops数
- **能耗分析**: 详细的功耗和能耗计算
- **拥塞建模**: 通过BookSim仿真考虑拥塞
- **位置感知**: 基于实际物理位置计算

### 🎯 核心分析函数
```python
# 在rapidchiplet.py中
- compute_latency()      # 延迟分析
- compute_power_summary() # 能耗分析
- compute_booksim_simulation() # 考虑拥塞的精确仿真
```

## 第二步：准备必需的输入信息

### 🔧 你需要提供的信息

#### 1. 芯片配置 (inputs/chiplets/)
```json
{
  "chiplet1": {
    "dimensions": {"x": 10.0, "y": 10.0},
    "unit_count": 8,
    "base_chiplet_power": 20.0,
    "phy_power": 0.125,
    "phys": [
      {"x": 0.0, "y": 5.0},   # PHY 0: 西
      {"x": 5.0, "y": 0.0},   # PHY 1: 南
      {"x": 10.0, "y": 5.0},  # PHY 2: 东
      {"x": 5.0, "y": 10.0}   # PHY 3: 北
    ]
  },
  // chiplet2, chiplet3, chiplet4 类似配置
}
```

#### 2. 位置信息 (inputs/placements/)
```json
{
  "chiplets": [
    {"position": {"x": 0, "y": 0}, "rotation": 0, "name": "chiplet1"},
    {"position": {"x": 15, "y": 0}, "rotation": 0, "name": "chiplet2"},
    {"position": {"x": 0, "y": 15}, "rotation": 0, "name": "chiplet3"},
    {"position": {"x": 15, "y": 15}, "rotation": 0, "name": "chiplet4"}
  ],
  "interposer_routers": []
}
```

#### 3. 网络拓扑 (inputs/topologies/)
```json
[
  {
    "ep1": {"type": "chiplet", "outer_id": 0, "inner_id": 2},
    "ep2": {"type": "chiplet", "outer_id": 2, "inner_id": 0},
    "color": "#000099"
  },
  // 定义chiplet1到chiplet3的连接
  {
    "ep1": {"type": "chiplet", "outer_id": 1, "inner_id": 2},
    "ep2": {"type": "chiplet", "outer_id": 3, "inner_id": 0},
    "color": "#009900"
  },
  // 定义chiplet2到chiplet4的连接
  // ... 其他连接
]
```

#### 4. 路由表 (inputs/routing_tables/)
RapidChiplet会自动生成，或使用generate_routing.py生成

#### 5. 你的流量模式 (inputs/traffic_by_unit/)
```json
{
  "(0, 0)-(2, 1)": x,  // chiplet1的单元0到chiplet3的单元1，数据量x
  "(1, 0)-(3, 1)": y   // chiplet2的单元0到chiplet4的单元1，数据量y
}
```

#### 6. 封装和工艺参数
- **封装配置** (inputs/packagings/): 链路延迟、带宽等
- **工艺技术** (inputs/technologies/): 功耗密度、面积缩放等

## 第三步：实现方案

### 方案A：快速分析（推荐入门）

#### 步骤1：生成完整输入
```bash
python3 generate_inputs.py \
  --grid_scale "2x2" \
  --topology "mesh" \
  --traffic_pattern "custom" \
  --custom_traffic "your_traffic.json"
```

#### 步骤2：运行分析
```bash
python3 rapidchiplet.py \
  -df inputs/designs/your_design.json \
  -rf results/your_results.json \
  -l -t -ps  # 计算+延迟+吞吐量+功耗
```

#### 步骤3：查看结果
```python
import helpers as hlp
results = hlp.read_json("results/your_results.json")

# 延迟结果
latency = results["latency"]["avg_latency"]
print(f"平均延迟: {latency} cycles")

# 能耗结果
power = results["power_summary"]["total_power"]
print(f"总功耗: {power} W")
```

### 方案B：精确仿真（考虑拥塞）

#### 步骤1：生成BookSim配置
```bash
python3 rapidchiplet.py \
  -df inputs/designs/your_design.json \
  -rf results/your_results.json \
  -bs  # 启用BookSim仿真
```

#### 步骤2：分析拥塞情况
BookSim会仿真不同负载下的网络性能，包括：
- 包级别的延迟
- 缓冲区占用率
- 链路利用率
- 拥塞导致的延迟增加

## 第四步：具体实现代码

### 创建自定义流量生成器
```python
# create_custom_traffic.py
import helpers as hlp
import json

def create_your_traffic():
    # 读取基础配置
    placement = hlp.read_json("inputs/placements/your_placement.json")
    chiplets = hlp.read_json("inputs/chiplets/your_chiplets.json")

    # 定义你的流量
    traffic = {}

    # chiplet1 -> chiplet3, 数据量x
    traffic[(0, 0), (2, 1)] = x  # (chiplet_id, unit_id)

    # chiplet2 -> chiplet4, 数据量y
    traffic[(1, 0), (3, 1)] = y

    return traffic

# 保存流量配置
traffic = create_your_traffic()
hlp.write_json("inputs/traffic_by_unit/your_traffic.json", traffic)
```

### 运行完整分析
```python
# run_analysis.py
import rapidchiplet as rc
import helpers as hlp

def analyze_multi_chiplet_communication():
    # 设置输入
    inputs = {
        "design": "inputs/designs/your_design.json",
        "verbose": True,
        "validate": True
    }

    # 设置要计算的指标
    do_compute = {
        "latency": True,      # 延迟分析
        "throughput": True,   # 吞吐量分析
        "power_summary": True, # 功耗分析
        "booksim_simulation": True # 考虑拥塞的精确仿真
    }

    # 运行分析
    intermediates = {}
    results = rc.rapidchiplet(inputs, intermediates, do_compute, "multi_chiplet_results")

    # 提取你关心的结果
    print("=== 延迟分析结果 ===")
    latency_results = results["latency"]
    print(f"平均延迟: {latency_results['avg_latency']} cycles")
    print(f"最大延迟: {latency_results['max_latency']} cycles")

    print("\n=== 能耗分析结果 ===")
    power_results = results["power_summary"]
    print(f"总功耗: {power_results['total_power']} W")
    print(f"动态功耗: {power_results['dynamic_power']} W")
    print(f"静态功耗: {power_results['static_power']} W")

    # 如果启用了BookSim仿真
    if "booksim_simulation" in results:
        print("\n=== BookSim精确仿真结果 ===")
        booksim_results = results["booksim_simulation"]
        for load, data in booksim_results.items():
            if hlp.is_float(load):
                print(f"负载 {load}: 延迟 {data['packet_latency']['avg']} cycles")

    return results

if __name__ == "__main__":
    analyze_multi_chiplet_communication()
```

## 第五步：高级配置选项

### 考虑拥塞的配置
```json
// inputs/booksim_configs/your_config.json
{
  "network": "anynet",
  "sim_cycles": 10000,
  "warmup_cycles": 1000,
  "buffer_size": 8,
  "link_bandwidth": 10,
  "routing_function": "xy_routing",
  "vc_allocator": "separable",
  "sw_allocator": "round_robin"
}
```

### 调整网络参数
```json
// inputs/packagings/your_packaging.json
{
  "link_latency_type": "distance_based",
  "link_latency": "lambda length: 0.1*length + 2",
  "link_bandwidth": 100,  // Gbps
  "link_routing": "manhattan"
}
```

## 第六步：结果解读

### 延迟结果解读
- **计算延迟**: 基于hops数和链路延迟
- **排队延迟**: 考虑拥塞的影响
- **传输延迟**: 基于数据量和链路带宽
- **总延迟**: 端到端的总延迟

### 能耗结果解读
- **计算能耗**: chiplet计算功耗
- **通信能耗**: 链路传输和路由器功耗
- **静态能耗**: 静态功耗
- **总能耗**: 系统总能耗

## 完整工作流程总结

1. **准备阶段**: 配置chiplet、位置、拓扑
2. **流量定义**: 指定你的通信模式和数量
3. **运行分析**: 调用RapidChiplet进行计算
4. **结果解读**: 分析延迟和能耗结果
5. **优化迭代**: 根据结果调整配置

## 下一步行动建议

1. **从示例开始**: 先运行examples了解基本流程
2. **逐步定制**: 在示例基础上逐步修改为你的配置
3. **验证结果**: 使用已知情况验证结果的正确性
4. **参数调优**: 根据需要调整网络参数
5. **扩展分析**: 可以考虑更多chiplet和更复杂的通信模式

这个框架完全支持你的需求，而且能够考虑你关心的所有因素（hops数、拥塞等）。开始建议先用方案A进行快速分析，熟悉后再用方案B进行精确仿真。