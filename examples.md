# Examples

## Help

``` bash
# run -h for usage
vc -h

# run help on commands (add/commit/...)
vc commit -h
```

## Init and first commits

``` bash
vc init -v v1

vc add -p test1.c

# commit can be run with --dry-run in order to see results
vc commit -m "message" -v v1 --dry-run
vc commit -m "message" -v v1
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

# run dry-run before comiting 
vc commit -m "update return" -v v1 v2
```


Now we can checkout between v1 and v2 - the file will update

``` bash
vc checkout v1
vc checkout v2
```

## Diff

``` bash
vc diff -f v1 -t v2 -p main.c
```

## Stash

Do some changes to the file but then checkout another verison, changes will be stashed. The stash can be applied with stash id

``` bash
vc stash --list
vc stash --apply stash_id
```
