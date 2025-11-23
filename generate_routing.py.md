# generate_routing.py 文件总结

## 功能概述
`generate_routing.py` 是路由表生成模块，实现了多种路由算法，为芯片间互连网络提供确定性的、无死锁的路由配置。

## 主要功能

### 支持的路由算法

#### 1. SPLIF算法（Shortest Path Lowest ID First）
- **函数**: `shortest_path_lowest_id_first_routing()`
- **特点**: 总是选择最低下一跳ID的最短路径
- **优势**: 确定性、无死锁
- **缺点**: 路径多样性差，可能导致拥塞

#### 2. SPTMR算法（Shortest Path Turn Model Random）
- **函数**: `shortest_path_turn_model_random_routing()`
- **特点**: 基于转弯模型的最短路径随机选择
- **优势**: 更好的路径多样性，减少拥塞
- **保障**: 保持无死锁特性

### 路由算法实现细节

#### SPLIF算法实现
- 使用Dijkstra算法计算最短路径
- 芯片ID低于所有互连路由器ID
- 优先选择ID最小的下一跳
- 为每个节点生成到所有芯片目的地的路由表

#### SPTMR算法实现
- 基于转弯模型的约束路由
- 随机选择多个合法路径
- 保证无死锁的转弯约束
- 提高网络负载均衡性能

### 核心数据结构

#### ICI图表示
- `nodes`: 网络节点列表
- `relay_map`: 中继映射
- `adj_list`: 邻接表
- `chiplets`: 芯片节点列表

#### 路由表结构
```python
routing_table = {
    node: {
        destination: next_hop
    }
}
```

### 图算法应用
- **Dijkstra算法**: 计算最短路径
- **优先队列**: 高效的路径搜索
- **图遍历**: 网络拓扑分析

### 路由表生成流程
1. 构建网络图表示
2. 对每个目标芯片运行路由算法
3. 计算所有节点到目标的下一跳
4. 生成完整的路由表

## 命令行接口
```bash
python3 generate_routing.py -df <design_file> -rtf <routing_table_file> -ra <routing_algorithm>
```

### 参数说明
- `-df`: 设计文件路径
- `-rtf`: 路由表文件名
- `-ra`: 路由算法（splif/sptmr）

## 输入输出
- **输入**: 网络拓扑和布局配置
- **输出**: JSON格式的路由表文件
- **存储位置**: `inputs/routing_tables/` 目录

## 依赖关系
- **外部库**: `networkx`, `itertools`, `queue`
- **内部模块**: `helpers.py`, `routing_utils.py`

## 使用场景
- 网络路由配置生成
- 不同路由算法性能比较
- 设计空间探索
- 网络性能优化

## 技术特点
- 实现多种标准路由算法
- 保证无死锁路由
- 高效的图算法实现
- 标准化的输出格式
- 完整的命令行接口