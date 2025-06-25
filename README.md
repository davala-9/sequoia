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

SOURCES FILESTRUCTURE

1) test-main folder contains the source code of the main testing program. The main testing program does all tests, and it has a variety of options to do several tests. Every option not included is set to default value. The options are:  
@ "-i INPUTFOLDER" for the input folder
@ "-o OUTPUTFOLDER" for the output folder
@ "-h HARNESSESFOLDER" for the harnesses folder
@ "-r REPETITIONS" for the number of repetitions per ontology and reasoner
Other options are ("loadtest" for a load only test, "nohash" to do no hash, "nowrite" to not write taxonomy.)
2) individual-harnesses contains the encapsulated run of the reasoners. 


TEST FILESTRUCTURE

1) There should be a root folder, where the test jar is put.
2) Root folder should contain a folder "data/" where all folders with each dataset are.
3) Root folder should contain a folder "harnesses/" where all individual harnesses are, as *.jar, and with the name of the reasoner in lower caps.
4) Root folder should contain a folder "outputs/" where each test output folder will be created. These output folders will in turn contain a folder with taxonomies for each pair of ontology + reasoner, and a file where (possibly, depending on the test options) average times and hashes are written. 

HOW TO DO THE TESTS

1) Ensure that all new compiled reasoners are in individual harnesses lib files.
2) Ensure that all individual harnesses are compiled.
3) Ensure that the test main program is compiled.
4) Ensure that the test filestructure is updated with the last compilations to copy them to the test ground.
5) Run the command java -jar test-main.jar [options] 