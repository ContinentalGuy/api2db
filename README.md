# api2db
Cloud Foundry connector to SAP HANA DB.
Ready to deploy scripts.

### **Steps**:
+ Download cf plugin from this page: https://github.com/cloudfoundry/cli#downloadsInformation
+ Log into ***CloudFoundry*** service through command line.
  ```bash
  cf login
  ```
+ Create trial account in ***CloudFoundry*** environment. Copy API endpoint from top of the page.
+ Insert your API endpoint, email and password.
  ```bash
  API endpoint: https://api.cf.eu10.hana.ondemand.com
  
  Email> bla.blabla@bla.com
  
  Password> *secret*
  Authenticating...
  OK

  Targeted org XXXXXXXX_trial

  Targeted space dev



  API endpoint:   https://api.cf.eu10.hana.ondemand.com (API version: 2.101.0)
  User:           bla.blabla@bla.com
  Org:            XXXXXXXX_trial
  Space:          dev
  ```
+ Go to directory with this project.
  ```bash
  cd ./api2db
  ```
+ Push created project up to the clouds.
  ```bash
  cf push
  ```
