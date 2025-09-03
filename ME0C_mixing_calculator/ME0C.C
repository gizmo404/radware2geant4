//---------------------------------------------------------------------------------------
//
//      ME0C (Mixed E0 calculator)
//      
//      Mixed_E0_calculator is used to generate the conversion coefficients and intensity to be included so to perform the NPTool simulation (example for E2 or M1 + E0 mixing)
//
//      Author: Adrian Montes Plaza (amontesplaza@cns.s.u-tokyo.ac.jp)
//      Comand: $ root "ME0C.C(\"input.txt\")" > output.txt
//
//---------------------------------------------------------------------------------------

#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TLine.h"
#include "TPad.h"
#include "TString.h"
#include "TF1.h"
#include "TLine.h"
#include "TGraphErrors.h"
#include "TSpectrum.h"
#include "TFitResult.h"
#include "TAttLine.h"
#include "TStyle.h"
#include "TPolyMarker.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include <TMath.h>
#include <math.h>
#include <cstring>
#include <cstddef>
#include <string>
#include <stdio.h>
#include <iomanip>
#include <vector>

using namespace std;
bool Debug = true;

string output_name;
string bricc_output[2];

int Z;
int shells[6] = {0}; // Number of shells given Z: K is always there so, #L, #M, #N, #O, #P, #Q (Tot and the ratio are included in all)

double gmma, gamma_intensity, k_icc;
//BrIcc
  string line;
  string S, L, w;
  int e, u;
  bool mixing;
  double d;

double icc_mix[13] = {0};
double icc_E0[4], factor_E0[4];

double tot_icc_mix;

inline bool file_exists(string name) {
  ifstream f(name.c_str());
  bool DidExists = f.good();
  f.close();
  return DidExists;
};

// Function to get the energy of each subshell from BrIcc output - all transitions output
double GetEnergy(ifstream & bricc_file){
  string line;
  double energy = 0.0;
  getline(bricc_file,line);
  getline(bricc_file,line);
  getline(bricc_file,line);
  unsigned int pos = line.find("=");
  energy = stod(line.substr(pos+2,6));
  return energy;
};

// PURE transitions
// Function to get the total ICC of a shell from BrIcc output - pure/mixed transition output
double GetICCtot(ifstream & bricc_file){
  string line;
  double icc = 0.0;
  getline(bricc_file,line);
  getline(bricc_file,line);
  icc = stod(line.substr(3,10));
  getline(bricc_file,line);
  return icc;
};

// Function to get the ICC of a subshell from BrIcc output - pure/mixed transition output
double GetICC(ifstream & bricc_file){
  string line;
  double icc = 0.0;
  getline(bricc_file,line);
  getline(bricc_file,line);
  getline(bricc_file,line);
  icc = stod(line.substr(3,10));
  getline(bricc_file,line);
  return icc;
};

// Function to get the ratio among shells from BrIcc output - pure/mixed transition output
double GetRatio(ifstream & bricc_file){
  string line;
  double ratio = 0.0;
  getline(bricc_file,line);
  getline(bricc_file,line);
  getline(bricc_file,line);
  getline(bricc_file,line);
  ratio = stod(line);
  getline(bricc_file,line);
  return ratio;
};

// Retrieving atomic number Z of elements 
int Reading_Z_from_BrIcc(string _bricc_output){

  string line;
  if(Debug) cout << " Reading the Z from BrIcc Z outputs...";
  if(Debug) cout << endl << " Case: " << _bricc_output << endl;
  ifstream bricc_file (_bricc_output);
  if(bricc_file.is_open()){
    getline(bricc_file,line);
    getline(bricc_file,line);
    unsigned int pos = line.find("z=");
    return stoi(line.substr(pos+3,3));
  }
  cerr << "Unable to open BrIcc output for reading the Z of the nucleus." << endl; 
  return 0;
};

// Number of shells as a function of the atomic number Z
int Z_to_shells(int Z) {
  if(Z < 6) {cerr << "Not supported element!" << endl; return 0;}
  // L2        L
  if(Z <= 6){  shells[0]=2; return 4;}
  // L3
  if(Z <= 10){ shells[0]=3; return 5;}
  // M1                     M
  if(Z <= 12){ shells[0]=3; shells[1]=1; return 7;}
  // M2 
  if(Z <= 14){ shells[0]=3; shells[1]=2; return 8;} 
  // M3
  if(Z <= 18){ shells[0]=3; shells[1]=3; return 9;} 
  // N1                                  N
  if(Z <= 20){ shells[0]=3; shells[1]=3; shells[2]=1; return 11;} 
  // M4
  if(Z <= 23){ shells[0]=3; shells[1]=4; shells[2]=1; return 12;} 
  // M5
  if(Z <= 30){ shells[0]=3; shells[1]=5; shells[2]=1; return 13;}
  // N2          
  if(Z <= 32){ shells[0]=3; shells[1]=5; shells[2]=2; return 14;} 
  // N3
  if(Z <= 36){ shells[0]=3; shells[1]=5; shells[2]=3; return 15;} 
  // O1                                               O
  if(Z <= 38){ shells[0]=3; shells[1]=5; shells[2]=3; shells[3]=1; return 17;} 
  // N4
  if(Z <= 41){ shells[0]=3; shells[1]=5; shells[2]=4; shells[3]=1; return 18;} 
  // N5
  if(Z <= 45){ shells[0]=3; shells[1]=5; shells[2]=5; shells[3]=1; return 19;} 
  // No O1
  if(Z <= 46){ shells[0]=3; shells[1]=5; shells[2]=5; return 17;} 
  // O1 back
  if(Z <= 48){ shells[0]=3; shells[1]=5; shells[2]=5; shells[3]=1; return 19;}
  // O2
  if(Z <= 50){ shells[0]=3; shells[1]=5; shells[2]=5; shells[3]=2; return 20;} 
  // O3
  if(Z <= 54){ shells[0]=3; shells[1]=5; shells[2]=5; shells[3]=3; return 21;} 
  // P1                                                            P
  if(Z <= 56){ shells[0]=3; shells[1]=5; shells[2]=5; shells[3]=3; shells[4]=1; return 23;} 
  // O4
  if(Z <= 57){ shells[0]=3; shells[1]=5; shells[2]=5; shells[3]=4; shells[4]=1; return 24;} 
  // N6
  if(Z <= 59){ shells[0]=3; shells[1]=5; shells[2]=6; shells[3]=4; shells[4]=1; return 25;} 
  // No O4
  if(Z <= 62){ shells[0]=3; shells[1]=5; shells[2]=6; shells[3]=3; shells[4]=1; return 24;} 
  // N7
  if(Z <= 63){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=3; shells[4]=1; return 25;}
  // O4 back
  if(Z <= 64){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=4; shells[4]=1; return 26;} 
  // No O4
  if(Z <= 70){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=3; shells[4]=1; return 25;} 
  // O4 back
  if(Z <= 74){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=4; shells[4]=1; return 26;} 
  // O5
  if(Z <= 80){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=5; shells[4]=1; return 27;} 
  // P2
  if(Z <= 82){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=5; shells[4]=2; return 28;} 
  // P3
  if(Z <= 86){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=5; shells[4]=3; return 29;} 
  // Q1                                                                         Q
  if(Z <= 88){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=5; shells[4]=3; shells[5]=1; return 31;}
  // P4
  if(Z <= 90){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=5; shells[4]=4; shells[5]=1; return 32;} 
  // O6
  if(Z <= 93){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=6; shells[4]=4; shells[5]=1; return 33;} 
  // No P4
  if(Z <= 94){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=6; shells[4]=3; shells[5]=1; return 32;} 
  // O7
  if(Z <= 95){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=7; shells[4]=3; shells[5]=1; return 33;} 
  // P4 back
  if(Z <= 97){ shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=7; shells[4]=4; shells[5]=1; return 34;} 
  // No P4
  if(Z <= 102){shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=7; shells[4]=3; shells[5]=1; return 33;}
  // P4 back
  if(Z <= 106){shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=7; shells[4]=4; shells[5]=1; return 34;} 
  // P5
  if(Z <= 110){shells[0]=3; shells[1]=5; shells[2]=7; shells[3]=7; shells[4]=5; shells[5]=1; return 35;}
  cerr << " Not supported element!" << endl; return 0;
};

bool ReadInputFile(string input_name){ 

  if (Debug) cout << "Extracting the data from the input file...";
  ifstream input_file (input_name.c_str());
  if(input_file.is_open()){

    for(int i=0; i<4; i++) getline(input_file,line);
    input_file >> S >> gmma >> e >> L >> w >> mixing >> d >> u >> gamma_intensity >> k_icc;
    if (Debug) cout << endl << S << "   " << gmma << "   " << e << "   " << L << "   " << w << "   " << mixing << "   " << d << "   " << u << "   " << gamma_intensity << "   " << k_icc << endl;
    input_file.close();

  } else{
      cerr << endl << "Unable to open the input file" << endl;
      return false;
    }
  
  if (Debug) cout << " ...Finished!!" << endl << endl;
  return true;
};

string briccs_exe(string bricc_output){
  
  // BrIcc error: arguments can't be longer than 8 char.
  ostringstream prec3_g, prec3_d;
  prec3_g << setprecision(8) << gmma;
  prec3_d << setprecision(8) << d;

  string bricc_command;
  string output_folder = "briccs_outputs";
  string mkdir_command = "mkdir -p " + output_folder;

  bricc_command = "briccs";
  bricc_command += " -S " + S;
  bricc_command += " -g " + prec3_g.str();
  bricc_command += " -e " + to_string(e);
  bricc_command += " -L " + L;
  //bricc_command += " -d " + prec3_d.str();
  //bricc_command += " -u " + to_string(u);
  bricc_command += " -a -w " + w;
      
  bricc_output = output_folder + "/briccs_out_" + S + "_g_" + prec3_g.str() + "_" + L + ".txt";
  bricc_command += " > " + bricc_output;
      
  if (Debug) cout << "Running briccs!" << endl;
  system(mkdir_command.c_str());
  system(bricc_command.c_str());
  if (Debug) cout << "-> " << bricc_command << endl;
  return bricc_output;
};

void ReadingBrIccsOutput(string bricc_output){
  
  int index = 0; // It counts regardless the filled shells
  double holder;
  int subshells[6] = {3, 5, 7, 7, 5, 1};
  if(Debug) cout << "Reading the BrIcc_mix output..." << endl << "Case: " << bricc_output << endl;

  ifstream bricc_file (bricc_output);
  if(bricc_file.is_open()){
    while(getline(bricc_file,line)) {
      if(line == "    Shell=\"Tot\""){
        tot_icc_mix  = GetICCtot(bricc_file);
        holder       = GetEnergy(bricc_file);
        icc_mix[0]   = GetICC(bricc_file); // K
        index ++;
        // L, M, N, O, P, Q (index K)
        for(int k=0; k<2; k++){
          if(shells[k] != 0){
            for(int j=0; j<shells[k]; j++){
              holder            = GetEnergy(bricc_file);
              icc_mix[index]  = GetICC(bricc_file);
              index ++;
            }
            holder = GetEnergy(bricc_file);
            holder = GetICC(bricc_file);
            holder = GetRatio(bricc_file);
          }else index += subshells[k];
        }
        if(shells[2] != 0) while(getline(bricc_file,line)){
          if(line == "    Shell=\"N-tot\""){           
            getline(bricc_file,line);
            getline(bricc_file,line);
            getline(bricc_file,line);
            getline(bricc_file,line);
            icc_mix[9] = stod(line.substr(3,10));
            break;
          }
        }
        if(shells[3] != 0) while(getline(bricc_file,line)){
          if(line == "    Shell=\"O-tot\""){           
            getline(bricc_file,line);
            getline(bricc_file,line);
            getline(bricc_file,line);
            getline(bricc_file,line);
            icc_mix[10] = stod(line.substr(3,10));
            break;
          }
        }
        if(shells[4] != 0) while(getline(bricc_file,line)){
          if(line == "    Shell=\"P-tot\""){           
            getline(bricc_file,line);
            getline(bricc_file,line);
            getline(bricc_file,line);
            getline(bricc_file,line);
            icc_mix[11] = stod(line.substr(3,10));
            break;
          }
        }
        if(shells[5] != 0) while(getline(bricc_file,line)){
          if(line == "    Shell=\"Q-tot\""){           
            getline(bricc_file,line);
            getline(bricc_file,line);
            getline(bricc_file,line);
            getline(bricc_file,line);
            icc_mix[12] = stod(line.substr(3,10));
            break;
          }
        }
      
        //Summary
        if (Debug){
          cout << endl << endl << "ICCs_mix: " << endl;
          for(int i=0; i<13; i++) cout << icc_mix[i] << "  \t";
          cout << endl;
        }

      } // shell
    } //getline
    bricc_file.close();
  
  }else cout << endl << "Unable to open " + bricc_output << endl;

  if(Debug) cout << " ...Finished!!" << endl << endl;
  return;
};

void ReadingBrIccsOutput_E0(string bricc_output){
  
  if(Debug) cout << "Reading the BrIcc_E0 output..." << endl << "Case: " << bricc_output << endl;
  ifstream bricc_file (bricc_output);
  if(bricc_file.is_open()){
    while(getline(bricc_file,line)) {
      if(line == "    Shell=\"K\">"){
        for(int i=0; i<3; i++) getline(bricc_file,line);
        factor_E0[0] = stod(line.substr(3,15)); //K
        for(int i=0; i<6; i++) getline(bricc_file,line);
        factor_E0[1] = stod(line.substr(3,15)); //L1
        for(int i=0; i<6; i++) getline(bricc_file,line);
        factor_E0[2] = stod(line.substr(3,15)); //L2
        for(int i=0; i<4; i++) getline(bricc_file,line);

        factor_E0[3] = factor_E0[1] /3;         //M1
        
            // Summary:
            if (Debug){
              cout << endl << endl << "Electronic factors: " << endl;
              for(int i=0; i<4; i++) cout << factor_E0[i] << "  \t";
              cout << endl;
            }

        double tot_factor_E0 = 0;
        for(int i=0; i<4; i++) tot_factor_E0 += factor_E0[i];

        for(int i=0; i<4; i++) icc_E0[i] = factor_E0[i] / tot_factor_E0;

            //Summary
            if (Debug){
              cout << endl << endl << "ICCs_E0: " << endl;
              for(int i=0; i<4; i++) cout << icc_E0[i] << "  \t";
              cout << endl;
            }
      } // shell
    } //getline
    bricc_file.close();

  }else cout << endl << "Unable to open " + bricc_output << endl;

  if(Debug) cout << " ...Finished!!" << endl << endl;
  return;
};











void ME0C(string input_name){ //Main function
  
  // Header
  cout << endl;
  cout << "           ME0C Program" << endl;
  cout << "      (Mixed E0 calculator)" << endl;
  cout << "     (by Adrian Montes Plaza)" << endl << endl;
  cout << "Insert input file: ";
  //cin >> input_name;
  //input_name = "2+_2+_190Pb.txt";
  //input_name = "4+_4+_190Pb.txt";
  cout << input_name << endl << endl;
  
  // Checking input file
  if (!file_exists(input_name))
    return;
    
  // Sanity test!
  // Checking whether the briccs code is installed or not
  int ret = system("which briccs >/dev/null 2>&1");
  bool isInstalled = ret;
  if (isInstalled) {
    cerr << endl << " -> briccs is not installed!!" << endl;
    cerr << "    More info here:    https://bricc.anu.edu.au/download.php" << endl << endl;
    return;
  }
  
  // Reading the Input file and extracting all the information
  if (!ReadInputFile(input_name.c_str())){
    cerr << endl << " Please review the input file!" << endl << endl;
    return;
  }
 
// 
  // Running BrIccs
  string L_mix = L;
  bricc_output[0] = briccs_exe(bricc_output[0]);
  L = "E0";
  bricc_output[1] = briccs_exe(bricc_output[1]);

  Z = Reading_Z_from_BrIcc(bricc_output[0]);

  // Definition of number of shells for the given nucleus
  Z_to_shells(Z);

  if(Debug){
    cout << " Number of shells" << endl;
    cout << "\t\tK\tL\tM\tN\tO\tP\tQ" << endl;
    cout << " " << to_string(gmma) << " keV: \t";
    cout << "1 \t";
    for(int j=0; j<6; j++) cout << shells[j] << " \t";
    cout << endl;
    cout << endl;
  }

  if(Debug) cout << endl << bricc_output[0] << endl << bricc_output[1] << endl << endl << endl << endl;
  // READING the bricc_ouput FILES for ICCs
  ReadingBrIccsOutput(bricc_output[0]);
  ReadingBrIccsOutput_E0(bricc_output[1]);
  if(Debug) cout << endl << endl << endl;

  // CALCULATOR
  cout << "Transition energy: " << gmma << " keV" << endl << endl;
  cout << "BrIccs INPUT: "<< endl << endl;

  cout << L_mix << "-component ICCs:"  << endl;
  cout << "Total = " << tot_icc_mix << endl;
  int counter_icc =0;
  cout << "K  = " << icc_mix[0] << endl;
  counter_icc ++;
  if(shells[0] != 0){
    for(int i=0; i<shells[0]; i++) cout << "L" << to_string(i+counter_icc) + " = " << icc_mix[i+counter_icc] << " \t";
    cout << endl;
    counter_icc += shells[0];
  }
  if(shells[1] != 0){
    for(int i=0; i<shells[1]; i++) cout << "M" << to_string(i+1) + " = " << icc_mix[i+counter_icc] << " \t";
    cout << endl;
    counter_icc += shells[1];
  }
  if(shells[2] != 0) cout << "N  = " << icc_mix[9] << " \t";
  if(shells[3] != 0) cout << "O  = " << icc_mix[10] << "\t";
  if(shells[4] != 0) cout << "P  = " << icc_mix[11] << endl;

  cout << L << "-component normalised fractional shell emission (Sum = 1):"  << endl;
  cout << "K     = " << icc_E0[0] << endl;
  cout << "L1    = " << icc_E0[1] << " \t" << "L2 = " << icc_E0[2] << endl;
  cout << "M1    = " << icc_E0[3] << endl << endl;

  cout << endl << endl << "RESULTS: " << endl << endl;
  cout << "Input -> Experimental K-ICC (" << L_mix << "+" << L << ") = \t" << k_icc << endl;
  cout << "Input -> Gamma intensity = \t\t" << gamma_intensity << endl;
  
  double E2_intensity = gamma_intensity* (1 + tot_icc_mix);
  double E0_intensity = gamma_intensity* (k_icc - icc_mix[0])/icc_E0[0];
  double electron_intensity = (gamma_intensity * tot_icc_mix) + E0_intensity;
  double total_intensity = gamma_intensity + electron_intensity;
  double total_conversion_coefficient = electron_intensity / gamma_intensity;

  cout << "E2 intensity = \t\t\t\t" << E2_intensity << endl;
  cout << "E0 intensity = \t\t\t\t" << E0_intensity << endl;
  cout << "Electron intensity = \t\t\t" << electron_intensity << endl;
  cout << "Total intensity = \t\t\t" << total_intensity << endl;
  cout << "Total ICC = \t\t\t\t" << total_conversion_coefficient << endl << endl;
  
  double intensity_e_E2[13];
  for(int i=0; i<13; i++) intensity_e_E2[i] = gamma_intensity * icc_mix[i];

  double intensity_e_E0[13] = {0};
  intensity_e_E0[0] = E0_intensity * icc_E0[0]; // K
  intensity_e_E0[1] = E0_intensity * icc_E0[1]; // L1
  intensity_e_E0[2] = E0_intensity * icc_E0[2]; // L2
  intensity_e_E0[4] = E0_intensity * icc_E0[3]; // M1

  double intensity_e[13];
  for(int i=0; i<13; i++) intensity_e[i] = intensity_e_E2[i] + intensity_e_E0[i];

  double frac_icc[10];
  for(int i=0; i<9; i++) frac_icc[i] = intensity_e[i] / electron_intensity;
  frac_icc[9] = (intensity_e[9] + intensity_e[10] + intensity_e[11] + intensity_e[12]) / electron_intensity;

  cout << "Line to be included in the file user_zXX.aYY for NPTool (Geant4): " << endl;
  cout << "(Total conversion coefficient and fractional ICCs)" << endl;
  cout << "ICC \t\tK \t\tL1 \t\tL2 \t\tL3 \t\tM1 \t\tM2 \t\tM3 \t\tM4 \t\tM5 \t\tOUTER" << endl << endl;
  cout << total_conversion_coefficient << "\t";
  for(int i=0; i<10; i++) cout << frac_icc[i] << "\t";
  cout << endl << endl;

  return;
}
