# Statutory-Instrument-Index

[View demo application](https://joe-crawford.github.io/Statutory-Instrument-Index/) [loads ~7MB in browser]

This is a static Angular website that lists UK Statutory Instruments, indexed by the Act that enabled them. Data was scraped from www.legislation.gov.uk and processed with Python scripts in `dataset_index_scripts` directory to build a JSON index.

Angular sources are in `src/`, output from `ng build` for GitHub Pages are in `docs/`.

**Note:** This is intended as a demo of an Angular website, it has not been checked for accuracy.