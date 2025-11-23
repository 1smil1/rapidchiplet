# create_plots.py 文件总结

## 功能概述
`create_plots.py` 是一个结果可视化工具，用于将 RapidChiplet 的仿真结果转换为图表格式，便于分析和展示。

## 主要功能

### 图表创建
- **`create_latency_vs_load_plot()`**: 创建延迟vs负载的关系图
- 从 BookSim 仿真结果中提取数据
- 生成负载-延迟曲线，展示网络性能特征

### 数据处理
- 验证结果文件中是否包含必要的 BookSim 仿真数据
- 提取负载点（浮点数键）和对应的平均延迟值
- 对数据进行排序以确保图表的正确性

### 图表配置
- 使用 matplotlib 创建 3x3 英寸的标准图表
- 配置网格、坐标轴标签和标题
- 自动保存为 PDF 格式到 `plots/` 目录

## 使用方式
```bash
python3 create_plots.py -rf results/<results-file> -pt latency_vs_load
```

## 参数说明
- `-rf/--results_file`: 指定要绘制的结果文件路径
- `-pt/--plot_type`: 指定图表类型（目前仅支持 `latency_vs_load`）

## 支持的图表类型
- **latency_vs_load**: 延迟与负载关系图
  - X轴：负载（注入率）
  - Y轴：平均延迟（周期）
  - 数据点：使用圆形标记

## 输出文件
- 图表保存为 `plots/latency_vs_load.pdf`
- 支持学术论文和报告使用

## 依赖关系
- **外部库**: `matplotlib`, `argparse`
- **内部模块**: `helpers.py`
- **数据源**: 包含 `booksim_simulation` 的结果文件

## 扩展性
- 代码结构支持添加新的图表类型
- 标准化的参数解析和错误处理
- 易于扩展以支持更多可视化需求