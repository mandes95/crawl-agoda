# Big Data For Tourism Statistics : Crawling Agoda

As part of the drive towards innovation and exploiting new sources of data, we are currently analyzing alternative sources of data for accommodation statistics using web scraping technique. Web scraping is defined as an automated procedure of extracting relevant items of information from websites and turning it into structured information that can be used for following analysis.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

List of Requirement for the project:
1. OS Windows 7 or higher.
2. Python 2.7 (Recommended using Anaconda Navigator)
3. Google Chrome Browser with the driver
4. Mozilla Firefox Browser with the driver
5. Python Library (Pandas, Selenium, Joblib)

Script to install the Python Library:
```
conda install pandas
conda install -c conda-forge selenium
conda install -c anaconda joblib
```

### Running The Script & Start The Robots

First step to do is to install the requirement for the project. We recommend to use Anaconda Navigator to install the python environment in the OS Windows.

Next, open the script [agoda_build_directory.py](agoda_build_directory.py) and change the script in the configuration section to match the settings that should be on your computer.
For example :
```
...
firefox_driver_path = 'YOUR DRIVER PATH' #setup the path of gecko driver

city_code = '17193' #agoda city code 17193 for Bali, Indonesia
cIn = '2018-07-08' #set the default check-in date
cOut = '2018-07-09' #set the default check-out date
output_path = "resBALI_"+cIn+".xlsx"
...
```
After that, run the script and wait until the process is complete. The [agoda_build_directory.py](agoda_build_directory.py) will generate accomodation directory as the crawling results from agoda with basic information (links, hotel name, star rating, and score). This directory, will be used to get more information from every hotel page, like remaining rooms available, year opened, etc.

To access every hotel page links that have been available in the crawling directory, we used  the [agoda_parallel_bali.py](agoda_parallel_bali.py). Configure the script first, then run the script in daily basis to capture the information about remaining rooms available everyday. To make it easy, we can configure the task scheduler to run [agoda_parallel_bali.py](agoda_parallel_bali.py) automatically.

Tutorial to setup the task scheduler can be seen on the following page:
https://stackoverflow.com/questions/44727232/scheduling-a-py-file-on-task-scheduler-in-windows-10

Note* :
Stable Internet Access is very necessary in order to make the crawling process run without any obstacle.

## Authors

* **Amanda Pratama Putra**
* **Heny Wulandari**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
