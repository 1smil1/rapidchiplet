#!/usr/bin/env python3
"""
RapidChiplet结果分析脚本
深度分析4个chiplet通信的延迟和能耗结果
"""

import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import helpers as hlp

class ResultAnalyzer:
    def __init__(self):
        self.quick_results = None
        self.precise_results = None

    def load_results(self, quick_file="results/test_results_quick.json",
                     precise_file="results/test_results_precise.json"):
        """加载结果文件"""
        print("📂 加载结果文件...")

        # 加载快速分析结果
        if os.path.exists(quick_file):
            try:
                self.quick_results = hlp.read_json(quick_file)
                print(f"✅ 快速分析结果已加载: {quick_file}")
            except Exception as e:
                print(f"❌ 加载快速分析结果失败: {e}")

        # 加载精确仿真结果
        if os.path.exists(precise_file):
            try:
                self.precise_results = hlp.read_json(precise_file)
                print(f"✅ 精确仿真结果已加载: {precise_file}")
            except Exception as e:
                print(f"❌ 加载精确仿真结果失败: {e}")

    def analyze_communication_patterns(self):
        """分析通信模式"""
        print("\n📊 通信模式分析:")
        print("-" * 50)

        print("🎯 主要通信路径:")
        print("  • chiplet1 (计算) → chiplet3 (内存): 10GB/s")
        print("  • chiplet2 (计算) → chiplet4 (内存): 5GB/s")

        print("\n📏 预期路径分析:")
        print("  • chiplet1→chiplet3: 可能经过2 hops")
        print("    chiplet1 → chiplet2 → chiplet3 或")
        print("    chiplet1 → chiplet3 (直连)")
        print("  • chiplet2→chiplet4: 可能经过2 hops")
        print("    chiplet2 → chiplet1 → chiplet4 或")
        print("    chiplet2 → chiplet4 (直连)")

    def analyze_latency(self):
        """分析延迟结果"""
        print("\n⏱️  延迟分析:")
        print("-" * 50)

        if self.quick_results and "latency" in self.quick_results:
            latency = self.quick_results["latency"]

            avg_latency = latency.get("avg_latency", 0)
            max_latency = latency.get("max_latency", 0)
            min_latency = latency.get("min_latency", 0)

            print(f"📈 快速分析延迟结果:")
            print(f"  • 平均延迟: {avg_latency:.2f} cycles")
            print(f"  • 最大延迟: {max_latency:.2f} cycles")
            print(f"  • 最小延迟: {min_latency:.2f} cycles")

            # 延迟分布分析
            if max_latency > 0:
                latency_variation = (max_latency - min_latency) / avg_latency * 100
                print(f"  • 延迟变化率: {latency_variation:.1f}%")

        if self.precise_results and "booksim_simulation" in self.precise_results:
            booksim = self.precise_results["booksim_simulation"]

            print(f"\n🎯 BookSim精确仿真延迟结果:")

            loads = []
            latencies = []

            for load, data in booksim.items():
                if hlp.is_float(load):
                    packet_latency = data.get("packet_latency", {})
                    avg_latency = packet_latency.get("avg", 0)
                    loads.append(float(load))
                    latencies.append(avg_latency)
                    print(f"  • 负载 {load}: {avg_latency:.2f} cycles")

            # 计算延迟增长率
            if len(latencies) > 1:
                latency_increase = (latencies[-1] - latencies[0]) / latencies[0] * 100
                print(f"  • 高负载延迟增长: {latency_increase:.1f}%")

    def analyze_power(self):
        """分析功耗结果"""
        print("\n⚡ 功耗分析:")
        print("-" * 50)

        if self.quick_results and "power_summary" in self.quick_results:
            power = self.quick_results["power_summary"]

            total_power = power.get("total_power", 0)
            dynamic_power = power.get("dynamic_power", 0)
            static_power = power.get("static_power", 0)

            print(f"📈 功耗分析结果:")
            print(f"  • 总功耗: {total_power:.2f} W")
            print(f"  • 动态功耗: {dynamic_power:.2f} W")
            print(f"  • 静态功耗: {static_power:.2f} W")

            if total_power > 0:
                dynamic_ratio = dynamic_power / total_power * 100
                static_ratio = static_power / total_power * 100
                print(f"  • 动态功耗占比: {dynamic_ratio:.1f}%")
                print(f"  • 静态功耗占比: {static_ratio:.1f}%")

                # 功耗效率分析
                total_data_rate = 15.0  # 10GB/s + 5GB/s
                if total_data_rate > 0:
                    power_efficiency = total_data_rate / total_power
                    print(f"  • 功耗效率: {power_efficiency:.2f} GB/s per W")

    def analyze_throughput(self):
        """分析吞吐量结果"""
        print("\n📊 吞吐量分析:")
        print("-" * 50)

        if self.quick_results and "throughput" in self.quick_results:
            throughput = self.quick_results["throughput"]

            aggregate_throughput = throughput.get("aggregate_throughput", 0)
            max_throughput = throughput.get("max_throughput", 0)
            min_throughput = throughput.get("min_throughput", 0)

            print(f"📈 吞吐量分析结果:")
            print(f"  • 聚合吞吐量: {aggregate_throughput:.2f}")
            print(f"  • 最大吞吐量: {max_throughput:.2f}")
            print(f"  • 最小吞吐量: {min_throughput:.2f}")

            # 理论vs实际吞吐量对比
            theoretical_throughput = 15.0  # 10 + 5 GB/s
            if theoretical_throughput > 0:
                efficiency = aggregate_throughput / theoretical_throughput * 100
                print(f"  • 理论吞吐量: {theoretical_throughput:.2f} GB/s")
                print(f"  • 吞吐量效率: {efficiency:.1f}%")

    def analyze_link_utilization(self):
        """分析链路利用率"""
        print("\n🔗 链路利用率分析:")
        print("-" * 50)

        if self.quick_results and "link_summary" in self.quick_results:
            links = self.quick_results["link_summary"]

            bandwidths = links.get("bandwidths", {})
            lengths = links.get("lengths", {})

            print(f"📈 链路统计:")
            if bandwidths:
                print(f"  • 带宽范围: {bandwidths.get('min', 0):.2f} - {bandwidths.get('max', 0):.2f}")
            if lengths:
                print(f"  • 长度范围: {lengths.get('min', 0):.2f} - {lengths.get('max', 0):.2f} mm")

                # 平均链路长度
                if isinstance(lengths, dict) and len(lengths) > 0:
                    avg_length = sum(lengths.values()) / len(lengths)
                    print(f"  • 平均链路长度: {avg_length:.2f} mm")

    def create_comparison_plots(self):
        """创建对比图表"""
        print("\n📈 生成对比图表...")

        try:
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False

            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle('RapidChiplet 4-Chiplet通信分析结果', fontsize=16)

            # 延迟对比
            ax1 = axes[0, 0]
            if self.quick_results and "latency" in self.quick_results:
                latency = self.quick_results["latency"]
                categories = ['平均延迟', '最大延迟']
                values = [latency.get("avg_latency", 0), latency.get("max_latency", 0)]
                ax1.bar(categories, values, color=['#66AADD', '#DDAA66'])
                ax1.set_title('延迟分析')
                ax1.set_ylabel('延迟 (cycles)')

            # 功耗分析
            ax2 = axes[0, 1]
            if self.quick_results and "power_summary" in self.quick_results:
                power = self.quick_results["power_summary"]
                categories = ['动态功耗', '静态功耗']
                values = [power.get("dynamic_power", 0), power.get("static_power", 0)]
                ax2.bar(categories, values, color=['#66BB99', '#FF6600'])
                ax2.set_title('功耗分析')
                ax2.set_ylabel('功耗 (W)')

            # 吞吐量分析
            ax3 = axes[1, 0]
            if self.quick_results and "throughput" in self.quick_results:
                throughput = self.quick_results["throughput"]
                categories = ['聚合吞吐量']
                values = [throughput.get("aggregate_throughput", 0)]
                ax3.bar(categories, values, color=['#990099'])
                ax3.set_title('吞吐量分析')
                ax3.set_ylabel('吞吐量')

            # BookSim延迟曲线
            ax4 = axes[1, 1]
            if self.precise_results and "booksim_simulation" in self.precise_results:
                booksim = self.precise_results["booksim_simulation"]
                loads = []
                latencies = []

                for load, data in booksim.items():
                    if hlp.is_float(load):
                        packet_latency = data.get("packet_latency", {})
                        avg_latency = packet_latency.get("avg", 0)
                        loads.append(float(load))
                        latencies.append(avg_latency)

                if loads and latencies:
                    ax4.plot(loads, latencies, 'o-', color='#CC3333', linewidth=2)
                    ax4.set_title('BookSim延迟vs负载')
                    ax4.set_xlabel('负载')
                    ax4.set_ylabel('延迟 (cycles)')
                    ax4.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.savefig('results/test_analysis_plots.png', dpi=300, bbox_inches='tight')
            print("✅ 对比图表已保存: results/test_analysis_plots.png")

        except Exception as e:
            print(f"❌ 生成图表失败: {e}")

    def generate_summary_report(self):
        """生成总结报告"""
        print("\n📋 生成总结报告...")

        report = {
            "test_configuration": {
                "chiplet_size": "10mm x 10mm",
                "layout": "2x2 grid",
                "topology": "Mesh",
                "communications": [
                    {"source": "chiplet1", "destination": "chiplet3", "data_rate": "10GB/s"},
                    {"source": "chiplet2", "destination": "chiplet4", "data_rate": "5GB/s"}
                ]
            },
            "analysis_timestamp": str(__import__('datetime').datetime.now()),
            "results": {}
        }

        # 收集快速分析结果
        if self.quick_results:
            report["results"]["quick_analysis"] = {}

            if "latency" in self.quick_results:
                latency = self.quick_results["latency"]
                report["results"]["quick_analysis"]["latency"] = {
                    "avg_cycles": latency.get("avg_latency"),
                    "max_cycles": latency.get("max_latency")
                }

            if "power_summary" in self.quick_results:
                power = self.quick_results["power_summary"]
                report["results"]["quick_analysis"]["power"] = {
                    "total_watts": power.get("total_power"),
                    "dynamic_watts": power.get("dynamic_power"),
                    "static_watts": power.get("static_power")
                }

            if "throughput" in self.quick_results:
                throughput = self.quick_results["throughput"]
                report["results"]["quick_analysis"]["throughput"] = {
                    "aggregate": throughput.get("aggregate_throughput")
                }

        # 收集精确仿真结果
        if self.precise_results and "booksim_simulation" in self.precise_results:
            booksim = self.precise_results["booksim_simulation"]
            report["results"]["precise_simulation"] = {}

            for load, data in booksim.items():
                if hlp.is_float(load):
                    packet_latency = data.get("packet_latency", {})
                    report["results"]["precise_simulation"][f"load_{load}"] = {
                        "latency_avg_cycles": packet_latency.get("avg"),
                        "latency_max_cycles": packet_latency.get("max")
                    }

        # 保存报告
        hlp.write_json("results/test_summary_report.json", report)
        print("✅ 总结报告已保存: results/test_summary_report.json")

    def run_full_analysis(self):
        """运行完整分析"""
        print("🔍 开始完整结果分析...")
        print("=" * 60)

        # 加载结果
        self.load_results()

        if not self.quick_results and not self.precise_results:
            print("❌ 没有找到结果文件！请先运行 run_test.py")
            return

        # 各项分析
        self.analyze_communication_patterns()
        self.analyze_latency()
        self.analyze_power()
        self.analyze_throughput()
        self.analyze_link_utilization()

        # 生成图表和报告
        self.create_comparison_plots()
        self.generate_summary_report()

        print("\n🎉 分析完成！")
        print("📁 生成的文件:")
        print("  • 对比图表: results/test_analysis_plots.png")
        print("  • 总结报告: results/test_summary_report.json")

def main():
    """主函数"""
    analyzer = ResultAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()