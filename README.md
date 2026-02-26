## 🌿Testing using coverage

- Running tests using `coverage` and excluding `venv` directory

```bash
 coverage run --omit='*/venv/*' manage.py test
```

- Return a HTML results of the test:

```bash
coverage html
```

this creates a `htmlcov` directory containing the `index.html` as a result for the tests.

- Accessing `coverage` HTML output (linux):

```bash
# in root dir
cd htmlcov && explorer.exe index.html
```
