import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle, FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 全局样式配置 - 现代化专业风格
# ==========================================

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 自定义颜色方案 - 现代化商务配色
colors_category = {
    "主料": "#2563EB",      # 专业蓝
    "辅料": "#7C3AED",      # 紫罗兰
    "包装材料": "#059669"   # 翠绿
}

colors_waste_reason = {
    "存储不当": "#DC2626",   # 警示红
    "加工工艺": "#F59E0B",   # 琥珀黄
    "运输破损": "#0891B2",   # 青色
    "质量问题": "#4B5563",   # 石墨灰
    "过期报废": "#8B5CF6"    # 紫色
}

# 渐变配色方案
gradient_colors = ["#DBEAFE", "#BFDBFE", "#93C5FD", "#60A5FA", "#3B82F6", "#2563EB"]

# 设置全局样式
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#FAFAFA'
plt.rcParams['axes.edgecolor'] = '#E5E7EB'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['grid.color'] = '#E5E7EB'
plt.rcParams['grid.linewidth'] = 0.8
plt.rcParams['grid.alpha'] = 0.8

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
    for batch in range(1, 4):
        if material["category"] == "主料":
            base_waste_rate = np.random.uniform(2, 8)
        elif material["category"] == "辅料":
            base_waste_rate = np.random.uniform(3, 12)
        else:
            base_waste_rate = np.random.uniform(5, 15)
        
        waste_reason = np.random.choice(waste_reasons, p=list(waste_reason_weights.values()))
        
        if waste_reason == "存储不当":
            waste_rate = base_waste_rate * np.random.uniform(1.0, 1.3)
        elif waste_reason == "加工工艺":
            waste_rate = base_waste_rate * np.random.uniform(0.9, 1.2)
        elif waste_reason == "运输破损":
            waste_rate = base_waste_rate * np.random.uniform(1.1, 1.4)
        elif waste_reason == "质量问题":
            waste_rate = base_waste_rate * np.random.uniform(0.8, 1.1)
        else:
            waste_rate = base_waste_rate * np.random.uniform(0.7, 1.0)
        
        waste_rate = round(waste_rate, 2)
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
df.to_csv("原材料成本损耗数据集.csv", index=False, encoding='utf-8-sig')

print("=" * 60)
print("原材料成本与损耗率关联分析 - 数据集生成完成")
print("=" * 60)
print(f"\n数据集概览：共 {len(df)} 条记录")
print(f"\n数据统计：")
print(df.groupby("品类").agg({
    "原材料名称": "nunique",
    "总成本": "sum",
    "损耗率(%)": "mean",
    "损耗成本": "sum"
}).round(2))

# ==========================================
# 第二步：创建优化后的可视化图表
# ==========================================

fig = plt.figure(figsize=(26, 34))
fig.patch.set_facecolor('white')
fig.suptitle('原材料成本与损耗率关联分析可视化方案', fontsize=24, fontweight='bold', y=0.98, color='#1F2937')

# ==========================================
# 第一维度：成本分布可视化
# ==========================================

# 1.1 品类成本占比 - 圆环图（更现代）
ax1 = plt.subplot(4, 3, 1)
category_cost = df.groupby("品类")["总成本"].sum()
colors_pie = [colors_category[cat] for cat in category_cost.index]

# 创建圆环图
wedges, texts, autotexts = ax1.pie(category_cost.values, labels=None, autopct='',
                                    colors=colors_pie, startangle=90,
                                    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3))

# 中心文字
centre_circle = plt.Circle((0, 0), 0.3, fc='white', linewidth=0)
ax1.add_patch(centre_circle)
ax1.text(0, 0.05, '总成本', ha='center', va='center', fontsize=12, color='#6B7280')
ax1.text(0, -0.1, f'¥{category_cost.sum()/1e6:.2f}M', ha='center', va='center', fontsize=14, fontweight='bold', color='#1F2937')

# 自定义图例
legend_labels = [f"{cat}\n¥{cost/1e6:.2f}M ({cost/category_cost.sum()*100:.1f}%)" for cat, cost in zip(category_cost.index, category_cost.values)]
ax1.legend(wedges, legend_labels, title="品类分布", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), 
          fontsize=10, frameon=False)
ax1.set_title("品类成本占比分布", fontsize=16, fontweight='bold', pad=20, color='#1F2937')

# 1.2 各品类成本柱状图 - 渐变效果
ax2 = plt.subplot(4, 3, 2)
categories = category_cost.index
values = category_cost.values

# 创建渐变柱状图
bars = ax2.bar(categories, values, color=[colors_category[cat] for cat in categories],
               edgecolor='white', linewidth=2, width=0.6)

# 添加圆角效果（通过路径）
for bar in bars:
    bar.set_linewidth(0)
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.02,
             f'¥{height/1e6:.2f}M',
             ha='center', va='bottom', fontsize=12, fontweight='bold', color='#374151')

ax2.set_ylabel("总成本 (元)", fontsize=13, color='#4B5563', fontweight='bold')
ax2.set_title("各品类总成本对比", fontsize=16, fontweight='bold', pad=15, color='#1F2937')
ax2.set_ylim(0, max(values) * 1.15)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#E5E7EB')
ax2.spines['bottom'].set_color('#E5E7EB')
ax2.tick_params(colors='#6B7280', labelsize=11)
ax2.yaxis.grid(True, linestyle='--', alpha=0.5)
ax2.set_axisbelow(True)

# 1.3 单品成本排序TOP15 - 水平柱状图优化
ax3 = plt.subplot(4, 3, 3)
material_cost = df.groupby("原材料名称")["总成本"].first().sort_values(ascending=True).tail(15)
material_category = df.groupby("原材料名称")["品类"].first()

# 创建颜色映射
colors_bar = [colors_category[material_category[name]] for name in material_cost.index]

bars = ax3.barh(range(len(material_cost)), material_cost.values, color=colors_bar, 
                edgecolor='white', linewidth=2, height=0.7)

ax3.set_yticks(range(len(material_cost)))
ax3.set_yticklabels(material_cost.index, fontsize=11, color='#374151')
ax3.set_xlabel("总成本 (元)", fontsize=13, color='#4B5563', fontweight='bold')
ax3.set_title("单品成本排序 TOP15", fontsize=16, fontweight='bold', pad=15, color='#1F2937')

# 添加数值标签
for i, (bar, value) in enumerate(zip(bars, material_cost.values)):
    ax3.text(value + max(material_cost.values)*0.01, bar.get_y() + bar.get_height()/2.,
             f'¥{value/1000:.0f}K',
             ha='left', va='center', fontsize=10, color='#6B7280')

ax3.set_xlim(0, max(material_cost.values) * 1.25)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_color('#E5E7EB')
ax3.spines['bottom'].set_color('#E5E7EB')
ax3.tick_params(colors='#6B7280', labelsize=10)
ax3.xaxis.grid(True, linestyle='--', alpha=0.5)
ax3.set_axisbelow(True)

# ==========================================
# 第二维度：损耗率高低可视化
# ==========================================

# 2.1 各品类平均损耗率对比 - 带标记的柱状图
ax4 = plt.subplot(4, 3, 4)
category_waste = df.groupby("品类")["损耗率(%)"].mean().sort_values(ascending=False)

bars = ax4.bar(category_waste.index, category_waste.values, 
               color=[colors_category[cat] for cat in category_waste.index],
               edgecolor='white', linewidth=2, width=0.6)

# 添加数值标签
for bar, value in zip(bars, category_waste.values):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.2,
             f'{value:.2f}%',
             ha='center', va='bottom', fontsize=12, fontweight='bold', color='#374151')

# 添加警戒线和区域
ax4.axhline(y=8, color='#DC2626', linestyle='--', linewidth=2, alpha=0.7)
ax4.text(2.3, 8.3, '警戒线 8%', fontsize=10, color='#DC2626', fontweight='bold')
ax4.fill_between([-0.5, 2.5], 8, 15, alpha=0.1, color='#DC2626')

ax4.set_ylabel("平均损耗率 (%)", fontsize=13, color='#4B5563', fontweight='bold')
ax4.set_title("各品类平均损耗率对比", fontsize=16, fontweight='bold', pad=15, color='#1F2937')
ax4.set_ylim(0, max(category_waste.values) * 1.3)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.spines['left'].set_color('#E5E7EB')
ax4.spines['bottom'].set_color('#E5E7EB')
ax4.tick_params(colors='#6B7280', labelsize=11)
ax4.yaxis.grid(True, linestyle='--', alpha=0.5)
ax4.set_axisbelow(True)

# 2.2 高损耗率原材料TOP15
ax5 = plt.subplot(4, 3, 5)
material_waste = df.groupby("原材料名称")["损耗率(%)"].mean().sort_values(ascending=True).tail(15)
material_category = df.groupby("原材料名称")["品类"].first()

# 根据损耗率设置颜色深浅
colors_bar = []
for name in material_waste.index:
    base_color = colors_category[material_category[name]]
    colors_bar.append(base_color)

bars = ax5.barh(range(len(material_waste)), material_waste.values, color=colors_bar,
                edgecolor='white', linewidth=2, height=0.7)

ax5.set_yticks(range(len(material_waste)))
ax5.set_yticklabels(material_waste.index, fontsize=11, color='#374151')
ax5.set_xlabel("平均损耗率 (%)", fontsize=13, color='#4B5563', fontweight='bold')
ax5.set_title("高损耗率原材料 TOP15", fontsize=16, fontweight='bold', pad=15, color='#1F2937')

# 添加警戒线和数值标签
ax5.axvline(x=10, color='#DC2626', linestyle='--', linewidth=2, alpha=0.7)
ax5.text(10.2, 14, '高风险线', fontsize=9, color='#DC2626', fontweight='bold')

for i, (bar, value) in enumerate(zip(bars, material_waste.values)):
    color = '#DC2626' if value > 10 else '#6B7280'
    ax5.text(value + 0.3, bar.get_y() + bar.get_height()/2.,
             f'{value:.2f}%',
             ha='left', va='center', fontsize=10, color=color, fontweight='bold' if value > 10 else 'normal')

ax5.set_xlim(0, max(material_waste.values) * 1.2)
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)
ax5.spines['left'].set_color('#E5E7EB')
ax5.spines['bottom'].set_color('#E5E7EB')
ax5.tick_params(colors='#6B7280', labelsize=10)
ax5.xaxis.grid(True, linestyle='--', alpha=0.5)
ax5.set_axisbelow(True)

# 2.3 损耗率分布区间 - 小提琴图（更美观）
ax6 = plt.subplot(4, 3, 6)
categories = ["主料", "辅料", "包装材料"]
violin_data = [df[df["品类"] == cat]["损耗率(%)"].values for cat in categories]

parts = ax6.violinplot(violin_data, positions=range(len(categories)), showmeans=True, showmedians=True)

# 设置小提琴图颜色
for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(colors_category[categories[i]])
    pc.set_alpha(0.6)
    pc.set_edgecolor(colors_category[categories[i]])
    pc.set_linewidth(2)

parts['cmeans'].set_color('#1F2937')
parts['cmeans'].set_linewidth(2)
parts['cmedians'].set_color('#DC2626')
parts['cmedians'].set_linewidth(2)
parts['cbars'].set_color('#6B7280')
parts['cmins'].set_color('#6B7280')
parts['cmaxes'].set_color('#6B7280')

ax6.set_xticks(range(len(categories)))
ax6.set_xticklabels(categories, fontsize=12, color='#374151')
ax6.set_ylabel("损耗率 (%)", fontsize=13, color='#4B5563', fontweight='bold')
ax6.set_title("损耗率分布区间分析", fontsize=16, fontweight='bold', pad=15, color='#1F2937')
ax6.spines['top'].set_visible(False)
ax6.spines['right'].set_visible(False)
ax6.spines['left'].set_color('#E5E7EB')
ax6.spines['bottom'].set_color('#E5E7EB')
ax6.tick_params(colors='#6B7280', labelsize=11)
ax6.yaxis.grid(True, linestyle='--', alpha=0.5)
ax6.set_axisbelow(True)

# ==========================================
# 第三维度：损耗原因对成本的影响可视化
# ==========================================

# 3.1 各损耗原因的成本损耗金额
ax7 = plt.subplot(4, 3, 7)
reason_cost = df.groupby("损耗原因")["损耗成本"].sum().sort_values(ascending=False)
colors_reason = [colors_waste_reason[reason] for reason in reason_cost.index]

bars = ax7.bar(reason_cost.index, reason_cost.values, color=colors_reason,
               edgecolor='white', linewidth=2, width=0.6)

for bar, value in zip(bars, reason_cost.values):
    height = bar.get_height()
    ax7.text(bar.get_x() + bar.get_width()/2., height + max(reason_cost.values)*0.01,
             f'¥{value/1000:.0f}K',
             ha='center', va='bottom', fontsize=11, fontweight='bold', color='#374151')

ax7.set_ylabel("损耗成本金额 (元)", fontsize=13, color='#4B5563', fontweight='bold')
ax7.set_title("各损耗原因对应的成本损耗", fontsize=16, fontweight='bold', pad=15, color='#1F2937')
ax7.set_ylim(0, max(reason_cost.values) * 1.15)
plt.setp(ax7.xaxis.get_majorticklabels(), rotation=20, ha='right', fontsize=11)
ax7.spines['top'].set_visible(False)
ax7.spines['right'].set_visible(False)
ax7.spines['left'].set_color('#E5E7EB')
ax7.spines['bottom'].set_color('#E5E7EB')
ax7.tick_params(colors='#6B7280', labelsize=11)
ax7.yaxis.grid(True, linestyle='--', alpha=0.5)
ax7.set_axisbelow(True)

# 3.2 损耗原因占比 - 树状图风格
ax8 = plt.subplot(4, 3, 8)

# 创建水平树状条形图
y_pos = np.arange(len(reason_cost))
colors_reason = [colors_waste_reason[reason] for reason in reason_cost.index]

bars = ax8.barh(y_pos, reason_cost.values, color=colors_reason,
                edgecolor='white', linewidth=2, height=0.6)

ax8.set_yticks(y_pos)
ax8.set_yticklabels(reason_cost.index, fontsize=12, color='#374151')
ax8.set_xlabel("损耗成本 (元)", fontsize=13, color='#4B5563', fontweight='bold')
ax8.set_title("损耗原因成本占比分布", fontsize=16, fontweight='bold', pad=15, color='#1F2937')

# 添加百分比标签
total = reason_cost.sum()
for i, (bar, value) in enumerate(zip(bars, reason_cost.values)):
    percentage = value / total * 100
    ax8.text(value + max(reason_cost.values)*0.02, bar.get_y() + bar.get_height()/2.,
             f'{percentage:.1f}%',
             ha='left', va='center', fontsize=11, fontweight='bold', color='#374151')

ax8.set_xlim(0, max(reason_cost.values) * 1.3)
ax8.spines['top'].set_visible(False)
ax8.spines['right'].set_visible(False)
ax8.spines['left'].set_color('#E5E7EB')
ax8.spines['bottom'].set_color('#E5E7EB')
ax8.tick_params(colors='#6B7280', labelsize=11)
ax8.xaxis.grid(True, linestyle='--', alpha=0.5)
ax8.set_axisbelow(True)

# 3.3 品类×损耗原因热力图 - 优化配色
ax9 = plt.subplot(4, 3, 9)
heatmap_data = df.pivot_table(values="损耗成本", index="损耗原因", columns="品类", aggfunc="sum")

# 使用更柔和的颜色映射
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='Reds', ax=ax9,
            cbar_kws={'label': '损耗成本 (元)', 'shrink': 0.8},
            linewidths=2, linecolor='white', annot_kws={'size': 11, 'weight': 'bold'})

ax9.set_title("品类×损耗原因 成本损耗热力图", fontsize=16, fontweight='bold', pad=15, color='#1F2937')
ax9.set_xlabel("品类", fontsize=13, color='#4B5563', fontweight='bold')
ax9.set_ylabel("损耗原因", fontsize=13, color='#4B5563', fontweight='bold')
ax9.tick_params(colors='#374151', labelsize=11)

# ==========================================
# 综合分析图表
# ==========================================

# 4.1 成本vs损耗率散点图 - 气泡图
ax10 = plt.subplot(4, 3, 10)
material_summary = df.groupby("原材料名称").agg({
    "总成本": "first",
    "损耗率(%)": "mean",
    "品类": "first",
    "损耗成本": "first"
})

# 根据品类绘制不同颜色和大小的气泡
for category in ["主料", "辅料", "包装材料"]:
    cat_data = material_summary[material_summary["品类"] == category]
    scatter = ax10.scatter(cat_data["总成本"], cat_data["损耗率(%)"],
                          c=colors_category[category], label=category, 
                          s=cat_data["损耗成本"]/500 + 50,  # 气泡大小表示损耗成本
                          alpha=0.7, edgecolors='white', linewidth=1.5)

ax10.set_xlabel("总成本 (元)", fontsize=13, color='#4B5563', fontweight='bold')
ax10.set_ylabel("平均损耗率 (%)", fontsize=13, color='#4B5563', fontweight='bold')
ax10.set_title("成本与损耗率关联分析\n(气泡大小=损耗成本)", fontsize=16, fontweight='bold', pad=15, color='#1F2937')
ax10.legend(title="品类", loc='upper right', fontsize=11, frameon=True, fancybox=True)

# 添加象限分割线
mean_cost = material_summary["总成本"].median()
mean_waste = material_summary["损耗率(%)"].mean()
ax10.axhline(y=mean_waste, color='#9CA3AF', linestyle='--', linewidth=1.5, alpha=0.7)
ax10.axvline(x=mean_cost, color='#9CA3AF', linestyle='--', linewidth=1.5, alpha=0.7)

# 象限标签
ax10.text(max(material_summary["总成本"])*0.95, mean_waste*1.1, '高成本\n高损耗', 
         ha='right', va='bottom', fontsize=10, color='#DC2626', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEE2E2', edgecolor='#DC2626', alpha=0.8))

ax10.spines['top'].set_visible(False)
ax10.spines['right'].set_visible(False)
ax10.spines['left'].set_color('#E5E7EB')
ax10.spines['bottom'].set_color('#E5E7EB')
ax10.tick_params(colors='#6B7280', labelsize=10)
ax10.grid(True, linestyle='--', alpha=0.3)
ax10.set_axisbelow(True)

# 4.2 采购批次损耗率趋势 - 面积图
ax11 = plt.subplot(4, 3, 11)
batch_waste = df.groupby(["采购批次", "品类"])["损耗率(%)"].mean().unstack()

x = range(len(batch_waste.index))
for category in ["主料", "辅料", "包装材料"]:
    if category in batch_waste.columns:
        ax11.fill_between(x, 0, batch_waste[category].values, alpha=0.3, color=colors_category[category])
        ax11.plot(x, batch_waste[category].values, marker='o', linewidth=3,
                 markersize=10, label=category, color=colors_category[category])

ax11.set_xticks(x)
ax11.set_xticklabels(batch_waste.index, fontsize=12, color='#374151')
ax11.set_xlabel("采购批次", fontsize=13, color='#4B5563', fontweight='bold')
ax11.set_ylabel("平均损耗率 (%)", fontsize=13, color='#4B5563', fontweight='bold')
ax11.set_title("采购批次损耗率趋势分析", fontsize=16, fontweight='bold', pad=15, color='#1F2937')
ax11.legend(title="品类", loc='best', fontsize=11, frameon=True, fancybox=True)
ax11.spines['top'].set_visible(False)
ax11.spines['right'].set_visible(False)
ax11.spines['left'].set_color('#E5E7EB')
ax11.spines['bottom'].set_color('#E5E7EB')
ax11.tick_params(colors='#6B7280', labelsize=11)
ax11.yaxis.grid(True, linestyle='--', alpha=0.5)
ax11.set_axisbelow(True)

# 4.3 成本结构分析 - 堆叠柱状图
ax12 = plt.subplot(4, 3, 12)

effective_cost = df.groupby("品类").agg({
    "总成本": "sum",
    "损耗成本": "sum"
})
effective_cost["有效成本"] = effective_cost["总成本"] - effective_cost["损耗成本"]

categories = effective_cost.index.tolist()
x_pos = np.arange(len(categories))
width = 0.5

# 堆叠柱状图
bars1 = ax12.bar(x_pos, effective_cost["有效成本"], width, label='有效成本',
                color='#3B82F6', edgecolor='white', linewidth=2)
bars2 = ax12.bar(x_pos, effective_cost["损耗成本"], width, bottom=effective_cost["有效成本"],
                label='损耗成本', color='#EF4444', edgecolor='white', linewidth=2)

ax12.set_ylabel("成本金额 (元)", fontsize=13, color='#4B5563', fontweight='bold')
ax12.set_title("成本结构分析：有效成本 vs 损耗成本", fontsize=16, fontweight='bold', pad=15, color='#1F2937')
ax12.set_xticks(x_pos)
ax12.set_xticklabels(categories, fontsize=12, color='#374151')
ax12.legend(loc='upper right', fontsize=11, frameon=True, fancybox=True)

# 添加损耗率标注
for i, cat in enumerate(categories):
    total = effective_cost.loc[cat, "总成本"]
    waste = effective_cost.loc[cat, "损耗成本"]
    rate = waste / total * 100
    ax12.text(i, total + max(effective_cost["总成本"])*0.02,
             f'损耗率\n{rate:.1f}%',
             ha='center', va='bottom', fontsize=10, fontweight='bold', color='#DC2626')

ax12.set_ylim(0, max(effective_cost["总成本"]) * 1.15)
ax12.spines['top'].set_visible(False)
ax12.spines['right'].set_visible(False)
ax12.spines['left'].set_color('#E5E7EB')
ax12.spines['bottom'].set_color('#E5E7EB')
ax12.tick_params(colors='#6B7280', labelsize=11)
ax12.yaxis.grid(True, linestyle='--', alpha=0.5)
ax12.set_axisbelow(True)

plt.tight_layout(pad=4.0, rect=[0, 0, 1, 0.97])
plt.savefig("成本与损耗率关联分析可视化方案_v2.png", dpi=150, bbox_inches='tight', facecolor='white')
print("\n优化后的可视化图表已保存：成本与损耗率关联分析可视化方案_v2.png")

# ==========================================
# 生成关键洞察摘要
# ==========================================
print("\n" + "=" * 60)
print("关键洞察摘要")
print("=" * 60)

total_cost = df["总成本"].sum()
total_waste_cost = df["损耗成本"].sum()
waste_rate_overall = (total_waste_cost / total_cost) * 100

print(f"\n【成本分析】")
print(f"  • 月度总成本：¥{total_cost:,.2f}")
print(f"  • 月度损耗成本：¥{total_waste_cost:,.2f}")
print(f"  • 整体损耗率：{waste_rate_overall:.2f}%")
print(f"  • 最高成本品类：{category_cost.index[0]} (¥{category_cost.iloc[0]:,.2f})")

high_waste_materials = material_summary[material_summary["损耗率(%)"] > 10].sort_values("损耗率(%)", ascending=False)
print(f"\n【损耗率分析】")
print(f"  • 平均损耗率最高品类：{category_waste.index[0]} ({category_waste.iloc[0]:.2f}%)")
print(f"  • 高损耗原材料数量：{len(high_waste_materials)} 种")
if len(high_waste_materials) > 0:
    print(f"  • 最高损耗原材料：{high_waste_materials.index[0]} ({high_waste_materials.iloc[0]['损耗率(%)']:.2f}%)")

print(f"\n【损耗原因分析】")
print(f"  • 最大损耗原因：{reason_cost.index[0]} (¥{reason_cost.iloc[0]:,.2f})")
print(f"  • 损耗原因占比：{(reason_cost.iloc[0]/total_waste_cost)*100:.1f}%")

# 高风险材料
high_risk = material_summary[(material_summary["总成本"] > material_summary["总成本"].median()) & 
                             (material_summary["损耗率(%)"] > material_summary["损耗率(%)"].mean())]
print(f"\n【高风险材料（高成本高损耗）】")
for idx, row in high_risk.head(3).iterrows():
    print(f"  • {idx}: 成本¥{row['总成本']:,.0f}, 损耗率{row['损耗率(%)']:.2f}%, 损耗成本¥{row['损耗成本']:,.0f}")

print("\n" + "=" * 60)
print("分析完成！请查看优化后的可视化图表。")
print("=" * 60)

plt.show()
