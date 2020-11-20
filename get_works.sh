# Create pages path if doesn't exists
WORKS_PATH=works
if [ ! -d "$WORKS_PATH" ]; then
  mkdir -p "$WORKS_PATH"
else
  echo "Skip folder."
fi


download_page () {
  local url=$1
  local i=$2
  echo "Downloading page... #$i: $url"

  wget $1 --directory-prefix=$WORKS_PATH

#  sleep 2  # Wait n seconds
}


FILE_URLS=$1
N=16
i=0
while read URL;
do
    i=$((i + 1))
    download_page "$URL" "$i" &  # Fork process (parallel)
    ((counter=i%N)); ((counter++==0)) && wait  # Wait for N parallel processes to finish
done < $FILE_URLS

echo "Done!"