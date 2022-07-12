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
    * [Build MetaMapLite Directory from SQL/CSV](#mml-to-txt)
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

[contributors-shield]: https://img.shields.io/github/contributors/kpwhri/eye_extractor.svg?style=flat-square

[contributors-url]: https://github.com/kpwhri/eye_extractor/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/kpwhri/eye_extractor.svg?style=flat-square

[forks-url]: https://github.com/kpwhri/eye_extractor/network/members

[stars-shield]: https://img.shields.io/github/stars/kpwhri/eye_extractor.svg?style=flat-square

[stars-url]: https://github.com/kpwhri/eye_extractor/stargazers

[issues-shield]: https://img.shields.io/github/issues/kpwhri/eye_extractor.svg?style=flat-square

[issues-url]: https://github.com/kpwhri/eye_extractor/issues

[license-shield]: https://img.shields.io/github/license/kpwhri/eye_extractor.svg?style=flat-square

[license-url]: https://kpwhri.mit-license.org/

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555

[linkedin-url]: https://www.linkedin.com/company/kaiserpermanentewashingtonresearch
<!-- [product-screenshot]: images/screenshot.png -->
