import ROOT

with ROOT.TFile("tree_write.root", "READ") as f:
    t = f.Get("mytree")

    h = ROOT.TH1D("h", "Energy;E (GeV);Events", 100, 3, 7)

    for entry in t:
        h.Fill(entry.energy)

    h.Fit("gaus", "S")
    func = h.GetFunction("gaus")
    print(f"Mean  = {func.GetParameter(1):.4f}")
    print(f"Sigma = {func.GetParameter(2):.4f}")

    c = ROOT.TCanvas("c", "c", 800, 600)
    h.Draw()
    func.SetLineColor(ROOT.kRed)
    func.Draw("same")
    c.SaveAs("energy_dist.png")

input("按回车退出...")
