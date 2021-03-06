// Class: ReadLD
// Automatically generated by MethodBase::MakeClass
//

/* configuration options =====================================================

#GEN -*-*-*-*-*-*-*-*-*-*-*- general info -*-*-*-*-*-*-*-*-*-*-*-

Method         : LD::LD
TMVA Release   : 4.1.4         [262404]
ROOT Release   : 5.34/05       [336389]
Creator        : jbochenek
Date           : Sun May  5 11:08:05 2013
Host           : Linux ubuntu 3.2.0-39-generic #62-Ubuntu SMP Wed Feb 27 22:05:17 UTC 2013 i686 i686 i386 GNU/Linux
Dir            : /mnt/hgfs/work/HZZ4l_2013/tmva
Training events: 4531
Analysis type  : [Classification]


#OPT -*-*-*-*-*-*-*-*-*-*-*-*- options -*-*-*-*-*-*-*-*-*-*-*-*-

# Set by User:
V: "False" [Verbose output (short form of "VerbosityLevel" below - overrides the latter one)]
VarTransform: "None" [List of variable transformations performed before training, e.g., "D_Background,P_Signal,G,N_AllClasses" for: "Decorrelation, PCA-transformation, Gaussianisation, Normalisation, each for the given class of events ('AllClasses' denotes all events of all classes, if no class indication is given, 'All' is assumed)"]
H: "True" [Print method-specific help message]
CreateMVAPdfs: "True" [Create PDFs for classifier outputs (signal and background)]
# Default:
VerbosityLevel: "Default" [Verbosity level]
IgnoreNegWeightsInTraining: "False" [Events with negative weights are ignored in the training (but are included for testing and performance evaluation)]
##


#VAR -*-*-*-*-*-*-*-*-*-*-*-* variables *-*-*-*-*-*-*-*-*-*-*-*-

NVar 8
f_angle_phi                   f_angle_phi                   f_angle_phi                   f_angle_phi                                                     'F'    [-3.14075922966,3.14134144783]
f_angle_phistar1              f_angle_phistar1              f_angle_phistar1              f_angle_phistar1                                                'F'    [-3.13764119148,3.1392698288]
f_angle_costhetastar          f_angle_costhetastar          f_angle_costhetastar          f_angle_costhetastar                                            'F'    [-0.999878108501,0.999902367592]
f_angle_costheta1             f_angle_costheta1             f_angle_costheta1             f_angle_costheta1                                               'F'    [-0.999634683132,0.999896764755]
f_angle_costheta2             f_angle_costheta2             f_angle_costheta2             f_angle_costheta2                                               'F'    [-0.999993145466,0.999796390533]
f_pt4l                        f_pt4l                        f_pt4l                        f_pt4l                                                          'F'    [1.03734540939,735.01965332]
f_massjj                      f_massjj                      f_massjj                      f_massjj                                                        'F'    [21.865064621,1646.53356934]
f_deltajj                     f_deltajj                     f_deltajj                     f_deltajj                                                       'F'    [0.000423192977905,6.7660369873]
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

class ReadLD : public IClassifierReader {

 public:

   // constructor
   ReadLD( std::vector<std::string>& theInputVars ) 
      : IClassifierReader(),
        fClassName( "ReadLD" ),
        fNvars( 8 ),
        fIsNormalised( false )
   {      
      // the training input variables
      const char* inputVars[] = { "f_angle_phi", "f_angle_phistar1", "f_angle_costhetastar", "f_angle_costheta1", "f_angle_costheta2", "f_pt4l", "f_massjj", "f_deltajj" };

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
      fVmin[0] = -3.14075922966003;
      fVmax[0] = 3.1413414478302;
      fVmin[1] = -3.13764119148254;
      fVmax[1] = 3.13926982879639;
      fVmin[2] = -0.999878108501434;
      fVmax[2] = 0.999902367591858;
      fVmin[3] = -0.999634683132172;
      fVmax[3] = 0.999896764755249;
      fVmin[4] = -0.999993145465851;
      fVmax[4] = 0.999796390533447;
      fVmin[5] = 1.03734540939331;
      fVmax[5] = 735.019653320312;
      fVmin[6] = 21.8650646209717;
      fVmax[6] = 1646.53356933594;
      fVmin[7] = 0.000423192977905273;
      fVmax[7] = 6.76603698730469;

      // initialize input variable types
      fType[0] = 'F';
      fType[1] = 'F';
      fType[2] = 'F';
      fType[3] = 'F';
      fType[4] = 'F';
      fType[5] = 'F';
      fType[6] = 'F';
      fType[7] = 'F';

      // initialize constants
      Initialize();

   }

   // destructor
   virtual ~ReadLD() {
      Clear(); // method-specific
   }

   // the classifier response
   // "inputValues" is a vector of input values in the same order as the 
   // variables given to the constructor
   double GetMvaValue( const std::vector<double>& inputValues ) const;

 private:

   // method-specific destructor
   void Clear();

   // common member variables
   const char* fClassName;

   const size_t fNvars;
   size_t GetNvar()           const { return fNvars; }
   char   GetType( int ivar ) const { return fType[ivar]; }

   // normalisation of input variables
   const bool fIsNormalised;
   bool IsNormalised() const { return fIsNormalised; }
   double fVmin[8];
   double fVmax[8];
   double NormVariable( double x, double xmin, double xmax ) const {
      // normalise to output range: [-1, 1]
      return 2*(x - xmin)/(xmax - xmin) - 1.0;
   }

   // type of input variable: 'F' or 'I'
   char   fType[8];

   // initialize internal variables
   void Initialize();
   double GetMvaValue__( const std::vector<double>& inputValues ) const;

   // private members (method specific)
   std::vector<double> fLDCoefficients;
};

inline void ReadLD::Initialize() 
{
   fLDCoefficients.push_back( 0.00042334019711 );
   fLDCoefficients.push_back( 0.000193428544296 );
   fLDCoefficients.push_back( 1.13707146174e-05 );
   fLDCoefficients.push_back( 0.00027260557614 );
   fLDCoefficients.push_back( -9.45353497708e-05 );
   fLDCoefficients.push_back( 0.000680272931258 );
   fLDCoefficients.push_back( -1.0791552209e-06 );
   fLDCoefficients.push_back( 4.99787262479e-06 );
   fLDCoefficients.push_back( -0.0010604090611 );

   // sanity check
   if (fLDCoefficients.size() != fNvars+1) {
      std::cout << "Problem in class \"" << fClassName << "\"::Initialize: mismatch in number of input values"
                << fLDCoefficients.size() << " != " << fNvars+1 << std::endl;
      fStatusIsClean = false;
   }         
}

inline double ReadLD::GetMvaValue__( const std::vector<double>& inputValues ) const
{
   double retval = fLDCoefficients[0];
   for (size_t ivar = 1; ivar < fNvars+1; ivar++) {
      retval += fLDCoefficients[ivar]*inputValues[ivar-1];
   }

   return retval;
}

// Clean up
inline void ReadLD::Clear() 
{
   // clear coefficients
   fLDCoefficients.clear(); 
}
   inline double ReadLD::GetMvaValue( const std::vector<double>& inputValues ) const
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
            retval = GetMvaValue__( iV );
         }
         else {
            retval = GetMvaValue__( inputValues );
         }
      }

      return retval;
   }
