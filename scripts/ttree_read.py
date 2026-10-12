import ROOT

with ROOT.TFile("tree_write.root", "READ") as f:
    t = f.Get("mytree")
    print(f"Total entries: {t.GetEntries()}")

    # 方法一：Python 迭代（推荐）
    for i, entry in enumerate(t):
        if i < 5:
            print(f"Event {i}: px={entry.px:.3f}, E={entry.energy:.3f}")

    # 方法二：逐条读取（适合随机访问）
    for i in range(5):
        t.GetEntry(i)
        print(f"GetEntry {i}: px={t.px:.3f}, E={t.energy:.3f}")

    # 方法三：快速画图，不遍历
    t.Draw("energy", ""."goff")
