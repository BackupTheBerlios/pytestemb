

echo "clean"
rm -R -v ctp/ctp/*.*


echo "create directory"
mkdir ctp/ctp
mkdir ctp/ctp/data
mkdir ctp/ctp/images
mkdir ctp/ctp/wxcustom
echo "copy file"
cp -v  ../src/ctp/*.py ctp/ctp/
cp -v  ../src/ctp/data/*.py ctp/ctp/data
cp -v  ../src/ctp/images/*.png ctp/ctp/images
cp -v  ../src/ctp/wxcustom/*.py ctp/ctp/wxcustom


echo "Version (x.x.x) :"
read version

name_file="ctp-$version.tar.gz" 
echo "Create package : $name_file"

tar -pczf ctp/$name_file ctp/ctp

echo "end"