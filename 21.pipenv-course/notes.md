Source: [https://www.youtube.com/watch?v=6Qmnh5C4Pmo]

1. `python --version` gives the python version in terminal. If you are using python 3 then you have to use `python3 --version`

2. Install pipenv using `pip3 install pipenv` in vscode terminal

3. `pip3 freeze` shows everything which we have in my current virtual environment which is the global environment.

4. Now, `pipenv shell` creates a Pipfile and the virtual environment. This Pipfile is similar to package.json in node js.

5. Now, `python --version` will give the python version of its virtual environment.

6. `exit` will exit the virtual environment.

7. So, again write `pipenv shell` to activate the virtual environment.

8. Install the camelcase package as `pipenv install camelcase` as an example. Now, check the pipfile and "camelcase = "*" shows the latest version of package camelcase.

you can run example.py using `python example.py`

9. To list all the packages, you can use `pipenv graph`

10. To uninstall a package, you can use `pipenv uninstall camelcase`

11. To install dev packages for development not production, use command `pipenv install nose --dev`. Now, check the pipfile.

12. To install packages from requirements.txt file of the same directory, use `pipenv install -r ./requirements.txt` and now check the pipfile again.
 
13. For security and vulnerabilities of packages, use `pipenv check` or `pipenv audit`

14. If you have changed any version of packages in pipfile then use `pipenv install` to update the packages.


15. To show dependency of packages, use `pipenv graph`

16. To deploy on server use pipfile.lock and ignore pipfile, for this first prepare pipfile.lock using `pipenv lock` and then use `pipenv install --ignore-pipfile`

17. exit the virtual environment using `exit` and then type `pipenv run python example.py` to use python version of virtual environment and you can verify by running `pipenv run python` first and then in python interpreter type `import sys` and then `sys.executable` and type `quit()` to exit from python interpreter.

18. You can see the location of virtual environment using `pipenv --venv` and now delete all the virtual environments using `rm -rf /Users/ankit/.local/share/virtualenvs/*` if the location is `/Users/ankit/.local/share/virtualenvs/`

19. To run tests, run the command: `pipenv run pytest .`