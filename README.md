python scrape_amazon.py
.venv\Scripts\activate
deactivate


python -m venv venv

python scrape_myntra.py



echo "# Dressify" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/miday-vishalkeshari/Dressify.git
git push -u origin main





============================================================================================================================================================
to count number of lines of code:

Get-ChildItem -Recurse -Include *.kt,*.java,*.xml | Get-Content | Measure-Object -Line