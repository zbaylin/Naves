echo "Compiling UI files..."
for ui_file in *.ui; do
  pyside2-uic $ui_file -o $(echo $ui_file | awk -F".ui" '{$0=$1}1').py
done &&
echo "$(tput setaf 2)Compiled successfully!" ||
echo "$(tput setaf 1)Error compiling UI files!"
tput setaf 7
echo "Running main program..."
python main.py
echo "$(tput setaf 2)Process killed!"
tput setaf 7
echo "Cleaning Python files..."
for ui_file in *.ui; do
  rm $(echo $ui_file | awk -F".ui" '{$0=$1}1').py
done &&
echo "$(tput setaf 2)Directory cleaned!" ||
echo "$(tput setaf 1)Unable to clean directory!"