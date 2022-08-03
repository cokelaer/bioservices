rm -rf dist
python setup.py sdist
twine upload --repository testpypi dist/* || exit 1
twine upload dist/*
