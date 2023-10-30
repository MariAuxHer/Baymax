/*
    We will use something similar to the data structure implemented in this file to classify the doctors 
    information based on their specialization and region.
*/

#include <iostream> 
#include <fstream>
#include <map>
#include <vector>
#include <iomanip>

using namespace std; 

struct Doctor { 
    string name; 
    string mailing_address;
};

istream &operator>>(istream &in, Doctor &doctor) {
  in >> doctor.name >> doctor.mailing_address;
  return in;
}

ostream &operator<<(ostream &out, Doctor &doctor) {
  out << "Name: " << setw(20) << left << doctor.name << "Address: " << setw(20) << left << doctor.mailing_address;
  return out;
}

typedef map<string, map<string, vector<Doctor> > > map_doctors_specialization; 
typedef map<string, vector<Doctor> > map_doctors_region;

int main() { 
    ifstream fin("doc.txt"); 
    string specialization; 
    string region; 
    Doctor doctor; 
    map_doctors_specialization doctors_specialization; 
    vector<Doctor> vec_doctors_per_region;
    map_doctors_specialization::iterator it_specialization; 
    map_doctors_region::iterator it_region; 

    if(!fin.is_open()) { 
        cerr << "Can't open the file" << endl;
        return 1;
    }

    while (fin >> specialization >> region >> doctor) { 
        it_specialization = doctors_specialization.find(specialization); 
        if (it_specialization == doctors_specialization.end()) { 
            map_doctors_region doctors_region;
            vector<Doctor> vec_doctors_per_region;
            doctors_region[region] = vec_doctors_per_region; 
            doctors_specialization[specialization] = doctors_region;
            it_specialization = doctors_specialization.find(specialization); 
        }
        else {
            it_region = it_specialization->second.find(region); 
            if (it_region == it_specialization->second.end()) { 
                vector<Doctor> vec_doctors_per_region;
                it_specialization->second[region] = vec_doctors_per_region;
            }
        }
        it_specialization->second[region].push_back(doctor);
    }

    for (it_specialization = doctors_specialization.begin(); it_specialization != doctors_specialization.end(); it_specialization++) { 
        cout << "\n\nSpecialization: " << it_specialization->first << endl;
        for (it_region = it_specialization->second.begin(); it_region != it_specialization->second.end(); it_region++) { 
            cout << "\tRegion: " << it_region->first << endl; 
            cout << "\tProvider's Info: " << endl;
            for (size_t i = 0; i < it_region->second.size(); i++) { 
                cout << "\t\t" << it_region->second[i] << endl;
            }
        }
    }
}