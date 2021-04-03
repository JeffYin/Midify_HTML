# Create a Python Virtual Environment
virtualenv virenv

# Start the virtual env
virenv/Scripts/activate.bat

# Install the dependencies. Beautifulsoup4 is the only dependency. 
pip3 install -r requirement.txt

# Execute. It automatically search the HTML files recursevily. 
python trimHtml.py




