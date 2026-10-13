import ROOT
import numpy as np
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
fig_dir = os.path.join(script_dir, "..", "figures")
os.makedirs(fig_dir, exist_ok=True)
h = ROOT.TH1D("h", "test", 100, -5, 5)
h.FillRandom("gaus", 5000)

c = ROOT.TCanvas()
h.Draw()
c.Draw()
c.SaveAs(os.path.join(fig_dir, "hist.png"))
input("按回车退出...")
