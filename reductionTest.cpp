#include <omp.h>
#include <iostream>
#include <iostream>
#include <cmath>
#include <fstream>
#include <vector>
#include <iomanip>


using namespace std;

int main()
{
    vector<int> trials; //stores multiple values for "parts to split" so that trials on different sizes can be easily automated
    ofstream outFile("output.csv");
    outFile << "total,parts,sum,aggsum,correct\n";
    trials.push_back(1);
    for(int p = 1; p < 25; p++)
    	trials.push_back(pow(2,p));

    for(int j = 0; j < trials.size(); j++)
    {
        float base = .5f;
        float next = base;
        double correct = 0.0;
        int parts = trials.at(j);
        float * sumArr = new float[parts];
        unsigned int total = 0;

        for(int i = 0; i < parts; i++)
        {
            sumArr[i] = 0.0f;
        }

        for(; next <= 1.0; total++) {
           next = nextafterf(next, 10.0f);
           //std::cout << next << std::endl;
        }

        next = base; //reset next after counting how many values to expect

        for(int i = 0; i < total; i++)
        {
            next = nextafterf(next,10.0);
            sumArr[i % parts] += next;
	    correct += next;
        }

        //BEGIN REDUCTION TEST
        float sum = 0.0f;
        for(int i = 0; i < parts; i++)
        {
            sum += sumArr[i];
        }

        float redSum = 0.0f;
        #pragma omp parallel for reduction(+:redSum)
        for(int i = 0; i < parts; i++){
            redSum += sumArr[i];
        }
	
	outFile << total << "," << parts << "," << setprecision(25) << sum << "," << setprecision(25) << redSum << "," << setprecision(25) << correct << "\n";
        std::cout << parts << ".) Agg Sum: " << setprecision(25) << sum << std::endl;
        std::cout << parts << ".) Red Sum: " << setprecision(25) << redSum << std::endl;

        delete[] sumArr;

    }
    outFile.close();
    return 0;
}

