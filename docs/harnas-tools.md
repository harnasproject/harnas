
## Advanced settings

Harnaś invokes tools from image when checking tasks:

* **init** -- is invoked once for each submission. The submission files are placed in `/test/submission` (tars and zips are unpacked). By convention, the script should create executable file `/test/runsolution` which will execute the solution. If this script returns 1, submission will be marked as failed with status "compilation error".
* **run** -- is invoked for each test. Parameters: `$(testname)`.

With standard Harnaś images there is a set scripts called 'haranas-tools' provided. Example usage:

* init: `harnas-compile --allowed-languages=c,cpp,pascal $(solutiondir)`.
* run: `harnas-run --memlimit 256 --timelimit 2 --input $(testname).in --expected $(testname).out --checker harnas-diff -c--compare-floats`
