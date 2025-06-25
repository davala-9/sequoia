SOURCES FILESTRUCTURE

1) test-main folder contains the source code of the main testing program. The main testing program does all tests, and it has a variety of options to do several tests. Every option not included is set to default value. The options are:  
@ "-i INPUTFOLDER" for the input folder
@ "-o OUTPUTFOLDER" for the output folder
@ "-h HARNESSESFOLDER" for the harnesses folder
@ "-r REPETITIONS" for the number of repetitions per ontology and reasoner
@ "-y REASONER1 REASONER2 ... " for using only particular reasoners. This requires that individual harnesses are in the HarnessesFolder with the name used in this option.
Other options are ("loadtest" for a load only test, "nohash" to do no hash, "nowrite" to not write taxonomy.)
2) individual-harnesses contains the encapsulated run of the reasoners. Due to the need to do each separately (though I still could create a library that does most and use that in the capsules: TODO) changes in one must be copied to the rest. 
3) copy new reasoners in the lib folders of the individual harnesses


TEST FILESTRUCTURE

1) There should be a root folder, where the test jar is put.
2) Root folder should contain a folder "data/" where all folders with each dataset are.
3) Root folder should contain a folder "harnesses/" where all individual harnesses are, as *.jar, and with the name of the reasoner in lower caps.
4) Root folder should contain a folder "outputs/" where each test output folder will be created. These testoutput folders will in turn contain a folder with taxonomies for each pair of ontology + reasoner, and a file where (possibly, depending on the test options) average times and hashes are written. 

HOW TO DO THE TESTS

-3) Ensure that all new compiled reasoners are in individual harnesses lib files.
-2) Ensure that all individual harnesses are compiled.
-1) Ensure that the test main program is compiled.
0) Ensure that the test filestructure is updated with the last compilations (use command scp davala@krr-linux-2:/home/...) to copy them to the test ground.
1) SSH to server by typing ssh davala@krr-linux-2
2) Same password as clpc265a
3) Go to /home/davala/testing/ (TODO: doublecheck this, this is root folder)
4) Run the command java -jar test-main.jar [options] 
5) Export outputs to this computer with scp, and verify anything you need.