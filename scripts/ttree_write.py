import ROOT
import numpy as np

ROOT.gRandom.SetSeed(42)   # 固定种子，保证可复现

with ROOT.TFile("tree_write.root", "RECREATE") as f:
    t = ROOT.TTree("mytree", "Example TTree")

    # 定义变量（用 numpy 数组，支持写入）
    px     = np.zeros(1, dtype=np.float64)
    py     = np.zeros(1, dtype=np.float64)
    pz     = np.zeros(1, dtype=np.float64)
    energy = np.zeros(1, dtype=np.float64)

    # 创建分支，"/D" 表示双精度浮点
    t.Branch("px",     px,     "px/D")
    t.Branch("py",     py,     "py/D")
    t.Branch("pz",     pz,     "pz/D")
    t.Branch("energy", energy, "energy/D")

    # 填充 10000 个事件
    for i in range(10000):
        px[0]     = ROOT.gRandom.Gaus(0, 1)
        py[0]     = ROOT.gRandom.Gaus(0, 1)
        pz[0]     = ROOT.gRandom.Gaus(0, 1)
        energy[0] = ROOT.gRandom.Gaus(5, 0.5)
        t.Fill()          # 把当前变量值写入树

    t.Write()             # 写入文件

print("Generated: tree_write.root")
