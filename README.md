# ROOT 与高能物理数据分析基础

基于 CERN ROOT 的高能物理数据分析训练项目。使用 Python（PyROOT）完成随机数据生成、
直方图拟合、TTree 读写、双粒子不变质量重建等内容。所有随机过程使用固定种子，结果可复现。

---

## 项目简介

本项目模拟一个共振态 **J/ψ 介子**（质量约 3.1 GeV）衰变为一对正负 μ 子的过程：

$$
J/\psi \to \mu^+ + \mu^-
$$

通过重建两个 μ 子的不变质量，在直方图上找回 J/ψ 的质量峰，并拟合出探测器分辨率。

项目涵盖：

1. WSL2/Ubuntu 科研环境搭建与 ROOT 安装；
2. 使用 ROOT 产生高斯随机数据并完成直方图与高斯拟合；
3. ROOT 文件、TTree 与 branch 的读写；
4. 编写程序重建两个粒子的不变质量；
5. 代码上传 Git，提供可复现的文档。

---

## 环境要求

| 项目 | 版本 |
|------|------|
| 操作系统 | Ubuntu 26.04（WSL2） |
| ROOT | 6.38.06 |
| Python | 3.10+ |
| numpy | 任意版本 |
| gcc / g++ | 15.2+ |
| Git | 任意版本 |

### ROOT 安装（Ubuntu 26.04）

ROOT 官方提供预编译二进制包，安装步骤：

```bash
# 1. 安装依赖
sudo apt update
sudo apt install -y binutils cmake dpkg-dev g++ gcc libssl-dev git \
  libx11-dev libxext-dev libxft-dev libxpm-dev python3 \
  libtbb-dev libvdt-dev libgif-dev

# 2. 下载并解压
mkdir -p /HEP && cd /HEP
wget https://root.cern/download/root_v6.38.06.Linux-ubuntu26.04-x86_64-gcc15.2.tar.gz
tar xvf root_v6.38.06.Linux-ubuntu26.04-x86_64-gcc15.2.tar.gz
mv root_v6.38.06.Linux-ubuntu26.04-x86_64-gcc15.2 root

# 3. 配置环境变量
echo 'source /HEP/root/bin/thisroot.sh' >> ~/.bashrc
source ~/.bashrc

# 4. 验证
root-config --version      # 应输出 6.38.06
```

### Python 依赖

```bash
sudo apt install -y python3-numpy
```

---

## 运行方式

```bash
# 1. 激活 ROOT 环境
source /HEP/root/bin/thisroot.sh

# 2. 进入脚本目录
cd scripts

# 3. 直方图 + 高斯拟合
python3 test.py
python3 gauss.py

# 4. TTree 写入与读取
python3 ttree_write.py
python3 ttree_read.py

# 5. 不变质量重建
python3 invariant_mass.py
```

---

## 输出说明

| 脚本 | 输出文件 | 含义 |
|------|----------|------|
| test.py | hist.png | 直方图 |
| gauss.py | hist_fit.png | 拟合结果图 |
| ttree_write.py | tree_write.root | 含 10000 个事件的 TTree |
| ttree_read.py | （终端输出） | 读取验证 |
| invariant_mass.py | events.root | 模拟的 J/ψ → μμ 事件 |
| invariant_mass.py | mass_result.root | 不变质量直方图 |
| invariant_mass.py | invariant_mass.png | 不变质量谱 |

---

## 文件结构

```
root-training/
├── README.md
├── .gitignore
├── requirements.txt
├── scripts/
│   ├── test.py		 # 直方图
│   ├── gauss.py         # 高斯拟合
│   ├── ttree_write.py           # 写入 TTree
│   ├── ttree_read.py            # 读取 TTree
│   └── invariant_mass.py        # 不变质量重建
├── figures/
│   ├── hist_fit.png
│   └── invariant_mass.png
└── report/
    └── 学习报告.pdf
```

---

## 物理背景

### 不变质量

两个粒子的不变质量由四动量之和的模给出：

$$
M_{inv} = \sqrt{(E_1 + E_2)^2 - (\vec{p}_1 + \vec{p}_2)^2}
$$

在高能物理中，探测器直接测量的是粒子的横动量 $p_T$、赝快度 $\eta$、方位角 $\phi$
和质量 $m$。用这四个量可以构造四动量：

```python
p = ROOT.TLorentzVector()
p.SetPtEtaPhiM(pt, eta, phi, m)
```

两个四动量相加后取模，即得不变质量：

```python
m_inv = (p1 + p2).M()
```

### 洛伦兹不变量

不变质量是**洛伦兹不变量**：无论母粒子在实验室里如何运动，无论观测者在哪个参考系，
只要正确测量两个子粒子的四动量，重建出的不变质量都等于母粒子的静止质量。

### J/ψ 介子

J/ψ 由粲夸克和反粲夸克组成，质量约 3.097 GeV。1974 年由丁肇中和 Richter 分别发现，
证实了粲夸克的存在，获 1976 年诺贝尔物理学奖。因为其质量在 D 介子对产生阈值以下，
强衰变被禁戒，寿命较长，在不变质量谱上表现为锐利的峰。

### 两体衰变运动学

在共振态静止系中，两个子粒子动量大小相等、方向相反：

$$
p^* = \sqrt{(M/2)^2 - m_\mu^2}
$$

其中 $M$ 为共振态质量，$m_\mu$ 为子粒子质量。随后通过洛伦兹变换（boost）
将系统变换到实验室系，模拟母粒子在探测器中的运动。

---

## 可复现性声明

- 所有随机过程使用固定种子：`ROOT.gRandom.SetSeed(42)`；
- 每次运行产生完全相同的结果；
- 不变质量重建中使用的物理参数：

| 参数 | 值 | 说明 |
|------|-----|------|
| 共振态质量 | 3.1 GeV | J/ψ 质量 |
| μ 子质量 | 0.105 GeV | 粒子质量假设 |
| 探测器分辨率 | 0.05 GeV | 模拟探测误差 |
| 事件数 | 10000 | 统计量 |

---

## 主要结果

运行 `invariant_mass.py` 后，拟合结果：

```
Fitted mass  ≈ 3.1000 GeV    （与 J/ψ 真值 3.1 GeV 一致）
Fitted sigma ≈ 0.05   GeV    （对应探测器分辨率）
```

---

## 致谢

本项目参考 CERN ROOT 官方文档与入门课程：

- ROOT 官网：https://root.cern/
- ROOT 入门课程：https://root.cern/learn/
- ROOT 教程：https://root.cern/tutorials
