# master_AI_Integration_In_Ur_Application
master_AI_Integration_In_Ur_Application


**Prerequisites:**

* Python installed on your system.
* A Groq license.

**Steps:**

1. **Install Project Dependencies:**

   - Grab the necessary packages with the help of `pip`:
   
     ```bash
     pip install -r requirements.txt
     ```
     
2. **Run Server**

  ```bash

    #start mapping server
    python mapping_server.py

    python server.py
    
    #test
    curl -s http://127.0.0.1:5000/supply-chain-data?query=order_tracking
    
    python dashboard.py
    
  ```



   


