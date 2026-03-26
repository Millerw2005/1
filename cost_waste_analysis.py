import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置样式
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8-whitegrid')

# ==========================================
# 第一步：生成原材料数据集
# ==========================================
np.random.seed(42)

# 定义原材料数据
raw_materials = [
    # 主料（15种）
    {"name": "优质钢材A", "category": "主料", "unit_price": 4500, "monthly_usage": 120},
    {"name": "铝合金型材", "category": "主料", "unit_price": 2800, "monthly_usage": 85},
    {"name": "铜材", "category": "主料", "unit_price": 6200, "monthly_usage": 45},
    {"name": "不锈钢板", "category": "主料", "unit_price": 3800, "monthly_usage": 95},
    {"name": "塑料颗粒", "category": "主料", "unit_price": 1200, "monthly_usage": 200},
    {"name": "橡胶原料", "category": "主料", "unit_price": 1800, "monthly_usage": 150},
    {"name": "玻璃原片", "category": "主料", "unit_price": 2200, "monthly_usage": 110},
    {"name": "电子元件", "category": "主料", "unit_price": 3500, "monthly_usage": 75},
    {"name": "精密轴承", "category": "主料", "unit_price": 4800, "monthly_usage": 60},
    {"name": "液压元件", "category": "主料", "unit_price": 5200, "monthly_usage": 55},
    {"name": "碳纤维材料", "category": "主料", "unit_price": 8500, "monthly_usage": 25},
    {"name": "钛合金", "category": "主料", "unit_price": 12000, "monthly_usage": 18},
    {"name": "陶瓷原料", "category": "主料", "unit_price": 3200, "monthly_usage": 65},
    {"name": "纺织面料", "category": "主料", "unit_price": 950, "monthly_usage": 180},
    {"name": "木材", "category": "主料", "unit_price": 1500, "monthly_usage": 140},
    
    # 辅料（12种）
    {"name": "焊接材料", "category": "辅料", "unit_price": 280, "monthly_usage": 300},
    {"name": "密封件", "category": "辅料", "unit_price": 150, "monthly_usage": 450},
    {"name": "紧固件", "category": "辅料", "unit_price": 80, "monthly_usage": 600},
    {"name": "润滑油", "category": "辅料", "unit_price": 350, "monthly_usage": 250},
    {"name": "涂料", "category": "辅料", "unit_price": 420, "monthly_usage": 200},
    {"name": "胶粘剂", "category": "辅料", "unit_price": 180, "monthly_usage": 380},
    {"name": "绝缘材料", "category": "辅料", "unit_price": 260, "monthly_usage": 320},
    {"name": "过滤材料", "category": "辅料", "unit_price": 120, "monthly_usage": 500},
    {"name": "研磨材料", "category": "辅料", "unit_price": 95, "monthly_usage": 420},
    {"name": "清洗剂", "category": "辅料", "unit_price": 65, "monthly_usage": 550},
    {"name": "防锈剂", "category": "辅料", "unit_price": 140, "monthly_usage": 400},
    {"name": "催化剂", "category": "辅料", "unit_price": 580, "monthly_usage": 150},
    
    # 包装材料（8种）
    {"name": "纸箱", "category": "包装材料", "unit_price": 25, "monthly_usage": 800},
    {"name": "塑料袋", "category": "包装材料", "unit_price": 12, "monthly_usage": 1200},
    {"name": "泡沫板", "category": "包装材料", "unit_price": 35, "monthly_usage": 600},
    {"name": "木托盘", "category": "包装材料", "unit_price": 85, "monthly_usage": 350},
    {"name": "缠绕膜", "category": "包装材料", "unit_price": 45, "monthly_usage": 480},
    {"name": "标签纸", "category": "包装材料", "unit_price": 8, "monthly_usage": 1500},
    {"name": "缓冲材料", "category": "包装材料", "unit_price": 55, "monthly_usage": 400},
    {"name": "打包带", "category": "包装材料", "unit_price": 18, "monthly_usage": 900},
]

# 损耗原因及权重
waste_reasons = ["存储不当", "加工工艺", "运输破损", "质量问题", "过期报废"]
waste_reason_weights = {"存储不当": 0.35, "加工工艺": 0.30, "运输破损": 0.20, "质量问题": 0.10, "过期报废": 0.05}

# 生成完整数据集
data = []
for material in raw_materials:
    # 生成多个采购批次
    for batch in range(1, 4):
        # 根据品类设定基础损耗率范围
        if material["category"] == "主料":
            base_waste_rate = np.random.uniform(2, 8)
        elif material["category"] == "辅料":
            base_waste_rate = np.random.uniform(3, 12)
        else:  # 包装材料
            base_waste_rate = np.random.uniform(5, 15)
        
        # 随机选择损耗原因
        waste_reason = np.random.choice(waste_reasons, p=list(waste_reason_weights.values()))
        
        # 根据损耗原因微调损耗率
        if waste_reason == "存储不当":
            waste_rate = base_waste_rate * np.random.uniform(1.0, 1.3)
        elif waste_reason == "加工工艺":
            waste_rate = base_waste_rate * np.random.uniform(0.9, 1.2)
        elif waste_reason == "运输破损":
            waste_rate = base_waste_rate * np.random.uniform(1.1, 1.4)
        elif waste_reason == "质量问题":
            waste_rate = base_waste_rate * np.random.uniform(0.8, 1.1)
        else:  # 过期报废
            waste_rate = base_waste_rate * np.random.uniform(0.7, 1.0)
        
        waste_rate = round(waste_rate, 2)
        
        # 计算总成本和损耗成本
        total_cost = material["unit_price"] * material["monthly_usage"]
        waste_cost = total_cost * (waste_rate / 100)
        
        data.append({
            "原材料名称": material["name"],
            "品类": material["category"],
            "采购单价": material["unit_price"],
            "月使用量": material["monthly_usage"],
            "总成本": round(total_cost, 2),
            "损耗率(%)": waste_rate,
            "损耗原因": waste_reason,
            "采购批次": f"批次{batch}",
            "损耗成本": round(waste_cost, 2)
        })

df = pd.DataFrame(data)

# 保存原始数据
df.to_csv("原材料成本损耗数据集.csv", index=False, encoding='utf-8-sig')
print("=" * 60)
print("原材料成本与损耗率关联分析 - 数据集生成完成")
print("=" * 60)
print(f"\n数据集概览：共 {len(df)} 条记录")
print(f"\n数据预览：")
print(df.head(10).to_string())
print(f"\n数据统计：")
print(df.groupby("品类").agg({
    "原材料名称": "nunique",
    "总成本": "sum",
    "损耗率(%)": "mean",
    "损耗成本": "sum"
}).round(2))

# ==========================================
# 第二步：创建可视化图表
# ==========================================

# 创建一个大图表，包含3个维度的分析
fig = plt.figure(figsize=(24, 32))

# 定义颜色方案
colors_category = {"主料": "#2E86AB", "辅料": "#A23B72", "包装材料": "#F18F01"}
colors_waste_reason = {"存储不当": "#E63946", "加工工艺": "#F4A261", "运输破损": "#2A9D8F", 
                       "质量问题": "#264653", "过期报废": "#9B5DE5"}

# ==========================================
# 第一维度：成本分布可视化
# ==========================================

# 1.1 品类成本占比饼图
ax1 = plt.subplot(4, 3, 1)
category_cost = df.groupby("品类")["总成本"].sum()
colors_pie = [colors_category[cat] for cat in category_cost.index]
wedges, texts, autotexts = ax1.pie(category_cost.values, labels=category_cost.index, 
                                    autopct='%1.1f%%', colors=colors_pie,
                                    explode=[0.02, 0.02, 0.02], startangle=90)
ax1.set_title("第一维度：品类成本占比分布\n（总成本构成分析）", fontsize=14, fontweight='bold', pad=20)
for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')

# 添加图例说明
legend_labels = [f"{cat}: ¥{cost:,.0f}" for cat, cost in zip(category_cost.index, category_cost.values)]
ax1.legend(wedges, legend_labels, title="品类成本", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

# 1.2 各品类成本柱状图
ax2 = plt.subplot(4, 3, 2)
bars = ax2.bar(category_cost.index, category_cost.values, color=[colors_category[cat] for cat in category_cost.index],
               edgecolor='black', linewidth=1.2)
ax2.set_ylabel("总成本 (元)", fontsize=12)
ax2.set_title("各品类总成本对比", fontsize=13, fontweight='bold')
ax2.set_ylim(0, max(category_cost.values) * 1.15)

# 添加数值标签
for bar, value in zip(bars, category_cost.values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'¥{value:,.0f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# 添加网格线
ax2.yaxis.grid(True, linestyle='--', alpha=0.7)
ax2.set_axisbelow(True)

# 1.3 单品成本排序TOP15
ax3 = plt.subplot(4, 3, 3)
material_cost = df.groupby("原材料名称")["总成本"].first().sort_values(ascending=True).tail(15)
material_category = df.groupby("原材料名称")["品类"].first()
colors_bar = [colors_category[material_category[name]] for name in material_cost.index]

bars = ax3.barh(range(len(material_cost)), material_cost.values, color=colors_bar, edgecolor='black', linewidth=0.8)
ax3.set_yticks(range(len(material_cost)))
ax3.set_yticklabels(material_cost.index, fontsize=10)
ax3.set_xlabel("总成本 (元)", fontsize=12)
ax3.set_title("单品成本排序 TOP15\n（高成本原材料识别）", fontsize=13, fontweight='bold')

# 添加数值标签
for i, (bar, value) in enumerate(zip(bars, material_cost.values)):
    ax3.text(value, bar.get_y() + bar.get_height()/2.,
             f' ¥{value:,.0f}',
             ha='left', va='center', fontsize=9)

ax3.set_xlim(0, max(material_cost.values) * 1.2)

# ==========================================
# 第二维度：损耗率高低可视化
# ==========================================

# 2.1 各品类平均损耗率对比
ax4 = plt.subplot(4, 3, 4)
category_waste = df.groupby("品类")["损耗率(%)"].mean().sort_values(ascending=False)
bars = ax4.bar(category_waste.index, category_waste.values, 
               color=[colors_category[cat] for cat in category_waste.index],
               edgecolor='black', linewidth=1.2)
ax4.set_ylabel("平均损耗率 (%)", fontsize=12)
ax4.set_title("第二维度：各品类平均损耗率对比\n（损耗率高低识别）", fontsize=14, fontweight='bold', pad=20)
ax4.set_ylim(0, max(category_waste.values) * 1.2)

# 添加数值标签
for bar, value in zip(bars, category_waste.values):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{value:.2f}%',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# 添加警戒线
ax4.axhline(y=8, color='red', linestyle='--', linewidth=2, alpha=0.7, label='警戒线 (8%)')
ax4.legend(loc='upper right', fontsize=10)
ax4.yaxis.grid(True, linestyle='--', alpha=0.7)
ax4.set_axisbelow(True)

# 2.2 单品损耗率排序TOP15（高损耗预警）
ax5 = plt.subplot(4, 3, 5)
material_waste = df.groupby("原材料名称")["损耗率(%)"].mean().sort_values(ascending=True).tail(15)
material_category = df.groupby("原材料名称")["品类"].first()
colors_bar = [colors_category[material_category[name]] for name in material_waste.index]

bars = ax5.barh(range(len(material_waste)), material_waste.values, color=colors_bar, edgecolor='black', linewidth=0.8)
ax5.set_yticks(range(len(material_waste)))
ax5.set_yticklabels(material_waste.index, fontsize=10)
ax5.set_xlabel("平均损耗率 (%)", fontsize=12)
ax5.set_title("高损耗率原材料 TOP15\n（损耗管控重点对象）", fontsize=13, fontweight='bold')

# 添加数值标签
for i, (bar, value) in enumerate(zip(bars, material_waste.values)):
    ax5.text(value, bar.get_y() + bar.get_height()/2.,
             f' {value:.2f}%',
             ha='left', va='center', fontsize=9)

ax5.axvline(x=10, color='red', linestyle='--', linewidth=2, alpha=0.7)
ax5.set_xlim(0, max(material_waste.values) * 1.15)

# 2.3 损耗率分布区间箱线图
ax6 = plt.subplot(4, 3, 6)
categories = df["品类"].unique()
box_data = [df[df["品类"] == cat]["损耗率(%)"].values for cat in ["主料", "辅料", "包装材料"]]
bp = ax6.boxplot(box_data, labels=["主料", "辅料", "包装材料"], patch_artist=True)

for patch, cat in zip(bp['boxes'], ["主料", "辅料", "包装材料"]):
    patch.set_facecolor(colors_category[cat])
    patch.set_alpha(0.7)

for whisker in bp['whiskers']:
    whisker.set(color='black', linewidth=1.5)
for cap in bp['caps']:
    cap.set(color='black', linewidth=1.5)
for median in bp['medians']:
    median.set(color='red', linewidth=2)

ax6.set_ylabel("损耗率 (%)", fontsize=12)
ax6.set_title("损耗率分布区间分析\n（箱线图展示数据离散程度）", fontsize=13, fontweight='bold')
ax6.yaxis.grid(True, linestyle='--', alpha=0.7)
ax6.set_axisbelow(True)

# ==========================================
# 第三维度：损耗原因对成本的影响可视化
# ==========================================

# 3.1 各损耗原因的成本损耗金额
ax7 = plt.subplot(4, 3, 7)
reason_cost = df.groupby("损耗原因")["损耗成本"].sum().sort_values(ascending=False)
colors_reason = [colors_waste_reason[reason] for reason in reason_cost.index]

bars = ax7.bar(reason_cost.index, reason_cost.values, color=colors_reason, edgecolor='black', linewidth=1.2)
ax7.set_ylabel("损耗成本金额 (元)", fontsize=12)
ax7.set_title("第三维度：各损耗原因对应的成本损耗\n（损耗原因影响权重分析）", fontsize=14, fontweight='bold', pad=20)
ax7.set_ylim(0, max(reason_cost.values) * 1.15)
plt.setp(ax7.xaxis.get_majorticklabels(), rotation=15, ha='right')

# 添加数值标签
for bar, value in zip(bars, reason_cost.values):
    height = bar.get_height()
    ax7.text(bar.get_x() + bar.get_width()/2., height,
             f'¥{value:,.0f}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

ax7.yaxis.grid(True, linestyle='--', alpha=0.7)
ax7.set_axisbelow(True)

# 3.2 损耗原因占比饼图
ax8 = plt.subplot(4, 3, 8)
wedges, texts, autotexts = ax8.pie(reason_cost.values, labels=reason_cost.index, 
                                    autopct='%1.1f%%', colors=colors_reason,
                                    explode=[0.03]*len(reason_cost), startangle=90)
ax8.set_title("损耗原因成本占比分布", fontsize=13, fontweight='bold')
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')

# 3.3 品类×损耗原因热力图
ax9 = plt.subplot(4, 3, 9)
heatmap_data = df.pivot_table(values="损耗成本", index="损耗原因", columns="品类", aggfunc="sum")
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax9, 
            cbar_kws={'label': '损耗成本 (元)'}, linewidths=0.5)
ax9.set_title("品类×损耗原因 成本损耗热力图\n（交叉分析矩阵）", fontsize=13, fontweight='bold')
ax9.set_xlabel("品类", fontsize=12)
ax9.set_ylabel("损耗原因", fontsize=12)

# ==========================================
# 综合分析图表
# ==========================================

# 4.1 成本vs损耗率散点图（核心关联分析）
ax10 = plt.subplot(4, 3, 10)
material_summary = df.groupby("原材料名称").agg({
    "总成本": "first",
    "损耗率(%)": "mean",
    "品类": "first",
    "损耗成本": "first"
})

for category in ["主料", "辅料", "包装材料"]:
    cat_data = material_summary[material_summary["品类"] == category]
    ax10.scatter(cat_data["总成本"], cat_data["损耗率(%)"], 
                c=colors_category[category], label=category, s=120, alpha=0.7, edgecolors='black', linewidth=1)

ax10.set_xlabel("总成本 (元)", fontsize=12)
ax10.set_ylabel("平均损耗率 (%)", fontsize=12)
ax10.set_title("成本与损耗率关联散点图\n（高成本高损耗核心对象识别）", fontsize=13, fontweight='bold')
ax10.legend(title="品类", loc='upper right', fontsize=10)
ax10.grid(True, linestyle='--', alpha=0.5)

# 添加象限分割线
ax10.axhline(y=material_summary["损耗率(%)"].mean(), color='red', linestyle='--', linewidth=1.5, alpha=0.7)
ax10.axvline(x=material_summary["总成本"].median(), color='red', linestyle='--', linewidth=1.5, alpha=0.7)

# 标注高风险点（高成本高损耗）
high_risk = material_summary[(material_summary["总成本"] > material_summary["总成本"].median()) & 
                             (material_summary["损耗率(%)"] > material_summary["损耗率(%)"].mean())]
for idx, row in high_risk.head(3).iterrows():
    ax10.annotate(idx, (row["总成本"], row["损耗率(%)"]), 
                 xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

# 4.2 采购批次损耗率趋势
ax11 = plt.subplot(4, 3, 11)
batch_waste = df.groupby(["采购批次", "品类"])["损耗率(%)"].mean().unstack()
for category in ["主料", "辅料", "包装材料"]:
    if category in batch_waste.columns:
        ax11.plot(batch_waste.index, batch_waste[category], marker='o', linewidth=2.5, 
                 markersize=8, label=category, color=colors_category[category])

ax11.set_xlabel("采购批次", fontsize=12)
ax11.set_ylabel("平均损耗率 (%)", fontsize=12)
ax11.set_title("采购批次损耗率趋势分析\n（批次质量稳定性监控）", fontsize=13, fontweight='bold')
ax11.legend(title="品类", loc='best', fontsize=10)
ax11.grid(True, linestyle='--', alpha=0.5)
ax11.set_axisbelow(True)

# 4.3 成本损耗结构瀑布图（简化版）
ax12 = plt.subplot(4, 3, 12)

# 计算各品类有效成本（总成本-损耗成本）
effective_cost = df.groupby("品类").agg({
    "总成本": "sum",
    "损耗成本": "sum"
})
effective_cost["有效成本"] = effective_cost["总成本"] - effective_cost["损耗成本"]

categories = effective_cost.index.tolist()
x_pos = np.arange(len(categories))
width = 0.35

bars1 = ax12.bar(x_pos - width/2, effective_cost["有效成本"], width, label='有效成本', 
                color='#2E86AB', edgecolor='black', linewidth=1)
bars2 = ax12.bar(x_pos + width/2, effective_cost["损耗成本"], width, label='损耗成本', 
                color='#E63946', edgecolor='black', linewidth=1)

ax12.set_ylabel("成本金额 (元)", fontsize=12)
ax12.set_title("成本结构分析：有效成本 vs 损耗成本\n（成本损耗结构分解）", fontsize=13, fontweight='bold')
ax12.set_xticks(x_pos)
ax12.set_xticklabels(categories)
ax12.legend(loc='upper right', fontsize=10)

# 添加数值标签
for bar in bars1:
    height = bar.get_height()
    ax12.text(bar.get_x() + bar.get_width()/2., height,
             f'¥{height:,.0f}',
             ha='center', va='bottom', fontsize=9)
for bar in bars2:
    height = bar.get_height()
    ax12.text(bar.get_x() + bar.get_width()/2., height,
             f'¥{height:,.0f}',
             ha='center', va='bottom', fontsize=9)

ax12.yaxis.grid(True, linestyle='--', alpha=0.7)
ax12.set_axisbelow(True)

plt.tight_layout(pad=3.0)
plt.savefig("成本与损耗率关联分析可视化方案.png", dpi=150, bbox_inches='tight', facecolor='white')
print("\n可视化图表已保存：成本与损耗率关联分析可视化方案.png")

# ==========================================
# 生成关键洞察摘要
# ==========================================
print("\n" + "=" * 60)
print("关键洞察摘要")
print("=" * 60)

# 成本洞察
total_cost = df["总成本"].sum()
total_waste_cost = df["损耗成本"].sum()
waste_rate_overall = (total_waste_cost / total_cost) * 100

print(f"\n【成本分析】")
print(f"  • 月度总成本：¥{total_cost:,.2f}")
print(f"  • 月度损耗成本：¥{total_waste_cost:,.2f}")
print(f"  • 整体损耗率：{waste_rate_overall:.2f}%")
print(f"  • 最高成本品类：{category_cost.index[0]} (¥{category_cost.iloc[0]:,.2f})")

# 损耗率洞察
high_waste_materials = material_summary[material_summary["损耗率(%)"] > 10].sort_values("损耗率(%)", ascending=False)
print(f"\n【损耗率分析】")
print(f"  • 平均损耗率最高品类：{category_waste.index[0]} ({category_waste.iloc[0]:.2f}%)")
print(f"  • 高损耗原材料数量：{len(high_waste_materials)} 种")
if len(high_waste_materials) > 0:
    print(f"  • 最高损耗原材料：{high_waste_materials.index[0]} ({high_waste_materials.iloc[0]['损耗率(%)']:.2f}%)")

# 损耗原因洞察
print(f"\n【损耗原因分析】")
print(f"  • 最大损耗原因：{reason_cost.index[0]} (¥{reason_cost.iloc[0]:,.2f})")
print(f"  • 损耗原因占比：{(reason_cost.iloc[0]/total_waste_cost)*100:.1f}%")

# 高风险材料
print(f"\n【高风险材料（高成本高损耗）】")
for idx, row in high_risk.head(3).iterrows():
    print(f"  • {idx}: 成本¥{row['总成本']:,.0f}, 损耗率{row['损耗率(%)']:.2f}%, 损耗成本¥{row['损耗成本']:,.0f}")

print("\n" + "=" * 60)
print("分析完成！请查看生成的可视化图表和数据集。")
print("=" * 60)

plt.show()
