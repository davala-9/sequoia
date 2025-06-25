[![License: GPL v3](https://img.shields.io/badge/license-GNU%20GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.org/andrewdbate/Sequoia.svg?branch=master)](https://travis-ci.org/andrewdbate/Sequoia)
[![Build Status](https://ci.appveyor.com/api/projects/status/github/andrewdbate/Sequoia?branch=master&svg=true)](https://ci.appveyor.com/project/andrewdbate/sequoia)

# Parallel Reasoning in Sequoia

Sequoia is an ontology reasoner that supports OWL 2 DL ontologies. Sequoia can be used from the command line, through
the Protégé plug-in, or via the OWL API.

Sequoia is free and open-source software that is licensed under the [GNU GPL v3](https://github.com/andrewdbate/Sequoia/blob/master/LICENSE) only.

_Note:_ To compile Sequoia you will need JDK 8 installed. Compiling with Java 9 is not supported at this time.

#### Current Limitations
 * Datatypes are not supported.
 * SWRL rules are not supported.

To build Sequoia, you will need [SBT](https://www.scala-sbt.org/) installed on your system.

The Sequoia reasoner is comprised of multiple subprojects:
 * `reasoner-macros` contains Scala macros used throughout the other subprojects.
 * `reasoner-kernel` contains the implementation of the core algorithm and data structures.
 * `reasoner-owl-api` contains the implementation of the OWL API bindings.
 * `reasoner-cli` contains the implementation of the command-line interface of the reasoner.
 * `reasoner-protege-plugin` contains the implementation of the Protégé plugin.

To compile all subprojects and run all tests in a single command, first clone this repository,
and then from the root directory, type `sbt test`. The tests will take several minutes to complete.

