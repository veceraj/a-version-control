# Version control

## TODO:

- [x] add
- [ ] add multiple files/directory
- [x] checkout
- [ ] while checkout when files are stages exit with message commit or reset
- [ ] when checking out to new branch - confirm create?
- [ ] delete branch
- [x] mv
- [x] commit
- [x] commit --dry-run
- [ ] commit - add option to commit to all?
- [x] reset
- [x] stash
- [x] apply stash 
- [ ] stash confirm?
- [ ] handle operation types (mv/add/...)
- [x] import of commands from config
- [x] diff + and -
- [ ] update mv to new structure
- [ ] refactor to classes
- [ ] add return types to all functions
- [ ] handle exceptions
- [ ] add tests
- [ ] commit - blocks of code in one loop
 
## Bug Issues

- [x] fix diff for larger files
- [x] fix join/patch indexing
- [x] fix diff for example "c-tutorial-diff-bug"
- [ ] fix joining of commits 
- [ ] fix when diff add file with multiple lines change 
- [x] vc reset should overwrite the file with old log
- [x] fix diff when adding at the end of the file
- [x] when adding same file with updates for the second time, take into account staged
- [ ] when checkout delete files that dont exist