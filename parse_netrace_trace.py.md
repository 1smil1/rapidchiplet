# parse_netrace_trace.py 文件总结

## 功能概述
`parse_netrace_trace.py` 是Netrace轨迹解析模块，用于将标准的Netrace网络轨迹格式转换为RapidChiplet可用的格式，支持真实应用流量的仿真分析。

## 主要功能

### 轨迹格式转换
- **`export_trace()`**: 核心轨迹转换函数
- 将Netrace轨迹转换为RapidChiplet内部格式
- 支持节点映射和单位ID转换

### 包类型映射
定义了Netrace包类型到flit数量的映射：
```python
packet_type_to_size_map = {
    0: -1, 1: 1, 2: 9, 3: 9, 4: 9, 5: 1, 6: 9,
    13: 1, 14: 1, 15: 1, 16: 9, 25: 1, 27: 1,
    28: 1, 29: 1, 30: 9
}
```

### 节片映射系统
支持三种映射关系：
1. **trace_type_to_chiplet_type**: Netrace节点类型到芯片类型的映射
2. **units_per_chiplet_type**: 每种芯片类型包含的单元数量
3. **instances_per_chiplet_type**: 每种芯片类型的实例数量
4. **chiplet_id_list_per_chiplet_type**: 每种芯片类型的ID列表

### 坐标转换算法

#### 源节点转换
- 计算源芯片索引：`source // units_per_chiplet`
- 计算源芯片ID：从芯片ID列表中获取
- 计算源单元ID：`source % units_per_chiplet`

#### 目标节点转换
- 计算目标芯片索引：`destination // units_per_chiplet`
- 计算目标芯片ID：从芯片ID列表中获取
- 计算目标单元ID：`destination % units_per_chiplet`

### 数据包转换
将Netrace包格式转换为RapidChiplet格式：
```python
{
    "id": 包ID,
    "injection_cycle": 注入周期,
    "source_chiplet": 源芯片ID,
    "source_unit": 源单元ID,
    "destination_chiplet": 目标芯片ID,
    "destination_unit": 目标单元ID,
    "size_in_flits": flit数量
}
```

### 验证机制
- **节点数量验证**: 检查轨迹节点数与芯片配置的匹配性
- **类型映射验证**: 确保所有节点类型都有对应的芯片类型
- **一致性检查**: 验证转换结果的正确性

## 命令行接口
```bash
python3 parse_netrace_trace.py -df <design_file> -if <input_trace> -of <output_trace>
```

### 参数说明
- `-df`: 设计文件路径
- `-if`: 输入轨迹文件（Netrace格式）
- `-of`: 输出轨迹文件（RapidChiplet格式）

## 输入输出格式

### 输入格式（Netrace）
```json
{
    "nodes": 节点总数,
    "packets": [
        {
            "id": 包ID,
            "cycle": 注入周期,
            "src": 源节点ID,
            "dst": 目标节点ID,
            "src_type": 源节点类型,
            "dst_type": 目标节点类型,
            "type": 包类型
        }
    ]
}
```

### 输出格式（RapidChiplet）
转换为以芯片-单元为标识符的格式，便于RapidChiplet仿真使用。

## 使用场景

### 真实应用仿真
- 使用实际应用的通信模式
- 验证网络在真实负载下的性能
- 与合成流量模式进行对比

### 性能评估
- 不同应用特征的网络性能
- 真实流量模式下的拥塞分析
- 网络配置的有效性验证

### 研究应用
- 网络优化策略验证
- 新颖路由算法测试
- 芯片间通信模式研究

## 技术特点

### 灵活的映射系统
- 支持任意的芯片类型映射
- 可配置的单元数量
- 动态的芯片ID分配

### 高效的转换算法
- 线性时间复杂度
- 最小化内存占用
- 批量处理优化

### 完整的验证机制
- 多层次的数据验证
- 详细的错误报告
- 一致性保证

## 依赖关系
- **内部模块**: `helpers.py`
- **数据来源**: Netrace轨迹文件
- **集成**: 与RapidChiplet仿真系统无缝集成