{
    TFile *infile = new TFile("performance_without_armcut.root", "r");
    TGraph *tg_ARM_FWHM = (TGraph*)infile->Get("tg_ARM_FWHM");

    TF1 *fit_func = new TF1("fit_func", "[0] + TMath::Log(x) * [1] + TMath::Log(x) ** 2 * [2]", 400, 10000);
    tg_ARM_FWHM->Fit(fit_func, "", "", 400, 10000);
    tg_ARM_FWHM->Fit(fit_func, "", "", 400, 10000);
    tg_ARM_FWHM->Fit(fit_func, "", "", 400, 10000);

    tg_ARM_FWHM->Draw();
    fit_func->Draw("same");
    
    ofstream ofs("fit.dat");
    ofs << "p0,p1,p2" << endl;
    ofs << fit_func->GetParameter(0) << "," << fit_func->GetParameter(1) << "," << fit_func->GetParameter(2) << endl;
}
