:: replace 'E:' by the disk letter on which your Git Folder exists; 
E:
:: replace 'E:\00_GitNuke' by the full disk path to your Git Folder;
cd E:\00_GitTest
git config --global core.autocrlf false
git pull --rebase --autostash
pause