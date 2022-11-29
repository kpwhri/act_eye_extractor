[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div>
  <p>
    <!-- a href="https://github.com/kpwhri/eye_extractor">
      <img src="images/logo.png" alt="Logo">
    </a -->
  </p>

<h3 align="center">ACT EYE EXTRACTOR</h3>

  <p>
    Code for Extracting Eye-related information from Optometry, Ophthalmology, and Surgeries
  </p>
</div>


<!-- TABLE OF CONTENTS -->

## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

## About the Project

Code for Extracting Eye-related information from Optometry, Ophthalmology, and Surgeries.


<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

* Python 3.9+
* pip install .
    * See pyproject.toml for updated dependencies.

### Installation

0. Setup a virtual environment
    ```shell
    python -m venv .venv 
    ```
1. Clone the repo
    ```sh
    git clone https://github.com/kpwhri/eye_extractor.git
    ```
2. Install the package (using pyproject.toml)
    ```sh
    pip install .
    ```

## Usage

`eye_extractor` is designed to construct a CSV file with particular variables. This is completed in two steps:

1. *Extract* data from optometry/ophthalmology reports -> `jsonl` file
2. *Build* a CSV file from the `jsonl` file

The reasons for this two-stage approach is multiple:
* Allow debugging (more info can be included in `jsonl` file)
* Simplify construction of variables which rely on a wide amount of inputs.

### Running Application

Running the application will provide a JSONL file of all extracted variables and a CSV file of final summary values.

For the following to work, you must:
* Install Python 3.10+ (most recent version recommended)
* Install required packages: `pip install requirements.txt`
* Assemble a directory/folder (on the file system) with relevant notes
  * Only optometry, ophthalmology, and cataract surgery notes
  * Other types of notes may produce FPs
  * The note should be in a file labeled something like `1.txt`
  * Metadata associated with the note can be included in the same file as `1.meta`
    * This should be in json format with simple key-value pairs (please include `note_id` and `date`):
      * `{'note_id': 1, 'date': '2022-02-22 00:00:00'}`
  * (Optional) The notes can be pre-sectioned using something like `sectag` into a json file called `1.sect`
* Ensure that the project root (`/src`) is on the PYTHONPATH
  * E.g., `set/export PYTHONPATH=C:\eye_extractor\src`
  * E.g., powershell likes `$env:PYTHONPATH=-C:\eye_extractor\src'`

#### Extract Step

The extract step produces a jsonl file where each line represents all the NLP work on a single note.

Assuming all notes are in the directory: `C:\notes`, and the output info should be in `C:\extract`, run:
```
   python src\eye_extractor\extract.py C:\notes --outdir C:\extract\run0
```

NB: it is best practice to place each run into a separate directory (e.g., the addition of `run0` to the path). 
This will simplify running the extract step.

To speed up processing, one option is to run this across multiple subsets of notes. 
These notes could be placed in different directories, or be split among different filelists. 
A filelist is a file with one file listed per line (full path, including filename). Add a filelist 
to tell a run which files to look for.

```
   python src\eye_extractor\extract.py C:\notes --outdir C:\extract\run1 --filelist C:\filelist1.txt
   python src\eye_extractor\extract.py C:\notes --outdir C:\extract\run1 --filelist C:\filelist2.txt
   python src\eye_extractor\extract.py C:\notes --outdir C:\extract\run1 --filelist C:\filelist3.txt
```

Each run will create a jsonlines file. To merge these together and build separate variables, see the Extract Step.

#### Build Step

The build step produces a CSV file with individual eye-related variables from the jsonlines output of the build step.

1. Ensure that the extract output `jsonl` file(s) are in a single directory (let's assume this is `C:\extract\run1`)
2. Let's suppose we want to output the CSV to `C:\build`
3. `docid`, `studyid`, `date`, `enc_id`, and `train` metadata will be used from the `1.meta` file. To use additional values (e.g., 'department'), add the argument `--add-column department`.
4. Run: `python src\eye_extractor\build_table.py C:\extract\run1 C:\build`
5. The resulting CSV will have a single `note_id`/`docid` per line.
6. You can interpret the output variables by generating a data dictionary from the `output/columns.py` file.


#### Performance Expectations

Every optometry, ophthalmology, and other note types look distinct based on author, location, etc., etc. 
While this algorithm has been tuned to particular sites, it is not guaranteed to perform as well in new environments. 
For this reason, expect to put some effort into fixing variables. One approach might be to look at outputs where all values are missing.


### Tools Exploring Results

To run these commands, the `eye_extractor` package must be installed.
* `cd eye_extractor`
* `pip install .`

#### Build an HTML Report for a Document 

The `eyex-lookup` command will generate an HTML report for a particular document id.
It uses an interactive loop which awaits document ids as input.
This includes information from `jsonl` files, the original text, and the output `csv` file.

    eyex-lookup CORPUS_PATH[, ...] --intermediate-path INTERMEDIATE_PATH --result-path RESULT_PATH

* CORPUS_PATH: 
  * path to directories of notes that were used in running the extract code
  * multiple paths can be listed
  * assumption: documents must have the name `docid.txt`
* INTERMEDIATE_PATH
  * the output _directory_ from the `extract` step
* RESULT_PATH
  * CSV file output by the `build` step


#### Explore the JSONL file only

The `eyex-lookup-jsonl` command returns the `jsonl` text for a particular docid (this is the intermediate output of `extract` step).
In general, it's better to just use the `eyex-lookup` process above.

    eyex-lookup-json INTERMEDIATE_PATH [DOCID]

* INTERMEDIATE_PATH
  * the output _directory_ from the `extract` step
* DOCID (optional)
  * document id

### Building a New Variable

These are the steps for adding a new variable (and the variable is assumed to belong to a particular 'category').

1. Create a new file with the variable name in `src/category/variable.py`
2. Ensure the extract method is included in `extract.py`
   1. More correctly, the `extract.py` usually calls a `src/category/algorithm.py` which then calls `./variable.py`
3. Create a relevant test file: `test/category/test_variable.py`
   1. What to test?
      1. Ensure regular expressions match expected values
      2. Test that the expected json is build from the `extract` step
      3. Test extraction/building in a single step
4. Create a 'builder' function in `src/output/category.py` and ensure this is called by `extract.py`
5. Add the variable to the `columns.py` file.



## Versions

Uses [SEMVER](https://semver.org/).

See https://github.com/kpwhri/eye_extractor/releases.

<!-- ROADMAP -->

## Roadmap

See the [open issues](https://github.com/kpwhri/eye_extractor/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->

## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the MIT License.

See `LICENSE` or https://kpwhri.mit-license.org for more information.



<!-- CONTACT -->

## Contact

Please use the [issue tracker](https://github.com/kpwhri/eye_extractor/issues).


<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/kpwhri/act_eye_extractor.svg?style=flat-square

[contributors-url]: https://github.com/kpwhri/act_eye_extractor/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/kpwhri/act_eye_extractor.svg?style=flat-square

[forks-url]: https://github.com/kpwhri/act_eye_extractor/network/members

[stars-shield]: https://img.shields.io/github/stars/kpwhri/act_eye_extractor.svg?style=flat-square

[stars-url]: https://github.com/kpwhri/act_eye_extractor/stargazers

[issues-shield]: https://img.shields.io/github/issues/kpwhri/act_eye_extractor.svg?style=flat-square

[issues-url]: https://github.com/kpwhri/act_eye_extractor/issues

[license-shield]: https://img.shields.io/github/license/kpwhri/act_eye_extractor.svg?style=flat-square

[license-url]: https://kpwhri.mit-license.org/

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555

[linkedin-url]: https://www.linkedin.com/company/kaiserpermanentewashingtonresearch
<!-- [product-screenshot]: images/screenshot.png -->
