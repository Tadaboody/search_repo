# Search Repo 
### Finds the most relevant repo in the command line

### Usage
```bash
$ search_repo cppcoro
git@github.com:lewissbaker/cppcoro
$ git clone (search_repo cppcoro)
Cloning into 'cppcoro'...
remote: Enumerating objects: 15, done.
remote: Counting objects: 100% (15/15), done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 2393 (delta 4), reused 2 (delta 0), pack-reused 2378
Receiving objects: 100% (2393/2393), 838.75 KiB | 1.19 MiB/s, done.
Resolving deltas: 100% (1560/1560), done.
$ cd cppcoro/
$ git remote get-url origin 
git@github.com:lewissbaker/cppcoro
```