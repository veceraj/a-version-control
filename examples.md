# Examples

## Help

``` bash
# run -h for usage
vc -h

# run help on commands (add/commit/...)
vc commit -h
```

## Init and first commits

At the moment operations are only available from the root - throws error "Version Control not initialized.".

On initialize .vc folder will be created where a metadata.json object is createad. The metadata structure is described in dataobjects.py.

Difflog file is created after running the Add commmand and is stored inside the logs directory under the .vc folder. At the moment, the difflog files are stored in raw format for debugging but can be encodeed in any format in the future.

``` bash
vc init -v v1

vc add -p test1.c

# commit can be run with --dry-run in order to see results
vc commit -m "message" -v v1 --dry-run
vc commit -m "message" -v v1
```

## Add

There are more ways how we can add files. As mentioned before, this can only be done from the root at the moment.

``` bash

# single file
vc add -p test1.c

# multiple files
vc add -p test1.c dir/test1.c

# the whole directory
vc add -p dir

# all files
vc add -p *

```

## Reset

Stage can be reset and the file will return to last commit value

``` bash
vc add --path test1.c
vc commit -m "message" -v v1 --dry-run
vc reset
```

## New version

``` bash
vc checkout -v v2
```

Make some changes to the file, add and commit them

``` bash
vc add -p test1.c 

vc commit -m "add functions" -v v2
```

## Commiting to multiple versions

Make some changes to v2 and then commit to multiple versions.

The indexes for each line will be recalculated based on previous changes.
``` bash
vc add -p test1.c 

vc commit -m "update return" -v v1 v2 --dry-run

# -all / --all-versions in order to commit to current version and all following versions 
vc commit -m "update return" -all --dry-run

# run dry-run before comiting 
vc commit -m "update return" -v v1 v2
```


Now we can checkout between v1 and v2 - the file will update

``` bash
vc checkout v1
vc checkout v2
```

## Commits and Inverted commits

This version control is currently linear and does not yet support branching. 
There is one thing this version control tries to deal on its own and that is inverting commits to versions it was not specified to commit to. 

In previous example, we were commiting to v1 and v2 (at a moment where both versions were already created). What happens when we dont want to commit to v2? This is handled with help of inverted commits which take the currently commited changes and makes inverse operation for them.

This part can sometimes cause something like "merge conflics". It may be due to bad calculation of line indexes and in some scenarios may be fixed. Its best to run the --dry-run option at all times when dealing with these inverse commits at the moment. 

## Diff

``` bash
vc diff -f v1 -t v2 -p main.c
```

<!-- ## Stash

Do some changes to the file but then checkout another verison, changes will be stashed. The stash can be applied with stash id

``` bash
vc stash --list
vc stash --apply stash_id
``` -->

## Publishing 

Apart from versioning, this program also adds the ability to publish documents. These are at the moment only narrowed down to markdown documents but it could be possible to implement providers for other formats too. 

Let's create a new file tutorial.md with following code.

Filename: tutorial.md

``` md
Nyni si ukazeme, jak by vypadal jednoduchy program odpovidajici na otazku smyslu zivota, vesmiru a tak vubec. Tento program najdeme v adresari "/foo/bar.c" a nas budou zajimat radky 10 az 12.

<snippet path="foo/bar.c" start="10" end="12"/>

Vsimneme si, zejmena radku 11, kde vydime prikaz return...
```

Upon running the publish command it will automaticaly load the code from specified file between lines start and end. Concidered that the file passed as path exists.

``` bash
# now we can publis it

vc publish -p tutorial.md

# or if we want to publish all md files
vc publish -p *
```


#### Ouput

The output will be placed under .output directory (which should ignored by the version control).
After running the publish command. File will be genereted with .output/tutorial.md path and the content will be following:

Filename: .output/tutorial.md

``` md
Nyni si ukazeme, jak by vypadal jednoduchy program odpovidajici na otazku smyslu zivota, vesmiru a tak vubec. Tento program najdeme v adresari "/foo/bar.c" a nas budou zajimat radky 10 az 12.

10: int foo() {
11:   return 42;
12: }

Vsimneme si, zejmena radku 11, kde vydime prikaz return...
```

At the time of writing this example the start and end refere to same lines in all versions at the moment. But I am working on implementing a feature that will update offsets of the read lines.

## Unit testing

This part is currently under work and needs to be implemented.
Currently only one TestScenario is halfway done.

The test create new files and directories and then automatically delete them inside the project.

``` bash
# run unit tests from this project
python run_tests.py
```