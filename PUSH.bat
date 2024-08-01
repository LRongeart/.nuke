E:
cd E:\00_GitNuke
git config --global core.autocrlf false
git add .
git commit -m "Adding new items to current repository"
git push --set-upstream origin master -v --force-with-lease
git merge master
pause