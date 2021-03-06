// Class: ReadCutsD
// Automatically generated by MethodBase::MakeClass
//

/* configuration options =====================================================

#GEN -*-*-*-*-*-*-*-*-*-*-*- general info -*-*-*-*-*-*-*-*-*-*-*-

Method         : Cuts::CutsD
TMVA Release   : 4.1.4         [262404]
ROOT Release   : 5.34/05       [336389]
Creator        : jbochenek
Date           : Mon Apr 15 11:17:54 2013
Host           : Linux ubuntu 3.2.0-39-generic #62-Ubuntu SMP Wed Feb 27 22:05:17 UTC 2013 i686 i686 i386 GNU/Linux
Dir            : /mnt/hgfs/work/HZZ4l_2013/scripts
Training events: 10000
Analysis type  : [Classification]


#OPT -*-*-*-*-*-*-*-*-*-*-*-*- options -*-*-*-*-*-*-*-*-*-*-*-*-

# Set by User:
V: "False" [Verbose output (short form of "VerbosityLevel" below - overrides the latter one)]
VarTransform: "Decorrelate" [List of variable transformations performed before training, e.g., "D_Background,P_Signal,G,N_AllClasses" for: "Decorrelation, PCA-transformation, Gaussianisation, Normalisation, each for the given class of events ('AllClasses' denotes all events of all classes, if no class indication is given, 'All' is assumed)"]
H: "False" [Print method-specific help message]
FitMethod: "MC" [Minimisation Method (GA, SA, and MC are the primary methods to be used; the others have been introduced for testing purposes and are depreciated)]
EffMethod: "EffSel" [Selection Method]
# Default:
VerbosityLevel: "Default" [Verbosity level]
CreateMVAPdfs: "False" [Create PDFs for classifier outputs (signal and background)]
IgnoreNegWeightsInTraining: "False" [Events with negative weights are ignored in the training (but are included for testing and performance evaluation)]
CutRangeMin[0]: "-1.000000e+00" [Minimum of allowed cut range (set per variable)]
    CutRangeMin[1]: "-1.000000e+00"
    CutRangeMin[2]: "-1.000000e+00"
    CutRangeMin[3]: "-1.000000e+00"
    CutRangeMin[4]: "-1.000000e+00"
    CutRangeMin[5]: "-1.000000e+00"
    CutRangeMin[6]: "-1.000000e+00"
CutRangeMax[0]: "-1.000000e+00" [Maximum of allowed cut range (set per variable)]
    CutRangeMax[1]: "-1.000000e+00"
    CutRangeMax[2]: "-1.000000e+00"
    CutRangeMax[3]: "-1.000000e+00"
    CutRangeMax[4]: "-1.000000e+00"
    CutRangeMax[5]: "-1.000000e+00"
    CutRangeMax[6]: "-1.000000e+00"
VarProp[0]: "FSmart" [Categorisation of cuts]
    VarProp[1]: "FSmart"
    VarProp[2]: "FSmart"
    VarProp[3]: "FSmart"
    VarProp[4]: "FSmart"
    VarProp[5]: "FSmart"
    VarProp[6]: "FSmart"
##


#VAR -*-*-*-*-*-*-*-*-*-*-*-* variables *-*-*-*-*-*-*-*-*-*-*-*-

NVar 7
f_angle_costhetastar          f_angle_costhetastar          f_angle_costhetastar          f_angle_costhetastar                                            'F'    [-99,0.999695241451]
f_angle_costheta1             f_angle_costheta1             f_angle_costheta1             f_angle_costheta1                                               'F'    [-99,0.999956786633]
f_angle_costheta2             f_angle_costheta2             f_angle_costheta2             f_angle_costheta2                                               'F'    [-99,0.999614596367]
f_angle_phi                   f_angle_phi                   f_angle_phi                   f_angle_phi                                                     'F'    [-99,3.1414334774]
f_angle_phistar1              f_angle_phistar1              f_angle_phistar1              f_angle_phistar1                                                'F'    [-99,3.14026069641]
f_Z1mass                      f_Z1mass                      f_Z1mass                      f_Z1mass                                                        'F'    [40.3993835449,117.858093262]
f_Z2mass                      f_Z2mass                      f_Z2mass                      f_Z2mass                                                        'F'    [12.0253534317,114.000205994]
NSpec 0


============================================================================ */

#include <vector>
#include <cmath>
#include <string>
#include <iostream>

#ifndef IClassifierReader__def
#define IClassifierReader__def

class IClassifierReader {

 public:

   // constructor
   IClassifierReader() : fStatusIsClean( true ) {}
   virtual ~IClassifierReader() {}

   // return classifier response
   virtual double GetMvaValue( const std::vector<double>& inputValues ) const = 0;

   // returns classifier status
   bool IsStatusClean() const { return fStatusIsClean; }

 protected:

   bool fStatusIsClean;
};

#endif

class ReadCutsD : public IClassifierReader {

 public:

   // constructor
   ReadCutsD( std::vector<std::string>& theInputVars ) 
      : IClassifierReader(),
        fClassName( "ReadCutsD" ),
        fNvars( 7 ),
        fIsNormalised( false )
   {      
      // the training input variables
      const char* inputVars[] = { "f_angle_costhetastar", "f_angle_costheta1", "f_angle_costheta2", "f_angle_phi", "f_angle_phistar1", "f_Z1mass", "f_Z2mass" };

      // sanity checks
      if (theInputVars.size() <= 0) {
         std::cout << "Problem in class \"" << fClassName << "\": empty input vector" << std::endl;
         fStatusIsClean = false;
      }

      if (theInputVars.size() != fNvars) {
         std::cout << "Problem in class \"" << fClassName << "\": mismatch in number of input values: "
                   << theInputVars.size() << " != " << fNvars << std::endl;
         fStatusIsClean = false;
      }

      // validate input variables
      for (size_t ivar = 0; ivar < theInputVars.size(); ivar++) {
         if (theInputVars[ivar] != inputVars[ivar]) {
            std::cout << "Problem in class \"" << fClassName << "\": mismatch in input variable names" << std::endl
                      << " for variable [" << ivar << "]: " << theInputVars[ivar].c_str() << " != " << inputVars[ivar] << std::endl;
            fStatusIsClean = false;
         }
      }

      // initialize min and max vectors (for normalisation)
      fVmin[0] = -6.06122446060181;
      fVmax[0] = 2.32528018951416;
      fVmin[1] = -6.26787805557251;
      fVmax[1] = 1.92864608764648;
      fVmin[2] = -6.26516056060791;
      fVmax[2] = 2.09687876701355;
      fVmin[3] = -5.61559534072876;
      fVmax[3] = 1.36879086494446;
      fVmin[4] = -5.50871753692627;
      fVmax[4] = 1.52690136432648;
      fVmin[5] = 5.09922313690186;
      fVmax[5] = 13.9291725158691;
      fVmin[6] = 0.842832744121552;
      fVmax[6] = 6.90109777450562;

      // initialize input variable types
      fType[0] = 'F';
      fType[1] = 'F';
      fType[2] = 'F';
      fType[3] = 'F';
      fType[4] = 'F';
      fType[5] = 'F';
      fType[6] = 'F';

      // initialize constants
      Initialize();

      // initialize transformation
      InitTransform();
   }

   // destructor
   virtual ~ReadCutsD() {
      Clear(); // method-specific
   }

   // the classifier response
   // "inputValues" is a vector of input values in the same order as the 
   // variables given to the constructor
   double GetMvaValue( const std::vector<double>& inputValues ) const;

 private:

   // method-specific destructor
   void Clear();

   // input variable transformation

   double fDecTF_1[3][7][7];
   void InitTransform_1();
   void Transform_1( std::vector<double> & iv, int sigOrBgd ) const;
   void InitTransform();
   void Transform( std::vector<double> & iv, int sigOrBgd ) const;

   // common member variables
   const char* fClassName;

   const size_t fNvars;
   size_t GetNvar()           const { return fNvars; }
   char   GetType( int ivar ) const { return fType[ivar]; }

   // normalisation of input variables
   const bool fIsNormalised;
   bool IsNormalised() const { return fIsNormalised; }
   double fVmin[7];
   double fVmax[7];
   double NormVariable( double x, double xmin, double xmax ) const {
      // normalise to output range: [-1, 1]
      return 2*(x - xmin)/(xmax - xmin) - 1.0;
   }

   // type of input variable: 'F' or 'I'
   char   fType[7];

   // initialize internal variables
   void Initialize();
   double GetMvaValue__( const std::vector<double>& inputValues ) const;

   // private members (method specific)
   // not implemented for class: "ReadCutsD"
};
   inline double ReadCutsD::GetMvaValue( const std::vector<double>& inputValues ) const
   {
      // classifier response value
      double retval = 0;

      // classifier response, sanity check first
      if (!IsStatusClean()) {
         std::cout << "Problem in class \"" << fClassName << "\": cannot return classifier response"
                   << " because status is dirty" << std::endl;
         retval = 0;
      }
      else {
         if (IsNormalised()) {
            // normalise variables
            std::vector<double> iV;
            int ivar = 0;
            for (std::vector<double>::const_iterator varIt = inputValues.begin();
                 varIt != inputValues.end(); varIt++, ivar++) {
               iV.push_back(NormVariable( *varIt, fVmin[ivar], fVmax[ivar] ));
            }
            Transform( iV, -1 );
            retval = GetMvaValue__( iV );
         }
         else {
            std::vector<double> iV;
            int ivar = 0;
            for (std::vector<double>::const_iterator varIt = inputValues.begin();
                 varIt != inputValues.end(); varIt++, ivar++) {
               iV.push_back(*varIt);
            }
            Transform( iV, -1 );
            retval = GetMvaValue__( iV );
         }
      }

      return retval;
   }

//_______________________________________________________________________
inline void ReadCutsD::InitTransform_1()
{
   // Decorrelation transformation, initialisation
   fDecTF_1[0][0][0] = 1.30423683616;
   fDecTF_1[0][0][1] = -0.478252429541;
   fDecTF_1[0][0][2] = -0.513051204126;
   fDecTF_1[0][0][3] = -0.112732192545;
   fDecTF_1[0][0][4] = -0.131446643973;
   fDecTF_1[0][0][5] = -0.00641220858768;
   fDecTF_1[0][0][6] = -0.00217275284613;
   fDecTF_1[0][1][0] = -0.478252429541;
   fDecTF_1[0][1][1] = 1.38916758738;
   fDecTF_1[0][1][2] = -0.581471489524;
   fDecTF_1[0][1][3] = -0.138031238209;
   fDecTF_1[0][1][4] = -0.122766655395;
   fDecTF_1[0][1][5] = -0.00612158102522;
   fDecTF_1[0][1][6] = -5.05738287474e-05;
   fDecTF_1[0][2][0] = -0.513051204126;
   fDecTF_1[0][2][1] = -0.581471489524;
   fDecTF_1[0][2][2] = 1.42456511272;
   fDecTF_1[0][2][3] = -0.129400901549;
   fDecTF_1[0][2][4] = -0.131518737336;
   fDecTF_1[0][2][5] = -0.00664939244994;
   fDecTF_1[0][2][6] = 3.1546215733e-05;
   fDecTF_1[0][3][0] = -0.112732192545;
   fDecTF_1[0][3][1] = -0.138031238209;
   fDecTF_1[0][3][2] = -0.129400901549;
   fDecTF_1[0][3][3] = 0.492364475203;
   fDecTF_1[0][3][4] = -0.0523442271708;
   fDecTF_1[0][3][5] = -0.00289752001724;
   fDecTF_1[0][3][6] = -0.00106514564261;
   fDecTF_1[0][4][0] = -0.131446643973;
   fDecTF_1[0][4][1] = -0.122766655395;
   fDecTF_1[0][4][2] = -0.131518737336;
   fDecTF_1[0][4][3] = -0.0523442271708;
   fDecTF_1[0][4][4] = 0.499041913825;
   fDecTF_1[0][4][5] = -0.00460590956939;
   fDecTF_1[0][4][6] = -0.000241966438421;
   fDecTF_1[0][5][0] = -0.00641220858768;
   fDecTF_1[0][5][1] = -0.00612158102522;
   fDecTF_1[0][5][2] = -0.00664939244994;
   fDecTF_1[0][5][3] = -0.00289752001724;
   fDecTF_1[0][5][4] = -0.00460590956939;
   fDecTF_1[0][5][5] = 0.120090305679;
   fDecTF_1[0][5][6] = -0.00150434688918;
   fDecTF_1[0][6][0] = -0.00217275284613;
   fDecTF_1[0][6][1] = -5.05738287474e-05;
   fDecTF_1[0][6][2] = 3.1546215733e-05;
   fDecTF_1[0][6][3] = -0.00106514564261;
   fDecTF_1[0][6][4] = -0.000241966438421;
   fDecTF_1[0][6][5] = -0.00150434688918;
   fDecTF_1[0][6][6] = 0.0523810611057;
   fDecTF_1[1][0][0] = 1.3122649842;
   fDecTF_1[1][0][1] = -0.50002561548;
   fDecTF_1[1][0][2] = -0.519699242694;
   fDecTF_1[1][0][3] = -0.117644140256;
   fDecTF_1[1][0][4] = -0.121987490547;
   fDecTF_1[1][0][5] = -0.00418862828514;
   fDecTF_1[1][0][6] = -0.000521333639957;
   fDecTF_1[1][1][0] = -0.50002561548;
   fDecTF_1[1][1][1] = 1.40979087364;
   fDecTF_1[1][1][2] = -0.592086127165;
   fDecTF_1[1][1][3] = -0.130400730779;
   fDecTF_1[1][1][4] = -0.132539110297;
   fDecTF_1[1][1][5] = -0.00699692952164;
   fDecTF_1[1][1][6] = -0.00208218508001;
   fDecTF_1[1][2][0] = -0.519699242694;
   fDecTF_1[1][2][1] = -0.592086127165;
   fDecTF_1[1][2][2] = 1.42557270868;
   fDecTF_1[1][2][3] = -0.128235434787;
   fDecTF_1[1][2][4] = -0.130840041025;
   fDecTF_1[1][2][5] = -0.00633097448851;
   fDecTF_1[1][2][6] = -0.00151127577745;
   fDecTF_1[1][3][0] = -0.117644140256;
   fDecTF_1[1][3][1] = -0.130400730779;
   fDecTF_1[1][3][2] = -0.128235434787;
   fDecTF_1[1][3][3] = 0.487471535831;
   fDecTF_1[1][3][4] = -0.0615424513596;
   fDecTF_1[1][3][5] = -0.00749743611859;
   fDecTF_1[1][3][6] = -0.00208665315663;
   fDecTF_1[1][4][0] = -0.121987490547;
   fDecTF_1[1][4][1] = -0.132539110297;
   fDecTF_1[1][4][2] = -0.130840041025;
   fDecTF_1[1][4][3] = -0.0615424513596;
   fDecTF_1[1][4][4] = 0.495597451837;
   fDecTF_1[1][4][5] = -0.00587594715119;
   fDecTF_1[1][4][6] = -0.000346564435978;
   fDecTF_1[1][5][0] = -0.00418862828514;
   fDecTF_1[1][5][1] = -0.00699692952164;
   fDecTF_1[1][5][2] = -0.00633097448851;
   fDecTF_1[1][5][3] = -0.00749743611859;
   fDecTF_1[1][5][4] = -0.00587594715119;
   fDecTF_1[1][5][5] = 0.117435201827;
   fDecTF_1[1][5][6] = 0.00466468006409;
   fDecTF_1[1][6][0] = -0.000521333639957;
   fDecTF_1[1][6][1] = -0.00208218508001;
   fDecTF_1[1][6][2] = -0.00151127577745;
   fDecTF_1[1][6][3] = -0.00208665315663;
   fDecTF_1[1][6][4] = -0.000346564435978;
   fDecTF_1[1][6][5] = 0.00466468006409;
   fDecTF_1[1][6][6] = 0.0661064114772;
   fDecTF_1[2][0][0] = 1.30850242302;
   fDecTF_1[2][0][1] = -0.492138454792;
   fDecTF_1[2][0][2] = -0.517455625723;
   fDecTF_1[2][0][3] = -0.115926039843;
   fDecTF_1[2][0][4] = -0.125624987575;
   fDecTF_1[2][0][5] = -0.00513465876546;
   fDecTF_1[2][0][6] = -0.00131248335458;
   fDecTF_1[2][1][0] = -0.492138454792;
   fDecTF_1[2][1][1] = 1.40169696185;
   fDecTF_1[2][1][2] = -0.588926705706;
   fDecTF_1[2][1][3] = -0.133280772265;
   fDecTF_1[2][1][4] = -0.128957198135;
   fDecTF_1[2][1][5] = -0.00667566806836;
   fDecTF_1[2][1][6] = -0.00132433921759;
   fDecTF_1[2][2][0] = -0.517455625723;
   fDecTF_1[2][2][1] = -0.588926705706;
   fDecTF_1[2][2][2] = 1.42459794959;
   fDecTF_1[2][2][3] = -0.128712912183;
   fDecTF_1[2][2][4] = -0.130924285758;
   fDecTF_1[2][2][5] = -0.00648255905033;
   fDecTF_1[2][2][6] = -0.00104307774806;
   fDecTF_1[2][3][0] = -0.115926039843;
   fDecTF_1[2][3][1] = -0.133280772265;
   fDecTF_1[2][3][2] = -0.128712912183;
   fDecTF_1[2][3][3] = 0.488822772529;
   fDecTF_1[2][3][4] = -0.0586259907034;
   fDecTF_1[2][3][5] = -0.00590965011225;
   fDecTF_1[2][3][6] = -0.00149409433741;
   fDecTF_1[2][4][0] = -0.125624987575;
   fDecTF_1[2][4][1] = -0.128957198135;
   fDecTF_1[2][4][2] = -0.130924285758;
   fDecTF_1[2][4][3] = -0.0586259907034;
   fDecTF_1[2][4][4] = 0.496127837859;
   fDecTF_1[2][4][5] = -0.00538048251394;
   fDecTF_1[2][4][6] = 5.69902002868e-05;
   fDecTF_1[2][5][0] = -0.00513465876546;
   fDecTF_1[2][5][1] = -0.00667566806836;
   fDecTF_1[2][5][2] = -0.00648255905033;
   fDecTF_1[2][5][3] = -0.00590965011225;
   fDecTF_1[2][5][4] = -0.00538048251394;
   fDecTF_1[2][5][5] = 0.117905285764;
   fDecTF_1[2][5][6] = 0.00171189141911;
   fDecTF_1[2][6][0] = -0.00131248335458;
   fDecTF_1[2][6][1] = -0.00132433921759;
   fDecTF_1[2][6][2] = -0.00104307774806;
   fDecTF_1[2][6][3] = -0.00149409433741;
   fDecTF_1[2][6][4] = 5.69902002868e-05;
   fDecTF_1[2][6][5] = 0.00171189141911;
   fDecTF_1[2][6][6] = 0.0591671687208;
}

//_______________________________________________________________________
inline void ReadCutsD::Transform_1( std::vector<double>& iv, int cls) const
{
   // Decorrelation transformation
   if (cls < 0 || cls > 2) {
       if (2 > 1 ) cls = 2;
       else cls = 2;
   }

   // define the indices of the variables which are transformed by this transformation
   std::vector<int> indicesGet;
   std::vector<int> indicesPut;

   indicesGet.push_back( 0);
   indicesGet.push_back( 1);
   indicesGet.push_back( 2);
   indicesGet.push_back( 3);
   indicesGet.push_back( 4);
   indicesGet.push_back( 5);
   indicesGet.push_back( 6);
   indicesPut.push_back( 0);
   indicesPut.push_back( 1);
   indicesPut.push_back( 2);
   indicesPut.push_back( 3);
   indicesPut.push_back( 4);
   indicesPut.push_back( 5);
   indicesPut.push_back( 6);

   std::vector<double> tv;
   for (int i=0; i<7;i++) {
      double v = 0;
      for (int j=0; j<7; j++)
         v += iv[indicesGet.at(j)] * fDecTF_1[cls][i][j];
      tv.push_back(v);
   }
   for (int i=0; i<7;i++) iv[indicesPut.at(i)] = tv[i];
}

//_______________________________________________________________________
inline void ReadCutsD::InitTransform()
{
   InitTransform_1();
}

//_______________________________________________________________________
inline void ReadCutsD::Transform( std::vector<double>& iv, int sigOrBgd ) const
{
   Transform_1( iv, sigOrBgd );
}
