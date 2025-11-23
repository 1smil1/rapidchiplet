# generate_traffic.py 文件总结

## 功能概述
`generate_traffic.py` 是流量模式生成模块，支持多种合成流量模式和真实网络轨迹处理，用于网络性能分析和测试。

## 主要功能

### 支持的流量模式

#### 1. 随机均匀流量（Random Uniform）
- **函数**: `generate_random_uniform_traffic()`
- **特点**: 源节点随机选择目标节点
- **分布**: 所有目标节点概率相等
- **参数**: 发送芯片类型、接收芯片类型

#### 2. 转置流量（Transpose）
- **函数**: `generate_transpose_traffic()`
- **特点**: 矩阵转置的通信模式
- **适用**: 方形芯片布局
- **用途**: 模拟矩阵运算等应用

#### 3. 置换流量（Permutation）
- **函数**: `generate_permutation_traffic()`
- **特点**: 一对一的映射关系
- **类型**: 随机置换或特定模式
- **保证**: 每个节点有唯一的源和目标

#### 4. 热点流量（Hotspot）
- **函数**: `generate_hotspot_traffic()`
- **特点**: 部分节点接收大量流量
- **参数**: 热点数量、热点概率
- **用途**: 测试网络拥塞处理能力

### 流量生成算法

#### 随机均匀流量算法
1. 识别发送和接收类型的芯片
2. 为每个源单元生成流量分布
3. 均匀分配流量到所有可能的目标
4. 标准化流量值为1.0/n_dst

#### 热点流量算法
1. 随机选择指定数量的热点芯片
2. 分配高概率流量到热点
3. 剩余流量均匀分布到其他节点
4. 保证流量总和标准化

### 芯片类型过滤
支持基于芯片类型的流量生成：
- **计算芯片** (compute): 主要的流量发送者
- **内存芯片** (memory): 主要是流量接收者
- **I/O芯片** (io): 可发送可接收

### 流量数据结构
```python
traffic = {
    (source_chiplet_id, source_unit_id): {
        (dest_chiplet_id, dest_unit_id): flow_rate
    }
}
```

### 命令行接口
```bash
python3 generate_traffic.py -df <design_file> -tf <traffic_file> -tp <traffic_pattern> -par <parameters>
```

### 参数说明
- `-df`: 设计文件路径
- `-tf`: 流量文件名
- `-tp`: 流量模式类型
- `-par`: 模式特定参数（JSON格式）

## 模式特定参数

#### 随机均匀流量
```json
{
    "sending_types": ["compute"],
    "receiving_types": ["memory", "compute"]
}
```

#### 热点流量
```json
{
    "n_hotspot": 4,
    "p_hotspot": 0.5,
    "sending_types": ["compute"],
    "receiving_types": ["memory", "compute"]
}
```

## 输出文件
生成两个流量文件：
1. **按芯片的流量** (`inputs/traffic_by_chiplet/`)
2. **按单元的流量** (`inputs/traffic_by_unit/`)

## 流量转换
- 支持不同粒度的流量表示
- 自动转换单元级流量到芯片级流量
- 保持流量总量的一致性

## 使用场景
- 网络性能基准测试
- 应用流量模式模拟
- 拥塞分析
- 负载均衡研究

## 技术特点
- 多种标准流量模式
- 灵活的参数配置
- 芯片类型过滤
- 标准化输出格式
- 完整的命令行接口

## 依赖关系
- **内部模块**: `helpers.py`
- **数据结构**: 与芯片和布局配置紧密集成