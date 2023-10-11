TString simfilename = "source.root";
TString cetreefilename = "cetree_source.root";
TString outfilename = "cetree_source_addparam.root";

float cal_distance( float hit1_posx, float hit1_posy, float hit1_posz, 
                    float hit2_posx, float hit2_posy, float hit2_posz ){
   
    TVector3 vec1(hit1_posx, hit1_posy, hit1_posz);
    TVector3 vec2(hit2_posx, hit2_posy, hit2_posz);
    float distance = (vec1 - vec2).Mag();

    return distance;
}

float cal_scattering_direction_angle( float hit1_posx, float hit1_posy, float hit1_posz, 
                                      float hit2_posx, float hit2_posy, float hit2_posz,
                                      TVector3 source_direction){
    TVector3 scattering_direction(hit1_posx - hit2_posx, hit1_posy - hit2_posy, hit1_posz - hit2_posz);
    float scattering_direction_angle = scattering_direction.Angle(source_direction);
    return scattering_direction_angle;
}

bool check_different_segment(TVector3 pos_vec1, TVector3 pos_vec2, float segment_size){
    if( TMath::Floor(pos_vec1.X() / segment_size) == TMath::Floor(pos_vec2.X() / segment_size)
     && TMath::Floor(pos_vec1.Y() / segment_size) == TMath::Floor(pos_vec2.Y() / segment_size) ){
        return false;
    }
    return true;
}

int cal_segment_flag(TTree* hittree, ULong64_t target_eventid, Short_t target_num_hits, Long64_t &start_index){
    Long64_t eventid;
    hittree->SetBranchAddress("eventid", &eventid);
    float posx; float posy; float posz;
    hittree->SetBranchAddress("posx", &posx);
    hittree->SetBranchAddress("posy", &posy);
    hittree->SetBranchAddress("posz", &posz);

    std::vector< TVector3 > vec_pos_vec;
    for(auto i_event = start_index; i_event < hittree->GetEntries(); ++i_event){
        hittree->GetEntry(i_event);
        if(eventid == (Long64_t)target_eventid){
            TVector3 pos_vec(posx, posy, posz);
            vec_pos_vec.push_back(pos_vec);
        }else if(eventid > (Long64_t)target_eventid){
            start_index = i_event;
            break;
        }
    }

    int segment_flag = 0b1111;
    auto num_hits = vec_pos_vec.size();
    
    if(num_hits != target_num_hits){
        std::cout << "!!!" << std::endl;
    }

    for(auto i = 0; i < num_hits - 1; ++i){
        for(auto j = i+1; j < num_hits; ++j){
            float segment_size;

            segment_size = 2.5;
            int param0 = check_different_segment(vec_pos_vec[i], vec_pos_vec[j], segment_size) << 0;

            segment_size = 5.0;
            int param1 = check_different_segment(vec_pos_vec[i], vec_pos_vec[j], segment_size) << 1;

            segment_size = 10.0;
            int param2 = check_different_segment(vec_pos_vec[i], vec_pos_vec[j], segment_size) << 2;

            segment_size = 20.0;
            int param3 = check_different_segment(vec_pos_vec[i], vec_pos_vec[j], segment_size) << 3;

            segment_flag = segment_flag & ( param0 | param1 | param2 | param3);
        }
    }
    
    return segment_flag;
}

void add_param(){
    TVector3 source_direction(0.0, 0.0, 1.0);

    TFile *hittree_file = new TFile(simfilename, "r");
    TTree *hittree = (TTree*)hittree_file->Get("hittree");

    TFile *cetree_file = new TFile(cetreefilename, "r");
    TTree *cetree = (TTree*)cetree_file->Get("cetree");
    
    ULong64_t eventid;
    cetree->SetBranchAddress("eventid", &eventid);
    Short_t num_hits;
    cetree->SetBranchAddress("num_hits", &num_hits);
    float costheta;
    cetree->SetBranchAddress("costheta", &costheta);
    float hit1_posx; float hit1_posy; float hit1_posz;
    cetree->SetBranchAddress("hit1_posx", &hit1_posx);
    cetree->SetBranchAddress("hit1_posy", &hit1_posy);
    cetree->SetBranchAddress("hit1_posz", &hit1_posz);
    float hit2_posx; float hit2_posy; float hit2_posz;
    cetree->SetBranchAddress("hit2_posx", &hit2_posx);
    cetree->SetBranchAddress("hit2_posy", &hit2_posy);
    cetree->SetBranchAddress("hit2_posz", &hit2_posz);
    
    TFile *out_file = new TFile(outfilename, "recreate");
    TTree* cetree_add_param = (TTree*)cetree->CloneTree(0);

    float scattering_angle;
    cetree_add_param->Branch("scattering_angle", &scattering_angle, "scattering_angle/F");
    float scattering_direction_angle;
    cetree_add_param->Branch("scattering_direction_angle", &scattering_direction_angle, "scattering_direction_angle/F");
    float first_interaction_distance;
    cetree_add_param->Branch("first_interaction_distance", &first_interaction_distance, "first_interaction_distance/F");
    int segment_flag;
    cetree_add_param->Branch("segment_flag", &segment_flag, "segment_flag/I");
    
    Long64_t start_index = 0;
    for(auto i_event = 0; i_event < cetree->GetEntries(); ++i_event){
        if(i_event % 10000 == 0) std::cout << i_event << "/" << cetree->GetEntries() << std::endl;
        cetree->GetEntry(i_event);
        
        scattering_angle = TMath::ACos(costheta);
        scattering_direction_angle = cal_scattering_direction_angle( hit1_posx, hit1_posy, hit1_posz, 
                                                                     hit2_posx, hit2_posy, hit2_posz,
                                                                     source_direction );
        first_interaction_distance = cal_distance( hit1_posx, hit1_posy, hit1_posz, 
                                                   hit2_posx, hit2_posy, hit2_posz );
        segment_flag = cal_segment_flag(hittree, eventid, num_hits, start_index); 

        cetree_add_param->Fill();
    }
    
    out_file->cd();
    cetree_add_param->Write();
    out_file->Close();
}
