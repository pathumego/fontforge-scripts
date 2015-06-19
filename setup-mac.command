FFPY="/Applications/FontForge.app/Contents/Resources/opt/local/share/fontforge/python"
cd "`dirname "$0"`"
cp -a python/*/*.py $FFPY
osascript -e 'tell application "Terminal" to quit' &
exit