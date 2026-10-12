import ROOT
import numpy as np

# 1. 建直方图并填充随机数据
h = ROOT.TH1D("h", "Gaussian Distribution;x;Counts", 100, -5, 5)
h.FillRandom("gaus", 5000)

# 2. 高斯拟合
h.Fit("gaus", "S")

# 3. 从拟合结果里取参数
func = h.GetFunction("gaus")
mean = func.GetParameter(1)
sigma = func.GetParameter(2)
mean_err = func.GetParError(1)
sigma_err = func.GetParError(2)
print(f"Mean  = {mean:.4f} +/- {mean_err:.4f}")
print(f"Sigma = {sigma:.4f} +/- {sigma_err:.4f}")

# 4. 绘图
c = ROOT.TCanvas()
h.Draw()
func.SetLineColor(ROOT.kRed)
func.SetLineWidth(2)
func.Draw("same")

# 5. 保存图片
c.SaveAs("hist_fit.png")

input("按回车退出...")
