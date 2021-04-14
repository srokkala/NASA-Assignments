# FORS/S3VI Coding Exercise
##  Steven Rokkala
## Part 1 (FORS) (Bonus Part Completed)
### Getting Started

```bash
# Go inside the directory
    cd FORS

# Install Dependencies
    npm install

# Start Node server
    node server
    
```

## Walkthrough

1). Now that the Node web server has been started, navigate to `localhost:3000` on your browser to see the table.

2). The node server serves the JSON file from which the displayed table  retreives its data from. I've used the node server to serve the JSON file in order to avoid any Cross-Origin Resource Sharing issues.

3). To help contruct the table, I've used a Javascript library called Tabulator.

4). The table's columns can be sorted and table data can be downloaded in either CSV or Excel format depending on which labeled button below the table is clicked by the user.

5). I've also completed the bonus functionality by allowing users to edit and save fields in the table. 


## Part 2 (S3VI) (Python 3.8.2)
### Getting Started

```bash
# Go inside the directory
    cd S3VI

# Run Default Script To Query All Results from MongoDB
    python3 S3VI.py
```

### Things to Keep in Mind
- I have verified that my script works since I have created a free account on MongoDb. The username is ```user``` and the password is ```1234``` for the sake of easy authenication
- Every time the script is run, the collection is deleted first in order to avoid duplicate results. If the collection doesn't exist, an error message would be displayed to indicate it. This is the reason why the error message is automatically be triggered the first time the script is run. 
- This script connects to my MongoDB account. If you would like to verify the database you can simply uncomment lines 28-35 (labelled as MongoDB Collection Checker). Initially, it will throw an error (as it should) because the collection hasn't been created yet and after running the script a second time, it will display the number of documents in it.

## Example Commands + Walkthrough

1). Running  ```python3 S3VI.py``` will display all results since no arguments are being passed hence the default data type will be ``` "ALL" ```

2). Running ```python3 S3VI.py -h``` will display the help menu displaying optional arguments

3). Running ``` python3 S3VI.py -t "SSC" ``` will display all data from the RSS links

4). Running ``` python3 S3VI.py -t "SSD" ``` will display all data from the JSON file.

5). Running ```python3 S3VI.py --type "SSC" -s "\"Initial Results from the TechnoSat In-Orbit Demonstration\"" ``` will look for results containing the second argument in the title or description

6). Running ```python3 S3VI.py -s "\"Initial Results from the TechnoSat In-Orbit Demonstration\""``` will automatically set data type to "ALL" since the data type argument was not specified and will search for results containing the second argument in the title or description





