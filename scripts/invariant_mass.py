import ROOT
import numpy as np

ROOT.gRandom.SetSeed(42)


def generate_data(filename, n_events=10000, M_resonance=3.1, resolution=0.05):
    """
    模拟共振态衰变，并加入探测器分辨率效应。
    resolution: 不变质量的分辨率（GeV），模拟探测器测量误差。
    """
    f = ROOT.TFile(filename, "RECREATE")
    t = ROOT.TTree("events", "Two-particle events")

    pt1  = np.zeros(1, dtype=np.float64)
    eta1 = np.zeros(1, dtype=np.float64)
    phi1 = np.zeros(1, dtype=np.float64)
    m1   = np.zeros(1, dtype=np.float64)
    pt2  = np.zeros(1, dtype=np.float64)
    eta2 = np.zeros(1, dtype=np.float64)
    phi2 = np.zeros(1, dtype=np.float64)
    m2   = np.zeros(1, dtype=np.float64)

    t.Branch("pt1",  pt1,  "pt1/D")
    t.Branch("eta1", eta1, "eta1/D")
    t.Branch("phi1", phi1, "phi1/D")
    t.Branch("m1",   m1,   "m1/D")
    t.Branch("pt2",  pt2,  "pt2/D")
    t.Branch("eta2", eta2, "eta2/D")
    t.Branch("phi2", phi2, "phi2/D")
    t.Branch("m2",   m2,   "m2/D")

    m_mu = 0.105
    p_star = np.sqrt((M_resonance / 2)**2 - m_mu**2)
    E_star = M_resonance / 2

    for _ in range(n_events):
        cos_theta = 2 * ROOT.gRandom.Rndm() - 1
        sin_theta = np.sqrt(1 - cos_theta**2)
        phi = 2 * np.pi * ROOT.gRandom.Rndm()

        px_star = p_star * sin_theta * np.cos(phi)
        py_star = p_star * sin_theta * np.sin(phi)
        pz_star = p_star * cos_theta

        p1 = ROOT.TLorentzVector(px_star, py_star, pz_star, E_star)
        p2 = ROOT.TLorentzVector(-px_star, -py_star, -pz_star, E_star)

        # 随机 boost 到实验室系
        bx = ROOT.gRandom.Gaus(0, 0.3)
        by = ROOT.gRandom.Gaus(0, 0.3)
        bz = ROOT.gRandom.Gaus(0, 0.3)
        p1.Boost(bx, by, bz)
        p2.Boost(bx, by, bz)

        # --- 模拟探测器分辨率：给动量加上高斯扰动 ---
        smear_scale = resolution / M_resonance  # 相对分辨率
        p1_smeared = ROOT.TLorentzVector(
            p1.Px() * (1 + ROOT.gRandom.Gaus(0, smear_scale)),
            p1.Py() * (1 + ROOT.gRandom.Gaus(0, smear_scale)),
            p1.Pz() * (1 + ROOT.gRandom.Gaus(0, smear_scale)),
            p1.E()  * (1 + ROOT.gRandom.Gaus(0, smear_scale))
        )
        p2_smeared = ROOT.TLorentzVector(
            p2.Px() * (1 + ROOT.gRandom.Gaus(0, smear_scale)),
            p2.Py() * (1 + ROOT.gRandom.Gaus(0, smear_scale)),
            p2.Pz() * (1 + ROOT.gRandom.Gaus(0, smear_scale)),
            p2.E()  * (1 + ROOT.gRandom.Gaus(0, smear_scale))
        )
        # --- 扰动结束 ---

        # 从扰动后的四矢量中提取探测器能测到的量
        pt1[0]  = p1_smeared.Pt()
        eta1[0] = p1_smeared.Eta()
        phi1[0] = p1_smeared.Phi()
        m1[0]   = m_mu

        pt2[0]  = p2_smeared.Pt()
        eta2[0] = p2_smeared.Eta()
        phi2[0] = p2_smeared.Phi()
        m2[0]   = m_mu

        t.Fill()

    t.Write()
    f.Close()
    print(f"Generated {n_events} events -> {filename}")


def reconstruct_invariant_mass(input_file, output_file):
    """从 TTree 读取数据，计算不变质量，填直方图并拟合。"""
    f = ROOT.TFile(input_file, "READ")
    t = f.Get("events")

    if not t:
        print(f"错误：文件 {input_file} 里找不到 events 树")
        f.Close()
        return

    h_mass = ROOT.TH1D("h_mass",
                       "Invariant Mass;M_{inv} (GeV);Events",
                       100, 2.5, 3.7)

    n_entries = t.GetEntries()
    print(f"Reading {n_entries} events...")

    for i in range(n_entries):
        t.GetEntry(i)

        p1 = ROOT.TLorentzVector()
        p2 = ROOT.TLorentzVector()
        p1.SetPtEtaPhiM(t.pt1, t.eta1, t.phi1, t.m1)
        p2.SetPtEtaPhiM(t.pt2, t.eta2, t.phi2, t.m2)

        m_inv = (p1 + p2).M()
        h_mass.Fill(m_inv)

    print(f"h_mass entries = {h_mass.GetEntries()}")
    print(f"h_mass mean    = {h_mass.GetMean():.4f}")
    print(f"h_mass stddev  = {h_mass.GetStdDev():.4f}")

    func = None
    # 只有在直方图有足够数据时才拟合
    if h_mass.GetEntries() > 10 and h_mass.GetStdDev() > 0:
        h_mass.Fit("gaus", "SQ")
        func = h_mass.GetFunction("gaus")

    if func is not None:
        mean  = func.GetParameter(1)
        sigma = func.GetParameter(2)
        print(f"Fitted mass  = {mean:.4f} GeV")
        print(f"Fitted sigma = {sigma:.4f} GeV")
    else:
        print("拟合失败或未返回函数")

    fout = ROOT.TFile(output_file, "RECREATE")
    h_mass.Write()
    fout.Close()

    c = ROOT.TCanvas("c", "Invariant Mass", 800, 600)
    h_mass.Draw()
    if func is not None:
        func.SetLineColor(ROOT.kRed)
        func.SetLineWidth(2)
        func.Draw("same")
    c.SaveAs("invariant_mass.png")
    print("Saved: invariant_mass.png")

    f.Close()


if __name__ == "__main__":
    generate_data("events.root", n_events=10000, M_resonance=3.1, resolution=0.05)
    reconstruct_invariant_mass("events.root", "mass_result.root")
    input("按回车退出...")
