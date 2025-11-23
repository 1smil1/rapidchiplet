#!/usr/bin/env python3
"""
RapidChiplet测试脚本
运行4个chiplet的通信延迟和能耗分析
"""

import sys
import os
import json
import time
import argparse

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import rapidchiplet as rc
import helpers as hlp
import visualizer as vis

def run_quick_analysis():
    """运行快速分析（方案A）"""
    print("=" * 60)
    print("🚀 开始运行快速分析（方案A）")
    print("=" * 60)

    # 设置输入
    inputs = {
        "design": "inputs/designs/test_design.json",
        "verbose": True,
        "validate": True
    }

    # 设置要计算的指标
    do_compute = {
        "latency": True,           # 延迟分析
        "throughput": True,        # 吞吐量分析
        "power_summary": True,     # 功耗分析
        "link_summary": True,      # 链路分析
        "cost": True               # 成本分析
    }

    # 运行分析
    intermediates = {}
    start_time = time.time()

    try:
        results = rc.rapidchiplet(inputs, intermediates, do_compute, "test_results_quick")
        end_time = time.time()

        print(f"\n✅ 快速分析完成！耗时: {end_time - start_time:.2f}秒")

        # 保存结果
        hlp.write_json("results/test_results_quick.json", results)
        print("📊 结果已保存到: results/test_results_quick.json")

        return results

    except Exception as e:
        print(f"❌ 快速分析失败: {e}")
        return None

def run_precise_simulation():
    """运行精确仿真（方案B）"""
    print("\n" + "=" * 60)
    print("🎯 开始运行精确仿真（方案B - BookSim）")
    print("=" * 60)

    # 设置输入
    inputs = {
        "design": "inputs/designs/test_design.json",
        "verbose": True,
        "validate": True
    }

    # 设置要计算的指标
    do_compute = {
        "booksim_simulation": True  # 启用BookSim仿真
    }

    # 运行仿真
    intermediates = {}
    start_time = time.time()

    try:
        results = rc.rapidchiplet(inputs, intermediates, do_compute, "test_results_precise")
        end_time = time.time()

        print(f"\n✅ 精确仿真完成！耗时: {end_time - start_time:.2f}秒")

        # 保存结果
        hlp.write_json("results/test_results_precise.json", results)
        print("📊 结果已保存到: results/test_results_precise.json")

        return results

    except Exception as e:
        print(f"❌ 精确仿真失败: {e}")
        print("💡 提示: 请确保BookSim2已正确编译")
        return None

def visualize_design():
    """生成设计可视化"""
    print("\n" + "=" * 60)
    print("🎨 生成设计可视化")
    print("=" * 60)

    try:
        inputs = {
            "design": "inputs/designs/test_design.json",
            "verbose": True,
            "validate": True
        }

        # 生成可视化
        vis.visualize_design(inputs, "test_design", show_chiplet_id=True, show_phy_id=False)
        print("✅ 设计可视化已生成: images/test_design.pdf")

    except Exception as e:
        print(f"❌ 可视化生成失败: {e}")

def analyze_results(quick_results, precise_results):
    """分析并对比结果"""
    print("\n" + "=" * 60)
    print("📈 结果分析")
    print("=" * 60)

    if quick_results:
        print("\n🚀 快速分析结果:")
        print("-" * 40)

        # 延迟分析
        if "latency" in quick_results:
            latency = quick_results["latency"]
            print(f"📏 平均延迟: {latency.get('avg_latency', 'N/A')} cycles")
            print(f"📏 最大延迟: {latency.get('max_latency', 'N/A')} cycles")
            print(f"⏱️  分析时间: {latency.get('time_taken', 'N/A')} 秒")

        # 功耗分析
        if "power_summary" in quick_results:
            power = quick_results["power_summary"]
            print(f"⚡ 总功耗: {power.get('total_power', 'N/A')} W")
            print(f"⚡ 动态功耗: {power.get('dynamic_power', 'N/A')} W")
            print(f"⚡ 静态功耗: {power.get('static_power', 'N/A')} W")

        # 吞吐量分析
        if "throughput" in quick_results:
            throughput = quick_results["throughput"]
            print(f"📊 聚合吞吐量: {throughput.get('aggregate_throughput', 'N/A')}")

        # 链路分析
        if "link_summary" in quick_results:
            links = quick_results["link_summary"]
            bandwidths = links.get("bandwidths", {})
            print(f"🔗 链路带宽范围: {bandwidths.get('min', 'N/A')} - {bandwidths.get('max', 'N/A')}")

    if precise_results:
        print("\n🎯 精确仿真结果:")
        print("-" * 40)

        if "booksim_simulation" in precise_results:
            booksim = precise_results["booksim_simulation"]

            print("📊 不同负载下的性能:")
            for load, data in booksim.items():
                if hlp.is_float(load):
                    packet_latency = data.get("packet_latency", {})
                    print(f"  负载 {load}: 延迟 {packet_latency.get('avg', 'N/A')} cycles")

    print("\n💡 分析要点:")
    print("  • chiplet1→chiplet3 数据量: 10GB/s")
    print("  • chiplet2→chiplet4 数据量: 5GB/s")
    print("  • 网络拓扑: Mesh网络")
    print("  • 布局: 2×2网格")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='RapidChiplet 4-Chiplet通信测试')
    parser.add_argument('--quick', action='store_true', help='只运行快速分析')
    parser.add_argument('--precise', action='store_true', help='只运行精确仿真')
    parser.add_argument('--visualize', action='store_true', help='只生成可视化')
    parser.add_argument('--all', action='store_true', help='运行所有测试（默认）')

    args = parser.parse_args()

    # 默认运行所有测试
    if not any([args.quick, args.precise, args.visualize]):
        args.all = True

    # 确保输出目录存在
    os.makedirs("results", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    print("🎯 RapidChiplet 4-Chiplet通信分析测试")
    print("📋 测试配置:")
    print("  • 芯片尺寸: 10mm × 10mm")
    print("  • 布局: 2×2网格")
    print("  • 通信模式: chiplet1→chiplet3(10GB/s), chiplet2→chiplet4(5GB/s)")
    print("  • 网络拓扑: Mesh")

    quick_results = None
    precise_results = None

    # 运行测试
    if args.all or args.quick:
        quick_results = run_quick_analysis()

    if args.all or args.precise:
        precise_results = run_precise_simulation()

    if args.all or args.visualize:
        visualize_design()

    # 分析结果
    if quick_results or precise_results:
        analyze_results(quick_results, precise_results)

    print("\n🎉 测试完成！")
    print("📁 结果文件位置:")
    print("  • 快速分析: results/test_results_quick.json")
    print("  • 精确仿真: results/test_results_precise.json")
    print("  • 可视化图: images/test_design.pdf")

if __name__ == "__main__":
    main()